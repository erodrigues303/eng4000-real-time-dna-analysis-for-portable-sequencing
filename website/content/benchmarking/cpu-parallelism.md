<p class="eyebrow">Benchmarking study · Preliminary</p>

# How does CPU parallelism affect throughput and energy?

On the tested Ryzen 7 7800X3D configuration, increasing DeepNano-Blitz caller threads from one to eight reduced mean full-command runtime from **15.187 s to 2.917 s**, a reported **5.21× speedup**. This is evidence of scaling on a small recorded workload, not a live-sequencing or biological-accuracy result. [BLITZ-005 evidence](../evidence/index.md#blitz005).

## Experimental design

[BLITZ-005](../experiments/BLITZ-005.md) holds [D4](../datasets/D4.md), [network 64](../models/blitz-network64.md), beam size 5 and `OMP_NUM_THREADS=1` fixed on the [7800X3D system](../systems/brian-7800x3d.md). Caller threads vary across 1, 2, 4 and 8. Each setting has one excluded warm-up and three measured runs. GNU Time covers the complete command, including startup, input loading and output writing.

The dataset contains 48 FAST5 reads and 9,033,454 signal samples. Warm-up can leave files cached. Exact commands, original timings and output files for this experiment have not been supplied.

## Results

![BLITZ-005 mean full-command runtime and sample standard deviation for 1, 2, 4 and 8 caller threads](../assets/blitz005-runtime.svg)

<p class="caption">Ryzen 7 7800X3D; D4; network 64; beam 5. Bars show mean runtime, whiskers show sample SD across three runs (not confidence intervals). Generated from the canonical report transcription, B p.11; corroborated by B2 p.11.</p>

The [full results table](../evidence/index.md#blitz005) includes per-run wall times, throughput, peak host RSS and CPU utilization. All 12 outputs reportedly matched by read ID, sequence and quality string. This validates reported consistency across settings, not correctness against a biological reference.

## Interpretation

The measured speedup is sublinear: eight caller threads do not produce an eightfold improvement. These timings alone cannot attribute the remaining cost to decoding, I/O, synchronization or another stage; profiling is required.

The larger [BLITZ-007](../experiments/BLITZ-007.md) workload reports **315.31 ± 0.65 s** over three runs at eight threads, processing 4,467 D5 reads. It extends the observation to approximately five minutes of recorded-file processing, with reported matching outputs. It does not measure queue stability under incoming signal. [Evidence](../evidence/index.md#blitz007).

## Energy is a separate measurement

The 5700U follow-up reports CPU-package efficiency increasing from **20,749 to 77,907 samples/J** across one to eight threads. These values come from one continuous power session with repeated D4 processes, not independent energy replicates and not BLITZ-005. [Energy-session evidence](../evidence/index.md#weiqin-power-scaling).

[BLITZ-006](../experiments/BLITZ-006.md) and [BLITZ-008](../experiments/BLITZ-008.md) provide separate 7800X3D CPU-package measurements. Neither establishes whole-system energy consumption. Keep workload and electrical boundaries visible when comparing them.

## Limitations

- D4 is a small historical-chemistry fixture; the same reads are reused.
- Raw artifacts and weight checksums are unavailable; the figure reproduces report values.
- CPU-package energy includes other package activity and excludes much of the host.
- The 5700U follow-ups have no assigned experiment IDs; they are retained under descriptive evidence-table keys.
- Output matching, predicted quality and reference accuracy are distinct claims.

## Next investigation

Recover original commands and artifacts, interleave thread configurations on larger compatible data, record thermal state and caching, and repeat independent power sessions. Profile stage boundaries before choosing an optimization hypothesis.

## Supporting experiments and reproduction

[BLITZ-003](../experiments/BLITZ-003.md) · [BLITZ-004](../experiments/BLITZ-004.md) · [BLITZ-005](../experiments/BLITZ-005.md) · [BLITZ-006](../experiments/BLITZ-006.md) · [BLITZ-007](../experiments/BLITZ-007.md) · [BLITZ-008](../experiments/BLITZ-008.md)

[Reproduction guide](../resources/reproduce.md) · [Source revisions](../docs/sources.md)
