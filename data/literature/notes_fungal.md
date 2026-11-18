# Batch `fungal` — heterologous secretion in filamentous fungi

Scope: *Trichoderma reesei* first, plus *Aspergillus niger / oryzae / awamori (luchuensis)*,
*Myceliophthora thermophila* (= *Thermothelomyces heterothallica*, "C1"), *Neurospora crassa*.
Two record classes: (a) food proteins, (b) benchmark heterologous proteins that bound the host's
secretory capacity (`notes` contains `benchmark_non_food`).

Output: `titers_fungal.tsv` (100 rows), `papers_fungal.tsv` (59 papers), this file.

## Headline numbers

| | protein | host | titer | source |
|---|---|---|---|---|
| **Food ceiling, T. reesei** | porcine lactoferrin | T. reesei, 30-L fermenter | **2370 mg/L** | Xu et al. 2026, 10.1007/s43393-026-00509-w |
| Food, T. reesei (peer-reviewed full text read) | ovalbumin | T. reesei M2146, 1-L fed-batch | **2000 mg/L** | Aro et al. 2023 |
| | beta-lactoglobulin | T. reesei M2144, 1-L fed-batch | 1000 mg/L (800 on lactose/spent grain) | Aro et al. 2023 |
| | human lactoferrin | T. reesei CJ2095 dpea1::pdi1, 5-L | 1349.5 mg/L | Zhang et al. 2025 |
| | brazzein (sweet protein) | T. reesei, bioreactor | 1300 mg/L | Rantasalo et al. 2025 |
| **Food ceiling, Aspergillus** | hen egg white lysozyme | A. niger, soy-milk medium | 60 mg/L | Ntana et al. 2020 (review) |
| | bovine kappa-casein | A. oryzae, flask | 4.14 mg/L | Zhang et al. 2026 |
| **Non-food ceiling, single protein, T. reesei** | human IFN alpha-2b | T. reesei M674 (damp2) + SBTI | **6300 mg/L total** (4500 free + 1800 carrier-bound) | Landowski et al. 2016 |
| Non-food, total secreted protein, T. reesei | cellulase cocktail | engineered RUT-C30, molasses fed-batch | **80 600 mg/L** | Fonseca et al. 2020 |
| Non-food, total secreted protein, T. reesei (abstract only) | cellulase | ACE3 S705H, 30-L | ~125 000 mg/L | Gao et al. 2027 |
| **Non-food ceiling, any filamentous fungus** | mAb1 | T. heterothallica C1 | 24 000 mg/L (*data not shown*) | Hakkinen et al. 2026 |

## Searches run

Europe PMC REST (`/search`, `resultType=core`, pageSize 25–100) and `/{PMCID}/fullTextXML`,
driven from `curl` through small local scripts. Queries (abbreviated):

