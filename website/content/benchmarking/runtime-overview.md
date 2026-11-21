---
title: "Basecaller Runtime Comparison and Measurement Coverage"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# Basecaller Runtime Comparison and Measurement Coverage

## Objective

Consolidate available runtime measurements and expose the controls still needed for a reproducible basecaller comparison.

## Work Performed

Reported runtimes for Dorado, DeepNano-Blitz and Slorado are assembled below without changing values. Groups retain workload, hardware and timing scope. Bonito and DeepNano-Coral were reviewed but not measured; no SoCall runtime is established.

### Investigation history

| Technical addition, newest first | Supporting work |
|---|---|
| Paired format/pipeline measurements | [POD5/BLOW5](pipeline-overhead.md); no assigned ID |
| Embedded CPU measurements | [BLITZ-009](../experiments/BLITZ-009.md) |
| Desktop timing and power sessions | [CPU report](cpu-parallelism.md), BLITZ-003–008 |
| Model-tier observations | [Fast/HAC](fast-vs-hac.md); no assigned IDs |
| Platform and GPU baselines | [Cross-platform report](hardware-throughput.md), DORADO-001–006 |

This synthesis has no new run date; it follows the team's investigation sequence.

## Experimental Setup / Methodology

Compare within matched groups before making any cross-tool claim. D1/Dorado uses a newer named model and a short basecalling stage; D4/D5/Blitz uses historical FAST5 and full-command timing. D2/D3 tier timer boundaries are unverified. Format runs have separate stage and command times. Power-session duration is not interchangeable with timing-only averages.

## Results

### Execution coverage

| Basecaller | Measured execution | Runtime interpretation |
|---|---|---|
| Dorado | CPU, CUDA, Metal; D1 and exploratory D2/D3 | Stage values and uncertain tier intervals; some command totals recorded |
| DeepNano-Blitz | Desktop/laptop CPU and ARM64 TX2 CPU; D4/D5 | Full-command measurements; separate power-session durations |
| Slorado | Exploratory BLOW5 comparison | Stage and command time; exact build/controls incomplete |
| Bonito | Source/compatibility review only | No measured runtime |
| DeepNano-Coral | Source review only | No measured runtime |
| SoCall | Model/weights access reported | No verified baseline/runtime |

#### D1 platform observations — basecalling stage

<!-- evidence:dorado-d1 -->

#### D2/D3 model tiers — timer boundaries unverified

<!-- evidence:ege-tiers -->

#### D4 desktop CPU — full command

<!-- evidence:blitz003 -->

<!-- evidence:blitz004 -->

<!-- evidence:blitz005 -->

<!-- evidence:weiqin3 -->

<!-- evidence:weiqin30 -->

#### D5 desktop CPU — full command

<!-- evidence:blitz007 -->

#### D4 embedded CPU — full command

<!-- evidence:tx2 -->

#### Separate power-session durations — repeated inputs labelled

<!-- evidence:blitz-power -->

<!-- evidence:weiqin-power-scaling -->

#### Dorado/Slorado format comparison — stage and command

<!-- evidence:formats -->

## Findings and Interpretation

Within the tested conditions, CUDA reduces Dorado stage time, additional caller threads reduce Blitz complete-command time, and HAC incurs a runtime cost in the exploratory tier tests. The Dorado/Slorado stage-versus-command reversal shows why a single runtime column without scope would mislead. These observations do not establish which basecaller is globally fastest or most accurate.

## Limitations

Datasets, chemistries, model generations, output formats, hardware and timing intervals differ. Missing original artifacts, model hashes, biological scoring and some exact commands prevent a controlled cross-tool ranking. Reported numerical precision is retained; power uncertainty is not removed by inclusion in this overview.

## Next Steps

Define compatible comparison groups, pin artifacts, use shared quality evaluation and record both end-to-end and stage timing. Extend the harness to repeated, independently reproducible measurements before using results to select SoCall optimization targets.

## Supporting Experiments and Evidence

Tables are generated from `results/summaries/report-observations.json`; [download the canonical observations](../results/summaries/report-observations.json). B2 pp.9–18; [source crosswalk](../docs/sources.md), [experiment registry](../experiments/index.md), [methodology](../docs/methodology.md).
