# Grammar induction: protocol (FROZEN 2026-11-03 AT THE OWNER'S WORD, THE FIVE RECOMMENDED DECISIONS TAKEN; nothing built or run)

**Asked by the owner on 2026-11-02** (ProppQueue.md item (r); the order of work, step 5). The aim is a tool that infers a corpus's own Propp-style grammar instead of assuming Propp's.
- **The order of work:** it is tried first on the Russian wondertales, where the answer is known, and trusted elsewhere only if it finds Propp there.
- **Then the act layer:** it is run on the act layer, which was not built on Propp's card.
- **Its place:** this is a companion to item (q), which refines the fixed Propp-based grammar, but a project of its own.

**What it does not change.** The frozen story grammar, its weights and its verdicts are not touched. Nothing here is fitted to them or scored as them.

## 1. The strings

**Function strings.** The units are those `StoryGrammar/storyGrammar.py load` takes, so the induced grammar compares with the frozen one:
- **Which rows and keys:** rows marked Y, keys known to `tragedyScore.NUM`, X left out, each unit keeping its move.
- **Short stories:** stories of fewer than three units are left out.
- **Which corpora:** all seven: the wondertales (card U), animal tales, fables (Aesop and Fables), tragedies, the myths (the Library's 126), and the Native American and East Asian tales.
- **Readers:** transcribers A and B apart.
- **Versions:** each story is weighted 1 over its number of versions.

**Act strings.** The acts layer, one study per story and describer, as `StoryModels/common.py` reads it:
- **Order:** in event, then entry, order, with `other` left out as `Ngrams/NgramProtocol.md` leaves it out.
- **Which corpora:** the six that have acts (not the myths or Aesop; `Data/Coverage.txt`).
- **Moves:** the acts have no moves, so each act string is read as one sequence.

## 2. The split

- **The draw:** within each corpus and layer, the stories are sorted, shuffled with seed 20261103 and halved. The first half is for **induction**, the second for **checking**.
- **When it is written:** the halves are written to `Induction/Split.txt` before any string is counted.
- **The rule:** nothing from the checking half is read before the induced results of the induction half are committed.
- **Both readers:** the same split serves both transcribers.
- **Why not `HeldOut.txt`:** the story grammar's held-out fifth would leave 9 wondertales for checking, too few for the self-test (decision 2).

## 3. Layer 1: the corpus's own order (no model)

**P1. The precedence table.**
- **Which functions:** every function in at least 5 stories of the induction half.
- **The share:** for each pair i, j, the share of pairs of occurrences in the same move in which i comes first. Each story is weighted as in section 1.
- **The test:** a sign test over stories. A story counts for i first if most of its i, j pairs have i first.

**P2. The partial order.**
- **The relation:** i precedes j when the share is at least 0.75, at least 10 stories hold both, and the sign test gives p at most 0.05.
- **The report:** its transitive reduction (the Hasse diagram), as a list.
- **The linear order:** the order implied by it, by Copeland score (wins minus losses).

**P3. Checked.**
- **On the checking half:** the share of P2's relations whose direction holds again.
- **Between readers:** the agreement of A and B (relations in both over relations in either).
- **Against Propp:** Kendall's tau between the linear order and Propp's numbering of the functions (`tragedyScore.NUM`).

## 4. Layer 2: the corpus's own pairs and blocks

**Q1. Pairs within the move.** This extends `Ngrams/ngrams.py`: its statistic (the count of y after x, against 1,000 shuffles, seed 46), counted within the move and at any distance.
- **A candidate:** on the induction half, for both transcribers, a count of at least 5, a lift of at least 1.5, and p at most 0.01.
- **Confirmed:** on the checking half, for both transcribers, a lift above 1 and p at most 0.05.
- **Not assumed:** Propp's pairs are not given to the tool.

**Q2. Blocks.**
- **What a block is:** a set of three or more functions in which every ordered pair, in one order, is a confirmed pair (a clique in the graph of confirmed pairs).
- **Reporting:** each block is reported in that order.

**Q3. Against Propp.**
- **Recall:** among Propp's 12 pairs (`NgramProtocol.md`) that occur at least 5 times, the share confirmed.
- **Precision:** among the confirmed pairs, the share that are Propp's.
- **Blocks:** each block is set against v46's blocks.

## 5. Layer 3: the induced grammar

**H1. The model.** A hidden-state model, a first-order HMM with discrete emissions, one per corpus, layer and transcriber, fitted on the induction half.
- **Start, end and moves:** each move begins from the start distribution, and the end of each move is an emitted end symbol. The model learns each move's own course.
- **Fitting:** Baum-Welch from 20 random starts (fixed seeds), keeping the best likelihood. Emissions are smoothed by adding 0.01.
- **Not assumed:** no state is tied to a section, and no order is imposed: the model may learn any order.

**H2. The number of states.** K is chosen from 2 to 12 by five-fold cross-validation within the induction half: the K with the highest mean held-out log-likelihood per unit (decision 1).

**H3. The induced sections.**
- **Each function's section:** each function is assigned to the state that emits it most, weighted by the state's occupancy.
- **The order:** the states are ordered by the mean position, within the move, of the units they emit.

**H4. The regular grammar.**
- **The rules:** transitions of probability at least 0.05 are written as rules, in the style of v46: each state a nonterminal, its functions the alternatives, its likely successors the continuation.
- **Where it is written:** `Induction/Grammar-<corpus>-<layer>-<A or B>.txt`.

**H5. Checked.**
- **Against baselines:** on the checking half, the log-likelihood per unit against a unigram baseline and a bigram (first-order Markov) baseline fitted on the same half. It must beat the unigram to be reported as a grammar.
- **Between readers:** the agreement of A's and B's sections, by the adjusted Rand index over the functions both assign.

## 6. The self-test, first

**On the wondertales, function layer, both transcribers.** The tool is trusted on other corpora only if it passes (decision 3).

**S1. Sections.** The induced sections against Propp's ten (`constraintGrammar.SECTION_GROUPS`), by the adjusted Rand index over the functions in at least 5 stories.
- **The bar:** above at least 95% of 1,000 random assignments with the same section sizes.
- **And the order:** the states' order agrees with Propp's section order by Kendall's tau of at least 0.6.

**S2. Order.** P2's linear order agrees with Propp's numbering by Kendall's tau of at least 0.6, with p at most 0.05.

**S3. Pairs.** Q1 confirms at least half of Propp's pairs that occur at least 5 times (the bar of `NgramProtocol.md`'s prediction 1).

