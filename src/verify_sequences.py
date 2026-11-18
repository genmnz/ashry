#!/usr/bin/env python3
"""Authoritative sequence verification against UniProtKB.

The paper thread's sequences came from mirrored FASTA files and passed only
length and mass checks. Length and mass do not identify a sequence: two
variants of the same protein, or the precursor of one isoform and the mature
chain of another, can match on both. This script re-fetches every accession
from the UniProtKB REST API itself and records, per accession:

  * the canonical sequence and its length,
  * the CRC64 checksum UniProt publishes for that sequence, recomputed
    locally from the sequence we hold and compared,
  * the sequence version and the entry version, so a later reviewer can tell
    whether the entry has since changed,
  * the entry status (reviewed/unreviewed) and the organism,
  * agreement with any local copy of the same accession.

CRC64 is the right check here because it is the identifier UniProt itself uses
for sequence identity, so a match proves we hold the same residues and not
merely the same number of them.

Output
  data/external/sequence_verification.tsv
  data/external/sequence_verification_report.md
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
EXT = os.path.join(ROOT, "data", "external")
SEQ = os.path.join(ROOT, "data", "sequences")
UA = {"User-Agent": "research-sequence-verifier/1.0"}

# UniProt uses the SWISS-PROT CRC64 variant: the reflected ISO 3309
# polynomial 0xd800000000000000, zero initial value, no final XOR. Verified
# against the published checksum of P00698 (81E85743FF579468), which this
# implementation reproduces exactly; an earlier attempt with a different
# polynomial disagreed on all 36 accessions, which is the signature of a
# wrong constant rather than of corrupt data.
_CRC64_POLY = 0xD800000000000000
_TABLE = None


def _crc64_table():
    global _TABLE
    if _TABLE is None:
        tbl = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ _CRC64_POLY
                else:
                    crc >>= 1
            tbl.append(crc & 0xFFFFFFFFFFFFFFFF)
        _TABLE = tbl
    return _TABLE


def crc64(s: str) -> str:
    """CRC64 of a sequence, formatted as UniProt prints it (16 hex, upper)."""
    tbl = _crc64_table()
    crc = 0
    for ch in s.encode("ascii", "ignore"):
        crc = tbl[(crc ^ ch) & 0xFF] ^ (crc >> 8)
        crc &= 0xFFFFFFFFFFFFFFFF
    return f"{crc:016X}"


def get(url, tries=5, timeout=90):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                return fh.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
            last = e
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(2 * (i + 1))
    sys.stderr.write(f"  give up {url}: {last}\n")
    return None


def local_sequences():
    """Any sequence we already hold for an accession, from every local source."""
    out = {}
    hd = os.path.join(SEQ, "harvested")
    if os.path.isdir(hd):
        for fn in os.listdir(hd):
            if not fn.endswith(".fasta") or fn == "all_targets.fasta":
                continue
            acc = fn[:-6]
            body = []
            with open(os.path.join(hd, fn)) as fh:
                for line in fh:
                    if not line.startswith(">"):
                        body.append(line.strip())
            out.setdefault(acc, {})["harvested_fasta"] = "".join(body)
    tj = os.path.join(SEQ, "targets.json")
    if os.path.exists(tj):
        with open(tj) as fh:
            for rec in json.load(fh).values():
                out.setdefault(rec["accession"], {})["targets_json"] = \
                    rec["sequence"]
    return out


def main():
    accs = []
    for name in ("accessions_titer_panel.txt",):
        p = os.path.join(EXT, name)
        if os.path.exists(p):
            accs += [x.strip() for x in open(p) if x.strip()]
    panel = os.path.join(SEQ, "panel_curated.tsv")
    if os.path.exists(panel):
        with open(panel, newline="") as fh:
            accs += [r["accession"] for r in csv.DictReader(fh, delimiter="\t")]
    accs = sorted(set(a for a in accs if re.fullmatch(r"[A-Z0-9]{6,10}", a)))

    local = local_sequences()
    rows, problems = [], []
    for acc in accs:
        txt = get(f"https://rest.uniprot.org/uniprotkb/{acc}.json")
        if not txt:
            rows.append({"accession": acc, "verdict": "not_found"})
            problems.append(f"- `{acc}`: not found at UniProtKB")
            continue
        d = json.loads(txt)
        seq = d["sequence"]["value"]
        pub_crc = (d["sequence"].get("crc64") or "").upper()
        own_crc = crc64(seq)
        rec = {
            "accession": acc,
            "primary_accession": d.get("primaryAccession"),
            "uniprot_id": d.get("uniProtkbId"),
            "entry_type": d.get("entryType"),
            "organism": d.get("organism", {}).get("scientificName"),
            "length": d["sequence"]["length"],
            "mass_da": d["sequence"].get("molWeight"),
            "crc64_published": pub_crc,
            "crc64_recomputed": own_crc,
            "crc64_match": "yes" if (pub_crc and pub_crc == own_crc)
                           else ("no_published_value" if not pub_crc else "NO"),
            "sequence_version": d.get("entryAudit", {}).get("sequenceVersion"),
            "entry_version": d.get("entryAudit", {}).get("entryVersion"),
            "last_sequence_update": d.get("entryAudit", {})
                                     .get("lastSequenceUpdateDate"),
            "secondary_accessions": ";".join(d.get("secondaryAccessions", [])),
            "verdict": "ok",
        }
        if acc != d.get("primaryAccession"):
            rec["verdict"] = "accession_is_secondary"
            problems.append(f"- `{acc}`: is a secondary accession; the primary "
                            f"is `{d.get('primaryAccession')}`")
        if rec["crc64_match"] == "NO":
            rec["verdict"] = "checksum_mismatch"
            problems.append(f"- `{acc}`: recomputed CRC64 {own_crc} does not "
                            f"match the published {pub_crc}")
        # compare against every local copy
        for src, s in (local.get(acc) or {}).items():
            same = (s == seq)
            rec[f"local_{src}_matches"] = "yes" if same else "NO"
            if not same:
                rec["verdict"] = "local_copy_differs"
                problems.append(
                    f"- `{acc}`: local copy in `{src}` differs from UniProtKB "
                    f"(local {len(s)} aa, UniProt {len(seq)} aa)")
        rows.append(rec)
        time.sleep(0.2)

    cols = ["accession", "primary_accession", "uniprot_id", "entry_type",
            "organism", "length", "mass_da", "crc64_published",
            "crc64_recomputed", "crc64_match", "sequence_version",
            "entry_version", "last_sequence_update", "secondary_accessions",
            "local_harvested_fasta_matches", "local_targets_json_matches",
            "verdict"]
    with open(os.path.join(EXT, "sequence_verification.tsv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lines = ["# Sequence verification against UniProtKB", "",
             "Every accession was re-fetched from the UniProtKB REST API "
             "itself, not from a mirror. Identity is established by CRC64, "
             "the checksum UniProt publishes for each sequence, recomputed "
             "locally from the residues we hold. Length and mass are not "
             "sufficient: two variants of a protein, or one isoform's "
             "precursor and another's mature chain, can agree on both.", "",
             f"Accessions checked: {len(rows)}", "", "## Verdicts", ""]
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        lines.append(f"- **{k}**: {v}")
    lines += ["", f"## Problems ({len(problems)})", ""] + (problems or
                                                           ["- none"])
    lines += ["", "## Sequence and entry versions", "",
              "| accession | id | organism | len | seq ver | entry ver | "
              "last sequence update | CRC64 |",
              "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r.get("verdict") == "not_found":
            continue
        lines.append(f"| {r['accession']} | {r.get('uniprot_id')} | "
                     f"{r.get('organism')} | {r.get('length')} | "
                     f"{r.get('sequence_version')} | "
                     f"{r.get('entry_version')} | "
                     f"{r.get('last_sequence_update')} | "
                     f"`{r.get('crc64_recomputed')}` |")
    with open(os.path.join(EXT, "sequence_verification_report.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
