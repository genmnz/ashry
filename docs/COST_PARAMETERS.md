# Cost-model parameters and their provenance

Every number in `src/protein_cost.py::CostParams`, where it comes from, and the
range used in sensitivity analysis. DOIs listed here were resolved against
Crossref; anything not verified is marked **unverified**.

## Host model

| item | value | source |
|---|---|---|
| base GEM | iMT1026 v3 — 2,237 reactions, 1,706 metabolites, 1,026 genes, 9 compartments | BioModels `MODEL1612130000`. Tomàs-Gamisans, Ferrer & Albiol, *PLoS ONE* 11:e0148031 (2016), doi:10.1371/journal.pone.0148031; v3 update: Tomàs-Gamisans, Ferrer & Albiol, *Microb Biotechnol* (2017), doi:10.1111/1751-7915.12871 |
| biomass equations | carbon-source specific: `BIOMASS_glyc`, `BIOMASS_meoh`, and 80:20 / 60:40 / 40:60 mixes | as distributed in the model |
| growth-associated ATP | 68.692 mmol ATP gDW⁻¹ (glycerol biomass reaction) | model, `BIOMASS_glyc` |
| non-growth maintenance | `ATPM` ≥ 2.9 mmol gDW⁻¹ h⁻¹ | model |
| host protein AA composition | `PROTEINS_glyc` pseudoreaction, mmol gDW⁻¹ | model; used for the compositional-strain feature |

The model is used as published. The only structural addition is a
mitochondrial protoheme export reaction (`PHEMEtm`, `pheme_m → pheme_c`),
needed because iMT1026 v3 contains protoheme only in the mitochondrion while
a cytosolically expressed globin must acquire it in the cytosol. Haem
biosynthesis in yeast is mitochondrial and the product is exported to the
cytosol, so this reaction adds no capability the organism lacks; it is
declared explicitly because it changes the feasible set.

## Translation

| parameter | default | range | basis |
|---|---|---|---|
| `atp_per_residue` | 4.3 | 4.0 – 5.2 | 2 ATP-equivalents for aminoacyl-tRNA charging (ATP → AMP + PPi consumes two high-energy phosphate bonds) + 1 GTP for eEF1A delivery + 1 GTP for eEF2 translocation = 4.0; the remainder covers initiation, termination and proofreading/mischarging. Written into the model as ATP-equivalent hydrolysis (ATP + H₂O → ADP + Pᵢ + H⁺). |
| `initiation_atp` | 2.0 | 1 – 4 | per chain, initiation + termination + release |

The whole precursor is translated, signal peptide included, so the energetic
cost scales with the precursor length while the amino-acid draw scales with
the mature chain (see `recycle_signal_peptide`).

## Signal peptide

| parameter | default | basis |
|---|---|---|
| `include_signal_peptide` | True | the signal peptide is always synthesised before cleavage |
| `recycle_signal_peptide` | True | signal-peptide peptidase and the downstream peptidases that clear the fragment are ATP-independent, so returning the residues as free amino acids is the conservative choice: it keeps the cost estimate a lower bound |

Water bookkeeping for this case is derived in the source: polymerising the
precursor releases (L_p − 1) H₂O, cleaving the signal peptide consumes 1 H₂O,
and hydrolysing the released fragment to free amino acids consumes
(L_sp − 1) H₂O, so the net is (L_mature − 1) H₂O released.

## Oxidative folding

| parameter | default | range | basis |
|---|---|---|---|
| `o2_per_disulfide` | 1.0 O₂ per disulfide, giving 1 H₂O₂ | fixed by chemistry | One disulfide releases two electrons; Ero1p passes them via FAD to O₂ in a two-electron step, so one FADH₂ reduces one O₂ to one H₂O₂. Tu & Weissman, *Mol Cell* 10:983 (2002), doi:10.1016/s1097-2765(02)00696-2. The reaction written into the model is electron-balanced: the chain loses 2 H per disulfide and one H₂O₂ (2 H) appears on the product side. |
| `isomerisation_cycles_per_disulfide` | 0.0 | 0 – 3 | futile reduction/re-oxidation cycles during isomerisation, each drawing NADPH through glutathione reductase. Baseline 0 so the stoichiometric estimate is a strict lower bound. |

Disulfides are formed only when `secreted=True`: the cytosol is reducing, so a
cytosolically expressed globin forms none even where UniProt annotates them in
the native protein.

## N-glycosylation

