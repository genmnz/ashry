#!/usr/bin/env python3
"""Stoichiometric ceilings for every accession held, not only the curated panel.

Two reasons to widen the panel beyond the twenty curated food proteins.

First, the questions that decide the paper's headline cannot be answered on
food proteins alone. Refitting inside the food subset needs a therapeutic
subset to contrast it with, and testing sensitivity to collagen needs collagen
in the table.

Second, and more important, keying on the UniProt accession rather than on a
canonical name plus species lets a protein appear many times. Human
interferon alpha-2b has thirteen secreted records in T. reesei alone, and
type III collagen has five in K. phaffii. A panel keyed on one best titer per
protein throws that away, and it is exactly the information needed to ask
whether the spread in realised production is between proteins at all, or
within them.

PTM assumptions for the sixteen accessions that are not in the curated panel:
disulfides and N-glycosylation sequons are charged as UniProt annotates them,
and no phosphorylation or O-glycosylation is charged. This is deliberately the
cheap end. None of these proteins is a casein, so none depends on
phosphorylation for function, and charging a PTM that the process does not
require would understate the ceiling and so overstate the gap, which is the
direction that would flatter the paper's claim.

Output
  results/tables/ceilings_by_accession.csv
"""
from __future__ import annotations

import csv
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protein_cost import CostParams, ProteinSpec, compute_cost  # noqa: E402
from uniprot_features import annotation  # noqa: E402
from yields import load_model, max_yield  # noqa: E402

UNI = os.path.join(ROOT, "data", "external", "uniprot")
SEQ = os.path.join(ROOT, "data", "sequences")
RES = os.path.join(ROOT, "results", "tables")
STANDARD_FEED_G_PER_L = 100.0


def panel_rows():
    with open(os.path.join(SEQ, "panel_curated.tsv"), newline="") as fh:
        return {r["accession"]: r for r in csv.DictReader(fh, delimiter="\t")}


def spec_for(acc, prow):
    a = annotation(acc)
    with open(os.path.join(UNI, f"{acc}.json")) as fh:
        d = json.load(fh)
    seq = d["sequence"]["value"]
    if a["mature_end"] != a["length_precursor"]:
        seq = seq[:a["mature_end"]]
    if prow is not None:
        req = prow["ptm_required"]
        n_phos = a["n_phosphosite"] if "phosphorylation" in req else 0
        n_oglyc = a["n_o_glyc_site"] if "O-glycosylation" in req else 0
        haem = int(prow["haem"])
        secreted = prow["secreted"].strip().lower() == "yes"
        name, cat = prow["name"], prow["category"]
    else:
        n_phos = n_oglyc = haem = 0
        secreted = True
        name = (d.get("uniProtkbId") or acc).lower()
        cat = "extended"
    return ProteinSpec(
        name=name, sequence=seq, signal_end=a["mature_start"] - 1,
        n_disulfide=a["n_disulfide"], n_o_glyc_site=n_oglyc,
        n_phosphosite=n_phos, n_sequon=a["n_glyc_site"], n_haem=haem,
        accession=acc, secreted=secreted, notes=cat), cat, d


def main():
    os.makedirs(RES, exist_ok=True)
    model = load_model()
    params = CostParams()
    panel = panel_rows()
    accs = sorted(f[:-5] for f in os.listdir(UNI) if f.endswith(".json"))

    rows = []
    for acc in accs:
        spec, cat, d = spec_for(acc, panel.get(acc))
        cost = compute_cost(spec, params)
        ys = {}
        for sub in ("glycerol", "methanol", "glyc_meoh", "glucose"):
            r = max_yield(model, spec, params, sub, mu=0.0)
            ys[sub] = r["Y_g_per_g"] if r else None
        rows.append({
            "accession": acc,
            "uniprot_id": d.get("uniProtkbId"),
            "protein": spec.name,
            "organism": d.get("organism", {}).get("scientificName"),
            "category": cat,
            "in_curated_panel": "yes" if acc in panel else "no",
            "length_mature": cost.length_mature,
            "mass_kda": round(cost.product_mass_da / 1000.0, 3),
            "n_disulfide": int(cost.breakdown["n_disulfide"]),
            "n_sequon": int(cost.breakdown["n_sequon"]),
            "n_phosphosite": int(spec.n_phosphosite),
            "n_o_glyc_site": int(spec.n_o_glyc_site),
            "n_haem": int(cost.haem),
            "atp_per_mol": round(cost.atp, 1),
            "atp_per_g": round(cost.atp_per_g, 2),
            "Y_max_glycerol_g_per_g": round(ys["glycerol"], 4),
            "Y_max_methanol_g_per_g": round(ys["methanol"], 4),
            "Y_max_glyc_meoh_g_per_g": round(ys["glyc_meoh"], 4),
            "Y_max_glucose_g_per_g": round(ys["glucose"], 4),
            "ceiling_titer_mg_L_glycerol":
                round(ys["glycerol"] * STANDARD_FEED_G_PER_L * 1000.0, 1),
        })

    out = os.path.join(RES, "ceilings_by_accession.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    ys = [r["Y_max_glycerol_g_per_g"] for r in rows]
    print(f"wrote {out}  ({len(rows)} accessions)")
    print(f"Y_max on glycerol: min {min(ys):.3f}  max {max(ys):.3f}  "
          f"spread {max(ys)/min(ys):.2f}x")
    for r in sorted(rows, key=lambda r: r["Y_max_glycerol_g_per_g"]):
        print(f"  {r['accession']:8s} {str(r['uniprot_id']):16s} "
              f"{r['Y_max_glycerol_g_per_g']:.3f}  "
              f"SS {r['n_disulfide']:2d}  Nglyc {r['n_sequon']:2d}  "
              f"L {r['length_mature']:4d}  {r['category']}")


if __name__ == "__main__":
    main()
