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

**Events stage, P08, Electra, from `master` at de1b9c5: in form.**
135 events, 37 told as past, numbered in order and cited in the order of telling; a cast of 36, each name once; hero Orestes.
The hero is close: the lister counts Orestes in 62 events and Electra in 60, and reports that several of its own calls could tie or reverse that; a tie would still go to Orestes, who is in the last event and Electra is not.
The count cannot be checked here, since the event format records no participants; the list is kept as the rule gave it, and the closeness is kept in view for P08's results.
The lister's other uncertainties are those of earlier plays: retellings, choral myth, which exits count, and past or now for acts the night before.

**P08, Electra, from `master` at 8c7175c: both transcriptions in form; sealed, not scored.**
Both cover all 135 events, A in 136 entries and B in 141; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt`.
The reports show judgment calls at gaps, not departures.
New to this play: transcriber A asks whether "later" in the relevance rule means later in the telling or later in the story, for past harms told late as the causes of acts told early (Iphigenia's sacrifice as a cause of Agamemnon's murder); A read it as the telling, so they are marked N and open no move, and B marked them N too, on the ground that nothing later depends on them.
The two transcribers handle an act with two doers differently: A names one performer and puts the other in the note, B joins both with semicolons; the format does not say; the scoring does not read the performer field, but the building-block plan's character spheres will have to take both forms.
The request rule against B and γ recurs, as in P06 and P07, and so does the question whether a function can be read for a character other than the hero.

**P09, Medea: set up in Coleridge's own wording.**
PerseusDL's English file for *Medea* is Coleridge's translation without the Perseus modernization the earlier Coleridge plays carry, so its English is archaic ("doth", "ne'er"); the translator is the one the protocol names, and the text is used as it stands.

**Events stage, P09, Medea, from `master` at 2ecaf4e: in form.**
79 events, 12 told as past, numbered in order and cited in the order of telling; a cast of 19, each name once; hero Medea, with no tie.
The cast rule's gap on addressees, logged at P05, is now resolved both ways: the P05 and P07 listers put the gods prayed to in the cast, and the P09 lister left out gods who are only called on, keeping only those who act (the Sun-god, Phoebus).
Transcribers who find an addressee missing from the cast write `-`, as at P07, so this bears on the character spheres of the building-block plan, which should count prayers' addressees only where both readings agree, and not on the symbols.
The lister's other uncertainties are the familiar ones: retellings, the messenger's report placed at the first brief telling with only new detail listed from the full account, and which speeches count.

**P09, Medea, from `master` at 9eb419c: both transcriptions in form; sealed, not scored.**
Both cover all 79 events, A in 87 entries and B in 82; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt`.
The reports show judgment calls at gaps, not departures.
Transcriber A found a real inconsistency in the rules' wording, carried over unchanged from the Aesop rules: the bold line says each act in an event gets one entry, a function or X, while the lines under it give an own entry only to each act that fulfills a function, and one X only to an event none of whose acts does. A followed the lines under it, so in an event that mixes a function with a non-function act the second act gets no entry.
Every play, and the Aesop run, was transcribed under the same wording, so the instrument is the same throughout; its effect is that X counts events with no function, not acts, and the X analysis of the building-block plan must read it that way.
The rest are the familiar gaps: the request rule against γ, whether a lack serving an end already pursued opens a move, F and F− for a requester who is not the hero, retellings, and acts with two undergoers.

**Events stage, P10, Iphigenia in Tauris, from `master` at 0490c58: in form.**
124 events, 37 told as past, numbered in order and cited in the order of telling; a cast of 35, each name once; hero Orestes.
The hero is closer than at P08: the lister counts Orestes in 66 events and Iphigenia in 65, and names events whose participants are a judgment call. The last event is the chorus's, with neither in it, so a tie would name both and the play would be transcribed once for each.
The list is kept as the rule gave it, as at P08. The event format records no participants, so these counts cannot be checked; for the rules' next revision, a participants field on each event would make the hero checkable.
The lister's other uncertainties are the familiar ones: retellings, a speaking member merged into the group he belongs to, and choral myth.

