# Chapter 6 — What the gap tracks

Chapter 5 established a gap of one to four orders of magnitude between what metabolism permits and what has been achieved, and showed that the bound is some thirty times less dispersed than the outcome. This chapter asks what the outcome *is* explained by. It reports no positive result. Every pre-specified sequence feature fails, the model that contains them performs worse than one that does not, and the conclusion is drawn entirely from the negatives.

An earlier draft of this chapter did report a positive result — disulfide bond density, negatively associated with titre — and §6.2 records in full how it was lost, because the way it was lost is itself a finding about how this kind of analysis goes wrong.

The design was fixed before the analysis ran and is stated in §3.10. It is repeated in outline here because the credibility of a small-sample result depends entirely on whether the analyst could have fished.

## 6.1 The dataset

Applying the inclusion rules to the rebuilt corpus gives **53 records over 25 distinct proteins**: secreted production in *K. phaffii* or *P. pastoris*, high-confidence evidence, CRC64-verified sequence available, fragments and fusions excluded. The response is log₁₀ of titre in mg L⁻¹, which spans just under four orders of magnitude.

Seven mechanistic features were specified in advance: log length, disulfides per 100 residues, N-glycosylation sequons per 100 residues, disordered fraction, GRAVY hydropathy, absolute mean net charge per residue, and the maximum theoretical yield from Chapter 4. A fed-batch indicator was included because the corpus documents within-study flask-to-bioreactor ratios of 8- to 88-fold, which would otherwise masquerade as a protein property.

Two measurement changes since the first draft matter to what follows. Disulfide counts are now read from the UniProtKB feature tables for all 36 accessions rather than assumed as cysteines ÷ 2; the assumption was wrong for 15 of the 36, by up to eight bonds (§3.5). And disorder is now measured with metapredict v3, a neural predictor, rather than with FoldIndex alone.

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

### 6.2.1 How the disulfide result was lost, and why it is worth reporting

The first draft of this chapter reported disulfide density at ρ = −0.438, p = 0.036, as the thesis's one positive finding, with the caveat that it did not survive multiple-testing correction (q = 0.255). Two things then changed at once: the corpus was rebuilt and roughly doubled, and disulfide counts were taken from the UniProt annotation instead of being assumed. Changing two things at once is not a diagnosis, so each was changed separately.

**Table 6.2 — The same association under each change**

| Corpus | Disulfide measure | *n* proteins | Spearman ρ | p |
|---|---|---|---|---|
| Original records | assumed, cysteines ÷ 2 | 23 | −0.423 | **0.045** |
| Original records | annotated, UniProt | 23 | −0.307 | 0.155 |
| Merged corpus | assumed, cysteines ÷ 2 | 25 | −0.294 | 0.154 |
| Merged corpus | annotated, UniProt | 25 | −0.188 | 0.369 |

Either change alone removes the result. It was therefore not simply a small-sample finding that failed to replicate in a larger one, and not simply a measurement artefact: it was both, each sufficient on its own.

The measurement half deserves the emphasis. Assuming that cysteines pair up is a defensible, uniformly applied convention, and it was documented as an assumption rather than smuggled in. It was still wrong for 15 of 36 proteins. Human basic fibroblast growth factor has six cysteines and no annotated disulfide bonds at all: it is a cytosolic growth factor whose cysteines are free, and the assumption gave it three bonds. Ovalbumin has six cysteines and one bond. Type III collagen has twenty-two cysteines and three intramolecular bonds, the rest being inter-chain in the triple helix. The assumption systematically over-assigned bonds to exactly the proteins — cytosolic, fibrous, or secreted but reduced — whose titres sit at the extremes of the distribution, and it was the only variable the chapter's positive result rested on.

The general lesson is not about disulfides. It is that in a seven-feature, twenty-five-protein analysis, the feature a positive result rests on is the one whose measurement must be verified first, and an assumption applied uniformly is not thereby a measurement. This is reported at length because the alternative — quietly dropping a finding that an earlier draft announced — would be the dishonest option.

## 6.3 The negative results, which are the informative ones

### 6.3.1 Metabolic cost does not predict titre

The maximum theoretical yield has essentially zero association with titre (ρ = +0.062, p = 0.770). This is the empirical counterpart of Chapter 5's narrow ceiling, obtained independently: Chapter 5 showed the bound barely varies, and Chapter 6 shows that what little variation exists carries no information about the outcome.

Together these close the question the thesis was built to ask. **The binding constraint on producing food proteins in *K. phaffii* is not the metabolic cost of building them.** This is a negative result about a widely assumed mechanism, obtained from two independent directions, and it is the most useful thing in this thesis because it tells a developer where *not* to spend.

### 6.3.2 Disorder does not predict titre

Predicted intrinsic disorder shows no association whatsoever (ρ = −0.007, p = 0.974). This is uncomfortable, because disorder is the standard explanation offered for why caseins are hard, and it deserves to be stated carefully rather than read as a triumph.

The measurement is no longer the weak point. The first draft of this chapter measured disorder with FoldIndex alone, a 2005-vintage charge–hydropathy criterion, and had to carry the caveat that a better predictor might find what FoldIndex missed. Disorder is now measured with metapredict v3, and the two measures are reported side by side for every protein (§3.6). The neural predictor separates the panel cleanly and in the expected direction — κ-casein 1.00 disordered fraction, α-S1-casein 0.63, α-S2-casein 0.58, β-casein 0.46, against 0.00 for β-lactoglobulin, α-lactalbumin, ovalbumin and leghemoglobin and 0.02 for lactoferrin — so the null is not a failure of the instrument. On this corpus, disorder as measured by a current neural predictor carries no information about titre.

