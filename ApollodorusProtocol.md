# ApollodorusProtocol

**This protocol sets out how to transcribe the myths of Apollodorus's *Library* into Propp's notation, so that `ProppEBNF46.txt` can be tested on Greek myth.**
The test asks whether Greek myth, taken from a handbook nobody chose because it fits Propp, follows the same syntax as the Russian wondertales of Appendix III.
Everything below is fixed before any myth is transcribed, so that the transcriptions cannot be shaped, even unintentionally, to pass.

**The claim under test is speculation, not from Propp.**
Propp built his morphology on one hundred Russian wondertales and claimed it for that genre only.
The claim here is that his morphology describes Greek myth as well as it describes the wondertale.
It is stated as three measurements in the section "The prediction", with thresholds to be fixed before the run.

## The source

**The text is Frazer's English translation of the *Library* and the *Epitome*.**
It is the Loeb edition of 1921, in two volumes, and the Perseus Digital Library publishes it under a Creative Commons Attribution-ShareAlike 3.0 United States license.
Citations take Perseus's form, book, chapter and section, such as 2.4.1 for the *Library* and E.1.1 for the *Epitome*.

**The transcriber reads Frazer's text and not Frazer's notes.**
The notes compare Apollodorus with other ancient sources, and reading them would import other versions of the myth into the one being transcribed.
The keeper takes the text from the Perseus project's TEI files, `tlg0548.tlg001.perseus-eng2.xml` for the *Library* and `tlg0548.tlg002.perseus-eng2.xml` for the *Epitome*, from the PerseusDL `canonical-greekLit` repository, which licenses them under Creative Commons Attribution-ShareAlike 4.0.
`Apollodorus/extract.py` strips the notes before the text reaches the transcribers, so the rule is enforced rather than asked.
It yields 209 sections of the *Library*, 38,368 words, and 177 of the *Epitome*, 11,399 words, in `Apollodorus/Library.txt` and `Apollodorus/Epitome.txt`.

**The *Library* is a handbook, and that shapes what the test can show.**
Apollodorus summarizes; he does not tell tales at a storyteller's length.
Much of the work is genealogy, and many myths get one or two sentences.
A summary drops functions, the preparatory ones especially, so a Greek move will usually be shorter than a Russian one.
A shorter string is easier for a permissive grammar to accept, which is why the prediction includes a baseline from shuffled strings.

## Who does what

**The transcriber has read Propp and has not seen this project's grammar or results.**
The transcriber reads Propp's Chapters II, III and IX, where he defines the functions and the move, and may consult them throughout.
The transcriber must not see `ProppEBNF46.txt`, `StepTests.txt`, `SemanticCatalog46.md`, `CorpusGroups.txt`, or any measurement made from them.
Anyone who has worked on the grammar, a language model included, is disqualified as the transcriber for the same reason.

**The transcribers are two fresh language-model instances, and others take the census.**
The census is taken by four fresh instances, one for each part of the text: the *Library*'s three books and the *Epitome*.
Each instance starts with no memory of this project and none of the conversation in which the grammar was built.
The two transcribers run on different models, so that a shared habit of one model does not pass for agreement.
Each is given only the transcriber's rules, the stripped text, and Propp's Chapters II, III and IX.
They may not search the web or use any published analysis of Greek myth in Propp's terms.
The rules they work from are `Apollodorus/TranscriberRules.md`, and the prompts they are given are in `Apollodorus/prompts/`, both committed before any instance runs.
Their blindness rests on instruction: they run with access to the machine's files and are told not to open the project's.
The results are reported as transcribed by two language-model instances without access to the grammar, which is a weaker claim of independence than human transcribers would give.

**An auditor checks a sample of the notes for fidelity to the text.**
Fifty entries are drawn at random from each transcription, with the seed committed first.
For each, the auditor asks only whether the cited clause says what the symbol claims.
The audit needs no blindness, since it judges the reading of the text and not the fit to any grammar.

**The keeper freezes the files, runs the programs, and transcribes nothing.**
The keeper commits each stage's file to git before the next stage begins, so the history shows what was fixed when.
The keeper also computes the Russian baselines and applies the derivation rules in the section "From transcription to test".

**Both transcribers transcribe the whole corpus.**
Each works without seeing the other's work, so agreement is measured on every episode.

## Stage 1: the census

