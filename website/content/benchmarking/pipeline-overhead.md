---
title: "POD5 vs BLOW5: Input Pipeline and Command Overhead"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# POD5 vs BLOW5: Input Pipeline and Command Overhead

## Objective

Characterize input-pipeline and setup costs, separating basecalling-stage performance from complete-command cost.

## Work Performed

The team compared Dorado/POD5 and Slorado/BLOW5 runs, recording stage/command timing, reported power/energy and GPU memory. The comparison changes model version and output format, so it cannot isolate a file-format effect.

### Investigation history

| Addition | Technical contribution | Evidence |
|---|---|---|
| After the Blitz work in the team-provided sequence; exact run date missing | Added paired pipeline timing, memory and reported energy observations | B2 pp.17–18; [format table](../evidence/index.md#formats) |

No experiment ID is assigned. This is separate from DORADO-003's 1.401 s observation.

## Experimental Setup / Methodology

The report compares Dorado HAC v6.0.0/POD5/BAM with Slorado HAC v5.0.0/BLOW5/FASTQ. P identifies RTX 4070. Exact build, conversion commands and post-conversion signal identity are incomplete. Electrical scope and energy integration details remain unverified.

## Results

<!-- evidence:formats -->

## Findings and Interpretation

Dorado reports the shorter basecalling stage, while Slorado reports the shorter complete command. The reversal makes timing boundaries important, but does not identify which pipeline component caused the difference. Different model and output choices prevent a causal format-speed claim.

## Limitations

Signal equivalence, model matching, cache conditions and original logs are missing. Energy values have incomplete measurement scope. These exploratory observations cannot rank POD5 and BLOW5 independently of the software pipeline.

## Next Steps

Match input signals, model/backend/output and cache policy; verify conversion identity. Time conversion, loading, inference and output separately and archive synchronized telemetry.

## Supporting Experiments and Evidence

B2 pp.17–18; [sources](../docs/sources.md), [planned format scenario](../configs/scenarios/README.md), [Slorado model record](../models/slorado-hac-v5.md), [reproduction guide](../resources/reproduce.md). No invented record is used for this unnumbered comparison.
