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

**Result:** not yet run.
