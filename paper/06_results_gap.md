# Chapter 5 — The gap between the ceiling and the record

Chapter 4 computed what metabolism permits. This chapter measures what has been achieved, and expresses the second as a fraction of the first. That ratio is the central quantity of this thesis.

## 5.1 Why the ratio is the right quantity

Published titres cannot be compared to one another directly. A gram per litre of a 15 kDa globin and a gram per litre of an 80 kDa glycoprotein are not the same achievement; a shake-flask result and a fed-batch bioreactor result differ by one to two orders of magnitude for reasons that have nothing to do with the protein; and a process fed 150 g L⁻¹ of substrate cannot be judged against one fed 500.

Dividing each titre by the ceiling of the very protein that was produced removes the first of these problems entirely and makes the third explicit as a scanned parameter. What remains — the fraction of its own stoichiometric limit that a process reached — is dimensionless, comparable, and bounded above by one.

## 5.2 The measurement

Applying the inclusion rules of §3.9 to the rebuilt corpus gives **75 high-confidence records of secreted production** in *K. phaffii*, *P. pastoris* or *T. reesei*, covering **26 distinct proteins** for which a CRC64-verified sequence was available. Twenty-five records were excluded as fragments or fusions, for reasons §5.4 develops.

**Table 5.1 — Fraction of its own stoichiometric ceiling reached, at 350 g L⁻¹ substrate loading**

| Protein | Best titre (g L⁻¹) | *Y*<sub>max</sub> (g g⁻¹) | Ceiling (g L⁻¹) | % of ceiling | Gap |
|---|---|---|---|---|---|
| Human-like type III collagen | 19.40 | 0.696 | 243 | 7.97% | 13× |
| Human serum albumin | 17.47 | 0.649 | 227 | 7.69% | 13× |
| **β-lactoglobulin** | 13.88 | 0.651 | 228 | 6.09% | 16× |
| *Candida antarctica* lipase B | 10.00 | 0.642 | 225 | 4.45% | 22× |
| **Soy leghemoglobin** | 6.00 | 0.622 | 218 | 2.75% | 36× |
| Human interferon α-2b | 6.30 | 0.656 | 230 | 2.74% | 36× |
| Human GM-CSF | 4.30 | 0.567 | 199 | 2.17% | 46× |
| Type XVII human-like collagen | 4.70 | 0.682 | 239 | 1.97% | 51× |
| **Hen egg white lysozyme** | 3.50 | 0.683 | 239 | 1.46% | 68× |
| **Human lactoferrin** | 2.21 | 0.642 | 225 | 0.99% | 102× |
| **Ovalbumin** | 2.00 | 0.645 | 226 | 0.89% | 113× |
| **Brazzein** | 1.30 | 0.697 | 244 | 0.53% | 188× |
| **Hen ovomucoid** | 0.93 | 0.531 | 186 | 0.50% | 200× |
| **Human α-lactalbumin** | 0.60 | 0.555 | 194 | 0.31% | 324× |
| **Avidin** | 0.33 | 0.618 | 216 | 0.15% | 656× |
| Human interleukin-6 | 0.28 | 0.630 | 220 | 0.13% | 787× |
| **Porcine myoglobin** | 0.29 | 0.650 | 227 | 0.13% | 797× |
| Human insulin precursor | 0.25 | 0.655 | 229 | 0.11% | 917× |
| **Bovine lactoferrin** | 0.23 | 0.615 | 215 | 0.11% | 925× |
| Human bFGF | 0.15 | 0.696 | 244 | 0.06% | 1,624× |
| **Bovine κ-casein** | 0.13 | 0.657 | 230 | 0.06% | 1,729× |
| Human G-CSF | 0.10 | 0.646 | 226 | 0.04% | 2,262× |
| *T. reesei* hydrophobin HFBI | 0.09 | 0.677 | 237 | 0.04% | 2,736× |
| Human interleukin-15 | 0.07 | 0.617 | 216 | 0.03% | 2,878× |
| Human interferon λ-1 | 0.07 | 0.616 | 216 | 0.03% | 3,318× |
| Human serum transferrin | 0.03 | 0.638 | 223 | 0.01% | 7,441× |

