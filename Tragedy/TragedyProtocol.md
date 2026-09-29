# TragedyProtocol

**This protocol tests whether the surviving Greek tragedies follow Propp's morphology as well as the Russian wondertale does.**
The claim is speculation, not Propp's; it is the claim the Apollodorus test failed on a handbook's summaries, tested again on myth told at length.
Everything below is fixed before any play is transcribed.

**It uses the machinery of the Aesop test.**
The transcriber half lives in its own repository, `Story Language/Tragedy` (GitHub `Propp-Tragedy`), which holds nothing of the grammar, the thresholds or the scoring; the keeper's half lives here until every play is transcribed.
Fresh language-model instances list each play's events and transcribe it, run as cloud sessions on that repository: transcriber A on Opus, transcriber B on Sonnet.
They work from `TragedyRules.md`, carried over from the Aesop rules as amended by the Aesop pilot, with the definitions card in place of Propp's chapters and the relevance mark on every entry.

## The corpus

**The 32 surviving tragedies, one play per session, in an order drawn before any play was fetched.**
`TragedyPrediction.txt` names the corpus and the seed, and `PlayOrder.txt` the order `tragedyOrder.py` drew: Rhesus first.
Each author is read in one translator from the PerseusDL `canonical-greekLit` repository: Aeschylus in Smyth's, Sophocles in Jebb's, Euripides in Coleridge's.

**Euripides's satyr play *Cyclops*, outside the corpus, is the pilot.**
It is a Greek play of the same form, so the rules can be tried on it without spending one of the 32.

## What changes for a play

**The unit is the play, and its events include acts shown on stage and acts reported in speech.**
A play is extracted one speech per line, with stage directions kept, since they show acts being performed.
A messenger's report of what has just happened offstage is an event, told where it is reported; choral reflection is not, unless it narrates or performs an act.

**Each event is marked as told past or happening now.**
An event is past when it happened before the play's action begins, as in a prologue.
The primary reading keeps the play's own order; a second reading, reported and not judged, moves the past events before the rest, to ask whether tragedy's order is Propp's once its backstory is put first.

## The measures

**The thresholds are the Apollodorus thresholds, on the primary reading of functions marked as mattering.**
Coverage at least 80%; acceptance at `move` at least 85.2%; and a gap over shuffled moves at least the Russian gap in each length band holding at least ten moves.
Both grammars, as shipped and with the tragic extensions, are judged, with a verdict for each; the claim holds for a grammar only if all three are met on both transcriptions.
The verdict is given once all 32 plays are transcribed; each play's results, and the pooled results as plays accrue, are reported and not judged.

**From P05 on, results are sealed.**
Each play from *Hecuba* on is checked for form and not scored until a tragedy grammar, built from the catalog's building blocks, is proposed and frozen on other material; P05 to P32 are then its held-out test, and are scored under this protocol's measures as well.
From P05 on, the event lister also lists the cast, and the transcribers name performers and undergoers by it, so that each character's sphere of action can be read from the entries.

## Order of work for each play

**Each stage is committed before the next begins.**
1. The play's text, fetched and extracted, and its prompts.
2. Its events and hero, listed in a cloud session and checked here for form.
3. Its two transcriptions, in a cloud session, checked here for form and scored.
The pilot, *Cyclops*, runs between the first play's events and its transcription, and the rules are amended only where its transcribers report a gap.
