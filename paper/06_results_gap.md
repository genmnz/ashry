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

Food and food-adjacent proteins are shown in bold; the remainder are human therapeutics, flagged as such in the corpus and analysed separately in §5.2.5.

### 5.2.1 The headline contrast

An earlier draft of this chapter stated the contrast as a pair of max-over-min ratios: the ceiling spans 1.4-fold, achievement spans 628-fold. That is the right idea expressed in the wrong statistic. A ratio of extremes is decided by exactly two records — the single most optimistic and the single most pessimistic in the corpus — so it moves when one row is added, removed or reclassified, and an examiner is entitled to attack it on precisely that ground. It is replaced here by the distribution, with the extremes retained only as named examples.

Across these 26 proteins, at the central loading:

| Quantity | Median | IQR | Range | log₁₀ SD |
|---|---|---|---|---|
| Stoichiometric ceiling, *Y*<sub>max</sub> | 0.646 g g⁻¹ | 1.06-fold | 0.531–0.697 (1.31-fold) | **0.029** |
| Fraction of ceiling achieved | 0.40% | 0.073–2.12% (28.9-fold) | 0.013–7.97% | **0.851** |

The two log₁₀ standard deviations are the comparison that matters, because both quantities are then measured in the same units — orders of magnitude — on the same 26 proteins. **The outcome is about thirty times more dispersed than the bound** (0.851 against 0.029). Half the corpus sits between 0.07% and 2.1% of its own ceiling, a 29-fold interquartile spread, while the ceiling's interquartile spread is 6%.

This is the result the thesis exists to state, and unlike the ratio of extremes it is a property of the whole distribution. It is robust to every assumption tested: it holds across the whole scanned range of substrate loading, across the translation-cost scan, whether the product basis or the polypeptide basis is used, and — see §5.2.5 — within the food-protein subset alone, where the 15 food and food-adjacent proteins have median utilisation 0.50% and log₁₀ SD 0.780 against the same 1.31-fold ceiling span.

The extremes are still worth naming, as examples rather than as the statistic. The best process in the corpus reached 8.0% of its ceiling; the worst reached 0.013%; the ratio between those two particular records is 593-fold, and the reader should treat that number as an illustration of the spread, not as a measurement of it.

### 5.2.2 Nobody is close to the ceiling

The best process in the entire corpus — a human-like collagen at 19.4 g L⁻¹ — reached **8.0%** of what the stoichiometry of its host permits. The best food protein, β-lactoglobulin at 13.88 g L⁻¹, reached 6.1%. The median protein reached 0.40%, which is a factor of 250 from its bound. This is worth stating plainly because the field's language sometimes suggests that titres are approaching a biological limit. They are not approaching it; the median published process is more than two orders of magnitude away from it, and the best is more than one.

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

And the central claim does not depend on the choice at all. Nitrogen content varies by only **1.10-fold** across the panel, and the carbon ceiling by 1.31-fold. Substituting the nitrogen bound for the carbon bound therefore rescales every protein's utilisation by nearly the same factor: it moves the median but not the dispersion, and the dispersion is the argument. Whichever bound is used, the ceiling's log₁₀ SD stays near 0.03 while utilisation's stays near 0.85. The argument of §5.2.1 survives both substitutions, which is the strongest thing that can be said for it.

### 5.2.4 The ordering is not the expected one

Chapter 2 declared the expectation in advance: the published expert judgement is that whey proteins are the most tractable targets and caseins and lactoferrin the least. The measurement partly contradicts it.

β-lactoglobulin does indeed sit near the top, at 6.1% of its ceiling and the best food protein in the corpus. But **α-lactalbumin, the other "easy" whey protein, is far down the table** at 0.31% — a factor of twenty below β-lactoglobulin, and below lactoferrin, ovalbumin and lysozyme. By stoichiometry it is an ordinary protein, 0.555 g g⁻¹ against a median of 0.646. By achievement it is in the bottom half of the corpus. Meanwhile soy leghemoglobin, which requires a haem cofactor the host must be engineered to supply, sits fifth.

Two readings are available and the data here cannot separate them. Either α-lactalbumin is genuinely difficult — four disulfides in 123 residues is a high disulfide density for a food protein — or it has received far less engineering effort than β-lactoglobulin, which has a commercial product behind it. The first reading was the more attractive one while disulfide density appeared to predict titre; Chapter 6 withdraws that finding, which leaves the effort reading carrying most of the weight. It is developed in §6.5, where it becomes the chapter's main conclusion rather than a caveat.

### 5.2.5 Food proteins and therapeutics, separated

Eleven of the 26 proteins in Table 5.1 are human therapeutics: interferons, interleukins, colony-stimulating factors, insulin, transferrin, albumin. Pooling them with food proteins is a confound rather than a convenience, because a therapeutic is developed under a cost structure and a regulatory regime that justify effort no food protein can. Reclassifying one row from one group to the other would also move a max-over-min ratio, which is a further reason not to rest the headline on one.

The corpus carries an explicit flag, so the analysis is simply repeated on the 15 food and food-adjacent proteins alone:

| Subset | *n* proteins | Median utilisation | IQR | log₁₀ SD | Ceiling span |
|---|---|---|---|---|---|
| All proteins | 26 | 0.40% | 0.073–2.12% | 0.851 | 1.31-fold |
| Food and food-adjacent | 15 | 0.50% | 0.117–1.22% | 0.780 | 1.31-fold |

Nothing of substance changes. The food proteins are if anything slightly *better* utilised at the median, their dispersion is almost as wide, and the ceiling span is identical because the ceiling is set by composition rather than by product category. The decomposition is therefore not an artefact of mixing two markets.

## 5.3 The caseins: from an absence to a measurement

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
2. The stoichiometric ceiling has a log₁₀ standard deviation of **0.029** across 26 proteins; utilisation of it has a log₁₀ standard deviation of **0.851**. The outcome is about thirty times more dispersed than the bound, which excludes metabolic cost as the explanation of the ordering. Reported as a distribution rather than as a ratio of extremes, the conclusion does not depend on any single record.
3. Carbon, not oxygen, is the binding bound at the product level in all 36 protein-by-transfer-rate combinations tested. Nitrogen binds before carbon in a batch, but not in the fed-batch processes these titres came from, and substituting either bound rescales the median without touching the dispersion.
4. Separating food proteins from human therapeutics changes nothing material: 15 food and food-adjacent proteins, median utilisation 0.50%, log₁₀ SD 0.780, identical ceiling span.
5. The published expert ordering of food proteins by tractability is partly contradicted: α-lactalbumin, a "tractable" whey protein, sits at 0.31% of its ceiling, below lactoferrin, ovalbumin and lysozyme.
6. Intact κ-casein does have published titres, 28–133 mg L⁻¹ in *K. phaffii*, and it has among the *highest* ceilings and the lowest utilisation in the corpus. α-S2- and β-casein still have none in any microbial host.

The gap is therefore real, large, well characterised as a distribution, and unexplained by anything computed so far. The next chapter asks what it tracks, and reports that the answer is not the protein.
