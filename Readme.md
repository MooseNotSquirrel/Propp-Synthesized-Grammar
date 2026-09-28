# SynthesizedProppGrammar

**This is the second project that ruling 47 of Propp Grammar Test Cases split off.**
It begins from copies of that project's files and is not governed by its rulings.
Its question is what structure and meaning a grammar of Propp's folktale can carry once the licenses he grants in prose are built into it, rather than applied afterward.

**It began on 2026-09-27 from Propp Grammar Test Cases at commit 0f27783.**
Six files were copied unchanged: `ProppEBNF44.txt`, `ProppEBNF43.txt`, `ProppMidLevelGroupsEbnf.txt`, `parse.py`, `equivCheck.py` and `regression.py`.
Others are copied when a step needs them, and each copy is recorded here.
`falsify44.py` and `ResolvedMoves.txt` were copied on 2026-09-27 from the first project at 8d38129, for the corpus runner. `TaleTokenStreamsV4Utf8.txt` and `resolve.py` were copied on 2026-09-27 from the first project at 0979f9f, for the whole-tale derivation. `ProppEBNF43.txt` was refreshed on 2026-09-27 after the first project corrected its note on combining moves (finding FV); no production changed.
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
| 6 | language-changing, as decided: the F groups merged, the tested agent (after D or E, Propp's DEF) against the untested agent (every other F, the father's gift included) | built and tagged `step6`; 47 of 47 binding tests pass; 80 of 84 unchanged; **LL(1), no conflict**, and `regression.py` passes outright |
| 7 | language-changing: embedded moves, a move pausing after any function for a whole inserted move, bracketed ⟨ ... ⟩, to any depth (p.93 methods 2 and 3) | built and tagged `step7`; 93 of 93 binding tests pass; context-free and still LL(1); with the pause removed, proved exactly step 6; **41 of 45 whole tales**, the four refused holding the genuine counterexamples |
| 8 | language-changing: two more of p.93's methods at tale level, a common ending shared by two moves (method 5) and two seekers parting into two branches (method 6), in Propp's own signs } < Y | built and tagged `step8`; 104 of 104 binding tests pass; still LL(1); with both removed, proved exactly step 7; 41 of 45 tales unchanged |
| 9 | language-changing: p.107's inverted sequence, the departure or the donor sequence before the crisis, the last license of pp.107-108 | built and tagged `step9`; 118 of 118 binding tests pass; still LL(1); with it removed, proved exactly step 8; under option 1, as decided, the corpus derivation still drops the parked cells left of A, so no verdict moves |
| 10 | v43's two genre extensions overlaid and COMMENTED OUT, as decided: tragedy (a combat ending in defeat, exposure and punishment, with its own defeat sign I-) and the Dundes consequence tale (its own root, Dundes's order of Consequence before Attempted Escape, correcting v43) | built and tagged `step10`; 132 of 132 binding tests pass; commented out, proved exactly step 9; switched on in a copy (`ProppEBNF46.txt+tragedy`, `+dundes@consequenceTale`), still LL(1) and only adding |
| 11 | a second tragic variant, the fall after success, COMMENTED OUT: a reversal Rv closing a move, then recognition, exposure or punishment turned on the hero, as Prometheus and Oedipus fall; Aristotle's warrant, not Propp's | built and tagged `step11`; 154 of 154 binding tests pass; commented out, proved exactly step 10; switched on (`+reversal`), alone or with the others, still LL(1) and only adding. Success is a matter of perspective: from Zeus's side Prometheus is a punished villain, so none is required before the reversal. With the combat fall, meant to cover Greek myth, myth generally and any genre not bound to a happy ending; untested until such a corpus is run |

**At step 4 the grammar accepts 80 of the 84 move-strings, ruling 48's target, and refuses only the four genuine counterexamples: 126 II, 127 I, 137 II and 138 III.**
The corpus was first met at step 3: 72 of 84, against v44's 69.
`runCorpus.py` runs a grammar over `ResolvedMoves.txt` with `falsify44.py`'s own derivation, so a changed verdict is the grammar's doing.
It was calibrated first: with v44 it fails exactly `falsify44.py`'s 15.
Step 3 frees exactly the three moves predicted before the run, 139 II by the exchange and 164 II and 166 II by T's instability.
Of the twelve still failing, eight carry licenses not yet built in (the pre-departure donor F in six, fight after pursuit in 93 III, the humorous inversion in 150 II) and four are genuine counterexamples; step 4 built the eight in, as predicted before its run.

