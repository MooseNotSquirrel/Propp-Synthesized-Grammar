# ApollodorusResult

**The Apollodorus test ran as frozen, and the claim does not hold.**
The claim was that Propp's morphology describes Greek myth as well as it describes the Russian wondertale; it is speculation, not Propp's, who claimed his morphology for the wondertale only.
It fails every measure fixed in `ApollodorusPrediction.txt`, for both transcribers, for the grammar as shipped and with its extensions, and whether doubtful entries are kept or dropped.
The run's full output is `Apollodorus/ApollodorusRun.txt`, and the protocol is `ApollodorusProtocol.md`.

## The verdict

**Neither transcription reaches any threshold.**
The figures below are the primary reading, with the entries a transcriber marked doubtful kept.

| Transcriber | Grammar | Coverage (80%) | Acceptance (85.2%) | Moves | Verdict |
|---|---|---|---|---|---|
| A | as shipped | 57.0% | 52.6% | 387 | does not hold |
| A | with extensions | 57.0% | 50.7% | 387 | does not hold |
| B | as shipped | 69.9% | 29.4% | 339 | does not hold |
| B | with extensions | 69.9% | 28.2% | 339 | does not hold |

Coverage is the share of census events given at least one of Propp's functions; the rest were written X.
Acceptance is the share of moves `ProppEBNF46.txt` accepts at `move`, against 95.2% of the Russian moves.

**The grammar barely tells the Greek moves from shuffled ones.**
In each length band, real acceptance minus the acceptance of the same moves shuffled with the opener kept first:

| Band | A: moves | A: real | A: shuffled | A: gap | B: moves | B: real | B: shuffled | B: gap | Russian gap |
|---|---|---|---|---|---|---|---|---|---|
| 1-4 | 258 | 73.8% | 68.8% | 5.0 | 182 | 48.0% | 44.4% | 3.6 | 85.7 |
| 5-6 | 68 | 17.0% | 4.4% | 12.6 | 64 | 17.5% | 2.9% | 14.5 | 97.9 |
| 7-9 | 39 | 5.1% | 0.6% | 4.5 | 58 | 3.4% | 0.4% | 3.1 | 97.5 |
| 10+ | 19 | 5.3% | 5.3% | 0.0 | 34 | 0.0% | 0.0% | 0.0 | 82.4 |

Two thirds of transcriber A's moves hold four functions or fewer, and at that length a shuffled move passes nearly as often as the real one.
Longer Greek moves are almost all refused, real or shuffled.

## Where the Greek moves fail

**Four patterns account for most refusals.**
- Trickery and complicity (η, θ) and interdiction (γ) stand inside moves, after the villainy or lack. v46 admits the preparatory functions only before the first move, as Propp's Russian material has them. In Perseus, Polydectes's trickery follows the lack; transcriber A's move is refused at the η.
- Moves open on something other than a villainy, lack or mediation: a departure, a struggle, a victory, a task. The census cut episodes by central figure, not by tale, so an episode need not begin where a Proppian move begins.
- Two villainies stand side by side in one move. Transcriber B often kept a run of harms in one move, where the rule opens a new move at each; the grammar refuses the second A.
- The donor sequence follows guidance, as when Perseus is led to the Graeae before he meets them as donors; v46 requires the donor first.

**The extensions change almost nothing.**
With the tragic fall and the fall after success switched on, acceptance drops slightly, from 52.6% to 50.7% for A and from 29.4% to 28.2% for B.
As shipped, a lost fight, I with a minus, reads as I, as the Russian derivation reads it; with the extensions, it reads as a defeat, which the grammar accepts only when exposure and punishment follow.

## How far the two transcriptions agree

**They agree on what an act is more than on how the moves are cut.**

| Measure | Result |
|---|---|
| Events given the same symbols by both | 1,510 of 2,506 (60.3%) |
| Events both gave a function, sharing a symbol | 986 of 1,301 (75.8%) |
| Distinct move strings, A and B | 378 and 338, of which 19 are identical |
| Episode versions identical throughout | 3 of 176 |

`Apollodorus/agreeApollodorus.py` computes this; it was written after the run, since the scoring program left the agreement uncomputed, and it touches no verdict.

## What the result shows, and what it does not

**The failure does not depend on which transcriber is right.**
The two differ widely, in how many acts they wrote X, in where their moves begin, and in how often they marked an entry doubtful (53% for A, 18% for B), yet every measure fails for both.

**It tests a handbook's summaries against a grammar built on Russian wondertales.**
Apollodorus compresses: most myths get a few sentences, and many episodes are chronicle rather than tale.
Propp's Russian schemes begin at the villainy, while these episodes begin wherever their central figure first acts.
Both are part of what the test found: Apollodorus does not tell his myths as Proppian moves.
Neither says how Greek myth told at length, in tragedy or epic, would fare; the queued test on the tragedies asks that.

**It rests on transcription by language models.**
Two fresh instances on different models transcribed without access to the grammar, but their blindness rested on instruction, and each departed from the rules in ways `Apollodorus/KeeperLog.md` records, none corrected.
Transcriber A reordered acts within a clause toward a tidier sequence in a few places, which could only have raised its acceptance.
The audit of fifty entries from each transcription, for fidelity to the text, has not yet been done.

**It is consistent with Propp's own scope.**
Propp built his morphology on one hundred Russian wondertales and claimed it for that genre.
This test finds that a Greek mythographer's handbook, read under frozen rules, does not follow that morphology's order.

## Exploratory measures, made after the test

**Everything in this section was measured after the verdict and revises nothing.**
`Apollodorus/driftApollodorus.py` computes it, and its output is `Apollodorus/ApollodorusDrift.txt`; the Greek moves are the primary derivation, the grammar as shipped.

**The vocabulary is shared; the proportions differ.**
The Jensen-Shannon divergence between the Russian and Greek shares of each function is 0.12 bits for either transcriber, against 0.03 between the two transcribers.
Greek moves carry more villainy (about 20% of entries against 8%), victory (10% to 11% against 5%) and punishment (4% against 2.4%), and less of the decision to act (1.5% to 3% against 9%), the donor's test and the hero's reaction (about 2% each against 4.5% to 5%), and the return (1.4% to 2.6% against 6.3%).
The preparatory functions stand at 0% in the Russian moves only because Propp's move schemes omit them.

**The order differs far more than the vocabulary.**
Against Propp's numbering of the functions, 1.5% of ordered pairs in a Russian move run backward, against 32% to 33% in a Greek move and 40% to 43% in a shuffled one.

**The edits that would pass the Greek moves would pass shuffled ones too.**
Deleting at most one entry lets v46 accept 72.5% of transcriber A's moves, against 66.6% of the same moves shuffled; deleting at most two, 84.4% against 80.3%.
The entries deleted most are the preparatory functions inside moves for transcriber A (trickery alone 16%) and a second villainy inside a move for transcriber B (25%).

**The task pair holds across both.**
A difficult task is followed by its solution in the same move in 77% of transcriber A's cases and 82% of B's, against all 10 in the Russian moves.

**Ulysses ends as a Proppian tale, and then goes on.**
Both transcribers, working apart, wrote the suitors' villainy, the unrecognized arrival (o), a recognition, the task of the bow (M, N), the suitors' punishment (U), the liquidation (K) and the wedding (W).
Apollodorus then tells a further war, a departure, Ulysses's death at Telegonus's hand and Telegonus's marriage to Penelope.
