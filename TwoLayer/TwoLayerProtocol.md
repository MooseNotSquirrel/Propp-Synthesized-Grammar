# A catalog of acts and relations: the test

**Frozen 2026-10-12 at the owner's word, before any transcription under it.** A departure is logged in `TwoLayer/KeeperLog.md`, not made here.

## The question

Propp's functions bind an act to a role and a place: trickery is the villain deceiving a victim before the harm.
The X study found that most recurring acts in the events his functions leave empty are the same acts with other roles or places, and that, given a role-free name for an act, transcribers often prefer it to Propp's function.
This test asks whether a two-layer reading describes stories better than Propp's functions alone: an **act layer**, what is done, whoever does it; and a **relation layer**, who does it to whom and how they stand to each other, with no hero named.
Propp's functions can be recovered from the two layers, by bringing in the hero afterward and applying a fixed mapping.

## The instrument

**The acts and relations:** `Acts.md`, thirty-six acts and `other`, ten relations.
**The transcription:** for each listed event, one entry per act: the act, the one who does it, the one it is done to (or `-`), their relation, whether it matters to the course of the story (Y or N), and a note quoting the text. No hero is named and no Propp function is written.
**The transcribers:** fresh instances, A on Opus and B on Sonnet, blind to each other, under `ActsRules.md`, which keeps the genres' own rules for reading events and drops Propp's functions.

## The material

Held-out stories that the original transcriptions already read under Propp's functions, so the two readings can be compared event by event:
the 23 Russian test tales of `Calibration/Split.txt` (originals: arm U), the 49 fables of the first two held-out batches (originals: Propp-Fables), and the 8 tragedies P17-P24 (originals: Propp-Tragedy).
The transcribers work in a separate repository holding only these stories, their event lists, the rules and the prompts.

## The mapping to Propp's functions

`twoLayer.py` turns each entry into a function, or into none, from its act and whether the hero (the event lists' hero, matched by the first word of the name, articles and punctuation left out) does it, undergoes it, or neither, following the definitions card:
leave by another than the hero is β, by the hero ↑; forbid γ; disobey δ; seek-information ε; reveal-information to another than the hero ζ, to the hero B; deceive by another than the hero η; be-taken-in θ; harm by another than the hero A; want a; plead or send to the hero B; decide by the hero C; test of the hero D; respond by the hero E; give to the hero, or receive by the hero, F; guide of the hero G; fight with the hero H; win by the hero I; lose by the hero I-; mark of the hero J; repair K; return by the hero ↓; pursue of the hero Pr; escape by the hero Rs; arrive-unknown by the hero o; claim-falsely L; set-task to the hero M; do-task by the hero N; recognize of the hero Q; expose of another than the hero Ex; transform of the hero T; punish of another than the hero U; marry with the hero W.
Every other combination maps to no function.

## The measures

Per event, all hero versions together; an act or function counts for an event if any of its entries there carries it.
1. **Coverage:** for each transcriber, the share of events given at least one act other than `other`, against the share given at least one of Propp's functions in that transcriber's original transcription of the same events.
2. **Agreement on acts:** between A and B, the events where both write an act over the events where either does, summed over acts; against the same figure for Propp's functions in the original transcriptions of the same events.
3. **Recovering Propp:** for each transcriber, the same agreement figure between the functions the mapping derives from the new transcription and the functions written in that transcriber's original transcription; averaged over A and B.

## The verdict

**THE TWO-LAYER CATALOG IS ADOPTED** as the instrument for later work if:
1. coverage is at least 10 points higher for both transcribers;
2. agreement on acts is at least the agreement on Propp's functions; and
3. the recovered functions agree with the originals at least as well as the original A and B agree with each other.

**IT IS NOT ADOPTED** otherwise; each failing test is named.

**Reported, not judged:** agreement on relations, where both transcribers give the same act to an event; the acts the hero performs that Propp reserves for others, deceiving and harming above all, per genre (the trickster); the share of each act per genre.