**The census lists every episode in the *Library* and the *Epitome* before anyone reads for Propp.**
It is written without reference to Propp's functions, so what enters the corpus does not depend on whether it fits.

**An event is a clause that narrates an action or a change of state.**
These are not events:
- genealogy, such as "he married X and begat Y";
- etiology, such as "hence the place is called Z";
- lists of names;
- reports of what authorities say, such as "some say".

**An episode is a maximal run of events that share one central figure.**
The central figure is the character who takes part, as doer or as sufferer, in the most events of the run.
An episode begins with the first event in which that figure takes part.
It ends where the text turns to events in which the figure takes no part.
A figure who returns after an interval of other events begins a new episode, and the census notes that the two are connected.

**Every episode of five events or more enters the corpus.**
None is excluded for any other reason.
Episodes of fewer than five events are listed in the census and counted, but not transcribed.

**The census is one line per episode, with a second file listing the events.**
Each census line gives an identifier, the citation span, the central figure, the number of events, and, from Stage 2, the hero.
The events file gives one line per event: its episode, its number, its citation and a plain paraphrase without Propp's terms.
The transcribers write exactly one entry for each listed event, so coverage has a fixed denominator and the two transcriptions can be compared event by event.
The files are `ApollodorusCensus.txt` and `ApollodorusEvents.txt`, committed before any transcription.

**Every listed episode is transcribed, and no sample is drawn.**
The protocol allowed a random sample if the corpus proved too large to transcribe; with model transcribers it is not too large.

**The census as taken: 412 episodes, 3,066 events, and 175 episodes to transcribe.**
Four fresh instances took it, one per part, and the keeper merged the parts with `Apollodorus/keeper.py merge`, which checks that every episode's count equals its listed events.
The 175 are the episodes of five events or more that are not variants, holding 2,513 events: 31 from the *Library*'s first book, 26 from its second, 72 from its third, and 46 from the *Epitome*.
Twenty-three sections yield no events; each is genealogy or a list, as the instance that took it reported.

**The four instances judged some unsettled points differently, and the census is kept as taken.**
All four treated groups acting together as figures, and all four let a short aside stay inside an episode, but their tolerance differed, from one event to about three.
Two counted a report introduced by "some say" as an event when it is the only account given, and two did not.
Where the first version of a story is genealogy only, they chose differently which version to list.
These choices change where episodes begin and end and how many events some hold.
The census makes no use of Propp's functions, so the differences add noise but cannot favor the grammar, and taking it again would itself be a choice made after seeing it.

## Stage 2: whose tale

**The hero is the character whose fortunes the episode follows.**
Propp draws the line this way at p.36: where a girl is carried off and the tale follows the one who goes after her, the hero is the seeker; where it follows the girl, the hero is the victim.
Operationally, the hero is the census's central figure.
Where two figures tie, the hero is the one who takes part in the episode's last event.
Where they still tie, the episode is transcribed once for each, and both versions are kept and marked.

**The hero is fixed on the census line before the episode is transcribed.**
This matters most for myths read differently from different sides.
From Zeus's side, Prometheus is a thief who is punished; from his own, he is the one who brings fire.
The rule decides between them before anyone asks which reading passes.

**The transcriber assigns functions, not roles.**
Propp defines each role by what its deeds mean for the hero (p.81), so roles follow from the functions and their performers.
The transcriber records who performs and who undergoes each function, and does not label anyone villain, donor or helper.

## Stage 3: transcription

**Each act in a census event gets one entry: a function symbol, or X.**
Most events narrate one act; where an event's words narrate two or more distinct acts, each act that fulfills a function gets its own entry, in the order narrated.
The pilot added this rule, since forcing one entry on an event that narrates a struggle and its outcome drops a function Propp's own tables would record.
Propp defines a function as "an act of a character, defined from the point of view of its significance for the course of the action" (p.21).
Where the act's significance is unclear, the function is defined by its consequences, as Propp does himself (p.67).

**When in doubt, write X.**
An event that fits no function is written X, with the nearest candidate in the notes, such as "X, perhaps D".
Stretching a function to cover an event is the error the test most needs to avoid, because a notation stretched to fit anything will make any grammar pass.
The share of X in the corpus is itself one of the measurements.

