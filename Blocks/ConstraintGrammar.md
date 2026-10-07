# One soft grammar for every genre: Propp's rules as weighted constraints

**Frozen 2026-10-06, before any weight was fitted.** A departure is logged in `Calibration/KeeperLog.md`, not made here.

## The question

The tests so far found that Propp's pairs and groups hold together in every genre while their order is a tendency, close to Propp's in the wondertale and the fable and different in tragedy.
This test asks whether one kind of model, the same for every genre, can describe that: Propp's rules of order written as soft constraints, each with a weight learned from a genre's own stories.
If it works, the weights are the genre's grammar, and comparing them shows how the genres differ.

## The model, in plain terms

**Each of Propp's rules of order becomes a constraint a story may break, at a cost.**
"The complication comes before the struggle" is one constraint; "a test's two halves stand together" is another.
The model learns, for each genre, how much breaking each constraint makes a story look like a scrambled version of itself.
A large weight means the genre keeps that rule; a weight near zero means the genre does not care; a negative weight means the genre prefers to break it.
A story's score is the total cost of the constraints it breaks; a reordering of the same story's functions that breaks more, or costlier, constraints scores worse.

**The constraints** (`constraintGrammar.py`):
- **Order of sections.** Propp's sections, in his order: 0 the preparatory section (β γ δ ε ζ η θ λ), then the nine of `Calibration/sectionGrammar.py` (complication, donor, transfer, struggle, liquidation, return, arrival and claims, task, endgame). For each pair of sections i before j, one constraint: j should not come before i. Forty-five constraints.
- **Order inside Propp's pairs.** For γ–δ, ε–ζ, η–θ, D–E, E–F, H–I, Pr–Rs, M–N and o–L: the second half should not come before the first. Nine constraints.
- **Cohesion of Propp's pairs.** For the same nine: when the first half comes before the second, they should stand side by side. Nine constraints.
Each count is divided by the number of pairs of functions in the story, so that long and short stories weigh alike.

**Fitting.** For each training story, 200 random reorderings of its own functions (seed 46); the weights are those of a logistic model that tells the real order from its reorderings, with an L2 penalty of 1.0.
Content is held fixed: only the order is modeled.

## The genres, each split once

| Genre | Fitted on | Tested on |
|---|---|---|
| Russian wondertale | the 22 development tales of `Calibration/Split.txt`, arm U | its 23 test tales, arm U |
| Fable | the 100 drawn Aesop fables | the 99 held-out fables |
| Tragedy | P01-P04 | P05-P32 |

Both transcribers' stories are pooled for fitting and kept apart for testing. A story is a whole tale, fable or play version (a play with k heroes weighs 1/k per version), its functions marked Y in the order of the notes, X left out; stories of fewer than three functions are left out.

## The measure

**For each held-out story: the share of 1000 random reorderings of its functions (seed 46) that the model scores worse than the real order, ties counting half.**
This is the model's judgment of how grammatical the real story is, against what else could be made of its parts: 50% is chance, 100% means every reordering looks worse.
The same measure is computed for **Propp's plain order**, whose score is the number of function pairs out of Propp's numbering; it has nothing fitted.

## The verdict

**THE CONSTRAINT MODEL SERVES EVERY GENRE** if, for each genre and each transcriber:
1. its mean share on the held-out stories exceeds 50%, by a sign-flip test over stories on (share − 0.5), 10,000 flips, seed 46, p at most 0.05; and
2. it is not more than 2 points below Propp's plain order on the same stories.

**IT DOES NOT** otherwise; each failing cell is named.

**Reported, not judged:** each genre's constraint weights, largest first, in plain words; each genre's model tested on the other genres' held-out stories, a 3-by-3 table; the owner's five tales under the Russian model.

## Known before freezing

The tragedy order model and the genre order test (`Blocks/GenreOrder.md`) used the same held-out sets and found Propp's order strong in the Russian tales and the fables and weaker than tragedy's own in tragedy. The section-order exploration and test used the Russian split. No constraint weight has been fitted.
