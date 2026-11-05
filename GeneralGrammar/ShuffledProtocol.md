# Events coded apart from their tales: protocol (FROZEN 2026-11-04 AT THE OWNER'S WORD, THE SIX RECOMMENDED DECISIONS TAKEN; nothing run)

**Asked by the owner on 2026-11-04,** after `CardPilotReport.md`. The tale's order survived a neutral card, but both readers recognized Propp, so a reader who knows his scheme may still write his order in. This test takes away what such a reader would need: where an event falls in its tale.

**What it does not change.** No earlier verdict, table or string. New strings go in their own folder. It stands in place of the pilot's part 2, which is not run (decision 1).

**The caution:** the readers are modern models. The event lines are English paraphrases written by listers who read each tale in order.

## 1. The question, and what it cannot answer

**The question:** with each event coded alone, by a reader who cannot tell its place, and the labels then put back in story order, does his order still appear?

**What a yes would show:** the order comes from what the events are, and not from a reader expecting what comes next.

**What a yes would not show,** stated now:
- **That the order is Propp's in particular.** A return or a wedding comes late in most stories anywhere, and a harm comes before its repair. A yes may reflect narrative logic generally, which is the question of `StructureProtocol.md`'s control E2 and of the other corpora.
- **That the lines hold no clue to place.** "Next morning", "the third flock" and "again" remain. So part of this is measured (section 4).

**What a no would not separate:** a reader's expectation from the real help that context gives. Section 5 reads a no with that limit.

## 2. The design

**The tales:** the 15 wondertales and 15 East Asian tales already drawn (`PilotDraw.txt`): 488 and 376 events. So the wondertales can be set beside part 1.

**The batches.** Per corpus, six batches of about 81 and 63 lines:
- Each tale's events are dealt round the batches in turn, from a seeded start, so that **two events close together in a tale never share a batch,** and any two in a batch stand at least six apart in their tale.
- Each batch is shuffled by a seed.
- Each line carries a random identifier, and no tale identifier, title or event number.
- The key stays in the keeper's repository until the labels are committed.

**The readers:** A on Opus, B on Sonnet, one fresh reader per batch, so no reader sees more than a sixth of a tale. 24 subagents.

**What a reader sees:**
- **The card:** cell S's, neutral and shuffled, as it was approved for part 1.
- **The rules,** cut to what still applies. Each event gets its entries or X, a symbol standing for an act by what it does for the course of the action. Assign it whoever performs it. In doubt, write X. Gone, as they need the whole tale: reading the tale first, marking what matters, and the moves.
- **Each line:** the identifier, the event's paraphrase, and the tale's hero, as functions are defined around a hero (decision 2).
- **An instruction:** code each line by itself, and do not try to work out which lines belong together.
- **At the end, one line each:** whether the card reminded them of a published scheme, and whether they could tell where events fell in their tales.

**The format:** `e0413 | <entries, or X> | ? if unsure | <a note of at most six words>`, so kept short for cost, after the owner's figure for part 1 of the pilot (about 60 points of the budget).

## 3. Why these are the numbers

From existing strings before this draft (`shuffleNoise.py`, `ShuffleNoise.txt`).

**The order measure resists noise.** Mean-position tau with his numbering, no preparatory units, when labels are replaced at random at rate p, the sequence untouched (15 tales, 300 draws):

| | p = 0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| Wondertales, A | 0.76 | 0.67 | 0.54 | 0.39 | 0.21 |
| Wondertales, B | 0.72 | 0.66 | 0.57 | 0.43 | 0.24 |
| East Asian, A | 0.75 | 0.67 | 0.55 | 0.40 | 0.22 |
| East Asian, B | 0.67 | 0.58 | 0.48 | 0.34 | 0.19 |

So **worse coding alone predicts a known fall,** and the test need not mistake one for the other. Shuffling labels within the story gives about 0.

**What agreement to expect.** Two whole-tale codings of the same tales by the same reader agree at kappa 0.59 to 0.79. A and B on the same card, 0.63 to 0.70.

