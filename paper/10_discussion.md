# Chapter 9 — Discussion, limitations and what to do next

## 9.1 What was found

The thesis set out to decide, for a panel of food proteins in *Komagataella phaffii*, which of the field's named bottlenecks actually binds. Six findings answer that.

1. **The stoichiometric ceiling is nearly flat.** Maximum theoretical yields span 9.4% across the nine panel proteins on glycerol, and 1.31-fold across the 26 proteins of the wider validation set, with a log₁₀ standard deviation of 0.029. The carbon source moves the ceiling by about 30%, far more than the protein does.

2. **Phosphorylation is energetically free.** Thirteen phosphoserines on α-S2-casein cost 0.12% of yield. The casein problem is the absence of a Golgi casein kinase, not the price of a phosphate group — a catalytic problem with a catalytic solution.

3. **Glycosylation is the one expensive modification, and the metric matters.** Core N-glycosylation costs 8–9% of polypeptide yield in α-lactalbumin and lactoferrin. Under this host's native hypermannosylation that rises to 41% for a single-sequon protein, while the *mass* yield simultaneously improves. Reporting one number without the other inverts the conclusion.

4. **Published titres sit 12- to 7,573-fold below their own ceilings.** No process in the corpus exceeds 8.3% of its stoichiometric limit; the best food protein reaches 6.1%.

5. **The ceiling explains none of it.** Utilisation of the ceiling has a log₁₀ standard deviation of 0.851 against the ceiling's 0.029 — the outcome is about thirty times more dispersed than the bound — and maximum theoretical yield has no univariate association with titre (ρ = +0.062, p = 0.770).

6. **None of the seven pre-specified sequence features associates with titre** — the strongest is log length at ρ = +0.232, p = 0.265 — and a single indicator of whether the run was in a bioreactor outperforms all seven combined. An earlier draft reported disulfide density at ρ = −0.438, p = 0.036; re-reading disulfide counts from the UniProt feature tables removed it (§6.2.1).

7. **No feature outside the seven carries one either.** Mean predicted disorder was reported at ρ = −0.833 by an independent analysis and falls to ρ = −0.483, p = 0.117 once three faults in the underlying titre records are corrected. Its direction is consistent across every fit and it rests, in every version, on the contrast between κ-casein and everything else. It is carried forward as the thesis's leading untested hypothesis, not as a result, and Appendix F documents the episode.

Taken together: for food proteins in this host, **metabolism is not the binding constraint, and nothing measurable about the molecule explains the published record.** The property with the best claim to an exception, chain disorder, points away from synthesis and towards survival of the product once made — but the data cannot yet distinguish that from chance. Two things follow for anyone deciding where to spend. Do not spend on carbon efficiency: the ceiling is not what is binding, and it barely varies between proteins. Do spend on titre and recovery, which Chapter 8 shows are what the economics turn on.

The third thing — where to spend inside the secretory pathway — is the one this thesis cannot settle, and the disorder episode shows why it matters. Disorder is conventionally offered as a *folding* explanation for why caseins are hard. The decomposition says the opposite about cost: a disordered chain is metabolically cheap, carries no disulfides and no glycans, and κ-casein has one of the highest ceilings in the corpus while reaching 0.06% of it. If disorder does track the gap, what it plausibly tracks is proteolytic survival in a protease-rich supernatant rather than difficulty of folding, and the one intact κ-casein study reports exactly that failure. The two readings imply different spending — improve the folding machinery, or remove proteases and shorten residence time — and separating them is the most valuable experiment the thesis can name. §9.5 states it.

The secretory pathway remains the leading candidate for the residual, on three independent grounds: the stoichiometric model is structurally blind to it, the host literature responds to protein disulfide isomerase and unfolded-protein-response engineering, and the sources behind the lowest-utilisation records in the corpus report proteolysis and saturating copy-number responses rather than substrate limitation. None of those three is a measurement made here. Chapter 9's proposed successor analysis, a proteome-constrained secretory model, is the way to make one.

## 9.2 The honest status of the negative result

