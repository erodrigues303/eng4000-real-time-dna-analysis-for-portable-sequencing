# Evidence register

Repository audit on 2026-11-11: the checkout contained only a one-line README and Git metadata. No raw logs, scripts, original experiment cards, weights or port patches were present. Both supplied PDFs were read in full; the TX2 and format-comparison tables were also visually checked. Local PDF extracts are ignored, not published. Student numbers and administrative content are deliberately not migrated.

| Source ID | Supplied file | Pages | SHA-256 |
|---|---|---:|---|
| B | Project 22 - Preliminary Benchmarking Report.docx (1).pdf | 17 | `139ba95108a1254de7b7252f1e4a8a65e1659ac5ee4f16322e82b70a24987975` |
| P | Project22_Progress_Report_1 - Submission.docx - Google Docs.pdf | 20 | `80b9007942623d284056bca52b468b40de531930bec61382dbf76686f0a0c77c` |
| U | Repository-foundation request, 2026-11-11 | — | Conversation; no file checksum |

B is referenced as November 2026 by P p.20; its own exact issue date is unknown. P is submitted November 6, 2026. Page references use physical PDF pages. Original PDFs remain with the team; repository-accessible archival location and publication permission are TBD. Request them by exact filename and checksum. The underlying weekly progress log, appendices cited by B and dated raw folders are not supplied. Report transcriptions are secondary evidence, never reconstructed raw telemetry.

## Reconciliation decisions

| Conflict / gap | Treatment |
|---|---|
| B pp.8–9 calls RTX 3070 runs DORADO-001/002 or DORADO-004; P p.13 calls it DORADO-006 | Use DORADO-006 as the canonical repository ID following P; preserve aliases and require original-card confirmation. |
| B pp.8,17 says no Jetson benchmark; P pp.15–16 documents BLITZ-009 | Retain the newer TX2 result; do not repeat the older absence claim. |
| P pp.7,19 suggests ARM64 Dorado should run on Jetson; P p.20 and U require older/non-Dorado paths on TX2 | No current-Dorado-on-TX2 support claim. Exact compatible release/build remains TBD. |
| P repeatedly says SoCall unavailable, but P p.20 says model/weights provided; U confirms provision | Access has been reported; baseline and publication permission remain unestablished. No private implementation details or weights copied. |
| P pp.9,12 says only non-human data; B p.6 identifies D1 as human | Preserve D1's historical use, flag the policy conflict. Future dataset policy/licensing needs team resolution; do not relabel D1. |
| B pp.11–12 has Blitz per-experiment warm-up detail; P p.13 generalizes a warm-up to all Blitz | Prefer specific records. BLITZ-003 includes its slow first run; warm-up is unknown there. |
| P pp.11–12 mixes planned harness features with language implying completed checks | No harness existed in checkout; do not claim automation or tests were delivered historically. |
| B p.5 says “five” percentages but contains six rows | Retain all six rows without silently dropping RTX 3070. |
| B p.16 format comparison uses HAC v6 vs v5 and BAM vs FASTQ | Confounded exploratory comparison, not an isolated file-format effect. Do not merge its 1.294 s Dorado row with DORADO-003's 1.401 s. |
| B p.10 says modified-base tags reported but confirmation outstanding | MM/ML presence remains unverified. |
| B reports retained raw artifacts, but none are supplied | List expected evidence; no invented raw files, hashes, commands or per-run values. |

Detailed gaps and suggested issues: [gaps](gaps.md). External methodology references inform future design only, not historical measurements.
