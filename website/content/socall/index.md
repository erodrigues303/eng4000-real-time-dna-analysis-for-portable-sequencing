<p class="eyebrow">Research pillar B</p>

# SoCall Engineering

SoCall is the laboratory's convolutional CTC basecaller, supplied to the project as FP32 weights, under investigation for resource-constrained execution. Int8/fixed-point execution is the project's target, and quantization is project work. SoCall remains **one implementation to develop and optimize**, alongside the broader basecaller benchmark.

> **Current state:** SoCall runs on the Jetson TX2 GPU with reference-scored accuracy on matching-chemistry data: [SOCALL-011](../experiments/SOCALL-011.md) reproduced the laptop pipeline's D5 accuracy at 44% of the 4 kHz full-channel throughput reference. Two exact optimizations are measured: greedy-decode vectorisation (SOCALL-006 to 010) almost doubled TX2 throughput, and folding BatchNorm into the convolutions (SOCALL-013, SOCALL-015) added about 4% with the same accuracy. FP16 through PyTorch passed the accuracy budget on D5 but ran slower than FP32 (SOCALL-014, SOCALL-016). A TensorRT FP16 engine built from the folded model reaches the 4 kHz real-time rate on D1 (SOCALL-019, 99.98% of 2.048 M samples/s, 2.12× the control) and passes the FP16 accuracy budget on D5 (SOCALL-021), where FAST5 reading and normalization keep the whole pipeline at 89% of real time. Private source, weights and engines are not published here.

## Architecture and implementation

SoCall is a fully convolutional 1D CNN with a CTC head and 446,893 parameters: five convolution blocks (Conv1d, BatchNorm, ReLU) with kernels 9, 13, 27, 25 and 9, then a 1×1 decoder to log-probabilities over blank/A/C/G/T. The first convolution has stride 3, so the model emits one output step per 3 signal samples, and each step sees 219 input samples. That works out to about 148,600 multiply-adds per input sample; the 104→80, kernel-27 layer is roughly half of it, which makes it the first target for profiling and compression. At 4 kHz, real time for 512 channels needs about 609 GFLOP/s, against a TX2 GPU peak of about 666 GFLOP/s in FP32 and 1.33 TFLOP/s in FP16, which is why FP16 is the main optimization path.

The model was supplied as FP32 weights with no preprocessing, decoder or training code. The project supplies the rest: per-read median/MAD normalization, 4,800-sample chunking, greedy and beam-search CTC decoding, and reference scoring. Training data and normalization were not documented, so these follow the supervisor's recollection and are checked against D5 accuracy. Full details are in the [model record](../models/socall-private.md); source code and weights are not published.

## Correctness and verification

Output changes are checked in three ways. Exact changes within one runtime must reproduce the baseline FASTQ byte for byte (SHA-256 of the whole file); the decoder variants below were checked this way against [SOCALL-004](../experiments/SOCALL-004.md). Exact changes that move the same FP32 math to another runtime (ONNX Runtime, TensorRT, CUDA vs Apple MPS) can't meet that rule, because two runtimes round FP32 differently and an argmax between two labels tied to about 1e-7 can go either way. For those, log-probabilities must agree within 1e-4, sequences may differ only at near-ties (top two labels within 2e-4), and D5 median identity and mapped fraction must stay unchanged at two decimals. Changes that move between platforms or numeric formats are scored against the D5 reference genome with the shared [reference-accuracy method](../benchmarking/d5-accuracy.md) and compared read by read. On D5, the TX2 output ([SOCALL-011](../experiments/SOCALL-011.md)) and the Apple M2 output ([SOCALL-001](../experiments/SOCALL-001.md)) agree in mapped fraction (97.31%) and median identity (79.39% vs 79.38%). Most reads differ only in their last few bases because the two wrappers handle the final chunk differently, and 64 reads differ mid-read by a few bases for a reason not yet verified. Fixed-point scaling and saturation checks wait for the quantized variants.

## Baseline characterization

