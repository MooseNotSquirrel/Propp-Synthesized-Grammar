# Preliminary findings

**This file gathers what the genre tests and the building-block work have found so far, what has been withdrawn, and the readings and ideas worth keeping for when all the data is in.**
It is a working document, not a result: every figure below is recorded, with its program and its frozen rule, in the file each entry names, and those files win wherever this one disagrees with them.
Each entry is marked: ESTABLISHED (frozen before the data, or replicated on unseen data, and passing the risk checks), TENTATIVE (measured, not yet replicated or checked), WITHDRAWN, or SPECULATION, NOT FROM PROPP (a reading, labelled as such).
Last brought level: 2026-09-30.

## 1. The genre tests of Propp's whole morphology

**ESTABLISHED: Propp's full grammar does not describe Greek myth summaries or Aesop's fables.**
Apollodorus failed on every measure; Aesop failed on coverage and order (Propp-Apollodorus, Propp-Aesop, each with its result file).
The tragedy test is at 20 of 32 plays; its interim results (P01-P04) fall short and P05 on are sealed (`Tragedy/`).

## 2. Propp's blocks

**ESTABLISHED: the two halves of Propp's pairs and groups are told together, next to each other, more often than chance.**
Found in the training fables and tragedy P01-P04, replicated on the 99 held-out fables, and it passes the risk checks:
- against a positional null that keeps each function's habits of position, it survives in every fable cell and in tragedy's strict reading (`Blocks/PositionNull.txt`);
- the two transcribers find the same blocks in the same story beyond chance in every fable cell (`Blocks/Agreement.txt`);
- it holds whether the incidental and doubtful entries are matched or not, 35 of 36 cells (`Blocks/Robustness.txt`).
`DeceptionTrap`, the trick with the victim's complicity, is the most reliable block: about three times chance in the fables, and 78% to 88% of its instances found by both transcribers.

**TENTATIVE: in tragedy the effect is weaker.** Its loose reading is mostly habit of position (weakened against the positional null), its strict reading survives, and the transcribers' agreement on strict blocks falls just short of the rule on 40 blocks. The sealed plays test it; the prediction is frozen in `Tragedy/BlockPrediction.txt`.

**WITHDRAWN: that the order inside a block is near obligatory, like the fixed order inside a phrase of Latin or Russian.**
The definitions card defines the second half of most blocks by the first ("taken in by the deception", "the prohibition is broken", "the task is accomplished"), so a reversal can occur only in a flashback, and the absence of reversals measures the card, not the stories (`Blocks/DefinitionCheck.md`).
Order inside a block can be tested only on the blocks the card leaves free: `StruggleAndOutcome`, `FraudPosture`, `ReturnJourney`, `Ordeal`, and the free parts of `complication` and `TestedAcquisition`. They are rare so far.

**THE CARD IS KEPT, AND NOTHING IS RE-TRANSCRIBED (decision, 2026-09-30).**
The coupling is Propp's own: he defines complicity as yielding to the deception and violation as breaking the interdiction, so a card that decoupled them would no longer describe his functions, and the Afanasyev calibration needs his definitions. The coupling makes order inside those blocks a matter of logic, not of evidence; it does not touch co-occurrence and adjacency, which the transcribers could have found or not, and it does not touch the order between blocks. Re-transcribing would also break the tragedy test's single instrument. What changes is the claim, not the data.

## 3. The order between blocks

**ESTABLISHED, IN PART: the fable grammar failed its frozen test on coverage, and its order held on unseen fables.**
`FableEBNF01.txt` accepted 55.6% and 61.7% of the held-out fables against a frozen 65%, so the claim that it describes most fables fails. Its gap over shuffled order held (+27.4 and +29.8 against a frozen 20), and beat v46's (+10.6 and +15.1) (`Fables/KeeperLog.md`).
So the order between blocks is not free, as the plan first supposed: it is a strong preference, not a rule. A yes-or-no grammar is the wrong instrument for a preference; a scored model of block order is the right one, and would be tested on the about 110 undrawn fables.

**SPECULATION, NOT FROM PROPP: story languages may be like languages with free word order, such as Latin and Russian, in the order BETWEEN their units: strong default orders, departed from for effect.** The half of the analogy about fixed order inside the unit is withdrawn (section 2).

## 4. The fable as a genre

**ESTABLISHED: the fables' kernel is the villain's want, the trick and complicity, then the harm (`a DeceptionTrap A`).** Found in the training fables and recurring in the held-out ones: the trick block is followed by the harm 10 times in 27 and 8 times in 20.

**TENTATIVE: the trick has two outcomes.** In the held-out fables it is also followed by its defeat, victory I or rescue Rs, 6 times in 20, often with an exposure after. Noticed on the held-out fables, so it needs fresh fables to test.

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
- The mixed-event wording was read two ways; scores are unaffected, the X study counts events, not X entries.
- The hero rule picks close heroes by one or two events (four tragedies: P08, P10, P14, P17); a margin within which both are named would suit plays that follow two characters.
- The request rule overlaps γ and B; "later" in the relevance rule is read as later in telling or in story; functions defined for the hero are given to others; a deception whose dupe is not its victim has no clean notation.
- Every transcriber is a Claude model that knows Propp; the audits found the entries faithful (91 to 99%), but not whether a label leaned on its neighbours.

## 8. What would strengthen or overturn these findings

In order of value:
1. A scored model of block order, frozen, tested on the undrawn fables.
2. The block analysis of the sealed tragedies, as frozen in `Tragedy/BlockPrediction.txt`.
3. An audit by the owner of about twenty `DeceptionTrap` instances against the text.
4. The Afanasyev calibration: can the transcribers reproduce Propp's own schemes on his own tales? Then his excluded animal tales, and Dundes's North American material.
5. A corpus outside the Indo-European family, to tell an Indo-European pattern from a general one.
6. The character spheres, counted properly, including how often one species fills both villain's and hero's functions: the trickster reading's test.
