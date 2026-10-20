# One model of the genres: the test

**Frozen 2026-10-20 at the owner's word, before any story is fitted.** Once frozen, a departure is logged in `Model/KeeperLog.md`, not made here.

## The question

The studies so far measured the story language's parts one at a time: which devices a genre uses, how its pairs and long links are completed, how it orders its blocks. This test joins them in one model and asks whether, together, they tell the genres apart on stories the model has not seen.
If they do, the model is the base for the cross-cultural work: a new corpus can be placed by the frozen model before it is described in any other way.

## The stories

The original transcriptions under Propp's functions, transcribers A (Opus) and B (Sonnet) apart: the 45 Russian tales (Propp-Afanasyev, arm U), the fables (Propp-Aesop and Propp-Fables), the 32 tragedies (Propp-Tragedy), and the myths of Apollodorus (Propp-Apollodorus). Where a story was read twice, once for each of two heroes, its first reading is used. Stories with fewer than 3 of Propp's functions are left out, as too short to show their structure: about 105 fables and 120 myths remain for each transcriber, with all the tales and tragedies.

## The model

**Each story is described by four groups of features:**
- **the lexicon:** the share of each of Propp's functions among its functions (32);
- **the relations:** for each of seven tight pairs (γ δ, ε ζ, η θ, D E, H I, M N, Pr Rs), whether the second follows the first, does not, or the first is absent; and for five links in the same move (villainy or lack to liquidation, departure to return, branding to recognition, false claim to exposure, reaction to the gift), the same;
- **the order:** the share of pairs of its functions that run against Propp's order;
- **what lies outside:** the share of its entries written X.

**Length is left out**, so that the model cannot tell a fable by its shortness; a model of length alone is reported for comparison.
**The genres are learned** by a multinomial logistic regression, features standardized, L2 penalty 1.0, classes weighted to their sizes, fitted on half the stories of each genre (sorted, shuffled with seed 46), and tested on the other half.
**The measure** is balanced accuracy, the mean over the four genres of the share of held-out stories guessed right; chance is 0.25. Its p is the share of 1,000 refits with the fitting labels shuffled that score at least as high.

## What is already known

Each feature group was measured before, genre by genre: the share of entries outside Propp's list (tales 63% to 72% covered, tragedies 44% to 46%), the links, the pairs, the orders. No model joining them has been fitted, and no story's genre has been guessed.

## The predictions

1. **The full model guesses the genre** of held-out stories with balanced accuracy at least 0.60, p at most 0.01, for both transcribers.
2. **The relations alone carry genre:** the pairs and links alone guess above chance, p at most 0.05, for both transcribers.
3. **The full model beats length alone**, for both transcribers.
4. **The genre signal is not one reader's habit:** a model fitted on one transcriber's stories guesses the other's held-out stories with balanced accuracy at least 0.50, both ways.

## Checked before the freeze

`model.py selftest`: four planted genres differing only in which pair they complete are told apart by the relations alone (balanced accuracy 0.95); the same stories with their genres shuffled are not (0.26, p 0.42).

## Reported, not judged

The balanced accuracy of each feature group alone (lexicon, relations, order, outside); the confusion between genres; the features that mark each genre most.
