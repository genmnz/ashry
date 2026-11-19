# What tracks the ceiling gap?

Spearman rank correlations of log10(ceiling utilisation) against one feature at a time, with bootstrap 95% intervals, permutation p-values and Benjamini-Hochberg FDR adjustment across all features tested. No multi-feature model is fitted: the sample is far too small, and reporting one would be indefensible.

## Komagataella phaffii  (n = 14 proteins)

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|
| `metapredict_mean` | 14 | -0.833 | -0.98 to -0.45 | 0.00025 | 0.008 |
| `gravy` | 14 | +0.688 | +0.17 to +0.94 | 0.0082 | 0.12427 |
| `disorder_frac_foldindex` | 14 | -0.661 | -0.91 to -0.08 | 0.01165 | 0.12427 |
| `fold_index` | 14 | +0.534 | -0.13 to +0.88 | 0.05235 | 0.34507 |
| `n_phosphosite` | 14 | -0.508 | -0.86 to -0.24 | 0.0647 | 0.34507 |
| `phosphosite_per_100aa` | 14 | -0.508 | -0.86 to -0.24 | 0.0647 | 0.34507 |
| `metapredict_max` | 14 | -0.442 | -0.80 to +0.12 | 0.11394 | 0.52087 |
| `ss_frac_helix` | 14 | +0.367 | -0.25 to +0.88 | 0.19649 | 0.78596 |
| `ss_frac_turn` | 14 | -0.332 | -0.82 to +0.39 | 0.25184 | 0.81973 |
| `metapredict_frac_gt_0_5` | 14 | -0.312 | -0.77 to +0.30 | 0.27229 | 0.81973 |
| `frac_aromatic` | 14 | +0.279 | -0.33 to +0.75 | 0.34083 | 0.81973 |
| `aromaticity` | 14 | +0.279 | -0.33 to +0.75 | 0.34083 | 0.81973 |
| `fcr` | 14 | -0.268 | -0.84 to +0.40 | 0.34968 | 0.81973 |
| `frac_ser_thr` | 14 | -0.266 | -0.74 to +0.35 | 0.35863 | 0.81973 |

Features surviving FDR < 0.10: `metapredict_mean`

## Trichoderma reesei  (n = 4 proteins)

**n = 4. Correlations at this sample size are descriptive only; the intervals below are wide enough to include zero for almost everything, and that is the honest answer.**

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|

Features surviving FDR < 0.10: **none**

