# Measuring the measurer: blind machine transcription against Propp's own analyses of the 45 tales of his Appendix III

*Draft. Figures are taken from the result files named in section 10.*

## Abstract

**Propp's printed analyses of Russian wondertales have served for nearly a century as an answer key, but how far another reader reproduces them has been tested only on a handful of tales.**
We transcribed all 45 tales whose function schemes Propp printed in Appendix III of the *Morphology of the Folktale*, reading the tales in the original language, with two language-model transcribers that never saw his schemes.
The transcribers find 74% to 77% of the functions Propp found, far beyond chance: matched against Propp's scheme for a different tale, the same transcriptions agree 0.40 to 0.42 on content, against 0.58 to 0.59 for the right tale, and no one of 1000 random pairings comes close.
They agree with Propp less than they agree with each other (content 0.58 to 0.59 against 0.75; order 0.34 to 0.37 against 0.59), chiefly because they mark functions where Propp marks none and divide the tales into more moves.
A rule that folds repeated functions into one, as Propp's schemes do, closes only a small part of the gap on held-out tales.
A memory probe finds no sign that the models recall Propp's schemes.
We argue that Propp's schemes are a compressed and partly inferred record, so that agreement with them has a ceiling well below one, and that studies using them as ground truth should measure against that ceiling, not against perfect agreement.

## 1. Introduction

**Propp's *Morphology of the Folktale* (1928) reduced the plots of one hundred Russian wondertales to a sequence of 31 functions, the acts of characters defined by their significance for the course of the action.**
In Appendix III he printed the scheme of 45 of those tales: for each tale, the string of function symbols it realizes, divided into moves, the units of plot that run from a villainy or lack to its resolution.
These schemes are the most concrete part of the book.
Folklorists have used them as models when analyzing other corpora, and computational work on narrative has used them as the reference against which annotations and learned models are scored.

**An answer key is only as useful as it is reproducible, and Propp's has rarely been tested.**
If a careful reader, given Propp's definitions, cannot arrive at Propp's schemes from the tales, then disagreement with Propp measures the key as much as the reader.
The few published tests, discussed in section 2, used between three and fifteen tales, read in English translation, by annotators who in one case were given Propp's schemes to place in the text.

**This paper tests reproducibility on all 45 tales, in the original language, with transcribers that never see the schemes.**
The transcribers are two language models working under fixed written rules and a one-page definitions card.
Using two of them gives a yardstick: the agreement between two transcribers of the same tale is the most one can expect either to show with Propp.
A chance baseline, pairing each transcription with Propp's scheme for a different tale, shows how much agreement comes from what all wondertales share.
Every measure, threshold and baseline was fixed in a written protocol before any transcription was read.

**The contributions are four.**
First, a measurement of how closely blind transcription reproduces Propp's schemes, against both a chance baseline and the transcribers' agreement with each other.
Second, a diagnosis of where the disagreements come from, symbol by symbol.
Third, a held-out test of whether a simple rule can bring the transcriptions into Propp's form.
Fourth, a comparison with published human annotations of the same tales.

## 2. Prior work

**Three lines of work have compared annotations with Propp's schemes, each on few tales.**
Bod, Fisseni, Kurji and Löwe (2012) trained university students in Propp's system for 45 minutes and had them annotate three tales in English translation; nine students took part in a first experiment and six in a second.
They compared the students' function strings with Propp's by inspection and found that the assignment of characters to Propp's roles, and some functions, were hard to reproduce.
Fisseni, Kurji and Löwe (2014) extended this with training experiments and concluded that the system can be trained reliably for simple tales with sufficient time.

