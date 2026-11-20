<p class="eyebrow">Benchmarking study · Exploratory</p>

# Can the current measurements isolate input-format overhead?

No. The available Dorado/POD5 and Slorado/BLOW5 comparison changes the model version and output representation as well as the signal format. It is useful for motivating controls, but cannot establish a file-format performance advantage.

## Experimental design

The report compares HAC v6.0.0 with HAC v5.0.0, and BAM with FASTQ. Signal identity after conversion, exact build and commands are not archived. This comparison has no assigned experiment ID and must not be merged with DORADO-003.

## Results and interpretation

[The full exploratory table](../evidence/index.md#formats) preserves the reported stage and command timings, memory and provisional energy values. A reversal between stage and command timing emphasizes that different timing boundaries answer different questions. It does not identify the cause of the difference.

## Limitations

Model, pipeline and output differences prevent attribution to the input format. Power scope and integration details are incomplete. The original conversion and execution logs are unavailable.

## Next investigation and reproduction

Use identical signal records, verify conversion identity, and match model, backend, output and cache policy. Measure conversion, loading, inference and complete-command costs separately. See the [planned scenarios](../configs/scenarios/README.md), [methodology](../docs/methodology.md) and [reproduction guide](../resources/reproduce.md).
