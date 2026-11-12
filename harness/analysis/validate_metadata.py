"""Validate Phase 1 records and cross-references; never run benchmark commands."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    ids = {}
    count = 0
    for kind, directory, pattern in [("system", "systems", "*.json"), ("model", "models", "*.json"), ("dataset", "datasets", "*.json"), ("experiment", "configs/experiments", "*.yaml")]:
        schema = read(ROOT / "schemas" / f"{kind}.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        ids[kind] = {}
        for path in sorted((ROOT / directory).glob(pattern)):
            record = read(path)  # Experiment YAML intentionally uses JSON subset.
            errors = list(validator.iter_errors(record))
            if errors:
                raise SystemExit(f"{path.relative_to(ROOT)}: " + "; ".join(f"{list(e.path)}: {e.message}" for e in errors))
            key = record[kind + "_id"]
            if key in ids[kind] or path.stem != key:
                raise SystemExit(f"Duplicate ID or filename mismatch: {path}")
            ids[kind][key] = record
            count += 1
    scenarios = read(ROOT / "configs/scenarios/scenarios.json")
    scenario_ids = {s["scenario_id"] for s in scenarios}
    if len(scenario_ids) != len(scenarios):
        raise SystemExit("Duplicate scenario IDs")
    for key, record in ids["experiment"].items():
        for kind in ["system", "dataset"]:
            if record[kind + "_id"] not in ids[kind]:
                raise SystemExit(f"{key}: missing {kind} reference")
        if any(mid not in ids["model"] for mid in record["model_ids"]):
            raise SystemExit(f"{key}: missing model reference")
        if record["scenario_id"] not in scenario_ids:
            raise SystemExit(f"{key}: missing scenario reference")
    print(f"Validated {count} records, four schemas and cross-references to {len(scenario_ids)} scenarios.")

if __name__ == "__main__":
    main()