1. `AUTH:"Aro" AND "beta-lactoglobulin" AND "Trichoderma"` — located the anchor paper (2 hits).
2. `"Trichoderma reesei" AND "heterologous protein" AND (titer OR titre OR "g/L" OR yield)` — 311 hits, top 60 screened.
3. `"Trichoderma reesei" AND (chymosin OR rennin OR "human serum albumin" OR interleukin)` — 298 hits, 60 screened.
4. `"Trichoderma reesei" AND (ovalbumin OR "beta-lactoglobulin" OR casein OR lactoferrin OR myoglobin OR leghemoglobin)` — 547 hits, 60 screened.
5. `AUTH:"Landowski" AND (Trichoderma OR fungal OR secretion)` — 33 hits, all screened (Landowski is a common surname; most hits were ophthalmology/gastroenterology).
6. `AUTH:"Nordlund E" OR (AUTH:"Saloheimo M" AND Trichoderma)` — 169 hits, 40 screened (VTT line).
7. `"Aspergillus awamori" AND (chymosin OR "serum albumin" OR glucoamylase fusion)` — 172 hits, 40 screened.
8. `"Aspergillus niger" AND (lactoferrin OR lysozyme OR "egg white" OR ovalbumin OR casein)` — 3428 hits, 40 screened (very low precision).
9. `TITLE:("Trichoderma reesei" OR Aspergillus) AND TITLE:(expression OR production OR secretion) AND OPEN_ACCESS:Y AND FIRST_PDATE:[2015 TO 2026]` — 761 hits, 50 screened.
10. `"Myceliophthora thermophila" AND (secretion OR heterologous OR titer OR "g/L")` — 547 hits, 50 screened.
11. `"Neurospora crassa" AND ("heterologous protein" OR "recombinant protein" OR secretion) AND (titer OR "mg/L")` — 460 hits, 50 screened.
12. **Abstract-regex sweeps** (most productive method): full abstracts pulled for 100 records per query and machine-filtered for `mg/L`, `g/L`, `g l-1` patterns:
    - `TITLE:"Trichoderma reesei" AND (ABSTRACT:"mg/L" OR ABSTRACT:"g/L" OR ABSTRACT:"mg/l")` — 88 hits, all screened, ~40 carried numbers.
    - `(TITLE:"Aspergillus niger" OR "A. oryzae" OR "A. awamori" OR Myceliophthora) AND TITLE:(expression|production|secretion|heterologous|recombinant) AND (ABSTRACT:"mg/L" OR "g/L")` — 277 hits, 100 screened.
    - `(T. reesei OR Aspergillus OR Myceliophthora OR Thermothelomyces) AND (chymosin OR "serum albumin" OR phytase OR "Fab fragment" OR antibody OR interleukin OR laccase OR lipase OR "glucoamylase fusion")` — 14 931 hits, 100 screened.
    - `(chymosin OR prochymosin) AND (Aspergillus OR Trichoderma)`; `"human serum albumin" AND (Aspergillus OR Trichoderma OR filamentous fung*)`; `phytase AND "Aspergillus niger"`; `(T. reesei OR Aspergillus) AND (hemoglobin OR myoglobin OR leghemoglobin OR "sweet protein" OR brazzein OR thaumatin OR monellin OR "alpha-lactalbumin" OR collagen OR "egg white")`; `T. reesei AND (cellobiohydrolase OR CBHI OR Cel7A)`.
13. WebSearch (extended) + WebFetch for the paywalled anchors: Aro 2023 (ScienceDirect full text), the 2025 JAFC human-lactoferrin paper, the 2026 porcine-lactoferrin paper, Dunn-Coleman 1991 *Nature Biotechnology*, and the 2020 *Catalysts* Aspergillus review.

**Records screened: ~700 titles/abstracts; 30 open-access full texts downloaded and text-mined; 100 titer rows extracted from 59 papers.** Mining scripts kept at
`/tmp/claude-0/-home-user/ae1ee774-8ef2-5a0c-85ce-688089c65a13/scratchpad/fungal/` (`srch.py`, `abs.py`, `mine.py`, `mine2.py`, `txt.py`, `build.py`, `papers.py`, `ft/`).

## The Landowski / Nordlund / VTT line (requested explicitly)

Reconstructed and fully logged:

