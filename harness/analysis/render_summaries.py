"""Render report tables and catalogue cards without changing reported values."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TBD = "TBD — needs verification"

def cell(value):
    if value is None:
        return TBD
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("|", r"\|").replace("\n", "<br>")

def evidence_table_body(table):
    note = (table.get("notes") or "").strip()
    columns = table["columns"]
    lines = [note, ""] if note else []
    lines += ["| " + " | ".join(map(cell, columns)) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in table["rows"]:
        if len(row) != len(columns):
            raise ValueError(f"Wrong row width: {table['key']}")
        lines.append("| " + " | ".join(map(cell, row)) + " |")
    return "\n".join(lines)

def outputs():
    for folder, kind in [("models", "model"), ("systems", "system"), ("datasets", "dataset")]:
        for path in sorted((ROOT / folder).glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            lines = [f"# {record[kind + '_id']}", "", f"Generated from `{path.name}`; edit the JSON and rerun the renderer.", "", "| Field | Recorded value |", "|---|---|"]
            lines += [f"| {key.replace('_', ' ')} | {cell(value)} |" for key, value in record.items()]
            lines += ["", "Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry."]
            yield path.with_suffix(".md"), "\n".join(lines) + "\n"
    records = json.loads((ROOT / "results/summaries/report-observations.json").read_text(encoding="utf-8"))
    lines = ["# Historical results — preliminary report transcriptions", "", "Generated from `report-observations.json`; no new benchmark runs or raw telemetry are represented. All numerical precision is retained as reported. [Evidence register](../../docs/sources.md).", ""]
    for table in records["tables"]:
        lines += [f"## {table['title']}", "", evidence_table_body(table), ""]
    yield ROOT / "results/summaries/historical-summary.md", "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files differ; do not write")
    args = parser.parse_args()
    stale = []
    count = 0
    for path, content in outputs():
        count += 1
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated files: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Rendered'} {count} files.")

if __name__ == "__main__":
    main()
