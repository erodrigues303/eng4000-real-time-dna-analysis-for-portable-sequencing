---
title: "Dorado GPU Acceleration: CPU and CUDA Baselines"
---
<p class="eyebrow">Technical investigation · Preliminary record</p>

# Dorado GPU Acceleration: CPU and CUDA Baselines

## Objective

Quantify the computational benefit of CUDA execution and the additional cost of modified-base calling, while separating inference-stage measurements from command overhead.

## Work Performed

The team ran D1/HAC on the Ryzen 5 1500X CPU and GTX 1060, then measured an RTX 4070 baseline and its modified-base companion. B2 pp.9–10 reports approximately 79.2× shorter GPU stage runtime for GTX 1060 versus the CPU and 8.21% additional stage time for the RTX 4070 modified-base run.

### Investigation history

| Addition | Technical contribution | Record |
|---|---|---|
| 14 Oct 2026 | Added newer GPU baseline and modified-base comparison | [DORADO-003](../experiments/DORADO-003.md), [DORADO-004](../experiments/DORADO-004.md) |
| 8 Oct 2026 | Completed CPU/GPU reference pair | [DORADO-002](../experiments/DORADO-002.md), [DORADO-001](../experiments/DORADO-001.md) |

## Experimental Setup / Methodology

Dorado 2.1.2, D1 and HAC v6.0.0 are fixed by name. GTX 1060 and CPU results use the same reported host; RTX 4070 uses a different host and automatic batching. DORADO-004 adds the matched 5mCG/5hmCG companion model. Timings are single reported basecalling intervals.

## Results

| Record | Execution | Stage time (s) | Source |
|---|---|---:|---|
| DORADO-002 | Ryzen 5 1500X CPU | 4,216.234 | [Canonical table](../evidence/index.md#dorado-d1) |
| DORADO-001 | GTX 1060 CUDA | 53.213 | [Canonical table](../evidence/index.md#dorado-d1) |
| DORADO-003 | RTX 4070 CUDA | 1.401 | [Canonical table](../evidence/index.md#dorado-d1) |
| DORADO-004 | RTX 4070 CUDA + modified bases | 1.516 | [Canonical table](../evidence/index.md#dorado-d1) |

## Findings and Interpretation

CUDA substantially reduces reported stage time on this workload. The RTX 4070 versus GTX 1060 comparison also changes host and tuning settings, so it does not isolate GPU generation. Modified-base overhead is 0.115 s in this short run; throughput reduction and runtime increase use different denominators. No Jetson GPU or SoCall speedup was measured.

## Limitations

Small input, single runs and setup/autotuning limit generalization. MM/ML tag presence is reported but confirmation is still outstanding. Modified-base biological accuracy and sustained overhead are unestablished.

## Next Steps

Repeat with larger inputs and archived tuning settings, time transfers/inference/decoding separately and validate modified-base output. Evaluate any Jetson CUDA path only after verifying software compatibility and correctness.

## Supporting Experiments and Evidence

[DORADO-001](../experiments/DORADO-001.md) · [DORADO-002](../experiments/DORADO-002.md) · [DORADO-003](../experiments/DORADO-003.md) · [DORADO-004](../experiments/DORADO-004.md). B2 pp.9–10; [sources](../docs/sources.md). [Cross-platform report](hardware-throughput.md) retains the broader platform and memory record.
