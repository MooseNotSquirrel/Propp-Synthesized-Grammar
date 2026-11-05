# The general grammar's versions (GeneralGrammarProtocol.md section 5)

Each attempt: what it changed, why, what it scored, what was learned. Nothing is rescored. Every version passes rungs 0 and 1 again.

## Rung 1's rules, fixed before any version ran (2026-11-04)

**Corpora.** 20 each of G1 and G2 at 45 stories; 10 each of G3 to G7 at 45 stories; 5 of each generator at 20 and at 100 stories. 160 in all. Rates are stipulated in `generators.py` and read from no corpus. G1: each function in at least 30%, one opening (A or a) a pass, pairs follow at 0.8, one pass plus more at 0.45, each unit swapped with its neighbour at 0.1.

**The verdict.** `ordered` means the slot shape won the ladder and the partial order covers at least 30% of the symbol pairs. The ladder runs unigram, slots, bigram, HMM. Each step needs a one-sided paired sign-flip test over stories at p at most 0.05 against the shape in hand. The slots go first because they have fewer parameters than the bigram: with both about equal, the simpler stands.

**Rung 1 passes when, at 45 stories, in at least 80% of corpora:**

| Generator | Required |
|---|---|
| G1 Propp's stated order | ordered |
| G2 relabelled | ordered |
| G3 branches | ordered |
| G4 episodes | not ordered |
| G5 local links | shape is bigram |
| G6 hidden phases | not ordered |
| G7 no order | shape is unigram |

**And also:**
- **The bars,** by the protocol's rule: each of relation tau, order tau, pair recall and pass F-score is set at G1's 10th percentile at 45 stories.
- **G2 against its own scrambled order:** at least 80% reach the tau bars.
- **G2 against Propp's order, the test of not forcing him:** at most 5% reach the tau bars.
- **G3:** at least half of the cross-branch pairs flagged as branches in at least 80% of corpora, and G1 flags no more than 5% of its pairs on average.

Sizes 20 and 100 are reported and do not decide.

**If rung 1 fails,** no real string is read, and the failure is recorded here as that version's result.

## Version 1 (2026-11-04)

The protocol's model. **Details the protocol left open, fixed here:** bootstrap searches take a warm start from the full fit plus 3 random starts, for speed; the HMM's K comes from the same held-out score, which favours it slightly; 2 HMM starts of 25 iterations; a level-2 step must gain 2 nats. The blocks of level 4 are secondary and not yet written; they come before rung 2.

**Result: RUNG 1 FAILS** (`Rung1-v1.txt`). No real string was read.

| | Required | Met |
|---|---|---|
| G1 | ordered | 8 of 20 |
| G2 | ordered | 10 of 20 |
| G3 | ordered | 4 of 10 |
| G4 | not ordered | 8 of 10 |
| G5, G6, G7 | as required | all |

- **What worked:** the order itself. Order tau 0.997 on G1, 0.999 on G2's own order, and **against Propp's order G2 gave a median of 0.004, none reaching the bars.** Pair recall 0.83.
- **What failed:** the verdict, the passes (F 0.10) and the branches (none found).

**What was learned:**
1. **Beating the bigram cannot be the test of order.** The bigram holds the slot grammar inside it, so with enough data it always wins (0 of 5 at 100 stories). The verdict confused "which predicts best" with "is there an order".
2. **A bug:** a merged unit was counted as two base symbols when cuts were mapped back, shifting the boundaries. Rung 0 did not catch it.
3. **Every small slip back was read as a new pass.** A swap of neighbours cannot be told from a restart in this model.
4. **Level 2 merged on noise:** about 11 merges on G7, which has no structure.
5. **G1 is too easy.** Its bars come out at tau 0.99, which no real strings should be asked to reach. This is the old fault in reverse.

## Version 2 (2026-11-04)

