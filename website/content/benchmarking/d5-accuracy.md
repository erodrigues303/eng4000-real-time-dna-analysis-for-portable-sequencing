---
title: "Blitz vs SoCall: Reference Accuracy on D5"
---
<p class="eyebrow">Technical investigation · Preliminary reference-alignment evidence</p>

# Blitz vs SoCall: Reference Accuracy on D5

**Brian Changkit · 23 November 2026.** Analysis of an existing BLITZ-007 output, not a new basecalling or timing run. The new scoring record is [BLITZ-010](../experiments/BLITZ-010.md).

## Research question

How do DeepNano-Blitz network 64 / beam 5 and the supplied FP32 SoCall pipeline agree with the same reference genome on the same D5 reads?

**Finding:** Blitz had higher mapped-read identity and mapped more reads than the two saved SoCall configurations on this dataset. This describes the tested pipelines and settings; it does not establish a universal model ranking, a hardware speedup or a cause of SoCall's errors.

## Experimental setup and evidence

[D5](../datasets/D5.md) is Wick's *Acinetobacter pittii* 16-377-0801 dataset: 4,467 FAST5 reads, 1,290,238,981 signal samples at 4 kHz. Acquisition metadata is labelled R9.4-family; the exact pore subrevision and any overlap with pretrained-model training data remain unverified.

| Output | Recorded configuration | Execution and source |
|---|---|---|
| Blitz | Network 64, beam 5, 8 caller threads, `OMP_NUM_THREADS=1` | Brian's 7800X3D / Ubuntu WSL, BLITZ-007 run 1, basecalled 24 Oct; scored 23 Nov ([BLITZ-010](../experiments/BLITZ-010.md)) |
| SoCall greedy | Supplied FP32 weights, 4,800-sample chunks, no overlap, batch 64; per-read median/MAD normalization | Ege's Apple M2 / MPS, 19 Nov ([SOCALL-001](../experiments/SOCALL-001.md)) |
| SoCall beam 5 | Same recorded SoCall setup, beam width 5 | Ege's Apple M2 / MPS, 19 Nov ([SOCALL-002](../experiments/SOCALL-002.md)) |

The two beam-5 settings are included for context; beam width alone does not make decoding, preprocessing, architecture or training identical. The M2 SoCall outputs, not the D1/TX2 throughput runs SOCALL-003–005, are the comparison inputs.

### Scoring and verification

All three use `minimap2 via mappy 2.31`, preset `map-ont`, primary alignment only, against the identical uncompressed reference SHA-256:

```text
b846951645ed1f5218da21539125c7e3110ec9c78f5956896aa2d0e554617958
```

Brian downloaded the scoring script from repository commit `5db279483d38ed8d7efc303e5561060ecd450b87` (script SHA-256 `c0046e5b0621f11a77078139fa1469fc3a0d51dc664d71bbc0cd05aa176ce649`). His uploaded JSON and per-read CSV are preserved without alteration. The comparison script recomputes every numeric summary field from each CSV, checks the scoring/reference metadata and verifies **4,467 unique, identical read IDs** in all three files. This checks the saved alignment evidence; it is not independent realignment of the FASTQs.

Identity is `M/(M+S+I+D)`, where M is matches, S substitutions, I inserted bases and D deleted bases. Median identity weights mapped reads equally; pooled identity weights alignment columns. Error rates use the pooled alignment-column denominator. Unmapped reads remain in the mapping-rate denominator, but are excluded from identity/error statistics. Aligned-base fraction reports aligned query bases divided by all predicted query bases, including unmapped reads; it is not reference-genome coverage.

## Results

<!-- d5-accuracy:summary -->

![Empirical cumulative distributions of primary-alignment identity among mapped reads for Blitz, SoCall greedy and SoCall beam 5](../assets/d5-accuracy-ecdf.svg)

The chart shows the full mapped-read distributions. A curve further right generally indicates higher identity. Unmapped reads are excluded from this chart and retained in the table. No error bars are shown: this is a descriptive comparison of one dataset, not independent timing repetitions or a confidence interval.

### Comparison by read ID

<!-- d5-accuracy:paired -->

Blitz's overall median exceeds SoCall beam-5 by **7.09 percentage points**. The median of per-read differences among reads mapped by both is **6.93 percentage points**; these are different statistics. Shared-mapped comparisons omit mapping failures, so report them alongside the mapping categories above. The two SoCall outputs are two decoder configurations, not two independent accuracy replicates.

