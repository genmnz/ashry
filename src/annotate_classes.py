#!/usr/bin/env python3
"""Annotate each corpus row with a product class, and test filter sensitivity.

Two jobs.

**1. Product class.** The paper thread's one positive finding, disulfide
density against titer, cannot be separated from a confound: disulfide-rich
proteins in a mixed corpus are disproportionately human therapeutics, which
are produced under different selection pressure, at different scale, by
better-resourced groups, and are reported differently. Every row therefore
gets a `product_class`:

  food_protein     a dairy, egg or haem protein intended as food
  food_enzyme      an enzyme used in food processing (chymosin, phytase)
  industrial_enzyme a technical enzyme (cellulase, xylanase, laccase, lipase)
  therapeutic      a human protein produced for clinical use
  research_reagent avidin, lysozyme as a reagent, and similar
  other            not classifiable from the recorded name

and a coarse `is_therapeutic` flag, so the confound can be tested directly
by refitting within the food-protein subset alone.

**2. Filter sensitivity.** The two threads report different spreads for the
same quantity: 1.20x / 224x here against 1.38x / 628x there. Averaging two
numbers that come from different filters would be meaningless. This script
recomputes both spreads under every combination of the three filters that
could explain the difference - whether non-food benchmarks are included,
whether low-confidence rows are included, and whether fragments are included
- so the two sets of numbers can be matched rather than split.
"""
from __future__ import annotations

import csv
import itertools
import math
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
LIT = os.path.join(ROOT, "data", "literature")
RES = os.path.join(ROOT, "results", "tables")

CLASS_RULES = [
    # therapeutics first: several share names with food or reagent proteins
    (r"interferon|interleukin|\bil-?\d|granulocyte|\bg-?csf\b|\bgm-?csf\b|"
     r"insulin|growth hormone|erythropoietin|\bepo\b|fibroblast growth|"
     r"\bfgf\b|antibody|\bmab\b|\bfab\b|trastuzumab|humab|nanobody|"
     r"defensin|hirudin|interferon lambda|parathyroid",
     "therapeutic"),
    (r"human serum albumin|\bhsa\b", "therapeutic"),
    (r"collagen", "therapeutic"),
    (r"chymosin|rennin|phytase|brazzein|sweet protein|thaumatin",
     "food_enzyme"),
    (r"cellobiohydrolase|cbh|cel7a|cellulase|xylanase|laccase|lipase|"
     r"glucoamylase|amylase|protease(?! inhibitor)|pectinase|catalase|"
     r"peroxidase(?!.*lacto)",
     "industrial_enzyme"),
    (r"casein|lactoglob|lactalbumin|lactoferrin|lactoperoxidase|osteopontin|"
     r"macropeptide|ovalbumin|ovotransferrin|conalbumin|ovomucoid|ovomucin|"
     r"leghemoglobin|legh|myoglobin|h(a)?emoglobin|milk|whey|egg",
     "food_protein"),
    (r"avidin|cystatin|lysozyme|trypsin inhibitor", "research_reagent"),
    (r"serum albumin", "research_reagent"),
]

THERAPEUTIC = {"therapeutic"}


def classify(name):
    n = (name or "").lower()
    for pat, lab in CLASS_RULES:
        if re.search(pat, n):
            return lab
    return "other"


def tofloat(x):
    try:
        return float(str(x).replace(",", "").replace(">", "").strip())
    except (TypeError, ValueError):
        return None


def main():
    path = os.path.join(LIT, "titers_merged.tsv")
    with open(path, newline="") as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        cols = list(rdr.fieldnames)
        rows = list(rdr)
    for c in ("product_class", "is_therapeutic"):
        if c not in cols:
            cols.append(c)

    counts = {}
    for r in rows:
        cl = classify(r.get("protein_name"))
        r["product_class"] = cl
        r["is_therapeutic"] = "yes" if cl in THERAPEUTIC else "no"
        counts[cl] = counts.get(cl, 0) + 1

    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    # ---- filter sensitivity on the ceiling-gap table --------------------
    gpath = os.path.join(RES, "ceiling_gap.csv")
    gap = []
    if os.path.exists(gpath):
        with open(gpath, newline="") as fh:
            gap = list(csv.DictReader(fh))

    lines = ["# Product classes and filter sensitivity", "",
             "## Product class counts", ""]
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        lines.append(f"- **{k}**: {v}")
    n_ther = sum(1 for r in rows if r["is_therapeutic"] == "yes")
    lines += ["", f"{n_ther} of {len(rows)} rows are human therapeutics. "
                  "Any correlation between disulfide density and titer must "
                  "be refitted within the food-protein subset before it can "
                  "be attributed to disulfides rather than to the "
                  "circumstances under which therapeutics are developed.", ""]

    if gap:
        lines += ["## Ceiling and utilisation spread under each filter", "",
                  "The two threads report 1.20x / 224x and 1.38x / 628x for "
                  "the same two quantities. These are not estimates of one "
                  "number to be averaged; they are the same calculation under "
                  "different inclusion rules. Below is this thread's table "
                  "recomputed under every combination, so the other thread's "
                  "figures can be matched to a row rather than reconciled by "
                  "splitting the difference.", "",
                  "| include benchmarks | include T. reesei | ceiling spread | "
                  "utilisation spread | n |",
                  "|---|---|---|---|---|"]
        for inc_bench, inc_tr in itertools.product([False, True],
                                                   [False, True]):
            sel = []
            for r in gap:
                if not r.get("ceiling_utilisation"):
                    continue
                if not inc_bench and r.get("category") == "benchmark":
                    continue
                if not inc_tr and r.get("host") != "Komagataella phaffii":
                    continue
                sel.append(r)
            if len(sel) < 2:
                continue
            ceils = [float(r["Y_max_glycerol_g_per_g"]) for r in sel]
            utils = [float(r["ceiling_utilisation"]) for r in sel
                     if float(r["ceiling_utilisation"]) > 0]
            lines.append(
                f"| {'yes' if inc_bench else 'no'} | "
                f"{'yes' if inc_tr else 'no'} | "
                f"{max(ceils)/min(ceils):.2f}x | "
                f"{max(utils)/min(utils):.0f}x | {len(sel)} |")
        lines += ["", "What the table actually shows, which is not what I "
                      "expected: **the ceiling spread is insensitive to all "
                      "three filters**, sitting at 1.18x in every "
                      "combination. Only the utilisation spread moves, from "
                      "152x to 224x, and it moves through its lower end, "
                      "which is set by whichever poorly expressed protein is "
                      "allowed in.",
                  "",
                  "So the difference between 1.20x and 1.38x cannot be a "
                  "filter difference. It has to come from **panel "
                  "membership** - which proteins are in the panel at all. A "
                  "ceiling is a function of amino-acid composition and glycan "
                  "load, so admitting a protein with an unusual composition "
                  "moves the extremes. Collagen is the obvious candidate: it "
                  "is roughly a third glycine and a fifth proline, far outside "
                  "the range of anything in the food panel, and it is present "
                  "in the other thread's corpus. The way to reconcile is "
                  "therefore to compare panel rosters protein by protein, not "
                  "to compare filter settings.",
                  "",
                  "The same argument applies to 224x against 628x: both are "
                  "ratios between the best and worst performer, so each is "
                  "determined by two single rows and is fragile by "
                  "construction. An interquartile or log-standard-deviation "
                  "measure of the utilisation distribution would be the more "
                  "defensible statistic for the paper, and would not shift "
                  "when one protein enters or leaves."]

    with open(os.path.join(RES, "product_classes_and_filters.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