**What the target cost in LL(1).** The domestic agent puts F in two places, and one token after C cannot tell whether a departure will follow, so F joins J as a conflict. Ruling 48 named this obstruction.
Step 5 removed the J conflict, which was a true ambiguity, by the repair v44's own comment names.
The F conflict cannot be removed while the father's agent and the donor's stay separate groups, for any lookahead: a run of F's belongs to one or the other depending on whether a departure follows the whole run. Only merging the two groups would remove it; changing the reading of p.108 alone would not.
**Step 6 made the merge, as decided, and the grammar is LL(1).** The split is now drawn at the test instead of at the departure: an F after D or E is the tested agent, the reward of the donor episode, and every other F is the untested agent, the father's gift or an agent that comes to hand on the road. The token before each F decides its group. The untested agent sits in the complication, on either side of the departure. The cost is a small widening: an untested agent may now be followed by a test, as in `A F D E`, which no page licenses and none forbids. No corpus verdict moves.

Moves are separated by `/`, and since step 7 a move may hold an inserted move, bracketed ⟨ ... ⟩.
The separator is editorial and follows Appendix III's layout of one row per move. It was adopted when step 2's frozen LL(1) test failed: without it, a move opening on B could not be told from a B inside the move before.

## Files

- `ProppEBNF46.txt`: the grammar, at its latest step.
- `StepTests.txt`: the frozen tests for every step written so far.
- `Step3Spec.txt`: the flat specification of step 3's move language, which the grammar is proved equal to.
- `runSteps.py`: runs them.
- `runCorpus.py`: runs a grammar over the resolved move-strings.
- `parseTree.py`: parses with the LL(1) table and reports where each function lands; `--corpus` writes the group counts.
- `CorpusGroups.txt`: those counts for the 80 accepted moves.
- `villainy.py`: the forms of villainy and what becomes of the villain, pinned by a test and cited in the catalog.
- `heroType.py`: which hero the tale follows, seeker or victim, read from B's variety digit by p.37, pinned by a test and cited in the catalog.
- `falseHero.py`: how the tales treat the false hero, pinned by a test and cited in the catalog.
- `agentForms.py`: how the hero receives the agent, tested or untested, by Propp's nine forms; its figures are pinned by a test and cited in the catalog's Measured lines.
- `SemanticCatalog46.md`: the catalog of v46's groups and pairs, checked against the grammar.
- `embedCorpus.py`: the whole-tale derivation with interruptions embedded, and its runner.
- The copied files listed above.

## Next session: start here

**State at the close of 2026-09-27: step 11, tagged `step11`, and nothing is half-done.**
ALL THREE OF RULING 48'S TARGETS ARE MET.
v46 accepts 80 of the 84 resolved move-strings, refusing only the four genuine counterexamples, 126 II, 127 I, 137 II and 138 III.
It is LL(1) with no conflict, and `regression.py` passes it outright.
It embeds moves: over the 45 whole tales of `embedCorpus.py`'s derivation it accepts 41, refusing the four tales that hold those counterexamples.
It states every license Propp grants on pp.107-108, the last, p.107's inverted sequence, added at step 9.
Of p.93's six methods of combining moves it expresses five: sequence, interruption, nested interruption, the common ending and the parting of two seekers. Method 4, two villainies at once, is not built, since its two A-K spans cross and no corpus case is identified.

**Run these first, with `PYTHONIOENCODING=utf-8` set, and check the figures.**
- `python runSteps.py 11` prints `156 binding, 0 failed, 0 pending for later steps, 34 closed by an earlier step`.
- `python embedCorpus.py --check` prints `CALIBRATED: 84 moves, 4 embedded`, and `python embedCorpus.py ProppEBNF46.txt` prints `PASS 41, FAIL 4`.
- `python parseTree.py ProppEBNF46.txt --corpus` reproduces `CorpusGroups.txt`.
- `python runCorpus.py ProppEBNF46.txt --start move` prints `PASS: 80` and `FAIL: 4`.
- `python regression.py ProppEBNF46.txt` prints `RESULT: ALL PASS`.
- `git tag` lists `step1` to `step11`.

