#!/usr/bin/env python3
"""Verify every bibliography entry against the DOI registries.

The 232-entry bibliography was assembled from literature sweeps, so each
entry's DOI, first author, year, title and venue are as recorded by whoever
read the paper, not as the registry states them. The titer corpus has already
been through this check (see reference_corrections.md, which rebuilt 62 wrong
first authors); the bibliography has not, which is why every DOI in the
rendered reference list still carries an [unverified] marker.

Procedure, per entry:

  1. If a DOI is recorded, resolve it against the Crossref REST API and
     re-derive first author, year, title and container title from the
     registry, keeping the recorded value beside it.
  2. A Crossref 404 is NOT taken as proof the DOI is wrong. Several prefixes
     are registered with other agencies (DataCite, mEDRA, JaLC, KISTI), and
     four rows in the titer corpus that Crossref could not find resolved
     normally at doi.org. Every Crossref miss is therefore re-tried against
     doi.org, and only a DOI that fails at both is called bad_doi.
  3. If no DOI is recorded, the entry is a software, industry or regulatory
     source, or a paper whose identifier was never captured. These are
     reported as no_identifier. For the scholarly types a Crossref title
     query is attempted and a hit is recorded as a *suggestion* only, and
     only when the normalised titles agree closely, so that a human can
     accept it rather than having a guessed DOI silently inserted.

Nothing is deleted. Verdicts:

  ok                        DOI resolved in Crossref
  resolves_outside_crossref DOI not in Crossref but live at doi.org
  bad_doi                   DOI resolved nowhere
  no_identifier             no DOI recorded

Output
  data/literature/bibliography_verified.tsv
  data/literature/bibliography_corrections.md
  data/literature/bibliography_repaired.csv   (same columns as the input)
"""
from __future__ import annotations

import csv
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LIT = os.path.join(ROOT, "data", "literature")
SRC = os.path.join(LIT, "bibliography_thread_f20slk.csv")

# Crossref asks automated clients to identify the tool; no personal details.
UA = {"User-Agent": "bibliography-verifier/1.0 (automated reference check)"}
PLACEHOLDER = re.compile(r"^\s*(not retrieved|\[author list not retrieved\]|n/?a|)\s*$", re.I)


def get(url, tries=4, timeout=60, accept_404=True):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                return fh.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400) and accept_404:
                return None
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (i + 1))
    sys.stderr.write(f"  give up {url}: {last}\n")
    return None


def doi_org_resolves(doi):
    """True if doi.org has a handle for this DOI, independent of Crossref."""
    url = "https://doi.org/api/handles/" + urllib.parse.quote(doi, safe="/")
    txt = get(url)
    if not txt:
        return False
    try:
        return json.loads(txt).get("responseCode") == 1
    except ValueError:
        return False


def crossref_work(doi):
    txt = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))
    if not txt:
        return None
    try:
        return json.loads(txt)["message"]
    except (ValueError, KeyError):
        return None


def norm_title(s):
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split()


def title_sim(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm_title(a)),
                                   " ".join(norm_title(b))).ratio()


def crossref_by_title(title):
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 5})
    txt = get("https://api.crossref.org/works?" + q)
    if not txt:
        return None
    try:
        items = json.loads(txt)["message"]["items"]
    except (ValueError, KeyError):
        return None
    best, best_s = None, 0.0
    for it in items:
        t = (it.get("title") or [""])[0]
        s = title_sim(title, t)
        if s > best_s:
            best, best_s = it, s
    if best is not None and best_s >= 0.92:
        return best, best_s
    return None


def first_author(msg):
    for a in msg.get("author") or []:
        fam = a.get("family")
        if fam:
            return fam
        if a.get("name"):
            return a["name"]
    return ""


def authors_string(msg):
    auth = msg.get("author") or []
    if not auth:
        return ""
    fam = first_author(msg)
    if not fam:
        return ""
    return f"{fam} et al." if len(auth) > 1 else fam


