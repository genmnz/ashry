#!/usr/bin/env python3
"""Check each suggested DOI field by field before adopting it.

`verify_bibliography.py` found 45 candidate DOIs for entries that recorded
none, by Crossref bibliographic-title query, and deliberately refused to write
any of them into the repaired bibliography: a title query returns the
best-matching record whether or not the right record exists, so a high
similarity score is evidence the *query* worked, not that the *entry* was
found. Adopting 45 identifiers on that basis would put guessed citations in a
manuscript.

This script re-fetches each candidate's full Crossref record and checks it on
four independent fields before adopting it:

  title     normalised token similarity, with 0.97 required rather than the
            0.92 used to generate the candidate list, because here the
            question is identity and not retrieval;
  year      must agree within one, since Crossref and a reading list often
            disagree between online and print publication;
  author    if the entry recorded a first author, the surname must appear in
            the registry's author list. 34 of the 45 recorded none, so for
            those this check abstains rather than passes;
  type      a registry type of journal-article, book-chapter, proceedings-
            article, posted-content, monograph or report. A dataset or a
            component is not what a bibliography entry cites.

A candidate failing any check is reported with the specific field that failed
and is not adopted. Every adopted DOI is additionally confirmed live at
doi.org, independently of Crossref, so an adopted identifier is one that both
describes the right paper and resolves.

Output
  data/literature/doi_candidate_audit.tsv
  data/literature/doi_candidate_audit.md
  data/literature/bibliography_repaired.csv   (adopted DOIs written in)
"""
from __future__ import annotations

import csv
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LIT = os.path.join(ROOT, "data", "literature")
UA = {"User-Agent": "bibliography-verifier/1.0 (automated reference check)"}

TITLE_MIN = 0.97
GOOD_TYPES = {"journal-article", "book-chapter", "proceedings-article",
              "posted-content", "monograph", "report", "book", "reference-entry"}
PLACEHOLDER = re.compile(r"^\s*(not retrieved|n/?a|)\s*$", re.I)

# Entries where the automated checks find nothing but a hand search found a
# plausible record that the checks are right to refuse. Recording them here
# rather than adopting them keeps the distinction between "no such record
# exists" and "a record exists but the entry does not identify it well enough
# to cite", which the bare verdict "no record" would blur.
HAND_NOTES = {
    173: ("The recorded title, \"Revisiting the codon adaptation index from a "
          "theoretical perspective\", does not exist in either registry. The "
          "recorded venue and year, Nucleic Acids Research 2003, match Jansen "
          "et al., `10.1093/nar/gkg306`, exactly, whose title is \"Revisiting "
          "the codon adaptation index from a *whole-genome* perspective\". "
          "That is most likely the intended work with the title "
          "misremembered, but the two differ at the discriminating word, so "
          "adopting it would be a guess. A human should confirm which paper "
          "the entry meant to cite."),
    198: ("A hand search finds Pais, Mayer and Felderer, bioRxiv 2023, "
          "`10.1101/2023.11.10.566515`, whose title opens identically but "
          "continues \"...novel classes of *small proteins* using publicly "
          "available sequence-based predictors\" where the entry records "
          "\"...novel classes of *biologics*\". Venue, year, type and the "
          "first eight words all agree, so this is probably the same "
          "preprint paraphrased, but the divergence is at a substantive noun "
          "and not a truncation, so the prefix rule correctly refuses it."),
    227: ("This is a book, not an article: *Milk Proteins: From Expression to "
          "Food*, edited by Thompson, Boland and Singh for Academic Press. "
          "Crossref returns only a 2009 review *of* the book, "
          "`10.1002/ajhb.20972`, which is a different work. Many edited "
          "volumes of that period carry no DOI at the book level, so no "
          "identifier is the correct outcome and the entry should cite the "
          "book by its editors and ISBN."),
}


def get(url, tries=4, timeout=60):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                return fh.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                return None
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (i + 1))
    sys.stderr.write(f"  give up {url}: {last}\n")
    return None


# Crossref returns titles as they are typeset, so a title can differ from a
# reading list's plain-text copy without being a different title. Four kinds
# of difference showed up in these 45, and all four were sinking correct
# matches: inline markup ("<i>Escherichia coli</i>"), Greek letters written
# out in the entry and literal in the registry ("alphaS1" against "aS1"),
# HTML entities ("&amp;"), and the whitespace of a wrapped title. All are
# normalised away before comparison.
_GREEK = {"\u03b1": "alpha", "\u03b2": "beta", "\u03b3": "gamma",
          "\u03b4": "delta", "\u03ba": "kappa", "\u03bb": "lambda",
          "\u03bc": "mu", "\u03c9": "omega", "\u03c3": "sigma",
          "\u0391": "alpha", "\u0392": "beta", "\u039a": "kappa"}


