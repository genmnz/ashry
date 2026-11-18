# Precision Fermentation: Microbial Cell Factories for Animal-Free Dairy, Heme and Alternative Proteins

### The ceiling–gap decomposition: how far below its stoichiometric limit is each food protein, and why

**التخمير الدقيق: مصانع خلوية ميكروبية لإنتاج بروتينات الألبان والهيم والبروتينات البديلة دون الحاجة إلى الحيوانات**

*Graduation research project*

---

## Abstract

Precision fermentation — programming a microorganism by recombinant DNA to secrete a protein that an animal would otherwise have made — has moved from laboratory demonstration to supermarket shelf in under a decade. Bovine β-lactoglobulin from *Trichoderma reesei* and soy leghemoglobin from *Komagataella phaffii* are both cleared for sale in the United States. Yet the field's own framing of its central problem has remained qualitative: proteins are said to be hard to make because they fold poorly, because they require post-translational modifications the host cannot perform, or because purification is expensive. These claims are rarely quantified, and they are almost never compared against each other on a common scale.

This work asks a narrower and answerable question: **for a panel of nine food proteins, what does each candidate bottleneck actually cost, and which of them is binding?** The analysis is entirely computational and entirely reproducible from the accompanying repository.

Three things are established. First, the stoichiometric ceiling is nearly flat across the panel. Maximum theoretical yields computed by installing explicit, sequence-derived synthesis and secretion reactions into the genome-scale metabolic model iMT1026v3 of *K. phaffii* span only about 9% between the cheapest and the most expensive of the four caseins, β-lactoglobulin, α-lactalbumin, ovalbumin, soy leghemoglobin C2 and bovine lactoferrin, while the choice of carbon source moves the ceiling by roughly 30%. Within the post-translational load, phosphorylation is energetically free — charging α-S2-casein's thirteen phosphoserines costs under 0.12% of yield — whereas N-glycosylation is expensive and becomes dominant under the hypermannosylation that *K. phaffii* performs natively.

Second, realised production is nowhere near that ceiling. Joining the model-derived ceilings to a purpose-built database of 109 published titres, each carrying a verbatim evidential quotation and a citation, shows that the best reported titre for each panel protein lies between 16-fold and roughly 1900-fold below its stoichiometric ceiling, and that the spread between proteins in realised titre exceeds two orders of magnitude. A property that varies by 9% cannot explain an outcome that varies by a factor of a hundred. Metabolic cost is therefore excluded as the explanation of why some food proteins are harder to make than others.

Third, a direct test of what does explain it. Across 37 high-confidence records of secreted production in *K. phaffii*, covering 25 distinct proteins, the density of disulfide bonds is the only sequence feature significantly associated with the titre achieved (Spearman ρ = −0.46, p = 0.021). Maximum theoretical yield is not associated with titre at all (ρ = 0.04), confirming the first result empirically and independently, and predicted intrinsic disorder is not associated either, which complicates the usual explanation offered for the caseins. A cross-validated regression ranks proteins weakly but has no skill in predicting absolute titre against the trivial baseline; this negative result is reported rather than concealed, and is interpreted as evidence that published titres are dominated by how much strain and process engineering each protein has received rather than by the protein itself.

The practical consequences are developed in two further chapters: protein-specific metabolic engineering targets obtained by flux scanning with enforced objective function, and a techno-economic model in which every parameter carries a source and the result is reported against the stoichiometric cost floor implied by the computed yields. The cost analysis finds a floor near $1/kg of raw carbon against a modelled plant cost near $43/kg, and identifies recovery, titre and plant utilisation — not substrate price — as what determines whether precision-fermented proteins reach commodity economics.

The contribution of this thesis is not a new protein, a new strain or a new tool, and it is deliberately narrower than it first appears. Computing per-protein synthesis costs in a genome-scale model is not new: Feizi and co-workers did it across the yeast proteome in 2013, Gutierrez and co-workers reconstructed the mammalian secretory pathway and its per-protein costs in 2020, and pcSecYeast built protein-specific secretion reactions with per-protein bottleneck calls in 2022. Predicting producibility from sequence is not new either. Those steps are used here, with citation, as tools rather than claimed as findings.

What is new is the **decomposition**: computing each food protein's own stoichiometric ceiling, expressing every published titre as a fraction of *its own* ceiling rather than comparing titres to each other, and attributing the residual. That measurement has not been made for these proteins in these hosts, and it is what licenses the central claim — that the binding constraint on animal-free food proteins is not what it costs the cell to build them.

---

## ملخص

التخمير الدقيق هو برمجة الكائنات الدقيقة باستخدام تقنية الحمض النووي المؤتلف لإنتاج بروتينات حيوانية المنشأ دون الحاجة إلى الحيوان نفسه. انتقلت هذه التقنية خلال أقل من عقد من المختبر إلى الأسواق، إذ حصل بروتين بيتا لاكتوغلوبولين المنتج من الفطر *Trichoderma reesei* وبروتين الليغهيموغلوبين المنتج من الخميرة *Komagataella phaffii* على موافقات تنظيمية في الولايات المتحدة.

ومع ذلك، ظل وصف التحدي الأساسي في هذا المجال وصفاً نوعياً لا كمياً: يقال إن بعض البروتينات صعبة الإنتاج بسبب الطي البروتيني غير الصحيح، أو بسبب التعديلات بعد الترجمة التي لا يستطيع المضيف الميكروبي إجراءها، أو بسبب كلفة التنقية. هذه الادعاءات نادراً ما تُقاس، ونادراً ما تُقارن على مقياس واحد.

تطرح هذه الدراسة سؤالاً أضيق وقابلاً للإجابة: ما هي الكلفة الفعلية لكل عائق مفترض، وأيها هو العائق الحقيقي المُقيِّد؟ الدراسة حاسوبية بالكامل وقابلة للتكرار بالكامل.

توصلت الدراسة إلى ثلاث نتائج رئيسية. الأولى أن السقف الكيميائي الحيوي شبه ثابت: لا تتجاوز الفروق في العائد النظري الأقصى بين البروتينات التسعة نحو 9%، بينما يغيّر مصدر الكربون العائد بنحو 30%. كما تبيّن أن الفسفرة لا تكلف الخلية طاقياً تقريباً، في حين أن الغلكزة مكلفة، وتصبح العائق الأكبر عند حدوث فرط المَنَزة المميز لهذه الخميرة.

الثانية أن الإنتاج الفعلي أبعد ما يكون عن ذلك السقف: أفضل إنتاجية منشورة لكل بروتين تقع بين 16 ضعفاً وحوالي 1900 ضعف دون السقف النظري. لذلك لا يمكن لخاصية تتغير بنسبة 9% أن تفسر نتيجة تتغير بمئة ضعف.

الثالثة، وهي اختبار مباشر: من بين 37 سجلاً موثقاً تغطي 25 بروتيناً، كانت كثافة الروابط ثنائية الكبريتيد هي الخاصية التسلسلية الوحيدة المرتبطة إحصائياً بالإنتاجية. أما العائد النظري فلم يرتبط بها إطلاقاً، وكذلك الاضطراب البنيوي المتوقع.

خلاصة هذا العمل ليست بروتيناً جديداً ولا سلالة جديدة، بل قياس: التفكيك الكمي الأول لمواضع الكلفة الحقيقية في إنتاج بروتينات الغذاء في خميرة *K. phaffii*، والاختبار المباشر الأول لما إذا كانت تلك الكلفة تفسر السجل الإنتاجي المنشور. وقد تبيّن أنها لا تفسره.

---

## Declaration of computational scope

No wet-laboratory work was performed. Every number in this thesis is produced by code in the accompanying repository from publicly available sequences, models and published measurements, and every figure is regenerated from a table that the code writes. Where a quantity could not be obtained from a primary source, it is either omitted or explicitly labelled as an assumption. Predictions are called predictions throughout; none of them is a measurement of a real fermentation, and the final chapter sets out the minimal wet-lab programme that would test them.

## Software and data availability

All code, data, intermediate tables and figures are in the repository accompanying this thesis.

```
src/            analysis code (Python 3.13)
  protein_cost.py     per-protein synthesis reactions and yield computation
  targets.py          UniProt annotation of the nine panel proteins
  build_targets.py    sequence verification against UniProt mass and length
  features.py         sequence feature panel
  codon_opt.py        codon optimisation and construct design
  flux_targets.py     shadow prices and FSEOF engineering targets
  efficiency_gap.py   model ceiling versus published titre
  producibility.py    the sequence-to-titre model and its validation
  tea.py              techno-economic model
  figures.py          every figure in this document
data/
  models/             iMT1026 and iMT1026v3 genome-scale models (SBML)
  sequences/          verified panel sequences and harvested validation set
  literature/         curated titre database and 232-reference bibliography
  external/           codon usage table
results/
  tables/             every computed table
  figures/            every figure
  constructs/         synthesis-ready codon-optimised coding sequences
```


---

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


---

# Chapter 2 — Literature review and prior-art audit

This chapter has two jobs. The first is the ordinary one: to lay out what is known about precision fermentation, about the two hosts, about the nine proteins and about the computational methods used later. The second is less common in a thesis and more important here: to establish, by systematic search, precisely which parts of the proposed contribution have already been made by somebody else. A novelty claim that has not been audited is not a claim, it is a hope.

The literature corpus assembled for this thesis contains 232 references across nine topic clusters, each entry carrying the retrieved citation and, where available, a verbatim quotation of the fact it supports. Counts by cluster: industry and regulation 21; *Komagataella phaffii* as a host 34; *Trichoderma reesei* as a host 17; milk proteins 31; egg and haem proteins 17; computational methods 49; genome-scale modelling and protein cost 29; techno-economics and life-cycle assessment 17; prior art on producibility prediction 17.

---

## 2.1 The industrial and regulatory state of the field

Precision fermentation of food proteins passed from demonstration to commerce between 2018 and 2025, and the regulatory record is the cleanest way to see it.

Soy leghemoglobin produced in *Pichia pastoris* was the first of the modern wave: the United States Food and Drug Administration issued its response to GRAS Notice 737 in 2018, and in 2019 the Federal Register listed soy leghemoglobin as a colour additive exempt from certification (84 FR 37573), a separate and additional approval reflecting its role in the appearance of the product. Bovine β-lactoglobulin produced in *Trichoderma reesei* followed under GRAS Notice 863, with the agency's "no questions" response in March 2020. Egg-white protein produced in *Komagataella phaffii* (strain ATCC GSD-1235) was cleared under GRAS Notice 1104, closed 17 October 2023.

Beyond those three, the record thins into self-affirmation and trade press, and this thesis treats it accordingly. Animal-free casein has been self-determined as GRAS by at least one company (2024); lactoferrin has been claimed as self-affirmed GRAS and later reported as receiving FDA clearance (2024–2025); an ovalbumin producer submitted a formal GRAS notification in December 2024 without a published notice number traceable in the sources retrieved here; and an animal-free whey producer was reported in 2025 to have received a no-questions letter. These are recorded in the bibliography as industry-type references and are not used to support any quantitative claim in this thesis.

The financial context is worth one sentence, because it shapes what counts as a useful result. Fermentation-sector investment fell from $632 million in 2024 to $357 million in 2025 according to the Good Food Institute's industry analysis. In a contracting funding environment, work that tells a developer *which bottleneck to spend money on* is worth more than work that adds another candidate target.

## 2.2 *Komagataella phaffii* as a cell factory

*K. phaffii*, the methylotrophic yeast long known as *Pichia pastoris*, is the dominant host for secreted recombinant protein production in food biotechnology, and the one this thesis models. Its advantages are well documented: growth to very high cell density on simple defined media, a strong and tightly regulated methanol-inducible promoter (AOX1) alongside strong constitutive alternatives (GAP), efficient secretion of heterologous protein against a low background of native secreted protein, and an absence of the hyper-immunogenic terminal α-1,3-mannose found in *Saccharomyces cerevisiae*.

