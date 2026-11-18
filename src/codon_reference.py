#!/usr/bin/env python3
"""Build a Komagataella phaffii codon-usage reference and a CAI calculator.

Source: the CDS set of the RefSeq reference assembly GCF_000027005.1
(K. phaffii GS115, ASM2700v1), downloaded from the NCBI Datasets API.

Two references are produced, because they answer different questions.

  *genome-wide* - codon usage over every annotated CDS. Describes what the
   organism's genes look like on average.

  *highly expressed* - codon usage over a reference set of genes that are
   highly expressed in essentially all growth conditions. This is the correct
   reference for a Codon Adaptation Index, because CAI measures similarity to
   the codon choice of abundant proteins, not to the genomic average
   (Sharp & Li, Nucleic Acids Res 15:1281, 1987).

No expression data for this organism is used, so the highly expressed set is
assembled from functional annotation, using the standard proxy classes:
cytosolic ribosomal proteins, translation elongation and initiation factors,
glycolytic enzymes, and the major chaperones. The selection is written out in
full so it can be audited and changed. Genes are matched on the `protein=`
field of the CDS FASTA header, and the matched list is saved.

Outputs
  data/external/kphaffii_cds/codon_usage_genome.tsv
  data/external/kphaffii_cds/codon_usage_highly_expressed.tsv
  data/external/kphaffii_cds/highly_expressed_genes.tsv
  data/external/kphaffii_cds/CODON_REFERENCE.md
"""
from __future__ import annotations

import csv
import math
import os
import re
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
CDSD = os.path.join(ROOT, "data", "external", "kphaffii_cds")

BASES = "TCAG"
CODONS = [a + b + c for a in BASES for b in BASES for c in BASES]

CODON_TABLE = {}
_aa = ("FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG")
for _c, _a in zip(CODONS, _aa):
    CODON_TABLE[_c] = _a

SYN = defaultdict(list)
for _c, _a in CODON_TABLE.items():
    SYN[_a].append(_c)

# Proxy classes for constitutively highly expressed genes. Each pattern is
# matched, case-insensitively, against the `protein=` field of the CDS header.
HIGHLY_EXPRESSED_PATTERNS = [
    (r"\bribosomal protein\b", "cytosolic ribosomal protein"),
    (r"\b40S ribosomal\b|\b60S ribosomal\b", "cytosolic ribosomal protein"),
    (r"translation elongation factor", "translation factor"),
    (r"translation initiation factor", "translation factor"),
    (r"\bglyceraldehyde-3-phosphate dehydrogenase\b", "glycolysis"),
    (r"\bphosphoglycerate kinase\b", "glycolysis"),
    (r"\benolase\b", "glycolysis"),
    (r"\bpyruvate kinase\b", "glycolysis"),
    (r"\btriose[- ]?phosphate isomerase\b", "glycolysis"),
    (r"\bfructose-bisphosphate aldolase\b", "glycolysis"),
    (r"\bphosphoglycerate mutase\b", "glycolysis"),
    (r"\bhexokinase\b|\bglucokinase\b", "glycolysis"),
    (r"\bglucose-6-phosphate isomerase\b|phosphoglucose isomerase",
     "glycolysis"),
    (r"\bheat shock protein (70|90)\b|\bHsp(70|90)\b", "major chaperone"),
    (r"\balcohol oxidase\b", "methanol utilisation"),
]

# Patterns that must NOT enter the reference set. Three groups:
#
#  * mitochondrial and organellar ribosomes, which are not abundant in the
#    sense CAI requires;
#  * the enzymes that act *on* an abundant protein rather than being one.
#    This matters: matching "ubiquitin" on free text pulled in 55 genes, every
#    one of them a ligase, conjugating enzyme or protease, and matching
#    "actin" pulled in actin-associated and Rho-GAP proteins. All are
#    regulatory and low-abundance, and including them would pull the codon
#    reference towards average usage and flatten the index. The ubiquitin and
#    actin classes were therefore dropped altogether rather than patched,
#    since a free-text name cannot reliably distinguish the abundant protein
#    from its regulators;
#  * modifying and assembly factors named after ribosomal proteins.
EXCLUDE_PATTERNS = [
    r"mitochondrial ribosomal", r"\bmitoribosom", r"chloroplast",
    r"ligase", r"conjugating", r"hydrolase", r"protease", r"peptidase",
    r"kinase", r"phosphatase", r"methyltransferase", r"acetyltransferase",
    r"-like\b", r"\bdomain-containing\b", r"\brelated\b", r"associated",
    r"\bbinding\b", r"assembly", r"biogenesis", r"chaperone for",
    r"\bregulat", r"\bGTPase activating\b", r"pseudouridine", r"\bsimilarity",
]