The most important sentence in Chapter 6 is that **all of the model's apparent skill is the process term**. The full model recovers 10.1% of the prediction error against a predict-the-mean baseline; the fed-batch indicator on its own recovers 15.9%; the seven sequence features on their own are 8.3% *worse* than predicting the mean. It would have been easy to report the full model's rank correlation alone (ρ = 0.543, p < 0.001) and call it a predictive model of producibility. That would have been misleading, and both the baseline and the nested controls were specified to prevent it.

The right reading is that **the published record of titres is dominated by engineering effort, not by protein identity**. β-lactoglobulin reaches twenty times more of its ceiling than human α-lactalbumin, two whey proteins of similar size and almost identical stoichiometric cost, and the difference between the studies is not the molecule: one had a commercial programme and omics-guided host rewiring behind it, the others a chaperone co-expression experiment and a study whose subject was CRISPR editing efficiency.

This has a consequence for the whole comparative literature. Statements of the form "protein X is more tractable than protein Y", when supported by titres from different papers, are weakly supported. Only within-study comparisons are clean, and there are few of them.

It also means the field's standard tractability ranking — whey easy, caseins and lactoferrin hard — is not confirmed here. α-lactalbumin, a canonical "easy" protein, sits near the bottom of the achievement table. The expectation was declared in Chapter 2 before the measurement, so the contradiction is reportable rather than embarrassing.

## 9.3 Limitations

These are ordered by how much they could change a conclusion.

**The model has no secretory machinery.** iMT1026v3 represents metabolism. It has no chaperones, no endoplasmic-reticulum volume, no translocon occupancy, no COPII throughput and no protein disulfide isomerase pool. This is a severe limitation and the most consequential one, because Chapter 6 concludes that the binding constraint lives exactly there. The thesis can show that metabolism does not explain the gap; it cannot, with this instrument, show what does. The disulfide association is evidence, not proof.

**Flux balance analysis predicts capability, not realisation.** Every ceiling here is an optimistic upper bound — the unconstrained growth rate of 0.674 h⁻¹ in §7.3 is itself two to three times the experimentally reported maximum. The gaps in Chapter 5 are therefore *lower bounds* on the true gap, which strengthens rather than weakens the central claim but should not be glossed over.

**Statistical controls do not validate records.** Appendix F documents a correlation that passed a permutation test, FDR correction across 32 features, a bootstrap interval and leave-one-out validation, on data containing an intracellular yield recorded as a secretion titre, a titre borrowed from another species through an orthologue-pooling join, and a carrier construct counted as its passenger. This thesis's own filter had let the same carrier record through. The controls in this thesis are therefore not offered as a guarantee of its numbers; the verbatim quotation attached to every record is, because that is what made the fault findable.

**Sample size.** Twenty-five proteins and 53 records, which is small for a seven-feature analysis and is the reason no feature is claimed. An earlier draft did claim one, disulfide density at p = 0.036, and §6.2.1 reports in full how re-measuring that one variable from the UniProt annotations removed it. The corpus would need to be several times larger, and to carry a measure of engineering effort, before a sequence feature could be distinguished from the process term that §6.4 shows carries all of the available signal.

**The titre corpus is not a random sample.** Publication bias, unequal effort, inconsistent reporting of whether a figure is product or total extracellular protein, and the impossibility of controlling for strain and process engineering all remain. Thirteen fragments and fusions were removed; some residual contamination of this kind is likely.

**The disorder hypothesis is under-tested where it would be decided.** Disorder is measured with metapredict v3, a current neural predictor, and it separates the panel cleanly, so the null is not an artefact of the instrument. But of the four caseins — the proteins the disorder hypothesis is really about — only κ-casein has a published titre in these hosts, and one protein is an anecdote rather than a test. α-S1-, α-S2- and β-casein remain the decisive missing measurements.

**The codon index is genome-wide, not expression-weighted.** Classical CAI needs a highly expressed reference set; only a whole-genome table was reachable. This compresses the differences between designs and is why no conclusion in this thesis rests on codon adaptation.

**Sequence provenance is indirect.** UniProt was unreachable from the analysis machine, so sequences were recovered from mirrors and accepted only on exact length and mass agreement with the UniProt record, or on two-repository consensus. Every panel protein passed, but direct re-verification against UniProt is a required pre-submission step.

**Citation integrity is an open task.** A verification pass found that inferred rather than resolved DOIs were wrong roughly half the time. Re-resolution of all 306 records against Crossref and Europe PMC is in progress and must complete before submission.

