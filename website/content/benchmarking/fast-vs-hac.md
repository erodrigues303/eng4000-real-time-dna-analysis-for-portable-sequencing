---
title: "Dorado Fast vs HAC: Performance and Accuracy Tradeoffs"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# Dorado Fast vs HAC: Performance and Accuracy Tradeoffs

## Objective

Measure the computational cost of higher-accuracy model tiers and distinguish predicted quality from reference-based accuracy.

## Work Performed

The team compared Fast and HAC on Apple M2 using 4,000 real Zymo fecal reads and 200 simulated E. coli reads. Runtime and reported quality/accuracy were recorded for both tiers.

### Investigation history

| Addition | Technical contribution | Evidence |
|---|---|---|
| Reported in 14 Oct 2026 weekly entry; exact run dates unverified | Added real-input quality and simulated-input accuracy comparisons | W p.5, B2 p.10; [tier table](../evidence/index.md#ege-tiers) |

These comparisons have no assigned experiment IDs. DORADO-005 provides platform context, not their exact run configuration.

## Experimental Setup / Methodology

D2 is real Zymo fecal POD5; D3 is Squigulator E. coli simulation. The surrounding context is Dorado 2.1.2 on M2. Exact model/build identifiers, commands and timer boundaries are unverified for these comparisons. D2 reports median predicted Q; D3 reports an undocumented accuracy calculation.

## Results

<!-- evidence:ege-tiers -->

## Findings and Interpretation

HAC took longer and produced higher reported quality/accuracy values on both inputs. B2 p.10 reports a 5.9 percentage-point increase and approximately 86.4× runtime on D3. The unknown scoring method prevents treating that percentage as validated biological accuracy; D2 predicted Q cannot substitute for empirical alignment accuracy.

## Limitations

No signal-sample totals, exact model identities or reproducible scoring pipeline are available. Simulation parameters and reference identity are incomplete. These results do not establish real-time capacity or a general accuracy ranking.

## Next Steps

Recover model IDs and commands, pin simulation and reference settings, evaluate held-out biological data with a shared scoring method, and report throughput alongside mapped fraction and error distributions.

## Supporting Experiments and Evidence

B2 p.10; W pp.5,16; [source register](../docs/sources.md), [D2](../datasets/D2.md), [D3](../datasets/D3.md), [methodology](../docs/methodology.md). No new experiment IDs or measurements are assigned here.