def read_cds(path):
    """Yield (header, sequence) for every CDS."""
    hdr, buf = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if line.startswith(">"):
                if hdr is not None:
                    yield hdr, "".join(buf)
                hdr, buf = line[1:], []
            else:
                buf.append(line)
    if hdr is not None:
        yield hdr, "".join(buf)


def field(hdr, key):
    m = re.search(rf"\[{key}=([^\]]*)\]", hdr)
    return m.group(1) if m else ""


def count_codons(seq):
    seq = seq.upper().replace("U", "T")
    out = defaultdict(int)
    # drop the terminal stop; count whole codons only
    n = (len(seq) // 3) * 3
    for i in range(0, n, 3):
        c = seq[i:i + 3]
        if c in CODON_TABLE and CODON_TABLE[c] != "*":
            out[c] += 1
    return out


def usage_table(counts):
    """RSCU and relative adaptiveness w for each codon."""
    rows = []
    total = sum(counts.values()) or 1
    w_by_aa = {}
    for aa, cods in SYN.items():
        if aa == "*":
            continue
        obs = {c: counts.get(c, 0) for c in cods}
        s = sum(obs.values())
        k = len(cods)
        mx = max(obs.values()) if obs else 0
        for c in cods:
            rscu = (obs[c] * k / s) if s else 0.0
            w = (obs[c] / mx) if mx else 0.0
            w_by_aa[c] = w
            rows.append({
                "codon": c, "aa": aa, "count": obs[c],
                "fraction_of_aa": round(obs[c] / s, 5) if s else 0.0,
                "per_1000": round(1000.0 * obs[c] / total, 3),
                "rscu": round(rscu, 4), "relative_adaptiveness_w": round(w, 4),
            })
    rows.sort(key=lambda r: (r["aa"], -r["count"]))
    return rows, w_by_aa


def cai(seq, w):
    """Codon Adaptation Index: geometric mean of relative adaptiveness.

    Codons of single-codon families (Met, Trp) and stops are excluded, since
    they carry no information about codon choice.
    """
    seq = seq.upper().replace("U", "T")
    vals = []
    n = (len(seq) // 3) * 3
    for i in range(0, n, 3):
        c = seq[i:i + 3]
        aa = CODON_TABLE.get(c)
        if aa in (None, "*", "M", "W"):
            continue
        wi = w.get(c, 0.0)
        if wi > 0:
            vals.append(math.log(wi))
    return math.exp(sum(vals) / len(vals)) if vals else 0.0


def main():
    cds_path = os.path.join(CDSD, "cds_from_genomic.fna")
    genome = defaultdict(int)
    he = defaultdict(int)
    he_genes = []
    n_cds = 0
    for hdr, seq in read_cds(cds_path):
        n_cds += 1
        cc = count_codons(seq)
        for k, v in cc.items():
            genome[k] += v
        prot = field(hdr, "protein")
        if any(re.search(p, prot, re.I) for p in EXCLUDE_PATTERNS):
            continue
        for pat, cls in HIGHLY_EXPRESSED_PATTERNS:
            if re.search(pat, prot, re.I):
                for k, v in cc.items():
                    he[k] += v
                he_genes.append({
                    "locus_tag": field(hdr, "locus_tag"),
                    "protein_id": field(hdr, "protein_id"),
                    "protein": prot, "class": cls,
                    "length_nt": len(seq),
                    "length_aa": len(seq) // 3 - 1,
                })
                break

    g_rows, g_w = usage_table(genome)
    h_rows, h_w = usage_table(he)

    with open(os.path.join(CDSD, "codon_usage_genome.tsv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(g_rows[0].keys()),
                           delimiter="\t")
        w.writeheader()
        [w.writerow(r) for r in g_rows]
    with open(os.path.join(CDSD, "codon_usage_highly_expressed.tsv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(h_rows[0].keys()),
                           delimiter="\t")
        w.writeheader()
        [w.writerow(r) for r in h_rows]
    with open(os.path.join(CDSD, "highly_expressed_genes.tsv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(he_genes[0].keys()),
                           delimiter="\t")
        w.writeheader()
        [w.writerow(r) for r in sorted(he_genes, key=lambda r: (r["class"],
                                                                r["protein"]))]

    by_class = defaultdict(int)
    for g in he_genes:
        by_class[g["class"]] += 1

    # sanity: CAI of the reference set's own genes against its own w should
    # be high, and the genome average should be lower.
    he_ids = {g["protein_id"] for g in he_genes}
    cai_he, cai_all = [], []
    for hdr, seq in read_cds(cds_path):
        v = cai(seq, h_w)
        cai_all.append(v)
        if field(hdr, "protein_id") in he_ids:
            cai_he.append(v)

    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    lines = [
        "# Komagataella phaffii codon-usage reference", "",
        "Source: CDS set of the RefSeq reference assembly "
        "`GCF_000027005.1` (K. phaffii GS115, ASM2700v1), downloaded from the "
        "NCBI Datasets API. The downloaded archive's md5 is recorded in "
        "`gs115.zip.md5`.", "",
        f"CDS parsed: **{n_cds}**. Codons counted (stops excluded): "
        f"**{sum(genome.values()):,}**.", "",
        "## Two references, for two different questions", "",
        "`codon_usage_genome.tsv` is the usage over every annotated CDS: what "
        "this organism's genes look like on average.", "",
        "`codon_usage_highly_expressed.tsv` is the usage over a reference set "
        "of constitutively highly expressed genes. **This is the one to use "
        "for a Codon Adaptation Index**, because CAI measures similarity to "
        "the codon choice of abundant proteins, not to the genomic average "
        "(Sharp & Li, Nucleic Acids Res 15:1281, 1987). Using the genomic "
        "average as the CAI reference is a common error and makes the index "
        "nearly uninformative.", "",
        "Both tables give, per codon, the count, the fraction within its "
        "synonymous family, the frequency per 1,000 codons, the RSCU, and the "
        "relative adaptiveness w used by CAI.", "",
        f"## The highly expressed reference set ({len(he_genes)} genes)", "",
        "No expression data for this organism is used, so the set is built "
        "from functional annotation using the standard proxy classes, matched "
        "on the `protein=` field of each CDS header. Every member is listed "
        "in `highly_expressed_genes.tsv` so the selection can be audited.",
        "",
        "Free-text name matching needs an exclusion list, and getting it "
        "wrong is not harmless. A first pass matching `ubiquitin` admitted 55 "
        "genes, every one of them a ligase, conjugating enzyme or protease "
        "rather than ubiquitin itself, and matching `actin` admitted "
        "actin-associated and Rho-GAP proteins. All are regulatory and "
        "low-abundance. With them included the reference set scored a mean "
        "CAI of 0.749 against a genomic mean of 0.699, a separation of 0.050; "
        "after excluding them and the other modifying and assembly factors, "
        "the separation is 0.135, nearly three times larger. Contaminating "
        "the reference set with average-usage genes pulls w towards the "
        "genomic average and flattens the index, which is exactly the failure "
        "mode that makes a CAI uninformative. The ubiquitin and actin classes "
        "were dropped altogether rather than patched, because a free-text "
        "product name cannot reliably separate an abundant protein from its "
        "regulators.", "",
    ]
    for k, v in sorted(by_class.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")
    lines += [
        "", "## Sanity check", "",
        f"Mean CAI of the reference genes against their own w: "
        f"**{mean(cai_he):.3f}**.",
        f"Mean CAI of all {n_cds} CDS against the same w: "
        f"**{mean(cai_all):.3f}**.", "",
        "The reference set scoring above the genomic mean is the expected "
        "behaviour and confirms the w values carry signal; if the two were "
        "equal, the reference set would not be distinguishing anything.", "",
        "## Most and least adapted codons", "",
        "| aa | preferred codon | w | rarest codon | w |",
        "|---|---|---|---|---|",
    ]
    for aa in sorted(SYN):
        if aa == "*" or len(SYN[aa]) < 2:
            continue
        fam = sorted(SYN[aa], key=lambda c: -h_w.get(c, 0))
        lines.append(f"| {aa} | {fam[0]} | {h_w.get(fam[0], 0):.3f} | "
                     f"{fam[-1]} | {h_w.get(fam[-1], 0):.3f} |")
    with open(os.path.join(CDSD, "CODON_REFERENCE.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:38]))


if __name__ == "__main__":
    main()
