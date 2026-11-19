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

from corpus import drop_fragments, food_subset, load_titres
import uniprot_annotations
from thesis_features import featurise
from thesis_model import ProteinSpec, read_fasta, yield_analysis, load_model

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"
HARVEST = REPO / "data" / "sequences" / "harvested"
MANIFEST = REPO / "data" / "sequences" / "harvest_manifest.json"

FEATURES = [
    "log_length", "disulfides_per_100aa", "sequons_per_100aa",
    "disorder_fraction", "gravy", "abs_net_charge", "theoretical_yield",
]

# One feature added after the pre-specified seven were fitted, and labelled as
# such wherever it is reported. An independent analysis of the same literature,
# run on a separately curated panel of dairy, egg and haem proteins, found the
# *mean* metapredict disorder score strongly associated with ceiling
# utilisation. The pre-specified disorder feature here was the thresholded
# fraction of residues scoring above 0.5, which is a different statistic: it is
# identically zero for every globular protein in the panel and therefore throws
# away the whole gradient among them. Adding the mean is a replication test of
# an externally generated hypothesis whose sign and magnitude were fixed before
# this fit, not a new search, and it is reported separately from the
# pre-specified set so that the two cannot be confused.
REPLICATION_FEATURE = "disorder_mean"


def sequence_library() -> dict[str, str]:
    """All sequences available by accession, verified entries taking priority.

    The 36 accessions in the corpus were re-fetched from the UniProtKB REST API
    and checked against their CRC64 checksums, which establishes identity rather
    than merely consistency of length and mass. Those sequences are used wherever
    they exist; the GitHub-consensus harvest remains as the fallback for any
    accession the REST pass did not cover.
    """
    lib: dict[str, str] = {}
    for acc, a in uniprot_annotations.load_all().items():
        if a["sequence"]:
            lib[acc] = a["sequence"]
    meta_path = REPO / "data" / "sequences" / "targets_metadata.json"
    if meta_path.exists():
        meta = {m["accession"]: m for m in json.loads(meta_path.read_text())}
        for header, seq in read_fasta(
                REPO / "data" / "sequences" / "targets.fasta").items():
            parts = header.split("|")
            if len(parts) > 1:
                lib.setdefault(parts[1], seq)
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
    titres = load_titres()
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
            ann = dict(annotations.get(acc, {}))
            feat = featurise(acc, seq, ann)
            ss = ann.get("disulfide_bonds")
            ss_source = "uniprot_annotation"
            if ss is None:
                ss = count_disulfides_unknown(seq)
                ss_source = "assumed_cys_over_2"
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
                "disulfides_total_per_100aa": 100.0 * int(
                    ann.get("disulfide_bonds_total", ss)) / len(seq),
                "disulfide_source": ss_source,
                "sequons_per_100aa": 100.0 * feat["n_sequons"] / len(seq),
                "disorder_fraction": feat["disorder_fraction"],
                "disorder_mean": feat["disorder_mean"],
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
            "reference": r.reference,
            "provenance": r.provenance,
            "product_class": r.product_class,
            "is_therapeutic": r.is_therapeutic,
        })
        rows.append(row)
    return pd.DataFrame(rows)


def leave_one_protein_out(df: pd.DataFrame, features: list[str],
                          include_fed_batch: bool = True) -> dict:
    """Leave-one-protein-out ridge, with the process term optional.

    The process term matters more than it looks. A fed-batch bioreactor run of
    the same construct beats a shake flask by one to two orders of magnitude, so
    a model containing a fed-batch indicator can appear to predict titre while
    knowing nothing about the protein. Any claim that sequence carries signal
    therefore has to be made against two nested controls: a model with the
    process term and nothing else, and a model with the sequence features and no
    process term. Both are fitted in main() and reported beside the full model.
    """
    cols = list(features) + (["fed_batch"] if include_fed_batch else [])
    X = df[cols].to_numpy(dtype=float)
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
        "features": cols,
        "coefficients": {f: float(c) for f, c in zip(cols, full.coef_)},
        "alpha": float(full.alpha_),
    }


