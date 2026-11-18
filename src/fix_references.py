#!/usr/bin/env python3
"""Rewrite every reference string in the corpus from registry metadata.

The verification pass found 55 rows whose DOI and PMID resolve correctly but
whose recorded first author is wrong - for example a row citing
"Rantasalo et al., Front Bioeng Biotechnol 2025" for a paper whose registered
first author is Mojzita D, and a row citing "Zhang et al., J Agric Food Chem
2025" for one whose first author is Hu C. The identifiers are right, so the
measurements are traceable, but the citation strings are not, and in a paper
they would produce wrong in-text citations throughout.

This script takes the authoritative first author, journal and year from Europe
PMC (via the row's PMID) or Crossref (via its DOI), rebuilds the reference
string, and keeps the original in `reference_as_recorded` so every change is
auditable. Rows with no resolvable identifier are left untouched and listed.

Output
  data/literature/titers_merged.tsv          rewritten in place
  data/literature/reference_corrections.md   every change, old -> new
"""
from __future__ import annotations

import csv
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
LIT = os.path.join(ROOT, "data", "literature")
UA = {"User-Agent": "research-reference-fixer/1.0"}
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works/"

_cache = {}


def _get(url, tries=4, timeout=60):
    if url in _cache:
        return _cache[url]
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                out = fh.read().decode("utf-8", "replace")
            _cache[url] = out
            return out
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                _cache[url] = None
                return None
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (i + 1))
    sys.stderr.write(f"  give up {url}: {last}\n")
    return None


def clean_doi(d):
    d = (d or "").strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    return d if d.lower().startswith("10.") else ""


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def meta_for(doi, pmid):
    """(first_author_family, journal, year, title) from a registry, or None."""
    if pmid and re.fullmatch(r"\d{6,9}", pmid):
        q = urllib.parse.quote(f"EXT_ID:{pmid} AND SRC:MED")
        txt = _get(f"{EPMC}?query={q}&format=json&pageSize=1&resultType=core")
        if txt:
            try:
                res = json.loads(txt)["resultList"]["result"]
            except (KeyError, json.JSONDecodeError):
                res = []
            if res:
                e = res[0]
                auth = (e.get("authorString") or "").split(",")[0].strip()
                fam = auth.split(" ")[0] if auth else ""
                jrnl = (e.get("journalInfo", {}).get("journal", {})
                        .get("title") or e.get("journalTitle") or "")
                return (fam, jrnl, str(e.get("pubYear") or ""),
                        strip_tags(e.get("title")))
    if doi:
        txt = _get(CROSSREF + urllib.parse.quote(doi))
        if txt:
            try:
                m = json.loads(txt)["message"]
            except (KeyError, json.JSONDecodeError):
                return None
            au = m.get("author") or []
            fam = au[0].get("family", "") if au else ""
            jrnl = (m.get("container-title") or [""])[0]
            yr = m.get("issued", {}).get("date-parts", [[""]])[0][0]
            return (fam, jrnl, str(yr or ""),
                    strip_tags((m.get("title") or [""])[0]))
    return None


def main():
    path = os.path.join(LIT, "titers_merged.tsv")
    with open(path, newline="") as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        cols = list(rdr.fieldnames)
        rows = list(rdr)
    if "reference_as_recorded" not in cols:
        cols.insert(cols.index("reference") + 1, "reference_as_recorded")
    if "source_title" not in cols:
        cols.insert(cols.index("reference_as_recorded") + 1, "source_title")

    changes, unresolved = [], []
    seen = {}
    for r in rows:
        doi, pmid = clean_doi(r.get("doi")), (r.get("pmid") or "").strip()
        key = (doi, pmid)
        if key not in seen:
            seen[key] = meta_for(doi, pmid)
            time.sleep(0.15)
        m = seen[key]
        old = (r.get("reference") or "").strip()
        r["reference_as_recorded"] = old
        if not m or not m[0]:
            unresolved.append((r.get("record_id"), old, doi or "-", pmid or "-"))
            r["source_title"] = m[3] if m else ""
            continue
        fam, jrnl, yr, title = m
        new = f"{fam} et al., {jrnl} {yr}".replace("  ", " ").strip()
        r["reference"] = new
        r["source_title"] = title
        if re.sub(r"[^a-z]", "", fam.lower()) not in re.sub(r"[^a-z]", "",
                                                            old.lower()):
            changes.append((r.get("record_id"), old, new, doi or pmid))

    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    lines = ["# Reference-string corrections", "",
             "Every reference string in the corpus was rebuilt from registry "
             "metadata: the first author, journal and year come from Europe "
             "PMC via the row's PMID, or from Crossref via its DOI. The "
             "original string is preserved in `reference_as_recorded` and the "
             "registry's title is recorded in `source_title`, so each change "
             "can be checked.", "",
             f"Rows: {len(rows)}. Distinct identifier pairs resolved: "
             f"{sum(1 for v in seen.values() if v and v[0])} of {len(seen)}.",
             "",
             f"## First-author corrections ({len(changes)})", ""]
    for rid, old, new, ident in changes:
        lines.append(f"- `{rid}` (`{ident}`): \"{old}\" -> **\"{new}\"**")
    lines += ["", f"## Left unchanged, no resolvable identifier "
                  f"({len(unresolved)})", ""]
    for rid, old, doi, pmid in unresolved:
        lines.append(f"- `{rid}`: \"{old}\" (doi `{doi}`, pmid `{pmid}`)")
    with open(os.path.join(LIT, "reference_corrections.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"corrected first author on {len(changes)} rows; "
          f"{len(unresolved)} rows had no resolvable identifier")
    for c in changes[:25]:
        print(f"  {c[0]:26s} {c[1][:44]:46s} -> {c[2][:50]}")


if __name__ == "__main__":
    main()
