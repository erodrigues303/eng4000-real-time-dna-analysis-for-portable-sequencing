# MLCommons alignment gap analysis

## Closest categories and scenarios

For this project's embedded goal, **MLPerf Inference: Edge** is the closest system-category analogy; this is a project interpretation, not an official classification of nanopore basecalling. Recorded-file throughput is conceptually closest to Offline processing. A future streaming experiment should borrow explicit arrival and latency controls, but continuous variable-length signal is not automatically equivalent to an MLPerf query stream. See [MLPerf Inference: Edge](https://mlcommons.org/benchmarks/inference-edge/) and [scenario rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc), reviewed 2026-11-20.

The [power policy](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc) requires total system-under-test power and identifies synchronized performance/power timestamps and reproducibility. The project's CPU-package and provisional module-input readings do not meet that whole-system boundary. No LoadGen integration or official benchmark execution has been implemented. These are methodology influences and documented gaps, not adopted compliance claims. A rules commit must be pinned before a formal alignment assessment.

## Principle-by-principle gaps

Status: research/design gap analysis. No MLPerf compliance, submission, certification or implemented alignment is claimed. Nanopore basecalling is not established here as an official MLPerf workload.

MLCommons emphasizes representative workloads, quality and reproducibility; its inference rules define scenarios and execution/quality constraints. Sources reviewed on 2026-11-11: [benchmark goals](https://mlcommons.org/benchmarks/), [inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc), [power rules](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc). These are moving references; the version/commit for a future detailed assessment is TBD. No numerical MLPerf rules are adopted by implication.

| Concept | Evidence in this project | Gap / intended treatment |
|---|---|---|
| Fixed workload and model | D1 hardware comparisons; D4 fixed network/beam in Blitz scaling | Pin hashes, precision, preprocessing and compatible chemistries. Different models/chemistries are separate comparison groups. |
| Quality threshold | Output equality checks; simulated percentages | Reference scoring and acceptable quality loss TBD. P's 0.5% proposed tolerance is not an approved threshold. |
| Performance scenarios | Recorded-file timing | Define offline versus sustained versus streaming. Nanopore variable read lengths and continuous signal arrivals need explicit workload units. Do not relabel replay as an MLPerf scenario. |
| Load generation / latency | None supplied | Arrival process, queue limits, deadlines and percentile methodology TBD; no official LoadGen integration. |
| Repetition / statistics | Three-run Blitz tests and 30-run follow-ups | Dorado repetition missing; power trials often single sessions. One warm-up + three is a project proposal, not an MLPerf-derived rule. |
| Power measurement | CPU package traces; provisional TX2 rail readings | Sensor calibration, whole-system scope, synchronized windows and independent repeats missing. Existing telemetry is not an official MLPerf power measurement. |
| Hardware / software disclosure | Reported CPU/GPU/OS and partial build provenance | Driver/runtime, clocks, thermal state, power mode and executable hashes incomplete. |
| Validation / audit | Reported output comparisons | Original artifacts, automatic checks and independent reproduction missing. No compliance suite/audit performed. |
| Reproducibility | This repository's schema and evidence layout | Recover exact commands and environment locks; implement small runners and derived analysis incrementally. |

Project-specific deviations to document: signal samples versus fixed inference queries; model–chemistry compatibility; overlapping chunks and read stitching; basecalling-stage versus full pipeline timing; variable biological quality; unknown pretrained-model data overlap; CPU/GPU/module electrical boundaries. An external methodology review cannot establish what was actually measured historically.

Before claiming selected-principle alignment, pin a rules revision, map each selected rule to an implemented protocol and artifact, justify exclusions, validate quality and power methods, and obtain an independent reproduction. [Wick's comparison](https://github.com/rrwick/Basecalling-comparison) inspires explicit data, commands and reproducible analysis; it does not make unlike datasets or hardware comparable.