**Preliminary TX2 baseline (D1, FP32, unchanged model):** [SOCALL-004](../experiments/SOCALL-004.md) ran the supplied model and weights on the reflashed [Jetson TX2 (JetPack 4.6.6)](../systems/jetson-tx2-jp466.md) GPU with the supervisor's chunking (4800 samples, no overlap, batch 64) and greedy decoding. Four repeated runs gave 0.509 M samples/s (SD 0.002), about 25% of the 2.05 M samples/s needed for 512 channels at 4 kHz and 20% of 2.56 M samples/s at 5 kHz. Rep4 averaged 8.5 W module input (5.2 W above idle). The same model on the TX2 CPU ([SOCALL-005](../experiments/SOCALL-005.md), 5-read subset) ran at 0.002 M samples/s. [SOCALL-003](../experiments/SOCALL-003.md) repeats the GPU run with 300-sample overlap (0.49 M samples/s).

These are throughput and power results only. D1 is R10.4.1 at 5 kHz, while SoCall was trained on R9.4.1 at about 4 kHz, so no accuracy is claimed for these runs; [SOCALL-001/002](../experiments/SOCALL-001.md) provide the matching-chemistry accuracy reference on D5.

**TX2 baseline on D5 (matching chemistry):** [SOCALL-011](../experiments/SOCALL-011.md) ran all 4,467 D5 reads on the TX2 GPU with the GPU-side exact greedy decoder from [SOCALL-010](../experiments/SOCALL-010.md), reading FAST5 inside the timed pass. It reached 0.906 M samples/s, 44.2% of the 2.048 M samples/s needed for 512 channels at 4 kHz, at 12.2 W average module input (8.9 W above idle) and 86% GPU utilisation. Median mapped-read identity was 79.39% with 97.31% of reads mapped, matching SOCALL-001. This is one timed pass on one board, with greedy decoding only. [BLITZ-009](../experiments/BLITZ-009.md) is a DeepNano-Blitz CPU reference on the earlier TX2 image, not a SoCall baseline.

## D5 reference-accuracy comparison

[DeepNano-Blitz vs SoCall: Reference Accuracy on D5](../benchmarking/d5-accuracy.md) compares the saved SOCALL-001/002 outputs with the retained BLITZ-007 run-1 output, scored as BLITZ-010. All three have the same 4,467 read IDs and reference/scoring method. Blitz median mapped-read identity was 88.09%, versus 79.38% (SoCall greedy) and 81.00% (SoCall beam 5). These preliminary pipeline-output results do not rank hardware performance or establish the cause of the accuracy gap.

## Profiling and bottlenecks

Stage timing in SOCALL-004 (CUDA-synchronized at each boundary) attributes 48.9% of wall time to model inference and 47.3% to greedy CTC decoding, with normalization, stitching and host-device transfers together under 4%. GPU utilisation averaged 44%. Decoding cost here belongs to the benchmark wrapper (a per-base Python loop on the ARM CPU), not to the SoCall model. Inference alone corresponds to about 1.0 M samples/s, so FP32 inference by itself is also below the real-time target. This is a first profile, not a complete bottleneck analysis: per-kernel GPU profiling, memory movement and synchronization are not yet measured.

After the decoder change below, inference is 92.5% of wall time on D1 ([SOCALL-010](../experiments/SOCALL-010.md)) and 87.4% on D5 ([SOCALL-011](../experiments/SOCALL-011.md)), where FAST5 reading (4.4%) and normalization (4.0%) come next. FP32 inference alone corresponds to about 1.04 M samples/s, roughly half the 4 kHz target, so the model's arithmetic is now the bottleneck. Folding and FP16 did not change this split: inference stays at 92 to 94% of wall time on D1 (SOCALL-012 to 014). The TensorRT FP16 engine changes it: inference falls to 84.1% on D1 ([SOCALL-019](../experiments/SOCALL-019.md)) and 76.1% on D5 ([SOCALL-021](../experiments/SOCALL-021.md)), and normalization (8.5% and 8.1%) and FAST5 reading (7.4% on D5) are now the next stages to work on.

