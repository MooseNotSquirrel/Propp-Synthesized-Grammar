# A general story grammar: protocol (FROZEN 2026-11-04 AT THE OWNER'S WORD, THE SIX RECOMMENDED DECISIONS TAKEN; nothing built or run)

**Asked by the owner on 2026-11-04,** after the audit of the failed self-test (`Induction/AuditReport.md`). The task, in the owner's terms: a general model that retrieves Propp's model from his corpus, and adapts to a different corpus to retrieve its model, without forcing Propp onto it. Propp's functions and the acts are the base. There must be flexibility in moving up from that base, and candidates may be added to it.

**What it does not change.** The FAILS verdict of `InductionProtocol.md`, the frozen story grammar and its verdicts, and `StoryModels/StructureProtocol.md` all stand.

**The precedent, at the owner's word.** V46, the regular language with the shape of V43, accepted 80 of 84 moves (shuffles 0.8%) and was then tried on other corpora. This model follows that course, so it does not need unseen wondertales before going on. What it needs is rung 1, below.

## 1. How much Propp is in it

| Where | Now | Here |
|---|---|---|
| The alphabet | Propp's functions; the acts | **Kept, as an input.** The tool takes any alphabet and knows none of them. |
| The order | `induce.py`'s `order_key` sorts the vocabulary and breaks ties by Propp's number | **Removed.** No Propp number in the tool. |
| The sections | The frozen story grammar's features are his ten sections and nine pairs; only the weights are fitted | **Removed.** That grammar measures fit to Propp and cannot infer another model. It stays as it is, for that. |
| The moves | The card's rule cuts moves by villainy or lack, and the audit found its filing rule misplaces preparation | **Not read.** The tool takes whole stories and infers its own passes. |
| The target | ARI against ten sections | **Scored apart,** by a program the tool does not import. |

**What stays baked in, stated plainly:**
- The function alphabet carries Propp's categories, and readers were trained on his card, whose list runs in his order. **The acts layer is the control:** it was not built on his card.
- Dropping X leaves out events his alphabet cannot name. X's share is reported per corpus as a measure of that misfit.

## 2. The model

**One rule governs every level: a level is kept only if it raises cross-validated likelihood on held-out stories.** So any level can come back empty, and "no grammar found" is a possible answer.

**Input.** Stories as strings over a named alphabet, one transcriber at a time, whole, without move labels. Symbols in at least 5 stories are modelled; the rest share one rare symbol. Five-fold cross-validation over stories, seeded.

**Level 1. The base:** the symbols.

