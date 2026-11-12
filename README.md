# Project 22 — Enabling Real-Time DNA Analysis for Portable Sequencing

York University ENG 4000 capstone

This repository is the technical record for two connected contributions: a reproducible modern nanopore basecalling benchmark, and evidence-led characterization and optimization of **SoCall**, the lab's int8/fixed-point implementation intended for embedded NVIDIA Jetson hardware. SoCall remains one implementation under study; its correctness and performance baseline has not yet been established. Publication permission for its code and weights is unconfirmed.

Portable MinION sequencing needs computation that can keep pace with incoming signal without excessive latency, memory use or energy demand. We extend the reproducible-data-and-command philosophy of [Ryan Wick's basecalling comparison](https://github.com/rrwick/Basecalling-comparison) with model/chemistry documentation, modern hardware, power and energy, and eventual streaming tests. The course report records the capstone process; this repository records what was measured and how to reproduce it.

## Current status

**Phase 1 foundation; all imported results are preliminary.** Two supplied reports were reviewed: the preliminary benchmarking report and Progress Report 1 (submitted November 6, 2026). Original commands, raw logs and port sources were not supplied. The [evidence register](docs/sources.md) records file hashes, page references and conflicts; [gaps](docs/gaps.md) records missing information. No experiment was rerun during this migration. There are no independently validated benchmark results, no SoCall baseline and no established live-streaming result.

| Basecaller                     | Evidence / status                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Dorado 2.1.2                   | Executed on CPU, NVIDIA CUDA and M2 Metal; HAC v6.0.0 on D1; modified-base companion tested.                |
| Slorado                        | Exploratory BLOW5 comparison using HAC v5.0.0; exact build/model identity incomplete.                       |
| DeepNano-Blitz / deepnano2 0.1 | CPU regression, thread scaling, larger-workload and package-energy tests; owned ARM64 CPU port used on TX2. |
| DeepNano-Coral                 | Source review only; CNN/int8/Edge TPU path; no execution established.                                       |
| Bonito v1.1.0                  | Source/configuration review only; no measured run or uniquely identified tested model.                      |
| SoCall                         | Access to model/weights reported; baseline, profiling and optimization pending; private material excluded.  |

## Preliminary observations

| Experiment / workload       | System                     | Reported result                             | Scope and limitation                                                                                 |
| --------------------------- | -------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| DORADO-001 / D1, 59 reads   | GTX 1060                   | 525,235 samples/s; 53.213 s                 | Tool-reported stage; single small run.                                                               |
| DORADO-002 / D1             | Ryzen 5 1500X CPU          | 6,628.981 samples/s; 4,216.234 s            | Same named model/data, different backend; not full-pipeline comparison.                              |
| DORADO-003 / D1             | RTX 4070                   | 19,949,560 samples/s; 1.401 s               | Full command ~12 s; stage capacity 779.28% of theoretical 5 kHz target is not proven live operation. |
| DORADO-005 / D1             | Apple M2 Metal             | ~113,217 samples/s; 246.9 s                 | Single small run; memory/power scope incomplete.                                                     |
| DORADO-006 / D1             | RTX 3070 Mobile            | 3,663,565 samples/s; 7.6 s                  | Canonical ID from progress report; earlier ID conflict retained.                                     |
| BLITZ-005 / D4, 48 reads    | Ryzen 7 7800X3D            | 5.21× speedup, 1→8 threads                  | Three timing runs per setting; output consistency, not biological accuracy.                          |
| BLITZ-007 / D5, 4,467 reads | Ryzen 7 7800X3D, 8 threads | 315.31 ± 0.65 s; 4,092,013 samples/s        | Three full-command runs, ~5 minutes each; recorded input.                                            |
| BLITZ-008 / D5              | Same CPU                   | 70.18 W average; 22,430 J; 57,524 samples/J | Separate single power trial; CPU package only.                                                       |
| 5700U extended D4 follow-up | Ryzen 7 5700U              | 4.17× timing speedup, 1→8 threads           | 30 runs per setting; one separate continuous power session reports 20,749→77,907 samples/J.          |
| BLITZ-009 / D4              | Jetson TX2 CPU, 8 threads  | 214,574 samples/s; 42.101 ± 0.353 s         | Three runs; 10.48% of theoretical 4 kHz target. Module power calibration unverified.                 |

Sources: B pp.9,11–15 and P pp.13,15–16; [all tables and provenance](results/summaries/historical-summary.md). Different datasets/models/timing and electrical scopes prevent a controlled cross-tool ranking. Modified-base overhead on RTX 4070 was 8.21% in stage time on D1; MM/ML verification and biological accuracy remain open. The Dorado/Slorado format comparison changes model version and output format, so it does not isolate file-format performance.

## Systems and datasets

[System cards](systems/): Ryzen 5 1500X + GTX 1060 3 GB; RTX 4070 12 GB desktop; Apple M2 / 8 GB unified memory; Ryzen 7 7800X3D desktop (4070 Ti unused for Blitz); Ryzen 7 5700U laptop; Ryzen 9 5900HX + RTX 3070 Mobile laptop; and Jetson TX2 / 8 GB shared memory. Detailed OS/runtime gaps are explicit. The TX2 ran a CPU port of Blitz; **current Dorado support on TX2 is not established and must not be assumed**.

| Dataset              | Recorded input                                                              | Use                                                         |
| -------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [D1](datasets/D1.md) | DeepMod2 v0.3.0; human; 59 POD5 reads; Dorado-detected R10.4.1/E8.2/400 bps | Smoke and preliminary comparison; not a training corpus.    |
| [D2](datasets/D2.md) | ONT Zymo fecal; 4,000 POD5 reads                                            | Exploratory model-tier evaluation; chemistry/reference TBD. |
| [D3](datasets/D3.md) | Squigulator E. coli; 200 BLOW5 reads                                        | Simulation; generator and scoring details TBD.              |
| [D4](datasets/D4.md) | Blitz fixture; 48 FAST5 reads; 9,033,454 samples; inspected 4 kHz metadata  | Regression/thread scaling; old R9.4-labelled acquisition.   |
| [D5](datasets/D5.md) | Wick A. pittii; 4,467 FAST5 reads; 1,290,238,981 samples; 4 kHz             | Larger workload/evaluation; archive MD5 recorded.           |

R10.4.1 training data and separately held-out reference evaluation data still need selection and documentation. No large signal files or model weights are included.

## Benchmark dimensions and methodology

[Methodology](docs/methodology.md) defines stage and full-command timing, samples/s, bases/s, latency, memory, scoped power, energy, samples/J or bases/J, output consistency, reference accuracy and real-time capacity. GPU device power, CPU package power, Jetson module input and wall power are distinct. A theoretical 512-channel target is 2.56 million samples/s at 5 kHz or 2.048 million at 4 kHz; exceeding it in a short test does not establish stable queues or acceptable latency.

The [MLCommons gap analysis](docs/mlcommons-alignment.md) identifies relevant principles and missing evidence. We do **not** claim MLPerf compliance or completed principle alignment. [Scenarios](configs/scenarios/) cover offline/sustained throughput, power, accuracy, streaming, chunk sweeps and format comparisons; they are definitions, not delivered execution support.

## Repository map

```text
README.md, CONTRIBUTING.md, .gitignore, requirements-dev.txt
docs/
  methodology.md, mlcommons-alignment.md, sources.md, gaps.md
  results/                   # Interpretation and limitations
  platforms/                 # TX2, Windows/CUDA, WSL, Apple/Metal
harness/
  runners/                   # Execution wrappers pending
  telemetry/                 # Collectors pending
  analysis/                  # Metadata validation and table/card rendering
configs/
  experiments/               # Historical records; commands missing
  scenarios/                 # Proposed scenario definitions
schemas/                     # Experiment/system/model/dataset JSON Schemas
systems/, models/, datasets/ # JSON metadata + generated Markdown cards
results/
  raw/                       # Reserved for original evidence, currently empty
  summaries/                 # Report transcriptions and generated tables
ports/                       # Owned patch recovery/compatibility documentation
```

## Reproduction path

1. Select an [experiment record](configs/experiments/) and inspect its limitations. Current records are metadata, not executable recipes: exact commands are missing from the supplied reports.
2. Recover the original invocation, environment, input/model artifacts and checksums; resolve the relevant catalogue and platform gaps.
3. Use the scenario's explicit timing, warm-up, repetition and telemetry protocol. Save original evidence under the [results convention](results/README.md), with large artifacts hosted externally.
4. Validate outputs, align to a pinned reference for accuracy, then generate tables with their source records. A teammate independently reproduces before upgrading result status.

Foundation checks (Python 3.10+):

```sh
python -m pip install -r requirements-dev.txt
python harness/analysis/validate_metadata.py
python harness/analysis/render_summaries.py --check
```

Edit catalogue JSON or `results/summaries/report-observations.json`, then run the renderer without `--check` to update cards/tables. No benchmark runner is implemented in this phase. The next priorities are original-evidence recovery, TX2 sensor verification, model/data provenance, reference accuracy and a correctness-first SoCall baseline. See [proposed team issues](docs/gaps.md#recommended-github-issues).