Food and food-adjacent proteins are shown in bold; the remainder are human therapeutics, flagged as such in the corpus and analysed separately in §5.2.6.

### 5.2.1 The headline contrast

An earlier draft of this chapter stated the contrast as a pair of max-over-min ratios: the ceiling spans 1.4-fold, achievement spans 628-fold. That is the right idea expressed in the wrong statistic. A ratio of extremes is decided by exactly two records — the single most optimistic and the single most pessimistic in the corpus — so it moves when one row is added, removed or reclassified, and an examiner is entitled to attack it on precisely that ground. It is replaced here by the distribution, with the extremes retained only as named examples.

Across these 26 proteins, at the central loading:

| Quantity | Median | IQR | Range | log₁₀ SD |
|---|---|---|---|---|
| Stoichiometric ceiling, *Y*<sub>max</sub> | 0.646 g g⁻¹ | 1.06-fold | 0.531–0.697 (1.31-fold) | **0.029** |
| Fraction of ceiling achieved | 0.40% | 0.073–2.12% (28.9-fold) | 0.013–7.97% | **0.851** |

The two log₁₀ standard deviations are the comparison that matters, because both quantities are then measured in the same units — orders of magnitude — on the same 26 proteins. **The outcome is about thirty times more dispersed than the bound** (0.851 against 0.029). Half the corpus sits between 0.07% and 2.1% of its own ceiling, a 29-fold interquartile spread, while the ceiling's interquartile spread is 6%.

This is the result the thesis exists to state, and unlike the ratio of extremes it is a property of the whole distribution. It is robust to every assumption tested: it holds across the whole scanned range of substrate loading, across the translation-cost scan, whether the product basis or the polypeptide basis is used, and — see §5.2.6 — within the food-protein subset alone, where the 15 food and food-adjacent proteins have median utilisation 0.50% and log₁₀ SD 0.780 against the same 1.31-fold ceiling span.

The extremes are still worth naming, as examples rather than as the statistic. The best process in the corpus reached 8.0% of its ceiling; the worst reached 0.013%; the ratio between those two particular records is 593-fold, and the reader should treat that number as an illustration of the spread, not as a measurement of it.

### 5.2.2 Most of the spread is reproduced at fixed sequence

Table 5.1 reports one record per protein — the best published titre — because that is the fairest way to ask how close the field has come. It is not, however, the right table for asking *what the spread is attached to*. Joining every qualifying record to its ceiling on the UniProt accession rather than on a protein name lets a single protein appear as many times as it has been published, and once it can, something becomes visible that the best-of table hides.

The same protein, in the same host, reaches wildly different titres in different hands.

**Table 5.2 — Within-protein spread in ceiling utilisation, for proteins with three or more qualifying records**

| Protein | Accession | Records | log₁₀ SD within protein | Fold range |
|---|---|---|---|---|
| Hen ovalbumin | P01012 | 4 | 1.192 | 200× |
| Human type III collagen | P02461 | 5 | 0.807 | 88× |
| Human α-lactalbumin | P00709 | 6 | 0.784 | 115× |
| **Bovine κ-casein** | P02668 | 5 | 0.758 | 102× |
| Bovine β-lactoglobulin | P02754 | 4 | 0.589 | 17× |
| Human serum albumin | P02768 | 6 | 0.532 | 17× |
| Porcine myoglobin | P02189 | 8 | 0.518 | 38× |
| Human lactoferrin | P02788 | 7 | 0.484 | 19× |
| Human interferon α-2b | P01563 | 14 | 0.426 | 32× |
| Soy leghemoglobin | P02236 | 3 | 0.294 | 4× |

