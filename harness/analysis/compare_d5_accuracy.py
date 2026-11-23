"""Validate saved alignment evidence and render the D5 Blitz/SoCall comparison.

No basecalling or alignment is performed. Requires only the standard library;
--plot additionally requires matplotlib. Run from any directory.
"""
import argparse
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = {
    "BLITZ-010": "results/raw/brian-7800x3d/blitz/reference-accuracy/BLITZ-010",
    "SOCALL-001": "results/raw/ege-m2/socall/reference-accuracy/SOCALL-001",
    "SOCALL-002": "results/raw/ege-m2/socall/reference-accuracy/SOCALL-002",
}
REFERENCE = "b846951645ed1f5218da21539125c7e3110ec9c78f5956896aa2d0e554617958"
ALIGNER = "minimap2 via mappy 2.31, preset map-ont, primary alignment only"
IDENTITY = "M / (M + S + I + D) per primary alignment"


def read_evidence(folder):
    folder = Path(folder)
    summary = json.loads((folder / "accuracy.json").read_text())
    if summary["reference_sha256"] != REFERENCE or summary["aligner"] != ALIGNER or summary["identity_definition"] != IDENTITY:
        raise ValueError(f"Reference/scoring method mismatch: {folder}")
    rows = {}
    with (folder / "alignments.csv").open(newline="") as f:
        for raw in csv.DictReader(f):
            key = raw["read_id"]
            if not key or key in rows:
                raise ValueError(f"Empty/duplicate read ID: {folder}")
            if raw["mapped"] not in ("True", "False"):
                raise ValueError("Invalid mapped flag")
            row = {k: int(raw[k]) for k in ["read_length", "matches", "substitutions", "insertions", "deletions", "aligned_read_bases"]}
            row.update(mapped=raw["mapped"] == "True", identity=float(raw["identity"]))
            if any(row[k] < 0 for k in ["read_length", "matches", "substitutions", "insertions", "deletions", "aligned_read_bases"]):
                raise ValueError("Negative count")
            if not math.isfinite(row["identity"]) or not 0 <= row["identity"] <= 1 or row["aligned_read_bases"] > row["read_length"]:
                raise ValueError("Invalid identity/coverage")
            columns = sum(row[k] for k in ["matches", "substitutions", "insertions", "deletions"])
            if row["mapped"] and (not columns or not math.isclose(row["identity"], row["matches"] / columns, abs_tol=1e-12)):
                raise ValueError("Per-read identity does not match edit counts")
            if not row["mapped"] and (columns or row["aligned_read_bases"] or row["identity"]):
                raise ValueError("Unmapped read has alignment counts")
            rows[key] = row
    mapped = [r for r in rows.values() if r["mapped"]]
    columns = sum(r[k] for r in mapped for k in ["matches", "substitutions", "insertions", "deletions"])
    bases = sum(r["read_length"] for r in rows.values())
    totals = {
        "reads": len(rows), "mapped_reads": len(mapped), "mapped_fraction": len(mapped) / len(rows),
        "median_identity": statistics.median(r["identity"] for r in mapped),
        "mean_identity": statistics.fmean(r["identity"] for r in mapped),
        "pooled_identity": sum(r["matches"] for r in mapped) / columns,
        "substitution_rate": sum(r["substitutions"] for r in mapped) / columns,
        "insertion_rate": sum(r["insertions"] for r in mapped) / columns,
        "deletion_rate": sum(r["deletions"] for r in mapped) / columns,
        "total_bases": bases, "aligned_base_fraction": sum(r["aligned_read_bases"] for r in mapped) / bases,
    }
    for key, value in totals.items():
        if not math.isclose(summary[key], value, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError(f"Summary/CSV mismatch for {key}: {folder}")
    return summary, rows


def compare(records):
    blitz = records["BLITZ-010"][1]
    paired = {}
    for eid in ["SOCALL-001", "SOCALL-002"]:
        other = records[eid][1]
        if blitz.keys() != other.keys():
            raise ValueError(f"Read sets differ for {eid}; do not silently intersect")
        common = sorted(i for i in blitz if blitz[i]["mapped"] and other[i]["mapped"])
        deltas = [100 * (blitz[i]["identity"] - other[i]["identity"]) for i in common]
        paired[eid] = {
            "same_read_ids": True, "both_mapped": len(common),
            "blitz_only_mapped": sum(blitz[i]["mapped"] and not other[i]["mapped"] for i in blitz),
            "socall_only_mapped": sum(other[i]["mapped"] and not blitz[i]["mapped"] for i in blitz),
            "neither_mapped": sum(not other[i]["mapped"] and not blitz[i]["mapped"] for i in blitz),
            "blitz_higher": sum(d > 0 for d in deltas), "socall_higher": sum(d < 0 for d in deltas),
            "ties": sum(d == 0 for d in deltas),
            "median_identity_difference_pp": statistics.median(deltas),
            "mean_identity_difference_pp": statistics.fmean(deltas),
        }
    return paired


def render_plot(records, path):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "d5-blitz-socall-accuracy"
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
    for (eid, label, color) in [("BLITZ-010", "Blitz network 64, beam 5", "#116961"), ("SOCALL-001", "SoCall FP32, greedy", "#94633a"), ("SOCALL-002", "SoCall FP32, beam 5", "#495db6")]:
        vals = sorted(100 * r["identity"] for r in records[eid][1].values() if r["mapped"])
        ax.step(vals, [(i + 1) / len(vals) for i in range(len(vals))], where="post", label=label, color=color)
    ax.set(xlabel="Primary-alignment identity (%)", ylabel="Fraction of mapped reads at or below identity", xlim=(0, 100), ylim=(0, 1), title="D5: read identity distributions (mapped reads only)")
    ax.grid(alpha=.2)
    ax.legend(loc="upper left")
    fig.savefig(path, metadata={"Date": None})
    if path.suffix == ".svg":
        path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    records = {eid: read_evidence(ROOT / path) for eid, path in EVIDENCE.items()}
    if any(len(rows) != 4467 for _, rows in records.values()):
        raise ValueError("D5 comparison requires all 4467 reads")
    paired = compare(records)
    payload = {
        "dataset": "D5", "analysis_date": "2026-11-23", "reference_sha256": REFERENCE,
        "aligner": ALIGNER, "identity_definition": IDENTITY,
        "summaries": {eid: summary for eid, (summary, _) in records.items()}, "paired": paired,
        "artifacts": {eid: {name: hashlib.sha256((ROOT / folder / name).read_bytes()).hexdigest() for name in ["accuracy.json", "alignments.csv"]} for eid, folder in EVIDENCE.items()},
        "limitations": ["Saved alignment evidence checked; FASTQs not independently realigned.", "Identity and error rates exclude unmapped reads and unaligned sequence; report mapping and aligned-base fractions alongside them.", "One organism/dataset; pretrained-model training overlap and exact D5 pore subrevision unknown.", "Not a controlled speed/energy comparison, consensus accuracy, or clinical validation."],
    }
    out = ROOT / "results/summaries/d5-accuracy-comparison.json"
    content = json.dumps(payload, indent=2) + "\n"
    if args.check:
        if not out.exists() or out.read_text() != content:
            raise SystemExit("Stale D5 comparison; run compare_d5_accuracy.py")
    else:
        out.write_text(content)
    if args.plot:
        render_plot(records, ROOT / "website/content/assets/d5-accuracy-ecdf.svg")
    print(json.dumps({"rows_per_caller": 4467, "all_summary_fields_recomputed": True, "paired": paired}, indent=2))


if __name__ == "__main__":
    main()
