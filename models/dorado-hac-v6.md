# dorado-hac-v6

Generated from `dorado-hac-v6.json`; edit the JSON and rerun the renderer.

| Field | Recorded value |
|---|---|
| model id | dorado-hac-v6 |
| basecaller | Dorado 2.1.2 |
| full model name | dna_r10.4.1_e8.2_400bps_hac@v6.0.0 |
| architecture | Source-review notes describe flstm_softout and CRF; complete architecture unverified |
| layers blocks | 7 flstm_softout layers reported; other blocks TBD |
| parameter count | TBD — needs verification |
| numerical precision | Floating point reported in P p.7; exact storage/compute precision per backend TBD |
| decoder | CRF state_len 4 reported; decoder algorithm/settings TBD |
| framework runtime | Dorado CPU / CUDA / Metal tested |
| target chemistry | R10.4.1 / E8.2 / 400 bps |
| sampling rate hz | TBD — needs verification |
| chunk input assumptions | DORADO-003: chunk size 12288, batch size 896 (automatic); other settings TBD |
| training data | TBD — needs verification |
| weights source | ONT Dorado; exact download artifact/hash TBD |
| weights sha256 | TBD — needs verification |
| status | historical-preliminary |
| provenance | ["B pp.7,9", "P p.7"] |
| limitations | ["~5 kHz model condition; dataset sampling metadata unverified.", "Parameter count, complete architecture and backend precision need pinned model inspection."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
