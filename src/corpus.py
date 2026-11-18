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
)

_FRAGMENT_RE = re.compile("|".join(FRAGMENT_PATTERNS), re.I)


def is_fragment_or_fusion(protein_name: str) -> bool:
    """True when the produced molecule is not the intact protein itself."""
    return bool(_FRAGMENT_RE.search(str(protein_name)))


def drop_fragments(df, column: str = "protein_name"):
    """Return (kept, dropped) so that the exclusion is always reportable."""
    mask = df[column].map(is_fragment_or_fusion)
    return df[~mask].copy(), df[mask].copy()
