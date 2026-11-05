# Can coding apart say no? The tragedies: protocol (DRAFT 2026-11-04, for the owner's review; nothing set up or run)

**Asked by the owner on 2026-11-04,** after `ShuffledReport.md`. The test of events coded apart has so far said yes in two traditions. This asks whether it can say no.

**The contrast.** Whole-play tragedies stand at tau 0.23 and 0.24 with Propp's order, against about 0.7 for the wondertales and East Asian tales. If they stay low when coded apart, the test separates corpora. If they rise to the others' level, the labels bring the order with them whatever the story, and that undercuts `ShuffledReport.md` and `CardPilotReport.md`.

**What it does not change.** No earlier verdict, table or string. It is `ShuffledProtocol.md`'s design and measure on a third corpus, and only what differs is written here.

## 1. What differs

**The events: a sample.** The 32 plays hold 3,262 events, too many for the budget. So 15 events per play, 480 in all, drawn by seed 20261104 and evenly spread through each play, so that the sample keeps each play's beginning, middle and end. This is decision 1. All 32 plays are used, as the corpus's order should not rest on a few.

**Noise, measured on the old strings before this draft** (`tragedyNoise.py`, `TragedyNoise.txt`), with even samples, 500 draws:

| Events | Reader A, 90% range | Reader B, 90% range | Functions measured |
|---|---|---|---|
| 300 | −0.07 to 0.65 | −0.09 to 0.69 | about 10 |
| 400 | −0.03 to 0.57 | 0.00 to 0.61 | about 12 |
| 600 | 0.06 to 0.52 | 0.04 to 0.57 | about 15 |
| All | 0.23 | 0.24 | 23 to 24 |

Sampling lifts the figure a little (about 0.30) and widens it a good deal. **So the comparison is made paired, on the same sampled events** under the whole-play labels and the coded-apart labels.

**The batches:** six of 80 lines, each play's sampled events dealt round them as before, with random identifiers and each line carrying its play's hero.

**The card:** the neutral card and rules of `lines/Rules.md`, unchanged, so that the three corpora are coded alike. The tragedies' own card differs by one sentence in θ's definition. The whole-play labels are the old ones, on that card.

## 2. How it will be read, fixed now

Per reader. D is coded-apart tau minus whole-play tau, on the same sampled events and the functions both have, with a 90% interval by paired bootstrap of plays. Agreement is checked as in `ShuffledProtocol.md`: below 0.25 is too poor to read.

| Reading | Rule |
|---|---|
| **The test says no** | Coded-apart tau is under 0.45, and D is under 0.20 |
| **The labels carry the order** | Coded-apart tau is at least 0.50, and D is at least 0.20 with an interval above 0 |
| **In part** | Anything else; the figures are reported, and neither is claimed |
| **Too poor** | Kappa with the whole-play labels, or A's with B's, is under 0.25 |

**Beside it, not deciding:** the same difference from the wondertales' and East Asian coded-apart figures, by bootstrap of stories; which functions stand where.

**The keeper's expectation, not from Propp, marked as such:** the test says no, in both readers.

## 3. Limits, stated now

- **A "no" would not make the order in the other corpora Propp's.** It would show the labels do not bring that order regardless of story, and that tales differ from plays. Narrative logic of a tale-like kind remains possible.
- **The plays are famous.** The readers may know Orestes' story and so place an event from memory of the play. That could only raise a play's internal consistency, and need not bring it nearer Propp's order.
- **Only 12 to 15 functions will be measured,** so one or two moving can shift the tau. The range above says how much.
- **Tragedy's form differs from a tale's:** events come as speeches and reports, so the same functions may not mean the same act.

## 4. Tests, before any reader runs

As `ShuffledProtocol.md` section 6: every sampled event in exactly one batch; events sharing a batch far apart in their play; nothing pointing to Propp or a play's identifier beyond what a line's own words and hero say; the key returns each line to its place; the reading's four results on planted figures; two runs byte-identical.

## 5. Decisions for the owner

1. **480 events.** Recommended. Near the wondertale part in size, and the same 12 subagents. 400 would save a sixth but widen the range; 600 would narrow it at a quarter more cost.
2. **The reading's numbers (0.45, 0.50, 0.20).** Recommended. They are the keeper's judgment from the table above, set before any new label.
3. **Run it whole, not in parts.** Recommended: there is one corpus.

## 6. Order of work and cost

The owner's decisions and the freeze; `tragedyApartSetup.py` and the measure, committed, tests passed; the stage `lines-tragedy` at the owner's word; the report.

**Cost:** readers: about the size of the wondertale part. **The cost of the earlier parts is not yet settled:** the owner's figure of 26% could be a new level after a reset, or the cost of the East Asian part. If it was the cost, this would likely take about 30 points.
