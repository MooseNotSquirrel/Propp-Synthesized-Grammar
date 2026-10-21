# The normalized data set: plan, session by session

**Drafted 2026-10-21 at the owner's request, against `DataProtocol.md` with its four decisions taken.** The work is cut into sessions that each end with everything committed and pushed, so that any session can stop at its close and the next can start cold. Each session begins by reading this file and `KeeperLog.md` in this folder, and ends by adding one dated entry to `KeeperLog.md` and levelling `ProppQueue.md`'s START HERE block.

**Budget.** Sessions 1 to 4 and 6 are program work: no reader stages and no subagents, so they are cheap. Session 5 runs analyses already written. Only session 7 runs reader stages, and it is the one to schedule when the weekly budget allows.

## Session 1: freeze the tests, then the story, event and function tables

1. Bring `DataProtocol.md` section 5 (T1 to T4) to the owner and freeze it at the owner's word, with the commit named in `KeeperLog.md`. Nothing below starts before that.
2. Write `Data/build.py` for `stories.tsv`, `events.tsv`, `functions.tsv`, `aliases.tsv` and `census.txt`, reading the six function corpora (wondertales on both cards, animal tales, both fable repositories, tragedy, myths) and Propp's own codes.
3. Run T1 and T4 on those tables. A failure is attributed and recorded before anything is changed.
4. **Done when:** the three tables are built, T1 and T4 pass on them, and the census is committed.

## Session 2: the description tables

1. Extend `build.py` to `acts.tsv`, `significance.tsv`, `problems.tsv`, `free.tsv` and `heroes.tsv`, from Propp-ActsRoles and the hero files, mapping describer B's `S00n` plays through `aliases.tsv`.
2. Run T1, T2 and T4 on every table.
3. **Done when:** all nine tables are built and T1, T2 and T4 pass.

## Session 3: the table-backed reader, and the first three programs

1. Write `Data/tables.py`, one reader of the tables with filters for corpus, reader, card and version.
2. Move `Model/model.py`, `Links/links.py` and `Ngrams/ngrams.py` onto it, each on its own commit, and run T3 for each: its run file must come out byte for byte the committed one.
3. **Done when:** those three pass T3, or each difference is attributed in a finding.

## Session 4: the rest of T3

1. Move `Problems/problems.py`, `Free/free.py`, `Heroes/heroes.py`, `Animal/animal.py`, `Animal/agreement.py` and `Animal/layers.py`, and run T3 for each.
2. **Done when:** all nine programs of T3 pass, or each difference is attributed. From here, by decision 4, new programs read only the tables.

## Session 5: parity on the data that exist

1. Freeze, before running, what each run on a new corpus predicts or is only reported, as with every other test.
2. On the animal tales, compared with the wondertales on the corrected card `C` (decision 3): the pairs as n-grams, the links, the blocks, the spheres of action and the values.
3. On the myths, with the data they have: the pairs as n-grams and the blocks beyond their order.
4. **Done when:** every analysis in `DataProtocol.md` section 2's second table has a row of results for every corpus with the layers it needs, or the cell says why not.

## Session 6: the parity report

1. Write `Data/Parity.md`: the two tables of `DataProtocol.md` section 2, regenerated from the tables, and what each new run found.
2. Write the results into `PreliminaryFindings.md` and `Process/Chronology.md`.

## Session 7, when the budget allows: the reader stages

1. **The animal tales' heroes by two readers:** 50 stories, one stage, set up as `hero-1` and `hero-2` were.
2. **Tragedy, acts and significance for P01 to P08:** two stages, set up as `p-acts` and `p-sig` were.
3. Each stage is cleared only after its test is frozen. Each is merged, put in form, built into the tables, and the parity report is regenerated.

## Not in this plan, by decision

Further description of Apollodorus (decision 1), and the 108 fables beyond the 90 described (decision 2).
