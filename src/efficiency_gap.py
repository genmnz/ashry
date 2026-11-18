"""
How far is each published titre from the stoichiometric ceiling of the very
protein that was produced?

A reported titre in g/L is not comparable to a yield in g/g until you say how much
substrate the fermentation was fed. Published fed-batch processes for K. phaffii
feed of order 150-500 g of glycerol plus methanol per litre of final broth, so

    ceiling [g/L] = substrate_loading [g/L] * Y_poly [g/g]

and the measured quantity is titre / ceiling: the fraction of its own protein's
stoichiometric limit that a process reached. Because the loading is uncertain it
is scanned and the answer is reported as a band.

Three rules keep the comparison honest:

* The ceiling is computed for the **exact protein of the record**, from its own
  accession and sequence, not for a same-named relative. Human alpha-lactalbumin
  and bovine alpha-lactalbumin are different molecules and get different ceilings.
* Only hosts this analysis can speak about are included: K. phaffii / P. pastoris,
  plus T. reesei records, which are flagged because the model is a yeast model.
* Fragments and fusions are excluded (see corpus.py), because the titre of a
  casein macropeptide is not the titre of a casein.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from corpus import drop_fragments
from producibility import count_disulfides_unknown, sequence_library
from protein_cost import ProteinSpec, load_model, yield_analysis

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"

SUBSTRATE_LOADINGS = (150.0, 250.0, 350.0, 500.0)
CENTRAL_LOADING = 350.0


def annotations() -> dict[str, dict]:
    path = REPO / "data" / "sequences" / "targets_metadata.json"
    out: dict[str, dict] = {}
    if path.exists():
        for m in json.loads(path.read_text()):
            out[m["accession"]] = {
                "disulfide_bonds": m["disulfide_bonds"],
                "n_glyc_sites_annotated": m["n_glyc_sites_annotated"],
                "phosphoserines": m["phosphoserines"],
                "haem_per_chain": m["haem_per_chain"],
                "category": m["category"],
                "display_name": m["display_name"],
            }
    return out


def main() -> None:
    lib = sequence_library()
    ann = annotations()
    base = load_model()

    titres = pd.read_csv(REPO / "data" / "literature" / "titers_host_panel.csv")
    titres, dropped = drop_fragments(titres)
    titres = titres[titres.confidence == "high"]
    titres = titres[titres.titer_mg_L.notna() & (titres.titer_mg_L > 0)]
    titres["accession"] = titres.uniprot_accession.astype(str).str.strip()
    titres = titres[titres.host.astype(str).str.contains(
        "phaffii|pastoris|reesei", case=False)]
    matched = titres[titres.accession.isin(lib)].copy()

    print(f"corpus: {len(dropped)} fragment/fusion records excluded; "
          f"{len(titres)} high-confidence in-host records; "
          f"{len(matched)} with a verified sequence "
          f"({matched.accession.nunique()} distinct proteins)")

    ceilings: dict[str, dict] = {}
    for acc in sorted(matched.accession.unique()):
        seq = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "", lib[acc].upper())
        a = ann.get(acc, {})
        ss = a.get("disulfide_bonds")
        ss = count_disulfides_unknown(seq) if ss is None else ss
        spec = ProteinSpec(
            name=acc, sequence=seq, accession=acc,
            disulfide_bonds=int(ss),
            n_glycosylation_sites=a.get("n_glyc_sites_annotated"),
            phosphoserines=int(a.get("phosphoserines", 0)),
            haem_per_chain=int(a.get("haem_per_chain", 0)))
        r = yield_analysis(spec, substrate="glycerol", model=base)
        ceilings[acc] = {
            "y_poly": r.get("g_polypeptide_per_g_substrate", float("nan")),
            "length": len(seq),
            "disulfides": int(ss),
            "sequons": spec.sequons(),
        }

    rows = []
    for _, r in matched.iterrows():
        c = ceilings[r.accession]
        titre = float(r.titer_mg_L) / 1000.0
        for loading in SUBSTRATE_LOADINGS:
            ceiling = loading * c["y_poly"]
            rows.append({
                "accession": r.accession,
                "protein_name": r.protein_name,
                "display_name": ann.get(r.accession, {}).get("display_name", ""),
                "host": r.host,
                "cultivation_mode": r.cultivation_mode,
                "year": r.year,
                "doi_or_url": r.doi_or_url,
                "titer_g_L": titre,
                "length": c["length"],
                "disulfides": c["disulfides"],
                "sequons": c["sequons"],
                "theoretical_yield_g_per_g": c["y_poly"],
                "substrate_loading_g_L": loading,
                "ceiling_g_L": ceiling,
                "fraction_of_ceiling": titre / ceiling,
                "gap_fold": ceiling / titre if titre else float("nan"),
            })

    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "efficiency_gap.csv", index=False)

    central = out[out.substrate_loading_g_L == CENTRAL_LOADING]
    best = (central.sort_values("titer_g_L", ascending=False)
            .groupby("accession").head(1)
            .sort_values("fraction_of_ceiling", ascending=False))
    best.to_csv(TABLES / "efficiency_gap_best.csv", index=False)

    summary = {
        "central_loading_g_L": CENTRAL_LOADING,
        "loadings_scanned": list(SUBSTRATE_LOADINGS),
        "n_records": int(len(matched)),
        "n_proteins": int(matched.accession.nunique()),
        "ceiling_span_fold": float(best.theoretical_yield_g_per_g.max()
                                   / best.theoretical_yield_g_per_g.min()),
        "fraction_span_fold": float(best.fraction_of_ceiling.max()
                                    / best.fraction_of_ceiling.min()),
        "best": {"protein": str(best.iloc[0].protein_name),
                 "fraction_of_ceiling": float(best.iloc[0].fraction_of_ceiling)},
        "worst": {"protein": str(best.iloc[-1].protein_name),
                  "fraction_of_ceiling": float(best.iloc[-1].fraction_of_ceiling)},
    }
    (TABLES / "efficiency_gap_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"\nceiling spans {summary['ceiling_span_fold']:.2f}x; "
          f"fraction of ceiling spans {summary['fraction_span_fold']:.0f}x\n")
    print(f"{'protein':<44}{'titre':>9}{'Ymax':>7}{'ceil':>7}{'% ceil':>8}{'gap':>8}")
    for r in best.itertuples():
        print(f"{str(r.protein_name)[:43]:<44}{r.titer_g_L:>8.2f}"
              f"{r.theoretical_yield_g_per_g:>7.3f}{r.ceiling_g_L:>7.0f}"
              f"{100 * r.fraction_of_ceiling:>7.2f}%{r.gap_fold:>7.0f}x")


if __name__ == "__main__":
    main()
