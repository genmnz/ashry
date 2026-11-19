# Chapter 4 — The stoichiometric ceiling

This chapter establishes what the metabolism of *Komagataella phaffii* permits. Every number is a maximum: it assumes a cell that makes no biomass, wastes nothing, and diverts its entire carbon and energy budget to one protein. No strain can exceed it. The purpose of computing it is not to predict a titre but to establish a denominator.

## 4.1 Maximum theoretical yields

Table 4.1 gives the maximum theoretical polypeptide yield for each panel protein on each of three carbon sources, at the default translation cost of 4.3 ATP-equivalents per peptide bond, with the full post-translational load charged.

**Table 4.1 — Maximum theoretical yield (g polypeptide per g substrate), iMT1026v3, zero growth**

| Protein | Glycerol | Glucose | Methanol |
|---|---|---|---|
| κ-casein | 0.670 | 0.598 | 0.468 |
| α-S2-casein | 0.666 | 0.597 | 0.469 |
| α-S1-casein | 0.659 | 0.593 | 0.466 |
| β-lactoglobulin | 0.653 | 0.585 | 0.460 |
| ovalbumin | 0.645 | 0.574 | 0.449 |
| β-casein | 0.640 | 0.577 | 0.453 |
| leghemoglobin C2 | 0.622 | 0.558 | 0.439 |
| lactoferrin | 0.616 | 0.551 | 0.431 |
| α-lactalbumin | 0.612 | 0.548 | 0.428 |

Two things are immediately visible, and the second is the point of the chapter.

**The protein hardly matters.** From κ-casein at the top to α-lactalbumin at the bottom, the range on glycerol is 0.612 to 0.670 g g⁻¹: a spread of **9.4%** across proteins that differ by a factor of 5.6 in chain length, by sixteen disulfide bonds, by five glycosylation sites, by thirteen phosphorylation sites and by the presence or absence of a haem cofactor. In carbon terms the convergence is tighter still: carbon yields on glycerol run from 0.829 to 0.920 C-mol per C-mol. These molecules are, from the cell's accounting point of view, nearly the same molecule.

**The carbon source matters a great deal.** Methanol yields are 30% below glycerol yields for every protein without exception (0.428–0.469 against 0.612–0.670). Glucose sits in between, about 10% below glycerol. The mechanism is in the model's own parameters: dissimilating methanol through formaldehyde to carbon dioxide to regenerate reducing power carries a growth-associated maintenance requirement of 166.8 mmol ATP per gram against 68.7 for glycerol, and the first oxidation step by alcohol oxidase passes electrons to oxygen through hydrogen peroxide, discarding their free energy entirely.

This has a direct process consequence. The AOX1 promoter, the field's standard strong inducible promoter, requires methanol. Choosing it therefore costs approximately a third of the stoichiometric ceiling before any other consideration. That is a quantified argument for the methanol-free induction systems reviewed in Chapter 2, and it is an argument that is usually made on safety and handling grounds rather than on yield.

### 4.1.1 Why the proteins converge

The convergence is not an artefact. Proteins are built from the same twenty monomers, and while those monomers differ substantially in biosynthetic cost — aromatic residues are expensive, alanine and glycine cheap — real proteins do not differ enough in composition for those differences to accumulate. β-casein is 16.7% proline and 9.6% glutamine; β-lactoglobulin is 13.6% leucine and only 4.9% proline; lactoferrin carries 4.9% cysteine against zero in β-casein and α-S1-casein. These are large compositional differences by the standards of protein chemistry. They produce a 9% difference in metabolic cost.

The two proteins at the bottom of the table, α-lactalbumin and lactoferrin, are there for the same reason: they are the two most heavily modified. Their polypeptide-basis yields are depressed by the diversion of carbon into glycan and by the oxygen consumed in disulfide formation, which §4.3 decomposes.

### 4.1.2 Sensitivity to the translation cost

The translation cost *k* is the one genuinely uncertain parameter in the construction. Scanning *k* from 2.0 to 5.5 ATP-equivalents per peptide bond moves yields by about 7% — for β-casein, from 0.669 to 0.626 g g⁻¹ — and does not change the rank order or the magnitude of the between-protein spread. No conclusion in this thesis depends on the choice.

### 4.1.3 Oxygen and carbon dioxide

