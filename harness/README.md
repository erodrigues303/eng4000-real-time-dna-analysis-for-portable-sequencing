# Harness boundary

Phase 1 provides metadata validation and report-table rendering only. There is no basecaller execution framework yet.

- `runners/`: future thin wrappers retaining commands, exit codes, timing boundaries and artifacts.
- `telemetry/`: future scoped collectors with synchronized timestamps, sensor units and gap checks.
- `analysis/`: current metadata checks and deterministic report-derived tables/cards; future reference alignment and energy analysis.

Do not execute historical configs whose commands are null. Follow [methodology](../docs/methodology.md) and recover original scripts first.
