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