At the optimum on glycerol, production of one gram of protein consumes 9.4–10.2 mmol of oxygen and releases 3.7–5.2 mmol of carbon dioxide. The oxygen figure is the one that matters industrially: it is nearly invariant across the panel, and combined with the oxygen transfer capacity of a large aerated vessel it is what sets the maximum volumetric productivity a plant can sustain. It is used in Chapter 8 to size the aeration duty.

## 4.2 Production against growth

Protein production and growth compete for the same carbon. Fixing the specific growth rate and re-maximising protein gives a linear trade-off: for β-casein, the ceiling falls from 0.640 g g⁻¹ at zero growth to 0.595 at µ = 0.05 h⁻¹, 0.550 at 0.10 h⁻¹ and 0.459 at 0.20 h⁻¹. Every panel protein behaves the same way, losing roughly 0.9 g g⁻¹ of yield per unit of specific growth rate.

The practical reading is that a decoupled process — grow the biomass, then hold it non-growing and productive — is worth up to a third of the yield relative to one in which production is coupled to fast growth. This is the stoichiometric argument for the two-phase fed-batch that the field already practises for empirical reasons.

## 4.3 Decomposing the post-translational load

Charging each modification explicitly, then removing it and recomputing, isolates its cost. Table 4.2 reports the result on glycerol. Two columns are needed because two different questions are being asked: the **mass-yield change** treats the modification as part of the product sold, while the **polypeptide penalty** counts only the protein backbone.

**Table 4.2 — Cost of the post-translational load (glycerol, 4.3 ATP/bond)**

| Protein | Modifications | Mass-yield change | Polypeptide penalty |
|---|---|---|---|
| β-lactoglobulin | 2 S–S | −0.02% | 0.00% |
| κ-casein | 1 pSer | +0.41% | 0.01% |
| β-casein | 5 pSer | +1.65% | 0.05% |
| α-S1-casein | 9 pSer | +3.04% | 0.09% |
| α-S2-casein | 13 pSer | +4.14% | 0.12% |
| ovalbumin | 1 S–S, 1 N-glycan, 2 pSer | +1.43% | 3.14% |
| leghemoglobin C2 | 1 haem, 1 pSer | −0.06% | 4.36% |
| lactoferrin | 16 S–S, 5 N-glycans | +2.78% | 8.40% |
| α-lactalbumin | 4 S–S, 1 N-glycan | +2.96% | 8.96% |

### 4.3.1 Phosphorylation is free

α-S2-casein carries thirteen phosphoserines. Installing all thirteen costs **0.12%** of the polypeptide yield. β-casein's five cost 0.05%. The reason is trivial once stated: a phosphate group costs one ATP and adds 80 Da to a 24,000 Da molecule, so the energetic burden of casein phosphorylation is three orders of magnitude below the cost of the polypeptide it decorates.

This matters because it settles an ambiguity the field's language does not. The statement "caseins are hard because they require phosphorylation" is true, but not for the reason the phrasing implies. The host is not being asked to pay an unaffordable energetic price. It is being asked to perform a reaction for which it has no enzyme: the Golgi casein kinase FAM20C that phosphorylates the Ser-x-Glu/pSer motifs of secretory phosphoproteins has no yeast counterpart. The casein problem is **catalytic, not energetic**, and the engineering consequence follows directly — transplant a kinase, do not optimise the energy budget. A heterologous kinase expressed alongside the casein would cost the cell essentially nothing in carbon.

This is, as far as the audit in Chapter 2 could establish, the first quantification of that statement.

### 4.3.2 Disulfide bonds are nearly free, too

β-lactoglobulin's two disulfides cost nothing measurable: the oxidative folding relay consumes half a mole of oxygen per bond, which against a protein's total oxygen demand of about 10 mmol per gram is negligible. Even lactoferrin's sixteen disulfides contribute only a small part of its penalty; most of lactoferrin's 8.4% is glycan.

This is worth emphasising because Chapter 6 finds that disulfide **density is the one sequence feature that predicts titre**. Those two results are only superficially in tension. Disulfide formation is stoichiometrically cheap and mechanistically demanding: it requires correct pairing among a combinatorial number of possibilities, protein disulfide isomerase to reshuffle incorrect pairs, and residence time in the endoplasmic reticulum. The model used here has no representation of any of that. That the energetic cost is negligible while the empirical association is the strongest in the panel is therefore not a contradiction but a localisation: it places the constraint squarely in the folding machinery, which is exactly where a stoichiometric model is blind.