- **Nyyssönen et al. 1993** — murine Fab as a CBHI-carrier fusion, 150 mg/L in a 15-L fermenter. Recorded from two independent secondary statements (Landowski 2015 introduction; Table 4 of the 2026 antibody review). Primary (AEM/Nat Biotechnol era) not fetched.
- **Landowski et al. 2015** (PLoS ONE, 10.1371/journal.pone.0134723) — the 9-protease-deletion lineage; also the 23 g/L flask total-protein datum and the "chymosin and murine Fab both 150 mg/L" benchmark sentence.
- **Landowski et al. 2016** (Microb Cell Fact, 10.1186/s12934-016-0508-5) — IFN alpha-2b. 13 rows extracted (M577/M668/M671/M672/M673/M674, two media, with and without protease inhibitors, microscale and bioreactor). This is the richest single paper in the batch.
- **Rantasalo et al. 2018** (NAR, universal fungal SES) → **2019** (Sci Rep, pure-protein production: 20.9 vs 15.7 g/L total protein, ~10 g/L carrier+CalB) → **Aro et al. 2023** (BLG/OVA) → **Rantasalo et al. 2025** (brazzein). The same synthetic-promoter + CBHI-carrier platform runs through all four.
- **Nordlund E.** appears as a co-author on Aro 2023 and the brazzein paper; her other 150+ Europe PMC records are cereal/oat food-technology work with no recombinant titers, so nothing else was logged from that author stream.
- Brazzein paper states, citing VTT unpublished data, that a *single* heterologous protein has reached **>80 g/L** in T. reesei. Not recorded as a titer row (no measurement, no product named); flagged here because if true it moves the T. reesei ceiling by an order of magnitude.

## Conventions and judgement calls

- Ranges: maximum taken, per spec rule 4, and the range stated in `notes` (affects ~10 rows).
- Lower bounds (">2 g/L", "exceeding 400 mg/L", "more than one gram per liter") recorded at the bound with a `notes` flag.
- `evidence_quote` is always text actually read. Quotes mined from JATS XML have Greek letters, delta symbols, `≤` and `±` transliterated (`alpha`, `delta`, `<=`, `+/-`) because the TSV is written as plain ASCII-safe text; each such row says so in `notes`. Two quotes are split mid-sentence at "A. niger"/"T. reesei" because the sentence tokenizer broke on the abbreviation — noted on those rows.
- Rows taken from review tables (the 2026 antibody review, the 2020 *Catalysts* review, the 2025 egg-protein review, the 2023 AMB review) are `confidence=medium` with `secondary_source` in `notes` and the primary author named in `reference`. Primaries were not fetched for those.
- `titer_basis=total_secreted_protein` is used wherever the number is broth protein rather than the product — e.g. Rantasalo's ~10 g/L "mainly CBHI-carrier and calB", the A. niger aspartic-proteinase 27.5 g/L, all cellulase-cocktail ceilings. These must **not** be read as single-product titers.
- `fungal-100` (review-table ovalbumin, 2 g/L, strain "M1908") is the **same measurement** as `fungal-3` (Aro, strain M2146). Kept for provenance; do not double-count. The strain/plasmid naming discrepancy between review and primary is unresolved.
- `fungal-4` and the TLL-lipase row carry `titer_mg_L=NA` deliberately: the arm exists in the literature but no number was published. They document coverage, not data.
- Three C1/Thermothelomyces rows (24 g/L mAb1, 13 g/L glyco-mAb, >2 g/L RBD) are `confidence=low` because the papers label them "data not shown", "our unpublished data", or give no data. They are the largest numbers in the batch and should be treated as company claims.
- No DOI, PMID or number in this batch was inferred. Where a DOI could not be confirmed it is `NA` (Dunn-Coleman 1991 has a DOI but no PMID; the *Catalysts* review and the porcine-lactoferrin paper have DOIs but no PMID in Europe PMC).

## Gaps and failures

**Genuine gaps in the literature (not search failures):**

