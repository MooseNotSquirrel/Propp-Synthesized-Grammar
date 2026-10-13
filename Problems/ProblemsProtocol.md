# The genres' problem structures: the test

**DRAFT, 2026-10-13, to be frozen at the owner's word, before any description of the test stories.** Once frozen, a departure is logged in `Problems/KeeperLog.md`, not made here.

## The question

Option B made the catalog of role-free acts the primary instrument for comparing genres.
The significance test added a layer to it that two describers agree on closely (the hero's part 91%, value 80%, place in a problem 76%), and that does not lead back to Propp's functions.
This test asks whether that layer tells the genres apart: whether wondertale, fable and tragedy differ in how their problems are solved, who opens them, and whom the story's acts help and harm, beyond what the stories' length produces.

## Length, and the null that removes it

**A random description passes a naive test.** The first draft compared genres on the raw measures; random descriptions of the test stories' acts passed 8 of its 16 predictions, because a long story with randomly placed acts almost surely has a repair somewhere and a five-act fable often has none.
**Each story is therefore scored by its excess over a random description of its own acts.** For each describer, each act's hero's part, value and place are drawn together from that describer's descriptions of all the stories scored, pooled across genres, and its problem label from the labels the describer used in that story; 200 draws, seed 46. A story's excess on a measure is its own figure minus the mean over the draws. The null keeps the story's length and number of problems, so the excess is the structure beyond what length and the describer's overall habits produce.
**What the null showed on the development stories:** the tale's and the fable's rates of repair are about what their lengths give (the tale's 93% against a null 80%, the fable's 43% against 31%); the tragedy repairs far less than its length gives (62% to 71% against 87% to 96%), and ends with its last problem unrepaired far more often.

## The development stories, already seen

The 75 stories the significance test described (22 tales, 45 fables, 8 tragedies) are the development set; `problemsExplore.py` (`ProblemsExplore.txt`) and `problems.py dev` (`ProblemsDev.txt`) measured them.
The predictions below are the comparisons they admit by a fixed rule, so the predictions are tested only on stories not yet described.

## The test stories

Stories with a judged hero (`Heroes/`) that no act describer has read:
the 22 development tales of `Calibration/Split.txt`; the 41 of the 50 held-out fables of the third and fourth batches (Propp-Fables) with a judged hero; and sixteen plays, P09 to P16 and P25 to P32, by the owner's choice.

## The instrument, unchanged

Two stages per story, as in the two tests before: the acts, under `ActsRules.md` unchanged, by describers A (Opus) and B (Sonnet); then the significance layer, under `SigRules.md` unchanged, by fresh describers of the same letter on those acts, told the judged hero.
The material sits in `problems/` in Propp-ActsRoles, apart from the earlier tests' files. Six cloud stages, each in a fresh session: `p-acts-1` (tales and fables), `p-acts-2` and `p-acts-3` (eight plays each); then, once the keeper has checked their form and written the inputs (`problems.py setup-sig`), `p-sig-1` (tales and fables), `p-sig-2` and `p-sig-3`.
A tragedy line that carries a speech number where the play belongs is read as the two-layer test's reader read it, every speech number checked against the play's event list.

## The measures

Per story, from each describer's layer; a problem is a story's label with at least one act placed in it.
- **Problems in the story:** reported only, since the null keeps it fixed.
- **Repaired:** the share of its problems with an act placed as repairing it.
- **Open:** the share with no act repairing, punishing or rewarding in it.
- **Hero opens:** the share whose opening act the hero does.
- **Ends repaired:** whether the problem opened last is repaired.
- **Acts help:** the share of its acts that help the hero.
- **Acts harm:** the share that harm the hero.

A story with no problem is left out of the measures that need one.

## The predictions

**The rule:** every comparison of excesses that the development stories show in the same direction for both describers, by at least 0.10. It admits eleven:
1. Repaired: tale above tragedy.
2. Repaired: fable above tragedy.
3. Open: tragedy above tale.
4. Open: tragedy above fable.
5. Hero opens: fable above tale.
6. Ends repaired: tale above tragedy.
7. Ends repaired: fable above tragedy.
8. Acts help: tale above fable.
9. Acts help: tale above tragedy.
10. Acts harm: fable above tale.
11. Acts harm: tragedy above tale.

**A prediction holds** when, for both describers, the higher genre's mean excess is above the lower's by at least 0.05 and a one-sided permutation test, shuffling genre labels among the two genres' stories 10,000 times (seed 46), gives p at most 0.05.

## The verdict

**THE GENRES HAVE DISTINCT PROBLEM STRUCTURES** if at least nine of the eleven hold.
**THEY DIFFER IN PART** if three to eight hold, naming which.
**NOT SHOWN** if fewer than three hold.

## Checked before the freeze

**On the development stories,** where the predictions come from, 10 of 11 hold (the fourth, tragedy more open than fable, has p 0.089 for A), with eight tragedies; the test has sixteen.
**On random descriptions** of the test stories' acts, run end to end through the setup, form checks and scorer in a scratch folder: 0 of 11 hold.

## Reported, not judged

Every figure per genre and describer, raw and excess; the comparisons not predicted, two-sided; the describers' agreement on the layer in the new stories, as the significance test measured it; and the form checks of the six stages.