**No experimental work.** Nothing here has been measured in a vessel.

## 9.4 Where the analysis could be wrong

Three ways, stated so that a reader can look for them.

**If the substrate loading assumption is badly wrong**, the absolute gaps change — but only proportionally, and the dispersion of achievement is independent of loading entirely, since loading multiplies every ceiling equally. The central claim is safe; the specific fold-gaps are not precise.

**If the disulfide association is a confound**, the mechanistic conclusion weakens. Disulfide-rich proteins in this corpus are also disproportionately human therapeutic proteins, which may have been produced under different standards and for different purposes than food enzymes. A larger corpus with a therapeutic-versus-food indicator would separate the two, and this is the first analysis to run on the merged corpus when it lands.

**If the ceiling were not the right denominator** — for instance because real processes are oxygen-transfer-limited long before they are carbon-limited — the gap would be partly an artefact. This one has been checked and survives: §5.2.4 computes the oxygen-limited ceiling from the model's own oxygen demand of 9.4–10.2 mmol per gram of product and finds carbon to be the tighter bound in all 36 protein-by-transfer-rate combinations, with the tightest oxygen bound still 1.9-fold above the carbon bound. The check is generous to oxygen, so the conclusion is conservative. Nitrogen is a different matter and is reported in full in §5.2.4: at any batch nitrogen loading a fermentation is nitrogen-limited well before it is carbon-limited, and only continuous ammonia feeding — which every fed-batch process in the corpus uses for pH control — removes that bound. Since nitrogen content varies by just 1.10-fold across the panel against 1.31-fold for the carbon ceiling, the central contrast is unaffected by the substitution, but the absolute fractions in Table 5.1 would change substantially for a batch process. Phosphate and heat removal are now computed rather than deferred (§5.2.4). Phosphate binds only on the caseins and only below about 2 g of phosphorus per litre, far under the 7.3 g L⁻¹ that basal salts medium supplies — but it is the only bound in the thesis that varies strongly between proteins, twelve-fold against carbon's 1.31-fold, so it is the one place where protein identity changes the operative constraint instead of merely scaling it. Heat is the weakest of the four checks: the heat of product synthesis alone, 4.3–4.7 kJ per gram at 460 kJ per mole of oxygen, leaves carbon tighter in every case but by only 1.49-fold at 5 kW m⁻³, and the calculation excludes growth and maintenance respiration, which dominate total oxygen uptake in a high-cell-density fed-batch. It therefore overstates its own ceiling, and heat removal at scale stays an open question rather than a closed one.

## 9.5 What to do next, computationally

In priority order:

1. **Port the analysis to a proteome-constrained secretory model.** pcSecYeast already builds protein-specific secretion reactions with post-translational requirements and makes per-protein bottleneck calls. Running this panel through it would test Chapter 6's disulfide conclusion directly, with machinery rather than inference.
2. **Scan the remaining candidate bounds** — phosphate and heat removal — as oxygen and nitrogen have now been scanned (§5.2.4).
3. **Enlarge the corpus and re-run.** The merged database approaching 300 records, with resolved identifiers, roughly triples the sample and would let the disulfide association be tested properly, with multiple-testing control and a therapeutic-versus-food covariate.
4. **Replace FoldIndex with a modern disorder predictor** and re-test the disorder null.
5. **Rebuild the codon reference** from the coding sequences of the host's most highly expressed genes.
6. **Model glyco-engineered strains explicitly**, since Chapter 4 values the fix at up to 41% of polypeptide yield.

## 9.6 What to do next, experimentally

The analysis is dry, and it should say precisely what would make it wet. Four experiments, each small, each testing something this thesis predicts.

**Experiment 1 — the three missing casein numbers, which are also the test of this thesis's leading hypothesis.** Express intact bovine α-S1-, α-S2- and β-casein in *K. phaffii* in one strain background under one promoter and leader, and report fed-batch titres with phosphorylation state characterised by mass spectrometry. No number exists in the literature for any of the three, in any microbial host (§5.3).

This is first on the list for two reasons rather than one. It fills the largest hole in the public record for this field: the most commercially valuable class of food protein has no published quantitative titre. And it is the decisive test of the **disorder hypothesis**, which this thesis carries as its leading untested idea precisely because the evidence for it did not survive audit.

