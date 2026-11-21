---
title: "DeepNano-Blitz on Jetson TX2: ARM64 CPU Baseline"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# DeepNano-Blitz on Jetson TX2: ARM64 CPU Baseline

## Objective

Establish an executable embedded CPU reference and assess caller scaling against a dataset-matched signal-rate target before measuring SoCall independently.

## Work Performed

The team ran the ARM64 CPU BLAS port, swept 1/2/4/8 caller threads, compared all measured FASTQ outputs and collected module-input power. Eight threads reported **214,574 samples/s**, or **10.48%** of the theoretical 4 kHz full-channel target.

### Investigation history

| Addition | Technical contribution | Record |
|---|---|---|
| 5 Nov 2026 | Added repeated full-command timing, output agreement and module-input telemetry | [BLITZ-009](../experiments/BLITZ-009.md) |
| Preliminary port checks; date unrecorded | Compared single-read debug/release output before full-dataset measurements | B2 p.13; part of BLITZ-009 context |

## Experimental Setup / Methodology

D4: 48 FAST5 reads, 9,033,454 samples and inspected 4,000 Hz acquisition metadata. B2 pp.4,13 specifies network 64, beam 5, Rust release extension, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, one excluded warm-up and three runs per thread setting. Monotonic timing covers launch through output writing. INA3221 VDD_IN is sampled about every 0.5 s and integrated over the workload.

The original P-based configuration still has unknown settings; B2 supplies additional report descriptions, not a recovered execution manifest. CUDA was unused.

## Results

<!-- evidence:tx2 -->

## Findings and Interpretation

Four threads delivered 207,860 samples/s, close to the eight-thread result. Profiling is needed to explain the limited additional scaling. The capacity denominator is 512 × 4,000 = 2,048,000 samples/s, not measured instrument yield. Matching outputs support reported consistency; this is neither a GPU nor a SoCall benchmark.

## Limitations

Sensor scaling and the low idle reading remain unverified. Module-input power cannot be ranked directly against CPU-package watts. Memory, utilization, thermal state and power mode are missing. The short historical dataset does not establish live latency or biological accuracy.

## Next Steps

Recover port patches and raw artifacts, verify sensor scaling, measure sustained input and queue latency, and establish SoCall correctness and its own baseline before choosing CPU/GPU optimizations.

## Supporting Experiments and Evidence

[BLITZ-009](../experiments/BLITZ-009.md), B2 pp.4,13,16–18; [sources](../docs/sources.md), [Jetson notes](../docs/platforms/jetson-tx2.md), [SoCall engineering](../socall/index.md).
