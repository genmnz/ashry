# Batch `kpdairy` — milk/dairy protein expression in yeast and fungal hosts

Scope: every published report of milk/dairy protein expression in *Komagataella phaffii*
(*Pichia pastoris*) and other yeasts (*S. cerevisiae*, *Kluyveromyces lactis/marxianus*,
*Yarrowia lipolytica*, *Hansenula/Ogataea*), plus filamentous-fungal hosts where they set the
benchmark (*Trichoderma reesei*, *Aspergillus* spp.). Target proteins: the four caseins,
β-lactoglobulin, α-lactalbumin, lactoferrin, lactoperoxidase, osteopontin, milk lysozyme,
caseinomacropeptide, and serum albumin as a dairy-adjacent secretion benchmark.

Output files:
- `titers_kpdairy.tsv` — 54 titer rows, 10 distinct protein entries, 10 distinct hosts
- `papers_kpdairy.tsv` — 79 papers logged (40 `titer`, 18 `method`, 12 `background`, 9 `prior_art`)

## What was searched

### Europe PMC REST API (`/search`, `/fullTextXML`)
Three sweeps, 34 distinct structured queries. First sweep (broad, free-text):
`("Pichia pastoris" OR Komagataella) AND <protein>` for β-lactoglobulin (44 hits),
α-lactalbumin (35), lactoferrin (309), casein (754), lactoperoxidase (41), osteopontin (79),
serum albumin (2702), plus host-specific sweeps for *K. lactis* (418), *S. cerevisiae* (7275),
*Y. lipolytica* (911), *Hansenula/Ogataea* (462), *K. marxianus* (298), `"precision fermentation"
AND (casein OR whey OR "milk protein")` (217), `"milk protein" AND Pichia/Komagataella` (95),
and lysozyme + milk/human (825).

Second sweep (`TITLE_ABS:` field-restricted, 11 queries) returned **1316 screened records** in
`screen.txt`; third sweep (8 gap-filling queries, caseins/LPO/OPN/HSA/animal-free/CMP) returned
several hundred more. A fourth targeted sweep covered human lysozyme in yeast (62 hits) and
β-lactoglobulin/α-lactalbumin 2015–2026 (11 hits).

Total records screened by title/abstract: **well over 1,500**; ~110 were pulled as full
abstracts via NCBI E-utilities `efetch` (4 batches), and 8 open-access papers were mined as
full text via Europe PMC `fullTextXML`.

### Open-access full texts actually mined
- `PMC13735683` — Iaria et al. 2026, κ-casein in *P. pastoris* (the only κ-casein titer series
  in the literature; copy-number, bioreactor and LC-MS/MS numbers all came from the body text,
  not the abstract)
- `PMC4926436` — Iglesias-Figueroa et al. 2016, bovine lactoferrin in *P. pastoris*
- `PMC10855427` — Yen et al. 2024, porcine lactoferrin, glucose-inducible PG1 promoter
- `PMC11184742` — Zhong et al. 2024, human lysozyme in *K. phaffii*
- `PMC11993488` — mycotoxin-free *A. oryzae* lineage (no titers; GRAS context only)
- `PMC1217000`, `PMC10528908`, `PMC9652177`, `PMC10155391` — requested but returned empty or
  unhelpful XML from Europe PMC (see "could not access")

