"""MkDocs hook: validated, allowlisted publication; never execute scientific workloads."""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".site-docs"
sys.path.insert(0, str(ROOT / "harness/analysis"))
sys.path.insert(0, str(ROOT / "website"))
from experiment_reports import experiment_page
from validate_metadata import main as validate_metadata
from render_summaries import evidence_table_body, outputs


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path, content):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def table_markup(table, heading_level=2):
    tag = f"h{heading_level}"
    key = html.escape(table["key"], quote=True)
    title = html.escape(table["title"])
    return f'<{tag} id="{key}">{title}</{tag}>\n\n{evidence_table_body(table)}\n\n'


def chart(table):
    """Accessible standalone SVG; values come exclusively from the transcription."""
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 330" role="img" aria-labelledby="title desc">',
             '<title id="title">BLITZ-005 full-command runtime by caller threads</title>',
             '<desc id="desc">Ryzen 7 7800X3D, D4, network 64. Mean and sample SD of three runs per setting. Values are also in the adjacent table.</desc>',
             '<style>:root{color-scheme:light dark;--paper:#fff;--ink:#1c303d;--grid:#d8e2e5;--bar:#116961;--whisker:#132833}'
             '@media(prefers-color-scheme:dark){:root{--paper:#181818;--ink:#d4d4d4;--grid:#343638;--bar:#79bdb0;--whisker:#e5edf0}}'
             '.paper{fill:var(--paper)}.labels{fill:var(--ink)}.grid{stroke:var(--grid)}.bar{fill:var(--bar)}.whisker{stroke:var(--whisker)}</style>',
             '<rect class="paper" width="800" height="330"/>',
             '<g class="labels" font-family="system-ui,sans-serif" font-size="16">']
    for tick in range(0, 21, 5):
        x = 110 + tick * 27
        parts += [f'<path class="grid" d="M{x} 30V260"/>', f'<text x="{x}" y="285" text-anchor="middle">{tick}</text>']
    for i, row in enumerate(table["rows"]):
        mean, sd = map(float, row[1].split(" ± "))
        y = 50 + i * 55
        end, left, right = 110 + mean * 27, 110 + (mean - sd) * 27, 110 + (mean + sd) * 27
        parts += [f'<text x="90" y="{y+21}" text-anchor="end">{row[0]}</text>',
                  f'<rect class="bar" x="110" y="{y}" width="{mean*27}" height="30"/>',
                  f'<path class="whisker" d="M{left} {y+15}H{right} M{left} {y+8}V{y+22} M{right} {y+8}V{y+22}" stroke-width="2"/>',
                  f'<text x="{end+15}" y="{y+21}">{row[1]} s</text>']
    parts += ['<text x="380" y="320" text-anchor="middle">Full-command runtime (seconds; mean ± sample SD)</text>',
              '<text transform="translate(25 165) rotate(-90)" text-anchor="middle">Caller threads</text>', '</g></svg>']
    write("assets/blitz005-runtime.svg", "\n".join(parts))


