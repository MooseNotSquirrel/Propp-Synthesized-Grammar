# The X study: functions Propp's list may lack

**Frozen 2026-10-06, before any X event was read or labeled.** A departure is logged in `XStudy/KeeperLog.md`, not made here.

## The question

An X entry is an event in which a transcriber found none of Propp's functions.
In the three genres transcribed, about 1,280 events were left X by both transcribers and judged by both to matter to the course of the story.
This study asks whether some of them share a kind of act that recurs across genres, which would be a function Propp's list lacks, and then tests each candidate on stories the discovery never saw.

## The material

**The unit is the event, not the X entry.**
An event counts when, in the original transcriptions, both transcribers wrote only X for it and both marked it as mattering (Y).
Counting events where both agree keeps out a function one transcriber simply missed, and counting events rather than entries keeps out the two ways the rules on mixed events were read.

**Each genre is split once, before anything is read.**

| Genre | Discovery | Test |
|---|---|---|
| Russian wondertale | the 22 development tales of `Calibration/Split.txt`, arm U | its 23 test tales, arm U |
| Fable | the 100 drawn Aesop fables (Propp-Aesop) | the 99 held-out fables (Propp-Fables) |
| Tragedy | P01-P16 | P17-P32 |

`xTargets.py` selects the events and writes the labelers' material into the transcriber-side repository `Story Language/XStudy`.
Nothing there names Propp, functions, transcriptions or the reason the events were chosen.

## Stage 1: labeling

**Two fresh labelers, transcriber A on Opus and B on Sonnet, blind to each other, describe the act in each marked event.**
Each sees every event of the story, for context, with the target events marked, and writes for each target one short phrase: what is done, and what it does to the course of the story, in the present tense, naming no character and no role (no "the hero", "the villain").
Four batches: the discovery tales, the discovery fables, tragedy P01-P08, tragedy P09-P16.

## Stage 2: grouping

**One fresh grouper on Opus receives all the labels, from both labelers, with no story, genre or event text, and proposes the kinds of act they describe.**
Each kind gets a short name, a one-sentence definition of the act and its effect on the story, and two example labels; at most thirty kinds.

## Stage 3: assignment

**Two fresh assigners, on Opus and on Sonnet, blind to each other, assign each target event to one kind, or to none.**
Each sees the kinds, the event, its two labels and the story's events for context.

## Stage 4: candidates, counted by the keeper

**A kind becomes a candidate function if:**
1. both assigners put at least 10 events in it, counting only events where they agree;
2. those events come from at least two genres, with at least 3 in each; and
3. in at least half of them, at least one original transcription linked the event to another, which shows that the act had a consequence in the story.

Each candidate is written on the definitions card's model, from the grouper's definition, and frozen before stage 5.

## Stage 5: the test, on the held-out stories

**Fresh transcribers, A on Opus and B on Sonnet, re-transcribe the test stories of each genre under the same rules, with the candidates added to the card.**
A candidate holds if:
1. **the transcribers agree on it as well as they agree on Propp's functions:** its agreement, the events where both write it divided by the events where either writes it, is at least the same figure for Propp's functions in the same stories, pooled;
2. **it takes up X events, not Propp's:** at least 75% of the events where either transcriber writes it were left X by both in the original transcription; and
3. **it is used in at least two genres** in the new transcriptions.

Each candidate is judged on its own. Stage 5 is a cost in cloud runs, sized when the candidates exist; the owner decides when it runs.

## Known before freezing

A cursory look at the held-out fables, before this protocol, suggested two kinds: a spoken verdict or moral, and harm from one's own act with no villain. The held-out fables are test material here, and that impression is not used.
