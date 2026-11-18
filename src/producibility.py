"""
The producibility model: does anything about a protein's sequence predict how
much of it people manage to secrete from Komagataella phaffii?

Design decisions, made before looking at the answer
---------------------------------------------------
* Response: log10 of the reported titre in mg/L. Titres span four orders of
  magnitude, so a log scale is the only sane one.
* Rows are filtered to a single comparable regime: K. phaffii or P. pastoris,
  secreted product, high-confidence evidence. Shake-flask and fed-batch runs are
  kept separate by an indicator, because the curated database documents
  within-study flask-to-bioreactor gaps of 8x to 88x; pooling them without that
  term would be a mistake.
* Features are few and mechanistic, because the sample is small:
      log length, disulfides per 100 aa, N-glycosylation sequons per 100 aa,
      fraction of disordered residues, GRAVY, absolute net charge per residue,
      and the maximum theoretical yield from the genome-scale model.
  Seven features is already generous for this n; the model is therefore ridge
  regression with leave-one-protein-out cross-validation, and the honest baseline
  (predict the mean) is reported beside it.
* A protein appearing in several studies is one unit, not several: the
  cross-validation leaves out all rows of a protein together, so the score cannot
  be inflated by memorising a protein from its own replicate rows.

If the model does not beat the baseline, that is the result and it is reported as
such. The purpose is to find out which bottleneck binds, not to produce a number.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from scipy import stats

from corpus import drop_fragments
from features import featurise
from protein_cost import ProteinSpec, read_fasta, yield_analysis, load_model

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"
HARVEST = REPO / "data" / "sequences" / "harvested"
MANIFEST = REPO / "data" / "sequences" / "harvest_manifest.json"

FEATURES = [
    "log_length", "disulfides_per_100aa", "sequons_per_100aa",
    "disorder_fraction", "gravy", "abs_net_charge", "theoretical_yield",
]


def sequence_library() -> dict[str, str]:
    """All sequences available by accession: panel targets plus harvested ones."""
    lib: dict[str, str] = {}
    meta_path = REPO / "data" / "sequences" / "targets_metadata.json"
    if meta_path.exists():
        meta = {m["accession"]: m for m in json.loads(meta_path.read_text())}
        for header, seq in read_fasta(
                REPO / "data" / "sequences" / "targets.fasta").items():
            parts = header.split("|")
            if len(parts) > 1:
                lib[parts[1]] = seq
    for path in sorted(HARVEST.glob("*.fasta")):
        acc = path.stem
        seqs = read_fasta(path)
        if seqs:
            lib.setdefault(acc, next(iter(seqs.values())))
    return lib


def count_disulfides_unknown(seq: str) -> float:
    """Without UniProt annotation, assume cysteines pair up: Cys // 2.

    This is the standard conservative assumption for secreted proteins, which are
    overwhelmingly oxidised, and it is applied uniformly so it cannot favour any
    one protein. Annotated counts are used where available.
    """
    return seq.count("C") // 2


def build_dataset(annotations: dict[str, dict]) -> pd.DataFrame:
    lib = sequence_library()
    titres = pd.read_csv(REPO / "data" / "literature" / "titers_host_panel.csv")
    titres, dropped = drop_fragments(titres)
    print(f"excluded {len(dropped)} fragment/fusion records "
          f"(their titre is not the intact protein's)")
    titres = titres[titres.confidence == "high"]
    titres = titres[titres.titer_mg_L.notna() & (titres.titer_mg_L > 0)]
    titres = titres[titres.host.astype(str).str.contains(
        "phaffii|pastoris", case=False, regex=True)]
    titres = titres[titres.secreted.astype(str).str.lower().str.startswith("yes")]
    titres["accession"] = titres.uniprot_accession.astype(str).str.strip()
    titres = titres[titres.accession.isin(lib)]

    base = load_model()
    rows = []
    cache: dict[str, dict] = {}
    for _, r in titres.iterrows():
        acc = r.accession
        if acc not in cache:
            seq = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "", lib[acc].upper())
            ann = annotations.get(acc, {})
            feat = featurise(acc, seq, ann)
            ss = ann.get("disulfide_bonds")
            ss = count_disulfides_unknown(seq) if ss is None else ss
            spec = ProteinSpec(
                name=f"p_{acc}", sequence=seq, accession=acc,
                disulfide_bonds=int(ss), n_glycosylation_sites=None,
                phosphoserines=int(ann.get("phosphoserines", 0)),
                haem_per_chain=int(ann.get("haem_per_chain", 0)))
            ymax = yield_analysis(spec, substrate="glycerol", model=base)
            cache[acc] = {
                "accession": acc,
                "length": len(seq),
                "log_length": math.log10(len(seq)),
                "disulfides_per_100aa": 100.0 * int(ss) / len(seq),
                "sequons_per_100aa": 100.0 * feat["n_sequons"] / len(seq),
                "disorder_fraction": feat["disorder_fraction"],
                "gravy": feat["gravy"],
                "abs_net_charge": abs(feat["net_charge_per_res"]),
                "theoretical_yield": ymax.get("g_protein_per_g_substrate",
                                              float("nan")),
            }
        row = dict(cache[acc])
        row.update({
            "protein_name": r.protein_name,
            "titer_mg_L": float(r.titer_mg_L),
            "log_titer": math.log10(float(r.titer_mg_L)),
            "fed_batch": int("fed-batch" in str(r.cultivation_mode).lower()
                             or "bioreactor" in str(r.cultivation_mode).lower()),
            "year": r.year,
            "doi_or_url": r.doi_or_url,
        })
        rows.append(row)
    return pd.DataFrame(rows)


def leave_one_protein_out(df: pd.DataFrame, features: list[str]) -> dict:
    X = df[features + ["fed_batch"]].to_numpy(dtype=float)
    y = df["log_titer"].to_numpy(dtype=float)
    groups = df["accession"].to_numpy()

    preds = np.full(len(y), np.nan)
    for g in np.unique(groups):
        test = groups == g
        train = ~test
        if train.sum() < 5:
            continue
        scaler = StandardScaler().fit(X[train])
        model = RidgeCV(alphas=np.logspace(-2, 3, 30)).fit(
            scaler.transform(X[train]), y[train])
        preds[test] = model.predict(scaler.transform(X[test]))

    ok = ~np.isnan(preds)
    if ok.sum() < 5:
        return {"status": "insufficient_data", "n": int(ok.sum())}

    baseline = np.full(ok.sum(), y[ok].mean())
    rmse = float(np.sqrt(np.mean((preds[ok] - y[ok]) ** 2)))
    rmse_base = float(np.sqrt(np.mean((baseline - y[ok]) ** 2)))
    rho, p = stats.spearmanr(preds[ok], y[ok])
    r, pr = stats.pearsonr(preds[ok], y[ok])

    scaler = StandardScaler().fit(X)
    full = RidgeCV(alphas=np.logspace(-2, 3, 30)).fit(scaler.transform(X), y)

    return {
        "status": "ok",
        "n_rows": int(ok.sum()),
        "n_proteins": int(len(np.unique(groups))),
        "loo_rmse_log10": rmse,
        "baseline_rmse_log10": rmse_base,
        "skill_vs_baseline": 1.0 - rmse / rmse_base,
        "spearman_rho": float(rho), "spearman_p": float(p),
        "pearson_r": float(r), "pearson_p": float(pr),
        "coefficients": {f: float(c) for f, c in zip(features + ["fed_batch"],
                                                     full.coef_)},
        "alpha": float(full.alpha_),
    }


def univariate_table(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    rows = []
    per_protein = df.groupby("accession").agg(
        log_titer=("log_titer", "max"),
        **{f: (f, "first") for f in features})
    for f in features:
        rho, p = stats.spearmanr(per_protein[f], per_protein["log_titer"])
        rows.append({"feature": f, "spearman_rho": rho, "p_value": p,
                     "n_proteins": len(per_protein)})
    return pd.DataFrame(rows).sort_values("p_value")


def main() -> None:
    ann_path = REPO / "data" / "sequences" / "targets_metadata.json"
    annotations: dict[str, dict] = {}
    if ann_path.exists():
        for m in json.loads(ann_path.read_text()):
            annotations[m["accession"]] = {
                "disulfide_bonds": m["disulfide_bonds"],
                "n_glyc_sites_annotated": m["n_glyc_sites_annotated"],
                "phosphoserines": m["phosphoserines"],
                "haem_per_chain": m["haem_per_chain"],
                "category": m["category"],
            }

    df = build_dataset(annotations)
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLES / "producibility_dataset.csv", index=False)
    print(f"dataset: {len(df)} rows, {df.accession.nunique()} distinct proteins")
    if df.empty:
        return

    uni = univariate_table(df, FEATURES)
    uni.to_csv(TABLES / "producibility_univariate.csv", index=False)
    print("\nper-protein univariate association with best log titre:")
    print(uni.to_string(index=False))

    res = leave_one_protein_out(df, FEATURES)
    (TABLES / "producibility_model.json").write_text(json.dumps(res, indent=2))
    print("\nleave-one-protein-out ridge:")
    for k, v in res.items():
        if k != "coefficients":
            print(f"  {k}: {v}")
    if "coefficients" in res:
        print("  coefficients (standardised):")
        for f, c in sorted(res["coefficients"].items(), key=lambda kv: -abs(kv[1])):
            print(f"    {f:<24}{c:+.3f}")


if __name__ == "__main__":
    main()
