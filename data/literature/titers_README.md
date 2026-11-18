# Reported secreted/expressed titers — validation dataset

Compiled 2026-11-18. Two tables:

| File | Rows | Scope |
|---|---|---|
| `titers_host_panel.csv` | 109 | Recombinant protein titers in *Komagataella phaffii* (*Pichia pastoris*), *Trichoderma reesei*, plus a small set of non-*Pichia* comparator hosts |
| `titers_target_proteins.csv` | 32 | The thesis target proteins (caseins, β-lactoglobulin, α-lactalbumin, ovalbumin, soy leghemoglobin, lactoferrin) in **any** microbial host, with PTM and functionality notes |

---

## 1. Search strategy

All retrieval was done with web search / web fetch tools (the container's `curl` cannot reach
UniProt, NCBI, EBI or publishers). The NCBI E-utilities endpoint and `pmc.ncbi.nlm.nih.gov`
were unavailable (robots-disallowed / CAPTCHA), so the primary harvesting engine was the
**Europe PMC REST article API** (`https://europepmc.org/api/get/articleApi`), which returns
full abstracts plus structured metadata (PMID, authors, journal, year, volume, DOI) for up to
~25 records per query.

Query families used (each run against `resultType=core`):

1. `"Pichia pastoris" AND ABSTRACT:"g/L" AND ABSTRACT:secret*`
2. `"Komagataella phaffii" AND ABSTRACT:"mg/L" AND secretory`
3. `"Pichia pastoris" AND ABSTRACT:"mg/L" AND ABSTRACT:"alpha-factor"` (targets rows where the
   secretion leader is actually reported — the main reason the `signal_peptide` column is
   populated at all)
4. Enzyme-class queries: `lipase`, `phytase`, `xylanase`, `cellulase/endoglucanase`,
   `trypsin/glucose oxidase/chymosin`, `antibody fragment`
5. `"Trichoderma reesei" AND ABSTRACT:"g/L"` and `... ABSTRACT:"mg/L"`, plus
   `"Trichoderma reesei" AND "heterologous protein"`
6. Target-protein queries: `beta-lactoglobulin`, `alpha-lactalbumin`, `ovalbumin`, `casein`,
   `beta-casein`, `lactoferrin`, `leghemoglobin OR myoglobin`, each `AND recombinant AND
   ABSTRACT:"mg/L"` or `"g/L"`
7. Direct record pulls by `EXT_ID:<pmid>` to verify specific papers
8. Publisher/abstract pages fetched directly for records not in Europe PMC
   (ScienceDirect for *Food Bioscience* and *Process Biochemistry*; dairy-journal.org for
   *Dairy Science and Technology*; pubmed.gov for two anchors)

Review articles were used as a secondary source only where a primary paper could not be
reached: Cos et al. 2006 (*Microb Cell Fact* 5:17, Table 6) and Beck et al. 2025
(*BMC Biotechnol* 25, recombinant egg proteins).

### Anchor verification (all four requested anchors were checked, not assumed)

| Anchor | Status | What the source actually says |
|---|---|---|
| β-lactoglobulin ~1 g/L and ovalbumin ~2 g/L in *T. reesei* (Aro et al. 2023, *Food Res Int* 163:112131) | **verified** | "The production level of TrBLG and TrOVA were 1 g/L and 2 g/L, respectively." DOI 10.1016/j.foodres.2022.112131 |
| Soy leghemoglobin 3.5 g/L in *P. pastoris* (Shao et al. 2022, *Bioresour Technol* 363:127884) | **verified** | "maximal leghemoglobin titer and heme binding ratio reached as high as 3.5 g/L and 93 %" |
| Human lactoferrin ~1200 mg/L (Jiang et al. 2008) | **verified**, citation corrected | Jiang T, Chen L, Jia S, Chen L, Ma Y. *Dairy Science and Technology* 88(2):173–181, DOI 10.1051/dst:2007019. "A yield of approximately 1200 mg·L-1 was obtained in fed-batch fermentation with this system" |
| β-lactoglobulin 13.88 g/L in *K. phaffii* (Yao et al., *Food Bioscience* 2026, 82:109383) | **verified**, title/authors recovered | Yao C, Zhu H, An Q, Zhang M, Zheng Y, Cai M. "Omics-guided global rewiring of yeast metabolism enables high-level production of β-lactoglobulin", DOI 10.1016/j.fbio.2026.109383. "resulting in a final titer of 13.88 g/L in bioreactor fermentation" |