| parameter | default | range | basis |
|---|---|---|---|
| `n_glycan_glcnac` | 2 | fixed | the core GlcNAc₂ of the dolichol-linked precursor |
| `n_glycan_mannose` | 9 | 5 (glyco-engineered) – 14 (hypermannosylated) | *K. phaffii* transfers Glc₃Man₉GlcNAc₂, trims to Man₈GlcNAc₂, then extends with α-1,2/α-1,6 outer-chain mannose; secreted recombinant glycoproteins carry predominantly Man₈–Man₁₄ |
| `n_glycan_transient_glucose` | 3 | fixed | the three glucoses of the dolichol precursor, added and then trimmed by glucosidases I/II — paid for even though they do not stay on the protein |
| `recycle_transient_glucose` | True | — | the trimmed glucose returns to the cytosolic hexose pool; releasing it from UDP-Glc consumes one water per residue |

Donor split: the first five mannoses are drawn directly from GDP-mannose on
the cytosolic face of the ER; anything beyond Man₅, and all O-mannose, is
delivered as dolichyl-phosphate-mannose, which is itself made from
GDP-mannose, so the GDP-mannose draw is the total. Sugar-nucleotide donors and
the per-protein feature set (signal peptide, N- and O-glycosylation site
counts, disulfide count, localisation) follow the secretory-pathway
reconstruction of Feizi, Österlund, Petranović, Bordel & Nielsen, *PLoS ONE*
8:e63284 (2013), and the *P. pastoris* glycosylation GEM of Irani, Kerkhoven,
Shojaosadati & Nielsen, *Biotechnol Bioeng* (2015), doi:10.1002/bit.25863.

Sequons are counted as N-X-S/T with X ≠ P, overlapping matches included.
Sequon occupancy is **not** assumed to be complete; the default charges every
sequon, which is the upper bound on glycan cost, and the glyco-engineered
scenario (Man₅) plus a partial-occupancy scenario bracket it.

## O-mannosylation

| parameter | default | range | basis |
|---|---|---|---|
| `o_mannose_per_site` | 2 | 1 – 5 | *K. phaffii* O-mannosylates Ser/Thr with short α-1,2-linked mannose chains |

Sites are taken from UniProt O-linked annotation rather than predicted, so
this term is a floor: unannotated Ser/Thr in the host may also be modified.

## Phosphorylation

| parameter | default | basis |
|---|---|---|
| `atp_per_phosphorylation` | 1.0 | one kinase phosphotransfer per site |
| `phosphorylate` | False | wild-type *K. phaffii* and *T. reesei* do not phosphorylate casein; True only in the engineered PTM-competent scenario |

Written as a phosphotransfer, not a hydrolysis: the ATP is charged in the
hydrolytic form elsewhere in the reaction, so for each site the water
consumption and the free-phosphate release are reversed out and the phosphoryl
group is placed on the protein instead.

## Chaperones and traffic

| parameter | default | range | basis |
|---|---|---|---|
| `bip_atp_per_residue` | 0.0 | 0 – 0.5 | BiP/Kar2 ATPase cycles. Zero at baseline so the stoichiometric figure is a strict lower bound; this is the term through which sequence features (disorder, hydrophobic patches) are allowed to raise metabolic cost in the folding-burden scenarios. |
| `transport_gtp_per_molecule` | 6.0 | 3 – 20 | COPII budding, COPI retrieval and Rab/Ypt cycles; GTP usage per transport step follows Feizi *et al.* 2013. Per gram of product this term is negligible, and is included for completeness rather than effect. |

## Prosthetic groups

| parameter | default | basis |
|---|---|---|
| `haem_per_molecule` | 1 for monomeric globins, else 0 | one protoheme b per globin monomer, as assumed by Pentjuss *et al.*, *Sci Rep* 13:15816 (2023), doi:10.1038/s41598-023-42865-w, for soy leghemoglobin in *P. pastoris* |

## Validation of the implementation

1. Every reaction is checked with `cobra` mass balance. iMT1026 v3 stores
   Asp/Glu anionic, Lys/Arg cationic and the sugar nucleotides deprotonated,
   so reactions are closed with free protons and **any** residual in an
   element other than H raises an assertion.
2. The proton count required for β-lactoglobulin is exactly
   (n_Asp + n_Glu) − (n_Lys + n_Arg), which is the value predicted from the
   model's ionisation conventions and was not used in building the reaction.
3. All 36 proteins × secreted/cytosolic × phosphorylated/not — 144 variants —
   balance.
