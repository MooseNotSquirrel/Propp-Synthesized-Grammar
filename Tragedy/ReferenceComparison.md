# The tragedies against the transcribed wondertales

**Frozen 2026-10-05, while P05 to P32 are sealed, after the Afanasyev calibration showed that the tragedy protocol's thresholds cannot be met by the instrument even on Propp's own tales.** A second comparison, added beside `TragedyProtocol.md`, which is not changed: its verdict is still given as frozen. A departure is logged in `KeeperLog.md`, not made here.

## Why

The tragedy protocol judges coverage and acceptance against levels set from Propp's own schemes (80% and 85.2%). On the 45 Appendix III tales the same instrument covers 62% to 67% of events and v46 accepts 22% to 29% of its moves (`Calibration/KeeperLog.md`). A tragedy failing those levels therefore says nothing about tragedy. The fair reference is the instrument's own reading of Russian wondertales.

## The two corpora, one instrument

**Tragedy:** the 32 plays, transcribers A (Opus) and B (Sonnet), under `TragedyRules.md`.
**Wondertale:** the 45 Appendix III tales, arm U, transcribers A (Opus) and B (Sonnet), under `AfanasyevRules-U.md`.
The definitions card is the same, byte for byte, in both. The rules differ only where a play differs from a tale (speeches, told-past events, the cast list). Each event list was made by fresh Opus listers under its own rules; that difference is part of the instrument and is reported, not removed.

## The measures, per story

1. **Coverage:** the share of the story's events with a function entry kept by the primary reading (marked Y, doubtful included).
2. **Acceptance:** the share of the story's moves that `ProppEBNF46.txt`, as shipped, accepts at `move`; moves built as `tragedyScore.py` builds them.
3. **Backward order:** the share of the story's pairs of function entries, in the story's order, that run against Propp's numbering, as `tragedyScore.py` counts them (primary reading, play order as told).

A play with k heroes counts once, its value the mean of its k versions. A story with no move, or no pair, is left out of that measure.

## The test

For each measure and transcriber: the difference of means, tragedy minus wondertale, against 10,000 random relabellings of the 77 stories into groups of 32 and 45, seed 46; two-sided p.

**For each measure, the tragedies DIFFER from the wondertale** if p is at most 0.05 for both transcribers, with the difference in the same direction; **DO NOT DIFFER** if p exceeds 0.05 for both; **UNSETTLED** otherwise. The direction is reported: lower coverage, lower acceptance and more backward order read as tragedy less like the wondertale.

No overall verdict: three measures, each reported.

## When

The program (`tragedyReference.py`) is committed with this file and run on P01 to P04 for form only. It reads P05 to P32 only when the seal lifts under `TragedyProtocol.md`, and the verdict is given only on all 32.
