---
title: "POD5 vs BLOW5: Input Pipeline Performance"
---

<p class="eyebrow">Technical investigation · Phase 1</p>

# POD5 vs BLOW5: Input Pipeline Performance

## Objective

Compare recorded basecalling and full-command costs for the Dorado/POD5 and Slorado/BLOW5 pipelines and identify what must be controlled to measure file-format overhead.

## Experimental Setup / Methodology

The [RTX 4070 system](../systems/matthew-4070.md) ran Dorado with [HAC v6.0.0](../models/dorado-hac-v6.md), POD5 input and BAM output, and Slorado with [HAC v5.0.0](../models/slorado-hac-v5.md), BLOW5 input and FASTQ output. The report lists basecalling-stage and full-command durations, peak GPU memory and temperature, and stage and command energy. Exact executable builds, conversion commands, matched signal identity and electrical measurement boundaries are unverified.

## Results

<!-- evidence:formats -->

## Findings

Dorado had the shorter basecalling stage (1.294 s versus 4.886 s), while Slorado completed the command sooner (6.27 s versus 8.86 s). The reported energy ordering also reversed between the basecalling stage and full command. The 1.294 s Dorado result is a separate observation from the 1.401 s stage in DORADO-003.

The comparison changes the basecaller implementation, model version and output format together. Bulk reading, preprocessing, batching, setup and serialization may also differ. The data support a comparison of these two recorded configurations. The effect of input format alone remains unidentified.

## Limitations

The read and signal equivalence after conversion, cache state, exact timing boundaries and raw logs are missing. Power scope, sampling and energy integration are undocumented. The reported energy and memory differences cannot be assigned to the input reader.

## Next Steps

1. Convert one pinned read set to both formats and check read IDs, sample counts, signal values, calibration and read order. Time conversion separately.
2. Run both readers into the same basecaller build with identical model weights, backend, batching, preprocessing and output. Measure cold and warm runs in repeated, interleaved order on the same device and storage.
3. Measure open/read/decompress, conversion to the caller's input representation, inference, decoding and serialization separately, as well as full command. Validate equivalent outputs and use synchronized telemetry with one defined electrical boundary.
4. If the same caller cannot accept both formats, benchmark reader-only loading to a common representation and report the end-to-end results separately as a comparison of complete pipelines.

## Related Investigations and Evidence

- [Planned measurement scenarios](../configs/scenarios/README.md)
- [Dorado Cross-Platform Performance](hardware-throughput.md)
