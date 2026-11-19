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

Signal peptide boundaries, disulfide bond counts, N-glycosylation sites, phosphorylation sites and cofactor requirements were taken from the UniProt feature table of each entry. For the nine-member target panel they are recorded in `src/targets.py` with the position lists; for all 36 accessions in the wider validation corpus they are extracted programmatically in `src/uniprot_annotations.py` from the locally stored, CRC64-verified entries.

Parsing a UniProt feature table correctly turned out to require five explicit decisions, each of which was wrong in a first implementation and each of which inflated a protein's apparent modification load. They are recorded because every one of them changes a computed ceiling.

- **"Alternate" means opposite things on different feature types, and this is the subtlety that bit both implementations of this pipeline.** On a `Glycosylation` feature it marks an alternative *glycoform at an occupied site*, so the site is real and the extra lines are duplicates of one site. On a `Disulfide bond` feature it marks an alternative *pairing*, so keeping it invents a bond that does not coexist with the one beside it. In both cases the alternate lines are dropped, but for opposite reasons, and an implementation that applies one rule to both will be wrong on one of them.
- **An alternate annotation is not an extra feature.** β-lactoglobulin lists three DISULFID features (82–176, 122–135, 122–137), the last marked *Alternate*: it is the same cysteine pair in an alternative pairing, so the protein has two disulfides and one free cysteine. The same rule applies to glycosylation: UniProt writes one line per observed glycoform, so bovine lactoferrin's **five** N-glycosylation sites appear as **nine** lines, Asn-387 and Asn-495 each carrying three alternate entries for complex, high-mannose and hybrid glycans. All counts are therefore over distinct sequence positions, not over feature lines.
- **An inter-chain disulfide is stored twice.** UniProt records it as a point feature on each of the two partner cysteines. Bovine κ-casein's entry carries one intramolecular bond (Cys-32–Cys-109) plus two point features describing that same pair in the casein polymer; counted naively it has three bonds. Point features are counted once as inter-chain and reported separately.
- **Glycation is not glycosylation.** Human serum albumin's entry carries 24 `Glycosylation` lines reading "N-linked (Glc) (glycation) lysine", several marked *in vitro*. These are non-enzymatic glycation of lysine, not oligosaccharyltransferase products; albumin is not a glycoprotein. Charging it 24 glycans depressed its computed ceiling by a third. A site is counted only if it is N-linked, is not glycation, and sits on an asparagine in the sequence itself.
- **A signal peptide marked "Not cleaved" is not a cleavage site.** Ovalbumin's Signal feature spans residues 22–48 and is annotated *Not cleaved*: it is an internal signal sequence and the mature protein is the whole chain. Treating 48 as a cleavage point would have deleted an eighth of the protein.
- **An assumption is not a measurement.** Where no annotation was available the earlier analysis assumed cysteines pair, ⌊Cys/2⌋. Applied to the 36 annotated accessions, that assumption is wrong for **15 of them**, by up to eight bonds, and it over-assigns bonds specifically to cytosolic and fibrous proteins whose cysteines are free. It survives only as a declared fallback, and §6.2.1 reports what it did to the one positive result of the first draft.

