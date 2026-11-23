<p class="eyebrow">Research pillar B</p>

# SoCall Engineering

SoCall is the laboratory's int8/fixed-point basecaller implementation under investigation for resource-constrained execution. It remains **one implementation to develop and optimize**, alongside the broader basecaller benchmark.

> **Current state:** access to model and weights has been reported. A preliminary TX2 throughput/power baseline and first stage profile now exist (SOCALL-003-005); embedded correctness on matching-chemistry data and measured optimizations are not yet established. Private source and weights are not published here.

## Architecture and implementation

The [canonical model record](../models/socall-private.md) separates the reported fixed-point design from unverified architecture, parameter count, precision details and training provenance. Obtain permitted implementation documentation and identify preprocessing, inference and decoding boundaries before making architecture claims.

## Correctness and verification

Next: define trusted outputs and permitted test inputs; check fixed-point scaling, saturation, tensor shapes and sequence/quality validity. Compare output changes by read ID and define reference-based biological evaluation separately. No completed verification suite is claimed.

## Baseline characterization

**Preliminary TX2 baseline (D1, FP32, unchanged model):** [SOCALL-004](../experiments/SOCALL-004.md) ran the supplied model and weights on the reflashed [Jetson TX2 (JetPack 4.6.6)](../systems/jetson-tx2-jp466.md) GPU with the supervisor's chunking (4800 samples, no overlap, batch 64) and greedy decoding. Four repeated runs gave 0.509 M samples/s (SD 0.002), about 25% of the 2.05 M samples/s needed for 512 channels at 4 kHz and 20% of 2.56 M samples/s at 5 kHz. Rep4 averaged 8.5 W module input (5.2 W above idle). The same model on the TX2 CPU ([SOCALL-005](../experiments/SOCALL-005.md), 5-read subset) ran at 0.002 M samples/s. [SOCALL-003](../experiments/SOCALL-003.md) repeats the GPU run with 300-sample overlap (0.49 M samples/s).

These are throughput and power results only. D1 is R10.4.1 at 5 kHz, while SoCall was trained on R9.4.1 at about 4 kHz, so no accuracy is claimed for these runs; [SOCALL-001/002](../experiments/SOCALL-001.md) provide the matching-chemistry accuracy reference on D5. [BLITZ-009](../experiments/BLITZ-009.md) is a DeepNano-Blitz CPU reference on the earlier TX2 image, not a SoCall baseline.

## D5 reference-accuracy comparison

[Blitz vs SoCall on D5](../benchmarking/d5-accuracy.md) compares the saved SOCALL-001/002 outputs with Brian’s BLITZ-007 run 1, scored as BLITZ-010. All three have the same 4,467 read IDs and reference/scoring method. Blitz median mapped-read identity was 88.09%, versus 79.38% (SoCall greedy) and 81.00% (SoCall beam 5). These preliminary pipeline-output results do not rank hardware performance or establish the cause of the accuracy gap.

## Profiling and bottlenecks

Stage timing in SOCALL-004 (CUDA-synchronized at each boundary) attributes 48.9% of wall time to model inference and 47.3% to greedy CTC decoding, with normalization, stitching and host-device transfers together under 4%. GPU utilisation averaged 44%. Decoding cost here belongs to the benchmark wrapper (a per-base Python loop on the ARM CPU), not to the SoCall model. Inference alone corresponds to about 1.0 M samples/s, so FP32 inference by itself is also below the real-time target. This is a first profile, not a complete bottleneck analysis: per-kernel GPU profiling, memory movement and synchronization are not yet measured.

## Optimization studies

Chunk-size, batching, CPU/GPU partitioning and CUDA implementations are candidate investigations. Select them after correctness and profiling, then revalidate outputs and measure throughput, latency, memory and energy. No optimization speedup is claimed.

## Shared scientific foundation

[Measurement protocol](../docs/methodology.md) · [Reproduction and access](../resources/reproduce.md) · [Model catalogue](../models/index.md) · [Evidence gaps](../docs/gaps.md)
