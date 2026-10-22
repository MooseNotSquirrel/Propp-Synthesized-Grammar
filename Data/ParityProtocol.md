# Parity runs on the data that exist: protocol (FROZEN 2026-10-21 AT THE OWNER'S WORD, AS DRAFTED)

**Drafted 2026-10-21 for `Plan.md` session 5, under the parity rule** (`DataProtocol.md`, decision 4): an analysis is not done until it has run on every corpus that has the layers it needs. Two corpora have layers that some analyses never read: the animal tales (every layer, but never the n-grams, the links beyond pursuit and rescue, the blocks, the spheres or the values) and the myths (functions only, never the n-grams or the blocks beyond their order). Nothing below has been run on them. The predictions are written before any run, and each is scored HOLDS or FAILS, with no overall verdict.

## What is run, and how

**Every run reads only `Data/tables/`, and reuses the original analysis's program and thresholds unchanged.** Seed 46 throughout. Each analysis is run on the new corpus and, beside it, on the wondertales read the same way, so that the comparison the owner asked for stands in one file.

- **The animal tales are compared with the wondertales on the corrected card `C`** (decision 3), both transcribers. Where an analysis has published wondertale figures on card `U`, those stand as frozen and are not changed; the `C` figures are new and reported beside them.
- **The myths are read as the joint model reads them:** the `L` units only (the Epitome's `E` units were never part of any myth analysis), each story's first reading.
- **A result file per run**, `Data/Parity/<analysis>-<corpus>.txt`, and one summary, `Data/Parity.md` (session 6).

## The predictions

**The n-grams** (`Ngrams/`, its confirmation half and its frozen candidate list `Candidates.txt`, unchanged; the new corpus was in no discovery half, so all of it serves as confirmation):
1. **Animal tales, functions:** at least half of Propp's pairs that occur at least 5 times, adjacent or near, for both transcribers, are confirmed (Ngrams prediction 1).
2. **Animal tales, acts:** at least half of their counterparts, so counted, are confirmed among the acts (Ngrams prediction 2).
3. **Animal tales, both layers:** the next token is more predictable than in shuffled strings, for both layers and transcribers (Ngrams prediction 4).
4. **Myths, functions:** predictions 1 and 3 above, on the myths' functions.

**The links** (`Links/`, its statistic, shuffles and the rule that a link is tested only where its first function stands in at least 5 moves):
5. **Animal tales:** every tight link tested (struggle and victory, task and solution, test and reaction and the gift, pursuit and rescue) holds, for both transcribers. Pursuit and rescue was found holding in the animal test; this runs the others where they are common enough, and says so where they are not.
6. **Reported, not predicted:** the frame links in the animal tales (villainy or lack and liquidation, departure and return), beside the wondertales on card `C`.

**The blocks** (the block analysis of `PreliminaryFindings.md` section 2, its programs unchanged):
7. **Animal tales:** Propp's blocks' halves are told together more often than chance, for both transcribers, as in every genre measured so far.
8. **Myths:** the same.
9. **Reported, not predicted:** which genre's block order fits the animal tales best (`Blocks/GenreOrder.md`'s measure), because their placement already splits by transcriber (`Animal/AnimalRun.txt`).

**The character sets and the values, reported only, as their first looks were** (`Spheres/explore.py`, `Values/explore.py`, exploratory, not frozen tests):
10. **Spheres of action** in the animal tales, beside the wondertales on card `C`: which spheres occur, and how often one character holds two.
11. **Values** in the animal tales from their significance layer: whom pleading, deceiving and harming help.

## Checked before the freeze

**To be done before the owner freezes this, and recorded here:** each program runs on the new corpus without error on a dry run that prints only counts (stories, moves, tokens per transcriber), no result; and a self-test of each new corpus argument, on the wondertales on card `U`, reproduces the published figures byte for byte.

## Not run, by decision

The 108 fables beyond the 90 described (decision 2), and Apollodorus beyond its functions (decision 1).
