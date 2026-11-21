---
title: "DeepNano-Blitz CPU Scaling and Package Energy"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# DeepNano-Blitz CPU Scaling and Package Energy

## Objective

Establish CPU baselines and quantify caller-thread scaling, workload-size effects and package energy before selecting embedded optimization targets.

## Work Performed

The team ran Blitz on Ryzen 7 5700U and 7800X3D systems, checked output agreement, swept caller threads, processed a larger recorded dataset and collected separate CPU-package power sessions. BLITZ-005 reports a **5.21×** one-to-eight-thread speedup; biological accuracy and streaming capability remain unverified.

### Investigation history

| Addition | Technical contribution | Supporting record |
|---|---|---|
| 25 Oct 2026 | Extended 5700U timing to 30 runs per setting and added package-energy analysis | [Timing](../evidence/index.md#weiqin30), [energy](../evidence/index.md#weiqin-power-scaling); unnumbered follow-ups |
| 24 Oct 2026 | Added D5 timing and a separate power trial | [BLITZ-007](../experiments/BLITZ-007.md), [BLITZ-008](../experiments/BLITZ-008.md) |
| 24 Oct 2026 | Established 7800X3D baseline, thread sweep and repeated-D4 power session | [BLITZ-004](../experiments/BLITZ-004.md), [BLITZ-005](../experiments/BLITZ-005.md), [BLITZ-006](../experiments/BLITZ-006.md) |
| 16 Oct 2026 | Measured initial 5700U one/four-thread timing and output consistency | [BLITZ-003](../experiments/BLITZ-003.md) |

## Experimental Setup / Methodology

Network 64, beam size 5, FASTQ output and `OMP_NUM_THREADS=1` are fixed in the controlled desktop follow-ups. [D4](../datasets/D4.md) contains 48 reads / 9,033,454 samples; [D5](../datasets/D5.md) contains 4,467 reads / 1,290,238,981 samples. GNU Time measures complete-command time and host RSS. BLITZ-005/007 use one excluded warm-up and three measured runs per setting. BLITZ-003 retains its slow first run; an excluded warm-up is not established there.

HWiNFO64 CPU Package Power is sampled approximately every 2.01 s, aligned to workload UTC intervals and integrated by the trapezoidal rule. Timing repetitions and independent power trials are different quantities.

## Results

![BLITZ-005 full-command runtime, mean and sample SD across three runs](../assets/blitz005-runtime.svg)

<p class="caption">7800X3D, D4, network 64, beam 5. Whiskers show sample SD, not confidence intervals. Canonical report transcription, corroborated by B2 p.11.</p>

<!-- evidence:blitz005 -->

<!-- evidence:blitz007 -->

<!-- evidence:blitz-power -->

The [5700U extended timing](../evidence/index.md#weiqin30) reports a 4.17× speedup. Its [energy analysis](../evidence/index.md#weiqin-power-scaling) reports 20,749 to 77,907 samples/J from one to eight threads in one continuous power session.

## Findings and Interpretation

Caller parallelism reduced runtime on both systems. BLITZ-005 scaling is sublinear; timings alone cannot assign remaining cost to I/O, decoding or synchronization. BLITZ-007 extends reported repeatability to approximately five minutes of recorded-file processing. Matching outputs establish consistency, not reference accuracy.

Energy observations suggest reduced processing time can improve samples/J without a proportional power increase. Whole-system savings and independent energy variability remain unestablished. The [TX2 investigation](embedded-feasibility.md) evaluates the embedded CPU path separately.

## Limitations

- D4 reuses a small historical-chemistry fixture; cache and background activity can affect timing.
- BLITZ-005 and later follow-ups lack original commands/artifacts; tables remain secondary evidence.
- Weight hashes, biological scoring, sustained arrival rates and latency distributions are incomplete.
- CPU-package readings exclude much of the host. Single power sessions do not provide independent energy replicates.

## Next Steps

Recover invocations and artifacts, interleave thread settings on larger compatible inputs, record cache/thermal state and repeat power sessions. Profile stages and verify biological quality before transferring optimization conclusions to SoCall.

## Supporting Experiments and Evidence

[BLITZ-003](../experiments/BLITZ-003.md) · [BLITZ-004](../experiments/BLITZ-004.md) · [BLITZ-005](../experiments/BLITZ-005.md) · [BLITZ-006](../experiments/BLITZ-006.md) · [BLITZ-007](../experiments/BLITZ-007.md) · [BLITZ-008](../experiments/BLITZ-008.md).

B2 pp.4,7,11–16; [source register](../docs/sources.md), [reproduction guide](../resources/reproduce.md). Individual experiment records retain the available commands, settings and measurement details.
