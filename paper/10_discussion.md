# Chapter 9 — Discussion, limitations and what to do next

## 9.1 What was found

The thesis set out to decide, for a panel of food proteins in *Komagataella phaffii*, which of the field's named bottlenecks actually binds. Six findings answer that.

1. **The stoichiometric ceiling is nearly flat.** Maximum theoretical yields span 9.4% across the nine panel proteins on glycerol, and 1.38-fold across the 24 proteins of the wider validation set. The carbon source moves the ceiling by about 30%, far more than the protein does.

2. **Phosphorylation is energetically free.** Thirteen phosphoserines on α-S2-casein cost 0.12% of yield. The casein problem is the absence of a Golgi casein kinase, not the price of a phosphate group — a catalytic problem with a catalytic solution.

3. **Glycosylation is the one expensive modification, and the metric matters.** Core N-glycosylation costs 8–9% of polypeptide yield in α-lactalbumin and lactoferrin. Under this host's native hypermannosylation that rises to 41% for a single-sequon protein, while the *mass* yield simultaneously improves. Reporting one number without the other inverts the conclusion.

4. **Published titres sit 12- to 7,573-fold below their own ceilings.** No process in the corpus exceeds 8.3% of its stoichiometric limit; the best food protein reaches 6.1%.

5. **The ceiling explains none of it.** Achievement varies 628-fold while the ceiling varies 1.38-fold, and maximum theoretical yield has no univariate association with titre (ρ = +0.026, p = 0.907).

6. **Disulfide density is the only sequence feature that does associate** (ρ = −0.438, p = 0.036), and since disulfide formation is stoichiometrically almost free, the constraint it marks must lie in the oxidative folding machinery rather than in metabolism.

Taken together: for food proteins in this host, **metabolism is not the binding constraint, and the evidence points at the secretory pathway**. Three things follow for anyone deciding where to spend — do not spend on carbon efficiency; do spend on folding and secretion capacity, and on titre and recovery, which Chapter 8 shows are what the economics turn on.

## 9.2 The honest status of the negative result

The most important sentence in Chapter 6 is that the cross-validated model has **no skill** against predicting the mean. It would have been easy to report only the rank correlation (ρ = 0.370, p = 0.029) and call it a predictive model. That would have been misleading, and the baseline was pre-specified precisely to prevent it.

The right reading is that **the published record of titres is dominated by engineering effort, not by protein identity**. β-lactoglobulin reaches 120 times more of its ceiling than human α-lactalbumin, and the difference between the two studies is not mainly the molecule: one had a commercial programme and omics-guided host rewiring behind it, the other a chaperone co-expression experiment.

This has a consequence for the whole comparative literature. Statements of the form "protein X is more tractable than protein Y", when supported by titres from different papers, are weakly supported. Only within-study comparisons are clean, and there are few of them.

It also means the field's standard tractability ranking — whey easy, caseins and lactoferrin hard — is not confirmed here. α-lactalbumin, a canonical "easy" protein, sits near the bottom of the achievement table. The expectation was declared in Chapter 2 before the measurement, so the contradiction is reportable rather than embarrassing.

## 9.3 Limitations

These are ordered by how much they could change a conclusion.

**The model has no secretory machinery.** iMT1026v3 represents metabolism. It has no chaperones, no endoplasmic-reticulum volume, no translocon occupancy, no COPII throughput and no protein disulfide isomerase pool. This is a severe limitation and the most consequential one, because Chapter 6 concludes that the binding constraint lives exactly there. The thesis can show that metabolism does not explain the gap; it cannot, with this instrument, show what does. The disulfide association is evidence, not proof.

**Flux balance analysis predicts capability, not realisation.** Every ceiling here is an optimistic upper bound — the unconstrained growth rate of 0.674 h⁻¹ in §7.3 is itself two to three times the experimentally reported maximum. The gaps in Chapter 5 are therefore *lower bounds* on the true gap, which strengthens rather than weakens the central claim but should not be glossed over.

**Sample size.** Twenty-three proteins and 35 records. The disulfide association at p = 0.036 would not survive a strict multiple-testing correction across seven features (Bonferroni threshold 0.0071). It is reported as a single pre-specified association with a nominal p-value, it is consistent with independent mechanistic evidence from the host literature, and it is the kind of result that needs replication on a larger corpus rather than defence.

**The titre corpus is not a random sample.** Publication bias, unequal effort, inconsistent reporting of whether a figure is product or total extracellular protein, and the impossibility of controlling for strain and process engineering all remain. Thirteen fragments and fusions were removed; some residual contamination of this kind is likely.

**Disorder is measured weakly.** FoldIndex, not a modern neural predictor, because the environment could not install one. The disorder null is therefore a null about this measure on this set, and the caseins — the proteins the disorder hypothesis is really about — are absent from the set entirely.

**The codon index is genome-wide, not expression-weighted.** Classical CAI needs a highly expressed reference set; only a whole-genome table was reachable. This compresses the differences between designs and is why no conclusion in this thesis rests on codon adaptation.