### What is open, in order

**1. Review of the drafted meanings, continued.**
`SemanticCatalog46.md` separates three kinds of claim: **From Propp** (a page), **Measured** (counted by a program here and pinned by a test), and a **Cultural meaning** marked *Draft*, resting on a speculative reading set out in the catalog's section "A speculative reading, not from Propp".
Discussed on 2026-09-27, with the catalog revised to match: the princess and her father (the king assigns and grants, the princess chooses, the outcome is never in doubt), the donor, the helper, the false hero (the liar and scapegoat), the villain, and the hero (the one whose fortunes the tale follows, usually but not always the chooser).
NOT YET DISCUSSED: the dispatcher among the roles, and the drafted cultural meanings of the groups and functions generally.

**2. The parked area left of A.**
Step 9 built p.107's inverted sequence into the grammar but, under option 1, as decided, left the corpus derivation dropping the cells Propp parks left of A. Were they read in place, the eight regions the license fully covers would pass, and 139 I, 154 I and 155 III, each carrying an unlicensed G or W* beside licensed cells, would newly fail: 77 of 84 moves and 38 of 45 tales. The quarantine rests on a reading of Propp's table, not on a page. Still to be decided.

**3. `SemanticBundling.md`, in the first project.** Whether it points to this catalog or is replaced by it. It is part of the first project's publication, so a decision still to make.

**4. Optional work, none begun.**
- A TEST OF THE TRAGIC VARIANTS ON MYTH OR TRAGEDY. The 32 surviving Greek tragedies are a fixed corpus. Transcribe their function schemes and run v46 with `+tragedy,reversal`, freezing the prediction first. Fix in the derivation rules, before transcribing, WHOSE TALE each one is: Prometheus, Oedipus and Medea read differently depending on whose deeds count "for the hero" (p.81), and Prometheus is a punished villain from Zeus's side. Ideally the schemes are written by someone who has not seen the grammar.
- The Russian behind "various tempters" among Propp's partial helpers (p.82): the helper entry says it may mean skilled or wonder-working people, to be checked against the Russian.
- Propp's braces, repetition and branching, as grammar structure; today the runner expands them.
- Varieties, negative forms and variety binding, such as A¹ with a matching K: attribute-level, and v45C's territory rather than an order grammar's.
- The three interruption sites with dots and no numeral, 155 III, 155 IV and 167 I: a question for the page, since Propp prints no indication.
- Method 4, two villainies at once, set aside as an odd case: its A-K spans cross.
- A TALE GENERATOR, discussed on 2026-09-27. Skeletons are easy, by sampling v46 with weights from `CorpusGroups.txt` and a depth limit on interruption. Proppian skeletons need what v46 omits on purpose, since it is a permissive falsifier: v45C's pairs and dependencies, `AKCorrespondence.txt` and the D-F bindings for varieties, Appendix IV's inventory of what each variety means, and Appendix I with Ch. VI-VIII for the cast. Prose is a separate problem, by templates or a language model given the skeleton as a plan; Gervás's PropperWryter (2013) is prior work.

**5. Housekeeping.** This project has no remote; one can be created if wanted. The first project's publication for SourceForge is on hold.

### What the catalog now measures

Each finding is counted by a program here and pinned by a frozen test; the catalog carries it as a **Measured:** line.
- `agentForms.py`: an agent received at home is always given, made or bought (12 of 12); seizure comes only after a test (3 of 3), where Propp binds it to a hostile donor; an offer of service follows a test 7 times in 8.
- `agentForms.py --helper`: transference follows a received agent (37% against 22%); nothing else of the helper's does, and the corpus records no performers.
- `falseHero.py`: in all 5 tales where the false hero appears, his claim stands in the tale's last move, he is punished, and the tale ends in the wedding.
- `villainy.py`: abduction of a person is a third of all villainies and expulsion the second form; in villainy moves the harm is undone in 65% but punishment stands in only 20%. Propp gives punishment to the princess and her father as "punishment of a second villain" (pp.79-80).
- `heroType.py`: of the 32 tales carrying B, 26 follow a seeker and 3 a victimized hero (95, 98, 101), none both, as p.36 says; C stands in 27 of 30 seeker moves and 3 of 4 victim moves, less cleanly than p.38 says. It reproduces the first project's findings BM and BO.
- Of Propp's 31 function headings, 18 name the hero or the seeker and none the princess, her father or the king; p.81 defines characters by their deeds' meaning for the hero.

