"""
Assemble the verified target sequence set.

Sequences are taken from mirrored UniProt-derived FASTA files in data/sequences/
and are accepted ONLY if the molecular mass recomputed from the sequence matches
the molecular mass stated in the corresponding UniProt entry. This guards against
a mirrored file carrying a truncated, variant or mis-labelled record.

Writes:
  data/sequences/targets.fasta
  data/sequences/targets_metadata.json
  results/tables/target_composition.csv
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from thesis_model import ProteinSpec, composition_table, read_fasta
from targets import TARGETS

REPO = Path(__file__).resolve().parents[1]
SEQ_DIR = REPO / "data" / "sequences"
TABLES = REPO / "results" / "tables"

TOLERANCE_PER_10KDA = 1.0  # Da


def load_sources() -> dict[str, dict[str, str]]:
    return {p.name: read_fasta(p) for p in SEQ_DIR.glob("*.fasta")
            if p.name != "targets.fasta"}


def find_record(records: dict[str, str], accession: str) -> tuple[str, str] | None:
    for header, seq in records.items():
        if f"|{accession}|" in header or header.split()[0] == accession:
            return header, seq
    return None


def main() -> int:
    sources = load_sources()
    specs: list[ProteinSpec] = []
    meta: list[dict] = []
    failures: list[str] = []

    for t in TARGETS:
        records = sources.get(t.source_file)
        if records is None:
            failures.append(f"{t.key}: source file {t.source_file} missing")
            continue
        hit = find_record(records, t.accession)
        if hit is None:
            failures.append(f"{t.key}: accession {t.accession} not in {t.source_file}")
            continue
        header, seq = hit

        spec = ProteinSpec(
            name=t.key, sequence=seq, accession=t.accession,
            signal_peptide_end=t.signal_peptide_end,
            disulfide_bonds=t.disulfide_bonds,
            n_glycosylation_sites=t.n_glyc_sites,
            phosphoserines=t.phosphoserines,
            haem_per_chain=t.haem_per_chain,
            notes=t.notes,
        )

        mw_precursor = spec.mw(mature=False)
        tol = max(1.0, TOLERANCE_PER_10KDA * t.uniprot_mw / 10000.0)
        if len(seq) != t.uniprot_len:
            failures.append(
                f"{t.key}: length {len(seq)} != UniProt {t.uniprot_len}")
            continue
        if abs(mw_precursor - t.uniprot_mw) > tol:
            failures.append(
                f"{t.key}: recomputed MW {mw_precursor:.1f} != UniProt "
                f"{t.uniprot_mw} (tol {tol:.1f})")
            continue

        specs.append(spec)
        meta.append({
            "key": t.key, "accession": t.accession, "display_name": t.display_name,
            "category": t.category, "source_file": t.source_file,
            "source_header": header,
            "length_precursor": len(seq), "length_mature": spec.length(),
            "mw_precursor_Da": round(mw_precursor, 2),
            "mw_mature_Da": round(spec.mw(), 2),
            "uniprot_len": t.uniprot_len, "uniprot_mw": t.uniprot_mw,
            "signal_peptide_end": t.signal_peptide_end,
            "disulfide_bonds": t.disulfide_bonds,
            "n_glyc_sites_annotated": t.n_glyc_sites,
            "n_glyc_sequons_in_mature": spec.sequons(),
            "phosphoserines": t.phosphoserines,
            "haem_per_chain": t.haem_per_chain,
            "notes": t.notes,
        })

    SEQ_DIR.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    with (SEQ_DIR / "targets.fasta").open("w") as fh:
        for spec in specs:
            fh.write(f">{spec.name}|{spec.accession}|mature\n")
            for i in range(0, len(spec.mature), 60):
                fh.write(spec.mature[i:i + 60] + "\n")

    (SEQ_DIR / "targets_metadata.json").write_text(json.dumps(meta, indent=2))

    rows = composition_table(specs)
    if rows:
        with (TABLES / "target_composition.csv").open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    print(f"verified {len(specs)} / {len(TARGETS)} targets")
    for m in meta:
        print(f"  {m['key']:<22} {m['accession']}  precursor {m['length_precursor']:>4} aa"
              f"  mature {m['length_mature']:>4} aa  {m['mw_mature_Da']/1000:>6.2f} kDa")
    if failures:
        print("\nFAILED verification:")
        for f in failures:
            print("  " + f)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
