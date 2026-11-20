# Research website

The implementation contract is [docs/SITE_SPEC.md](../docs/SITE_SPEC.md), not a root-level file. The site uses **MkDocs 1.6.1**, a small local Jinja theme and plain JavaScript. This keeps Markdown authoring and Python metadata integration without a frontend build chain or backend. Zensical was considered, but the requested layout does not require another theme/runtime layer. MkDocs' documented hooks, custom theme and project-site URL support cover the requirements.

## Build and preview

From the repository root, Python 3.10+:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-site.txt
python -m mkdocs build --strict
python website/check_site.py
python -m mkdocs serve
```

Open the URL printed by MkDocs. The project path is included in preview:
`http://127.0.0.1:8000/eng4000-real-time-dna-analysis-for-portable-sequencing/`.

The generated staging directory is rebuilt at startup. After editing canonical metadata or authored content during preview, restart `mkdocs serve` to regenerate it; the default watcher observes the staging directory rather than all upstream sources.

## Source structure

Appearance automatically follows the device's light/dark preference through CSS `prefers-color-scheme`, including live preference changes. Dark mode uses charcoal surfaces, muted text and blue links. The generated SVG chart has its own matching palette. No JavaScript toggle or saved preference overrides the device setting.

- `website/content/`: human-authored home, research studies, SoCall overview, resources and About.
- `website/theme/`: semantic page template; assets live in `website/content/assets/`.
- `website/generate.py`: MkDocs configuration hook; validates metadata and builds ignored `.site-docs/`.
- `website/studies.json`: editorial study relationships only; no copied measurements.
- `website/experiment-evidence.json`: explicit links from stable experiment IDs to canonical evidence table keys.
- Existing `configs/`, `datasets/`, `models/`, `systems/`, `results/` and selected `docs/` remain canonical.
- `site-build/`: ignored production output, the only directory uploaded by Pages.

Every build generates the registry, individual `/experiments/ID/` records, catalogue indexes, report tables and the BLITZ-005 plot. Records come from the existing JSON-subset YAML files. The chart uses the existing observation JSON. Unknown fields are displayed rather than inferred. Copying source Markdown and metadata uses an explicit public allowlist; private weights, raw data, PDFs and `.local-evidence/` never enter the site.

To edit a study, edit its Markdown. To change measurements or model properties, edit the canonical JSON with provenance, then run `python harness/analysis/render_summaries.py`. To add an experiment, create its schema-valid configuration and add explicit study/evidence associations where applicable. Unnumbered follow-ups remain evidence tables until the team assigns IDs.

## Deployment

The actual origin is `erodrigues303/eng4000-real-time-dna-analysis-for-portable-sequencing`; `mkdocs.yml` uses that project-site URL. The workflow builds and checks pull requests without deploying. Only a push to `main` can deploy via the `github-pages` environment, `upload-pages-artifact` and `deploy-pages`. Configure required reviewers on that environment if a separate release approval is wanted. The user's brief says Pages uses GitHub Actions; account settings have not been independently inspected.

No changes are pushed or published by local build commands. Review the scientific content and source permissions before merging to `main`. The workflow has not run on GitHub during local implementation.

## Audit and evidence decisions

The starting checkout was clean on `feat/research-site`, with 13 experiment configurations, six model records, five datasets and seven systems. No original raw artifacts or runnable benchmark harness were present. Two additional report revisions were supplied for this task; their hashes and crosswalk are in `docs/sources.md`. W supplies several previously missing commands, but does not establish independent reproduction. BLITZ-005 still lacks its original invocation.

The two research pillars share catalogues and methods. SoCall's lifecycle is grouped on one substantive page because no measured baseline/profiling/optimization exists. Four study pages are supported by current secondary evidence. Speed–accuracy and training data remain open questions. All numerical statements link to evidence; the site does not turn output agreement into biological accuracy or short throughput into streaming capability.

The principal publication gaps remain original artifact recovery, exact model/weight identities and parameter counts, R10.4.1 training-data selection, biological scoring, TX2 power calibration, conflicting RTX 3070 IDs and confidential SoCall publication permission. Source PDFs are not redistributed.

## Validation completed on 2026-11-20

- `mkdocs build --strict`: passed after the final research metadata/source updates.
- Metadata validation: 31 records, four schemas and references to seven scenarios passed.
- Canonical Markdown renderer freshness: passed as part of the build hook.
- `website/check_site.py`: passed for 64 HTML pages, local links/fragments, all 13 registry records and publication boundaries.
- Browser: inspected homepage, study, experiment and registry rendering; followed the Benchmarking → CPU parallelism → BLITZ-005 path. Registry controls and all 13 records rendered.
- Further interaction and mobile testing stopped at the user's request. Search/filter behavior, mobile viewport layout and comprehensive accessibility checks were not fully exercised.
- GitHub Actions execution and deployment were not run. No benchmarks were executed, and no changes were pushed or published.

Review the research interpretation and PDF/publication permissions before merging. The deployment job is gated to a push on `main`; pull requests and manual workflow dispatches build without publication.