Four strands of the host literature bear directly on this work.

**Promoters and induction.** The AOX1 promoter remains the workhorse, but methanol handling at scale is a safety and cost problem, which has driven sustained work on methanol-free induction: retrofitting AOX1-based strains for methanol-independent expression, engineering trans-acting elements to decouple AOX1 from methanol, mapping the transcriptional regulatory networks of methanol-independent expression, and comparing alternative promoters such as ADH3 against the standard set. This matters for Chapter 4, where the stoichiometric penalty of methanol as a carbon source is quantified and turns out to be substantial.

**Secretion leaders.** The *S. cerevisiae* α-mating-factor prepro leader is the default secretion signal and is not always the best one; comparisons of the α-factor leader against native and endogenous signal peptides are a recurring theme, as is the discovery that *K. phaffii* YPS1-5 encodes a Bar1-like protease that degrades α-factor, and the finding that native secretion signals combined with higher induction temperature can outperform the default.

**Folding and the unfolded protein response.** Overexpression of a secreted protein imposes endoplasmic-reticulum stress; activation of the UPR in *P. pastoris* requires splicing of HAC1 mRNA, Ire1 participates in cytosolic and nuclear quality control, and engineering translocation and the UPR has been shown to raise secretion of a difficult human enzyme. This is the mechanism that Chapter 6 implicates when disulfide density turns out to be the one sequence feature associated with titre.

**Glycosylation.** *K. phaffii* transfers a core Man8GlcNAc2 glycan in the endoplasmic reticulum and then extends it in the Golgi, producing high-mannose structures that are not the mammalian structures a food protein would carry naturally. Genome-scale metabolic modelling of native and humanised glycosylation in this host already exists (Irani et al. 2015, 10.1002/bit.25863) and is the direct ancestor of the glycosylation accounting used in Chapter 4.

## 2.3 *Trichoderma reesei* as a host

*T. reesei* is the other industrially proven host, and the one that produced the first regulatory-cleared precision-fermented dairy protein. Its distinguishing property is secretory capacity: the organism was selected for decades for cellulase titres measured in tens of grams per litre, and that capacity can be redirected. The classic enabling trick is fusion to a carrier, most often cellobiohydrolase I, which improves secretion of otherwise poorly secreted heterologous proteins; hydrophobin fusions serve a related purpose for intracellular production.

Two practical problems recur. The first is proteolysis: the organism secretes proteases that degrade heterologous product, and protease-deletion strains are a standard remedy. The second is the production load itself, examined at genome scale. Both limit how far the host's cellulase-scale capacity transfers to a foreign protein.

The food-protein literature in this host is thin but decisive: the VTT work producing bovine β-lactoglobulin and hen ovalbumin in *T. reesei* by precision fermentation is the primary source for the benchmark titres used in Chapter 5, and the quantity of comparable fungal data is one of the limitations recorded in Chapter 9. Only eight of the 109 titre records compiled for this thesis are from *T. reesei*, and this is a property of the literature — fungal papers report activity or fold-change far more often than product mass — rather than an artefact of the search.

## 2.4 The proteins

### 2.4.1 Caseins and the phosphorylation problem

The caseins are not globular proteins and should not be analysed as if they were. They are intrinsically disordered phosphoproteins whose biological function is to carry calcium and phosphate at concentrations far above the solubility limit without precipitating, and whose food function — gelation, rennet coagulation, the melt and stretch of cheese — follows from that.

The mechanism is now well characterised. Clusters of phosphorylated serine residues sequester amorphous calcium phosphate as nanoclusters of defined size, and the casein micelle is a sequestration structure built on that principle. The quantitative nanocluster model has been developed over three decades by Holt and colleagues and refined into explicit ion-equilibrium models of the micelle. The direct experimental demonstration that matters most for precision fermentation is that dephosphorylated caseins lose the ability to form micelles: the modification is not decorative.

This is the point at which the field's language becomes ambiguous, and the ambiguity is what Chapter 4 resolves. The statement "caseins are hard because they need phosphorylation" can mean that the phosphorylation is metabolically expensive, or that the host lacks the kinase. Chapter 4 shows the first reading is quantitatively false and the second is the whole of the problem.

### 2.4.2 Whey proteins

β-lactoglobulin is a 162-residue lipocalin with a well-characterised eight-stranded β-barrel, two disulfide bonds and a free cysteine, first solved in 1986 and extensively studied as a ligand binder. α-lactalbumin is a 123-residue calcium-binding protein with four disulfide bonds, homologous to lysozyme, and the regulatory subunit of lactose synthase. Both are small, globular, and free of essential post-translational modification, which is why the field's reviews place them in the tractable tier — a judgement this thesis tests rather than assumes.

### 2.4.3 Lactoferrin

Bovine lactoferrin is a 689-residue bilobal iron-binding glycoprotein with sixteen disulfide bonds and five N-glycosylation sites. It is commercially attractive and biophysically the most demanding target in the panel, which is exactly why it is included: if folding load rather than metabolic cost is what limits production, lactoferrin is where that should be visible.

### 2.4.4 Ovalbumin

Ovalbumin is a 386-residue serpin-family protein that is secreted without cleavage of an N-terminal signal peptide, carrying instead an internal non-cleaved signal. It has one disulfide bond, one N-glycosylation site and two phosphoserines. Recombinant production data are sparse: essentially one primary experimental source in *T. reesei*, with company life-cycle assessments and a demonstration of secretion in *K. phaffii* that reports no titre.

### 2.4.5 Soy leghemoglobin

Leghemoglobin C2 is a 145-residue plant globin that binds one haem b. Production in yeast therefore requires the host to supply protohaem at a rate far above its own needs, and the published route to high titre is precisely that: enhanced globin expression combined with remodelling of haem metabolism. Related work engineering haem supply and limiting haemoglobin degradation in yeast, and metabolic engineering of *S. cerevisiae* for haem itself, establishes the pathway as the recognised constraint. Chapter 4 quantifies the stoichiometric part of that constraint and finds it to be real but modest, which places the weight on flux capacity and catalysis instead.

## 2.5 Computational methods used in this field

The methods cluster of the bibliography (49 references) covers the tools this thesis uses or deliberately declines to use.

**Structure and disorder.** AlphaFold made high-confidence structure prediction routine, and protein language models extended it to single-sequence inference. For intrinsically disordered proteins, however, structure predictors are the wrong instrument; dedicated disorder predictors (IUPred3, flDPnn, metapredict) and comparative evaluations of AlphaFold2 against them are the appropriate reference. This thesis uses a transparent, dependency-free disorder estimate (the charge–hydropathy FoldIndex of Prilusky and colleagues) as its primary disorder feature, for reasons of reproducibility set out in Chapter 3, and treats the resulting disorder values as a weak measurement — a limitation that matters for the interpretation of the null result in Chapter 6.

**Post-translational modification prediction.** NetPhos, GPS and MusiteDeep predict phosphorylation sites; sequon scanning predicts N-glycosylation. This thesis uses annotated UniProt modification sites in preference to predicted ones for the nine panel proteins, and sequon counts for the wider validation set, which is stated as an asymmetry in Chapter 3.

**Signal peptides and localisation.** SignalP 6.0 and DeepLoc 2.0 are the standard tools. They are discussed but not run here, because every construct designed in Chapter 4 uses a single common secretion leader, which removes signal-peptide choice as a variable rather than predicting it.

**Codon usage.** The codon adaptation index of Sharp and Li remains the standard measure. Its correct computation requires a reference set of highly expressed genes; Chapter 3 explains why only a whole-genome table was available to this analysis and what that weakens.

**Aggregation.** TANGO and related predictors of aggregation propensity exist and would be a natural addition to the feature panel; they are listed as future work in Chapter 9 rather than used, to keep the feature count defensible at the sample size available.

## 2.6 Genome-scale metabolic models of *K. phaffii*

Four generations of model exist for this organism: PpaMBEL1254, iLC915, the iMT1026 lineage, and the recent iPichia consensus model with its subsequent gene–protein–reaction curation. This thesis uses **iMT1026v3** (Tomàs-Gamisans et al. 2017, 10.1111/1751-7915.12871), which fine-tunes the iMT1026 reconstruction for improved prediction of growth on glycerol and methanol and carries separate biomass equations for each carbon source — a feature that is directly load-bearing in Chapter 4, where the carbon-source dependence of the yield ceiling is the largest effect found.

Related modelling work in this host includes contextualised models that reveal growth-rate-dependent metabolic effects, comparative genome-scale analysis used to select a production strain background, a constraint-based estimate of recombinant protein production, and the glycosylation-aware model already mentioned. The proteome-constrained modelling tradition — GECKO, ME-models, and the yeast proteome-constrained work that improves recombinant protein production predictions — represents the methodological frontier, and Chapter 9 identifies porting this analysis onto a proteome-constrained *K. phaffii* model as the single most valuable extension.

On the cost side, the conceptual foundation is Akashi and Gojobori's demonstration that amino acids differ systematically in biosynthetic cost and that proteomes are composed accordingly, extended to yeast specifically and more recently tied to stability and abundance.

## 2.7 Techno-economics and sustainability

Published cost estimates for precision-fermented protein diverge enormously. The Good Food Institute's meta-analysis of public techno-economic models found figures spanning three orders of magnitude, driven by differing assumptions rather than by differing biology, and its European arm's 2025 analysis placed food-grade α-lactalbumin near $24/kg with high-purity grades near $100/kg. For reference, commodity whey protein trades at a few dollars per kilogram, and the benchmark repeatedly cited for commodity competitiveness is under $20/kg.

Peer-reviewed techno-economic analysis specific to precision fermentation of food proteins barely exists. The closest rigorous anchors are Humbird's scale-up economics for cultured meat — whose treatment of bioreactor capital, oxygen transfer and media cost transfers directly — and the single-cell protein literature, which has several recent quantitative analyses. Downstream processing is separately reviewed and is repeatedly identified as the cost driver for food-grade products, because chromatography designed for pharmaceutical purity is not affordable at food prices; a demonstrated alternative is polyphosphate precipitation of β-lactoglobulin from *P. pastoris*, which raised protein content from 26 to 72 weight per cent while preserving emulsification.

Life-cycle assessments report large reductions in greenhouse-gas emissions, water and land use relative to bovine milk protein, but the range is wide and electricity-mix dependent, and dissenting analyses exist. Chapter 8 reports ranges and dissent rather than a single headline figure.

## 2.8 Prior-art audit: what has already been done

This section states, as precisely as the search permits, which parts of the proposed contribution are already claimed. It is based on a targeted audit of roughly 220 screened records with verified identifiers.

**Already done: per-protein biosynthetic cost in a metabolic model.** Feizi and colleagues (2013, 10.1371/journal.pone.0063284) modelled the protein secretory machinery in *S. cerevisiae* at genome scale and computed per-protein costs in ATP, GTP, GDP-mannose and UDP-GlcNAc across the proteome from essentially the same features used here. Gutierrez and colleagues (2020, 10.1038/s41467-019-13867-y) reconstructed the mammalian secretory pathway and computed per-protein metabolic costs and secretion limits, together with which features most affect secretion, in a CHO and human context. **This step is therefore not novel and is not claimed as such.**

**Already done: protein-specific secretion reactions with bottleneck attribution.** The proteome-constrained model pcSecYeast (Li and Nielsen 2022, 10.1038/s41467-022-30689-7) constructs protein-specific secretion reactions from sequence and post-translational requirements for eight recombinant proteins, including a haemoglobin, performs cross-validated feature-importance analysis, and makes explicit per-protein bottleneck calls. This is the closest methodological prior art to Chapter 6 and anticipates the general question "which bottleneck binds". **It is cited as the method's origin rather than competed with.**

