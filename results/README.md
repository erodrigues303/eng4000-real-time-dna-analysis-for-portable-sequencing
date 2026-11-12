# Results and evidence

`raw/<system>/<basecaller>/<scenario>/<experiment-id>/` is reserved for original evidence. No original raw artifacts accompanied the supplied PDFs, so no historical raw directories or synthetic measurement files have been created.

For future runs, include `manifest.yaml` (experiment-schema record plus artifact references), `runs.csv`, `power.csv` when measured, stdout/stderr, environment details, validation report and `output.sha256`. Large artifacts remain external; the manifest records location, size, SHA-256 and access conditions. Suggested run columns: variant, run_index, warmup, start_utc, end_utc, wall_time_s, exit_status, input_samples, completed_reads, output_bases, peak_rss_mib. Power columns: timestamp_utc, power_w, scope, sensor, quality_flag. These are proposed formats, not implemented collectors.

`results/summaries/report-observations.json` stores secondary report transcriptions with PDF pages, units and scope. It is not raw data. `historical-summary.md` is generated from that file; reported values remain unchanged even where rounded or inconsistent. Original artifacts and independent reproduction are needed before validation. No inferred per-run values are synthesized from means/SDs.

Generate tables: `python harness/analysis/render_summaries.py`. Check freshness: add `--check`. No plots have been introduced; future figures must include generating code and cite the exact observation records.