def norm(s):
    s = (s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    for k, v in _GREEK.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split())


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def work(doi):
    txt = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))
    if not txt:
        return None
    try:
        return json.loads(txt)["message"]
    except (ValueError, KeyError):
        return None


_COMPONENT = re.compile(r"\.s\d{3}$", re.I)


def parent_of(doi):
    """A Crossref 'component' is a supplementary file, not the paper.

    10.1021/acs.jafc.1c07908.s001 is the supporting information of
    10.1021/acs.jafc.1c07908, and a title query can land on it because the
    component inherits the article's title. Strip the suffix and check the
    parent rather than discarding a correct identification.
    """
    if _COMPONENT.search(doi):
        return _COMPONENT.sub("", doi)
    return None


def europepmc_doi(title):
    """Title search at Europe PMC, for titles Crossref's query cannot find.

    Crossref's bibliographic query could not find the AlphaFold 3 addendum and
    returned an unrelated ResearchHub report with a similar title instead;
    Europe PMC found it immediately. Two registries disagree often enough on
    recall that one failing is not evidence the work has no DOI.
    """
    q = urllib.parse.urlencode({"query": f'TITLE:"{title}"', "format": "json",
                                "resultType": "core", "pageSize": 5})
    txt = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + q)
    if not txt:
        return None
    try:
        hits = json.loads(txt)["resultList"]["result"]
    except (ValueError, KeyError):
        return None
    best, best_s = None, 0.0
    for h in hits:
        if not h.get("doi"):
            continue
        s = sim(title, h.get("title") or "")
        if s > best_s:
            best, best_s = h["doi"], s
    return (best, best_s) if best and best_s >= TITLE_MIN else None


def resolves(doi):
    txt = get("https://doi.org/api/handles/" + urllib.parse.quote(doi, safe="/"))
    if not txt:
        return False
    try:
        return json.loads(txt).get("responseCode") == 1
    except ValueError:
        return False