**No anchor failed verification.** Two anchors had incomplete bibliographic data in the brief
(journal for Jiang 2008; authors/title for Yao 2026) and those were completed from the sources.

---

## 2. Inclusion criteria

A row was created only if **all** of the following held:

- The source was actually retrieved in this session (abstract page, publisher abstract, or
  Europe PMC `core` record). Nothing was entered from memory.
- A **mass-per-volume** figure (g/L, mg/L, µg/L) for a recombinant protein is stated in the
  retrieved text, and that exact sentence is copied into `evidence_quote`.
- The host is a microbial production host. For `titers_host_panel.csv` the emphasis is
  *K. phaffii* and *T. reesei*; a small number of non-*Pichia* rows are retained explicitly as
  comparators and are identifiable from the `host` column.

## 3. Exclusion criteria

- **Activity-only reports.** U/mL, U/L, IU/mL or katal values with no mass titer were dropped
  (this removed a large fraction of the phytase, xylanase and cellulase literature).
- **Small-molecule titers.** Many *K. phaffii* metabolic-engineering papers surface on `"g/L"`
  queries but report lactate, 3-HP, kestose, sclareol, ethanol, Neu5Ac, itaconate or citrate.
  All excluded.
- **Biomass.** Dry cell weight in g/L (e.g. "DCW 120 g/L") is not a titer.
- **Non-volumetric units.** mg/kg seed, g/kg brown rice, % of total soluble protein.
- **Non-microbial hosts** (CHO, transgenic mice, rice, Arabidopsis, cell-free systems) unless
  needed to document a gap.
- **Press releases and company marketing claims.** None were used. The one company-derived
  value present (ovomucoid 3.2 g/L, EVERY Company, reached via Beck et al. 2025) is marked
  `medium` and its origin is stated in `notes`; the single `low`-confidence row in the panel is
  a platform-capability claim quoted in a paper's background, not a measured result.

## 4. Normalisation rules

- `titer_mg_L` = `titer_value` converted to mg/L: g/L × 1000, mg/L × 1, µg/L ÷ 1000.
  Nothing else is transformed.
- Where a paper reports mg/mL, the original string is quoted verbatim and the conversion is
  recorded in `notes` (e.g. Chen GH 2009: "0.15 mg/mL of broth" → 150 mg/L).
- **No activity-to-mass conversion was attempted.** Specific activity is protein- and
  assay-dependent, so U/mL was never converted.
- Where a paper reports several stages (flask → bioreactor, baseline → engineered), each stage
  is a **separate row** and the `notes` column says that the rows come from one study and are
  therefore **not statistically independent**. Affected sets include Li C 2015 (phytase 0.75 →
  9.58 g/L), Liu C 2024 (OVA 42 mg/L → 3.70 g/L), Qin P 2024 (84.6 mg/L → 3.4 g/L), Deng M 2022
  (5.2 → 56.3 mg/L), Hu C 2025 (368 → 1349 mg/L), Chen H 2025 (1.1 → 4.5 → 6.0 g/L), Wu Z 2026
  (410 mg/L → 3.14 g/L), Zahrl 2022 (Fab and scFv share one quote).
- `secreted` takes `yes`, `no`, or `intracellular`. `no` means the product is not secreted into
  the medium (e.g. VLPs, cytoplasmic fusion proteins) where the source does not use the word
  "intracellular" itself.

## 5. Confidence levels

| Level | Definition |
|---|---|
| `high` | Verbatim titer sentence taken from the abstract or abstract page of a peer-reviewed primary research paper |
| `medium` | Value read out of a review table or a secondary record where the primary paper was not retrieved; or a non-English primary paper with no DOI in the index |
| `low` | Platform/company capability claim, kept separate and not to be pooled with measured rows |
| `unverified` | Row retained **only to document a gap** — `titer_value` is empty and `evidence_quote` says plainly that no titer was found |

### Row counts by confidence

**`titers_host_panel.csv` — 109 rows**

| Confidence | Rows |
|---|---|
| high | 96 |
| medium | 12 |
| low | 1 |

By host: *K. phaffii* / *P. pastoris* 91 · *T. reesei* 8 · other comparator hosts 10.

**`titers_target_proteins.csv` — 32 rows**

| Confidence | Rows |
|---|---|
| high | 28 |
| medium | 1 |
| unverified | 3 |

