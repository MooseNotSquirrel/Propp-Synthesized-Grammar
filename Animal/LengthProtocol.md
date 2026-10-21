# Whether transcriber A's placement of the animal tales follows from how much A marks: the test

**Frozen 2026-10-20 at the owner's word, as drafted, after the animal tales were scored and before the length-matched placement was run.** Once frozen, a departure is logged in `Animal/KeeperLog.md`, not made here.

## The question

The frozen joint model placed B's animal tales as fable (25 of 48) and A's as tale (26 of 48), so the first prediction of `AnimalProtocol.md` failed.
A check made afterward (`AgreementCheck.txt`) found that A and B agree on these tales about as well as on any corpus, but that A marks a third more of Propp's functions in each tale (10.2 against 7.6), where on every other corpus they are within a fifth of each other.
The keeper's reading was that the split follows how much each transcriber marks, not what each reads the tales as.
This test asks that directly: placed again with A's transcriptions cut down to B's, are A's animal tales placed as fable?

## What is already known

**Everything the frozen score printed, and the agreement check.**
The data are seen, so this test cannot confirm the keeper's reading the way a test on unseen stories would; what it can do is fail it.
It is frozen so that the arms, the draws and the criterion are fixed before the placement is rerun.

## The instrument, unchanged

The joint model as `animal.py` uses it (`Model/model.py` at 3ce7a3c), fitted on all of transcriber A's stories of the four genres, its floor of 3 functions kept.
Each animal tale is read as `animal.py` reads it, the first reading only.

## The two arms

1. **Thinned:** each of A's tales with more of Propp's functions than B's transcription of the same tale is thinned to B's count, function entries removed at random, X entries and the order of what remains kept; 100 draws, seed 46.
2. **Shared events:** each of A's tales keeps only its function entries on events where B also wrote one of Propp's functions.

The first removes quantity and nothing else; the second removes the events only A marked.

## The predictions

1. **Thinned to B's count, A's animal tales are placed as fable ahead of every other genre in at least 51 of the 100 draws.**
2. **Kept to the events B also marked, A's animal tales are placed as fable ahead of every other genre.**

Each is reported HOLDS or FAILS.
**If both hold,** the split on placement is a matter of how much A marks.
**If only the second holds,** it is a matter of which events A marks, not how many.
**If neither holds,** the split is not explained by A's extra entries, and the keeper's reading is withdrawn.

## Checked before the freeze

`lengthCheck.py selftest` (`LengthSelfTest.txt`) runs without the animal tales' placement:
**The plumbing:** A's tales thinned to their own count reproduce the frozen placement exactly (tale 26, fable 12, tragedy 3, myth 7).
**Whether thinning alone makes a fable:** held-out stories of known genre, the model fitted on the other half, thinned to lengths drawn from B's animal tales, are placed as fable ahead of every other genre in 2 and 15 of 100 draws for the wondertales (A and B), 0 and 4 for the tragedies, 0 and 0 for the myths.
Thinning alone does not turn a story into a fable, so the first prediction can tell.

## Reported, not judged

The unthinned placement; the placements summed over the draws; B's tales kept to the events A also marked, placed by B's own model.
