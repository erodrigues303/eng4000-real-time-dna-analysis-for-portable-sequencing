# blitz-network64

Generated from `blitz-network64.json`; edit the JSON and rerun the renderer.

| Field | Recorded value |
|---|---|
| model id | blitz-network64 |
| basecaller | DeepNano-Blitz / deepnano2 0.1 |
| full model name | Supplied network 64 |
| architecture | Optimized recurrent neural network (RNN) |
| layers blocks | TBD — needs verification |
| parameter count | TBD — needs verification |
| numerical precision | Floating point reported; exact storage/compute types TBD |
| decoder | Beam size 5 in recorded CPU tests; complete decoder implementation TBD |
| framework runtime | Python/Rust; x86 MKL path; TX2 owned ARM64 math-library port |
| target chemistry | Designed for older R9.4 per P p.7; exact supported subrevision/motor TBD |
| sampling rate hz | TBD — needs verification |
| chunk input assumptions | FAST5 input; network 64; OMP_NUM_THREADS=1 in desktop follow-ups; chunk/overlap TBD |
| training data | TBD — needs verification |
| weights source | Supplied network in Blitz repository; commit 15bd04b94c291debac75823811a2c86820dda589 documented for Brian follow-up build |
| weights sha256 | TBD — needs verification |
| status | historical-preliminary |
| provenance | ["B pp.7,11–12", "P pp.7,15"] |
| limitations | ["Network 64 is a model selector, not a verified parameter or layer count.", "Weight checksum and exact model/port identity on TX2 need verification.", "Historical acquisition model names in FAST5 metadata are not this neural network."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
