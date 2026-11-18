# Batch `eggheme` — extraction notes

Scope: egg-white proteins (ovalbumin, ovotransferrin/conalbumin, ovomucoid, ovomucin, avidin,
hen egg-white lysozyme, cystatin) and heme/globin proteins (soy leghemoglobin/LGB2, plant
non-symbiotic hemoglobins, bovine/porcine/equine myoglobin, human/bovine haemoglobin subunits,
neuroglobin, heme-protein precision fermentation), expressed in *Komagataella phaffii*,
*Trichoderma reesei*, *Aspergillus* spp., *Saccharomyces cerevisiae*, *Yarrowia lipolytica* or
*Escherichia coli* (E. coli kept as an out-of-host comparator and flagged in `notes`).

Outputs: `titers_eggheme.tsv` (61 rows), `papers_eggheme.tsv` (57 papers).

## 1. Searches run

### Europe PMC REST (`/europepmc/webservices/rest/search`)
55 distinct queries, `pageSize` 30–100. First sweep (40 queries) covered each target protein
crossed with each in-scope host, plus generic terms:

```
"Pichia pastoris" AND leghemoglobin | ... AND ovalbumin | ... AND myoglobin
"Komagataella phaffii" AND ovalbumin
"Saccharomyces cerevisiae" AND ovalbumin AND recombinant
"Trichoderma reesei" AND ovalbumin | AND (hemoglobin OR myoglobin)
Aspergillus AND ovalbumin AND recombinant AND expression
"Escherichia coli" AND ovalbumin AND recombinant AND expression
ovotransferrin / conalbumin / ovomucoid / ovomucin AND recombinant AND expression
avidin AND recombinant AND (Pichia OR Aspergillus OR "Escherichia coli") AND expression
"hen egg white lysozyme" AND recombinant AND (Pichia OR Saccharomyces OR Aspergillus)
lysozyme AND "Pichia pastoris" AND titer
cystatin AND "egg white" AND recombinant | "chicken cystatin" AND recombinant
leghemoglobin AND recombinant AND expression AND titer | "soy leghemoglobin" AND Pichia
leghemoglobin AND "Escherichia coli" AND expression
"nonsymbiotic hemoglobin" / "non-symbiotic hemoglobin" AND expression
myoglobin AND recombinant AND "Escherichia coli" AND (yield OR titer)
myoglobin AND "Komagataella" | "bovine/porcine/equine myoglobin" AND recombinant
hemoglobin AND "Pichia pastoris" AND expression
"human hemoglobin" AND "Saccharomyces cerevisiae" AND expression
"haemoglobin" AND recombinant AND "Escherichia coli" AND yield
neuroglobin AND recombinant AND expression
"heme protein" AND "precision fermentation"
heme AND pathway AND engineering AND Pichia AND globin
"Yarrowia lipolytica" AND (hemoglobin OR myoglobin OR heme) | AND ovalbumin
"Aspergillus oryzae" AND (myoglobin OR hemoglobin OR leghemoglobin) | AND "egg white"
"egg white protein" AND recombinant AND fermentation
"animal-free" AND "egg white" AND fermentation
"Aspergillus niger" AND lysozyme AND expression
"Vitreoscilla hemoglobin" AND expression AND yield
```

Second sweep (15 gap-filling queries): `"hen egg white lysozyme" AND "Pichia pastoris"`,
`lysozyme AND Aspergillus AND secret* AND (g/L OR mg/L)`, `"human lysozyme" AND "Pichia pastoris" AND yield`,
`ovalbumin AND quail AND "Pichia pastoris"`, `"soybean hemoglobin" AND "Saccharomyces cerevisiae" AND titer`,
`"human hemoglobin" AND "Escherichia coli" AND "g/L"`, `neuroglobin AND "Escherichia coli" AND purification AND yield`,
`"beta-globin" AND recombinant AND yeast AND expression`, `"Yarrowia lipolytica" AND heme AND protein AND production`,
`ovotransferrin AND "Pichia pastoris"`, `avidin AND "Pichia pastoris" AND secretion`,
`"heme biosynthesis" AND "Komagataella phaffii" AND myoglobin`,
`"Trichoderma reesei" AND "precision fermentation" AND protein AND titer`, `"ovomucoid" AND "Komagataella"`,
plus an author-targeted query that located Xue et al. 2023.