**Finlayson's ProppLearner corpus annotated fifteen tales from Propp's corpus in English translation, but its annotators placed Propp's functions rather than finding their own.**
Finlayson (2015/2017) restricted the corpus to tales of a single move and had two trained annotators mark each function Propp's Appendix III assigns to the tale, choosing the passage that realizes it.
Agreement between the annotators was 0.22 by strict F1 and 0.71 by a lenient measure that counts overlapping regions.
He named four obstacles that recur in our results: unclear placement of functions in the text, implicit functions that no words express (his example is C, the hero's decision to act), inconsistently marked trebling, and schemes that disagree with the tale.
Finlayson (2016) then learned Propp's functions from that annotation.

**Gervás and Méndez (2024) asked two language models to tag English synopses of eleven tales with Propp's functions and scored them against Propp's assignment.**
Precision ranged from 0.37 to 0.46 and recall from 0.22 to 0.34 across models and prompting strategies, and the authors reported the results as negative.

**What this study adds is scale, the original language, blindness, and controls.**
It uses all 45 tales of Appendix III, read in the original; the transcribers never see Propp's schemes, and a probe checks whether they recall them; two transcribers give a yardstick, a derangement baseline gives chance, and the protocol was fixed before the data.
Seven of Gervás and Méndez's tales (93, 104, 127, 131, 133, 139, 155) and two of Bod and colleagues' (151, 152) are among our 45, which allows a tale-by-tale comparison (sections 7 and 8).

## 3. Material

**The tales are the 45 of Appendix III, numbered 93 to 167 in the modern numbering of Afanasyev's collection.**
Their texts were taken from Russian Wikisource, which follows the academic edition of 1984-85, and cut out by number with the editors' notes, footnotes and wiki markup removed.
The 45 texts hold 62,497 words.
Most are Russian; by the listers' reading three are Belarusian (126, 132, 135), one Ukrainian (133), and one strongly dialectal (143).

**Propp's schemes were read from a machine-readable transcription of Appendix III made for an earlier project.**
Each scheme is reduced to its base symbols, with Propp's numbered varieties and signs dropped.
Where Propp groups repeated or parallel episodes in braces, every row is kept, in printed order; where he embeds one move inside another, the embedded move is expanded where it stands.
Propp's schemes print no preparatory functions (the first seven, which set up the tale before the villainy), so these are left out of both sides of every comparison.
The result is 84 moves and 737 function symbols.

**One discrepancy with a prior study was checked against the printed page.**
Bod and colleagues print the opening of tale 151 as A8, a villainy; Appendix III reads a⁵, a lack, as our transcription has it.

## 4. Method

### 4.1 Two stages, fresh instances, nothing shared

**Each tale was first listed as a sequence of events, and the events were then transcribed into Propp's functions.**
Three fresh model instances (Claude Opus; exact model versions to be taken from the run records), each given fifteen tales, listed every event in each tale in order, in English, with the character who takes part in the most events named as the hero.
They listed 1,633 events.
The listers were told nothing about Propp.

**Two transcribers then assigned Propp's functions to every listed event, blind to each other and to Propp's schemes.**
Transcriber A was Claude Opus and transcriber B Claude Sonnet, each run as fresh instances, three batches of fifteen tales each.
They read the tale in its original language and wrote in English.
For each event they wrote one entry per act: the function symbol, or X where no function applies; the performer and the one acted on; whether the act matters to the course of the tale; the quoted words it rests on; and the move it belongs to.
The rules and the definitions card are those used in earlier tests of fables and Greek tragedies with the same method.
Nothing given to a transcriber said that Propp had analyzed these tales.

**The definitions card states each function in one or two lines, in Propp's terms.**
The card was written for the earlier tests from Propp's chapter III and kept unchanged here, so that the calibration measures the instrument those tests used.

### 4.2 Two arms

**The instrument was run twice: once with the card as used, and once with one sentence added.**
An audit in the earlier fable test found that transcribers wrote complicity (θ, the victim yielding to a deception) also for victims who refused or saw through the trick.
Arm U uses the card as it was; arm C adds to the θ line that a victim who refuses or sees through the trick has not performed θ.
Each arm was transcribed by both transcribers, from the same event lists.

### 4.3 The memory probe

**After both arms were transcribed, fresh instances of each model were asked to recall Propp's scheme for each tale from memory.**
Each was given the tale's number and Russian title, told not to work a scheme out from the plot, and asked for the scheme or "unknown", with a confidence.
The probe had to come last, because its prompt names Propp's appendix.

### 4.4 Measures, yardstick and baseline

**Each transcription becomes, per tale, the string of its function symbols marked as mattering, in the order of its notes.**
X entries and preparatory functions are left out, and symbols are reduced to base symbols as Propp's are.
Four measures compare a transcription with Propp:
- **content**, the Dice overlap of the two multisets of symbols, averaged over tales;
- **order**, one minus the Levenshtein distance between the two strings divided by the longer one's length, averaged over tales;
- **moves**, the share of tales whose move count equals Propp's;
- **acceptance**, the share of the transcription's moves accepted by a formal grammar of Propp's move sequence, written in an earlier project from Propp's text, which accepts 80 of Propp's own 84 moves.

**The yardstick is the agreement between the two transcribers, and the baseline is agreement with the wrong tale.**
Measures 1 to 3 computed between transcribers A and B of the same arm show how far two transcribers agree, the most one can expect either to show with Propp.
For the baseline, each transcription is set against Propp's scheme for a different tale, under 1000 random derangements of the 45 tales (seed 46).

**The verdict rule was fixed in advance.**
The instrument is calibrated if content and order with Propp each reach 0.8 of the transcribers' agreement with each other, both beat the baseline with at most 50 of 1000 derangements at or above, and the grammar accepts at least 75% of the moves.
It is partly calibrated if the baseline criterion holds and any other fails, and not calibrated if the baseline criterion fails.

## 5. Results

### 5.1 The calibration

**By the rule fixed in advance, the instrument is partly calibrated, in both arms and for both transcribers.**

| Arm, transcriber | Content with Propp | Order with Propp | Baseline content, order | Moves equal | Grammar accepts |
|---|---|---|---|---|---|
| U, A (Opus) | 0.591 | 0.364 | 0.404, 0.202 | 33.3% | 28.9% of 142 |
| U, B (Sonnet) | 0.592 | 0.363 | 0.421, 0.210 | 37.8% | 22.5% of 129 |
| C, A (Opus) | 0.593 | 0.371 | 0.405, 0.199 | 28.9% | 28.8% of 139 |
| C, B (Sonnet) | 0.578 | 0.342 | 0.423, 0.207 | 28.9% | 27.0% of 152 |
| A against B, arm U | 0.754 | 0.590 | | 55.6% | |
| A against B, arm C | 0.750 | 0.586 | | 33.3% | |

**The transcriptions are about the tale in front of them.**
In every cell, agreement with the right tale's scheme exceeds agreement with any other tale's, and none of 1000 derangements reaches the real figure.

**They agree with Propp less than with each other.**
Content reaches 0.77 to 0.79 of the transcribers' mutual agreement, just short of the 0.8 required; order reaches 0.58 to 0.63.
The transcribers cut the tales into 129 to 152 moves where Propp has 84, and the grammar that accepts 80 of Propp's moves accepts 23% to 29% of theirs.

**The raw content figure flatters the agreement, because any two wondertale schemes already share much.**
Corrected for chance, as (real − chance) / (1 − chance), content agreement with Propp is 0.30 to 0.31, against 0.57 between the transcribers; order is 0.19 to 0.20, against 0.49.
On this scale the instrument matches Propp about half as well as it matches itself.

### 5.2 Recall and precision

**The transcribers find three quarters of Propp's functions, and half of what they write is in his schemes.**
Matched as multisets tale by tale, transcriber A finds 73.7% of Propp's 737 symbols and transcriber B 77.3% in arm U (75.2% each in arm C).
Of the symbols they write, 1,058 and 1,157 in arm U, 51.3% and 49.3% are in Propp's scheme for the tale.
Counting each function once per tale on both sides, the question becomes which functions a tale contains, and agreement rises to 0.75 and 0.78, with 80% and 84% of Propp's functions found.

### 5.3 The arms and the probe

**The corrected card changes nothing measurable.**
Arm C's figures differ from arm U's by about 0.02 or less on content and order, in either direction.

**The models do not recall Propp's schemes.**
The Opus instance answered "unknown" for 44 tales and gave one scheme at low confidence; the Sonnet instance answered "unknown" for all 45.
By the rule fixed in advance (recall content at least 0.15 below the model's transcription content), recall from memory is implausible.

**The tales where the hero rule picks someone other than Propp's hero are not outliers.**
In four tales (149, 151, 163, 164) the listers' rule named a different character from the one Propp's scheme follows; their figures fall within the range of the rest.

## 6. Where the disagreements come from

**The transcribers mark more functions than Propp, and the excess is concentrated in a few.**

| Symbol | Propp | Transcribers (mean of A and B, arm U) | Ratio |
|---|---|---|---|
| F, receipt of a magical agent | 57 | 138.5 | 2.43 |
| I, victory | 35 | 83.5 | 2.39 |
| a, lack | 30 | 70.5 | 2.35 |
| M, difficult task | 13 | 35.5 | 2.73 |
| N, solution | 15 | 32.5 | 2.17 |
| A, villainy | 55 | 94.0 | 1.71 |
| C, decision to counteract | 65 | 44.5 | 0.68 |
| T, transfiguration | 9 | 6.0 | 0.67 |
| ↓, return | 45 | 38.0 | 0.84 |
| Pr, pursuit | 20 | 17.0 | 0.85 |

**Part of the excess is repetition.**
A hero who receives three gifts, or wins three fights, is often written F or I once in Propp's scheme, or grouped in braces, but three times by the transcribers.
Finlayson reports inconsistent marking of such trebling in Propp's schemes.
Section 7 tests how much of the gap this explains.

**Part of the shortfall is inference.**
Propp writes C, the hero's decision to act, where the tale moves straight from the call to the departure without stating a decision.
The transcribers, who mark acts the text expresses, write C about two thirds as often.
Finlayson names the same function as his example of an implicit one.

**Move division differs most.**
The transcribers' move counts equal Propp's in 29% to 38% of tales, and each other's in 33% to 56%.

**The order gap is not an artifact of how Propp's braces are flattened.**
On the 22 development tales of section 7, tales whose schemes contain braces or embedded moves agree on order slightly better (0.36, 0.37) than tales without (0.33, 0.34).

## 7. Can the transcriptions be brought into Propp's form?

**We fixed a test in advance: develop a rule on half the tales, then score it once on the other half.**
The 45 tales were split at random (seed 46) into 22 development tales and 23 test tales.
On the development tales we tried folding immediately repeated runs of functions, writing each function once per move or once per tale, supplying an implicit C before a departure that follows a villainy, lack or mediation with no C between, and keeping only functions that several of the four readings (two arms, two transcribers) give an event.
The rule chosen, before the test tales were scored, writes each function once per move where it first appears and then supplies the implicit C.
A rule would be adopted if, in all four readings, content and order each improved significantly (one-sided paired sign-flip test, p at most 0.05), each improvement was at least half the improvement on the development tales, and both still beat the baseline.

**The rule was not adopted.**
On the development tales it raised content by 0.09 to 0.13 and order by 0.09 to 0.11.
On the test tales it raised content by 0.040 to 0.058, significant in all four readings (p at most 0.004), but only one reading reached half its development gain; it raised order by 0.018 to 0.030, significant in one reading.
Folding repetition explains a small, real part of the content gap and almost none of the order gap.

**Consensus does not help either.**
Keeping only the functions three of four readings agree on did no better than a single reading, which means the readings' departures from Propp are shared, not independent noise.

## 8. A human benchmark

**Published annotations of two of our tales give a first comparison with human readers.**
Bod and colleagues print the function strings their students wrote for tales 151 (*Shabarsha*) and 152 (*Ivanko*), nine in one experiment and six in another.
Scored exactly as the models are, the students reach content 0.62 to 0.68 with Propp on 151, against 0.54 for the models, and 0.59 to 0.60 on 152, level with the models' 0.59.
On order the students do better (0.43 to 0.53, against 0.37 to 0.38), in part because they wrote short lists of the functions present, as long as Propp's, where the models record every occurrence.
The students agree with each other (content 0.55 to 0.63) about as well as they agree with Propp.

**A reader who knows Propp's system well, working from the same event lists and card, matched Propp less closely than the models did.**
Five tales were chosen in advance (93, 131, 133, 145, 151), and the rule for reading the result was fixed before the annotation: if the human matched Propp no better than the models, or better by at most 0.05, the models would be read as near the task's ceiling.
The reader recalled none of the five schemes and worked from the English event lists alone.
Content with Propp was 0.39, against 0.59 for the models; order 0.26, against 0.39; the reader was below the models on every tale.
The reader agreed with the models (content 0.50 to 0.55) more than with Propp.
Like the models, the reader marked more functions than Propp (106 symbols against his 60), but on different ones: the hero's reaction E 27 times against Propp's 4, where the models' excess falls on F, I and a.
In tale 151 the reader judged that the hero the event lists named, the Little Devil, is not the hero, and read Shabarsha's tricks as a donor's tests; Propp reads them as contest and victory over the villain.
One reader and five tales decide nothing alone, but together with the students' strings they point the same way: the gap between any careful reader and Propp's schemes is mostly the schemes' own conventions.

**On the tales Gervás and Méndez used, the transcribers find far more of Propp's functions than tagging from synopses did.**
On those seven tales our transcribers find 77.8% to 81.7% of Propp's symbols, with 44% to 48% of theirs in his schemes; Gervás and Méndez report recall of 0.22 to 0.34 and precision of 0.37 to 0.46.
The measures are not identical (theirs match labels to passages of a synopsis, ours match multisets of symbols per tale), so the comparison shows a difference of degree, not a like-for-like gain.

## 9. Discussion

**Agreement with Propp's schemes has a ceiling well below one, and the ceiling belongs to the schemes as much as to the readers.**
Two transcribers who share rules, card and event lists agree with each other at 0.75 on content; students trained in the system agree with each other at 0.55 to 0.63.
Propp's schemes add choices no reader can recover from the text: which repetitions to fold, which implicit decisions to write, where one move ends and the next begins.
A reader who matched Propp perfectly would be reproducing his conventions, not only reading the tale.

**Studies that score against Propp should score against that ceiling and against chance, not against perfect agreement.**
Raw agreement overstates what is shared: two wondertale schemes picked at random already agree about 0.4 on content.
Thresholds set from Propp's own schemes can be out of reach for any instrument.
In companion tests on fables and Greek tragedy, thresholds for grammar acceptance and coverage set from Propp's schemes could not be met by this instrument even on Propp's own tales, so their failure said nothing about the genres; comparisons made instrument to instrument, with these 45 transcribed tales as the reference, did.

**What the instrument does well is read the tale in front of it, consistently.**
It beats the wrong-tale baseline in every cell, two different models agree with each other well beyond chance, and a correction to the card changes nothing measurable.
Measures that compare the instrument with itself, such as shuffle baselines or one genre against another, are therefore on firmer ground than measures that compare it with Propp's printed levels.

**Limitations.**
Both transcribers and the listers are models of one family, so their shared departures from Propp may reflect a shared reading; a third family, and the human benchmark, are needed to separate the two.
The event lists were made by models and fixed the units the transcribers labeled; Propp worked from the tales directly.
The rules and card are in English while the tales are not.
Appendix III covers 45 of Propp's hundred tales; the others have no printed scheme to compare with.

## 10. Data and code

**Every text, prompt, transcription and program is public, and every result can be rerun.**
- The tale texts, extraction, rules, prompts, event lists, transcriptions and probe answers: the repository Propp-Afanasyev.
- Propp's schemes and the grammar: the repositories Propp-Grammar and Propp-Synthesized-Grammar.
- The protocol and comparison program (`Calibration/CalibrationProtocol.md`, `Calibration/compare.py`, output `Calibration/CompareRun.txt`); the improvement test (`Calibration/ImproveProtocol.md`, `Calibration/Split.txt`, `Calibration/improveTest.py`, outputs `Calibration/ImproveDev.txt` and `Calibration/ImproveTestRun.txt`); the published human strings and their scoring (`Calibration/PriorHuman/`): Propp-Synthesized-Grammar.

## References

*Every reference is to be checked against its source before submission.*

Bod, R., Fisseni, B., Kurji, A. and Löwe, B. (2012). Objectivity and reproducibility of Proppian narrative annotations. *Proceedings of the Third Workshop on Computational Models of Narrative (CMN 2012)*, 15-19.

Finlayson, M. A. (2016). Inferring Propp's functions from semantically annotated text. *Journal of American Folklore* 129, from p. 55. [Pages to be checked.]

Finlayson, M. A. (2017). ProppLearner: Deeply annotating a corpus of Russian folktales to enable the machine learning of a Russian formalist theory. *Digital Scholarship in the Humanities* 32(2), from p. 284. [Pages to be checked.]

Fisseni, B., Kurji, A. and Löwe, B. (2014). Annotating with Propp's *Morphology of the Folktale*: reproducibility and trainability. *Literary and Linguistic Computing* 29(4), 488-510.

Gervás, P. and Méndez, G. (2024). Tagging narrative with Propp's character functions using large language models. *Proceedings of the Text2Story'24 Workshop*, CEUR Workshop Proceedings 3671.

Propp, V. (1928). *Morfologiya skazki*. Leningrad: Academia. English: *Morphology of the Folktale*, 2nd ed., trans. L. Scott, rev. L. A. Wagner. Austin: University of Texas Press, 1968.
