# Transcriber rules: Apollodorus in Propp's notation

These rules turn the myths of Apollodorus's *Library* and *Epitome* into strings of Propp's function symbols.
They are fixed before any myth is transcribed, so that the transcriptions cannot be shaped, even unintentionally, to fit any expected result.
Follow them exactly.
Where a rule leaves you unsure what to write, say so in your report; do not invent a rule.

## Where you may look, and where you may not

**Work only in the folder `C:\Users\Steve1\Desktop\Story Language\ApollodorusWork`.**
Read the text from `Library.txt` and `Epitome.txt` there.
Each line is one section, `citation | text`.
Citations are book.chapter.section for the *Library*, such as 2.4.1, and E.chapter.section for the *Epitome*, such as E.1.1.
Frazer's notes have already been removed.

**Read Propp only in the chapters named here.**
Propp's *Morphology of the Folktale* is at `C:\Users\Steve1\Desktop\Story Language\Propp PDF\Propp Morphology Extracted.md`.
Read Chapter II (lines 1434 to 1664), Chapter III (lines 1665 to 3379) and Chapter IX (lines 4386 to 5520).
Do not read the rest of that file.

**Do not open anything else.**
In particular, do not open, list or search the folders `Story Language\Project Files` or `Story Language\SynthesizedProppGrammar`, or any other folder in `Story Language`.
Do not search the web.
Do not use any published analysis of Greek myth in Propp's terms.
Transcribe from the text and from Propp's definitions alone.

**Write only the files your task names, inside your own subfolder of `ApollodorusWork`.**
Do not open another transcriber's subfolder.

## The source is a handbook

**Transcribe what Apollodorus says, at his length.**
He summarizes; much of the work is genealogy, and many myths get one or two sentences.
Do not fill in what other tellings add, even when you know them.

## Stage 1: the census

**The census lists every episode and every event, without reference to Propp.**
Do not think about Propp's functions while taking the census.

**An event is a clause that narrates an action or a change of state.**
These are not events:
- genealogy, such as "he married X and begat Y";
- etiology, such as "hence the place is called Z";
- lists of names;
- reports of what authorities say, such as "some say" (but see variants below).

**An episode is a maximal run of events that share one central figure.**
The central figure is the character who takes part, as doer or as sufferer, in the most events of the run.
The episode begins with the first event in which that figure takes part, and ends where the text turns to events in which the figure takes no part.
A figure who returns after other events begins a new episode; mark the two as connected.

**Every episode is listed, whatever its length.**
Episodes of five events or more will be transcribed; shorter ones are listed and counted only.

**Variants are listed apart.**
Where Apollodorus gives more than one version of the same events ("some say", "others say"), the first version he gives belongs to the episode.
List each other version as a separate variant episode, marked as a variant of the first.

## Stage 2: whose tale

**The hero is the character whose fortunes the episode follows.**
Propp draws the line this way (p.36): where a girl is carried off and the tale follows the one who goes after her, the hero is the seeker; where it follows the girl herself, the hero is the victim.
In practice, the hero is the episode's central figure.
If two figures tie, the hero is the one who takes part in the episode's last event.
If they still tie, write both, and the episode will be transcribed once for each.

**The hero is fixed in the census, before any transcription.**
Some myths read differently from different sides; the rule settles which side the transcription takes.

## Census formats

**`Census.txt` has one line per episode.**

```
L1-001 | 1.1.1-1.1.4 | Sky | 6 | hero: Sky | connected: - | variant of: -
```

The fields are: identifier, citation span, central figure, number of events, hero, connected episodes, and the episode this is a variant of.
Identifiers are prefixed by part: L1, L2 and L3 for the *Library*'s three books, E for the *Epitome*.

**`Events.txt` has one line per event.**

```
L1-001 | 1 | 1.1.2 | Sky binds the Cyclopes and casts them into Tartarus
```

The fields are: episode identifier, event number within the episode, citation, and a short plain paraphrase of the event.
Paraphrase in plain words; do not use Propp's terms.

## Stage 3: transcription

**Each census event gets exactly one entry: a function symbol, or X.**
Propp's definition of a function: "an act of a character, defined from the point of view of its significance for the course of the action" (p.21).
Where an act's significance is unclear, define it by its consequences, as Propp does himself (p.67).
Record who performs and who undergoes each function.
Do not label anyone villain, donor or helper; roles follow from the functions.

**When in doubt, write X.**
An event that fits no function is written X, with the nearest candidate in your notes, such as "X, perhaps D".
Stretching a function to cover an event is the error this work most needs to avoid: a notation stretched to fit anything will let anything pass.
A high share of X is a finding, not a failure on your part.

**Keep the census's order.**
Entries follow the events in the order the text narrates them, which is the census's order.
A flashback is written where it is told, and marked as a flashback in your notes.

**A new move begins with each new villainy or lack.**
This is Propp's definition of the move (p.92).
Number moves I, II, III within an episode.
Events before the first villainy or lack belong to move I.
Where one move breaks off for another and later resumes, write each move separately, and mark in your notes where the break and the resumption fall.

**The alphabet is Propp's, and X.**

| Symbol | Propp's function | Symbol | Propp's function |
|---|---|---|---|
| α | initial situation | F | receipt of a magical agent |
| β | absentation | G | guidance to the place sought |
| γ | interdiction | H | struggle |
| δ | violation | I | victory |
| ε | reconnaissance | J | branding, marking |
| ζ | delivery | K | liquidation of the misfortune or lack |
| η | trickery | ↓ | return |
| θ | complicity | Pr | pursuit |
| λ | preliminary misfortune | Rs | rescue |
| A | villainy | o | unrecognized arrival |
| a | lack | L | unfounded claims |
| B | mediation, the connective incident | M | difficult task |
| C | beginning counteraction | N | solution |
| ↑ | departure | Q | recognition |
| D | the first function of the donor | Ex | exposure |
| E | the hero's reaction | T | transfiguration |
| | | U | punishment |
| | | W | wedding |

Propp's own definitions in Chapter III govern; the names are reminders only.

**A minus marks a negative result, as Propp marks it.**
Write E− for a test the hero fails, F− where nothing is given, and I− where the hero loses the fight (note to p.46).
Use the minus sign − (U+2212).

**Write a variety number only when you can name it from Propp's lists.**
Propp numbers the forms of each function, such as A¹ for abduction of a person.
If you can identify the form from his lists in Chapter III, write the number as a superscript; otherwise write the bare letter.

## Transcription formats

**`Streams.txt` has one block per transcribed episode.**

```
tale: L1-001
name: 1.1.1-1.1.4, Sky
move: I   | <entries, separated by spaces>
move: II  | <entries>
```

X entries appear in the stream like any other entry.

**`Notes.txt` has one line per entry.**

```
L1-001 | I | 3 | ev 3 | 1.1.2 | D | <performer> | <undergoer> |   | "<the key words of the clause, quoted>"; <note>
L1-001 | I | 4 | ev 4 | 1.1.2 | X | <performer> | <undergoer> | ? | "<quoted words>"; X, perhaps E
```

The fields are: episode, move, position in the move, census event number, citation, symbol, performer, undergoer, a question mark if you are unsure, and a note that quotes the words of the text the entry rests on.
Every entry quotes its words; an entry without them will be treated as unsupported.

## Your report

**End your work with a short report.**
List every place where a rule left you unsure what to write, with the episode and event.
Do not summarize the results or comment on how well Propp fits.
