# Is the order inside a block built into the instrument?

**A desk check, 2026-09-30, of the definitions card that the Aesop, Propp-Fables and Tragedy transcribers all used (the card is identical in `AesopRules.md` and `TragedyRules.md`).**
The question: can a transcriber write a block's two halves in reverse order at all? If the card defines the second half by pointing back to the first, a reversed block can arise only when a text tells the second act before the first, as a flashback, since events are listed in the order of telling.

## The blocks

| Block | Second half as the card defines it | Reversal |
|---|---|---|
| `DeceptionTrap`, η then θ | θ: the victim "is taken in by the deception" | definitional: only by a flashback |
| `RuleViolation`, γ then δ | δ: "The prohibition is broken" | definitional: only by a flashback |
| `InformationGathering`, ε then ζ | ζ: "The villain receives that information" | definitional: only by a flashback |
| `TaskAndSolution`, M then N | N: "The task is accomplished" | definitional: only by a flashback |
| `TestedAcquisition`, D then E, then F | E: "responds to that test or request"; F stands alone | D to E definitional; F free |
| `complication`, the trigger, then B, C, ↑ | B: "The misfortune or lack is made known"; C: acts "against the misfortune or lack"; ↑ stands alone | trigger to B and C definitional; ↑ free |
| `StruggleAndOutcome`, H then I | I: "The villain is defeated", with no reference to a struggle | free |
| `FraudPosture`, o then L | each stands alone | free |
| `ReturnJourney`, `Ordeal` | each part stands alone | free |
| `PursuitFirst` and `RescueFirst`, `Endgame` | both orders are forward entries, or the group is order-free | never flagged as reversed |

## What it means for the block findings

**The finding that reversed blocks fall at or below chance is mostly the instrument, not the stories.**
Every block that carried the finding, `DeceptionTrap` and `complication` above all, is definitional: the card makes its second half mean "after the first", so a reversal needs a flashback, which fables almost never use. The shuffle baseline did not know this, and expected reversals the card makes nearly impossible.
The statement made on 2026-09-30, that the order inside a block is "near-obligatory", like the fixed order inside a phrase of Latin or Russian, IS WITHDRAWN AS STATED: for the definitional blocks the order is fixed by definition, and for the free blocks the counts are too small to say (in the fables, `StruggleAndOutcome` forward 2 to 3, reversed 0, with about 0.5 of each by chance).

**What survives.**
The halves of Propp's pairs are told together, adjacent in the stream, more often than chance: coverage by blocks stays above the shuffles in every reading and both corpora, and replicated on the held-out fables. That is a finding about co-occurrence and adjacency, not order. Part of the co-occurrence is also definitional, since θ cannot occur without an η; what is not definitional is that the trick and the complicity are told next to each other, with nothing between.
The order between blocks, measured by the fable grammar's gap over shuffled order on unseen fables (+27 and +30), is untouched by this check: those ranks are not definitional.

## What would test the order inside blocks properly

Only the free blocks can: `StruggleAndOutcome`, `FraudPosture`, `ReturnJourney`, `Ordeal`, and the free parts of `complication` (↑) and `TestedAcquisition` (F). They are rare in fables and in the four open tragedies, so the test needs the tragedy run's end or a larger corpus such as Afanasyev's; its prediction is frozen in `Tragedy/BlockPrediction.txt`.
