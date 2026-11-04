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

**Result:** not yet run.
