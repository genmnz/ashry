#!/usr/bin/env python3
"""Verify every DOI and PMID in the titer corpus against Europe PMC and Crossref.

One of the four literature sweeps reported that DOIs it had inferred rather
than resolved were wrong roughly half the time, and caught 28 of its own. The
other sweeps did not run that check, so no identifier in the corpus can be
trusted until it has been resolved against a registry. This script does that
for every row and writes a verdict per identifier.

For each row:
  * if a PMID is present, fetch the Europe PMC record for that PMID and take
    its authoritative DOI, title, journal and year;
  * if a DOI is present, resolve it against Crossref;
  * compare the two, and compare both against the row's `reference` string.

Verdicts
  ok             DOI resolves and agrees with the PMID record
  doi_corrected  DOI resolved to a different value from the PMID record
  doi_bad        DOI does not resolve anywhere
  no_identifier  neither DOI nor PMID present
  pmid_bad       PMID does not resolve

Output
  data/literature/identifier_verification.tsv
  data/literature/identifier_verification_report.md
"""
from __future__ import annotations

import csv
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
UA = {"User-Agent": "research-identifier-verifier/1.0"}

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


def epmc_by_pmid(pmid):
    q = urllib.parse.quote(f"EXT_ID:{pmid} AND SRC:MED")
    txt = _get(f"{EPMC}?query={q}&format=json&pageSize=1&resultType=core")
    if not txt:
        return None
    try:
        res = json.loads(txt)["resultList"]["result"]
    except (KeyError, json.JSONDecodeError):
        return None
    return res[0] if res else None


def crossref_by_doi(doi):
    txt = _get(CROSSREF + urllib.parse.quote(doi))
    if not txt:
        return None
    try:
        return json.loads(txt)["message"]
    except (KeyError, json.JSONDecodeError):
        return None


def clean_doi(d):
    d = (d or "").strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    return d if d.lower().startswith("10.") else ""


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def main():
    src = os.path.join(LIT, "titers_merged.tsv")
    with open(src, newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))

    out = []
    counts = {}
    seen = {}
    for i, r in enumerate(rows, 1):
        doi = clean_doi(r.get("doi"))
        pmid = (r.get("pmid") or "").strip()
        pmid = pmid if re.fullmatch(r"\d{6,9}", pmid) else ""
        key = (doi, pmid)
        if key in seen:
            rec = dict(seen[key])
            rec["record_id"] = r.get("record_id")
            out.append(rec)
            counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
            continue

        rec = {"record_id": r.get("record_id"),
               "protein": r.get("protein_canonical"),
               "doi_as_recorded": doi, "pmid_as_recorded": pmid,
               "doi_authoritative": "", "title_authoritative": "",
               "journal_authoritative": "", "year_authoritative": "",
               "verdict": "", "note": ""}

        epmc = epmc_by_pmid(pmid) if pmid else None
        if pmid and not epmc:
            rec["note"] = "PMID did not resolve in Europe PMC"
        if epmc:
            rec["doi_authoritative"] = clean_doi(epmc.get("doi"))
            rec["title_authoritative"] = epmc.get("title", "")[:180]
            rec["journal_authoritative"] = epmc.get("journalTitle", "")
            rec["year_authoritative"] = epmc.get("pubYear", "")

        cr = crossref_by_doi(doi) if doi else None
        if cr and not rec["title_authoritative"]:
            rec["title_authoritative"] = (cr.get("title") or [""])[0][:180]
            rec["journal_authoritative"] = (cr.get("container-title")
                                            or [""])[0]
            rec["year_authoritative"] = str(cr.get("issued", {})
                                            .get("date-parts",
                                                 [[""]])[0][0])

        if not doi and not pmid:
            rec["verdict"] = "no_identifier"
        elif pmid and not epmc:
            rec["verdict"] = "pmid_bad"
        elif doi and not cr:
            if rec["doi_authoritative"] and rec["doi_authoritative"] != doi:
                rec["verdict"] = "doi_corrected"
                rec["note"] = ("DOI as recorded does not resolve; Europe PMC "
                               "gives a different DOI for this PMID")
            else:
                rec["verdict"] = "doi_bad"
                rec["note"] = "DOI does not resolve in Crossref"
        elif (doi and rec["doi_authoritative"]
              and rec["doi_authoritative"].lower() != doi.lower()):
            rec["verdict"] = "doi_corrected"
            rec["note"] = (f"recorded {doi}, Europe PMC gives "
                           f"{rec['doi_authoritative']} for PMID {pmid}")
        else:
            rec["verdict"] = "ok"
            if not rec["doi_authoritative"]:
                rec["doi_authoritative"] = doi

        # does the recorded reference string agree with the real first author?
        ref = norm(r.get("reference"))
        auth = ""
        if epmc:
            auth = norm((epmc.get("authorString") or "").split(",")[0])
        elif cr and cr.get("author"):
            auth = norm(cr["author"][0].get("family", ""))
        if auth and ref and auth.split(" ")[0] not in ref:
            rec["note"] = ((rec["note"] + "; ") if rec["note"] else "") + \
                f"reference string does not name the registry first author ({auth})"

        seen[key] = rec
        out.append(rec)
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
        time.sleep(0.2)
        if i % 25 == 0:
            sys.stderr.write(f"  {i}/{len(rows)}\n")

    cols = ["record_id", "protein", "doi_as_recorded", "pmid_as_recorded",
            "doi_authoritative", "verdict", "title_authoritative",
            "journal_authoritative", "year_authoritative", "note"]
    with open(os.path.join(LIT, "identifier_verification.tsv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        for r in out:
            w.writerow(r)

    lines = ["# Identifier verification", "",
             f"Rows checked: {len(out)}",
             f"Distinct identifier pairs resolved: {len(seen)}", "",
             "## Verdicts", ""]
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        lines.append(f"- **{k}**: {v}")
    bad = [r for r in out if r["verdict"] in ("doi_corrected", "doi_bad",
                                              "pmid_bad")]
    lines += ["", f"## Problems ({len(bad)} rows)", ""]
    for r in bad[:200]:
        lines.append(f"- `{r['record_id']}` {r['protein']}: "
                     f"recorded `{r['doi_as_recorded'] or '-'}` / PMID "
                     f"`{r['pmid_as_recorded'] or '-'}` -> "
                     f"**{r['verdict']}**. {r['note']}")
    flagged = [r for r in out if "reference string" in (r["note"] or "")
               and r["verdict"] == "ok"]
    lines += ["", f"## Attribution mismatches ({len(flagged)})", ""]
    for r in flagged[:100]:
        lines.append(f"- `{r['record_id']}`: {r['note']}")
    with open(os.path.join(LIT, "identifier_verification_report.md"),
              "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:60]))


if __name__ == "__main__":
    main()
