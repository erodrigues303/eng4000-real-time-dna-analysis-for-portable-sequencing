---
title: "Dorado Cross-Platform Performance"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# Dorado Cross-Platform Performance

## Objective

Establish existing-basecaller reference behaviour across Windows CPU/CUDA and macOS Metal, identifying deployment and measurement differences relevant to portable sequencing.

## Work Performed

Dorado 2.1.2 processed the same named 59-read D1 sample on CPU, NVIDIA GPUs and Apple M2 Metal. The team recorded stage runtime, throughput and partial output/memory summaries. The [GPU acceleration report](gpu-acceleration.md) separately examines CPU/CUDA speed differences.

### Investigation history

| Addition | Technical contribution | Supporting record |
|---|---|---|
| Date not recorded | Added RTX 3070 Mobile observation; historical ID conflict retained | [DORADO-006](../experiments/DORADO-006.md) |
| 14 Oct 2026 | Added RTX 4070, modified-base companion and M2 Metal results | [DORADO-003](../experiments/DORADO-003.md), [004](../experiments/DORADO-004.md), [005](../experiments/DORADO-005.md) |
| 8 Oct 2026 | Established CPU reference | [DORADO-002](../experiments/DORADO-002.md) |
| 6 Oct 2026 | Completed initial GPU basecalling workflow | [DORADO-001](../experiments/DORADO-001.md) |

The undated addition is shown separately from the dated sequence.

## Experimental Setup / Methodology

[D1](../datasets/D1.md), Dorado 2.1.2 and the named [HAC v6.0.0 model](../models/dorado-hac-v6.md) are shared. Hosts, backends and automatic batch settings differ. Values cover tool-reported basecalling intervals; exact boundaries and repeated-run statistics are incomplete. The modified-base row is a different workload.

## Results

<!-- evidence:dorado-d1 -->

<!-- evidence:dorado-memory -->

## Findings and Interpretation

All recorded platforms completed the small workload, but runtime differs substantially. Automatic tuning and differing host configurations prevent attributing every difference to accelerator hardware. The RTX 4070's approximately 12 s complete command is longer than its 1.401 s stage interval; report both boundaries when planning deployment.

## Limitations

D1 is small; repeated Dorado trials, complete environments and biological scoring are missing. Memory scopes differ. B2 p.9 labels the RTX 3070 result DORADO-004; the repository retains DORADO-006 following P. No sustained streaming claim follows from short stage throughput.

## Next Steps

Pin model/input hashes and environments, repeat larger compatible workloads, and collect full-command timing, scoped memory/power and reference-based quality. Preserve platform-specific setup costs.

## Supporting Experiments and Evidence

[DORADO-001](../experiments/DORADO-001.md) · [DORADO-002](../experiments/DORADO-002.md) · [DORADO-003](../experiments/DORADO-003.md) · [DORADO-004](../experiments/DORADO-004.md) · [DORADO-005](../experiments/DORADO-005.md) · [DORADO-006](../experiments/DORADO-006.md).

B2 pp.7–10; W pp.7–11. [Source conflicts](../docs/sources.md) · [Reproduction](../resources/reproduce.md).
