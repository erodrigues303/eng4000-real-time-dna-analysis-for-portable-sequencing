# R10.4.1 training-data status

**No suitable R10.4.1 training corpus has been selected and verified in the project records.** [D1](../datasets/D1.md) is a small human DeepMod2 tutorial sample with Dorado-detected R10.4.1 chemistry; it is not an established training corpus. D4/D5 are historical R9.4-labelled inputs. D2 chemistry and D3 simulation parameters remain incomplete.

## What must be established

Record a raw-signal source, pore/motor/sampling conditions, reference or training labels, accession and file hashes, licensing, specimen provenance, and a documented training/validation/test split. A sequence-only archive does not establish that raw signal is available for training. Avoid specimen/read overlap and assess possible overlap with pretrained-model data.

The weekly log describes Bonito's training-data preparation interface, but neither a command description nor a model configuration establishes that a suitable corpus was acquired or validated. See the [dataset catalogue](../datasets/index.md) and [reference-accuracy protocol](../docs/methodology.md#correctness-and-reference-accuracy).

## Next deliverable

A reviewed dataset card with verified signal and reference access, chemistry, licence and partitioning. The website intentionally leaves this as open research rather than relabelling existing smoke-test inputs as training data.
