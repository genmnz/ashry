#!/usr/bin/env python3
"""Correct extraction of PTM counts and the mature chain from UniProtKB.

Counting UniProt feature *lines* is wrong, and wrong in four distinct ways
that all inflate the secretory load of a protein. Each rule below was derived
from a case where the naive count disagreed with the curated truth, and each
is covered by a regression test in `self_test()`.

1. **Glycosylation is not all enzymatic.** Human serum albumin (P02768)
   carries 24 Glycosylation lines, of which 22 read "N-linked (Glc)
   (glycation) lysine": non-enzymatic glycation of lysine by glucose, not an
   oligosaccharyltransferase site. The remaining two are genuine
   "N-linked (GlcNAc...) asparagine" entries but both are qualified "in
   variant Redhill" and "in variant Casebrook", so wild-type albumin has no
   N-glycan at all. Charging all 24 as sequons cut albumin's computed ceiling
   by a third. Rule: require an N-linked GlcNAc entry on asparagine, reject
   glycation, and reject anything restricted to a named variant.

2. **One line per glycoform, not per site.** Bovine lactoferrin (P24627) has
   9 N-linked lines at 5 distinct positions, because Asn-387 and Asn-495 each
   carry three alternate glycoform entries. Rule: count distinct positions.

3. **A signal peptide is not always cleaved.** Ovalbumin (P01012) has
   Signal 22-48 annotated "Not cleaved", and a Chain feature covering 2-386.
   Treating position 48 as the cleavage site deletes an eighth of the
   protein. Rule: ignore a signal annotated as not cleaved, and prefer the
   Chain feature as the authoritative mature range.

4. **An inter-chain disulfide is a point feature on each partner.**
   Kappa-casein (P02668) has three Disulfide bond lines: the real bond 32-109,
   plus 32-32 and 109-109, which are the same bond annotated once on each
   partner cysteine. Beta-lactoglobulin (P02754) has 82-176, 122-135 and
   122-137, the last qualified "Alternate", so it has two disulfides and not
   three. Rules: drop point features where start equals end, drop entries
   qualified Alternate, and deduplicate by position pair.

The same alternate/variant rules apply to modified residues, so a
phosphosite annotated only in a variant or as an alternate to another
modification is not double-counted.
"""
from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Optional, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
UNIPROT_DIR = os.path.join(ROOT, "data", "external", "uniprot")

# Qualifiers meaning the feature is absent from the wild-type canonical
# protein. Note that "alternate" is deliberately NOT here, because it means
# different things on different feature types:
#
#   on a Glycosylation line it marks an alternate *glycoform at an occupied
#   site* - bovine lactoferrin's Asn-387 carries complex, high-mannose and
#   hybrid entries all qualified "alternate", and the site is occupied in
#   every case, so rejecting them would lose two real sequons;
#
#   on a Disulfide bond line it marks an alternate *bonding pattern* -
#   beta-lactoglobulin's 122-137 is an alternative pairing to 122-135, so
#   counting both would invent a disulfide that does not exist.
#
# The two cases therefore use different filters, below.
_NOT_CANONICAL = re.compile(
    r"\bin variant\b|\bin isoform\b|\bin vitro\b|\bby host\b|\bin Ref\.",
    re.I)
_ALTERNATE = re.compile(r"\balternate\b", re.I)
_NOT_CLEAVED = re.compile(r"not cleaved", re.I)
# an enzymatic N-glycan: GlcNAc transferred to asparagine
_N_GLYCAN = re.compile(r"^N-linked \(GlcNAc", re.I)
_O_GLYCAN = re.compile(r"^O-linked", re.I)
_GLYCATION = re.compile(r"glycation", re.I)
_PHOSPHO = re.compile(r"^Phospho", re.I)


def load(acc: str) -> dict:
    with open(os.path.join(UNIPROT_DIR, f"{acc}.json")) as fh:
        return json.load(fh)


def _features(d: dict, ftype: str):
    for f in d.get("features", []):
        if f["type"] != ftype:
            continue
        loc = f["location"]
        yield (loc["start"].get("value"), loc["end"].get("value"),
               f.get("description") or "")


def mature_range(d: dict) -> Tuple[int, int, str]:
    """(start, end, basis) of the mature chain, 1-based inclusive."""
    length = d["sequence"]["length"]
    chains = [(s, e, desc) for s, e, desc in _features(d, "Chain")
              if s and e and not _NOT_CANONICAL.search(desc)]
    signals = [(s, e, desc) for s, e, desc in _features(d, "Signal")]
    cleaved = [(s, e, desc) for s, e, desc in signals
               if not _NOT_CLEAVED.search(desc)
               and not _NOT_CANONICAL.search(desc)]
    if chains:
        # the longest canonical chain is the mature product
        s, e, _ = max(chains, key=lambda t: (t[1] - t[0]))
        return s, e, "Chain feature"
    if cleaved:
        return cleaved[0][1] + 1, length, "signal cleavage site"
    return 1, length, "full precursor (no signal, no chain)"


