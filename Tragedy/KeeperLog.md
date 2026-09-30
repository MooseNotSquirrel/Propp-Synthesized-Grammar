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

**Events stage, P05, Hecuba, from `master` at b51d95b: in form.**
97 events, 20 told as past, numbered in order and cited in the order of telling; a cast of 28, each name once, in the new format; hero Hecuba, named in the cast, with no tie.
The cast rule left one gap, which the lister reported and resolved one way: whether the addressee of a plea or prayer takes part in the event, so "Powers below" and "The gods" are in the cast.
One other name, "daughter of Tyndareus", stands among the other names of both Helen and Agamemnon's wife, as the text uses it for each; the transcribers name characters by the first field, which is unique.
The rules are not amended mid-run; both points are kept for the rules' next revision, if one is made.

**P05, Hecuba, from `master` at db08d17: both transcriptions in form; sealed, not scored.**
Both cover all 97 events, with 105 entries each; the form check finds no problems, and every performer and undergoer in both is a name from `Cast.txt`.
The reports show judgment calls at gaps, not departures. The recurring ones are those of earlier plays: whether a request or order is a, γ or B; whether a repeated want is a new one; and whether a later harm opens a new move or continues an earlier one. Transcriber B's reading of the last produced twelve moves, and it names the contestable move openings.
New to this play: the vengeance plot, where the blinding and the killing of the children could each be U, K, I or A, and the rule to choose by what an act causes does not decide between them.
Transcriber A asked whether "matters" is judged by the act or by the telling of it, for events told only in passing.

**Events stage, P06, Antigone, from `master` at 4a9d9b9: in form.**
91 events, 22 told as past, numbered in order and cited in the order of telling; a cast of 30, each name once; hero Creon, named in the cast.
The hero rule, which counts the events a character takes part in, chose Creon, in 45 events, over Antigone, in 25, with no tie to settle; the list is kept as the rule gives it.
The lister's uncertainties are those of P05: retellings listed once, where an unstated timing falls, which choral narration and prayer count, and which groups are one character.

**P06, Antigone, from `master` at 29381b3: both transcriptions in form; sealed, not scored.**
Both cover all 91 events, with 92 entries each; the form check finds no problems, and every performer and undergoer in both is a name from `Cast.txt`.
The reports show judgment calls at gaps, not departures.
The gap reported most is now stated outright by both transcribers: the request rule, which makes a request or demand the asker's want (a, or X when stated before), overlaps γ for orders and B for the hero asked to act, and both resolved it the same way, γ for commands and prohibitions and a only for wants.
Transcriber A also asks whether "stated before" means the same asker or the same want.
The rule is not amended mid-run, since the plays from P05 are a held-out test and must share one instrument; the overlap is kept for the card's next revision.

**P07, Suppliants: speeches the source names no speaker for.**
Smyth's text leaves the speaker off eight speeches, seven of them in divisions the source marks as choral; `extract.py` had written "?" for any such speech.
From P07 it writes "Chorus" inside a choral division and "(no speaker in the source)" elsewhere, following the source's markup and adding nothing from outside it; P07 has one of the latter, at lines 825-835.
Re-extracting P01 to P05 with the change gives the committed texts exactly. P06 differs only in two speeches, lines 446 and 1219-1240, that its text gives as "?"; the check at P06's setup looked for leftover markup and missed them. P06's text stays as its lister and transcribers used it.

**Events stage, P07, Suppliants, from `master` at 80d697b: in form.**
101 events, 27 told as past, numbered in order and cited in the order of telling; a cast of 29, each name once; hero the Chorus, the Danaids, in about 60 events against about 25 for the King.
It is the first play whose hero is a group, which the cast rule allows: a group that acts together is one character.
The lister took the Chorus as the speaker of the one speech the source names no speaker for (lines 825-835).
The other names in `Cast.txt` are separated by commas here and by semicolons before; the format does not fix the separator, and the transcribers use only the first field.
The lister's other uncertainties are those of P05 and P06: prayers' addressees counted in the cast, retellings listed once, and which choral narration counts.

**P07, Suppliants, from `master` at 163e2f3: both transcriptions in form; sealed, not scored.**
Both cover all 101 events, A in 101 entries and B in 103; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt`, with `-` where the text's addressee is not in it.
The reports show judgment calls at gaps, not departures, and new ones from the play's form. Its backstory, the myth of Io told as proof of lineage, is full of acts that are functions by what they are, and the rules give no exception for embedded myth: transcriber A marked Hera's harm to Io as mattering, so it opens a move and the King's scenes fall inside it, while B marked it incidental, so it opens none.
Transcriber A also notes that the relevance rule's clause for replies, that an act answering an earlier act matters, makes nearly every reply matter.
The request rule against γ recurs, as in P06, at the herald's demands.
