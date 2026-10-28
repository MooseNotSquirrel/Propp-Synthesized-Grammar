# The revealed villain: protocol (FROZEN 2026-10-28 AT THE OWNER'S WORD, THE FOUR RECOMMENDED DECISIONS TAKEN, THE QUESTION AS DRAFTED)

**Drafted 2026-10-28 at the owner's word**, after the failed-hero test (`FailedHeroProtocol.md`); **frozen the same day at the owner's word**, every decision of section 6 taken as recommended and the question of section 2 worded exactly as drafted. Nothing here is built, and no figure it tests has been read.

## 1. The question

**The owner's observation:** in Oedipus the surprise at the close is that the hero is the villain. He has killed his father and married his mother, before the play opens and without knowing it.

**Why the failed-hero test could not see it.** Propp's functions mark what happens in the action, in order. A villainy committed before the story and uncovered in it is told as recognition (Q) or exposure (Ex), not as villainy (A). The sphere grouping credits the villain's sphere only to the performer of A, so a hero whose crime is uncovered is not counted as fused. In P03 transcriber A's fused character is "thebes", not Oedipus.

**The question:** is the revealed villain, a hero shown to be the cause of the harm the story turns on, a mark of tragedy? It is the owner's pattern, tested as its own measure. It is not from Propp, though it uses his functions where it can.

## 2. Two routes (decision 1)

- **(a) From the tables, no readers.** A story counts when its judged hero is the undergoer of an exposure (Ex), or of a recognition (Q) that follows a villainy (A) in the same story. This is cheap and repeatable, but the letters do not say whose crime is exposed. An exposure of the hero as a false claimant would count wrongly, and a revelation the transcribers wrote only in a note would be missed.
- **(b) Two readers, one question a story.** Each reader gets the story's title, its event list (`tables/events.tsv`) and the judged hero's name, and answers:

  > Does the story reveal, at some point, that its hero is himself the cause of the harm the story turns on, whether he did it before the story begins or during it, knowingly or not? Answer yes or no, give the number of the event where it is revealed, and one sentence of reason.

  The answer counts where both readers say yes. This is closer to the owner's pattern, but it is a judgement by two models, reported as such.
- **Recommended: both.** Route (b) is primary; route (a) is reported beside it, with their agreement. Where they differ, the table's letters are shown not to carry the pattern.

## 3. The material

- **The hero:** the judged hero, as mended on 2026-10-28. Stories whose readers named no single hero, or none, are left out.
- **The corpora for the reader stage (decision 2):**
  - **(i) recommended:** the tragedies and the wondertales, the comparison that matters, 51 stories with a judged hero. That is one or two batches, about 4 readers and 250,000 tokens;
  - **(ii)** every corpus with judged heroes, about 280 stories, 4 batches, about 8 readers and 500,000 tokens.
- **The myths:** they have no judged heroes, so they take no part, as in the failed-hero test.

## 4. Tests, before any result is read

- **R1. Invented stories** for route (a), with known answers: a hero exposed after his own A; a false hero exposed; a villain exposed. The program must give each answer exactly.
- **R2. The reader stage's form**, as in the name stages: every story answered once, yes or no, an event number that exists, and a reason.
- **R3. Controls in the reader stage:** six stories whose answer is plain and fixed in advance, mixed in unmarked: three yes (Oedipus P03 if its hero is judged, and two the keeper names from the events before the stage) and three no (wondertales with a separate villain). Both readers must answer at least five of the six as fixed; otherwise the stage is reported and not scored.
- **R4. The same answer twice:** route (a) gives byte-identical output.

## 5. Predictions, to be frozen with this file

Tested per transcriber, with the readers' answers attached to each transcriber's stories. It **HOLDS** if for both, **SPLIT** if for one, **FAILS** if for neither. The test is a permutation test at p at most 0.05, with a floor of 10 stories a side.

1. **By the readers (route b):** the hero is revealed as the cause of the harm in a higher share of tragedies than of wondertales.
2. **By the tables (route a):** the same, from the letters.

**Reported, not tested:**
- the agreement of the two routes, story by story;
- the readers' agreement;
- the list of revealed-villain stories, with the revealing event;
- whether the revealed villain and the fused hero of the failed-hero test are the same stories.

## 6. Decisions for the owner before the freeze

**Taken 2026-10-28: the owner accepted all four recommendations, with the question worded as drafted.** Route: both, (b) primary. Corpora for the readers: (i), the tragedies and the wondertales. The question: exactly as in section 2, "knowingly or not" and "the harm the story turns on" kept. The controls: the six of R3 named by the keeper before the stage.

1. **The route:** both, route (b) primary (recommended); (a) alone; or (b) alone.
2. **The corpora for the readers:** (i) the tragedies and wondertales (recommended), or (ii) every corpus with judged heroes.
3. **The question's wording** in section 2, to be fixed exactly as frozen. In particular: whether "knowingly or not" stays in, and whether "the harm the story turns on" should read "a harm in the story".
4. **The controls:** the six of R3 named by the keeper before the stage (recommended), or by the owner.

## 7. After the freeze

1. Commit this file frozen (done 2026-10-28).
2. Write and commit the invented stories of R1, the program for route (a), and the stage's inputs, prompts and controls; dry-run.
3. Run route (a). Then run the reader stage in portions, at the owner's word.
4. Score, log, and enter the finding in `PreliminaryFindings.md` at the owner's word.
