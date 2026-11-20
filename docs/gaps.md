# Missing information and technical backlog

These gaps are evidence limitations, not invitations to infer values. `TBD — needs verification` is the display convention; structured unknowns use null. This inventory covers significant missing/uncertain items across the supplied reports and resulting records. Record-level fields remain visible in generated cards/configs.

## Evidence and historical reconstruction — highest priority

- Original weekly progress log, exact experiment cards, appendices A/D referenced by B, dated raw folders, per-run stdout/stderr, FASTQ/BAM outputs, checksums and environment exports are missing. Reports claim retention elsewhere; locations/access/hashes need recovery.
- Exact commands, shells, working directories, executable hashes and most experiment dates are missing across the supplied reports. No historical config is runnable as-is.
- Resolve RTX 3070 aliases with its original card; DORADO-006 currently follows P p.13. Assign stable IDs to unnumbered 5700U timing/power follow-ups, D2/D3 tests and format comparisons without overwriting existing IDs.
- Recover BLITZ-001/002 complete settings; confirm BLITZ-003 and BLITZ-004 warm-up practice. Confirm BLITZ-009 build/model/settings instead of inheriting desktop values.
- Check numerical consistency from original unrounded records: printed rates and rounded means are not always reconstructible, especially 5700U extended rates. Do not silently recalculate historical observations.
- Team archival location/publication rights for the source PDFs remain TBD. PDFs contain administrative/personal information and are not published by this migration.

## Models and compatibility

- Every model: verified parameter count, weights hash, training corpus/splits, exact artefact/source, licence/redistribution terms and complete architecture remain missing.
- Dorado HAC v6: verify the reported seven flstm_softout layers and CRF state_len 4 against pinned config/source, remaining blocks, backend storage/compute precision, decoder settings, supported sampling rate, overlap and automatic batch choices on each system.
- Modified-base model: architecture, parameters, precision, decoder, runtime details and target-label validation; verify MM/ML tags and modification ground truth.
- Blitz network 64: complete layer structure, numerical types, decoder implementation, chunks/overlap, chemistry/motor support and weight checksum; identify exact TX2 port model/build.
- Slorado: full HAC v5 identifier/chemistry, code version/commit, architecture/precision/runtime and converted input identity.
- Coral: exact model/version/weights, architecture depth/parameters, chemistry/sample rate, training data and CPU feasibility. Source review is not execution.
- Bonito: reviewed configurations are not a uniquely identified tested model; historical platform restrictions need version-pinned verification before deployment.
- SoCall: publication permission; training data, normalization and chunk size are from supervisor recollection only; embedded (TX2) baseline. Reference-accuracy baseline on a laptop exists (SOCALL-001/002). Keep unpublished architecture and private weights outside the public repository. Profile before optimizing.

## Datasets and accuracy

- D1: exact URL/subset/hash/licence, signal count, reference accession and ground truth, file-level sample rate and kit. Resolve human-data use versus stated non-human policy. It is not training data.
- D2: accession/download/subset/hash/licence, chemistry/kit/rate, signal count and reference. Exact Fast/HAC models unknown.
- D3: generator version/command/seed, reference/hash, simulation pore/speed/rate, signal count, licence/download and exact tested models. Reported accuracy definition/alignment unavailable.
- D4: biological reference (revision `15bd04b`, MIT licence and read/sample counts now recorded), all-file chemistry/rate audit, pore subrevision and motor. expected.fastq is only a regression fixture.
- D5: exact pore subrevision/motor and possible training-data overlap. Reference genome, licences and archive SHA-256/MD5 were recorded and verified on 2026-11-19 (E).
- All datasets: train/evaluation leakage audit and complete manifest. Find separate R10.4.1 training and held-out evaluation corpora with references and sufficient scale/diversity.
- Accuracy: `harness/analysis/reference_accuracy.py` fixes aligner (minimap2 map-ont, primary only), identity = M/(M+S+I+D) and keeps unmapped reads in the denominator; reference coverage, trimming policy and confidence intervals remain open. Proposed 0.5% quality tolerance in P needs agreement and precise units; not an established acceptance gate.

