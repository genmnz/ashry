# Precision Fermentation: Microbial Cell Factories for Animal-Free Dairy, Heme and Alternative Proteins

### Why do proteins with nearly identical stoichiometric ceilings reach such different titres? A ceiling–utilisation decomposition for food proteins in *Komagataella phaffii*

**التخمير الدقيق: مصانع خلوية ميكروبية لإنتاج بروتينات الألبان والهيم والبروتينات البديلة دون الحاجة إلى الحيوانات**

*Graduation research project*

---

## Abstract

Precision fermentation — programming a microorganism by recombinant DNA to secrete a protein that an animal would otherwise have made — has moved from laboratory demonstration to supermarket shelf in under a decade. Bovine β-lactoglobulin from *Trichoderma reesei* and soy leghemoglobin from *Komagataella phaffii* are both cleared for sale in the United States. Yet the field's own framing of its central problem has remained qualitative: proteins are said to be hard to make because they fold poorly, because they require post-translational modifications the host cannot perform, or because purification is expensive. These claims are rarely quantified, and they are almost never compared against each other on a common scale.

This work asks a narrower and answerable question: **for a panel of nine food proteins, what does each candidate bottleneck actually cost, and which of them is binding?** The analysis is entirely computational and entirely reproducible from the accompanying repository.

Three things are established. First, the stoichiometric ceiling is nearly flat across the panel. Maximum theoretical yields computed by installing explicit, sequence-derived synthesis and secretion reactions into the genome-scale metabolic model iMT1026v3 of *K. phaffii* span only about 9% between the cheapest and the most expensive of the four caseins, β-lactoglobulin, α-lactalbumin, ovalbumin, soy leghemoglobin C2 and bovine lactoferrin, while the choice of carbon source moves the ceiling by roughly 30%. Within the post-translational load, phosphorylation is energetically free — charging α-S2-casein's thirteen phosphoserines costs under 0.12% of yield — whereas N-glycosylation is expensive and becomes dominant under the hypermannosylation that *K. phaffii* performs natively.

Second, realised production is nowhere near that ceiling. Joining the model-derived ceilings to a purpose-built database of **306 published titres**, each carrying a verbatim evidential quotation, a resolved identifier and a confidence grade, gives 75 high-confidence records of secreted production over 26 proteins whose sequences were verified by checksum against UniProtKB. Expressing each titre as a fraction of *its own* protein's ceiling: the ceiling has a log₁₀ standard deviation of **0.029** while utilisation of it has a log₁₀ standard deviation of **0.851**, with a median of 0.40% and an interquartile range of 0.07% to 2.1%. **The outcome is about thirty times more dispersed than the bound.** The best process in the corpus reached 8.0% of its ceiling and the median reached a four-hundredth of it. Metabolic cost is therefore excluded as the explanation of why some food proteins are harder to make than others, and the exclusion rests on the shape of a distribution rather than on a ratio between two records.

Third, and the answer to the question the thesis asks: **about half the dispersion in realised production is reproduced within single proteins.** Joining every qualifying record to its ceiling on the UniProt accession rather than on a protein name lets one protein appear as many times as it has been published, and once it can, the mean log₁₀ spread *inside* a single protein is 0.638 against 0.892 across the whole 88-record corpus. Hen ovalbumin spans 200-fold across four records; κ-casein spans 102-fold across five; human α-lactalbumin 115-fold across six. A crossed random-effects model over 88 records, 30 proteins and 52 studies places 44% of the variance between proteins, 16% between studies of the same protein and 40% within studies, and adding the seven sequence features halves the between-protein component without touching the residual — the signature of regressors absorbing protein identity rather than predicting from it. Cultivation mode is the one large and unambiguous effect: a shake flask costs a factor of five against a batch bioreactor (*p* = 0.002). Since half the dispersion occurs where the sequence does not vary at all, **no sequence-derived quantity can account for it**, and this is reported as an association and a negative result about method rather than as an identification of any mechanism.

Fourth, a direct test of what does explain it, which returns a null consistent with the above. Across 53 high-confidence records of secreted production in *K. phaffii* covering 25 distinct proteins, with seven mechanistic sequence features specified in advance, **no feature is associated with titre**: maximum theoretical yield at ρ = +0.06, disulfide density at ρ = −0.19, predicted disorder at ρ = −0.01, nothing reaching an uncorrected p of 0.05 let alone a corrected one. An earlier version of this work reported disulfide density as a significant association; re-reading disulfide counts from the UniProt feature tables instead of assuming that cysteines pair — an assumption wrong for 15 of 36 proteins — removed it, and the thesis reports that decomposition rather than the finding. Cross-validated against two nested controls, a single indicator of whether the run was in a bioreactor recovers 15.9% of the prediction error against a predict-the-mean baseline, adding the seven sequence features *reduces* that to 10.1%, and the sequence features alone are 8.3% worse than predicting the mean. The signal in the published record is overwhelmingly in the experiment rather than in the protein: **published titres are largely a record of how much engineering each protein has received rather than of how hard each protein is.**

