# The genres' problem structures: the test

**DRAFT, 2026-10-13: the design is open for the owner's choices below, and nothing is frozen.** Once frozen, a departure is logged in `Problems/KeeperLog.md`, not made here.

## The question

Option B made the catalog of role-free acts the primary instrument for comparing genres.
The significance test added a layer to it that two describers agree on closely (the hero's part 91%, value 80%, place in a problem 76%), and that does not lead back to Propp's functions.
This test asks whether that layer tells the genres apart: whether wondertale, fable and tragedy differ in how many problems a story has, how often they are solved, who opens them, and whom the story's acts help and harm.

## The development stories, already seen

The 75 stories the significance test described (22 tales, 45 fables, 8 tragedies) are the development set.
`problemsExplore.py` (output `ProblemsExplore.txt`, exploratory) measured them; both describers give the same three profiles:
- **The tale:** about three problems; nearly all repaired (92% to 94%); almost none left open (3%); the hero opens 15% to 21% of them; the last one repaired in 86% to 91% of tales; 60% to 69% of acts help the hero.
- **The fable:** about one problem; 44% repaired; about half left open; the hero opens about half; the last one repaired in 38%; 27% of acts help the hero, 47% to 48% harm.
- **The tragedy:** three to five problems; 63% to 72% repaired; about a fifth left open; the hero opens 30% to 44%; the last one repaired in 50% to 62%; 30% to 35% of acts help the hero.

The predictions below are drawn from these figures, so they are tested only on stories not yet described.

## The test stories

Stories with a judged hero (`Heroes/`) that no act describer has read:
the 22 development tales of `Calibration/Split.txt`, all with a judged hero; the 41 of the 50 held-out fables of the third and fourth batches (Propp-Fables) with a judged hero; and **the plays, the owner's choice: eight (P25 to P32) or sixteen (P09 to P16 and P25 to P32)**.

## The instrument, unchanged

Two stages per story, as in the two tests before: the acts, under `ActsRules.md` unchanged, by describers A (Opus) and B (Sonnet); then the significance layer, under `SigRules.md` unchanged, by fresh describers of the same letter on those acts, told the judged hero.
In Propp-ActsRoles, four cloud stages: `acts-3` (tales and fables), `acts-4` (plays), then, once the keeper has checked their form and written the inputs, `sig-3` and `sig-4`.

## The measures

Per story, from each describer's layer; a problem is a story's label with at least one act placed in it.
1. Problems in the story.
2. The share of its problems repaired (an act placed as repairing it).
3. The share left open (no act repairs, punishes or rewards in it).
4. The share opened by the hero's own act (the act placed as opening it is one the hero does).
5. Whether the problem opened last is repaired.
6. The share of its acts that help the hero.
7. The share of its acts that harm the hero.

A genre's figure is the mean over its stories; a story with no problem is left out of measures 2 to 5.

## The predictions

Each names one genre and the two it differs from, in a stated direction:
1. **Fable fewer problems** than tale and than tragedy.
2. **Tale more repaired** than fable and than tragedy.
3. **Fable more left open** than tale and than tragedy.
4. **Tale fewer opened by the hero** than fable and than tragedy.
5. **Tale more often ends repaired** than fable and than tragedy.
6. **Tale more acts helping the hero** than fable and than tragedy.
7. **Fable more acts harming the hero** than tale and than tragedy.

A comparison holds when the difference goes the predicted way and a one-sided permutation test, shuffling genre labels among the two genres' stories 10,000 times (seed 46), gives p at most 0.05.
A prediction holds when both its comparisons hold for both describers.

## The verdict

**THE GENRES HAVE DISTINCT PROBLEM STRUCTURES** if at least five of the seven predictions hold.
**THEY DIFFER IN PART** if two to four hold, naming which.
**NOT SHOWN** if fewer than two hold.

## Reported, not judged

Every figure per genre and describer; the comparisons not predicted (tale against tragedy on problems per story, unstable in development); the describers' agreement on the layer in the new stories, as the significance test measured it; and the form checks of the four stages.
