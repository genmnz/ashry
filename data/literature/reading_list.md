# First 25 papers to read, in order

Ordered so that the prior-art risk is resolved first, then the hosts, then the targets, then the
methods, then the economics. Full metadata and DOIs are in `bibliography.csv`.

## Tier 1 — resolve the novelty question (read in week one)

1. **Guo et al. 2026, "Toward Rational Design of Precision-Fermented Milk Proteins", Compr Rev Food
   Sci Food Saf, 10.1111/1541-4337.70618** — the closest prior art; already states the tractability
   ordering the thesis intends to derive. Read first and decide how to position against it.
2. **Genome-scale reconstructions of the mammalian secretory pathway predict metabolic costs and
   limitations of protein secretion, Nat Commun 2020, 10.1038/s41467-019-13867-y** — the per-protein
   secretion-cost model that already exists, in mammalian cells. This is the template to port.
3. **Feizi et al. 2013, Genome-Scale Modeling of the Protein Secretory Machinery in Yeast,
   10.1371/journal.pone.0063284** — the yeast ancestor of (2); the secretory stoichiometry to reuse.
4. **Presep, PLOS ONE 2013, 10.1371/journal.pone.0079749** — the only sequence-to-secretion model
   built specifically for *P. pastoris*; the baseline the sequence half must beat or justify.
5. **Deciphering the determinants of recombinant protein expression across the human secretome,
   PNAS 2025, 10.1073/pnas.2506036122** — the strongest modern evidence on which sequence features
   actually matter; use it to choose features rather than inventing them.
6. **Balasubramanian, "Precision fermentation of milk proteins" (DTU PhD thesis)** — a whole thesis
   on the same problem space; read for scope overlap before fixing your own chapter plan.

## Tier 2 — the modelling platform

7. **Tomàs-Gamisans et al. 2017, Fine-tuning the P. pastoris iMT1026 model, 10.1111/1751-7915.12871**
   — the working model; read the biomass and maintenance assumptions closely.
8. **Kocabaş et al., Curation of GPR associations enhances the iPichia GEM, 10.1002/bit.70402** —
   decide here which model version the thesis commits to, and say why.
9. **Irani et al. 2015, GEM of P. pastoris with native and humanized glycosylation,
   10.1002/bit.25863** — the only existing coupling of glycosylation stoichiometry to a K. phaffii
   GEM; directly reusable for the PTM cost term.
10. **Lewis et al. 2010, pFBA, 10.1038/msb.2010.47** — the flux-parsimony criterion the simulations
    rest on; read for the assumptions, not the algorithm.
11. **Sánchez et al. 2017, GECKO, 10.15252/msb.20167411** — how to add enzyme/proteome constraints,
    which is what makes the yield numbers discriminate at all.
12. **O'Brien et al. 2013, ME-models, 10.1038/msb.2013.52** — the resource-allocation formalism for
    charging translation and folding to the cell.
13. **Akashi & Gojobori 2002, 10.1073/pnas.062526999** plus **Evolutionary Systems Biology of Amino
    Acid Biosynthetic Cost in Yeast, 10.1371/journal.pone.0011935** — read as a pair; use the yeast
    cost table, not the *E. coli* one.
14. **Burić et al. 2025, Amino acid sequence encodes protein abundance shaped by protein stability
    at reduced synthesis cost, 10.1002/pro.5239** — the cleanest existing link between sequence,
    cost and abundance; the conceptual spine of the index.

## Tier 3 — hosts and their real bottlenecks

15. **Puxbaum et al. 2015, Quo vadis? Challenges of recombinant protein folding and secretion in
    Pichia pastoris, 10.1007/s00253-015-6470-z** — the canonical account of what actually limits
    titer; tells you which features belong in the index.
16. **Zou et al. 2022, α-mating factor and endogenous signal peptides in K. phaffii,
    10.1186/s13068-022-02243-6** — the evidence base for the secretion-leader feature.
17. **Barrigón et al. 2015, macrokinetic meta-analysis of P. pastoris production, 10.1002/bit.25518**
    — read specifically to understand why published titers are not comparable; this is your defence
    against the main examiner objection.
18. **Li et al. 2025, Unlocking the potential of Trichoderma reesei as a super-host,
    10.1002/biot.70121** — the best current T. reesei review; the fungal half of the comparison.
19. **Nyyssönen et al. 1995, Multiple roles of CBHI in enhancing fusion antibody production,
    10.1007/bf00311884** — the original carrier-fusion strategy the thesis must model for T. reesei.

## Tier 4 — the target proteins

20. **Järvinen et al. 2022, Production of bovine β-lactoglobulin and hen egg ovalbumin by
    Trichoderma reesei (Food Research International, S0963996922011899)** — the single most important
    validation datapoint: both targets, the right host, with techno-functional testing.
21. **Heterologous Caseins: The Role of Phosphorylation in Their Functionality and How to Achieve It
    (PMC12292773)** — defines exactly what the casein PTM penalty is and whether it can be engineered
    away.
22. **Holt 2021, A quantitative calcium phosphate nanocluster model of the casein micelle,
    10.1007/s00249-021-01533-5** — tells you which casein PTMs are functionally indispensable rather
    than merely present.
23. **High-level secretory production of leghemoglobin in P. pastoris through enhanced globin
    expression and heme biosynthesis, 10.1016/j.biortech.2022.127884** — the leghemoglobin titer
    anchor, and the cofactor-supply constraint to model.

## Tier 5 — methods caveats and economics

24. **Systematic identification of conditionally folded intrinsically disordered regions by
    AlphaFold2, 10.1073/pnas.2304302120** (with **Zhao & Kurgan 2023, 10.1016/j.csbj.2023.06.001**)
    — read before trusting any AlphaFold output on caseins; the methodological caveat the examiners
    will probe.
25. **Downstream Processing of Food Proteins from Precision Fermentation, Annu Rev Food Sci Technol,
    10.1146/annurev-food-060424-091647** (with **Humbird 2021, 10.1002/bit.27848** as the sceptical
    counterweight) — read together: the first gives recovery and cost structure, the second stops the
    TEA chapter from being optimistic by default.