## Systems and measurements

- All machines: exact inventory/OS build, architecture confirmation where not reported, driver/CUDA/runtime, power mode/clocks/thermal state, background activity and environment lockfiles. Matthew CPU, Weiqin RAM, mobile GPU VRAM/power limit and Brian WSL version are specifically absent.
- TX2: JetPack/CUDA/driver, exact CPU/GPU configuration, port math-library identity/version/patch and build instructions; power mode, affinity and temperature. BLITZ-009 memory and CPU utilization absent. Current Dorado is not assumed supported.
- TX2 power: validate INA3221 units/scaling/rail and low idle readings against a known load/external meter; recover integration algorithm, per-run traces, timestamp alignment and aggregation method. Watts, joules and samples/J remain provisional.
- Dorado/Slorado: power instrument, electrical scope, sample rate, clock/window alignment, integration/idle policy, repeat trials, exact stage boundaries and memory measurement definitions. Do not derive new energy from mismatched intervals.
- HWiNFO: recover traces, runner phases and analysis scripts; Weiqin software version missing. Independent energy repeats, sensor uncertainty, idle drift and monitoring overhead unresolved. Whole-system power is absent.
- General: sustained duration/thermal criteria, cache policy, output-completion timing, latency distributions, streaming arrival schedules, backlog/backpressure/drop policy, deadlines and live occupancy. No reference-validated or live-streaming result yet.
- File-format study: identical models/settings/output and verified identical signal data, conversion cost, cold/warm cache, exact commands and repeats. Existing differences cannot be attributed to file format alone.
- MLCommons: pin relevant rule revision, select/map principles, define quality/performance validation and justify nanopore-specific deviations. No compliance claim.

## Recommended GitHub issues

1. **Recover and archive historical evidence** — All six owners supply original cards, commands, exports and immutable artifact hashes; reconcile RTX IDs and assign IDs to follow-ups. Acceptance: one traceable manifest per historical experiment, no synthetic raw data.
2. **Validate TX2 power telemetry and capture system inventory** — Eric: sensor units/rail/calibration, clocks/power mode/temperature, RSS and utilization. Acceptance: repeat known-load checks and independently repeated scoped energy trials.
3. **Recover the owned ARM64 Blitz port** — Eric/Brian: minimal patch, upstream commit, library/build instructions and licences. Acceptance: reproducible TX2 build and output comparison with pinned x86 baseline.
4. **Complete model provenance and permission review** — Tool owners: pinned configs, weight hashes, parameters, architecture/precision/decoder/chemistry; confirm SoCall publication boundaries. Acceptance: reviewed model cards without private disclosures.
5. **Curate R10.4.1 training and held-out evaluation data** — Krish/team: exact sources/licences, manifests, reference labels and leakage-safe splits; resolve D1 policy conflict. Acceptance: separate documented corpora, no signals in Git.
6. **Define and implement reference accuracy analysis** — Ege/team: reference/aligner/scoring/filtering and quality thresholds. Acceptance: reproducible mapped-fraction/coverage/error report on an identified evaluation set, distinct from predicted Q and regression equality.
7. **Implement minimal experiment runner and artifact capture** — Team: one tool first, explicit stage/full timing, one warm-up plus repeated measurements, exit/output checks and manifests. Acceptance: teammate reproduces one D5 baseline using recorded commands and configs.
8. **Repeat controlled Dorado/Slorado and sustained comparisons** — Matthew/Ege: fixed data/model/output, conversion identity, cache policy and repeated scoped measurements. Acceptance: isolate format effects or clearly explain why a matched comparison is unavailable.
9. **Establish SoCall correctness and baseline before profiling** — Team: permitted local setup, verified compatible data, reference outputs, scoped timing/memory/power; then profile stage bottlenecks. Acceptance: reproducible baseline before any optimization claims.
10. **Specify streaming workload and MLCommons mapping** — Team: pin external rules, arrival/queue/deadline policy, quality gate and documented deviations. Acceptance: reviewed replay specification followed by sustained latency/backlog measurements; no premature compliance claim.
