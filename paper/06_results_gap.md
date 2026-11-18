# Chapter 5 — The gap between the ceiling and the record

Chapter 4 computed what metabolism permits. This chapter measures what has been achieved, and expresses the second as a fraction of the first. That ratio is the central quantity of this thesis.

## 5.1 Why the ratio is the right quantity

Published titres cannot be compared to one another directly. A gram per litre of a 15 kDa globin and a gram per litre of an 80 kDa glycoprotein are not the same achievement; a shake-flask result and a fed-batch bioreactor result differ by one to two orders of magnitude for reasons that have nothing to do with the protein; and a process fed 150 g L⁻¹ of substrate cannot be judged against one fed 500.

Dividing each titre by the ceiling of the very protein that was produced removes the first of these problems entirely and makes the third explicit as a scanned parameter. What remains — the fraction of its own stoichiometric limit that a process reached — is dimensionless, comparable, and bounded above by one.

## 5.2 The measurement

Applying the inclusion rules of §3.9 to the curated corpus gives 41 high-confidence records of secreted production in *K. phaffii*, *P. pastoris* or *T. reesei*, covering 24 distinct proteins for which a verified sequence was available. Thirteen records were excluded as fragments or fusions, for reasons §5.4 develops.

**Table 5.1 — Fraction of its own stoichiometric ceiling reached, at 350 g L⁻¹ substrate loading**

| Protein | Best titre (g L⁻¹) | *Y*<sub>max</sub> (g g⁻¹) | Ceiling (g L⁻¹) | % of ceiling | Gap |
|---|---|---|---|---|---|
| Human-like type III collagen | 19.40 | 0.668 | 234 | 8.30% | 12× |
| Human serum albumin | 17.47 | 0.662 | 232 | 7.54% | 13× |
| **β-lactoglobulin** | 13.88 | 0.653 | 229 | 6.07% | 16× |
| **Soy leghemoglobin** | 6.00 | 0.622 | 218 | 2.75% | 36× |
| *Candida antarctica* lipase B | 5.41 | 0.642 | 225 | 2.41% | 42× |
| Human GM-CSF | 4.30 | 0.567 | 199 | 2.17% | 46× |
| Type XVII human-like collagen | 4.70 | 0.658 | 230 | 2.04% | 49× |
| Hen egg white lysozyme | 3.50 | 0.683 | 239 | 1.46% | 68× |
| Human interferon α-2b | 2.40 | 0.656 | 230 | 1.05% | 96× |
| **Ovalbumin** (*T. reesei*) | 2.00 | 0.645 | 226 | 0.89% | 113× |
| **Human lactoferrin** | 1.35 | 0.642 | 225 | 0.60% | 167× |
| Brazzein | 1.30 | 0.697 | 244 | 0.53% | 188× |
| Hen ovomucoid | 0.93 | 0.506 | 177 | 0.52% | 191× |
| Human interleukin-6 | 0.28 | 0.597 | 209 | 0.13% | 746× |
| Porcine myoglobin | 0.29 | 0.650 | 227 | 0.13% | 797× |
| Human insulin precursor | 0.25 | 0.655 | 229 | 0.11% | 917× |
| **Bovine lactoferrin** | 0.23 | 0.616 | 216 | 0.11% | 927× |
| Human bFGF | 0.15 | 0.696 | 244 | 0.06% | 1,624× |
| **Human α-lactalbumin** | 0.11 | 0.597 | 209 | 0.05% | 1,844× |
| Human G-CSF | 0.10 | 0.646 | 226 | 0.04% | 2,262× |
| Human interleukin-15 | 0.07 | 0.540 | 189 | 0.04% | 2,521× |
| *T. reesei* hydrophobin HFBI | 0.09 | 0.677 | 237 | 0.04% | 2,736× |
| Human interferon λ-1 | 0.07 | 0.616 | 216 | 0.03% | 3,318× |
| Human serum transferrin | 0.03 | 0.649 | 227 | 0.01% | 7,573× |

Food proteins are shown in bold.

### 5.2.1 The headline contrast

Across these 24 proteins:

- the **stoichiometric ceiling spans 1.38-fold**, from 0.506 g g⁻¹ for hen ovomucoid to 0.697 for brazzein;
- the **fraction of that ceiling actually achieved spans 628-fold**, from 8.30% to 0.01%.

A quantity that varies by a factor of 1.4 cannot explain an outcome that varies by a factor of 628. This is the result the thesis exists to state, and it is robust to every assumption tested: it holds across the whole scanned range of substrate loading, across the translation-cost scan, and whether the product basis or the polypeptide basis is used.

### 5.2.2 Nobody is close to the ceiling

The best process in the entire corpus — a human-like collagen at 19.4 g L⁻¹ — reached **8.3%** of what the stoichiometry of its host permits. The best food protein, β-lactoglobulin at 13.88 g L⁻¹, reached 6.1%. This is worth stating plainly because the field's language sometimes suggests that titres are approaching a biological limit. They are not approaching it; they are one to four orders of magnitude away from it.