def on_config(config):
    config.docs_dir = str(OUT)
    validate_metadata()
    for path, content in outputs():
        if path.read_text(encoding="utf-8") != content:
            raise ValueError(f"Stale canonical rendering: {path.relative_to(ROOT)}")
    # Only this exact generated staging directory may be cleared.
    if OUT.exists():
        if OUT.is_symlink() or OUT.resolve() != ROOT.resolve() / ".site-docs":
            raise ValueError("Unsafe staging directory")
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "website/content", OUT)
    # Explicit public allowlist. PDFs, local evidence, weights and source ports never enter it.
    paths = [ROOT / "CONTRIBUTING.md"]
    for folder in ["datasets", "models", "systems", "schemas", "configs/experiments", "configs/scenarios", "results", "results/summaries", "ports"]:
        paths += [p for p in (ROOT / folder).iterdir() if p.is_file() and p.suffix in {".md", ".json", ".yaml"}]
    paths += [ROOT / "docs" / name for name in ["methodology.md", "mlcommons-alignment.md", "sources.md", "gaps.md"]]
    paths += list((ROOT / "docs/platforms").glob("*.md"))
    paths += [ROOT / "docs/results/README.md", ROOT / "harness/README.md"]
    # Explicitly reviewed, non-human D5 scoring artifacts; do not publish raw/ broadly.
    paths += [ROOT / "results/raw/brian-7800x3d/blitz/reference-accuracy/BLITZ-010" / name
              for name in ["accuracy.json", "alignments.csv"]]
    for path in paths:
        if path.name == "README.md" and path.parent.name in {"models", "datasets", "systems"}:
            continue
        target = OUT / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    tables = {t["key"]: t for t in read("results/summaries/report-observations.json")["tables"]}
    studies = read("website/studies.json")
    d5 = read("results/summaries/d5-accuracy-comparison.json")
    scoring = d5["summaries"]
    columns = ["Metric", "Blitz network 64 / beam 5", "SoCall greedy", "SoCall beam 5"]
    metrics = [("reads", "Reads scored", False), ("mapped_reads", "Mapped reads", False),
               ("mapped_fraction", "Mapped reads (%)", True), ("median_identity", "Median mapped-read identity (%)", True),
               ("mean_identity", "Mean mapped-read identity (%)", True), ("pooled_identity", "Pooled identity (%)", True),
               ("substitution_rate", "Substitution rate (%)", True), ("insertion_rate", "Insertion rate (%)", True),
               ("deletion_rate", "Deletion rate (%)", True), ("aligned_base_fraction", "Aligned predicted bases (%)", True),
               ("total_bases", "Predicted bases", False)]
    lines = ["| " + " | ".join(columns) + " |", "|---|---:|---:|---:|"]
    for key, label, pct in metrics:
        values = [f"{100 * scoring[eid][key]:.2f}" if pct else f"{scoring[eid][key]:,}" for eid in ["BLITZ-010", "SOCALL-001", "SOCALL-002"]]
        lines.append("| " + " | ".join([label] + values) + " |")
    summary_table = "\n".join(lines)
    lines = ["| Paired metric | Blitz vs SoCall greedy | Blitz vs SoCall beam 5 |", "|---|---:|---:|"]
    for key, label in [("both_mapped", "Both mapped"), ("blitz_only_mapped", "Only Blitz mapped"),
                       ("socall_only_mapped", "Only SoCall mapped"), ("neither_mapped", "Neither mapped"),
                       ("blitz_higher", "Blitz higher identity, among both mapped"), ("socall_higher", "SoCall higher identity, among both mapped"),
                       ("ties", "Equal identity, among both mapped"), ("median_identity_difference_pp", "Median paired identity difference (Blitz minus SoCall, pp)"),
                       ("mean_identity_difference_pp", "Mean paired identity difference (pp)")]:
        values = [f"{d5['paired'][eid][key]:.2f}" if key.endswith("_pp") else f"{d5['paired'][eid][key]:,}" for eid in ["SOCALL-001", "SOCALL-002"]]
        lines.append("| " + " | ".join([label] + values) + " |")
    report_path = OUT / "benchmarking/d5-accuracy.md"
    report_path.write_text(report_path.read_text(encoding="utf-8").replace("<!-- d5-accuracy:summary -->", summary_table).replace("<!-- d5-accuracy:paired -->", "\n".join(lines)), encoding="utf-8")
    records = [read(p.relative_to(ROOT)) for p in sorted((ROOT / "configs/experiments").glob("*.yaml"))]
    ids = {r["experiment_id"] for r in records}
    for slug, study in studies.items():
        if set(study["experiments"]) - ids or set(study["tables"]) - tables.keys():
            raise ValueError(f"Invalid study references: {slug}")
        if not (OUT / f"benchmarking/{slug}.md").exists():
            raise ValueError(f"Missing study: {slug}")
        report_path = OUT / f"benchmarking/{slug}.md"
        report = report_path.read_text(encoding="utf-8")
        def evidence(match):
            key = match.group(1)
            if key not in study["tables"]:
                raise ValueError(f"Undeclared evidence table {key} in {slug}")
            return table_markup(tables[key], heading_level=3)
        report = re.sub(r"<!-- evidence:([a-z0-9-]+) -->", evidence, report)
        report_path.write_text(report, encoding="utf-8")
    # Shared evidence tables specify the exact first-column label for each experiment.
    associations = read("website/experiment-evidence.json")
    reports = read("website/experiment-reports.json")
    if set(associations) - ids or set(reports) != ids:
        raise ValueError("Experiment report metadata does not match the registry")
    registry = []
    for record in records:
        eid = record["experiment_id"]
        related = [(slug, study) for slug, study in studies.items() if eid in study["experiments"]]
        selectors = associations.get(eid, {})
        if selectors.keys() - tables.keys():
            raise ValueError(f"Unknown evidence table for {eid}")
        system_id, dataset_id = record["system_id"], record["dataset_id"]
        system = read(f"systems/{system_id}.json") if system_id else None
        dataset = read(f"datasets/{dataset_id}.json") if dataset_id else None
        models = {model_id: read(f"models/{model_id}.json") for model_id in record["model_ids"]}
        content = experiment_page(record, reports[eid], system, dataset, models,
                                  selectors, tables, scoring, related, ROOT)
        write(f"experiments/{eid}.md", content)
        searchable = json.dumps([record, system, reports[eid]["title"], [s['title'] for _, s in related]], ensure_ascii=False).lower()
        registry.append({"id": eid, "tool": record["tool"]["name"], "system": record["system_id"], "dataset": record["dataset_id"], "search": searchable, "command": bool(record["command"])})
    controls = '<div id="registry-controls" hidden><div class="filters"><label>Search experiments<input id="query" type="search" placeholder="ID, hardware, model, research question"></label>'
    controls += ''.join(f'<label>{label}<select id="filter-{key}"><option value="">All {label.lower()}</option></select></label>' for key, label in [("tool", "Basecallers"), ("system", "Systems"), ("dataset", "Datasets")])
    controls += '</div><button id="reset-filters" type="button">Reset filters</button><p id="result-count" role="status" aria-live="polite"></p></div>'
    rows = []
    for r in registry:
        attrs = ' '.join(f'data-{key}="{html.escape(r[key], quote=True)}"' for key in ["tool", "system", "dataset", "search"])
        rows.append(f'<tr {attrs}><td><a href="{r["id"]}/">{r["id"]}</a></td><td>{r["tool"]}</td><td>{r["system"]}</td><td>{r["dataset"]}</td><td>{"Report command available" if r["command"] else "Command missing"}; raw artifacts missing</td></tr>')
    write("experiments/index.md", "# Experiment registry\n Browse and search our benchmarking experiments by basecaller, hardware, or experiment ID.\n\n" + controls + '<noscript><p>Search requires JavaScript. All records remain available below.</p></noscript><table id="registry"><thead><tr><th>Experiment</th><th>Basecaller</th><th>System</th><th>Dataset</th><th>Evidence completeness</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table><p id="empty-state" hidden>No experiments match. Clear a filter or try another term.</p>\n')
    write("assets/experiments.json", json.dumps(registry, indent=2, ensure_ascii=False))
    write("evidence/index.md", "# Reported evidence tables\n\nThese are secondary report transcriptions, not recovered raw measurements. [Source hashes, page references and conflicts](../docs/sources.md). [Download canonical observations](../results/summaries/report-observations.json).\n\n" + ''.join(table_markup(t) for t in tables.values()))
    for folder, kind in [("models", "model"), ("datasets", "dataset"), ("systems", "system")]:
        lines = [f"# {folder.capitalize()} catalogue", "", "Generated from canonical JSON. Unknown properties remain explicitly unverified.", ""]
        for path in sorted((ROOT / folder).glob("*.json")):
            record = read(path.relative_to(ROOT))
            key = record[kind + "_id"]
            lines.append(f"- [{key}]({key}.md)")
        write(f"{folder}/index.md", "\n".join(lines))
    for path in OUT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for folder in ["models", "datasets", "systems"]:
            content = content.replace(f"{folder}/README.md", f"{folder}/index.md")
        path.write_text(content, encoding="utf-8")
    chart(tables["blitz005"])
    return config
