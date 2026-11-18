# Chapter 7 — Where the flux would have to come from

Chapters 5 and 6 located the binding constraint outside metabolism. That does not make the metabolic analysis useless; it changes what it is for. If a strain is engineered so that folding and secretion no longer limit it, metabolism becomes the next constraint, and the model can say in advance which part of it will bind first and for which protein. This chapter reports that, for each panel protein, from two complementary analyses.

A caution applies throughout. These are predictions of *capability* from a stoichiometric model. They identify where flux would have to be redirected; they do not predict that redirecting it will raise a titre today, because today something else is limiting.

## 7.1 Amino-acid supply pressure

At the production optimum, the shadow price of each cytosolic amino-acid pool measures how much additional protein could be made per additional unit of that amino acid. Weighting each shadow price by the protein's own demand for that residue gives a per-protein picture of where supply pressure falls.

**Table 7.1 — The three amino acids under greatest demand-weighted supply pressure**

| Protein | First | Second | Third |
|---|---|---|---|
| β-lactoglobulin | Leu (13.6% of residues) | Lys | Glu |
| α-lactalbumin | Leu | Lys | Ile |
| leghemoglobin C2 | Lys | Leu | Phe |
| β-casein | **Pro (16.7%)** | Leu | Val |
| κ-casein | **Pro (11.8%)** | Tyr | Ile |
| α-S1-casein | Leu | Glu (12.6%) | Lys |
| α-S2-casein | Lys | Tyr | Glu |
| ovalbumin | Leu | Phe | Val |
| lactoferrin | Leu | Lys | Phe |

Two patterns are visible.

The first is generic: **leucine and lysine dominate almost everywhere**. Leucine is both abundant in proteins and expensive to make, and the combination puts it at the top for six of nine targets. This is a statement about protein synthesis in general rather than about food proteins specifically, and it is consistent with the amino-acid cost literature from Akashi and Gojobori onward.

The second is protein-specific and more useful: **the caseins break the pattern**. β-casein and κ-casein are the only proteins in the panel for which **proline** carries the greatest supply pressure, because they are 16.7% and 11.8% proline respectively — three to ten times the proline content of β-lactoglobulin or α-lactalbumin. α-S1-casein puts glutamate second, at 12.6% of its residues.

If an intact casein is ever produced at a titre where metabolism matters, the proline biosynthetic pathway is where the model says to look first — glutamate to glutamyl-phosphate to glutamate-5-semialdehyde to proline, through PRO1, PRO2 and PRO3 in yeast nomenclature. That prediction is specific to caseins, it falls out of composition rather than intuition, and it is directly testable by overexpressing the pathway in a casein-producing strain.

## 7.2 Flux scanning with enforced objective function

FSEOF steps the protein demand from zero to its maximum while maximising growth, and retains reactions whose flux moves monotonically. Reactions that rise are amplification candidates; reactions that fall are attenuation candidates.

**Table 7.2 — FSEOF summary (glycerol, 10 mmol gDW⁻¹ h⁻¹)**

| Protein | Max production (mmol gDW⁻¹ h⁻¹) | Amplification targets | Attenuation targets |
|---|---|---|---|
| α-lactalbumin | 0.0397 | 117 | 319 |
| leghemoglobin C2 | 0.0369 | 130 | 334 |
| β-lactoglobulin | 0.0329 | 117 | 327 |
| κ-casein | 0.0325 | 145 | 324 |
| α-S1-casein | 0.0264 | 128 | 312 |
| α-S2-casein | 0.0252 | 134 | 327 |
| β-casein | 0.0250 | 101 | 329 |
| ovalbumin | 0.0139 | 119 | 321 |
| lactoferrin | 0.0074 | 137 | 324 |

The molar maxima differ by a factor of five, but almost entirely because the proteins differ in size: lactoferrin is 689 residues against α-lactalbumin's 123, so five times fewer molecules carry the same mass. On a mass basis these collapse back to the narrow band of Chapter 4, which is the same result seen from another angle.

### 7.2.1 Which subsystems the targets fall in

Aggregating the amplification candidates across the panel by subsystem:

| Subsystem | Amplification targets |
|---|---|
| Glycolysis / gluconeogenesis | 54 |
| Extracellular transport | 29 |
| Exchange reactions | 27 |
| Alanine and aspartate metabolism | 17 |
| Peroxisomal transport | 17 |
| Glycine and serine metabolism | 16 |
| Threonine and lysine metabolism | 13 |
| Nucleotide metabolism | 12 |
| Pyruvate metabolism | 9 |

The picture is coherent and, read correctly, mildly deflationary. The amplification targets are overwhelmingly in **central carbon metabolism and amino-acid supply**, not in anything exotic. Enforcing protein production pushes flux up through glycolysis from glycerol, up through pyruvate carboxylase to replenish oxaloacetate for the aspartate family, and up through serine and glycine biosynthesis; it pulls flux down through the tricarboxylic acid cycle and oxidative phosphorylation, because carbon that becomes protein is carbon that is not burned.

Per-protein examples from the full table in `results/tables/fseof_targets.csv`: for α-S1-casein, enolase (ENO), phosphoglycerate kinase (PGK), glyceraldehyde-3-phosphate dehydrogenase (GAPD), pyruvate kinase (PYK) and pyruvate carboxylase (PC, 2.3-fold) rise monotonically, while glutamate dehydrogenase (GLUDxi), mitochondrial malate dehydrogenase (MDHm), the ATP synthase and the respiratory chain fall. Gene associations are reported with the model's locus identifiers.

### 7.2.2 What this is worth, honestly

The attenuation targets outnumber the amplification targets three to one, and most of them are respiratory. The model is saying that to make more protein you should burn less carbon — which is true and not actionable, since the cell needs that respiration to make ATP for the translation it is being asked to do more of.

The amplification set is more useful but is still generic: it is largely "increase glycolytic flux and amino-acid supply", which is the standard answer for any secreted product in this host. The genuinely protein-specific signal in this chapter is the proline result of §7.1, and it is specific because it comes from composition rather than from network topology.

This is reported as a modest result rather than inflated. FSEOF on a purely metabolic model produces metabolic targets; since Chapter 6 located the constraint in the secretory machinery, the targets that would matter most are ones this model cannot generate. A proteome-constrained secretory model would generate them, and Chapter 9 names that as the priority extension.

## 7.3 A sanity check worth recording

The unconstrained maximum growth rate in these simulations, at 10 mmol glycerol gDW⁻¹ h⁻¹ with no protein production, is 0.674 h⁻¹. Reported maximum specific growth rates for *K. phaffii* on glycerol are substantially lower, around 0.2–0.3 h⁻¹. The model is therefore optimistic about growth in the same way it is optimistic about production: it reports stoichiometric capability with no kinetic, proteomic or regulatory limitation.

This is not an error, and it does not affect the yields of Chapter 4, which are computed at zero or fixed growth. But it is a useful reminder of what the whole instrument is: an upper bound. Every ceiling in this thesis is a ceiling of the same optimistic kind, which is precisely why the gaps measured against them in Chapter 5 should be read as *lower bounds on the gap*, not as precise distances.
