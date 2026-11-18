# Precision Fermentation: Microbial Cell Factories for Animal-Free Dairy, Heme and Alternative Proteins

### The ceiling–gap decomposition: how far below its stoichiometric limit is each food protein, and why

**التخمير الدقيق: مصانع خلوية ميكروبية لإنتاج بروتينات الألبان والهيم والبروتينات البديلة دون الحاجة إلى الحيوانات**

*Graduation research project*

---

## Abstract

Precision fermentation — programming a microorganism by recombinant DNA to secrete a protein that an animal would otherwise have made — has moved from laboratory demonstration to supermarket shelf in under a decade. Bovine β-lactoglobulin from *Trichoderma reesei* and soy leghemoglobin from *Komagataella phaffii* are both cleared for sale in the United States. Yet the field's own framing of its central problem has remained qualitative: proteins are said to be hard to make because they fold poorly, because they require post-translational modifications the host cannot perform, or because purification is expensive. These claims are rarely quantified, and they are almost never compared against each other on a common scale.

This work asks a narrower and answerable question: **for a panel of nine food proteins, what does each candidate bottleneck actually cost, and which of them is binding?** The analysis is entirely computational and entirely reproducible from the accompanying repository.

Three things are established. First, the stoichiometric ceiling is nearly flat across the panel. Maximum theoretical yields computed by installing explicit, sequence-derived synthesis and secretion reactions into the genome-scale metabolic model iMT1026v3 of *K. phaffii* span only about 9% between the cheapest and the most expensive of the four caseins, β-lactoglobulin, α-lactalbumin, ovalbumin, soy leghemoglobin C2 and bovine lactoferrin, while the choice of carbon source moves the ceiling by roughly 30%. Within the post-translational load, phosphorylation is energetically free — charging α-S2-casein's thirteen phosphoserines costs under 0.12% of yield — whereas N-glycosylation is expensive and becomes dominant under the hypermannosylation that *K. phaffii* performs natively.

Second, realised production is nowhere near that ceiling. Joining the model-derived ceilings to a purpose-built database of 109 published titres, each carrying a verbatim evidential quotation and a citation, shows that the best reported titre for each panel protein lies between 16-fold and roughly 1900-fold below its stoichiometric ceiling, and that the spread between proteins in realised titre exceeds two orders of magnitude. A property that varies by 9% cannot explain an outcome that varies by a factor of a hundred. Metabolic cost is therefore excluded as the explanation of why some food proteins are harder to make than others.

Third, a direct test of what does explain it. Across 37 high-confidence records of secreted production in *K. phaffii*, covering 25 distinct proteins, the density of disulfide bonds is the only sequence feature significantly associated with the titre achieved (Spearman ρ = −0.46, p = 0.021). Maximum theoretical yield is not associated with titre at all (ρ = 0.04), confirming the first result empirically and independently, and predicted intrinsic disorder is not associated either, which complicates the usual explanation offered for the caseins. A cross-validated regression ranks proteins weakly but has no skill in predicting absolute titre against the trivial baseline; this negative result is reported rather than concealed, and is interpreted as evidence that published titres are dominated by how much strain and process engineering each protein has received rather than by the protein itself.

The practical consequences are developed in two further chapters: protein-specific metabolic engineering targets obtained by flux scanning with enforced objective function, and a techno-economic model in which every parameter carries a source and the result is reported against the stoichiometric cost floor implied by the computed yields. The cost analysis finds a floor near $1/kg of raw carbon against a modelled plant cost near $43/kg, and identifies recovery, titre and plant utilisation — not substrate price — as what determines whether precision-fermented proteins reach commodity economics.

The contribution of this thesis is not a new protein, a new strain or a new tool, and it is deliberately narrower than it first appears. Computing per-protein synthesis costs in a genome-scale model is not new: Feizi and co-workers did it across the yeast proteome in 2013, Gutierrez and co-workers reconstructed the mammalian secretory pathway and its per-protein costs in 2020, and pcSecYeast built protein-specific secretion reactions with per-protein bottleneck calls in 2022. Predicting producibility from sequence is not new either. Those steps are used here, with citation, as tools rather than claimed as findings.

