---
title: "Jetson TX2: ARM64 Port and Embedded CPU Baseline"
---

<p class="eyebrow">Technical investigation · Phase 1</p>

# Jetson TX2: ARM64 Port and Embedded CPU Baseline

## Objective

Establish an embedded CPU baseline for DeepNano-Blitz and compare its recorded-file throughput with a dataset-matched MinION signal-rate target.

## Work Performed

The team adapted Blitz's CPU math-library path from x86 MKL to an ARM64 BLAS backend for its Python/Rust extension. Single-read debug and release checks preceded the full-dataset trials. The exact patch, linked library version, build commands and upstream commit remain unavailable. [Port record](../ports/README.md)

## Experimental Setup / Methodology

[BLITZ-009](../experiments/BLITZ-009.md) ran on November 5, 2026, using the [Jetson TX2](../systems/jetson-tx2.md) with Ubuntu 16.04.5, Jetson Linux R28.2.1 and 8 GB of shared memory. The historical build used the ARM64 CPU. The integrated GPU and CUDA were unused.

The input was [D4](../datasets/D4.md), with 48 FAST5 reads and 9,033,454 signal samples at 4 kHz. The report describes the Rust release extension, network 64, beam 5, `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`. Those settings come from the report, with no original run manifest to verify the effective configuration.

Each of the 1, 2, 4 and 8 caller-thread settings used one excluded warm-up and three measured runs. A monotonic timer covered launch through output writing. INA3221 VDD_IN module-input power was sampled about every 0.5 s and integrated over the workload. Sensor scaling remains unverified.

## Results

<!-- evidence:tx2 -->

All 12 FASTQ outputs reportedly matched. The underlying verification artifacts are missing. The platform record also gives idle readings of 0.979 W over 20 s and a separate initial 1.415 W, both subject to the sensor-scaling uncertainty. [Jetson platform notes](../docs/platforms/jetson-tx2.md)

## Findings

Eight threads reached 214,574 samples/s in 42.101 ± 0.353 s, a 3.50× speedup over one thread. Four threads reached 207,860 samples/s. The modest gain from four to eight threads needs profiling to explain it.

D4's 4 kHz metadata gives a theoretical full-occupancy target of 512 × 4,000 = 2,048,000 samples/s for the MinION. The eight-thread rate reached **10.48%** of this target. Active channels and practical input rate vary during sequencing. [ONT MinION hardware documentation](https://nanoporetech.com/document/hardware)

## Limitations

- Module-input watts and derived joules and samples/J are provisional until the INA3221 scale is verified. The electrical boundary differs from desktop CPU-package measurements.
- Peak memory, CPU utilization, affinity, power mode, thermals and clock state were not recorded.
- The small historical FAST5 fixture establishes reported CPU execution and output consistency. It provides no reference-scored accuracy, live arrival, queue latency or sustained streaming evidence.

## Next Steps

Recover the port patch and pinned build manifest. Validate VDD_IN scaling against an external measurement, then repeat longer tests with logged clocks, temperature, power mode and memory. Measure sustained throughput and queue latency against a controlled input arrival rate.

## Related Investigations and Evidence

- [BLITZ-009](../experiments/BLITZ-009.md)
- [DeepNano-Blitz CPU Scaling and Energy Efficiency](cpu-parallelism.md)
