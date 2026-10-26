# Parity across the corpora: the report

**Written 2026-10-25 for `Plan.md` session 6.** The parity rule (`DataProtocol.md`, decision 4) says an analysis is not done until it has run on every corpus that has the layers it needs, and a corpus is not collected until it has every layer. This file states where the five corpora stand on that rule, counted from the normalized tables (`tables/`), and what the parity runs of session 5 found (`ParityProtocol.md`, frozen 2026-10-21; results in `Parity/`, the keeper's account in `KeeperLog.md`).

## 1. The layers, by corpus

**Stories with the layer from both describers, counted from the tables on 2026-10-26, after session 7.**

| Layer | Wondertale | Animal tale | Fable | Tragedy | Myth |
|---|---|---|---|---|---|
| Stories in the collection | 45 | 50 | 313 | 32 | 412 units |
| Event lists | 45 | 50 | 201 | 32 | 412 |
| Propp's functions | 45, on cards U and C, and Propp's own | 50, card C | 198 | 32 | 126 |
| Role-free acts | 45 | 50 | 90 | 32 | 0 |
| Significance | 45 | 50 | 90 | 32 | 0 |
| Free verbs | 45 | 50 | 90 | 32 | 0 |
| Hero, two readers | 45 | 50 | 198 | 32 | 0 |
| Hero, judged agreed | 40 | 45 | 158 | 27 | 0 |

**What remains to collect, by decision and by plan.**
- **Collected in session 7** (`Session7Protocol.md`; `KeeperLog.md`, 2026-10-26): the animal tales' heroes by two readers, the tragedies' acts and significance for P01 to P08, and significance for the five stories that have acts (wondertale A098; fables F043, F060, F114, F124), with the heroes their readers gave taken as agreed at the owner's word. *Hero, judged agreed* counts by the word rule unchanged (`Heroes/withJudgedHeroes.py`): with its role words kept, the animal tales agree in 50 of 50 (`Parity/heroes-animal.txt`), and the five stories above in all five.
- **The fables beyond the 90 described, and the myths beyond their functions:** not to be collected, by decisions 2 and 1. The next ancient corpus gets every layer from the start.
- **The character-set layer** (`ProppQueue.md` item (m)): not yet built; part of the parity rule once it is.

## 2. The analyses, by corpus

**Which corpora each analysis has now been run on.** "Parity" marks a run of session 5.

| Analysis | Wondertale | Animal tale | Fable | Tragedy | Myth |
|---|---|---|---|---|---|
| Function frequencies, order, placement (`Model/`) | yes | placed | yes | yes | yes |
| Pairs as n-grams (`Ngrams/`) | yes; card C parity | parity | yes | yes | parity |
| Links at a distance (`Links/`, `Genre/`) | yes; card C parity | parity | yes | yes | yes |
| Blocks told together (`Blocks/`) | yes | parity | yes | yes | parity |
| Block order by genre (`Blocks/GenreOrder.md`, `Genre/mythOrder.py`) | yes | parity | yes | yes | yes |
| Spheres of action (`Spheres/`, exploratory) | yes; card C parity | parity | yes | yes | yes |
| Heroes and hero types (`Heroes/`) | yes | waits for two readers | yes | yes | no, by decision 1 |
| Problem structure (`Problems/`, `Animal/layers.py`) | yes | yes | yes | yes | no, by decision 1 |
| Free verbs, the bottom-up test (`Free/`) | yes | reported | yes | yes | no, by decision 1 |
| Values (`Values/`, exploratory) | yes | parity | yes | yes | no, by decision 1 |

## 3. What the parity runs found

**Every run read only the tables, reused the original analysis's program and thresholds, and was self-tested against the published run and dry-run before it produced a result; each program was committed before its run.**

| # | Prediction or report | Corpus | Result |
|---|---|---|---|
| 1 | At least half of Propp's pairs confirmed among the functions | animal tales | **fails**, 2 of 6 (trickery and complicity, struggle and victory) |
| 2 | At least half of their counterparts confirmed among the acts | animal tales | **fails**, 3 of 7 (seek and reveal, deceive and be taken in, test and respond) |
| 3 | The next token more predictable than shuffled | animal tales | **holds**, both layers, both transcribers |
| 4 | Predictions 1 and 3 on the functions | myths | **holds**, pairs 5 of 9, entropy both transcribers |
| 5 | Every tight link tested holds | animal tales | **holds, on one link**, pursuit and rescue; the other three too rare to test |
| 6 | The frame links, reported | animal tales | liquidation after villainy or lack 25% and 19% of moves, return after departure 36% and 19%; the wondertales on card C 44% and 41%, 33% and 39% |
| 7 | Propp's blocks told together beyond chance | animal tales | **holds**, every reading, both transcribers (blocks 61% and 62% of functions against 42% and 44% shuffled) |
| 8 | The same | myths | **holds** (48% and 42% against 31% and 30%) |
| 9 | The order model fitting best, reported | animal tales | the fable's, both transcribers |
| 10 | Spheres, reported | animal tales | the villain's sphere in 90% of tales, the hero's in 58% and 46% (wondertales 98%); hero and villain in one character in 32% and 20% (wondertales on card C 58% and 67%) |
| 11 | Values, reported | animal tales | on every device between tale and fable; the hero's deceptions help the hero in 77% and 80% (tales 94%, fables about 50%) |

**The wondertales on the corrected card, run beside them, behave as on the uncorrected card:** the same six of Propp's pairs confirmed, the acts' counterparts 7 of 10, the frame links within a few points.

## 4. What it means

**The facts.** The animal tales keep Propp's blocks, his tight link of pursuit and rescue, and the sequencing that makes the next function predictable; they drop most of his pairs, keeping those of the trick and the fight; they close their frame about half as often as the wondertales; their hero's sphere is often empty while the villain's is nearly always filled; and on order, values and placement they sit with or near the fable. The myths keep Propp's pairs and his blocks, as far as functions alone can show.

**The keeper's reading, not tested:** the animal tale is the trickster's genre inside the story language Propp described. It keeps the devices of the trick, the fight and the escape, and lets go of the frame that turns a tale into a hero's passage from harm to its undoing; and so it stands on the boundary between the tale and the fable, which every measure in turn has placed it on.

**What this changes in the plan.** Nothing: the agreed order of work stands (`ProppQueue.md` item (n)). Session 7 collects the missing layers when the budget allows; the character-set layer and the cross-cultural corpora come after.
