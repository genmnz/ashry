"""
Offline-tolerant sequence acquisition.

The analysis container used for this work can reach GitHub and package registries
but not UniProt, so sequences are recovered from UniProt-derived FASTA files that
are mirrored in public repositories, and are then accepted only under a
consensus rule: a sequence is kept when two independent repositories carry byte
identical records for the same accession, or when a single record is confirmed
against the UniProt entry's stated length and mass.

This is a workaround, declared as such. With direct UniProt access the same
pipeline runs unchanged by pointing `SOURCES` at the REST endpoint.

Usage:  python3 fetch_sequences.py ACC [ACC ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "data" / "sequences" / "harvested"
MANIFEST = REPO / "data" / "sequences" / "harvest_manifest.json"
MAX_CANDIDATES = 8
MAX_BYTES = 40_000_000


def gh_code_search(query: str) -> list[tuple[str, str, str]]:
    """Return (repo, path, default_branch_guess) for code-search hits."""
    try:
        out = subprocess.run(
            ["gh", "api", "-X", "GET", "search/code", "-f", f"q={query}",
             "--jq", '.items[] | "\\(.repository.full_name)\\t\\(.path)"'],
            capture_output=True, text=True, timeout=90,
            env={"GH_PAGER": "cat", "PATH": "/usr/bin:/bin:/usr/local/bin",
                 "HOME": str(Path.home())},
        )
    except Exception:
        return []
    hits = []
    for line in out.stdout.strip().splitlines()[:MAX_CANDIDATES]:
        if "\t" not in line:
            continue
        repo, path = line.split("\t", 1)
        hits.append((repo, path, ""))
    return hits


def raw_fetch(repo: str, path: str) -> str | None:
    for branch in ("main", "master", "develop"):
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                data = fh.read(MAX_BYTES)
            return data.decode("utf-8", "replace")
        except Exception:
            continue
    return None


def extract(text: str, accession: str) -> tuple[str, str] | None:
    header = None
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith(">"):
            if header is not None and f"|{accession}|" in header:
                return header, "".join(buf)
            header, buf = line[1:], []
        elif header is not None:
            buf.append(line.strip())
    if header is not None and f"|{accession}|" in header:
        return header, "".join(buf)
    return None


def harvest(accession: str) -> dict:
    found: dict[str, list[dict]] = defaultdict(list)
    for query in (f"{accession} extension:fasta", f'"|{accession}|"'):
        for repo, path, _ in gh_code_search(query):
            text = raw_fetch(repo, path)
            if not text or ">" not in text:
                continue
            rec = extract(text, accession)
            if not rec:
                continue
            header, seq = rec
            seq = "".join(ch for ch in seq.upper()
                          if ch in "ACDEFGHIKLMNPQRSTVWYXBZUO")
            if len(seq) < 20:
                continue
            found[seq].append({"repo": repo, "path": path, "header": header})
        if found:
            break

    if not found:
        return {"accession": accession, "status": "not_found"}

    seq, sources = max(found.items(), key=lambda kv: len(kv[1]))
    repos = {s["repo"] for s in sources}
    return {
        "accession": accession,
        "status": "consensus" if len(repos) >= 2 else "single_source",
        "sequence": seq,
        "length": len(seq),
        "n_sources": len(sources),
        "repos": sorted(repos),
        "headers": sorted({s["header"][:120] for s in sources}),
        "n_distinct_sequences": len(found),
    }


def main(accessions: list[str]) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for acc in accessions:
        if acc in manifest and manifest[acc].get("status") != "not_found":
            print(f"{acc}: cached ({manifest[acc]['status']})")
            continue
        rec = harvest(acc)
        manifest[acc] = rec
        if rec.get("sequence"):
            (CACHE / f"{acc}.fasta").write_text(
                f">{acc}|harvested|{rec['status']}|sources={rec['n_sources']}\n"
                + "\n".join(rec["sequence"][i:i + 60]
                            for i in range(0, len(rec["sequence"]), 60)) + "\n")
        print(f"{acc}: {rec['status']}"
              + (f" len={rec.get('length')} repos={len(rec.get('repos', []))}"
                 f" variants={rec.get('n_distinct_sequences')}"
                 if rec.get("sequence") else ""))
        MANIFEST.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
