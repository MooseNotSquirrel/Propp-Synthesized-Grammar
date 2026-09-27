# SynthesizedProppGrammar

**This is the second project that ruling 47 of Propp Grammar Test Cases split off.**
It begins from copies of that project's files and is not governed by its rulings.
Its question is what structure and meaning a grammar of Propp's folktale can carry once the licenses he grants in prose are built into it, rather than applied afterward.

**It began on 2026-09-27 from Propp Grammar Test Cases at commit 0f27783.**
Six files were copied unchanged: `ProppEBNF44.txt`, `ProppEBNF43.txt`, `ProppMidLevelGroupsEbnf.txt`, `parse.py`, `equivCheck.py` and `regression.py`.
Others are copied when a step needs them, and each copy is recorded here.
`falsify44.py` and `ResolvedMoves.txt` were copied on 2026-09-27 from the first project at 8d38129, for the corpus runner.
`ProppMidLevelGroupsEbnf.txt` was refreshed on 2026-09-27, after the first project's ruling 104 let an absentation be told after the interdiction, as both whole tales Propp analyzes in Ch. IX tell it.

## Method: test first, one step at a time

**The grammar is one file, `ProppEBNF46.txt`, and every step changes it.**
It follows v43, v44 and v45C in the project's numbering.
v44's language is the invariant and v43 is a source of shapes: a name or grouping is borrowed from v43 only when the regrouped grammar is proved to keep v44's strings.
Each finished step is tagged in git, `step1`, `step2` and so on, so any earlier state can be recovered and rerun.

**Every step is labeled language-preserving or language-changing before it is built.**
A language-preserving step adds structure and no strings, and its test is equivalence to the grammar before it.
A language-changing step adds or removes strings, and its tests are written and frozen first, each citing the page it rests on.

**The tests live in `StepTests.txt`, and `runSteps.py` runs them.**
`python runSteps.py N` runs every test that binds at step N, and counts the tests for later steps as pending.
A test binds from its step onward, or over a range such as `1-2` when a later step is planned to break it; the range is written when the test is frozen, not after it fails.
A test is never edited to fit a result: a test found wrong is commented out with a dated reason, and its correction is added below it.

**`equivCheck.py` is the proof instrument.**
It decides whether two grammar files accept the same strings, and prints a shortest string on which they differ when they do not.
It handles grammars whose productions do not refer back to themselves, which covers every step until interruption is taken up.

## Steps

| step | kind | state |
|---|---|---|
| 1 | language-preserving: v44 regrouped into Propp's pairs and groups | built and tagged `step1`; 2 of 2 tests pass |
| 2 | language-changing: the tale layer, a preparatory section and then sequential moves separated by `/` | built and tagged `step2`; 16 of 16 binding tests pass, J still the only LL(1) conflict |
| 3 | language-changing: p.108's licenses in the move, T anywhere and the exchange of recognition, exposure, marriage and punishment on FN's reading | built and tagged `step3`; the move layer proved equal to `Step3Spec.txt`, J still the only LL(1) conflict; 72 of 84 corpus moves |
| 4 | language-changing: the three licenses left, the domestic agent (p.108), the fight after pursuit (p.107) and the humorous inversion (p.147) | built and tagged `step4`; 36 of 36 binding tests pass; **80 of 84 corpus moves**, only the four genuine counterexamples refused; LL(1) conflicts on F and J |

**At step 4 the grammar accepts 80 of the 84 move-strings, ruling 48's target, and refuses only the four genuine counterexamples: 126 II, 127 I, 137 II and 138 III.**
The corpus was first met at step 3: 72 of 84, against v44's 69.
`runCorpus.py` runs a grammar over `ResolvedMoves.txt` with `falsify44.py`'s own derivation, so a changed verdict is the grammar's doing.
It was calibrated first: with v44 it fails exactly `falsify44.py`'s 15.
Step 3 frees exactly the three moves predicted before the run, 139 II by the exchange and 164 II and 166 II by T's instability.
Of the twelve still failing, eight carry licenses not yet built in (the pre-departure donor F in six, fight after pursuit in 93 III, the humorous inversion in 150 II) and four are genuine counterexamples; step 4 built the eight in, as predicted before its run.

**What the target cost in LL(1).** The domestic agent puts F in two places, and one token after C cannot tell whether a departure will follow, so F joins J as a conflict. Ruling 48 named this obstruction; resolving it without losing the constituents is open.

Moves are sequential for now, separated by `/`; embedding is a later step.
The separator is editorial and follows Appendix III's layout of one row per move. It was adopted when step 2's frozen LL(1) test failed: without it, a move opening on B could not be told from a B inside the move before.

## Files

- `ProppEBNF46.txt`: the grammar, at its latest step.
- `StepTests.txt`: the frozen tests for every step written so far.
- `Step3Spec.txt`: the flat specification of step 3's move language, which the grammar is proved equal to.
- `runSteps.py`: runs them.
- `runCorpus.py`: runs a grammar over the resolved move-strings.
- The copied files listed above.