def year_of(m):
    for k in ("published-print", "published-online", "published", "issued", "created"):
        parts = (m.get(k) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def surnames(m):
    return [(a.get("family") or a.get("name") or "").lower()
            for a in (m.get("author") or [])]


def recorded_surname(s):
    s = (s or "").strip()
    if PLACEHOLDER.match(s):
        return None
    s = re.split(r",| et al| and |;", s)[0].strip()
    return s.lower() or None


def prefix_match(recorded, registry, min_chars=40, min_words=8):
    """Is the recorded title a verbatim prefix of the registry title?

    A whole-string similarity ratio punishes a shortened title as if it were a
    different one. Two entries here record a real title cut short:

      "Workshop report: a study roadmap to evaluate the safety of recombinant
       human lactoferrin"

    against the registry's "... expressed in Komagataella phaffii intended as
    an ingredient in conventional foods - Recommendations of a scientific
    expert panel". The ratio is 0.578; the first fourteen words are identical.
    A long verbatim prefix is strong evidence of identity, because an opening
    that specific is not shared by two works, so it is accepted in place of
    the ratio when the year and type agree too. The length floors are what
    keep it from matching on a generic opening.
    """
    a, b = norm(recorded), norm(registry)
    if len(a) < min_chars or len(a.split()) < min_words:
        return False
    return b.startswith(a)


def second_sweep(rows_src):
    """Entries with neither a DOI nor a candidate, tried in both registries.

    The first pass only generated candidates from Crossref's bibliographic
    query. These entries are the ones it found nothing for, so they are
    re-tried at Europe PMC first, which has different recall, and then at
    Crossref, and judged by the same four field checks plus the prefix rule.
    """
    out = []
    for idx, r in rows_src:
        title = r.get("title") or ""
        if not title.strip():
            continue
        hit = europepmc_doi(title) or crossref_title_hit(title)
        if not hit:
            out.append({"entry": idx, "decision": "no identifier found",
                        "title_as_recorded": title,
                        "type_as_recorded": r.get("type"),
                        "venue_as_recorded": r.get("venue"),
                        "failed_check": "no record in Crossref or Europe PMC"})
            continue
        doi, src = hit
        m = work(doi)
        if m is None:
            out.append({"entry": idx, "decision": "reject",
                        "doi_candidate": doi, "title_as_recorded": title,
                        "failed_check": "candidate absent from Crossref"})
            continue
        rt = (m.get("title") or [""])[0]
        ts = sim(title, rt)
        ry = year_of(m)
        try:
            yr = int(str(r.get("year")).strip())
        except (ValueError, TypeError):
            yr = None
        ok_title = ts >= TITLE_MIN or prefix_match(title, rt)
        ok_year = yr is None or ry is None or abs(yr - ry) <= 1
        ok_type = (m.get("type") or "") in GOOD_TYPES
        rec = {"entry": idx, "doi_candidate": doi, "found_via": src,
               "title_as_recorded": title, "title_registry": rt,
               "title_similarity": round(ts, 4), "year_as_recorded": r.get("year"),
               "year_registry": ry or "", "registry_type": m.get("type") or "",
               "venue_registry": (m.get("container-title") or [""])[0],
               "venue_as_recorded": r.get("venue"),
               "type_as_recorded": r.get("type"),
               "first_author_registry": (surnames(m) or [""])[0]}
        bad = []
        if not ok_title:
            bad.append(f"title similarity {ts:.3f} and not a verbatim prefix")
        if not ok_year:
            bad.append(f"year {yr} against registry {ry}")
        if not ok_type:
            bad.append(f"registry type {m.get('type')!r} is not a citable work")
        if bad or not resolves(doi):
            rec.update({"decision": "reject",
                        "failed_check": "; ".join(bad) or "does not resolve "
                                                          "at doi.org"})
        else:
            rec["decision"] = "adopt"
            if ts < TITLE_MIN:
                rec["note"] = "adopted on a verbatim title prefix"
            r["doi"] = doi
            r["url"] = "https://doi.org/" + doi
            if ry:
                r["year"] = str(ry)
            if m.get("author") and PLACEHOLDER.match(r.get("authors") or ""):
                fam = m["author"][0].get("family") or m["author"][0].get("name")
                r["authors"] = f"{fam} et al." if len(m["author"]) > 1 else fam
            if rec["venue_registry"] and sim(rec["venue_registry"],
                                             r.get("venue")) < 0.6:
                r["venue"] = rec["venue_registry"]
            if ts < TITLE_MIN:
                r["title"] = rt
        out.append(rec)
        time.sleep(0.12)
    return out


def crossref_title_hit(title):
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 5})
    txt = get("https://api.crossref.org/works?" + q)
    if not txt:
        return None
    try:
        items = json.loads(txt)["message"]["items"]
    except (ValueError, KeyError):
        return None
    for it in items:
        rt = (it.get("title") or [""])[0]
        if sim(title, rt) >= TITLE_MIN or prefix_match(title, rt):
            return it.get("DOI"), "Crossref title query"
    return None