The mean spread *inside* a single protein is **0.638** in log₁₀, against **0.892** across the whole 88-record corpus. Roughly **half the variance in realised production is reproduced within single proteins**, before any protein is compared with any other. Hen ovalbumin alone spans 200-fold; κ-casein, the central test case of §5.3, spans 102-fold across five records.

This reframes the question the thesis asks. If half the dispersion occurs when the sequence does not vary at all, then no quantity derived from the sequence can account for it, and a "producibility index" built from sequence features is predicting something that is only half there.

**The variance decomposition.** A random-intercept model with crossed intercepts for protein identity and study identity, and fixed effects for cultivation mode and host, splits the variance in log₁₀ utilisation across 88 records, 30 proteins and 52 studies:

**Table 5.3 — Variance decomposition of log₁₀ ceiling utilisation**

| Model | Between proteins | Between studies | Residual | Share between proteins |
|---|---|---|---|---|
| Intercept only | 0.342 | 0.120 | 0.354 | 41.9% |
| + cultivation | 0.221 | 0.109 | 0.244 | 38.4% |
| + cultivation + host | 0.254 | 0.096 | 0.232 | 43.7% |
| + cultivation + host + sequence features | 0.127 | 0.114 | 0.235 | 26.7% |

Taking the cultivation-and-host model as the reference, **44% of the variance sits between proteins, 16% between studies of the same protein, and 40% within studies.** Adding the seven sequence features of §3.6 halves the between-protein component, from 0.254 to 0.127, while leaving the residual untouched at 0.232 against 0.235. That is the signature of regressors absorbing protein identity rather than predicting from it: the features are acting as a noisy label for which protein a row is, not as a mechanism. Chapter 6 reaches the same conclusion by cross-validation, and this is the more defensible form of it.

Two fixed effects are worth reporting, both relative to a batch bioreactor. Shake flask costs **−0.731** in log₁₀, a factor of 5.4, with *p* = 0.002: cultivation mode is a real and large effect, and it is the one effect in the model that is unambiguously significant. Fed-batch against batch is **+0.195**, *p* = 0.43 — which means that once protein identity is admitted as a random effect, the fed-batch indicator this thesis carries through Chapter 6 weakens to nothing. *T. reesei* against *K. phaffii* is +0.453, *p* = 0.072.

**Intervals, not ratios of extremes.** Every distributional statistic in this chapter is reported with a 4,000-sample bootstrap interval, computed over records rather than over best-of-protein rows:

**Table 5.4 — Distributional statistics with bootstrap intervals (88 records)**

| Quantity | Estimate | 95% interval |
|---|---|---|
| Median ceiling utilisation | 0.507% | 0.350% – 1.333% |
| First quartile | 0.167% | 0.110% – 0.268% |
| Third quartile | 2.417% | 1.532% – 5.108% |
| log₁₀ SD of utilisation | 0.892 | 0.751 – 1.017 |
| log₁₀ SD of the ceiling | 0.0193 | 0.0130 – 0.0245 |

The ratio of the last two is **46**: realised production is about forty-six times more variable, on a log scale, than the stoichiometry that bounds it. The per-protein figures of §5.2.1 (0.851 against 0.029, a ratio near thirty) and these per-record figures are the same statement computed on two defensible denominators, and the interval on the ceiling's dispersion — 0.013 to 0.025 — does not come close to the interval on utilisation's. The conclusion does not depend on which convention is adopted.

**What this does and does not establish.** It establishes an association and a negative result about method: the spread in realised production is mostly not attached to the protein, which rules a sequence-derived index out as a predictor. It does not identify folding, secretion, proteolysis or any other process as the mechanism, and nothing in an 88-record observational corpus could: process conditions, strain background, copy number and quantification method all vary together across studies and cannot be separated from one another at this sample size. The defensible claim is the one stated here — that metabolic stoichiometry does not bound these processes anywhere near their observed range, and that what does vary is a property of the process rather than of the protein.

