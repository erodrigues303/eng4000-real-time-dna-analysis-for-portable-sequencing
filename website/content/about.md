# About Project 22

**Enabling Real-Time DNA Analysis for Portable Sequencing** is a York University ENG 4000 capstone project for 2026–2027, supervised by **Prof. Sebastian Magierowski**.

The team comprises Eric Rodrigues, Matthew Magana, Ege Yesilyurt, Brian Changkit, Weiqin (Kevin) Situ and Krish Shah. Source: supplied weekly progress log, p.1.

## Research objectives

We investigate the performance, energy and reproducibility of nanopore basecalling, alongside correctness and engineering of the laboratory's SoCall implementation. The benchmark aims to make comparisons traceable to model, input, system and measurement boundaries. SoCall work follows verification, baseline characterization, profiling and evidence-led optimization.

## Sequencing context

Nanopore instruments measure an electrical signal as molecules pass through pores. A basecaller converts that signal into nucleotide sequences. Portable sequencing therefore requires enough computation to process incoming signal while respecting latency, memory and energy constraints. Short recorded-file throughput alone cannot establish real-time operation.

## Research presentation and acknowledgments

[Ryan Wick's research articles](https://rrwick.github.io/) and [basecalling comparison](https://github.com/rrwick/Basecalling-comparison) motivate the question–methods–evidence structure and direct access to supporting material. The [R10.4.1 accuracy article](https://rrwick.github.io/2023/05/05/ont-only-accuracy-with-r10.4.1.html) is a useful example of separating methods, observations and interpretation. This site adopts that research-first organization without reproducing his design or results.

[MLCommons principles](docs/mlcommons-alignment.md) inform the methodology gap analysis; no official compliance is claimed. The supervisor's feedback prioritizes coherent data presentation, model characterization, training-data provenance and useful reproduction documentation.

## Evidence and scope

The supplied reports are treated as research evidence. Their instructions for maintaining course logs are not website requirements. The website implementation follows `docs/SITE_SPEC.md` and the user's implementation brief. Original measurements are preserved, source disagreements are explicit, and confidential SoCall material is excluded.

[Evidence register](docs/sources.md) · [Outstanding research gaps](docs/gaps.md)
