# Stoichiometric production ceilings and realised titers in *Komagataella phaffii* and *Trichoderma reesei*

A dry-lab study of recombinant food proteins. No experiments were run; everything
here is computed from public genome-scale metabolic models, public protein
annotation, and a hand-curated corpus of titers read out of published papers.

## The question and the answer

Recombinant food proteins are produced at titers that differ by orders of
magnitude, and the field has largely looked for the explanation in the proteins
themselves: how many disulfide bonds, how many glycosylation sites, how
expensive the chain is to build. This project asked whether metabolic
stoichiometry can account for the differences, and then whether anything about
the protein can.

**It cannot, and the reason is specific.** Two findings, in the order they were
established:

1. **The stoichiometric ceiling is nearly flat.** The maximum theoretical yield
   of protein per gram of substrate varies only **1.26-fold** across 36
   proteins, from caseins to collagens to cytokines, while realised titers span
   several orders of magnitude. On a log scale realised production is about
   **46 times more variable** than the ceiling that bounds it. Metabolic cost is
   not the binding constraint, which inverts the usual tractability ranking:
   by stoichiometry the caseins are among the *cheapest* targets.

2. **About half the variation is not attached to the protein at all.** Matching
   every published measurement to its protein by UniProt accession rather than
   by name lets one protein appear many times, and then the same protein in
   different hands spreads enormously: hen ovalbumin 200-fold across four
   studies, human α-lactalbumin 115-fold, κ-casein 102-fold, type III collagen
   88-fold. The mean log₁₀ spread *within* a single protein is 0.638 against
   0.892 across the whole corpus, so roughly **half the variance in realised
   production is reproduced at fixed sequence**. A predictor computed from a
   sequence cannot explain variation that occurs when the sequence does not
   vary.

Both are statements of association. Neither identifies folding, secretion or
proteolysis as the mechanism, and this corpus could not: process conditions,
strain background, gene copy number and assay method all vary together across
studies and cannot be separated with 88 records.

## What is a contribution and what is not

`docs/PRIOR_ART_AUDIT.md` is an adversarial audit of the prior art and should be
read before the results. It concedes plainly that **per-protein metabolic cost
modelling from sequence features is established work** — published in
*S. cerevisiae* twice, in CHO, and in *K. phaffii* itself. The cost engine here
is an implementation of a known method, not a new one.

What is new is narrower: the method applied to this target panel, validated
against *measured* literature titers rather than simulated production rates,
with the gap against the ceiling decomposed into protein, study and process
components.

## Repository map

| Path | What is in it |
|---|---|
| `src/` | Every analysis script. See `src/README.md` for the run order. |
| `docs/` | The prior-art audit, every cost parameter with its source, the titer-database schema, and the original brief. |
| `data/literature/` | The curated titer corpus (306 records) and the 232-entry bibliography, with their verification reports. |
| `data/sequences/` | The curated 20-protein panel and the harvested sequences. |
| `data/external/` | UniProt entries, AlphaFold models, *K. phaffii* CDS. |
| `data/models/` | The genome-scale metabolic models, iMT1026v3 among them. |
| `results/tables/` | Every output table and results write-up. |
| `paper/` | The manuscript: one Markdown file per chapter, the Word template and the HTML stylesheet. `python3 src/make_docx_template.py && python3 src/build_thesis.py` writes `paper/build/thesis.{md,html,docx}`. |

## Reading order for the results

1. `results/tables/variance_decomposition.md` — the headline, with bootstrap
   intervals and the variance components.
2. `results/tables/ceiling_gap.csv` — ceiling, best measured titer and
   utilisation, per protein and host.
3. `results/tables/food_subset_signal.md` — the sequence-feature search, and a
   **retraction**: an earlier disorder correlation of ρ −0.833 did not survive
   correct titer matching and is recorded here with the reason it looked robust.
4. `results/tables/product_classes_and_filters.md` — filter sensitivity.
5. `data/literature/titers_merged_report.md` — how the corpus was built.

## Data integrity

The corpus is the part most likely to be wrong, so it was audited rather than
trusted. Each report below records what was checked and what changed, with the
value as originally recorded preserved beside every correction.

- `data/external/sequence_verification_report.md` — every sequence re-fetched
  from UniProtKB and identified by its published CRC64 checksum, not by length
  and mass, which do not identify a sequence.
- `data/literature/identifier_verification_report.md` and
  `reference_corrections.md` — 62 reference strings carried the wrong first
  author; all were rebuilt from registry metadata.
- `data/literature/bibliography_corrections.md` and `doi_candidate_audit.md` —
  191 of 232 bibliography entries now carry a registry-verified DOI. The 41
  without are FDA notices, company reports, trade press and theses, which have
  none to find.

Five faults in the analysis itself were found and fixed by these audits, each
recorded in the commit that fixed it: UniProt feature *lines* counted as PTM
sites; a protein fragment pooled with its parent; orthologues pooled across
species; a quail titer read as a chicken one; and a fusion carrier counted as
the product. Four of the five would have made the paper's claims look stronger
than the data supports.

## Reproducing

Python 3 with `cobra`, `numpy`, `scipy`, `pandas`, `statsmodels` and
`biopython`; `metapredict` is optional and only affects the disorder features.
Scripts take no arguments and resolve paths relative to the repository, so from
the repository root:

    python3 src/<script>.py

Run order and dependencies are in `src/README.md`. The scripts that call out to
UniProt, Crossref and Europe PMC need network access; everything else runs from
the data already in the repository.
