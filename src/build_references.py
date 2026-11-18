"""
Render the bibliography into a reference list grouped by thesis topic cluster.

The list carries a verification banner. Identifiers that were inferred rather than
resolved were found to be wrong roughly half the time during an audit, so each
entry is marked with whether it carries a DOI at all, and the banner states that
the re-resolution pass against Crossref and Europe PMC has not yet been applied.
Printing an unverified identifier as though it were verified is the failure mode
this file is designed to make impossible to commit by accident.
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
        ident = f" doi:{r.doi.strip()} [unverified]"
    elif isinstance(r.url, str) and r.url.strip():
        ident = f" <{r.url.strip()}>"
    kind = "" if pd.isna(r.type) else f" ({str(r.type).strip()})"
    return f"{authors}{year}. {title}.{venue}{kind}{ident}"


def main() -> None:
    bib = pd.read_csv(BIB)
    lines = [
        "# References",
        "",
        "**Verification status.** This list is generated directly from the "
        "project bibliography. An audit found that identifiers which had been "
        "inferred rather than resolved were wrong roughly half the time, so every "
        "DOI below is marked `[unverified]` until the re-resolution pass against "
        "Crossref and Europe PMC has been applied and recorded. Entries whose "
        "author list could not be retrieved say so rather than carrying a guess. "
        "Neither shortcut is acceptable in a submitted thesis, and Appendix E "
        "lists both as blocking tasks.",
        "",
        f"Total entries: {len(bib)}. With a DOI: "
        f"{int(bib.doi.notna().sum())}. Peer-reviewed or review: "
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