### NCBI E-utilities
- `esearch` on PubMed for `("hen egg white lysozyme" OR "egg white lysozyme") AND (Pichia OR Komagataella OR Aspergillus OR cerevisiae)` → 41 records, all screened.
- `esearch` for `lysozyme AND "Aspergillus niger" AND secretion AND expression`, `Masuda AND lysozyme AND "Pichia pastoris" AND sweet`, `ovalbumin AND "Pichia pastoris" AND Ito AND glycosylation`, `Yang quail ovalbumin oviduct Pichia pastoris`.
- `efetch` (XML) for 3 batches of abstracts covering 46 PMIDs; all abstracts read in full.
- `esearch` on `EXT_ID:<pmid> AND SRC:MED` (core resultType) for all 54 PMIDs in the papers file, to resolve DOIs and journal names from the record rather than from memory.

### Open-access full text mined (`/europepmc/webservices/rest/<PMCID>/fullTextXML`)
`PMC12224593` (egg-protein review, Table 2 + reference list), `PMC10602571` (Yu 2023 Adv Sci, Pichia
heme chassis), `PMC12799817` (OVA/ER stress), `PMC12049782` (CRISPR toolkit, OVA reporter),
`PMC10804453` (K. marxianus LegH), `PMC10176901` (C. glutamicum plant Hb), `PMC12455655` (cell-free
LegH), `PMC13565620` (Tremella Hb), `PMC12098746` (mitochondrial heme), `PMC12260557` (B. subtilis
globins), `PMC12375200`, `PMC13520740` (plant chloroplast Mb), `PMC11211803` + `PMC11565058` (EFSA
opinions), `PMC10581837` (LegH toxicology). Each was regex-mined for every sentence containing a
mg/L, g/L, µg/mL or mg/mL figure, and for strain/promoter/copy-number statements.

### Web search
FDA GRAS inventory and company GRAS notices for soy leghemoglobin (GRN 737) and for ovalbumin
(The EVERY Company). See §4 for what this did and did not yield.

## 2. Screening volume

- **1,157 unique Europe PMC records** returned across the 55 queries after de-duplication.
- **226** had a target protein or heme/globin keyword in the title; these were read as title+metadata.
- **~60** were shortlisted as production/expression/engineering reports and read as abstract or full text.
- **46 abstracts** retrieved in full via `efetch` and read.
- **15 open-access full texts** downloaded and systematically mined for numbers.
- **61 titer rows** extracted, **57 papers** logged.

Row distribution by host: *K. phaffii* 25, *E. coli* 15, *S. cerevisiae* 13, *A. niger* 7,
*T. reesei* 1. By confidence: high 34, medium 20, low 7.

## 3. Highest-confidence titer per protein (in-scope hosts)

