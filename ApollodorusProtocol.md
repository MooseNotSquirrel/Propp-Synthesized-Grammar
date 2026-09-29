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

**The keeper freezes the files, runs the programs, and transcribes nothing.**
The keeper commits each stage's file to git before the next stage begins, so the history shows what was fixed when.
The keeper also computes the Russian baselines and applies the derivation rules in the section "From transcription to test".

**A second transcriber checks agreement on a random fifth of the corpus.**
The second transcriber meets the same conditions as the first and works without seeing the first transcriber's work.

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

**The census is one line per episode.**
Each line gives an identifier, the citation span, the central figure, and the number of events.
The file is `ApollodorusCensus.txt`, and it is committed before Stage 2.

**If the corpus is too large to transcribe, a random sample is drawn.**
The sample size and the random seed are committed before the draw.
Every episode in the census has the same chance of entering the sample.

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

**Each event gets exactly one entry: a function symbol, or X.**
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
The transcriber transcribes them, the rules in this stage are amended where the pilot shows a gap, and the amended protocol is committed.
The three pilot episodes are then left out of the scored corpus, because they were transcribed under rules that changed.

## From transcription to test

**The keeper's derivation rules are fixed here, before any transcription is read.**
They turn the streams and notes into the strings the grammar reads, by the same derivation `runCorpus.py` and `embedCorpus.py` apply to the Russian corpus.

**Doubt produces two corpora.**
One keeps the entries marked as doubtful, and one drops them.
Both are scored and both are reported.

**X is removed before parsing, and counted.**
The grammar's alphabet has no X.
Coverage, the share of events that received a function, is reported beside every acceptance figure.

**A fall after success is marked from the notes, not by the transcriber.**
The grammar's extension for a fall after success reads a sign, Rv, that Propp never used, so the transcriber is not given it.
Where the notes show a U, Q or Ex whose undergoer is the hero, after a liquidation K or a wedding W in the same move, the keeper writes Rv before it.
This is applied only in the run with the extensions switched on.

## The prediction

**Three measurements decide the test, with thresholds fixed before the run.**
- Coverage: the share of events that received a function rather than X.
- Acceptance: the share of moves `ProppEBNF46.txt` accepts, once as shipped and once with its commented extensions switched on (`+tragedy,reversal`).
- Discrimination: acceptance of the real strings against acceptance of the same strings shuffled.

**Discrimination guards against a grammar that accepts nearly anything.**
Each move's entries are shuffled many times, keeping the same symbols in a random order, and the grammar is run on the shuffles.
If the shuffled strings pass nearly as often as the real ones, acceptance says little about Greek myth.
The same shuffle is run on the Russian corpus, so the two gaps can be compared.

**The keeper computes the Russian baselines before Stage 3.**
As shipped, `ProppEBNF46.txt` accepts 80 of the 84 Russian moves.
The keeper adds the Russian shuffle acceptance, with the number of shuffles and the random seed committed first.

**The thresholds are a decision still to be made, and these are recommended values.**
- Coverage of at least 80%.
- Acceptance, as shipped, within 10 points of the Russian figure.
- A gap between real and shuffled acceptance at least as large as the Russian gap.

The claim holds if all three are met.
Acceptance is reported twice, as shipped and with the extensions, and the two results say different things.
Passing as shipped would mean Greek myth follows Propp's syntax as he gave it.
Passing only with the extensions would mean it follows that syntax with a turned ending, the fall that tragedy adds.
Which of the two the claim requires is one of the decisions before Stage 1.
The run also reports where in the move the rejected strings fail, since failures clustered at one position would show a specific difference rather than a general one.

**The prediction is committed as `ApollodorusPrediction.txt` before Stage 3 begins.**

## Agreement

**The second transcriber's work measures how far the transcription depends on the transcriber.**
A random fifth of the corpus is drawn, with the seed committed first, and transcribed independently.
The report gives the share of moves on which the two transcribers wrote the same string, and the number of single-entry changes separating them where they differ.
Low agreement does not stop the test, but every acceptance figure is then read with that doubt attached.

## Files and order

**Each file is committed before the stage after it begins.**
1. `ApollodorusProtocol.md`, this file, and after the pilot its amended version.
2. `ApollodorusCensus.txt`, with the sample size and seed if a sample is drawn.
3. `ApollodorusPrediction.txt`, with the thresholds and the Russian baselines.
4. `ApollodorusStreams.txt` and `ApollodorusNotes.txt`, and the second transcriber's files.
5. The run and its report.

## Decisions before Stage 1

**Six decisions are open, and each has a recommendation but one.**
- The thresholds in "The prediction": the recommended values above.
- Which grammar the claim requires, as shipped or with the extensions: no recommendation, since it is the substance of the claim.
- The *Epitome*: include it, since it carries the Trojan cycle and the returns, Odysseus among them.
- The event threshold for an episode: five events.
- The sample size, if the census is too large: set after the census, by how much transcription is feasible, and committed before the draw.
- Who transcribes: someone who has not seen the grammar, and a second person for the agreement check.