## Optimization studies

### Greedy-decode vectorisation (TX2, D1)

SOCALL-004's profile put half the wall time in greedy CTC decoding, a per-base Python loop on the ARM CPU. Four replacements were run in one session, round-robin, three process runs each, against an unchanged same-session control. Exact variants had to reproduce SOCALL-004's FASTQ byte for byte.

| Record | Decoder | Mean samples/s | vs control | Output vs SOCALL-004 |
|---|---|---:|---:|---|
| [SOCALL-006](../experiments/SOCALL-006.md) | Per-base Python loop (control) | 507,518 | 1.00× | Identical |
| [SOCALL-007](../experiments/SOCALL-007.md) | Vectorised on CPU, float32 quality math | 939,502 | 1.85× | Same sequences, 2 quality characters differ |
| [SOCALL-008](../experiments/SOCALL-008.md) | Argmax on GPU, float32 quality math | 966,791 | 1.91× | Same sequences, 2 quality characters differ |
| [SOCALL-009](../experiments/SOCALL-009.md) | Vectorised on CPU, float64 quality math | 946,386 | 1.86× | Identical |
| [SOCALL-010](../experiments/SOCALL-010.md) | Argmax on GPU, float64 quality math | 964,273 | 1.90× | Identical |

The float32 variants computed the quality score's log10 in single precision, which moved 2 of 1,434,692 quality characters by one Phred step; computing it in float64 made the GPU-side decoder exact at the same speed. SOCALL-010's decoder is the default for later TX2 runs. Decoding is now 1 to 2% of wall time.

### BatchNorm folding and FP16 (TX2, D1 and D5)

Inference was about 92% of wall time after the decoder change, so the next studies changed the network itself. Folding replaces each convolution and the BatchNorm after it with one convolution whose weights and bias already include the normalization (computed in float64 from the stored statistics, epsilon 1e-3). It is exact up to FP32 rounding and removes five layers. The FP16 variant runs the folded model in half precision and keeps the final log-softmax in FP32. On the Apple M2, FP16 changed full-D5 median identity by −0.007 points (greedy) and +0.001 points (beam 5), well inside the 0.1-point budget. Both variants were then measured on the TX2: D1 in one session, three process runs each, round-robin against an unchanged control, and all of D5 once per variant.

| Record | Model | Data | Mean samples/s | vs control | Output |
|---|---|---|---:|---:|---|
| [SOCALL-012](../experiments/SOCALL-012.md) | FP32, unchanged (control) | D1 | 964,038 | 1.00× | Identical to SOCALL-004 |
| [SOCALL-013](../experiments/SOCALL-013.md) | BatchNorm folded, FP32 | D1 | 997,182 | 1.034× | Same sequences on all 59 reads |
| [SOCALL-014](../experiments/SOCALL-014.md) | Folded, FP16 (PyTorch) | D1 | 841,616 | 0.873× | Accuracy checked on D5 |
| [SOCALL-015](../experiments/SOCALL-015.md) | BatchNorm folded, FP32 | D5 | 944,755 | 1.043× SOCALL-011 | 79.39% median identity, 97.31% mapped (same as SOCALL-011) |
| [SOCALL-016](../experiments/SOCALL-016.md) | Folded, FP16 (PyTorch) | D5 | 807,280 | 0.891× SOCALL-011 | 79.38% median identity, 97.38% mapped |

Folding is a small exact gain and becomes the base model for later variants. FP16 kept accuracy on the TX2's own GPU (0.010 points below SOCALL-011) but was 15% slower than folded FP32, while the same FP16 model is 2.6× faster than FP32 on the M2. The likely reason is that PyTorch 1.10 runs these FP16 convolutions with FP32 accumulation, which doesn't use the Pascal GPU's double-rate half2 arithmetic; this is not verified. An inference-only check in the same session gave the same ordering (1.050, 1.088 and 0.892 M samples/s for the control, folded FP32 and FP16). TensorRT 8.2 on this board reports fast FP16 and no fast int8, so the next study builds TensorRT engines from an ONNX export of the folded model.

