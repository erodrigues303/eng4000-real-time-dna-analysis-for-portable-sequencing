"""Every artifact an experiment record lists must exist in the repository with its recorded SHA-256."""

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECORDS = sorted((ROOT / "configs" / "experiments").glob("*.yaml"))


def _repo_artifacts():
    for path in RECORDS:
        record = json.loads(path.read_text(encoding="utf-8"))
        for artifact in record["artifacts"]:
            location = artifact["location"]
            if location.startswith("results/raw/") and artifact.get("sha256"):
                yield pytest.param(record["experiment_id"], location, artifact["sha256"], id=location)


@pytest.mark.parametrize("experiment_id,location,sha256", list(_repo_artifacts()))
def test_artifact_matches_recorded_sha256(experiment_id, location, sha256):
    path = ROOT / location
    assert path.is_file(), f"{experiment_id} lists missing artifact {location}"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha256
