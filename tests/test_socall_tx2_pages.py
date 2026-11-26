"""The TX2 decode and D5 records must render their measured values on the built site."""

import json
import subprocess
import sys
from pathlib import Path
from statistics import mean

import pytest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results/raw/jetson-tx2-jp466/socall/offline-throughput"
NEW_IDS = ["SOCALL-006", "SOCALL-007", "SOCALL-008", "SOCALL-009", "SOCALL-010", "SOCALL-011"]


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "-q", "-d", str(out)],
                   cwd=ROOT, check=True)
    return out


def _page(site, eid):
    return (site / "experiments" / eid / "index.html").read_text(encoding="utf-8")


def _pass_rates(eid):
    rates = []
    for stats in sorted((RAW / eid).glob("run-stats_*.json")):
        data = json.loads(stats.read_text(encoding="utf-8"))
        rates += [p["input_samples"] / p["wall_time_s"] for p in data["per_pass"]]
    return rates


@pytest.mark.parametrize("eid", NEW_IDS)
def test_record_page_shows_mean_pass_throughput(site, eid):
    rates = _pass_rates(eid)
    assert rates, f"no run-stats evidence for {eid}"
    assert f"{mean(rates):,.0f}" in _page(site, eid)


def test_d5_tx2_page_shows_reference_accuracy(site):
    page = _page(site, "SOCALL-011")
    assert "79.39%" in page  # median mapped-read identity scored on the Mac
    assert "97.31%" in page  # mapped fraction


def test_socall_overview_no_longer_calls_the_model_int8(site):
    page = (site / "socall" / "index.html").read_text(encoding="utf-8")
    assert "int8/fixed-point basecaller implementation" not in page
    for eid in NEW_IDS:
        assert f"{eid}" in page


def _registry_status(site, eid):
    page = (site / "experiments" / "index.html").read_text(encoding="utf-8")
    row = page.split(f'<a href="{eid}/">{eid}</a>', 1)[1].split("</tr>", 1)[0]
    return row.rsplit("<td>", 1)[1]


def test_registry_reports_raw_artifact_completeness(site):
    assert "raw artifacts in repository" in _registry_status(site, "SOCALL-011")
    # SOCALL-004's tegrastats .gz arrived in 5fdf3aa; BLITZ-003 has no raw artifacts at all.
    assert "raw artifacts in repository" in _registry_status(site, "SOCALL-004")
    assert _registry_status(site, "BLITZ-003").endswith("; raw artifacts missing</td>")


def test_model_card_and_socall_page_describe_the_architecture(site):
    card = (site / "models" / "socall-private" / "index.html").read_text(encoding="utf-8")
    assert "446,893" in card or "446893" in card
    assert "stride 3" in card and "CTC" in card
    page = (site / "socall" / "index.html").read_text(encoding="utf-8")
    assert "446,893 parameters" in page
    assert "before making architecture claims" not in page