**Verdicts:**
- The self-test PASSES if S1, S2 and S3 hold for both transcribers.
- It is SPLIT if they hold for one.
- It FAILS otherwise.
- On a FAIL, the other corpora are run but reported only as the output of an unverified tool.

**The act layer's self-test.** The act vocabulary has no sections of Propp's, so the wondertales' act states are compared with the sections of the functions at the same events.
- **The tokens:** each act token takes the section of the function, or the most common section of the functions, its event carries in the functions layer (same transcriber letter). Events with no function are left out.
- **The bar:** S1's adjusted Rand index and bar, on the act tokens.
- **The meaning:** a pass means the act layer, built without Propp, falls into Propp's sections by itself.
- **This test is not a gate.** It is the act layer's answer.

## 7. Tests of the tool, before any figure is read

- **I1. Planted grammar.** Strings are generated from a known 10-state model, at the wondertales' size (45 stories, about 80 units each, two transcribers each with its own noise).
  - **H1 to H3:** they must recover its states with an adjusted Rand index of at least 0.8, and K within 2 of 10.
  - **P2:** it must recover the planted order with tau at least 0.8.
  - **Q1:** it must confirm two planted pairs and no more than two others.
- **I2. Shuffled wondertales.** The wondertales' functions are shuffled within each move (seed fixed).
  - **S1 and S2 must fail:** an ARI not above the 95% bar, and tau under 0.6.
  - **Q1:** it confirms no more than two pairs.
  - **The aim:** this shows the self-test cannot be passed by the units' frequencies alone.
- **I3. The split.** No checking-half story is in any induction-half count (the programs assert it).
- **T. The same answer twice.** Two runs are byte-identical.

## 8. Decisions for the owner

**Taken 2026-11-03: the owner accepted all five recommendations.**
- K chosen from 2 to 12 by five-fold cross-validation.
- The program's own halves, seed 20261103.
- The self-test's bars as in section 6. On a FAIL the other corpora are run and labelled as an unverified tool's output.
- The self-test is the one verdict; everything else is reported only.
- The act layer's self-test event-aligned and reported, not a gate.

1. **The number of states:** chosen from 2 to 12 by cross-validation (recommended), or fixed at 10, Propp's section count.
2. **The checking stories:** the program's own halves (recommended), or the story grammar's `HeldOut.txt` (9 wondertales to check on).
3. **The self-test's bars:** as in section 6 (recommended), or other bars. Also whether a FAIL stops the other corpora (they are run but labelled, recommended) or withholds them.
4. **Reported only, or with predictions.** Recommended: the self-test is the one verdict, and the other corpora are reported only (exploratory). A further reading is left as speculation, *not from Propp*, until the self-test passes: for example, that the new corpora's induced section orders differ from Propp's more than the animal tales' do.
5. **The act layer's self-test:** event-aligned to the functions' sections and reported, not a gate (recommended), or a gate for the act layer's other corpora.

## 9. Order of work, and the cost

1. The owner's review and decisions; this file frozen (done 2026-11-03).
2. **`Induction/split.py` writes `Split.txt`,** committed.
3. **The programs** (`Induction/induce.py`, with its own small HMM in numpy, since `hmmlearn` is not installed) are written and committed. I1 to I3 and T must pass before any figure is read.
4. **The self-test** on the wondertales' functions, at the owner's word: the verdict.
5. **The function layer** on the other six corpora; then **the act layer**, its self-test first.

**The cost:** no readers, only computing. The cross-validated HMM fits are the largest piece: seconds per fit, a few minutes per corpus.
