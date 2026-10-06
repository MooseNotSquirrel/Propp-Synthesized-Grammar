# Each genre's order of blocks, tested on every genre

**Frozen 2026-10-06, before any genre's order model but tragedy's is fitted, and before any model is scored on another genre's test set.** A departure is logged in `KeeperLog.md` (Calibration), not made here.

## The question

The tragedy order model (`Tragedy/TragedyOrder01.txt`) held on unseen plays, about twice as strong as Propp's order. Does each genre have an order of its own, or do the genres share one? And does the Russian wondertale, read by the same instrument, follow Propp's order best, as it should if Propp described its order rightly?

## Three genres, each split once

| Genre | Fitted on | Tested on | Transcriptions |
|---|---|---|---|
| Russian wondertale | the 22 development tales of `Calibration/Split.txt` | its 23 test tales | Propp-Afanasyev, arm U |
| Fable | the 100 drawn Aesop fables (Propp-Aesop) | the 99 held-out fables (Propp-Fables) | both |
| Tragedy | P01-P04 | P05-P32 | Propp-Tragedy |

Transcribers A (Opus) and B (Sonnet) throughout, kept apart; each genre's model is fitted on both transcribers pooled, as the tragedy model was.

## The models

Each genre's model is fitted by `Tragedy/tragedyGrammar.py`'s recipe, unchanged: `blockStream.py`'s `blocks` reading, transparent items dropped, a block one unit named by its entry, a bare function one unit named by its symbol, each unit name's mean relative position, names seen fewer than 3 times unranked. The tragedy model is `TragedyOrder01.txt` as frozen. The fourth model is Propp's order: a unit's rank is Propp's number of its first function.

## The measure

For each model, test set and transcriber: concordance, the weighted share of pairs of ranked units with different ranks that stand in the model's order (a story with k versions weighs 1/k per version); the gap over 1000 in-place shuffles of each version's units, seed 46. A 4-by-3 table per transcriber.

## The predictions

1. **Each genre's own order fits it best.** On each genre's test set, its own model's gap is the largest of the four, for both transcribers.
2. **The wondertale follows Propp.** On the Russian test tales, Propp's order's gap is at least the fable and tragedy models' gaps, for both transcribers.

Each holds only if it holds for both transcribers; each is reported on its own. Reported, not judged: every cell's shuffles at or above the real; the rank correlation (Spearman) between each pair of fitted models over the unit names both rank.

## Known before freezing

On the tragedy test set, the tragedy model's gap (+0.133, +0.122) exceeds Propp's (+0.072, +0.063): part of prediction 1 for tragedy is already known. Over all 45 Russian tales, by another measure, function pairs run against Propp's numbering 28% to 31% of the time. Nothing else in the table has been computed.
