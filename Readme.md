# SynthesizedProppGrammar

**This is the second project that ruling 47 of Propp Grammar Test Cases split off.**
It begins from copies of that project's files and is not governed by its rulings.
Its question is what structure and meaning a grammar of Propp's folktale can carry once the licenses he grants in prose are built into it, rather than applied afterward.

**It began on 2026-09-27 from Propp Grammar Test Cases at commit 0f27783.**
Six files were copied unchanged: `ProppEBNF44.txt`, `ProppEBNF43.txt`, `ProppMidLevelGroupsEbnf.txt`, `parse.py`, `equivCheck.py` and `regression.py`.
Others are copied when a step needs them, and each copy is recorded here.

## Method: test first, one step at a time

**Every step is labeled language-preserving or language-changing before it is built.**
A language-preserving step adds structure and no strings, and its test is equivalence to the grammar before it.
A language-changing step adds or removes strings, and its tests are written and frozen first, each citing the page it rests on.

**The tests live in `StepTests.txt`, and `runSteps.py` runs them.**
`python runSteps.py N` runs every test for steps 1 to N, and counts the tests for later steps as pending.
A test is never edited to fit a result: a test found wrong is commented out with a dated reason, and its correction is added below it.

**`equivCheck.py` is the proof instrument.**
It decides whether two grammar files accept the same strings, and prints a shortest string on which they differ when they do not.
It handles grammars whose productions do not refer back to themselves, which covers every step until interruption is taken up.

## Steps

| step | kind | grammar | state |
|---|---|---|---|
| 1 | language-preserving: v44 regrouped into Propp's pairs and groups | `SynthesizedGrammar01.txt` | built; 2 of 2 tests pass |
| 2 | language-changing: the tale layer, a preparatory section and then sequential moves | `SynthesizedGrammar02.txt` | tests frozen; two questions open for the owner |
| 3 | language-changing: p.108's exchange of recognition, exposure, marriage and punishment | `SynthesizedGrammar03.txt` | tests frozen on FN's reading |

Moves are sequential for now; embedding is a later step.

## Files

- `SynthesizedGrammar01.txt`: step 1.
- `StepTests.txt`: the frozen tests for every step written so far.
- `runSteps.py`: runs them.
- The six copied files listed above.