| protein | best titer | host / condition | confidence |
|---|---|---|---|
| soy leghemoglobin | **3,500 mg/L** secreted | *K. phaffii*, 10-L fed-batch, Shao 2022 | high |
| soybean Hb (shake flask) | 286.5 mg/L secreted | *K. phaffii* P1H9, Yu 2023 | high |
| porcine myoglobin | 296.6 mg/L (secondary) / **246.95 mg/L** read directly | *K. phaffii* P1H9, Yu 2023/2024 | medium / high |
| bovine myoglobin | 68.9 mg/L intracellular | *S. cerevisiae*, Xue 2023 | medium |
| clover hemoglobin | 13.7 mg/L intracellular | *S. cerevisiae*, Xue 2023 | medium |
| Vitreoscilla hemoglobin | 66.3 mg/L secreted | *K. phaffii* P1H9, Yu 2023 | high |
| ovalbumin (hen) | **3,700 mg/L** intracellular | *E. coli* Nissle 1917, 3-L bioreactor, Liu 2024 | high |
| ovalbumin (hen, fungal host) | 2,000 mg/L secreted | *T. reesei* M1908, bioreactor, Aro 2023 | high |
| ovalbumin (hen, *K. phaffii*) | 35 mg/L secreted | CRISPR toolkit strains, 2025 | medium |
| ovalbumin (quail) | 5,450 mg/L secreted — **outlier, see §5** | *K. phaffii*, pAOX1, ELISA, Yang 2009 | medium |
| hen egg-white lysozyme | **3,500 mg/L** secreted | *K. phaffii* GS115 + xylanase carrier, 15-L fed-batch, Cui 2022 | high |
| HEWL (fungal host) | 1,000 mg/L secreted, shake flask | *A. niger* + glucoamylase G498 carrier, Jeenes 1993 | high |
| ovomucoid | 3,200 mg/L secreted | *K. phaffii*, pAOX1, 168 h — **patent claim** | low |
| ovotransferrin | 97 mg/L secreted | *K. phaffii* KM71, pAOX1 | medium |
| avidin | 330 mg/L secreted | *K. phaffii* GS115, 3.6-L bioreactor, Zocchi 2003 | high |
| cystatin | **no numeric titer found** | — | — |
| ovomucin | **no report found** | — | — |
| neuroglobin | **no production titer found** | — | — |

## 4. Gaps, failures and inaccessible sources

**Hard gaps — no defensible number exists in anything screened:**
- **Ovomucin** — zero recombinant production reports in any host. It is 132 kDa, N- and
  O-glycosylated and proteolytically processed; the egg-protein review lists it in its
  physicochemical table but it is absent from the production table.
- **Egg-white cystatin** — four papers express chicken cystatin in *K. phaffii* X-33 (pGAP,
  α-MF, multi-copy) or *E. coli*, and one is titled "high-level production", but **none reports a
  mg/L figure in its abstract** and all four are behind ACS paywalls. Two rows were written with
  `titer_mg_L=NA` to preserve the construct record. Closing this gap needs the Chen 2001 and
  Tzeng 2004 full texts (ACS).
- **Neuroglobin** — abundant neuroscience literature (overexpression in neurons, stem cells,
  secretome studies) but no recombinant *production* report with a titer in any in-scope host.
- **Plant non-symbiotic hemoglobin** — the only production report found is cell-free
  (ACS Synth Biol 2025, ~0.5 mg/mL), not a host expression system. No yeast/fungal nsHb titer.
- **Human and bovine haemoglobin subunits** — nothing in-scope surfaced. Xue 2023 reports bovine
  and porcine *Hb* but the abstract gives numbers only for soybean/clover Hb and bovine/porcine Mb;
  the bovine Hb number is presumably in the paywalled body.
- ***Yarrowia lipolytica*** — **no egg-white or globin expression report at all**. All five queries
  crossing *Y. lipolytica* with ovalbumin, hemoglobin, myoglobin, heme and protein production
  returned nothing on target. This is a genuine white space, not a search failure.
- ***Aspergillus* for globins** — no myoglobin/hemoglobin/leghemoglobin report in any *Aspergillus*
  species. *Aspergillus* appears here only for lysozyme (*A. niger*).
- ***Trichoderma reesei*** — exactly one target-protein titer (Aro 2023 ovalbumin, 2 g/L). No
  T. reesei globin or other egg-protein report.
- **Equine myoglobin** — no recombinant production titer found (the equine *lysozyme* paper from
  *A. niger* is a different protein and is logged as prior art).

