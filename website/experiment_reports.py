"""Render compact experiment reports from catalogue records and measured evidence."""
import csv
import html
import json
import re
from statistics import mean, stdev

from render_summaries import cell, evidence_table_body


def label_value(value):
    if isinstance(value, list):
        return ", ".join(label_value(item) for item in value)
    if isinstance(value, int):
        return f"{value:,}"
    return str(value) if value is not None else ""


def compact_table(columns, rows):
    return evidence_table_body({"key": "experiment", "columns": columns, "rows": rows})


def artifact_path(record, root, name):
    matches = [root / item["location"] for item in record["artifacts"]
               if item["location"].rsplit("/", 1)[-1] == name]
    if len(matches) != 1:
        raise ValueError(f"Expected one {name} artifact for {record['experiment_id']}")
    return matches[0]


def json_artifact(record, root, name):
    return json.loads(artifact_path(record, root, name).read_text(encoding="utf-8"))


def csv_artifact(record, root, name):
    with artifact_path(record, root, name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def stage_table(stages, title="Stage timing"):
    names = {"h2d": "Host to device", "d2h": "Device to host", "forward": "Inference", "read_io": "Read input"}
    rows = [(names.get(key, key.capitalize()), f"{seconds:,.3f}") for key, seconds in stages.items()]
    return f"### {title}\n\n" + compact_table(["Stage", "Seconds"], rows)


def historical_results(selectors, tables):
    summary, details = [], []
    for key, selector in selectors.items():
        table = tables[key]
        if selector is None:
            title = "CPU thread scaling and module-input power" if key == "tx2" else table["title"]
            details.append(f"### {title}\n\n" + compact_table(table["columns"], table["rows"]))
            continue
        matches = [row for row in table["rows"] if row[0] == selector]
        if len(matches) != 1:
            raise ValueError(f"Expected one row for {selector!r} in {key}")
        labels = table["columns"][1:]
        values = matches[0][1:]
        if key == "dorado-d1":
            labels, values = labels[1:], values[1:]
            labels[-1] = "5 kHz full-channel reference (%)"
        elif key == "dorado-memory":
            labels = ["Memory and output"]
        elif key == "dorado-power":
            labels = [f"Reported {name[0].lower()}{name[1:]}" for name in labels]
        elif key == "blitz-power":
            # The setup rows already show the thread count and workload.
            labels, values = labels[2:], values[2:]
            labels = ["Power-session duration (s)", "Average / sampled peak CPU-package power (W)",
                      "CPU-package energy (J)", "CPU-package efficiency (samples/J)", "Power-session samples/s"]
        summary.extend(zip(labels, values, strict=True))
    return summary, details


def accuracy_results(summary):
    return [
        ("Reads scored", label_value(summary["reads"])),
        ("Mapped reads", f"{summary['mapped_reads']:,} ({summary['mapped_fraction']:.2%})"),
        ("Median / mean mapped-read identity", f"{summary['median_identity']:.2%} / {summary['mean_identity']:.2%}"),
        ("Pooled alignment identity", f"{summary['pooled_identity']:.2%}"),
        ("Substitution / insertion / deletion rate",
         " / ".join(f"{summary[key]:.2%}" for key in ("substitution_rate", "insertion_rate", "deletion_rate"))),
        ("Aligned predicted bases", f"{summary['aligned_base_fraction']:.2%}"),
        ("Predicted bases", label_value(summary["total_bases"])),
    ]


def jetson_power_results(power, capture):
    rows = [
        ("Capture", capture),
        ("Duration / sampling interval (s)", f"{power['duration_s']:g} / {power['interval_s']:g}"),
        ("Average / peak module-input power (W)", f"{power['avg_VDD_IN_W']:g} / {power['peak_VDD_IN_W']:g}"),
        ("Idle / average above idle (W)", f"{power['idle_VDD_IN_W']:g} / {power['avg_above_idle_W']:g}"),
        ("Gross module-input energy over the capture (J)", f"{power['energy_J_gross']:,}"),
        ("Average GPU / CPU rail power (W)", f"{power['avg_VDD_SYS_GPU_W']:g} / {power['avg_VDD_SYS_CPU_W']:g}"),
        ("Average GPU / CPU utilization", f"{power['avg_gpu_util_pct']:g}% / {power['avg_cpu_util_pct']:g}%"),
        ("Peak system RAM", f"{power['peak_ram_used_MB']:,} MB"),
        ("Peak GPU temperature", f"{power['peak_gpu_temp_C']:g} °C"),
    ]
    return "### Module-input power and energy\n\n" + compact_table(["Measurement", "Recorded value"], rows)


# Records that ran a derived model name it in environment.model_variant; the unchanged model is socall-v1.
MODEL_VARIANTS = {
    "socall-v1-bnfold": "BatchNorm folded into the convolutions, FP32, 446,205 parameters",
    "socall-v1-fp16": "BatchNorm folded, FP16 weights and activations, log-softmax in FP32",
}

TX2_SESSION_IDS = {"SOCALL-006", "SOCALL-007", "SOCALL-008", "SOCALL-009", "SOCALL-010", "SOCALL-011",
                   "SOCALL-012", "SOCALL-013", "SOCALL-014", "SOCALL-015", "SOCALL-016"}


def repeated_tx2_results(record, root):
    """Records whose process runs each wrote run-stats_<tag>.json and power-summary_<tag>.json."""
    def kept(prefix):
        # Excluded attempts reuse the same file names under excluded/, so select by full location.
        return [json.loads((root / location).read_text(encoding="utf-8")) for location in sorted(
            item["location"] for item in record["artifacts"]
            if item["location"].rsplit("/", 1)[-1].startswith(prefix) and "/excluded/" not in item["location"])]

    stats = kept("run-stats_")
    powers = kept("power-summary_")
    rates = [p["input_samples"] / p["wall_time_s"] for s in stats for p in s["per_pass"]]
    spread = f" ± {stdev(rates):,.0f}" if len(rates) > 1 else ""
    summary = [
        ("Mean ± sample SD over timed passes (samples/s)" if len(rates) > 1 else "Signal throughput (samples/s)",
         f"{mean(rates):,.0f}{spread}"),
        ("Share of the 2.048 M samples/s 4 kHz target", f"{mean(rates) / 2.048e6:.1%}"),
        ("Peak CUDA allocation", f"{max(s['cuda_max_memory_allocated_mib'] for s in stats):g} MiB"),
    ]
    run_rows = [(i, s["started_utc"], len(s["per_pass"]), f"{s['wall_seconds']:,.2f}", f"{s['samples_per_second']:,.0f}",
                 f"{p['avg_VDD_IN_W']:g}", f"{p['avg_gpu_util_pct']:g}%")
                for i, (s, p) in enumerate(zip(stats, powers, strict=True), 1)]
    runs = "### Process runs\n\n" + compact_table(
        ["Run", "Start (UTC)", "Timed passes", "Timed wall (s)", "Samples/s", "Avg VDD_IN (W)", "GPU util"], run_rows)
    stages = {name: sum(s["stage_seconds"][name] for s in stats) for name in stats[0]["stage_seconds"]}
    power = jetson_power_results(powers[-1], f"Process run {len(powers)}, including setup and warm-up")
    stage_title = "Stage timing summed over all timed passes"
    return summary, [runs, power, stage_table(stages, stage_title)]


def socall_results(record, root):
    eid = record["experiment_id"]
    if eid in TX2_SESSION_IDS:
        return repeated_tx2_results(record, root)
    if eid in {"SOCALL-001", "SOCALL-002"}:
        stats = json_artifact(record, root, "run-stats.json")
        return [
            ("Profiled wall time (s)", f"{stats['wall_seconds']:,.2f}"),
            ("Profiled signal throughput (samples/s)", f"{stats['samples_per_second']:,.2f}"),
        ], [stage_table(stats["stage_seconds"])]

    if eid == "SOCALL-003":
        runs = csv_artifact(record, root, "timing.csv")
        run_rows = [(i, run["wall_s"], run["Msamples_s"], run["inference"], run["decode"])
                    for i, run in enumerate(runs, 1)]
        run_columns = ["Process run", "Timed passes (s)", "Million samples/s", "Inference (s)", "Decode (s)"]
        power_name = "power-summary.json"
        capture = "Both process runs, including setup and warm-up"
        summary = []
    else:
        runs = csv_artifact(record, root, "runs.csv")
        run_rows = [(i, run["wall_time_s"], run["samples_per_s"], run["peak_rss_mib"])
                    for i, run in enumerate(runs, 1)]
        run_columns = ["Timed pass", "Wall time (s)", "Samples/s", "Peak process RSS (MiB)"]
        if eid == "SOCALL-004":
            rates = [float(run["samples_per_s"]) for run in runs]
            repetitions = [json_artifact(record, root, f"run-stats_rep{i}.json")
                           for i in range(1, record["measured_run_count"] + 1)]
            summary = [
                ("Mean ± sample SD over timed passes (samples/s)", f"{mean(rates):,.0f} ± {stdev(rates):,.0f}"),
                ("Peak CUDA allocation", f"{max(rep['cuda_max_memory_allocated_mib'] for rep in repetitions):g} MiB"),
            ]
            stages = {name: sum(rep["stage_seconds"][name] for rep in repetitions)
                      for name in repetitions[0]["stage_seconds"]}
            power_name = "power-summary_rep4.json"
            capture = "Repetition 4 only, including setup and warm-up"
        else:
            stats = json_artifact(record, root, "run-stats_cpu5.json")
            summary = [
                ("Timed wall time (s)", f"{stats['wall_seconds']:,.4f}"),
                ("Signal throughput (samples/s)", f"{stats['samples_per_second']:,.1f}"),
                ("Base throughput (bases/s)", f"{stats['bases_per_second']:,.1f}"),
                ("Peak process RSS", f"{stats['peak_rss_mib']:,.0f} MiB"),
            ]
            power_name = "power-summary_cpu5.json"
            capture = "Five-read CPU process, including setup and warm-up"
    power = jetson_power_results(json_artifact(record, root, power_name), capture)
    if eid == "SOCALL-005":
        return summary, [stage_table(stats["stage_seconds"]), power]
    timing = "### Repeated timing\n\n" + compact_table(run_columns, run_rows)
    if eid == "SOCALL-004":
        return summary, [timing, power, stage_table(stages, "Stage timing across eight timed passes")]
    return summary, [timing, power]


def experiment_page(record, report, system, dataset, models, selectors, tables, scoring, related, root):
    eid = record["experiment_id"]
    tool = record["tool"]
    environment = record["environment"]
    is_socall = eid.startswith("SOCALL-")
    tool_name = "SoCall" if is_socall else tool["name"]
    software = " · ".join(part for part in (tool_name, tool["version"], tool["commit"]) if part)
    model_links = []
    for model_id, model in models.items():
        name = model["full_model_name"] or ("SoCall FP32 weights_30.pt" if is_socall else model["basecaller"])
        details = [model.get("parameter_count")]
        if model_id == "blitz-network64":
            details.append(model["architecture"])
        model_links.append(f"[{name}](../models/{model_id}.md)" + "".join(
            f" · {label_value(value)}" for value in details if value is not None
        ))
    variant = (record.get("environment") or {}).get("model_variant")
    if variant in MODEL_VARIANTS:
        model_links.append(f"Variant {variant}: {MODEL_VARIANTS[variant]}")
    summary = [
        ("Basecaller", software),
        ("Model", "<br>".join(model_links)),
        ("Hardware / backend", f"[{report['backend']}](../systems/{record['system_id']}.md)" if system else report["backend"]),
        ("Operating system", system.get("os") if system else None),
    ]

    if dataset:
        dataset_id = record["dataset_id"]
        source = dataset["source"]
        url = re.search(r"https?://[^\s;]+", dataset["download_reference"] or "")
        source_url = url.group() if url else None
        if dataset_id == "D1":
            source_url = "https://github.com/WGLab/DeepMod2/releases/tag/v0.3.0"
        reads, samples = dataset["read_count"], dataset["signal_sample_count"]
        input_format = dataset["file_format"]
        if eid in {"SOCALL-003", "SOCALL-004", "SOCALL-005"} or (eid in TX2_SESSION_IDS and dataset_id == "D1"):
            input_format += " → calibrated float32 NPZ"
        elif eid in TX2_SESSION_IDS:
            input_format += ", streamed one read at a time"
        if eid == "SOCALL-005":
            stats = json_artifact(record, root, "run-stats_cpu5.json")
            reads, samples = stats["reads"], stats["dataset_samples"]
        input_details = [input_format, f"{reads:,} reads" if reads is not None else None,
                         f"{samples:,} signal samples" if samples is not None else None]
        summary.extend([
            ("Dataset", f"[{dataset_id} · {dataset['name']}](../datasets/{dataset_id}.md)"),
            ("Dataset source", f"[{source}]({source_url})" if source_url else source),
            ("Input", " · ".join(part for part in input_details if part)),
            ("Chemistry", dataset["chemistry"]),
            ("Acquisition kit", dataset["kit_model"].removeprefix("Inspected file: ") if dataset["kit_model"] else None),
            ("Sampling rate", f"{dataset['sampling_frequency_hz']:,} Hz" if dataset["sampling_frequency_hz"] else None),
        ])
        if dataset_id == "D5" and (eid in scoring or eid in TX2_SESSION_IDS):
            summary.append(("Reference", "[A. pittii 16-377-0801 circular chromosome](https://doi.org/10.26180/5c5a5fcf72e40) · 3,814,719 bp"))

    settings = record["settings"]
    setting_labels = {"chunk_size": "chunk size (samples)", "overlap": "overlap (samples)",
                      "batch_size": "batch size", "caller_threads": "caller threads", "beam_size": "beam width"}
    setup = [f"{label}: {label_value(settings[key])}" for key, label in setting_labels.items()
             if settings.get(key) is not None]
    if setup:
        summary.append(("Settings", " · ".join(setup)))
    if is_socall:
        decoder = "CTC beam search" if settings["beam_size"] else "Greedy CTC"
        if report.get("decode"):
            decoder += f" · {report['decode']}"
        summary.extend([("Decoder", decoder), ("Precision", "FP32"), ("Normalization", "Per-read median / MAD")])
    runtime = [f"{label} {environment[key]}" for key, label in [
        ("python", "Python"), ("torch", "PyTorch"), ("cuda", "CUDA"), ("cudnn", "cuDNN"),
        ("mappy", "mappy"), ("fast-ctc-decode", "fast-ctc-decode")
    ] if environment.get(key)]
    if runtime:
        summary.append(("Software environment", " · ".join(runtime)))
    if environment.get("OMP_NUM_THREADS"):
        summary.append(("OpenMP threads", environment["OMP_NUM_THREADS"]))
    if environment.get("power_mode"):
        summary.append(("Power mode", environment["power_mode"]))

    timing = (report.get("timing") or record["timing_scope"] or "").removesuffix("; exact timer boundaries TBD")
    summary.extend([
        ("Timing boundary" if eid != "BLITZ-010" else "Scoring scope", timing),
        ("Warm-ups" if not is_socall else "Warm-up passes per process", record["warmup_count"]),
        ("Measured runs per setting" if eid in {"BLITZ-003", "BLITZ-005", "BLITZ-009"} else
         "Measured process runs" if is_socall else "Measured runs",
         record["measured_run_count"]),
        ("Workload passes per process" if is_socall else "Workload repetitions",
         record["workload_repetitions"] if record["workload_repetitions"] not in {None, 1} else None),
        ("Output", record["output_format"]),
        ("Output check", report.get("output_check")),
    ])
    if eid in {"BLITZ-003", "BLITZ-005", "BLITZ-007"}:
        summary.append(("Memory measurement", record["telemetry"]["memory_method"]))
    if eid in {"BLITZ-006", "BLITZ-008", "BLITZ-009"}:
        interval = record["telemetry"]["sampling_interval_s"]
        summary.append(("Power measurement", ("HWiNFO64 CPU-package power" if eid != "BLITZ-009" else "INA3221 module input (VDD_IN)")
                        + (f", sampled every {interval:g} s" if interval else "")))

    results, details = historical_results(selectors, tables)
    if eid in TX2_SESSION_IDS and record["dataset_id"] == "D5":
        scoring = dict(scoring, **{eid: json_artifact(record, root, "accuracy.json")})
    if eid in scoring:
        results.extend(accuracy_results(scoring[eid]))
        results.append(("Scoring method", "minimap2 map-ont via mappy 2.31, primary alignments"))
    if is_socall:
        run_summary, run_details = socall_results(record, root)
        results.extend(run_summary)
        details.extend(run_details)
    if eid == "DORADO-003":
        results.append(("Complete command (s)", "Approximately 12"))

    title = f"{eid} — {report['title']}"
    metadata = " · ".join(html.escape(part) for part in (record["date"], record["owner"]) if part)
    sections = [f"# {title}", f'<p class="experiment-meta">{metadata}</p>' if metadata else "", report["objective"],
                "## Setup and results", compact_table(["Item", "Recorded value"], [
                    (label, label_value(value)) for label, value in summary + results if value is not None and value != ""
                ])]
    if details:
        sections.extend(["## Detailed results", *details])
    if record["command"]:
        command = record["command"]
        fence = "`" * max(3, 1 + max((len(run) for run in re.findall(r"`+", command)), default=0))
        sections.extend(["## Recorded command", f"{fence}text\n{command}\n{fence}"])
    sections.extend(["## Observations", report["observation"], "## Limitations", report["limitations"]])
    if eid in {"DORADO-001", "DORADO-002", "DORADO-003", "DORADO-004"}:
        sections.append("The scope and timing window of the recorded power readings are unverified. They cannot be used to estimate energy.")
    links = []
    if related:
        links.extend(f"[{study['title']}](../benchmarking/{slug}.md)" for slug, study in related)
    elif is_socall:
        links.append("[SoCall Engineering: Baseline characterization](../socall/index.md#baseline-characterization)")
    links.append(f"[Machine-readable configuration](../configs/experiments/{eid}.yaml)")
    if eid == "BLITZ-010":
        scored = "../results/raw/brian-7800x3d/blitz/reference-accuracy/BLITZ-010"
        links.extend([f"[Accuracy JSON]({scored}/accuracy.json)", f"[Per-read alignments]({scored}/alignments.csv)"])
    sections.extend(["---", " · ".join(links)])
    return "\n\n".join(section for section in sections if section) + "\n"
