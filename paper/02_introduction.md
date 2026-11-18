# Chapter 1 — Introduction

## 1.1 What precision fermentation is, and what it is not

Fermentation has been used to transform food for several thousand years. What distinguishes *precision* fermentation from that tradition is not the vessel, the organism or the sugar: it is the specificity of the instruction. In traditional fermentation a microbial consortium is given a substrate and allowed to do what its metabolism does — to acidify milk, to leaven dough, to produce ethanol. The product is the aggregate output of an organism behaving as itself. In precision fermentation the organism is given a gene it does not possess, and its protein synthesis machinery is redirected to manufacture one defined molecule, usually a single protein, which is then separated from the cells and sold as an ingredient.

The distinction matters because it determines what can go wrong. A traditional fermentation fails when the culture is contaminated or the conditions drift. A precision fermentation can fail in a much larger number of ways, because the host is being asked to do something it was never selected to do: to transcribe a foreign gene at high rate, to translate a messenger RNA whose codon composition belongs to another kingdom, to fold a polypeptide whose native folding environment was a mammary gland or a plant root nodule, to install chemical modifications it may not possess the enzymes for, to push the finished molecule out through a secretory pathway evolved for its own proteins, and to do all of this while still growing.

The technology is no longer speculative. Recombinant chymosin, produced in *Aspergillus niger* and *Kluyveromyces lactis*, has been used in the majority of industrial cheesemaking for decades and is the proof that the business model works. More recently, bovine β-lactoglobulin produced in the filamentous fungus *Trichoderma reesei* received a "no questions" letter from the United States Food and Drug Administration under GRAS Notice 863 in March 2020, and soy leghemoglobin produced in the methylotrophic yeast *Komagataella phaffii* — the protein responsible for the meat-like flavour and appearance of a widely sold plant-based burger — was cleared under GRAS Notice 737. Egg-white protein from *K. phaffii* followed under GRAS Notice 1104 in October 2023. These are the two hosts and several of the proteins that this thesis analyses, which means the work rests on an established and documented industrial reality rather than on a hypothetical one.

## 1.2 Why the proteins in this panel

Five product categories drive the field, and they map onto a panel of nine proteins analysed here.

**Caseins** (α-S1, α-S2, β and κ) make up roughly 80% of the protein in bovine milk and are what makes cheese behave like cheese. They are intrinsically disordered phosphoproteins that assemble into colloidal micelles stabilised by calcium phosphate nanoclusters nucleated on clusters of phosphorylated serine residues. They are the hardest target in the panel and also the most commercially valuable, because no whey protein can replace them in a melting, stretching cheese.

**Whey proteins** — β-lactoglobulin and α-lactalbumin — are small, globular, disulfide-bonded and far better behaved. β-lactoglobulin is the single most successful precision-fermented dairy protein to date; α-lactalbumin is the principal protein of human milk and a target for infant formula.

**Lactoferrin** is an iron-binding, antimicrobial milk protein with sixteen disulfide bonds and five N-glycosylation sites, and it is included here precisely because it carries the heaviest folding and modification load of anything in the panel.

**Ovalbumin** is the dominant egg-white protein, the target for animal-free egg products, and an unusual case because it is secreted without cleavage of an N-terminal signal peptide.

**Soy leghemoglobin C2** is a plant haemoglobin and the only cofactor-dependent protein in the panel; producing it requires the host to supply protohaem at a rate it does not normally need to.

Taken together the panel spans a wide range of the properties a host must cope with: intrinsic disorder against tight globular folds, zero to sixteen disulfide bonds, zero to five glycosylation sites, zero to thirteen phosphorylation sites, a cofactor requirement, and a nearly sixfold range of chain length. That spread is what makes a comparative analysis informative.

## 1.3 The problem this thesis addresses

The literature of this field names its central challenge consistently: achieving correct folding, achieving the right post-translational modifications, and scaling downstream purification affordably. The project brief that initiated this work names the same three. What the literature does not do is quantify them against one another.

This is not a trivial omission. "Caseins are hard because they require phosphorylation" is a causal claim with a measurable content: it says that the phosphorylation requirement imposes a cost that the host cannot bear. If that cost turns out to be negligible, the sentence is still true in some sense — yeast genuinely cannot phosphorylate casein the way a mammary cell does — but the *reason* it matters is completely different. It is not that phosphorylation is expensive; it is that the enzyme is absent and the product is therefore wrong, not scarce. Those two readings imply different engineering programmes: the first says improve the energetics, the second says transplant a kinase. Deciding between them requires a number.

