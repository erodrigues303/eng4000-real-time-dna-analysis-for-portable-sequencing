<p class="eyebrow">Research pillar B</p>

# SoCall Engineering

SoCall is the laboratory's int8/fixed-point basecaller implementation under investigation for resource-constrained execution. It remains **one implementation to develop and optimize**, alongside the broader basecaller benchmark.

> **Current state:** access to model and weights has been reported. Correctness, a reproducible performance baseline, profiling and measured optimizations are not yet established. Private source and weights are not published here.

## Architecture and implementation

The [canonical model record](../models/socall-private.md) separates the reported fixed-point design from unverified architecture, parameter count, precision details and training provenance. Obtain permitted implementation documentation and identify preprocessing, inference and decoding boundaries before making architecture claims.

## Correctness and verification

Next: define trusted outputs and permitted test inputs; check fixed-point scaling, saturation, tensor shapes and sequence/quality validity. Compare output changes by read ID and define reference-based biological evaluation separately. No completed verification suite is claimed.

## Baseline characterization

Next: pin code and weights privately, record the [Jetson environment](../systems/jetson-tx2.md), and measure complete-command and stage timings with explicit memory and electrical boundaries. [BLITZ-009](../experiments/BLITZ-009.md) is a DeepNano-Blitz CPU reference, not a SoCall baseline.

## Profiling and bottlenecks

Next: measure preprocessing, chunking, batching, inference, decoding, memory movement and synchronization. No measured SoCall bottleneck has been identified in the supplied evidence.

## Optimization studies

Chunk-size, batching, CPU/GPU partitioning and CUDA implementations are candidate investigations. Select them after correctness and profiling, then revalidate outputs and measure throughput, latency, memory and energy. No optimization speedup is claimed.

## Shared scientific foundation

[Measurement protocol](../docs/methodology.md) · [Reproduction and access](../resources/reproduce.md) · [Model catalogue](../models/index.md) · [Evidence gaps](../docs/gaps.md)