At a loading of 150 g L⁻¹ the β-lactoglobulin result rises to 14.2% of ceiling and at 500 g L⁻¹ it falls to 4.3%, so the conclusion is not an artefact of the central loading assumption: no plausible loading brings any published process within a factor of seven of its ceiling.

### 5.2.3 The ordering is not the expected one

Chapter 2 declared the expectation in advance: the published expert judgement is that whey proteins are the most tractable targets and caseins and lactoferrin the least. The measurement partly contradicts it.

β-lactoglobulin does indeed sit near the top. But **α-lactalbumin, the other "easy" whey protein, is close to the bottom** at 0.05% of its ceiling — below lactoferrin, below ovalbumin, below several cytokines. By stoichiometry it is an ordinary protein; by achievement it is among the worst in the corpus. Meanwhile soy leghemoglobin, which requires a cofactor the host must be engineered to supply, sits fourth.

Two readings are available and the data here cannot fully separate them. Either α-lactalbumin is genuinely difficult — four disulfides in 123 residues is the highest disulfide density of any food protein in the panel, and Chapter 6 finds disulfide density to be the one predictive feature — or it has simply received far less engineering effort than β-lactoglobulin, which has a commercial product behind it. Both are probably true. The second reading is developed in §6.5, where it becomes the chapter's main conclusion rather than a caveat.

## 5.3 The caseins: an absence that is a result

The caseins do not appear in Table 5.1, and that is the single most striking thing about it.

An earlier version of this analysis credited κ-casein with 1.02 g L⁻¹, placing it mid-table. That number came from a record for **bovine casein macropeptide**, the 64-residue glycopeptide that chymosin releases from κ-casein during coagulation. A strain secreting casein macropeptide has not secreted a casein; it has secreted about a third of one, without the part that matters. The error entered through a name-based join matching "casein" in both strings, and it inflated the caseins' apparent performance by a factor of nearly eight. It was caught by cross-checking against an independent analysis of the same corpus, and the corpus filter that now removes fragments, fusions, isolated domains and antibody fragments is shared between both pipelines so that neither can repeat it.

With the fragment removed, the finding is this: **no intact casein — α-S1, α-S2, β or κ — has a published volumetric titre in *K. phaffii* or *T. reesei*.** The systematic search found secretion demonstrated, constructs described and functional studies performed, but no number in grams or milligrams per litre from a peer-reviewed primary source in either host.

This is not a gap in the search; it is a gap in the literature, and it has three implications.

First, the most commercially valuable target in animal-free dairy — the protein class that makes cheese behave like cheese — is also the one with the least public quantitative data. Companies producing animal-free casein exist and have self-affirmed regulatory status, so the knowledge exists; it is simply not in the public record.

Second, any ranking of food proteins by tractability that places caseins last is, for these hosts, ranking them on an absence of data rather than on data. The published expert ordering may well be right, but it is not currently supported by a measurement.

Third, it tells a student or a company where the open ground is. A rigorous, published fed-batch titre for an intact casein in *K. phaffii*, with phosphorylation state characterised, would be a genuinely novel experimental contribution. It is the first item in the wet-laboratory programme proposed in Chapter 9.

## 5.4 What the exclusions remove, and why it matters

Thirteen records were excluded as fragments or fusions. The category matters because each exclusion is a case where a reported titre overstates what was achieved for the protein of interest:

- **Fragments** (casein macropeptide, lactoferricin, antimicrobial peptides excised from precursors) are shorter and structurally simpler than the parent, and are often produced precisely because the parent is difficult.
- **Fusions** (a SUMO-tagged holin, an sfGFP-tagged lipase at 5.1 g L⁻¹) report a titre that includes the partner's mass, and the partner is frequently chosen because it improves secretion.
- **Antibody fragments and isolated domains** (Fab, scFv, a viral receptor-binding domain) are engineered constructs, not natural proteins, and their sequence features belong to the construct rather than to anything in UniProt.

Including any of these inflates apparent performance. Excluding them costs sample size — 13 of 88 in-host high-confidence records — and the trade is worth making, but it is recorded here because a reader comparing this table against the raw corpus will find the difference.

## 5.5 What this chapter establishes

1. No published process for any protein in these hosts has reached more than 8.3% of its stoichiometric ceiling, and food proteins reach between 6.1% and 0.05%.
2. The ceiling varies by 1.38-fold while achievement varies by 628-fold, which excludes metabolic cost as the explanation of the ordering.
3. The published expert ordering of food proteins by tractability is partly contradicted: α-lactalbumin, a "tractable" whey protein, performs worse than lactoferrin and ovalbumin.
4. No intact casein has a published titre in either host, so the hardest and most valuable class in the panel is undocumented rather than documented as hard.

The gap is therefore real, large, and unexplained by anything computed so far. The next chapter asks what it tracks.
