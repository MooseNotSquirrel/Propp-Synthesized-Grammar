# AesopProtocol

**This protocol tests whether Aesop's fables are built from Propp's functions in Propp's order.**
The claim under test is speculation, not Propp's: that short tales, of the kind told every day, are samples of the production rules of Propp's morphology, a few functions at a time in his order, rather than whole moves.
Propp built his morphology on Russian wondertales and claimed it for them alone.
Everything below is fixed before any fable is transcribed.

**It follows the Apollodorus test, with three lessons from it.**
The unit is a tale the text itself gives, one fable, and not an episode cut out of a chronicle.
Each entry is marked for whether it matters to the course of the fable, since the Apollodorus audit found entries faithful to the text but incidental to any tale, which Propp's definition of a function (p.21) excludes.
The measures suit short tales, since a grammar cannot tell real order from shuffled order in a string of four functions or fewer.

## The source

**The text is George Fyler Townsend's translation, *Three Hundred Aesop's Fables*.**
It is Project Gutenberg eBook 21, in the public domain, kept in the Aesop repository as `source/pg21.txt`.
`extract.py` there takes the fables from it by the book's own contents list, leaving out the preface, the life of Aesop, the footnotes and the index: 313 fables, 34,072 words, a median of 97 words each.

**A random sample of 100 fables is transcribed, and three others form the pilot.**
The seeds are committed in `AesopPrediction.txt` before the draw.
The pilot is drawn from the fables outside the sample, so the sample is untouched by any rule the pilot changes.

## Who does what

**The event lister and both transcribers are fresh language-model instances, run as cloud sessions.**
The event lister lists each fable's events, its hero and its moral, without reference to Propp.
Transcriber A runs on Opus and transcriber B on Sonnet; each transcribes every sampled fable without seeing the other's work.
Each instance is given its material in its prompt: the rules, the definitions card, the fables and, for transcription, the event list.
The Aesop repository holds only that material, and nothing of the grammar, its results or these thresholds.

**The definitions card replaces Propp's chapters.**
Propp's text cannot be placed where cloud instances can read it, so the rules carry a card defining each function in plain words, close to his own.
The card is reviewed and approved before any transcription begins.
Variety numbers are not written, since the card does not give Propp's lists of forms.

**The keeper merges, checks and scores, and transcribes nothing.**
The keeper commits each stage before the next begins.

**An auditor checks fifty entries from each transcription, on two questions.**
Do the quoted words show the act the symbol claims, and does the act matter to the course of the fable as its mark says?
The entries are drawn by a seed committed first, mixed, and shown without the transcriber's name or any result.

## The rules

**The transcriber rules are `AesopRules.md` in the Aesop repository.**
They carry over the Apollodorus rules as amended by its pilot: one entry for each act, a function assigned whoever performs it, an act judged by what follows it and not by the sequence it would make, a threatened act written X, and a move opened only by a villainy or lack (p.92).
They add the relevance mark: each entry is Y when something later in the same fable depends on it and N when nothing does, with the event it depends on or leads to named.

## The measures

**The primary derivation keeps only entries marked Y.**
Entries marked N are treated as X.
All entries are scored as well, as a secondary reading, and the doubtful entries are handled as in the Apollodorus test.

**Three measures decide the claim, each on both transcriptions.**
- Coverage: the share of events with at least one entry that is a function marked Y.
- Order: the share of ordered pairs of functions within a fable that run backward against Propp's numbering of the functions, against the same entries shuffled within each fable.
- Pairs: for each of Propp's pairs whose first function occurs at least ten times, how often it is followed by the second within the fable, against the same entries shuffled.
The thresholds are in `AesopPrediction.txt`.

**Other measures are reported and not judged.**
The share of entries marked N; the share of fables that hold a villainy or lack followed by its liquidation; the grammar's acceptance of each move at `move`, as shipped and with its extensions, set against shuffled moves by length, for comparison with the Apollodorus test; and the agreement between the transcribers.

## Files and order

**Each file is committed before the stage after it begins.**
1. `AesopRules.md` and the definitions card, in the Aesop repository; this protocol and `AesopPrediction.txt`, here.
2. The sample and the pilot, drawn by the committed seeds.
3. The event list, the heroes and the morals.
4. The pilot transcriptions, and any rule amended at a gap they report.
5. The two transcriptions.
6. The run, the audit and the report.
