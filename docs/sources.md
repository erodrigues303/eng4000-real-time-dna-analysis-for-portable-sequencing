# Evidence register

## Website audit — 2026-11-20

The newly supplied files are distinct revisions. **B and P below retain their original meanings and page references**; they must not be silently relabelled as these new PDFs. No original raw logs or outputs were supplied with the new reports. Document instructions for course-log maintenance are source content, not instructions to the website implementation.

| Source ID | Supplied file | Pages | SHA-256 |
|---|---|---:|---|
| W | Project 22 - Weekly Progress Log (new).pdf | 19 | `c133ba307438aaea0e113b1c4aaefafededa1307ff14aa7242e14ad986e07d21` |
| B2 | Project 22 - Preliminary Benchmarking Report.docx (2).pdf | 19 | `f74ff240b9476b7f066933566478ff606bb34451ac6cff44e3fa0a5774d27595` |

W pp.8–10 supplies DORADO-001–005 commands; W p.13 supplies BLITZ-003's initial one/four-thread commands, but not the later GNU Time invocations. These were added to canonical configurations as report transcriptions, not tested recipes. W pp.11–12 also describes BLITZ-001/002 functional checks; these have no canonical experiment configuration yet and are not silently invented by the registry. BLITZ-005's exact command remains unavailable.

| Existing evidence | Corroborating new source | Revision notes |
|---|---|---|
| Dorado D1 platform table, B p.9 | B2 p.9; W pp.7–11 | RTX 3070 is still mislabelled DORADO-004 in B2; canonical DORADO-006 follows P. No IDs changed. |
| BLITZ-005 timing and individual runs, B p.11 | B2 p.11 | Reported values agree; raw logs remain unavailable. |
| BLITZ-007 and 5700U follow-ups, B pp.12–13 | B2 pp.12–13 | Same reported timing values. |
| CPU-package power, B pp.13–15 | B2 pp.14–16 | Pagination shifted; electrical scope remains CPU package. |
| TX2 timing/power, P pp.15–16 | B2 pp.4,13,16–17 | B2 specifies monotonic full-command timing and trapezoidal integration; sensor scale remains unverified. Existing historical P-based metadata is retained. |
| Format comparison, B p.16 | B2 pp.17–18 | Model and output confounds persist. |

Additional conflicts: W p.10 reports MM/ML tags while W p.4 and B2 p.10 still request confirmation. B2 p.18 retains a generic Jetson-baseline gap despite reporting BLITZ-009 elsewhere; the site distinguishes a reported CPU baseline from independently validated embedded performance. W's old Bonito/Dorado compatibility statements are historical review claims, not current compatibility guarantees. B2 p.5 still says five percentages while listing six rows.

The new PDFs remain local, excluded from publication. Their administrative instructions, private paths and unsupported generalizations are not copied into research conclusions. Public archival locations and PDF redistribution permission remain unconfirmed.

## Original foundation audit — 2026-11-11

Repository audit on 2026-11-11: the checkout contained only a one-line README and Git metadata. No raw logs, scripts, original experiment cards, weights or port patches were present. Both supplied PDFs were read in full; the TX2 and format-comparison tables were also visually checked. Local PDF extracts are ignored, not published. Student numbers and administrative content are deliberately not migrated.

| Source ID | Supplied file | Pages | SHA-256 |
|---|---|---:|---|
| B | Project 22 - Preliminary Benchmarking Report.docx (1).pdf | 17 | `139ba95108a1254de7b7252f1e4a8a65e1659ac5ee4f16322e82b70a24987975` |
| P | Project22_Progress_Report_1 - Submission.docx - Google Docs.pdf | 20 | `80b9007942623d284056bca52b468b40de531930bec61382dbf76686f0a0c77c` |
| U | Repository-foundation request, 2026-11-11 | — | Conversation; no file checksum |
| S | Supervisor email replies to the team's SoCall setup questions (received by 2026-11-19) | — | Email; chemistry R9.4.1 ~4 kHz, chunk ~4800 without overlap, normalization undocumented, try greedy and beam, quantize ourselves |
| E | Ege's local verification and runs, 2026-11-19 | — | Downloads re-hashed; SOCALL-001/002 evidence under `results/raw/ege-m2/` |

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