Two candidate positive findings arose during this work and neither survived audit, which is reported rather than concealed. The second is documented at length in Appendix F because of what it demonstrates: a correlation between mean predicted disorder and ceiling utilisation, reported at ρ = −0.833 with a permutation p of 0.00025, FDR control across 32 features and a leave-one-out check that held throughout, fell to ρ = −0.483, p = 0.117 once three faults in the underlying titre records were corrected — an intracellular yield recorded as a secretion titre, a best-titre join that pooled orthologues so that one protein borrowed another species' number, and a carrier construct counted as its passenger. **Four statistical controls that are normally treated as sufficient all passed on data that did not mean what its column headings said.** The direction of the disorder effect is consistent across every fit and the thesis treats it as an untested hypothesis, naming the measurement that would decide it: titres for α-S1-, α-S2- and β-casein, the three most disordered proteins in the target class and the three with no published number in any microbial host.

The practical consequences are developed in two further chapters: protein-specific metabolic engineering targets obtained by flux scanning with enforced objective function, and a techno-economic model in which every parameter carries a source and the result is reported against the stoichiometric cost floor implied by the computed yields. The cost analysis finds a floor near $1/kg of raw carbon against a modelled plant cost near $43/kg, and identifies recovery, titre and plant utilisation — not substrate price — as what determines whether precision-fermented proteins reach commodity economics.

The contribution of this thesis is not a new protein, a new strain or a new tool, and it is deliberately narrower than it first appears. Computing per-protein synthesis costs in a genome-scale model is not new: Feizi and co-workers did it across the yeast proteome in 2013, Gutierrez and co-workers reconstructed the mammalian secretory pathway and its per-protein costs in 2020, and pcSecYeast built protein-specific secretion reactions with per-protein bottleneck calls in 2022. Predicting producibility from sequence is not new either. Those steps are used here, with citation, as tools rather than claimed as findings.

What is new is the **decomposition**: computing each food protein's own stoichiometric ceiling, expressing every published titre as a fraction of *its own* ceiling rather than comparing titres to each other, and attributing the residual. That measurement has not been made for these proteins in these hosts, and it is what licenses the central claim — that the binding constraint on animal-free food proteins is not what it costs the cell to build them.

The decomposition's sharpest single application is to the commercially most important target. Intact bovine κ-casein, whose first published titres in *K. phaffii* appeared during this work at 28–133 mg L⁻¹, has one of the **highest** stoichiometric ceilings in the corpus and the lowest utilisation of it: it is metabolically cheap to build, carrying no glycans, no appreciable disulfide load and phosphorylation that costs nothing measurable, and it reaches 0.06% of what its host's stoichiometry permits. The casein problem is not a cost problem.

---

## ملخص

التخمير الدقيق هو برمجة الكائنات الدقيقة باستخدام تقنية الحمض النووي المؤتلف لإنتاج بروتينات حيوانية المنشأ دون الحاجة إلى الحيوان نفسه. انتقلت هذه التقنية خلال أقل من عقد من المختبر إلى الأسواق، إذ حصل بروتين بيتا لاكتوغلوبولين المنتج من الفطر *Trichoderma reesei* وبروتين الليغهيموغلوبين المنتج من الخميرة *Komagataella phaffii* على موافقات تنظيمية في الولايات المتحدة.

ومع ذلك، ظل وصف التحدي الأساسي في هذا المجال وصفاً نوعياً لا كمياً: يقال إن بعض البروتينات صعبة الإنتاج بسبب الطي البروتيني غير الصحيح، أو بسبب التعديلات بعد الترجمة التي لا يستطيع المضيف الميكروبي إجراءها، أو بسبب كلفة التنقية. هذه الادعاءات نادراً ما تُقاس، ونادراً ما تُقارن على مقياس واحد.

تطرح هذه الدراسة سؤالاً أضيق وقابلاً للإجابة: ما هي الكلفة الفعلية لكل عائق مفترض، وأيها هو العائق الحقيقي المُقيِّد؟ الدراسة حاسوبية بالكامل وقابلة للتكرار بالكامل.

