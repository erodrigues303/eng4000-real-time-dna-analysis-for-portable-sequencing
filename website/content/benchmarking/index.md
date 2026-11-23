---
title: Basecaller Benchmarking
---
<p class="eyebrow">Living technical record · Preliminary measurements</p>

# Basecaller Benchmarking

The team has established Dorado platform baselines, compared model tiers, assessed Bonito compatibility, measured DeepNano-Blitz on desktop and embedded CPUs, and explored signal-format pipelines. Work progresses toward reproducible benchmarking and a separately verified embedded SoCall baseline.

## Technical Investigations

Newest work first, following the team's supplied investigation sequence. This is the order of technical work, not publication dates; exact dates appear in report histories only where recorded.

| Investigation | Work completed | Evidence state |
|---|---|---|
| [Blitz vs SoCall: Reference Accuracy on D5](d5-accuracy.md) | Scored 4,467 matching read IDs against one pinned reference; compared distributions and paired identities | Preliminary; saved alignment artifacts verified |
| [POD5 vs BLOW5: Input Pipeline and Command Overhead](pipeline-overhead.md) | Compared stage/command time, memory and reported energy | Exploratory; models and outputs differ |
| [DeepNano-Blitz on Jetson TX2: ARM64 CPU Baseline](embedded-feasibility.md) | Ran the port, swept threads and collected module-input telemetry | Preliminary; sensor scale unverified |
| [DeepNano-Blitz CPU Scaling and Package Energy](cpu-parallelism.md) | Established CPU baselines, thread scaling, larger-workload timing and energy sessions | Preliminary; raw artifacts incomplete |
| [Bonito Compatibility Assessment for Jetson TX2](bonito-compatibility.md) | Reviewed dependencies and excluded the reviewed configuration from TX2 execution | Source review; no measured run |
| [Dorado Fast vs HAC: Performance and Accuracy Tradeoffs](fast-vs-hac.md) | Compared runtime and reported quality on real/simulated input | Exploratory; empirical accuracy unresolved |
| [Dorado GPU Acceleration: CPU and CUDA Baselines](gpu-acceleration.md) | Compared CPU/CUDA execution and modified-base overhead | Preliminary; short stage intervals |
| [Dorado Cross-Platform Performance](hardware-throughput.md) | Established Windows CPU/CUDA and macOS Metal observations | Preliminary; systems/settings differ |

## Cross-investigation reference

[Basecaller Runtime Comparison and Measurement Coverage](runtime-overview.md) collects reported runtimes for Dorado, Blitz and Slorado by workload and timing boundary. Bonito, Coral and SoCall are explicitly marked as unmeasured. This maintained synthesis is not another dated experiment or a cross-tool leaderboard.

[Experiment registry](../experiments/index.md) · [Measurement protocol](../docs/methodology.md) · [Reproduction guide](../resources/reproduce.md) · [SoCall engineering](../socall/index.md)
