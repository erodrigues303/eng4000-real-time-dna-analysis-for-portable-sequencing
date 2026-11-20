"""Check production HTML links, fragments, registry coverage and publication boundaries."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site-build"
BASE = "/eng4000-real-time-dna-analysis-for-portable-sequencing/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


def main():
    pages = {path.resolve(): Page(path) for path in SITE.rglob("*.html")}
    if not pages:
        raise SystemExit("No site built")
    errors = []
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            route = unquote(url.path)
            if route.startswith("/"):
                if not route.startswith(BASE):
                    errors.append(f"Root-relative link escapes project base: {link}")
                    continue
                target = SITE / route[len(BASE):]
            else:
                target = path.parent / route if route else path
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.is_relative_to(SITE.resolve()) or not target.exists():
                errors.append(f"{path.relative_to(SITE)}: missing {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(SITE)}: missing fragment {link}")
    records = json.loads((SITE / "assets/experiments.json").read_text(encoding="utf-8"))
    canonical_ids = {p.stem for p in (ROOT / "configs/experiments").glob("*.yaml")}
    if {r["id"] for r in records} != canonical_ids or len(records) != len(canonical_ids):
        errors.append("Registry IDs differ from canonical configurations")
    for eid in canonical_ids:
        if not (SITE / f"experiments/{eid}/index.html").exists():
            errors.append(f"Missing stable experiment page: {eid}")
    forbidden = {".pdf", ".pod5", ".fast5", ".bam", ".fastq", ".pt", ".onnx", ".pem", ".key"}
    for path in SITE.rglob("*"):
        if path.is_file() and (path.suffix in forbidden or any(x in path.parts for x in [".local-evidence", "private", "node_modules", ".git"])):
            errors.append(f"Forbidden publication artifact: {path}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} HTML pages, local links/fragments, {len(records)} registry records and publication boundaries.")


if __name__ == "__main__":
    main()