**Already done: predicting producibility from sequence, including in fungi.** Presep (2013, 10.1371/journal.pone.0079749) predicts secretion propensity specifically in *P. pastoris*. Dykstra, Rousu and Arvas (2017, 10.1101/138560) used the term "predicting protein producibility" for filamentous fungi. Large-scale empirical analyses — 11,430 recombinant protein production experiments (10.1371/journal.pcbi.1009461), the human secretome determinants study (10.1073/pnas.2506036122), deep protein representations for expression prediction, ExpressUrself, PERISCOPE-Opt — populate this space thoroughly, and the field's own opinion literature asks openly whether protein expression can be "solved". The biologics developability-index tradition establishes composite sequence-based scores as a legitimate construct. **A "producibility index" is therefore not a novel object, and this thesis does not claim one.** An earlier framing of this work did; the audit retired it.

**Already done, and concurrent: the same host and model.** A publicly visible, unpublished repository (github.com/RaghavAcharya/kphaffii-metabolic-bottlenecks, last pushed October 2026) implements translation, glycosylation, disulfide and COPII cost builders on iMT1026v3 in *K. phaffii* with FSEOF and a per-protein nutrient-cost pipeline. No associated paper was found. This is recorded here as concurrent independent work on overlapping ground, which is the honest description.

**Already done: qualitative tractability ranking of milk proteins.** A 2026 review in *Comprehensive Reviews in Food Science and Food Safety* (10.1111/1541-4337.70618) states that α-lactalbumin and β-lactoglobulin are the most tractable targets given minimal post-translational-modification dependency, and places caseins and lactoferrin in a harder tier. The ordering this thesis might otherwise have claimed to discover is therefore already in print — as an expert judgement, with no score, no stoichiometry, no model and no validation against titres.

**Not found, and claimed here: the ceiling–gap decomposition.** No retrieved work computes, for a panel of named food proteins in *K. phaffii* or *T. reesei*, the maximum theoretical yield of each protein, expresses each published titre as a fraction of *its own* protein's ceiling, and attributes the residual. A fluxomic study of *K. phaffii* re-examined during the audit was confirmed to report no leghemoglobin or haem yield. The components exist; this particular assembly and the measurement it produces do not.

## 2.9 What the audit implies for this thesis

Three consequences follow, and all three are adopted.

First, Chapters 3 and 4 **concede** the prior art explicitly at the point of use. The synthesis-cost machinery is presented as an application of Feizi, Gutierrez and pcSecYeast to a panel they did not cover, not as an invention.

Second, the contribution is **narrowed to the measurement**: the ceiling, the gap expressed as a fraction of each protein's own ceiling, and what the residual does and does not track. This is a smaller claim than the project began with and a defensible one.

Third, the fact that the qualitative ordering is already published turns a potential weakness into a design feature. If this analysis recovers the published expert ordering from first principles, that is a validation of the method, provided — and only provided — the expectation is declared in advance of looking. It is declared here: the literature predicts whey proteins easiest, caseins and lactoferrin hardest. Chapter 6 reports what the data say, including where they contradict that expectation.

---

*A note on the bibliography, and a warning.* For a minority of entries no authoritative record returned an author list during retrieval; those entries carry "Not retrieved" in the author field rather than a guessed one, and are cited in this text by title and venue.

More seriously: a verification pass over the corpus found that **digital object identifiers which had been inferred rather than resolved were wrong roughly half the time**, with 28 incorrect identifiers caught in a single sweep. An inferred DOI looks exactly like a resolved one and fails silently, which makes this the most dangerous class of error in a literature-heavy thesis. Every DOI and PubMed identifier across all 306 bibliographic records is therefore being re-resolved against Europe PMC and Crossref, and **no identifier in this document should be treated as verified until that pass is complete and recorded**. Identifiers quoted in §2.8, which came from the targeted prior-art audit, were individually resolved at the time of retrieval; the remainder are pending. This is stated here rather than discovered by an examiner.


---

# Chapter 3 — Materials and methods

Everything in this chapter is computational. The governing principle is that any number appearing later in this thesis must be regenerable by running code in the accompanying repository against data files whose provenance is recorded. Where that principle could not be met — and there are three such places, all caused by network restrictions on the analysis machine — the compromise is stated explicitly here rather than buried.

## 3.1 Software environment

Analyses were performed in Python 3.13 using COBRApy 0.32.1 for constraint-based modelling with the GLPK linear-programming solver, Biopython for sequence analysis, pandas and NumPy for data handling, scikit-learn for regression and cross-validation, SciPy for statistics, and Matplotlib for figures. No commercial software, no graphics-processing hardware and no cloud compute service was used; the entire analysis runs on a four-core machine in under an hour.

## 3.2 The metabolic model

The genome-scale metabolic model **iMT1026v3** of *Komagataella phaffii* was used throughout (Tomàs-Gamisans et al. 2017, 10.1111/1751-7915.12871). As loaded, it contains 2,237 reactions, 1,706 metabolites and 1,026 genes. Two properties made it the right choice over the alternatives.

First, it carries **separate biomass and macromolecular composition equations for growth on glycerol and on methanol** (BIOMASS_glyc and BIOMASS_meoh, with corresponding PROTEINS_glyc and PROTEINS_meoh amino-acid composition reactions). Since the carbon-source effect turns out to be the largest single effect in Chapter 4, a model that treats methanol growth with its own composition and maintenance parameters is not a convenience but a requirement. The growth-associated maintenance term differs substantially between them (68.7 against 166.8 mmol ATP per gram of biomass), which encodes the known energetic penalty of methanol dissimilation.

Second, it is distributed as standard SBML and loads without curation into COBRApy, which keeps the pipeline reproducible.

The earlier iMT1026 reconstruction and the iLC915 model are included in the repository for comparison but are not used for the reported results.

## 3.3 Target proteins and sequence provenance

### 3.3.1 The panel

Nine proteins were analysed: bovine α-S1-casein (UniProt P02662), α-S2-casein (P02663), β-casein (P02666) and κ-casein (P02668); bovine β-lactoglobulin (P02754) and α-lactalbumin (P00711); hen ovalbumin (P01012); soybean leghemoglobin C2 (P02236); and bovine lactoferrin (P24627).

### 3.3.2 Sequence verification, and why it was necessary

The analysis machine could not reach UniProt, NCBI, EBI or RCSB; only GitHub and package registries were accessible. Sequences were therefore recovered from UniProt-derived FASTA files mirrored in public repositories, which creates an obvious risk: a mirrored file may carry a truncated, variant or mislabelled record.

That risk was closed by a verification rule applied before any sequence entered the analysis. For each protein, the UniProt entry's stated sequence length and molecular mass were obtained from the entry's own text record, and the sequence recovered from the mirror was accepted **only if its length matched exactly and its molecular mass, recomputed from average residue masses, agreed to within 1 Da per 10 kDa**. All nine panel proteins passed. The check is implemented in `src/build_targets.py` and re-runs on every build, so a corrupted data file causes a loud failure rather than a quiet wrong answer.

For the wider validation set of Chapter 6, a second rule was used: a sequence was accepted when **two or more independent repositories carried byte-identical records** for the same accession. Of 24 accessions harvested this way, 23 met the two-repository consensus criterion and one is flagged as single-source in the manifest.

This is a workaround and is declared as one. With direct database access the same pipeline runs unchanged against the REST endpoint, and re-verification against UniProt is listed in Chapter 9 as a required pre-submission task.

### 3.3.3 Annotation

Signal peptide boundaries, disulfide bond counts, N-glycosylation sites, phosphorylation sites and cofactor requirements were taken from the UniProt feature table of each entry and recorded in `src/targets.py` with the position lists. Two annotation decisions were made explicitly:

- **β-lactoglobulin is treated as having two disulfide bonds**, not three. UniProt lists three DISULFID features (82–176, 122–135, 122–137), but the last is an alternate annotation of the same bond; the protein has two disulfides and one free cysteine. This resolution is recorded because an independent reimplementation initially parsed three.
- **The leghemoglobin accession is P02236** (soybean leghemoglobin C2, 145 residues, 15,525 Da). The nearby accession P02234 is leghemoglobin alpha of *Phaseolus vulgaris*, a different species, and was rejected during cross-checking.

Mature chains were used throughout: the signal peptide is cleaved during secretion and does not appear in the product. Ovalbumin is the exception, having an internal non-cleaved signal, and is therefore analysed at full length.

## 3.4 Per-protein synthesis and secretion reactions

This is the step that prior work established and this thesis applies. Feizi and colleagues (2013) computed per-protein costs across the yeast proteome; Gutierrez and colleagues (2020) did the equivalent for the mammalian secretory pathway; pcSecYeast (Li and Nielsen 2022) built protein-specific secretion reactions from sequence and post-translational requirements. The construction below follows that tradition and claims no novelty for the mechanism, only for the panel it is applied to and the comparison it enables.

For a protein of mature length *L* with amino-acid counts *n<sub>i</sub>*, a synthesis reaction producing one millimole of polypeptide is added to the model:

> Σ<sub>i</sub> *n<sub>i</sub>* · (amino acid)<sub>i</sub> + *k*(*L*−1) ATP + *k*(*L*−1) H₂O → polypeptide + *k*(*L*−1) ADP + *k*(*L*−1) P<sub>i</sub> + *k*(*L*−1) H⁺ + (*L*−1) H₂O

with the post-translational terms added to the same reaction:

- **Translation cost** *k* = 4.3 ATP-equivalents per peptide bond by default (two for aminoacyl-tRNA charging, since ATP → AMP + PP<sub>i</sub> is two high-energy bonds; two GTP for elongation; a small proofreading term). The model's own biomass equation lumps translation into growth-associated maintenance, so it must be charged explicitly for a non-biomass protein. Every reported result is accompanied by a sensitivity scan over *k* ∈ {2.0, 4.3, 5.5}.
- **Disulfide bond formation**: 0.5 O₂ consumed and one H₂O released per bond, representing the Ero1–PDI relay that passes electrons from the forming disulfide to molecular oxygen.
- **N-glycosylation**: per occupied sequon, 2 UDP-GlcNAc and *m* GDP-mannose consumed, releasing UDP and GDP. The default *m* = 9 corresponds to the core Man₈GlcNAc₂ transferred in the endoplasmic reticulum, which is the conservative floor; Golgi outer-chain extension is scanned at *m* ∈ {9, 20, 60, 100} to represent the hypermannosylation characteristic of this host.
- **Phosphorylation**: one ATP → ADP per phosphoserine.
- **Haem**: one protohaem IX per chain for leghemoglobin. iMT1026v3 synthesises protohaem only in the mitochondrial compartment (pheme_m), so an explicit mitochondrial export reaction was added to make the cofactor available to a cytosolic apoprotein. This addition is physiologically real but is flagged, since it is a modification to the published model.

A demand reaction then removes the finished protein from the system, standing in for secretion and harvest.

### 3.4.1 Product mass: a correction worth recording

An early version of this analysis charged the cell for glycans, phosphate and haem but computed the yield using the mass of the **polypeptide alone**. That is inconsistent: the modification mass is paid for and leaves the cell, so it must be credited somewhere. The error was found by an independent reimplementation of the same engine, which computed bovine lactoferrin's product mass as 85.44 kDa against the 76.14 kDa polypeptide — a 9.3 kDa discrepancy exactly equal to five core glycans.

The resolution adopted is to compute and report **both** yields:

- **Product-basis yield**, in grams of the secreted molecule including its modifications per gram of substrate (glycan residues at 203.195 Da for HexNAc and 162.142 Da for hexose, phosphate at 79.980 Da, haem b at 616.487 Da, less 2.016 Da per disulfide).
- **Polypeptide-basis yield**, counting only the backbone.

These answer different questions and diverge sharply under hypermannosylation, which is itself one of the findings of Chapter 4. Where a single number is needed — in particular when comparing against published titres, which are measured as protein — the **polypeptide basis** is used, because it is the conservative choice and because mannan is not what a food application is buying.

