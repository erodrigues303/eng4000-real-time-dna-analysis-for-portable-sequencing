---
title: "Dorado Model Configuration and Performance Tradeoffs"
---

<p class="eyebrow">Technical investigation · Phase 1</p>

# Dorado Model Configuration and Performance Tradeoffs

## Objective

Measure the runtime cost of switching from Fast to HAC and of enabling modified-base inference. Evaluate what the recorded output metrics can establish about call quality.

## Fast versus HAC

### Experimental Setup / Methodology

The exploratory tests on [Apple M2](../systems/ege-m2.md) compared Fast and HAC on [D2](../datasets/D2.md), 4,000 real Zymo fecal reads, and [D3](../datasets/D3.md), 200 Squigulator-simulated *E. coli* reads. The surrounding work used Dorado 2.1.2 on Metal. Exact builds, Fast/HAC model identifiers, commands and timing boundaries for these particular runs are unverified. The D3 dataset record lists BLOW5. The actual input to the caller or a conversion step remains undocumented.

### Results

<!-- evidence:ege-tiers -->

HAC took about 106× as long on D2 and 86.4× as long on D3. D2's median predicted Q increased from 12.3 to 19.8. D3's reported accuracy rose 5.9 percentage points, but the reference and scoring method are unknown. No signal throughput can be established without reliable signal counts and timing scope.

## Modified-base inference

### Experimental Setup / Methodology

[DORADO-003](../experiments/DORADO-003.md) and [DORADO-004](../experiments/DORADO-004.md) used Dorado 2.1.2 on the [RTX 4070](../systems/matthew-4070.md) with the same named 59-read [D1](../datasets/D1.md) sample. The baseline used [`dna_r10.4.1_e8.2_400bps_hac@v6.0.0`](../models/dorado-hac-v6.md). The companion run added [`dna_r10.4.1_e8.2_400bps_hac@v6.0.0_5mCG_5hmCG@v1`](../models/dorado-hac-v6-modified.md). The baseline's automatic batch and chunk settings are recorded. Effective settings for the companion run remain unverified.

### Results

The reported stage increased from 1.401 s to 1.516 s, an extra 0.115 s or **8.21%**. Throughput fell from 19,949,560 to 18,436,240 samples/s, about 7.59% relative to the baseline. Reported average/peak power changed from 110.3/172.19 W to 133.7/188.80 W. Instrument scope and alignment to the timed interval are unknown. Peak memory for the companion run was not measured. [Timing and throughput](hardware-throughput.md#dorado-d1) · [Historical power observations](hardware-throughput.md#dorado-power)

## Findings and Limitations

- D2 Q scores summarize predicted quality. The D3 percentages are exploratory because the simulation settings, reference and scoring definition are missing. Neither result establishes a reference-scored accuracy advantage on real reads.
- The modified-base pair measures a short stage on one small sample. Its runtime change does not establish repeated or sustained overhead. Historical notes report BAM MM/ML tags, but tag presence and correctness are unverified. Modified-base accuracy was not measured.

## Next Steps

Repeat Fast and HAC on larger matched biological read sets using pinned compatible models, logged decoder configuration, repeated stage and command timings, and a shared reference-scoring protocol. Report mapped fraction, identity and predicted Q separately. Repeat the modified-base on/off comparison with the same input, batch/chunk policy and output settings, verify MM/ML tags, and use known modification truth before reporting accuracy.

## Related Investigations and Evidence

- [Dorado Cross-Platform Performance](hardware-throughput.md)
- [DORADO-004](../experiments/DORADO-004.md)
