"""Read-level accuracy of a FASTQ against a pinned reference genome (minimap2 via mappy).

Tool-agnostic: works on output from any basecaller. Each read keeps its primary
alignment only; unmapped and empty reads stay in the denominator of
mapped_fraction so filtering cannot hide failures (docs/methodology.md).

Example:
    python harness/analysis/reference_accuracy.py reads.fastq reference.fasta --out-dir results/raw/.../SOCALL-001
"""

import argparse
import csv
import hashlib
import json
import statistics
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

import mappy

PRESET = "map-ont"
IDENTITY_DEFINITION = "M / (M + S + I + D) per primary alignment"
CIGAR_INSERTION = 1
CIGAR_DELETION = 2


@dataclass(frozen=True)
class AlignmentResult:
    read_id: str
    read_length: int
    mapped: bool
    identity: float = 0.0
    matches: int = 0
    substitutions: int = 0
    insertions: int = 0
    deletions: int = 0
    aligned_read_bases: int = 0


def read_fastq(path: Path) -> Iterator[tuple[str, str]]:
    with open(path) as f:
        while header := f.readline():
            seq = f.readline().strip()
            f.readline()
            f.readline()
            yield header[1:].split()[0], seq


def align_reads(reference: Path | str, reads: Iterable[tuple[str, str]]) -> list[AlignmentResult]:
    """identity uses minimap2's mlen (matches) over blen (alignment columns)."""
    aligner = mappy.Aligner(str(reference), preset=PRESET)
    if not aligner:
        raise RuntimeError(f"could not build minimap2 index for {reference}")
    results = []
    for read_id, seq in reads:
        hit = next((h for h in aligner.map(seq) if h.is_primary), None) if seq else None
        if hit is None:
            results.append(AlignmentResult(read_id, len(seq), mapped=False))
            continue
        insertions = sum(n for n, op in hit.cigar if op == CIGAR_INSERTION)
        deletions = sum(n for n, op in hit.cigar if op == CIGAR_DELETION)
        results.append(
            AlignmentResult(
                read_id=read_id,
                read_length=len(seq),
                mapped=True,
                identity=hit.mlen / hit.blen,
                matches=hit.mlen,
                substitutions=hit.NM - insertions - deletions,
                insertions=insertions,
                deletions=deletions,
                aligned_read_bases=hit.q_en - hit.q_st,
            )
        )
    return results


def summarize(results: list[AlignmentResult]) -> dict:
    mapped = [r for r in results if r.mapped]
    columns = sum(r.matches + r.substitutions + r.insertions + r.deletions for r in mapped)
    total_bases = sum(r.read_length for r in results)

    def rate(count: int) -> float | None:
        return count / columns if columns else None

    return {
        "reads": len(results),
        "mapped_reads": len(mapped),
        "mapped_fraction": len(mapped) / len(results) if results else 0.0,
        "median_identity": statistics.median(r.identity for r in mapped) if mapped else None,
        "mean_identity": statistics.fmean(r.identity for r in mapped) if mapped else None,
        "pooled_identity": rate(sum(r.matches for r in mapped)),
        "substitution_rate": rate(sum(r.substitutions for r in mapped)),
        "insertion_rate": rate(sum(r.insertions for r in mapped)),
        "deletion_rate": rate(sum(r.deletions for r in mapped)),
        "total_bases": total_bases,
        "aligned_base_fraction": sum(r.aligned_read_bases for r in mapped) / total_bases if total_bases else 0.0,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("fastq", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("--out-dir", type=Path, help="defaults to the FASTQ's folder")
    args = parser.parse_args()

    out_dir = args.out_dir or args.fastq.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    results = align_reads(args.reference, read_fastq(args.fastq))
    with open(out_dir / "alignments.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[field for field in AlignmentResult.__dataclass_fields__])
        writer.writeheader()
        writer.writerows(asdict(r) for r in results)
    summary = summarize(results) | {
        "identity_definition": IDENTITY_DEFINITION,
        "aligner": f"minimap2 via mappy {mappy.__version__}, preset {PRESET}, primary alignment only",
        "reference_name": args.reference.name,
        "reference_sha256": sha256(args.reference),
        "fastq_sha256": sha256(args.fastq),
    }
    (out_dir / "accuracy.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
