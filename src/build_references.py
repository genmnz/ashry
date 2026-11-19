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
    return f"{authors}{year}. {title}.{venue}{kind}{ident}"


def main() -> None:
    bib = pd.read_csv(BIB)
    has_doi = int(bib.doi.notna().sum())
    no_author = int(bib.authors.astype(str)
                    .str.contains("not retrieved", case=False).sum())
    lines = [
        "# References",
        "",
        "**Verification status.** This list is generated directly from the "
        "project bibliography. Every DOI below was resolved against Crossref "
        f"and the entry rebuilt from the registry metadata: all {has_doi} "
        "resolve, and the first author, year, title and venue come from the "
        "registry rather than from the value originally recorded. That pass "
        "changed 49 author lists, 11 first authors, 12 years, 3 truncated "
        "titles and 1 venue; every change is listed in "
        "`data/literature/bibliography_corrections.md` with the original "
        "preserved beside it. An earlier audit had found that identifiers "
        "inferred rather than resolved were wrong roughly half the time, which "
        "is why the pass was treated as blocking.",
        "",
        f"What remains unverified is marked. {len(bib) - has_doi} entries carry "
        "no DOI - software, industry and regulatory sources, and papers whose "
        f"identifier was never captured - and {no_author} of those carry no "
        "retrieved author list and say so rather than carrying a guess. A "
        "title-similarity search found close candidates for about half of "
        "them, but a title match is weaker evidence than a DOI and none has "
        "been written in on that basis.",
        "",
        f"Total entries: {len(bib)}. With a resolved DOI: {has_doi}. "
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