def n_disulfide(d: dict) -> int:
    seen = set()
    for s, e, desc in _features(d, "Disulfide bond"):
        if s is None or e is None:
            continue
        if s == e:
            # point feature: the partner annotation of a bond already listed
            continue
        if _NOT_CANONICAL.search(desc) or _ALTERNATE.search(desc):
            # "Alternate" on a disulfide means an alternative pairing of the
            # same cysteines, so counting it would invent a bond.
            continue
        seen.add((min(s, e), max(s, e)))
    return len(seen)


def n_glyc_sites(d: dict) -> int:
    """Distinct asparagines carrying an enzymatic N-glycan."""
    pos = set()
    for s, e, desc in _features(d, "Glycosylation"):
        if not _N_GLYCAN.match(desc):
            continue
        if _GLYCATION.search(desc) or _NOT_CANONICAL.search(desc):
            continue
        # "alternate" is kept: it marks an alternate glycoform at a site that
        # is occupied either way, not an uncertain site.
        pos.add(s)
    return len(pos)


def o_glyc_sites(d: dict) -> int:
    pos = set()
    for s, e, desc in _features(d, "Glycosylation"):
        if not _O_GLYCAN.match(desc) or _NOT_CANONICAL.search(desc):
            continue
        pos.add(s)
    return len(pos)


def n_phosphosites(d: dict) -> int:
    pos = set()
    for s, e, desc in _features(d, "Modified residue"):
        if not _PHOSPHO.match(desc) or _NOT_CANONICAL.search(desc):
            continue
        if _ALTERNATE.search(desc):
            # an alternate modification competing for the same residue
            continue
        pos.add(s)
    return len(pos)


def annotation(acc: str) -> Dict[str, object]:
    d = load(acc)
    s, e, basis = mature_range(d)
    seq = d["sequence"]["value"]
    return {
        "accession": acc,
        "uniprot_id": d.get("uniProtkbId"),
        "organism": d.get("organism", {}).get("scientificName"),
        "length_precursor": d["sequence"]["length"],
        "mature_start": s,
        "mature_end": e,
        "mature_basis": basis,
        "length_mature": e - s + 1,
        "mature_sequence": seq[s - 1:e],
        "n_disulfide": n_disulfide(d),
        "n_glyc_site": n_glyc_sites(d),
        "n_o_glyc_site": o_glyc_sites(d),
        "n_phosphosite": n_phosphosites(d),
    }


# ---------------------------------------------------------------------------
# regression tests: one per failure mode that was actually observed
# ---------------------------------------------------------------------------

EXPECTED = [
    # (accession, field, expected, why)
    ("P02768", "n_glyc_site", 0,
     "all 24 Glycosylation lines are lysine glycation or variant-only, so "
     "wild-type human serum albumin carries no enzymatic N-glycan"),
    ("P24627", "n_glyc_site", 5,
     "9 N-linked lines at 5 distinct positions; Asn-387 and Asn-495 each "
     "carry three alternate glycoform entries"),
    ("P01012", "length_mature", 385,
     "ovalbumin's Signal 22-48 is annotated 'Not cleaved' and its Chain "
     "feature covers 2-386, so the mature chain is 385 residues"),
    ("P02668", "n_disulfide", 1,
     "kappa-casein's 32-109 bond is also annotated as point features 32-32 "
     "and 109-109, one on each partner cysteine"),
    ("P02754", "n_disulfide", 2,
     "beta-lactoglobulin has 82-176 and 122-135; the third line, 122-137, is "
     "qualified 'Alternate'"),
]


def self_test(verbose: bool = True) -> bool:
    ok = True
    for acc, field, want, why in EXPECTED:
        got = annotation(acc)[field]
        good = (got == want)
        ok = ok and good
        if verbose:
            mark = "PASS" if good else "FAIL"
            print(f"[{mark}] {acc} {field}: got {got}, expected {want}")
            if not good:
                print(f"       {why}")
    return ok


if __name__ == "__main__":
    import sys
    passed = self_test()
    print()
    accs = sorted(f[:-5] for f in os.listdir(UNIPROT_DIR)
                  if f.endswith(".json"))
    print(f"{'acc':8s} {'id':16s} {'Lpre':>5s} {'Lmat':>5s} {'SS':>3s} "
          f"{'Nglyc':>5s} {'Oglyc':>5s} {'P':>3s}  basis")
    for acc in accs:
        a = annotation(acc)
        print(f"{acc:8s} {str(a['uniprot_id']):16s} "
              f"{a['length_precursor']:5d} {a['length_mature']:5d} "
              f"{a['n_disulfide']:3d} {a['n_glyc_site']:5d} "
              f"{a['n_o_glyc_site']:5d} {a['n_phosphosite']:3d}  "
              f"{a['mature_basis']}")
    sys.exit(0 if passed else 1)