## 3.5 Yield computation

The substrate exchange reaction was constrained to 10 mmol gDW⁻¹ h⁻¹ for the carbon source under test, all other carbon exchanges were closed, oxygen was left unconstrained, and the non-growth maintenance requirement of the model (2.9 mmol ATP gDW⁻¹ h⁻¹) was retained. Biomass formation was fixed at zero for the maximum-yield case — the theoretical ceiling assumes no cell growth — and at a series of fixed non-zero rates for the production-versus-growth envelope. The protein demand reaction was then maximised by flux balance analysis.

Yields are reported as grams of protein per gram of substrate, as carbon moles of product per carbon mole of substrate, and as the substrate mass required per gram of protein. Carbon dioxide and oxygen exchange at the optimum are recorded alongside, since they bound the heat and aeration duties used in Chapter 8.

Three carbon sources were analysed: glycerol (the standard biomass-accumulation substrate for this host), methanol (the inducer for AOX1-driven expression) and glucose.

## 3.6 Sequence feature panel

Features were computed in `src/features.py`: length and molecular mass; isoelectric point, GRAVY hydropathy, aromaticity and instability index from Biopython's ProtParam; mean net charge per residue and fraction of charged residues; cysteine count, annotated disulfide count and disulfides per 100 residues; N-glycosylation sequons; annotated phosphosites; and amino-acid composition as twenty fractions.

**Disorder** is estimated by FoldIndex (Prilusky et al. 2005), *2.785⟨H⟩ − |⟨R⟩| − 1.151*, where ⟨H⟩ is mean Kyte–Doolittle hydropathy scaled to the unit interval and ⟨R⟩ is mean net charge per residue, evaluated both globally and in a 51-residue sliding window to give a disordered fraction and the longest disordered run. A neural disorder predictor (metapredict) is supported by the code and used automatically when installed; it could not be installed in the analysis environment, so **all reported disorder values are FoldIndex values**. This is a weak predictor relative to the current state of the art, and Chapter 6's null result for disorder must be read with that in mind: the honest statement is that *this* measure of disorder does not predict titre, not that disorder is irrelevant.

## 3.7 Codon optimisation

A *Komagataella phaffii* codon usage table derived from the Codon Usage Database was used to compute relative adaptiveness *w<sub>i</sub>* within each synonymous family and a codon adaptation index as the geometric mean of *w<sub>i</sub>* along a coding sequence.

A caveat is load-bearing and is stated rather than hidden: classical CAI (Sharp and Li 1987) uses a reference set of **highly expressed** genes, not whole-genome usage. Only a whole-genome table was reachable from the analysis machine, so what is computed here is a genome-wide adaptation index. It is unbiased but weaker, it compresses the differences between designs, and it is never used as a sole criterion. Rebuilding the reference from the coding sequences of the organism's most highly expressed genes is listed in Chapter 9 as a required improvement.

Three designs were generated per protein: a maximum-CAI design using the most adapted codon everywhere; a **harmonised** design sampling codons in proportion to host usage subject to design filters (no homopolymer run of six or more nucleotides, GC content between 35 and 60 per cent in every 50-nucleotide window, no internal BamHI, EcoRI, XhoI, NotI, SacI or SalI sites, no AATAAA or TATATA motifs); and a uniform-synonymous null as a negative control. The harmonised sequences are the ones proposed for synthesis and are in `results/constructs/`. All designs are deterministic given the random seed recorded in the code.

## 3.8 The titre database

No suitable compilation of published titres for food proteins in these hosts existed, so one was built. Records were retrieved principally through the Europe PMC REST article interface, with publisher and PubMed landing pages as fallbacks.

Each record carries: protein and source organism; UniProt accession where the identification was unambiguous; host and strain; secretion leader and promoter where reported; cultivation mode; the titre as reported and normalised to mg L⁻¹; whether the product was secreted; year, first author, journal and DOI; **a verbatim quotation of the sentence stating the titre**; and a confidence grade. Nothing was entered from memory.

The database contains 109 host-panel records (96 high confidence, 12 medium, 1 low) and 32 records specific to the panel proteins across any microbial host. Ninety-one records are from *K. phaffii* or *P. pastoris* and eight from *T. reesei*.

Three documented hazards are carried into the analysis rather than silently averaged away. Some high reported figures are **total extracellular protein** rather than product mass, and are flagged per row. Multi-stage results from a single study are **not independent**, and eight such sets are identified. Within-study flask-to-bioreactor ratios of 8- to 88-fold mean that **cultivation modes must not be pooled**, which is why Chapter 6 carries an explicit fed-batch indicator.

Two gaps are material and are reported as gaps: no primary volumetric titre was found for β-casein or α-S2-casein in any microbial host, and secretion of ovalbumin in *K. phaffii* has been demonstrated without a stated titre.

## 3.9 The ceiling–gap measurement

For each protein, the stoichiometric ceiling at a given fed-batch substrate loading *S* is *S* × *Y*<sub>poly</sub>, where *Y*<sub>poly</sub> is the maximum theoretical polypeptide yield on glycerol. Published fed-batch processes for this host feed of order 150–500 g L⁻¹ of glycerol plus methanol, so *S* is scanned across {150, 250, 350, 500} g L⁻¹ and results are reported as a band, with 350 g L⁻¹ as the central case. Each high-confidence titre is then expressed as a fraction of its own protein's ceiling, and the reciprocal is reported as the gap in fold.

## 3.10 Testing what the gap tracks

The design was fixed before the analysis was run.

**Response**: log₁₀ of titre in mg L⁻¹. **Inclusion**: *K. phaffii* or *P. pastoris* only; secreted product only; high-confidence records only; sequence available and verified. This yields 37 records over 25 distinct proteins. **Features**: seven mechanistic predictors — log length, disulfides per 100 residues, sequons per 100 residues, disordered fraction, GRAVY, absolute mean net charge, and the maximum theoretical yield — plus a fed-batch indicator. **Model**: ridge regression with the penalty chosen by internal cross-validation on standardised features. **Validation**: leave-one-protein-out, so that all records of a protein are withheld together and the score cannot be inflated by memorising a protein from its own replicates. **Baseline**: predicting the training mean, reported beside the model, because a model that cannot beat that baseline has no skill regardless of its correlation coefficient.

Univariate associations are computed per protein rather than per record, using each protein's best reported titre, to avoid weighting well-studied proteins more heavily.

Where disulfide counts were not annotated for a validation-set protein, cysteines were assumed to pair (⌊Cys/2⌋). This is the standard assumption for secreted proteins and is applied uniformly, so it cannot favour any one protein; it nevertheless introduces noise into the single feature that turns out to matter, which is noted in Chapter 9.

## 3.11 Metabolic engineering targets

Two analyses were run per protein. **Shadow prices** of the twenty cytosolic amino-acid pools were extracted at the production optimum and weighted by the protein's demand for each residue, giving a per-protein picture of where supply pressure falls. **Flux scanning with enforced objective function** (FSEOF; Choi et al. 2010) was run by stepping the protein demand from zero to its maximum in eleven stages while maximising growth, and retaining reactions whose flux changed monotonically; increasing reactions are amplification candidates and decreasing ones attenuation candidates. Gene associations are reported with the model's locus identifiers.

## 3.12 Techno-economic model

A transparent fed-batch model was implemented in `src/tea.py`. Every parameter is a typed object carrying a value, a unit and a **source string**, and parameters that are assumptions say so in that string rather than acquiring false authority by appearing in a table. The model computes annual production from reactor volume, working fraction, cycle time and uptime; costs are decomposed into substrate, other media, utilities (aeration, agitation and cooling power), downstream processing, annualised capital, maintenance and labour.

Two reference quantities are reported alongside the cost. The **stoichiometric floor** is the raw carbon cost of the product if the organism achieved the maximum theoretical yield computed in Chapter 4, with no cells, no losses and no equipment; nothing can be cheaper. The **engineering gap** is the ratio of modelled plant cost to that floor. One-at-a-time sensitivity (±50%) and a log-normal Monte Carlo (20,000 draws, 25% relative standard deviation) are reported.

## 3.13 Independent cross-check

Parts of this analysis were independently reimplemented from the same published model by a separate effort that had not seen this code. The two implementations agree on maximum theoretical yields to within about 1% (β-casein on glycerol: 0.6400 here against 0.636; β-lactoglobulin: 0.6535 against 0.647) and agree exactly on lactoferrin's 85.44 kDa product mass after the mass-accounting correction described in §3.4.1. That cross-check also produced the three corrections recorded in §3.3.3 and §3.4.1. Independent reimplementation is reported here as a validation step because, for a thesis whose entire evidence base is computed, it is the closest available analogue to a replicate experiment.

## 3.14 Known limitations of the method

Stated here so that the results chapters are not interrupted by them, and developed in Chapter 9.

1. Flux balance analysis predicts **capability, not realisation**. A computed ceiling says what the stoichiometry permits, not what a strain will do.
2. The model has **no secretory-pathway capacity**. Chaperone availability, endoplasmic-reticulum volume, COPII vesicle throughput and translocon occupancy are absent, which is precisely why a pathway-aware model such as pcSecYeast is the natural successor to this analysis.
3. **Disorder is measured weakly** (§3.6).
4. The **codon index is genome-wide, not expression-weighted** (§3.7).
5. The titre corpus is subject to **publication bias and unequal research effort**, which is a confound the design cannot remove and which Chapter 6 argues is in fact the main finding.
6. **No experimental validation** was performed.


---

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


![**Figure 4.1** Maximum theoretical yield of each panel protein on glycerol, glucose and methanol, computed in iMT1026v3 with an explicit sequence-derived synthesis reaction and the full post-translational load charged. The protein changes the ceiling by under 10%; the carbon source changes it by about 30%.](../results/figures/fig1_theoretical_yields.png)

**Figure 4.1** Maximum theoretical yield of each panel protein on glycerol, glucose and methanol, computed in iMT1026v3 with an explicit sequence-derived synthesis reaction and the full post-translational load charged. The protein changes the ceiling by under 10%; the carbon source changes it by about 30%.

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


![**Figure 4.2** Yield penalty of the post-translational load on a polypeptide basis. Phosphorylation, however many sites, costs almost nothing; disulfide bonding is nearly free; glycosylation dominates.](../results/figures/fig2_ptm_cost.png)

**Figure 4.2** Yield penalty of the post-translational load on a polypeptide basis. Phosphorylation, however many sites, costs almost nothing; disulfide bonding is nearly free; glycosylation dominates.


![**Figure 4.3** Yeast outer-chain extension scanned from the ER core glycan (Man9) to Man100. Solid lines: polypeptide yield, which falls. Dashed lines: glycoprotein mass yield, which rises. A process measured on the wrong basis looks better as it gets worse.](../results/figures/fig3_hypermannosylation.png)

**Figure 4.3** Yeast outer-chain extension scanned from the ER core glycan (Man9) to Man100. Solid lines: polypeptide yield, which falls. Dashed lines: glycoprotein mass yield, which rises. A process measured on the wrong basis looks better as it gets worse.

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


---

# Chapter 5 — The gap between the ceiling and the record

Chapter 4 computed what metabolism permits. This chapter measures what has been achieved, and expresses the second as a fraction of the first. That ratio is the central quantity of this thesis.

## 5.1 Why the ratio is the right quantity

Published titres cannot be compared to one another directly. A gram per litre of a 15 kDa globin and a gram per litre of an 80 kDa glycoprotein are not the same achievement; a shake-flask result and a fed-batch bioreactor result differ by one to two orders of magnitude for reasons that have nothing to do with the protein; and a process fed 150 g L⁻¹ of substrate cannot be judged against one fed 500.

Dividing each titre by the ceiling of the very protein that was produced removes the first of these problems entirely and makes the third explicit as a scanned parameter. What remains — the fraction of its own stoichiometric limit that a process reached — is dimensionless, comparable, and bounded above by one.