**Sequence provenance is indirect.** UniProt was unreachable from the analysis machine, so sequences were recovered from mirrors and accepted only on exact length and mass agreement with the UniProt record, or on two-repository consensus. Every panel protein passed, but direct re-verification against UniProt is a required pre-submission step.

**Citation integrity is an open task.** A verification pass found that inferred rather than resolved DOIs were wrong roughly half the time. Re-resolution of all 306 records against Crossref and Europe PMC is in progress and must complete before submission.

**No experimental work.** Nothing here has been measured in a vessel.

## 9.4 Where the analysis could be wrong

Three ways, stated so that a reader can look for them.

**If the substrate loading assumption is badly wrong**, the absolute gaps change — but only proportionally, and the 628-fold spread in achievement is independent of loading entirely, since loading multiplies every ceiling equally. The central claim is safe; the specific fold-gaps are not precise.

**If the disulfide association is a confound**, the mechanistic conclusion weakens. Disulfide-rich proteins in this corpus are also disproportionately human therapeutic proteins, which may have been produced under different standards and for different purposes than food enzymes. A larger corpus with a therapeutic-versus-food indicator would separate the two, and this is the first analysis to run on the merged corpus when it lands.

**If the ceiling is not the right denominator** — for instance because real processes are oxygen-transfer-limited long before they are carbon-limited — then the gap is partly an artefact of comparing against the wrong bound. The oxygen demand computed in §4.1.3 (about 10 mmol O₂ per gram of protein, nearly invariant across proteins) is the quantity that would decide this, and computing an oxygen-limited ceiling alongside the carbon-limited one is a concrete and worthwhile extension.

## 9.5 What to do next, computationally

In priority order:

1. **Port the analysis to a proteome-constrained secretory model.** pcSecYeast already builds protein-specific secretion reactions with post-translational requirements and makes per-protein bottleneck calls. Running this panel through it would test Chapter 6's disulfide conclusion directly, with machinery rather than inference.
2. **Compute the oxygen-transfer-limited ceiling** alongside the carbon-limited one, and report the gap against whichever binds first.
3. **Enlarge the corpus and re-run.** The merged database approaching 300 records, with resolved identifiers, roughly triples the sample and would let the disulfide association be tested properly, with multiple-testing control and a therapeutic-versus-food covariate.
4. **Replace FoldIndex with a modern disorder predictor** and re-test the disorder null.
5. **Rebuild the codon reference** from the coding sequences of the host's most highly expressed genes.
6. **Model glyco-engineered strains explicitly**, since Chapter 4 values the fix at up to 41% of polypeptide yield.

## 9.6 What to do next, experimentally

The analysis is dry, and it should say precisely what would make it wet. Four experiments, each small, each testing something this thesis predicts.

**Experiment 1 — the missing casein number.** Express an intact bovine β-casein in *K. phaffii* under a constitutive promoter with the α-mating-factor leader, and report a fed-batch titre with phosphorylation state characterised by mass spectrometry. No such number exists in the literature (§5.3). Whatever it is, it is publishable, and it fills the largest hole in the public record for this field.

**Experiment 2 — the kinase test.** Co-express a heterologous Golgi casein kinase (FAM20C, or the bacterial PrkD/YabT kinases already shown to phosphorylate α-S1-casein in *E. coli*) alongside the casein. Chapter 4 predicts that the carbon and energy cost of doing so is negligible, so if the kinase works, titre should be essentially unaffected while phosphorylation state changes. A measurable titre penalty would falsify the "phosphorylation is free" claim.

**Experiment 3 — the disulfide test.** Produce two proteins of similar length and comparable codon optimisation but very different disulfide density — α-lactalbumin (4 bonds in 123 residues) against β-casein (none) — in the same strain background, same promoter, same leader, same process. Chapter 6 predicts a large titre difference attributable to folding rather than to metabolism. This is the single cleanest test of the thesis's main inference, and it is one fermentation pair.

**Experiment 4 — the glyco-engineering test.** Produce α-lactalbumin in a wild-type and in an outer-chain-deficient (*och1*) background and compare polypeptide yield per gram of substrate, not secreted mass. Chapter 4 predicts a difference of up to 41% in favour of the glyco-engineered strain on a protein basis, with the mass basis moving the other way. This also tests the methodological warning of §8.4.

## 9.7 Conclusion

The field describes its central problem as folding, modification and purification, and names them together. This thesis separated them and measured what it could.

Metabolism, which is the thing a genome-scale model is best at measuring, turned out not to be the answer: it costs essentially the same to build any of these proteins, phosphorylation costs nothing, and the economics barely notice carbon efficiency. What is left — folding, secretion, recovery, and the simple fact that most of these proteins have had very little engineering effort spent on them — is where the distance between 8% of a ceiling and 100% of it actually lies.

That is a smaller claim than the project began with, and a better supported one. The useful product of a dry-lab thesis is not a prediction that something will work. It is a defensible statement about where the remaining work is, and a list of experiments that would prove it wrong.
