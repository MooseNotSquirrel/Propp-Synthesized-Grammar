# Improving the measuring stick: development and test

**Frozen 2026-10-05, after the calibration's result (`KeeperLog.md`) and before any improvement was built.** A departure is logged in `KeeperLog.md`, not made here.

## The question

The calibration found the instrument PARTLY CALIBRATED: it reads the tale in front of it, but writes about 1.5 times as many functions as Propp prints and agrees with his order poorly. This test asks whether processing the transcriptions we already hold, without new transcription and without consulting Propp's scheme for any tale being scored, brings them closer to Propp.

## What was seen before this was frozen

The aggregate figures over all 45 tales in `CompareRun.txt` and the diagnostics in `KeeperLog.md` (symbol counts, recall and precision, the once-per-tale reading). No tale's stream has been read against its scheme. This contaminates the choice of ideas, not the test half's scores.

## The split

`Split.txt`: 22 development tales and 23 test tales, drawn with seed 46. Everything is built, tuned and compared on the development tales only. The test tales are scored once, with the pipeline frozen and committed first.

## The candidates

1. **A Propp view.** A fixed rule, applied to a transcriber's stream, that writes it as Propp writes a scheme: for instance, a repeated episode written once. The rule may use the transcription's own entries, notes, events and moves, and the general conventions of Propp's book; it may not use any tale's scheme.
2. **Consensus.** For each event, keep the functions that a set share of the four readings (arm U and C, transcribers A and B) give it.
3. **Order, diagnosed.** Order agreement on tales where Propp prints braces or embedded moves, against tales where he prints neither. Diagnostic only: the frozen comparison's reading of Propp's schemes is not changed by this test.

The development may combine 1 and 2, or choose neither. What it ends with is one pipeline, written as a program and committed, with its development figures, before the test tales are scored.

## The test, on the 23 test tales

The pipeline's output and the transcriptions as written are each scored against Propp by `compare.py`'s content and order measures, for each transcriber (or once, for a consensus). Reported with each: the chance-corrected figure, (real − chance) / (1 − chance), with chance from 1000 derangements of the test tales, seed 46, since the raw figure flatters (KeeperLog); v46 acceptance; and the A-B agreement where two readings remain.

**The pipeline is ADOPTED if, on the test tales:**
1. content and order with Propp each improve over the transcriptions as written, by a paired sign-flip permutation test on the per-tale differences, 10,000 permutations, seed 46, p at most 0.05 for each; and
2. each improvement is at least half the improvement it showed on the development tales, so that what was tuned is not mostly fitted to them; and
3. both measures still beat the derangement baseline with at most 50 of 1000 at or above.

**NOT ADOPTED** otherwise, and the instrument as written stands. Either way the result, development and test, goes into the paper.

## If adopted

The same program is run, unchanged, on the Aesop, fable and tragedy transcriptions. The sealed tragedies are processed only when their seal lifts.
