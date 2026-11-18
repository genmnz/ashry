#!/usr/bin/env python3
"""Sequence-feature panel for recombinant-protein producibility.

Every feature is computed from the mature amino-acid sequence alone (plus the
UniProt PTM annotation already curated in the panel), so the index can be
applied to any candidate protein before any construct exists.

Feature families
----------------
size/composition : length, mass, residue fractions, aromaticity, GRAVY,
                   instability index, isoelectric point
charge/disorder  : fraction of charged residues (FCR), net charge per residue
                   (NCPR), Das-Pappu diagram-of-states class, charge
                   patterning kappa, FoldIndex, metapredict disorder if the
                   package is installed
secretory load   : disulfide count and density, odd-cysteine flag,
                   N-X-S/T sequon count and density, O-glycosylation sites,
                   phosphosite count and density, haem requirement
host strain      : compositional distance between the target's amino-acid
                   demand and the host's own biomass protein composition, and
                   the share of the target's residues that are metabolically
                   expensive for the host

References for each formula are in docs/FEATURE_PANEL.md.
"""
from __future__ import annotations

import json
import math
import os
from typing import Dict, List, Optional

# Kyte & Doolittle 1982 hydropathy
KD = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5,
    "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9,
    "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9,
    "Y": -1.3, "V": 4.2,
}
KD_MIN, KD_MAX = -4.5, 4.5

POS = set("KR")
NEG = set("DE")
AROMATIC = set("FWY")

# Akashi & Gojobori (2002) biosynthetic cost of each amino acid, in units of
# high-energy phosphate bonds (~P) in a glucose-respiring heterotroph.  Used
# only as a composition-weighting scale; the authoritative per-protein cost in
# this work comes from the genome-scale model, not from this table.
AKASHI_GOJOBORI_COST = {
    "A": 11.7, "R": 27.3, "N": 14.7, "D": 12.7, "C": 24.7, "Q": 16.3,
    "E": 15.3, "G": 11.7, "H": 38.3, "I": 32.3, "L": 27.3, "K": 30.3,
    "M": 34.3, "F": 52.0, "P": 20.3, "S": 11.7, "T": 18.7, "W": 74.3,
    "Y": 50.0, "V": 23.3,
}

# iMT1026v3 PROTEINS_glyc pseudoreaction: the host's own protein amino-acid
# composition on glycerol, mmol/gDW.  Normalised to fractions below.
HOST_AA_MMOL = {
    "A": 0.8071, "R": 0.4967, "N": 0.4495, "D": 0.4495, "C": 0.0320,
    "Q": 0.7272, "E": 0.7272, "G": 0.5811, "H": 0.1909, "I": 0.4094,
    "L": 0.6606, "K": 0.6166, "M": 0.0749, "F": 0.2932, "P": 0.4063,
    "S": 0.6103, "T": 0.6189, "W": 0.0970, "Y": 0.2054, "V": 0.5404,
}
_hs = sum(HOST_AA_MMOL.values())
HOST_AA_FRAC = {k: v / _hs for k, v in HOST_AA_MMOL.items()}


# ---------------------------------------------------------------------------
# charge patterning
# ---------------------------------------------------------------------------

def _blob_sigma(blob: str) -> float:
    n = len(blob)
    if n == 0:
        return 0.0
    npos = sum(1 for a in blob if a in POS)
    nneg = sum(1 for a in blob if a in NEG)
    fcr = (npos + nneg) / n
    if fcr == 0:
        return 0.0
    ncpr = (npos - nneg) / n
    return ncpr ** 2 / fcr


def _delta(seq: str, blob: int) -> float:
    """Das & Pappu (2013) delta: variance of blob charge asymmetry."""
    n = len(seq)
    if n < blob:
        return 0.0
    sigma_seq = _blob_sigma(seq)
    nb = n - blob + 1
    acc = 0.0
    for i in range(nb):
        acc += (_blob_sigma(seq[i:i + blob]) - sigma_seq) ** 2
    return acc / nb


def _delta_max(seq: str, blob: int) -> float:
    """delta of the maximally charge-segregated permutation of `seq`."""
    npos = sum(1 for a in seq if a in POS)
    nneg = sum(1 for a in seq if a in NEG)
    nneu = len(seq) - npos - nneg
    seg = "K" * npos + "A" * nneu + "D" * nneg
    return _delta(seg, blob)


