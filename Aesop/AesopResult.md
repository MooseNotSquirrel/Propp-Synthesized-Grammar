# AesopResult

**The Aesop test ran as frozen, and the claim does not hold.**
The claim, speculation and not Propp's, was that short tales are samples of Propp's production rules: a few of his functions at a time, in his order.
For both transcribers, the fables fall short on coverage, fail on order, and hold only one of Propp's pairs.
The full output is `AesopRun.txt`; the protocol is `AesopProtocol.md` and the thresholds `AesopPrediction.txt`.

## The verdict

**Both transcribers miss all three measures on the primary reading, the functions marked as mattering.**

| Measure | Threshold | Transcriber A | Transcriber B |
|---|---|---|---|
| Coverage | at least 60% | 57.0% | 56.1% |
| Order: pairs of functions running backward | at most 15%, and 20 points below shuffled | 31.9% (shuffled 50.1%) | 30.1% (shuffled 50.0%) |
| Pairs with at least 10 cases beating shuffled by 20 points | every one | trickery-complicity yes; villainy or lack-liquidation and departure-return no | trickery-complicity yes; villainy or lack-liquidation no |

The sample is 99 fables, transcribed as 118 versions where a fable names two heroes.
The reading with all functions, and the reading without doubtful entries, fail in the same way.

## The keeper's guesses, frozen with the thresholds

**Two guesses held and three failed.**
- Coverage would fall short of 60%: it did, at 56% to 57%, higher than the guessed 50%.
- Order would be met, at about 10% backward: it was not; about 30% of pairs run backward.
- Trickery-complicity would hold: it did. Struggle-victory would also reach ten cases and hold: it reached only 5 to 7 cases.
- The share of entries marked incidental would be under 15%: it was 0.3% and 1.7%.
- The claim would fail on coverage alone: it failed on all three.

## What the fables show

**Fables are tight: almost nothing in them is incidental.**
Only 1 of transcriber A's 368 function entries, and 6 of B's 361, were marked as not mattering to the course of the fable, against the Apollodorus audit's finding that most of the handbook's entries mattered little to any tale.

**Trickery followed by complicity is the one Propp pair that holds.**
Trickery is followed by the victim's complicity in 71% of A's cases and 65% of B's, against 47% and 44% shuffled.

**Most harms and wants are never set right.**
A villainy or lack is followed by its liquidation in only 27% and 24% of cases, against 16% and 15% shuffled, and only a fifth of the fables hold a harm or want that is later set right.
A departure is almost never followed by a return.

**Order runs backward against Propp's numbering in about a third of pairs.**
Propp numbers trickery and complicity before villainy, as preparation for it; in the fables a want often comes first and the trick follows it, so the pair counts as backward.

**The grammar still cannot judge moves this short.**
Most moves hold four functions or fewer, and at that length v46 accepts the shuffled moves about as often as the real ones, 62% against 63% for A and 59% against 61% for B.

## Agreement

**The two transcribers agree far more than on Apollodorus.**
They gave the same symbols to 74.5% of events (Apollodorus: 60.3%), shared a function on 90.1% of the events both gave one (75.8%), and gave the same relevance mark to 97.3%.
The definitions card and the tale-sized unit appear to have made the notation easier to apply the same way.

## What the result does and does not show

**The failure rests on transcription by language models, as before.**
The transcribers worked blind to the grammar, which was not in the repository they were given, and blind to each other by instruction.
Their reports show judgment calls at gaps in the rules, logged in `KeeperLog.md` and none corrected; the most consequential is a different reading of when a harm after a want opens a new move, which changes move counts but none of the decisive measures.
The audit, of fidelity and of relevance, has not been done.

**It tests fables against Propp's order, not against a fable's own.**
The measures ask whether fables sample Propp's sequence; they do not ask what sequence fables follow instead.

## Exploratory: the order the fables follow

**Everything in this section was measured after the verdict and revises nothing.**
`fableShapes.py` computes it on the primary reading, and its output is `FableShapes.txt`.

**The fables keep a stable order of their own, only loosely Propp's.**
Placing each function by its mean position within its fable, the two transcribers agree on the outline: a want or a departure early (a at 0.20 to 0.24); trickery, mediation and villainy in the middle (0.41 to 0.52); complicity, help received and the hero's reaction after them (0.58 to 0.73); victory and liquidation late (0.74 to 0.81); punishment and exposure last (0.83 to 0.99).
The rank correlation of this order with Propp's numbering is 0.26 for transcriber A and 0.47 for B: positive, and weak.

**A fable opens on a want and often closes on a harm.**
A want opens 36% and 43% of the fables and a villainy 22% and 23%; a villainy closes 26% of them, a liquidation 13% and 16%, an exposure 13% and 8%.

**Propp's local pairs are the transitions most above chance.**
Test to reaction (37 times chance, transcriber A), false claim to exposure (26 times), trickery to complicity (19 and 17 times), then want to help received (5 times), want to decision to act (7 times, B), want to liquidation (2 to 3 times) and complicity to villainy (2 to 3 times).

**A speculative reading, not from Propp: many fables are the villain's move, told from the villain's side.**
The recurring shape is a want, a trick, the victim's complicity and a harm: a, η, θ, A.
In Propp's order trickery and complicity stand before the villainy as preparation, and the villain's own want is not told; the fable tells that want first and ends at the harm, so its hero is often the trickster.
Read this way, a fable is Propp's preparatory section with the villainy, told whole, with the moral in place of the rest of the tale.

**The tragedy extensions found nothing to work on.**
The hero loses a fight twice in each transcription, and no move has the hero punished, recognized or exposed after a liquidation or wedding, the fall after success.
A fable's ruin is a harm done to the foolish, not a defeat in combat or a fall from success, so both grammars accept the same moves.
