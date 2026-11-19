# Chapter 6 — What the gap tracks

Chapter 5 established a gap of one to four orders of magnitude between what metabolism permits and what has been achieved, and showed that the bound is some thirty times less dispersed than the outcome. This chapter asks what the outcome *is* explained by.

The answer is that nothing about the protein explains it. None of the seven features specified in advance is associated with titre, and the model containing them performs worse than a model containing only an indicator of how the fermentation was run. That is the chapter's result, and §§6.2–6.4 establish it.

Two candidate positive findings arose during this work and neither survived. Disulfide bond density was reported in an earlier draft at ρ = −0.438, p = 0.036; §6.2.1 records how re-reading the counts from the UniProt feature tables removed it. Mean predicted disorder was reported at ρ = −0.833 by an independent analysis of the same literature, and fell to ρ = −0.483, p = 0.117 once three faults in the underlying titre records were corrected (§6.5, Appendix F).

The design was fixed before the analysis ran and is stated in §3.10. It is repeated in outline here because the credibility of a small-sample result depends entirely on whether the analyst could have fished.

## 6.1 The dataset

Applying the inclusion rules to the rebuilt corpus gives **53 records over 25 distinct proteins**: secreted production in *K. phaffii* or *P. pastoris*, high-confidence evidence, CRC64-verified sequence available, fragments and fusions excluded. The response is log₁₀ of titre in mg L⁻¹, which spans just under four orders of magnitude.

Seven mechanistic features were specified in advance: log length, disulfides per 100 residues, N-glycosylation sequons per 100 residues, disordered fraction, GRAVY hydropathy, absolute mean net charge per residue, and the maximum theoretical yield from Chapter 4. A fed-batch indicator was included because the corpus documents within-study flask-to-bioreactor ratios of 8- to 88-fold, which would otherwise masquerade as a protein property.

Two measurement choices matter to what follows. Disulfide counts are read from the UniProtKB feature tables for all 36 accessions rather than assumed as cysteines ÷ 2, an assumption wrong for 15 of the 36 by up to eight bonds (§3.5); and disorder is measured with metapredict v3 rather than FoldIndex alone.

Univariate associations are computed **per protein**, using each protein's best reported titre, so that a well-studied protein with many records does not dominate.

## 6.2 The result that did not survive

**Table 6.1 — Univariate association with best log titre (n = 25 proteins)**

| Feature | Spearman ρ | p | permutation p | 95% CI | q (BH) |
|---|---|---|---|---|---|
| log length | +0.232 | 0.265 | 0.260 | −0.230 to +0.616 | 1.000 |
| disulfides per 100 residues | −0.188 | 0.369 | 0.366 | −0.570 to +0.259 | 1.000 |
| absolute net charge per residue | +0.175 | 0.403 | 0.409 | −0.299 to +0.572 | 0.940 |
| GRAVY | −0.122 | 0.560 | 0.558 | −0.553 to +0.338 | 0.940 |
| sequons per 100 residues | +0.111 | 0.598 | 0.595 | −0.277 to +0.477 | 0.837 |
| maximum theoretical yield | +0.062 | 0.770 | 0.766 | −0.351 to +0.468 | 0.837 |
| disordered fraction | −0.007 | 0.974 | 0.975 | −0.466 to +0.420 | 0.837 |

**Nothing is associated with titre.** No feature reaches p = 0.05 uncorrected, let alone the Bonferroni threshold of 0.0071 or a Benjamini–Hochberg q below 0.05. Every confidence interval spans zero. The permutation p-values, computed by 20,000 relabellings because an asymptotic p is not trustworthy at this sample size, agree with the asymptotic ones to three decimal places.

### 6.2.1 How the disulfide result was lost

An earlier draft reported disulfide density at ρ = −0.438, p = 0.036 as the thesis's one positive finding, not surviving multiple-testing correction (q = 0.255). Two things then changed at once: the corpus was rebuilt and roughly doubled, and disulfide counts were taken from the UniProt annotation instead of being assumed. Changing two things at once is not a diagnosis, so each was changed separately.

**Table 6.2 — The same association under each change**

