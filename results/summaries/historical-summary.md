# Historical results — preliminary report transcriptions

Generated from `report-observations.json`; no new benchmark runs or raw telemetry are represented. All numerical precision is retained as reported. [Evidence register](../../docs/sources.md).

## Dorado 2.1.2, HAC v6.0.0 — D1 (59 reads)

Times represent reported basecalling intervals, not full-command execution. The RTX 4070 command took approximately 12 s. Capacity is relative to a theoretical 2,560,000 samples/s input rate; it is not a live-streaming measurement.

| Experiment | Hardware | Basecalling time (s) | Samples/s | 5 kHz reference (%) |
|---|---|---|---|---|
| DORADO-001 | GTX 1060 | 53.213 | 525,235 | 20.52 |
| DORADO-002 | Ryzen 5 1500X | 4,216.234 | 6,628.981 | 0.26 |
| DORADO-003 | RTX 4070 | 1.401 | 19,949,560 | 779.28 |
| DORADO-004 | RTX 4070 + modified-base calling | 1.516 | 18,436,240 | 720.17 |
| DORADO-005 | Apple M2 (Metal) | 246.9 | ~113,217 | 4.42 |
| DORADO-006 | RTX 3070 Mobile | 7.6 | 3,663,565 | 143.11 |

## Dorado memory and output observations

Memory values use different measurement methods and are not directly comparable. The RTX 4070 figure is a tuning allocation, not a measured peak. Predicted Q-scores are not reference-based accuracy.

| Experiment | Observation |
|---|---|
| DORADO-001 | 2,896 MB reported (approximately 2.83 GB; unit convention unverified) |
| DORADO-003 | Approximately 7.5 GB allocated during model tuning; batch size 896, chunk size 12,288 |
| DORADO-004 | Peak memory not measured |
| DORADO-005 | 4.1 GB reported peak (measurement scope unverified); median Q-score 20.4 (range 10.3–23.5), median read length 30,983 bases, 2.0 Mb output |

## Dorado Fast and HAC on Apple M2

These exploratory runs lack complete model and timing records. D2 values are predicted Q-scores; the accuracy method for simulated D3 reads was not documented.

| Dataset | Model tier | Time (s) | Reported quality / accuracy |
|---|---|---|---|
| D2 (4,000 reads) | Fast | 11 | Median predicted Q 12.3 |
| D2 (4,000 reads) | HAC | 1,164 | Median predicted Q 19.8 |
| D3 (200 simulated reads) | Fast | 2.8 | Reported accuracy 86.7% |
| D3 (200 simulated reads) | HAC | 242 | Reported accuracy 92.6% |

## DeepNano-Blitz on Ryzen 7 5700U — initial thread comparison

Three runs per configuration, including a slower first run. Outputs matched for all 48 reads. The initial results reported reads/s, not signal samples/s.

| Run | 1 thread (s) | 4 threads (s) | Peak memory, 1 / 4 threads (MiB) |
|---|---|---|---|
| 1 | 48.232 | 17.340 | Not measured |
| 2 | 29.600 | 12.060 | 118.11 / 102.01 |
| 3 | 27.740 | 11.250 | 118.41 / 109.64 |
| Mean | 35.191 | 13.550 | Not summarized |
| Diagnostic single-thread | 29.20 and 29.16 | — | — |

## DeepNano-Blitz on Ryzen 7 7800X3D — initial D4 baseline

Three runs processed the same 48 reads and produced identical FASTQ output. Warm-up conditions for this baseline were not documented.

| Run | Wall time (s) |
|---|---|
| 1 | 15.22 |
| 2 | 14.87 |
| 3 | 14.95 |
| Reported mean ± SD | 15.01 ± 0.18 |

## DeepNano-Blitz on Ryzen 7 7800X3D — CPU thread scaling

Each thread setting had one warm-up followed by three complete-command measurements. All 12 FASTQ outputs matched. Peak RSS is the highest value among measured runs.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) | Run times (s) | CPU use |
|---|---|---|---|---|---|---|
| 1 | 15.187 ± 0.114 | 594,828 | 1.00× | 119.29 | 15.06 / 15.28 / 15.22 | 99% |
| 2 | 8.053 ± 0.256 | 1,121,704 | 1.89× | 109.38 | 7.76 / 8.17 / 8.23 | 198% |
| 4 | 4.403 ± 0.061 | 2,051,504 | 3.45× | 109.98 | 4.35 / 4.39 / 4.47 | 375–377% |
| 8 | 2.917 ± 0.006 | 3,097,184 | 5.21× | 108.98 | 2.91 / 2.92 / 2.92 | 701–706% |

## DeepNano-Blitz on D5 — larger-workload performance

Each run processed 4,467 reads (1,290,238,981 signal samples) after warm-up, with matching output. Mean throughput was 4,092,013 samples/s: 199.81% of a 4 kHz full-channel signal-rate reference (159.84% at 5 kHz). This was offline processing, not live streaming.

| Run | Wall time (s) | Peak RSS (MiB) | CPU utilization |
|---|---|---|---|
| 1 | 315.23 | 169.66 | 798% |
| 2 | 315.99 | 166.26 | 798% |
| 3 | 314.70 | 167.73 | 798% |
| Mean ± SD | 315.31 ± 0.65 | Highest peak 169.66 | 798% each |

## DeepNano-Blitz on Ryzen 7 5700U — four-setting thread sweep