Across backends, exact ties at FP32 resolution can round either way: 75 of 4,467 D5 reads differ between SOCALL-015 and SOCALL-011, all at steps where the two most likely labels were almost equal, with no change in accuracy.

### TensorRT engines (TX2, D1 and D5)

The folded model was exported to ONNX (opset 13, dynamic batch, 4,800-sample chunks) and built on the board into two TensorRT 8.2 engines with trtexec, one in FP32 and one with FP16 enabled, both for batches of 1 to 64. The engine replaces only the network's forward pass: normalization, chunking, decoding and stitching are the same code as in SOCALL-010. At load time each run checks the engine against the folded FP32 PyTorch model (max abs log-prob difference 2.5e-5 for FP32 and 0.066 for FP16). The FP32 engine is a cross-runtime exact change; the FP16 engine is held to the FP16 budget. D1 was run in one session, three process runs each, round-robin against an unchanged control, then all of D5 once per engine.

| Record | Model | Data | Mean samples/s | vs control | Output |
|---|---|---|---:|---:|---|
| [SOCALL-017](../experiments/SOCALL-017.md) | FP32, unchanged (control) | D1 | 964,608 | 1.00× | Identical to SOCALL-004 |
| [SOCALL-018](../experiments/SOCALL-018.md) | Folded, TensorRT FP32 | D1 | 1,764,090 | 1.829× | Same sequences on 58 of 59 reads |
| [SOCALL-019](../experiments/SOCALL-019.md) | Folded, TensorRT FP16 | D1 | 2,047,572 | 2.123× | Accuracy checked on D5 |
| [SOCALL-020](../experiments/SOCALL-020.md) | Folded, TensorRT FP32 | D5 | 1,553,038 | 1.714× SOCALL-011 | 79.39% median identity, 97.31% mapped (same as SOCALL-011) |
| [SOCALL-021](../experiments/SOCALL-021.md) | Folded, TensorRT FP16 | D5 | 1,820,970 | 2.009× SOCALL-011 | 79.38% median identity, 97.38% mapped |

TensorRT is the first change that cuts the network's own cost by a large factor. The FP32 engine alone gives 1.83× on D1, so most of the gain is already there at full precision (which TensorRT optimization accounts for it was not profiled). FP16 adds another 1.16× and brings D1 to 99.98% of the 4 kHz real-time rate. On D5 the FP16 engine is 0.009 points of median identity below SOCALL-011 and 0.07 points above it in mapped fraction, almost the same as PyTorch FP16 (SOCALL-016), so it passes the budget. The FP32 engine matches SOCALL-011's accuracy exactly; 110 of 4,467 D5 reads differ from folded PyTorch (SOCALL-015), each in a single base, a similar count to the 75 between SOCALL-015 and SOCALL-011. That fits FP32 near-ties, but the steps were not checked one by one. Module power fell from about 11.8 W to 8.8 W (FP32) and 9.4 W (FP16), so gross energy per sample on D1 dropped from 12.2 µJ to 5.0 and 4.6 µJ.

D5 stays below real time (88.9%) because the timed pass includes FAST5 reading and normalization, which TensorRT doesn't touch.

### Next candidates

Normalization on the GPU or vectorised, FAST5 reading overlapped with inference, and batching across reads, since inference is no longer more than 90% of wall time. After that: chunk size and overlap, and int8 for the CPU path, since GPU int8 isn't fast on this board. Each is revalidated against the exact or reference-accuracy check above before its speed is reported.

## Shared scientific foundation

[Measurement protocol](../docs/methodology.md) · [Reproduction and access](../resources/reproduce.md) · [Model catalogue](../models/index.md) · [Evidence gaps](../docs/gaps.md)
