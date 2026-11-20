# Harness boundary

Phase 1 provides metadata validation and report-table rendering only. There is no basecaller execution framework yet.

- `runners/`: future thin wrappers retaining commands, exit codes, timing boundaries and artifacts.
- `telemetry/`: future scoped collectors with synchronized timestamps, sensor units and gap checks.
- `analysis/`: metadata checks, report-derived tables/cards, and `reference_accuracy.py` (read-level accuracy of any FASTQ against a pinned reference; tests in `tests/`). Energy analysis is future work.

Do not execute historical configs whose commands are null. Follow [methodology](../docs/methodology.md) and recover original scripts first.