### 5.2.3 Nobody is close to the ceiling

The best process in the entire corpus — a human-like collagen at 19.4 g L⁻¹ — reached **8.0%** of what the stoichiometry of its host permits. The best food protein, β-lactoglobulin at 13.88 g L⁻¹, reached 6.1%. The median protein reached 0.40%, which is a factor of 250 from its bound. This is worth stating plainly because the field's language sometimes suggests that titres are approaching a biological limit. They are not approaching it; the median published process is more than two orders of magnitude away from it, and the best is more than one.

At a loading of 150 g L⁻¹ the β-lactoglobulin result rises to 14.2% of ceiling and at 500 g L⁻¹ it falls to 4.3%, so the conclusion is not an artefact of the central loading assumption: no plausible loading brings any published process within a factor of seven of its ceiling.

### 5.2.4 Is carbon the right bound? Four alternative bounds, computed

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

And the central claim does not depend on the choice at all. Nitrogen content varies by only **1.10-fold** across the panel, and the carbon ceiling by 1.31-fold. Substituting the nitrogen bound for the carbon bound therefore rescales every protein's utilisation by nearly the same factor: it moves the median but not the dispersion, and the dispersion is the argument. Whichever bound is used, the ceiling's log₁₀ SD stays near 0.03 while utilisation's stays near 0.85. The argument of §5.2.1 survives both substitutions, which is the strongest thing that can be said for it.

#### Phosphate, and the one bound that is protein-specific

Phosphorus enters the product only as phosphoserine, one atom per site, and ATP turnover consumes none of it net because the phosphate is recycled. The product's own phosphorus content is therefore the right quantity for a product-level bound, and it is the only bound in this thesis that varies strongly between proteins:

| Protein | Phosphoserines | P (% of mass) | 0.5 g P L⁻¹ | 2 g P L⁻¹ | 7.3 g P L⁻¹ |
|---|---|---|---|---|---|
| α-S2-casein | 13 | 1.65% | **30** | **121** | 441 |
| α-S1-casein | 9 | 1.21% | **41** | **165** | 602 |
| β-casein | 5 | 0.66% | **76** | 305 | 1,112 |
| κ-casein | 3 | 0.49% | **102** | 408 | 1,491 |
| Leghemoglobin C2 | 1 | 0.20% | 251 | 1,002 | 3,659 |
| Ovalbumin | 2 | 0.14% | 346 | 1,384 | 5,053 |

Ceilings in g L⁻¹; bold where phosphate is tighter than the 214–234 g L⁻¹ carbon bound. Three of the nine panel proteins — β-lactoglobulin, α-lactalbumin and lactoferrin — carry no phosphorus at all, so for them the bound does not exist.

Two things follow. **Phosphate does not bind in a standard medium.** Basal salts medium for this host is built on phosphoric acid, 26.7 mL L⁻¹ of 85% H₃PO₄ or about 7.3 g of phosphorus per litre, at which even α-S2-casein's phosphate ceiling is 441 g L⁻¹, nearly twice the carbon bound. Phosphate binds in 10 of 45 protein-by-supply combinations, all of them caseins at or below 2 g P L⁻¹.

**But it is the only bound that discriminates between proteins.** Carbon spans 1.31-fold across the panel, nitrogen 1.10-fold, oxygen essentially not at all. Phosphate spans **twelve-fold**, from α-S2-casein to ovalbumin, because it scales with a count that genuinely differs. That matters for a specific practical case: a developer reducing phosphate — to cut downstream salt load, or because high phosphate interferes with a precipitation step — is reducing the one bound that a heavily phosphorylated casein will hit first and an unphosphorylated whey protein will never hit at all. It is the only place in this analysis where the identity of the protein changes the operative constraint rather than merely scaling it.

#### Heat removal, the one check that cannot be dismissed outright

