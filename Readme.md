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
| 5 | language-changing: the J conflict removed by letting the task-run J come only after a task, as v44's own comment proposes | built and tagged `step5`; 42 of 42 binding tests pass; 80 of 84 unchanged; F the only LL(1) conflict |
| 6 | language-changing, by the owner's decision: the F groups merged, the tested agent (after D or E, Propp's DEF) against the untested agent (every other F, the father's gift included) | built and tagged `step6`; 47 of 47 binding tests pass; 80 of 84 unchanged; **LL(1), no conflict**, and `regression.py` passes outright |

**At step 4 the grammar accepts 80 of the 84 move-strings, ruling 48's target, and refuses only the four genuine counterexamples: 126 II, 127 I, 137 II and 138 III.**
The corpus was first met at step 3: 72 of 84, against v44's 69.
`runCorpus.py` runs a grammar over `ResolvedMoves.txt` with `falsify44.py`'s own derivation, so a changed verdict is the grammar's doing.
It was calibrated first: with v44 it fails exactly `falsify44.py`'s 15.
Step 3 frees exactly the three moves predicted before the run, 139 II by the exchange and 164 II and 166 II by T's instability.
Of the twelve still failing, eight carry licenses not yet built in (the pre-departure donor F in six, fight after pursuit in 93 III, the humorous inversion in 150 II) and four are genuine counterexamples; step 4 built the eight in, as predicted before its run.

**What the target cost in LL(1).** The domestic agent puts F in two places, and one token after C cannot tell whether a departure will follow, so F joins J as a conflict. Ruling 48 named this obstruction.
Step 5 removed the J conflict, which was a true ambiguity, by the repair v44's own comment names.
The F conflict cannot be removed while the father's agent and the donor's stay separate groups, for any lookahead: a run of F's belongs to one or the other depending on whether a departure follows the whole run. Only merging the two groups would remove it; changing the reading of p.108 alone would not.
**Step 6 made the merge, by the owner's decision, and the grammar is LL(1).** The split is now drawn at the test instead of at the departure: an F after D or E is the tested agent, the reward of the donor episode, and every other F is the untested agent, the father's gift or an agent that comes to hand on the road. The token before each F decides its group. The untested agent sits in the complication, on either side of the departure. The cost is a small widening: an untested agent may now be followed by a test, as in `A F D E`, which no page licenses and none forbids. No corpus verdict moves.

Moves are sequential for now, separated by `/`; embedding is a later step.
The separator is editorial and follows Appendix III's layout of one row per move. It was adopted when step 2's frozen LL(1) test failed: without it, a move opening on B could not be told from a B inside the move before.

## Files

- `ProppEBNF46.txt`: the grammar, at its latest step.
- `StepTests.txt`: the frozen tests for every step written so far.
- `Step3Spec.txt`: the flat specification of step 3's move language, which the grammar is proved equal to.
- `runSteps.py`: runs them.
- `runCorpus.py`: runs a grammar over the resolved move-strings.
- `parseTree.py`: parses with the LL(1) table and reports where each function lands; `--corpus` writes the group counts.
- `CorpusGroups.txt`: those counts for the 80 accepted moves.
- `SemanticCatalog46.md`: the catalog of v46's groups and pairs, checked against the grammar.
- The copied files listed above.

## Next session: start here

**State at the close of 2026-09-27: step 6, tagged `step6`, and nothing is half-done.**
v46 accepts 80 of the 84 resolved move-strings, refusing only the four genuine counterexamples, 126 II, 127 I, 137 II and 138 III.
It is LL(1) with no conflict, and `regression.py` passes it outright.
Of ruling 48's three targets, two are met, 80 of 84 and LL(1); embedded moves are not begun.

**Run these first, with `PYTHONIOENCODING=utf-8` set, and check the figures.**
- `python runSteps.py 6` prints `88 binding, 0 failed, 0 pending for later steps, 12 closed by an earlier step`.
- `python parseTree.py ProppEBNF46.txt --corpus` reproduces `CorpusGroups.txt`.
- `python runCorpus.py ProppEBNF46.txt --start move` prints `PASS: 80` and `FAIL: 4`.
- `python regression.py ProppEBNF46.txt` prints `RESULT: ALL PASS`.
- `git tag` lists `step1` to `step6`.

### The work, in the owner's order

**1. Tree-level tests: DONE on 2026-09-27.**
`parseTree.py` parses with `parse.py`'s LL(1) table, unchanged, and records the named groups above every token.
`runSteps.py` has two new kinds, `under` and `notunder`, and 27 tree tests were frozen before the tool was written, run red, then passed.
They cover the tested and untested agent, the A-K span, the complication, the move type at the opener, the three J's, the endgame, β in the interdiction pair, α outside every move, and T under `FloatingT` only.
The tool was checked to fail on false claims and on rejected strings.
`CorpusGroups.txt` counts, for each named group, how many of the 80 accepted moves use it: for instance the tested agent 32, the untested agent 17, Combat 32, TaskCycle 9, and the two step-4 licenses once each.
It is the raw material for the catalog `SemanticBundling.md` was meant to become.

**1a. The semantic catalog: BUILT on 2026-09-27, as `SemanticCatalog46.md`.**
It has one entry for each of v46's 24 groups and pairs, each giving its kind, level, contents, page, name source, corpus count, tree test and meaning, plus the J-Q dependency and what the catalog teaches.
A frozen `catalog` test keeps it in step with the grammar: one entry per group, a tree test for every group, and no entry for a group the grammar lacks. It was shown to fail on a missing entry and on a false function entry.
THE FUNCTIONS COME NEXT IN IT, by the owner's decision: the 31 functions, in the reserved "Functions" section at the end, since each function carries meaning of its own. The check already requires each such entry to name one of the grammar's single-function productions.
Whether the first project's `SemanticBundling.md` then points to this catalog, or is replaced by it, is the owner's call; that file is part of the first project's publication.

**2. Embedded moves, ruling 48's third target. A full-budget session, not a small step.**
It needs three things this project does not yet have.
- **A second derivation of the corpus that keeps Propp's interruption markers.** `resolve.py` strips them. `ColumnLayout.md` in the first project lists the seven marker sites: 138 II, 155 III, 155 IV, 159 I, 159 III, 162 I and 167 I.
- **A grammar in which a move can contain a move.** That is self-embedding, so the language is context-free and no longer regular.
- **A new proof instrument.** `equivCheck.py` refuses recursive grammars by design.
Finding FO point 4 argues that the markers make an LL(1) grammar plausible, since they tell the parser where an interrupting move begins.

**3. Small open items.**
- Whether an initial situation α may stand before a later move. The owner reads p.86 as the tale's initial situation, and admitting one later would be a small edit.
- p.108's "all seven functions of this section are never encountered within one tale", left out by the owner's decision.
- Step 6's widening: an untested agent followed by a test, as in `A F D E`, is a cost of the merge and not a license.
- The exchange of p.108 is built on finding FN's reading, the four exchanging among themselves; on the narrow reading, `U Q W` would be refused.

**4. Housekeeping.**
- This project has no remote. If the owner wants it on GitHub beside the first, the owner creates the repository.
- `SemanticBundling.md`, in the first project, does not yet point at v46's groups.
- The first project's publication items for SourceForge are on hold by the owner's decision.

### Conventions and traps this session learned

**Tests first, always.** Write a step's tests, run them red, then build.
A test is never edited to fit a result: a wrong one is commented out with a dated reason and its correction added below.

**A test describing a step's own change closes at that step, written `N-N`.** That covers an equivalence, an inclusion, an LL(1) expectation, or a reject the step's reading decides.
Only tests of what Propp's pages fix bind onward.
Three onward-binding tests broke at the next step before this rule was written.

**An argument written `TAG:FILE` names a file as it stood at a git tag**, so a test can compare the grammar with its own earlier step, as `step5:ProppEBNF46.txt`.

**The corpus runner must read the corpus exactly as `falsify44.py` does.** Its first run missed `falsify44.py`'s alias table, KF as K and w as W, and failed eleven moves it should have passed. The frozen calibration caught it. Keep the calibration test binding.

**A formal claim needs checking before it is written down.** Step 5's note said changing the reading of p.108 would also remove the F conflict. It would not, and the note was corrected before the close.

**Tool traps on this machine.**
- Git rewrites line endings after a commit, and the Edit tool then reports the file modified since it was read. Re-read it before editing.
- Escapes inside a bash heredoc, such as `\\n`, arrive mangled. Write a script to a file and run it instead.
