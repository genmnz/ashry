"""
Codon optimisation of the panel for Komagataella phaffii, and the codon-level
features used by the producibility model.

What is computed
----------------
* w_i, the relative adaptiveness of each codon within its synonymous family,
  from the host codon-usage table.
* CAI_genome: the geometric mean of w_i over a coding sequence. NOTE the honest
  caveat carried through the thesis: classical CAI (Sharp & Li 1987) uses a
  reference set of highly expressed genes, not whole-genome usage. With only a
  whole-genome table available offline this is a genome-wide adaptation index,
  which is a weaker but unbiased proxy; it is never used as the sole feature.
* Three designs per protein:
    - "native_like"  : the mammalian/avian codon usage transplanted unchanged
                       (what you get if you order the natural gene)
    - "max_cai"      : always the most adapted codon (maximises CAI, but creates
                       long homopolymers and unrealistic GC runs)
    - "harmonised"   : sampling proportional to host usage, with design filters:
                       no run of >= 6 identical nucleotides, GC between 35 and 60%
                       in every 50-nt window, no internal BamHI/EcoRI/XhoI/NotI
                       sites, no AATAAA-like premature polyadenylation motifs.
  The harmonised design is the one proposed for synthesis in the appendix.

Everything is deterministic given the seed, so the appendix sequences are
reproducible.
"""
from __future__ import annotations

import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CDS_DIR = REPO / "data" / "external" / "kphaffii_cds"
TABLE_HIGH = CDS_DIR / "codon_usage_highly_expressed.tsv"
TABLE_GENOME = CDS_DIR / "codon_usage_genome.tsv"
# Kept for comparison only: a built-in genome-average table with no CDS count
# and no retrieval provenance beyond a 2012 software release.
TABLE_LEGACY = REPO / "data" / "external" / "codon_usage_p_pastoris_kazusa.json"
TABLE = TABLE_HIGH

STOP = "*"
RESTRICTION = {
    "BamHI": "GGATCC", "EcoRI": "GAATTC", "XhoI": "CTCGAG",
    "NotI": "GCGGCCGC", "SacI": "GAGCTC", "SalI": "GTCGAC",
}
POLYA_MOTIFS = ("AATAAA", "TATATA")


def _finalise(by_aa, source: str, weights: dict[str, float] | None = None) -> dict:
    if weights is None:
        weights = {}
        for aa, codons in by_aa.items():
            mx = max(f for _, f in codons) or 1.0
            for codon, f in codons:
                weights[codon] = (f / mx) if f > 0 else 1e-3
    return {
        "source": source,
        "by_aa": {aa: sorted(c, key=lambda x: -x[1]) for aa, c in by_aa.items()},
        "weights": weights,
    }


def load_table(path: Path = TABLE) -> dict:
    """Codon usage and relative adaptiveness for *K. phaffii*.

    The reference set matters more than it appears to. CAI (Sharp and Li 1987)
    measures how closely a gene's codon choice resembles that of *highly
    expressed* genes, not the genomic average. Against a genome-average table
    every native gene scores near the middle by construction and the index
    carries almost no information: the point of the index is the separation
    between abundant-protein usage and average usage, and a genome-average
    reference sets that separation to zero.

    The default table is therefore the 165-gene highly expressed reference
    computed from the RefSeq GS115 CDS set (GCF_000027005.1, 5,040 CDS,
    2,399,341 sense codons): cytosolic ribosomal proteins, translation factors,
    chaperones, glycolytic enzymes and alcohol oxidase, the standard proxy
    classes where no expression data for the organism exists. The genome-average
    table and the legacy 2012 built-in table load through the same function so
    that the three can be compared, which is done explicitly in main().
    """
    path = Path(path)
    by_aa: dict[str, list[tuple[str, float]]] = defaultdict(list)
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        for c in data["codons"]:
            by_aa[c["amino_acid"]].append((c["codon"], float(c["fraction"])))
        return _finalise(by_aa, data.get("source", ""))

    weights: dict[str, float] = {}
    with path.open() as fh:
        header = fh.readline().rstrip("\n").split("\t")
        idx = {name: i for i, name in enumerate(header)}
        for line in fh:
            if not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            aa = f[idx["aa"]]
            codon = f[idx["codon"]]
            if aa in ("*", "Stop"):
                continue
            by_aa[aa].append((codon, float(f[idx["fraction_of_aa"]])))
            w = float(f[idx["relative_adaptiveness_w"]])
            weights[codon] = w if w > 0 else 1e-3
    label = ("highly expressed reference set, 165 genes"
             if "highly" in path.name else "genome average, all CDS")
    return _finalise(by_aa, f"RefSeq GCF_000027005.1 ({label})", weights)


def cai(cds: str, weights: dict[str, float]) -> float:
    codons = [cds[i:i + 3] for i in range(0, len(cds) - 2, 3)]
    vals = [weights.get(c, 1e-3) for c in codons
            if c in weights and weights.get(c) is not None]
    vals = [v for v in vals if v > 0]
    if not vals:
        return float("nan")
    return math.exp(sum(math.log(v) for v in vals) / len(vals))


