Project 22 — Research Website Specification
Project: Enabling Real-Time DNA Analysis for Portable Sequencing
Context: York University ENG 4000, Project 22 (2026–2027)
Supervisor: Prof. Sebastian Magierowski
Document purpose: Implementation contract for Astra and future site contributors
Status: Approved information-architecture direction; implementation and framework selection pending
Last specified: 2026-11-20
Read this first: Build a credible, easily navigable technical research website, not a student portfolio, course-report replica, or real-time analytics dashboard. Implement the agreed structure; do not invent research or silently modify experimental evidence. Inspect the actual repository and source materials before writing code.

1. Mission and editorial principles
   The website should make Project 22's evolving scientific and engineering contributions understandable, verifiable, and reproducible for:

- Prof. Magierowski and capstone reviewers;
- nanopore-sequencing, basecalling, and systems researchers;
- engineers seeking to run or reproduce benchmarks;
- future students continuing the work; and
- team members organizing new experiments.
  A technically informed visitor should quickly locate the relevant research question, study, experiment, model, dataset, platform, or reproduction guide. Do not assume the homepage must teach nanopore sequencing. Put foundational explanations and capstone background on a dedicated About page.

Editorial rules:

1. Research-first: Questions, controls, evidence, limitations, and reproducibility take precedence over visual flair.
2. Wick-inspired coherence: Study Ryan Wick's site (https://rrwick.github.io/) for how he connects research questions, methods, plots, results, conclusions, and supporting scripts/data. Do not clone its visual identity.
3. Evidence over claims: Important numerical statements must link to identifiable experiment records and supporting artifacts.
4. Progressive detail: Readers see the research conclusion first, with methods and individual run records one or two clicks away.
5. No false maturity: A working implementation, a repeatable benchmark, an accurate basecaller, and a sustained real-time system are different claims.
6. Low maintenance: Use canonical structured metadata in the repository. Avoid copying identical facts into many pages.
7. Scalable without overengineering: Prefer a simple static documentation site and a generated experiment index over a backend, application framework, or database.
8. Research identity: two pillars, one foundation
   Pillar A — Basecaller Benchmarking
   Primary question: How do nanopore basecallers, models, and computing platforms compare under defined accuracy, throughput, memory, power, energy, and real-time constraints?

This pillar is an evolving, potentially standalone benchmarking and methodology contribution. It should be organized by research question, not by software package or team member. Tools such as Dorado, DeepNano-Blitz, and future SoCall measurements appear where they provide evidence for a question.
Pillar B — SoCall Engineering
Primary question: Can the lab's int8/fixed-point SoCall basecaller be verified, characterized, and improved for resource-constrained or embedded execution?

This pillar has an engineering lifecycle: understand the implementation → verify correctness → establish a baseline → profile → test optimization hypotheses → revalidate. Do not imply that SoCall has already been properly benchmarked or optimized.
Shared foundation
Both pillars use the same:

- benchmark protocols and metric definitions;
- model/basecaller, dataset, and hardware catalogues;
- stable, searchable experiment registry;
- evidence and artifact references;
- reproduction guides and environment specifications; and
- documented MLCommons/MLPerf methodological influences and deviations.
  Equal structural legitimacy does not require equal content volume. Benchmarking currently has more measured evidence; SoCall pages should expand only as the work is completed and verified.

3. Agreed navigation and hierarchy
   Global header (all pages): Project 22 wordmark/logo (links to Home), Benchmarking, SoCall, Experiments, Methodology, Resources, About. Keep this header concise and usable on mobile.

Proposed logical sitemap; avoid publishing empty or misleading placeholders:
Home
├── Benchmarking
│ ├── Phase 1 — Basecaller Exploration & Initial Benchmarking
│ │ ├── Basecaller Exploration & Feasibility
│ │ ├── Hardware Performance & Energy Efficiency
│ │ └── Model Configuration & Pipeline Evaluation
│ └── Phase 2 — Expanded Benchmarking & Validation
│   └── Basecaller Accuracy & Validation
├── SoCall
│ ├── Overview / current engineering state
│ ├── Architecture and implementation
│ ├── Correctness and verification
│ ├── Baseline characterization
│ ├── Profiling and bottlenecks
│ └── Optimization studies
├── Experiments
│ ├── Searchable experiment registry
│ └── Stable experiment record pages (e.g., BLITZ-005, BLITZ-009)
├── Methodology
│ ├── Benchmark protocol and controls
│ ├── Metrics, timing boundaries and repeatability
│ ├── Accuracy evaluation
│ ├── Real-time throughput, latency and streaming criteria
│ ├── Power, energy and memory measurement scope
│ └── MLCommons alignment and documented differences
├── Resources
│ ├── Models and basecallers
│ ├── Datasets
│ ├── Hardware and execution environments
│ └── Reproduce the experiments / running the tools
└── About
├── Project objectives and capstone context
├── Nanopore sequencing and basecalling background
├── Team and supervisor
└── Scope, acknowledgments and references
The sitemap is a content model, not a command to generate every page at launch. Group or rename lower-level entries if doing so improves readability without violating the agreed top-level structure.
3.1 Home