By target protein: lactoferrin 10 · β-lactoglobulin 5 · ovalbumin 4 · soy leghemoglobin 4 ·
α-lactalbumin 3 · caseins 4 (α-s1 1, κ 1, κ-CMP 1, plus 2 gap rows for β-casein and α-s2-casein)
· 1 PTM-constraint provenance row.

---

## 6. Known biases and cautions

1. **Publication bias toward record titers.** Every query term that finds a titer ("highest",
   "g/L", "high-level") selects for papers whose selling point is a new maximum. Low or failed
   expression is largely unpublished. The distribution in these tables is an upper envelope,
   not a population mean.
2. **Shake flask and fed-batch are not comparable.** Within single studies the gap is 13× (Li C
   2015, phytase), 40× (Qin P 2024), 88× (Liu C 2024, ovalbumin) and 7.7× (Wu Z 2026,
   lactoferrin). Never pool `cultivation_mode` classes. A large number of rows have
   `cultivation_mode` = "not reported" because the abstract does not say — these should be
   treated as missing, not as flask.
3. **"Titer" often means total extracellular protein.** Several high *K. phaffii* values are
   reported as "total protein content" or "protein concentration", not product-specific mass:
   Xiao 2023 (5.41 g/L), Xiao 2025 (3.83 g/L), Dai 2023 (15.8 g/L), Liu C 2024 xylanase
   (11.8 g/L), Ahmad 2025 (0.79 g/L), Zhou 2026 (8.5 g/L extracellular protein for HiC).
   These are flagged in `notes` and will inflate any product-titer analysis.
4. **Suspected outliers, retained with the quote.** Zhu W 2021 HSA 17.47 g/L,
   Watanabe 2009 phytase 23 g/L (unit basis unclear in the abstract), Li H 2026 endoglucanase
   23 g/L, Viader-Salvadó 2013 phytase 6.4 g/L (mass vs total protein ambiguous). Keep or drop
   deliberately; do not drop silently.
5. **Secreted vs intracellular.** The two highest leghemoglobin numbers are of different kinds:
   7.27 g/L (Tian 2023) is **intracellular** in *K. marxianus*, whereas 6.0 g/L (Chen 2025) and
   3.5 g/L (Shao 2022) are secreted in *K. phaffii*. Filter on `secreted` before comparing.
6. **Host-panel imbalance.** 91 of 109 panel rows are *K. phaffii*/*P. pastoris* and only 8 are
   *T. reesei*. *T. reesei* heterologous-protein work overwhelmingly reports enzyme activity or
   fold-change rather than mass titers, so the fungal arm is genuinely sparse in the literature,
   not just under-searched here.
7. **Abstract-level metadata only.** Promoter, signal peptide and strain are blank or "not
   reported" wherever the abstract omitted them. Full-text retrieval was blocked for most
   paywalled journals, so these columns are systematically incomplete. Do not infer "alpha-MF"
   from a vector name unless `notes` says so (pPIC9K / pPICZαA rows where this inference was
   made are flagged).
8. **Recent-record skew.** The Europe PMC relevance ranking favoured 2024–2026 publications, so
   classic 1990s–2000s high-titer reports (e.g. the original *P. pastoris* HSA work) are
   under-represented. Rows from 1990–2011 were added deliberately to widen the year range.
9. **Collagen over-representation.** Recombinant human-like collagens dominate the very high
   *K. phaffii* titers (10.3, 15.3, 19.4 g/L). They are highly repetitive, non-glycosylated,
   protease-resistant polypeptides and are a poor proxy for globular food proteins. Consider
   excluding them from any "what titer is achievable for a milk protein" estimate.
10. **UniProt accessions are hand-assigned and partial.** The column is filled only where the
    identity of the protein and its source species were unambiguous; it is blank otherwise
    rather than guessed. Accessions were not machine-verified against UniProt in this session
    (UniProt is unreachable from the container) — re-validate before publication.

## 7. Documented gaps requiring follow-up

- **β-casein** and **α-s2-casein**: no primary microbial-host titer in g/L or mg/L was found.
  Both appear as `unverified` rows with empty `titer_value`. The likely sources are patents and
  company regulatory filings rather than journal articles.
- **Ovalbumin in *K. phaffii***: secretion is demonstrated (García-Calvo 2025,
  10.1186/s12934-025-02716-x, "successfully expressing and secreting chicken ovalbumin") but no
  titer is stated. Marked `unverified`; do not use quantitatively.
- Review tables (Cos 2006 Tables 1–5) could not be fully retrieved — the BioMed Central table
  endpoints returned robots-disallowed after the first request. Only Table 6 was obtained.
