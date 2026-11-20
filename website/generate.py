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
from validate_metadata import main as validate_metadata
from render_summaries import outputs, cell


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path, content):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def fields(record):
    return "| Field | Recorded value |\n|---|---|\n" + "\n".join(
        f"| {key.replace('_', ' ')} | {cell(value)} |" for key, value in record.items()) + "\n"


def table_markup(table):
    return (f"<h2 id=\"{table['key']}\">{html.escape(table['title'])}</h2>\n\n"
            f"Source: {table['source']}. {table['status']}.\n\n{table['notes']}\n\n"
            + "| " + " | ".join(map(cell, table["columns"])) + " |\n"
            + "|" + "|".join("---" for _ in table["columns"]) + "|\n"
            + "\n".join("| " + " | ".join(map(cell, row)) + " |" for row in table["rows"]) + "\n\n")


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
    for path in paths:
        if path.name == "README.md" and path.parent.name in {"models", "datasets", "systems"}:
            continue
        target = OUT / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    tables = {t["key"]: t for t in read("results/summaries/report-observations.json")["tables"]}
    studies = read("website/studies.json")
    records = [read(p.relative_to(ROOT)) for p in sorted((ROOT / "configs/experiments").glob("*.yaml"))]
    ids = {r["experiment_id"] for r in records}
    for slug, study in studies.items():
        if set(study["experiments"]) - ids or set(study["tables"]) - tables.keys():
            raise ValueError(f"Invalid study references: {slug}")
        if not (OUT / f"benchmarking/{slug}.md").exists():
            raise ValueError(f"Missing study: {slug}")
    # Table links are explicit editorial associations, never guessed from experiment numbering.
    associations = read("website/experiment-evidence.json")
    if set(associations) - ids:
        raise ValueError("Evidence links reference an unknown experiment")
    registry = []
    for record in records:
        eid = record["experiment_id"]
        related = [(s, v) for s, v in studies.items() if eid in v["experiments"]]
        links = "\n".join(f"- [{v['title']}](../benchmarking/{s}.md)" for s, v in related) or "No linked research study yet."
        command = "```text\n" + record["command"] + "\n```\n\nReport-transcribed command; not rerun or independently verified. Paths and environment must be recovered before use." if record["command"] else "**Exact command not supplied.** This record is not an executable reproduction recipe."
        content = f"# {eid}\n\n{record['tool']['name']} · {record['date'] or 'Date not recorded'} · {record['owner'] or 'Owner not recorded'}\n\n"
        content += f"> **{record['status']}** · Workflow completion: reported in secondary evidence. Raw artifacts: {'listed; verify access' if record['artifacts'] else 'not supplied'}. Independent reproduction: not established.\n\n"
        content += "## Research context\n\n" + links + "\n\n"
        content += f"## Inputs and environment\n\n[Dataset {record['dataset_id']}](../datasets/{record['dataset_id']}.md) · [System {record['system_id']}](../systems/{record['system_id']}.md)\n\n"
        content += " · ".join(f"[Model: {mid}](../models/{mid}.md)" for mid in record["model_ids"])
        content += "\n\n## Execution and measurement\n\n" + command + "\n\n"
        content += fields({k: record[k] for k in ["tool", "shell", "working_directory", "environment", "settings", "warmup_count", "measured_run_count", "workload_repetitions", "timing_scope", "telemetry", "output_format", "output_validation"]})
        content += "\n## Reported results\n\n"
        for key in associations.get(eid, []):
            if key not in tables:
                raise ValueError(f"Unknown evidence table {key}")
            content += f"[{tables[key]['title']}](../evidence/index.md#{key}) — {tables[key]['source']}. Shared tables may contain other configurations; use the labelled experiment row.\n\n"
        if not associations.get(eid):
            content += "No numerical result table is linked. See the recorded output validation above.\n\n"
        content += "## Limitations\n\n" + "\n".join("- " + x for x in record["limitations"])
        content += f"\n\n## Configuration and evidence\n\n- [Canonical configuration](../configs/experiments/{eid}.yaml)\n- [Evidence register and revision conflicts](../docs/sources.md)\n- [Reproduction guide](../resources/reproduce.md)\n\nProvenance: {'; '.join(record['provenance'])}.\n\n"
        content += "Original raw logs, output files and checksums are unavailable in this checkout. Report citations are secondary evidence.\n" if not record["artifacts"] else fields({"artifacts": record["artifacts"]})
        write(f"experiments/{eid}.md", content)
        system = read(f"systems/{record['system_id']}.json")
        searchable = json.dumps([record, system, [s['title'] for _, s in related]], ensure_ascii=False).lower()
        registry.append({"id": eid, "tool": record["tool"]["name"], "system": record["system_id"], "dataset": record["dataset_id"], "search": searchable, "command": bool(record["command"])})
    controls = '<div id="registry-controls" hidden><div class="filters"><label>Search experiments<input id="query" type="search" placeholder="ID, hardware, model, research question"></label>'
    controls += ''.join(f'<label>{label}<select id="filter-{key}"><option value="">All {label.lower()}</option></select></label>' for key, label in [("tool", "Basecallers"), ("system", "Systems"), ("dataset", "Datasets")])
    controls += '</div><button id="reset-filters" type="button">Reset filters</button><p id="result-count" role="status" aria-live="polite"></p></div>'
    rows = []
    for r in registry:
        attrs = ' '.join(f'data-{key}="{html.escape(r[key], quote=True)}"' for key in ["tool", "system", "dataset", "search"])
        rows.append(f'<tr {attrs}><td><a href="{r["id"]}/">{r["id"]}</a></td><td>{r["tool"]}</td><td>{r["system"]}</td><td>{r["dataset"]}</td><td>{"Report command available" if r["command"] else "Command missing"}; raw artifacts missing</td></tr>')
    write("experiments/index.md", "# Experiment registry\n\nHistorical records, searchable by scientific question, model, hardware and ID. All current records are preliminary; schema validation does not establish scientific validity.\n\n" + controls + '<noscript><p>Search requires JavaScript. All records remain available below.</p></noscript><table id="registry"><thead><tr><th>Experiment</th><th>Basecaller</th><th>System</th><th>Dataset</th><th>Evidence completeness</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table><p id="empty-state" hidden>No experiments match. Clear a filter or try another term.</p>\n\nUnnumbered follow-ups remain in the [evidence tables](../evidence/index.md); they have not been assigned invented experiment IDs.\n')
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