- Minimal and direct. One brief technical headline and a one- or two-sentence statement of purpose.
- Two prominent, distinct, clickable entry points: Basecaller Benchmarking and SoCall Engineering. This is the one place where restrained visual flair is encouraged: subtle color separation, technical motifs, and modest hover effects.
- Optionally show a small Latest research or Selected findings area (approximately 2–3 items) that links to the corresponding study. Every finding must be scoped and qualified.
- Quick access to Experiments and Resources, but no giant dashboard or long educational introduction.
- About is visible in the header. Project/team background and nanopore explanations go there rather than on Home.
  3.2 Benchmarking landing page
- A curated directory of research questions and active studies, not a catalog grouped by Dorado/Blitz/Bonito or a KPI dashboard.
- Prioritize evidence-backed studies; show short descriptions and the current evidence maturity.
- Group investigations by phase, then by research category. Include a short description and evidence status for each investigation.
- Studies under investigation without enough evidence can appear as Open questions / In progress entries rather than empty paper-like pages.
- Readers must reach a study in one click and the supporting experiment from that study in another.
  3.3 SoCall landing page
- Explain SoCall's fixed-point/embedded engineering objective succinctly, along with actual current status.
- Show an engineering progression: Architecture → Verification → Baseline → Profiling → Optimization Studies.
- Link to the canonical SoCall model record, Jetson platform record, related experiments, and reproduction guide (where permitted and available).
- Distinguish engineering milestones (e.g., compiled successfully) from research investigations (e.g., whether overlapping stages improves end-to-end throughput).
- Avoid progress percentages and claims that correctness, baseline measurement, profiling, CUDA acceleration, or optimization have already been completed without source evidence.

4. Page templates and reader journeys
   4.1 Research study — human-authored scientific narrative
   Use consistently under both pillars, adapted to their subject:
1. Question and concise answer/status: What is being tested, and what can currently be concluded?
1. Experimental design: Scope, variables, controls, dataset/model/system, metrics, and linked experiment IDs.
1. Results: Comparisons, informative plots, tables, consistent units, and figure captions.
1. Interpretation: What the evidence supports and what engineering decisions it informs.
1. Limitations: Missing controls, methodology gaps, measurement scope, and non-comparable observations.
1. Next investigation: What evidence would improve or disconfirm the interpretation?
1. Supporting experiments and reproducibility: Links to records, configurations, data, scripts, and logs.
   Studies should feel like concise scientific articles rather than automatically generated dumps. Titles should identify questions, e.g. How Does CPU Parallelism Affect Basecalling Throughput and Energy Efficiency? A study can draw from multiple tools or experiment IDs. One experiment can support multiple studies without duplicating its raw evidence.
   4.2 Experiment record — structured, citable technical evidence
   Use stable public URLs such as /experiments/BLITZ-005/, subject to the selected static-site router. Each page should display available fields and label missing ones explicitly:

- Stable ID, short title, date, owner/contributor if appropriate, objective, workflow/evidence status;
- tool/build/commit, model and weight identifier/checksum when known;
- dataset ID, chemistry, read count, signal-sample count, provenance/checksum when known;
- system ID, OS, architecture, runtime/driver, power mode and measurement hardware when known;
- fixed settings and swept variables (e.g., caller threads, chunk size, batch size);
- exact execution/reproduction command and measurement boundaries if archived and verified;
- warm-ups, run count, per-trial values, aggregate summary and dispersion;
- throughput, time, latency, memory, power, energy, samples/J, and output validation only where collected;
- limitations, related studies, references to configuration and raw evidence artifacts.
  Experiment ID ≠ process invocation. For example, BLITZ-005 is one controlled thread-scaling experiment with configurations and replicate trials; do not make every timed invocation a separate top-level experiment.

Keep the page more structured than prose-heavy. It does not need to retell the study's introduction or conclusions. Include copyable commands only when faithfully reproduced from source; otherwise show a clear missing-command note.
4.3 Raw evidence and reproduction
The site should link to, but not replace, canonical repository artifacts:

- configuration/metadata file;
- archived logs, timings and power traces;
- checksums and data provenance;
- output validation summaries;
- relevant runner or reproduction script.
  A research reader follows Benchmarking → Study → Experiment → Evidence. A teammate can follow Experiments → Experiment → Config/Logs directly.
  4.4 Experiment lifecycle and maturity
  An experiment may be registered before it supports a published study. Keep it discoverable. Distinguish at least:
- Workflow state: planned / running / completed / failed / superseded, based on actual records;
- Evidence completeness: reproducible artifacts available / partial provenance / missing data;
- Scientific claim maturity: exploratory / preliminary / sufficiently supported for a specific claim.
  Do not collapse these dimensions into a generic green “validated” badge. Output consistency, biological accuracy, repeatable runtime, and calibrated power measurements are different properties.

5. Central searchable experiment registry
   A dedicated Experiments navigation item should lead to a lightweight, static, searchable index. The index should not dominate Home or the Benchmarking landing page.

Desired capabilities:

- Fast text search by ID, title, basecaller, hardware, dataset, and research question;
- useful filters (e.g., tool, platform, dataset, study, date, evidence status), as supported by actual metadata;
- direct stable link to every experiment record;
- clear counts, empty states, mobile usability, and accessible keyboard navigation;
- provenance markers so records with incomplete metadata are not misrepresented;
- links from study pages to related experiment IDs and, ideally, reverse links from experiments to studies.
  Implementation preference: produce the registry and record pages at build time from validated local YAML/JSON/CSV metadata. Client-side search is sufficient; no application backend or database is required. Preserve IDs. Fail validation on duplicate identifiers or invalid references rather than silently dropping them.

6. Canonical repository structure and source-of-truth rules
   The supplied repository tree already separates artifact types:
   configs/experiments/ # Existing experiment YAML records
   configs/scenarios/ # Existing scenario definitions
   models/ # Model JSON and Markdown metadata
   datasets/ # Dataset JSON and Markdown metadata
   systems/ # Hardware / execution-environment metadata
   schemas/ # Metadata schemas
   harness/ # Benchmark / analysis / validation infrastructure
   results/ # Raw results, summaries, historical observations
   docs/ # Existing method and platform documents
   .local-evidence/ # Local/reference material; DO NOT auto-publish
   This structure comes from a supplied directory listing, not a live source-code audit. Astra must inspect the current checkout, actual files, git status, schemas, and data relationships before changing anything.

Rules:

1. Repository = code, configurations, metadata, raw and processed results, reproduction. Website = readable presentation and links to those sources.
2. Do not restructure/delete the existing benchmark infrastructure merely to suit site navigation.
3. Prefer one canonical data definition: configs/experiments/ for experiments, models/ for models, datasets/ for datasets, and systems/ for environments, subject to verification of actual schemas.
4. Research-study interpretations are human-reviewed Markdown, not automatically inferred from raw data.
5. If reports, YAML records, and derived summaries disagree, flag the conflict for review. Do not silently change values or assign a winner without a grounded reason.
6. Avoid committing generated dependency/vendor trees, huge sequencing files, temporary output, secrets, private source/weights, or .local-evidence/ to the public site.
7. For SoCall private/restricted material, publish permitted descriptive metadata and an honest access statement; never publish confidential code or weights.
8. Site builds must not execute basecalling benchmarks, download raw sequencing datasets, or require GPU/Jetson hardware.
   Authoritative project materials
   The site must ground its research content in the materials provided by the team:

- Project 22 — Weekly Progress Log (new).pdf;
- Project 22 — Preliminary Benchmarking Report.docx (2).pdf;
- Prof. Magierowski's supplied feedback/message; and
- the current repository's original validated experiment artifacts.
  The reports and supervisor feedback define the documented research state. Exact run configurations and raw evidence should be cross-checked with the repository. When a fact is absent or conflicting, clearly mark TBD, Not measured, Not verified, or Source conflict. Do not fill gaps through assumptions. Do not treat this specification as an independent source of experimental truth.

7. Research-specific accuracy and caution rules
   The following are presentation guardrails, not permission to generate new metrics:

- Dorado early tests used Dorado 2.1.2 and dna_r10.4.1_e8.2_400bps_hac@v6.0.0 on the small D1 DeepMod2 POD5 sample (59 reads). Tool version and model version are different pieces of metadata.
- Reported RTX 4070 throughput of approximately 19.95 million signal samples/s on D1 is a short basecalling-interval observation, not a proven sustained, end-to-end, real-time processing rate. The recorded full command had substantial setup time.
- The report's provisional R10.4.1 full-channel 5 kHz comparison rate is 512 × 5,000 = 2,560,000 samples/s. This theoretical target is not measured MinION sustained yield or a latency/queue guarantee.
- Historical D4/Blitz samples use inspected 4 kHz acquisition metadata; a dataset-matched 512-channel reference is 2,048,000 samples/s. Always label the denominator and condition when showing real-time capacity.
- BLITZ-009 is a CPU-only ARM64 port of DeepNano-Blitz on Jetson TX2, not a Jetson GPU or SoCall test. The reported 8-thread measurement is 214,574 samples/s on D4; Jetson power-sensor scaling and module-input energy require further verification.
- Output agreement by read ID/sequence/quality is not biological accuracy. Predicted Q-scores are not directly equivalent to reference-aligned empirical accuracy.
- Power scopes differ: CPU-package, GPU/accelerator readings, Jetson module input, and whole-system wall power must never be ranked interchangeably without clear qualifications.
- Existing POD5/Dorado vs BLOW5/Slorado exploratory measurements change more than just file format (including HAC model versions and pipeline details). Do not attribute observed differences solely to file format.
- DeepNano-Blitz historical datasets/chemistries and Dorado newer chemistry must be labelled; do not claim all tools were evaluated on identical input.
- SoCall correctness, characterization, Jetson baseline, profiling, and optimization remain ongoing/unverified unless newer authoritative artifacts demonstrate otherwise.
- Model architecture, parameter count, precision, training data, weights, exact chemistry, driver/runtime, and dataset checksums must be supplied or verified rather than invented.
  Publication language: Prefer “preliminary measurement,” “under the tested configuration,” and “not yet established” where appropriate. A completed run does not imply real-time streaming, generalized accuracy, or validated energy efficiency.

8. Methodology and MLCommons positioning
   Dedicate a methodology page to the extent to which the platform follows relevant MLCommons/MLPerf benchmarking principles, and clearly state differences required for nanopore signal processing:

- controlled workloads and stable input/model identifiers;
- repeatability, warm-up, and clearly defined timing intervals;
- hardware/runtime disclosure;
- throughput and latency reporting;
- accuracy methodology and reference validation;
- power measurement boundary, sampling, synchronization and integration;
- streaming workload, input arrival rate, queue stability, and bounded latency;
- whether and how results can be compared across systems and software generations.
  Do not claim MLPerf compliance, certification, or official MLCommons benchmark status. Explain the principles adopted, those not yet met, and nanopore-specific adaptations.

9. Visual and navigation direction
   Overall feel: Ryan Wick-inspired clarity and academic restraint, with a little intentional flair on Home.

- Predominantly light background, high-contrast text, generous spacing and a readable content width.
- Subtle teal/blue accent for Benchmarking and complementary muted slate/blue accent for SoCall; both belong to one brand.
- Elegant but simple typography; monospace for commands, paths, experiment IDs, and parameters.
- Home: horizontal header, no sidebar, two visually distinct large research entry cards; subtle hover/transition permitted.
- Pillar landing pages: horizontal header, no persistent sidebar, concise curated index.
- Study pages: readable article presentation and optional right-side table of contents.
- Experiment/method/reference pages: contextual left sidebar where depth warrants it, with a clear main-content area.
- Responsive/mobile navigation, accessible focus states, semantic headings, sufficient contrast, and appropriately scrollable/wrappable technical tables.
- Plots should have explicit axes, units, conditions, legends, and captions. Prefer clear 2D scientific charts over flashy dashboards.
- Use subtle indicators for maturity; don't use colors as the only way to communicate status.
- Avoid decorative 3D graphics, animated backgrounds, oversized hero imagery, excessive cards, and generic marketing copy.
- Dark mode is optional; not a launch blocker.

10. Implementation and deployment constraints
    Target hosting: GitHub Pages. The repository's Pages source has been set to GitHub Actions. No custom domain has been confirmed.

Framework: Not yet locked. Evaluate a simple Markdown-oriented static documentation stack (such as MkDocs or Zensical) against the required navigation, content generation, search, and GitHub Pages deployment. Choose the least complex maintainable option; check current tool/theme compatibility before committing. Avoid introducing Next.js/React or a backend without demonstrating necessity.

Important:

- Do not assume the repository has been renamed to portable-basecalling. That was a suggested short name, not a confirmed change.
- Configure project-site base paths and canonical links according to the actual GitHub repository owner/name; don't hardcode an unconfirmed URL.
- Provide a documented local preview/build command and pinned or well-constrained dependencies.
- GitHub Actions should run validation/build checks on pull requests and deploy from an approved branch (prefer main) after review.
- Preserve existing experiment and analysis code behavior. New site automation must not run scientific workloads.
- Validate broken internal links, missing referenced files, duplicate IDs, and structured data schemas as part of the build where practical.
- Prefer a light, generated static search/index over runtime API calls or dynamic infrastructure.

11. Initial content and rollout scope
    Build progressively, not by generating dozens of thin pages all at once.
    Phase 0 — Audit and plan
    Inspect the checkout, existing README/docs, experiment schemas, model/dataset/system files, outputs, git ignore rules, report evidence, and current Pages settings. Identify source conflicts, private data, missing artifacts, and which exact runs are reproducible. Make a brief mapping from this spec to the repo before editing.
    Phase 1 — Site skeleton
    Establish the static site framework, header, navigation, responsive layouts, minimal Home, Benchmarking directory, SoCall overview, About, and placeholder-free links to sections with real material. Configure local preview and CI/deployment.
    Phase 2 — One complete evidence path (critical checkpoint)
    Implement a genuinely working path:

Home → Benchmarking → DeepNano-Blitz CPU Scaling and Energy Efficiency → BLITZ-005 experiment → available configuration, evidence and reproduction instructions.

Use actual archived data for a figure/table; link to canonical YAML/model/dataset/system files; present missing evidence openly. Check all links and mobile layouts before scaling up.
Phase 3 — Catalogue and registry
Generate a searchable registry and stable experiment pages from the existing metadata after schema validation. Render models, datasets, hardware, and reproduction guides without duplicating the canonical source. Add relevant study-to-record references.
Phase 4 — Expand research and refine
Add other evidence-supported studies (Dorado platforms, larger Blitz studies, Jetson CPU baseline, exploratory model/format comparisons with proper caveats), methods/MLCommons alignment, SoCall engineering pages grounded in completed work, and polished accessible charts and navigation. Keep incomplete future research as clearly labelled open questions, not fabricated findings. 12. Acceptance criteria
The initial public site is acceptable when:

- [ ] Home immediately offers Benchmarking and SoCall entry points; About contains the longer background.
- [ ] Benchmarking opens a research-question-first directory, not a tool list or metrics dashboard.
- [ ] SoCall describes current engineering state accurately and distinguishes milestones from optimization investigations.
- [ ] A complete study → experiment → evidence path works using genuine Project 22 records.
- [ ] A visitor can search experiment IDs and reach their stable record pages.
- [ ] Every quantitative headline links to supporting evidence and discloses key conditions/limitations.
- [ ] Experiment IDs, model/dataset/system references, and recorded values are not silently altered.
- [ ] Missing metadata and conflicting sources are visible rather than invented.
- [ ] Technical commands, figures, tables, and navigation work on desktop and mobile.
- [ ] Builds and deployments work through GitHub Actions; pull-request checks do not publish unreviewed changes.
- [ ] No private SoCall materials, secrets, large raw datasets, local vendor folders, or unsupported generated claims are published.
- [ ] The repository still serves as the canonical home of code/config/results; the site is its reader-friendly presentation.

13. Explicitly out of scope for the first release

- Full redesign of the research repository or benchmark harness;
- creating new benchmark results, re-running experiments, or performing biological analyses solely to fill site content;
- claiming SoCall optimizations exist before they are documented;
- live data infrastructure, accounts, databases, or complex submission portals;
- MLPerf certification/compliance claims;
- full-blown paper publication or automatic conclusions generated by an LLM;
- custom domain purchase or GitHub repository rename without explicit approval.

14. Open decisions for Astra to resolve or report
1. Select MkDocs/Zensical or another minimal static stack after repository inspection; explain the tradeoff briefly.
1. Confirm actual GitHub owner/repository, Pages base URL, and whether portable-basecalling will be adopted later (do not rename by default).
1. Determine which archive paths and result records can be safely linked publicly versus marked unavailable.
1. Determine whether source metadata already covers all registry filters; do not manufacture missing fields.
1. Identify conflicting IDs/values and report them before publishing generated comparisons.
1. Ask for human review of proposed scientific interpretations, especially SoCall state, comparative accuracy, power, file-format effects, and real-time claims.
   One-line design test
   Can a researcher find a precise question, understand what we actually measured, inspect the supporting experiment, and reproduce or critically evaluate it—without reading our course reports or guessing what was done?

If yes, the site is fulfilling its purpose.
