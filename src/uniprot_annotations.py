"""
Derive per-protein annotations from the verified UniProtKB entries.

Why this file exists
--------------------
The sequence-feature analysis in Chapter 6 rests on one positive result, the
negative association between disulfide bond density and achieved titre. Until
now the disulfide count for any protein outside the nine-member target panel was
*assumed*, as cysteines // 2, because no annotation was on hand. That assumption
is defensible but it is still an assumption, and it is being made on the very
variable the chapter's only positive finding depends on.

A parallel literature pass re-fetched all 36 accessions in the corpus from the
UniProtKB REST API and verified each against its CRC64 checksum, so the full
annotation record is now available locally. This module reads the real feature
tables instead:

  * Disulfide bonds   'Disulfide bond' features, counting an inter-chain bond
                      once and excluding alternatives. UniProt marks a bond that
                      is only observed in one of several reported pairings with
                      'Alternate' in its description; counting those would
                      double-count the same cysteine pair (bovine
                      beta-lactoglobulin is the case in point: three DISULFID
                      lines, one of them an alternate, hence two bonds).
  * N-glycosylation   'Glycosylation' features whose description names an
                      N-linked attachment, which is what the host's
                      oligosaccharyltransferase would install.
  * Phosphoserines    'Modified residue' features naming phosphoserine. These
                      matter for the caseins, which carry up to thirteen.
  * Signal peptide    the 'Signal' feature's end position, so that the mature
                      chain can be taken without guessing a cleavage site.
  * Haem              a 'Binding site' feature naming haem or heme.

Nothing here is inferred. If a feature is absent from the entry the count is
zero, and the count of *annotated* zero is reported separately from the
assumption-based fallback so that the two can never be confused downstream.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
UNIPROT = REPO / "data" / "external" / "uniprot"


def _desc(feature: dict) -> str:
    return str(feature.get("description") or "")


def annotate(entry: dict) -> dict:
    feats = entry.get("features", []) or []
    seq = entry.get("sequence", {}).get("value", "")

    ss = 0
    interchain = 0
    for f in feats:
        if f["type"] != "Disulfide bond":
            continue
        d = _desc(f).lower()
        if "alternate" in d:
            continue
        start = int(f["location"]["start"]["value"])
        end = int(f["location"]["end"]["value"])
        if start == end or "interchain" in d:
            # UniProt records an inter-chain bond as a point feature on each of
            # the two participating cysteines, so a single bond appears twice.
            # Bovine kappa-casein is the case that forced this rule: its entry
            # carries one intramolecular bond (32-109) plus two point features
            # describing that same pair "in linked form" in the casein polymer.
            # Counting those as bonds would treat one bond as three.
            interchain += 1
            continue
        ss += 1
    interchain //= 2

    # UniProt files non-enzymatic glycation of lysine under the same
    # 'Glycosylation' feature type and the same 'N-linked' prefix as true
    # oligosaccharyltransferase sites: human serum albumin carries 24 such
    # lines, all 'N-linked (Glc) (glycation) lysine', several of them in vitro.
    # Albumin is not a glycoprotein, and charging 24 glycans to it cut its
    # computed ceiling by a third. A site is counted only when it is N-linked,
    # is not glycation, and sits on an asparagine in the sequence itself.
    # Counts are over distinct *positions*, not feature lines. UniProt writes one
    # line per observed glycoform, so bovine lactoferrin's five glycosylation
    # sites appear as nine lines: Asn-387 and Asn-495 each carry three
    # 'alternate' entries for complex, high-mannose and hybrid glycans. Counting
    # lines would charge nine glycans to a five-site protein.
    n_sites, o_sites = set(), set()
    for f in feats:
        if f["type"] != "Glycosylation":
            continue
        d = _desc(f).lower()
        if "glycation" in d:
            continue
        pos = int(f["location"]["start"]["value"])
        residue = seq[pos - 1] if 0 < pos <= len(seq) else ""
        if "n-linked" in d and residue == "N":
            n_sites.add(pos)
        elif "o-linked" in d and residue in ("S", "T"):
            o_sites.add(pos)
    n_glyc, o_glyc = len(n_sites), len(o_sites)
    phos = len({int(f["location"]["start"]["value"]) for f in feats
                if f["type"] == "Modified residue"
                and "phosphoserine" in _desc(f).lower()})
    haem = sum(1 for f in feats if f["type"] == "Binding site"
               and ("heme" in _desc(f).lower() or "haem" in _desc(f).lower()))
    # A 'Signal' feature marked 'Not cleaved' is not a cleavage site. Ovalbumin
    # is the case: residues 22-48 form an internal, uncleaved signal sequence, so
    # the mature protein is the whole chain and treating 48 as a cleavage point
    # would delete an eighth of it.
    signal_end = 0
    for f in feats:
        if f["type"] != "Signal":
            continue
        if "not cleaved" in _desc(f).lower():
            continue
        signal_end = int(f["location"]["end"]["value"])
        break

    return {
        "accession": entry["primaryAccession"],
        "uniprot_id": entry.get("uniProtkbId", ""),
        "organism": entry.get("organism", {}).get("scientificName", ""),
        "length": int(entry.get("sequence", {}).get("length", len(seq))),
        "sequence": seq,
        "signal_peptide_end": signal_end,
        "disulfide_bonds": ss,
        "interchain_disulfides": interchain,
        "disulfide_bonds_total": ss + interchain,
        "disulfide_bonds_annotated": True,
        "n_glyc_sites_annotated": n_glyc,
        "o_glyc_sites_annotated": o_glyc,
        "phosphoserines": phos,
        "haem_per_chain": 1 if haem else 0,
        "cysteines": seq.count("C"),
    }


def load_all() -> dict[str, dict]:
    """Every locally verified UniProt entry, keyed by accession."""
    out = {}
    for path in sorted(UNIPROT.glob("*.json")):
        entry = json.loads(path.read_text())
        a = annotate(entry)
        out[a["accession"]] = a
    return out


def main() -> None:
    import csv
    anns = load_all()
    out = REPO / "results" / "tables" / "uniprot_annotations.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = [c for c in next(iter(anns.values())) if c != "sequence"]
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for a in anns.values():
            w.writerow({c: a[c] for c in cols})

    print(f"{'acc':<9}{'id':<16}{'len':>5}{'sig':>5}{'S-S':>5}{'Cys':>5}"
          f"{'Cys//2':>8}{'Nglyc':>6}{'Oglyc':>6}{'pSer':>5}{'haem':>5}")
    for a in anns.values():
        print(f"{a['accession']:<9}{a['uniprot_id']:<16}{a['length']:>5}"
              f"{a['signal_peptide_end']:>5}{a['disulfide_bonds']:>5}"
              f"{a['cysteines']:>5}{a['cysteines'] // 2:>8}"
              f"{a['n_glyc_sites_annotated']:>6}{a['o_glyc_sites_annotated']:>6}"
              f"{a['phosphoserines']:>5}{a['haem_per_chain']:>5}")
    mism = [a for a in anns.values()
            if a["disulfide_bonds"] != a["cysteines"] // 2]
    print(f"\nthe cysteines//2 assumption is wrong for {len(mism)} of "
          f"{len(anns)} accessions:")
    for a in mism:
        print(f"  {a['accession']} {a['uniprot_id']:<14} annotated "
              f"{a['disulfide_bonds']} vs assumed {a['cysteines'] // 2}")


if __name__ == "__main__":
    main()
