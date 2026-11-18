#!/usr/bin/env python3
"""Fetch target protein sequences + annotation from UniProt REST.

Writes:
  data/sequences/targets.json   full records (sequence, features, PTMs)
  data/sequences/targets.fasta  mature-chain-annotated fasta
"""
import json
import os
import sys
import time
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "sequences")
os.makedirs(OUT, exist_ok=True)

# name -> uniprot accession.  Chosen for food-protein relevance + benchmark calibration.
TARGETS = {
    # bovine caseins
    "alpha_s1_casein_bovine": "P02662",
    "alpha_s2_casein_bovine": "P02663",
    "beta_casein_bovine": "P02666",
    "kappa_casein_bovine": "P02668",
    "beta_casein_human": "P05814",
    "kappa_casein_human": "P07498",
    # bovine whey
    "beta_lactoglobulin_bovine": "P02754",
    "alpha_lactalbumin_bovine": "P00711",
    "alpha_lactalbumin_human": "P00709",
    "lactoferrin_bovine": "P24627",
    "lactoferrin_human": "P02788",
    "lactoperoxidase_bovine": "P80025",
    "osteopontin_bovine": "P31096",
    "serum_albumin_bovine": "P02769",
    "serum_albumin_human": "P02768",
    # egg white
    "ovalbumin_chicken": "P01012",
    "ovotransferrin_chicken": "P02789",
    "ovomucoid_chicken": "P01005",
    "avidin_chicken": "P02701",
    "lysozyme_c_chicken": "P00698",
    "cystatin_chicken": "P01038",
    # heme proteins
    "leghemoglobin_c2_soybean": "P02234",
    "leghemoglobin_a_soybean": "P02232",
    "myoglobin_bovine": "P02192",
    "myoglobin_pig": "P02189",
    "hemoglobin_alpha_human": "P69905",
    "hemoglobin_beta_human": "P68871",
    # benchmark / calibration proteins with well-documented Pichia or Trichoderma titers
    "chymosin_bovine": "P00794",
    "human_growth_hormone": "P01241",
    "insulin_human": "P01308",
    "trypsin_porcine": "P00761",
    "phytase_aspergillus_niger": "P34752",
    "cbhi_cel7a_trichoderma": "P62694",
    "xylanase_ii_trichoderma": "P36217",
    "glucoamylase_aspergillus_niger": "P69328",
    "hsa_domain_free_control": "P02768",
}

FIELDS = ",".join([
    "accession", "id", "protein_name", "organism_name", "sequence", "length",
    "mass", "ft_signal", "ft_chain", "ft_disulfid", "ft_mod_res",
    "ft_carbohyd", "ft_propep", "cc_ptm", "ft_transmem", "ft_region",
])


def fetch(acc, tries=4):
    url = (f"https://rest.uniprot.org/uniprotkb/{acc}.json")
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                return json.load(fh)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"  retry {i+1} {acc}: {e}\n")
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"failed {acc}")


def main():
    recs = {}
    for name, acc in TARGETS.items():
        print(f"fetch {name} ({acc})", flush=True)
        d = fetch(acc)
        seq = d["sequence"]["value"]
        feats = d.get("features", [])

        def of(ftype):
            out = []
            for f in feats:
                if f["type"] != ftype:
                    continue
                loc = f["location"]
                out.append({
                    "start": loc["start"].get("value"),
                    "end": loc["end"].get("value"),
                    "desc": f.get("description", ""),
                })
            return out

        recs[name] = {
            "name": name,
            "accession": acc,
            "uniprot_id": d.get("uniProtkbId"),
            "protein_name": (d.get("proteinDescription", {})
                             .get("recommendedName", {})
                             .get("fullName", {}).get("value")),
            "organism": d.get("organism", {}).get("scientificName"),
            "sequence": seq,
            "length": d["sequence"]["length"],
            "mass_da": d["sequence"].get("molWeight"),
            "signal": of("Signal"),
            "propeptide": of("Propeptide"),
            "chain": of("Chain"),
            "disulfide": of("Disulfide bond"),
            "mod_res": of("Modified residue"),
            "carbohyd": of("Glycosylation"),
            "transmem": of("Transmembrane"),
        }
        time.sleep(0.3)

    with open(os.path.join(OUT, "targets.json"), "w") as fh:
        json.dump(recs, fh, indent=1)
    with open(os.path.join(OUT, "targets.fasta"), "w") as fh:
        for n, r in recs.items():
            fh.write(f">{n}|{r['accession']}|{r['organism']}\n")
            s = r["sequence"]
            for i in range(0, len(s), 60):
                fh.write(s[i:i + 60] + "\n")
    print(f"\nwrote {len(recs)} records")
    for n, r in recs.items():
        print(f"  {n:38s} {r['accession']}  L={r['length']:5d}  "
              f"SP={len(r['signal'])} SS={len(r['disulfide'])} "
              f"MOD={len(r['mod_res'])} GLY={len(r['carbohyd'])}")


if __name__ == "__main__":
    main()