**Paywalled — titer taken from the abstract only (noted per row):**
Shao 2022 (Bioresour Technol), Xue 2023 (Bioresour Technol), Jin 2024 (Int J Biol Macromol),
Dong 2024 (J Agric Food Chem), Liu 2024 (J Agric Food Chem), Zhang 2021 (J Agric Food Chem),
Aro 2023 (Food Res Int), Cui 2022, Masuda 2005, Gheshlaghi 2005, Zocchi 2003, Jeenes 1993,
Archer 1990, MacKenzie 1994. For these, strain/promoter/vessel details absent from the abstract
were taken from the BMC Biotechnol 2025 review's Table 2 where it covers the same study, and the
row's `notes` says so.

**Paywalled with no number anywhere accessible:**
- **Yu et al., Metab Eng 2024** (the heme-biosensor paper). Its abstract reports no titer. The
  296.6 mg/L porcine-Mb figure in the row comes from Wang et al. PNAS 2025, which attributes it to
  this paper as its ref 16. Recorded `confidence=medium` with the secondary attribution spelled out.
  **This row should be re-verified against the primary before it is used as a benchmark.**
- **Qian et al., 3 Biotech 2025** — PMC11971115 returned an empty full-text response (151 bytes) on
  repeated attempts despite being indexed as open access. Abstract gives only fold-changes
  (+112.28% porcine Mb, +5.78-fold soybean Hb), no absolute titers, so no row was written.
- **The EVERY Company patent WO2016077457** — the 3.2 g/L and 1 g/L ovomucoid claims were read only
  in the review's Table 2, not in the patent. Both rows are `confidence=low` with `company_claim`.

**Regulatory sources — screened, no titers disclosed:**
Both EFSA opinions and all four Impossible Foods safety papers were retrieved and mined. They
contain **no volumetric titer**. What they do give, and what was captured in a dedicated row, is the
commercial strain disclosure: *K. phaffii* **MXY0541** (predecessor MXY0291; parent Bg11, derived
from NRRL Y-11430), soy **LGB2** in **three expression cassettes at three genomic loci**, native
haem biosynthetic pathway upregulated, submerged fed-batch fermentation, product is a cell lysate,
and leghemoglobin accounts for **68–77% of total product protein** across three batches. Promoter
identity and several construction steps are redacted (`■■■■■`) in the published opinion. EFSA also
ties the authorisation specifically to strain MXY0541, which is a real constraint on re-engineering.

The FDA side was less productive: web search surfaced the GRN 737 agency response letter and
several secondary trade-press and aggregator pages, but no FDA GRAS notice PDF containing a titer
or strain-level fermentation figure was obtained. The EVERY Company ovalbumin GRAS notice could not
be pinned to a confirmed GRN number from the sources returned, so **no GRN number is recorded
anywhere in these files** rather than guess one. Anything an aggregator site asserted about
clearance counts or capacity was not used.

## 5. Caveats a modeller must carry forward

1. **The quail-ovalbumin outlier.** Yang 2009 claims 5.45 g/L secreted quail ovalbumin — one to two
   orders of magnitude above every later ovalbumin report in any host, including dedicated
   precision-fermentation efforts a decade later that struggle past 35 mg/L in the same host. It was
   quantified by polyclonal-antibody ELISA, the cultivation scale is unstated, and the review that
   cites it reports a 450–5450 mg/L spread across clones. Both ends are recorded; treat the figure
   as an upper bound only, and do not let it anchor a *K. phaffii* ovalbumin prior.
2. **Secretion, not synthesis, limits ovalbumin in yeast.** Jin 2024 is the clearest case: 132 mg/L
   total OVA but only 8 mg/L extracellular. Several reported "OVA production" numbers are total
   cell-associated protein. Rows distinguish this in `localisation` and `notes`; do not compare a
   total-protein number against a secreted one.
3. **Carrier fusions dominate fungal egg-protein titers.** The two highest fungal/yeast lysozyme
   numbers both come from carrier fusions — *A. niger* glucoamylase-G498 (1 g/L vs ~50 mg/L
   without, same paper, 10–20×) and *K. phaffii* xylanase XynCDBFV (3.5 g/L). This is a
   construct-design covariate, not a host property, and the matched pairs in the table let it be
   estimated directly.
