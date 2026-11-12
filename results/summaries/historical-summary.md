# Historical results — preliminary report transcriptions

Generated from `report-observations.json`; no new benchmark runs or raw telemetry are represented. All numerical precision is retained as reported. [Evidence register](../../docs/sources.md).

## Dorado 2.1.2 HAC v6 on D1 (59 reads)

Source: B p.9; P p.13. Status: preliminary-report-transcription.

Single-run tool-reported basecalling stage. Exact timing boundaries unverified; RTX 4070 total command ~12 s. DORADO-006 ID follows P; B aliases conflict. Capacity uses fixed 2,560,000 samples/s, not measured live performance.

| Experiment | Hardware | Time (s) | Samples/s | Reported capacity (%) |
|---|---|---|---|---|
| DORADO-001 | GTX 1060 | 53.213 | 525,235 | 20.52 |
| DORADO-002 | Ryzen 5 1500X | 4,216.234 | 6,628.981 | 0.26 |
| DORADO-003 | RTX 4070 | 1.401 | 19,949,560 | 779.28 |
| DORADO-004 | RTX 4070 + modifications | 1.516 | 18,436,240 | 720.17 |
| DORADO-005 | M2 Metal | 246.9 | ~113,217 | 4.42 |
| DORADO-006 | RTX 3070 Mobile | 7.6 | 3,663,565 | 143.11 |

## Dorado memory and output summaries

Source: B p.9. Status: preliminary-report-transcription.

These scopes are not interchangeable. MB/GB units and the report’s approximate conversions are preserved; do not interpret model tuning allocation as standardized peak RSS. Predicted Q is not reference accuracy.

| Experiment | Reported observation |
|---|---|
| DORADO-001 | 2,896 MB (approximately 2.83 GB in report; unit convention unverified) |
| DORADO-003 | ~7.5 GB model memory during tuning; batch 896, chunk 12288 |
| DORADO-004 | Peak memory not measured |
| DORADO-005 | 4.1 GB reported peak; scope/method TBD; median Q 20.4 (10.3–23.5), median length 30,983 bases, total output 2.0 Mb |

## Exploratory Fast/HAC comparisons on Apple M2

Source: B p.10. Status: preliminary-report-transcription.

Exact tool builds, models, commands and timing boundaries unverified. D3 reference/scoring undefined; D2 predicted Q is not empirical accuracy. No total signal counts.

| Dataset | Tier | Time (s) | Quality / accuracy |
|---|---|---|---|
| D2 (4,000 reads) | Fast | 11 | Median predicted Q 12.3 |
| D2 (4,000 reads) | HAC | 1,164 | Median predicted Q 19.8 |
| D3 (200 simulated reads) | Fast | 2.8 | Reported accuracy 86.7% |
| D3 (200 simulated reads) | HAC | 242 | Reported accuracy 92.6% |

## BLITZ-003: initial 5700U D4 thread comparison

Source: B p.11. Status: preliminary-report-transcription.

Three paired measurements; first slow run retained, no established excluded warm-up. All 48 IDs/sequences/qualities match. Mean speedup 2.60×. Original samples/s not reported; do not retroactively label later sample counts as original observations.

| Run | 1 thread (s) | 4 threads (s) | Peak MiB 1 / 4 |
|---|---|---|---|
| 1 | 48.232 | 17.340 | Not measured |
| 2 | 29.600 | 12.060 | 118.11 / 102.01 |
| 3 | 27.740 | 11.250 | 118.41 / 109.64 |
| Mean | 35.191 | 13.550 | No pooled peak |
| Diagnostic single-thread | 29.20 and 29.16 | — | — |

## BLITZ-004: 7800X3D D4 baseline

Source: B p.11. Status: preliminary-report-transcription.

48 reads each; byte-identical repeated FASTQ reported. Warm-up for this specific baseline needs confirmation.

| Run | Wall time (s) |
|---|---|
| 1 | 15.22 |
| 2 | 14.87 |
| 3 | 14.95 |
| Reported mean ± SD | 15.01 ± 0.18 |

