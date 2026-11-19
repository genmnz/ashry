"""
Is carbon really the binding bound, or is the process oxygen-limited first?

Chapter 5 measures every titre against a carbon ceiling. If real fermentations hit
an oxygen-transfer wall long before they run out of carbon, then that comparison
is against the wrong bound and the measured gap is partly an artefact.

This script computes the alternative. At the carbon-limited optimum the model
already reports the oxygen consumed per gram of product (about 10 mmol/g, nearly
invariant across the panel). An aerated vessel can deliver oxygen at a maximum
volumetric transfer rate OTR, so the oxygen-limited ceiling over a batch of
duration t is

    ceiling_O2 [g/L] = OTR [mmol/L/h] * t [h] / (O2 demand [mmol/g])

This is deliberately generous: it spends the entire oxygen budget on product and
none on growth or maintenance, which no real process can do. If even this generous
oxygen bound sits above the carbon bound, then carbon is the tighter of the two
and Chapter 5's denominator is the right one.

OTR values are scanned rather than assumed, covering the range from a modestly
aerated large vessel to an aggressively sparged one.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"

OTR_SCAN = (50.0, 100.0, 200.0, 300.0)   # mmol O2 per litre per hour
# Ammonium nitrogen actually supplied. A batch medium for this host carries a few
# grams of nitrogen per litre; a fed-batch adds ammonia continuously as the pH
# titrant, which is why the upper end of this scan is far above any batch recipe.
N_SCAN_G_PER_L = (2.0, 5.0, 10.0, 30.0, 60.0)
BATCH_HOURS = 90.0
# Phosphate actually supplied. Basal salts medium for this host is built on
# phosphoric acid: the standard recipe carries 26.7 mL/L of 85% H3PO4, which is
# about 7.3 g of phosphorus per litre. The scan brackets that from a
# phosphate-poor medium upwards.
P_SCAN_G_PER_L = (0.5, 1.0, 2.0, 5.0, 7.3)
# Heat of reaction per mole of oxygen consumed. Aerobic catabolism releases a
# nearly substrate-independent 440-490 kJ per mole of O2 (the oxycalorific
# equivalent), which is why oxygen uptake is the standard proxy for fermenter
# heat load.
KJ_PER_MOL_O2 = 460.0
# Volumetric heat-removal capacity. A jacketed vessel with internal coils at
# production scale manages roughly 5-20 kW per cubic metre; the scan runs from
# a cooling-poor large vessel to a well-equipped one.
COOLING_SCAN_KW_PER_M3 = (5.0, 10.0, 20.0, 40.0)
CARBON_LOADING = 350.0                    # g/L, the central case of Chapter 5


def main() -> None:
    meta = {m["key"]: m for m in json.loads(
        (REPO / "data" / "sequences" / "targets_metadata.json").read_text())}
    y = pd.read_csv(TABLES / "protein_yields.csv")
    y = y[(y.substrate == "glycerol") & (y.charge_ptms)
          & (y.atp_per_bond == 4.3)]
    if "mannose_per_glycan" in y.columns:
        y = y[y.mannose_per_glycan == 9.0]

    rows = []
    for r in y.itertuples():
        o2 = float(r.o2_mmol_per_g_protein)
        carbon_ceiling = CARBON_LOADING * float(r.g_polypeptide_per_g_substrate)
        for otr in OTR_SCAN:
            o2_ceiling = otr * BATCH_HOURS / o2
            rows.append({
                "protein": r.protein,
                "o2_mmol_per_g_protein": o2,
                "otr_mmol_L_h": otr,
                "batch_h": BATCH_HOURS,
                "oxygen_ceiling_g_L": o2_ceiling,
                "carbon_ceiling_g_L": carbon_ceiling,
                "binding_bound": "oxygen" if o2_ceiling < carbon_ceiling else "carbon",
                "ratio_o2_to_carbon": o2_ceiling / carbon_ceiling,
            })

    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "oxygen_ceiling.csv", index=False)

    # nitrogen bound: protein is roughly 16% nitrogen by mass, computed here
    # exactly from each protein's elemental composition
    comp = pd.read_csv(TABLES / "target_composition.csv")
    n_rows = []
    for c in comp.itertuples():
        n_mass_frac = c.N * 14.007 / (c.mw_kda * 1000.0)
        carbon_ceiling = CARBON_LOADING * float(
            y[y.protein == c.protein].g_polypeptide_per_g_substrate.iloc[0])
        for n_supply in N_SCAN_G_PER_L:
            n_rows.append({
                "protein": c.protein,
                "nitrogen_mass_fraction": n_mass_frac,
                "nitrogen_supplied_g_L": n_supply,
                "nitrogen_ceiling_g_L": n_supply / n_mass_frac,
                "carbon_ceiling_g_L": carbon_ceiling,
                "binding_bound": "nitrogen" if n_supply / n_mass_frac < carbon_ceiling
                else "carbon",
            })
    n_df = pd.DataFrame(n_rows)
    n_df.to_csv(TABLES / "nitrogen_ceiling.csv", index=False)
    print("\nnitrogen content of the panel: "
          f"{100 * n_df.nitrogen_mass_fraction.min():.1f}-"
          f"{100 * n_df.nitrogen_mass_fraction.max():.1f}% by mass")
    print(n_df.pivot_table(index="protein", columns="nitrogen_supplied_g_L",
                           values="nitrogen_ceiling_g_L").round(0).to_string())
    binds = n_df[n_df.binding_bound == "nitrogen"]
    print(f"nitrogen binds before carbon in {len(binds)} of {len(n_df)} cases; "
          f"it stops binding above about "
          f"{binds.nitrogen_supplied_g_L.max() if len(binds) else 0:.0f} g N/L")

    # ------------------------------------------------------------------
    # Phosphate bound. Phosphorus enters the *product* only as phosphoserine,
    # one phosphorus per site. ATP turnover consumes no net phosphate, since the
    # phosphate is recycled, so the product's own phosphorus content is the
    # right quantity for a product-level bound. For the unphosphorylated
    # proteins the bound does not exist, which is itself the result: phosphate
    # can only ever bind on the caseins.
    p_rows = []
    for c in comp.itertuples():
        y_poly = float(y[y.protein == c.protein].g_polypeptide_per_g_substrate.iloc[0])
        carbon_ceiling = CARBON_LOADING * y_poly
        meta_row = meta.get(c.protein, {})
        n_pser = int(meta_row.get("phosphoserines", 0))
        p_mass_frac = n_pser * 30.9738 / (c.mw_kda * 1000.0)
        for p_supply in P_SCAN_G_PER_L:
            ceiling = (p_supply / p_mass_frac) if p_mass_frac > 0 else float("inf")
            p_rows.append({
                "protein": c.protein,
                "phosphoserines": n_pser,
                "phosphorus_mass_fraction": p_mass_frac,
                "phosphorus_supplied_g_L": p_supply,
                "phosphate_ceiling_g_L": ceiling,
                "carbon_ceiling_g_L": carbon_ceiling,
                "binding_bound": "phosphate" if ceiling < carbon_ceiling else "carbon",
            })
    p_df = pd.DataFrame(p_rows)
    p_df.to_csv(TABLES / "phosphate_ceiling.csv", index=False)
    phos = p_df[p_df.phosphoserines > 0]
    print("\nphosphorus content of the phosphorylated proteins: "
          f"{100 * phos.phosphorus_mass_fraction.min():.2f}-"
          f"{100 * phos.phosphorus_mass_fraction.max():.2f}% by mass "
          f"({phos.protein.nunique()} of {p_df.protein.nunique()} panel proteins "
          "carry any phosphorus at all)")
    print(phos.pivot_table(index="protein", columns="phosphorus_supplied_g_L",
                           values="phosphate_ceiling_g_L").round(0).to_string())
    binds = p_df[p_df.binding_bound == "phosphate"]
    print(f"phosphate binds before carbon in {len(binds)} of {len(p_df)} cases"
          + (f"; the highest supply at which it still binds is "
             f"{binds.phosphorus_supplied_g_L.max():.1f} g P/L" if len(binds) else ""))

    # ------------------------------------------------------------------
    # Heat-removal bound. Oxygen uptake is the standard proxy for fermenter heat
    # load, at a nearly substrate-independent 460 kJ per mole of O2. This counts
    # only the oxygen drawn by product synthesis and so UNDERSTATES the heat a
    # real process must remove, which means it OVERSTATES this ceiling. Unlike
    # the oxygen and nitrogen bounds, therefore, this one is generous in the
    # unhelpful direction and is reported as an upper bound on an upper bound.
    h_rows = []
    for r in y.itertuples():
        o2 = float(r.o2_mmol_per_g_protein)
        kj_per_g = o2 * KJ_PER_MOL_O2 / 1000.0
        carbon_ceiling = CARBON_LOADING * float(r.g_polypeptide_per_g_substrate)
        for kw in COOLING_SCAN_KW_PER_M3:
            # kW/m3 * h -> kWh/m3; 1 kWh = 3600 kJ; per m3 -> per litre / 1000
            kj_per_L = kw * BATCH_HOURS * 3600.0 / 1000.0
            ceiling = kj_per_L / kj_per_g
            h_rows.append({
                "protein": r.protein,
                "kj_per_g_product": kj_per_g,
                "cooling_kW_per_m3": kw,
                "batch_h": BATCH_HOURS,
                "heat_ceiling_g_L": ceiling,
                "carbon_ceiling_g_L": carbon_ceiling,
                "binding_bound": "heat" if ceiling < carbon_ceiling else "carbon",
                "ratio_heat_to_carbon": ceiling / carbon_ceiling,
            })
    h_df = pd.DataFrame(h_rows)
    h_df.to_csv(TABLES / "heat_ceiling.csv", index=False)
    print(f"\nheat of reaction attributable to product synthesis: "
          f"{h_df.kj_per_g_product.min():.1f}-{h_df.kj_per_g_product.max():.1f} "
          "kJ per gram of product")
    print("heat-limited ceiling (g/L) over a 90 h batch:")
    print(h_df.pivot_table(index="protein", columns="cooling_kW_per_m3",
                           values="heat_ceiling_g_L").round(0).to_string())
    hb = h_df[h_df.binding_bound == "heat"]
    print(f"heat binds before carbon in {len(hb)} of {len(h_df)} cases; "
          f"the tightest heat bound is "
          f"{h_df.ratio_heat_to_carbon.min():.2f}x the carbon bound")

    summary_extra = {
        "phosphorus_mass_fraction_range_phosphorylated": [
            float(phos.phosphorus_mass_fraction.min()),
            float(phos.phosphorus_mass_fraction.max())],
        "phosphate_scanned_g_L": list(P_SCAN_G_PER_L),
        "phosphate_binds_in_n_cases": int(len(binds)),
        "cooling_scanned_kW_per_m3": list(COOLING_SCAN_KW_PER_M3),
        "kj_per_mol_o2": KJ_PER_MOL_O2,
        "kj_per_g_product_range": [float(h_df.kj_per_g_product.min()),
                                   float(h_df.kj_per_g_product.max())],
        "heat_binds_in_n_cases": int(len(hb)),
        "min_ratio_heat_to_carbon": float(h_df.ratio_heat_to_carbon.min()),
    }

    piv = out.pivot_table(index="protein", columns="otr_mmol_L_h",
                          values="oxygen_ceiling_g_L")
    summary = {
        "batch_hours": BATCH_HOURS,
        "otr_scanned_mmol_L_h": list(OTR_SCAN),
        "carbon_loading_g_L": CARBON_LOADING,
        "o2_demand_range_mmol_per_g": [float(out.o2_mmol_per_g_protein.min()),
                                       float(out.o2_mmol_per_g_protein.max())],
        "oxygen_binds_in_n_cases": int((out.binding_bound == "oxygen").sum()),
        "total_cases": int(len(out)),
        "min_ratio_o2_to_carbon": float(out.ratio_o2_to_carbon.min()),
    }
    summary.update(summary_extra)
    (TABLES / "oxygen_ceiling_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"oxygen demand per gram of product: "
          f"{summary['o2_demand_range_mmol_per_g'][0]:.1f}-"
          f"{summary['o2_demand_range_mmol_per_g'][1]:.1f} mmol/g")
    print(f"carbon ceiling at {CARBON_LOADING:.0f} g/L loading: "
          f"{out.carbon_ceiling_g_L.min():.0f}-{out.carbon_ceiling_g_L.max():.0f} g/L\n")
    print("oxygen-limited ceiling (g/L) over a 90 h batch:")
    print(piv.round(0).to_string())
    print(f"\noxygen is the binding bound in "
          f"{summary['oxygen_binds_in_n_cases']} of {summary['total_cases']} cases; "
          f"the tightest oxygen bound is {summary['min_ratio_o2_to_carbon']:.1f}x "
          f"the carbon bound")


if __name__ == "__main__":
    main()