4. **Heme supply caps every globin titer, and heme occupancy is often poor.** Zhang 2021 obtained
   only 0.22 mol heme per mol myoglobin; Yu 2023 reports a 22% heme-binding ratio even with
   150 mg/L exogenous hemin; the plant-chloroplast work found ~35% occupancy vs 80% for
   E. coli-made Mb. Against this, Shao 2022 reports 93% heme binding at 3.5 g/L. **A globin titer
   without a stated heme-binding ratio is not a functional-protein titer** and should not be
   modelled as one.
5. **Some figures are purified yields, not broth titers** — Masuda 2005 (400 mg/L after
   ultrafiltration and ion exchange), Zocchi 2003, Rupa 2003 (4–5 mg/L "after purification"). These
   under-report fermentation performance; flagged per row.
6. **Ranges and bounds.** Per spec rule, ranges were recorded at their maximum (ovomucoid 4–5 → 5;
   avidin 0.25–0.5 → 0.5; A. niger HEWL 8–10 → 10 and 30–60 → 60), always with the original range
   quoted in `evidence_quote` and restated in `notes`. One value is a lower bound only (avidin
   `>1 mg/L`), recorded as 1 with `confidence=low`.
7. **Two deliberate duplicates.** `eggheme-2` restates Shao 2022's 3.5 g/L as read in an
   open-access third-party full text, and the paired quail-ovalbumin rows give the two ends of one
   clone range. Both say so in `notes`. De-duplicate on `doi`+`titer_mg_L` before fitting.
8. **Three derived productivity figures** (`volumetric_productivity_mg_L_h`) were computed by this
   extractor from titer ÷ stated duration, not taken from the papers; each is labelled DERIVED in
   `notes`. Every other productivity cell is `NA`.
9. **UniProt accessions** are confident for the egg-white proteins (P01012 ovalbumin, P02789
   ovotransferrin, P01005 ovomucoid, P02701 avidin, P00698 lysozyme, P01038 cystatin — the last four
   corroborated by the review's Table 1) and for myoglobins (P02189 porcine, P02192 bovine). The
   leghemoglobin assignment (P02237, Lbc2/LGB2) and VHb (P04252) are best guesses and are marked
   `uniprot_best_guess` in `notes`. Clover hemoglobin and quail ovalbumin are `NA`.
10. **Out-of-scope hosts were logged as papers, never as titer rows** — *K. marxianus* (7.27 g/L and
    10.1 g/L intracellular LegH, the highest leghemoglobin numbers anywhere), *B. subtilis*
    (0.82–1.11 g/L globins in 15 h), *C. glutamicum*, *Tremella fuciformis*, plant chloroplasts and
    cell-free systems. They are the right external benchmarks and several are open access, so they
    are the cheapest place to look next.
11. **Every DOI in both files was resolved from the Europe PMC record, not from memory.** A
    verification pass queried `EXT_ID:<pmid> AND SRC:MED` for all 54 PMIDs and overwrote the DOI
    field from the returned record. This **corrected 28 wrong DOIs** that had initially been
    inferred — including the BMC Biotechnol 2025 review, whose DOI is `10.1186/s12896-025-01002-3`
    (not the `…-01007-y` first written) and which is cited by 12 titer rows, and the Microb Cell
    Fact 2025 toolkit paper (`10.1186/s12934-025-02716-x`). Two identifiers could not be resolved
    and are therefore `NA`: Kojima et al. *Gene* 1994 (PMID 8206380, no DOI in Europe PMC) and the
    *Trends Food Sci Technol* 2023 soy leghemoglobin review (indexed with no DOI and no PMID).
    The EVERY Company patent row is `NA`/`NA` by nature. **Lesson for later batches: resolve DOIs
    from the index before writing them — a plausible-looking DOI is frequently wrong.**
