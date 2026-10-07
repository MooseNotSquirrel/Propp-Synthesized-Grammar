# Preliminary findings

**This file gathers what the genre tests and the building-block work have found so far, what has been withdrawn, and the readings and ideas worth keeping for when all the data is in.**
It is a working document, not a result: every figure below is recorded, with its program and its frozen rule, in the file each entry names, and those files win wherever this one disagrees with them.
Each entry is marked: ESTABLISHED (frozen before the data, or replicated on unseen data, and passing the risk checks), TENTATIVE (measured, not yet replicated or checked), WITHDRAWN, or SPECULATION, NOT FROM PROPP (a reading, labelled as such).
Last brought level: 2026-10-06, after the seal on the tragedies was lifted.

## 1. The genre tests of Propp's whole morphology

**WEAKENED BY THE CALIBRATION (2026-10-05): that Propp's full grammar does not describe Greek myth summaries or Aesop's fables.**
Apollodorus failed on every measure; Aesop failed on coverage and order (Propp-Apollodorus, Propp-Aesop, each with its result file).
The tragedy test is complete, 32 of 32 plays: by its frozen thresholds the claim does not hold for either grammar or transcriber (coverage 38% to 39%, acceptance 30% to 36%; `Tragedy/TragedyRun-All.txt`).
BUT the thresholds those tests used, 85.2% acceptance and 80% coverage, were set from Propp's own schemes, and the instrument does not reach them on Propp's own tales: v46 accepts 22% to 29% of its moves for the 45 Appendix III tales, below Aesop's 57% to 59%, and it covers 62% to 67% of their events (section 7). So the acceptance and coverage failures measure the instrument at least as much as the genre. What survives: Apollodorus (57% to 70%) and Aesop (56% to 57%) do not clearly differ from Propp's tales in coverage; the tragedies do, tested instrument to instrument (below).

**ESTABLISHED (2026-10-06): measured with the same instrument, the 32 tragedies cover far fewer of their events with Propp's functions than the 45 Russian tales, and run against Propp's order far more often.** Coverage 38% and 39% against 63% and 68%; function pairs backward against Propp's numbering 44% and 46% against 28% and 31%, where random order gives 50%; both p 0.0001, both transcribers, frozen before the seal lifted (`Tragedy/ReferenceComparison.md`, `ReferenceRun.txt`). Acceptance does not separate the genres (p 0.11, 0.20), as the calibration led us to expect.

## 2. Propp's blocks

**ESTABLISHED: the two halves of Propp's pairs and groups are told together, next to each other, more often than chance.**
Found in the training fables and tragedy P01-P04, replicated on the 99 held-out fables, and it passes the risk checks:
- against a positional null that keeps each function's habits of position, it survives in every fable cell and in tragedy's strict reading (`Blocks/PositionNull.txt`);
- the two transcribers find the same blocks in the same story beyond chance in every fable cell (`Blocks/Agreement.txt`);
- it holds whether the incidental and doubtful entries are matched or not, 35 of 36 cells (`Blocks/Robustness.txt`).
`DeceptionTrap` is the most reliable block: about three times chance in the fables, and 78% to 88% of its instances found by both transcribers. BUT THE OWNER'S AUDIT (`Blocks/TrickAudit.txt`, 13 of 20 supported, DOUBTFUL by its rule) found that it is the trick and the victim's RESPONSE, not always the complicity Propp names: the trick is real in all 20, but in 6 the victim balks or sees through it and the transcribers wrote θ anyway, both of them in the same fables. So part of the block's count and of the transcribers' agreement on it comes from that shared habit. Read faithfully, about two thirds are complicity and about a third its refusal.

**ESTABLISHED (2026-10-06): the blocks hold in tragedy too, on 28 unseen plays.** The frozen prediction (`Tragedy/BlockPrediction.txt`, results in `KeeperLog.md`): adjacency holds in both readings for both transcribers (blocks 49% to 50% of functions against 35% to 40% shuffled, strict 29% to 32% against 19% to 20%, 0 of 200 each), and complication and RuleViolation each occur above chance. On P01-P04 alone the effect had looked weaker; with 28 plays it does not. On the held-out plays the transcribers find the same blocks beyond chance in both readings (61% and 63% against 51%, 0 of 200; `Tragedy/AgreementHeldOut.txt`); and the effect survives the positional null in all four cells (0 of 200 each; `Tragedy/PositionNullHeldOut.txt`), where on P01-P04 the loose reading had looked like habit of position.