One warm-up and three measured runs per setting. All outputs matched by read ID, sequence, and quality string.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) |
|---|---|---|---|---|
| 1 | 19.953 ± 0.545 | 452,729 | 1.00× | 118.29 |
| 2 | 10.873 ± 0.337 | 830,790 | 1.84× | 105.30 |
| 4 | 7.050 ± 0.523 | 1,281,341 | 2.83× | 108.44 |
| 8 | 5.503 ± 0.475 | 1,641,451 | 3.63× | 106.70 |

## DeepNano-Blitz on Ryzen 7 5700U — 30-run thread sweep

Thirty measured runs per setting followed an excluded warm-up. All 120 FASTQ outputs matched. Reported throughput values are retained as recorded.

| Threads | Mean ± SD (s) | Samples/s | Speedup | Peak RSS (MiB) |
|---|---|---|---|---|
| 1 | 22.344 ± 2.602 | 404,005 | 1.00× | 118.39 |
| 2 | 12.748 ± 0.518 | 707,791 | 1.75× | 109.27 |
| 4 | 7.676 ± 0.486 | 1,174,570 | 2.91× | 110.25 |
| 8 | 5.357 ± 0.276 | 1,681,417 | 4.17× | 110.04 |

## Dorado power observations

The original records do not identify a verified instrument, electrical boundary, or matching timing window. These power readings cannot be used to calculate reliable energy consumption.

| Configuration | Average power (W) | Peak power (W) |
|---|---|---|
| Ryzen 5 1500X CPU | 32.34 | 55.63 |
| GTX 1060 | 95.91 | 120.00 |
| RTX 4070 | 110.3 | 172.19 |
| RTX 4070 modified | 133.7 | 188.80 |

## DeepNano-Blitz CPU-package power and energy

Power was sampled at approximately 2 s intervals and integrated over each workload. Measurements cover CPU-package power, not the complete system. Each configuration has one power session; D4 ×30 repeats the same 48 reads (271,003,620 signal samples).

| Experiment / CPU | Threads | Dataset | Duration (s) | Avg / peak power (W) | Energy (J) | Samples/J | Samples/s |
|---|---|---|---|---|---|---|---|
| BLITZ-006 / 7800X3D | 8 | D4 ×30 | 77.32 | 64.48 / 70.13 | 4,986 | 54,358 | 3,504,778 |
| BLITZ-008 / 7800X3D | 8 | D5 | 319.60 | 70.18 / 71.52 | 22,430 | 57,524 | 4,037,003 |
| 5700U separate session | 4 | D4 ×30 | 245.31 | 21.63 / 22.73 | 5,306 | 51,072 | 1,104,720 |

## DeepNano-Blitz on Ryzen 7 5700U — thread scaling and energy

Each setting repeated D4 thirty times after warm-up, processing 271,003,620 signal samples. CPU-package power was recorded during one continuous measurement session, not independent energy trials.

| Threads | Duration (s) | Avg / peak power (W) | Energy (J) | Samples/J |
|---|---|---|---|---|
| 1 | 670.79 | 19.47 / 24.33 | 13,061 | 20,749 |
| 2 | 382.89 | 21.71 / 22.88 | 8,311 | 32,607 |
| 4 | 230.73 | 21.61 / 23.07 | 4,985 | 54,362 |
| 8 | 161.18 | 21.58 / 22.73 | 3,479 | 77,907 |

## DeepNano-Blitz on Jetson TX2 — CPU performance and power

Three complete-command runs per thread setting followed warm-up; all 12 outputs matched. Power was sampled from the VDD_IN rail at roughly 0.5 s intervals. Sensor scaling remains unverified, so power and energy figures are provisional. The 4 kHz reference is 2,048,000 samples/s; memory and power mode were not recorded.

| Threads | Mean ± SD (s) | Samples/s | Speedup | 4 kHz reference (%) | Avg / peak power (W) | Energy/run (J) | Samples/J |
|---|---|---|---|---|---|---|---|
| 1 | 147.182 ± 0.588 | 61,377 | 1.00× | 3.00 | 3.254 / 3.365 | 478.878 | 18,865 |
| 2 | 76.070 ± 0.384 | 118,754 | 1.93× | 5.80 | 4.310 / 4.472 | 327.878 | 27,552 |
| 4 | 43.460 ± 0.118 | 207,860 | 3.39× | 10.15 | 6.022 / 6.342 | 261.697 | 34,519 |
| 8 | 42.101 ± 0.353 | 214,574 | 3.50× | 10.48 | 6.158 / 6.342 | 259.241 | 34,847 |

## Dorado/POD5 and Slorado/BLOW5 — initial comparison

The pipelines used different HAC model versions and output formats, so these measurements cannot isolate file-format overhead. Signal identity, conversion steps, and power-measurement boundaries still need verification.

| Metric | Dorado / POD5 / HAC v6.0.0 | Slorado / BLOW5 / HAC v5.0.0 |
|---|---|---|
| Basecalling time (s) | 1.294 | 4.886 |
| Complete command time (s) | 8.86 | 6.27 |
| Samples/s | 21,599,180 | 5,720,411 |
| Idle power (W) | 19.30 | 27.27 |
| Average basecalling power (W) | 110.3 | 115.6 |
| Peak power, full run (W) | 172.19 | 125.51 |
| Basecalling energy (J) | 142.7 | 565.1 |
| Complete command energy (J) | 1,039.3 | 611.3 |
| Basecalling energy per read (J) | 2.42 | 9.58 |
| Energy per million samples (J) | 5.10 | 20.22 |
| Peak GPU memory (MiB) | 11,942 | 3,286 |
| Peak GPU temperature (°C) | 58 | 47 |
| Output | BAM | FASTQ |