توصلت الدراسة إلى ثلاث نتائج رئيسية. الأولى أن السقف الكيميائي الحيوي شبه ثابت: لا تتجاوز الفروق في العائد النظري الأقصى بين البروتينات التسعة نحو 9%، بينما يغيّر مصدر الكربون العائد بنحو 30%. كما تبيّن أن الفسفرة لا تكلف الخلية طاقياً تقريباً، في حين أن الغلكزة مكلفة، وتصبح العائق الأكبر عند حدوث فرط المَنَزة المميز لهذه الخميرة.

الثانية أن الإنتاج الفعلي أبعد ما يكون عن ذلك السقف. بعد بناء قاعدة بيانات من 306 سجلات منشورة، يحمل كل سجل منها اقتباساً نصياً حرفياً ومعرِّفاً رقمياً مُتحقَّقاً منه، أمكن التعبير عن 75 سجلاً عالي الثقة تغطي 26 بروتيناً كنسبة من سقف البروتين نفسه. الانحراف المعياري اللوغاريتمي للسقف هو 0.029، بينما الانحراف المعياري اللوغاريتمي لنسبة الاستفادة منه هو 0.851، بوسيط 0.40% ومدى ربيعي من 0.07% إلى 2.1%. أي أن التشتت في النتيجة يبلغ نحو ثلاثين ضعف التشتت في الحد الأقصى. أفضل عملية في القاعدة بلغت 8.0% من سقفها فقط.

الثالثة، وهي الإجابة المباشرة على سؤال هذه الدراسة: نحو نصف التشتت في الإنتاج الفعلي يتكرر داخل البروتين الواحد نفسه. فعند ربط كل سجل بسقفه عبر معرِّف UniProt بدلاً من اسم البروتين، يظهر أن متوسط التشتت اللوغاريتمي داخل البروتين الواحد يبلغ 0.638 مقابل 0.892 على مستوى القاعدة كلها (88 سجلاً). فبروتين الألبومين في بياض البيض يمتد على مدى 200 ضعف في أربعة سجلات، وكابا كازين 102 ضعف في خمسة سجلات، وألفا لاكتالبومين البشري 115 ضعف في ستة سجلات. ويوزّع نموذج التأثيرات العشوائية المتقاطعة (88 سجلاً، 30 بروتيناً، 52 دراسة) التشتت على النحو التالي: 44% بين البروتينات، و16% بين الدراسات على البروتين نفسه، و40% داخل الدراسات. وطريقة الاستزراع هي العامل الوحيد الكبير والمؤكد إحصائياً: الدوارق المرجوجة تخسر نحو خمسة أضعاف مقارنةً بالمفاعل الحيوي (p = 0.002). وبما أن نصف التشتت يحدث حيث لا يتغير التسلسل أصلاً، فلا يمكن لأي مقياس مستخرج من التسلسل أن يفسره. وتُقدَّم هذه النتيجة كارتباط ونتيجة سالبة بشأن المنهج، لا كإثبات لأي آلية بعينها.

الرابعة، وهي اختبار مباشر انتهى إلى نتيجة سالبة متوافقة مع ما سبق: من بين 53 سجلاً موثقاً تغطي 25 بروتيناً، وبسبع خصائص تسلسلية مُحدَّدة سلفاً، لم ترتبط أي خاصية بالإنتاجية ارتباطاً معنوياً. وكانت نسخة سابقة من هذا العمل قد أفادت بأن كثافة الروابط ثنائية الكبريتيد مرتبطة بالإنتاجية، إلا أن قراءة أعداد الروابط من جداول UniProt الموثقة، بدلاً من افتراض اقتران السيستينات وهو افتراض خاطئ في 15 بروتيناً من 36، أزالت ذلك الارتباط. أما عند التحقق المتقاطع، فإن مؤشراً واحداً يدل على ما إذا أُجريت التجربة في مفاعل حيوي يفسر 15.9% من الخطأ، في حين أن إضافة الخصائص التسلسلية السبع تخفض ذلك إلى 10.1%، والخصائص التسلسلية وحدها أسوأ من مجرد التنبؤ بالمتوسط بنسبة 8.3%. أي أن الإشارة في السجل المنشور تكمن في التجربة لا في البروتين.

خلاصة هذا العمل ليست بروتيناً جديداً ولا سلالة جديدة، بل قياس: التفكيك الكمي الأول لمواضع الكلفة الحقيقية في إنتاج بروتينات الغذاء في خميرة *K. phaffii*، والاختبار المباشر الأول لما إذا كانت تلك الكلفة تفسر السجل الإنتاجي المنشور. وقد تبيّن أنها لا تفسره.

