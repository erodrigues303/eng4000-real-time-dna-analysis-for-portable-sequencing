# socall-private

Generated from `socall-private.json`; edit the JSON and rerun the renderer.

| Field | Recorded value |
|---|---|
| model id | socall-private |
| basecaller | SoCall |
| full model name | TBD — needs verification |
| architecture | TBD — needs verification |
| layers blocks | TBD — needs verification |
| parameter count | TBD — needs verification |
| numerical precision | FP32 weights as supplied (all floating-point tensors FP32, checked E); int8/fixed-point is the project target and quantization is project work (S) |
| decoder | TBD — needs verification |
| framework runtime | Intended embedded NVIDIA Jetson target; verified runtime TBD |
| target chemistry | R9.4.1 (supervisor recollection, S) |
| sampling rate hz | 4000 |
| chunk input assumptions | 4800 samples, no overlap (supervisor recollection, S); training normalization undocumented, per-read median/MAD works for inference (S, E) |
| training data | TBD — needs verification |
| weights source | Supplied privately by the supervisor (handoff prepared 2026-11-05); not redistributed |
| weights sha256 | 7e91b61ab5b89318c02c13fd65686dff067863366d6bdf0363b16cc43081e1fa |
| status | planned-private |
| provenance | ["U", "P pp.4,20", "S", "E", "M"] |
| limitations | ["Preliminary reference-accuracy baseline on a laptop (SOCALL-001/002, D5) and preliminary embedded throughput/power baseline on the reflashed TX2 (SOCALL-003-005, D1, FP32); no embedded accuracy baseline on matching-chemistry data yet.", "Publication permission unconfirmed: no code, weights or unpublished architecture exposed.", "Chemistry, sample rate and chunk size come from the supervisor's recollection; training data and normalization are undocumented."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
