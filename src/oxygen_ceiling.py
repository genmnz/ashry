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
BATCH_HOURS = 90.0
CARBON_LOADING = 350.0                    # g/L, the central case of Chapter 5


def main() -> None:
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