**NOT SHOWN: a fixed order inside tragedy's free blocks.** Forward occurrences far outnumber reversed ones (15 to 3 and 12 to 0), but transcriber A's 3 reversals exceed the shuffled mean (1.63), so the frozen prediction fails.

**WITHDRAWN: that the order inside a block is near obligatory, like the fixed order inside a phrase of Latin or Russian.**
The definitions card defines the second half of most blocks by the first ("taken in by the deception", "the prohibition is broken", "the task is accomplished"), so a reversal can occur only in a flashback, and the absence of reversals measures the card, not the stories (`Blocks/DefinitionCheck.md`).
Order inside a block can be tested only on the blocks the card leaves free: `StruggleAndOutcome`, `FraudPosture`, `ReturnJourney`, `Ordeal`, and the free parts of `complication` and `TestedAcquisition`. They are rare so far.

**THE CARD IS KEPT, AND NOTHING IS RE-TRANSCRIBED (decision, 2026-09-30).**
The coupling is Propp's own: he defines complicity as yielding to the deception and violation as breaking the interdiction, so a card that decoupled them would no longer describe his functions, and the Afanasyev calibration needs his definitions. The coupling makes order inside those blocks a matter of logic, not of evidence; it does not touch co-occurrence and adjacency, which the transcribers could have found or not, and it does not touch the order between blocks. Re-transcribing would also break the tragedy test's single instrument. What changes is the claim, not the data.

## 3. The order between blocks

**ESTABLISHED, IN PART: the fable grammar failed its frozen test on coverage, and its order held on unseen fables.**
`FableEBNF01.txt` accepted 55.6% and 61.7% of the held-out fables against a frozen 65%, so the claim that it describes most fables fails. Its gap over shuffled order held (+27.4 and +29.8 against a frozen 20), and beat v46's (+10.6 and +15.1) (`Fables/KeeperLog.md`).
So the order between blocks is not free, as the plan first supposed: it is a strong preference, not a rule. CORRECTED 2026-10-06 by the genre order test (`Blocks/GenreOrder.md`, `GenreOrderRun.txt`): measured pair by pair, Propp's order fits the held-out fables as well as an order fitted to the fables (gaps +0.218 and +0.168 against +0.220 and +0.152), and the same holds for the Russian tales. So the fables' order is not shown to be their own; the fable grammar's advantage was over v46's yes-or-no moves, not over Propp's order. Of the three genres, only tragedy has an order of its own that Propp's does not match (prediction 1 fails for that reason; prediction 2, that the wondertale follows Propp at least as well as the other genres' orders, holds). A yes-or-no grammar is the wrong instrument for a preference; a scored model of block order is the right one, and would be tested on the about 110 undrawn fables.

**ESTABLISHED (2026-10-06): tragedy orders the blocks in an order of its own, closer to the plays than Propp's order.** The tragedy block grammar, frozen as a scored order model (`Tragedy/TragedyOrder01.txt`, `TragedyGrammarPrediction.txt`): each block's mean position fitted on P01-P04 alone. On the 28 held-out plays the fitted order beats shuffling by +0.133 and +0.122 (0 of 1000 shuffles as high; +0.06 needed), and Propp's order by about double (Propp's gap +0.072 and +0.063). It kept most of its training gap (+0.166, +0.135). A preference, not a rule: the concordance is 0.62 to 0.63 against 0.50. Propp's order is present in tragedy, but weaker than tragedy's own.
In the fitted order the villainy or lack and the backstory's recognitions, rewards and marriages come early; the complication, the broken prohibition and the struggle in the middle; the deception, the departure, the exposure, the liquidation and the ending late (ranks in `TragedyOrder01.txt`). In Propp's sequence trickery and complicity (6, 7) precede the villainy (8), and the departure (11) precedes the liquidation (19) by much.

