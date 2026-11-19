"""
Which part of metabolism limits each food protein?

Two complementary analyses on iMT1026v3 with the protein-specific synthesis
reaction installed:

1. **Shadow prices of the amino-acid pools.** At the optimum, the shadow price of
   a metabolite is the improvement in the objective obtainable per extra unit of
   that metabolite. Ranking amino acids by shadow price x the protein's demand for
   them gives a per-protein picture of where the supply pressure falls, which is
   not the same for a glutamine/proline-rich casein and a cysteine-rich lactoferrin.

2. **FSEOF (Flux Scanning with Enforced Objective Function, Choi et al. 2010,
   Appl Environ Microbiol 76:3097).** The protein demand is forced from zero to its
   maximum in steps while growth is maximised; reactions whose flux rises
   monotonically with enforced production are amplification targets, those that
   fall are candidate knockdowns. This is the standard way to propose metabolic
   engineering targets from a model, and it has not been run for these proteins.

Outputs
-------
results/tables/shadow_prices.csv
results/tables/fseof_targets.csv
results/tables/fseof_summary.csv
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import cobra

from thesis_model import AA_MET, ProteinSpec, add_protein_reactions, load_model, read_fasta, set_substrate
from targets import TARGETS_BY_KEY

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"


def load_specs() -> list[ProteinSpec]:
    meta = {m["key"]: m for m in json.loads(
        (REPO / "data" / "sequences" / "targets_metadata.json").read_text())}
    out = []
    for header, seq in read_fasta(REPO / "data" / "sequences" / "targets.fasta").items():
        key = header.split("|")[0]
        t = TARGETS_BY_KEY[key]
        out.append(ProteinSpec(
            name=key, sequence=seq, accession=t.accession, signal_peptide_end=0,
            disulfide_bonds=t.disulfide_bonds, n_glycosylation_sites=t.n_glyc_sites,
            phosphoserines=t.phosphoserines, haem_per_chain=t.haem_per_chain,
            notes=meta[key]["category"]))
    return out


def prepare(spec: ProteinSpec, substrate: str = "glycerol",
            base: cobra.Model | None = None) -> tuple[cobra.Model, str]:
    m = (base or load_model()).copy()
    sink_id, _, _ = add_protein_reactions(m, spec)
    set_substrate(m, substrate, 10.0)
    for rid in ("BIOMASS_meoh", "BIOMASS"):
        m.reactions.get_by_id(rid).bounds = (0.0, 0.0)
    m.reactions.get_by_id("BIOMASS_glyc").bounds = (0.0, 1000.0)
    return m, sink_id


def shadow_prices(spec: ProteinSpec, base: cobra.Model) -> list[dict]:
    m, sink_id = prepare(spec, base=base)
    m.reactions.get_by_id("BIOMASS_glyc").bounds = (0.0, 0.0)
    m.objective = sink_id
    sol = m.optimize()
    if sol.status != "optimal":
        return []
    comp = spec.composition()
    total = sum(comp.values()) or 1
    rows = []
    for aa, met_id in AA_MET.items():
        met = m.metabolites.get_by_id(met_id)
        sp = float(sol.shadow_prices.get(met_id, 0.0))
        rows.append({
            "protein": spec.name, "category": spec.notes, "amino_acid": aa,
            "metabolite": met_id, "residues": comp.get(aa, 0),
            "residue_fraction": comp.get(aa, 0) / total,
            "shadow_price": sp,
            "demand_weighted_pressure": sp * comp.get(aa, 0) / total,
        })
    return rows


def fseof(spec: ProteinSpec, base: cobra.Model, steps: int = 11,
          min_flux: float = 1e-6) -> tuple[list[dict], dict]:
    m, sink_id = prepare(spec, base=base)
    sink = m.reactions.get_by_id(sink_id)
    biomass = m.reactions.get_by_id("BIOMASS_glyc")

    m.objective = sink
    max_prod = m.optimize().objective_value or 0.0
    if max_prod <= 0:
        return [], {}

    m.objective = biomass
    profiles: dict[str, list[float]] = defaultdict(list)
    fractions = [i / (steps - 1) for i in range(steps)]
    growths = []
    for f in fractions:
        sink.bounds = (f * max_prod * 0.999, 1000.0)
        sol = m.optimize()
        if sol.status != "optimal":
            growths.append(float("nan"))
            for r in m.reactions:
                profiles[r.id].append(float("nan"))
            continue
        growths.append(sol.objective_value)
        for r in m.reactions:
            profiles[r.id].append(float(sol.fluxes[r.id]))

    rows = []
    for rid, prof in profiles.items():
        if any(p != p for p in prof):   # NaN
            continue
        if max(abs(p) for p in prof) < min_flux:
            continue
        start, end = prof[0], prof[-1]
        increasing = all(prof[i + 1] >= prof[i] - 1e-9 for i in range(len(prof) - 1))
        decreasing = all(prof[i + 1] <= prof[i] + 1e-9 for i in range(len(prof) - 1))
        if not (increasing or decreasing):
            continue
        if abs(end - start) < min_flux:
            continue
        rxn = m.reactions.get_by_id(rid)
        rows.append({
            "protein": spec.name, "category": spec.notes, "reaction": rid,
            "name": rxn.name, "subsystem": getattr(rxn, "subsystem", "") or "",
            "genes": ";".join(sorted(g.id for g in rxn.genes)),
            "flux_start": start, "flux_end": end,
            "fold_change": (abs(end) / abs(start)) if abs(start) > min_flux else float("inf"),
            "direction": "amplify" if abs(end) > abs(start) else "attenuate",
            "monotonic": "up" if increasing else "down",
        })
    rows.sort(key=lambda r: -abs(r["flux_end"] - r["flux_start"]))
    summary = {
        "protein": spec.name, "max_production_mmol_gDW_h": max_prod,
        "growth_at_zero_production": growths[0],
        "growth_at_max_production": growths[-1],
        "n_amplify": sum(1 for r in rows if r["direction"] == "amplify"),
        "n_attenuate": sum(1 for r in rows if r["direction"] == "attenuate"),
    }
    return rows, summary


def main() -> None:
    specs = load_specs()
    base = load_model()
    TABLES.mkdir(parents=True, exist_ok=True)

    sp_rows: list[dict] = []
    fs_rows: list[dict] = []
    summaries: list[dict] = []
    for spec in specs:
        sp_rows.extend(shadow_prices(spec, base))
        rows, summary = fseof(spec, base)
        fs_rows.extend(rows[:60])
        if summary:
            summaries.append(summary)
        print(f"  {spec.name:<22} fseof targets kept {len(rows[:60]):>3} "
              f"(amplify {summary.get('n_amplify', 0)}, "
              f"attenuate {summary.get('n_attenuate', 0)})")

    for path, rows in ((TABLES / "shadow_prices.csv", sp_rows),
                       (TABLES / "fseof_targets.csv", fs_rows),
                       (TABLES / "fseof_summary.csv", summaries)):
        if not rows:
            continue
        with path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    print("\nTop amino-acid supply pressure per protein:")
    by_prot: dict[str, list[dict]] = defaultdict(list)
    for r in sp_rows:
        by_prot[r["protein"]].append(r)
    for prot, rows in by_prot.items():
        top = sorted(rows, key=lambda r: -abs(r["demand_weighted_pressure"]))[:4]
        print(f"  {prot:<22}" + ", ".join(
            f"{t['amino_acid']}({t['demand_weighted_pressure']:.3g})" for t in top))


if __name__ == "__main__":
    main()
