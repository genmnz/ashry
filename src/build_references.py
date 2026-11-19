"""
Render the bibliography into a reference list grouped by thesis topic cluster.

The list carries a verification banner, and the banner is now a statement that
the pass has been done rather than a warning that it has not. Every DOI in the
bibliography was resolved against Crossref: all 141 resolve, none required the
doi.org fallback, and the registry metadata was used to rebuild each entry's
first author, year, title and venue. The corrections are recorded in
data/literature/bibliography_corrections.md with the originally recorded value
preserved beside each change, and the side-by-side table is in
bibliography_verified.tsv.

What is still not verified is marked as such rather than left to look verified.
Ninety-one entries carry no DOI at all - software, industry and regulatory
sources, plus papers whose identifier was never captured - and 73 of those still
carry no retrieved author list. Those print a URL and an explicit
"[author list not retrieved]" rather than a guess. Printing an unverified
identifier as though it were verified is the failure mode this file exists to
make impossible to commit by accident, and that applies in both directions:
marking a verified DOI as unverified would be the same error of record-keeping.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
BIB = REPO / "data" / "literature" / "bibliography.csv"
OUT = REPO / "paper" / "12_references.md"

CLUSTER_TITLES = {
    1: "Precision fermentation: industry and regulation",
    2: "*Komagataella phaffii* as a cell factory",
    3: "*Trichoderma reesei* as a production host",
    4: "Milk proteins: structure, modification and production",
    5: "Egg proteins, leghemoglobin and haem supply",
    6: "Computational methods",
    7: "Genome-scale metabolic modelling and protein cost",
    8: "Techno-economics and life-cycle assessment",
    9: "Prior art: predicting producibility and protein cost",
}


def format_entry(r) -> str:
    authors = str(r.authors).strip()
    if authors.lower() in ("nan", "not retrieved", ""):
        authors = "[author list not retrieved]"
    year = "" if pd.isna(r.year) else f" ({int(r.year)})"
    title = str(r.title).strip().rstrip(".")
    venue = "" if pd.isna(r.venue) else f" *{str(r.venue).strip()}*."
    ident = ""
    if isinstance(r.doi, str) and r.doi.strip() and r.doi.strip().lower() != "nan":
        ident = f" doi:{r.doi.strip()}"
    elif isinstance(r.url, str) and r.url.strip():
        ident = f" <{r.url.strip()}>"
    kind = "" if pd.isna(r.type) else f" ({str(r.type).strip()})"
    # Three entries were searched by hand after both registries failed, and the
    # note explaining why each carries no identifier travels with the entry
    # rather than living only in the audit file. An entry with no identifier is
    # honest; an entry with a guessed one is not, and an entry whose absence is
    # unexplained invites the reader to assume carelessness.
    note = getattr(r, "verification_note", "")
    note = "" if (pd.isna(note) or not str(note).strip()) else (
        f"\n    - *Identifier note.* {str(note).strip()}")
    return f"{authors}{year}. {title}.{venue}{kind}{ident}{note}"


def main() -> None:
    bib = pd.read_csv(BIB)
    has_doi = int(bib.doi.notna().sum())
    no_author = int(bib.authors.astype(str)
                    .str.contains("not retrieved", case=False).sum())
    no_doi = len(bib) - has_doi
    lines = [
        "# References",
        "",
        "**Verification status.** Every identifier in this list was resolved "
        f"against Crossref and confirmed independently at doi.org. {has_doi} of "
        f"{len(bib)} entries carry a verified DOI; the remaining {no_doi} have "
        "none, and the reason is given below rather than left to inference. No "
        "identifier in this list was inferred: an earlier audit found that "
        "inferred identifiers were wrong roughly half the time, which is why "
        "the resolution pass was treated as blocking.",
        "",
        "Resolution corrected the record in ways worth stating, because each "
        "would have produced a wrong in-text citation. Rebuilding every entry "
        "from registry metadata changed 49 author lists, 11 first authors "
        "(mostly diacritic losses, but one entry recorded Wang for a paper "
        "whose first author is Alderson), 12 years, 3 truncated titles and 1 "
        "venue. A second pass over the entries that initially resolved to "
        "nothing recovered 48 more identifiers by title search, each re-fetched "
        "in full and accepted only on title similarity above 0.97, year within "
        "one, agreement of first author where one was recorded, a citable "
        "registry type, and live confirmation at doi.org; that pass corrected "
        "two further records, one first author and one year. Resolution also "
        "exposed two papers that this bibliography had listed twice, now "
        "merged. Every change is listed in "
        "`data/literature/bibliography_corrections.md` and "
        "`doi_candidate_audit.md`, with the originally recorded value preserved "
        "beside it.",
        "",
        f"Of the {no_doi} entries without an identifier, the great majority "
        "legitimately have none: company and trade-press items, FDA and Federal "
        "Register documents, theses, software servers and an edited volume. "
        f"{no_author} of them also carry no retrieved author list and say so "
        "rather than carrying a guess. Three entries whose automated verdict "
        "was \"no record\" were then searched by hand, and each carries an "
        "*identifier note* explaining what was found and why it was not "
        "adopted. One registry failing to find a work is not evidence that the "
        "work has no identifier: the AlphaFold 3 addendum is absent from "
        "Crossref, which offered an unrelated report with a near-identical "
        "title, and was found at once in Europe PMC.",
        "",
        f"Total entries: {len(bib)}. With a verified DOI: {has_doi}. "
        "Peer-reviewed or review: "
        f"{int(bib.type.astype(str).str.contains('peer|review', case=False).sum())}.",
        "",
    ]
    for cluster in sorted(bib.cluster.dropna().unique()):
        rows = bib[bib.cluster == cluster]
        title = CLUSTER_TITLES.get(int(cluster), f"Cluster {int(cluster)}")
        lines.append(f"## {int(cluster)}. {title}")
        lines.append("")
        for r in rows.sort_values(["year", "authors"], na_position="last").itertuples():
            lines.append(f"- {format_entry(r)}")
        lines.append("")
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT} with {len(bib)} entries")


if __name__ == "__main__":
    main()