**P10, Iphigenia in Tauris, from `master` at ca87233: both transcriptions in form; sealed, not scored.**
Both cover all 124 events, A in 127 entries and B in 129; the form check finds no problems.
Every performer and undergoer is a name from `Cast.txt`, or, in twelve of transcriber A's fields, two cast names joined by a comma; so an act with two doers or two undergoers is now written three ways across plays (one name with the other in the note, a semicolon, a comma), which the character spheres of the building-block plan must read alike.
The reports show judgment calls at gaps, not departures: the request rule against γ and B, the same oracle told twice getting two symbols (B, then F as the answer to a plea), whether "later" means in the telling or in the story (a villainy told late marked N by A and Y by B), Q when the one recognized is not the hero, and whether myth told in a choral ode matters to the play.
Transcriber B also asks whether θ is credited to the deceived or to the deceiver.

**P11, Andromache: set up in Coleridge's own wording, with no stage directions.**
As with P09, PerseusDL's English file is Coleridge's translation without the Perseus modernization, so its English is archaic; and it carries no stage directions, so acts shown on stage are known only from the speeches. The text is used as it stands.

**Events stage, P11, Andromache, from `master` at ff82cb3: in form.**
124 events, 43 told as past, numbered in order and cited in the order of telling; a cast of 40, each name once; hero Andromache, in 39 events against 35 for Hermione.
The lister counted as taking part the future persons a god's prophecy names (Helenus, the Nereids), and an unnamed voice from the shrine as Apollo, on the messenger's blaming Phoebus.
Its other uncertainties are the familiar ones: retellings, past or now at the prologue's edge, choral myth, and names for characters the text leaves unnamed.

**P11, Andromache, from `master` at 23ed5c3: both transcriptions in form; sealed, not scored.**
Both cover all 124 events, A in 127 entries and B in 125; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt` (B joins two names with a semicolon twice).
The reports show judgment calls at gaps, not departures, but the two readings of the move rules now diverge widely: A reads "each new lack creates a new move" literally and splits the play into many moves, while B treats later harms and wants as the same harm or the want stated before and keeps four.
The question of what "later" means in the relevance rule is now answered both ways across plays: at P08 transcriber A read it as later in the telling, and here transcriber A reads it as later in the story, so past acts told late are marked Y and open moves.
Both points, with the request rule against γ, are for the rules' next revision; the move count is not scored until the held-out test, and these readings will bear on acceptance there.

**P12, Orestes: one speaker label misspelled in the source.**
The source labels speech S343 (line 1130) "Oretes", in a stichomythia between Orestes and Pylades; the text is extracted as the source gives it and not corrected, since the context makes the speaker plain.

**Events stage, P12, Orestes, from `master` at 67e9920: in form.**
170 events, 50 told as past, numbered in order and cited in the order of telling; a cast of 50, each name once; hero Orestes, in about 95 events, far ahead of Menelaus and Electra.
The largest list so far. The lister split Apollo's closing speech into ten events, one per prophecy or command, and kept the escaped Phrygian apart from the group of Helen's servants because he acts alone.
Its other uncertainties are the familiar ones: retellings, past or now at the prologue's edge, and asides that hardly matter.

**P12, Orestes, from `master` at a144317: both transcriptions in form; sealed, not scored.**
Both cover all 170 events, A in 172 entries and B in 173; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt`.
The reports show judgment calls at gaps, not departures. The two transcribers' move counts are close this time, 7 and 8.
New to this play: the rule that an event narrating an act is never α meets a genealogy prologue of births and marriages. Transcriber A wrote α for them, as only introducing the family, and B wrote X, as the rule's letter requires.
Both read the matricide as A rather than I, by what it causes, so it opens a move, and both asked whether a hero's killing of the villain is I or A.
The request rule against B recurs, and B's report asks how strong a dependence must be for Y.

**P13, Ajax: one speech the source names no speaker for.**
Speech S284 (lines 1290-1315) carries no speaker in the source; it follows Teucer's speech and goes on answering Agamemnon, and `extract.py` labels it "(no speaker in the source)", adding nothing from outside the text.

