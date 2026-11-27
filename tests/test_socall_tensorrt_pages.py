"""The TensorRT TX2 records (SOCALL-017 to 021) must render their measured values."""

import json
import subprocess
import sys
from pathlib import Path
from statistics import mean

import pytest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results/raw/jetson-tx2-jp466/socall/offline-throughput"
IDS = ["SOCALL-017", "SOCALL-018", "SOCALL-019", "SOCALL-020", "SOCALL-021"]


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "-q", "-d", str(out)], cwd=ROOT, check=True)
    return out


def _page(site, eid):
    return (site / "experiments" / eid / "index.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("eid", IDS)
def test_record_page_shows_mean_pass_throughput(site, eid):
    rates = [p["input_samples"] / p["wall_time_s"]
             for f in sorted((RAW / eid).glob("run-stats_*.json"))
             for p in json.loads(f.read_text(encoding="utf-8"))["per_pass"]]
    assert rates
    assert f"{mean(rates):,.0f}" in _page(site, eid)


@pytest.mark.parametrize("eid", ["SOCALL-020", "SOCALL-021"])
def test_d5_pages_show_the_mac_scored_accuracy(site, eid):
    accuracy = json.loads((RAW / eid / "accuracy.json").read_text(encoding="utf-8"))
    page = _page(site, eid)
    assert f"{accuracy['median_identity']:.2%}" in page
    assert f"{accuracy['mapped_fraction']:.2%}" in page


def test_socall_overview_reports_the_tensorrt_study(site):
    page = (site / "socall" / "index.html").read_text(encoding="utf-8")
    assert "TensorRT engines" in page
    for eid in IDS:
        assert eid in page


def test_socall_overview_states_the_tie_aware_rule(site):
    # The page used to promise byte-identical FASTQs for every exact change, which a runtime switch can't meet.
    page = (site / "socall" / "index.html").read_text(encoding="utf-8")
    assert "near-ties" in page
    assert "Changes meant to be exact must reproduce the baseline FASTQ byte for byte" not in page


@pytest.mark.parametrize("eid,variant", [("SOCALL-017", None),
                                         ("SOCALL-018", "socall-v1-bnfold-trt-fp32"), ("SOCALL-019", "socall-v1-bnfold-trt-fp16"),
                                         ("SOCALL-020", "socall-v1-bnfold-trt-fp32"), ("SOCALL-021", "socall-v1-bnfold-trt-fp16")])
def test_model_row_names_the_engine_that_ran(site, eid, variant):
    row = _page(site, eid).split("<td>Model</td>", 1)[1].split("</tr>", 1)[0]
    if variant:
        assert variant in row
    else:
        assert "socall-v1-" not in row

