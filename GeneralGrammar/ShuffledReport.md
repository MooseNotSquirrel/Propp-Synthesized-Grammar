# Events coded apart from their tales, the wondertales: report (2026-11-04)

The protocol is `ShuffledProtocol.md`; the figures are in `Shuffled-wonder.txt`, from `shuffled.py`; the strings are in TaleCoding at 7ee978d. 488 events from 15 tales, 2 readers, 12 batches; all coded, no code off the card. The East Asian part has not been run.

## The frozen reading

| Reader | Tau, coded apart | Whole-tale tau | Kappa with whole-tale | Expected at that rate | Null 95th | Reading |
|---|---|---|---|---|---|---|
| **A** (Opus) | **0.575** | 0.740 | 0.508 | 0.332 to 0.680 | 0.290 | **IN THE EVENTS** |
| **B** (Sonnet) | **0.563** | 0.621 | 0.358 | 0.147 to 0.526 | 0.282 | **IN THE EVENTS** |

Kappa of A with B, coded apart: 0.555.

**His order still appears with each event coded alone, by readers who could not see its place.** The fall from the whole-tale figure is no greater than worse coding alone predicts. Reader B is above the top of its expected range.

## What this does and does not show

**It shows:** for the wondertales, the order does not need a reader following a tale in sequence, so it is not written in by expecting what comes next. It stands in what the events are.

**It does not show that the order is Propp's in particular.** Readers said as much: "some lines plainly come at the start (introductions, births) or the end (weddings, returns)". A return or wedding comes late in most stories anywhere. This is a mark of narrative logic at least as much as of his scheme. Only the other corpora, and control E2, can part them.

**Other limits:**
- **Recognition did not go away.** All six of A's batches named Propp; two of B's six did. Those readers know his functions, though they could not see an event's place. Reader A4 wrote that "tale-type knowledge made the rough position clear for many lines".
- **The labels still carry knowledge of what each function is,** so the mapping from event to function is his, by design. It is the sequence that was withheld.
- **Hero names** let a reader guess which lines share a tale, as A5 noted. A reader held about a sixth of a tale, spaced at least six apart.

## Beside the reading

- **The words alone give little place:** position predicted from a line's words on held-out tales, R squared 0.064. That is a plain word model, which knows less than a reader does, so it is a floor.
- **Coverage.** Given a symbol: A 70% against 72% whole-tale; B 62% against 87%. Reader B's rise under the neutral card in the whole-tale cell vanished here. B moved 119 more events to X, most of them from F, E, D, B, θ and the departure, which depend most on context.
- **Preparatory units coded alone** (mean place apart, whole-tale). β 0.05, 0.11 (A); γ 0.34, 0.38 and 0.43, 0.39; **η 0.49, 0.49 and 0.43, 0.46; θ 0.34, 0.61 and 0.42, 0.57.** Absentation stands first. **Trickery stands mid-tale even coded alone,** so that is in the events and not the card's filing rule: this supports the owner's point about deception after villainy. Complicity moves early when alone, so whole-tale coding ties θ to later events.
- **Exploratory, added after the reading** (`ShuffledSubset.txt`): reader B's batches that said no scheme came to mind give tau 0.434 (null 95th 0.330; 325 events); those that named Propp give 0.309 (null 0.355; 163 events). So no sign here that recognizing him is what makes the order. It is a self-report, on few batches, and no test.

## Cost

No failures. The owner's usage figure gives the measure.

# The East Asian tales (2026-11-04)

`Shuffled-east.txt`; TaleCoding a4f6a23. 376 events from 15 tales, all coded, no code off the card. The baseline is the old strings, so run noise of up to 0.12 stays in the comparison.

| Reader | Tau, coded apart | Whole-tale tau | Kappa with whole-tale | Expected at that rate | Null 95th | Reading |
|---|---|---|---|---|---|---|
| **A** (Opus) | **0.695** | 0.785 | 0.507 | 0.360 to 0.708 | 0.259 | **IN THE EVENTS** |
| **B** (Sonnet) | **0.440** | 0.711 | 0.453 | 0.249 to 0.641 | 0.268 | **IN PART** |

Kappa of A with B, coded apart: 0.618.

**Reader B is "in part" only because it is under the bar of 0.5.** It stands above the null and inside what worse coding alone predicts, so nothing points to the order needing the sequence. Neither reader in either corpus came near "needs the sequence".

**Beside the reading:**
- **The words alone give no place:** R squared −0.121 on held-out tales.
- **Recognition:** all six of A's batches named Propp; three of B's six did. A's readers said lines often showed "whether an event fell early, in the middle or late".
- **With preparatory units the tau falls:** 0.473 and 0.364. Those functions do not keep his early place here: η 0.42, 0.47 and θ 0.54, 0.36 coded alone, γ about 0.48. β is 0.34 in reader A, against 0.14 whole-tale.

## The two corpora together

| Tau, no preparatory units | Whole-tale A, B | Coded apart A, B |
|---|---|---|
| Wondertales (15) | 0.74, 0.62 | 0.58, 0.56 |
| East Asian (15) | 0.79, 0.71 | 0.70, 0.44 |

**That two unrelated traditions give about the same order, coded apart, cuts two ways.** It may be that Propp's order reaches beyond the Russian tale. Or it may be narrative logic that any story would show. The contrast needed is a corpus with a different form. Whole-tale tragedies stand at about 0.2, so a coded-apart run there would show whether this test can say no.

# The tragedies: can the test say no? (2026-11-04)

`TragedyApartProtocol.md`; `TragedyApart.txt`, from `tragedyApart.py`; TaleCoding 2b84b49. 480 events sampled from 32 plays, all coded, no code off the card.

| Reader | Tau, coded apart | Whole-play, same events | D, on shared functions | Kappa with whole-play | Reading |
|---|---|---|---|---|---|
| **A** (Opus) | **0.117** | 0.134 | −0.177 [−0.458, 0.258] | 0.515 | **THE TEST SAYS NO** |
| **B** (Sonnet) | **0.243** | 0.426 | −0.214 [−0.472, 0.371] | 0.468 | **THE TEST SAYS NO** |

Kappa of A with B, coded apart: 0.612. The keeper's expectation held.

## All three corpora, coded apart

| Tau with his order | A | B |
|---|---|---|
| Wondertales | 0.575 | 0.563 |
| East Asian | 0.695 | 0.440 |
| **Tragedies** | **0.117** | **0.243** |

**The same card and method, by readers who recognized it just as often** (all six of A's batches, four of B's six), give a low tau on plays. So the labels do not bring his order regardless of story. This removes the reading that would have undercut the last two reports.

**How firm the contrast is.** Reader A: tragedies below wondertales, 90% interval of the difference 0.084 to 0.634, and below East Asian, 0.027 to 0.692. Reader B: the intervals include 0 (−0.128 to 0.547, −0.218 to 0.529). So the direction is the same in both readers, and clear only in A. These are small samples, measuring about 15 functions.

**What it bears on narrative logic.** Plays are stories too, with harms and repairs, and they do not show his order. So the order is not what every story shows, and "narrative logic in general" is weaker for this. It is not gone. Some functions keep their late place in plays too (K, Q and U stand late in both readers), and a logic particular to tales would still fit. Wedding stands early here (0.34, 0.33), against about 0.75 in the tales; so do arrival and return.

**The cost:** from 29% to 47% of the budget, 18 points, including the keeper's setup, for 12 subagents and 480 lines. The East Asian part, 12 subagents and 376 lines, took 26 by the owner's figure.