| Corpus | Disulfide measure | *n* proteins | Spearman ρ | p |
|---|---|---|---|---|
| Original records | assumed, cysteines ÷ 2 | 23 | −0.423 | **0.045** |
| Original records | annotated, UniProt | 23 | −0.307 | 0.155 |
| Merged corpus | assumed, cysteines ÷ 2 | 25 | −0.294 | 0.154 |
| Merged corpus | annotated, UniProt | 25 | −0.188 | 0.369 |

Either change alone removes the result, so it was both a small-sample finding that failed to replicate and a measurement artefact, each sufficient on its own. The measurement half matters more: assuming cysteines pair up is a defensible convention, uniformly applied and documented as an assumption, and it was still wrong for 15 of 36 proteins. Human basic fibroblast growth factor has six cysteines and no annotated bonds at all; type III collagen has twenty-two cysteines and three intramolecular bonds, the rest inter-chain. The assumption over-assigned bonds to exactly the cytosolic, fibrous and reduced proteins whose titres sit at the extremes — the only variable the positive result rested on. In a seven-feature, twenty-five-protein analysis, the feature a positive result rests on is the one whose measurement must be verified first, and an assumption applied uniformly is not thereby a measurement.

## 6.3 The negative results, which are the informative ones

### 6.3.1 Metabolic cost does not predict titre

The maximum theoretical yield has essentially zero association with titre (ρ = +0.062, p = 0.770). This is the empirical counterpart of Chapter 5's narrow ceiling, obtained independently: Chapter 5 showed the bound barely varies, and Chapter 6 shows that what little variation exists carries no information about the outcome.

Together these close the question the thesis was built to ask. **The binding constraint on producing food proteins in *K. phaffii* is not the metabolic cost of building them.** This is a negative result about a widely assumed mechanism, obtained from two independent directions, and it is the most useful thing in this thesis because it tells a developer where *not* to spend.

### 6.3.2 Disorder, as pre-specified, does not predict titre

The pre-specified disorder feature — the fraction of residues scoring above 0.5 — shows no association whatsoever (ρ = −0.007, p = 0.974). This is the feature as declared in §3.10, and reported on its own terms it is a null. **It is also the wrong summary of the predictor, and §6.5 is given over to why**: the thresholded fraction is identically zero for every globular protein in the panel, so it discards the gradient that the mean score retains. The null below stands as the result for the feature as pre-specified; the mean-score result is in §6.5 and is labelled throughout as a replication of an externally generated hypothesis rather than as one of the seven.

Disorder is measured with metapredict v3, with FoldIndex retained alongside it for every protein (§3.6), so the null is not a failure of the instrument: the neural predictor separates the panel cleanly and in the expected direction — κ-casein 1.00 disordered fraction, α-S1-casein 0.63, α-S2-casein 0.58, β-casein 0.46, against 0.00 for β-lactoglobulin, α-lactalbumin, ovalbumin and leghemoglobin and 0.02 for lactoferrin. On this corpus, disorder as measured by a current neural predictor carries no information about titre.

What remains is a coverage limitation. The feature most characteristic of caseins can barely be tested on a casein: only one is in the dataset, bovine κ-casein, the most disordered protein in the corpus at a disordered fraction of 1.00, and it sits near the bottom of the table at 0.06% of its ceiling. That is one point in the direction the hypothesis predicts, and one point is an anecdote. α-S1-, α-S2- and β-casein still have no titre in these hosts, so the hypothesis remains under-tested at exactly the end of the corpus where it would be decided.

### 6.3.3 Glycosylation sequons do not predict titre

Sequon density shows nothing (ρ = +0.111, p = 0.598). Given Chapter 4's finding that glycosylation is the one expensive modification, this is worth pausing on. The likely explanation is that the metabolic cost of glycosylation, while the largest in the panel, is still only an 8–9% effect at the core-glycan level, and an 8% effect cannot be detected against a residual spread of 0.85 in log₁₀. The hypermannosylation penalty is far larger, but how heavily any given protein is hypermannosylated in any given study is not reported, so it cannot enter the model as a variable.

### 6.3.4 The food-protein subset, tested separately

Eleven of the 25 proteins are human therapeutics, developed under a cost structure that justifies effort no food protein can. Refitting on the 14 food and food-adjacent proteins alone — 32 records — changes which feature comes closest to significance without changing the conclusion:

| Feature | Spearman ρ | p | q (BH) |
|---|---|---|---|
| absolute net charge per residue | +0.607 | 0.021 | 0.149 |
| GRAVY | +0.442 | 0.114 | 0.149 |
| disulfides per 100 residues | −0.383 | 0.177 | 0.149 |
| maximum theoretical yield | −0.244 | 0.401 | 0.149 |
| sequons per 100 residues | +0.208 | 0.475 | 0.149 |
| log length | +0.099 | 0.737 | 0.149 |
| disordered fraction | −0.082 | 0.781 | 0.149 |

Disulfide density is **absent** here rather than weak: on the external dairy, egg and haem panel it is ρ = +0.115, p = 0.70, with the sign reversed. Net charge is the nearest thing to a signal among the pre-specified features, at ρ = +0.607 and an uncorrected p of 0.021, and it is reported as what it is: a seventh test on fourteen proteins, with a q of 0.149 and a confidence interval running from +0.065 to +0.892. It was not pre-specified as a directional hypothesis and it has no stated mechanism behind it: a more charged protein secreting *better* is not what the solubility literature would predict. It is recorded as a hypothesis for a future, larger corpus and nothing is built on it.

## 6.4 All of the model's skill is the process term

A ridge regression over the eight predictors, cross-validated by leaving out all records of each protein together, is reported against two nested controls. The controls are the point of the exercise. A fed-batch bioreactor run beats a shake flask by one to two orders of magnitude, so a model containing a fed-batch indicator can look predictive while knowing nothing whatever about the protein.

**Table 6.3 — Leave-one-protein-out performance, 53 records over 25 proteins**

| Model | RMSE (log₁₀) | Skill vs predict-the-mean | Spearman ρ |
|---|---|---|---|
| Predict the mean (baseline) | 0.908 | — | — |
| **Process term only** (fed-batch indicator) | **0.764** | **+15.9%** | 0.207 (p = 0.136) |
| Seven sequence features + process term | 0.816 | +10.1% | 0.543 (p < 0.001) |
| **Seven sequence features, no process term** | **0.984** | **−8.3%** | 0.089 (p = 0.528) |

The ordering is unambiguous. A single binary indicator of whether the run was in a bioreactor recovers 15.9% of the error against the baseline. Adding seven mechanistic sequence features to it *reduces* performance to 10.1%. The sequence features on their own are worse than predicting the mean, by 8.3%.

The same pattern holds in the food subset: process term alone +10.6% skill, sequence features plus process term −11.4%. Being food or therapeutic does not rescue the features.

This also disposes of the rank correlation. The full model's predictions correlate with observed titre at ρ = 0.543, p < 0.001, which read on its own looks like a result. The process-only model, which contains no sequence information at all, achieves better RMSE with a *lower* rank correlation. A model can rank tolerably while predicting badly, and a rank correlation reported without a baseline is not evidence of skill. That is why the baseline row is in the table.

**The finding of this chapter is simple.** It is not that the sequence features are weak predictors; it is that they carry no signal that survives a control for how the fermentation was run, on a corpus of 53 records over 25 proteins with annotation-grade features and a pre-specified design. A residual standard deviation of 0.76 in log₁₀, after the process term is accounted for, means a typical protein's reported titre remains uncertain by nearly a factor of six for reasons the protein does not explain.

## 6.5 The disorder result, and why it is not reported as a finding

Of all the features that could explain the gap, predicted disorder is the one with a mechanism waiting for it: the caseins are disordered, the caseins are hard, and *K. phaffii* secretes into a protease-rich supernatant where a chain with no folded core has nothing to protect it. It nearly became this thesis's positive result.

An independent analysis of the same literature reported mean metapredict disorder at ρ = −0.833, permutation p = 0.00025, q = 0.008. This thesis's own pre-specified disorder feature had returned nothing, and the audit established that this was a real error on this side: the pre-specified feature was the *fraction of residues scoring above 0.5*, which is identically zero for every globular protein in the panel and so collapses twelve of fourteen proteins to one tied value. From the same predictions, the two statistics give ρ = −0.72 and ρ = −0.31. **Pre-specifying a feature does not make it the right summary of what it measures**, and that lesson stands whatever happened to the result.

What happened to the result is that it did not survive its own data. The correlation was a contrast between two clusters rather than a trend — within the globular twelve it fell to ρ = −0.455, p = 0.138 — and three faults in the underlying titre records, described in Appendix F, removed one of the two disordered proteins entirely. Corrected, the association is **ρ = −0.483, p = 0.117, with nothing surviving FDR correction**, and it has been retracted. On this thesis's corpus the comparable figure is ρ = −0.612, p = 0.060 across the ten dairy, egg and haem proteins with titres, falling to −0.116 across the full corpus.

