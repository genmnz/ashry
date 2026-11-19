# Bibliography verification

Every entry in `bibliography_thread_f20slk.csv` (byte-identical to `bibliography.csv` on the paper branch) was checked against the DOI registries. First author, year, title and venue were re-derived from Crossref; the recorded value is preserved beside the registry value in `bibliography_verified.tsv`, so every change below is checkable against its row.

A Crossref 404 is not treated as proof that a DOI is wrong. Some prefixes are registered with other agencies, and four unresolvable rows in the titer corpus turned out to be live at doi.org. Every Crossref miss was therefore re-tried against the doi.org handle API, and only a DOI that failed at both is called `bad_doi`. Nothing was deleted.

Entries: 232

## Verdicts

- **ok**: 141
- **no_identifier**: 91

## Author lists filled from the registry (38)

These entries recorded no author list at all.

| entry | DOI | first author | year | venue |
|---|---|---|---|---|
| 61 | `10.1038/s41467-022-30689-7` | Li et al. | 2022 | Nature Communications |
| 63 | `10.1007/s11367-026-02765-3` | Quandt et al. | 2026 | The International Journal of Life Cycle Assessment |
| 64 | `10.5851/kosfa.2025.e33` | Purba et al. | 2025 | Food Science of Animal Resources |
| 68 | `10.1371/journal.pone.0079749` | Tian et al. | 2013 | PLoS ONE |
| 69 | `10.1371/journal.pcbi.1009461` | Bhandari et al. | 2021 | PLOS Computational Biology |
| 70 | `10.1073/pnas.2506036122` | Masson et al. | 2025 | Proceedings of the National Academy of Sciences |
| 71 | `10.1101/2022.12.02.518907` | Dunne et al. | 2022 | bioRxiv |
| 74 | `10.1038/s41598-022-15086-w` | Wollborn et al. | 2022 | Scientific Reports |
| 105 | `10.1007/s10930-025-10310-8` | Li et al. | 2025 | The Protein Journal |
| 106 | `10.1038/s41598-024-84066-z` | Yang et al. | 2025 | Scientific Reports |
| 111 | `10.1002/bit.70402` | Kocabaş | 2026 | Biotechnology and Bioengineering |
| 114 | `10.1186/s12934-024-02314-3` | Rebnegger et al. | 2024 | Microbial Cell Factories |
| 115 | `10.1186/s12934-026-03147-y` | Antón et al. | 2026 | Microbial Cell Factories |
| 116 | `10.1128/aem.00110-26` | Xin et al. | 2026 | Applied and Environmental Microbiology |
| 117 | `10.1186/s12934-026-03009-7` | Ford et al. | 2026 | Microbial Cell Factories |
| 121 | `10.1080/07388551.2024.2385996` | Xu et al. | 2025 | Critical Reviews in Biotechnology |
| 122 | `10.1186/s13068-016-0547-5` | Pakula et al. | 2016 | Biotechnology for Biofuels |
| 123 | `10.1038/s41598-019-41573-8` | Rantasalo et al. | 2019 | Scientific Reports |
| 127 | `10.1007/s00253-023-12660-8` | Liu et al. | 2023 | Applied Microbiology and Biotechnology |
| 137 | `10.1146/annurev-food-072023-034256` | Nielsen et al. | 2024 | Annual Review of Food Science and Technology |
| 154 | `10.1146/annurev-food-060424-091647` | Keppler et al. | 2026 | Annual Review of Food Science and Technology |
| 155 | `10.1021/acs.est.3c10312` | Jean et al. | 2024 | Environmental Science &amp; Technology |
| 158 | `10.1038/s41467-025-56364-1` | Fasihi et al. | 2025 | Nature Communications |
| 160 | `10.11648/j.bmb.20261101.11` | Le | 2026 | Biochemistry and Molecular Biology |
| 167 | `10.1186/s12934-021-01696-y` | Huang et al. | 2021 | Microbial Cell Factories |
| 168 | `10.1186/s12934-021-01580-9` | Xu et al. | 2021 | Microbial Cell Factories |
| 186 | `10.1371/journal.pone.0011935` | Barton et al. | 2010 | PLoS ONE |
| 188 | `10.1038/s41467-019-13867-y` | Gutierrez et al. | 2020 | Nature Communications |
| 190 | `10.1186/1475-2859-11-57` | Jordà et al. | 2012 | Microbial Cell Factories |
| 191 | `10.1186/1475-2859-11-83` | Carnicer et al. | 2012 | Microbial Cell Factories |
| 197 | `10.1073/pnas.2026658118` | Golinski et al. | 2021 | Proceedings of the National Academy of Sciences |
| 200 | `10.1007/s44462-026-00065-5` | Wang et al. | 2026 | Agricultural Products Processing and Storage |
| 203 | `10.1007/s00253-026-14051-1` | Mahmoud et al. | 2026 | Applied Microbiology and Biotechnology |
| 209 | `10.1016/j.biortech.2022.127884` | Shao et al. | 2022 | Bioresource Technology |
| 216 | `10.3390/foods15213817` | Usturoi et al. | 2026 | Foods |
| 223 | `10.1007/s00253-025-13482-6` | Lehmbeck et al. | 2025 | Applied Microbiology and Biotechnology |
| 226 | `10.3390/biom16111607` | Soceanu et al. | 2026 | Biomolecules |
| 230 | `10.3389/fimmu.2024.1380028` | Anaya et al. | 2024 | Frontiers in Immunology |