The same ambiguity runs through every other claim in the field. Is N-glycosylation a problem because it burdens metabolism, or because yeast glycans are the wrong glycans? Is a long, disulfide-rich protein hard because it is expensive to build, or because the oxidative folding machinery of the endoplasmic reticulum saturates? Is leghemoglobin limited by the energy of haem synthesis or by the flux capacity of a pathway that normally supplies only the cell's own cytochromes? In every case, two mechanisms with very different remedies are being described by the same word, *bottleneck*, and the field's reviews move between them without distinguishing.

## 1.4 The question, and how it is made answerable

The question this thesis asks is:

> **For each protein in the panel, how much of the distance between what is theoretically possible and what has actually been achieved is explained by the cost of building the molecule, and how much is not?**

This is made answerable by a decomposition in three steps.

The first step establishes the **ceiling**. For each protein, its exact amino-acid composition, disulfide count, glycosylation sites, phosphosites and cofactor requirement are converted into an explicit synthesis and secretion reaction and installed into the genome-scale metabolic model iMT1026v3 of *K. phaffii*. Maximising that reaction under a fixed substrate supply gives the maximum theoretical yield in grams of protein per gram of glycerol, methanol or glucose: a hard upper bound that no strain, however engineered, can exceed while obeying the stoichiometry of its own metabolism.

The second step establishes the **floor**: what has actually been achieved. This required building a database of published titres from primary literature, because no suitable compilation exists. Every record carries a verbatim quotation of the sentence reporting the number, a citation, and a confidence grade, so that the comparison rests on evidence that can be checked rather than on recollection.

The third step is the **decomposition**. Expressing each published titre as a fraction of that protein's own ceiling converts incomparable numbers into a comparable one, and the residual — the part of the gap that the ceiling does not explain — becomes an object that can itself be analysed against the properties of the protein.

## 1.5 What is new here, stated conservatively

Honesty about novelty is more useful than enthusiasm about it, and the prior-art audit conducted for this thesis (Chapter 2) found a great deal of relevant prior work.

Computing per-protein biosynthetic costs in a metabolic model is established practice. Feizi and colleagues computed ATP, GTP and glycosylation-donor costs across the yeast proteome in 2013. Gutierrez and colleagues reconstructed the mammalian secretory pathway in 2020 and computed per-protein secretion costs and limits. The proteome-constrained model pcSecYeast built protein-specific secretion reactions from sequence and post-translational requirements for eight recombinant proteins, including a haemoglobin, and called the bottleneck for each. Predicting expression or secretion success from sequence features is likewise a developed field, from Presep for *P. pastoris* in 2013 through secretome-scale analyses in 2025, and the phrase "predicting protein producibility" was already used for filamentous fungi in 2017. A publicly visible but unpublished repository is, concurrently with this work, building translation, glycosylation and disulfide cost reactions on the same iMT1026v3 model.

None of those steps is claimed here as a discovery. They are used as instruments, with citation, in Chapters 3 and 4.

What has not been done, and what this thesis contributes, is the decomposition itself:

1. **Per-protein stoichiometric ceilings for this panel of named food proteins** in *K. phaffii*, resolved by carbon source and by post-translational component, including the separation of the glycoprotein mass yield from the polypeptide yield that a food application actually cares about.
2. **Each published titre expressed as a fraction of its own protein's ceiling**, over a curated and quotation-backed titre corpus — which turns the field's incommensurable numbers into a single measurable quantity, the gap.
3. **A direct test of what the residual gap tracks**, including the negative results, which turn out to be the informative ones.

## 1.6 Structure of the thesis

Chapter 2 reviews the field and reports the prior-art audit in full, including the work that comes closest to this one and exactly how close it comes. Chapter 3 sets out the computational methods, the data provenance rules and the verification procedures, including the independent reimplementation that cross-checked the central numbers. Chapter 4 computes the stoichiometric ceilings and decomposes the post-translational load. Chapter 5 presents the ceiling–gap measurement. Chapter 6 tests what the gap tracks and reports both the positive and the negative findings. Chapter 7 derives protein-specific metabolic engineering targets. Chapter 8 develops the techno-economic consequences. Chapter 9 discusses limitations, the confounds that the analysis cannot remove, and the minimal wet-laboratory programme that would test the predictions made here.