## Interpretation and next experiments

The results establish a reference-backed starting point beyond the earlier example-output/repeatability checks. The saved SoCall beam-5 configuration improves on greedy decoding, but the tested Blitz pipeline still has higher identity on most shared mapped reads. Profiling and controlled changes to normalization, decoding and chunk boundaries can now be evaluated against this baseline. This result alone does not identify which stage explains the gap.

Next: inspect poor alignments and unaligned sequence, evaluate permitted SoCall preprocessing/chunk/decoder changes one at a time with before/after accuracy, and repeat on additional reference-backed compatible datasets. Verify training/evaluation separation before generalization claims. Measure speed/energy on common hardware and common input with identical timing/electrical boundaries before making efficiency rankings; retain hardware/precision/settings disclosures if that is not feasible.

### Scope and limitations

- One bacterial isolate and one frozen output per configuration; no consensus accuracy, held-out training guarantee, variant accuracy or clinical validation.
- Primary local alignment can omit difficult read ends and other unaligned regions; identity is not the percentage of every predicted base that is correct. Circular-reference boundary handling and split alignments are not specially evaluated.
- Basecalling was performed on different hardware and at different dates, with different models, preprocessing and decoding. This is a pipeline-output comparison, not an isolated architecture or hardware experiment.
- FASTQs remain outside the repository. Their recorded hashes identify outputs, but they were not independently re-hashed or realigned during this comparison. Original signal contents were not re-hashed here. Matching output IDs is necessary but not a proof of byte-identical raw input.
- The new analysis has no measured timing, power, memory or live-arrival result. Earlier BLITZ-007 throughput and BLITZ-008 package energy remain separate evidence and must not be combined with D1/TX2 SoCall results to claim a controlled speed or energy advantage.
- This follows selected reproducibility/quality principles; it is not an official MLPerf result. No improvement threshold has been approved by implication.

## Reproduction and downloadable evidence

Use Python 3.12 with `mappy==2.31` to repeat the alignment step. Install the Ubuntu `zlib1g-dev` build dependency if mappy must be compiled. Obtain BLITZ-007 `run1.fastq` from Brian and the D5 reference from the [dataset card](../datasets/D5.md), verify hashes, and run from `~/capstone-blitz/comparison-d5`:

```bash
python reference_accuracy.py \
  ~/capstone-blitz/deepnano-blitz/benchmarks/large-dataset-20261024-201712/run1.fastq \
  reference.fasta \
  --out-dir blitz-d5-accuracy
```

To reproduce the comparison from the checked-in scoring evidence, from the public repository root:

```bash
python harness/analysis/compare_d5_accuracy.py
python harness/analysis/compare_d5_accuracy.py --check
# Optional chart regeneration (requires matplotlib):
python harness/analysis/compare_d5_accuracy.py --plot
```

[Comparison JSON and artifact hashes](../results/summaries/d5-accuracy-comparison.json) · [Blitz accuracy JSON](../results/raw/brian-7800x3d/blitz/reference-accuracy/BLITZ-010/accuracy.json) · [Blitz per-read CSV](../results/raw/brian-7800x3d/blitz/reference-accuracy/BLITZ-010/alignments.csv).

SoCall source artifacts: [greedy JSON](https://github.com/erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing/blob/5db279483d38ed8d7efc303e5561060ecd450b87/results/raw/ege-m2/socall/reference-accuracy/SOCALL-001/accuracy.json), [greedy CSV](https://github.com/erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing/blob/5db279483d38ed8d7efc303e5561060ecd450b87/results/raw/ege-m2/socall/reference-accuracy/SOCALL-001/alignments.csv), [beam-5 JSON](https://github.com/erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing/blob/5db279483d38ed8d7efc303e5561060ecd450b87/results/raw/ege-m2/socall/reference-accuracy/SOCALL-002/accuracy.json), [beam-5 CSV](https://github.com/erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing/blob/5db279483d38ed8d7efc303e5561060ecd450b87/results/raw/ege-m2/socall/reference-accuracy/SOCALL-002/alignments.csv).

[Evidence register](../docs/sources.md) · [Blitz CPU timing/energy study](cpu-parallelism.md) · [SoCall engineering](../socall/index.md).
