#!/usr/bin/env python3
"""Merge the independent titer sweeps into one corpus and deduplicate.

Inputs
  data/literature/titers_*.tsv              this thread's three sweeps
  data/literature/titers_host_panel.csv     the modelling thread's panel
  data/literature/titers_target_proteins.csv

Output
  data/literature/titers_merged.tsv         one row per measurement
  data/literature/titers_merged_report.md   provenance and dedup decisions

Deduplication key: (normalised protein name, host genus/species, rounded
titer in mg/L, DOI when present else first author + year). Rows that collide
are merged into one, keeping the highest-confidence source and recording every
contributing record id, so nothing is silently discarded and secondary
citations of the same measurement cannot be double-counted.
"""
from __future__ import annotations

import csv
import glob
import os
import re
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
LIT = os.path.join(ROOT, "data", "literature")

CANON_COLS = [
    "record_id", "protein_name", "protein_canonical", "uniprot",
    "source_organism", "host_species", "host_canonical", "host_strain",
    "promoter", "signal_peptide", "copy_number", "localisation",
    "cultivation", "carbon_source", "titer_mg_L", "titer_basis",
    "quantification", "volumetric_productivity_mg_L_h", "year", "doi",
    "pmid", "reference", "evidence_quote", "confidence", "notes",
    "provenance", "duplicate_of",
]

CONF_RANK = {"high": 3, "medium": 2, "low": 1, "": 0}

# protein name normalisation: map the many spellings onto one label
PROTEIN_CANON = [
    # Fragments and single domains MUST be matched before the parent protein,
    # otherwise a name like "bovine casein macropeptide (kappa-casein
    # fragment)" is pooled with intact kappa-casein. That pooling is not
    # harmless: the macropeptide reaches 1,020 mg/L in K. phaffii while
    # intact kappa-casein reaches 133 mg/L, so pooling inflates the casein
    # figure 7.7-fold and destroys the comparison the analysis rests on.
    (r"macropeptide|caseinomacropeptide|\bcmp\b|\bgmp\b",
     "casein macropeptide (fragment)"),
    (r"\bn-?lobe\b|\bc-?lobe\b|domain ?3|single domain|lactoferricin",
     "protein fragment or single domain"),
    (r"beta[- ]?lactoglob|b[- ]?lg\b|blg\b", "beta-lactoglobulin"),
    (r"alpha[- ]?lactalb|a[- ]?la\b", "alpha-lactalbumin"),
    (r"alpha[- ]?s1[- ]?casein|as1[- ]?casein", "alpha-s1-casein"),
    (r"alpha[- ]?s2[- ]?casein|as2[- ]?casein", "alpha-s2-casein"),
    (r"beta[- ]?casein", "beta-casein"),
    (r"kappa[- ]?casein", "kappa-casein"),
    (r"casein ?macropeptide|caseinomacropeptide|\bcmp\b", "casein macropeptide"),
    (r"lactoferrin|\blf\b", "lactoferrin"),
    (r"lactoperoxidase|\blpo\b", "lactoperoxidase"),
    (r"osteopontin|\bopn\b", "osteopontin"),
    (r"leghemoglobin|legh\b|lbc2|lba\b", "leghemoglobin"),
    (r"ovalbumin|\bova\b", "ovalbumin"),
    (r"ovotransferrin|conalbumin", "ovotransferrin"),
    (r"ovomucoid", "ovomucoid"),
    (r"lysozyme", "lysozyme"),
    (r"avidin", "avidin"),
    (r"myoglobin", "myoglobin"),
    (r"h(a)?emoglobin", "haemoglobin"),
    (r"serum albumin|\bhsa\b|\bbsa\b", "serum albumin"),
    (r"chymosin|rennin", "chymosin"),
    (r"cellobiohydrolase|cbh ?i|cel7a", "cellobiohydrolase I"),
    (r"xylanase", "xylanase"),
    (r"glucoamylase", "glucoamylase"),
    (r"phytase", "phytase"),
    (r"interferon", "interferon"),
    (r"brazzein", "brazzein"),
    (r"transferrin", "transferrin"),
    (r"collagen", "collagen"),
]

HOST_CANON = [
    (r"komagataella|pichia pastoris|k\.? ?phaffii|p\.? ?pastoris",
     "Komagataella phaffii"),
    (r"trichoderma|t\.? ?reesei", "Trichoderma reesei"),
    (r"saccharomyces|s\.? ?cerevisiae", "Saccharomyces cerevisiae"),
    (r"kluyveromyces lactis|k\.? ?lactis", "Kluyveromyces lactis"),
    (r"kluyveromyces marxianus|k\.? ?marxianus", "Kluyveromyces marxianus"),
    (r"yarrowia|y\.? ?lipolytica", "Yarrowia lipolytica"),
    (r"hansenula|ogataea|h\.? ?polymorpha", "Ogataea polymorpha"),
    (r"ogataea minuta|o\.? ?minuta", "Ogataea minuta"),
    (r"aspergillus niger|a\.? ?niger", "Aspergillus niger"),
    (r"aspergillus oryzae|a\.? ?oryzae", "Aspergillus oryzae"),
    (r"aspergillus awamori|a\.? ?awamori|luchuensis", "Aspergillus awamori"),
    (r"myceliophthora|thermothelomyces|\bc1\b", "Thermothelomyces heterothallica"),
    (r"neurospora", "Neurospora crassa"),
    (r"escherichia|e\.? ?coli", "Escherichia coli"),
    (r"bacillus", "Bacillus subtilis"),
    (r"tremella", "Tremella fuciformis"),
]


