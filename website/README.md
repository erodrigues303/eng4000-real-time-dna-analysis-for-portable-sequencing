# Research website

The implementation contract is [docs/SITE_SPEC.md](../docs/SITE_SPEC.md), not a root-level file. The site uses **MkDocs 1.6.1**, a small local Jinja theme and plain JavaScript. This keeps Markdown authoring and Python metadata integration without a frontend build chain or backend. Zensical was considered, but the requested layout does not require another theme/runtime layer. MkDocs' documented hooks, custom theme and project-site URL support cover the requirements.

## Build and preview

From the repository root, Python 3.10+:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-site.txt
python harness/analysis/compare_d5_accuracy.py --check
python -m mkdocs build --strict
python website/check_site.py
python -m mkdocs serve
```

Open the URL printed by MkDocs. The project path is included in preview:
`http://127.0.0.1:8000/eng4000-real-time-dna-analysis-for-portable-sequencing/`.

The generated staging directory is rebuilt at startup. After editing canonical metadata or authored content during preview, restart `mkdocs serve` to regenerate it; the default watcher observes the staging directory rather than all upstream sources.

## Source structure

The D5 accuracy follow-up is generated from saved alignment evidence, separate from historical timing transcriptions. Run `python harness/analysis/compare_d5_accuracy.py` after a reviewed evidence change; `--check` validates CSV/JSON consistency, reference/scoring metadata, identical read sets and the derived comparison JSON. The build embeds its values in `benchmarking/d5-accuracy.md`. Optional plot regeneration uses `--plot` with matplotlib (created with 3.10.8); charts are not recomputed during site builds. The public allowlist includes only the two reviewed bacterial BLITZ-010 scoring artifacts, not the rest of `results/raw/`.

Appearance automatically follows the device's light/dark preference through CSS `prefers-color-scheme`, including live preference changes. Dark mode uses charcoal surfaces, muted text and blue links. The generated SVG chart has its own matching palette. No JavaScript toggle or saved preference overrides the device setting.

- `website/content/`: human-authored home, research studies, SoCall overview, resources and About.
- `website/theme/`: semantic page template; assets live in `website/content/assets/`.
- `website/generate.py`: MkDocs configuration hook; validates metadata and builds ignored `.site-docs/`.
- `website/studies.json`: editorial study relationships only; no copied measurements.
- `website/experiment-evidence.json`: explicit links from stable experiment IDs to canonical evidence table keys.
- Existing `configs/`, `datasets/`, `models/`, `systems/`, `results/` and selected `docs/` remain canonical.
- `site-build/`: ignored production output, the only directory uploaded by Pages.

Every build generates the registry, individual `/experiments/ID/` records, catalogue indexes, report tables and the BLITZ-005 plot. Records come from the existing JSON-subset YAML files. The chart uses the existing observation JSON. Unknown fields are displayed rather than inferred. Copying source Markdown and metadata uses an explicit public allowlist; private weights, raw data, PDFs and `.local-evidence/` never enter the site.

Edit the investigation Markdown for objectives, methods, results, findings and limitations. Add next steps and directly relevant evidence links where applicable. Individual experiment records retain run configuration and provenance.

Use `<!-- evidence:TABLE_KEY -->` in a report to embed a canonical result table. Declare the key in that report's `tables` list in `website/studies.json`; the build rejects undeclared or missing table references. Values are rendered directly from the observation JSON. To change measurements or model properties, edit canonical JSON with provenance, then run `python harness/analysis/render_summaries.py`. To add an experiment, create its schema-valid configuration and add explicit investigation/evidence associations where applicable. Unnumbered follow-ups remain evidence tables until the team assigns IDs.

The Benchmarking directory lists seven investigations by phase and category. Each report identifies the workload and timing boundary of its results. Unnumbered runs remain in the canonical evidence tables.

## Deployment

The actual origin is `erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing`; `mkdocs.yml` uses that project-site URL. The workflow builds and checks pull requests without deploying. Only a push to `main` can deploy via the `github-pages` environment, `upload-pages-artifact` and `deploy-pages`. Configure required reviewers on that environment if a separate release approval is wanted. The user's brief says Pages uses GitHub Actions; account settings have not been independently inspected.

No changes are pushed or published by local build commands. Review the scientific content and source permissions before merging to `main`. The workflow has not run on GitHub during local implementation.

## Audit and evidence decisions

The starting checkout was clean on `feat/research-site`, with 13 experiment configurations, six model records, five datasets and seven systems. No original raw artifacts or runnable benchmark harness were present. Two additional report revisions were supplied for this task; their hashes and crosswalk are in `docs/sources.md`. W supplies several previously missing commands, but does not establish independent reproduction. BLITZ-005 still lacks its original invocation.

The two research pillars share catalogues and methods. Benchmarking covers setup and source review, cross-platform performance, CPU scaling, embedded feasibility, model configuration, input-pipeline performance, and reference-aligned accuracy. Training-data selection remains open.

The principal publication gaps remain original artifact recovery, exact model/weight identities and parameter counts, R10.4.1 training-data selection, biological scoring, TX2 power calibration, conflicting RTX 3070 IDs and confidential SoCall publication permission. Source PDFs are not redistributed.

## Initial implementation validation on 2026-11-20

These build/browser results precede the later appearance and investigation-report revisions; they do not certify the revised build.

- `mkdocs build --strict`: passed after the final research metadata/source updates.
- Metadata validation: 31 records, four schemas and references to seven scenarios passed.
- Canonical Markdown renderer freshness: passed as part of the build hook.
- `website/check_site.py`: passed for 64 HTML pages, local links/fragments, all 13 registry records and publication boundaries.
- Browser: inspected homepage, study, experiment and registry rendering; followed the Benchmarking → CPU parallelism → BLITZ-005 path. Registry controls and all 13 records rendered.
- Further interaction and mobile testing stopped at the user's request. Search/filter behavior, mobile viewport layout and comprehensive accessibility checks were not fully exercised.
- GitHub Actions execution and deployment were not run. No benchmarks were executed, and no changes were pushed or published.

Review the research interpretation and PDF/publication permissions before merging. The deployment job is gated to a push on `main`; pull requests and manual workflow dispatches build without publication.
