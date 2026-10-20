# The frozen models' predictions for Afanasyev's animal tales: the test

**Drafted 2026-10-20, not yet frozen; to be frozen at the owner's word, before any animal tale is transcribed.** Once frozen, a departure is logged in `Animal/KeeperLog.md`, not made here.

## The question

The joint model (`Model/`) tells the four genres measured so far apart on stories it has not seen, and is to be the base for placing each new corpus before it is described in any other way.
Afanasyev's animal tales are the first new corpus: the fifty numbers that open his collection, which Propp left out, and the in-family comparison for Dundes's North American tales, most of which are animal tales.
This test asks the frozen instruments, before any animal tale is transcribed, four things: where the joint model places the animal tales; whether their tricksters fuse the hero's and the villain's spheres (`Spheres/`); whether their trouble is put right (`Links/`); and whether the tight pairs hold in them (`Links/`, `Genre/`).

## The tales and their transcription

**The tales:** A001 to A050 in Propp-AnimalTales (`tales/`), in Russian, with their event lists and heroes (`Events.txt`, `Heroes.txt`: 1,283 events, a hero for each tale), listed under the calibration's event-listing rules with no mention of Propp.
**The transcription, set up after the freeze:** the tales transcribed under Propp's functions by transcriber A (Opus) and transcriber B (Sonnet), reading the Russian, under the calibration's rules with the definitions card corrected for refusals (`AfanasyevRules-C.md` in Propp-Afanasyev: a refusal is not θ), the card decided on before any new corpus; the calibration found the correction changes nothing measurable, so the transcriptions stay comparable with the uncorrected ones the model was fitted on.
Each transcriber is given the event lists and heroes, as in the calibration; the tales are split into batches as the calibration split its 45.
The stage runs in Propp-ActsRoles (`animal/`), where cloud sessions open, and the transcriptions are copied to Propp-AnimalTales as `transcriptions/A/bN/Notes.txt` and `transcriptions/B/bN/Notes.txt`, in the calibration's format, the function in the fifth field.
**A note for the scorer:** the animal tales are A001 to A050 and the wondertales A093 to A167; `animal.py` reads the animal tales from Propp-AnimalTales alone, so the shared prefix cannot mix them.

## What is already known

**The listing stage's form, nothing of the tales' structure.** The keeper who checked the event lists saw their form (events numbered without gaps, a hero for each tale, 6 to 52 events a tale); the keeper who drafted this protocol read neither the event lists nor the heroes.
**No instrument has been run on the animal tales.** The joint model has never placed a corpus outside the four genres it was fitted on.
**The reasons below draw on the published description of the animal tale**, not on these tales: the animal tale is short, often built on a trick, often led by a trickster (the fox), and often a chain of encounters; the folklorists' type index keeps it apart from the wondertale, in a class of its own (types 1 to 299), and it is the fable's near kin. That description is what the predictions test against the instruments.

## The instruments, unchanged

