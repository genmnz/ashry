"""
Techno-economic model for precision-fermented food proteins, driven by the
stoichiometric yields computed in protein_cost.py.

Design principle
----------------
Most published cost estimates for precision fermentation are opaque: a single
dollar figure whose assumptions cannot be audited. This model is built the other
way round. Every parameter lives in `Parameters` with an explicit source string,
the cost is decomposed into substrate, other media, utilities, downstream and
annualised capital, and the model reports two reference points that bound the
whole debate:

  * the **stoichiometric floor**: the raw-material cost of the carbon alone if
    the organism hit the maximum theoretical yield computed from the genome-scale
    model, with no cells, no losses and no equipment. Nothing can be cheaper.
  * the **engineering gap**: the ratio of the modelled plant cost to that floor.

A claim such as "precision fermentation will reach $10/kg" is then testable: it
either sits above the floor at a plausible gap, or it does not.

Nothing here is calibrated to a company's unpublished data; all parameters are
either cited or declared as assumptions.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


@dataclass
class Parameter:
    value: float
    unit: str
    source: str

    def __float__(self) -> float:  # pragma: no cover
        return float(self.value)


@dataclass
class Parameters:
    """All economics in one auditable place. `source` must never be empty."""

    # --- titre and kinetics -------------------------------------------------
    titer_g_per_L: Parameter
    batch_time_h: Parameter
    turnaround_h: Parameter
    # --- biology ------------------------------------------------------------
    yield_g_protein_per_g_substrate: Parameter      # realised, not theoretical
    theoretical_yield_g_per_g: Parameter            # from the genome-scale model
    # --- prices -------------------------------------------------------------
    substrate_price_usd_per_t: Parameter
    media_other_usd_per_m3: Parameter
    electricity_usd_per_kWh: Parameter
    # --- plant --------------------------------------------------------------
    reactor_volume_m3: Parameter
    working_fraction: Parameter
    plant_uptime_frac: Parameter
    capex_usd_per_m3: Parameter
    capex_life_years: Parameter
    maintenance_frac_capex: Parameter
    labour_usd_per_year: Parameter
    # --- energy -------------------------------------------------------------
    aeration_kW_per_m3: Parameter
    agitation_kW_per_m3: Parameter
    cooling_kW_per_m3: Parameter
    # --- downstream ---------------------------------------------------------
    dsp_recovery_frac: Parameter
    dsp_usd_per_kg_product: Parameter

    def as_dict(self) -> dict:
        return {k: asdict(v) for k, v in self.__dict__.items()}


def default_parameters() -> Parameters:
    """Baseline case: glycerol-fed, GAP-promoter K. phaffii at 200 m3.

    Prices are order-of-magnitude commodity figures and are declared as such;
    the thesis reports the full sensitivity rather than leaning on any one value.
    """
    P = Parameter
    return Parameters(
        titer_g_per_L=P(10.0, "g/L", "assumption; literature range 1-14 g/L for food proteins"),
        batch_time_h=P(90.0, "h", "assumption: typical fed-batch cycle"),
        turnaround_h=P(12.0, "h", "assumption: clean/sterilise/fill"),
        yield_g_protein_per_g_substrate=P(0.10, "g/g", "assumption: realised yield, to be scanned"),
        theoretical_yield_g_per_g=P(0.64, "g/g", "computed here from iMT1026v3"),
        substrate_price_usd_per_t=P(600.0, "USD/t", "assumption: technical glycerol, to be sourced"),
        media_other_usd_per_m3=P(30.0, "USD/m3", "assumption: salts, biotin, antifoam"),
        electricity_usd_per_kWh=P(0.08, "USD/kWh", "assumption: industrial tariff"),
        reactor_volume_m3=P(200.0, "m3", "assumption: commercial scale"),
        working_fraction=P(0.75, "-", "assumption"),
        plant_uptime_frac=P(0.90, "-", "assumption"),
        capex_usd_per_m3=P(12000.0, "USD/m3", "assumption: installed fermentation capacity"),
        capex_life_years=P(15.0, "a", "assumption: straight-line depreciation"),
        maintenance_frac_capex=P(0.04, "1/a", "assumption"),
        labour_usd_per_year=P(1.5e6, "USD/a", "assumption: plant crew"),
        aeration_kW_per_m3=P(0.6, "kW/m3", "assumption"),
        agitation_kW_per_m3=P(1.5, "kW/m3", "assumption: high-cell-density aerobic"),
        cooling_kW_per_m3=P(0.5, "kW/m3", "assumption"),
        dsp_recovery_frac=P(0.70, "-", "assumption: cell removal, UF/DF, spray dry"),
        dsp_usd_per_kg_product=P(6.0, "USD/kg", "assumption: chromatography-free route"),
    )


@dataclass
class CostBreakdown:
    substrate: float = 0.0
    media_other: float = 0.0
    utilities: float = 0.0
    downstream: float = 0.0
    capital: float = 0.0
    maintenance: float = 0.0
    labour: float = 0.0

    @property
    def total(self) -> float:
        return (self.substrate + self.media_other + self.utilities
                + self.downstream + self.capital + self.maintenance + self.labour)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["total"] = self.total
        return d


def run_model(p: Parameters) -> dict:
    v = {k: float(x.value) for k, x in p.__dict__.items()}

    working_m3 = v["reactor_volume_m3"] * v["working_fraction"]
    cycle_h = v["batch_time_h"] + v["turnaround_h"]
    cycles_per_year = 8760.0 * v["plant_uptime_frac"] / cycle_h

    protein_per_batch_kg = v["titer_g_per_L"] * working_m3  # g/L * m3 = kg
    product_kg_per_batch = protein_per_batch_kg * v["dsp_recovery_frac"]
    product_kg_per_year = product_kg_per_batch * cycles_per_year

    substrate_kg_per_batch = protein_per_batch_kg / v["yield_g_protein_per_g_substrate"]
    substrate_cost = (substrate_kg_per_batch / 1000.0) * v["substrate_price_usd_per_t"]

    media_cost = working_m3 * v["media_other_usd_per_m3"]

    power_kW = working_m3 * (v["aeration_kW_per_m3"] + v["agitation_kW_per_m3"]
                             + v["cooling_kW_per_m3"])
    utilities_cost = power_kW * v["batch_time_h"] * v["electricity_usd_per_kWh"]

    capex = v["reactor_volume_m3"] * v["capex_usd_per_m3"]
    capital_per_year = capex / v["capex_life_years"]
    maintenance_per_year = capex * v["maintenance_frac_capex"]

    cb = CostBreakdown(
        substrate=substrate_cost / product_kg_per_batch,
        media_other=media_cost / product_kg_per_batch,
        utilities=utilities_cost / product_kg_per_batch,
        downstream=v["dsp_usd_per_kg_product"],
        capital=capital_per_year / product_kg_per_year,
        maintenance=maintenance_per_year / product_kg_per_year,
        labour=v["labour_usd_per_year"] / product_kg_per_year,
    )

    floor = (v["substrate_price_usd_per_t"] / 1000.0) / v["theoretical_yield_g_per_g"]

    return {
        "cost_usd_per_kg": cb.total,
        "breakdown_usd_per_kg": cb.as_dict(),
        "stoichiometric_floor_usd_per_kg": floor,
        "engineering_gap_x": cb.total / floor if floor else float("nan"),
        "product_t_per_year": product_kg_per_year / 1000.0,
        "cycles_per_year": cycles_per_year,
        "substrate_t_per_year": substrate_kg_per_batch * cycles_per_year / 1000.0,
        "yield_frac_of_theoretical": v["yield_g_protein_per_g_substrate"]
        / v["theoretical_yield_g_per_g"],
    }


def scan(p: Parameters, field_name: str, values: list[float]) -> list[dict]:
    rows = []
    original = getattr(p, field_name).value
    for val in values:
        getattr(p, field_name).value = val
        r = run_model(p)
        rows.append({field_name: val, **{k: v for k, v in r.items()
                                         if not isinstance(v, dict)}})
    getattr(p, field_name).value = original
    return rows


def tornado(p: Parameters, spread: float = 0.5) -> list[dict]:
    """One-at-a-time sensitivity: each parameter moved +/- `spread` fraction."""
    base = run_model(p)["cost_usd_per_kg"]
    rows = []
    for name, par in p.__dict__.items():
        if name == "theoretical_yield_g_per_g":
            continue
        original = par.value
        par.value = original * (1 - spread)
        low = run_model(p)["cost_usd_per_kg"]
        par.value = original * (1 + spread)
        high = run_model(p)["cost_usd_per_kg"]
        par.value = original
        rows.append({
            "parameter": name, "unit": par.unit, "base_value": original,
            "cost_low": low, "cost_high": high, "base_cost": base,
            "swing_usd_per_kg": abs(high - low),
            "swing_pct_of_base": 100.0 * abs(high - low) / base if base else float("nan"),
        })
    return sorted(rows, key=lambda r: -r["swing_usd_per_kg"])


def monte_carlo(p: Parameters, n: int = 20000, rel_sd: float = 0.25,
                seed: int = 42) -> dict:
    import random
    rng = random.Random(seed)
    originals = {k: par.value for k, par in p.__dict__.items()}
    samples = []
    for _ in range(n):
        for k, par in p.__dict__.items():
            if k == "theoretical_yield_g_per_g":
                continue
            mu = math.log(originals[k]) if originals[k] > 0 else 0.0
            par.value = math.exp(rng.gauss(mu, rel_sd))
        samples.append(run_model(p)["cost_usd_per_kg"])
    for k, par in p.__dict__.items():
        par.value = originals[k]
    samples.sort()

    def q(x: float) -> float:
        return samples[min(len(samples) - 1, int(x * len(samples)))]

    return {"n": n, "rel_sd": rel_sd, "p05": q(0.05), "p25": q(0.25),
            "median": q(0.50), "p75": q(0.75), "p95": q(0.95),
            "mean": sum(samples) / len(samples)}


def main() -> None:
    p = default_parameters()
    base = run_model(p)
    out = REPO / "results" / "tables"
    out.mkdir(parents=True, exist_ok=True)

    (out / "tea_baseline.json").write_text(json.dumps(
        {"parameters": p.as_dict(), "result": base,
         "tornado": tornado(p), "monte_carlo": monte_carlo(p)}, indent=2))

    rows = []
    for titer in (1, 2, 5, 10, 20, 40):
        p.titer_g_per_L.value = float(titer)
        for yfrac in (0.10, 0.20, 0.30, 0.50):
            p.yield_g_protein_per_g_substrate.value = (
                yfrac * p.theoretical_yield_g_per_g.value)
            r = run_model(p)
            rows.append({"titer_g_per_L": titer, "yield_frac_of_theoretical": yfrac,
                         "cost_usd_per_kg": r["cost_usd_per_kg"],
                         "substrate_share_pct": 100 * r["breakdown_usd_per_kg"]["substrate"]
                         / r["cost_usd_per_kg"],
                         "capital_share_pct": 100 * r["breakdown_usd_per_kg"]["capital"]
                         / r["cost_usd_per_kg"],
                         "product_t_per_year": r["product_t_per_year"]})
    p = default_parameters()
    with (out / "tea_titer_yield_grid.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"baseline cost  : ${base['cost_usd_per_kg']:.2f}/kg")
    print(f"stoich. floor  : ${base['stoichiometric_floor_usd_per_kg']:.2f}/kg")
    print(f"engineering gap: {base['engineering_gap_x']:.1f}x")
    print(f"output         : {base['product_t_per_year']:.0f} t/a")
    print("\nbreakdown $/kg:")
    for k, v in base["breakdown_usd_per_kg"].items():
        print(f"  {k:<12}{v:>8.2f}")
    print("\ntop sensitivities:")
    for r in tornado(p)[:6]:
        print(f"  {r['parameter']:<34}{r['swing_usd_per_kg']:>8.2f} $/kg")


if __name__ == "__main__":
    main()