## 5.2 The measurement

Applying the inclusion rules of §3.9 to the curated corpus gives 41 high-confidence records of secreted production in *K. phaffii*, *P. pastoris* or *T. reesei*, covering 24 distinct proteins for which a verified sequence was available. Thirteen records were excluded as fragments or fusions, for reasons §5.4 develops.

**Table 5.1 — Fraction of its own stoichiometric ceiling reached, at 350 g L⁻¹ substrate loading**

| Protein | Best titre (g L⁻¹) | *Y*<sub>max</sub> (g g⁻¹) | Ceiling (g L⁻¹) | % of ceiling | Gap |
|---|---|---|---|---|---|
| Human-like type III collagen | 19.40 | 0.668 | 234 | 8.30% | 12× |
| Human serum albumin | 17.47 | 0.662 | 232 | 7.54% | 13× |
| **β-lactoglobulin** | 13.88 | 0.653 | 229 | 6.07% | 16× |
| **Soy leghemoglobin** | 6.00 | 0.622 | 218 | 2.75% | 36× |
| *Candida antarctica* lipase B | 5.41 | 0.642 | 225 | 2.41% | 42× |
| Human GM-CSF | 4.30 | 0.567 | 199 | 2.17% | 46× |
| Type XVII human-like collagen | 4.70 | 0.658 | 230 | 2.04% | 49× |
| Hen egg white lysozyme | 3.50 | 0.683 | 239 | 1.46% | 68× |
| Human interferon α-2b | 2.40 | 0.656 | 230 | 1.05% | 96× |
| **Ovalbumin** (*T. reesei*) | 2.00 | 0.645 | 226 | 0.89% | 113× |
| **Human lactoferrin** | 1.35 | 0.642 | 225 | 0.60% | 167× |
| Brazzein | 1.30 | 0.697 | 244 | 0.53% | 188× |
| Hen ovomucoid | 0.93 | 0.506 | 177 | 0.52% | 191× |
| Human interleukin-6 | 0.28 | 0.597 | 209 | 0.13% | 746× |
| Porcine myoglobin | 0.29 | 0.650 | 227 | 0.13% | 797× |
| Human insulin precursor | 0.25 | 0.655 | 229 | 0.11% | 917× |
| **Bovine lactoferrin** | 0.23 | 0.616 | 216 | 0.11% | 927× |
| Human bFGF | 0.15 | 0.696 | 244 | 0.06% | 1,624× |
| **Human α-lactalbumin** | 0.11 | 0.597 | 209 | 0.05% | 1,844× |
| Human G-CSF | 0.10 | 0.646 | 226 | 0.04% | 2,262× |
| Human interleukin-15 | 0.07 | 0.540 | 189 | 0.04% | 2,521× |
| *T. reesei* hydrophobin HFBI | 0.09 | 0.677 | 237 | 0.04% | 2,736× |
| Human interferon λ-1 | 0.07 | 0.616 | 216 | 0.03% | 3,318× |
| Human serum transferrin | 0.03 | 0.649 | 227 | 0.01% | 7,573× |

Food proteins are shown in bold.

### 5.2.1 The headline contrast

Across these 24 proteins:

- the **stoichiometric ceiling spans 1.38-fold**, from 0.506 g g⁻¹ for hen ovomucoid to 0.697 for brazzein;
- the **fraction of that ceiling actually achieved spans 628-fold**, from 8.30% to 0.01%.

A quantity that varies by a factor of 1.4 cannot explain an outcome that varies by a factor of 628. This is the result the thesis exists to state, and it is robust to every assumption tested: it holds across the whole scanned range of substrate loading, across the translation-cost scan, and whether the product basis or the polypeptide basis is used.

### 5.2.2 Nobody is close to the ceiling

The best process in the entire corpus — a human-like collagen at 19.4 g L⁻¹ — reached **8.3%** of what the stoichiometry of its host permits. The best food protein, β-lactoglobulin at 13.88 g L⁻¹, reached 6.1%. This is worth stating plainly because the field's language sometimes suggests that titres are approaching a biological limit. They are not approaching it; they are one to four orders of magnitude away from it.

At a loading of 150 g L⁻¹ the β-lactoglobulin result rises to 14.2% of ceiling and at 500 g L⁻¹ it falls to 4.3%, so the conclusion is not an artefact of the central loading assumption: no plausible loading brings any published process within a factor of seven of its ceiling.

### 5.2.3 Is carbon the right bound? The oxygen and nitrogen checks

A comparison is only as good as its denominator. If real fermentations hit an oxygen-transfer wall long before they exhaust their carbon, then measuring titres against a carbon ceiling compares them against a bound that never binds, and the gap is partly an artefact.

That alternative is computable from numbers already in hand. The model reports oxygen consumption at the production optimum as **9.4 to 10.2 mmol of O₂ per gram of product**, nearly invariant across the panel. An aerated vessel delivers oxygen at a maximum volumetric transfer rate, so over a 90-hour batch the oxygen-limited ceiling is the transfer rate times the batch time divided by that demand. Scanning the transfer rate from 50 to 300 mmol L⁻¹ h⁻¹:

| OTR (mmol L⁻¹ h⁻¹) | Oxygen ceiling (g L⁻¹) | Carbon ceiling (g L⁻¹) | Binding bound |
|---|---|---|---|
| 50 | 440–477 | 214–234 | carbon |
| 100 | 880–953 | 214–234 | carbon |
| 200 | 1,759–1,907 | 214–234 | carbon |
| 300 | 2,639–2,860 | 214–234 | carbon |

Carbon is the tighter bound in **all 36 protein-by-transfer-rate combinations**, and even at the lowest transfer rate the oxygen ceiling is 1.9-fold above the carbon ceiling. The calculation is deliberately generous to oxygen — it spends the entire oxygen budget on product and none on growth or maintenance, which no real process can do — so the conclusion is conservative in the right direction.

Oxygen transfer certainly constrains real processes through growth and maintenance demand, which this calculation excludes; what it does not do is constrain them *more tightly than carbon* at the product level.

**Nitrogen, however, does — in a batch.** The same calculation for nitrogen is less comfortable and is reported because of that. These proteins are 15.8–17.4% nitrogen by mass, so a medium supplying *N* grams of ammonium nitrogen per litre supports at most *N*/0.165 grams of protein:

| Nitrogen supplied (g L⁻¹) | Nitrogen ceiling (g L⁻¹) | Binding bound |
|---|---|---|
| 2 | 12–13 | nitrogen |
| 5 | 29–32 | nitrogen |
| 10 | 58–63 | nitrogen |
| 30 | 173–190 | nitrogen |
| 60 | 345–380 | carbon |

Nitrogen binds before carbon in 36 of 45 cases and stops binding only above about 30 g of nitrogen per litre, which is far more than any batch medium for this host contains. **A batch fermentation is nitrogen-limited long before it is carbon-limited.**

Two things keep this from overturning Table 5.1, and one of them is a genuine qualification.

The qualification first: *if* a process in the corpus were nitrogen-limited at, say, 5 g N L⁻¹, its ceiling would be about 31 g L⁻¹ rather than 229, and β-lactoglobulin's 13.88 g L⁻¹ would be 45% of it rather than 6.1%. That is a different picture, and a reader is entitled to it.

What keeps the carbon bound the right one for these records is that every high-titre process in the corpus is **fed-batch**, and a fed-batch fermentation of this host titrates with ammonia or ammonium hydroxide for pH control throughout the run. Nitrogen is fed continuously and is not a fixed inventory, so it is not the operative bound for the processes being measured. The nitrogen ceiling is the bound for a *batch* process, and batch processes are not where any of these titres came from.

And the central claim does not depend on the choice at all. Nitrogen content varies by only **1.10-fold** across the panel, and the carbon ceiling by 1.38-fold. Whichever bound is used, the ceiling is nearly the same for every protein while achievement varies 628-fold. The argument of §5.2.1 survives both substitutions, which is the strongest thing that can be said for it.

### 5.2.4 The ordering is not the expected one

Chapter 2 declared the expectation in advance: the published expert judgement is that whey proteins are the most tractable targets and caseins and lactoferrin the least. The measurement partly contradicts it.

β-lactoglobulin does indeed sit near the top. But **α-lactalbumin, the other "easy" whey protein, is close to the bottom** at 0.05% of its ceiling — below lactoferrin, below ovalbumin, below several cytokines. By stoichiometry it is an ordinary protein; by achievement it is among the worst in the corpus. Meanwhile soy leghemoglobin, which requires a cofactor the host must be engineered to supply, sits fourth.

Two readings are available and the data here cannot fully separate them. Either α-lactalbumin is genuinely difficult — four disulfides in 123 residues is the highest disulfide density of any food protein in the panel, and Chapter 6 finds disulfide density to be the one predictive feature — or it has simply received far less engineering effort than β-lactoglobulin, which has a commercial product behind it. Both are probably true. The second reading is developed in §6.5, where it becomes the chapter's main conclusion rather than a caveat.


![**Figure 5.1** Best published titre against the stoichiometric ceiling of the same protein, at 350 g/L substrate loading, log scale. Labels give the gap in fold. No published process exceeds 8.3% of its own ceiling.](../results/figures/fig4_efficiency_gap.png)

**Figure 5.1** Best published titre against the stoichiometric ceiling of the same protein, at 350 g/L substrate loading, log scale. Labels give the gap in fold. No published process exceeds 8.3% of its own ceiling.


![**Figure 5.2** The ceiling varies 1.38-fold across 24 proteins; the fraction of it achieved varies 628-fold. A property with this little variation cannot explain an outcome with that much.](../results/figures/fig7_ceiling_vs_achievement.png)

**Figure 5.2** The ceiling varies 1.38-fold across 24 proteins; the fraction of it achieved varies 628-fold. A property with this little variation cannot explain an outcome with that much.

## 5.3 The caseins: an absence that is a result

The caseins do not appear in Table 5.1, and that is the single most striking thing about it.

An earlier version of this analysis credited κ-casein with 1.02 g L⁻¹, placing it mid-table. That number came from a record for **bovine casein macropeptide**, the 64-residue glycopeptide that chymosin releases from κ-casein during coagulation. A strain secreting casein macropeptide has not secreted a casein; it has secreted about a third of one, without the part that matters. The error entered through a name-based join matching "casein" in both strings, and it inflated the caseins' apparent performance by a factor of nearly eight. It was caught by cross-checking against an independent analysis of the same corpus, and the corpus filter that now removes fragments, fusions, isolated domains and antibody fragments is shared between both pipelines so that neither can repeat it.

With the fragment removed, the finding is this: **no intact casein — α-S1, α-S2, β or κ — has a published volumetric titre in *K. phaffii* or *T. reesei*.** The systematic search found secretion demonstrated, constructs described and functional studies performed, but no number in grams or milligrams per litre from a peer-reviewed primary source in either host.

This is not a gap in the search; it is a gap in the literature, and it has three implications.

First, the most commercially valuable target in animal-free dairy — the protein class that makes cheese behave like cheese — is also the one with the least public quantitative data. Companies producing animal-free casein exist and have self-affirmed regulatory status, so the knowledge exists; it is simply not in the public record.

Second, any ranking of food proteins by tractability that places caseins last is, for these hosts, ranking them on an absence of data rather than on data. The published expert ordering may well be right, but it is not currently supported by a measurement.

Third, it tells a student or a company where the open ground is. A rigorous, published fed-batch titre for an intact casein in *K. phaffii*, with phosphorylation state characterised, would be a genuinely novel experimental contribution. It is the first item in the wet-laboratory programme proposed in Chapter 9.

## 5.4 What the exclusions remove, and why it matters

Thirteen records were excluded as fragments or fusions. The category matters because each exclusion is a case where a reported titre overstates what was achieved for the protein of interest:

- **Fragments** (casein macropeptide, lactoferricin, antimicrobial peptides excised from precursors) are shorter and structurally simpler than the parent, and are often produced precisely because the parent is difficult.
- **Fusions** (a SUMO-tagged holin, an sfGFP-tagged lipase at 5.1 g L⁻¹) report a titre that includes the partner's mass, and the partner is frequently chosen because it improves secretion.
- **Antibody fragments and isolated domains** (Fab, scFv, a viral receptor-binding domain) are engineered constructs, not natural proteins, and their sequence features belong to the construct rather than to anything in UniProt.

Including any of these inflates apparent performance. Excluding them costs sample size — 13 of 88 in-host high-confidence records — and the trade is worth making, but it is recorded here because a reader comparing this table against the raw corpus will find the difference.

## 5.5 What this chapter establishes

1. No published process for any protein in these hosts has reached more than 8.3% of its stoichiometric ceiling, and food proteins reach between 6.1% and 0.05%.
2. The ceiling varies by 1.38-fold while achievement varies by 628-fold, which excludes metabolic cost as the explanation of the ordering.
3. The published expert ordering of food proteins by tractability is partly contradicted: α-lactalbumin, a "tractable" whey protein, performs worse than lactoferrin and ovalbumin.
4. No intact casein has a published titre in either host, so the hardest and most valuable class in the panel is undocumented rather than documented as hard.

The gap is therefore real, large, and unexplained by anything computed so far. The next chapter asks what it tracks.


---

# Chapter 6 — What the gap tracks

Chapter 5 established a gap of one to four orders of magnitude between what metabolism permits and what has been achieved, and showed that the gap is not explained by metabolic cost. This chapter asks what it *is* explained by, and reports an answer with one positive result, several negative ones, and a conclusion drawn mainly from the negatives.

The design was fixed before the analysis ran and is stated in §3.10. It is repeated in outline here because the credibility of a small-sample result depends entirely on whether the analyst could have fished.

## 6.1 The dataset

Applying the inclusion rules gives **35 records over 23 distinct proteins**: secreted production in *K. phaffii* or *P. pastoris*, high-confidence evidence, verified sequence available, fragments and fusions excluded. The response is log₁₀ of titre in mg L⁻¹, which spans just under four orders of magnitude.

Seven mechanistic features were specified in advance: log length, disulfides per 100 residues, N-glycosylation sequons per 100 residues, disordered fraction, GRAVY hydropathy, absolute mean net charge per residue, and the maximum theoretical yield from Chapter 4. A fed-batch indicator was included because the corpus documents within-study flask-to-bioreactor ratios of 8- to 88-fold, which would otherwise masquerade as a protein property.

Univariate associations are computed **per protein**, using each protein's best reported titre, so that a well-studied protein with many records does not dominate.

## 6.2 The positive result: disulfide density

**Table 6.1 — Univariate association with best log titre (n = 23 proteins)**

| Feature | Spearman ρ | p |
|---|---|---|
| **disulfides per 100 residues** | **−0.438** | **0.036** |
| log length | +0.297 | 0.169 |
| GRAVY | −0.223 | 0.306 |
| absolute net charge per residue | +0.097 | 0.659 |
| **maximum theoretical yield** | **+0.026** | **0.907** |
| sequons per 100 residues | +0.010 | 0.965 |
| **disordered fraction** | **−0.009** | **0.968** |

Only one feature is significantly associated with titre: **disulfide bond density, negatively** (ρ = −0.438, p = 0.036). Proteins that must form more disulfide bonds per unit length are secreted less well, across a set spanning caseins, whey proteins, cytokines, enzymes, a globin and a collagen.

The association survives in the multivariate model. In the ridge regression on standardised features, disulfide density carries the largest protein-derived coefficient (−0.213), second overall only to the fed-batch indicator (+0.265), which is a process variable rather than a protein property.

The interpretation is constrained by Chapter 4. Disulfide formation is stoichiometrically almost free: the Ero1–PDI relay consumes half a mole of oxygen per bond, which against a total oxygen demand of about 10 mmol per gram of protein is negligible, and β-lactoglobulin's two disulfides cost nothing measurable. So the cost of making the bonds is not what limits production. What limits production must be the **machinery** that makes them: the oxidative folding capacity of the endoplasmic reticulum, the availability of protein disulfide isomerase to reshuffle incorrect pairings, and the residence time a protein with many cysteines requires before it can leave. A protein with sixteen disulfides has an enormous number of incorrect pairings available to it, and getting the right one is a kinetic problem that no amount of carbon solves.

This is consistent with what the host literature already shows by other means — overexpression of protein disulfide isomerase improves secretion of difficult proteins, and engineering the unfolded protein response raises titres — and it is the kind of constraint a purely stoichiometric model is structurally unable to see. The value of finding it this way is that it is found *against* the metabolic explanation rather than instead of testing one.


![**Figure 6.1** Charge-hydropathy placement of the panel. The caseins fall on the disordered side of the Uversky boundary, as expected; Chapter 6 nevertheless finds that predicted disorder carries no association with titre among the proteins that have one.](../results/figures/fig6_charge_hydropathy.png)

**Figure 6.1** Charge-hydropathy placement of the panel. The caseins fall on the disordered side of the Uversky boundary, as expected; Chapter 6 nevertheless finds that predicted disorder carries no association with titre among the proteins that have one.

## 6.3 The negative results, which are the informative ones

### 6.3.1 Metabolic cost does not predict titre

The maximum theoretical yield has essentially zero association with titre (ρ = +0.026, p = 0.907). This is the empirical counterpart of Chapter 4's flat ceiling, obtained independently: Chapter 4 showed the ceiling barely varies, and Chapter 6 shows that what little variation exists carries no information about the outcome.

Together these close the question the thesis was built to ask. **The binding constraint on producing food proteins in *K. phaffii* is not the metabolic cost of building them.** This is a negative result about a widely assumed mechanism, obtained from two independent directions, and it is the most useful thing in this thesis because it tells a developer where *not* to spend.

### 6.3.2 Disorder does not predict titre

Predicted intrinsic disorder shows no association whatsoever (ρ = −0.009, p = 0.968). This is uncomfortable, because disorder is the standard explanation offered for why caseins are hard, and it deserves two caveats rather than a triumphant reading.

First, **the caseins are absent from this dataset**, for the reason given in §5.3: they have no published titre in these hosts. The one feature most associated with caseins cannot be tested on caseins. What the null says is that among the 23 proteins that *do* have titres, disorder carries no signal.

Second, **disorder is measured weakly here**. FoldIndex is a 2005-vintage charge–hydropathy criterion, not a modern neural predictor, and the analysis environment could not install the latter (§3.6). The honest statement is therefore: *this* measure of disorder, on *this* set, carries no information. A stronger predictor on a set that included caseins might well find something, and that is a specific, testable follow-up rather than a vague limitation.

### 6.3.3 Glycosylation sequons do not predict titre

Sequon density shows nothing (ρ = +0.010). Given Chapter 4's finding that glycosylation is the one expensive modification, this is worth pausing on. The likely explanation is that the metabolic cost of glycosylation, while the largest in the panel, is still only an 8–9% effect at the core-glycan level — and an 8% effect cannot be detected in a 628-fold spread. The hypermannosylation penalty is far larger, but how heavily any given protein is hypermannosylated in any given study is not reported, so it cannot enter the model as a variable.

## 6.4 The model has no predictive skill, and that is the finding

A ridge regression over all eight predictors, cross-validated by leaving out all records of each protein together, gives:

| | Value |
|---|---|
| Records / proteins | 35 / 23 |
| Leave-one-protein-out RMSE (log₁₀) | 0.937 |
| Baseline RMSE (predict the mean) | 0.933 |
| **Skill against baseline** | **−0.4%** |
| Spearman ρ (predicted vs observed) | 0.370 (p = 0.029) |
| Pearson r | 0.268 (p = 0.119) |

The model **ranks** proteins better than chance but predicts absolute titre no better than guessing the average. Reporting only the rank correlation would be misleading, which is why the baseline is in the table.

A model that cannot beat the mean on data spanning four orders of magnitude is telling us something specific: the variance in published titre is mostly not in the protein. The residual standard deviation of about 0.93 in log₁₀ means a typical protein's reported titre is uncertain by nearly a factor of ten before any sequence feature is consulted.

## 6.5 What the variance is actually in

Three sources, none of them properties of the molecule, dominate.

**Engineering effort.** β-lactoglobulin reaches 6.1% of its ceiling and human α-lactalbumin 0.05%, a 120-fold difference between two small whey proteins of similar size. The record for β-lactoglobulin comes from a study that rewired host metabolism using omics guidance; the record for α-lactalbumin comes from a smaller study of a chaperone co-expression. These are not comparable levels of investment, and the corpus contains no measure of investment to control for.

**Strain and process.** Promoter choice, secretion leader, gene copy number, protease deletion, feeding strategy, induction temperature and dissolved-oxygen control each move titres by factors that rival the entire between-protein spread. The corpus records some of these variables sporadically and none of them completely.

**Publication bias.** Low titres are reported when a paper is about something else — a new chaperone, a new promoter, a demonstration of feasibility — and high titres when the paper is about the titre. The distribution of published numbers is not the distribution of achievable numbers.

This is a confound the design cannot remove, and it is the reason the negative result in §6.4 should be read as a statement about the literature rather than only about the model. **The published record of recombinant protein titres is, to first order, a record of how much work was done, not of how hard each protein is.**

## 6.6 Consequences

**For the field.** Comparative statements of the form "protein X is more tractable than protein Y", when supported by titres drawn from different studies, are weakly supported at best. The only clean comparisons are within-study ones, and the corpus contains few.

**For a developer.** Two of the three candidate bottlenecks named in the project brief can now be ranked against each other with numbers. Metabolic cost is excluded. Folding — specifically oxidative folding of disulfide-rich proteins — is implicated by the one surviving association. Post-translational modification splits: phosphorylation is free and is a missing-enzyme problem (§4.3.1), glycosylation is the one metabolically expensive modification and is worth up to 41% of polypeptide yield under hypermannosylation (§4.3.4).

**For the method.** The right successor to this analysis is a model that represents the secretory machinery explicitly, because that is where the evidence now points and where a stoichiometric model is blind. pcSecYeast is the obvious vehicle. This is set out in Chapter 9.

**For the thesis's own claim.** The expectation declared in Chapter 2 — that whey proteins would rank as most tractable and caseins and lactoferrin least — is not recovered. That is reported as a contradiction rather than reconciled, because the declaration was made in advance precisely so that it could be.


---

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


---

# Chapter 8 — What it costs, and what it could cost

Published cost estimates for precision-fermented protein span three orders of magnitude, from under $20 per kilogram to figures in the thousands. That range is not a disagreement about biology; it is a disagreement about assumptions that are usually not shown. This chapter builds a model in which they are all shown, and anchors it to the stoichiometry of Chapter 4 so that one end of the range becomes a hard bound rather than an opinion.

## 8.1 The two reference points

The model reports every result against two anchors.

The **stoichiometric floor** is the cost of the raw carbon alone if the organism achieved the maximum theoretical yield, with no cells, no losses, no equipment, no labour and no recovery step. At a glycerol price of $600 per tonne and a maximum theoretical yield of 0.64 g g⁻¹, that floor is

> $0.94 per kilogram of protein.

Nothing can be cheaper. Any claim of a lower production cost for a glycerol-fed process is either using a cheaper feedstock or is wrong.

The **engineering gap** is the ratio of modelled plant cost to that floor, and it is where the entire argument about the economics of this industry actually lives.

## 8.2 Baseline case

The baseline is a 200 m³ fed-batch plant at 75% working volume and 90% uptime, 90-hour cycles, a titre of 10 g L⁻¹, a realised yield of 10 g of protein per 100 g of substrate (about 16% of theoretical), 70% downstream recovery through a chromatography-free route, and $6 per kilogram of downstream processing cost. Every one of those numbers carries a source string in the code, and all of them are declared as assumptions rather than measurements.

