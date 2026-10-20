# Where myth sits, retested on the order of its blocks

**Frozen 2026-10-19 at the owner's word, before any myth is scored.** Once frozen, a departure is logged in `Genre/KeeperLog.md`, not made here.

## Why a retest, and why on order

The myth test (`MythProtocol.md`, `MythRun.txt`) found the core holding in myth and myth's frame closing as seldom as tragedy's, but its third prediction, that myth is set like tragedy, failed: the transcribers split on a frame share standing on a dozen moves.
The frame shares cannot be used again: the keeper has seen them on the myths, and on the two well-supported ones both transcribers lie nearest tragedy, a check made after the result.
A fair retest needs a setting never measured on the myths. **The order of the blocks is one:** tragedy has an order of its own that holds on unseen plays (`Tragedy/TragedyOrder01.txt`), the wondertale and the fable follow Propp's order (`Blocks/GenreOrder.md`), and no order model has been scored on the myths.

## What is already known of the myths' order

The earlier test measured the myths against Propp's numbering of the functions only: 32% to 33% of ordered pairs in a Greek move run backward, against 40% to 43% in shuffled moves (`Apollodorus/ApollodorusResult.md`, exploratory measures). So Propp's order fits the myths a little better than chance; how the other orders fit them is not known.

## The instrument, unchanged

The four order models and the measure of `Blocks/GenreOrder.md`: the wondertale and fable models as fitted (`Blocks/GenreOrder-wondertale.txt`, `-fable.txt`), the tragedy model as frozen, and Propp's order; for each, the weighted concordance on the myths and its gap over 1,000 in-place shuffles of each version's units, seed 46.
**The myths** are read from the Apollodorus transcriptions as `genreOrder.py` reads the others, the symbol from its own field. The Apollodorus rules had no mark of whether an entry matters, so every myth entry is read as mattering, where the other genres set aside entries marked N.

## The prediction

**Tragedy's order fits the myths better than the wondertale's, the fable's and Propp's, for both transcribers** (the largest concordance gap of the four).
If it holds, myth is set like tragedy on a setting the keeper had not seen; if it fails, the closeness on the frame shares is not borne out by order.

## Checked before the freeze

`mythOrder.py selftest`, the held-out tragedies standing in for the myths: tragedy's order is best for both transcribers, and the gaps reproduce `Blocks/GenreOrderRun.txt`'s tragedy column to the third decimal but for one, fable on B, +0.076 against +0.075, the fable model being read from its file, where ranks are rounded to three decimals.