def gc(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else float("nan")


def gc3(cds: str) -> float:
    third = cds[2::3]
    return gc(third)


def longest_homopolymer(seq: str) -> int:
    best = 1
    run = 1
    for a, b in zip(seq, seq[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    return best


def violations(seq: str) -> list[str]:
    out = []
    if longest_homopolymer(seq) >= 6:
        out.append(f"homopolymer>={longest_homopolymer(seq)}")
    for name, site in RESTRICTION.items():
        if site in seq:
            out.append(f"site:{name}")
    for m in POLYA_MOTIFS:
        if m in seq:
            out.append(f"motif:{m}")
    for i in range(0, max(len(seq) - 50, 1), 10):
        w = seq[i:i + 50]
        if len(w) == 50 and not (0.35 <= gc(w) <= 0.60):
            out.append(f"gc_window@{i}:{gc(w):.2f}")
            break
    return out


def design_max_cai(protein: str, table: dict) -> str:
    return "".join(table["by_aa"][aa][0][0] for aa in protein)


def design_harmonised(protein: str, table: dict, seed: int = 20260101,
                      attempts: int = 20000) -> tuple[str, list[str]]:
    """Usage-proportional sampling with local repair of design-rule violations."""
    rng = random.Random(seed)
    by_aa = table["by_aa"]

    def sample(aa: str) -> str:
        codons = by_aa[aa]
        total = sum(f for _, f in codons) or 1.0
        r = rng.random() * total
        acc = 0.0
        for codon, f in codons:
            acc += f
            if r <= acc:
                return codon
        return codons[0][0]

    best: tuple[int, str] | None = None
    for _ in range(attempts):
        cds = "".join(sample(aa) for aa in protein)
        v = violations(cds)
        if not v:
            return cds, []
        if best is None or len(v) < best[0]:
            best = (len(v), cds)
    return best[1], violations(best[1])


def reverse_translate_uniform(protein: str, table: dict, seed: int = 7) -> str:
    """Uniform random choice among synonymous codons: the unadapted null.

    The ideal negative control would be the real bovine/avian coding sequence, but
    that requires a nucleotide database this pipeline does not assume. A uniform
    synonymous draw is the assumption-free null: it is what a gene would look like
    if the host's codon preferences carried no information at all.
    """
    rng = random.Random(seed)
    return "".join(rng.choice([c for c, _ in table["by_aa"][aa]]) for aa in protein)


def main() -> None:
    import csv

    from thesis_model import read_fasta

    table = load_table()
    seqs = read_fasta(REPO / "data" / "sequences" / "targets.fasta")
    out_dir = REPO / "results" / "constructs"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    fasta_lines = []
    for header, prot in seqs.items():
        key = header.split("|")[0]
        prot = prot.replace("U", "C")
        max_cds = design_max_cai(prot, table)
        harm_cds, viol = design_harmonised(prot, table)
        naive_cds = reverse_translate_uniform(prot, table)
        rows.append({
            "protein": key,
            "aa_length": len(prot),
            "cai_max_design": cai(max_cds, table["weights"]),
            "cai_harmonised": cai(harm_cds, table["weights"]),
            "cai_uniform_control": cai(naive_cds, table["weights"]),
            "gc_harmonised": gc(harm_cds),
            "gc3_harmonised": gc3(harm_cds),
            "gc_max_design": gc(max_cds),
            "gc3_max_design": gc3(max_cds),
            "longest_homopolymer_harmonised": longest_homopolymer(harm_cds),
            "design_violations": ";".join(viol) or "none",
            "cds_length_nt": len(harm_cds),
        })
        fasta_lines.append(f">{key}|harmonised_Kphaffii\n")
        for i in range(0, len(harm_cds), 60):
            fasta_lines.append(harm_cds[i:i + 60] + "\n")

    (out_dir / "codon_optimised_cds.fasta").write_text("".join(fasta_lines))
    tbl = REPO / "results" / "tables" / "codon_design.csv"
    with tbl.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # How much does the reference set matter? Score the same designs against all
    # three tables. If the genome-average and legacy tables compress the range,
    # any CAI reported against them was carrying less information than it looked.
    ref_rows = []
    for label, path in (("highly expressed (165 genes)", TABLE_HIGH),
                        ("genome average (5,040 CDS)", TABLE_GENOME),
                        ("legacy built-in table (2012)", TABLE_LEGACY)):
        tb = load_table(path)
        scores = {"reference": label, "source": tb["source"]}
        for kind, design in (("max_design", design_max_cai),
                             ("uniform_control", reverse_translate_uniform)):
            vals = [cai(design(prot.replace("U", "C"), tb), tb["weights"])
                    for prot in seqs.values()]
            scores[f"cai_{kind}_mean"] = sum(vals) / len(vals)
        scores["separation_max_minus_control"] = (
            scores["cai_max_design_mean"] - scores["cai_uniform_control_mean"])
        ref_rows.append(scores)
    ref_tbl = REPO / "results" / "tables" / "codon_reference_comparison.csv"
    with ref_tbl.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ref_rows[0]))
        w.writeheader()
        w.writerows(ref_rows)
    print("\nhow much the CAI reference set matters:")
    print(f"{'reference':<30}{'CAI(max)':>10}{'CAI(uniform)':>14}{'separation':>12}")
    for r in ref_rows:
        print(f"{r['reference']:<30}{r['cai_max_design_mean']:>10.3f}"
              f"{r['cai_uniform_control_mean']:>14.3f}"
              f"{r['separation_max_minus_control']:>12.3f}")
    print()

    print(f"{'protein':<22}{'CAI_max':>9}{'CAI_harm':>10}{'CAI_ctrl':>10}"
          f"{'GC':>7}{'GC3':>7}  violations")
    for r in rows:
        print(f"{r['protein']:<22}{r['cai_max_design']:>9.3f}"
              f"{r['cai_harmonised']:>10.3f}{r["cai_uniform_control"]:>10.3f}"
              f"{r['gc_harmonised']:>7.3f}{r['gc3_harmonised']:>7.3f}  "
              f"{r['design_violations']}")


if __name__ == "__main__":
    main()
