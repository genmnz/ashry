#!/usr/bin/env python3
"""Which sequence features track the gap between ceiling and realised yield?

The ceiling-gap analysis establishes that stoichiometry does not limit these
processes: ceilings span 1.2x while ceiling utilisation spans >200x. This
script asks what the 200x does track.

Deliberately conservative, because the sample is small. With one measurement
per protein per host there are ~16 independent points in K. phaffii, so a
multi-feature regression would be indefensible - a point the prior-art audit
made explicitly. Instead:

  * Spearman rank correlation of log10(ceiling utilisation) against each
    feature, one feature at a time;
  * a bootstrap confidence interval on each correlation;
  * a Benjamini-Hochberg false-discovery-rate adjustment across features,
    since many are tested;
  * no model selection, no composite score, no claim of prediction.

Hosts are analysed separately rather than pooled, because the same protein
appearing in two hosts is not an independent observation.

Output: results/tables/gap_attribution_<host>.csv and a short report.
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ceiling_gap import load_panel, spec_from_curated  # noqa: E402
from features import compute_features  # noqa: E402

RES = os.path.join(ROOT, "results", "tables")

NUMERIC_FEATURES = [
    "length", "frac_cys", "frac_pro", "frac_gly", "frac_ser_thr",
    "frac_aromatic", "gravy", "fcr", "ncpr", "abs_ncpr", "kappa",
    "fold_index", "disorder_frac_foldindex", "max_hydrophobic_patch",
    "n_disulfide", "disulfide_per_100aa", "n_sequon", "sequon_per_100aa",
    "n_o_glyc_site", "n_phosphosite", "phosphosite_per_100aa", "n_haem",
    "instability_index", "isoelectric_point", "aromaticity",
    "ss_frac_helix", "ss_frac_turn", "ss_frac_sheet",
    "aa_js_divergence_vs_host", "aa_cost_akashi", "aa_cost_ratio_vs_host",
    "metapredict_mean", "metapredict_frac_gt_0_5", "metapredict_max",
]


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(a, b):
    n = len(a)
    if n < 3:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va <= 0 or vb <= 0:
        return None
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    return cov / math.sqrt(va * vb)


def spearman(a, b):
    return pearson(rank(a), rank(b))


def boot_ci(a, b, n_boot=4000, seed=12345):
    import random
    rng = random.Random(seed)
    n = len(a)
    vals = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        r = spearman([a[i] for i in idx], [b[i] for i in idx])
        if r is not None and not math.isnan(r):
            vals.append(r)
    if len(vals) < 100:
        return (None, None)
    vals.sort()
    return (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))])


def perm_p(a, b, n_perm=20000, seed=999):
    """Two-sided permutation p-value for the Spearman correlation."""
    import random
    rng = random.Random(seed)
    obs = spearman(a, b)
    if obs is None:
        return None
    hits = 0
    bb = list(b)
    for _ in range(n_perm):
        rng.shuffle(bb)
        r = spearman(a, bb)
        if r is not None and abs(r) >= abs(obs) - 1e-12:
            hits += 1
    return (hits + 1) / (n_perm + 1)


def bh(ps):
    """Benjamini-Hochberg adjusted p-values."""
    idx = sorted(range(len(ps)), key=lambda i: ps[i])
    m = len(ps)
    adj = [1.0] * m
    prev = 1.0
    for rank_i, i in enumerate(reversed(idx), 1):
        k = m - rank_i + 1
        val = min(prev, ps[i] * m / k)
        adj[i] = val
        prev = val
    return adj


def main():
    panel = {r["name"]: r for r in load_panel()}
    feats = {}
    for name, row in panel.items():
        spec = spec_from_curated(row)
        feats[name] = compute_features(spec)

    with open(os.path.join(RES, "ceiling_gap.csv"), newline="") as fh:
        gap = [r for r in csv.DictReader(fh) if r["ceiling_utilisation"]]

    by_host = {}
    for r in gap:
        by_host.setdefault(r["host"], []).append(r)

    report = ["# What tracks the ceiling gap?", "",
              "Spearman rank correlations of log10(ceiling utilisation) "
              "against one feature at a time, with bootstrap 95% intervals, "
              "permutation p-values and Benjamini-Hochberg FDR adjustment "
              "across all features tested. No multi-feature model is fitted: "
              "the sample is far too small, and reporting one would be "
              "indefensible.", ""]

    for host, rows in sorted(by_host.items()):
        rows = [r for r in rows if r["category"] != "benchmark"] or rows
        names = [r["protein"] for r in rows]
        y = [math.log10(float(r["ceiling_utilisation"])) for r in rows]
        n = len(y)
        results = []
        for f in NUMERIC_FEATURES:
            xs, ys = [], []
            for nm, yy in zip(names, y):
                v = feats[nm].get(f)
                if v is None or isinstance(v, str):
                    continue
                xs.append(float(v))
                ys.append(yy)
            if len(set(xs)) < 3 or len(xs) < 6:
                continue
            rho = spearman(xs, ys)
            if rho is None:
                continue
            lo, hi = boot_ci(xs, ys)
            p = perm_p(xs, ys)
            results.append({"feature": f, "n": len(xs),
                            "spearman_rho": round(rho, 4),
                            "ci95_low": None if lo is None else round(lo, 4),
                            "ci95_high": None if hi is None else round(hi, 4),
                            "p_permutation": None if p is None else round(p, 5)})
        ps = [r["p_permutation"] for r in results]
        if ps and all(p is not None for p in ps):
            for r, q in zip(results, bh(ps)):
                r["p_bh_adjusted"] = round(q, 5)
        results.sort(key=lambda r: -abs(r["spearman_rho"]))

        slug = host.replace(" ", "_").replace(".", "")
        out = os.path.join(RES, f"gap_attribution_{slug}.csv")
        if results:
            with open(out, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
                w.writeheader()
                for r in results:
                    w.writerow(r)

        report += [f"## {host}  (n = {n} proteins)", ""]
        if n < 8:
            report.append(f"**n = {n}. Correlations at this sample size are "
                          "descriptive only; the intervals below are wide "
                          "enough to include zero for almost everything, and "
                          "that is the honest answer.**")
            report.append("")
        report.append("| feature | n | rho | 95% CI | p (perm) | p (BH) |")
        report.append("|---|---|---|---|---|---|")
        for r in results[:14]:
            report.append(
                f"| `{r['feature']}` | {r['n']} | {r['spearman_rho']:+.3f} | "
                f"{r['ci95_low']:+.2f} to {r['ci95_high']:+.2f} | "
                f"{r['p_permutation']} | {r.get('p_bh_adjusted','-')} |")
        report.append("")
        sig = [r for r in results if (r.get("p_bh_adjusted") or 1) < 0.1]
        report.append(f"Features surviving FDR < 0.10: "
                      f"{', '.join('`'+r['feature']+'`' for r in sig) if sig else '**none**'}")
        report.append("")

    with open(os.path.join(RES, "gap_attribution_report.md"), "w") as fh:
        fh.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