### Decided, so not re-opened

The move type is read at the opener, not the root. Moves are separated by `/`. The F groups are merged into the tested and the untested agent (step 6). α stands at the start of a tale only, on the reading of p.86 adopted at step 2. p.108's seven-never-together is left out. Step 6's widening, an untested agent before a test, is accepted as the cost of the merge. p.108's exchange follows finding FN's reading. The inverted sequence follows option 1. Tragedy, the Dundes consequence tale and the fall after success ship commented out; success before a reversal is a matter of perspective and is not required. The dramatis personae are roles for now, ordered by rank on a speculative reading. No interpretive reading, and no decision, is attributed to a person in this project's files.

### Done on 2026-09-27

- Steps 1 to 11, tagged, in the table above: all three of ruling 48's targets met, every license of pp.107-108 stated, five of p.93's six methods of combining moves expressed, v43's two genre extensions overlaid, tested and commented out, and a second tragic variant, the fall after success, likewise.
- `parseTree.py` and 55 tree tests; `CorpusGroups.txt`.
- `SemanticCatalog46.md`: 32 groups and pairs, 32 functions, 2 unnumbered elements, the extensions, and 7 dramatis personae, each with literal and cultural meaning, and nine entries with measured findings; kept in step with the grammar and the corpus by frozen tests (`catalog`, `catalogfunctions`, `catalogmeanings`, `catalogspheres`, `catalogmeasured`, and the pinned figures of `agentforms`, `helperafteragent`, `falsehero`, `villainy`, `herotype`).
- `embedCorpus.py`, the whole-tale derivation, calibrated against `resolve.py`.
- `agentForms.py`, `falseHero.py`, `villainy.py` and `heroType.py`, the measuring programs.
- `equivCheck.py` gained `--drop-a` and `--drop-b`, so this copy differs from the first project's; `runSteps.py` reads `TAG:FILE`, `FILE+NAME` and `FILE@START`; `runCorpus.py` and `runSteps.py` fall back to the LL(1) parser for a recursive grammar.
- In the first project, from this work: findings FR to FZ, ruling 104, two corrections to v43's comments, and the published files cleared of any mention of a person.

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

**A tool that no binding test exercises can break silently.** `runCorpus.py` failed on v46 from step 7 to step 9, and this handoff claimed it printed `PASS: 80`, because the move-level corpus tests had closed at step 6. Now the two corpus runners have health-check tests binding at step 11, which must be re-frozen at each new step. `regression.py` and `parseTree.py --corpus` have no test: check them by hand, as the checklist says.

**Check that a new test can fail.** Each new test kind this session was run against a deliberately broken copy before it was trusted.

**Extensions switch on in a copy.** Lines beginning `#+NAME ` are an extension and lines ending `#-NAME` the default it replaces; `FILE+NAME` in a test switches them on in a temporary copy, and `FILE@START` parses from another root.

**A stray `cat` with no input blocks a Bash command until it times out.** Stop it and confirm nothing was half-applied before retrying.

**Write a catalog test and its text in separate steps, and run the test red in between.** Twice on 2026-09-27 a test and its text went in one script, so the test was never seen failing; each was then checked against a broken copy, but the order was not test-first.

**Do not chain unrelated commands before an environment setting.** A failing `git stash` ended a chain before `PYTHONIOENCODING` was exported, and the run crashed on printing, which looked like a test failure until it was read.

**Keep the three kinds of claim apart in the catalog.** From Propp, Measured, and a drafted cultural meaning are labeled differently, and only the first two are evidence.
