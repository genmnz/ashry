# Prior-art assessment: is a producibility index for food proteins in *K. phaffii* / *T. reesei* still unclaimed?

Scope of this document. It assesses cluster 9 of the literature search: work that (a) ranks or
compares multiple food proteins for microbial producibility, (b) builds a predictive model of
recombinant protein titer from sequence features, or (c) computes protein-specific metabolic
cost or yield in *Komagataella phaffii*. Everything cited here was retrieved during the search and
appears in `bibliography.csv`. Where a DOI could not be confirmed from a retrieved record, the
bibliography leaves the DOI field blank and gives the URL that was actually fetched.

---

## 1. What the three strands of prior art actually contain

### Strand (a): ranking or comparing food proteins for producibility

The single most dangerous item found is **Guo et al. (2026), "Toward Rational Design of
Precision-Fermented Milk Proteins: Integrating Cross-Species Selection, Post-Translational
Modification, and AI Optimization", *Comprehensive Reviews in Food Science and Food Safety*,
10.1111/1541-4337.70618**. It is indexed as a Review. Its abstract performs exactly the
qualitative ranking the thesis proposes to quantify: it states that
"α-Lactalbumin and β-lactoglobulin are the most tractable targets given minimal PTM dependency",
and it places caseins and lactoferrin in a harder tier because they require phosphorylation and
glycosylation that microbial hosts do not natively deliver. It also covers cross-species sequence
selection (human vs bovine vs goat vs camel), host engineering, downstream purification, and an
appraisal of AI-driven optimisation, concluding that AI accelerates process optimisation but cannot
yet co-optimise yield, folding fidelity and PTM accuracy.

This means the *conclusion* the thesis is likely to reach for milk proteins is already in print.
What is not in print is the *derivation*. Guo et al. assert tractability from narrative reasoning
about PTM dependency; they publish no score, no weighting, no stoichiometry, no model, no
validation against titers, and no reproducible pipeline. The ordering is an expert judgement, not a
measurement. The review also restricts itself to milk proteins — it does not cover ovalbumin,
other egg-white proteins, or leghemoglobin, so the thesis panel is strictly wider.

Two other items sit in this strand. **"Advances in the biosynthesis of milk proteins fueled by
synthetic biology" (10.1007/s44462-026-00065-5)** and **"Engineering *Trichoderma reesei* into a
programmable eukaryotic chassis for efficient production of raw materials in the food industry"**
(Trends in Food Science and Technology, S0924224426003432) both survey the same territory from the
host side. Neither was readable in full during this search; both must be obtained and read before
the novelty claim is finalised, because a chassis review that happens to tabulate per-protein
titers would narrow the gap considerably. GFI's **"Deep dive: Fermentation protein ingredients and
food functionality"** does something similar in grey literature: it discusses which food proteins
are considered commercially tractable, again without a quantitative index.

### Strand (b): predicting titer or expressibility from sequence

This strand is well populated and, importantly, almost entirely outside food proteins.

**Presep (PLOS ONE 2013, 10.1371/journal.pone.0079749)** is the closest host-matched item: a
classifier that predicts the propensity of a protein to be secreted into the supernatant *when
expressed in Pichia pastoris*. This is a sequence-to-secretion model in the exact host. It is,
however, a binary/propensity classifier for secretion success, trained in 2013 on a
pre-language-model feature set; it does not predict titer, does not treat PTM requirements, and
does not touch metabolism.

**"Deciphering the determinants of recombinant protein expression across the human secretome"
(PNAS 2025, 10.1073/pnas.2506036122)** is the strongest modern entry: a secretome-scale empirical
dissection of what makes proteins express well. **"Deep protein representations enable recombinant
protein expression prediction"** (Comput Struct Biotechnol J, S1476927121001663) and
**ExpressUrself (10.1101/2022.12.02.518907)** build sequence-feature and spatial models of
expression. **"Analysis of 11,430 recombinant protein production experiments..."
(10.1371/journal.pcbi.1009461)** shows yield is tunable by synonymous changes at translation
initiation sites — a large-N sequence-to-yield analysis. **PERISCOPE-Opt** does ML titer and
condition prediction, but in *E. coli* periplasm. **"Predicting Membrane Protein Expression in
Yeast from Sequence-Derived Features"** does the same for membrane proteins in yeast.
**"Forecasting Host Cells for Recombinant Protein Expression" (10.11648/j.bmb.20261101.11)**
explicitly forecasts which host suits a protein — conceptually the nearest thing to a
producibility index, though published in a low-visibility venue and not validated on food proteins.
The *Trends in Biotechnology* opinion **"Can protein expression be 'solved'?"**
(S0167-7799(25)00166-0) is the field's own statement that the problem is open.

Adjacent and methodologically relevant: the biologics **developability index** tradition
(Developability Index for antibody aggregation; "Holistic in silico developability assessment of
novel classes of biologics", 10.1101/2023.11.10.566515; "High-throughput developability assays
enable library-scale identification of producible protein scaffold variants",
10.1073/pnas.2026658118). This establishes that composite sequence-based producibility scores are
a legitimate, accepted construct — but for therapeutic scaffolds, with aggregation and stability as
the objective, not fermentation yield in a food host.

