# A scored grammar of Propp's sections

**Frozen 2026-10-06, before the section grammar was fitted.** A departure is logged in `KeeperLog.md`, not made here.

## The question

Propp divides a move into large sections: the complication, the donor, the transfer, the struggle, the liquidation, the return, the arrival and false claims, the task, and the endgame.
His own schemes keep them in that order almost without exception, but readings of the same tales by machine and by hand do not (`SectionOrderExplore.txt`, below).
A yes-or-no grammar cannot describe an order that holds about five times in six.
A scored grammar can: it ranks the sections and measures how far a reading follows the ranking.
This test asks whether an order fitted to readings of the tales describes unseen tales better than Propp's own order of sections.

## Known before freezing

The exploration (`sectionGrammar.py explore`, output `SectionOrderExplore.txt`) read all 45 tales, development and test alike.
Of pairs of functions in different sections, 2.5% run against Propp's order in his own schemes, 16.6% and 17.4% in the two machine readings, and 15.9% in the owner's five tales, against about 50% for random order.
The commonest reversals put the donor before the complication and the struggle, transfer or return before the donor; leaving the donor out barely changes the share.
The test set's own figures for the fitted grammar have not been computed.

## The grammar

**The sections:** as in `sectionGrammar.py`'s header; the preparatory functions are left out.
**The streams:** each move of a transcription, its functions marked Y in the order of the notes, each replaced by its section; the transcriber's own moves.
**The fitted grammar** (`SectionGrammar01.txt`): each section's mean relative position within moves, over the 22 development tales of `Split.txt`, arm U, both transcribers pooled.
**Propp's grammar:** the sections in his order, 1 to 9.

## The measure

For each reading of the 23 test tales, moves of two or more different sections only: concordance, the share of pairs of sections in different ranks that stand in the grammar's order, pooled over moves; and its gap over 1000 in-place shuffles of each move, seed 46.
The two grammars are compared by the difference of their gaps, and tested by a two-sided paired sign-flip test over moves on the difference of concordant pairs, 10,000 flips, seed 46.

## The verdict

On arm U, for both transcribers:
- **THE FITTED ORDER IS BETTER** if its gap exceeds Propp's by at least 0.02 with p at most 0.05, for both;
- **PROPP'S ORDER IS BETTER** if Propp's gap exceeds the fitted one's by at least 0.02 with p at most 0.05, for both;
- **PROPP'S ORDER SUFFICES** otherwise: the fitted order does not do better.

Reported, not judged: arm C; the fitted ranking against Propp's, section by section.

## Why it matters

If the fitted order does better, the wondertale has an order of its own that Propp's sequence misdescribes, as tragedy does.
If Propp's order suffices, his sequence is the best simple description of the wondertale's order, and its looseness lies in how strictly the order holds, not in what the order is.
