# Method: how every test in this record was run

**Written 2026-10-20 from the practice the record shows.** It states what was done, so that a reader can judge each result, and a later study can follow the same rules.

## The roles

**The owner** sets the questions, decides what is hard to undo, and freezes each test by saying so.
**The keeper** (Claude, in Claude Code) designs each test, writes its programs, checks what comes back, scores it, and keeps the record; the keeper reads results, and so never transcribes.
**The transcribers and describers** are fresh language-model instances, A on Opus and B on Sonnet, blind to each other and to the project, each given one prompt file and the rules it names. Two readers on two models give every measure a check of agreement.
**The runner** is a cloud session that starts the describers, saves their replies word for word, checks that each folder holds what it should, and commits; it reads and judges nothing.

## The repositories

**Transcriber repositories** (Propp-Afanasyev, Propp-Aesop, Propp-Fables, Propp-Tragedy, Propp-XStudy, Propp-ActsRoles, Propp-Apollodorus) hold only the stories, their event lists, the rules, the prompts and `RUN.md`; nothing of the keeper's.
**The keeper's repositories** (the first project, `Project Files`, and the second, `SynthesizedProppGrammar`) hold the protocols, programs, results and logs. Each study has its folder: a protocol, its programs, its outputs and a keeper log.

## Test first

**A protocol is written and frozen before the data it tests exist or are read.** It states the question, the material, the instrument, the measures, the predictions with their thresholds, and the verdict's rule.
**The scorer is written in full and committed before scoring.**
**The freeze is the owner's word,** recorded in the protocol's first line and the keeper log with the commit it froze.
**Predictions are written as HOLDS or FAILS with numbers fixed in advance.** Where a prediction is drawn from data, those data are named as the development set, and the test is on stories not yet read.
**What the keeper already knows of the material is stated in the protocol,** and the predictions avoid it.

## Before the freeze

**Every scorer is run end to end on synthetic data**: data with a planted effect, which must be found, and random data, which must not. These dry runs caught a length confound, a criterion below chance and a threshold too strict before any real data were scored.
**A self-test should include the degenerate case,** not only the clean one; one that did not missed a grouping collapsing into a single class.

## The run

**A cloud stage per batch of describers,** started by the owner in a fresh session; `RUN.md` says which stages are cleared, and a runner refuses a stage not yet cleared.
**After each stage the keeper merges fast-forward only, checks the form** (every event covered, every value from the lists, no stray files), and logs the stage.
**Departures are logged, never corrected:** a describer who skims a play, a file cut short, a field written wrongly. A describer is never started again.

## Scoring

**The frozen scorer is run once,** and its verdict stands.
**Checks made after the verdict are reported, not judged,** and say so: dropping a describer's unread plays, mending a reader's fault, a different choice of measure. They can explain a result; they cannot reverse it.
**Faults found in the keeper's own work are named as the keeper's** in the log, with their size measured.

## Measures that recur

**Agreement** as both over either (Jaccard), summed over events.
**Chance** from shuffles: of a story's own items in place, of items across a genre's moves keeping lengths, of genre labels across stories; the p-value is the share of shuffles at least as extreme, plus one over the count plus one.
**Both transcribers must show an effect** for it to count.
**Discovery and confirmation** on separate halves of the stories, the candidate list committed between them.
**Length is removed** where it can drive a measure, by scoring a story against a random description of its own acts.

## Writing it down

**Each finding goes into `PreliminaryFindings.md`** marked as established, tested, tentative or withdrawn, and a reading is labelled as the keeper's, not Propp's and not the owner's.
**A claim found too strong is withdrawn in so many words,** where it stood.
**The queue** (`Project Files/ProppQueue.md`) names what is done and what is next, and each session begins by reading it.