### Strand (c): per-protein metabolic cost and yield in *K. phaffii*

This is where the thesis has its firmest ground, and also its sharpest single threat.

The sharpest threat is **"Genome-scale reconstructions of the mammalian secretory pathway predict
metabolic costs and limitations of protein secretion" (Nature Communications 2020,
10.1038/s41467-019-13867-y)**. This does precisely the conceptual thing the thesis proposes:
stoichiometrically reconstructs the secretory pathway and computes *per-protein* metabolic costs
and secretion limits. It is, however, mammalian (CHO-oriented). Its yeast ancestor is
**Feizi et al. (2013), "Genome-Scale Modeling of the Protein Secretory Machinery in Yeast"
(10.1371/journal.pone.0063284)** — *S. cerevisiae*, not *K. phaffii*, and not applied to food
proteins.

In *K. phaffii* specifically: **iMT1026v3** (Tomàs-Gamisans et al., 10.1111/1751-7915.12871), the
**iPichia consensus model** (Biochem Eng J, S1369703X25003146) and its **GPR curation**
(10.1002/bit.70402), **Kp1.0**, **Irani et al. (10.1002/bit.25863)** which couples native and
humanised glycosylation stoichiometry into a K. phaffii GEM, **Torres et al.
(10.1016/j.mec.2019.e00103)**, the 2012 constraint-based estimate of recombinant protein production
(S0959152412000741), the first K. phaffii GEM applied to heterologous protein analysis (Chung et
al.), and the **proteome-constrained yeast modelling** paper (10.1038/s41467-022-30689-7). There is
also a direct FBA study of **heme biosynthesis in K. phaffii** (Sci Rep, PMC10516909), which
pre-empts part of the leghemoglobin cofactor analysis.

On the cost side, the framework exists but has not been pointed at food proteins: **Akashi &
Gojobori (10.1073/pnas.062526999)** for amino-acid biosynthetic cost, the yeast-specific
**"Evolutionary Systems Biology of Amino Acid Biosynthetic Cost in Yeast"
(10.1371/journal.pone.0011935)**, **O'Brien et al. ME-models (10.1038/msb.2013.52)**, **GECKO
(10.15252/msb.20167411)**, and **Burić et al. 2025 (10.1002/pro.5239)**, which ties sequence,
stability and synthesis cost to abundance — the clearest existing bridge between the thesis's
stoichiometric and sequence halves.

Crucially: **no retrieved item computes protein-specific metabolic cost or maximum theoretical
yield for a panel of named food proteins in *K. phaffii* or *T. reesei*, and none validates such
numbers against published food-protein titers.** The components all exist; the assembly does not.

---

## 2. What is genuinely unclaimed

Stating it precisely, because the defensibility of the thesis depends on the precision:

1. **A stoichiometrically derived, per-protein yield and cost figure for a defined panel of food
   proteins** (caseins α-s1/α-s2/β/κ, β-lactoglobulin, α-lactalbumin, lactoferrin, ovalbumin and
   other egg-white proteins, soy leghemoglobin) in *K. phaffii* and *T. reesei*, on named carbon
   sources, from a current model. Nobody has done this panel in these hosts.
2. **A composite index that fuses that stoichiometric cost with sequence-derived folding, PTM and
   aggregation burden.** The two literatures — GEM/cost modelling and sequence-based
   expressibility — have not been joined for food proteins. Guo et al. join them only rhetorically.
3. **Validation of a producibility ordering against published titers.** Guo et al. assert an
   ordering and do not test it. Presep and the PNAS secretome paper test sequence models but not
   against food-protein titers. Nobody has assembled the food-protein titer table and scored a
   prediction against it.
4. **Cross-host comparison on the same footing.** *T. reesei* and *K. phaffii* are reviewed
   separately; no study computes the same per-protein cost in both and compares.

## 3. Verdict on defensibility

The novelty claim is defensible, but **only if it is stated as a method-and-validation claim, not a
findings claim**. If the thesis's headline is "α-lactalbumin and β-lactoglobulin are the easiest
targets and caseins the hardest", it is scooped by Guo et al. (2026) and by the general consensus
of the precision-fermentation reviews. If the headline is "here is a reproducible, stoichiometry-
grounded, sequence-informed index that reproduces the known ordering, quantifies the gaps between
tiers, extends the ordering to proteins nobody has ranked, and is tested against published titers",
that is new work and the overlap with Guo et al. becomes an *asset*: an independent qualitative
prediction the index can be checked against.

The thesis should therefore be framed as supplying the derivation for a claim the field currently
holds on authority. Recovering a known ordering from first principles is a validation result, not a
redundancy — provided the thesis says so explicitly and in advance, rather than appearing to
discover it.