1. **No globin in any filamentous fungus.** No myoglobin, haemoglobin or leghemoglobin titer exists for T. reesei, Aspergillus, Myceliophthora or Neurospora. The nearest fungal results are yeast/yeast-like: soy leghemoglobin 398 mg/L in *S. cerevisiae* and 1653 mg/L in *K. phaffii*; cyanobacterial Hb 106 mg/L in *Tremella fuciformis*. Both logged in `papers_fungal.tsv` as `prior_art` so the absence is documented. **This is the single biggest hole for the project's purposes.**
2. **No alpha-lactalbumin, beta-casein, alpha-s1-casein, ovotransferrin, ovomucoid, avidin or collagen titer in a filamentous host.** Only kappa-casein (A. oryzae, 4.14 mg/L) and the two Aro proteins. Every other milk/egg protein titer sits in yeast or *E. coli*.
3. **No human serum albumin titer in a filamentous fungus** could be found despite four dedicated queries. HSA was requested as a benchmark; it appears to live only in *K. phaffii* / *S. cerevisiae* literature. Treat the HSA benchmark as unavailable for this host class.
4. **No A. niger phytase titer in mg/L.** Phytase is the archetypal A. niger product but the literature reports it in FTU/g or U/mL. The only mg/L phytase numbers found are in *K. phaffii* (0.75–9.58 g/L) and *M. thermophila* phytase expressed in *K. phaffii* (1.6 g/L) — wrong host, so not recorded as fungal rows.
5. **Lipase and laccase benchmarks are activity-only** in the filamentous-host literature. The Trametes LacA / T. reesei paper reports 168.3 U/L; the TLL / A. niger paper reports U/mL. Only the Kiiskinen *M. albomyces* laccase (230 / 920 mg/L) converts to mass. Rows marked `titer_basis=activity_inferred`.
6. **Insulin glargine in T. reesei is reported in mIU/L only** (58.95 mIU/L flask, 144.75 mIU/L in a 1-L bioreactor). Converting to mg/L needs an assumed specific activity, which would be a fabricated number, so no titer row was written. Paper logged as `method`.
7. **The multi-plex 2A-peptide paper reports pmol, not mg/L** (128 : 13 : 5 pmol, an 18:2:1 ratio). No titer row; the ratio itself is the useful datum and is in the one-line finding.

**Inaccessible or partially accessible papers:**

- **Aro et al. 2023** — paywalled; the ScienceDirect full text *was* readable through WebFetch and all numbers in rows `fungal-1..4` come from it. The PMC record does not exist (`isOpenAccess=N`).
- **Zhang et al. 2025, human lactoferrin (JAFC)** — paywalled; PubMed page returned a client error on fetch, so the Europe PMC `core` abstract was used instead. All four rows are `abstract_only` (noted). Strain-level and promoter detail is therefore missing.
- **Xu et al. 2026, porcine lactoferrin** — Springer landing page only; cultivation mode (fed-batch vs batch) is not stated there, so `batch_bioreactor` is an assumption flagged in `notes`. `confidence=medium` for this reason, despite it being the top food titer.
- **Dunn-Coleman et al. 1991** — *Nature Biotechnology* 1991, no full text; the ">1 g/L" figure comes from the abstract on the publisher page.
- **Ward et al. 2004 (trastuzumab in A. niger var. awamori), Kaiser et al. 2024 (HuMab 87G7 in C1), Frenken 1998, Sotiriadis 2001, Joosten 2005a/b, Okazaki 2012, Jiang 2019, Huynh 2020, Havlik 2017** — none fetched; all recorded from the verbatim Table 4 rows of the 2026 antibody review. Nine rows depend on that one secondary source.
- **ACS SynBio 2022, "Building a Versatile Protein Production Platform Using Engineered Trichoderma reesei"** (10.1021/acssynbio.1c00570) — paywalled, no abstract numbers; not logged. Likely contains extractable titers and is the clearest remaining lead.
- **PMC CAPTCHA**: `pmc.ncbi.nlm.nih.gov` article pages returned a browser-check interstitial to WebFetch throughout. The Europe PMC `fullTextXML` endpoint worked reliably instead and is the right route for this kind of batch.

**Next actions that would most improve this batch:**

1. Obtain Kaiser et al. 2024 (C1 HuMab 87G7, 1.6 g/L) and Ward et al. 2004 — nine rows currently rest on one review table.
2. Obtain the ACS SynBio 2022 T. reesei platform paper.
3. Chase the VTT ">80 g/L single heterologous protein" claim to a citable source; it would change the ceiling used for producibility modelling.
4. Decide a project policy on activity-to-mass conversion; roughly a third of the filamentous-fungal enzyme literature is otherwise unusable.
