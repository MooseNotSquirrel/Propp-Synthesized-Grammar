# A significance layer: the test

**Frozen 2026-10-13 at the owner's word, before any description under it.** A departure after the freeze is logged in `Significance/KeeperLog.md`, not made here.

## The question

The two-layer test (`TwoLayer/TwoLayerProtocol.md`) found that a catalog of role-free acts and plain relations describes more of each story than Propp's functions do, and is more reliably agreed on, but that acts and the hero's part in them recover Propp's functions only about half as well as two transcribers agree on them (0.25 against 0.50, with the heroes two readers agree on).
The keeper's reading was that a function is an act with its significance for the course of the action, which is Propp's own definition (p.21), and that the act layer lacks the significance.
This test adds a third layer, recorded for each act already transcribed, and asks whether the three layers recover Propp's functions as well as two transcribers agree on them.

## Checked before the design, on data already scored

**The information is not already in the two layers.** `Significance/baseline.py` (output `BaselineExplore.txt`, exploratory) learns a mapping from the layers already transcribed to the original functions, two folds by story: the act alone, the act with the hero's part, with the relation, with the act's position against the story's first harm or want. Every variant stays between 0.22 and 0.26, against 0.50 for the transcribers; a mapping learned from the data does no better than the hand mapping.
**Where the transcribers' agreement comes from:** they agree 0.72 on which events carry a function at all, and 0.64 on the functions where both give one; so a recovery has to judge which acts matter as well as which function they fulfill.
**A pass is possible:** if each act's three new fields were filled in as well as they could be for the original transcription, the mapping below would recover the originals at 0.751 (A) and 0.690 (B), above 0.50. The test does not fail by construction.

## The layer

For each act already transcribed in the two-layer test, a describer who did not write it records, under `Significance.md` (copied to the describers as `sig/SigRules.md`):
1. **the hero's part:** does, undergoes, both, neither (the hero named for the describer; this replaces the name matching that failed in the two-layer test);
2. **its value for the hero:** helps, harms, neither, judged by what the act leads to;
3. **its place in a problem:** opens, worsens, serves, repairs, rewards, punishes, none; and **which problem**, labeled p1, p2 in the order they open, each named in a line once;
4. **a typed link:** answers, enables or none, with the act it links to.

## The material

The stories of the two-layer test that have a judged hero (`Heroes/`, the readers' answers matching on a shared name word): 22 of the 23 Russian test tales, 45 of the 49 fables, and the 8 tragedies P17-P24, 75 stories.
Each describer describes the acts of the same transcriber letter: describer A (Opus) the acts of act describer A, describer B (Sonnet) those of B, so that each new layer sits on one act layer.
Nine batches per describer: the tales in four (s1 to s4), the fables in one (s5), the plays two at a time as before (s6 to s9); the input files number every act e0001 onward.
The describers read each story's text, in the original language for the tales, and nothing else in the repository but their input file and the rules; they are told no system of analysis, and Propp is not named to them.
Two stages, `sig-1` (s1 to s5, ten describers) and `sig-2` (s6 to s9, eight), each in a fresh cloud session, as `RUN.md` in `Story Language/ActsRoles` describes.

## The mapping to Propp's functions

`significance.py derive3` turns each described act into a set of functions, following the definitions card the original transcribers used; an act is "after" when its problem has already opened at an earlier act.
**An act with no place in a problem maps to nothing.**
**The significance rules, for any act:** one that opens a problem is lack a if it is a want or does not harm the hero, and villainy A if it harms the hero and the hero does not do it; a harm, deception or other act that worsens a problem, harming the hero, done by another than the hero, is A; a repair, receipt, gift, escape or other act that repairs a problem is liquidation K; one that punishes, where the hero is not punished, is U; one that rewards the hero is W.
**The act rules:** leave by the hero ↑, by another, harming the hero, β; return by the hero ↓; forbid or send to the hero after the problem opened B, forbid otherwise γ, send to the hero before it opened γ; disobey δ; seek-information harming the hero ε; reveal-information harming the hero ζ, to the hero after the problem opened B; deceive by the hero that repairs I, deceive that harms the hero or by another that serves, opens or worsens η; be-taken-in that serves, opens or worsens θ; harm that repairs, not done to the hero, I; want that opens or worsens a; plead to the hero after the problem opened, not helping, B, otherwise D; plead by the hero that opens a; decide by the hero after the problem opened C; test of the hero D; respond by the hero E, to the hero helping F; give to the hero helping F (not as a reward); receive by the hero helping F (not as a reward or a repair); guide of the hero G; fight with the hero H; win by the hero I; lose by the hero I−, by another helping the hero I; mark of the hero J; repair K; pursue of the hero Pr; escape of the hero Rs; arrive-unknown by the hero o; claim-falsely L; set-task to the hero M; do-task by the hero N; recognize of the hero Q; expose of another than the hero Ex; transform of the hero T; punish of another, that punishes, U; marry of the hero W.
**The comparison:** the two-layer test's frozen mapping, with the hero's part as these describers give it (`derive2`), so that the two figures differ only by the significance fields.

## The measures

On the events in both original transcriptions and both descriptions, in stories with a judged hero; per event, an act or function counts if any of its entries carries it; agreement is the events where both carry a function over the events where either does, summed over functions.
1. **Recovering Propp:** for each describer, agreement between the functions the significance mapping derives and that letter's original transcription; averaged over A and B.
2. **The two-layer figure:** the same with the two-layer mapping.
3. **The target:** the original A against B.
4. **The share of the gap closed:** (measure 1 − measure 2) / (measure 3 − measure 2).

## The verdict

**THE THREE LAYERS RECOVER PROPP'S FUNCTIONS** if measure 1 is at least measure 3.
**THE SIGNIFICANCE LAYER CLOSES MOST OF THE GAP, BUT DOES NOT RECOVER PROPP'S FUNCTIONS** if it is below, and the share of the gap closed is at least one half.
**THE SIGNIFICANCE LAYER DOES NOT RECOVER PROPP'S FUNCTIONS** otherwise.

## The keeper's predictions

Recorded before any description; scored with the verdict.
1. Measure 1 lies between 0.30 and 0.40.
2. The verdict is the third level: the layer closes less than half the gap.
The reason: the describers will often disagree with the original transcribers about which acts matter, and a mapping written from definitions, not learned, will still add functions the originals leave out.

## Reported, not judged

Measures 1 and 2 per genre; a mapping learned from the act and hero's part, and from the act, hero's part, value and place, as `baseline.py` learns it; agreement between the two describers on the hero's part, value and place where both give an event the same act; and, per genre and describer, the problems a story, and the share of problems repaired, punished and rewarded.