### WebSearch / WebFetch
Six extended web searches (lactoperoxidase in yeast/fungi; β-casein in *K. phaffii*;
αs1-casein in *Pichia*; human lysozyme in *K. lactis*/*Pichia*; osteopontin in *K. phaffii*;
β-lactoglobulin engineering 2025–2026). These surfaced three papers that Europe PMC indexing
missed entirely and that supply two of the most important numbers in the batch:
- Yao et al. 2026, *Food Bioscience* — **13.88 g/L β-lactoglobulin in *K. phaffii***
- Zhang et al. 2024, *Future Foods* — **35.6 / 128.5 mg/L human milk osteopontin in *K. phaffii***
- Nielsen et al. 2026, *Industrial Biotechnology* — *A. oryzae* β-LG DoE (relative values only)

### UniProt REST
Every `uniprot` field was verified against `rest.uniprot.org` rather than written from memory.
Confirmed: P02754 (bovine β-LG), P67976 (ovine β-LG), P00711/P00712/P00709 (bovine/goat/human
α-LA), P02668 (bovine κ-casein), P02666 (bovine β-casein), P02662 (bovine αs1-casein),
P07498 (human κ-casein), P02788/P24627/P14632/O77811/Q29477 (human/bovine/porcine/equine/goat
lactoferrin), P02768 (HSA), P61626 (human lysozyme C), P10451 (human osteopontin),
P80025 (bovine lactoperoxidase). Set to `NA` where no reviewed entry exists: Tibetan sheep
lactoferrin, yak lactoferrin (only unreviewed *Bos grunniens* entries, e.g. A0A8B9XC45).

## Highest-confidence titer per protein

| protein | best titer | host / mode | reference | confidence |
|---|---|---|---|---|
| β-lactoglobulin | **13,880 mg/L** | *K. phaffii*, bioreactor, methanol-free | Yao et al., Food Bioscience 2026 | high |
| α-lactalbumin (human) | **600 mg/L** | *K. phaffii*, 3 L bioreactor, ethanol-inducible | Wang et al., JAFC 2025 | high |
| κ-casein (bovine, intact) | **133 mg/L** | *K. phaffii* X-33, 17 copies, shake flask | Iaria et al., Front Bioeng Biotechnol 2026 | high |
| casein macropeptide (bovine) | **1,020 mg/L** | *K. phaffii*, engineered pAOX1 | Qu et al., Chin J Biotechnol 2026 | medium |
| caseinomacropeptide (human) | **2,500 mg/L** | *S. cerevisiae*, fed-batch bioreactor | Kim et al., JIMB 2005 | high |
| lactoferrin | **3,140 mg/L** (human, *Y. lipolytica*, 5 L fed-batch) | — also 2,214 mg/L hLF in *K. phaffii* and 2,800 mg/L porcine LF in *K. phaffii* | Wu et al., Bioresour Technol 2026 | high |
| milk lysozyme (human) | **4,120 mg/L** | *K. phaffii* Δ*myo1*, fed-batch | Zhong et al., Microb Cell Fact 2024 | high (but *total* secreted protein) |
| osteopontin (human milk) | **128.5 mg/L** | *K. phaffii* X33 XPSA01-CP, 3 L bioreactor | Zhang et al., Future Foods 2024 | high |
| serum albumin (benchmark) | **17,470 mg/L** | *K. phaffii*, 192 h induction | Zhu et al., Protein Expr Purif 2021 | high |
| lactoperoxidase | **no yeast/fungal titer exists** | — | — | — |

Note: the single highest *bovine* lactoferrin number (3,500 mg/L, Iglesias-Figueroa 2016) is
recorded at `confidence=medium` because the sentence containing it mentions cell lysis, so it
may not be a purely secreted titer. The highest clean secreted lactoferrin numbers are
3,140 mg/L (hLF, *Y. lipolytica*) and 2,800 mg/L (porcine LF, *K. phaffii*).

## Coverage gaps

1. **Lactoperoxidase — total gap.** Exhaustive searching found no recombinant LPO production in
   any yeast or filamentous fungus. The only recombinant LPO work is in baculovirus/insect cells
   (PMID 14586116) and non-yeast systems for heme-environment studies (PMID 9891994), plus two
   unindexed patent records titled "Recombinant production of lactoperoxidase" (1991, 1992, 1998)
   whose text I could not retrieve. LPO needs a covalently-matured heme prosthetic group, which
   is the likely reason. **This is a genuine white space for the thesis, not a search failure.**
2. **αs1-casein and αs2-casein in yeast — no titers published.** All αs1-casein production
   numbers are in bacteria (*E. coli* with co-expressed kinases, PMID 40610262; *B. subtilis*,
   doi 10.3390/microorganisms13010060 — both outside this batch's host scope). Papers that
   *use* recombinant αs1-casein (foaming, PMID 41722421; in vivo, PMID 42878146) never state the
   host or the titer. αs2-casein appears nowhere in a yeast expression context.
3. **β-casein in yeast — no titer.** Choi & Jiménez-Flores 2001 (PMID 11308323) expressed and
   purified glycosylated bovine β-casein (L70S/P71S) in *P. pastoris* and is the key precedent
   (it even reports native-level phosphorylation), but gives no mg/L. The Iaria 2026 κ-casein
   paper refers to companion β-casein work "to be published". There is also a 1990 JAFC paper on
   bovine β-casein in *S. cerevisiae* (doi 10.1021/jf00094a049) with no PMID that I could not open.
4. **Intact κ-casein titers are tens of mg/L only** — the Iaria 2026 paper is the only source,
   and its own conclusion is that secretion efficiency, proteolysis and O-glycosylation cap it.
5. **No company titers recorded.** Perfect Day, Vivici, Remilk, Imagindairy, New Culture,
   TurtleTree and Onego all have GRAS filings, but none publishes a g/L number. The published
   company-affiliated papers (TurtleTree bLf PMID 39298790; Vivici β-LG PMID 42914272) are
   comparability/structure studies with no production data, so they are logged as `background`
   with no titer row. No `company_claim` rows were created because no defensible number was found.
6. **Quantification method is often unstated.** For ~12 rows the field reads "not stated in
   abstract" because the publisher page is paywalled. Where a method is named in the abstract or
   full text (ELISA, densitometry, LC-MS/MS, purification yield) it is recorded.
7. **Bovine α-lactalbumin in *K. phaffii*** — no titer found. Only *S. cerevisiae* precedents
   (1990, 1991) exist and neither reports mg/L; all quantitative α-LA work is on the *human* protein.
8. **Immunoglobulin-free whey components beyond β-LG/α-LA** (serum albumin aside) are unrepresented;
   no yeast expression reports were found for e.g. bovine serum albumin itself.

## Papers I could not access

- `10.1111/1541-4337.70618` (PMID 42634117) — *Toward Rational Design of Precision-Fermented
  Milk Proteins*, Compr Rev Food Sci Food Saf 2026. Marked not-open-access in Europe PMC; the
  PMC HTML returned a reCAPTCHA interstitial. Its collated titer tables could not be mined.
  **Highest-value missing source in this batch.**
- `10.1016/j.fbio.2026.109383` (Yao 2026, 13.88 g/L β-LG) — abstract/landing page only.
  Strain designation, working volume, quantification method and the full titer series are behind
  the paywall. The 13,880 mg/L row therefore has several `NA`/"not stated" fields.
- `10.1016/j.fufo.2024.100393` (Zhang 2024, hOPN) — intermediate titers (340.5 µg/L host
  screening; 11.3/15.4/15.2/20.5/23.6 mg/L for AFT1, GAL4-like, BCY1, PAB1, CPR5 steps) are
  reported in the body text, which I read only as a fetched summary rather than verbatim, so only
  the two numbers I have verbatim clauses for (35.6 and 128.5 mg/L) became rows.
- Europe PMC `fullTextXML` returned 150-byte empty responses for `PMC1217000` (Rocha 1996 ovine
  β-LG), `PMC10528908` (bgs13/β-LG), `PMC9652177` (β-LG immunogenicity) — abstracts used instead.
- `10.1046/j.1365-2621.1999.00317.x` — "Expression of recombinant wild-type and mutant
  beta-lactoglobulins in the yeast Pichia pastoris", Int J Food Sci Technol 1999. No PMID, no
  accessible text; likely contains additional BLG yields.
- `10.1021/jf00094a049` — bovine β-casein in *S. cerevisiae*, JAFC 1990. No PMID, inaccessible.
- PMID 15340513 (human LF, high-density *P. pastoris*) and PMID 42343796 (bovine CMP promoter
  engineering) are Chinese-language; only the English abstracts were available, so their rows are
  `confidence=medium`.
- Nielsen et al. 2026 (*A. oryzae* β-LG, doi 10.1177/15509087251398318) publishes **relative**
  product amounts only (100% centre point → 179% optimised). No absolute titer exists to extract,
  so no row was created despite it being directly on-topic.

## Methodological caveats for downstream use

- **Four rows are lower bounds** (`>1 g/L` BLG, `>2 g/L` hLF in *A. awamori*, `>60 mg/L` sheep
  LF, and `in excess of 2 g/l`). Treat them as censored data, not point estimates.
- **Three rows report a range** and the spec's max rule was applied: ovine β-LG 40–50 → 50;
  *S. cerevisiae* β-LG 3–4 → 4; *K. marxianus* rHSA 2.32–2.37 → 2.37 g/L. Noted in each row.
- **Basis differs and matters.** Three lysozyme rows and one *K. phaffii* lysozyme fed-batch row
  are `total_secreted_protein`, not target-specific; they are upper bounds on the true titer.
  Many lysozyme papers report only U/mL and were logged as papers with no titer row.
- **Volumetric productivities marked "derived by me"** in the notes column were computed by
  dividing the stated titer by the stated induction/fermentation time. They are arithmetic, not
  quotes. Nine rows have them; all others are `NA`.
- **One internally inconsistent published number** is recorded verbatim and flagged:
  Blondeau 1994 (*K. lactis* chemostat) states 75 mg/L/h productivity alongside 62 mg/L at
  D = 0.12 h⁻¹, which implies ~7.4 mg/L/h. Row is `confidence=low` with the discrepancy noted.
- **Chemostat/continuous cultivation has no spec vocabulary term**; the one such row uses
  `batch_bioreactor` with an explicit note. If the schema gains a `chemostat` value, that row
  should be re-coded.
- **Non-ASCII characters were transliterated** in `evidence_quote` fields to keep the TSV clean:
  `mg·L-1` → `mg*L-1`, `µg/mL` → `micrograms/mL`, `±` → `+/-`, Greek letters spelled out.
  The numbers and wording are otherwise verbatim from text I read.
- **Serum albumin rows are benchmarks, not dairy proteins.** Thirteen of the 54 rows are HSA.
  They were included per scope as a secretion-capacity ceiling for a large, disulfide-rich
  secreted protein, and should be excluded from any dairy-protein-only analysis.
- **Casein rows skew to fragments.** Of six casein-family rows, four are intact bovine κ-casein
  (tens of mg/L) and two are macropeptide fragments (1.0–2.5 g/L). The fragment titers are *not*
  evidence that intact casein is producible at g/L scale — CMP is a short, glycosylated,
  non-micelle-forming peptide.