**Level 2. Moving up from the base.** Two greedy operations, each accepted only under the one rule:
- **Join:** x and y that follow each other far more than chance become one unit (this is where Propp's pairs could appear).
- **Merge:** x and y that occur in the same contexts become one class (this is where his assimilations and alternatives could appear).

**Level 3. The slot grammar.** Each unit has one slot, and the order of the slots is learned:

P(next = y | current = x) = (1 − r_x) · F_x(y) + r_x · R(y)

- **F_x** is a distribution over later slots and the story's end.
- **r_x** is the chance of going back to begin again.
- **R** is one restart distribution, shared by all. That sharing is the model's claim: going back is a new pass, not a free jump.
- **The order** is searched by insertion moves from 50 random starts, never from Propp's or from any list's own order.

**Level 4. What is read off it:**
- **Partial order:** the search repeated on 200 bootstrap samples of stories. i precedes j only if it does so in at least 95% of them; otherwise they stay unordered, instead of being tied by a score.
- **Alternatives:** units that share a pass far less than chance allows, reported as branches (where H-I against M-N could appear).
- **Passes:** the story cut wherever a restart is the likelier reading. This is the model's own notion of a move.
- **Blocks:** adjacent slots grouped when a chain over the groups is kept under the one rule. This is its own notion of a section.

**The shape verdict.** Each corpus and alphabet is fitted by rival shapes and gets the one that wins on held-out stories, by a paired test over stories:

| Shape | Says of the corpus |
|---|---|
| Unigram | No sequence beyond what is in it |
| Bigram (interpolated) | Local links only |
| Free HMM, K by cross-validation | Hidden phases, not ordered |
| Slot grammar, one pass | One ordered pass |
| Slot grammar with restarts | Ordered passes |

This is the adaptation. A corpus need not come out ordered at all. Nothing favours the slot grammar, and the bigram is a strong rival (on Propp's strings it far outpredicted every HMM in the audit).

## 3. The rungs

Each rung is committed before the next is run.

**Rung 0. The tool's honesty.**
- **Renaming:** the same strings under renamed symbols give the identical grammar, name for name.
- **Source check:** a test fails if the tool imports `tragedyScore`, `constraintGrammar` or the story grammar.
- **Planted tests:** hand-worked likelihoods agree; two runs are byte-identical.

**Rung 1. Generated grammars.** No reader data and no real strings. Sizes 20, 45 and 100 stories.

| Generator | The tool must say |
|---|---|
| **G1.** Propp's stated order: functions optional, passes, his pairs | Ordered passes; his order and pairs |
| **G2.** G1 with the functions relabelled at random | Ordered passes; **the scrambled order, not his** |
| **G3.** Two exclusive branches | Ordered passes, with the branches |
| **G4.** Episodes repeated, no overall order | Not ordered |
| **G5.** Local links only | Bigram |
| **G6.** Hidden phases with interchangeable contents | Not slots |
| **G7.** No order at all | Unigram |

**G2 is the test of not forcing Propp.** G3 to G7 test that it can answer otherwise. **The bars for rung 2 are set here, by a rule fixed now:** each is the value that at least 90% of G1 corpora reach at the real size, with at most 5% of G2's relabelled answers scored against Propp's order reaching it. If rung 1 fails, the model is wrong, and no real string is read.

**Rung 2. Propp's own strings: the retrieval.** The 45 tales of `resolved.tsv`, 84 moves, fitted on all of them, as V46 was. His claims, each HOLDS or FAILS against rung 1's bars:

| Claim | Score |
|---|---|
| **Shape** | Ordered passes wins on held-out stories |
| **Order** | Kendall tau with his numbering, over the ordered pairs |
| **Pairs** | Recall of his pairs in the joins or links |
| **Moves** | The inferred passes against his 84 moves: boundary F-score |
| **Acceptance, reported beside V46** | How many of the 84 moves break no relation of the partial order, against shuffled moves, beside 80 of 84 and 0.8% |

Blocks against the ten sections are reported as secondary (section 6, decision 1). His strings have no preparatory units, so **functions 1 to 7 cannot be retrieved at this rung.** A fit on one half, read on the other, goes beside it.

**The limit:** Propp coded his tales with his scheme in hand, so this rung shows the tool can retrieve his model, not that the tales alone contain it.

**Rung 3. The readers' strings of the same 45 tales,** A and B, unchanged. The same scores, with the preparatory units now present. Not reading moves avoids the card's filing rule. The labelling by content remains, and belongs to card D. The gap from rung 2 measures what the transcription costs.

**Rung 4. The other corpora and the acts.** Each corpus and alphabet gets its own shape and grammar. With no known answer, it is judged by:
- **Replication:** the two transcribers' shapes agree, and their orders correlate.
- **Stability:** the bootstrap's support.
- **Prediction:** held-out gain over the unigram and the bigram.
- **Comparison with the wondertales:** the correlation of each order with theirs, with its interval. High and tight would mean Propp's order really is there. Near zero would mean that it is not, and the model did not force it.
- **Function against act layer:** where they disagree, the function layer's order is suspect.
- **Fair sizes:** every comparison repeated at the smallest corpus's size. Small corpora are expected to fall back on simpler shapes, and rung 1's sizes say how far that means anything.

Reported, with no prediction frozen, unless the owner wants one.

## 4. The base list and candidates

**The alphabet is a parameter, so a candidate needs no change to the tool.**
- **First run:** functions, and acts.
- **Candidates:** the sixteen X-study acts (`XStudy/Candidates.md`) and oath, prayer and curse need coded strings. Those exist only where they were transcribed, so most wait for card D at step 7. The audit's finding points the same way: the hero's tricks now coded η could go to `xDec`.
- **How one is judged:** coverage (X's share falls), bits per event, and whether the grammar gains. Likelihoods over different alphabets are not comparable directly, so every event, X included, is scored in bits.

## 5. Stepwise refinement

**The owner, 2026-11-04:** building a general model on Propp's example is very hard, and may need stepwise refinement, moving forward incrementally and improving the model as we learn from each attempt. That is the method here, not a fallback.

- **Each attempt is a numbered version** (`GeneralGrammar/Versions.md`): what it changed, why, what it scored, and what was learned.
- **Nothing is rescored.** A version's result stays on record.
- **Every version passes rungs 0 and 1 again.** Those are the regression suite. Whatever is learned from a failure may add a generator, and none is ever removed.
- **No version may use Propp's order, sections or pairs in the tool.** Rung 1's relabelled Propp enforces this: a refinement that only helps Propp fails there.
- **The count of versions is reported with any result.**
- **The data may be collected again.** The owner is not averse to rerunning all of the data collection if the cards prove wrong or bake in too much Propp. So a failure at rung 3 or 4 may lead to a new card and new transcriptions, as well as to a new version of the tool. Old strings stay on record.

## 6. Decisions for the owner

**Taken 2026-11-04: the owner accepted all six recommendations.**

1. **The target.** Recommended: order, pairs, moves and shape are the claims; the ten sections are secondary. They are this project's grouping (`constraintGrammar.SECTION_GROUPS`), and the keeper would first check against Propp's text how far they are his.
2. **Revisions.** Recommended: allowed and numbered, as in section 5. Forbidding them would be stricter than V46's course. Allowing them is the risk of teaching to the test, which rung 1 and the reported count guard against.
3. **Whole stories, no move labels.** Recommended. The cost: the moves are harder to get than if they were given.
4. **Bars from rung 1, by the rule in section 3.** Recommended, in place of fixed bars like the old 0.6.
5. **Fit rung 2 on all 45.** Recommended, by the owner's precedent, with the half-split reported beside it.
6. **Its place in the queue.** Recommended: ahead of step 6, whose protocol stays frozen, because a working general model decides what story grammar version 2 should be at step 7.

## 7. Order of work and cost

1. The owner's review and decisions; this file frozen (done 2026-11-04).
2. **Program and rung 0:** `GeneralGrammar/grammar.py` (the tool), `score.py` (the only file that knows Propp), `generators.py`; committed before anything runs.
3. **Rung 1,** bars committed. The owner sees it before any real string is read.
4. **Rungs 2 and 3,** then the owner's word for rung 4.

**Cost:** no readers. The keeper's estimate is minutes to a few hours of computing per rung, unmeasured until rung 0.
