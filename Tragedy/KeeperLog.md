# KeeperLog

The keeper's record of the tragedy run, kept before any scoring.
The keeper corrects no list and no transcription.

**Events stage, pilot and P01, in a cloud session: both lists in form.**
Cyclops (pilot): 69 events, 12 told as past; hero Odysseus, 43 events to the Cyclops's 38.
Rhesus (P01): 83 events, 21 told as past; hero Hector, tied with Rhesus at 30 events and given to Hector by the last-event rule.
The P01 lister reports the tie as fragile: moving a single character tag, or listing Rhesus's journey or boasts as more events, would make Rhesus the hero.
The rule stands as frozen, so the play is read as Hector's tale.

**The two listers ran at once, and the pilot lister saw P01's new files named in `git status`.**
It reports it did not open them; the lists make no use of Propp and cover different plays, so nothing that bears on the test was exposed.

**Pilot stage, Cyclops, in a cloud session: both transcriptions in form, not parsed.**
Transcriber A: 74 entries, 14 marked N; transcriber B: 73 entries, 19 marked N; every event covered.
Both reported four shared gaps, and the rules were amended at each, stated generally: a villainy or lack marked N opens no move; the request rule holds whatever harm came before; help that meets the want itself is K and not F; an oracle matters when a later event fulfils it or is done because of it.
The pilot is kept as a record and is not scored.

**P01, first run, set aside unread: it ran under the unamended rules.**
The cloud session that ran P01 was the pilot's, and it kept the pilot's branch, which lacked the rule amendments pushed to `master` after the pilot.
The protocol applies the amendments before the first corpus play, so the run is kept in `superseded/P01-unamended/` and not scored, and P01 is transcribed again.
RUN.md now requires the runner to start from the latest `master` and report the commit it started from.
The scoring program was committed before this branch was fetched.

**P01, second run, from `master` at 2f1176e: both transcriptions in form, under the amended rules.**
Transcriber A: 98 entries in 10 moves; transcriber B: 96 entries in 5 moves; every one of the 83 events covered.
The reports show judgment calls at gaps, not departures; the recurring ones are whether an order is γ or B, where a repeated harm ends and a new one begins (which accounts for the difference in move counts), and how to mark whether an act told as past matters.

**Events stage, P02, Heracleidae: in form.**
75 events, 16 told as past; hero Iolaus, in about 29 events against about 16 for Eurystheus.
The lister put the past events in the order they happened, where the P01 and pilot listers had put each event where it is told; in practice two events, 5 and 6, told late, stand among the prologue's past events, and the battle report keeps the order of telling.
The list is kept; the rule now states the order of telling, from P03 on.

**P02, Heracleidae, from `master` at aadf9d1: both transcriptions in form.**
Transcriber A: 86 entries in 4 moves. The reports show judgment calls at gaps, not departures: a demand read as a lack or an order; where a repeated harm stops opening moves; the oracle's demand for a maiden's sacrifice read as a lack (a) or a difficult task (M).
Transcriber A noticed the P02 event list's order, logged at the events stage, and followed the list as given.
Transcriber B kept its working script in a scratch folder outside the repository, against its prompt, which asked for working files inside its own folder and deleted; the script was not committed, and transcriber A was forbidden any folder but its own.

**Events stage, P03, Oedipus at Colonus: in form.**
115 events, 21 told as past, listed in the order of telling as the clarified rule requires (no event cited before the one listed ahead of it); hero Oedipus, well ahead of Theseus.
The lister listed an event told more than once only where the play first states it clearly.

**P03, Oedipus at Colonus, from `master` at 73ade1d: both transcriptions in form.**
Transcriber A: 119 entries; transcriber B: 121 entries in 10 moves; all 115 events covered.
The reports show judgment calls at gaps, not departures; the recurring one is again whether an order is an interdiction (γ) or a demand read as a lack, and how far "the want was stated before" reaches.

**Events stage, P04, Ion: in form.**
94 events, 20 told as past, in the order of telling; hero Ion, in 65 events against 54 for Creusa and 24 for Xuthus.
As in P03, an event told more than once is listed where it is first told, with a later telling listed only for what it adds.

**P04, Ion, from `master` at c0083bc: both transcriptions in form, every event covered.**
The reports show judgment calls at gaps, not departures; the recurring one remains how a request or order is read (a, γ or B), and whether a want held by a different character is a new want.

**From P05, results are sealed, and each play has a cast list.**
From *Hecuba* on, each play is checked for form and its transcribers' reports are logged, but it is not scored until the tragedy grammar the building-block plan calls for is proposed and frozen; P05 to P32 are then that grammar's held-out test, and scoring them earlier would let their results shape it.
`tragedyScore.py score` is not run in the meantime, and `TragedyResults.md` stays at P01 to P04.
The event lister now also writes `Cast.txt`, one name per character with the other names the text uses, and the transcribers must name performers and undergoers by it, so that character roles can be read from the performer and undergoer fields.
Both changes were committed to the transcriber repository before any P05 stage ran; the rules for events, relevance and symbols are unchanged.