The hypothesis is specific enough to be falsified. *Ceiling utilisation falls as mean predicted chain disorder rises, within dairy, egg and haem proteins in K. phaffii.* The sign was negative in all eleven fits run across two independently curated rosters, at ρ between −0.43 and −0.61 after the data faults of Appendix F were corrected, with p between 0.06 and 0.29 — consistently in one direction and consistently indistinguishable from chance. The reason it cannot be settled on existing data is structural, not statistical: in every version of the corpus, exactly **one** protein above a mean disorder of 0.4 has a published titre, and that protein is κ-casein. No amount of further analysis of fourteen points, twelve of which are globular proteins spanning a mean disorder range of 0.06 to 0.16, will decide a hypothesis about disordered proteins.

The three missing caseins are, by the same predictor, the three most disordered proteins in the target class — α-S1 at 0.63, α-S2 at 0.58, β at 0.46 on the mature chain. They are therefore the four-point test the literature is missing, with κ-casein's 0.86 as the fourth. The predictions are:

- If disorder tracks utilisation, all three should land below κ-casein's 0.06% of ceiling, and β-casein, the least disordered of them, should be the highest of the three.
- If disorder does not, they should scatter across the range occupied by the globular proteins, and the consistent negative sign across eleven fits was a coincidence of one extreme point.
- Either outcome is informative, and both are obtainable from one strain background and three fermentations.

The hypothesis also carries a mechanistic prediction that the same experiment can test cheaply. Chapter 4 shows a disordered casein is metabolically *cheap* — no disulfides, no N-glycans, and phosphorylation that costs nothing measurable — and κ-casein has one of the highest ceilings in the corpus. So if disorder matters it should be acting on **proteolytic survival rather than on folding**: the product should appear in the supernatant as degradation fragments rather than failing to appear at all. Running each casein in a wild-type and a protease-deficient background, and quantifying intact product against fragments by mass spectrometry rather than total secreted mass, separates the two readings. The one published intact κ-casein study already reports proteolysis that *pep4* and *yps1* knockouts did not stop, which makes this the more probable of the two and still leaves it unmeasured.

**Experiment 2 — the kinase test.** Co-express a heterologous Golgi casein kinase (FAM20C, or the bacterial PrkD/YabT kinases already shown to phosphorylate α-S1-casein in *E. coli*) alongside the casein. Chapter 4 predicts that the carbon and energy cost of doing so is negligible, so if the kinase works, titre should be essentially unaffected while phosphorylation state changes. A measurable titre penalty would falsify the "phosphorylation is free" claim.

**Experiment 3 — the disulfide test.** Produce two proteins of similar length and comparable codon optimisation but very different disulfide density — α-lactalbumin (4 bonds in 123 residues) against β-casein (none) — in the same strain background, same promoter, same leader, same process. This was proposed when Chapter 6 reported a disulfide association; that association has since been withdrawn (§6.2.1), which makes the experiment more valuable rather than less. The published record cannot separate disulfide load from engineering effort because no two records in the corpus share a strain and a process. A matched pair in one background is the only way to test the hypothesis at all, and it is one fermentation pair.

**Experiment 4 — the glyco-engineering test.** Produce α-lactalbumin in a wild-type and in an outer-chain-deficient (*och1*) background and compare polypeptide yield per gram of substrate, not secreted mass. Chapter 4 predicts a difference of up to 41% in favour of the glyco-engineered strain on a protein basis, with the mass basis moving the other way. This also tests the methodological warning of §8.4.

## 9.7 Conclusion

The field describes its central problem as folding, modification and purification, and names them together. This thesis separated them and measured what it could.

Metabolism, which is the thing a genome-scale model is best at measuring, turned out not to be the answer: it costs essentially the same to build any of these proteins, phosphorylation costs nothing, and the economics barely notice carbon efficiency. What is left — folding, secretion, recovery, and the simple fact that most of these proteins have had very little engineering effort spent on them — is where the distance between 8% of a ceiling and 100% of it actually lies.

That is a smaller claim than the project began with, and a better supported one. The useful product of a dry-lab thesis is not a prediction that something will work. It is a defensible statement about where the remaining work is, and a list of experiments that would prove it wrong.