def canon(value, table, default="other"):
    v = (value or "").lower()
    for pat, lab in table:
        if re.search(pat, v):
            return lab
    return default


def tofloat(x):
    try:
        return float(str(x).replace(",", "").replace(">", "")
                     .replace("~", "").strip())
    except (TypeError, ValueError):
        return None


def read_own():
    rows = []
    for path in sorted(glob.glob(os.path.join(LIT, "titers_*.tsv"))):
        if "merged" in path:
            continue
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                r["provenance"] = os.path.basename(path)
                rows.append(r)
    return rows


def read_other():
    """The modelling thread's two CSVs, mapped onto the common schema."""
    out = []
    mapping = {
        "protein_name": ("protein_name", "target_protein"),
        "source_organism": ("protein_source_organism",),
        "uniprot": ("uniprot_accession",),
        "host_species": ("host",),
        "signal_peptide": ("signal_peptide",),
        "promoter": ("promoter",),
        "cultivation": ("cultivation_mode",),
        "titer_mg_L": ("titer_mg_L",),
        "year": ("year",),
        "doi": ("doi_or_url",),
        "evidence_quote": ("evidence_quote",),
        "confidence": ("confidence",),
        "notes": ("notes",),
        "localisation": ("secreted",),
    }
    for name in ("titers_host_panel.csv", "titers_target_proteins.csv"):
        path = os.path.join(LIT, name)
        if not os.path.exists(path):
            continue
        with open(path, newline="") as fh:
            for i, r in enumerate(csv.DictReader(fh), 1):
                rec = {c: "" for c in CANON_COLS}
                for dst, srcs in mapping.items():
                    for s in srcs:
                        if r.get(s):
                            rec[dst] = r[s]
                            break
                rec["reference"] = (f"{r.get('first_author','')}, "
                                    f"{r.get('journal','')} {r.get('year','')}")
                rec["localisation"] = ("secreted"
                                       if str(rec["localisation"]).lower()
                                       in ("yes", "true", "secreted")
                                       else rec["localisation"])
                rec["record_id"] = f"{name.split('.')[0]}-{i}"
                rec["provenance"] = name
                out.append(rec)
    return out


def main():
    rows = read_own() + read_other()
    for r in rows:
        r["protein_canonical"] = canon(r.get("protein_name"), PROTEIN_CANON)
        r["host_canonical"] = canon(r.get("host_species"), HOST_CANON)
        r["is_fragment"] = ("yes" if ("fragment" in r["protein_canonical"]
                                      or "domain" in r["protein_canonical"])
                            else "no")

    groups = defaultdict(list)
    for r in rows:
        t = tofloat(r.get("titer_mg_L"))
        doi = (r.get("doi") or "").strip().lower().replace("https://doi.org/", "")
        key = (r["protein_canonical"], r["host_canonical"],
               round(t, 1) if t is not None else None,
               doi or (r.get("reference") or "").strip().lower()[:28])
        groups[key].append(r)

    merged, report = [], []
    for key, g in sorted(groups.items(), key=lambda kv: str(kv[0])):
        g.sort(key=lambda r: (-CONF_RANK.get((r.get("confidence") or "").lower(), 0),
                              len(r.get("evidence_quote") or "")*-1))
        keep = dict(g[0])
        if len(g) > 1:
            keep["duplicate_of"] = ";".join(x["record_id"] for x in g[1:])
            keep["provenance"] = ";".join(sorted({x["provenance"] for x in g}))
            report.append(f"- `{keep['protein_canonical']}` in "
                          f"{keep['host_canonical']} at {key[2]} mg/L: kept "
                          f"`{keep['record_id']}` ({keep.get('confidence')}), "
                          f"folded in {len(g)-1} other record(s): "
                          f"{keep['duplicate_of']}")
        merged.append(keep)

    outp = os.path.join(LIT, "titers_merged.tsv")
    with open(outp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CANON_COLS, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        for r in merged:
            w.writerow({c: r.get(c, "") for c in CANON_COLS})

    # provenance / coverage summary
    by_src = defaultdict(int)
    for r in rows:
        by_src[r["provenance"]] += 1
    by_prot = defaultdict(int)
    by_host = defaultdict(int)
    numeric = 0
    for r in merged:
        by_prot[r["protein_canonical"]] += 1
        by_host[r["host_canonical"]] += 1
        if tofloat(r.get("titer_mg_L")) is not None:
            numeric += 1

    lines = ["# Merged secretion-titer corpus", "",
             f"Input rows: {len(rows)}", f"Merged rows: {len(merged)}",
             f"Rows carrying a numeric mg/L value: {numeric}", "",
             "## Input provenance", ""]
    for k, v in sorted(by_src.items()):
        lines.append(f"- `{k}`: {v} rows")
    lines += ["", "## Rows per protein (merged)", ""]
    for k, v in sorted(by_prot.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")
    lines += ["", "## Rows per host (merged)", ""]
    for k, v in sorted(by_host.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")
    lines += ["", f"## Deduplication ({len(report)} groups collapsed)", ""]
    lines += report or ["- none"]
    with open(os.path.join(LIT, "titers_merged_report.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))
    print(f"\n... wrote {outp}")


if __name__ == "__main__":
    main()