def kappa(seq: str) -> Optional[float]:
    """Charge patterning parameter kappa in [0, 1]; None if uncharged.

    0 = charges perfectly mixed, 1 = perfectly segregated into blocks.
    Das R & Pappu RV, PNAS 110:13392 (2013).
    """
    npos = sum(1 for a in seq if a in POS)
    nneg = sum(1 for a in seq if a in NEG)
    if npos == 0 or nneg == 0:
        return None
    ks = []
    for blob in (5, 6):
        dmax = _delta_max(seq, blob)
        if dmax <= 0:
            continue
        ks.append(_delta(seq, blob) / dmax)
    return sum(ks) / len(ks) if ks else None


def das_pappu_class(fplus: float, fminus: float) -> str:
    """Diagram-of-states region (Das, Ruff & Pappu 2015)."""
    fcr = fplus + fminus
    ncpr = abs(fplus - fminus)
    if fcr < 0.25 and ncpr < 0.25:
        return "R1_globule_tadpole"
    if 0.25 <= fcr <= 0.35 and ncpr <= 0.35:
        return "R2_boundary"
    if fcr > 0.35 and ncpr <= 0.35:
        return "R3_strong_polyampholyte"
    if fcr > 0.35 and ncpr > 0.35:
        return "R4_R5_strong_polyelectrolyte"
    return "R2_boundary"


def fold_index(seq: str) -> float:
    """FoldIndex: >0 folded, <0 intrinsically unfolded.

    Prilusky J et al., Bioinformatics 21:3435 (2005):
        FoldIndex = 2.785 <H> - |<R>| - 1.151
    with <H> the mean Kyte-Doolittle hydrophobicity scaled to [0, 1] and <R>
    the net charge per residue.
    """
    if not seq:
        return 0.0
    h = sum(KD.get(a, 0.0) for a in seq) / len(seq)
    h01 = (h - KD_MIN) / (KD_MAX - KD_MIN)
    npos = sum(1 for a in seq if a in POS)
    nneg = sum(1 for a in seq if a in NEG)
    r = (npos - nneg) / len(seq)
    return 2.785 * h01 - abs(r) - 1.151


def fold_index_profile(seq: str, window: int = 51) -> List[float]:
    out = []
    half = window // 2
    for i in range(len(seq)):
        out.append(fold_index(seq[max(0, i - half):i + half + 1]))
    return out


def disorder_fraction_foldindex(seq: str, window: int = 51) -> float:
    prof = fold_index_profile(seq, window)
    return sum(1 for v in prof if v < 0) / len(prof) if prof else 0.0


# ---------------------------------------------------------------------------
# hydrophobic patches
# ---------------------------------------------------------------------------

def max_hydrophobic_patch(seq: str, window: int = 9,
                          threshold: float = 1.6) -> int:
    """Longest run of windows whose mean Kyte-Doolittle score exceeds a cut.

    A coarse, transparent surrogate for aggregation-prone stretches; it is
    reported alongside, not instead of, the charge/disorder descriptors.
    """
    if len(seq) < window:
        return 0
    run = best = 0
    for i in range(len(seq) - window + 1):
        mean = sum(KD.get(a, 0.0) for a in seq[i:i + window]) / window
        if mean >= threshold:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


# ---------------------------------------------------------------------------
# metapredict (optional)
# ---------------------------------------------------------------------------

_META = None


def _metapredict():
    global _META
    if _META is None:
        try:
            import metapredict as mp
            _META = mp
        except Exception:  # noqa: BLE001
            _META = False
    return _META


def disorder_metapredict(seq: str) -> Optional[Dict[str, float]]:
    mp = _metapredict()
    if not mp:
        return None
    try:
        scores = mp.predict_disorder(seq)
    except Exception:  # noqa: BLE001
        return None
    n = len(scores)
    return {
        "metapredict_mean": sum(scores) / n,
        "metapredict_frac_gt_0_5": sum(1 for s in scores if s > 0.5) / n,
        "metapredict_max": max(scores),
    }


# ---------------------------------------------------------------------------
# the panel
# ---------------------------------------------------------------------------