What is new is the **decomposition**: computing each food protein's own stoichiometric ceiling, expressing every published titre as a fraction of *its own* ceiling rather than comparing titres to each other, and attributing the residual. That measurement has not been made for these proteins in these hosts, and it is what licenses the central claim — that the binding constraint on animal-free food proteins is not what it costs the cell to build them.

---

## ملخص

التخمير الدقيق هو برمجة الكائنات الدقيقة باستخدام تقنية الحمض النووي المؤتلف لإنتاج بروتينات حيوانية المنشأ دون الحاجة إلى الحيوان نفسه. انتقلت هذه التقنية خلال أقل من عقد من المختبر إلى الأسواق، إذ حصل بروتين بيتا لاكتوغلوبولين المنتج من الفطر *Trichoderma reesei* وبروتين الليغهيموغلوبين المنتج من الخميرة *Komagataella phaffii* على موافقات تنظيمية في الولايات المتحدة.

ومع ذلك، ظل وصف التحدي الأساسي في هذا المجال وصفاً نوعياً لا كمياً: يقال إن بعض البروتينات صعبة الإنتاج بسبب الطي البروتيني غير الصحيح، أو بسبب التعديلات بعد الترجمة التي لا يستطيع المضيف الميكروبي إجراءها، أو بسبب كلفة التنقية. هذه الادعاءات نادراً ما تُقاس، ونادراً ما تُقارن على مقياس واحد.

تطرح هذه الدراسة سؤالاً أضيق وقابلاً للإجابة: ما هي الكلفة الفعلية لكل عائق مفترض، وأيها هو العائق الحقيقي المُقيِّد؟ الدراسة حاسوبية بالكامل وقابلة للتكرار بالكامل.

توصلت الدراسة إلى ثلاث نتائج رئيسية. الأولى أن السقف الكيميائي الحيوي شبه ثابت: لا تتجاوز الفروق في العائد النظري الأقصى بين البروتينات التسعة نحو 9%، بينما يغيّر مصدر الكربون العائد بنحو 30%. كما تبيّن أن الفسفرة لا تكلف الخلية طاقياً تقريباً، في حين أن الغلكزة مكلفة، وتصبح العائق الأكبر عند حدوث فرط المَنَزة المميز لهذه الخميرة.

الثانية أن الإنتاج الفعلي أبعد ما يكون عن ذلك السقف: أفضل إنتاجية منشورة لكل بروتين تقع بين 16 ضعفاً وحوالي 1900 ضعف دون السقف النظري. لذلك لا يمكن لخاصية تتغير بنسبة 9% أن تفسر نتيجة تتغير بمئة ضعف.

الثالثة، وهي اختبار مباشر: من بين 37 سجلاً موثقاً تغطي 25 بروتيناً، كانت كثافة الروابط ثنائية الكبريتيد هي الخاصية التسلسلية الوحيدة المرتبطة إحصائياً بالإنتاجية. أما العائد النظري فلم يرتبط بها إطلاقاً، وكذلك الاضطراب البنيوي المتوقع.

خلاصة هذا العمل ليست بروتيناً جديداً ولا سلالة جديدة، بل قياس: التفكيك الكمي الأول لمواضع الكلفة الحقيقية في إنتاج بروتينات الغذاء في خميرة *K. phaffii*، والاختبار المباشر الأول لما إذا كانت تلك الكلفة تفسر السجل الإنتاجي المنشور. وقد تبيّن أنها لا تفسره.

---

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
  literature/         curated titre database and 232-reference bibliography
  external/           codon usage table
results/
  tables/             every computed table
  figures/            every figure
  constructs/         synthesis-ready codon-optimised coding sequences
```