## 4. What is measured

**Primary: the same tau,** on the labels put back in story order, per corpus and reader.

**Beside it, needed for the reading:**
- **Agreement with the whole-tale coding,** the same reader, event by event: part 1's S labels for the wondertales, the old strings for the East Asian tales.
- **The expected tau:** the whole-tale labels replaced at the rate this disagreement implies, 1,000 draws, its 90% range.
- **The null:** labels shuffled within each tale, 1,000 draws.
- **A and B's kappa** on the shuffled coding.

**Beside it, not deciding:**
- **How much place the words give:** relative position predicted from each line's words alone, on held-out tales. No reader is needed. It tells how far the lines themselves carry place.
- **The same tau with preparatory units,** and each preparatory function's mean place. Do they stand early when coded alone, or mid-tale as before? This bears on the finding of the audit and on the owner's point about deception after villainy.
- **Share of events given a symbol,** beside part 1's rise.
- **Which functions move most** between whole-tale and shuffled coding.

## 5. How it will be read, fixed now

Per corpus and reader:

| Reading | Rule |
|---|---|
| **Too poor to read** | Kappa with the whole-tale coding, or A's with B's, is under 0.25 |
| **In the events** | Tau is at least 0.5, above the null's 95th percentile, and not below the expected range |
| **Needs the sequence** | Tau is at least 0.15 below the expected range's 5th percentile |
| **In part** | Anything else; the figures are reported, and neither is claimed |

**What follows** (for the owner to decide then, not bound here):
- **In the events:** memory of the sequence is not what makes the order. The work goes up to pairs with more confidence, with narrative logic in general still to be separated.
- **Needs the sequence:** the order leans on reading in sequence, as context or as expectation. These stay unseparated, and it would be fair to say the strings' order cannot be relied on as a finding about tales without more.
- **Too poor:** the design says nothing; another way would be needed.

## 6. Tests, before any reader runs

- The batches: no two events of one tale within six places share a batch; every event stands in exactly one; sizes as stated.
- No line, rule or prompt carries a tale identifier, title, event number, or anything of section 2's forbidden list from `test_pilot.py`.
- The key restores story order exactly: a planted labelling comes back in the right order.
- The expected tau reproduces section 3's table, and the null gives about 0.
- The reading gives its four results on planted figures.
- Two runs are byte-identical.

## 7. Decisions for the owner

**Taken 2026-11-04: the owner accepted all six recommendations.**

1. **This in place of part 2.** Recommended. Part 2 would likely meet the same recognition. It stays set up, should you want it later.
2. **The hero on each line.** Recommended. Functions are defined around a hero, and without one the coding would suffer. It does tell a reader which lines may share a tale, though not their order.
3. **Names left in the lines.** Recommended. Removing them would mean rewriting the paraphrases, a new source of error. A reader could group lines by name, but with only a sixth of a tale in hand, spaced at least six apart, that gives little.
4. **East Asian baseline: the old strings.** Recommended, to save running a whole-tale neutral cell. The cost: run noise of up to 0.12 (`CardPilotReport.md`) stays in that comparison.
5. **The reading's numbers (0.25, 0.5, 0.15).** Recommended. They are the keeper's judgment from section 3, set before any new label.
6. **In parts:** the wondertales first, then the East Asian tales. Recommended.

## 8. Order of work and cost

1. The owner's review and decisions; this file frozen (done 2026-11-04).
2. The batches, key, rules, prompts, measure and tests, in `shuffledSetup.py` and `shuffled.py`, in TaleCoding under `lines/`; committed before anything runs. The owner reads the cut rules.
3. Part 1, then part 2, at the owner's word.
4. The labels committed; the key applied; the measure run; the report.

**Cost:** readers again, but far less to read. 864 events, 2 readers, 24 subagents of about 60 to 80 lines, about 28,000 words of input plus the card each time, and no whole tales. Part 1 of the pilot had four readers each read 15 whole tales. The keeper expects a fraction of that, unmeasured. Your usage figure from part 1, if you have it, would size it better.
