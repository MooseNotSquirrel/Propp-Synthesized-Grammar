# The animal tales' problem structure, in acts and their significance: the test

**Drafted 2026-10-20, before any animal tale is described in acts, significance or free verbs; not yet frozen.** Once frozen at the owner's word, a departure is logged in `Animal/KeeperLog.md`, not made here.

## The question

The problem-structure test (`Problems/`) found that the wondertale, the fable and the tragedy differ in how their problems are opened and solved, measured in the catalog of role-free acts and the significance layer, beyond what the stories' length gives.
The animal tales' own test (`AnimalProtocol.md`) used Propp's functions only, and left this layer for a stage of its own: whether the hero opens the problem, and whom the acts help.
This test asks whether the animal tales are set like the fable against the wondertale on those measures, the trickster hero opening the trouble and the acts working against the hero, or like the wondertale they share a collector, language and tellers with.

## The tales and the stages

**The tales:** A001 to A050 in Propp-AnimalTales, with their event lists and heroes (`Events.txt`, `Heroes.txt`), the material the transcription stage used.
**Three cloud stages in Propp-ActsRoles,** each in a fresh session, describers A (Opus) and B (Sonnet), in the transcription stage's three batches (A001 to A017, A018 to A034, A035 to A050):
1. `animal-acts`: the acts, under `ActsRules.md` unchanged; output `animal/acts/<A or B>/<batch>/Notes.txt`.
2. `animal-free`: the acts in the describers' own verbs, under `free/FreeRules.md` unchanged; output `animal/free/<A or B>/<batch>/Notes.txt`. It needs nothing from the first stage and may run beside it.
3. `animal-sig`: once the keeper has checked the acts' form and written the inputs (`layers.py setup-sig`), the significance layer, under `sig/SigRules.md` unchanged, by fresh describers of the same letter, in five batches of ten tales; output `animal/sig/<A or B>/<batch>/Significance.txt`.

No describer opens the transcriptions, and none opens another stage's output.
After each stage is merged and in form, its results are copied to Propp-AnimalTales.
**One departure from the problem test:** its describers were told the hero two hero readers agreed on (`Heroes/`); the animal tales have no such reading, and the hero line is the event listers' (`Heroes.txt`), the hero the transcribers were also given.

## The instrument, unchanged

The problem test's seven measures, its null and its permutation test, as `Problems/problems.py` froze them: each story scored by its excess over 200 random descriptions of its own acts, the hero's part, value and place drawn together from the describer's pooled descriptions and the problem label from the story's own labels, seed 46.
**The comparison stories** are the problem test's: its 22 wondertales, 41 fables and 16 tragedies, with their descriptions as they stand.
The animal tales join the pool the null draws from, so the comparison stories' excesses move slightly from the published figures; every figure is computed again at scoring.

## The predictions

For each, both conditions must hold for both describers:
the animal tales' mean excess differs from the wondertales' in the predicted direction by at least 0.05, with a one-sided permutation p (genre labels shuffled between the two, 10,000 times) at most 0.05;
and the animal tales' own mean excess points the same way by at least 0.05, with a one-sided sign-flip p (10,000 flips) at most 0.05.

1. **The hero opens the problem** more often than in the wondertale, and more than the null gives.
2. **The problem is repaired** less often than in the wondertale, and less than the null gives.
3. **The acts help the hero** less than in the wondertale, and less than the null gives.
4. **The acts harm the hero** more than in the wondertale, and more than the null gives.

Each is reported HOLDS or FAILS.
**The animal tale is set like the fable** if all four hold; **in part** if two or three hold, naming which; **not shown** if fewer than two hold.

## The reasons, the keeper's

The published description of the animal tale makes it the fable's near kin: short, built on a trick, often led by a trickster who is both the one the tale follows and the one who does the harm.
The fable's hero opens its problem and its acts work against the hero, beyond what length gives; the wondertale's hero answers a harm done by another, and its acts help.
The second prediction is the one the transcription test already bears on (villainy or lack liquidated in 25% and 19% of moves, below the tale-fable midpoint), measured here by another instrument.

## Checked before the freeze

`layers.py selftest` (`LayersSelfTest.txt`):
**The problem test's 41 fables standing in for the animal tales:** predictions 1, 3 and 4 hold and 2 fails, since the fables repair about as often as their length gives (own excess -0.01 and +0.12).
**Random descriptions standing in** (the wondertales' acts with part, value and place drawn from the pool): none of the four holds.
**Two faults the self-test found, mended before this draft:** the first draft compared the animal tales with the wondertale alone, and random descriptions passed all four comparisons, because the wondertale is far from random and anything random differs from it; each prediction now also needs the animal tales' own excess. And a fifth prediction, that the hero deceives or harms in more animal tales than wondertales, was dropped: the wondertale's hero does so in about four in five tales (the fight with the villain is a harm), and random descriptions do so in 95%.
**The stages' plumbing,** on synthetic descriptions in a scratch folder: the readers, the form checks, the significance inputs and the free-verb report run end to end.

## Reported, not judged

Every measure per genre and describer, raw and excess; the trickster, as the mean share of the hero's own acts that are deceiving (in the self-test, 0.09 in the wondertales, 0.05 to 0.06 in the fables); the describers' agreement on the layer.
**The free verbs:** the bottom-up test's measures on the animal tales alone, whether a verb keeps apart the halves of the six pairs and of the request and its answer, and the pairs of verbs found and confirmed.
They carry no prediction: fifty short tales are a small fraction of what the bottom-up test read, and its discovery thresholds were set for that size, so a failure here could not be told from too little material.
