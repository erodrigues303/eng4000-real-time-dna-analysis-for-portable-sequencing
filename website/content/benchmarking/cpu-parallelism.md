---
title: "DeepNano-Blitz CPU Scaling and Energy Efficiency"
---

<p class="eyebrow">Technical investigation · Phase 1</p>

# DeepNano-Blitz CPU Scaling and Energy Efficiency

## Objective

Measure how caller threads and workload size affect full-command runtime, peak host memory, output repeatability and CPU-package energy.

## Experimental Setup / Methodology

The [Ryzen 7 7800X3D desktop](../systems/brian-7800x3d.md) and [Ryzen 7 5700U laptop](../systems/weiqin-5700u.md) used Ubuntu/WSL and CPU execution. The desktop follow-up build pinned `deepnano2` 0.1 at commit `15bd04b94c291debac75823811a2c86820dda589`. The recorded desktop and laptop follow-ups used [network 64](../models/blitz-network64.md), beam 5, FASTQ output and `OMP_NUM_THREADS=1`. Caller threads were varied independently. The model's weight hash, parameter count and exact compute precision remain unverified.

| Input | Recorded workload | Use |
|---|---|---|
| [D4](../datasets/D4.md) | 48 reads, 9,033,454 FAST5 samples at 4 kHz | Baselines, thread sweeps and repeated-input power sessions |
| [D5](../datasets/D5.md) | 4,467 reads, 1,290,238,981 FAST5 samples at 4 kHz | Larger recorded-file timing and separate power session |

Shell time and GNU Time cover the full command. GNU Time also records peak host RSS where available. Timing tables report sample standard deviation where recorded. Power sessions sampled HWiNFO64 CPU Package Power about every 2.01 s, aligned samples to workload UTC boundaries with interpolation, and integrated energy by the trapezoidal rule. Samples/J uses the signal sample count and integrated package energy.

## Results

The [initial functional checks](initial-basecaller-setup.md#deepnano-blitz) processed D4 twice on the 7800X3D with byte-identical FASTQ output. The historical [5700U comparison](../experiments/BLITZ-003.md) then measured one and four threads, including a slow first run. The [7800X3D baseline](../experiments/BLITZ-004.md) measured three one-thread runs with warm-up status unresolved.

<!-- evidence:blitz003 -->

<!-- evidence:blitz004 -->

[BLITZ-005](../experiments/BLITZ-005.md) used one excluded warm-up and three measured runs at each of four thread settings. All 12 outputs reportedly agreed by read ID, sequence and quality.

![Mean BLITZ-005 full-command runtime and sample standard deviation by caller-thread count](../assets/blitz005-runtime.svg)

<p class="caption">Ryzen 7 7800X3D, D4, network 64 and beam 5. Whiskers show sample standard deviation across three measured runs per setting.</p>

<!-- evidence:blitz005 -->

The 5700U follow-ups measured three and then 30 runs per thread setting. The extended sweep reported matching outputs across all 120 measured runs. Its eight-thread rate was 1,681,417 samples/s with a 110.04 MiB peak RSS.

<!-- evidence:weiqin3 -->

<!-- evidence:weiqin30 -->

[BLITZ-007](../experiments/BLITZ-007.md) moved the 7800X3D eight-thread configuration from D4 to D5. Three runs averaged 315.31 ± 0.65 s, with matching outputs, a reported 4,092,013 samples/s and a maximum RSS of 169.66 MiB.

<!-- evidence:blitz007 -->

[BLITZ-006](../experiments/BLITZ-006.md), [BLITZ-008](../experiments/BLITZ-008.md) and the 5700U power follow-ups were separate sessions from the timing-only runs. Each D4 ×30 session processed 271,003,620 samples across 1,440 read instances from the same 48-read fixture.

<!-- evidence:blitz-power -->

<!-- evidence:weiqin-power-scaling -->

## Findings

One-to-eight-thread speedup on D4 reached 5.21× on the 7800X3D and 4.17× in the 5700U extended sweep. The 7800X3D eight-thread rate increased from 3.10 million samples/s on D4 to 4.09 million on D5. Startup is a smaller fraction of a longer run, but the two datasets also differ in read composition. The measurements cannot isolate the cause of the rate increase.

In the continuous 5700U power sweep, package energy for the same workload fell from 13,061 J to 3,479 J as runtime fell. Efficiency rose from 20,749 to 77,907 samples/J even as average package power rose from 19.47 to 21.58 W. The 7800X3D's separate eight-thread sessions reported 54,358 samples/J on repeated D4 and 57,524 samples/J on D5. These values describe CPU-package energy for the recorded workloads.

## Limitations

- D4 is a small historical-chemistry fixture. Repeated processing can be affected by cache state and background activity. D5 is larger but still recorded input. Live queueing, latency and sustained arrival were not evaluated.
- The original timing logs, telemetry and many exact commands are missing. One independent power session per configuration does not establish energy variability. Package power excludes other host loads.
- Output agreement establishes repeatability. The later D5 alignment comparison scores one saved BLITZ-007 output. These timing and power runs do not establish accuracy across workloads or configurations.

## Next Steps

Recover commands, weight hashes and raw telemetry. Repeat power measurements in independent, interleaved runs with recorded thermal and cache state. Profile input, inference, decoding and output separately, and measure whole-system energy when comparing deployment platforms.

## Related Investigations and Evidence

- [BLITZ-005 configuration and available artifacts](../experiments/BLITZ-005.md)
- [Jetson TX2: ARM64 Port and Embedded CPU Baseline](embedded-feasibility.md)
- [DeepNano-Blitz vs SoCall: Reference Accuracy on D5](d5-accuracy.md)
