#!/usr/bin/env python3
"""Does the disorder signal survive once the titers are species-matched?

The short answer, recorded here because an earlier version of this analysis
reported the opposite, is no.

The paper's one positive sequence-level finding has to be defensible against
the obvious confound: a mixed corpus of food proteins and human therapeutics
compares processes developed under different selection pressure, at different
scale, by differently resourced groups. Any correlation fitted across the
whole corpus could be a proxy for that difference rather than for anything
about the protein.

The curated panel makes the test straightforward, because every non-benchmark
entry is a dairy, egg or haem food protein. Restricting to those 14 and
re-fitting therefore answers the question directly, and this script adds three
further checks that the result is not an artefact of panel membership:

  * dropping hen lysozyme and avidin, the two egg proteins that are in
    practice sold as research reagents rather than eaten;
  * keeping one protein per orthologous pair, since human and bovine
    lactoferrin (and the two alpha-lactalbumins) are near-duplicates in both
    the feature and the titer, and counting both inflates n;
  * leave-one-out across all 14, which is the check that matters most at this
    sample size, because a rank correlation on 14 points can be created by a
    single extreme protein.

Output
  results/tables/food_subset_signal.md
"""
from __future__ import annotations

import csv
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ceiling_gap import spec_from_curated  # noqa: E402
from features import compute_features  # noqa: E402
from gap_attribution import (NUMERIC_FEATURES, bh, boot_ci, load_panel,  # noqa: E402
                             perm_p, spearman)

RES = os.path.join(ROOT, "results", "tables")
HOST = "Komagataella phaffii"
REAGENTS = ("lysozyme_c_chicken", "avidin_chicken")
DUPLICATE_ORTHOLOGUES = ("alpha_lactalbumin_human", "lactoferrin_human")


def fit(feats, rows, feature):
    xs, ys = [], []
    for r in rows:
        v = feats[r["protein"]].get(feature)
        if v is None or isinstance(v, str):
            continue
        xs.append(float(v))
        ys.append(math.log10(float(r["ceiling_utilisation"])))
    if len(xs) < 6 or len(set(xs)) < 3:
        return None
    rho = spearman(xs, ys)
    if rho is None:
        return None
    lo, hi = boot_ci(xs, ys)
    return {"n": len(xs), "rho": rho, "lo": lo, "hi": hi,
            "p": perm_p(xs, ys)}


