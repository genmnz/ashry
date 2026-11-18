#!/usr/bin/env python3
"""Stoichiometric cost of recombinant protein synthesis and secretion.

Builds, for an arbitrary amino-acid sequence, an explicitly mass- and
electron-balanced synthesis reaction that can be inserted into a genome-scale
metabolic model (GEM).  The reaction accounts for

  1. amino-acid draw (every residue translated, including the signal peptide),
  2. translational energy (aminoacyl-tRNA charging + elongation, in ATP
     equivalents),
  3. oxidative folding (disulfide formation via Ero1/PDI, electrons to O2),
  4. N-glycosylation (sugar-nucleotide donors for the yeast core glycan plus
     outer-chain mannose),
  5. O-mannosylation (Dol-P-Man donors),
  6. serine/threonine phosphorylation (kinase ATP), used for the caseins,
  7. haem b prosthetic group (globins),
  8. chaperone (BiP/Kar2) ATPase cycles,
  9. vesicular transport GTP (COPII/COPI/Rab),
 10. signal-peptide cleavage with optional amino-acid recycling.

All parameters live in `CostParams` so that every number in the paper can be
traced to a citation and varied in sensitivity analysis.

References for the default parameter values are in
`docs/COST_PARAMETERS.md`.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

# ----------------------------------------------------------------------------
# Residue chemistry
# ----------------------------------------------------------------------------

# free amino acid elemental composition (neutral, zwitterion-free formula)
AA_FORMULA: Dict[str, Dict[str, int]] = {
    "A": {"C": 3, "H": 7, "N": 1, "O": 2},
    "R": {"C": 6, "H": 14, "N": 4, "O": 2},
    "N": {"C": 4, "H": 8, "N": 2, "O": 3},
    "D": {"C": 4, "H": 7, "N": 1, "O": 4},
    "C": {"C": 3, "H": 7, "N": 1, "O": 2, "S": 1},
    "Q": {"C": 5, "H": 10, "N": 2, "O": 3},
    "E": {"C": 5, "H": 9, "N": 1, "O": 4},
    "G": {"C": 2, "H": 5, "N": 1, "O": 2},
    "H": {"C": 6, "H": 9, "N": 3, "O": 2},
    "I": {"C": 6, "H": 13, "N": 1, "O": 2},
    "L": {"C": 6, "H": 13, "N": 1, "O": 2},
    "K": {"C": 6, "H": 14, "N": 2, "O": 2},
    "M": {"C": 5, "H": 11, "N": 1, "O": 2, "S": 1},
    "F": {"C": 9, "H": 11, "N": 1, "O": 2},
    "P": {"C": 5, "H": 9, "N": 1, "O": 2},
    "S": {"C": 3, "H": 7, "N": 1, "O": 3},
    "T": {"C": 4, "H": 9, "N": 1, "O": 3},
    "W": {"C": 11, "H": 12, "N": 2, "O": 2},
    "Y": {"C": 9, "H": 11, "N": 1, "O": 3},
    "V": {"C": 5, "H": 11, "N": 1, "O": 2},
}

# model metabolite id (cytosolic) for each residue, as used by iMT1026v3
AA_MET: Dict[str, str] = {
    "A": "ala_L_c", "R": "arg_L_c", "N": "asn_L_c", "D": "asp_L_c",
    "C": "cys_L_c", "Q": "gln_L_c", "E": "glu_L_c", "G": "gly_c",
    "H": "his_L_c", "I": "ile_L_c", "L": "leu_L_c", "K": "lys_L_c",
    "M": "met_L_c", "F": "phe_L_c", "P": "pro_L_c", "S": "ser_L_c",
    "T": "thr_L_c", "W": "trp_L_c", "Y": "tyr_L_c", "V": "val_L_c",
}

ATOMIC_MASS = {"C": 12.0107, "H": 1.00794, "N": 14.0067, "O": 15.9994,
               "S": 32.065, "P": 30.973762, "Fe": 55.845}

H2O = {"H": 2, "O": 1}
HPO3 = {"H": 1, "O": 3, "P": 1}          # phosphoryl group added by a kinase
GLCNAC_RES = {"C": 8, "H": 13, "N": 1, "O": 5}   # GlcNAc residue (-H2O)
MAN_RES = {"C": 6, "H": 10, "O": 5}              # hexose residue (-H2O)
HAEM_B = {"C": 34, "H": 30, "Fe": 1, "N": 4, "O": 4}   # protoheme, as in model


def _add(a: Dict[str, float], b: Dict[str, float], n: float = 1.0) -> None:
    for k, v in b.items():
        a[k] = a.get(k, 0.0) + n * v


def formula_mass(f: Dict[str, float]) -> float:
    return sum(ATOMIC_MASS[k] * v for k, v in f.items())


def formula_str(f: Dict[str, float]) -> str:
    out = []
    for k in ("C", "H", "N", "O", "P", "S", "Fe"):
        if f.get(k):
            v = f[k]
            v = int(round(v)) if abs(v - round(v)) < 1e-6 else round(v, 4)
            out.append(k if v == 1 else f"{k}{v}")
    return "".join(out)


# ----------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------

@dataclass
class CostParams:
    """Every tunable number in the cost model.

    Defaults are the literature-canonical values; see docs/COST_PARAMETERS.md.
    """

    # --- translation -------------------------------------------------------
    atp_per_residue: float = 4.3
    """ATP equivalents consumed per residue polymerised.

    2 per aminoacyl-tRNA charging (ATP -> AMP + PPi, i.e. two high-energy
    phosphate bonds) + 1 GTP for eEF1A delivery + 1 GTP for eEF2 translocation
    = 4; the extra 0.3 covers initiation, termination and proofreading/
    mischarging, and is the value used in the yeast GEM lineage.
    """
    initiation_atp: float = 2.0
    """ATP equivalents per chain for initiation + termination + release."""

    # --- signal peptide ----------------------------------------------------
    include_signal_peptide: bool = True
    """Translate the signal peptide (it is always synthesised before cleavage)."""
    recycle_signal_peptide: bool = True
    """Return the cleaved signal-peptide residues as free amino acids.

    Signal-peptide peptidase and the cytosolic peptidases that clear the
    fragment are ATP-independent, so recycling is the conservative choice; it
    makes the net amino-acid draw equal to the mature chain while the
    translational energy is still paid for the full precursor.
    """

    # --- oxidative folding -------------------------------------------------
    o2_per_disulfide: float = 1.0
    """O2 consumed per disulfide bond formed.

    One disulfide = 2 electrons; Ero1p passes them through FAD to O2 in a
    two-electron step giving H2O2, so 1 O2 -> 1 H2O2 per disulfide.
    """
    isomerisation_cycles_per_disulfide: float = 0.0
    """Futile reduction/re-oxidation cycles per disulfide (NADPH via GSH).

    Baseline 0 (perfect folding on the first pass); raised in the
    misfolding-burden scenarios.
    """

    # --- N-glycosylation ---------------------------------------------------
    n_glycan_mannose: float = 9.0
    """Mannose residues retained per N-glycan.

    K. phaffii transfers Glc3Man9GlcNAc2 and trims to Man8GlcNAc2, then
    extends with alpha-1,2 and alpha-1,6 outer-chain mannose; secreted
    recombinant glycoproteins carry predominantly Man8-Man14. 9 is the
    central value; 5 models a glyco-engineered (humanised) strain and 14 the
    hypermannosylated extreme.
    """
    n_glycan_glcnac: float = 2.0
    n_glycan_transient_glucose: float = 3.0
    """Glc residues added to the dolichol precursor and later trimmed.

    They are paid for even though they do not end up on the protein; the free
    glucose released is returned to the cytosol.
    """
    recycle_transient_glucose: bool = True

    # --- O-mannosylation ---------------------------------------------------
    o_mannose_per_site: float = 2.0
    """Mannose residues per O-mannosylated Ser/Thr in K. phaffii (1-5)."""

    # --- phosphorylation ---------------------------------------------------
    atp_per_phosphorylation: float = 1.0
    phosphorylate: bool = False
    """Whether the host is engineered to phosphorylate the target.

    False for wild-type K. phaffii / T. reesei, which do not phosphorylate
    casein; True in the PTM-competent scenario.
    """

    # --- chaperones and traffic -------------------------------------------
    bip_atp_per_residue: float = 0.0
    """BiP/Kar2 ATPase cycles per residue, as ATP equivalents.

    Baseline 0 so that the stoichiometric floor is a strict lower bound on
    cost; raised in the folding-burden scenarios, where it is the term that
    couples sequence features to metabolic cost.
    """
    transport_gtp_per_molecule: float = 6.0
    """GTP for COPII budding, COPI retrieval and Rab/Ypt cycles per molecule."""

    # --- prosthetic groups -------------------------------------------------
    haem_per_molecule: float = 0.0
    """Protoheme b per protein molecule (1 for monomeric globins)."""


# ----------------------------------------------------------------------------
# Sequence feature extraction
# ----------------------------------------------------------------------------

import re

SEQUON = re.compile(r"N[^P][ST]")


def count_sequons(seq: str) -> int:
    """N-X-S/T sequons, X != P, counted with overlap."""
    return sum(1 for i in range(len(seq) - 2) if SEQUON.match(seq, i))


def sequon_positions(seq: str) -> List[int]:
    return [i + 1 for i in range(len(seq) - 2) if SEQUON.match(seq, i)]


@dataclass
class ProteinSpec:
    """What the cost model needs to know about one protein."""
    name: str
    sequence: str                 # full precursor, signal peptide included
    signal_end: int = 0           # 1-based last residue of the signal peptide
    n_disulfide: int = 0
    n_sequon: Optional[int] = None        # default: computed from mature chain
    n_o_glyc_site: int = 0
    n_phosphosite: int = 0
    n_haem: int = 0
    accession: str = ""
    notes: str = ""
    secreted: bool = True
    """Whether the protein traverses the ER/Golgi in the production host.

    Cytosolically expressed targets (the globins, which are produced
    intracellularly in K. phaffii) pay no glycosylation, no vesicular
    transport and no Ero1-dependent oxidative folding: the cytosol is
    reducing, so annotated disulfides are not formed.
    """

    @property
    def mature(self) -> str:
        return self.sequence[self.signal_end:]

    @property
    def signal(self) -> str:
        return self.sequence[:self.signal_end]

    def sequons(self) -> int:
        if self.n_sequon is not None:
            return self.n_sequon
        return count_sequons(self.mature)


# ----------------------------------------------------------------------------
# Cost computation
# ----------------------------------------------------------------------------

@dataclass
class CostResult:
    name: str
    length_precursor: int
    length_mature: int
    # the product
    product_formula: Dict[str, float]
    product_mass_da: float
    # per molecule
    aa_draw: Dict[str, float]            # residue letter -> count (net)
    atp: float
    gtp: float
    o2: float
    h2o2: float
    nadph: float
    gdpmann: float
    uacgam: float
    udpg: float
    dolmanp: float
    haem: float
    # derived
    carbon_in_product: float
    carbon_in_precursors: float
    atp_per_g: float = 0.0
    nadph_per_g: float = 0.0
    carbon_per_g: float = 0.0
    breakdown: Dict[str, float] = field(default_factory=dict)


def compute_cost(spec: ProteinSpec, p: CostParams) -> CostResult:
    seq_full = spec.sequence
    seq_mat = spec.mature
    Lp, Lm = len(seq_full), len(seq_mat)

    # --- amino-acid draw --------------------------------------------------
    charged = seq_full if p.include_signal_peptide else seq_mat
    draw: Dict[str, float] = {}
    for a in charged:
        if a in AA_MET:
            draw[a] = draw.get(a, 0.0) + 1.0
    if p.include_signal_peptide and p.recycle_signal_peptide:
        for a in spec.signal:
            if a in AA_MET:
                draw[a] -= 1.0

    # --- product elemental formula (mature, modified chain) ---------------
    f: Dict[str, float] = {}
    for a in seq_mat:
        if a in AA_FORMULA:
            _add(f, AA_FORMULA[a])
    _add(f, H2O, -(Lm - 1))                 # peptide bonds
    n_ss = float(spec.n_disulfide) if spec.secreted else 0.0
    _add(f, {"H": -2.0 * n_ss})             # 2 H lost per disulfide
    n_seq = float(spec.sequons()) if spec.secreted else 0.0
    n_oglyc = float(spec.n_o_glyc_site) if spec.secreted else 0.0
    _add(f, GLCNAC_RES, p.n_glycan_glcnac * n_seq)
    _add(f, MAN_RES, p.n_glycan_mannose * n_seq)
    _add(f, MAN_RES, p.o_mannose_per_site * n_oglyc)
    n_phos = float(spec.n_phosphosite) if p.phosphorylate else 0.0
    _add(f, HPO3, n_phos)
    n_haem = float(spec.n_haem) if spec.n_haem else p.haem_per_molecule
    _add(f, HAEM_B, n_haem)
    mass = formula_mass(f)

    # --- energy -----------------------------------------------------------
    atp_translation = p.atp_per_residue * Lp + p.initiation_atp
    atp_bip = p.bip_atp_per_residue * Lp
    atp_phos = p.atp_per_phosphorylation * n_phos
    atp = atp_translation + atp_bip + atp_phos
    gtp = p.transport_gtp_per_molecule if spec.secreted else 0.0

    # --- redox ------------------------------------------------------------
    o2 = p.o2_per_disulfide * n_ss
    h2o2 = o2
    nadph = p.isomerisation_cycles_per_disulfide * n_ss

    # --- glycan donors ----------------------------------------------------
    uacgam = p.n_glycan_glcnac * n_seq
    # core mannose up to Man5 comes straight from GDP-Man on the cytosolic
    # face; the rest is delivered as Dol-P-Man.
    core_direct = min(p.n_glycan_mannose, 5.0) * n_seq
    via_dolmanp = max(p.n_glycan_mannose - 5.0, 0.0) * n_seq \
        + p.o_mannose_per_site * n_oglyc
    gdpmann = core_direct + via_dolmanp     # Dol-P-Man itself is made from GDP-Man
    dolmanp = via_dolmanp
    udpg = p.n_glycan_transient_glucose * n_seq

    # --- carbon accounting -------------------------------------------------
    c_prod = f.get("C", 0.0)
    c_prec = sum(AA_FORMULA[a]["C"] * n for a, n in draw.items() if n > 0)
    c_prec += 6 * (gdpmann + udpg) + 8 * uacgam + 34 * n_haem

    r = CostResult(
        name=spec.name, length_precursor=Lp, length_mature=Lm,
        product_formula=f, product_mass_da=mass, aa_draw=draw,
        atp=atp, gtp=gtp, o2=o2, h2o2=h2o2, nadph=nadph,
        gdpmann=gdpmann, uacgam=uacgam, udpg=udpg, dolmanp=dolmanp,
        haem=n_haem, carbon_in_product=c_prod, carbon_in_precursors=c_prec,
    )
    g = mass / 1e3            # mmol-scale: 1 mmol protein = mass/1000 g
    r.atp_per_g = atp / g
    r.nadph_per_g = nadph / g
    r.carbon_per_g = c_prec / g
    r.breakdown = {
        "atp_translation": atp_translation,
        "atp_chaperone": atp_bip,
        "atp_phosphorylation": atp_phos,
        "gtp_transport": gtp,
        "o2_disulfide": o2,
        "nadph_isomerisation": nadph,
        "gdpmannose_glycan": gdpmann,
        "udpglcnac_glycan": uacgam,
        "udpglucose_transient": udpg,
        "haem": n_haem,
        "n_sequon": n_seq,
        "n_disulfide": n_ss,
        "n_phosphosite": n_phos,
    }
    return r


# ----------------------------------------------------------------------------
# GEM reaction construction
# ----------------------------------------------------------------------------

def build_reactions(model, spec: ProteinSpec, p: CostParams,
                    rxn_prefix: str = "PROT_"):
    """Add synthesis + secretion reactions for `spec` to a cobra `model`.

    Returns (cost_result, synthesis_reaction, sink_reaction).
    The model is modified in place; wrap in `with model:` to undo.
    """
    import cobra

    r = compute_cost(spec, p)
    tag = rxn_prefix + spec.name

    prot_c = cobra.Metabolite(f"{tag}_c", name=f"{spec.name} (cytosol/secreted)",
                              compartment="c",
                              formula=formula_str(r.product_formula))

    stoich = {}

    def add(met_id, coeff):
        if coeff == 0:
            return
        m = model.metabolites.get_by_id(met_id)
        stoich[m] = stoich.get(m, 0.0) + coeff

    for a, n in r.aa_draw.items():
        add(AA_MET[a], -n)

    # translational and chaperone energy, as ATP equivalents
    add("atp_c", -r.atp)
    add("h2o_c", -r.atp)
    add("adp_c", r.atp)
    add("pi_c", r.atp)
    add("h_c", r.atp)

    # vesicular transport GTP
    add("gtp_c", -r.gtp)
    add("h2o_c", -r.gtp)
    add("gdp_c", r.gtp)
    add("pi_c", r.gtp)
    add("h_c", r.gtp)

    # Net water released by condensation.  The precursor is polymerised
    # (Lp-1 bonds, Lp-1 H2O released); the signal peptide is hydrolysed off
    # (1 H2O consumed) and, when recycled, hydrolysed to free amino acids
    # (sp_end-1 H2O consumed).  Net = Lp - sp_end - 1 = Lm - 1.
    if p.include_signal_peptide and p.recycle_signal_peptide:
        add("h2o_c", r.length_mature - 1)
    else:
        add("h2o_c", len(seq_full if p.include_signal_peptide else seq_mat) - 1)

    # oxidative folding
    add("o2_c", -r.o2)
    add("h2o2_c", r.h2o2)
    # futile isomerisation: NADPH -> NADP+ via glutathione reductase
    if r.nadph:
        add("nadph_c", -r.nadph)
        add("h_c", -r.nadph)
        add("nadp_c", r.nadph)
        # the electrons end up reducing O2 as well
        add("o2_c", -0.5 * r.nadph)
        add("h2o_c", r.nadph)

    # N- and O-glycan donors
    add("uacgam_c", -r.uacgam)
    add("udp_c", r.uacgam)
    add("gdpmann_c", -r.gdpmann)
    add("gdp_c", r.gdpmann)
    add("udpg_c", -r.udpg)
    add("udp_c", r.udpg)
    if p.recycle_transient_glucose and r.udpg:
        # UDP-Glc + H2O -> UDP + Glc: releasing the trimmed glucose as the
        # free sugar consumes one water per residue.
        add("glc_D_c", r.udpg)
        add("h2o_c", -r.udpg)

    # Phosphorylation is a phosphotransfer, not a hydrolysis: the kinase ATP
    # was charged above in the hydrolytic form (ATP + H2O -> ADP + Pi + H),
    # so for each site the water consumption and the free phosphate release
    # are reversed out and the phosphoryl group goes onto the protein instead.
    if r.breakdown["n_phosphosite"]:
        add("pi_c", -r.breakdown["n_phosphosite"])
        add("h2o_c", r.breakdown["n_phosphosite"])

    # haem b
    if r.haem:
        if "pheme_c" not in model.metabolites:
            hm = model.metabolites.get_by_id("pheme_m")
            hc = cobra.Metabolite("pheme_c", name="Protoheme", compartment="c",
                                  formula=hm.formula)
            model.add_metabolites([hc])
            tr = cobra.Reaction("PHEMEtm", name="Protoheme mitochondrial export")
            tr.bounds = (0.0, 1000.0)
            tr.add_metabolites({hm: -1.0, hc: 1.0})
            model.add_reactions([tr])
        add("pheme_c", -r.haem)

    stoich[prot_c] = stoich.get(prot_c, 0.0) + 1.0

    rxn = cobra.Reaction(tag, name=f"{spec.name} synthesis and secretion")
    rxn.bounds = (0.0, 1000.0)
    model.add_reactions([rxn])
    rxn.add_metabolites(stoich)

    # --- proton bookkeeping ------------------------------------------------
    # iMT1026v3 stores several metabolites in their physiological ionisation
    # state (Asp/Glu anionic, Lys/Arg cationic, sugar nucleotides
    # deprotonated) while the protein product is written as the neutral
    # polypeptide.  The resulting imbalance is purely in H and is closed with
    # free protons; nothing else is allowed to be unbalanced.
    resid = rxn.check_mass_balance()
    resid = {k: v for k, v in resid.items() if abs(v) > 1e-6}
    n_proton = 0.0
    if resid:
        if set(resid) - {"H", "charge"}:
            raise AssertionError(
                f"{tag}: reaction unbalanced in more than protons: {resid}")
        n_proton = -resid.get("H", 0.0)
        rxn.add_metabolites({model.metabolites.get_by_id("h_c"): n_proton})
        resid2 = {k: v for k, v in rxn.check_mass_balance().items()
                  if abs(v) > 1e-6 and k != "charge"}
        if resid2:
            raise AssertionError(f"{tag}: still unbalanced after H: {resid2}")
    r.breakdown["proton_balance_h"] = n_proton

    sink = cobra.Reaction("EX_" + tag, name=f"{spec.name} secretion (exchange)")
    sink.bounds = (0.0, 1000.0)
    model.add_reactions([sink])
    sink.add_metabolites({prot_c: -1.0})

    return r, rxn, sink


# ----------------------------------------------------------------------------
# Loading the target panel
# ----------------------------------------------------------------------------

def specs_from_uniprot_json(path: str,
                            phospho_from_annotation: bool = True
                            ) -> Dict[str, ProteinSpec]:
    with open(path) as fh:
        recs = json.load(fh)
    out = {}
    for name, d in recs.items():
        sp_end = d["signal"][0]["end"] if d["signal"] else 0
        n_ss = len(d["disulfide"])
        phos = 0
        o_gly = 0
        n_gly_ann = 0
        for m in d["mod_res"]:
            if "Phospho" in (m["desc"] or ""):
                phos += 1
        for c in d["carbohyd"]:
            desc = (c["desc"] or "")
            if desc.startswith("N-linked"):
                n_gly_ann += 1
            elif desc.startswith("O-linked"):
                o_gly += 1
        haem = 1 if ("globin" in name or "hemoglobin" in name) else 0
        out[name] = ProteinSpec(
            name=name, sequence=d["sequence"], signal_end=sp_end,
            n_disulfide=n_ss, n_o_glyc_site=o_gly,
            n_phosphosite=phos if phospho_from_annotation else 0,
            n_haem=haem, accession=d["accession"],
            notes=f"uniprot_Nglyc_annotated={n_gly_ann}",
        )
    return out


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    specs = specs_from_uniprot_json(
        os.path.join(here, "..", "data", "sequences", "targets.json"))
    p = CostParams()
    print(f"{'protein':38s} {'Lmat':>5s} {'SS':>3s} {'Nseq':>4s} {'P':>3s} "
          f"{'kDa':>7s} {'ATP/mol':>8s} {'ATP/g':>8s} {'C/g':>7s}")
    for n, s in sorted(specs.items()):
        r = compute_cost(s, p)
        print(f"{n:38s} {r.length_mature:5d} {int(s.n_disulfide):3d} "
              f"{int(s.sequons()):4d} {int(s.n_phosphosite):3d} "
              f"{r.product_mass_da/1000:7.2f} {r.atp:8.0f} "
              f"{r.atp_per_g:8.1f} {r.carbon_per_g:7.1f}")
