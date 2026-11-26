"""Every artifact an experiment record lists must exist in the repository with its recorded SHA-256."""

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECORDS = sorted((ROOT / "configs" / "experiments").glob("*.yaml"))
TX2 = "results/raw/jetson-tx2-jp466/socall/offline-throughput"
# Compressed on Matthew's machine while .gitignore still excluded *.gz, so never committed.
# strict xfail: once the files land, these start passing and the entries must be removed.
NOT_YET_COMMITTED = {
    f"{TX2}/SOCALL-003/tegrastats.log.gz",
    f"{TX2}/SOCALL-004/tegrastats_rep4.log.gz",
    f"{TX2}/SOCALL-005/tegrastats_cpu5.log.gz",
    f"{TX2}/SOCALL-005/power_cpu5.csv.gz",
}


def _repo_artifacts():
    for path in RECORDS:
        record = json.loads(path.read_text(encoding="utf-8"))
        for artifact in record["artifacts"]:
            location = artifact["location"]
            if location.startswith("results/raw/") and artifact.get("sha256"):
                marks = [pytest.mark.xfail(strict=True, reason="gzip artifact not committed yet")] \
                    if location in NOT_YET_COMMITTED else []
                yield pytest.param(record["experiment_id"], location, artifact["sha256"], id=location, marks=marks)


@pytest.mark.parametrize("experiment_id,location,sha256", list(_repo_artifacts()))
def test_artifact_matches_recorded_sha256(experiment_id, location, sha256):
    path = ROOT / location
    assert path.is_file(), f"{experiment_id} lists missing artifact {location}"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha256
