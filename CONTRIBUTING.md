# Contributing

Each of the six team members should submit focused PRs with evidence another teammate can inspect.

- Branches: `codex/<topic>` for agent work; `feat/<issue>-<topic>`, `docs/<issue>-<topic>` or `fix/<issue>-<topic>` for team work.
- Experiment IDs: `<TOOL>-<three-digit sequence>` (e.g. `BLITZ-010`). Reserve the next unused number in a PR. Preserve historical IDs and record aliases; use variant labels for thread/batch/chunk settings. Do not silently rename or overwrite results.
- Documentation belongs in `docs/`; execution in `harness/runners/`; sensors in `harness/telemetry/`; derived analysis in `harness/analysis/`; definitions in `configs/`; catalogues in `systems/`, `models/`, `datasets/`; owned compatibility changes in `ports/`.
- Minimum benchmark record: ID/date/owner, tool version/commit, model/dataset/system IDs and hashes, exact shell/command/environment, settings, warm-up and measured counts, timing/telemetry scope, units, output validation, artifact locations/checksums and limitations. Missing historical fields use null plus an explicit TBD note. No result without provenance.
- PRs explain the question, change, validation, evidence and limitations. Include per-run observations, failures/exclusions and the script behind derived tables; a teammate reviews comparison validity. Do not upgrade preliminary evidence merely because it parses.
- Run `python harness/analysis/validate_metadata.py` and `python harness/analysis/render_summaries.py --check` with `requirements-dev.txt` installed. Generated cards/tables must match their source records.
- Do not commit large signal datasets, FASTQ/BAM outputs, weights, archives or giant telemetry dumps. Use external immutable locations and checksums. Small genuine raw artifacts may be reviewed for size/privacy; `.gitignore` is not a complete safety control.
- Never commit credentials, private links with access tokens or personal identifiers. **Do not publish SoCall code, weights or unpublished implementation details until publication permission is explicitly confirmed.** Keep restricted work outside public paths.

The reports' “public non-human only” policy conflicts with historical human D1 use; resolve future dataset policy with the team. Do not erase or misrepresent historical records. See [source reconciliation](docs/sources.md).
