#!/usr/bin/env python3
"""The ceiling-gap analysis.

For each protein in the curated panel:

  1. compute the maximum theoretical secretion yield Y_max in g protein per g
     substrate, from the balanced synthesis reaction in iMT1026v3;
  2. convert it to a ceiling titer under a standardised feed, because almost
     no publication reports total substrate consumed, so a yield cannot be
     compared with a titer directly;
  3. take the highest defensible measured titer for that protein from the
     merged corpus;
  4. report ceiling utilisation = measured titer / ceiling titer.

The standardised feed is stated explicitly rather than fitted: 100 g/L of
glycerol-equivalent substrate, which is the order of magnitude of a
conventional K. phaffii fed-batch. Utilisation is therefore a *relative*
quantity whose absolute value scales with that assumption; what the analysis
turns on is the ratio between proteins, which is independent of it.

The point of the analysis is the comparison between two spreads:
  * how much the ceilings differ between proteins (little), versus
  * how much the utilisations differ between proteins (enormously).
If the first spread is small and the second is large, metabolic stoichiometry
cannot be what limits these processes, and the limitation has to be sought in
folding and secretion instead.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protein_cost import (AA_MET, CostParams, ProteinSpec, build_reactions,  # noqa: E402
                          compute_cost, count_sequons)
from yields import SUBSTRATES, load_model, max_yield  # noqa: E402

LIT = os.path.join(ROOT, "data", "literature")
SEQ = os.path.join(ROOT, "data", "sequences")
EXT = os.path.join(ROOT, "data", "external")
RES = os.path.join(ROOT, "results", "tables")

STANDARD_FEED_G_PER_L = 100.0

# map the curated panel onto the protein_canonical labels in the corpus
CORPUS_LABEL = {
    "beta_lactoglobulin_bovine": "beta-lactoglobulin",
    "alpha_lactalbumin_bovine": "alpha-lactalbumin",
    "alpha_lactalbumin_human": "alpha-lactalbumin",
    "alpha_s1_casein_bovine": "alpha-s1-casein",
    "alpha_s2_casein_bovine": "alpha-s2-casein",
    "beta_casein_bovine": "beta-casein",
    "kappa_casein_bovine": "kappa-casein",
    "lactoferrin_bovine": "lactoferrin",
    "lactoferrin_human": "lactoferrin",
    "osteopontin_bovine": "osteopontin",
    "ovalbumin_chicken": "ovalbumin",
    "ovotransferrin_chicken": "ovotransferrin",
    "ovomucoid_chicken": "ovomucoid",
    "lysozyme_c_chicken": "lysozyme",
    "avidin_chicken": "avidin",
    "leghemoglobin_lbc2_soybean": "leghemoglobin",
    "myoglobin_pig": "myoglobin",
    "serum_albumin_human": "serum albumin",
    "chymosin_bovine": "chymosin",
    "cbhi_cel7a_trichoderma": "cellobiohydrolase I",
}

HOSTS_OF_INTEREST = ("Komagataella phaffii", "Trichoderma reesei")


def load_panel():
    path = os.path.join(SEQ, "panel_curated.tsv")
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out.append(r)
    return out


def load_uniprot(acc):
    with open(os.path.join(EXT, "uniprot", f"{acc}.json")) as fh:
        return json.load(fh)


def spec_from_curated(row):
    d = load_uniprot(row["accession"])
    seq = d["sequence"]["value"]
    feats = d.get("features", [])
    sig = [f for f in feats if f["type"] == "Signal"]
    sp_end = sig[0]["location"]["end"]["value"] if sig else 0
    secreted = row["secreted"].strip().lower() == "yes"
    req = row["ptm_required"]
    n_ss = sum(1 for f in feats if f["type"] == "Disulfide bond")
    n_phos = sum(1 for f in feats if f["type"] == "Modified residue"
                 and "Phospho" in (f.get("description") or ""))
    n_oglyc = sum(1 for f in feats if f["type"] == "Glycosylation"
                  and (f.get("description") or "").startswith("O-linked"))
    # only count a PTM as required if the curation says so
    if "phosphorylation" not in req:
        n_phos = 0
    if "O-glycosylation" not in req:
        n_oglyc = 0
    return ProteinSpec(
        name=row["name"], sequence=seq, signal_end=sp_end,
        n_disulfide=n_ss, n_o_glyc_site=n_oglyc, n_phosphosite=n_phos,
        n_haem=int(row["haem"]), accession=row["accession"],
        secreted=secreted, notes=row["category"])


def best_measured(corpus_label):
    """Highest defensible titer for a protein, per host, from the corpus."""
    path = os.path.join(LIT, "titers_merged.tsv")
    best = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("protein_canonical") != corpus_label:
                continue
            host = r.get("host_canonical")
            if host not in HOSTS_OF_INTEREST:
                continue
            if (r.get("confidence") or "").lower() == "low":
                continue
            if (r.get("is_fragment") or "").lower() == "yes":
                continue
            name = (r.get("protein_name") or "").lower()
            if re.search(r"macropeptide|fragment|\bn-?lobe\b|\bc-?lobe\b|"
                         r"domain ?3|peptide\b", name):
                continue
            # a number that measured the target, not total broth protein
            if r.get("titer_basis") == "total_secreted_protein":
                continue
            try:
                t = float(str(r["titer_mg_L"]).replace(",", "")
                          .replace(">", "").strip())
            except (ValueError, KeyError, TypeError):
                continue
            cur = best.get(host)
            if cur is None or t > cur["titer_mg_L"]:
                best[host] = {
                    "titer_mg_L": t,
                    "localisation": r.get("localisation"),
                    "cultivation": r.get("cultivation"),
                    "reference": r.get("reference"),
                    "doi": r.get("doi"),
                    "confidence": r.get("confidence"),
                    "record_id": r.get("record_id"),
                    "evidence_quote": (r.get("evidence_quote") or "")[:200],
                }
    return best


def main():
    os.makedirs(RES, exist_ok=True)
    model = load_model()
    panel = load_panel()
    params = CostParams()

    rows = []
    for row in panel:
        spec = spec_from_curated(row)
        cost = compute_cost(spec, params)
        ys = {}
        for sub in ("glycerol", "methanol", "glyc_meoh", "glucose"):
            r = max_yield(model, spec, params, sub, mu=0.0)
            ys[sub] = r["Y_g_per_g"] if r else None
        measured = best_measured(CORPUS_LABEL.get(row["name"], ""))
        base = {
            "protein": row["name"],
            "accession": row["accession"],
            "category": row["category"],
            "secreted": row["secreted"],
            "ptm_required": row["ptm_required"],
            "length_mature": cost.length_mature,
            "mass_kda": round(cost.product_mass_da / 1000.0, 3),
            "n_disulfide": int(cost.breakdown["n_disulfide"]),
            "n_sequon": int(cost.breakdown["n_sequon"]),
            "n_phosphosite": int(spec.n_phosphosite),
            "n_haem": int(cost.haem),
            "atp_per_mol": round(cost.atp, 1),
            "atp_per_g": round(cost.atp_per_g, 2),
            "Y_max_glycerol_g_per_g": round(ys["glycerol"], 4),
            "Y_max_methanol_g_per_g": round(ys["methanol"], 4),
            "Y_max_glyc_meoh_g_per_g": round(ys["glyc_meoh"], 4),
            "Y_max_glucose_g_per_g": round(ys["glucose"], 4),
            "ceiling_titer_g_per_L_glycerol":
                round(ys["glycerol"] * STANDARD_FEED_G_PER_L, 2),
        }
        if not measured:
            r = dict(base)
            r.update({"host": "", "measured_titer_mg_L": "",
                      "ceiling_utilisation": "", "gap_fold": "",
                      "reference": "", "doi": "", "confidence": "",
                      "localisation": "", "cultivation": "",
                      "evidence_quote": "",
                      "note": "no measured titer in the corpus for this host set"})
            rows.append(r)
            continue
        for host, m in measured.items():
            ceil_mg = base["ceiling_titer_g_per_L_glycerol"] * 1000.0
            util = m["titer_mg_L"] / ceil_mg
            r = dict(base)
            r.update({
                "host": host,
                "measured_titer_mg_L": m["titer_mg_L"],
                "ceiling_utilisation": round(util, 6),
                "gap_fold": round(1.0 / util, 1) if util > 0 else "",
                "reference": m["reference"],
                "doi": m["doi"],
                "confidence": m["confidence"],
                "localisation": m["localisation"],
                "cultivation": m["cultivation"],
                "evidence_quote": m["evidence_quote"],
                "note": "",
            })
            rows.append(r)

    cols = list(rows[0].keys())
    out = os.path.join(RES, "ceiling_gap.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # headline comparison
    ceil = [r["Y_max_glycerol_g_per_g"] for r in rows]
    utils = [(r["protein"], r["host"], r["ceiling_utilisation"])
             for r in rows if r["ceiling_utilisation"] != ""]
    print(f"wrote {out}  ({len(rows)} rows)\n")
    print(f"Ceiling Y_max on glycerol: min {min(ceil):.3f}  "
          f"max {max(ceil):.3f}  spread {max(ceil)/min(ceil):.2f}x")
    if utils:
        vals = [u for _, _, u in utils if u > 0]
        print(f"Ceiling utilisation:       min {min(vals):.5f}  "
              f"max {max(vals):.5f}  spread {max(vals)/min(vals):.0f}x\n")
        print(f"{'protein':34s} {'host':24s} {'Ymax':>6s} {'ceil g/L':>9s} "
              f"{'measured mg/L':>14s} {'util':>9s}")
        for r in sorted(rows, key=lambda r: -(r["ceiling_utilisation"] or 0)
                        if r["ceiling_utilisation"] != "" else 1):
            if r["ceiling_utilisation"] == "":
                continue
            print(f"{r['protein']:34s} {r['host']:24s} "
                  f"{r['Y_max_glycerol_g_per_g']:6.3f} "
                  f"{r['ceiling_titer_g_per_L_glycerol']:9.1f} "
                  f"{r['measured_titer_mg_L']:14.1f} "
                  f"{100*r['ceiling_utilisation']:8.3f}%")


if __name__ == "__main__":
    main()