Changes, each from what version 1 taught, and all before any real string:
1. **The verdict:** ordered means the slots beat the unigram (p at most 0.05), keep at least 90% of what the bigram gains, and the partial order covers at least 70% of pairs. The two thresholds are read from version 1's generated corpora, so version 2 runs on **fresh draws.** Otherwise unigram, then bigram, then HMM; "local order" if slots beat those but cover too little.
2. **The bug fixed,** with a test added to rung 0.
3. **Slips:** a third part of the model, a step back of at most a learned window of slots (0, 2, 4 or 8, by held-out score). Cuts are made only where a restart beats going forward or slipping.
4. **Level 2** must also pass the paired test.
5. **Branches** flagged at p at most 0.01 rather than 0.001, since at 45 stories 0.001 could hardly be reached.
6. **A new generator, G8:** Propp's order made harder, with unequal rates (some functions rare), slips at 0.25, and about 17 units a story. It must also come out ordered in at least 80% of corpora, and keeps its place in every later version.

**The bars are for the owner.** The protocol's rule sets them from G1, which proved too easy. G8's figures are reported beside them.

**Result: RUNG 1 FAILS, on G8 alone** (`Rung1-v2.txt`). No real string was read.

| | Required | Met |
|---|---|---|
| G1 | ordered | 19 of 20 |
| G2 | ordered | 17 of 20 |
| G3 | ordered | 10 of 10 |
| G4 | not ordered | 9 of 10 |
| G5, G6, G7 | as required | all |
| **G8** | **ordered** | **1 of 20** |

On G1: passes F 0.97, up from 0.10. Branches found in all G3 corpora. Against Propp's order, G2 gave a median of −0.07, none reaching the bars. G1's false branches 0.002.

**What was learned:**
1. **The slips and the verdict worked.**
2. **On G8 what is stated is right, but little is stated:** relation tau about 1.0, on 20 to 245 relations, and coverage 0.30. Order tau has a median of only 0.50. The search reads order from immediate neighbours alone, and those are what slips disturb.
3. **One G2 corpus gave order tau −0.03, coverage 0.38 and F 0.0.** A rotated order may fit nearly as well, because a story's passes make a cycle. Reading across longer distances should settle this too.
4. **The bars by the protocol's rule are now relation tau 1.000 and order tau 0.986,** too high to ask of real strings. G8's are 0.986 and 0.037, too low. So the owner's decision on bars stands open.

## Version 3 (2026-11-04)

One change. **The order may also be read from precedence among units at most d apart** (d of 2, 4 or 8), beside the likelihood over immediate neighbours; the method for a corpus is chosen by held-out score. Passes are still not given: the window runs over the whole story, and the choice of d is how far it is allowed to reach. Fresh draws.

**Result: RUNG 1 PASSES** (`Rung1-v3.txt`). No real string was read.

| | Required | Met at 45 stories |
|---|---|---|
| G1 | ordered | 20 of 20 |
| G2 | ordered | 20 of 20 |
| G3 | ordered | 10 of 10 |
| G4 | not ordered | 10 of 10 |
| G5 | bigram | 10 of 10 |
| G6 | not ordered | 10 of 10 |
| G7 | unigram | 10 of 10 |
| G8 | ordered | 20 of 20 |

All are met at 20 and 100 stories too. **Against Propp's order, G2 gave a median of 0.006 (at most 0.267), none reaching the bars; 90% reached them on their own scrambled order.** Branches found in all G3 corpora; false branches 0.002.

