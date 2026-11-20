import json
import random
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("mappy")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness" / "analysis"))
from reference_accuracy import align_reads, read_fastq, summarize  # noqa: E402

SCRIPT = ROOT / "harness" / "analysis" / "reference_accuracy.py"


@pytest.fixture
def reference(tmp_path):
    rng = random.Random(0)
    genome = "".join(rng.choice("ACGT") for _ in range(50_000))
    path = tmp_path / "ref.fasta"
    path.write_text(f">chr\n{genome}\n")
    return path, genome


def substitute_every(seq, every):
    """Swap every `every`-th base, so identity is 1 - 1/every."""
    swap = {"A": "C", "C": "G", "G": "T", "T": "A"}
    return "".join(swap[b] if i % every == every - 1 else b for i, b in enumerate(seq))


def write_fastq(path, reads):
    path.write_text("".join(f"@{rid} extra=1\n{seq}\n+\n{'I' * len(seq)}\n" for rid, seq in reads))


def test_exact_read_has_identity_one(reference):
    path, genome = reference
    (result,) = align_reads(path, [("r1", genome[1000:6000])])
    assert result.mapped and result.identity == pytest.approx(1.0)


def test_substitutions_lower_identity_by_expected_amount(reference):
    path, genome = reference
    (result,) = align_reads(path, [("r1", substitute_every(genome[1000:9000], 20))])
    assert result.identity == pytest.approx(0.95, abs=0.01)
    assert result.substitutions > 0


def test_reverse_strand_read_maps(reference):
    path, genome = reference
    rc = genome[2000:7000][::-1].translate(str.maketrans("ACGT", "TGCA"))
    (result,) = align_reads(path, [("r1", rc)])
    assert result.mapped and result.identity == pytest.approx(1.0)


def test_unmapped_and_empty_reads_stay_in_the_count(reference):
    path, _ = reference
    rng = random.Random(1)
    junk = "".join(rng.choice("ACGT") for _ in range(3000))
    summary = summarize(align_reads(path, [("junk", junk), ("empty", "")]))
    assert summary["reads"] == 2
    assert summary["mapped_reads"] == 0
    assert summary["median_identity"] is None


def test_fastq_reader_keeps_first_header_token(tmp_path):
    fq = tmp_path / "x.fastq"
    write_fastq(fq, [("a", "ACGT"), ("b", "")])
    assert list(read_fastq(fq)) == [("a", "ACGT"), ("b", "")]


def test_cli_writes_summary_and_per_read_csv(reference, tmp_path):
    path, genome = reference
    fq = tmp_path / "reads.fastq"
    write_fastq(fq, [("good", genome[100:5100]), ("noisy", substitute_every(genome[9000:15000], 20))])
    out = tmp_path / "out"
    subprocess.run([sys.executable, str(SCRIPT), str(fq), str(path), "--out-dir", str(out)], check=True)
    summary = json.loads((out / "accuracy.json").read_text())
    assert summary["reads"] == summary["mapped_reads"] == 2
    assert summary["identity_definition"] == "M / (M + S + I + D) per primary alignment"
    assert len((out / "alignments.csv").read_text().splitlines()) == 3