Oxygen uptake is the standard proxy for fermenter heat load, because aerobic catabolism releases a nearly substrate-independent 440–490 kJ per mole of O₂. At the oxygen demands of §5.2.4 this is **4.3–4.7 kJ per gram of product**. A jacketed production vessel with internal coils removes roughly 5–20 kW m⁻³:

| Cooling capacity (kW m⁻³) | Heat-limited ceiling (g L⁻¹) | Carbon ceiling (g L⁻¹) | Binding bound |
|---|---|---|---|
| 5 | 344–373 | 214–234 | carbon |
| 10 | 688–746 | 214–234 | carbon |
| 20 | 1,377–1,492 | 214–234 | carbon |
| 40 | 2,754–2,984 | 214–234 | carbon |

Carbon is tighter in all 36 combinations, but the margin at the low-cooling end is **1.49-fold**, the narrowest of the three alternative bounds — oxygen's narrowest is 1.9-fold and nitrogen's is wide open once ammonia is fed.

And this calculation is **non-conservative**, which must be said plainly. It counts only the oxygen drawn by product synthesis, so it understates the heat a real process must remove and therefore overstates the heat ceiling. Growth and maintenance respiration in a high-cell-density fed-batch dominate total oxygen uptake, often by an order of magnitude, so the true heat-limited ceiling is well below the figures tabulated above and may be the tightest bound of all at a large scale with poor cooling. What this calculation establishes is the narrower claim that *the heat of product synthesis alone* does not bind. Unlike oxygen, heat removal cannot be dismissed as a candidate constraint on this evidence; it is simply not a constraint on the quantity Table 5.1 measures. Bounding it properly requires a whole-process energy balance with growth and maintenance included, which is beyond a product-level stoichiometric model and is named as such in §9.3.

### 5.2.5 The ordering is not the expected one

Chapter 2 declared the expectation in advance: the published expert judgement is that whey proteins are the most tractable targets and caseins and lactoferrin the least. The measurement partly contradicts it.

β-lactoglobulin does indeed sit near the top, at 6.1% of its ceiling and the best food protein in the corpus. But **α-lactalbumin, the other "easy" whey protein, is far down the table** at 0.31% — a factor of twenty below β-lactoglobulin, and below lactoferrin, ovalbumin and lysozyme. By stoichiometry it is an ordinary protein, 0.555 g g⁻¹ against a median of 0.646. By achievement it is in the bottom half of the corpus. Meanwhile soy leghemoglobin, which requires a haem cofactor the host must be engineered to supply, sits fifth.

Two readings are available and the data here cannot separate them. Either α-lactalbumin is genuinely difficult — four disulfides in 123 residues is a high disulfide density for a food protein — or it has received far less engineering effort than β-lactoglobulin, which has a commercial product behind it. The first reading was the more attractive one while disulfide density appeared to predict titre; Chapter 6 withdraws that finding, which leaves the effort reading carrying most of the weight. It is developed in §6.5, where it becomes the chapter's main conclusion rather than a caveat.

### 5.2.6 Food proteins and therapeutics, separated

Eleven of the 26 proteins in Table 5.1 are human therapeutics: interferons, interleukins, colony-stimulating factors, insulin, transferrin, albumin. Pooling them with food proteins is a confound rather than a convenience, because a therapeutic is developed under a cost structure and a regulatory regime that justify effort no food protein can. Reclassifying one row from one group to the other would also move a max-over-min ratio, which is a further reason not to rest the headline on one.

The corpus carries an explicit flag, so the analysis is simply repeated on the 15 food and food-adjacent proteins alone:

| Subset | *n* proteins | Median utilisation | IQR | log₁₀ SD | Ceiling span |
|---|---|---|---|---|---|
| All proteins | 26 | 0.40% | 0.073–2.12% | 0.851 | 1.31-fold |
| Food and food-adjacent | 15 | 0.50% | 0.117–1.22% | 0.780 | 1.31-fold |

