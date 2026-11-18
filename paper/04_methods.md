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
