# Does any sequence feature track the gap in the food subset?

Every non-benchmark entry in the curated panel is a dairy, egg or haem food protein, so the fit below is already free of the therapeutic confound: human serum albumin and bovine chymosin, the two benchmarks, are excluded, and no interferon, cytokine or antibody is in the panel at all. Five further entries drop out because the corpus holds no species-matched secreted titer for them: bovine alpha-lactalbumin, bovine osteopontin and the three caseins other than kappa. The correlation is between log10(ceiling utilisation) and one sequence feature at a time, with a bootstrap interval, a permutation p-value and Benjamini-Hochberg adjustment across every feature tested.

Proteins: 12 (Komagataella phaffii).

## All features, food subset only

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|
| `max_hydrophobic_patch` | 12 | -0.593 | -0.95 to +0.00 | 0.04680 | 0.88083 |
| `metapredict_max` | 12 | -0.517 | -0.87 to +0.11 | 0.09310 | 0.88083 |
| `abs_ncpr` | 12 | +0.483 | -0.10 to +0.87 | 0.11674 | 0.88083 |
| `metapredict_mean` | 12 | -0.483 | -0.92 to +0.27 | 0.11744 | 0.88083 |
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
| `instability_index` | 12 | -0.196 | -0.72 to +0.41 | 0.54482 | 0.90603 |
| `frac_cys` | 12 | +0.189 | -0.41 to +0.72 | 0.55417 | 0.90603 |
| `sequon_per_100aa` | 12 | -0.174 | -0.70 to +0.52 | 0.59172 | 0.90603 |
| `frac_aromatic` | 12 | +0.168 | -0.49 to +0.79 | 0.60452 | 0.90603 |
| `aromaticity` | 12 | +0.168 | -0.49 to +0.79 | 0.60452 | 0.90603 |
| `aa_cost_akashi` | 12 | -0.154 | -0.60 to +0.46 | 0.63422 | 0.90603 |
| `aa_cost_ratio_vs_host` | 12 | -0.154 | -0.60 to +0.46 | 0.63422 | 0.90603 |
| `frac_pro` | 12 | -0.140 | -0.68 to +0.51 | 0.67137 | 0.91550 |
| `isoelectric_point` | 12 | -0.098 | -0.58 to +0.55 | 0.76271 | 0.92286 |
| `ncpr` | 12 | -0.091 | -0.61 to +0.57 | 0.77901 | 0.92286 |
| `ss_frac_helix` | 12 | +0.088 | -0.61 to +0.69 | 0.78696 | 0.92286 |
| `frac_gly` | 12 | +0.084 | -0.61 to +0.67 | 0.79981 | 0.92286 |
| `ss_frac_sheet` | 12 | -0.049 | -0.64 to +0.54 | 0.88386 | 0.96884 |
| `ss_frac_turn` | 12 | -0.042 | -0.69 to +0.71 | 0.90425 | 0.96884 |
| `n_disulfide` | 12 | -0.014 | -0.60 to +0.63 | 0.97040 | 0.99130 |
| `fold_index` | 12 | -0.007 | -0.76 to +0.64 | 0.99130 | 0.99130 |

Features surviving FDR < 0.10: **none**

## The two-cluster problem

Mean predicted disorder is not spread across this panel, it is bimodal. The values are:

- `kappa_casein_bovine` 0.859
- `avidin_chicken` 0.153
- `myoglobin_pig` 0.151
- `lactoferrin_human` 0.116
- `ovomucoid_chicken` 0.104
- `ovotransferrin_chicken` 0.104
- `alpha_lactalbumin_human` 0.104
- `ovalbumin_chicken` 0.101
- `lactoferrin_bovine` 0.093
- `lysozyme_c_chicken` 0.088
- `leghemoglobin_lbc2_soybean` 0.074
- `beta_lactoglobulin_bovine` 0.064

Only 1 of 12 proteins sit above 0.4. A rank correlation computed across a gap like that is a contrast between two clusters wearing the clothes of a trend, and leave-one-out cannot detect it, because dropping one member of a cluster leaves the others. This is the check an earlier version of this analysis failed to apply.

## Robustness of `metapredict_mean`

A rank correlation on a dozen points can be manufactured by one extreme protein, so leave-one-out is a necessary check, though as the section above shows it is not a sufficient one.

| subset | n | rho | p (perm) |
|---|---|---|---|
| all food proteins | 12 | -0.483 | 0.11744 |
| minus the two egg reagents (lysozyme, avidin) | 10 | -0.345 | 0.33358 |
| one protein per orthologous pair | 10 | -0.539 | 0.11439 |
| minus beta_lactoglobulin_bovine | 11 | -0.327 | 0.32408 |
| minus alpha_lactalbumin_human | 11 | -0.491 | 0.13029 |
| minus kappa_casein_bovine | 11 | -0.436 | 0.18259 |
| minus lactoferrin_bovine | 11 | -0.545 | 0.08995 |
| minus lactoferrin_human | 11 | -0.536 | 0.09465 |
| minus ovalbumin_chicken | 11 | -0.627 | 0.04430 |
| minus ovotransferrin_chicken | 11 | -0.582 | 0.06595 |
| minus ovomucoid_chicken | 11 | -0.536 | 0.09390 |
| minus lysozyme_c_chicken | 11 | -0.327 | 0.32798 |
| minus avidin_chicken | 11 | -0.509 | 0.11409 |
| minus leghemoglobin_lbc2_soybean | 11 | -0.327 | 0.33168 |
| minus myoglobin_pig | 11 | -0.509 | 0.11834 |

Across the 12 leave-one-out fits rho ranges from -0.627 to -0.327 and the permutation p-value reaches 0.332.

## What this establishes

Nothing. The fit is rho -0.483 at permutation p 0.117, and only 1 of 12 proteins carry appreciable predicted disorder, so there is not enough spread in the predictor for a rank correlation to mean anything here.

This is a correction of an earlier version of this file, which reported rho -0.833 at p 0.00025 and called it robust. That number was an artefact of three faults in the titer assignment, all now fixed in `ceiling_gap.py` and `titers_merged.tsv`:

1. **Orthologues were pooled.** Matching on the canonical protein label alone gave bovine alpha-lactalbumin and bovine osteopontin human titers, and gave human and bovine lactoferrin the same single measurement, so one datum entered the correlation as two points. Requiring the source organism to match removes four panel entries from the fit, which is the honest outcome.
2. **A quail titer was read as a chicken one.** The 5450 mg/L ovalbumin figure is *Coturnix coturnix*. Hen ovalbumin's best species-matched secreted titer in K. phaffii is 35 mg/L, which moves it from the top of the utilisation ranking to the bottom.
3. **A lysate was counted as a secretion titer.** The 3500 mg/L lactoferrin record came from a construct with no signal sequence, measured after cell lysis and recovery of inclusion bodies. It is now classified intracellular and excluded.

What survives is the ceiling comparison itself, which does not depend on any of this: the stoichiometric ceiling is nearly flat across the panel while realised titers span orders of magnitude, so metabolic cost is not the binding constraint. What limits these processes is still an open question, and the defensible statement is that this corpus cannot answer it at n of about a dozen.