def main():
    panel = {r["name"]: r for r in load_panel()}
    feats = {n: compute_features(spec_from_curated(r)) for n, r in panel.items()}

    with open(os.path.join(RES, "ceiling_gap.csv"), newline="") as fh:
        rows = [r for r in csv.DictReader(fh)
                if r["ceiling_utilisation"] and r["host"] == HOST
                and r["category"] != "benchmark"]

    L = ["# Does any sequence feature track the gap in the food subset?", "",
         "Every non-benchmark entry in the curated panel is a dairy, egg or "
         "haem food protein, so the fit below is already free of the "
         "therapeutic confound: human serum albumin and bovine chymosin, the "
         "two benchmarks, are excluded, and no interferon, cytokine or "
         "antibody is in the panel at all. Five further entries drop out "
         "because the corpus holds no species-matched secreted titer for "
         "them: bovine alpha-lactalbumin, bovine osteopontin and the three "
         "caseins other than kappa. The correlation is between "
         "log10(ceiling utilisation) and one sequence feature at a time, with "
         "a bootstrap interval, a permutation p-value and "
         "Benjamini-Hochberg adjustment across every feature tested.", "",
         f"Proteins: {len(rows)} ({HOST}).", "",
         "## All features, food subset only", "",
         "| feature | n | rho | 95% CI | p (perm) | p (BH) |", "|---|---|---|---|---|---|"]

    res = []
    for f in NUMERIC_FEATURES:
        r = fit(feats, rows, f)
        if r:
            r["feature"] = f
            res.append(r)
    ps = [r["p"] for r in res]
    if ps and all(p is not None for p in ps):
        for r, q in zip(res, bh(ps)):
            r["q"] = q
    res.sort(key=lambda r: -abs(r["rho"]))
    for r in res:
        L.append(f"| `{r['feature']}` | {r['n']} | {r['rho']:+.3f} | "
                 f"{r['lo']:+.2f} to {r['hi']:+.2f} | {r['p']:.5f} | "
                 f"{r.get('q', float('nan')):.5f} |")
    survivors = [r["feature"] for r in res if r.get("q", 1) < 0.10]
    L += ["", "Features surviving FDR < 0.10: "
          + (", ".join(f"`{s}`" for s in survivors) or "**none**"), ""]

    best = survivors[0] if survivors else "metapredict_mean"

    dis = sorted(((r["protein"], float(feats[r["protein"]]["metapredict_mean"]))
                  for r in rows), key=lambda t: -t[1])
    n_disordered = sum(1 for _, v in dis if v > 0.4)
    L += ["## The two-cluster problem", "",
          "Mean predicted disorder is not spread across this panel, it is "
          "bimodal. The values are:", ""]
    L += ["- `%s` %.3f" % (nm, v) for nm, v in dis]
    L += ["", f"Only {n_disordered} of {len(rows)} proteins sit above 0.4. A "
          "rank correlation computed across a gap like that is a contrast "
          "between two clusters wearing the clothes of a trend, and "
          "leave-one-out cannot detect it, because dropping one member of a "
          "cluster leaves the others. This is the check an earlier version of "
          "this analysis failed to apply.", "",
          f"## Robustness of `{best}`", "",
          "A rank correlation on a dozen points can be manufactured by one "
          "extreme protein, so leave-one-out is a necessary check, though as "
          "the section above shows it is not a sufficient one.", "",
          "| subset | n | rho | p (perm) |", "|---|---|---|---|"]
    variants = [("all food proteins", rows),
                ("minus the two egg reagents (lysozyme, avidin)",
                 [r for r in rows if r["protein"] not in REAGENTS]),
                ("one protein per orthologous pair",
                 [r for r in rows if r["protein"] not in DUPLICATE_ORTHOLOGUES])]
    for label, sub in variants:
        r = fit(feats, sub, best)
        L.append(f"| {label} | {r['n']} | {r['rho']:+.3f} | {r['p']:.5f} |")
    for drop in rows:
        sub = [x for x in rows if x is not drop]
        r = fit(feats, sub, best)
        L.append(f"| minus {drop['protein']} | {r['n']} | {r['rho']:+.3f} | "
                 f"{r['p']:.5f} |")

    los = [fit(feats, [x for x in rows if x is not d], best) for d in rows]
    lo_rho = min(r["rho"] for r in los)
    hi_rho = max(r["rho"] for r in los)
    hi_p = max(r["p"] for r in los)
    full = fit(feats, rows, best)
    L += ["", f"Across the {len(rows)} leave-one-out fits rho ranges from "
          f"{lo_rho:+.3f} to {hi_rho:+.3f} and the permutation p-value reaches "
          f"{hi_p:.3f}.", "",
          "## What this establishes", ""]
    if full["p"] < 0.05 and n_disordered >= 4:
        L += ["Within a species-matched set of secreted food proteins in one "
              "host, predicted disorder ranks the realised fraction of the "
              f"stoichiometric ceiling: rho {full['rho']:+.3f}, permutation p "
              f"{full['p']:.4f}, with {n_disordered} proteins above the "
              "disorder threshold, so the correlation is not a two-point "
              "contrast. It says nothing about direction of causation."]
    else:
        L += [f"Nothing. The fit is rho {full['rho']:+.3f} at permutation p "
              f"{full['p']:.3f}, and only {n_disordered} of {len(rows)} "
              "proteins carry appreciable predicted disorder, so there is not "
              "enough spread in the predictor for a rank correlation to mean "
              "anything here.", "",
              "This is a correction of an earlier version of this file, which "
              "reported rho -0.833 at p 0.00025 and called it robust. That "
              "number was an artefact of three faults in the titer "
              "assignment, all now fixed in `ceiling_gap.py` and "
              "`titers_merged.tsv`:", "",
              "1. **Orthologues were pooled.** Matching on the canonical "
              "protein label alone gave bovine alpha-lactalbumin and bovine "
              "osteopontin human titers, and gave human and bovine "
              "lactoferrin the same single measurement, so one datum entered "
              "the correlation as two points. Requiring the source organism "
              "to match removes four panel entries from the fit, which is the "
              "honest outcome.",
              "2. **A quail titer was read as a chicken one.** The 5450 mg/L "
              "ovalbumin figure is *Coturnix coturnix*. Hen ovalbumin's best "
              "species-matched secreted titer in K. phaffii is 35 mg/L, which "
              "moves it from the top of the utilisation ranking to the bottom.",
              "3. **A lysate was counted as a secretion titer.** The 3500 "
              "mg/L lactoferrin record came from a construct with no signal "
              "sequence, measured after cell lysis and recovery of inclusion "
              "bodies. It is now classified intracellular and excluded.", "",
              "What survives is the ceiling comparison itself, which does not "
              "depend on any of this: the stoichiometric ceiling is nearly "
              "flat across the panel while realised titers span orders of "
              "magnitude, so metabolic cost is not the binding constraint. "
              "What limits these processes is still an open question, and the "
              "defensible statement is that this corpus cannot answer it at "
              "n of about a dozen."]

    out = os.path.join(RES, "food_subset_signal.md")
    with open(out, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