**Table 8.1 — Baseline cost breakdown (USD per kg of product)**

| Item | $/kg | Share |
|---|---|---|
| Labour | 18.48 | 43% |
| Substrate | 8.57 | 20% |
| Downstream processing | 6.00 | 14% |
| Other media | 4.29 | 10% |
| Utilities (aeration, agitation, cooling) | 2.67 | 6% |
| Capital (15-year straight line) | 1.97 | 5% |
| Maintenance | 1.18 | 3% |
| **Total** | **43.17** | |
| *Stoichiometric floor* | *0.94* | |
| **Engineering gap** | **46×** | |

Annual output is 81 tonnes.

A Monte Carlo over all parameters (20,000 draws, log-normal, 25% relative standard deviation) gives a median of $45/kg with a 5th-to-95th-percentile range of **$25 to $93 per kilogram**. The distribution is right-skewed, which is the normal behaviour of a cost that is inversely proportional to several uncertain quantities at once.

That range brackets the published food-grade estimates for α-lactalbumin of roughly $24/kg, which is a mild validation of the parameterisation: an independently built model lands in the same place as an industry analysis without having been tuned to it.

## 8.3 What actually drives the cost

One-at-a-time sensitivity (±50% on each parameter) ranks the drivers:

| Parameter | Cost swing ($/kg) |
|---|---|
| Downstream recovery fraction | 49.56 |
| **Titre** | 38.13 |
| Working volume fraction | 28.85 |
| Plant uptime | 28.85 |
| Reactor volume | 24.64 |
| Batch time | 21.77 |
| … | |
| Substrate price | ~8 |

Three observations follow, and the first is the one that matters.

**Carbon efficiency is nearly irrelevant.** Substrate is 20% of the baseline cost and the stoichiometric floor is 2% of it. Doubling the organism's yield on substrate — an enormous biological achievement — removes about $4 from a $43 cost. Chapter 4 showed the ceiling varies by only 9% between proteins; Chapter 8 shows that even if it varied by a factor of two it would barely move the economics. **The metabolic efficiency of the cell is not where the money is.**

**Titre and recovery are where the money is.** Both act as pure divisors on the fixed costs of a batch: a batch costs roughly the same to run whether it produces 1 or 20 g L⁻¹, so the cost per kilogram falls almost in proportion to titre. The grid in Table 8.2 shows this directly.

**Table 8.2 — Cost against titre, at 30% of theoretical yield**

| Titre (g L⁻¹) | Cost ($/kg) | Substrate share | Output (t/a) |
|---|---|---|---|
| 1 | 296 | 1.5% | 8 |
| 2 | 153 | 2.9% | 16 |
| 5 | 68 | 6.6% | 41 |
| 10 | 39 | 11.4% | 81 |
| 20 | 25 | 18.0% | 162 |
| 40 | 18 | 25.4% | 325 |

The $20/kg commodity threshold is crossed between 20 and 40 g L⁻¹ at this plant scale. For reference, the best published food-protein titre in the corpus is 13.88 g L⁻¹ for β-lactoglobulin, and Chapter 5 showed that this is 6.1% of its stoichiometric ceiling. **The titre required for commodity economics is well within what stoichiometry permits — it is about 15% of the ceiling, not 100%.** The barrier is not thermodynamic.

**Labour dominates because the plant is small.** At 81 t/a, a $1.5M annual crew is $18/kg. At 325 t/a it is $4.6/kg. This is a scale effect, not a biology effect, and it is the clearest argument in the model for consolidation into large plants rather than distributed small ones.


![**Figure 8.1** Production cost against titre at four levels of realised carbon efficiency. The curves are nearly superimposed: titre moves the cost, carbon efficiency barely does.](../results/figures/fig5_tea_cost.png)

**Figure 8.1** Production cost against titre at four levels of realised carbon efficiency. The curves are nearly superimposed: titre moves the cost, carbon efficiency barely does.

## 8.4 The glycan trap in cost models

Chapter 4 showed that hypermannosylation raises the mass yield while destroying the polypeptide yield. The economic consequence is direct and, as far as the literature retrieved for this thesis shows, unremarked.

A cost model that measures product as secreted mass will record a hyperglycosylating strain as *more* carbon-efficient. A customer who buys protein will find the same material worth less per kilogram, because up to half of it is mannan. For α-lactalbumin at Man₁₀₀ the mass yield rises 14% while the protein yield falls 41%: a model built on the wrong basis would show a cost *improvement* for a strain that is in fact 41% worse.

This is a specific, checkable methodological warning for anyone building a techno-economic model of a glycoprotein in a yeast host: state the basis, and use the polypeptide basis if the product is sold on protein content.

## 8.5 Sustainability, reported as a range

Life-cycle assessments of precision-fermented dairy protein report large reductions relative to bovine milk protein — greenhouse-gas emissions commonly cited as 85–97% lower, blue water 96–99% lower, non-renewable energy 29–60% lower in the most-cited industry-commissioned assessment. Independent syntheses of many assessments give similar central tendencies with wide spreads.

Three caveats are carried rather than suppressed.

First, the result is **electricity-mix dependent**. Fermentation is an electricity-intensive process, and peer-reviewed analyses exist in which fermentation protein has *higher* emissions than efficient dairy under a carbon-intensive grid.

Second, **land-use savings are more robust than carbon savings**. Removing a ruminant from the system removes a land requirement unconditionally; it removes a carbon footprint only if the energy replacing it is clean.

Third, most of the favourable assessments are **commissioned by producers**. They are not thereby wrong, but they are not independent, and a thesis should say so.

The honest summary is that the environmental case for precision fermentation is strong on land and water, conditional on grid decarbonisation for carbon, and that the ranges should be reported as ranges.

## 8.6 What this chapter establishes

1. The raw-carbon floor for glycerol-fed food protein is about $1/kg; the modelled plant cost is $43/kg at 10 g L⁻¹; the engineering gap is 46-fold.
2. Titre and downstream recovery dominate the cost; substrate price and carbon efficiency barely matter. This is the economic restatement of Chapter 6's finding that metabolism is not the binding constraint.
3. Commodity economics require 20–40 g L⁻¹ at this plant scale — roughly 15% of the stoichiometric ceiling, which no published process has yet reached but which is far below any thermodynamic limit.
4. Cost models of glycoproteins in yeast must state whether product means polypeptide or secreted mass, because hypermannosylation moves the two in opposite directions.


---

# Chapter 9 — Discussion, limitations and what to do next

## 9.1 What was found

The thesis set out to decide, for a panel of food proteins in *Komagataella phaffii*, which of the field's named bottlenecks actually binds. Six findings answer that.

1. **The stoichiometric ceiling is nearly flat.** Maximum theoretical yields span 9.4% across the nine panel proteins on glycerol, and 1.38-fold across the 24 proteins of the wider validation set. The carbon source moves the ceiling by about 30%, far more than the protein does.

2. **Phosphorylation is energetically free.** Thirteen phosphoserines on α-S2-casein cost 0.12% of yield. The casein problem is the absence of a Golgi casein kinase, not the price of a phosphate group — a catalytic problem with a catalytic solution.

3. **Glycosylation is the one expensive modification, and the metric matters.** Core N-glycosylation costs 8–9% of polypeptide yield in α-lactalbumin and lactoferrin. Under this host's native hypermannosylation that rises to 41% for a single-sequon protein, while the *mass* yield simultaneously improves. Reporting one number without the other inverts the conclusion.

4. **Published titres sit 12- to 7,573-fold below their own ceilings.** No process in the corpus exceeds 8.3% of its stoichiometric limit; the best food protein reaches 6.1%.

5. **The ceiling explains none of it.** Achievement varies 628-fold while the ceiling varies 1.38-fold, and maximum theoretical yield has no univariate association with titre (ρ = +0.026, p = 0.907).

6. **Disulfide density is the only sequence feature that does associate** (ρ = −0.438, p = 0.036), and since disulfide formation is stoichiometrically almost free, the constraint it marks must lie in the oxidative folding machinery rather than in metabolism.

Taken together: for food proteins in this host, **metabolism is not the binding constraint, and the evidence points at the secretory pathway**. Three things follow for anyone deciding where to spend — do not spend on carbon efficiency; do spend on folding and secretion capacity, and on titre and recovery, which Chapter 8 shows are what the economics turn on.

## 9.2 The honest status of the negative result

The most important sentence in Chapter 6 is that the cross-validated model has **no skill** against predicting the mean. It would have been easy to report only the rank correlation (ρ = 0.370, p = 0.029) and call it a predictive model. That would have been misleading, and the baseline was pre-specified precisely to prevent it.

The right reading is that **the published record of titres is dominated by engineering effort, not by protein identity**. β-lactoglobulin reaches 120 times more of its ceiling than human α-lactalbumin, and the difference between the two studies is not mainly the molecule: one had a commercial programme and omics-guided host rewiring behind it, the other a chaperone co-expression experiment.

This has a consequence for the whole comparative literature. Statements of the form "protein X is more tractable than protein Y", when supported by titres from different papers, are weakly supported. Only within-study comparisons are clean, and there are few of them.

It also means the field's standard tractability ranking — whey easy, caseins and lactoferrin hard — is not confirmed here. α-lactalbumin, a canonical "easy" protein, sits near the bottom of the achievement table. The expectation was declared in Chapter 2 before the measurement, so the contradiction is reportable rather than embarrassing.

## 9.3 Limitations

These are ordered by how much they could change a conclusion.

**The model has no secretory machinery.** iMT1026v3 represents metabolism. It has no chaperones, no endoplasmic-reticulum volume, no translocon occupancy, no COPII throughput and no protein disulfide isomerase pool. This is a severe limitation and the most consequential one, because Chapter 6 concludes that the binding constraint lives exactly there. The thesis can show that metabolism does not explain the gap; it cannot, with this instrument, show what does. The disulfide association is evidence, not proof.

**Flux balance analysis predicts capability, not realisation.** Every ceiling here is an optimistic upper bound — the unconstrained growth rate of 0.674 h⁻¹ in §7.3 is itself two to three times the experimentally reported maximum. The gaps in Chapter 5 are therefore *lower bounds* on the true gap, which strengthens rather than weakens the central claim but should not be glossed over.

**Sample size.** Twenty-three proteins and 35 records. The disulfide association at p = 0.036 would not survive a strict multiple-testing correction across seven features (Bonferroni threshold 0.0071). It is reported as a single pre-specified association with a nominal p-value, it is consistent with independent mechanistic evidence from the host literature, and it is the kind of result that needs replication on a larger corpus rather than defence.

**The titre corpus is not a random sample.** Publication bias, unequal effort, inconsistent reporting of whether a figure is product or total extracellular protein, and the impossibility of controlling for strain and process engineering all remain. Thirteen fragments and fusions were removed; some residual contamination of this kind is likely.

**Disorder is measured weakly.** FoldIndex, not a modern neural predictor, because the environment could not install one. The disorder null is therefore a null about this measure on this set, and the caseins — the proteins the disorder hypothesis is really about — are absent from the set entirely.

**The codon index is genome-wide, not expression-weighted.** Classical CAI needs a highly expressed reference set; only a whole-genome table was reachable. This compresses the differences between designs and is why no conclusion in this thesis rests on codon adaptation.

**Sequence provenance is indirect.** UniProt was unreachable from the analysis machine, so sequences were recovered from mirrors and accepted only on exact length and mass agreement with the UniProt record, or on two-repository consensus. Every panel protein passed, but direct re-verification against UniProt is a required pre-submission step.

**Citation integrity is an open task.** A verification pass found that inferred rather than resolved DOIs were wrong roughly half the time. Re-resolution of all 306 records against Crossref and Europe PMC is in progress and must complete before submission.

