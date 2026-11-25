---
title: "Initial Basecaller Setup and Evaluation"
---

<p class="eyebrow">Technical investigation · Phase 1</p>

# Initial Basecaller Setup and Evaluation

*September 28 – October 16, 2026*

## Objective

Establish working basecalling pipelines on available hardware, inspect raw-signal inputs and sequence outputs, and identify which existing implementations could support subsequent benchmarking.

## Work Performed

| Basecaller | Version / configuration | Work completed | Outcome |
|---|---|---|---|
| [Dorado](https://github.com/nanoporetech/dorado) | 2.1.2; HAC v6.0.0 | Ran real POD5 input on Windows CPU/CUDA and macOS Metal; inspected BAM output | Executed successfully |
| [DeepNano-Blitz](https://github.com/fmfi-compbio/deepnano-blitz) | `deepnano2` 0.1; network 64, beam 5 | Resolved Linux/WSL build dependencies; processed FAST5 input and compared repeated FASTQ outputs | Executed successfully |
| [Bonito](https://github.com/nanoporetech/bonito) | v1.1.0 reviewed | Examined model configurations, training workflow, decoder and platform requirements | Source review; not executed |
| [DeepNano-Coral](https://github.com/fmfi-compbio/coral-basecaller) | Source reviewed | Examined int8/TensorFlow Lite pipeline, Edge TPU requirements and CPU-test option | Source review; not executed |

Dorado and DeepNano-Blitz established functional signal-to-sequence workflows. Bonito and Coral were reviewed for architecture and compatibility; no benchmark measurements were collected for them.

The Bonito v1.1.0 review found a CUDA CRF path with a Linux x86_64 `ont-koi` wheel and no CPU fallback in that path. This did not establish an executable configuration for the ARM64 TX2. BONITO-001 remained a proposal, and the training-data review did not establish a verified R10.4.1 corpus. [Jetson platform notes](../docs/platforms/jetson-tx2.md) · [Training-data status](../resources/training-data.md)

## Datasets and Models

| Dataset | Source | Recorded characteristics | Use |
|---|---|---|---|
| [D1 — DeepMod2 sample](../datasets/D1.md) | [DeepMod2 v0.3.0](https://github.com/WGLab/DeepMod2/releases/tag/v0.3.0) | 59 POD5 reads; Dorado detected R10.4.1 / E8.2 / 400 bases/s | Dorado functional and initial hardware tests |
| [D4 — DeepNano-Blitz test sample](../datasets/D4.md) | [Blitz `test_sample`](https://github.com/fmfi-compbio/deepnano-blitz/tree/master/test_sample) | 48 FAST5 reads; later inspection found 4,000 Hz historical R9.4-labelled acquisition metadata | Blitz execution and repeatability checks |

**Dorado model:** [`dna_r10.4.1_e8.2_400bps_hac@v6.0.0`](../models/dorado-hac-v6.md), automatically selected/downloaded in the initial runs. The model identifier is distinct from the Dorado 2.1.2 software version. The model's exact parameter count, runtime numerical precision and training-data provenance were not verified in these tests. The `400bps` designation is not a signal sampling frequency.

**Blitz configuration:** supplied network-64 weights, beam size 5, one caller thread and `OMP_NUM_THREADS=1` for the initial functional checks. The network weight-file checksum and full numerical characterization were not archived at this stage.

## Initial Results

### Dorado

All 59 D1 reads were processed successfully. The first GPU and CPU checks produced BAM output containing DNA sequences, quality scores, read IDs and sequencing metadata.

| Experiment | Platform | Reported basecalling duration | Reported throughput |
|---|---|---:|---:|
| [DORADO-001](../experiments/DORADO-001.md) | GTX 1060 3 GB, CUDA | 53.213 s | 525,235 samples/s |
| [DORADO-002](../experiments/DORADO-002.md) | Ryzen 5 1500X, CPU | 4,216.234 s | 6,629 samples/s |

The GPU interval was approximately 79× shorter on this small input. These are recorded tool timings, **not standardized end-to-end or sustained-throughput measurements**. The team subsequently added RTX 4070 and Apple M2 tests; the detailed hardware comparison belongs in [Dorado Cross-Platform Performance](hardware-throughput.md).

An initial PowerShell redirection attempt produced invalid BAM output; using Dorado's `--output-dir` resolved the issue. Dorado also performed automatic model selection and, on the GTX 1060, batch-size tuning.

### DeepNano-Blitz

BLITZ-001 processed all 48 D4 reads on a Ryzen 7 7800X3D CPU under Ubuntu/WSL. A second identical-configuration execution, BLITZ-002, produced a byte-identical FASTQ file. Both checks are documented in the weekly log and lack standalone registry configurations. [Evidence register](../docs/sources.md#website-audit-2026-11-20)

Against the supplied `expected.fastq`, 34 generated sequences matched expected prefixes; the other 14 required 1–6 edits under the recorded comparison with trailing extensions unpenalized. The cause of these differences remains unresolved. **This was a functional/output-consistency check, not reference-based biological accuracy evaluation.**

The initial Blitz runs did not record full-command runtime, throughput, peak memory or power. These were added in later [CPU scaling and energy experiments](cpu-parallelism.md).

## Measurement Coverage and Limitations

| Requirement | Initial coverage |
|---|---|
| Input/output and successful execution | Confirmed for Dorado and Blitz |
| Software/model versions | Partially recorded; model characterization incomplete |
| Runtime and throughput | Initial Dorado figures; not captured for Blitz bring-up |
| Peak memory | Incomplete and not consistently scoped |
| Power and energy | Not systematically measured in these initial checks |
| Biological accuracy | Not established |
| Continuous real-time input | Not evaluated |
| Exact reproduction artifacts | Some commands and outputs recorded; environment details, hashes and artifacts incomplete |

**The main limitation is workload size.** D1 contains only 59 reads and D4 only 48. These were suitable for verifying functionality, but startup, model loading, automatic tuning, caching and other overheads can dominate short tests. The D1 and D4 chemistry/acquisition conditions differ, so their results cannot support a controlled Dorado-versus-Blitz ranking.

## Next Steps

1. Repeat hardware benchmarks using substantially larger datasets with verified chemistry, sampling rate, provenance, read counts and total signal samples.
2. Archive exact model identifiers and weights/checksums; document architecture, parameter counts, decoder and numerical precision where verifiable.
3. Standardize warm-up, repetitions, full-command versus basecalling-stage timing, memory scope and output validation.
4. Add power/energy instrumentation and reference-aligned accuracy as separate, clearly defined evaluations.
5. Assess sustained throughput against an explicitly defined MinION signal-rate target; do not equate short-run samples/s with live streaming capability.

## Related Investigations and Evidence

- [Dorado Cross-Platform Performance](hardware-throughput.md) — expanded CPU, CUDA and Metal observations.
- [DeepNano-Blitz CPU Scaling and Energy Efficiency](cpu-parallelism.md) — repeatability, threading, larger workload and CPU-package power.
- [Jetson TX2: ARM64 Port and Embedded CPU Baseline](embedded-feasibility.md) — later embedded execution.
- [Experiment Registry](../experiments/index.md) · [Reproduction Guide](../resources/reproduce.md)