**The joint model:** `Model/model.py` as frozen at 3ce7a3c, its features (the lexicon, the relations, the order, what lies outside), its settings (a multinomial logistic regression, features standardized, L2 penalty 1.0, classes weighted to their sizes) and its floor (stories of at least 3 of Propp's functions).
It is fitted on all the stories of the four genres, transcriber by transcriber, since the animal tales are the held-out set; each animal tale of at least 3 functions is placed in the genre the model gives it.
Length stays out of the model, as frozen.
**The spheres:** `Spheres/explore.py`'s reading, as committed at e3830c4 (each function credited to the character who performs it, names matched within a story), in its strict form: the hero's sphere is C, ↑, E and W, the villain's sphere villainy (A) and pursuit (Pr), struggle left out because transcribers credit it to whoever fights.
A story fuses the two when one character performs functions of both.
**The links:** `Links/links.py` as frozen at 0f36a91: for a link, the share of moves holding the first function in which the second stands after it in the same move; a link holds when the first stands in at least 5 moves, the lift over the corpus's functions shuffled across its moves (10,000 shuffles, seed 46) is above 1, and p is at most 0.05.
The animal tales' moves are read as `Links/` reads the wondertales: each entry as its function's letter, X and α left out, a negative result counted as its function.
**The comparison corpora** are those the instruments were frozen on: the 45 wondertales (Propp-Afanasyev, arm U), the fables (Propp-Aesop and Propp-Fables), the tragedies and the myths, each transcriber apart; every comparison figure is computed by `animal.py` at scoring, not taken from an earlier run.

## The predictions

1. **The frozen model places more animal tales as fable than as any other genre**, for both transcribers.
2. **One character holds both the hero's and the villain's sphere** in a larger share of the animal tales than of the wondertales, for both transcribers, with a one-sided permutation test (the story labels shuffled between the two corpora 10,000 times, seed 46) giving p at most 0.05.
3. **The animal tales' trouble is seldom put right:** villainy or lack is followed by liquidation in a share of animal-tale moves below the midpoint of the wondertales' share and the fables' share, for both transcribers.
4. **The core holds:** of the tight links (struggle to victory, task to solution, pursuit to rescue, false claim to exposure) whose first function stands in at least 5 animal-tale moves for both transcribers, all but at most one hold for both. If fewer than two links are common enough, the prediction is reported NOT TESTED.

Each is reported HOLDS, FAILS or NOT TESTED.
**The frozen instruments place the animal tales as predicted** if all four hold.

## The reasons, the keeper's

**For the first:** the joint model reads a story's devices and relations, not its culture or its collection. The animal tales share the wondertales' collector, language and tellers and the fables' matter and scale. If the model places them with the fable, a genre's settings follow its matter and form of telling more than the tradition it is told in; if with the wondertale, the tradition shapes the structure. The in-family answer is the baseline the Dundes comparison needs.
**For the second:** the trickster is both the one the tale follows and the one who does the harm. The fable already follows its villain (it fills the villain's sphere about twice as often as the hero's), but its villain seldom holds the hero's functions (3% to 4% of fables); tragedy's hero commits the villainy in two thirds of plays or more. If the animal tale's trickster is credited with both, the fusion is a setting of its own, apart from the fable's.
**For the third:** the trickster's victim is seldom made whole, and the tale often ends on the trick. The threshold sits between the two genres the animal tale is drawn between, not merely below the wondertale.
**For the fourth:** the tight links held in every genre measured, myth included; an in-family genre that broke them would be the first.

## Checked before the freeze

`animal.py selftest` runs the whole scorer with stories of a known genre standing in for the animal tales: the model fitted on the fitting half of the four genres, the stand-ins drawn from the held-out half and removed from the comparison corpora, links shuffled 1,000 times.
**Held-out wondertales standing in** (22 for each transcriber): predictions 1, 2 and 3 fail, as they must when the stand-ins are wondertales (placed as tale 11 and 15 of 22; fused in 18% and 41% against 17% and 17%, p 0.62 and 0.09; liquidation 42% and 41% against midpoints of 27%); prediction 4 holds.
**Held-out fables standing in** (52 for each transcriber): predictions 1 and 3 hold (placed as fable 32 and 38 of 52; liquidation 17% and 15% against midpoints of 28%); prediction 2 fails (fables seldom fuse the two spheres); prediction 4 is NOT TESTED, only struggle to victory being common enough.
**Two faults the self-test found, mended before this draft:** the comparison model of length alone read every feature, an empty list of feature groups falling through to the default; and the second prediction, first drafted as a bare comparison of shares, passed with the wondertales standing in for B (41% against 17%, on 22 and 23 stories), so it now needs a permutation test.

## Reported, not judged

For each transcriber: the animal tales of fewer than 3 functions, left out; the placement by the model with length added, by length alone, by the lexicon alone and by the relations alone; the fused share in the fables; every tight link's figures; and the wondertales' and fables' liquidation shares from which the midpoint is drawn.

## Not in this test

The acts, the significance layer and the free verbs (`Problems/`, `Free/`) are not run on the animal tales here; whether the hero opens the problem, and whom the acts help, wait for a stage of their own.
