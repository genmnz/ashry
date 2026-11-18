"""
Protein-specific metabolic cost and maximum theoretical yield in Komagataella phaffii.

Core idea
---------
Genome-scale models carry a *generic* protein pseudo-reaction whose amino-acid
composition is that of average biomass protein. A recombinant food protein is not
average: caseins are glutamine/proline rich, beta-lactoglobulin is leucine rich,
leghemoglobin carries a haem. This module builds, for any given sequence, an explicit
synthesis + secretion reaction in iMT1026v3 and computes:

  * the stoichiometric maximum yield  Y_max  [g protein / g substrate]
  * the ATP, NADPH and carbon cost per gram of protein
  * the growth / production trade-off envelope
  * the cost of the post-translational burden (disulfide bonds, N-glycans,
    phosphoserines, haem) carried explicitly rather than lumped into biomass

Conventions
-----------
* Amino-acid polymerisation cost is charged explicitly, because the model lumps
  translation into the growth-associated maintenance term of the BIOMASS reaction.
  Default 4.3 ATP-equivalents per peptide bond (2 ATP for aminoacyl-tRNA charging,
  ATP -> AMP + PPi counted as 2; 2 GTP for elongation; small proofreading term).
  Sensitivity over 2.0-5.5 is reported in the results, so no conclusion rests on it.
* One disulfide bond costs 1 FADH2-equivalent passed to O2 via Ero1/PDI; we charge
  it as 0.5 O2 + oxidation of one cysteine pair (net: loss of 2 [H] to water).
* One N-glycosylation sequon receives Man8GlcNAc2 in the ER (K. phaffii
  hyperglycosylates in the Golgi; the core transfer is the conservative floor).
* One phosphoserine costs 1 ATP -> ADP.
* Haem b is taken from the model's own biosynthetic network when present.

Every number this module produces is reproducible from the SBML file in
data/models/ and the FASTA files in data/sequences/.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

logging.disable(logging.WARNING)

import cobra  # noqa: E402
from cobra import Metabolite, Reaction  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
MODEL_PATH = REPO / "data" / "models" / "iMT1026" / "Ppa_iMT1026v3.xml"

# iMT1026v3 cytosolic amino-acid metabolite ids
AA_MET = {
    "A": "ala_L_c", "R": "arg_L_c", "N": "asn_L_c", "D": "asp_L_c", "C": "cys_L_c",
    "Q": "gln_L_c", "E": "glu_L_c", "G": "gly_c", "H": "his_L_c", "I": "ile_L_c",
    "L": "leu_L_c", "K": "lys_L_c", "M": "met_L_c", "F": "phe_L_c", "P": "pro_L_c",
    "S": "ser_L_c", "T": "thr_L_c", "W": "trp_L_c", "Y": "tyr_L_c", "V": "val_L_c",
}

# Monoisotopic-free average residue masses (Da), i.e. amino acid minus water
RESIDUE_MASS = {
    "A": 71.0788, "R": 156.1875, "N": 114.1038, "D": 115.0886, "C": 103.1388,
    "Q": 128.1307, "E": 129.1155, "G": 57.0519, "H": 137.1411, "I": 113.1594,
    "L": 113.1594, "K": 128.1741, "M": 131.1926, "F": 147.1766, "P": 97.1167,
    "S": 87.0782, "T": 101.1051, "W": 186.2132, "Y": 163.1760, "V": 99.1326,
}
WATER = 18.0153

# Elemental composition of each residue (C, H, N, O, S) for elemental balance checks
RESIDUE_ELEMENTS = {
    "A": (3, 5, 1, 1, 0), "R": (6, 12, 4, 1, 0), "N": (4, 6, 2, 2, 0),
    "D": (4, 5, 1, 3, 0), "C": (3, 5, 1, 1, 1), "Q": (5, 8, 2, 2, 0),
    "E": (5, 7, 1, 3, 0), "G": (2, 3, 1, 1, 0), "H": (6, 7, 3, 1, 0),
    "I": (6, 11, 1, 1, 0), "L": (6, 11, 1, 1, 0), "K": (6, 12, 2, 1, 0),
    "M": (5, 9, 1, 1, 1), "F": (9, 9, 1, 1, 0), "P": (5, 7, 1, 1, 0),
    "S": (3, 5, 1, 2, 0), "T": (4, 7, 1, 2, 0), "W": (11, 10, 2, 1, 0),
    "Y": (9, 9, 1, 2, 0), "V": (5, 9, 1, 1, 0),
}

SUBSTRATES = {
    # name: (exchange id, molar mass g/mol, carbon atoms)
    "glycerol": ("Ex_glyc", 92.0938, 3),
    "methanol": ("Ex_meoh", 32.0419, 1),
    "glucose": ("Ex_glc_D", 180.1559, 6),
}


# --------------------------------------------------------------------------- #
# sequence handling
# --------------------------------------------------------------------------- #
def read_fasta(path: Path) -> dict[str, str]:
    seqs, name = {}, None
    buf: list[str] = []
    for line in Path(path).read_text().splitlines():
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].strip(), []
        elif line.strip():
            buf.append(line.strip())
    if name:
        seqs[name] = "".join(buf)
    return seqs


@dataclass
class ProteinSpec:
    """A target protein and everything needed to charge its true synthesis cost."""

    name: str
    sequence: str
    accession: str = ""
    signal_peptide_end: int = 0          # 1-based last residue of the signal peptide
    disulfide_bonds: int = 0
    n_glycosylation_sites: int | None = None   # None -> count NxS/T sequons
    phosphoserines: int = 0
    haem_per_chain: int = 0
    notes: str = ""

    @property
    def mature(self) -> str:
        return self.sequence[self.signal_peptide_end:]

    def composition(self, mature: bool = True) -> dict[str, int]:
        seq = self.mature if mature else self.sequence
        seq = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "", seq.upper())
        return {aa: seq.count(aa) for aa in AA_MET if seq.count(aa)}

    def length(self, mature: bool = True) -> int:
        return len(self.mature if mature else self.sequence)

    def mw(self, mature: bool = True) -> float:
        """Average molecular mass of the polypeptide in Da (no PTMs)."""
        seq = self.mature if mature else self.sequence
        return sum(RESIDUE_MASS[a] for a in seq if a in RESIDUE_MASS) + WATER

    def sequons(self, mature: bool = True) -> int:
        seq = self.mature if mature else self.sequence
        return len(re.findall(r"(?=N[^P][ST])", seq))

    def n_glyc(self, mature: bool = True) -> int:
        return self.sequons(mature) if self.n_glycosylation_sites is None \
            else self.n_glycosylation_sites

    def elements(self, mature: bool = True) -> dict[str, float]:
        seq = self.mature if mature else self.sequence
        c = h = n = o = s = 0
        for a in seq:
            if a in RESIDUE_ELEMENTS:
                dc, dh, dn, do, ds = RESIDUE_ELEMENTS[a]
                c, h, n, o, s = c + dc, h + dh, n + dn, o + do, s + ds
        return {"C": c, "H": h + 2, "N": n, "O": o + 1, "S": s}


# --------------------------------------------------------------------------- #
# model surgery
# --------------------------------------------------------------------------- #
def load_model(path: Path = MODEL_PATH) -> cobra.Model:
    return cobra.io.read_sbml_model(str(path))


def _ensure_cytosolic_haem(model: cobra.Model) -> str | None:
    """iMT1026v3 synthesises protohaem IX in the mitochondrion (pheme_m).

    A cytosolic haemoprotein such as leghemoglobin must receive it in the cytosol,
    so if no cytosolic pool exists we add the (physiologically real, but not
    explicitly modelled) export of protohaem from the mitochondrion.
    """
    if "pheme_c" in model.metabolites:
        return "pheme_c"
    if "pheme_m" not in model.metabolites:
        return None
    pheme_m = model.metabolites.get_by_id("pheme_m")
    pheme_c = Metabolite("pheme_c", formula=pheme_m.formula, charge=pheme_m.charge,
                         compartment="c", name="Protoheme IX (cytosol)")
    tr = Reaction("PHEMEtm_thesis")
    tr.name = "Protoheme IX mitochondrial export (added for haemoprotein demand)"
    tr.lower_bound, tr.upper_bound = 0.0, 1000.0
    tr.add_metabolites({pheme_m: -1.0, pheme_c: 1.0})
    model.add_reactions([tr])
    return "pheme_c"


def add_protein_reactions(
    model: cobra.Model,
    spec: ProteinSpec,
    atp_per_bond: float = 4.3,
    charge_ptms: bool = True,
    mature: bool = True,
    mannose_per_glycan: float = 9.0,
) -> tuple[str, float]:
    """Add synthesis + secretion of `spec` to `model`. Returns (sink id, MW in g/mmol).

    The synthesis reaction produces 1 mmol of polypeptide, so the sink flux is in
    mmol/gDW/h and gram flux = flux * MW/1000 ... with MW in g/mol this is simply
    flux [mmol/gDW/h] * MW [g/mol] / 1000 = g/gDW/h.
    """
    comp = spec.composition(mature)
    length = spec.length(mature)
    mw = spec.mw(mature)

    prot = Metabolite(f"prot_{spec.name}_c", compartment="c",
                      name=f"{spec.name} polypeptide")
    rxn = Reaction(f"SYN_{spec.name}")
    rxn.name = f"Synthesis of {spec.name}"
    rxn.lower_bound, rxn.upper_bound = 0.0, 1000.0

    stoich: dict[Metabolite, float] = {}

    def add(met_id: str, coeff: float) -> None:
        met = model.metabolites.get_by_id(met_id)
        stoich[met] = stoich.get(met, 0.0) + coeff

    for aa, n in comp.items():
        add(AA_MET[aa], -float(n))

    # translation: atp_per_bond ATP-equivalents per peptide bond
    n_bonds = max(length - 1, 0)
    atp = atp_per_bond * n_bonds
    if charge_ptms:
        atp += spec.phosphoserines                       # 1 ATP per phosphoserine
    add("atp_c", -atp)
    add("h2o_c", -atp)
    add("adp_c", atp)
    add("pi_c", atp)
    add("h_c", atp)
    # water released by peptide-bond formation
    add("h2o_c", float(n_bonds))

    if charge_ptms:
        # disulfide formation: 2 cysteine thiols -> cystine, electrons to O2 via Ero1
        if spec.disulfide_bonds:
            add("o2_c", -0.5 * spec.disulfide_bonds)
            add("h2o_c", 1.0 * spec.disulfide_bonds)
        # core N-glycan Man8GlcNAc2: 2 UDP-GlcNAc + 9 GDP-mannose equivalents
        n_sites = spec.n_glyc(mature)
        if n_sites:
            for met_id, per_site in (("uacgam_c", 2.0),
                                     ("gdpmann_c", mannose_per_glycan)):
                if met_id in model.metabolites:
                    add(met_id, -per_site * n_sites)
            for met_id, per_site in (("udp_c", 2.0), ("gdp_c", mannose_per_glycan)):
                if met_id in model.metabolites:
                    add(met_id, per_site * n_sites)
        if spec.haem_per_chain:
            haem_id = _ensure_cytosolic_haem(model)
            if haem_id:
                add(haem_id, -float(spec.haem_per_chain))

    stoich[prot] = 1.0
    rxn.add_metabolites(stoich)
    model.add_reactions([rxn])

    sink = Reaction(f"DM_{spec.name}")
    sink.name = f"Secretion/demand of {spec.name}"
    sink.lower_bound, sink.upper_bound = 0.0, 1000.0
    sink.add_metabolites({prot: -1.0})
    model.add_reactions([sink])
    return sink.id, mw


def set_substrate(model: cobra.Model, substrate: str, uptake_mmol: float = 10.0) -> None:
    for name, (ex_id, _, _) in SUBSTRATES.items():
        ex = model.reactions.get_by_id(ex_id)
        if name == substrate:
            ex.lower_bound = -abs(uptake_mmol)
            ex.upper_bound = 1000.0
        else:
            ex.lower_bound = 0.0
    model.reactions.Ex_o2.lower_bound = -1000.0


def yield_analysis(
    spec: ProteinSpec,
    substrate: str = "glycerol",
    atp_per_bond: float = 4.3,
    charge_ptms: bool = True,
    growth_rate: float | None = 0.0,
    uptake_mmol: float = 10.0,
    model: cobra.Model | None = None,
    mannose_per_glycan: float = 9.0,
) -> dict:
    """Maximum theoretical yield of `spec` on `substrate`, optionally at fixed growth."""
    m = (model or load_model()).copy()
    sink_id, mw = add_protein_reactions(
        m, spec, atp_per_bond, charge_ptms,
        mannose_per_glycan=mannose_per_glycan)
    set_substrate(m, substrate, uptake_mmol)

    biomass = m.reactions.get_by_id("BIOMASS_glyc") if substrate != "methanol" \
        else m.reactions.get_by_id("BIOMASS_meoh")
    for rid in ("BIOMASS_glyc", "BIOMASS_meoh", "BIOMASS"):
        m.reactions.get_by_id(rid).bounds = (0.0, 0.0)
    if growth_rate is not None:
        biomass.bounds = (growth_rate, growth_rate)
    else:
        biomass.bounds = (0.0, 1000.0)

    m.objective = sink_id
    sol = m.optimize()
    if sol.status != "optimal":
        return {"protein": spec.name, "substrate": substrate, "status": sol.status}

    flux = sol.objective_value                      # mmol protein / gDW / h
    g_prot = flux * mw / 1000.0                     # g protein / gDW / h
    _, sub_mw, sub_c = SUBSTRATES[substrate]
    g_sub = uptake_mmol * sub_mw / 1000.0
    elements = spec.elements()
    c_prot = flux * elements["C"] / 1000.0          # mol C in product
    c_sub = uptake_mmol * sub_c / 1000.0

    return {
        "protein": spec.name,
        "substrate": substrate,
        "atp_per_bond": atp_per_bond,
        "charge_ptms": charge_ptms,
        "mannose_per_glycan": mannose_per_glycan,
        "growth_rate": growth_rate,
        "mw_kda": round(mw / 1000.0, 3),
        "length_mature": spec.length(),
        "status": sol.status,
        "flux_mmol_gDW_h": flux,
        "g_protein_per_g_substrate": g_prot / g_sub,
        "mol_protein_per_mol_substrate": flux / uptake_mmol,
        "carbon_yield_Cmol_per_Cmol": c_prot / c_sub,
        "substrate_g_per_g_protein": g_sub / g_prot if g_prot else float("nan"),
        "co2_mmol_per_g_protein": float(sol.fluxes.get("Ex_co2", 0.0)) / g_prot if g_prot else float("nan"),
        "o2_mmol_per_g_protein": -float(sol.fluxes.get("Ex_o2", 0.0)) / g_prot if g_prot else float("nan"),
    }


def composition_table(specs: list[ProteinSpec]) -> list[dict]:
    rows = []
    for s in specs:
        comp = s.composition()
        total = sum(comp.values()) or 1
        row = {
            "protein": s.name, "accession": s.accession,
            "length_precursor": s.length(False), "length_mature": s.length(),
            "mw_kda": round(s.mw() / 1000.0, 3),
            "cys": comp.get("C", 0), "disulfides": s.disulfide_bonds,
            "n_sequons": s.sequons(), "phosphoserines": s.phosphoserines,
        }
        for aa in sorted(AA_MET):
            row[f"f_{aa}"] = comp.get(aa, 0) / total
        row.update(s.elements())
        rows.append(row)
    return rows


if __name__ == "__main__":  # pragma: no cover - smoke test
    specs = [ProteinSpec(name="test", sequence="MKVLILACLVALALARELEELNVPGEIVESL")]
    print(json.dumps(yield_analysis(specs[0]), indent=2))
