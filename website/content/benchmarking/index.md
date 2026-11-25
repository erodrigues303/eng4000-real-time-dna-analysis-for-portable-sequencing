# Basecaller Benchmarking

Technical investigations into nanopore basecalling performance, accuracy, energy efficiency, and embedded execution.

## Technical Investigations

---

### Phase 1 — Basecaller Exploration & Initial Benchmarking

*September 28 – November 6, 2026*
{: .benchmark-phase-date }

> #### Basecaller Exploration & Feasibility
>
> | Investigation | Scope |
> |---|---|
> | [Initial Basecaller Setup and Evaluation](initial-basecaller-setup.md) | Dorado and DeepNano-Blitz execution; Bonito and DeepNano-Coral compatibility review |
>
> #### Hardware Performance & Energy Efficiency
>
> | Investigation | Scope |
> |---|---|
> | [Dorado Cross-Platform Performance](hardware-throughput.md) | CPU, CUDA, and Metal performance across available hardware |
> | [DeepNano-Blitz CPU Scaling and Energy Efficiency](cpu-parallelism.md) | CPU thread scaling, runtime, memory, and energy efficiency |
> | [Jetson TX2: ARM64 Port and Embedded CPU Baseline](embedded-feasibility.md) | ARM64 port, embedded CPU performance, and module-input power |
>
> #### Model Configuration & Pipeline Evaluation
>
> | Investigation | Scope |
> |---|---|
> | [Dorado Model Configuration and Performance Tradeoffs](dorado-model-configuration.md) | Fast versus HAC performance and accuracy; modified-base overhead |
> | [POD5 vs BLOW5: Input Pipeline Performance](pipeline-overhead.md) | Input pipeline timing, memory, power, and energy comparisons |

---

### Phase 2 — Expanded Benchmarking & Validation

*November 7 – December 23, 2026*
{: .benchmark-phase-date }

> #### Basecaller Accuracy & Validation
>
> | Investigation | Scope |
> |---|---|
> | [DeepNano-Blitz vs SoCall: Reference Accuracy on D5](d5-accuracy.md) | Reference-based mapping and sequence identity evaluation on D5 |

---