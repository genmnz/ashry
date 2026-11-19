"""
Target protein definitions for the thesis panel.

Every annotation here (signal peptide boundary, disulfide count, phosphosite count,
N-glycosylation sites, reported molecular weight) was read from the corresponding
UniProt entry (rest.uniprot.org/uniprotkb/<accession>.txt) and is checked at build
time against the sequence actually used: `build_targets.py` recomputes the average
molecular mass from the sequence and refuses to proceed if it disagrees with the
UniProt SQ-line mass by more than 1 Da per 10 kDa.

`uniprot_mw` and `uniprot_len` are therefore not decoration: they are the checksum
that proves the sequence taken from a mirrored FASTA is the canonical UniProt one.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TargetAnnotation:
    key: str
    accession: str
    display_name: str
    category: str                 # dairy-casein | dairy-whey | egg | heme | reference
    signal_peptide_end: int       # 0 if none cleaved
    uniprot_len: int
    uniprot_mw: float
    disulfide_bonds: int
    n_glyc_sites: int
    phosphoserines: int
    haem_per_chain: int = 0
    source_file: str = "contaminants_source_perutz_2026_01.fasta"
    notes: str = ""


TARGETS: list[TargetAnnotation] = [
    TargetAnnotation(
        key="alpha_s1_casein", accession="P02662", display_name="alpha-S1-casein",
        category="dairy-casein", signal_peptide_end=15, uniprot_len=214,
        uniprot_mw=24529, disulfide_bonds=0, n_glyc_sites=0, phosphoserines=9,
        notes="9 phosphoserines (56,61,63,79,81,82,83,90,130); intrinsically disordered",
    ),
    TargetAnnotation(
        key="alpha_s2_casein", accession="P02663", display_name="alpha-S2-casein",
        category="dairy-casein", signal_peptide_end=15, uniprot_len=222,
        uniprot_mw=26019, disulfide_bonds=0, n_glyc_sites=0, phosphoserines=13,
        notes="13 phosphoserines; two cysteines can form an intermolecular bond",
    ),
    TargetAnnotation(
        key="beta_casein", accession="P02666", display_name="beta-casein",
        category="dairy-casein", signal_peptide_end=15, uniprot_len=224,
        uniprot_mw=25107, disulfide_bonds=0, n_glyc_sites=0, phosphoserines=5,
        notes="5 phosphoserines (30,32,33,34,50) forming the SerP cluster",
    ),
    TargetAnnotation(
        key="kappa_casein", accession="P02668", display_name="kappa-casein",
        category="dairy-casein", signal_peptide_end=21, uniprot_len=190,
        uniprot_mw=21269, disulfide_bonds=1, n_glyc_sites=0, phosphoserines=3,
        notes="Corrected against the verified UniProtKB feature table: one "
              "intramolecular disulfide (Cys-32-Cys-109) plus an inter-chain "
              "bond between the same cysteines in the casein polymer, and three "
              "phosphoserine positions (148, 170 alternate, 187), not one. "
              "Eight O-glycosylation sites are annotated; the host installs "
              "O-glycans of its own structure, so they are not charged as "
              "mammalian O-glycans.",
    ),
    TargetAnnotation(
        key="beta_lactoglobulin", accession="P02754", display_name="beta-lactoglobulin",
        category="dairy-whey", signal_peptide_end=16, uniprot_len=178,
        uniprot_mw=19883, disulfide_bonds=2, n_glyc_sites=0, phosphoserines=0,
        notes="disulfides 82-176 and 122-135; one free cysteine (121)",
    ),
    TargetAnnotation(
        key="alpha_lactalbumin", accession="P00711", display_name="alpha-lactalbumin",
        category="dairy-whey", signal_peptide_end=19, uniprot_len=142,
        uniprot_mw=16247, disulfide_bonds=4, n_glyc_sites=1, phosphoserines=0,
        notes="4 disulfides; calcium-binding loop (98,101,103,106,107)",
    ),
    TargetAnnotation(
        key="ovalbumin", accession="P01012", display_name="ovalbumin",
        category="egg", signal_peptide_end=0, uniprot_len=386,
        uniprot_mw=42881, disulfide_bonds=1, n_glyc_sites=1, phosphoserines=2,
        notes="internal, non-cleaved signal (22-48); secreted without N-terminal cleavage",
    ),
    TargetAnnotation(
        key="leghemoglobin_c2", accession="P02236", display_name="soy leghemoglobin C2",
        category="heme", signal_peptide_end=0, uniprot_len=145,
        uniprot_mw=15525, disulfide_bonds=0, n_glyc_sites=0, phosphoserines=1,
        haem_per_chain=1, source_file="leghemoglobin_soybn.fasta",
        notes="binds one haem b; the commercial Impossible Foods target",
    ),
    TargetAnnotation(
        key="lactoferrin_bovine", accession="P24627", display_name="bovine lactoferrin",
        category="dairy-whey", signal_peptide_end=19, uniprot_len=708,
        uniprot_mw=78056, disulfide_bonds=16, n_glyc_sites=5, phosphoserines=0,
        source_file="lactoferrin_bovine.fasta",
        notes="16 disulfides and 5 N-glycans: the heaviest folding/PTM load in the panel",
    ),
]

TARGETS_BY_KEY = {t.key: t for t in TARGETS}
