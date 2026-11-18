# Komagataella phaffii codon-usage reference

Source: CDS set of the RefSeq reference assembly `GCF_000027005.1` (K. phaffii GS115, ASM2700v1), downloaded from the NCBI Datasets API. The downloaded archive's md5 is recorded in `gs115.zip.md5`.

CDS parsed: **5040**. Codons counted (stops excluded): **2,399,341**.

## Two references, for two different questions

`codon_usage_genome.tsv` is the usage over every annotated CDS: what this organism's genes look like on average.

`codon_usage_highly_expressed.tsv` is the usage over a reference set of constitutively highly expressed genes. **This is the one to use for a Codon Adaptation Index**, because CAI measures similarity to the codon choice of abundant proteins, not to the genomic average (Sharp & Li, Nucleic Acids Res 15:1281, 1987). Using the genomic average as the CAI reference is a common error and makes the index nearly uninformative.

Both tables give, per codon, the count, the fraction within its synonymous family, the frequency per 1,000 codons, the RSCU, and the relative adaptiveness w used by CAI.

## The highly expressed reference set (165 genes)

No expression data for this organism is used, so the set is built from functional annotation using the standard proxy classes, matched on the `protein=` field of each CDS header. Every member is listed in `highly_expressed_genes.tsv` so the selection can be audited.

Free-text name matching needs an exclusion list, and getting it wrong is not harmless. A first pass matching `ubiquitin` admitted 55 genes, every one of them a ligase, conjugating enzyme or protease rather than ubiquitin itself, and matching `actin` admitted actin-associated and Rho-GAP proteins. All are regulatory and low-abundance. With them included the reference set scored a mean CAI of 0.749 against a genomic mean of 0.699, a separation of 0.050; after excluding them and the other modifying and assembly factors, the separation is 0.135, nearly three times larger. Contaminating the reference set with average-usage genes pulls w towards the genomic average and flattens the index, which is exactly the failure mode that makes a CAI uninformative. The ubiquitin and actin classes were dropped altogether rather than patched, because a free-text product name cannot reliably separate an abundant protein from its regulators.

- cytosolic ribosomal protein: 129
- translation factor: 23
- major chaperone: 6
- glycolysis: 6
- methanol utilisation: 1

## Sanity check

Mean CAI of the reference genes against their own w: **0.726**.
Mean CAI of all 5040 CDS against the same w: **0.591**.

The reference set scoring above the genomic mean is the expected behaviour and confirms the w values carry signal; if the two were equal, the reference set would not be distinguishing anything.

## Most and least adapted codons

| aa | preferred codon | w | rarest codon | w |
|---|---|---|---|---|
| A | GCT | 1.000 | GCG | 0.048 |
| C | TGT | 1.000 | TGC | 0.519 |
| D | GAC | 1.000 | GAT | 0.974 |
| E | GAG | 1.000 | GAA | 0.857 |
| F | TTC | 1.000 | TTT | 0.742 |
| G | GGT | 1.000 | GGG | 0.072 |
| H | CAC | 1.000 | CAT | 0.661 |
| I | ATT | 1.000 | ATA | 0.229 |
| K | AAG | 1.000 | AAA | 0.446 |
| L | TTG | 1.000 | CTC | 0.164 |
| N | AAC | 1.000 | AAT | 0.426 |
| P | CCA | 1.000 | CCG | 0.088 |
| Q | CAA | 1.000 | CAG | 0.591 |
| R | AGA | 1.000 | CGG | 0.022 |
| S | TCT | 1.000 | TCG | 0.161 |
| T | ACT | 1.000 | ACG | 0.176 |
| V | GTT | 1.000 | GTA | 0.252 |
| Y | TAC | 1.000 | TAT | 0.405 |
