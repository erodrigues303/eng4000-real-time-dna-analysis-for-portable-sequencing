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
| framework runtime | PyTorch 1.10.0 FP32 on the NVIDIA Jetson TX2 GPU (JetPack 4.6.6), verified on D1 and D5 (SOCALL-004, SOCALL-010, SOCALL-011); Apple M2 MPS for the reference pipeline (SOCALL-001/002) |
| target chemistry | R9.4.1 (supervisor recollection, S) |
| sampling rate hz | 4000 |
| chunk input assumptions | 4800 samples, no overlap (supervisor recollection, S); training normalization undocumented, per-read median/MAD works for inference (S, E) |
| training data | TBD — needs verification |
| weights source | Supplied privately by the supervisor (handoff prepared 2026-11-05); not redistributed |
| weights sha256 | 7e91b61ab5b89318c02c13fd65686dff067863366d6bdf0363b16cc43081e1fa |
| status | planned-private |
| provenance | ["U", "P pp.4,20", "S", "E", "M", "T"] |
| limitations | ["Preliminary reference-accuracy baselines on a laptop (SOCALL-001/002, D5) and on the reflashed TX2 GPU (SOCALL-011, D5, FP32), plus TX2 throughput/power on D1 (SOCALL-003 to 010); greedy only on the TX2, no beam-search run there yet.", "Publication permission unconfirmed: no code, weights or unpublished architecture exposed.", "Chemistry, sample rate and chunk size come from the supervisor's recollection; training data and normalization are undocumented."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
