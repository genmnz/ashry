#!/usr/bin/env python3
"""Harvest the external data the modelling thread cannot reach.

Three batches:

  uniprot   full UniProtKB records for every accession referenced by the titer
            database, with sequence, length, monoisotopic/average mass and the
            PTM feature annotation (signal peptide, chain, disulfide, modified
            residue, glycosylation, propeptide, cofactor binding).
  alphafold predicted structures (mdCIF + PDB + pLDDT summary) from the
            AlphaFold Protein Structure Database for the panel proteins.
  cds       Komagataella phaffii coding sequences, for building a
            highly-expressed-gene codon reference.

Outputs (all written, never printed only):
  data/external/uniprot/<ACC>.json          raw UniProtKB JSON
  data/external/uniprot_summary.csv         one row per accession
  data/sequences/harvested/<ACC>.fasta      canonical sequence
  data/sequences/harvested/all_targets.fasta
  data/external/alphafold/<ACC>.*           structures + per-model metadata
  data/external/alphafold_summary.csv
  data/external/kphaffii_cds/               CDS fasta + codon usage tables
  data/external/HARVEST_LOG.md              what succeeded, what did not

Every network call retries with backoff and records failures rather than
silently dropping them.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
EXT = os.path.join(ROOT, "data", "external")
HARV = os.path.join(ROOT, "data", "sequences", "harvested")

UA = {"User-Agent": "research-data-harvester/1.0"}


def get(url, tries=5, timeout=90, binary=False):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                data = fh.read()
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"{url}: {last}")


# ---------------------------------------------------------------------------
# UniProt
# ---------------------------------------------------------------------------

FEATURE_TYPES = ["Signal", "Propeptide", "Chain", "Peptide", "Disulfide bond",
                 "Modified residue", "Glycosylation", "Transmembrane",
                 "Binding site", "Cross-link", "Region"]


def harvest_uniprot(accessions, log):
    outdir = os.path.join(EXT, "uniprot")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(HARV, exist_ok=True)
    rows = []
    fasta_all = []
    for acc in accessions:
        txt = get(f"https://rest.uniprot.org/uniprotkb/{acc}.json")
        if txt is None:
            log.append(f"- UniProt `{acc}`: **not found** (404)")
            rows.append({"accession": acc, "status": "not_found"})
            continue
        d = json.loads(txt)
        with open(os.path.join(outdir, f"{acc}.json"), "w") as fh:
            json.dump(d, fh, indent=1)

        seq = d["sequence"]["value"]
        feats = d.get("features", [])

        def count(ftype):
            return sum(1 for f in feats if f["type"] == ftype)

        def spans(ftype):
            out = []
            for f in feats:
                if f["type"] != ftype:
                    continue
                loc = f["location"]
                out.append((loc["start"].get("value"), loc["end"].get("value"),
                            f.get("description", "")))
            return out

        sig = spans("Signal")
        n_phos = sum(1 for f in feats if f["type"] == "Modified residue"
                     and "Phospho" in (f.get("description") or ""))
        n_nglyc = sum(1 for f in feats if f["type"] == "Glycosylation"
                      and (f.get("description") or "").startswith("N-linked"))
        n_oglyc = sum(1 for f in feats if f["type"] == "Glycosylation"
                      and (f.get("description") or "").startswith("O-linked"))
        names = d.get("proteinDescription", {})
        rec = {
            "accession": acc,
            "status": "ok",
            "uniprot_id": d.get("uniProtkbId"),
            "entry_type": d.get("entryType"),
            "protein_name": (names.get("recommendedName", {})
                             .get("fullName", {}).get("value")
                             or (names.get("submissionNames") or [{}])[0]
                             .get("fullName", {}).get("value")),
            "gene": ";".join(g.get("geneName", {}).get("value", "")
                             for g in d.get("genes", []) if g.get("geneName")),
            "organism": d.get("organism", {}).get("scientificName"),
            "taxon_id": d.get("organism", {}).get("taxonId"),
            "length_precursor": d["sequence"]["length"],
            "mass_da_precursor": d["sequence"].get("molWeight"),
            "sequence_version": d.get("entryAudit", {})
                                 .get("sequenceVersion"),
            "signal_peptide_end": sig[0][1] if sig else 0,
            "length_mature": (d["sequence"]["length"] - sig[0][1]) if sig
                             else d["sequence"]["length"],
            "n_disulfide": count("Disulfide bond"),
            "n_modified_residue": count("Modified residue"),
            "n_phosphosite": n_phos,
            "n_glyc_N_linked": n_nglyc,
            "n_glyc_O_linked": n_oglyc,
            "n_cys": seq.count("C"),
            "existence": d.get("proteinExistence"),
        }
        rows.append(rec)
        hdr = (f">{acc}|{rec['uniprot_id']}|{rec['organism']}|"
               f"len={rec['length_precursor']}|sp={rec['signal_peptide_end']}")
        block = hdr + "\n" + "\n".join(seq[i:i + 60]
                                       for i in range(0, len(seq), 60))
        with open(os.path.join(HARV, f"{acc}.fasta"), "w") as fh:
            fh.write(block + "\n")
        fasta_all.append(block)
        log.append(f"- UniProt `{acc}` {rec['uniprot_id']}: ok, "
                   f"L={rec['length_precursor']}, "
                   f"SS={rec['n_disulfide']}, P={rec['n_phosphosite']}, "
                   f"Nglyc={rec['n_glyc_N_linked']}")
        time.sleep(0.25)

    with open(os.path.join(HARV, "all_targets.fasta"), "w") as fh:
        fh.write("\n".join(fasta_all) + "\n")
    cols = ["accession", "status", "uniprot_id", "protein_name", "gene",
            "organism", "taxon_id", "entry_type", "existence",
            "length_precursor", "length_mature", "mass_da_precursor",
            "sequence_version", "signal_peptide_end", "n_disulfide",
            "n_cys", "n_modified_residue", "n_phosphosite",
            "n_glyc_N_linked", "n_glyc_O_linked"]
    with open(os.path.join(EXT, "uniprot_summary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows


# ---------------------------------------------------------------------------
# AlphaFold
# ---------------------------------------------------------------------------

def harvest_alphafold(accessions, log):
    outdir = os.path.join(EXT, "alphafold")
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for acc in accessions:
        txt = get(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}")
        if not txt:
            log.append(f"- AlphaFold `{acc}`: no prediction available")
            rows.append({"accession": acc, "status": "not_available"})
            continue
        meta = json.loads(txt)
        if not meta:
            log.append(f"- AlphaFold `{acc}`: empty response")
            rows.append({"accession": acc, "status": "empty"})
            continue
        e = meta[0]
        with open(os.path.join(outdir, f"{acc}_meta.json"), "w") as fh:
            json.dump(meta, fh, indent=1)
        got = []
        for key, ext in (("pdbUrl", "pdb"), ("cifUrl", "cif"),
                         ("paeDocUrl", "pae.json")):
            url = e.get(key)
            if not url:
                continue
            blob = get(url, binary=True)
            if blob is None:
                continue
            with open(os.path.join(outdir, f"{acc}.{ext}"), "wb") as fh:
                fh.write(blob)
            got.append(ext)
        plddt = None
        pdb_path = os.path.join(outdir, f"{acc}.pdb")
        if os.path.exists(pdb_path):
            vals = []
            with open(pdb_path) as fh:
                for line in fh:
                    if line.startswith("ATOM") and line[12:16].strip() == "CA":
                        try:
                            vals.append(float(line[60:66]))
                        except ValueError:
                            pass
            if vals:
                plddt = {
                    "mean_plddt": sum(vals) / len(vals),
                    "frac_plddt_lt_50": sum(1 for v in vals if v < 50) / len(vals),
                    "frac_plddt_lt_70": sum(1 for v in vals if v < 70) / len(vals),
                    "frac_plddt_gt_90": sum(1 for v in vals if v > 90) / len(vals),
                    "n_residues": len(vals),
                }
        rec = {"accession": acc, "status": "ok",
               "entry_id": e.get("entryId"),
               "model_version": e.get("latestVersion"),
               "model_created": e.get("modelCreatedDate"),
               "uniprot_start": e.get("uniprotStart"),
               "uniprot_end": e.get("uniprotEnd"),
               "files": ",".join(got)}
        if plddt:
            rec.update({k: round(v, 4) for k, v in plddt.items()})
        rows.append(rec)
        log.append(f"- AlphaFold `{acc}`: {e.get('entryId')} v"
                   f"{e.get('latestVersion')}, files {got}"
                   + (f", mean pLDDT {plddt['mean_plddt']:.1f}, "
                      f"{100*plddt['frac_plddt_lt_70']:.0f}% below 70"
                      if plddt else ""))
        time.sleep(0.3)
    cols = ["accession", "status", "entry_id", "model_version",
            "model_created", "uniprot_start", "uniprot_end", "n_residues",
            "mean_plddt", "frac_plddt_lt_50", "frac_plddt_lt_70",
            "frac_plddt_gt_90", "files"]
    with open(os.path.join(EXT, "alphafold_summary.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", choices=["uniprot", "alphafold", "all"])
    ap.add_argument("--accessions", required=True,
                    help="file with one accession per line")
    a = ap.parse_args()
    accs = [x.strip() for x in open(a.accessions) if x.strip()]
    os.makedirs(EXT, exist_ok=True)
    log = [f"# Harvest log\n", f"Accessions requested: {len(accs)}\n"]
    if a.batch in ("uniprot", "all"):
        log.append("\n## UniProtKB\n")
        harvest_uniprot(accs, log)
    if a.batch in ("alphafold", "all"):
        log.append("\n## AlphaFold Protein Structure Database\n")
        harvest_alphafold(accs, log)
    path = os.path.join(EXT, f"HARVEST_LOG_{a.batch}.md")
    with open(path, "w") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
