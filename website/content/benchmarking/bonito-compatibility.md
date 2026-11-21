---
title: "Bonito Compatibility Assessment for Jetson TX2"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# Bonito Compatibility Assessment for Jetson TX2

## Objective

Determine whether the reviewed Bonito software stack provides a practical execution/training path on the project's Jetson TX2.

## Work Performed

The team reviewed Bonito v1.1.0, model configurations, CRF decoding and training-data interfaces. The reviewed CUDA/ont-koi dependency path was excluded from the current TX2 execution plan. The supplied reports establish source review, not a completed Bonito performance test.

### Investigation history

| Addition | Technical contribution | Evidence |
|---|---|---|
| 14 Oct 2026 | Assessed platform requirements and documented candidate training-data preparation | W pp.5,16; B2 p.7 |

BONITO-001 is proposed future work in the source material, not an executed experiment record.

## Experimental Setup / Methodology

The historical review examined Bonito's dependency packaging and CUDA-only CRF path. W p.16 records an x86_64 Linux ont-koi wheel and no CPU fallback in the reviewed path. TX2 is ARM64 with an older installed stack. This assessment is version- and environment-specific, not a claim that every possible port or future Bonito release is unusable.

## Results

| Item reviewed | Recorded outcome |
|---|---|
| Reviewed software | Bonito v1.1.0 |
| Dependency/backend | ont-koi CUDA CRF path; reviewed wheel targets Linux x86_64 |
| Current TX2 path | No compatible, executed configuration established; excluded from baseline plan |
| Performance and accuracy | Not measured |
| Training-data interface | Reviewed; no verified R10.4.1 training corpus established |

Source: W p.16, B2 p.7; [evidence register](../docs/sources.md).

## Findings and Interpretation

The compatibility review redirected embedded baseline work toward an executable ARM64 CPU path, documented in [Blitz on TX2](embedded-feasibility.md). Bonito's research/training interfaces remain relevant to future model work, but source-level knowledge is not benchmark evidence.

## Limitations

No Bonito runtime, output validation or Jetson build artifact was supplied. Historical package observations do not prove permanent incompatibility. The review also does not establish current Dorado support on TX2.

## Next Steps

If Bonito is revisited, pin the release and dependency sources, demonstrate a compatible build and correctness check, then register a measured experiment. Continue SoCall verification and embedded baseline work independently.

## Supporting Experiments and Evidence

W pp.5,16; B2 p.7; [source register](../docs/sources.md), [Jetson platform notes](../docs/platforms/jetson-tx2.md), [training-data status](../resources/training-data.md). There is no measured BONITO experiment to link.
