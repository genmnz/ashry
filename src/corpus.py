"""
Shared filters for the titre corpus.

One rule in here is load-bearing. A record whose product is a *fragment* of a
panel protein, or a *fusion* carrying a partner, is not a record of that protein
being produced. Bovine casein macropeptide is a 64-residue glycopeptide released
from kappa-casein by chymosin; a strain secreting it has not secreted a casein.
Pooling the two inflates apparent casein performance by nearly an order of
magnitude, and the mistake is easy to make because a name-matching join on
"casein" catches both. It was caught during cross-checking between two
independent analyses of the same corpus, and this module exists so that the two
pipelines in this repository cannot make it again.

The same rule removes fusions (a sfGFP- or SUMO-tagged product includes the
partner's mass in the reported titre), isolated domains and antibody fragments,
and short antimicrobial peptides excised from a longer precursor, whose length
and composition features would otherwise be taken from the precursor.
"""
from __future__ import annotations

import re

FRAGMENT_PATTERNS = (
    r"\bfragment\b",
    r"macropeptide",
    r"\bpeptide\b",
    r"lactoferricin",
    r"\bfusion\b",
    r"\bhybrid\b",
    r"\bdomain\b",
    r"\bscFv\b",
    r"\bFab\b",
    r"\bRBD\b",
    r"-derived",
    # A carrier protein is a fusion by another name, and this one mattered. The
    # corpus's highest-titre lipase record, 10 g/L, is Candida antarctica lipase
    # B expressed on a *Trichoderma reesei* cellobiohydrolase I carrier: most of
    # the reported mass is the carrier, and the carrier was chosen because it
    # secretes well. It passed the filter because the record says "carrier"
    # rather than "fusion". A parallel analysis hit the same record from the
    # other direction, where a name match made the carrier the product and
    # credited cellobiohydrolase I with the whole 10 g/L.
    r"\bcarrier\b",
    r"\bchimera\b",
    r"\bchimaer",
    r"-tag\b",
    r"\bC-tag\b",
)

_FRAGMENT_RE = re.compile("|".join(FRAGMENT_PATTERNS), re.I)


def is_fragment_or_fusion(protein_name: str) -> bool:
    """True when the produced molecule is not the intact protein itself."""
    return bool(_FRAGMENT_RE.search(str(protein_name)))


def drop_fragments(df, column: str = "protein_name"):
    """Return (kept, dropped) so that the exclusion is always reportable."""
    mask = df[column].map(is_fragment_or_fusion)
    return df[~mask].copy(), df[mask].copy()


# ---------------------------------------------------------------------------
# Corpus loader
# ---------------------------------------------------------------------------
# The corpus was rebuilt by a parallel literature pass into
# data/literature/titers_merged.tsv: 306 records merged from five harvests, each
# carrying a verbatim evidence quote, a resolved DOI, a confidence grade and a
# product_class / is_therapeutic flag. It supersedes titers_host_panel.csv,
# which is kept only so that the earlier numbers in the repository history
# remain reproducible. The column names differ, so they are normalised here
# rather than in each analysis script.

from pathlib import Path

import pandas as pd

MERGED = Path(__file__).resolve().parents[1] / "data" / "literature" / "titers_merged.tsv"

_RENAME = {
    "host_canonical": "host",
    "localisation": "secreted",
    "cultivation": "cultivation_mode",
    "uniprot": "uniprot_accession",
    "doi": "doi_or_url",
}


def load_titres(path: Path | None = None) -> pd.DataFrame:
    """Load the merged corpus under the column names the analyses expect."""
    df = pd.read_csv(path or MERGED, sep="\t")
    df = df.rename(columns=_RENAME)
    # 'secreted' was a yes/no column in the old file; the merged corpus records
    # the localisation itself, so translate rather than reinterpret.
    df["secreted"] = df["secreted"].astype(str).str.contains(
        "secret", case=False).map({True: "yes", False: "no"})
    df["is_therapeutic"] = df["is_therapeutic"].astype(str).str.strip().str.lower()
    df["product_class"] = df["product_class"].astype(str).str.strip()
    return df


def food_subset(df: pd.DataFrame) -> pd.DataFrame:
    """Food and food-adjacent products only: therapeutics are a different game.

    A human therapeutic is developed under a cost structure and a regulatory
    regime that permit effort a food protein cannot justify, so pooling the two
    confounds protein difficulty with development spend. The flag comes from the
    corpus, not from this module.
    """
    return df[df.is_therapeutic != "yes"].copy()
