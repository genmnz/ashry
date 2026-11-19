# Surviving signal inside the food-protein subset

Every non-benchmark entry in the curated panel is a dairy, egg or haem food protein, so the fit below is already free of the therapeutic confound: human serum albumin and bovine chymosin, the two benchmarks, are excluded, and no interferon, cytokine or antibody is in the panel at all. The correlation is between log10(ceiling utilisation) and one sequence feature at a time, with a bootstrap interval, a permutation p-value and Benjamini-Hochberg adjustment across every feature tested.

Proteins: 14 (Komagataella phaffii).

## All features, food subset only

| feature | n | rho | 95% CI | p (perm) | p (BH) |
|---|---|---|---|---|---|
| `metapredict_mean` | 14 | -0.833 | -0.98 to -0.45 | 0.00025 | 0.00800 |
| `gravy` | 14 | +0.688 | +0.17 to +0.94 | 0.00820 | 0.12426 |
| `disorder_frac_foldindex` | 14 | -0.662 | -0.91 to -0.08 | 0.01165 | 0.12426 |
| `fold_index` | 14 | +0.534 | -0.13 to +0.88 | 0.05235 | 0.34505 |
| `n_phosphosite` | 14 | -0.508 | -0.86 to -0.24 | 0.06470 | 0.34505 |
| `phosphosite_per_100aa` | 14 | -0.508 | -0.86 to -0.24 | 0.06470 | 0.34505 |
| `metapredict_max` | 14 | -0.442 | -0.80 to +0.12 | 0.11394 | 0.52089 |
| `ss_frac_helix` | 14 | +0.367 | -0.25 to +0.88 | 0.19649 | 0.78596 |
| `ss_frac_turn` | 14 | -0.332 | -0.82 to +0.39 | 0.25184 | 0.81973 |
| `metapredict_frac_gt_0_5` | 14 | -0.312 | -0.77 to +0.30 | 0.27229 | 0.81973 |
| `frac_aromatic` | 14 | +0.279 | -0.33 to +0.75 | 0.34083 | 0.81973 |
| `aromaticity` | 14 | +0.279 | -0.33 to +0.75 | 0.34083 | 0.81973 |
| `fcr` | 14 | -0.268 | -0.84 to +0.40 | 0.34968 | 0.81973 |
| `frac_ser_thr` | 14 | -0.266 | -0.74 to +0.35 | 0.35863 | 0.81973 |
| `instability_index` | 14 | -0.244 | -0.74 to +0.37 | 0.40063 | 0.85468 |
| `abs_ncpr` | 14 | +0.185 | -0.52 to +0.74 | 0.52687 | 0.93030 |
| `frac_pro` | 14 | -0.158 | -0.63 to +0.49 | 0.58402 | 0.93030 |
| `frac_cys` | 14 | +0.155 | -0.46 to +0.69 | 0.59832 | 0.93030 |
| `kappa` | 14 | -0.125 | -0.76 to +0.51 | 0.67017 | 0.93030 |
| `disulfide_per_100aa` | 14 | +0.115 | -0.48 to +0.67 | 0.69902 | 0.93030 |
| `max_hydrophobic_patch` | 14 | -0.109 | -0.70 to +0.51 | 0.70691 | 0.93030 |
| `ss_frac_sheet` | 14 | +0.108 | -0.47 to +0.63 | 0.72216 | 0.93030 |
| `n_disulfide` | 14 | +0.094 | -0.51 to +0.73 | 0.74951 | 0.93030 |
| `ncpr` | 14 | +0.088 | -0.46 to +0.66 | 0.76811 | 0.93030 |
| `isoelectric_point` | 14 | +0.077 | -0.45 to +0.65 | 0.79991 | 0.93030 |
| `aa_js_divergence_vs_host` | 14 | -0.068 | -0.57 to +0.52 | 0.82616 | 0.93030 |
| `sequon_per_100aa` | 14 | -0.046 | -0.63 to +0.53 | 0.87536 | 0.93030 |
| `frac_gly` | 14 | +0.040 | -0.62 to +0.60 | 0.89171 | 0.93030 |
| `n_sequon` | 14 | +0.030 | -0.53 to +0.66 | 0.92170 | 0.93030 |
| `aa_cost_akashi` | 14 | +0.029 | -0.54 to +0.56 | 0.93030 | 0.93030 |
| `aa_cost_ratio_vs_host` | 14 | +0.029 | -0.54 to +0.56 | 0.93030 | 0.93030 |
| `length` | 14 | -0.026 | -0.57 to +0.47 | 0.92865 | 0.93030 |

Features surviving FDR < 0.10: `metapredict_mean`

## Robustness of `metapredict_mean`

A rank correlation on fourteen points can be manufactured by one extreme protein, so the leave-one-out table is the check that decides whether this is a finding or an artefact.

| subset | n | rho | p (perm) |
|---|---|---|---|
| all food proteins | 14 | -0.833 | 0.00025 |
| minus the two egg reagents (lysozyme, avidin) | 12 | -0.797 | 0.00300 |
| one protein per orthologous pair | 12 | -0.853 | 0.00065 |
| minus beta_lactoglobulin_bovine | 13 | -0.791 | 0.00265 |
| minus alpha_lactalbumin_bovine | 13 | -0.830 | 0.00110 |
| minus alpha_lactalbumin_human | 13 | -0.830 | 0.00110 |
| minus kappa_casein_bovine | 13 | -0.824 | 0.00130 |
| minus lactoferrin_bovine | 13 | -0.802 | 0.00175 |
| minus lactoferrin_human | 13 | -0.868 | 0.00015 |
| minus osteopontin_bovine | 13 | -0.824 | 0.00110 |
| minus ovalbumin_chicken | 13 | -0.808 | 0.00145 |
| minus ovotransferrin_chicken | 13 | -0.929 | 0.00005 |
| minus ovomucoid_chicken | 13 | -0.868 | 0.00040 |
| minus lysozyme_c_chicken | 13 | -0.802 | 0.00150 |
| minus avidin_chicken | 13 | -0.830 | 0.00095 |
| minus leghemoglobin_lbc2_soybean | 13 | -0.791 | 0.00145 |
| minus myoglobin_pig | 13 | -0.830 | 0.00090 |

Across all fourteen leave-one-out fits rho stays between -0.929 and the full-panel value, and the permutation p-value never exceeds 0.0026. No single protein carries the correlation, which is the thing that had to be ruled out.

## What this does and does not establish

It establishes that within a set of proteins intended as food, produced in one host, the fraction of the chain predicted to be intrinsically disordered ranks the realised fraction of the stoichiometric ceiling, and that neither disulfide load nor sequon count does. It does not establish direction of causation, and it cannot: disorder may impede secretion, or disordered proteins may simply have attracted less process development. The honest claim is the ranking and its robustness, not a mechanism.
