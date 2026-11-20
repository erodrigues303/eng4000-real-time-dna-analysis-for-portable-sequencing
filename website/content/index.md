<p class="eyebrow">Portable sequencing · Research & engineering</p>

# Enabling real-time DNA analysis for portable sequencing

<p class="lead">Measuring the computational cost of nanopore basecalling, and investigating a fixed-point implementation for embedded hardware.</p>

<div class="pillars">
<a class="pillar" href="benchmarking/"><span class="eyebrow">Comparative research</span><h2>Basecaller Benchmarking</h2><p>Explore how hardware, parallelism and measurement boundaries affect throughput and energy.</p><strong>Explore the studies</strong></a>
<a class="pillar" href="socall/"><span class="eyebrow">Implementation research</span><h2>SoCall Engineering</h2><p>Follow the path from architecture and correctness to a measured baseline and informed optimization.</p><strong>Explore the engineering work</strong></a>
</div>

## Selected research

<div class="study-list">
<section><p class="eyebrow">Preliminary · CPU scaling</p><h3><a href="benchmarking/cpu-parallelism/">What do more caller threads buy?</a></h3><p>BLITZ-005 reports a 5.21× speedup from one to eight threads on the 48-read D4 workload. Output consistency is reported; biological accuracy is not established.</p></section>
<section><p class="eyebrow">Preliminary · Embedded feasibility</p><h3><a href="benchmarking/embedded-feasibility/">A CPU baseline on Jetson TX2</a></h3><p>BLITZ-009 tests an ARM64 DeepNano-Blitz port. It provides an embedded reference point; SoCall and GPU execution remain separate investigations.</p></section>
</div>

## Inspect the evidence

[Search the experiment registry](experiments/index.md), inspect [models, datasets and hardware](resources/index.md), or read the [measurement methodology](docs/methodology.md).

All imported measurements are preliminary. [Evidence gaps and source conflicts](docs/sources.md) are retained alongside the results.