## BLITZ-005: 7800X3D D4 scaling

Source: B p.11. Status: preliminary-report-transcription.

One excluded warm-up and three measured runs per setting; all 12 outputs match by ID/sequence/quality. Full-command GNU Time; highest peak RSS among runs.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) | Per-run wall times (s) | CPU utilization |
|---|---|---|---|---|---|---|
| 1 | 15.187 ± 0.114 | 594,828 | 1.00× | 119.29 | 15.06 / 15.28 / 15.22 | 99% |
| 2 | 8.053 ± 0.256 | 1,121,704 | 1.89× | 109.38 | 7.76 / 8.17 / 8.23 | 198% |
| 4 | 4.403 ± 0.061 | 2,051,504 | 3.45× | 109.98 | 4.35 / 4.39 / 4.47 | 375–377% |
| 8 | 2.917 ± 0.006 | 3,097,184 | 5.21× | 108.98 | 2.91 / 2.92 / 2.92 | 701–706% |

## BLITZ-007: 7800X3D D5 larger workload, eight threads

Source: B p.12. Status: preliminary-report-transcription.

One excluded warm-up; 4,467 reads / 1,290,238,981 samples each run; all outputs match. Reported mean rate 4,092,013 samples/s, 199.81% of 4 kHz target and 159.84% of fixed 5 kHz target. Recorded input, not live streaming.

| Run | Wall time (s) | Peak RSS (MiB) | CPU utilization |
|---|---|---|---|
| 1 | 315.23 | 169.66 | 798% |
| 2 | 315.99 | 166.26 | 798% |
| 3 | 314.70 | 167.73 | 798% |
| Mean ± SD | 315.31 ± 0.65 | Highest peak 169.66 | 798% each |

## 5700U follow-up D4 scaling, 2026-10-25

Source: B p.12. Status: preliminary-report-transcription.

Unnumbered follow-up, separate from BLITZ-003. One excluded warm-up plus three measured runs per setting. All outputs match.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) |
|---|---|---|---|---|
| 1 | 19.953 ± 0.545 | 452,729 | 1.00× | 118.29 |
| 2 | 10.873 ± 0.337 | 830,790 | 1.84× | 105.30 |
| 4 | 7.050 ± 0.523 | 1,281,341 | 2.83× | 108.44 |
| 8 | 5.503 ± 0.475 | 1,641,451 | 3.63× | 106.70 |

## 5700U extended D4 scaling

Source: B pp.12–13. Status: preliminary-report-transcription.

Unnumbered follow-up. One excluded warm-up plus 30 measured runs per setting; 120 outputs match and exit 0. Reported rates retained as printed; rounded means alone do not reconstruct all rates.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) |
|---|---|---|---|---|
| 1 | 22.344 ± 2.602 | 404,005 | 1.00× | 118.39 |
| 2 | 12.748 ± 0.518 | 707,791 | 1.75× | 109.27 |
| 4 | 7.676 ± 0.486 | 1,174,570 | 2.91× | 110.25 |
| 8 | 5.357 ± 0.276 | 1,681,417 | 4.17× | 110.04 |

## Historical Dorado power

Source: B p.13; P p.14. Status: preliminary-report-transcription.

Instrument, electrical scope and timing-window alignment remain TBD. Do not derive energy by multiplying these averages by stage time.

| Configuration | Average W | Peak W |
|---|---|---|
| Ryzen 5 1500X CPU | 32.34 | 55.63 |
| GTX 1060 | 95.91 | 120.00 |
| RTX 4070 | 110.3 | 172.19 |
| RTX 4070 modified | 133.7 | 188.80 |

## Blitz CPU package energy sessions

Source: B pp.13–15. Status: preliminary-report-transcription.

HWiNFO64 ~2.01 s sampling; UTC alignment, interpolation and trapezoidal integration. Single independent power session per configuration; no whole-system energy. D4 ×30 = 271,003,620 samples / 1,440 read instances, not distinct reads. Separate from timing-only experiments.

