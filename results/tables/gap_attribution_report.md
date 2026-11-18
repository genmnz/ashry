# What tracks the ceiling gap?

Spearman rank correlations of log10(ceiling utilisation) against one feature at a time, with bootstrap 95% intervals, permutation p-values and Benjamini-Hochberg FDR adjustment across all features tested. No multi-feature model is fitted: the sample is far too small, and reporting one would be indefensible.

## Komagataella phaffii  (n = 14 proteins)

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|
| `metapredict_mean` | 14 | -0.719 | -0.99 to -0.22 | 0.0051 | 0.1136 |
| `gravy` | 14 | +0.697 | +0.18 to +0.93 | 0.0076 | 0.1136 |
| `disorder_frac_foldindex` | 14 | -0.670 | -0.91 to -0.12 | 0.01065 | 0.1136 |
| `fold_index` | 14 | +0.556 | -0.08 to +0.90 | 0.043 | 0.344 |
| `n_phosphosite` | 14 | -0.508 | -0.86 to -0.24 | 0.0647 | 0.34507 |
| `phosphosite_per_100aa` | 14 | -0.508 | -0.86 to -0.24 | 0.0647 | 0.34507 |
| `metapredict_max` | 14 | -0.411 | -0.80 to +0.20 | 0.14574 | 0.66624 |
| `ss_frac_helix` | 14 | +0.363 | -0.25 to +0.89 | 0.20419 | 0.75943 |
| `ss_frac_turn` | 14 | -0.358 | -0.83 to +0.34 | 0.21359 | 0.75943 |
| `metapredict_frac_gt_0_5` | 14 | -0.312 | -0.77 to +0.30 | 0.27269 | 0.87261 |
| `sequon_per_100aa` | 14 | -0.254 | -0.77 to +0.34 | 0.38073 | 0.9589 |
| `frac_ser_thr` | 14 | -0.244 | -0.73 to +0.38 | 0.39918 | 0.9589 |
| `fcr` | 14 | -0.238 | -0.83 to +0.44 | 0.41163 | 0.9589 |
| `instability_index` | 14 | -0.213 | -0.72 to +0.40 | 0.46513 | 0.9589 |

Features surviving FDR < 0.10: **none**

## Trichoderma reesei  (n = 4 proteins)

**n = 4. Correlations at this sample size are descriptive only; the intervals below are wide enough to include zero for almost everything, and that is the honest answer.**

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|

Features surviving FDR < 0.10: **none**