### 4.3.3 Glycosylation is the expensive modification

α-lactalbumin loses 8.96% and lactoferrin 8.40% of their polypeptide yield to the post-translational load, and in both cases the glycan dominates. A single core Man₈GlcNAc₂ glycan diverts eleven sugar nucleotides; the GDP-mannose and UDP-GlcNAc are made from the same hexose phosphate pool that would otherwise become protein.

### 4.3.4 Hypermannosylation, and why reporting one yield number misleads

*K. phaffii* does not stop at the core glycan. Golgi mannosyltransferases extend the outer chain, and high-mannose structures far larger than Man₉ are routine. Scanning the mannose count per glycan from 9 to 100 gives the result in Figure 4.3, which is the most consequential single number in this chapter:

**Table 4.3 — Hypermannosylation (glycerol, α-lactalbumin, one sequon)**

| Mannose per glycan | Product mass | Mass yield (g g⁻¹) | Polypeptide yield (g g⁻¹) |
|---|---|---|---|
| 9 (ER core) | 16.0 kDa | 0.692 | 0.612 |
| 20 | 17.8 kDa | 0.710 | 0.564 |
| 60 | 24.3 kDa | 0.756 | 0.441 |
| 100 | 30.8 kDa | 0.786 | 0.362 |

The two columns move in **opposite directions**. On a mass basis, hyperglycosylation makes the process look better: the cell converts more of its substrate into secreted material, because mannose is a cheaper, less reduced material than protein. On a polypeptide basis it is a catastrophe: a single-sequon protein loses **41%** of the protein it could otherwise have made, and the material the customer receives is more than half sugar. Bovine lactoferrin, with five sequons, behaves the same way, its polypeptide yield falling from 0.616 to 0.374 g g⁻¹.

This divergence was found because an independent reimplementation of the cost engine disagreed about the product mass of lactoferrin (§3.4.1). The disagreement was a real error, and resolving it turned a one-line result into a two-sided one. It also carries a methodological warning beyond this thesis: a techno-economic model that reports grams of product per gram of substrate without stating whether glycan counts as product can be wrong by a factor of two in the direction that flatters the process.

The engineering consequence is unambiguous and quantitative. Glyco-engineered *K. phaffii* strains, developed principally to make therapeutic glycoproteins human-compatible, are justified for food proteins on **yield grounds alone**, independent of any functional or immunological argument. For α-lactalbumin the prize is up to 41% of the attainable protein.

## 4.4 The haem cofactor

Leghemoglobin's single haem b costs 4.36% of the polypeptide yield, a figure obtained after adding an explicit mitochondrial export of protohaem IX to the model, which synthesises it only in the mitochondrion. The number is small but not negligible, and it is a lower bound: it charges only the stoichiometry of the tetrapyrrole, not the regulatory or flux limitations of a pathway that normally supplies a few cytochromes and is here asked to supply a gram per litre of product.

The published route to high leghemoglobin titre is precisely the remodelling of haem metabolism alongside enhanced globin expression. This analysis says that work is not about energy. Haem synthesis is not expensive; it is slow and tightly regulated, and that is a different problem with a different solution.

## 4.5 What this chapter establishes

1. The stoichiometric ceiling for making food protein in *K. phaffii* is 0.61–0.67 g per g of glycerol, and which of these nine proteins is being made changes that by less than 10%.
2. Methanol costs about 30% of that ceiling, which is a quantified yield argument against AOX1-driven processes.
3. Phosphorylation is energetically free, so the casein problem is a missing enzyme and not an energy budget.
4. Disulfide bonding is also energetically nearly free, which locates its known difficulty in the folding machinery rather than in metabolism.
5. Glycosylation is the one expensive modification, and under this host's native hypermannosylation it can destroy 41% of the polypeptide yield while simultaneously improving the mass yield — so the choice of metric is not cosmetic.

What the chapter cannot establish is whether any of this explains the production record. A property that varies by 9% is a poor candidate for explaining an outcome that varies by orders of magnitude. The next chapter measures that outcome.
