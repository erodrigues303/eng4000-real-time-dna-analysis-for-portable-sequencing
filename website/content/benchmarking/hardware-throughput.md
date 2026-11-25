---
title: "Dorado Cross-Platform Performance"
---

# Dorado Cross-Platform Performance

## Objective

Compare Dorado's runtime and signal throughput across the team's CPU, NVIDIA GPU, and Apple M2 systems. These tests establish initial hardware baselines; they do not measure sustained basecalling performance.

## Experimental Setup

All tests used **Dorado 2.1.2** and the same named dataset, [D1](../datasets/D1.md): a 59-read DeepMod2 POD5 sample from an R10.4.1 / E8.2 / 400 bases/s run. Later inspection counted **27,949,927 signal samples at 5 kHz**. The original runs did not preserve input hashes, so byte-for-byte identity between copies cannot be confirmed.

The basecalling model was [`dna_r10.4.1_e8.2_400bps_hac@v6.0.0`](../models/dorado-hac-v6.md).

| System | Backend | Experiments |
|---|---|---|
| [Ryzen 5 1500X desktop](../systems/eric-1500x.md) | Windows CPU; GTX 1060 3 GB CUDA | [DORADO-001](../experiments/DORADO-001.md), [DORADO-002](../experiments/DORADO-002.md) |
| [RTX 4070 desktop](../systems/matthew-4070.md) | Windows CUDA | [DORADO-003](../experiments/DORADO-003.md), [DORADO-004](../experiments/DORADO-004.md) |
| [Apple M2](../systems/ege-m2.md) | macOS Metal | [DORADO-005](../experiments/DORADO-005.md) |
| [RTX 3070 Mobile laptop](../systems/krish-3070-mobile.md) | Windows CUDA | [DORADO-006](../experiments/DORADO-006.md) |

Dorado selected the model automatically in the initial runs. GPU batch tuning differed by system; the RTX 4070 selected a batch size of **896** and chunk size of **12,288**. The other runs do not have equally complete configuration records. The RTX 4070 modified-base run (DORADO-004) used an additional model and is discussed separately in the [model configuration investigation](dorado-model-configuration.md).

## Results

<!-- evidence:dorado-d1 -->

<!-- evidence:dorado-memory -->

<!-- evidence:dorado-power -->

## Findings

On the same Windows desktop, Dorado's reported basecalling time fell from **4,216.234 s on the Ryzen 5 1500X CPU** to **53.213 s on the GTX 1060**—approximately a **79.2× difference**. The RTX 4070 recorded the shortest basecalling interval at **1.401 s**, but its complete command took approximately **12 s** once setup and tuning were included.

These results show the range of performance observed on the available systems, not a controlled ranking of their hardware. Batch selection, software environments, and the time spent outside basecalling were not measured consistently.

Throughput is also shown relative to a theoretical full-channel MinION input rate of **2,560,000 samples/s** (512 channels × 5,000 samples/s). Exceeding that rate during a short offline basecalling interval does **not** establish that a system can sustain live sequencing. See the [measurement protocol](../docs/methodology.md).

## Limitations

- **Small workload:** D1 contains only 59 reads, with one recorded result per configuration. Startup, model loading, caching, and automatic tuning can distort short-run comparisons.
- **Uneven measurements:** Complete-command timing, environment details, memory scope, and power-measurement boundaries were not captured consistently. The recorded power values cannot be used to derive reliable energy per run from stage times alone.
- **Incomplete provenance:** The original runs lack input hashes and some configuration details. Model architecture, parameter count, and backend numerical precision are not fully verified in the [model record](../models/dorado-hac-v6.md).
- **RTX 3070 Mobile record:** This result is filed as DORADO-006 because DORADO-004 identifies the modified-base test in the experiment registry. An earlier report reused DORADO-004 for the mobile GPU result; its original run card and date remain unavailable.

## Next Steps

Repeat the comparison on a larger, verified R10.4.1 dataset. Preserve input and model hashes, hardware/software settings, and batch configuration. Collect repeated **end-to-end and basecalling-stage times**, consistently scoped memory measurements, and synchronized power data. Use reference-based alignment to assess accuracy alongside speed.

A separate sustained-input test is needed to measure latency and backlog before making claims about real-time sequencing capacity.

## Related Investigations and Evidence

- [Initial Basecaller Setup and Evaluation](initial-basecaller-setup.md)
- [Reproduction guide](../resources/reproduce.md)
