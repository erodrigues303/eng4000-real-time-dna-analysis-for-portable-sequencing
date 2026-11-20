<p class="eyebrow">Research pillar A</p>

# Basecaller Benchmarking

How do model, hardware and execution choices affect basecalling under portable-computing constraints? These studies connect each question to its controls, reported measurements and remaining uncertainty.

## Active studies

### [How does CPU parallelism affect throughput and energy?](cpu-parallelism.md)

Controlled caller-thread sweeps, a larger recorded workload, and separately scoped CPU-package energy sessions. **Preliminary report evidence.**

### [How does the execution platform affect throughput?](hardware-throughput.md)

Dorado on the same named D1 input and HAC model across CPU, CUDA and Metal. Automatic batching, setup and incomplete environments limit attribution. **Exploratory comparison.**

### [How close is the TX2 CPU baseline to real-time capacity?](embedded-feasibility.md)

An ARM64 DeepNano-Blitz CPU port, thread scaling and a dataset-matched theoretical signal-rate target. **Preliminary; module power unverified.**

### [Can the current measurements isolate input-format overhead?](pipeline-overhead.md)

The Dorado/Slorado comparison changes model version and output format as well as signal format. **Exploratory; causal attribution unsupported.**

## Open questions

Reference-based speed–accuracy tradeoffs need a pinned reference, scoring method and matched model identities. Streaming feasibility needs timestamped arrivals, queue and latency measurements. These are open investigations, not completed studies.

[Browse every registered experiment](../experiments/index.md) · [Measurement definitions](../docs/methodology.md)
