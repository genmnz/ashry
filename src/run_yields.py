"""
Run the protein-specific yield analysis over the whole panel.

Produces results/tables/protein_yields.csv with, for every protein x substrate x
assumption combination, the maximum theoretical yield and the associated carbon,
oxygen and ATP economy; plus results/tables/ptm_cost.csv isolating the cost of the
post-translational load, and results/tables/growth_tradeoff.csv for the
production-versus-growth envelope.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from protein_cost import (
    ProteinSpec, SUBSTRATES, load_model, read_fasta, yield_analysis,
)
from targets import TARGETS_BY_KEY

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"
META = REPO / "data" / "sequences" / "targets_metadata.json"
FASTA = REPO / "data" / "sequences" / "targets.fasta"


def load_specs() -> list[ProteinSpec]:
    meta = {m["key"]: m for m in json.loads(META.read_text())}
    seqs = read_fasta(FASTA)
    specs = []
    for header, seq in seqs.items():
        key = header.split("|")[0]
        t = TARGETS_BY_KEY[key]
        m = meta[key]
        specs.append(ProteinSpec(
            name=key, sequence=seq, accession=t.accession,
            signal_peptide_end=0,              # targets.fasta already holds the mature chain
            disulfide_bonds=t.disulfide_bonds,
            n_glycosylation_sites=t.n_glyc_sites,
            phosphoserines=t.phosphoserines,
            haem_per_chain=t.haem_per_chain,
            notes=m["category"],
        ))
    return specs


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    keys: list[str] = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    specs = load_specs()
    base = load_model()

    rows = []
    for spec in specs:
        for substrate in SUBSTRATES:
            for atp in (2.0, 4.3, 5.5):
                for ptm in (True, False):
                    r = yield_analysis(
                        spec, substrate=substrate, atp_per_bond=atp,
                        charge_ptms=ptm, growth_rate=0.0, model=base)
                    r["category"] = spec.notes
                    rows.append(r)
    write_csv(TABLES / "protein_yields.csv", rows)

    # isolate the post-translational burden at the default assumption
    ptm_rows = []
    for spec in specs:
        for substrate in SUBSTRATES:
            with_ptm = yield_analysis(spec, substrate=substrate, charge_ptms=True,
                                      growth_rate=0.0, model=base)
            no_ptm = yield_analysis(spec, substrate=substrate, charge_ptms=False,
                                    growth_rate=0.0, model=base)
            if with_ptm.get("status") != "optimal" or no_ptm.get("status") != "optimal":
                continue
            # Two yields, because they answer different questions. The product
            # basis counts glycan, phosphate and haem mass as sold product; the
            # polypeptide basis counts only the backbone, which is what a food
            # protein is bought for. Glycosylation raises the first and lowers
            # the second, so quoting only one of them misleads.
            y1 = with_ptm["g_protein_per_g_substrate"]
            y0 = no_ptm["g_protein_per_g_substrate"]
            p1 = with_ptm["g_polypeptide_per_g_substrate"]
            ptm_rows.append({
                "protein": spec.name, "category": spec.notes, "substrate": substrate,
                "yield_with_ptm_product_basis": y1,
                "yield_with_ptm_polypeptide_basis": p1,
                "yield_backbone_only": y0,
                "ptm_mass_yield_change_pct": 100.0 * (y1 - y0) / y0 if y0 else float("nan"),
                "ptm_polypeptide_penalty_pct": 100.0 * (y0 - p1) / y0 if y0 else float("nan"),
                "disulfides": spec.disulfide_bonds,
                "n_glyc": spec.n_glyc(), "phosphoserines": spec.phosphoserines,
                "haem": spec.haem_per_chain,
            })
    write_csv(TABLES / "ptm_cost.csv", ptm_rows)

    # yeast hypermannosylation: K. phaffii extends the core Man8GlcNAc2 in the Golgi.
    # Core transfer (Man9) is the floor; Man20 and Man60 bracket reported outer chains.
    glyc_rows = []
    for spec in specs:
        if not spec.n_glyc():
            continue
        for man in (9.0, 20.0, 60.0, 100.0):
            r = yield_analysis(spec, substrate="glycerol", growth_rate=0.0,
                               model=base, mannose_per_glycan=man)
            r["category"] = spec.notes
            r["n_glyc_sites"] = spec.n_glyc()
            glyc_rows.append(r)
    write_csv(TABLES / "glycan_scenarios.csv", glyc_rows)

    # growth / production trade-off envelope on glycerol
    tr_rows = []
    for spec in specs:
        for mu in (0.0, 0.02, 0.05, 0.10, 0.15, 0.20):
            r = yield_analysis(spec, substrate="glycerol", growth_rate=mu, model=base)
            r["category"] = spec.notes
            tr_rows.append(r)
    write_csv(TABLES / "growth_tradeoff.csv", tr_rows)

    print(f"wrote {len(rows)} yield rows, {len(ptm_rows)} PTM rows, "
          f"{len(glyc_rows)} glycan rows, {len(tr_rows)} trade-off rows")

    print("\nMaximum theoretical yield, g protein / g substrate (4.3 ATP/bond, PTMs charged, mu=0):")
    print(f"{'protein':<22}" + "".join(f"{s:>12}" for s in SUBSTRATES))
    for spec in specs:
        line = f"{spec.name:<22}"
        for s in SUBSTRATES:
            v = [r for r in rows if r["protein"] == spec.name and r["substrate"] == s
                 and r["atp_per_bond"] == 4.3 and r["charge_ptms"]]
            line += f"{v[0].get('g_protein_per_g_substrate', float('nan')):>12.3f}" if v and v[0].get("status") == "optimal" else f"{'infeasible':>12}"
        print(line)


if __name__ == "__main__":
    main()