**So there is no disorder finding.** What there is, consistently, is a negative sign — eleven fits out of eleven — of a magnitude the data cannot distinguish from chance, resting in every version on the contrast between κ-casein and everything else. One protein is not a test of a hypothesis about a protein class. The three caseins with no published titre in any microbial host, α-S1, α-S2 and β, are the three most disordered proteins in the target class, and measuring them would decide this; that is §9.5's first experimental recommendation.

## 6.6 What the variance is actually in

Section 5.2.2 gives this question a quantitative answer. A crossed random-effects model over 88 records, 30 proteins and 52 studies places 44% of the variance in log₁₀ utilisation between proteins, 16% between studies of the same protein and 40% within studies, and the mean log₁₀ spread inside a single protein is 0.638 against 0.892 corpus-wide. Adding the seven sequence features halves the between-protein component, from 0.254 to 0.127, while the residual does not move (0.232 against 0.235). A regressor that absorbs the random intercept without reducing the residual is relabelling the groups, not predicting from them — which is the same conclusion §6.4 reaches by cross-validation, in the form that a reviewer is least able to argue with.

Within that frame, three sources dominate, and none of them is a property of the molecule.

**Engineering effort.** β-lactoglobulin reaches 6.1% of its ceiling and human α-lactalbumin 0.31%, a twentyfold difference between two small whey proteins of similar size and nearly identical stoichiometric cost. The record for β-lactoglobulin comes from a study that rewired host metabolism using omics guidance; the α-lactalbumin records come from smaller studies of chaperone co-expression and CRISPR editing efficiency. These are not comparable levels of investment, and the corpus contains no measure of investment to control for. The nested-control result of §6.4 is the quantitative version of this paragraph: the one variable in the corpus that does carry information is a variable about the experiment, not about the protein.

**Strain and process.** Promoter choice, secretion leader, gene copy number, protease deletion, feeding strategy, induction temperature and dissolved-oxygen control each move titres by factors that rival the entire between-protein spread. The corpus records some of these variables sporadically and none of them completely.

**Publication bias.** Low titres are reported when a paper is about something else — a new chaperone, a new promoter, a demonstration of feasibility — and high titres when the paper is about the titre. The distribution of published numbers is not the distribution of achievable numbers.

This is a confound the design cannot remove, and it is the reason the negative result in §6.4 should be read as a statement about the literature rather than only about the model. **The published record of recombinant protein titres is, to first order, a record of how much work was done, not of how hard each protein is.**

## 6.7 Consequences

**For the field.** Comparative statements of the form "protein X is more tractable than protein Y", when supported by titres drawn from different studies, are weakly supported at best. The only clean comparisons are within-study ones, and the corpus contains few.

**For a developer.** Of the three candidate bottlenecks named in the project brief, one can be excluded with numbers and the other two can be characterised but not ranked. Metabolic cost is excluded, from two independent directions. Post-translational modification splits cleanly: phosphorylation is energetically free and is therefore a missing-enzyme problem rather than a cost problem (§4.3.1), while glycosylation is the one metabolically expensive modification and is worth up to 41% of polypeptide yield under hypermannosylation (§4.3.4). Folding remains the leading candidate for the residual, but this chapter does not establish it: the disulfide association that appeared to support it did not survive correct measurement (§6.2.1). The positive evidence for folding is now the mechanism reported in the sources themselves — the κ-casein study's proteolysis and saturating copy-number response, the host literature's response to protein disulfide isomerase overexpression — rather than anything this chapter measured.

**For the method.** The right successor to this analysis is a model that represents the secretory machinery explicitly, because that is where the evidence now points and where a stoichiometric model is blind. pcSecYeast is the obvious vehicle. This is set out in Chapter 9.

**For the thesis's own claim.** The expectation declared in Chapter 2 — that whey proteins would rank as most tractable and caseins and lactoferrin least — is not recovered. α-lactalbumin, a "tractable" whey protein, sits below lactoferrin, ovalbumin and lysozyme. That is reported as a contradiction rather than reconciled, because the declaration was made in advance precisely so that it could be.