Two conditions must be met. First, the panel must extend beyond milk proteins; the egg-white and
leghemoglobin targets are what make the work wider than Guo et al. Second, the validation must be
real: a titer table assembled from primary sources (the VTT *T. reesei* β-lactoglobulin/ovalbumin
work in Food Research International; the α-lactalbumin work in *J. Agric. Food Chem.*; the
phosphorylated α-s1-casein work from Wageningen; the K. phaffii leghemoglobin work in
*Bioresource Technology*; the Barrigón et al. meta-analysis for non-food comparators), with
honest treatment of how incomparable those numbers are.

## 4. The strongest objection an examiner can raise, and the answer

**The objection.** "Your index has no predictive power you can demonstrate. Published titers are
not a validation set: they differ in strain background, promoter, copy number, leader sequence,
bioreactor mode, induction regime, measurement method and the amount of unpublished optimisation
behind them. The spread from process engineering alone spans orders of magnitude — Barrigón et
al.'s meta-analysis exists precisely because K. phaffii productivities are not comparable across
studies. With a handful of food proteins and that much nuisance variance, any ordering you
'validate' is consistent with your index, with Guo et al.'s narrative reasoning, and with chance.
Moreover, the stoichiometric cost term is close to constant: proteins of similar length and amino
acid composition cost almost the same number of ATP and precursors, so the maximum theoretical
yields will be nearly identical and will not discriminate between targets. Real titers differ by
orders of magnitude for reasons — folding, proteolysis, UPR saturation, secretion-machinery
capacity — that your model does not actually mechanise. So the stoichiometric half is
uninformative and the sequence half is unvalidated."

This objection is strong because both halves of it are substantially true. It should not be
deflected; it should be pre-empted.

**The answer, in four moves.**

*First, concede the yield point and convert it into a result.* It is very likely correct that
maximum theoretical yields for these proteins cluster tightly — that is a *finding*, not a failure.
If stoichiometry says every target should give similar grams per gram of substrate, and observed
titers span two orders of magnitude, then the thesis has quantified the size of the
non-stoichiometric gap. That gap is the thing worth measuring. The index's job is then explicitly
to explain the residual after stoichiometry, and the honest headline becomes: carbon and ATP
accounting is *not* what separates easy from hard food proteins, and the thesis can say by how much.
This is a much more defensible claim than "my index predicts titer", and it directly rebuts the
"uninformative" charge by making the uninformativeness the measurement.

*Second, do not claim quantitative prediction; claim ordinal, pre-registered, out-of-sample
discrimination.* Commit the index weighting in writing before looking at the titer table. Then
report rank correlation (Spearman, with a confidence interval) and, more importantly, report it on
the subset the index was *not* tuned on. With a panel this small the honest statement is "the index
separates tiers, not individual proteins", and that should be the stated resolution of the
instrument from the outset. Claiming less than the data supports is the only way to survive this
objection.

*Third, handle the nuisance variance explicitly rather than hoping it cancels.* Record, for every
titer in the validation table, the host, promoter, leader, copy number, cultivation mode and assay.
Then show the index's ordering survives stratification — for example, restricted to fed-batch
secreted products in K. phaffii under AOX1. Where stratification leaves too few points to say
anything, say that. Cite Barrigón et al. as the reason this discipline is necessary, which turns a
weakness into evidence of methodological awareness.

*Fourth, add one falsifiable mechanistic commitment.* The objection's real sting is that the model
does not mechanise folding or secretion capacity. Partly fix this: incorporate a secretory-pathway
cost term in the manner of Feizi et al. and the mammalian secretory reconstruction, so that
disulfide bonds, glycan assembly and ER processing carry explicit stoichiometric and energetic cost
rather than appearing only as a sequence heuristic. Then state a specific prediction the index makes
that could be wrong — for instance, that at matched cassette design, κ-casein's producibility
penalty relative to α-lactalbumin is driven by PTM/disorder terms rather than by cost, and that
removing the glycosylation requirement should move it by a predicted amount. A thesis that names
its own falsification condition is far harder to dismiss as unvalidated curve-fitting.

A fifth, non-technical point is worth making in the defence: the index's value is partly decision-
theoretic. Even a weak ordering, if it is transparent and reproducible, is more useful to someone
choosing a target than an expert assertion in a review, because it exposes its assumptions and can
be re-run when a weight or a model version changes. That is a legitimate contribution even at
modest predictive accuracy — but it must be argued as such, not smuggled in behind an
overclaimed correlation.

## 5. Residual risk and what to do next

Three items could not be read in full and remain the live risk: the **iPichia consensus model**
paper, **"Advances in the biosynthesis of milk proteins fueled by synthetic biology"**, and the
**T. reesei programmable-chassis review**. Obtain all three. Also obtain the **DTU PhD thesis
"Precision fermentation of milk proteins" (Balasubramanian)**, which covers the same problem space
at thesis length and is the most likely source of unflagged overlap. Finally, set a standing alert
on the Guo et al. citation graph: a quantitative follow-up to that review is the most plausible
route by which this thesis gets scooped in the next twelve months.