| 45 stories | Relation tau | Order tau | Pair recall | Pass F |
|---|---|---|---|---|
| G1, 10th percentile (the protocol's bars) | 1.000 | 0.995 | 0.833 | 0.943 |
| G8, 10th percentile | 0.993 | 0.971 | 0.541 | 0.835 |

**What this does and does not show:**
1. **It shows the tool retrieves an ordered grammar when one is there, says otherwise when none is, and does not lean to Propp.**
2. **It does not show the tool will retrieve anything from real strings.** The generators are of the same family as the model, written by the same hand, and real tales will be messier. The verdict's two thresholds were read from generated corpora: G5 reached a ratio of 0.87 against the bar of 0.90, a thin margin.
3. **Pair recall tops out at 0.83 by construction:** two of his twelve pairs (A with K, a with K) stand far apart, and links read neighbours only.
4. **Acceptance is not comparable to V46's yet.** Any single slip breaks a strict partial order, so G1 accepts only 34% and G8 12% with the true order fully recovered. V46's 80 of 84 is a different measure.

**The bars for rung 2: G8's, by the owner's decision, 2026-11-04,** in place of the protocol's rule, which gave G1's: relation tau 0.993, order tau 0.971, pair recall 0.541, pass F 0.835.

**Not yet written:** the blocks of level 4 (secondary), and the check of the ten sections against Propp's text. Rung 2's claims do not need them.

**Rung 2, version 3, on Propp's own strings** (`Rung2-v3.txt`), with G8's bars. Given his functions, the tool, knowing nothing of him, returned:

`A a B C up D E F G H I K down Pr Rs o L M N T Q Ex U W`

| Claim | Result | Bar | |
|---|---|---|---|
| Shape | ordered passes | | HOLDS |
| Order tau | 0.984 | 0.971 | HOLDS |
| Pair recall | 0.778 (7 of 9) | 0.541 | HOLDS |
| Relation tau | 0.984 (on 256 relations) | 0.993 | FAILS, narrowly |
| Pass F | 0.661 | 0.835 | FAILS |

Beside it: fitted on one half alone, order tau 0.856. 55 of 84 moves break no relation (shuffled 0.002), not comparable to V46's 80 of 84. The frozen self-test's order figures were 0.23 on the readers' strings and 0.43 on his.

**What this does not show:** the alphabet was given. He coded these strings with his scheme in hand, and they have no preparatory units. The readers' strings (rung 3) are not yet run.

## The owner's input, 2026-11-04: leaves first

The owner proposes that stepwise refinement should begin with the largest and most basic item: can Propp's functions plus candidates be retrieved from a corpus at all, from its verbs and acts, with correlation shown? Then up the hierarchy to pairs, with the distance between them, then groups, with order inferred and allowed to float, since deception has been found after villainy. The model adapts to each corpus to give its internal structure. The owner's speculation: functions plus candidates are about 80% correct for nearly all corpora.

**The keeper's first measures on it, exploratory, from the tables:**
- **Units given a function rather than X:** wondertales 71% to 73%; myths 65%; animal tales 60%; fables 58%; East Asian 55%; Native American 49%; tragedies 47%. This is a share labelled, not a share correct.
- **On one wondertale event, one reader, the act explains 28% of the uncertainty of the function** (4.63 bits, 3.33 given the act; a low estimate, as an event's acts and functions are crossed).

# The pairs tool's versions (`PairsProtocol.md`)

## Pairs, version 1 (2026-11-04)

The frozen design. One detail added before the run: where no shuffle reached the observed figure, p comes from a normal tail, as 2,000 shuffles alone could not satisfy the false discovery rate over hundreds of pairs.

**Result: RUNG 1 FAILS** (`PairsRung1-v1.txt`). Recall 0 on the planted pairs, even tight ones, on the easy G1. G7 and G4 gave no false pairs.

**What was learned, from one corpus inspected directly:** nothing is broken. His tight pairs reach p of about .001 to .005 on a half-sample of 23 stories, and the correction over about 450 candidates asks for far less. Some planted pairs stand together in only 2 stories, so counting them was unfair. Direction across whole stories is also diluted, at shares of 0.65 to 0.78, as a second pass can place x after an earlier y.

## Pairs, version 2 (2026-11-05)

A departure from the protocol, by section 3's rule, on generated strings only. **A test passes at p at most 0.05 on each of the two halves,** which gives about 1 false pair in 450 by chance, in place of the false discovery rate on the first half. **Recall counts only pairs both of whose symbols stand together in at least 5 stories.** Fresh draws.

**Result:** not yet run.
