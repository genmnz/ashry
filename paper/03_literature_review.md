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

*A note on the bibliography.* For a minority of entries no authoritative record returned an author list during retrieval; those entries carry "Not retrieved" in the author field rather than a guessed one, and are cited in this text by title and venue. They require completion from the papers themselves before submission, and this is recorded as an outstanding task rather than silently patched.