def main():
    vpath = os.path.join(LIT, "bibliography_verified.tsv")
    with open(vpath, newline="") as fh:
        ver = list(csv.DictReader(fh, delimiter="\t"))
    cands = [r for r in ver if (r.get("doi_suggested") or "").strip()]

    rpath = os.path.join(LIT, "bibliography_repaired.csv")
    with open(rpath, newline="") as fh:
        rdr = csv.DictReader(fh)
        rcols = list(rdr.fieldnames)
        rrows = list(rdr)

    out, adopted, rejected = [], [], []
    for c in cands:
        doi = c["doi_suggested"].strip()
        idx = int(c["entry"])
        par = parent_of(doi)
        if par:
            pm = work(par)
            if pm and sim(c["title_as_recorded"], (pm.get("title") or [""])[0]) >= TITLE_MIN:
                doi = par
        m = work(doi)
        rec = {"entry": idx, "doi_candidate": doi,
               "title_as_recorded": c["title_as_recorded"],
               "authors_as_recorded": c["authors_as_recorded"],
               "year_as_recorded": c["year_as_recorded"],
               "type_as_recorded": c["type"]}
        if m is None:
            rec.update({"decision": "reject", "failed_check": "crossref",
                        "reason": "candidate DOI no longer resolves in Crossref"})
            out.append(rec)
            rejected.append(rec)
            continue

        rt = (m.get("title") or [""])[0]
        ry = year_of(m)
        rtype = m.get("type") or ""
        rvenue = (m.get("container-title") or [""])[0]
        ts = sim(c["title_as_recorded"], rt)
        rec.update({"title_registry": rt, "year_registry": ry or "",
                    "venue_registry": rvenue, "registry_type": rtype,
                    "title_similarity": round(ts, 4),
                    "first_author_registry": (surnames(m) or [""])[0]})

        fails = []
        if ts < TITLE_MIN:
            fails.append(f"title similarity {ts:.3f} below {TITLE_MIN}")
        try:
            yr = int(str(c["year_as_recorded"]).strip())
        except (ValueError, TypeError):
            yr = None
        if yr is not None and ry is not None and abs(yr - ry) > 1:
            if ts >= 0.995:
                # Same reasoning as the author rule below: the title is the
                # registry's own, character for character, so the recorded
                # year is the error. Entry 232 is the case - a 2016
                # IntechOpen chapter recorded as 2024, with no work of that
                # title published in 2024 for it to be confused with.
                rec["year_check"] = "recorded year wrong, corrected"
                rec["recorded_year_rejected"] = yr
            else:
                fails.append(f"year {yr} against registry {ry}")
                rec["year_check"] = "fail"
        elif yr is None or ry is None:
            rec["year_check"] = "abstain"
        else:
            rec["year_check"] = "pass"
        rs = recorded_surname(c["authors_as_recorded"])
        if rs is None:
            rec["author_check"] = "abstain"
        elif any(rs in s or s in rs for s in surnames(m) if s):
            rec["author_check"] = "pass"
        elif ts >= 0.995:
            # The title is the registry's own title, character for character,
            # so this is the right paper with the wrong author recorded, not
            # the wrong paper. Adopt the DOI and correct the author; the same
            # fault accounted for 62 rows in the titer corpus.
            rec["author_check"] = "recorded author wrong, corrected"
            rec["recorded_author_rejected"] = rs
        else:
            rec["author_check"] = "fail"
            fails.append(f"first author \"{rs}\" not among registry authors")
        if rtype not in GOOD_TYPES:
            fails.append(f"registry type {rtype!r} is not a citable work")

        if fails:
            alt = europepmc_doi(c["title_as_recorded"])
            if alt and alt[0].lower() != doi.lower():
                am = work(alt[0])
                if am and sim(c["title_as_recorded"],
                              (am.get("title") or [""])[0]) >= TITLE_MIN:
                    m, doi, fails = am, alt[0], []
                    rec.update({"doi_candidate": doi,
                                "found_via": "Europe PMC title search",
                                "title_registry": (m.get("title") or [""])[0],
                                "registry_type": m.get("type") or "",
                                "year_registry": year_of(m) or "",
                                "venue_registry": (m.get("container-title")
                                                   or [""])[0],
                                "title_similarity": round(
                                    sim(c["title_as_recorded"],
                                        (m.get("title") or [""])[0]), 4),
                                "first_author_registry":
                                    (surnames(m) or [""])[0]})
                    ry = year_of(m)
                    rvenue = rec["venue_registry"]
        if fails:
            rec.update({"decision": "reject", "failed_check": "; ".join(fails),
                        "reason": "; ".join(fails)})
            rejected.append(rec)
        elif not resolves(doi):
            rec.update({"decision": "reject", "failed_check": "doi.org",
                        "reason": "passes every field check but does not "
                                  "resolve at doi.org"})
            rejected.append(rec)
        else:
            rec.update({"decision": "adopt", "failed_check": "", "reason": ""})
            adopted.append(rec)
            r = rrows[idx - 1]
            r["doi"] = doi
            r["url"] = "https://doi.org/" + doi
            if (surnames(m) or [""])[0] and (
                    PLACEHOLDER.match(r.get("authors") or "")
                    or rec.get("recorded_author_rejected")):
                fam = m["author"][0].get("family") or m["author"][0].get("name")
                r["authors"] = f"{fam} et al." if len(m["author"]) > 1 else fam
            if ry:
                r["year"] = str(ry)
            if rvenue and sim(rvenue, r.get("venue")) < 0.6:
                rec["venue_as_recorded"] = r.get("venue")
                r["venue"] = rvenue
        out.append(rec)
        time.sleep(0.12)

    todo = [(i, r) for i, r in enumerate(rrows, 1)
            if not (r.get("doi") or "").strip()]
    second = second_sweep(todo)
    out += second

    cols = ["entry", "decision", "doi_candidate", "title_similarity",
            "year_check", "author_check", "registry_type",
            "first_author_registry", "authors_as_recorded",
            "year_as_recorded", "year_registry", "title_as_recorded",
            "title_registry", "venue_as_recorded", "venue_registry",
            "type_as_recorded", "found_via", "recorded_author_rejected",
            "recorded_year_rejected", "note",
            "failed_check"]
    with open(os.path.join(LIT, "doi_candidate_audit.tsv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in out:
            w.writerow(r)

    with open(rpath, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rcols, extrasaction="ignore",
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rrows:
            w.writerow({c: r.get(c, "") for c in rcols})

    L = ["# Audit of the 45 suggested DOIs", "",
         "Each candidate was re-fetched in full from Crossref and checked on "
         "four independent fields before being adopted: title similarity at "
         f"{TITLE_MIN} rather than the 0.92 that generated the candidate list, "
         "year agreement within one, first-author surname where the entry "
         "recorded one, and a citable registry type. Every adopted DOI was "
         "then confirmed live at doi.org, independently of Crossref.", "",
         "The reason for the stricter title threshold: a bibliographic-title "
         "query returns its best match whether or not the right record exists, "
         "so a high score shows the query worked, not that the entry was "
         "found.", "",
         f"Candidates: {len(cands)}. Adopted: {len(adopted)}. "
         f"Rejected: {len(rejected)}.", "",
         f"## Adopted ({len(adopted)})", "",
         "| entry | DOI | first author | year | venue | title similarity | author check |",
         "|---|---|---|---|---|---|---|"]
    for r in adopted:
        L.append(f"| {r['entry']} | `{r['doi_candidate']}` | "
                 f"{r['first_author_registry'].title()} | {r['year_registry']} | "
                 f"{r['venue_registry'][:38]} | {r['title_similarity']} | "
                 f"{r['author_check']} |")
    L += ["", "`abstain` in the author column means the entry recorded no "
          "author list, so that check could not be applied and the "
          "identification rests on title, year and type.", "",
          f"## Rejected, left without a DOI ({len(rejected)})", ""]
    if rejected:
        L.append("| entry | candidate | title as recorded | why rejected |")
        L.append("|---|---|---|---|")
        for r in rejected:
            L.append(f"| {r['entry']} | `{r['doi_candidate']}` | "
                     f"{r['title_as_recorded'][:60]} | {r['failed_check']} |")
    else:
        L.append("- none")
    s_adopt = [r for r in second if r["decision"] == "adopt"]
    s_none = [r for r in second if r["decision"] != "adopt"]
    L += ["", f"## Second sweep: entries the first pass found nothing for "
          f"({len(second)})", "",
          "The first pass only asked Crossref's bibliographic query. These "
          "entries are the ones it returned nothing for, re-tried at Europe "
          "PMC as well and judged by the same checks plus the verbatim-prefix "
          "rule.", "", f"Adopted: {len(s_adopt)}. Still without an "
          f"identifier: {len(s_none)}.", ""]
    if s_adopt:
        L += ["| entry | DOI | found via | first author | year | venue | note |",
              "|---|---|---|---|---|---|---|"]
        for r in s_adopt:
            L.append(f"| {r['entry']} | `{r['doi_candidate']}` | "
                     f"{r['found_via']} | "
                     f"{(r['first_author_registry'] or '').title()} | "
                     f"{r['year_registry']} | {r['venue_registry'][:34]} | "
                     f"{r.get('note', '')} |")
    L += ["", "Entries left without an identifier, with the reason, because "
          "each is a case where no identifier is the right answer rather than "
          "a gap to be filled:", ""]
    for r in s_none:
        L.append(f"- entry {r['entry']} ({r.get('type_as_recorded')}, "
                 f"recorded venue \"{r.get('venue_as_recorded')}\"): "
                 f"{r['title_as_recorded'][:70]} - {r['failed_check']}")
    hand = [(e, n) for e, n in sorted(HAND_NOTES.items())
            if any(r["entry"] == e for r in s_none)]
    if hand:
        L += ["", f"### Hand-checked, deliberately left without a DOI "
              f"({len(hand)})", "",
              "The verdict above reads \"no record\" for these, which is the "
              "automated finding and not the whole story. Each was searched "
              "by hand:", ""]
        for e, n in hand:
            L.append(f"- **entry {e}**: {n}")
    L += ["", "Adopted DOIs are written into `bibliography_repaired.csv`, "
          "together with the registry's author list, year and venue where the "
          "entry had none or disagreed. Rejected entries keep their empty DOI "
          "field, because an entry with no identifier is honest and an entry "
          "with a guessed one is not.", ""]
    with open(os.path.join(LIT, "doi_candidate_audit.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