Nothing of substance changes. The food proteins are if anything slightly *better* utilised at the median, their dispersion is almost as wide, and the ceiling span is identical because the ceiling is set by composition rather than by product category. The decomposition is therefore not an artefact of mixing two markets.

## 5.3 The caseins: the central test case

The caseins were, until the corpus was rebuilt, absent from Table 5.1 altogether, and this section reported that absence as a result. It is worth recording what happened to that claim, because the correction runs in both directions and the second half of it is new.

**The first correction.** An earlier version of this analysis credited κ-casein with 1.02 g L⁻¹, placing it mid-table. That number came from a record for **bovine casein macropeptide**, the 64-residue glycopeptide that chymosin releases from κ-casein during coagulation. A strain secreting casein macropeptide has not secreted a casein; it has secreted about a third of one, without the part that matters. The error entered through a name-based join matching "casein" in both strings, and it inflated the caseins' apparent performance by a factor of nearly eight. It was caught by cross-checking against an independent analysis of the same corpus, and the corpus filter that removes fragments, fusions, isolated domains and antibody fragments is shared between both pipelines so that neither can repeat it.

With the fragment removed, this section stated that no intact casein had a published volumetric titre in either host. **That claim is now withdrawn.** A systematic re-harvest, deeper than the first and with every record carrying a verbatim quotation from the source, found it:

- **Bovine κ-casein in *K. phaffii*** (Iaria and co-workers, 2026): 28, 89 and 133 mg L⁻¹ in shake flask from one-, seven- and seventeen-copy strains, and an order-of-magnitude estimate of 10 mg L⁻¹ for a single-copy strain in a methanol fed-batch bioreactor at pH 3. The authors report extensive O-glycosylation and proteolysis, and note that production scales sub-linearly with copy number.
- **Bovine κ-casein in *Aspergillus oryzae***: 0.11, 0.18 and 4.14 mg L⁻¹ by ELISA, the highest of them with protease-pathway engineering and 10 g L⁻¹ yeast extract.
- **Bovine α-S1-casein in *Bacillus subtilis*** (Biermann and co-workers, 2025): 56.9 mg L⁻¹ in a genome-reduced strain, in a high-cell-density fed-batch. This is outside the two hosts of this thesis but it is the only quantitative α-S1-casein titre located anywhere.
- **α-S2-casein and β-casein**: still nothing. No primary source with a volumetric titre in any microbial host was retrieved for either.

So the absence was partly a failure of the first search and partly real, and the honest statement is now a measurement rather than a gap. It is a sharper result than the absence was.

**κ-casein has the third-highest stoichiometric ceiling of any protein in Table 5.1 and the sixth-lowest utilisation of it.** Its *Y*<sub>max</sub> is 0.657 g g⁻¹ against a corpus median of 0.646 — it is, metabolically, an unusually *cheap* protein to build, because it carries no disulfides to speak of, no N-glycans, and phosphorylation that Chapter 4 showed to be energetically free. And it reaches 0.06% of that ceiling, a gap of 1,729-fold, against β-lactoglobulin's 16-fold.

This is the thesis's central decomposition applied to the commercially most important target in animal-free dairy, and it says something specific: **the casein problem is not a cost problem.** Nothing about building a casein is expensive. What the sources themselves report is proteolysis, aberrant host O-glycosylation, and a copy-number response that saturates — failures of folding, trafficking and stability, not of carbon or ATP supply. The 2026 κ-casein study makes the point directly: *pep4* and *yps1* protease knockouts did not fully stop degradation.

Three implications follow.

First, the most commercially valuable target in animal-free dairy now has a public number, and it is two orders of magnitude below the whey protein beside it in the same host. The gap is where the engineering opportunity is.

Second, any ranking of food proteins by tractability that places caseins last is, for these hosts, now supported by data rather than by an absence of it — but the reason it is last is proteolytic and post-translational, which means the published expert ordering is right about the ranking and the mechanism both.