What remains is a coverage limitation, and it is narrower than it was. When this chapter was first drafted no casein had a published titre at all, so the feature most characteristic of caseins could not be tested on a casein. One is now in the dataset: bovine κ-casein, the most disordered protein in the corpus at a disordered fraction of 1.00, sits near the bottom of the table at 0.06% of its ceiling. That is one point in the direction the hypothesis predicts, and one point is an anecdote, not a test. α-S1-, α-S2- and β-casein still have no titre in these hosts, so the disorder hypothesis remains under-tested at the end of the corpus where it would be decided.

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

Net charge is the nearest thing to a signal anywhere in this chapter, at ρ = +0.607 and an uncorrected p of 0.021, and it is reported as what it is: a seventh test on fourteen proteins, with a q of 0.149 and a confidence interval running from +0.065 to +0.892. It was not pre-specified as a directional hypothesis, it has no stated mechanism behind it — a more charged protein secreting *better* is not what the solubility literature would predict — and the previous draft of this chapter demonstrates exactly what happens when an uncorrected p of 0.036 is promoted to a finding. It is recorded as a hypothesis for a future, larger corpus and nothing is built on it.

## 6.4 All of the model's skill is the process term

A ridge regression over the eight predictors, cross-validated by leaving out all records of each protein together, is reported against two nested controls. The controls are the point of the exercise. A fed-batch bioreactor run beats a shake flask by one to two orders of magnitude, so a model containing a fed-batch indicator can look predictive while knowing nothing whatever about the protein, and the first draft of this chapter did not separate the two.

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

**The finding of this chapter is therefore stronger and simpler than the finding of its first draft.** It is not that the sequence features are weak predictors. It is that they carry no signal that survives a control for how the fermentation was run, on a corpus of 53 records over 25 proteins with annotation-grade features and a pre-specified design. A residual standard deviation of 0.76 in log₁₀, after the process term is accounted for, means a typical protein's reported titre remains uncertain by nearly a factor of six for reasons the protein does not explain.

## 6.5 What the variance is actually in

Three sources, none of them properties of the molecule, dominate.

**Engineering effort.** β-lactoglobulin reaches 6.1% of its ceiling and human α-lactalbumin 0.31%, a twentyfold difference between two small whey proteins of similar size and nearly identical stoichiometric cost. The record for β-lactoglobulin comes from a study that rewired host metabolism using omics guidance; the α-lactalbumin records come from smaller studies of chaperone co-expression and CRISPR editing efficiency. These are not comparable levels of investment, and the corpus contains no measure of investment to control for. The nested-control result of §6.4 is the quantitative version of this paragraph: the one variable in the corpus that does carry information is a variable about the experiment, not about the protein.

**Strain and process.** Promoter choice, secretion leader, gene copy number, protease deletion, feeding strategy, induction temperature and dissolved-oxygen control each move titres by factors that rival the entire between-protein spread. The corpus records some of these variables sporadically and none of them completely.

**Publication bias.** Low titres are reported when a paper is about something else — a new chaperone, a new promoter, a demonstration of feasibility — and high titres when the paper is about the titre. The distribution of published numbers is not the distribution of achievable numbers.

This is a confound the design cannot remove, and it is the reason the negative result in §6.4 should be read as a statement about the literature rather than only about the model. **The published record of recombinant protein titres is, to first order, a record of how much work was done, not of how hard each protein is.**

## 6.6 Consequences

**For the field.** Comparative statements of the form "protein X is more tractable than protein Y", when supported by titres drawn from different studies, are weakly supported at best. The only clean comparisons are within-study ones, and the corpus contains few.

**For a developer.** Of the three candidate bottlenecks named in the project brief, one can be excluded with numbers and the other two can be characterised but not ranked. Metabolic cost is excluded, from two independent directions. Post-translational modification splits cleanly: phosphorylation is energetically free and is therefore a missing-enzyme problem rather than a cost problem (§4.3.1), while glycosylation is the one metabolically expensive modification and is worth up to 41% of polypeptide yield under hypermannosylation (§4.3.4). Folding remains the leading candidate for the residual, but this chapter does not establish it: the disulfide association that appeared to support it did not survive correct measurement (§6.2.1). The positive evidence for folding is now the mechanism reported in the sources themselves — the κ-casein study's proteolysis and saturating copy-number response, the host literature's response to protein disulfide isomerase overexpression — rather than anything this chapter measured.

**For the method.** The right successor to this analysis is a model that represents the secretory machinery explicitly, because that is where the evidence now points and where a stoichiometric model is blind. pcSecYeast is the obvious vehicle. This is set out in Chapter 9.

**For the thesis's own claim.** The expectation declared in Chapter 2 — that whey proteins would rank as most tractable and caseins and lactoferrin least — is not recovered. α-lactalbumin, a "tractable" whey protein, sits below lactoferrin, ovalbumin and lysozyme. That is reported as a contradiction rather than reconciled, because the declaration was made in advance precisely so that it could be.

**For the reader's confidence in the rest of the thesis.** This chapter withdrew its own headline finding after re-measuring the variable it rested on, and reported the decomposition that killed it. Chapter 5 replaced a ratio of extremes with a distribution after the same kind of scrutiny, and §5.3 withdrew a claim that no intact casein had a published titre. A thesis that corrects itself in public is making a claim about its remaining numbers, and that claim is the point of reporting the corrections at this length.
