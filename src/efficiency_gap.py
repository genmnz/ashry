"""
How far is the best published titre from the stoichiometric ceiling?

A reported titre in g/L is not comparable to a yield in g/g until you say how much
substrate the fermentation was fed. Published fed-batch processes for K. phaffii
feed on the order of 150-500 g of glycerol plus methanol per litre of final broth,
so the ceiling for a protein with maximum theoretical yield Y is

    ceiling [g/L] = substrate_loading [g/L] * Y [g/g]

and the fraction of the ceiling actually reached is titre / ceiling. Because the
loading is uncertain it is scanned, and the result is reported as a band rather
than a point.

This is the number that decides what the rest of the thesis is about: if titres
were already at 60-80% of the ceiling, the field's problem would be biochemistry
and feedstock. They are not, by well over an order of magnitude, so the problem is
expression, folding, secretion and recovery.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"

# how a protein_name in the titre database maps onto a panel protein
NAME_PATTERNS = {
    "beta_lactoglobulin": r"lactoglobulin|\bBLG\b",
    "alpha_lactalbumin": r"lactalbumin",
    "ovalbumin": r"ovalbumin|OVA\b",
    "leghemoglobin_c2": r"leghemoglobin|LegH|LBA\b",
    "lactoferrin_bovine": r"lactoferrin|lactotransferrin",
    "beta_casein": r"beta-casein|\bbeta casein",
    "kappa_casein": r"kappa-casein|casein macropeptide|\bCMP\b",
    "alpha_s1_casein": r"alpha-s1|alpha-S1",
    "alpha_s2_casein": r"alpha-s2|alpha-S2",
}

SUBSTRATE_LOADINGS = (150.0, 250.0, 350.0, 500.0)


def map_protein(name: str) -> str | None:
    for key, pat in NAME_PATTERNS.items():
        if re.search(pat, str(name), re.I):
            return key
    return None


def main() -> None:
    yields = pd.read_csv(TABLES / "protein_yields.csv")
    y = yields[(yields.substrate == "glycerol") & (yields.charge_ptms)
               & (yields.atp_per_bond == 4.3)
               & (yields.get("mannose_per_glycan", 9.0) == 9.0)]
    ymax = dict(zip(y.protein, y.g_protein_per_g_substrate))

    titres = pd.read_csv(REPO / "data" / "literature" / "titers_host_panel.csv")
    titres["panel_protein"] = titres.protein_name.map(map_protein)
    titres = titres[titres.panel_protein.notna() & titres.titer_mg_L.notna()]
    titres = titres[titres.confidence == "high"]

    rows = []
    for _, r in titres.iterrows():
        key = r.panel_protein
        if key not in ymax:
            continue
        titre_g_L = float(r.titer_mg_L) / 1000.0
        for loading in SUBSTRATE_LOADINGS:
            ceiling = loading * ymax[key]
            rows.append({
                "protein": key,
                "protein_name_reported": r.protein_name,
                "host": r.host,
                "cultivation_mode": r.cultivation_mode,
                "year": r.year,
                "doi_or_url": r.doi_or_url,
                "titer_g_L": titre_g_L,
                "substrate_loading_g_L": loading,
                "theoretical_yield_g_per_g": ymax[key],
                "ceiling_g_L": ceiling,
                "fraction_of_ceiling": titre_g_L / ceiling,
                "gap_fold": ceiling / titre_g_L if titre_g_L else float("nan"),
            })

    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "efficiency_gap.csv", index=False)

    best = (out[out.substrate_loading_g_L == 350.0]
            .sort_values("titer_g_L", ascending=False)
            .groupby("protein").head(1)
            .sort_values("fraction_of_ceiling", ascending=False))

    summary = {
        "substrate_loading_scanned_g_L": list(SUBSTRATE_LOADINGS),
        "n_titre_rows_used": int(len(titres)),
        "best_per_protein_at_350gL": [
            {"protein": r.protein, "best_titer_g_L": r.titer_g_L,
             "ceiling_g_L": round(r.ceiling_g_L, 1),
             "fraction_of_ceiling": round(r.fraction_of_ceiling, 4),
             "gap_fold": round(r.gap_fold, 1),
             "source": r.doi_or_url}
            for r in best.itertuples()],
    }
    (TABLES / "efficiency_gap_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"{'protein':<22}{'best titre':>12}{'ceiling':>10}{'% of ceiling':>14}{'gap':>8}")
    for r in best.itertuples():
        print(f"{r.protein:<22}{r.titer_g_L:>10.2f} g/L{r.ceiling_g_L:>9.0f}"
              f"{100 * r.fraction_of_ceiling:>13.1f}%{r.gap_fold:>7.0f}x")


if __name__ == "__main__":
    main()