def univariate_table(df: pd.DataFrame, features: list[str],
                     n_boot: int = 10000, n_perm: int = 20000,
                     seed: int = 11) -> pd.DataFrame:
    """Per-protein association, with a bootstrap interval, a permutation p-value
    and Benjamini-Hochberg control across the seven pre-specified features.

    At n = 23 the asymptotic Spearman p-value is not trustworthy on its own, and
    testing seven features without correction would be the classic way to
    manufacture a finding. Both are therefore reported, and the corrected q-value
    is what any claim in the text rests on.
    """
    rng = np.random.default_rng(seed)
    per_protein = df.groupby("accession").agg(
        log_titer=("log_titer", "max"),
        **{f: (f, "first") for f in features})
    y = per_protein["log_titer"].to_numpy(dtype=float)
    n = len(y)

    rows = []
    for f in features:
        x = per_protein[f].to_numpy(dtype=float)
        rho, p = stats.spearmanr(x, y)

        boots = np.empty(n_boot)
        for i in range(n_boot):
            idx = rng.integers(0, n, n)
            if len(np.unique(idx)) < 4:
                boots[i] = np.nan
                continue
            boots[i] = stats.spearmanr(x[idx], y[idx]).statistic
        boots = boots[~np.isnan(boots)]

        perm = np.empty(n_perm)
        for i in range(n_perm):
            perm[i] = stats.spearmanr(x, rng.permutation(y)).statistic
        p_perm = float((np.abs(perm) >= abs(rho)).mean())

        rows.append({
            "feature": f, "spearman_rho": float(rho), "p_value": float(p),
            "p_permutation": p_perm,
            "ci95_low": float(np.percentile(boots, 2.5)),
            "ci95_high": float(np.percentile(boots, 97.5)),
            "n_proteins": n,
        })

    out = pd.DataFrame(rows).sort_values("p_value").reset_index(drop=True)
    # Benjamini-Hochberg across the pre-specified feature set
    m = len(out)
    out["q_value_bh"] = (out.p_value * m / (out.index + 1)).cummin().clip(upper=1.0)
    out["bonferroni_threshold"] = 0.05 / m
    return out


def main() -> None:
    # Annotations come from the verified UniProtKB feature tables for every
    # accession the REST pass covered, which is all 36 in the corpus. The
    # cysteines // 2 assumption survives only as a fallback, and the table
    # records which of the two produced each number so the distinction is
    # auditable. The assumption was wrong for 15 of the 36 accessions.
    annotations: dict[str, dict] = {}
    for acc, a in uniprot_annotations.load_all().items():
        annotations[acc] = {
            "disulfide_bonds": a["disulfide_bonds"],
            "disulfide_bonds_total": a["disulfide_bonds_total"],
            "n_glyc_sites_annotated": a["n_glyc_sites_annotated"],
            "phosphoserines": a["phosphoserines"],
            "haem_per_chain": a["haem_per_chain"],
            "category": "",
        }
    ann_path = REPO / "data" / "sequences" / "targets_metadata.json"
    if ann_path.exists():
        for m in json.loads(ann_path.read_text()):
            annotations.setdefault(m["accession"], {}).setdefault(
                "category", m["category"])

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

    models = {
        "sequence_plus_process": leave_one_protein_out(df, FEATURES),
        "process_only": leave_one_protein_out(df, [], True),
        "sequence_only": leave_one_protein_out(df, FEATURES, False),
    }
    (TABLES / "producibility_model.json").write_text(json.dumps(models, indent=2))
    for name, res in models.items():
        print(f"\nleave-one-protein-out ridge [{name}]:")
        for k, v in res.items():
            if k not in ("coefficients", "features"):
                print(f"  {k}: {v}")
        for f, c in sorted(res.get("coefficients", {}).items(),
                           key=lambda kv: -abs(kv[1])):
            print(f"    {f:<24}{c:+.3f}")

    # The food subset. A human therapeutic carries development spend a food
    # protein cannot justify, so pooling the two confounds difficulty with
    # effort. The corpus flags each row; the positive result from the earlier,
    # smaller corpus is refitted here before anything is attributed to it.
    # Replication of the externally generated mean-disorder hypothesis.
    rep = univariate_table(df, [REPLICATION_FEATURE])
    print("\nreplication test, mean metapredict disorder (hypothesis from an "
          "independent panel):")
    print(rep.to_string(index=False))
    rep.to_csv(TABLES / "producibility_disorder_replication.csv", index=False)

    food = food_subset(df)
    print(f"\nfood and food-adjacent subset: {len(food)} rows, "
          f"{food.accession.nunique()} proteins "
          f"(excluded {len(df) - len(food)} human-therapeutic rows)")
    if food.accession.nunique() >= 8:
        uni_food = univariate_table(food, FEATURES + [REPLICATION_FEATURE])
        uni_food.to_csv(TABLES / "producibility_univariate_food.csv", index=False)
        print(uni_food.to_string(index=False))
        food_models = {
            "sequence_plus_process": leave_one_protein_out(food, FEATURES),
            "process_only": leave_one_protein_out(food, [], True),
        }
        (TABLES / "producibility_model_food.json").write_text(
            json.dumps(food_models, indent=2))
        for name, res in food_models.items():
            print(f"\nfood subset ridge [{name}]: "
                  f"skill {res.get('skill_vs_baseline')}, "
                  f"rho {res.get('spearman_rho')}, p {res.get('spearman_p')}")


if __name__ == "__main__":
    main()
