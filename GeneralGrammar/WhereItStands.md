# Where it stands (written 2026-11-05, to pick up on Sunday night, 2026-11-08)

**The decision waiting for the owner:** pairs on real strings with close pairs only, spanning left for later (the keeper's recommendation), or fix spanning first. Nothing runs until then.

## The aim, in the owner's words

A model that adapts to each corpus to give its internal structure, retrieving Propp's from his corpus without forcing Propp on others. Stepwise refinement means the largest and most basic item first, then up the tree: leaves (functions plus candidates, from verbs and acts), pairs with distance, groups, order inferred and floating. V46 is the regular language with the shape of V43, a flat model presented mostly as a tree; a tree of that kind, per corpus, is what is sought. The owner wants pushback when the keeper disagrees.

## What is established

| Step | File | Result |
|---|---|---|
| The self-test audit | `Induction/AuditReport.md` | FAILS stands. S1 real, S2 could not pass, S3 a design choice |
| The order tool, `grammar.py` v3 | `Versions.md`, `Rung2-v3.txt` | Given his functions, retrieves his order from his strings (tau 0.984); two bars missed (relation tau narrowly, moves 0.661 against 0.835) |
| The leaves | `LeafReport.md` | "A reasonable answer" NOT met (63%, 59% against 80%). Verb a fifth of the ceiling, significance adds most, no thesaurus beats the act. Clustering does not recover functions (AMI about 0.2). Tragedy's X events yield threats, curses, prayer, begging, vows, lament |
| The neutral card | `CardPilotReport.md` | Wondertale order survives (A survives, B in part), but readers recognized Propp |
| Events coded apart | `ShuffledReport.md` | Wondertales in the events (0.575, 0.563); East Asian A in the events (0.695), B in part (0.440); **tragedies: the test says no (0.117, 0.243)**, clear in A, same direction in B |

**What that adds up to.** The order is not written in by the card or by reading in sequence, and the labels do not bring it regardless of story. Corpora differ. Trickery stands mid-tale even coded alone, as the owner said. Still open: how far it is Propp's order or a logic of tales in general; readers' knowledge of what each function means stays built in; functions cannot yet be recovered bottom-up.

## Pairs, where the work stopped

`PairsProtocol.md` is frozen, with tools `pairs.py` and `pairsRung1.py`; the results are at the end of `Versions.md`. No real string has been read.

- **Version 3:** close pairs found (median 0.50; bar 0.29), about 2 false a corpus; scrambled Propp never read as Propp; random strings 0.1%.
- **Rung 1 fails on spanning pairs:** 20% of corpora at the gate, need 80%. A-K never found. Where x is nearly universal, dependence cannot show.
- **Two departures from the frozen rules, recorded in `Versions.md`, for the owner's eye:** the pass rule (p at most 0.05 on both halves, in place of the false discovery rate), and the spanning gate (C-W and G-U only).

**If close pairs only:** record the decision in `PairsProtocol.md`, write a rungs 2 to 4 program over `pairs.py`, run his strings first, the readers', the other corpora and the acts, then order, floating and overlap among pairs. Spanning reported as unverified. No readers.

**If spanning first:** the likeliest route is measuring direction within the passes `grammar.py` infers.

## Practical

- **Repositories, all pushed:** SynthesizedProppGrammar (`SemanticCatalog.md` there is the owner's uncommitted work, never staged), RegularProppGrammar (queue, closeout), Afanasyev, ActsRoles untouched by the pilot's part 2, TaleCoding (private, `C:/Users/Steve1/TaleCoding`, neutral: **the keys live only in `GeneralGrammar/PilotKey.json`, `ShuffledKey.json`, `TragedyKey.json`**).
- **Set up, not run:** the pilot's part 2, cell H's prompts in `GeneralGrammar/PilotH/`, should it ever be wanted.
- **Downloads outside the repositories:** Moby at `C:/Users/Steve1/moby_thesaurus`; VerbNet at `C:/Users/Steve1/nltk_wordnet`, unused, as its package shows no license.
- **A stale cache caught once:** `leaves.py` keeps a pickle in the system temp folder and now checks story counts on load.
- **Running a reader stage:** a cloud session on the repository, its brief saying only to follow `RUN.md`; the app does not say when one ends, so the owner pastes the runner's reply. Merge by fast-forward after fetching the stage's branch.
- **Closeout after commits:** in RegularProppGrammar, `python manifest.py`, then `python checkMirror.py -v`. Use `PYTHONIOENCODING=utf-8` and `PYTHONHASHSEED=0`.

## Cost: the keeper's estimates are not to be trusted

| Stage | Points of the budget |
|---|---|
| Pilot part 1: 4 readers, whole tales | about 60 |
| East Asian coded apart: 12 subagents, 376 lines | 26 |
| Tragedies coded apart: 12 subagents, 480 lines, with setup | 18 |

Event count does not predict cost. The budget reset on about 2026-11-04; the last figure was 47% used, 53% left, before the pairs work. Pairs needs no readers.

## Later in the queue, unchanged

Step 6 (`StoryModels/StructureProtocol.md`, frozen; its E2 prediction is no longer fully blind). Step 7: card D and the story grammar's version 2, which should now answer to this work: the frozen grammar's features are Propp's sections and pairs. Step 8: CrossCulture and new corpora. To check: how far the ten sections are Propp's own. The move rule and content labelling of preparatory functions go to card D.