Third, the open ground has moved. A rigorous fed-batch titre for an intact α-S1-, α-S2- or β-casein in *K. phaffii*, with phosphorylation state characterised, is still unpublished, and remains the first item in the wet-laboratory programme proposed in Chapter 9. For κ-casein the open question is no longer whether it can be made but why it degrades.

## 5.4 What the exclusions remove, and why it matters

Twenty-five records were excluded as fragments or fusions. The category matters because each exclusion is a case where a reported titre overstates what was achieved for the protein of interest:

- **Fragments** (casein macropeptide, lactoferricin, antimicrobial peptides excised from precursors) are shorter and structurally simpler than the parent, and are often produced precisely because the parent is difficult.
- **Fusions** (a SUMO-tagged holin, an sfGFP-tagged lipase at 5.1 g L⁻¹) report a titre that includes the partner's mass, and the partner is frequently chosen because it improves secretion.
- **Antibody fragments and isolated domains** (Fab, scFv, a viral receptor-binding domain) are engineered constructs, not natural proteins, and their sequence features belong to the construct rather than to anything in UniProt.

Including any of these inflates apparent performance. Excluding them costs sample size — 25 of 161 in-host high-confidence records — and the trade is worth making, but it is recorded here because a reader comparing this table against the raw corpus will find the difference.

## 5.5 What this chapter establishes

1. No published process for any protein in these hosts has reached more than **8.0%** of its stoichiometric ceiling. The median reached 0.40%, and half the corpus lies between 0.07% and 2.1%.
2. The stoichiometric ceiling has a log₁₀ standard deviation of **0.029** across 26 proteins; utilisation of it has a log₁₀ standard deviation of **0.851**. Computed per record rather than per protein, with bootstrap intervals, the same contrast is 0.0193 (0.0130–0.0245) against 0.892 (0.751–1.017), a ratio of 46. The outcome is about thirty times more dispersed than the bound, which excludes metabolic cost as the explanation of the ordering. Reported as a distribution rather than as a ratio of extremes, the conclusion does not depend on any single record.
3. Carbon, not oxygen, is the binding bound at the product level in all 36 protein-by-transfer-rate combinations tested, and the same holds against phosphate at any realistic supply and against the heat of product synthesis at any realistic cooling capacity. Nitrogen binds before carbon in a batch, but not in the fed-batch processes these titres came from. Substituting any of these bounds rescales the median without touching the dispersion. Two caveats are carried rather than buried: phosphate is the only bound that varies strongly between proteins, twelve-fold against carbon's 1.31-fold, and binds on the caseins below 2 g P L⁻¹; and the heat bound counts only product-associated respiration, so it is an upper bound on an upper bound and heat removal remains an open question at scale.
4. Separating food proteins from human therapeutics changes nothing material: 15 food and food-adjacent proteins, median utilisation 0.50%, log₁₀ SD 0.780, identical ceiling span.
5. The published expert ordering of food proteins by tractability is partly contradicted: α-lactalbumin, a "tractable" whey protein, sits at 0.31% of its ceiling, below lactoferrin, ovalbumin and lysozyme.
6. Intact κ-casein does have published titres, 28–133 mg L⁻¹ in *K. phaffii*, and it has among the *highest* ceilings and the lowest utilisation in the corpus. α-S2- and β-casein still have none in any microbial host.
7. **About half the dispersion in realised production is reproduced within single proteins.** The mean log₁₀ spread inside one protein is 0.638 against 0.892 corpus-wide; hen ovalbumin spans 200-fold across four records and κ-casein 102-fold across five. A variance decomposition attributes 44% of the variance to protein identity, 16% to study identity and 40% to within-study residual, and adding sequence features halves the between-protein component without touching the residual. Since half the spread occurs where the sequence does not vary, no sequence-derived quantity can account for it.

The gap is therefore real, large, well characterised as a distribution, and unexplained by anything computed so far. The next chapter asks what it tracks, and reports that the answer is not the protein.