def reg_year(msg):
    for k in ("published-print", "published-online", "published", "issued",
              "created"):
        parts = (msg.get(k) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return ""


def reg_venue(msg):
    ct = msg.get("container-title") or []
    if ct:
        return ct[0]
    return msg.get("institution", [{}])[0].get("name", "") if msg.get("institution") else ""


def main():
    with open(SRC, newline="") as fh:
        rdr = csv.DictReader(fh)
        incols = list(rdr.fieldnames)
        rows = list(rdr)

    out, changes, flagged, filled, suggestions = [], [], [], [], []
    for i, r in enumerate(rows, 1):
        doi = (r.get("doi") or "").strip().rstrip(".")
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
        rec = {
            "entry": i,
            "cluster": r.get("cluster"),
            "type": r.get("type"),
            "doi_as_recorded": r.get("doi") or "",
            "doi_normalised": doi,
            "authors_as_recorded": r.get("authors") or "",
            "year_as_recorded": r.get("year") or "",
            "title_as_recorded": r.get("title") or "",
            "venue_as_recorded": r.get("venue") or "",
        }
        msg = crossref_work(doi) if doi else None
        if msg is not None:
            rec["verdict"] = "ok"
        elif doi:
            rec["verdict"] = ("resolves_outside_crossref" if doi_org_resolves(doi)
                              else "bad_doi")
        else:
            rec["verdict"] = "no_identifier"

        if msg is not None:
            ra, ry = authors_string(msg), reg_year(msg)
            rt = (msg.get("title") or [""])[0]
            rv = reg_venue(msg)
            rec.update({"authors_registry": ra, "year_registry": ry,
                        "title_registry": rt, "venue_registry": rv,
                        "registry_type": msg.get("type") or "",
                        "title_similarity": round(title_sim(r.get("title"), rt), 3)})
            was_placeholder = bool(PLACEHOLDER.match(rec["authors_as_recorded"]))
            if ra and was_placeholder:
                filled.append((i, doi, ra, ry, rt, rv))
            elif ra and ra.split(",")[0].split()[0].lower() not in \
                    rec["authors_as_recorded"].lower():
                changes.append(("author", i, doi, rec["authors_as_recorded"], ra))
            if ry and rec["year_as_recorded"] and ry != rec["year_as_recorded"]:
                changes.append(("year", i, doi, rec["year_as_recorded"], ry))
            if rv and rec["venue_as_recorded"] and title_sim(rv, rec["venue_as_recorded"]) < 0.6:
                changes.append(("venue", i, doi, rec["venue_as_recorded"], rv))
            if rec["title_similarity"] < 0.85:
                changes.append(("title", i, doi, rec["title_as_recorded"], rt))
            # write the repaired row
            if ra and (was_placeholder or
                       ra.split(",")[0].split()[0].lower() not in
                       rec["authors_as_recorded"].lower()):
                r["authors"] = ra
            if ry:
                r["year"] = ry
            if rt and rec["title_similarity"] < 0.85:
                r["title"] = rt
            if rv and rec["venue_as_recorded"] and title_sim(rv, rec["venue_as_recorded"]) < 0.6:
                r["venue"] = rv
        else:
            if rec["verdict"] in ("bad_doi", "resolves_outside_crossref"):
                flagged.append((i, doi, rec["verdict"], rec["title_as_recorded"]))
            if rec["verdict"] == "no_identifier" and \
                    r.get("type") in ("peer-reviewed", "review", "preprint"):
                hit = crossref_by_title(r.get("title") or "")
                if hit:
                    m, s = hit
                    cand = m.get("DOI", "")
                    rec["doi_suggested"] = cand
                    rec["doi_suggested_similarity"] = round(s, 3)
                    rec["authors_registry"] = authors_string(m)
                    rec["year_registry"] = reg_year(m)
                    rec["venue_registry"] = reg_venue(m)
                    suggestions.append((i, cand, round(s, 3),
                                        rec["title_as_recorded"],
                                        authors_string(m), reg_year(m)))
        out.append(rec)
        r["_verdict"] = rec["verdict"]
        time.sleep(0.12)

    cols = ["entry", "cluster", "type", "verdict", "doi_as_recorded",
            "doi_normalised", "authors_as_recorded", "authors_registry",
            "year_as_recorded", "year_registry", "title_as_recorded",
            "title_registry", "title_similarity", "venue_as_recorded",
            "venue_registry", "registry_type", "doi_suggested",
            "doi_suggested_similarity"]
    with open(os.path.join(LIT, "bibliography_verified.tsv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for rec in out:
            w.writerow(rec)

    with open(os.path.join(LIT, "bibliography_repaired.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=incols, extrasaction="ignore",
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in incols})

    counts = {}
    for rec in out:
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1

    L = ["# Bibliography verification", "",
         "Every entry in `bibliography_thread_f20slk.csv` (byte-identical to "
         "`bibliography.csv` on the paper branch) was checked against the DOI "
         "registries. First author, year, title and venue were re-derived from "
         "Crossref; the recorded value is preserved beside the registry value "
         "in `bibliography_verified.tsv`, so every change below is checkable "
         "against its row.", "",
         "A Crossref 404 is not treated as proof that a DOI is wrong. Some "
         "prefixes are registered with other agencies, and four unresolvable "
         "rows in the titer corpus turned out to be live at doi.org. Every "
         "Crossref miss was therefore re-tried against the doi.org handle API, "
         "and only a DOI that failed at both is called `bad_doi`. Nothing was "
         "deleted.", "",
         f"Entries: {len(out)}", "", "## Verdicts", ""]
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        L.append(f"- **{k}**: {v}")

    L += ["", f"## Author lists filled from the registry ({len(filled)})", "",
          "These entries recorded no author list at all.", ""]
    if filled:
        L.append("| entry | DOI | first author | year | venue |")
        L.append("|---|---|---|---|---|")
        for i, d, a, y, t, v in filled:
            L.append(f"| {i} | `{d}` | {a} | {y} | {v} |")
    else:
        L.append("- none")

    bykind = {}
    for kind, i, d, old, new in changes:
        bykind.setdefault(kind, []).append((i, d, old, new))
    for kind in ("author", "year", "venue", "title"):
        items = bykind.get(kind, [])
        L += ["", f"## {kind.capitalize()} corrections ({len(items)})", ""]
        if not items:
            L.append("- none")
            continue
        for i, d, old, new in items:
            L.append(f"- entry {i} (`{d}`): \"{old}\" -> **\"{new}\"**")

    L += ["", f"## DOIs flagged, not deleted ({len(flagged)})", ""]
    if flagged:
        L.append("| entry | DOI | verdict | title as recorded |")
        L.append("|---|---|---|---|")
        for i, d, v, t in flagged:
            L.append(f"| {i} | `{d}` | {v} | {t[:80]} |")
    else:
        L.append("- none")

    L += ["", f"## DOIs suggested for entries that recorded none ({len(suggestions)})",
          "", "Found by a Crossref bibliographic-title query and accepted only "
          "where the normalised titles agree at 0.92 or better. These are "
          "suggestions, not edits: they are not written into the repaired "
          "file, because a title match is weaker evidence than a DOI.", ""]
    if suggestions:
        L.append("| entry | suggested DOI | title similarity | first author | year | title as recorded |")
        L.append("|---|---|---|---|---|---|")
        for i, d, s, t, a, y in suggestions:
            L.append(f"| {i} | `{d}` | {s} | {a} | {y} | {t[:70]} |")
    else:
        L.append("- none")

    L += ["", "## Files", "",
          "- `bibliography_verified.tsv` - one row per entry, recorded and "
          "registry values side by side, with the verdict.",
          "- `bibliography_repaired.csv` - the input file with authors, years, "
          "venues and titles replaced by the registry values where they "
          "differed. Same columns as the input, so it can be dropped in place "
          "of `bibliography.csv`. Suggested DOIs are deliberately NOT written "
          "here.", ""]

    with open(os.path.join(LIT, "bibliography_corrections.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