---

## Acknowledgements

I am grateful to my supervisor for the latitude to let this project change shape twice: once when the prior-art audit removed the object it had been built to produce, and again when a corrected database removed a finding that had already been written up. Both reversals improved the thesis, and neither would have survived a less patient review.

This work rests entirely on the published measurements of others. The 167 research groups whose titres make up the corpus of Chapter 5 did the fermentations; the contribution here is only to have read them carefully and divided their numbers by a computable bound. Particular debt is owed to the authors of iMT1026v3, without whose carbon-source-specific biomass equations the central calculation would not be possible, and to the maintainers of UniProtKB, COBRApy and Europe PMC, on whose freely available infrastructure every number in this document depends.

<div style="page-break-after: always"></div>

## Abbreviations and symbols

| | |
|---|---|
| **AOX1** | Alcohol oxidase 1; the methanol-inducible promoter of *K. phaffii* |
| **ATP / GTP** | Adenosine / guanosine triphosphate |
| **BH** | Benjamini–Hochberg, a false-discovery-rate correction |
| **CAI** | Codon adaptation index |
| **CBHI** | Cellobiohydrolase I, the principal secreted cellulase of *T. reesei* |
| **CRC64** | A 64-bit cyclic redundancy checksum, used here to verify sequence identity |
| **DOI** | Digital object identifier |
| **ER** | Endoplasmic reticulum |
| **FBA** | Flux balance analysis |
| **FDA** | United States Food and Drug Administration |
| **FSEOF** | Flux scanning with enforced objective function |
| **GAP** | Glyceraldehyde-3-phosphate dehydrogenase; a constitutive promoter of *K. phaffii* |
| **GEM** | Genome-scale metabolic model |
| **GRAS** | Generally recognised as safe; the US regulatory pathway for food ingredients |
| **GFI** | Good Food Institute |
| **IDP** | Intrinsically disordered protein |
| **IQR** | Interquartile range |
| **LCA** | Life-cycle assessment |
| **Man₈GlcNAc₂** | The core N-glycan transferred in the yeast endoplasmic reticulum |
| **PDI** | Protein disulfide isomerase |
| **PTM** | Post-translational modification |
| **SBML** | Systems Biology Markup Language |
| **TEA** | Techno-economic analysis |
| **UPR** | Unfolded protein response |
| **β-LG / α-LA** | β-lactoglobulin / α-lactalbumin |
| **ρ** | Spearman rank correlation coefficient |
| ***Y*<sub>max</sub>** | Maximum theoretical yield of product on substrate, g g⁻¹ |
| ***Y*<sub>poly</sub>** | Maximum theoretical yield on a polypeptide (backbone-only) basis |
| **log₁₀ SD** | Standard deviation computed on base-10 logarithms, i.e. in orders of magnitude |
| **Ceiling** | Stoichiometric upper bound on titre: substrate loading × *Y*<sub>poly</sub> |
| **Utilisation** | A published titre expressed as a fraction of that protein's own ceiling |

<div style="page-break-after: always"></div>

## Declaration of computational scope

No wet-laboratory work was performed. Every number in this thesis is produced by code in the accompanying repository from publicly available sequences, models and published measurements, and every figure is regenerated from a table that the code writes. Where a quantity could not be obtained from a primary source, it is either omitted or explicitly labelled as an assumption. Predictions are called predictions throughout; none of them is a measurement of a real fermentation, and the final chapter sets out the minimal wet-lab programme that would test them.

## Software and data availability

All code, data, intermediate tables and figures are in the repository accompanying this thesis.

```
src/            analysis code (Python 3.13)
  protein_cost.py     per-protein synthesis reactions and yield computation
  targets.py          UniProt annotation of the nine panel proteins
  build_targets.py    sequence verification against UniProt mass and length
  features.py         sequence feature panel
  codon_opt.py        codon optimisation and construct design
  flux_targets.py     shadow prices and FSEOF engineering targets
  efficiency_gap.py   model ceiling versus published titre
  producibility.py    the sequence-to-titre model and its validation
  tea.py              techno-economic model
  figures.py          every figure in this document
data/
  models/             iMT1026 and iMT1026v3 genome-scale models (SBML)
  sequences/          verified panel sequences and harvested validation set
  literature/         curated titre database and 230-reference bibliography
  external/           codon usage table
results/
  tables/             every computed table
  figures/            every figure
  constructs/         synthesis-ready codon-optimised coding sequences
```
