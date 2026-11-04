# The audit of the failed self-test: plan (2026-11-04, at the owner's word; written and committed before any audit figure)

**Asked by the owner on 2026-11-04.** The self-test of `InductionProtocol.md` FAILS for both transcribers (`Checked-functions-tale.txt`). **That verdict stays.** This audit asks why it failed and whether a modified model could help. Nothing here replaces it, and no result here is a pass. Everything is reported beside the record, by `Induction/audit.py`, in `Induction/Audit-*.txt`. No readers.

**What the keeper knows already, so this is not blind.** The self-test's figures; that the n-gram study confirmed 6 of 10 of Propp's pairs by adjacent and near statistics; that most functions tie at a Copeland score of 0; and, from tokenizing them, that Propp's own strings have no preparatory functions and run about nine units a move.

## The explanations being separated

1. **A fault in the code.** The program does not compute what the protocol says.
2. **The bars could not be met.** A perfect but coarser answer would still fail.
3. **The test was underpowered.** The tool cannot find a true section grammar at this size.
4. **The transcriptions.** The readers' strings differ from Propp's in a way that hides his structure.
5. **The strings do not carry his sections.** A model held to his sections predicts no better than one held to arbitrary sections.
6. **A design choice.** One choice of the tool's (the pair statistic, the number of states, free transitions, the order thresholds) causes the failure.

More than one may hold.

## The parts

**U0. The code.** `audit.py` reproduces the record's relations, K and sections for transcriber A from its own call of the same functions; a pair count and a precedence count are recomputed by plain loops, independent of the matrix code.

**U5. The bars.** For K from 2 to 10, every merging of Propp's ten sections into K consecutive groups is treated as a perfect K-state answer, on the record's eligible functions. Reported: the best ARI and tau at each K, and whether S1 would hold for it.

**U2. Propp's own strings.** `resolved.tsv`, 45 tales, keyed by `tragedyScore.key`, the markup `{ } [ ] /` dropped and alternatives kept in the order written. The frozen tool, unchanged, on the same split: S1, S2 and S3. This is the one unseen string set, so it is run once. Beside it, the closeness of the strings: normalized edit distance of A, B and Propp story by story, against the same distance to another story's string, with units per story and the share of preparatory units.

**U3. Do the strings fit Propp's sections?** A chain over sections: the next section given this one, and the function given its section, 0.01 added to every count, fitted on the induction half and scored per symbol on the checking half.
- The true sections against 10,000 random partitions of the functions with the same sizes.
- Beside it: the record's HMM, the unigram and the bigram.
- For A, B and Propp's strings.

**U4. The tool's choices, one at a time.** Exploratory, and many, so a lone good figure means little. For A, B and Propp's strings:
- **a. Pairs:** Q1 by the n-gram study's classes, adjacent (d = 1) and near (d = 2 to 4), within the move, on the same halves, against the any-distance count.
- **b. Order:** S2 with looser relations (share at least 0.6, at least 5 stories, p at most 0.1); by each function's mean relative position (no ties), with a null of 1,000 within-move shuffles; on the induction half and on all the stories.
- **c. States:** K fixed at 10; K fixed at 10 forward-only (no transition to an earlier state); forward-only at the record's K.
- **d. Data:** the tool on all 45 stories, K by cross-validation (S1 and S2 only). For A and B, the tool with the preparatory units removed, as Propp's strings have none.

**U1. The power of the test.** Strings generated from a chain over Propp's true sections, its counts taken from each transcriber's induction half, with the same number of stories and of moves per story.
- **At the real size:** 10 corpora per transcriber, the tool unchanged: how often S1 and S2 hold, and K, ARI and tau.
- **At twice and four times the size:** 5 and 3 corpora, transcriber A.
- **Order only at sixteen times the size:** 5 corpora per transcriber, S2 alone: what the order test gives as the data grow.
- This generator has sections and no planted pairs, so it says nothing of S3; U4a does.

## How the results will be read, fixed now

- **Explanation 1** stands if U0 finds any disagreement.
- **Explanation 2** stands if, at K of 4 to 6 (what the tool chose), the perfect merging cannot satisfy S1. It stands for S2 if the order test does not reach 0.6 at sixteen times the size in U1.
- **Explanation 3** stands if S1 and S2 together hold in fewer than half of U1's corpora at the real size. Then the self-test could not have passed even had the sections been true.
- **Explanation 4** gains if Propp's strings pass where A and B fail. It loses if they fail alike.
- **Explanation 5** gains if the true sections do not beat at least 95% of the random partitions in U3, for A and B. If they do beat them, the strings carry his sections and the tool failed to find them.
- **Explanation 6** gains for S3 if U4a's near classes reach recall of at least 0.5 where the any-distance count does not.

## What may follow, and its limits

- No modification is adopted here. If a modified tool is wanted, it needs its own protocol, frozen by the owner.
- The wondertales and, after U2, Propp's own strings will have been seen. A modified tool cannot be validated on them. It would need stories it has not seen, which may mean new transcriptions by readers.
- If the cause proves to lie in the transcriptions, the other models that read those strings are named in the report, with what follows for them.