**SPECULATION, NOT FROM PROPP: tragedy begins after the harm is done and saves the trick for the catastrophe** (Clytemnestra's welcome, Medea's gifts, Dionysus's luring of Pentheus): the deception moves from the tale's preparation to tragedy's climax. And Propp's claim in the Oedipus essay that tale and myth share their composition holds for the pieces and not for their order: two languages sharing a vocabulary with different word orders.

**ESTABLISHED (2026-10-06): in the Russian tales, Propp's order of his large sections is right, but it holds as a strong tendency, not a rule.**
Of pairs of functions in different sections of a move (complication, donor, transfer, struggle, liquidation, return, arrival and claims, task, endgame), 2.5% run against his order in his own schemes but about 16% in readings of the same tales, by both machine transcribers and by the owner, against 50% for random order (`Calibration/SectionOrderExplore.txt`).
A scored section grammar fitted on 22 tales did no better than Propp's order on the other 23 (frozen in `Calibration/SectionGrammar.md`; result `SectionGrammarRun.txt`: concordance about 0.84 for both, differences +0.005 and +0.007, not significant).
So Propp's sequence is the best simple description of the wondertale's order; his schemes overstate how strictly it holds, in part through his conventions (folding repeats, writing an implicit C, parking pre-crisis events, licensing the donor before the trouble).
A yes-or-no grammar cannot capture an order that holds five times in six, which is why v46, built on Propp's tidy strings, accepts only 22% to 29% of fresh readings of the same moves.

**SPECULATION, NOT FROM PROPP: the content of a tale is categorical and its order statistical.** Propp's pairs and groups hold together as units in every genre tested; their order is a preference whose strength and shape differ by genre, close to Propp's in the wondertale and the fable, its own in tragedy. On that reading the semantic catalog, which describes the units, is the primary tool, and order is a measured tendency.

**SPECULATION, NOT FROM PROPP: story languages may be like languages with free word order, such as Latin and Russian, in the order BETWEEN their units: strong default orders, departed from for effect.** The half of the analogy about fixed order inside the unit is withdrawn (section 2).

## 4. The fable as a genre

**ESTABLISHED, WITH THE AUDIT'S CORRECTION: the fables' kernel is the villain's want, the trick and the victim's response, then the harm (`a DeceptionTrap A`).** The audit found about a third of the 'complicity' to be refusals, so where the response is a refusal the kernel is the trick foiled, the second outcome below. Found in the training fables and recurring in the held-out ones: the trick block is followed by the harm 10 times in 27 and 8 times in 20.

**TENTATIVE, AND STRENGTHENED BY THE AUDIT: the trick has two outcomes.** In the held-out fables it is also followed by its defeat, victory I or rescue Rs, 6 times in 20, often with an exposure after; and the audit found the same split at the victim's response itself, about a third refusing. Noticed on the held-out fables and in the audit, so it needs fresh fables to test, with a card that separates yielding from refusing.

**SPECULATION, NOT FROM PROPP:**
- Many fables are the villain's move told from the villain's side, and end where Propp's tale begins: the fable is the magic tale's preparatory section made into a whole story, and the harm is the lesson.
- Propp's corpus left out Afanasyev's animal tales, numbers 1 to 49, the trickster's genre. The trickster is not missing from Propp's model: it is a character moving between two of his spheres, villain and hero, and the genre where that movement is the whole story is the one he excluded.

## 5. Characters (a quick look, not a frozen measure)

In the 199 fables: heroes about 71% animal, 22% human, 4% gods; the harm done mostly by predators, lion 17, eagle 10, cat 8, but also by goats, crows and robbers; tricks played most by the thief, the fox and the cat.
**SPECULATION, NOT FROM PROPP:** the mighty fall about as often as they strike: the lion and the eagle are victims (11 each) almost as often as doers of harm, and the eagle is the commonest dupe. Power does not protect in a fable.
The wolf is the second commonest hero but rarely does harm: the fable follows the villain whose schemes go wrong.

## 6. What the X entries may hold (a cursory look, held-out fables only)

About a third of the held-out events are X for both transcribers and matter. Two kinds stand out: **a spoken verdict or lesson**, a character rebuking, retorting or stating the moral, which no function of Propp's covers; and **harm from one's own act with no villain**, close to Dundes's consequence. An impression only; the X study's own discovery material is unread, and its method must be frozen first (the queue, item 3 (b2)).

## 7. The instrument: known weak points

- The definitions card couples most block halves (section 2).
- Both transcribers write θ for a victim who refuses a trick, against the card, which defines θ only as yielding (the trick audit); for later corpora the card should say plainly that a refusal is not θ.
- The mixed-event wording was read two ways; scores are unaffected, the X study counts events, not X entries.
- The hero rule picks close heroes by one or two events (four tragedies: P08, P10, P14, P17); a margin within which both are named would suit plays that follow two characters.
- The request rule overlaps γ and B; "later" in the relevance rule is read as later in telling or in story; functions defined for the hero are given to others; a deception whose dupe is not its victim has no clean notation.
- Every transcriber is a Claude model that knows Propp; the audits found the entries faithful (91 to 99%), but not whether a label leaned on its neighbours. The memory probe found that neither model recalls Propp's Appendix III schemes (Opus one, at low confidence; Sonnet none).
- ESTABLISHED, THE CALIBRATION (`Calibration/KeeperLog.md`, `CompareRun.txt`): on the 45 tales Propp analyzed, the instrument is PARTLY CALIBRATED in both arms and for both transcribers. It reads the tale in front of it (content 0.58 to 0.59 against Propp, 0.40 to 0.42 for another tale's scheme, 0 of 1000 derangements at or above), but agrees with Propp less than its two transcribers agree with each other: content at 0.77 to 0.79 of their agreement, just short of the frozen 0.80, and order at 0.58 to 0.63. It cuts more moves than Propp (129 to 152 against 84), and v46 accepts only 22% to 29% of them. The corrected card (arm C) changes nothing measurable. So the stick measures composition relative to itself well, and Propp's absolute levels poorly. A Propp view of the transcriptions (each function once per move, an implicit C), chosen on half the tales and tested on the other half, was NOT ADOPTED: it raises content by about 0.05 on unseen tales and order hardly at all, so most of the disagreement with Propp is substantive, not repetition.

## 8. What would strengthen or overturn these findings

In order of value:
1. A scored model of block order, frozen, tested on the undrawn fables.
2. DONE 2026-10-06: the block analysis of the sealed tragedies, and the tragedy block grammar (sections 2 and 3). Still open: the positional null and transcriber agreement on the held-out plays; a block-order model for the fables, tested on the undrawn ones.
3. DONE: the owner's audit of twenty `DeceptionTrap` instances, 13 supported, doubtful (section 2).
4. DONE 2026-10-05: the Afanasyev calibration, PARTLY CALIBRATED (section 7); it removes acceptance and coverage against Propp's levels as genre evidence (section 1). Next: genre comparisons instrument to instrument, with the 45 transcribed tales as the Russian reference; then his excluded animal tales, and Dundes's North American material.
   Plan for the texts (2026-09-30): the authoritative three-volume Afanasyev (Nauka, 1984-85) is digitized on FEB-web, in Russian only. Prefer listers and transcribers reading the Russian directly, rules and card in English, over machine translation, which would add a layer between text and function; choose between the two by a small frozen pilot scored against Propp's Appendix III. CORRECTED 2026-10-04: no concordance is needed. The first project's 45 tales are numbered 93 to 167, the collection's modern numbers (No. 113 is "Гуси-лебеди", Propp's Ch. IX example); "50-151" and "1-49" were the older numbering and are withdrawn. Russian Wikisource holds the tales one by one, public domain. Take only the tale texts (public domain), not the edition's commentary; each download needs the owner's go-ahead. The card should first say plainly that a refusal is not θ.
5. A corpus outside the Indo-European family, to tell an Indo-European pattern from a general one.
6. A block-frequency table across genres (suggested 2026-09-30): for each block and genre, the count, the rate per story and per 100 functions, the count expected under shuffling, their ratio, the information (minus the log of the block's rate), and the transcribers' agreement on it. Rare blocks carry more information and may mark a genre, common ones are the shared vocabulary; a rare block counts as a genre's mark only where the transcribers agree on it.
7. The character spheres, counted properly, including how often one species fills both villain's and hero's functions: the trickster reading's test.

## 9. Prior work to read before any write-up

From memory, each to be checked before it is cited:
- Propp, "Oedipus in the Light of Folklore" (1944), and *Historical Roots of the Wondertale* (1946): tale and myth share composition and differ in social function; Propp's 1966 reply to Lévi-Strauss's review "Structure and Form" (1960).
- Lévi-Strauss, "The Structural Study of Myth" (1955): the binary reading of Oedipus that our results, being about sequence and adjacency, do not support.
- Meletinsky, *The Poetics of Myth* (1976): myth centred on origins, the tale emerging as myth loses its sacred standing; a testable form is that in myth a liquidation is more often followed by a lasting change to the world.
- Dundes, *The Morphology of North American Indian Folktales* (1964): interdiction, violation, consequence, attempted escape.
- CHECKED 2026-10-05, the validation of Propp's own analyses, closest prior work to the calibration:
  - Bod, Fisseni, Kurji and Löwe, "Objectivity and reproducibility of Proppian annotations", CMN 2012: nine and then six students annotated three or four tales (among them 145, the Seven Semyons, and 151, Shabarsha) in English translation, compared with Propp's strings by inspection; dramatis personae and some functions were hard to reproduce. Fisseni, Kurji and Löwe, "Annotating with Propp's Morphology of the Folktale: reproducibility and trainability", *Literary and Linguistic Computing* 29.4 (2014), 488-510: reliable for simple tales with sufficient training.
  - Finlayson, "ProppLearner", *Digital Scholarship in the Humanities* (2015/2017): fifteen single-move tales in English translation, double-annotated by trained annotators who were given Propp's Appendix III and placed his functions in the text, so not blind to him; agreement between the annotators strict F1 0.22, lenient 0.71. Names the same four problems found here: unclear placement, implicit functions (his example is C), inconsistently marked trebling, and schemes that disagree with the tale. Finlayson, "Inferring Propp's Functions from Semantically Annotated Text", *Journal of American Folklore* 129 (2016): learns the functions from that annotation.
  - Gervás and Méndez, "Tagging Narrative with Propp's Character Functions Using Large Language Models", Text2Story 2024 (CEUR 3671): ChatGPT and Gemini on English synopses of eleven tales (93, 104, 123, 127, 131, 133, 139, 155, 198, 244, 247), against Propp's assignment: precision 0.37 to 0.46, recall 0.22 to 0.34; reported as negative results.
  What the calibration adds: all 45 Appendix III tales, read in the original language, blind to Propp's schemes (with a memory probe to check), two transcribers as a yardstick, a chance baseline, and a frozen protocol. It is the largest blind test against Propp's own analysis we have found, not the first comparison with it.
- Malec, PftML (about 2001), an XML markup of Propp's functions; Peinado, Gervás and colleagues, ProtoPropp (mid-2000s), an ontology of the functions for story generation; Gervás on Propp's morphology as a grammar for generation. Prior art for grouping functions into classes and relaxing their order; the difference here is empirical testing on blind transcriptions against a shuffle baseline and held-out data.

## 10. Positioning, for any write-up

The French structuralists made structure a philosophy: Lévi-Strauss read it as the mind's universal binary operations, Greimas and Barthes sought a general theory of meaning reached by deduction, and claims at that level resist falsification. This work uses structure as a system of measurement, closer to Propp's own "morphology", taken from Goethe's botany and built up from the material: predictions frozen before the data, shuffle baselines, held-out samples and agreement between transcribers, so that every claim can fail, and several have.
Measurement does not remove the theory; it moves it into the instruments. The definitions card is theory, and the definition check showed it can manufacture a finding (`Blocks/DefinitionCheck.md`). The difference claimed here is that the theory is placed where it can be tested, and the instrument is checked for making its own results.