**The alphabet is Propp's.**
It consists of the preparatory functions α to θ and λ, and the functions A, a, B, C, ↑, D, E, F, G, H, I, J, K, ↓, Pr, Rs, o, L, M, N, Q, Ex, T, U and W.
A minus marks a negative result, as Propp marks it in Appendix III (p.46, note): E− for a failed test, F− where nothing is given, I− where the hero loses the fight.
A variety number, such as A¹, is written only where the transcriber can identify it from Propp's lists; otherwise the bare letter is written.

**Entries are written in the order the text narrates them.**
Propp's Appendix III records a tale's functions in the order the tale tells them, and the order is what the grammar tests.
A flashback is written where it is told, and marked as a flashback in the notes.

**A new move begins with each new villainy or lack.**
This is Propp's definition of the move (p.92).
Moves are numbered I, II, III within an episode.
Where one move breaks off for another and later resumes, each move is written separately, and the notes mark where the break and the resumption fall.

**Variants are transcribed apart.**
Where Apollodorus gives more than one version ("some say"), the first version he gives is the episode's main transcription.
Each other version is transcribed as a separate variant record and is not scored with the main corpus.

**The streams follow the format of the Russian corpus.**
The file is `ApollodorusStreams.txt`, in the format of `TaleTokenStreamsV4Utf8.txt`:

```
tale: <census identifier>
name: <citation span and central figure>
move: I   | <entries, separated by spaces>
move: II  | <entries>
```

**The notes give one line per entry, with its performers.**
The file is `ApollodorusNotes.txt`.
Each line gives the episode, the move, the entry's position, its citation, the symbol, who performs it, who undergoes it, a doubt mark where the transcriber is unsure, and a free note.
Appendix III records functions and not their performers, a gap the Russian corpus cannot fill.
The performers are recorded here so that questions such as whose punishment a U is can be answered from the record rather than guessed.

**A pilot of three episodes comes first.**
The keeper draws three episodes at random from the census.
Both transcribers transcribe them and report every place where a rule left them unsure what to write.
The rules in this stage are amended only at those reported gaps, and the amended protocol is committed.
The keeper does not parse the pilot, so no amendment can be made with the grammar's verdict in view.
The three pilot episodes are then left out of the scored corpus, because they were transcribed under rules that changed.

**The pilot was L2-028, L3-044 and L3-083, and it changed five rules.**
Both transcribers reported where the rules left them unsure, and the keeper did not parse their strings.
The amendments, each resting on a page of Propp, are in `Apollodorus/TranscriberRules.md`:
- an event that narrates several distinct acts gets an entry for each act that fulfills a function (p.67 for a single act read two ways);
- a function is assigned whoever performs it, the hero or a figure told of in passing (p.21);
- an act is judged by what it is and what follows it, not by whether its usual partner appears;
- an act only threatened or intended is X, unless Propp lists the threat as a form;
- a move exists only from its villainy or lack, so events after a move has begun and before the next villainy belong to the move already begun (p.92).
The two transcribers had divided on the last point, one placing such events in the earlier move and one in the later.

## From transcription to test

**The keeper's derivation rules are fixed here, before any transcription is read.**
They turn the streams and notes into the strings the grammar reads, by the same derivation `runCorpus.py` and `embedCorpus.py` apply to the Russian corpus.

**`Apollodorus/scoreApollodorus.py` carries the derivation, and it was committed before any transcription was read.**
Its `check` mode validates a transcription's form without parsing it; its `score` mode runs the test.

**The preparatory section is read as v46 reads it.**
Propp's Russian move schemes leave out the preparatory functions, and v46 places them at the tale's head, before the first move.
Preparatory entries in move I that stand before its first villainy, lack or mediation are therefore removed from the move string and counted.
A preparatory entry anywhere else stays in the string, and the move grammar judges it.

**Nothing standing before the opener is dropped.**
In the Russian corpus, cells Propp's table parks before A are dropped, because the park answers the table's layout.
A Greek transcription's order is the text's order, so every entry is kept where it is told.

**Every other entry is reduced as the Russian moves are.**
Varieties and signs are stripped, and KF is read as K and w as W, by `runCorpus.py`'s own reduction.

**Doubt produces two corpora.**
One keeps the entries marked as doubtful, and one drops them.
Both are scored and both are reported; the verdict is read on the corpus that keeps them, the transcriber's best reading.