| Record / system | Threads | Workload | Duration (s) | Avg / sampled peak W | Energy (J) | Samples/J | Reported samples/s |
|---|---|---|---|---|---|---|---|
| BLITZ-006 / 7800X3D | 8 | D4 ×30 | 77.32 | 64.48 / 70.13 | 4,986 | 54,358 | 3,504,778 |
| BLITZ-008 / 7800X3D | 8 | D5 | 319.60 | 70.18 / 71.52 | 22,430 | 57,524 | 4,037,003 |
| 5700U separate session | 4 | D4 ×30 | 245.31 | 21.63 / 22.73 | 5,306 | 51,072 | 1,104,720 |

## 5700U thread-scaling CPU package energy

Source: B p.15. Status: preliminary-report-transcription.

One continuous power session; 30 processes per thread setting after an excluded warm-up. Every setting processes 271,003,620 signal samples. Not independent energy replicates.

| Threads | Duration (s) | Avg / sampled peak W | Energy (J) | Samples/J |
|---|---|---|---|---|
| 1 | 670.79 | 19.47 / 24.33 | 13,061 | 20,749 |
| 2 | 382.89 | 21.71 / 22.88 | 8,311 | 32,607 |
| 4 | 230.73 | 21.61 / 23.07 | 4,985 | 54,362 |
| 8 | 161.18 | 21.58 / 22.73 | 3,479 | 77,907 |

## BLITZ-009: TX2 CPU D4 baseline

Source: P pp.13,15–16, Table 14. Status: preliminary-report-transcription.

2026-11-05; one warm-up, three measured runs per setting. All 12 outputs reportedly match. Full-command timing; INA3221 VDD_IN module-input power ~0.5 s sampling. SENSOR SCALING UNVERIFIED; watts/joules/efficiency provisional. Capacity uses 2,048,000 samples/s. Memory/utilization/power mode/thermal state missing.

| Threads | Mean ± SD (s) | Samples/s | Speedup | 4 kHz capacity (%) | Avg / peak W | Energy/run (J) | Samples/J |
|---|---|---|---|---|---|---|---|
| 1 | 147.182 ± 0.588 | 61,377 | 1.00× | 3.00 | 3.254 / 3.365 | 478.878 | 18,865 |
| 2 | 76.070 ± 0.384 | 118,754 | 1.93× | 5.80 | 4.310 / 4.472 | 327.878 | 27,552 |
| 4 | 43.460 ± 0.118 | 207,860 | 3.39× | 10.15 | 6.022 / 6.342 | 261.697 | 34,519 |
| 8 | 42.101 ± 0.353 | 214,574 | 3.50× | 10.48 | 6.158 / 6.342 | 259.241 | 34,847 |

## Exploratory Dorado POD5 versus Slorado BLOW5

Source: B p.16; P pp.14–15. Status: preliminary-report-transcription.

RTX 4070 per P. Model versions and outputs differ; no isolated format-effect conclusion. Exact signal identity/conversion commands, tool build and electrical power scope TBD. Distinct from DORADO-003. Values transcribed unchanged; energy integration details missing.

| Metric | Dorado POD5 HAC v6.0.0 | Slorado BLOW5 HAC v5.0.0 |
|---|---|---|
| Basecalling time (s) | 1.294 | 4.886 |
| Full command time (s) | 8.86 | 6.27 |
| Samples/s | 21,599,180 | 5,720,411 |
| Idle power W | 19.30 | 27.27 |
| Average basecalling power W | 110.3 | 115.6 |
| Peak power whole run W | 172.19 | 125.51 |
| Basecalling energy J | 142.7 | 565.1 |
| Whole command energy J | 1,039.3 | 611.3 |
| Basecalling energy/read J | 2.42 | 9.58 |
| Energy/million samples J | 5.10 | 20.22 |
| Peak GPU memory MiB | 11,942 | 3,286 |
| Peak GPU temperature °C | 58 | 47 |
| Output | BAM | FASTQ |
