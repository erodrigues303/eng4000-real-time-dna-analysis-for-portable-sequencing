<p class="eyebrow">Benchmarking study · Exploratory</p>

# How does the execution platform affect throughput?

The D1 Dorado measurements show substantial platform differences within the reported basecalling interval. They do not isolate GPU generation from host configuration, backend or automatic batching.

## Experimental design

The records name Dorado 2.1.2, [HAC v6.0.0](../models/dorado-hac-v6.md) and [D1](../datasets/D1.md), a 59-read DeepMod2 POD5 sample. CPU, CUDA and Metal execute on different systems. Repetition, cache state and complete environment identity are not established consistently.

## Results and interpretation

[The reported platform table](../evidence/index.md#dorado-d1) gives **53.213 s** on GTX 1060, **4,216.234 s** on Ryzen 5 1500X CPU and **1.401 s** on RTX 4070. These are tool-reported stage measurements. The RTX 4070 command took approximately **12 s**, demonstrating why setup and basecalling must be timed separately. Source: B/B2 p.9; W pp.8–9.

The M2 and RTX 3070 Mobile observations add platform coverage, but do not make this a controlled accelerator ranking. Modified-base calling changes the workload; its result must remain separate from the baseline.

## Limitations

D1 is very small. Automatic batch sizes and host systems differ, biological accuracy is unverified, and power boundaries are incomplete. The RTX 3070 record has conflicting historical IDs: the repository retains DORADO-006 while B2 p.9 labels it DORADO-004. [Conflict register](../docs/sources.md).

## Next investigation

Pin model and input hashes, archive runtime environments, use larger compatible inputs, repeat full-command and stage measurements, and pair performance with reference-based quality.

## Supporting experiments and reproduction

[DORADO-001](../experiments/DORADO-001.md) · [DORADO-002](../experiments/DORADO-002.md) · [DORADO-003](../experiments/DORADO-003.md) · [DORADO-004](../experiments/DORADO-004.md) · [DORADO-005](../experiments/DORADO-005.md) · [DORADO-006](../experiments/DORADO-006.md)

[Report-transcribed commands and reproduction limits](../resources/reproduce.md).
