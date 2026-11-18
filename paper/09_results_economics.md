# Chapter 8 — What it costs, and what it could cost

Published cost estimates for precision-fermented protein span three orders of magnitude, from under $20 per kilogram to figures in the thousands. That range is not a disagreement about biology; it is a disagreement about assumptions that are usually not shown. This chapter builds a model in which they are all shown, and anchors it to the stoichiometry of Chapter 4 so that one end of the range becomes a hard bound rather than an opinion.

## 8.1 The two reference points

The model reports every result against two anchors.

The **stoichiometric floor** is the cost of the raw carbon alone if the organism achieved the maximum theoretical yield, with no cells, no losses, no equipment, no labour and no recovery step. At a glycerol price of $600 per tonne and a maximum theoretical yield of 0.64 g g⁻¹, that floor is

> $0.94 per kilogram of protein.

Nothing can be cheaper. Any claim of a lower production cost for a glycerol-fed process is either using a cheaper feedstock or is wrong.

The **engineering gap** is the ratio of modelled plant cost to that floor, and it is where the entire argument about the economics of this industry actually lives.

## 8.2 Baseline case

The baseline is a 200 m³ fed-batch plant at 75% working volume and 90% uptime, 90-hour cycles, a titre of 10 g L⁻¹, a realised yield of 10 g of protein per 100 g of substrate (about 16% of theoretical), 70% downstream recovery through a chromatography-free route, and $6 per kilogram of downstream processing cost. Every one of those numbers carries a source string in the code, and all of them are declared as assumptions rather than measurements.

**Table 8.1 — Baseline cost breakdown (USD per kg of product)**

| Item | $/kg | Share |
|---|---|---|
| Labour | 18.48 | 43% |
| Substrate | 8.57 | 20% |
| Downstream processing | 6.00 | 14% |
| Other media | 4.29 | 10% |
| Utilities (aeration, agitation, cooling) | 2.67 | 6% |
| Capital (15-year straight line) | 1.97 | 5% |
| Maintenance | 1.18 | 3% |
| **Total** | **43.17** | |
| *Stoichiometric floor* | *0.94* | |
| **Engineering gap** | **46×** | |

Annual output is 81 tonnes.

A Monte Carlo over all parameters (20,000 draws, log-normal, 25% relative standard deviation) gives a median of $45/kg with a 5th-to-95th-percentile range of **$25 to $93 per kilogram**. The distribution is right-skewed, which is the normal behaviour of a cost that is inversely proportional to several uncertain quantities at once.

That range brackets the published food-grade estimates for α-lactalbumin of roughly $24/kg, which is a mild validation of the parameterisation: an independently built model lands in the same place as an industry analysis without having been tuned to it.

## 8.3 What actually drives the cost

One-at-a-time sensitivity (±50% on each parameter) ranks the drivers:

| Parameter | Cost swing ($/kg) |
|---|---|
| Downstream recovery fraction | 49.56 |
| **Titre** | 38.13 |
| Working volume fraction | 28.85 |
| Plant uptime | 28.85 |
| Reactor volume | 24.64 |
| Batch time | 21.77 |
| … | |
| Substrate price | ~8 |

Three observations follow, and the first is the one that matters.

**Carbon efficiency is nearly irrelevant.** Substrate is 20% of the baseline cost and the stoichiometric floor is 2% of it. Doubling the organism's yield on substrate — an enormous biological achievement — removes about $4 from a $43 cost. Chapter 4 showed the ceiling varies by only 9% between proteins; Chapter 8 shows that even if it varied by a factor of two it would barely move the economics. **The metabolic efficiency of the cell is not where the money is.**

**Titre and recovery are where the money is.** Both act as pure divisors on the fixed costs of a batch: a batch costs roughly the same to run whether it produces 1 or 20 g L⁻¹, so the cost per kilogram falls almost in proportion to titre. The grid in Table 8.2 shows this directly.

**Table 8.2 — Cost against titre, at 30% of theoretical yield**

| Titre (g L⁻¹) | Cost ($/kg) | Substrate share | Output (t/a) |
|---|---|---|---|
| 1 | 296 | 1.5% | 8 |
| 2 | 153 | 2.9% | 16 |
| 5 | 68 | 6.6% | 41 |
| 10 | 39 | 11.4% | 81 |
| 20 | 25 | 18.0% | 162 |
| 40 | 18 | 25.4% | 325 |

The $20/kg commodity threshold is crossed between 20 and 40 g L⁻¹ at this plant scale. For reference, the best published food-protein titre in the corpus is 13.88 g L⁻¹ for β-lactoglobulin, and Chapter 5 showed that this is 6.1% of its stoichiometric ceiling. **The titre required for commodity economics is well within what stoichiometry permits — it is about 15% of the ceiling, not 100%.** The barrier is not thermodynamic.

**Labour dominates because the plant is small.** At 81 t/a, a $1.5M annual crew is $18/kg. At 325 t/a it is $4.6/kg. This is a scale effect, not a biology effect, and it is the clearest argument in the model for consolidation into large plants rather than distributed small ones.

## 8.4 The glycan trap in cost models

Chapter 4 showed that hypermannosylation raises the mass yield while destroying the polypeptide yield. The economic consequence is direct and, as far as the literature retrieved for this thesis shows, unremarked.

A cost model that measures product as secreted mass will record a hyperglycosylating strain as *more* carbon-efficient. A customer who buys protein will find the same material worth less per kilogram, because up to half of it is mannan. For α-lactalbumin at Man₁₀₀ the mass yield rises 14% while the protein yield falls 41%: a model built on the wrong basis would show a cost *improvement* for a strain that is in fact 41% worse.

This is a specific, checkable methodological warning for anyone building a techno-economic model of a glycoprotein in a yeast host: state the basis, and use the polypeptide basis if the product is sold on protein content.

## 8.5 Sustainability, reported as a range

Life-cycle assessments of precision-fermented dairy protein report large reductions relative to bovine milk protein — greenhouse-gas emissions commonly cited as 85–97% lower, blue water 96–99% lower, non-renewable energy 29–60% lower in the most-cited industry-commissioned assessment. Independent syntheses of many assessments give similar central tendencies with wide spreads.

Three caveats are carried rather than suppressed.

First, the result is **electricity-mix dependent**. Fermentation is an electricity-intensive process, and peer-reviewed analyses exist in which fermentation protein has *higher* emissions than efficient dairy under a carbon-intensive grid.

Second, **land-use savings are more robust than carbon savings**. Removing a ruminant from the system removes a land requirement unconditionally; it removes a carbon footprint only if the energy replacing it is clean.

Third, most of the favourable assessments are **commissioned by producers**. They are not thereby wrong, but they are not independent, and a thesis should say so.

The honest summary is that the environmental case for precision fermentation is strong on land and water, conditional on grid decarbonisation for carbon, and that the ranges should be reported as ranges.

## 8.6 What this chapter establishes

1. The raw-carbon floor for glycerol-fed food protein is about $1/kg; the modelled plant cost is $43/kg at 10 g L⁻¹; the engineering gap is 46-fold.
2. Titre and downstream recovery dominate the cost; substrate price and carbon efficiency barely matter. This is the economic restatement of Chapter 6's finding that metabolism is not the binding constraint.
3. Commodity economics require 20–40 g L⁻¹ at this plant scale — roughly 15% of the stoichiometric ceiling, which no published process has yet reached but which is far below any thermodynamic limit.
4. Cost models of glycoproteins in yeast must state whether product means polypeptide or secreted mass, because hypermannosylation moves the two in opposite directions.
