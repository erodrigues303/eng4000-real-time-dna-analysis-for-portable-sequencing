"""Prevent silent evidence drift and unfair comparisons of different read sets."""
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness/analysis"))
from compare_d5_accuracy import EVIDENCE, compare, read_evidence


@pytest.mark.parametrize("field,value", [("reference_sha256", "wrong"), ("median_identity", 1.0)])
def test_mismatched_reference_or_summary_is_rejected(tmp_path, field, value):
    source = ROOT / EVIDENCE["BLITZ-010"]
    for name in ["accuracy.json", "alignments.csv"]:
        shutil.copyfile(source / name, tmp_path / name)
    path = tmp_path / "accuracy.json"
    summary = json.loads(path.read_text())
    summary[field] = value
    path.write_text(json.dumps(summary))
    with pytest.raises(ValueError):
        read_evidence(tmp_path)


def test_comparison_rejects_different_read_sets():
    record = {eid: read_evidence(ROOT / path) for eid, path in EVIDENCE.items()}
    record["SOCALL-002"][1].pop(next(iter(record["SOCALL-002"][1])))
    with pytest.raises(ValueError, match="Read sets differ"):
        compare(record)