def compute_features(spec) -> Dict[str, float]:
    """`spec` is a protein_cost.ProteinSpec."""
    seq = spec.mature
    n = len(seq)
    comp = {a: seq.count(a) / n for a in "ACDEFGHIKLMNPQRSTVWY"}

    npos = sum(seq.count(a) for a in POS)
    nneg = sum(seq.count(a) for a in NEG)
    fplus, fminus = npos / n, nneg / n
    fcr = fplus + fminus
    ncpr = (npos - nneg) / n

    f: Dict[str, float] = {
        "length": n,
        "n_cys": seq.count("C"),
        "frac_cys": comp["C"],
        "odd_cysteine": 1.0 if seq.count("C") % 2 else 0.0,
        "frac_pro": comp["P"],
        "frac_gly": comp["G"],
        "frac_ser_thr": comp["S"] + comp["T"],
        "frac_aromatic": sum(comp[a] for a in AROMATIC),
        "gravy": sum(KD.get(a, 0.0) for a in seq) / n,
        "fcr": fcr,
        "ncpr": ncpr,
        "abs_ncpr": abs(ncpr),
        "fplus": fplus,
        "fminus": fminus,
        "kappa": kappa(seq),
        "das_pappu_class": das_pappu_class(fplus, fminus),
        "fold_index": fold_index(seq),
        "disorder_frac_foldindex": disorder_fraction_foldindex(seq),
        "max_hydrophobic_patch": max_hydrophobic_patch(seq),
        # secretory load
        "n_disulfide": spec.n_disulfide if spec.secreted else 0,
        "disulfide_per_100aa": (100.0 * spec.n_disulfide / n
                                if spec.secreted else 0.0),
        "n_sequon": spec.sequons() if spec.secreted else 0,
        "sequon_per_100aa": (100.0 * spec.sequons() / n
                             if spec.secreted else 0.0),
        "n_o_glyc_site": spec.n_o_glyc_site if spec.secreted else 0,
        "n_phosphosite": spec.n_phosphosite,
        "phosphosite_per_100aa": 100.0 * spec.n_phosphosite / n,
        "n_haem": spec.n_haem,
        "secreted": 1.0 if spec.secreted else 0.0,
        "has_signal_peptide": 1.0 if spec.signal_end else 0.0,
    }

    # Biopython descriptors
    try:
        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        pa = ProteinAnalysis(seq.replace("U", "C").replace("X", "A")
                                .replace("B", "N").replace("Z", "Q"))
        f["instability_index"] = pa.instability_index()
        f["isoelectric_point"] = pa.isoelectric_point()
        f["aromaticity"] = pa.aromaticity()
        f["molecular_weight"] = pa.molecular_weight()
        hel, trn, sht = pa.secondary_structure_fraction()
        f["ss_frac_helix"] = hel
        f["ss_frac_turn"] = trn
        f["ss_frac_sheet"] = sht
    except Exception:  # noqa: BLE001
        pass

    # host compositional strain
    tgt = {a: comp[a] for a in HOST_AA_FRAC}
    tot = sum(tgt.values())
    tgt = {a: v / tot for a, v in tgt.items()}
    f["aa_js_divergence_vs_host"] = _js(tgt, HOST_AA_FRAC)
    f["aa_cost_akashi"] = sum(AKASHI_GOJOBORI_COST[a] * v
                              for a, v in tgt.items())
    host_cost = sum(AKASHI_GOJOBORI_COST[a] * v
                    for a, v in HOST_AA_FRAC.items())
    f["aa_cost_ratio_vs_host"] = f["aa_cost_akashi"] / host_cost
    f["frac_rare_in_host"] = sum(tgt[a] for a in ("C", "M", "W")
                                 if a in tgt)

    md = disorder_metapredict(seq)
    if md:
        f.update(md)
    return f


def _js(p: Dict[str, float], q: Dict[str, float]) -> float:
    """Jensen-Shannon divergence, log base 2, in bits."""
    keys = set(p) | set(q)
    out = 0.0
    for k in keys:
        pi, qi = p.get(k, 0.0), q.get(k, 0.0)
        mi = 0.5 * (pi + qi)
        if pi > 0:
            out += 0.5 * pi * math.log2(pi / mi)
        if qi > 0:
            out += 0.5 * qi * math.log2(qi / mi)
    return out


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from protein_cost import specs_from_uniprot_json

    here = os.path.dirname(os.path.abspath(__file__))
    specs = specs_from_uniprot_json(
        os.path.join(here, "..", "data", "sequences", "targets.json"))
    cols = ["length", "fold_index", "disorder_frac_foldindex", "kappa",
            "fcr", "ncpr", "gravy", "n_disulfide", "n_sequon",
            "n_phosphosite", "aa_cost_ratio_vs_host",
            "aa_js_divergence_vs_host", "das_pappu_class"]
    hdr = f"{'protein':34s}" + "".join(f"{c[:9]:>11s}" for c in cols)
    print(hdr)
    for nm, s in sorted(specs.items()):
        f = compute_features(s)
        row = f"{nm:34s}"
        for c in cols:
            v = f.get(c)
            if isinstance(v, str):
                row += f"{v[:11]:>11s}"
            elif v is None:
                row += f"{'NA':>11s}"
            else:
                row += f"{v:11.3f}"
        print(row)
