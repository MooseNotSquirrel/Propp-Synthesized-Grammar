# The genre model's predictions for myth: the test

**Frozen 2026-10-19 at the owner's word, before any link is counted on the myths.** Once frozen, a departure is logged in `Genre/KeeperLog.md`, not made here.

## The question

`GenreModel.md` states a model: one shared core of relations between acts, and a genre as a setting of a few parameters on it.
A model that only summarizes the genres it was drawn from cannot fail. This test asks it to say, before measuring, what a fourth genre will look like: Greek myth, as Apollodorus's Library tells it, already transcribed under Propp's functions for an earlier test and never used in the work the model rests on.

## What is already known of the myths

The earlier test (`Apollodorus/ApollodorusResult.md`) measured coverage, acceptance by the grammar, and order against Propp's, and the keeper has read its results. The predictions therefore use none of those; they use the links at a distance, which no one has measured on the myths.

## The moves

The Apollodorus transcriptions (Propp-Apollodorus, `Apollodorus/transcriptions/A` and `B`, nine batches each), read by their moves as `Links/` reads the other genres: each entry as its function's letter, X and α left out, a negative result counted as its function. Read but not measured: A 303 moves, 1,189 functions; B 261 moves, 1,401.
The other genres are read as in `Links/`.

## The statistic

As `Links/LinksProtocol.md` freezes it, unchanged: for a link, the share of moves holding the first function in which the second follows; a link holds when the first stands in at least 5 moves, the lift over functions shuffled across moves is above 1, and p is at most 0.05.

## The predictions

1. **The core holds in myth.** Of the tight links (struggle to victory, task to solution, pursuit to rescue, false claim to exposure) whose first function stands in at least 5 myth moves for both transcribers, all but at most one hold for both.
2. **Myth's frame closes less often than the tale's.** Villainy or lack is followed by liquidation in a smaller share of myth moves than of tale moves, for both transcribers.
3. **Myth is set like tragedy.** On the frame shares (villainy or lack to liquidation, departure to return, test and reaction to the gift, each used where its first function stands in at least 5 myth moves for both transcribers), myth's profile lies nearer tragedy's than the tale's or the fable's, by the plain distance between the shares, for both transcribers.

The reason for the third: the tragedies dramatize the same myths, and the model holds that a genre is its settings, not its matter; if myth sits nearest tragedy, the settings travel with the matter, and if not, the genres are set by their form of telling.
Each is reported HOLDS or FAILS; the model passes this test if all three hold.

## Checked before the freeze

`myth.py score` run with the tale moves standing in for the myths, fewer shuffles: the core holds, prediction 2 fails as it must when the two are the same, and the stand-in lies nearest the tale at distance 0.

## Reported, not judged

Every link in myth and the three genres, both transcribers.
