<p class="eyebrow">Research pillar B</p>

# SoCall Engineering

SoCall is the laboratory's convolutional CTC basecaller, supplied to the project as FP32 weights, under investigation for resource-constrained execution. Int8/fixed-point execution is the project's target, and quantization is project work. SoCall remains **one implementation to develop and optimize**, alongside the broader basecaller benchmark.

> **Current state:** SoCall runs on the Jetson TX2 GPU (FP32) with reference-scored accuracy on matching-chemistry data: [SOCALL-011](../experiments/SOCALL-011.md) reproduced the laptop pipeline's D5 accuracy at 44% of the 4 kHz full-channel throughput reference. A first measured optimization (greedy-decode vectorisation, SOCALL-006 to 010) almost doubled TX2 throughput with byte-identical output. Inference now dominates, and real time is not yet reached. Private source and weights are not published here.

## Architecture and implementation

The [canonical model record](../models/socall-private.md) separates the reported fixed-point design from unverified architecture, parameter count, precision details and training provenance. Obtain permitted implementation documentation and identify preprocessing, inference and decoding boundaries before making architecture claims.

## Correctness and verification

Output changes are checked two ways. Changes meant to be exact must reproduce the baseline FASTQ byte for byte (SHA-256 of the whole file); the decoder variants below were checked this way against [SOCALL-004](../experiments/SOCALL-004.md). Changes that move between platforms or numeric formats are scored against the D5 reference genome with the shared [reference-accuracy method](../benchmarking/d5-accuracy.md) and compared read by read. On D5, the TX2 output ([SOCALL-011](../experiments/SOCALL-011.md)) and the Apple M2 output ([SOCALL-001](../experiments/SOCALL-001.md)) agree in mapped fraction (97.31%) and median identity (79.39% vs 79.38%). Most reads differ only in their last few bases because the two wrappers handle the final chunk differently, and 64 reads differ mid-read by a few bases for a reason not yet verified. Fixed-point scaling and saturation checks wait for the quantized variants.

## Baseline characterization

**Preliminary TX2 baseline (D1, FP32, unchanged model):** [SOCALL-004](../experiments/SOCALL-004.md) ran the supplied model and weights on the reflashed [Jetson TX2 (JetPack 4.6.6)](../systems/jetson-tx2-jp466.md) GPU with the supervisor's chunking (4800 samples, no overlap, batch 64) and greedy decoding. Four repeated runs gave 0.509 M samples/s (SD 0.002), about 25% of the 2.05 M samples/s needed for 512 channels at 4 kHz and 20% of 2.56 M samples/s at 5 kHz. Rep4 averaged 8.5 W module input (5.2 W above idle). The same model on the TX2 CPU ([SOCALL-005](../experiments/SOCALL-005.md), 5-read subset) ran at 0.002 M samples/s. [SOCALL-003](../experiments/SOCALL-003.md) repeats the GPU run with 300-sample overlap (0.49 M samples/s).

These are throughput and power results only. D1 is R10.4.1 at 5 kHz, while SoCall was trained on R9.4.1 at about 4 kHz, so no accuracy is claimed for these runs; [SOCALL-001/002](../experiments/SOCALL-001.md) provide the matching-chemistry accuracy reference on D5.

**TX2 baseline on D5 (matching chemistry):** [SOCALL-011](../experiments/SOCALL-011.md) ran all 4,467 D5 reads on the TX2 GPU with the GPU-side exact greedy decoder from [SOCALL-010](../experiments/SOCALL-010.md), reading FAST5 inside the timed pass. It reached 0.906 M samples/s, 44.2% of the 2.048 M samples/s needed for 512 channels at 4 kHz, at 12.2 W average module input (8.9 W above idle) and 86% GPU utilisation. Median mapped-read identity was 79.39% with 97.31% of reads mapped, matching SOCALL-001. This is one timed pass on one board, with greedy decoding only. [BLITZ-009](../experiments/BLITZ-009.md) is a DeepNano-Blitz CPU reference on the earlier TX2 image, not a SoCall baseline.

## D5 reference-accuracy comparison

[DeepNano-Blitz vs SoCall: Reference Accuracy on D5](../benchmarking/d5-accuracy.md) compares the saved SOCALL-001/002 outputs with the retained BLITZ-007 run-1 output, scored as BLITZ-010. All three have the same 4,467 read IDs and reference/scoring method. Blitz median mapped-read identity was 88.09%, versus 79.38% (SoCall greedy) and 81.00% (SoCall beam 5). These preliminary pipeline-output results do not rank hardware performance or establish the cause of the accuracy gap.

## Profiling and bottlenecks

Stage timing in SOCALL-004 (CUDA-synchronized at each boundary) attributes 48.9% of wall time to model inference and 47.3% to greedy CTC decoding, with normalization, stitching and host-device transfers together under 4%. GPU utilisation averaged 44%. Decoding cost here belongs to the benchmark wrapper (a per-base Python loop on the ARM CPU), not to the SoCall model. Inference alone corresponds to about 1.0 M samples/s, so FP32 inference by itself is also below the real-time target. This is a first profile, not a complete bottleneck analysis: per-kernel GPU profiling, memory movement and synchronization are not yet measured.

After the decoder change below, inference is 92.5% of wall time on D1 ([SOCALL-010](../experiments/SOCALL-010.md)) and 87.4% on D5 ([SOCALL-011](../experiments/SOCALL-011.md)), where FAST5 reading (4.4%) and normalization (4.0%) come next. FP32 inference alone corresponds to about 1.04 M samples/s, roughly half the 4 kHz target, so the model's arithmetic is now the bottleneck.

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

### Next candidates

With inference dominant, the next studies target the network: folding BatchNorm into the convolutions (exact), then FP16 and a TensorRT engine (accuracy budget 0.1 points of median identity on D5), then int8. Batching across reads, chunk size and overlap, and CPU/GPU overlap remain candidates. Each is revalidated against the exact or reference-accuracy check above before its speed is reported.

## Shared scientific foundation

[Measurement protocol](../docs/methodology.md) · [Reproduction and access](../resources/reproduce.md) · [Model catalogue](../models/index.md) · [Evidence gaps](../docs/gaps.md)
