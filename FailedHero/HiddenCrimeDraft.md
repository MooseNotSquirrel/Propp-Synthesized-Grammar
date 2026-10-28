# The hidden crime: a draft amendment to the revealed-villain protocol (DRAFT 2026-10-28, FOR THE OWNER'S REVIEW, NOT ADOPTED)

**Drafted 2026-10-28 at the owner's word.** Nothing is changed: `RevealedVillainProtocol.md`, its scoring and its verdicts of record stand as they are (`RevealedVillainReaders.txt`: prediction 1 FAILS).

## 1. Why a second question

The frozen question asked whether the story reveals that the hero is "himself the cause of the harm the story turns on". Both readers took it to mean *the hero is the cause*, whether or not that is hidden:
- In the tragedies they said yes to causes told openly from the start: P03 *Oedipus at Colonus*, P12 *Orestes*, P21 (Xerxes), P22 (Admetus), P29 (Eteocles).
- In the wondertales they said yes to a hero's carelessness: the zhikhar's shouting, the sister's neglect, Ivan freeing Koshchei.

The owner's pattern is narrower: **a crime of the hero's own, unknown to him or hidden, whose discovery late in the story is the turn**. That is *Oedipus the King*. The first question did not separate it.

**This is a second question prompted by the first one's answers.** Its result is to be reported beside the first, never in place of it, and read with that in mind.

## 2. The question

Two parts, so that the cause and the hiding are answered apart:

> **CAUSE:** Is the hero himself, by a deed of his own, the cause of the harm the story turns on? Answer yes or no.
>
> **HIDDEN:** If so, is that deed unknown to the hero, or hidden from those around him, until a point in the story where it is discovered? Answer yes or no (no if CAUSE is no).
>
> **EVENT:** the number of the event where the hero's part is discovered (0 if HIDDEN is no).
>
> **REASON:** one sentence.

The answer form is `ITEM | CAUSE | HIDDEN | EVENT | REASON`.

**What counts (decision 1):**
- **(a) Recommended:** the story counts when both readers answer CAUSE yes and HIDDEN yes.
- **(b)** As (a), and both readers' EVENT falls in the last third of the story's events, which is the "close" of the owner's words. This is stricter, and closer to "a surprise at the end", but it would drop a discovery made at mid-play.
- Whichever is not chosen is reported beside it.

## 3. The material, the readers and the cost

- **Stories:** the same 56 as `revealed-1`, the tragedies and wondertales with a judged hero, in two batches. `r3` holds the 20 tragedies and `r4` the 36 wondertales, under a new stage `revealed-2`.
- **Readers:** new ones, A on Opus and B on Sonnet, who have not seen the first question or its answers.
- **Cost:** four readers, about 440,000 tokens at `revealed-1`'s rate.

## 4. The controls (decision 3)

Six stories whose answers are plain from the events, fixed now:
- **yes:**
  - P20 *Oedipus the King*: he killed his father and married his mother unknowing, and discovers it;
  - P26 *Heracles*: he kills his children in madness and learns it when he wakes;
  - P13 *Ajax*: he slaughters the herds believing them his enemies, and learns it when his madness lifts.
- **no:**
  - P03 *Oedipus at Colonus*: the cause, his crime, is known from the start;
  - P12 *Orestes*: the matricide is open from the first event;
  - A098 *Daughter and Stepdaughter*: the villain is the stepmother.

P03 and P12 are chosen to test the very distinction the first question missed. The keeper has seen the first stage's answers for them, so their being controls rests on the events, not on those answers. Both readers must answer at least five of the six as fixed in both parts, or the stage is reported and not scored. The controls are left out of the prediction's score, as before.

## 5. The prediction, to be frozen with this amendment

3. **The hidden crime:** counted as in decision 1, the hero's own hidden crime is found in a higher share of tragedies than of wondertales.

It is tested per transcriber, with a permutation test at p at most 0.05 and a floor of 10 stories a side, the controls left out. It HOLDS if for both, SPLIT if for one, FAILS if for neither.

**Reported:** both readers' agreement on each part; the list of stories with the discovering event; set beside the first question's answers, story by story.

## 6. Decisions for the owner

1. **What counts:** (a) CAUSE and HIDDEN (recommended), or (b) with the discovery in the last third.
2. **The wording** of section 2, to be fixed exactly. In particular, whether "or hidden from those around him" stays. It admits a hero who knows his deed but keeps it hidden, which *Oedipus the King* does not need but a Clytaemestra-like hero would.
3. **The controls** of section 4, or others the owner names.
4. **Whether to run it at all,** given its cost and that it was prompted by the first answers.

## 7. If adopted

The amendment is entered in `RevealedVillainProtocol.md` as section 8. Then, in order:
1. `revealedVillain.py` gains `setup-c`, `form-c` and `score-c`, committed before they run.
2. The stage is dry-run, written, and added to `RUN.md` as `revealed-2`.
3. The stage runs at the owner's word.
