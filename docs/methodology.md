# Benchmark methodology — Phase 1 specification

Status: proposed shared protocol plus explicitly identified historical practice. This is not an implemented benchmark runner or an MLPerf-compliant benchmark. Historical evidence is registered in [sources](sources.md); results retain their original scopes and precision.

## Workload identity and execution

An experiment ID identifies a fixed tool/model/dataset/system/scenario. Preserve historical DORADO-001–006 and BLITZ-001–009; variants identify thread settings without reusing IDs. Unnumbered historical follow-ups retain descriptive transcription keys until the team assigns IDs. Record date, owner, executable version and commit, exact shell/working directory/command/environment, model and dataset hashes, input format, read/sample counts, output format, chunk/overlap/batch/thread settings and automatic tuning decisions. Chemistry is not architecture; 400 bases/s is not a 5 kHz signal sampling rate.

For new timing experiments: one excluded warm-up per configuration and at least three measured runs; use more runs when variability warrants it. This is a Phase 1 starting policy, not a statistical guarantee or MLPerf rule. Record all runs including failures, cold-start time, cache state, thermal stabilization, clocks, power mode and background activity. Do not silently exclude outliers. Predeclare exclusion reasons; report mean, sample SD, median, range and count where available. Randomize or interleave comparison order where feasible. Sustained workload duration and thermal-stability criteria are TBD per scenario.

Historical exceptions: Dorado D1 observations are single runs per P p.13; warm-up unknown. BLITZ-003 includes three paired measurements with a slow first run and no established warm-up. B pp.4,11–12 specifies one excluded warm-up and three timing runs for controlled follow-ups; 5700U extended tests use 30. BLITZ-006/008 power sessions are each single trials, even when a session contains 30 processes. BLITZ-009 uses one warm-up and three measured runs per P p.13; exact collection scripts are missing.

## Timing and throughput

Use a monotonic clock for durations and UTC timestamps for cross-device correlation. Identify startup, model load/autotuning, signal loading/preprocessing, host/device transfer, inference, decoding/stitching, and output writing. Synchronize asynchronous GPU work at documented boundaries. A tool-reported stage timer is not a full-command timer; full-command time includes process startup and output completion but excludes downloads and extraction unless explicitly stated. Retain both when possible.

For a stated interval T seconds, report signal samples/s = processed signal samples / T; bases/s = emitted bases / T; reads/s = completed reads / T. Define trimming, filtering, rejected reads and repeated-input accounting. Never infer signal count from rounded rate × runtime. Historical summary throughput sometimes uses N / mean(T), which differs from mean(N / T); keep the reported calculation. Input read counts and output counts must be separately checked.

Latency must specify read/chunk arrival and output-available endpoints, include queue delay, and report p50/p95/p99/max plus distribution and count. Per-read latency is not command duration divided by read count. No live latency measurements are established by these reports.

## Memory

Record measurement tool, poll period, units (bytes/MiB/GiB versus decimal MB/GB), process/child coverage and interval. Host maximum RSS from GNU Time, GPU allocated/reserved memory, device-wide GPU usage and Apple unified memory are separate metrics. VRAM capacity and model allocation during tuning are not standardized measured peak usage. Report sampled peaks as sampled peaks. TX2 BLITZ-009 memory and CPU utilization were not saved.

## Power and energy

Record instrument/sensor/software version, rail, units/scaling, clock domain, sampling interval, interpolation/integration, missing readings and measurement boundaries. Preserve the entire trace externally with checksums. Reject or flag energy intervals without bracketing samples; do not silently extrapolate across gaps. Sampled maxima can miss short peaks.

