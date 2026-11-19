# Scripts

No script takes arguments; each resolves its paths relative to the repository
root, so run them from there as `python3 src/<name>.py`. They are grouped below
by what they are for, and within each stage they are listed in the order they
have to run.

Three scripts need network access: `fetch_sequences.py`, `harvest_external.py`
and the four verification scripts. Everything else runs from data already in the
repository.

## Stage 1 — acquire

| Script | What it does |
|---|---|
| `fetch_sequences.py` | Fetches target sequences and annotation from the UniProt REST API. |
| `harvest_external.py` | Fetches UniProt entries and AlphaFold models, computes per-model pLDDT summaries, and logs every failure rather than skipping it silently. |
| `codon_reference.py` | Builds a *K. phaffii* codon-usage reference and a CAI calculator. The reference set is restricted to genuinely highly expressed genes; see the exclusion list and the note on why "ubiquitin" and "actin" name matches had to be dropped. |

## Stage 2 — curate the corpus

| Script | What it does |
|---|---|
| `merge_titers.py` | Merges the independent titer sweeps into one corpus and deduplicates. Fragment and carrier patterns are tested **before** parent-protein patterns, for the reason given in the comment above `PROTEIN_CANON`. |
| `annotate_classes.py` | Assigns a product class to every record, flags therapeutics, and recomputes the headline spreads under every combination of inclusion filters. |

## Stage 3 — verify, before trusting any of it

| Script | What it does |
|---|---|
| `verify_sequences.py` | Re-fetches every accession from UniProtKB and identifies it by the published CRC64 checksum, recomputed locally. Length and mass are not sufficient: two variants of a protein, or one isoform's precursor and another's mature chain, can agree on both. |
| `uniprot_features.py` | Correct extraction of PTM counts and the mature chain. Counting feature *lines* is wrong in four distinct ways, each inflating secretory load; there is a regression test per failure mode, so **run this directly to self-test** and it exits non-zero on failure. |
| `verify_identifiers.py` | Resolves every DOI and PMID in the titer corpus against Crossref and Europe PMC. |
| `fix_references.py` | Rebuilds every reference string from registry metadata, preserving the string as recorded. |
| `verify_bibliography.py` | The same treatment for the 232-entry bibliography. |
| `adopt_doi_candidates.py` | Checks each suggested DOI on title, year, author and work type before adopting it, then confirms it resolves at doi.org independently of Crossref. |

## Stage 4 — model

| Script | What it does |
|---|---|
| `protein_cost.py` | The cost engine: a mass- and electron-balanced synthesis and secretion reaction per protein. Every tunable parameter lives in `CostParams` and each is documented with a source in `docs/COST_PARAMETERS.md`. Reactions are closed on protons generically, with an assertion that nothing but hydrogen may remain unbalanced. |
| `yields.py` | Maximum theoretical yield in grams of protein per gram of substrate, on glycerol, methanol, both, or glucose. |
| `features.py` | The sequence-feature panel: FoldIndex, charge patterning κ, GRAVY, host amino-acid divergence, biosynthetic cost, and metapredict disorder when it is installed. Every feature is computed from the **mature** chain. |
| `ceilings_by_accession.py` | Ceilings for all 36 held accessions rather than only the curated panel, so therapeutics and collagens have ceilings to compare against. |

## Stage 5 — analyse

| Script | What it does |
|---|---|
| `ceiling_gap.py` | The per-protein table: ceiling, best defensible measured titer, and utilisation. Titers are matched on **both** canonical name and source organism, and only secreted measurements are used; the comment above `CORPUS_LABEL` records the three faults that made both rules necessary. |
| `gap_attribution.py` | Univariate Spearman correlations of each feature against the gap, with bootstrap intervals, permutation p-values and Benjamini–Hochberg correction. No multi-feature model is fitted; at this sample size reporting one would be indefensible. |
| `food_subset_signal.py` | The same search restricted to food proteins, with the two-cluster diagnostic that leave-one-out cannot provide. Contains the retraction of the earlier disorder result. |
| `variance_decomposition.py` | The headline. Splits the variance in realised production into between-protein, between-study and within-study components using crossed random intercepts, and reports the distributional statistics with bootstrap intervals. |

## Stage 6 — write

| Script | What it does |
|---|---|
| `make_docx_template.py` | Builds `paper/template.docx`, the Word reference document pandoc styles the thesis with, from code rather than from a binary nobody can review. Every typographic decision is a named constant with a comment, and each can be overridden for one run from the environment, e.g. `THESIS_LINE_SPACING=2.0` if an institution requires double spacing. |
| `build_thesis.py` | Assembles the twelve chapter files in order, inserts the figures with their captions, fills the title page from `paper/00_institution.yaml`, and writes `paper/build/thesis.{md,html,docx}`. The reference list is set in its own smaller style and placed in two columns; the HTML build is a single self-contained file styled by `paper/thesis.css`. |

## If you only run three

    python3 src/uniprot_features.py      # self-test; must pass before anything else
    python3 src/ceiling_gap.py           # the per-protein ceiling table
    python3 src/variance_decomposition.py # the headline result
