# What tracks the ceiling gap?

Spearman rank correlations of log10(ceiling utilisation) against one feature at a time, with bootstrap 95% intervals, permutation p-values and Benjamini-Hochberg FDR adjustment across all features tested. No multi-feature model is fitted: the sample is far too small, and reporting one would be indefensible.

## Komagataella phaffii  (n = 12 proteins)

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|
| `max_hydrophobic_patch` | 12 | -0.593 | -0.95 to +0.00 | 0.0468 | 0.8808 |
| `metapredict_max` | 12 | -0.517 | -0.87 to +0.11 | 0.0931 | 0.8808 |
| `abs_ncpr` | 12 | +0.482 | -0.10 to +0.87 | 0.11674 | 0.8808 |
| `metapredict_mean` | 12 | -0.482 | -0.92 to +0.27 | 0.11744 | 0.8808 |
| `kappa` | 12 | +0.420 | -0.25 to +0.93 | 0.17999 | 0.90603 |
| `length` | 12 | -0.357 | -0.76 to +0.25 | 0.25944 | 0.90603 |
| `aa_js_divergence_vs_host` | 12 | +0.357 | -0.27 to +0.82 | 0.26579 | 0.90603 |
| `frac_ser_thr` | 12 | -0.252 | -0.74 to +0.34 | 0.43653 | 0.90603 |
| `disorder_frac_foldindex` | 12 | -0.231 | -0.82 to +0.53 | 0.46798 | 0.90603 |
| `n_sequon` | 12 | -0.220 | -0.72 to +0.45 | 0.48738 | 0.90603 |
| `gravy` | 12 | +0.210 | -0.53 to +0.78 | 0.51272 | 0.90603 |
| `disulfide_per_100aa` | 12 | +0.203 | -0.40 to +0.76 | 0.52432 | 0.90603 |
| `fcr` | 12 | +0.203 | -0.48 to +0.76 | 0.52567 | 0.90603 |
| `metapredict_frac_gt_0_5` | 12 | -0.202 | -0.66 to +0.39 | 0.53902 | 0.90603 |

Features surviving FDR < 0.10: **none**

## Trichoderma reesei  (n = 3 proteins)

**n = 3. Correlations at this sample size are descriptive only; the intervals below are wide enough to include zero for almost everything, and that is the honest answer.**

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|

Features surviving FDR < 0.10: **none**