## Author corrections (11)

- entry 11 (`10.1186/s12934-025-02809-7`): "Buechner, K. et al." -> **"Büchner et al."**
- entry 16 (`10.1007/s00253-021-11336-5`): "Raschmanova, H. et al." -> **"Raschmanová et al."**
- entry 26 (`10.1016/j.ymben.2018.04.017`): "Pena, D.A. et al." -> **"Peña et al."**
- entry 30 (`10.1007/bf00311884`): "Nyyssoenen, E. et al." -> **"Nyyssönen et al."**
- entry 50 (`10.3168/jds.s0022-0302(95)76713-3`): "Perez, M.D. et al." -> **"Pérez et al."**
- entry 54 (`10.1111/1751-7915.12871`): "Tomas-Gamisans, M. et al." -> **"Tomàs‐Gamisans et al."**
- entry 84 (`10.1093/nar/gkab408`): "Erdos, G. et al." -> **"Erdős et al."**
- entry 104 (`10.1073/pnas.2304302120`): "Wang, J. et al." -> **"Alderson et al."**
- entry 165 (`10.1186/1471-2105-8-65`): "Conchillo-Sole, O. et al." -> **"Conchillo-Solé et al."**
- entry 184 (`10.15252/msb.20167411`): "Sanchez, B.J. et al." -> **"Sánchez et al."**
- entry 192 (`10.1002/biot.202300033`): "Russmayer, H. et al." -> **"Rußmayer et al."**

## Year corrections (12)

- entry 1 (`10.1007/978-1-0716-4779-0_19`): "2025" -> **"2026"**
- entry 20 (`10.1007/s00449-016-1701-y`): "2016" -> **"2017"**
- entry 40 (`10.1007/s00249-018-1330-2`): "2018" -> **"2019"**
- entry 52 (`10.1016/j.foodhyd.2020.106132`): "2020" -> **"2021"**
- entry 54 (`10.1111/1751-7915.12871`): "2017" -> **"2018"**
- entry 56 (`10.1002/bit.25863`): "2015" -> **"2016"**
- entry 101 (`10.1016/j.gpb.2022.06.004`): "2022" -> **"2023"**
- entry 103 (`10.1093/bioinformatics/bty715`): "2018" -> **"2019"**
- entry 104 (`10.1073/pnas.2304302120`): "2024" -> **"2023"**
- entry 106 (`10.1038/s41598-024-84066-z`): "2024" -> **"2025"**
- entry 121 (`10.1080/07388551.2024.2385996`): "2024" -> **"2025"**
- entry 154 (`10.1146/annurev-food-060424-091647`): "2025" -> **"2026"**

## Venue corrections (1)

- entry 200 (`10.1007/s44462-026-00065-5`): "Springer journal article" -> **"Agricultural Products Processing and Storage"**

## Title corrections (3)

- entry 22 (`10.1093/glycob/cwh104`): "Engineering of an artificial glycosylation pathway blocked in core oligosaccharide assembly in the yeast Pichia pastoris" -> **"Engineering of an artificial glycosylation pathway blocked in core oligosaccharide assembly in the yeast Pichia pastoris: production of complex humanized glycoproteins with terminal galactose"**
- entry 64 (`10.5851/kosfa.2025.e33`): "Biotechnology Approaches to Dairy Alternatives Through Precision Fermentation and Cellular Agriculture" -> **"Biotechnology in Dairy Alternatives: Current Perspectives on
                    Fermentation Technologies for Replacing Regular Milk with Artificial
                    Milk"**
