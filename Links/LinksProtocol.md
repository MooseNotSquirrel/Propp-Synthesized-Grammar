# Links at a distance: the test

**DRAFT, 2026-10-19, to be frozen at the owner's word, before any link is counted.** Once frozen, a departure is logged in `Links/KeeperLog.md`, not made here.

## The question

The catalog of Propp's pairs and groups (`ProppPairsAndGroups.md`) names eight links, after the owner's outline: villainy or lack to liquidation, departure to return, struggle to victory, task to solution, branding to recognition, false claim to exposure, test and reaction to the gift, pursuit to rescue.
Each joins two functions that can stand far apart, and the second may never come.
The frequency analysis looked only up to four places apart; the bottom-up test found that the second half of a pair is whatever act fulfils the first, a relation and not an act type.
This test measures each link as a relation: how often, in a move holding the first function, the second stands anywhere after it in the same move.

## The moves

**The transcriptions:** the original transcriptions under Propp's functions, kept by their move numbers: the 45 Russian tales (Propp-Afanasyev, arm U), the 198 fables (Propp-Aesop and Propp-Fables), the 32 tragedies (Propp-Tragedy); transcribers A and B apart. Each entry is read as its function's letter, X and α left out and a negative result counted as its function (F− as F).
**Propp's own moves:** the 84 moves of Appendix III (`ResolvedMoves.txt`), read through the corpus runner's reducer; a brace's rows are read in turn.

## The statistic

For a link, the moves holding its first function (where two are named, D and E, both), and among them the moves where the second function stands after it (after both, where two are named).
**The share** of moves holding the first in which the second follows is the link's strength: how far the first implies the second.
**The null** shuffles all of a genre's functions across its moves, each move keeping its length, 10,000 times (seed 46); the lift is the observed count over the null's mean, and p the share of shuffles at least as high (plus one, over 10,001).
**A link holds** in a corpus when the first function stands in at least 5 moves, the lift is above 1, and p is at most 0.05.
**A caution:** the definitions card defines some second halves by the first (a liquidation undoes an earlier villainy or lack), so transcribers write the second only after the first, and the lift is partly the card's. The share is not: villainy does not require liquidation, and how often the first is followed by the second is what the stories do.

## The predictions

1. In the tales, at least six of the eight links hold for both transcribers.
2. Villainy or lack is followed by liquidation in a smaller share of moves in the tragedies than in the tales, for both transcribers, as the problem-structure test found tragedy leaving its problems unrepaired.
3. In Propp's own moves, every link whose first function stands in at least 5 moves holds.

## Checked before the freeze

`links.py selftest`: a link planted in half of 80 random moves holds (lift 5.5, p 0.0005); a pair of random letters does not. On twenty sets of random moves the mean lift is 1.04 and one in twenty reaches p 0.05, as chance gives.

## Reported, not judged

Every link in every genre, transcriber and Propp's moves: the moves, the moves with the first function, the share followed by the second, the expected count, the lift and p.
