# Titer database extraction spec (v1)

All literature extraction writes **one TSV row per reported titer measurement** (not per paper).
File: `data/literature/titers_<batch>.tsv`. Header exactly as below, tab-separated, no quoting.

| column | meaning | rules |
|---|---|---|
| `record_id` | `<batch>-<n>` | unique within batch |
| `protein_name` | common name | e.g. `beta-lactoglobulin`, `bovine alpha-s1-casein` |
| `uniprot` | accession of the mature protein expressed | `NA` if not determinable; give best guess + note |
| `source_organism` | organism the gene came from | e.g. `Bos taurus`, `Glycine max` |
| `host_species` | expression host | `Komagataella phaffii`, `Trichoderma reesei`, `Saccharomyces cerevisiae`, ... |
| `host_strain` | strain if given | e.g. `GS115`, `X-33`, `CBS7435`, `QM9414` |
| `promoter` | e.g. `pAOX1`, `pGAP`, `pcbh1` | `NA` if unstated |
| `signal_peptide` | e.g. `alpha-MF`, `native`, `CBHI-carrier` | `NA` |
| `copy_number` | integer or `NA` | |
| `localisation` | `secreted` / `intracellular` | |
| `cultivation` | `shake_flask` / `fedbatch_bioreactor` / `batch_bioreactor` / `microscale` | |
| `carbon_source` | `glycerol`, `methanol`, `glycerol+methanol`, `glucose`, `lactose`, ... | |
| `titer_mg_L` | numeric, mg/L | convert g/L x1000; if a range, use the max and note it |
| `titer_basis` | `total_secreted_protein` / `target_protein_quantified` / `activity_inferred` | |
| `quantification` | `SDS-PAGE densitometry`, `ELISA`, `HPLC`, `BCA`, `LC-MS`, `heme assay`, ... |
| `volumetric_productivity_mg_L_h` | numeric or `NA` | |
| `year` | publication year |
| `doi` | DOI, or `NA` |
| `pmid` | PMID, or `NA` |
| `reference` | `FirstAuthor et al., Journal Year` |
| `evidence_quote` | <=240 chars, verbatim sentence containing the number |
| `confidence` | `high` (peer-reviewed, explicit number, clear units) / `medium` (inferred/derived) / `low` (preprint, company claim, abstract only) |
| `notes` | anything else material |

## Hard rules
1. **Never invent a number.** If a DOI/PMID can't be confirmed, set it `NA` and lower `confidence`.
2. `evidence_quote` must be text you actually read on the page you fetched. If you could only read an abstract, say so in `notes`.
3. Company press claims are allowed but must be `confidence=low` and `notes` must say `company_claim`.
4. Prefer **secreted, target-protein-quantified, bioreactor** rows; but record shake-flask rows too (they are usable with a cultivation covariate).
5. Record **every** independent titer in a paper (different strains/promoters/copy numbers = different rows).
6. Also write `data/literature/papers_<batch>.tsv` with: `doi`, `pmid`, `year`, `title`, `journal`, `url`, `relevance` (`titer`/`method`/`background`/`prior_art`), `one_line_finding`.
