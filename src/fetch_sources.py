#!/usr/bin/env python3
"""Pull every source the thesis cites into the repository, where that is allowed.

A bibliography is a set of promises that someone else's server will still be
there. This turns as much of it as licensing permits into files in the
repository, and records, for every entry, either where the local copy is or why
there is not one.

The rules, which are about redistribution rather than access:

* **OpenAlex decides.** For each DOI, OpenAlex gives the open-access status,
  the best open location, the licence on it, and the PMC identifier when there
  is one. A Creative Commons or public-domain licence is taken as permission to
  store a copy; anything else is not, however freely the paper can be read.
  OpenAlex answers in well under a second, where a Europe PMC title search
  takes twenty, which is the difference between this script taking minutes and
  taking hours.
* **The copy comes from Europe PMC where it can.** A PMC full text is XML:
  searchable, diffable and a tenth of the size of the PDF. Where OpenAlex names
  a PMCID and a CC licence, the XML is fetched; otherwise the publisher's open
  PDF is.
* **US government documents.** FDA letters, GRAS notices and Federal Register
  items are works of the US government and are not under copyright. Their PDFs
  are fetched directly.
* **Everything else gets metadata, a link, and an archive snapshot.** A
  paywalled paper, a trade-press article or a company page may be read at its
  source but not redistributed here, and a company page is also the kind of
  link that quietly disappears. For each of those the manifest records the
  Internet Archive snapshot alongside the live URL, so the citation survives
  the page being taken down.
* **Everything else gets metadata and a link.** A paywalled paper, a trade
  press article or a company page may be read at its source but not
  redistributed here. The manifest carries the DOI, the URL, the resolved
  metadata and the reason no copy is stored, which is what makes the citation
  checkable without infringing anything.

Nothing here sends identifying information to any service: requests carry a
generic client name and no contact address.

Outputs:
    data/sources/fulltext/*.xml      open-access full texts
    data/sources/documents/*.pdf     public-domain government documents
    data/sources/metadata/*.json     resolved metadata for every entry
    data/sources/manifest.tsv        one row per entry, machine readable
    data/sources/MANIFEST.md         the same, readable, with the counts

Usage:
    python3 src/fetch_sources.py            # resume; skips what is present
    python3 src/fetch_sources.py --refresh  # re-fetch metadata
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "data" / "literature" / "bibliography.csv"
OUT = ROOT / "data" / "sources"
FULLTEXT = OUT / "fulltext"
DOCUMENTS = OUT / "documents"
METADATA = OUT / "metadata"

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
OPENALEX = "https://api.openalex.org/works/doi:"
UA = "ashry-thesis-archive/1.0 (research archive; no contact stored)"
PAUSE = 0.34                      # about three requests a second

# Domains whose documents are works of the US federal government, and so are
# not under copyright and may be stored here.
PUBLIC_DOMAIN = (
    "fda.gov", "govinfo.gov", "federalregister.gov", "ncbi.nlm.nih.gov",
    "nih.gov", "usda.gov", "hfpappexternal.fda.gov",
)


def get(url: str, timeout: int = 45) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as fh:
            return fh.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    finally:
        time.sleep(PAUSE)


def key_for(row: dict, n: int) -> str:
    author = (row.get("authors") or "anon").split(",")[0].split(" ")[0]
    author = re.sub(r"[^A-Za-z]", "", author).lower() or "anon"
    year = re.sub(r"[^0-9]", "", str(row.get("year") or ""))[:4] or "nd"
    return f"{n:03d}_{author}_{year}"


def europepmc(doi: str, title: str) -> dict | None:
    """Resolve an entry at Europe PMC, by DOI if there is one, else by title."""
    if doi:
        q = f'DOI:"{doi}"'
    elif title:
        q = 'TITLE:"%s"' % title.replace('"', "")
    else:
        return None
    url = (f"{EPMC}/search?query={urllib.parse.quote(q)}"
           "&resultType=core&format=json&pageSize=1")
    raw = get(url)
    hits = []
    if raw:
        try:
            hits = json.loads(raw)["resultList"]["result"]
        except (ValueError, KeyError):
            hits = []
    if not hits and doi and title:
        # a DOI that Europe PMC has not indexed is still often there under its
        # title, and an entry resolved that way is what carries the PMCID
        return europepmc("", title)
    return hits[0] if hits else None


def openalex(doi: str) -> dict | None:
    """The best open-access location for a DOI, and the licence on it."""
    if not doi:
        return None
    raw = get(OPENALEX + urllib.parse.quote(doi))
    if not raw:
        return None
    try:
        work = json.loads(raw)
    except ValueError:
        return None
    best = work.get("best_oa_location") or {}
    ids = work.get("ids") or {}
    pmcid = (ids.get("pmcid") or "").rsplit("/", 1)[-1]
    return {
        "pmcid": pmcid,
        "pmid": (ids.get("pmid") or "").rsplit("/", 1)[-1],
        "oa_status": (work.get("open_access") or {}).get("oa_status"),
        "license": best.get("license"),
        "pdf_url": best.get("pdf_url"),
        "landing_page_url": best.get("landing_page_url"),
        "version": best.get("version"),
        "host": (best.get("source") or {}).get("display_name"),
    }


def cc_licensed(loc: dict | None) -> bool:
    """A Creative Commons or public-domain licence, which permits a copy here."""
    lic = ((loc or {}).get("license") or "").lower()
    return lic.startswith(("cc", "pd", "public"))


def redistributable(rec: dict) -> tuple[bool, str]:
    """Whether Europe PMC says this full text may be stored, and the reason."""
    if not rec:
        return False, "no Europe PMC record"
    if (rec.get("isOpenAccess") or "N").upper() != "Y":
        return False, "not open access"
    if not rec.get("pmcid"):
        return False, "open access but no PMC full text"
    licence = (rec.get("license") or "").lower()
    if licence and not licence.startswith(("cc", "pd", "publ")):
        return False, f"licence {licence} does not permit redistribution"
    return True, licence or "open access, licence unstated"


WAYBACK = "https://archive.org/wayback/available?url="


def wayback(url: str) -> str:
    """The Internet Archive's newest snapshot of a URL, if it has one."""
    if not url:
        return ""
    raw = get(WAYBACK + urllib.parse.quote(url, safe=""))
    if not raw:
        return ""
    try:
        snap = json.loads(raw)["archived_snapshots"].get("closest") or {}
    except (ValueError, KeyError):
        return ""
    return snap.get("url", "") if snap.get("available") else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    for d in (FULLTEXT, DOCUMENTS, METADATA):
        d.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(BIB.open()))
    if args.limit:
        rows = rows[: args.limit]

    manifest = []
    counts = {"fulltext": 0, "document": 0, "metadata": 0, "unresolved": 0}

    for n, row in enumerate(rows, 1):
        key = key_for(row, n)
        doi = (row.get("doi") or "").strip()
        url = (row.get("url") or "").strip()
        title = (row.get("title") or "").strip()
        meta_path = METADATA / f"{key}.json"

        if meta_path.exists() and not args.refresh:
            record = json.loads(meta_path.read_text())
        else:
            oa = openalex(doi)
            record = {
                "key": key, "cluster": row.get("cluster"),
                "authors": row.get("authors"),
                "year": str(row.get("year") or "").replace(".0", ""),
                "title": title, "venue": row.get("venue"),
                "type": row.get("type"), "doi": doi, "url": url,
                "openalex": oa,
            }
            meta_path.write_text(json.dumps(record, indent=2) + "\n")

        oa = record.get("openalex")
        stored, reason, why = "", "", ""

        ft = FULLTEXT / f"{key}.xml"
        if cc_licensed(oa) and oa.get("pmcid") and not ft.exists():
            body = get(f"{EPMC}/{oa['pmcid']}/fullTextXML")
            if body and b"<article" in body[:4000]:
                ft.write_bytes(body)
        if ft.exists():
            stored = str(ft.relative_to(ROOT))
            reason = f"open access in PMC ({oa.get('license')})"
            counts["fulltext"] += 1

        pdf_oa = FULLTEXT / f"{key}.pdf"
        if not stored and cc_licensed(oa) and oa.get("pdf_url"):
            if not pdf_oa.exists():
                body = get(oa["pdf_url"])
                if body and body[:5] == b"%PDF-":
                    pdf_oa.write_bytes(body)
            if pdf_oa.exists():
                stored = str(pdf_oa.relative_to(ROOT))
                reason = f"open access at publisher ({oa['license']})"
                counts["fulltext"] += 1
            else:
                why = f"open access ({oa['license']}) but the PDF was not served"
        elif not stored and oa and oa.get("pdf_url") and not cc_licensed(oa):
            why = (f"readable at the publisher but licensed "
                   f"{oa.get('license') or 'all rights reserved'}; link only")

        if not stored and url and any(d in url for d in PUBLIC_DOMAIN):
            pdf = DOCUMENTS / f"{key}.pdf"
            if not pdf.exists():
                body = get(url)
                if body and body[:5] == b"%PDF-":
                    pdf.write_bytes(body)
            if pdf.exists():
                stored = str(pdf.relative_to(ROOT))
                reason = "work of the US government, not under copyright"
                counts["document"] += 1

        if not stored:
            if not reason and oa and not oa.get("pdf_url"):
                why = (f"no open version (OpenAlex: "
                       f"{oa.get('oa_status') or 'unknown'}); link only")
            if not reason:
                reason = why if oa else (
                    "not indexed at OpenAlex; metadata and link only")
            counts["metadata" if oa else "unresolved"] += 1

        archived = record.get("wayback")
        if archived is None and not stored and url:
            archived = wayback(url)
            record["wayback"] = archived
            meta_path.write_text(json.dumps(record, indent=2) + "\n")

        manifest.append({
            "key": key,
            "cluster": row.get("cluster"),
            "authors": row.get("authors"),
            "year": str(row.get("year") or "").replace(".0", ""),
            "title": title,
            "venue": row.get("venue"),
            "doi": doi,
            "url": url,
            "pmcid": (oa or {}).get("pmcid") or "",
            "local_copy": stored,
            "archived": archived or "",
            "why": reason,
            "metadata": str(meta_path.relative_to(ROOT)),
        })
        if n % 20 == 0:
            print(f"  {n}/{len(rows)}", file=sys.stderr)

    fields = list(manifest[0].keys())
    with (OUT / "manifest.tsv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(manifest)

    lines = [
        "# Source manifest", "",
        f"Every one of the {len(manifest)} bibliography entries, with the local "
        "copy where one may be stored and the reason where one may not.",
        "Generated by `src/fetch_sources.py`.", "",
        f"* Open-access full texts stored: **{counts['fulltext']}**",
        f"* Public-domain government documents stored: **{counts['document']}**",
        f"* Metadata and link only: **{counts['metadata'] + counts['unresolved']}**",
        "",
        "A missing copy is a licensing limit, not a gap in the record: the DOI, "
        "the URL and the resolved metadata are here for every entry, in "
        "`data/sources/metadata/`.", "",
        "| # | Entry | Identifier | Local copy | Why |",
        "|---|---|---|---|---|",
    ]
    for row in manifest:
        ident = row["doi"] or row["url"] or "—"
        if not row["local_copy"] and row["archived"]:
            row = dict(row, why=row["why"] + f"; [archived copy]({row['archived']})")
        if len(ident) > 60:
            ident = ident[:57] + "…"
        who = (row["authors"] or "").split(",")[0]
        lines.append(
            f"| {row['key'].split('_')[0]} | {who} {row['year'] or ''} — "
            f"{row['title'][:70]} | `{ident}` | "
            f"{('`' + row['local_copy'] + '`') if row['local_copy'] else '—'} "
            f"| {row['why']} |")
    (OUT / "MANIFEST.md").write_text("\n".join(lines) + "\n")

    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
