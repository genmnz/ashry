"""
Does mean predicted disorder really track ceiling utilisation?

An independently curated panel of dairy, egg and haem proteins, built by a
parallel analysis of the same literature, reported the mean metapredict
disorder score as strongly associated with ceiling utilisation: rho = -0.833,
permutation p = 0.00025, surviving Benjamini-Hochberg correction across 32
features at q = 0.008, with leave-one-out holding rho between -0.79 and -0.93.

That is a positive finding in a thesis whose other sequence-feature results are
null, so it gets audited rather than adopted. This script runs the tests the
original analysis could not run on itself.

OUTCOME: the finding was retracted. This script's structural test showed the
correlation could not be distinguished from a two-cluster contrast, and a
parallel provenance audit of the primary sources found three faults in the
titres -- an intracellular yield recorded as a secretion titre, an orthologue-
pooling join that let bovine entries borrow human numbers, and a carrier
construct counted as its passenger. Corrected, the association is rho = -0.483,
p = 0.117, with nothing surviving FDR correction. The script is kept because the
comparison between the published figure and the corrected one is the evidence
for Appendix F, and because the tests themselves are the reusable part.

Three of them matter.

  1. Leave-one-out cannot detect a two-cluster artefact. The panel contains two
     intrinsically disordered proteins (bovine osteopontin and kappa-casein, both
     with mean disorder near 0.87) and twelve globular ones (0.06 to 0.16).
     Removing any single protein leaves the other disordered one in place, so the
     contrast survives. The test that discriminates is whether the association
     holds *within* the globular group, where the predictor varies over a narrow
     range and cannot simply be reading off protein class.

  2. The response may be reading the experiment rather than the protein. A
     fed-batch run beats a shake flask by one to two orders of magnitude, and
     Chapter 6 finds that indicator to be the only variable in the corpus with
     predictive skill. The association is therefore refitted with the process
     term partialled out and within the fed-batch records alone.

  3. Two of the panel's fourteen titres are the same datum. Human and bovine
     lactoferrin both carry 3,500 mg/L, which is a single medium-confidence
     bovine record whose own quotation describes recovery after cell lysis, and
     the two alpha-lactalbumins both carry 600 mg/L. Substituting the
     species-matched, high-confidence, secreted records from the merged corpus
     tests how much of the result rests on that.

Finally the hypothesis is refitted on this thesis's own corpus, which was
curated independently and has a different roster, as a genuine replication.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import uniprot_annotations

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"
PANEL = TABLES / "external_panel_ceiling_gap.csv"

BENCHMARKS = ("chymosin_bovine", "serum_albumin_human")
ORTHOLOGUE_DUPLICATES = ("lactoferrin_human", "alpha_lactalbumin_human")
# Species-matched, high-confidence, secreted replacements from titers_merged.tsv
SPECIES_MATCHED = {"lactoferrin_bovine": 232.6, "lactoferrin_human": 2214.0}
# The thesis's declared target class: dairy, egg and haem food proteins.
DAIRY_EGG_HAEM = {
    "P02662", "P02663", "P02666", "P02668",          # caseins
    "P02754", "P00711", "P00709",                      # whey
    "P01012", "P01005", "P02701", "P02789", "P00698",  # egg
    "P02236", "P02189",                                # haem
    "P24627", "P02788", "P31096",                      # lactoferrin, osteopontin
}


def mean_disorder(accession: str, anns: dict) -> float:
    import metapredict
    a = anns[accession]
    mature = a["sequence"][a["signal_peptide_end"]:]
    prof = list(metapredict.predict_disorder(mature))
    return sum(prof) / len(prof)


def partial_spearman(x, y, z) -> tuple[float, float]:
    """Spearman of x and y with z partialled out, on ranks."""
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    Z = np.column_stack([np.ones(len(z)), np.asarray(z, float)])
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    r, p = stats.pearsonr(ex, ey)
    return float(r), float(p)


def main() -> None:
    anns = uniprot_annotations.load_all()
    rows = []

    if PANEL.exists():
        d = pd.read_csv(PANEL)
        d = d[(d.host == "Komagataella phaffii") & (~d.protein.isin(BENCHMARKS))].copy()
        d["dm"] = [mean_disorder(a, anns) for a in d.accession]
        d["titer_fixed"] = [SPECIES_MATCHED.get(p, t)
                            for p, t in zip(d.protein, d.measured_titer_mg_L)]
        d["util_fixed"] = (d.ceiling_utilisation * d.titer_fixed
                           / d.measured_titer_mg_L)
        d["fedbatch"] = [int(any(k in str(c).lower() for k in
                                 ("fedbatch", "fed-batch", "bioreactor",
                                  "high-cell-density")))
                         for c in d.cultivation]

        def add(label, sub, col):
            if len(sub) < 5:
                return
            rho, p = stats.spearmanr(sub.dm, sub[col].map(math.log10))
            rows.append({"test": label, "n_proteins": len(sub),
                         "spearman_rho": float(rho), "p_value": float(p)})

        add("external panel, as published", d, "ceiling_utilisation")
        add("external panel, species-matched high-confidence lactoferrin",
            d, "util_fixed")
        add("  and one protein per orthologous pair",
            d[~d.protein.isin(ORTHOLOGUE_DUPLICATES)], "util_fixed")
        add("  and high-confidence records only", d[d.confidence == "high"],
            "util_fixed")
        add("  and within fed-batch records only", d[d.fedbatch == 1], "util_fixed")
        add("  GLOBULAR ONLY (mean disorder < 0.2)", d[d.dm < 0.2], "util_fixed")

        r, p = partial_spearman(d.dm, d.util_fixed.map(math.log10), d.fedbatch)
        rows.append({"test": "external panel, process term partialled out",
                     "n_proteins": len(d), "spearman_rho": r, "p_value": p})

    # Replication on this thesis's own corpus.
    own = pd.read_csv(TABLES / "producibility_dataset.csv")
    for label, sub in (
            ("this thesis's corpus, all proteins", own),
            ("this thesis's corpus, food and food-adjacent",
             own[own.is_therapeutic != "yes"]),
            ("this thesis's corpus, dairy/egg/haem only",
             own[own.accession.isin(DAIRY_EGG_HAEM)])):
        g = sub.groupby("accession").agg(y=("log_titer", "max"),
                                         dm=("disorder_mean", "first"))
        if len(g) < 5:
            continue
        rho, p = stats.spearmanr(g.dm, g.y)
        rows.append({"test": label, "n_proteins": len(g),
                     "spearman_rho": float(rho), "p_value": float(p)})
        if label.endswith("dairy/egg/haem only"):
            gg = g[g.dm < 0.2]
            rho, p = stats.spearmanr(gg.dm, gg.y)
            rows.append({"test": "  GLOBULAR ONLY (mean disorder < 0.2)",
                         "n_proteins": len(gg), "spearman_rho": float(rho),
                         "p_value": float(p)})

    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "disorder_replication.csv", index=False)
    print(f"{'test':<60}{'n':>4}{'rho':>9}{'p':>10}")
    for r in out.itertuples():
        print(f"{r.test:<60}{r.n_proteins:>4}{r.spearman_rho:>+9.3f}"
              f"{r.p_value:>10.4f}")


if __name__ == "__main__":
    main()
