# Product classes and filter sensitivity

## Product class counts

- **food_protein**: 129
- **other**: 71
- **therapeutic**: 61
- **industrial_enzyme**: 23
- **food_enzyme**: 13
- **research_reagent**: 9

61 of 306 rows are human therapeutics. Any correlation between disulfide density and titer must be refitted within the food-protein subset before it can be attributed to disulfides rather than to the circumstances under which therapeutics are developed.

## Ceiling and utilisation spread under each filter

The two threads report 1.20x / 224x and 1.38x / 628x for the same two quantities. These are not estimates of one number to be averaged; they are the same calculation under different inclusion rules. Below is this thread's table recomputed under every combination, so the other thread's figures can be matched to a row rather than reconciled by splitting the difference.

| include benchmarks | include T. reesei | ceiling spread | utilisation spread | n |
|---|---|---|---|---|
| no | no | 1.18x | 152x | 14 |
| no | yes | 1.18x | 152x | 18 |
| yes | no | 1.18x | 224x | 16 |
| yes | yes | 1.18x | 224x | 21 |

What the table actually shows, which is not what I expected: **the ceiling spread is insensitive to all three filters**, sitting at 1.18x in every combination. Only the utilisation spread moves, from 152x to 224x, and it moves through its lower end, which is set by whichever poorly expressed protein is allowed in.

So the difference between 1.20x and 1.38x cannot be a filter difference. It has to come from **panel membership** - which proteins are in the panel at all. A ceiling is a function of amino-acid composition and glycan load, so admitting a protein with an unusual composition moves the extremes. Collagen is the obvious candidate: it is roughly a third glycine and a fifth proline, far outside the range of anything in the food panel, and it is present in the other thread's corpus. The way to reconcile is therefore to compare panel rosters protein by protein, not to compare filter settings.

The same argument applies to 224x against 628x: both are ratios between the best and worst performer, so each is determined by two single rows and is fragile by construction. An interquartile or log-standard-deviation measure of the utilisation distribution would be the more defensible statistic for the paper, and would not shift when one protein enters or leaves.
