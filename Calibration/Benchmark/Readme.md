# The human benchmark

**Frozen 2026-10-05, before the owner annotated anything.** Five tales, the owner as transcriber, against Propp and against the four model readings.

## The tales

A093 *The Witch and the Sun's Sister*, A131 *Frolka the Sitter*, A133 *Pokatigoroshek*, A145 *The Seven Semyons*, A151 *Shabarsha*: the five shortest of the Appendix III tales that the earlier studies also used (Bod and colleagues 2012: 145, 151; Gervás and Méndez 2024: 93, 131, 133), 24 to 29 events each, 134 in all.

## What the owner works from

The English event list of each tale (`Benchmark-A0NN.txt`), the same list the model transcribers worked from, and the definitions card they used (`Card.md`). The hero line is the one they were given; in A151 the hero rule names the Little Devil, not Shabarsha (KeeperLog). The models also read the Russian text; the owner reads the event list alone, and may consult any English translation of the tale. Appendix III, Propp's chapters on these tales and the first project's token file are not opened during the annotation.

**The owner is not blind as the models are:** the owner built the first project's token file from Appendix III. Before annotating, the owner notes in this folder (`Memory.txt`) any of the five schemes remembered, even in part; the result is reported with that note.

## The annotation

For each event, after `fn:`, the function symbol or symbols from the card, or X; after `move:`, the move's numeral where a new move begins. Every symbol written is read as mattering (there is no Y or N mark).
Symbols may be typed on a plain keyboard: `up` and `down` for ↑ and ↓, and the Greek letters by name (`beta`, `gamma`, and so on); `Pr`, `Rs`, `Ex` as on the card. Several symbols for one event are separated by spaces. The preparatory functions (β to θ) are not scored, since Propp's schemes print none, so they may be left out. (Added before any annotation, with the matching change to `benchmark.py`.)

## The scoring (`benchmark.py`, committed with this file)

The owner's stream is the symbols in event order, reduced as `compare.py` reduces them, X and the preparatory functions left out. Content and order as in `compare.py`, against Propp, and against each of the four model readings; the models' figures against Propp on the same five tales beside them.

**The reading, fixed now:** with five tales none of this is a test; it is reported as a benchmark. If the owner's content agreement with Propp is below the models' mean or exceeds it by at most 0.05, the models are read as near the task's ceiling; if it exceeds the models' mean by 0.10 or more, the models are read as the weak point; between, as unsettled.
