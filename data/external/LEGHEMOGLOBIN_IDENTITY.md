# Which soybean leghemoglobin is "LegH"? — resolved

Three different accessions were in use across this project: P02234 (my cost
panel), P02236 (the modelling thread's panel) and P02237 (the egg/haem
literature sweep). They are three different molecules. Resolved against
UniProtKB on 2026-11-18.

## The entries

| accession | UniProt ID | gene | gene synonyms | recommended name | alternative names | length |
|---|---|---|---|---|---|---|
| P02234 | LGBA_PHAVU | LBA | — | Leghemoglobin alpha | — | 146 |
| P02235 | LGB2_SOYBN | LB2 | GLB2-3, **LBC1** | Leghemoglobin 2 | Hemoglobin 2-3, **Leghemoglobin C1**, Nodulin-50 | 144 |
| P02236 | LGB4_SOYBN | LB4 | GLB2-5, **LBC2** | Leghemoglobin 4 | Hemoglobin 2-5, **Leghemoglobin C2** | 145 |
| P02237 | LGB1_SOYBN | LB1 | GLB2-1, **LBC3**, LGB1 | Leghemoglobin 1 | Hemoglobin 2-1, **Leghemoglobin C3** | 145 |

## Findings

**1. P02234 is not soybean.** It is *Phaseolus vulgaris* (common bean)
leghemoglobin alpha. My own `leghemoglobin_c2_soybean` entry was wrong and the
sequence must be replaced, not relabelled. This was my error.

**2. The numbering traps.** Two independent numbering schemes are in use and
they do not line up:

- the *Lb* gene numbering (LB1, LB2, LB4) used by UniProt entry names, and
- the *Lbc* protein numbering (LBC1, LBC2, LBC3) used in most of the
  recombinant-expression literature.

`LGB2_SOYBN` (gene *LB2*) is **leghemoglobin C1**, not C2. The protein called
**leghemoglobin C2** is gene *LB4*, accession **P02236**. And P02237 carries
"LGB1" in its own gene-synonym list while being leghemoglobin C3.

**3. Which accession is right depends on which name the source used.**

- A source naming the **LBC2 / leghemoglobin C2** protein means **P02236**.
- A source naming the ***LGB2* gene** means **P02235**.

Shao *et al.*, *Bioresour Technol* 363:127884 (2022), doi
10.1016/j.biortech.2022.127884 — the 3.5 g/L secretory anchor titer — refers
to **LBC2**. Its correct accession is therefore **P02236**, which is what the
modelling thread used. That row is right.

**4. Corrections required.**

- My panel: `leghemoglobin_c2_soybean` = P02234 is wrong (wrong genus). Use
  P02236 for the Shao anchor.
- The `eggheme` titer sweep recorded P02237 for rows whose own evidence quote
  says "LBC2" and "Lbc2". P02237 is leghemoglobin C3. Those rows should be
  P02236.
- Any claim about the Impossible Foods construct must be checked against the
  name used in GRN 737 itself rather than inherited from a secondary source,
  because *LGB2* and leghemoglobin C2 are different molecules.

**5. Why this is not cosmetic.** The candidates differ in length (144 vs 145
residues) and in sequence. The choice changes the amino-acid draw, the
molecular mass used in the denominator of every g protein per g substrate
yield, the sequon count and therefore the glycan cost. The three mature
sequences differ at multiple positions within the first 50 residues alone.
