# Which soybean leghemoglobin is "LegH"?

Resolved against UniProtKB on 2026-11-18, because the two threads on this
project were using two different accessions and the nomenclature is a trap.

| accession | UniProt ID | gene | recommended name | alternative names | length |
|---|---|---|---|---|---|
| P02232 | LGB1_VICFA | LBI | Leghemoglobin-1 | Leghemoglobin I | 144 |
| P02233 | LGB1_PEA | - | Leghemoglobin-1 | Leghemoglobin I | 148 |
| P02234 | LGBA_PHAVU | LBA | Leghemoglobin alpha | - | 146 |
| P02235 | LGB2_SOYBN | **LB2** | Leghemoglobin 2 | Hemoglobin 2-3, **Leghemoglobin C1**, Nodulin-50 | 144 |
| P02236 | LGB4_SOYBN | **LB4** | Leghemoglobin 4 | Hemoglobin 2-5, **Leghemoglobin C2** | 145 |

## Findings

1. **P02234 is not soybean at all.** It is *Phaseolus vulgaris* (common bean)
   leghemoglobin alpha. Anything in this project labelled
   `leghemoglobin_c2_soybean` with accession P02234 is wrong; that was my
   error and the sequence must be replaced, not relabelled.

2. **The trap.** The gene called *LGB2* corresponds to UniProt
   `LGB2_SOYBN` / P02235, whose alternative name is Leghemoglobin **C1**.
   The protein whose alternative name is Leghemoglobin **C2** is a different
   gene, *LB4*, accession P02236. So "LGB2" and "leghemoglobin C2" are not
   the same molecule, and a label of `leghemoglobin_c2` is consistent with
   P02236 while a label of `LGB2` is consistent with P02235.

3. **Consequence for the project.** The Impossible Foods GRAS notice (GRN 737)
   and the recombinant-LegH literature refer to the *LGB2* gene product. If
   that is taken at face value the correct accession is **P02235**, not
   P02236 and certainly not P02234. This must be confirmed against the
   sequence actually reported in the primary papers before the panel is
   frozen, because every per-protein cost, yield and feature value for
   leghemoglobin depends on it.

The two candidate soybean sequences differ in length (144 vs 145 residues),
so the choice changes the amino-acid draw, the mass used in the g/g yield
denominator and the sequon count. It is not a cosmetic relabelling.