**X is removed before parsing, and counted.**
The grammar's alphabet has no X.
Coverage, the share of events that received a function, is reported beside every acceptance figure.

**A fall after success is marked from the notes, not by the transcriber.**
The grammar's extension for a fall after success reads a sign, Rv, that Propp never used, so the transcriber is not given it.
Where the notes show a U, Q or Ex whose undergoer is the hero, after a liquidation K or a wedding W in the same move, the keeper writes Rv before it.
This is applied only in the run with the extensions switched on.

## The prediction

**Three measurements decide the test, with thresholds fixed before the run.**
- Coverage: the share of census events at least one of whose entries is a function rather than X.
- Acceptance: the share of moves `ProppEBNF46.txt` accepts, once as shipped and once with its commented extensions switched on (`+tragedy,reversal`).
- Discrimination: acceptance of the real strings against acceptance of the same strings shuffled.

**Discrimination guards against a grammar that accepts nearly anything.**
Each move's entries are shuffled many times, keeping the same symbols in a random order, and the grammar is run on the shuffles.
If the shuffled strings pass nearly as often as the real ones, acceptance says little about Greek myth.
The same shuffle is run on the Russian corpus, so the two gaps can be compared.

**The Russian baselines are computed, with their parameters committed before the run.**
As shipped, `ProppEBNF46.txt` accepts 80 of the 84 Russian moves, 95.2%.
Shuffled, 1000 times per move, the same moves pass 0.8% of the time with every symbol shuffled, and 1.7% with the opener kept first; `shuffleBaseline.py` computes this, and `ApollodorusPrediction.txt` records the parameters and the result.

**Short moves pass shuffled far more often, so the comparison is made at matched lengths.**
Among Russian moves of four functions or fewer, 14.3% of opener-fixed shuffles pass; among moves of seven or more, almost none do.
A handbook's summaries will be short, and a short string has few orderings for a grammar to refuse.
The Greek gap between real and shuffled acceptance is therefore compared with the Russian gap in the same length bands, 1 to 4, 5 to 6, 7 to 9 and 10 or more functions, and never overall.

**The thresholds are decided.**
- Coverage of at least 80%.
- Acceptance, as shipped, within 10 points of the Russian figure.
- A gap between real and shuffled acceptance at least as large as the Russian gap, in each length band that holds enough Greek moves to measure.

The claim holds if all three are met.
Acceptance is reported twice, as shipped and with the extensions, and the two results say different things.
Passing as shipped would mean Greek myth follows Propp's syntax as he gave it.
Passing only with the extensions would mean it follows that syntax with a turned ending, the fall that tragedy adds.
Neither is privileged: the claim is judged twice, once for each grammar, and the report sets the two verdicts side by side to show how much the extensions change.
Each transcription is scored on its own, and the claim holds only if it holds on both.
The run also reports where in the move the rejected strings fail, since failures clustered at one position would show a specific difference rather than a general one.

**The prediction is committed as `ApollodorusPrediction.txt` before Stage 3 begins.**

## Agreement

**The two transcriptions measure how far the result depends on the transcriber.**
The report gives the share of moves on which the two transcribers wrote the same string, and the number of single-entry changes separating them where they differ.
Low agreement does not stop the test, but every acceptance figure is then read with that doubt attached.

## Files and order

**Each file is committed before the stage after it begins.**
1. `ApollodorusProtocol.md`, this file, and after the pilot its amended version.
2. `ApollodorusCensus.txt`.
3. `ApollodorusPrediction.txt`, with the thresholds and the Russian baselines.
4. `ApollodorusStreams.txt` and `ApollodorusNotes.txt` from each transcriber, kept apart by a suffix, A and B.
5. The run and its report.

## Decisions

**Six decisions are made.**
- The thresholds: coverage of at least 80%; acceptance, as shipped, within 10 points of the Russian figure; and a gap over shuffled strings at least as large as the Russian gap in each length band with enough Greek moves.
- The *Epitome* is included, since it carries the Trojan cycle and the returns, Odysseus among them.
- An episode needs five events or more.
- Every listed episode is transcribed; no sample is drawn.
- Two fresh language-model instances on different models transcribe, a third takes the census, and an auditor checks fifty entries from each transcription.
- The grammar: both are scored, as shipped and with the extensions, with a verdict for each and neither privileged.
