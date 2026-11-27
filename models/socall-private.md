# socall-private

Generated from `socall-private.json`; edit the JSON and rerun the renderer.

| Field | Recorded value |
|---|---|
| model id | socall-private |
| basecaller | SoCall |
| full model name | TBD — needs verification |
| architecture | Fully convolutional 1D CNN with a CTC output head (no recurrent or attention layers); 5 convolution blocks (Conv1d + BatchNorm + ReLU, dropout 0.05 in training) then a 1x1 Conv1d decoder and log-softmax over blank/A/C/G/T; total stride 3 (one output step per 3 signal samples); receptive field 219 samples (E) |
| layers blocks | Conv1d 1→48 k9 stride 3 · 48→104 k13 · 104→80 k27 · 80→64 k25 · 64→48 k9 (each with BatchNorm eps 1e-3 and ReLU) · decoder 48→5 k1; ~445,856 multiply-adds per output step, ~148,600 per input sample; the 104→80 k27 layer is about half the compute (E) |
| parameter count | 446893 |
| numerical precision | FP32 weights as supplied (all floating-point tensors FP32, checked E); an FP16 variant (BatchNorm folded, log-softmax in FP32) is within the 0.1-point accuracy budget on D5 through PyTorch (SOCALL-016) and as a TensorRT FP16 engine (SOCALL-021); int8/fixed-point is the project target and quantization is project work (S) |
| decoder | CTC, no decoder supplied with the model: project implementations of greedy CTC and CTC beam search (fast-ctc-decode, beam 5) (S, E) |
| framework runtime | PyTorch 1.10.0 on the NVIDIA Jetson TX2 GPU (JetPack 4.6.6), FP32 verified on D1 and D5 (SOCALL-004, SOCALL-010, SOCALL-011); BatchNorm-folded FP32 and FP16 variants measured on D1 and D5 (SOCALL-012 to 016); TensorRT 8.2.1 FP32 and FP16 engines built from an ONNX opset 13 export of the folded model, measured on D1 and D5 (SOCALL-017 to 021); Apple M2 MPS for the reference pipeline (SOCALL-001/002) |
| target chemistry | R9.4.1 (supervisor recollection, S) |
| sampling rate hz | 4000 |
| chunk input assumptions | 4800 samples, no overlap (supervisor recollection, S); training normalization undocumented, per-read median/MAD works for inference (S, E) |
| training data | TBD — needs verification |
| weights source | Supplied privately by the supervisor (handoff prepared 2026-11-05); not redistributed |
| weights sha256 | 7e91b61ab5b89318c02c13fd65686dff067863366d6bdf0363b16cc43081e1fa |
| status | planned-private |
| provenance | ["U", "P pp.4,20", "S", "E", "M", "T"] |
| limitations | ["Preliminary reference-accuracy baselines on a laptop (SOCALL-001/002, D5) and on the reflashed TX2 GPU (SOCALL-011, SOCALL-015, SOCALL-016, SOCALL-020, SOCALL-021, D5), plus TX2 throughput/power on D1 (SOCALL-003 to 014, SOCALL-017 to 019); greedy only on the TX2, no beam-search run there yet.", "Source code, weights, the ONNX export and the TensorRT engines are not redistributed; the architecture above is summarized from the supplied model definition so the work can be followed.", "Chemistry, sample rate and chunk size come from the supervisor's recollection; training data and normalization are undocumented."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