| Scope | Interpretation / limitation |
|---|---|
| GPU device power | Accelerator consumption, excludes CPU, storage and other host loads; sensor coverage must be stated. |
| CPU package power | Includes other package activity; excludes much of the computer; not basecaller-only power. |
| Jetson VDD_IN | Module input, not CPU-only or whole carrier-board/wall power; BLITZ-009 scaling unverified. |
| Whole-system wall/input power | Include meter location, peripherals, PSU losses and acquisition-computer boundary. |
| Historical Dorado/Slorado power | Sensor and electrical scope TBD; GPU hardware alone does not establish GPU-only measurement. |

Energy E = integral P(t) dt in joules; use timestamp-aware trapezoidal integration for sampled power with linearly interpolated endpoints. Time-weighted average power = E/T. Samples/J = processed samples/E; bases/J = emitted bases/E. Numerator and denominator must cover the SAME interval and workload. Do not multiply stage time by whole-command average power. Report gross workload energy; idle-subtracted energy is optional, separately labeled, with the baseline method and uncertainty. TDP is not measured power.

B pp.14–15: HWiNFO64 CPU Package Power is sampled approximately every 2.01 s, Windows America/Toronto timestamps aligned to runner UTC, interpolated and trapezoidally integrated. Workload energy excludes idle intervals but includes baseline activity within the workload. Brian used version 8.54-6090; Weiqin's version is unknown. Weiqin's 11.30 W pre-idle vs 5.11 W post-idle shows baseline drift. BLITZ-006 repeats D4 in 30 processes, not 30 independent energy trials. BLITZ-009 INA3221 VDD_IN sampled around 0.5 s; integration details/scaling remain TBD and power is provisional. No cross-scope energy ranking is justified.

## Real-time capacity and streaming

The fixed comparison target is 512 × 5,000 = 2,560,000 signal samples/s. D4/D5's dataset-matched target is 512 × 4,000 = 2,048,000 samples/s. Capacity (%) = 100 × throughput / explicitly labeled target. These assume continuously active channels. Later [D1 file inspection](../datasets/D1.md) verified a 5 kHz sampling rate for the named POD5 sample. Historical Dorado runs lack per-run input hashes. Measure actual incoming rate and active-channel occupancy for practical capacity.

A short stage rate above 100% does not demonstrate live operation. Future streaming tests need timestamped arrivals or a documented replay schedule, bounded queues, backpressure/drop accounting, chunk overlap/stitching semantics, output deadlines, latency distributions, sustained thermal behavior and quality checks. Separate file replay, accelerated replay and actual instrument acquisition. Queue and latency acceptance limits are TBD.

## Correctness and reference accuracy

Validate exit status, readable/nonempty FASTQ or BAM, unique expected read IDs, read counts, valid bases, matching sequence/quality lengths, and output checksums. Preserve original bytes; compare by read ID/sequence/quality to avoid order-dependent false differences. Record precision-dependent differences rather than assuming CPU/GPU identity. MM/ML modified-base tags require a separate check and appropriate ground truth.

Output equality is regression consistency, not biological accuracy. For reference evaluation, pin reference accession/version/hash and aligner/version/command; define trimming, secondary/supplementary mappings, unmapped reads, coverage, identity denominator, insertions/deletions, per-read versus pooled aggregation, and confidence intervals. Report mapped fraction and coverage alongside identity so filtering cannot hide failures. Exact aligner and scoring policy are TBD pending team agreement; no reference-validated results are claimed here. Predicted Q scores and B's simulated D3 accuracy percentages must remain distinct. Training/evaluation partitions must avoid read/specimen overlap and document possible pretrained-model exposure.

## Result release and reproducibility

Configs with null commands are historical metadata, not executable recipes. Obtain missing originals before attempting faithful reproduction. See [results layout](../results/README.md), [catalogue conventions](../schemas/README.md) and [contribution guide](../CONTRIBUTING.md). A validated result requires traceable raw artifacts, complete metadata, checksums, successful output checks and independent reproduction/review; schema validity alone is insufficient. Historical transcriptions are all preliminary. Scope, model, chemistry, dataset and quality differences must accompany comparisons. Optimize SoCall only after correctness, baseline measurement and stage-level profiling.
