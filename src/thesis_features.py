"""
Sequence-level feature panel for the producibility model.

Features are grouped by the bottleneck they are meant to report on:

  size/composition   length, molecular mass, amino-acid fractions
  folding            cysteines, disulfide bonds, FoldIndex, predicted disorder
  solubility         GRAVY, net charge at pH 7, pI, fraction charged residues,
                     Uversky mean net charge vs mean hydropathy placement
  PTM load           N-glycosylation sequons, annotated phosphosites, haem
  translation        codon adaptation of the optimised gene (see codon_opt.py)

FoldIndex (Prilusky et al. 2005, Bioinformatics 21:3435) is computed in full here
rather than called from a web service, so the pipeline runs offline:

    FoldIndex = 2.785 * <H> - |<R>| - 1.151

with <H> the mean Kyte-Doolittle hydropathy scaled to 0-1 and <R> the mean net
charge per residue. Negative values predict intrinsic disorder. It is a weak
predictor on its own, which is why metapredict is used when available and
FoldIndex is reported as the transparent, dependency-free fallback.
"""
from __future__ import annotations

import json
from pathlib import Path

from Bio.SeqUtils.ProtParam import ProteinAnalysis

REPO = Path(__file__).resolve().parents[1]

KD = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5,
    "G": -0.4, "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8,
    "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}
KD_MIN, KD_MAX = -4.5, 4.5

try:  # optional, heavy dependency
    import metapredict as _metapredict
except Exception:  # pragma: no cover
    _metapredict = None


def scaled_hydropathy(seq: str) -> float:
    vals = [(KD[a] - KD_MIN) / (KD_MAX - KD_MIN) for a in seq if a in KD]
    return sum(vals) / len(vals) if vals else float("nan")


def mean_net_charge(seq: str) -> float:
    pos = sum(seq.count(a) for a in "KR")
    neg = sum(seq.count(a) for a in "DE")
    return (pos - neg) / len(seq) if seq else float("nan")


def fold_index(seq: str) -> float:
    return 2.785 * scaled_hydropathy(seq) - abs(mean_net_charge(seq)) - 1.151


def fraction_charged(seq: str) -> float:
    return sum(seq.count(a) for a in "KRDE") / len(seq) if seq else float("nan")


def disorder_profile(seq: str) -> list[float] | None:
    if _metapredict is None:
        return None
    try:
        return list(_metapredict.predict_disorder(seq))
    except Exception:  # pragma: no cover
        return None


def window_fold_index(seq: str, window: int = 51) -> list[float]:
    """Sliding-window FoldIndex, the per-residue disorder fallback."""
    if len(seq) < window:
        return [fold_index(seq)] * len(seq)
    half = window // 2
    out = []
    for i in range(len(seq)):
        lo, hi = max(0, i - half), min(len(seq), i + half + 1)
        out.append(fold_index(seq[lo:hi]))
    return out


def longest_run(flags: list[bool]) -> int:
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


def featurise(name: str, seq: str, annotation: dict | None = None) -> dict:
    annotation = annotation or {}
    pa = ProteinAnalysis(seq)
    prof = disorder_profile(seq)
    # always compute the transparent fallback too, so both are on the record
    wfi_all = window_fold_index(seq)
    foldindex_fraction = sum(1 for v in wfi_all if v < 0) / len(wfi_all)
    foldindex_longest = longest_run([v < 0 for v in wfi_all])
    if prof is not None:
        disorder_frac = sum(1 for v in prof if v >= 0.5) / len(prof)
        longest_idr = longest_run([v >= 0.5 for v in prof])
        disorder_mean = sum(prof) / len(prof)
        disorder_method = "metapredict"
    else:
        wfi = window_fold_index(seq)
        disorder_frac = sum(1 for v in wfi if v < 0) / len(wfi)
        longest_idr = longest_run([v < 0 for v in wfi])
        disorder_mean = float("nan")
        disorder_method = "foldindex-window51"

    cys = seq.count("C")
    ss = int(annotation.get("disulfide_bonds", 0))
    row = {
        "protein": name,
        "length": len(seq),
        "mw_kda": pa.molecular_weight() / 1000.0,
        "pI": pa.isoelectric_point(),
        "gravy": pa.gravy(),
        "aromaticity": pa.aromaticity(),
        "instability_index": pa.instability_index(),
        "helix_frac": pa.secondary_structure_fraction()[0],
        "turn_frac": pa.secondary_structure_fraction()[1],
        "sheet_frac": pa.secondary_structure_fraction()[2],
        "net_charge_per_res": mean_net_charge(seq),
        "fraction_charged": fraction_charged(seq),
        "scaled_hydropathy": scaled_hydropathy(seq),
        "fold_index": fold_index(seq),
        "disorder_fraction": disorder_frac,
        "disorder_mean": disorder_mean,
        "longest_disordered_run": longest_idr,
        "disorder_method": disorder_method,
        "foldindex_disorder_fraction": foldindex_fraction,
        "foldindex_longest_run": foldindex_longest,
        "cysteines": cys,
        "disulfide_bonds": ss,
        "free_cysteines": max(cys - 2 * ss, 0),
        "disulfides_per_100aa": 100.0 * ss / len(seq),
        "n_sequons": len([1 for i in range(len(seq) - 2)
                          if seq[i] == "N" and seq[i + 1] != "P"
                          and seq[i + 2] in "ST"]),
        "n_glyc_annotated": int(annotation.get("n_glyc_sites_annotated", 0)),
        "phosphoserines": int(annotation.get("phosphoserines", 0)),
        "phosphosites_per_100aa": 100.0 * int(annotation.get("phosphoserines", 0)) / len(seq),
        "haem_per_chain": int(annotation.get("haem_per_chain", 0)),
        "category": annotation.get("category", ""),
    }
    for aa in "ACDEFGHIKLMNPQRSTVWY":
        row[f"frac_{aa}"] = seq.count(aa) / len(seq)
    return row


def main() -> None:
    import csv

    from thesis_model import read_fasta

    meta = {m["key"]: m for m in json.loads(
        (REPO / "data" / "sequences" / "targets_metadata.json").read_text())}
    seqs = read_fasta(REPO / "data" / "sequences" / "targets.fasta")

    rows = []
    for header, seq in seqs.items():
        key = header.split("|")[0]
        rows.append(featurise(key, seq, meta.get(key)))

    out = REPO / "results" / "tables" / "target_features.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"{'protein':<22}{'len':>5}{'disord':>8}{'longIDR':>9}{'foldIdx':>9}"
          f"{'gravy':>8}{'pI':>7}{'SS':>4}{'seq':>5}{'pS':>4}  method")
    for r in rows:
        print(f"{r['protein']:<22}{r['length']:>5}{r['disorder_fraction']:>8.2f}"
              f"{r['longest_disordered_run']:>9}{r['fold_index']:>9.3f}"
              f"{r['gravy']:>8.3f}{r['pI']:>7.2f}{r['disulfide_bonds']:>4}"
              f"{r['n_sequons']:>5}{r['phosphoserines']:>4}  {r['disorder_method']}")


if __name__ == "__main__":
    main()
