# Where the spread in realised production lives

The paper asks why proteins with nearly identical stoichiometric ceilings reach titers that differ by orders of magnitude. The question has an answer in this corpus, and it is not a protein property.

Records: 88. Proteins: 30. Studies: 52. Hosts: K. phaffii and T. reesei. Every record is a secreted, non-fragment, non-low-confidence measurement of a named protein, joined to its ceiling on the UniProt accession rather than on a protein name.

## The observation that reframes the question

Keying on the accession lets one protein appear many times, and once it can, the first thing visible is that the same protein in the same host reaches wildly different titers in different hands:

| protein | records | log10 SD within protein | fold range |
|---|---|---|---|
| OVAL_CHICK (`P01012`) | 4 | 1.192 | 200x |
| CO3A1_HUMAN (`P02461`) | 5 | 0.807 | 88x |
| LALBA_HUMAN (`P00709`) | 6 | 0.784 | 115x |
| CASK_BOVIN (`P02668`) | 5 | 0.758 | 102x |
| LACB_BOVIN (`P02754`) | 4 | 0.589 | 17x |
| ALBU_HUMAN (`P02768`) | 6 | 0.532 | 17x |
| MYG_PIG (`P02189`) | 8 | 0.518 | 38x |
| TRFL_HUMAN (`P02788`) | 7 | 0.484 | 19x |
| IFNA2_HUMAN (`P01563`) | 14 | 0.426 | 32x |
| LGB4_SOYBN (`P02236`) | 3 | 0.294 | 4x |

The average spread *inside* a single protein is 0.638 in log10, against 0.892 across the whole corpus. In other words roughly 51% of the variance in realised production is reproduced within single proteins, before any protein is compared with any other. A sequence-derived index cannot explain variation that occurs at fixed sequence.

## Variance decomposition

A random-intercept model with crossed intercepts for protein and study, and fixed effects for cultivation mode and host, splits the variance three ways.

| model | between proteins | between studies | residual | share between proteins |
|---|---|---|---|---|
| intercept only | 0.3417 | 0.1201 | 0.3543 | 41.9% |
| cultivation | 0.2205 | 0.1091 | 0.2440 | 38.4% |
| cultivation + host | 0.2544 | 0.0958 | 0.2321 | 43.7% |
| cultivation + host + sequence features | 0.1274 | 0.1143 | 0.2353 | 26.7% |

Taking the cultivation-and-host model as the reference: 44% of the variance in log10 utilisation sits between proteins, 16% between studies of the same protein, and 40% within studies. 

Fixed effects in that model, relative to batch bioreactor:

- `Intercept`: -2.119 in log10 (0.01x), p 0.0000
- `C(cultivation)[T.fed-batch]`: +0.195 in log10 (1.57x), p 0.4271
- `C(cultivation)[T.flask]`: -0.731 in log10 (0.19x), p 0.0019
- `C(cultivation)[T.not reported]`: -0.371 in log10 (0.43x), p 0.2600
- `C(host)[T.Trichoderma reesei]`: +0.453 in log10 (2.84x), p 0.0718

## Distributional statistics with intervals

Max-over-min ratios are determined by two records and move whenever either leaves the panel, so the quantities below are reported instead, each with a 4,000-sample bootstrap interval.

| quantity | estimate | 95% interval |
|---|---|---|
| median ceiling utilisation | 0.507% | 0.350% to 1.333% |
| first quartile | 0.167% | 0.110% to 0.268% |
| third quartile | 2.417% | 1.532% to 5.108% |
| log10 SD of utilisation | 0.892 | 0.751 to 1.017 |
| log10 SD of the ceiling | 0.0193 | 0.0130 to 0.0245 |

The headline ratio, the log10 spread of realised utilisation against the log10 spread of the ceiling, is 46.2. Realised production is therefore about 46 times more variable, on a log scale, than the stoichiometry that bounds it.

## Association, not mechanism

Everything above is association. The decomposition shows that most of the variance in realised production is not attached to the protein, which rules a sequence-derived index out as a predictor of titer and is a negative result about the method, not a positive one about biology. It does not identify folding, secretion, proteolysis or anything else as the mechanism, and nothing in this corpus could: process conditions, strain background, copy number and measurement method all vary together across studies and cannot be separated from one another with 88 records. The defensible claim is that metabolic stoichiometry does not bound these processes anywhere near their observed range, and that what does is a property of the process rather than of the protein.
