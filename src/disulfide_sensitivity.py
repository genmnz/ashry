"""
Why did the disulfide result disappear?

The earlier analysis, on a 35-record corpus with disulfide counts assumed as
cysteines // 2, found the only positive association in the thesis: disulfide
density against achieved titre, rho = -0.438, p = 0.036, which already failed
Benjamini-Hochberg correction at q = 0.255. On the rebuilt 306-record corpus
with counts read from the UniProtKB feature tables the association is rho =
-0.188, p = 0.37.

Two things changed at once, so this script changes them one at a time. It is the
difference between "the finding did not replicate in a larger sample" and "the
finding was an artefact of a measurement assumption", and those are different
statements about the thesis.
"""
from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"


def assoc(df: pd.DataFrame, col: str) -> tuple[float, float, int]:
    per = df.groupby("accession").agg(y=("log_titer", "max"), x=(col, "first"))
    rho, p = stats.spearmanr(per.x, per.y)
    return float(rho), float(p), len(per)


def main() -> None:
    d = pd.read_csv(TABLES / "producibility_dataset.csv")
    ann = pd.read_csv(TABLES / "uniprot_annotations.csv").set_index("accession")
    d["assumed_ss_per_100aa"] = [
        100.0 * (ann.cysteines.get(a, 0) // 2) / l
        for a, l in zip(d.accession, d.length)]

    # The original corpus is recoverable exactly: every merged record carries the
    # harvest file or files it came from, so the records that were available to
    # the first analysis are those whose provenance names titers_host_panel.csv.
    small = d[d.provenance.astype(str).str.contains("titers_host_panel")]

    rows = []
    for label, frame in (("original record set (titers_host_panel.csv)", small),
                         ("merged corpus (306 records)", d)):
        for measure, col in (("assumed (cysteines // 2)",
                              "assumed_ss_per_100aa"),
                             ("annotated (UniProt feature table)",
                              "disulfides_per_100aa")):
            rho, p, n = assoc(frame, col)
            rows.append({"corpus": label, "disulfide_measure": measure,
                         "n_records": len(frame),
                         "n_proteins": n, "spearman_rho": rho, "p_value": p})
    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "disulfide_sensitivity.csv", index=False)
    print(out.to_string(index=False))

    mis = ann[ann.disulfide_bonds != ann.cysteines // 2]
    print(f"\ncysteines//2 disagrees with the annotation for {len(mis)} of "
          f"{len(ann)} accessions; mean absolute error "
          f"{(ann.cysteines // 2 - ann.disulfide_bonds).abs().mean():.2f} bonds, "
          f"largest {(ann.cysteines // 2 - ann.disulfide_bonds).abs().max()} bonds")


if __name__ == "__main__":
    main()