**No experimental work.** Nothing here has been measured in a vessel.

## 9.4 Where the analysis could be wrong

Three ways, stated so that a reader can look for them.

**If the substrate loading assumption is badly wrong**, the absolute gaps change — but only proportionally, and the 628-fold spread in achievement is independent of loading entirely, since loading multiplies every ceiling equally. The central claim is safe; the specific fold-gaps are not precise.

**If the disulfide association is a confound**, the mechanistic conclusion weakens. Disulfide-rich proteins in this corpus are also disproportionately human therapeutic proteins, which may have been produced under different standards and for different purposes than food enzymes. A larger corpus with a therapeutic-versus-food indicator would separate the two, and this is the first analysis to run on the merged corpus when it lands.

**If the ceiling were not the right denominator** — for instance because real processes are oxygen-transfer-limited long before they are carbon-limited — the gap would be partly an artefact. This one has been checked and survives: §5.2.3 computes the oxygen-limited ceiling from the model's own oxygen demand of 9.4–10.2 mmol per gram of product and finds carbon to be the tighter bound in all 36 protein-by-transfer-rate combinations, with the tightest oxygen bound still 1.9-fold above the carbon bound. The check is generous to oxygen, so the conclusion is conservative. Nitrogen is a different matter and is reported in full in §5.2.3: at any batch nitrogen loading a fermentation is nitrogen-limited well before it is carbon-limited, and only continuous ammonia feeding — which every fed-batch process in the corpus uses for pH control — removes that bound. Since nitrogen content varies by just 1.10-fold across the panel against 1.38-fold for the carbon ceiling, the central contrast is unaffected by the substitution, but the absolute fractions in Table 5.1 would change substantially for a batch process. Phosphate and heat removal remain unchecked.

## 9.5 What to do next, computationally

In priority order:

1. **Port the analysis to a proteome-constrained secretory model.** pcSecYeast already builds protein-specific secretion reactions with post-translational requirements and makes per-protein bottleneck calls. Running this panel through it would test Chapter 6's disulfide conclusion directly, with machinery rather than inference.
2. **Scan the remaining candidate bounds** — phosphate and heat removal — as oxygen and nitrogen have now been scanned (§5.2.3).
3. **Enlarge the corpus and re-run.** The merged database approaching 300 records, with resolved identifiers, roughly triples the sample and would let the disulfide association be tested properly, with multiple-testing control and a therapeutic-versus-food covariate.
4. **Replace FoldIndex with a modern disorder predictor** and re-test the disorder null.
5. **Rebuild the codon reference** from the coding sequences of the host's most highly expressed genes.
6. **Model glyco-engineered strains explicitly**, since Chapter 4 values the fix at up to 41% of polypeptide yield.

## 9.6 What to do next, experimentally

The analysis is dry, and it should say precisely what would make it wet. Four experiments, each small, each testing something this thesis predicts.

**Experiment 1 — the missing casein number.** Express an intact bovine β-casein in *K. phaffii* under a constitutive promoter with the α-mating-factor leader, and report a fed-batch titre with phosphorylation state characterised by mass spectrometry. No such number exists in the literature (§5.3). Whatever it is, it is publishable, and it fills the largest hole in the public record for this field.

**Experiment 2 — the kinase test.** Co-express a heterologous Golgi casein kinase (FAM20C, or the bacterial PrkD/YabT kinases already shown to phosphorylate α-S1-casein in *E. coli*) alongside the casein. Chapter 4 predicts that the carbon and energy cost of doing so is negligible, so if the kinase works, titre should be essentially unaffected while phosphorylation state changes. A measurable titre penalty would falsify the "phosphorylation is free" claim.

**Experiment 3 — the disulfide test.** Produce two proteins of similar length and comparable codon optimisation but very different disulfide density — α-lactalbumin (4 bonds in 123 residues) against β-casein (none) — in the same strain background, same promoter, same leader, same process. Chapter 6 predicts a large titre difference attributable to folding rather than to metabolism. This is the single cleanest test of the thesis's main inference, and it is one fermentation pair.

**Experiment 4 — the glyco-engineering test.** Produce α-lactalbumin in a wild-type and in an outer-chain-deficient (*och1*) background and compare polypeptide yield per gram of substrate, not secreted mass. Chapter 4 predicts a difference of up to 41% in favour of the glyco-engineered strain on a protein basis, with the mass basis moving the other way. This also tests the methodological warning of §8.4.

## 9.7 Conclusion

The field describes its central problem as folding, modification and purification, and names them together. This thesis separated them and measured what it could.

Metabolism, which is the thing a genome-scale model is best at measuring, turned out not to be the answer: it costs essentially the same to build any of these proteins, phosphorylation costs nothing, and the economics barely notice carbon efficiency. What is left — folding, secretion, recovery, and the simple fact that most of these proteins have had very little engineering effort spent on them — is where the distance between 8% of a ceiling and 100% of it actually lies.

That is a smaller claim than the project began with, and a better supported one. The useful product of a dry-lab thesis is not a prediction that something will work. It is a defensible statement about where the remaining work is, and a list of experiments that would prove it wrong.


---

# Appendices

## Appendix A — The panel, as analysed

Every row was accepted only after the sequence recovered from a mirrored FASTA matched the UniProt entry's stated length exactly and its recomputed average mass to within 1 Da per 10 kDa (§3.3.2). All nine passed.

| Protein | Accession | Precursor → mature | Mature mass | S–S | N-glyc | pSer |
|---|---|---|---|---|---|---|
| α-S1-casein | P02662 | 214 → 199 aa | 22.97 kDa | 0 | 0 | 9 |
| α-S2-casein | P02663 | 222 → 207 aa | 24.35 kDa | 0 | 0 | 13 |
| β-casein | P02666 | 224 → 209 aa | 23.58 kDa | 0 | 0 | 5 |
| κ-casein | P02668 | 190 → 169 aa | 18.97 kDa | 0 | 0 | 1 |
| β-lactoglobulin | P02754 | 178 → 162 aa | 18.28 kDa | 2 | 0 | 0 |
| α-lactalbumin | P00711 | 142 → 123 aa | 14.19 kDa | 4 | 1 | 0 |
| ovalbumin | P01012 | 386 → 386 aa | 42.88 kDa | 1 | 1 | 2 |
| soy leghemoglobin C2 | P02236 | 145 → 145 aa | 15.52 kDa | 0 | 0 | 1 (+1 haem) |
| bovine lactoferrin | P24627 | 708 → 689 aa | 76.14 kDa | 16 | 5 | 0 |

Ovalbumin has no cleaved signal peptide and is therefore analysed at full length.

## Appendix B — Codon-optimised constructs

Harmonised coding sequences for *K. phaffii* are in `results/constructs/codon_optimised_cds.fasta`. They are generated deterministically by `src/codon_opt.py` from the host codon-usage table, sampling codons in proportion to host usage and rejecting designs that violate the manufacturability filters of §3.7.

| Protein | aa | CDS (nt) | CAI harmonised | CAI max | CAI uniform null | GC | GC3 | Residual violations |
|---|---|---|---|---|---|---|---|---|
| α-S1-casein | 199 | 597 | 0.760 | 1.000 | 0.671 | 0.441 | 0.432 | none |
| α-S2-casein | 207 | 621 | 0.741 | 1.000 | 0.672 | 0.435 | 0.556 | none |
| β-casein | 209 | 627 | 0.735 | 1.000 | 0.632 | 0.456 | 0.407 | none |
| κ-casein | 169 | 507 | 0.740 | 1.000 | 0.650 | 0.458 | 0.450 | none |
| β-lactoglobulin | 162 | 486 | 0.751 | 1.000 | 0.677 | 0.457 | 0.537 | none |
| α-lactalbumin | 123 | 369 | 0.762 | 1.000 | 0.700 | 0.412 | 0.496 | none |
| ovalbumin | 386 | 1158 | 0.738 | 1.000 | 0.633 | 0.439 | 0.448 | one low-GC window |
| leghemoglobin C2 | 145 | 435 | 0.756 | 1.000 | 0.658 | 0.455 | 0.414 | none |
| lactoferrin | 689 | 2067 | 0.732 | 1.000 | 0.625 | 0.457 | 0.411 | one homopolymer, one high-GC window |

Two observations, both of which argue for modest expectations from codon optimisation as practised here.

The **headroom is small**. A harmonised design reaches a genome-wide adaptation index of 0.73–0.76 against an unadapted uniform-synonymous null of 0.63–0.70: a difference of about 0.08. The maximum-CAI design reaches 1.000 by construction but is not proposed, because always choosing the same codon produces homopolymer runs, extreme local GC and the kind of translational pausing that codon optimisation is supposed to avoid.

The **index itself is weak**, for the reason given in §3.7: it is computed against whole-genome usage rather than against a highly expressed reference set, which compresses the differences between designs. Rebuilding the reference is listed as a required improvement, and no conclusion in this thesis rests on codon adaptation.

Two designs retain a residual violation after four thousand sampling attempts — lactoferrin, at 2,067 nucleotides, is long enough that avoiding every homopolymer and GC excursion by rejection sampling becomes improbable. A production design would repair these locally rather than by resampling.

## Appendix C — Computed tables

All are regenerated by the code and live in `results/tables/`.

| File | Contents |
|---|---|
| `target_composition.csv` | Amino-acid composition, elemental formula and modification counts for the panel |
| `target_features.csv` | Full sequence feature panel |
| `protein_yields.csv` | 162 rows: protein × substrate × translation cost × PTM on/off |
| `ptm_cost.csv` | Post-translational load decomposed, both yield bases |
| `glycan_scenarios.csv` | Outer-chain extension from Man9 to Man100 |
| `growth_tradeoff.csv` | Production against growth envelope |
| `efficiency_gap.csv`, `efficiency_gap_best.csv` | Every titre as a fraction of its own ceiling, loading scanned |
| `shadow_prices.csv` | Amino-acid supply pressure per protein |
| `fseof_targets.csv`, `fseof_summary.csv` | Amplification and attenuation candidates |
| `producibility_dataset.csv`, `producibility_univariate.csv`, `producibility_model.json` | The sequence-to-titre test and its validation |
| `codon_design.csv` | Construct designs |
| `tea_baseline.json`, `tea_titer_yield_grid.csv` | Techno-economic model, sensitivity and Monte Carlo |

## Appendix D — Reproducing this thesis

```bash
pip install cobra biopython scipy scikit-learn matplotlib pandas
cd src
python3 build_targets.py      # verify sequences against UniProt mass and length
python3 run_yields.py         # Chapter 4
python3 features.py           # sequence feature panel
python3 codon_opt.py          # Appendix B constructs
python3 efficiency_gap.py     # Chapter 5
python3 producibility.py      # Chapter 6
python3 flux_targets.py       # Chapter 7
python3 tea.py                # Chapter 8
python3 figures.py            # all figures
python3 build_thesis.py       # assemble the document
```

Every step is deterministic. `build_targets.py` exits non-zero if any sequence fails verification, so a corrupted input fails loudly rather than propagating.

## Appendix E — Outstanding tasks before submission

Recorded here rather than left implicit.

1. **Re-resolve every DOI and PubMed identifier.** A verification pass found that inferred identifiers were wrong roughly half the time. Until the re-resolution against Crossref and Europe PMC is complete, no identifier in this document should be treated as verified.
2. **Complete author lists.** A minority of bibliography entries carry "Not retrieved" rather than a guessed author list; these need filling from the papers.
3. **Re-verify sequences directly against UniProt** rather than against mirrors, now that network access is available.
4. **Merge the expanded titre corpus** (approaching 300 records) and re-run Chapters 5 and 6, which roughly triples the sample for the disulfide association and allows multiple-testing control.
5. **Re-run disorder with a modern predictor** and rebuild the codon reference from highly expressed genes.
6. **Format**: convert to the institution's required template, add the declaration and signature pages, and paginate.