- entry 71 (`10.1101/2022.12.02.518907`): "ExpressUrself: A spatial model for predicting recombinant protein expression" -> **"ExpressUrself: A spatial model for predicting recombinant expression from mRNA sequence"**

## DOIs flagged, not deleted (0)

- none

## DOIs suggested for entries that recorded none (45)

Found by a Crossref bibliographic-title query and accepted only where the normalised titles agree at 0.92 or better. These are suggestions, not edits: they are not written into the repaired file, because a title match is weaker evidence than a DOI.

| entry | suggested DOI | title similarity | first author | year | title as recorded |
|---|---|---|---|---|---|
| 58 | `10.1016/j.bej.2025.109940` | 1.0 | Kocabaş | 2026 | Modeling meets metabolic engineering: The iPichia consensus model as b |
| 59 | `10.1016/j.jprocont.2012.03.009` | 1.0 | Tortajada et al. | 2012 | Estimation of recombinant protein production in Pichia pastoris based  |
| 60 | `10.1073/pnas.062526999` | 0.964 | Akashi et al. | 2002 | Metabolic efficiency and amino acid composition in the proteomes of Es |
| 72 | `10.1016/j.compbiolchem.2021.107596` | 1.0 | Martiny et al. | 2021 | Deep protein representations enable recombinant protein expression pre |
| 73 | `10.1016/j.csbj.2022.06.006` | 0.988 | Packiam et al. | 2022 | PERISCOPE-Opt: Machine learning-based prediction of optimal fermentati |
| 113 | `10.1101/2023.09.04.556224` | 0.977 | Coltman et al. | 2023 | Characterising the metabolic rewiring of extremely slow growing Komaga |
| 118 | `10.1093/femsyr/foaf010` | 0.979 | Lv et al. | 2025 | Advancing recombinant protein expression in Komagataella phaffii: oppo |
| 119 | `10.1016/j.engmic.2026.100305` | 1.0 | Huang et al. | 2026 | Systematic optimization of Komagataella phaffii (Pichia pastoris) for  |
| 120 | `10.3390/metabo12040346` | 1.0 | Bustos et al. | 2022 | Advances in Cell Engineering of the Komagataella phaffii Platform for  |
| 125 | `10.1016/j.plasmid.2014.01.001` | 1.0 | Zhang et al. | 2014 | Enhanced production of heterologous proteins by the filamentous fungus |
| 126 | `10.1016/j.enzmictec.2022.109993` | 1.0 | Sun et al. | 2022 | Development of a novel expression platform for heterologous protein pr |
| 129 | `10.3390/ijms25031743` | 0.948 | Saenger et al. | 2024 | Structural Analysis of Breast-Milk alphaS1-Casein: An alpha-Helical Co |
| 130 | `10.3390/molecules28052023` | 1.0 | Runthala et al. | 2023 | Caseins: Versatility of Their Micellar Organization in Relation to the |
| 131 | `10.3390/biom15071031` | 1.0 | Mora Vásquez et al. | 2025 | Heterologous Caseins: The Role of Phosphorylation in Their Functionali |
| 132 | `10.1016/j.copbio.2022.102690` | 1.0 | Hettinga et al. | 2022 | Can recombinant milk proteins replace those produced by animals? |
| 134 | `10.1126/science.1217817` | 1.0 | Tagliabracci et al. | 2012 | Secreted kinase phosphorylates extracellular proteins that regulate bi |
| 136 | `10.1016/j.foodres.2022.112131` | 1.0 | Aro et al. | 2023 | Production of bovine beta-lactoglobulin and hen egg ovalbumin by Trich |
| 138 | `10.1186/s12896-025-01002-3` | 1.0 | Beck et al. | 2025 | Scientific and technological challenges of recombinant egg protein pro |
| 140 | `10.1016/j.ymben.2021.05.002` | 1.0 | Ishchuk et al. | 2021 | Improved production of human hemoglobin in yeast by engineering hemogl |
| 141 | `10.1016/j.ymben.2013.10.010` | 1.0 | Liu et al. | 2014 | Balanced globin protein expression and heme biosynthesis improve produ |
| 143 | `10.3389/fbioe.2023.1329016` | 1.0 | Tian et al. | 2024 | High-level expression of leghemoglobin in Kluyveromyces marxianus by r |
| 153 | `10.3390/fermentation10060315` | 1.0 | Knychala et al. | 2024 | Precision Fermentation as an Alternative to Animal Protein a Review |
| 156 | `10.3390/fermentation9080771` | 1.0 | Vlaeminck et al. | 2023 | Single-Cell Protein Production from Industrial Off-Gas through Acetate |
| 157 | `10.1016/j.cej.2026.180714` | 1.0 | Almeida Benalcázar et al. | 2026 | Techno-economic assessment of single-cell protein production at indust |
| 163 | `10.55277/researchhub.zto7x62j` | 0.943 | Zhang | 2026 | Addendum: Accurate structure prediction of biomolecular interactions w |
| 169 | `10.3390/jof11040282` | 1.0 | Lu et al. | 2025 | DNA Sequence Changes Resulting from Codon Optimization Affect Gene Exp |
| 170 | `10.1016/j.jbiotec.2021.11.001` | 1.0 | Liu et al. | 2022 | Strong negative correlation between codon usage bias and protein struc |
| 171 | `10.1016/j.csbj.2021.04.042` | 1.0 | Bahiri-Elitzur et al. | 2021 | Codon-based indices for modeling gene expression and transcript evolut |
| 174 | `10.1016/j.molmed.2014.09.003` | 1.0 | Mauro et al. | 2014 | A critical analysis of codon optimization in human therapeutics |
| 175 | `10.1016/s1046-5928(02)00526-0` | 1.0 | Sinclair et al. | 2002 | Synonymous codon usage bias and the expression of human glucocerebrosi |
| 180 | `10.1093/bioinformatics/bts426` | 1.0 | Chuang et al. | 2012 | Computational prediction of N-linked glycosylation incorporating struc |
| 189 | `10.1002/biot.201000078` | 0.972 | Sohn et al. | 2010 | Genome-scale metabolic model of methylotrophic yeast Pichia pastoris a |
| 194 | `10.1038/s41598-023-42865-w` | 1.0 | Pentjuss et al. | 2023 | Pichia pastoris growth-coupled heme biosynthesis analysis using metabo |
| 195 | `10.1007/s10295-014-1569-2` | 1.0 | Klein et al. | 2015 | Engineering the supply chain for protein production/secretion in yeast |
| 199 | `10.1002/jps.22758` | 1.0 | Lauer et al. | 2012 | Developability Index: A Rapid In Silico Tool for the Screening of Anti |
| 201 | `10.1016/j.tifs.2026.105871` | 1.0 | Hu et al. | 2026 | Engineering Trichoderma reesei into a programmable eukaryotic chassis  |
| 202 | `10.1016/j.tifs.2025.105488` | 1.0 | David et al. | 2026 | The role of techno-economic and life cycle assessment in guiding preci |
| 210 | `10.3389/fbioe.2023.1329016` | 1.0 | Tian et al. | 2024 | High-level expression of leghemoglobin in Kluyveromyces marxianus by r |
| 211 | `10.1016/j.tifs.2023.104199` | 1.0 | Ahmad et al. | 2023 | Soy Leghemoglobin: A review of its structure production safety aspects |
| 213 | `10.3390/pr11113215` | 1.0 | Bolmanis et al. | 2023 | Production and Purification of Soy Leghemoglobin from Pichia pastoris  |
| 215 | `10.3382/ps.2013-03391` | 1.0 | Abeyrathne et al. | 2013 | Egg White Proteins and Their Potential Use in Food Processing or as Nu |
| 222 | `10.5772/intechopen.1009019` | 1.0 | Ranjbar | 2025 | Precision Fermentation: The Path to Animal-Identical Dairy Solutions |
| 228 | `10.1038/s41598-026-38965-y` | 0.976 | Ehsasatvatan et al. | 2026 | Transplastomic biofactory for the production of functional human alpha |
| 229 | `10.1021/acs.jafc.1c07908.s001` | 1.0 |  | 2022 | Efficient Bioproduction of Human Milk Alpha-Lactalbumin in Komagataell |
| 232 | `10.5772/64187` | 1.0 | Bhat et al. | 2016 | Casein Proteins: Structural and Functional Aspects |

## Files

- `bibliography_verified.tsv` - one row per entry, recorded and registry values side by side, with the verdict.
- `bibliography_repaired.csv` - the input file with authors, years, venues and titles replaced by the registry values where they differed. Same columns as the input, so it can be dropped in place of `bibliography.csv`. Suggested DOIs are deliberately NOT written here.