The extractor was validated against the hand-curated nine-protein panel: it reproduces 43 of 45 annotation fields, and the two disagreements were both errors in the hand curation, since corrected (κ-casein's one intramolecular disulfide and three phosphoserine positions). The panel still verifies 9 of 9 against UniProt length and mass.

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

**Disorder** is estimated by FoldIndex (Prilusky et al. 2005), *2.785⟨H⟩ − |⟨R⟩| − 1.151*, where ⟨H⟩ is mean Kyte–Doolittle hydropathy scaled to the unit interval and ⟨R⟩ is mean net charge per residue, evaluated both globally and in a 51-residue sliding window to give a disordered fraction and the longest disordered run. A neural consensus disorder predictor (metapredict v3) is used for the reported disorder values, computed on the mature chain after signal-peptide removal, which matters: including the signal peptide shifts the mean score enough to change a rank correlation's magnitude (§6.5.2). Both a *mean* score and a *fraction of residues above 0.5* are recorded, and §6.5.1 reports why the choice between them turned out to be load-bearing; FoldIndex is retained and reported alongside as the transparent, dependency-free fallback, and the pipeline falls back to it automatically when the neural predictor is unavailable. An earlier version of this analysis ran on FoldIndex alone because the predictor could not be installed; both sets of values are in `results/tables/target_features.csv`, and the conclusions of Chapter 6 are reported for the neural predictor.

## 3.7 Codon optimisation

Codon usage was computed from the complete coding-sequence set of the RefSeq *K. phaffii* GS115 assembly (GCF_000027005.1, ASM2700v1): **5,040 coding sequences, 2,399,341 sense codons**, with the download archive's checksum recorded. Two tables were derived, giving per codon the count, the synonymous fraction, the frequency per thousand, the RSCU and the relative adaptiveness *w<sub>i</sub>*.

The reference set is the load-bearing choice. Classical CAI (Sharp and Li 1987) measures how closely a gene's codon choice resembles that of **highly expressed** genes, not the genomic average; against a genome-average table every native gene scores near the middle by construction and the index carries little information. No expression data for this organism was available, so the reference set was assembled from the standard proxy classes: **165 genes** comprising 129 cytosolic ribosomal proteins, 23 translation factors, 6 chaperones, 6 glycolytic enzymes and alcohol oxidase, all listed in `data/external/kphaffii_cds/highly_expressed_genes.tsv`.

Assembling that set by free-text matching on product names is a trap, and it was fallen into first. Matching "ubiquitin" admitted 55 genes that were ligases, conjugating enzymes and proteases, together with actin-associated and Rho-GAP proteins — all regulatory, all low-abundance. With those included, the reference set separated from the genomic average by only 0.050 in mean *w*; after exclusion the separation is 0.135, nearly three times larger. Contaminating a CAI reference with average-usage genes flattens the index towards the genomic average and quietly destroys its discriminating power.

The consequence is visible in the designs themselves. Scoring the same nine maximum-CAI designs against the same nine uniform-synonymous controls, the separation between them is **0.471** against the highly expressed reference and **0.296** against the genome average — so a genome-average index would have reported about a third less of the available signal. An earlier version of this analysis used a 2012 built-in genome-average table of unrecorded provenance, which gave 0.343. All three are tabulated in `results/tables/codon_reference_comparison.csv`; the highly expressed reference is used throughout.

Three designs were generated per protein: a maximum-CAI design using the most adapted codon everywhere; a **harmonised** design sampling codons in proportion to host usage subject to design filters (no homopolymer run of six or more nucleotides, GC content between 35 and 60 per cent in every 50-nucleotide window, no internal BamHI, EcoRI, XhoI, NotI, SacI or SalI sites, no AATAAA or TATATA motifs); and a uniform-synonymous null as a negative control. The harmonised sequences are the ones proposed for synthesis and are in `results/constructs/`. All designs are deterministic given the random seed recorded in the code.

## 3.8 The titre corpus

### 3.8.1 Why it had to be built

The measurement at the centre of this thesis divides a published titre by a computed ceiling. The computed side is reproducible by anyone with the model and the sequence. The published side is not, because the numbers are scattered across three decades of literature in units that do not match, under protein names that do not match, from cultivations that are not comparable, and — as §3.8.4 shows — sometimes mean something other than what a reader assumes. No compilation adequate to the task existed for these hosts, so one was built from primary sources, and it is reported here as a result of the work rather than as its supporting material.

The corpus holds **306 records** drawn from **167 distinct publications** spanning **1990 to 2027**, covering **29 distinct protein targets** across **15 host species**. Reported titres span more than six orders of magnitude, from 0.027 mg L⁻¹ to 125 g L⁻¹.

### 3.8.2 What each record carries

Every record carries, where the source states it: the protein name as published and a canonical name; a UniProt accession where identification was unambiguous (194 of 306); source organism; host species, canonicalised host, and strain; promoter and secretion leader; gene copy number; cellular localisation of the product; cultivation mode and carbon source; the titre as reported and normalised to mg L⁻¹; the basis on which it was reported; the quantification method; volumetric productivity where derivable; year, reference, source title, DOI and PMID; a confidence grade; free-text notes; and the file-level provenance of the row.

Two fields do more work than the rest.

**The evidence quotation.** Every one of the 306 records carries a verbatim quotation of the sentence in its source that states the number. This is not decoration. A normalised figure in a spreadsheet is unfalsifiable: a reader cannot tell whether 2.5 g L⁻¹ was the product, the total extracellular protein, a cell-lysate yield or a per-gram-biomass figure converted on an assumption the compiler did not record. The quotation makes each row auditable against its source in one step, and §3.8.4 records the cases where that audit changed an answer.

**The product-class field.** Each record is classified as food protein (129), other (71), human therapeutic (61), industrial enzyme (23), food enzyme (13) or research reagent (9), and separately flagged therapeutic or not (61 against 245). The reason is that therapeutic proteins are produced under a different economic regime: a monoclonal antibody fragment worth thousands of dollars per gram justifies strain-engineering effort that a dairy protein worth tens of dollars per kilogram does not, so a correlation fitted across both classes can be reading commercial incentive rather than molecular difficulty. The classification exists so that every association reported in Chapter 6 can be, and is, refitted on the food subset alone.

### 3.8.3 Confidence grading

Records are graded **high** (207), **medium** (78), **low** (18) or **unverified** (3). A high grade requires that the titre be stated numerically in the source for a defined volumetric basis, that the host and product be identifiable, and that the quotation support the number without inference. Medium covers numbers requiring a stated unit conversion or a secondary source. Low covers numbers recoverable only approximately — read from a figure, or reported as a range. The three unverified rows are retained, flagged, and excluded from every analysis. The quantitative analyses in Chapters 5 and 6 use high-confidence secreted records only; the remainder provide context and the negative-space mapping of Chapter 7.

### 3.8.4 Hazards carried into the analysis rather than averaged away

Four hazards are documented per row rather than silently smoothed.

**Basis mismatch.** Some high reported figures are total extracellular protein, not product mass. These are flagged in `titer_basis` and excluded from utilisation calculations.

**Localisation mismatch.** Twenty-two records are intracellular and five explicitly not secreted. A secretion analysis that pools these overstates what secretion achieves. One such case was caught only by its quotation: a record entered as a secretion titre carried a sentence containing the words "cell lysis, and purification", which places the number downstream of a lysis step and therefore inside the cell. Appendix F documents the episode and what it cost.

**Non-independence.** Multi-stage optimisation results from a single study are not independent observations. Thirty-three records are flagged against an earlier row by `duplicate_of`, and study identity is retained so that heterogeneity at the study level can be modelled rather than assumed away.

**Cultivation incomparability.** Within-study flask-to-bioreactor ratios in this corpus run from roughly 8-fold to 88-fold. Cultivation mode is therefore never pooled: Chapter 6 carries an explicit fed-batch indicator and reports every association both with and without it.

### 3.8.5 Gaps, reported as gaps

Two gaps in the literature are material to the panel and are reported rather than filled by inference. No primary volumetric titre was found for β-casein or α-S2-casein in any microbial host. Secretion of ovalbumin in *K. phaffii* has been demonstrated without a stated titre. These absences are not failures of retrieval; they are the shape of the field, and Chapter 7 treats them as findings.

## 3.9 The ceiling–gap measurement

For each protein, the stoichiometric ceiling at a given fed-batch substrate loading *S* is *S* × *Y*<sub>poly</sub>, where *Y*<sub>poly</sub> is the maximum theoretical polypeptide yield on glycerol. Published fed-batch processes for this host feed of order 150–500 g L⁻¹ of glycerol plus methanol, so *S* is scanned across {150, 250, 350, 500} g L⁻¹ and results are reported as a band, with 350 g L⁻¹ as the central case. Each high-confidence titre is then expressed as a fraction of its own protein's ceiling, and the reciprocal is reported as the gap in fold.

## 3.10 Testing what the gap tracks

The design was fixed before the analysis was run.

**Response**: log₁₀ of titre in mg L⁻¹. **Inclusion**: *K. phaffii* or *P. pastoris* only; secreted product only; high-confidence records only; sequence available and verified. On the rebuilt corpus this yields **53 records over 25 distinct proteins**. **Features**: seven mechanistic predictors — log length, disulfides per 100 residues, sequons per 100 residues, disordered fraction, GRAVY, absolute mean net charge, and the maximum theoretical yield — plus a fed-batch indicator. **Model**: ridge regression with the penalty chosen by internal cross-validation on standardised features. **Validation**: leave-one-protein-out, so that all records of a protein are withheld together and the score cannot be inflated by memorising a protein from its own replicates. **Baseline**: predicting the training mean, reported beside the model, because a model that cannot beat that baseline has no skill regardless of its correlation coefficient. **Nested controls**: two further models are fitted and reported beside the full one — the process indicator alone, and the seven sequence features without it. A fed-batch run beats a shake flask by one to two orders of magnitude, so a model containing the indicator can appear predictive while carrying no information about the protein, and only the nested comparison separates the two. **Subset refit**: the corpus flags each record as a human therapeutic or not, and the whole analysis is repeated on the food and food-adjacent subset, because a therapeutic is developed under a cost structure that justifies effort no food protein can.

Univariate associations are computed per protein rather than per record, using each protein's best reported titre, to avoid weighting well-studied proteins more heavily. Because seven features are tested at a sample size of twenty-three, each association is reported with a 10,000-sample bootstrap confidence interval, a 20,000-sample permutation p-value, and a Benjamini-Hochberg q-value across the pre-specified feature set. **No claim in this thesis rests on an uncorrected p-value.**

Disulfide counts for every protein in the validation corpus are read from its UniProt feature table, as described in §3.5. The ⌊Cys/2⌋ assumption used in an earlier version of this analysis is retained in the code only as a fallback for an accession with no annotation, and `src/disulfide_sensitivity.py` reports the association under both measures on both corpora so that the effect of the change is auditable rather than asserted.

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
4. The **codon index is genome-wide, not expression-weighted** (§3.7).
5. The titre corpus is subject to **publication bias and unequal research effort**, which is a confound the design cannot remove and which Chapter 6 argues is in fact the main finding.
6. **No experimental validation** was performed.