**Events stage, P13, Ajax, from `master` at 9e4d4c5: in form.**
117 events, 30 told as past, numbered in order and cited in the order of telling; a cast of 26, each name once; hero Ajax, in 85 events, far ahead of Teucer and Tecmessa.
The lister gave speech S284, which the source names no speaker for, to Teucer from its content.
It counted Menelaus and Agamemnon each where the text says "the Atreidae", rather than making the pair a group, and, as at P09, left gods only prayed to out of the cast.

**P13, Ajax, from `master` at a643a6d: both transcriptions in form; sealed, not scored.**
Both cover all 117 events, A in 132 entries and B in 126, in seven moves each; the form check finds no problems, and every performer and undergoer is a name from `Cast.txt`, with pairs joined by semicolons or commas.
The reports show judgment calls at gaps, not departures: the request rule against γ, threats and conditional curses written X, and which small lacks open moves.

**Correction to the P09 entry: the mixed-event wording has been read both ways.**
At P09 transcriber A gave no entry to a non-function act in an event that also holds a function; at P13 transcriber A gives it its own X. The P09 entry said every play was transcribed under one reading; the wording is the same throughout, but the reading is not.
The frozen measures are untouched by it: `tragedyScore.py` drops every X entry before measuring (`kept`), and coverage counts events with a kept function entry, not entries, so an added X in an event that has a function changes no score.
It does change X counts, so the X analysis of the building-block plan must count events with no function entry, not X entries, which reads both transcriptions alike.

**P14, Sophocles's Electra: five speeches the source names no speaker for.**
Speeches S010, S027, S115, S250 and S356 carry no speaker in the source; each is the second part of a speech the source splits, continuing Electra, Electra, the Paedagogus's report, Electra and the Paedagogus. `extract.py` labels them "(no speaker in the source)", adding nothing from outside the text.
The play tells the story of P08, Euripides's *Electra*; the prompts name the author, and the lister and transcribers open only this play's files.

**Events stage, P14, Sophocles's Electra, from `master` at 7574ea3: in form.**
78 events, 14 told as past, numbered in order and cited in the order of telling; a cast of 17, each name once; hero Orestes, in 37 events against 36 for Electra, and in the last event, so a tie would still name him.
Three plays have now had a hero decided by two events or fewer (P08 by 2, P10 by 1, P14 by 1), all of them Orestes against a sister. The rule is kept as frozen; for its next revision, a margin within which both are named, with the play transcribed once for each, would suit plays that follow two characters about equally.
The lister's other uncertainties are the familiar ones: retellings, the false report listed as one event without its invented contents, and choral myth.

**P14, Sophocles's Electra, from `master` at 7fd9a39: both transcriptions in form; sealed, not scored.**
Both cover all 78 events, A in 78 entries and B in 79, and both keep the whole play in one move, reading Agamemnon's murder as the harm Orestes's want of vengeance already names; the form check finds no problems.
Every performer and undergoer is a name from `Cast.txt`, or two of them joined, now in a fourth way: transcriber A writes "Clytaemnestra and Aegisthus" three times. The character spheres must read "and", commas and semicolons alike.
As at P02, transcriber B kept its generating script in a scratch folder outside the repository, against its prompt; it was not committed, and its output folder holds only the two files.
The reports show the familiar gaps: the request rule against γ and B, F− for a requester who is not the hero, whether "later" means in the telling, and whether a reply that changes nothing matters.

**P15, Euripides's Suppliants: set up in Coleridge's own wording.**
As with P09 and P11, the English file is Coleridge's translation without the Perseus modernization. The play shares its title with P07, Aeschylus's *Suppliants*, and tells another story; the prompts name the author, and the lister and transcribers open only this play's files.

**Events stage, P15, Euripides's Suppliants, from `master` at 30c4796: in form.**
76 events, 22 told as past, numbered in order and cited in the order of telling; a cast of 31, each name once; hero Theseus, well ahead of Adrastus.
The lister kept two characters named Eteocles apart by their fathers, and named the chorus of Argive mothers by who they are rather than "Chorus", with the speaker labels among its other names.
Its other uncertainties are the familiar ones: a plea told in two steps, retellings that add detail, and which laments count.
