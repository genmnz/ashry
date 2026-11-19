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

## 7.4 A per-protein engineering programme

The value of the decomposition to a developer is that it narrows the programme for each protein to the one or two interventions the evidence actually supports, and names what each intervention would and would not fix. This section collects that, protein by protein. It is the most directly usable output of the thesis, and every entry traces to a chapter rather than to judgement.

**Table 7.3 — What the analysis says to do, per protein**

| Protein | Binding problem, on the evidence | First intervention | What it will not fix |
|---|---|---|---|
| **β-casein** | No published titre anywhere; phosphorylation absent in host; proteolysis of a disordered chain | Protease-deficient background first, then a Fam20C-family kinase; proline supply only if a titre is ever reached where metabolism matters | Micelle function without phosphorylation, which is a product-identity problem rather than a yield problem |
| **α-S1-casein** | Same, with one reported production in *K. phaffii* and one quantitative titre in *B. subtilis* (56.9 mg L⁻¹) | Protease-deficient background; glutamate supply is second-ranked in §7.1 | — |
| **α-S2-casein** | No published titre anywhere | Nothing protein-specific can be said beyond the casein class result; this is a measurement gap first | — |
| **κ-casein** | Measured: 28–133 mg L⁻¹, 0.06% of a ceiling that is among the highest in the corpus; sources report proteolysis, aberrant O-glycosylation and a saturating copy-number response | Proteolysis, beyond *pep4* and *yps1*, which the 2026 source reports as insufficient; then O-glycosylation | Copy number. The published response saturates, so more copies is the one intervention the data argue against |
| **β-lactoglobulin** | Best-performing food protein at 6.1% of ceiling; nothing in the analysis identifies a protein-specific limit | Process intensification, not protein engineering. This is the one panel member where the generic FSEOF answer is the right answer | — |
| **α-lactalbumin** | 0.31% of ceiling, below lactoferrin and ovalbumin, contradicting the published expert ordering | Nothing in this analysis explains it. §5.2.2 shows the protein spans 115-fold across six records, so the first question is which process conditions produced the high end | Any sequence-derived remedy, since the spread is largely within the protein |
| **Lactoferrin** | 16 disulfides and 5 sequons; reaches 0.99% (human) and 0.11% (bovine) of ceiling | Oxidative folding capacity (PDI, UPR), then glycan engineering, which Chapter 4 prices at up to 41% of polypeptide yield under hypermannosylation | Species substitution. The order-of-magnitude human-versus-bovine difference in the corpus is a different sequence, not a different process |
| **Ovalbumin** | 0.89% of ceiling, and the largest within-protein spread in the corpus at 200-fold over four records | Process, emphatically. A 200-fold within-protein range means the protein is not the variable | — |
| **Soy leghemoglobin** | 2.75% of ceiling, the second-best food protein; haem supply is the recognised constraint | Haem pathway flux, as the published route already does. Chapter 4 prices the *stoichiometric* haem cost as real but modest, which places the constraint on flux capacity and catalysis rather than on carbon | Carbon or ATP supply for haem, which is not where the limit is |

Three class-level conclusions follow, and they are the ones worth carrying into a programme plan.

**The caseins need a protease programme, not a cost programme.** Every line of evidence points the same way: the ceiling is high, the cost of phosphorylation is negligible, and the primary sources report degradation. The remaining uncertainty is how large the protease programme has to be, and the honest answer from the literature is that the standard two knockouts are not enough.

**The whey proteins need process work, not protein work.** β-lactoglobulin is the best performer in the corpus and α-lactalbumin among the worst, from the same structural class with nearly identical ceilings. Whatever separates them is not in the molecules.

**Glycosylation is the one modification worth paying to change.** It is the only post-translational requirement in the panel with a material stoichiometric cost, the only one whose cost is computable, and the only one with a demonstrated engineering route in this host (§2.2.5). For lactoferrin specifically, the glycan question is simultaneously a yield question, a product-identity question and a regulatory question, which is a rare alignment of incentives.

## 7.5 Production white spaces, as a prospective direction

A by-product of building the corpus is a map of what has *not* been produced. These are recorded here as a prospective research direction rather than as a result of this thesis, because an absence in a literature search is weaker evidence than a measurement and because none of them strengthens the central argument.

Three classes of white space emerged.

**Panel proteins with no titre at all.** α-S2-casein and β-casein have no primary volumetric titre in any microbial host. Ovalbumin has a demonstrated secretion in *K. phaffii* with no stated titre. These are the cleanest publishable gaps in the panel, and §9.4 makes the first of them the leading item in the proposed wet-laboratory programme.

**Commercially named proteins absent from the production literature.** Several milk proteins with established food or nutraceutical interest — lactoperoxidase among them — appear in the dairy-science literature and in commercial discussion without a corresponding recombinant production record in either host. Whether that reflects technical difficulty, commercial disinterest or unpublished industrial work cannot be determined from a literature search, and the honest framing is as a question rather than an opportunity.

**Reporting white spaces rather than production white spaces.** The largest category is proteins that have been produced but whose titres were never reported in product mass, because the paper reported activity or fold-change instead. §2.3.3 argues that this is the single largest reason the corpus is smaller than the literature, and it is a white space that could be closed by re-measurement of existing strains rather than by new biology.

None of these is pursued here. They are listed because a reader planning work after this thesis will want the map, and because a map of absences is one of the few useful things a systematic corpus produces as a side-effect.
