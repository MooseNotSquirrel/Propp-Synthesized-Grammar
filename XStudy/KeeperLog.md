# Keeper log: the X study

**2026-10-06. The method frozen** (`XStudyProtocol.md`), with the recurrence threshold the owner approved: at least 10 events where both assigners agree, from at least two genres, at least 3 in each.

**The targets selected** (`xTargets.py`, `Targets.txt`): events that both original transcribers left X and both marked as mattering. Discovery: 142 in the 22 development tales, 169 in the 100 drawn fables (75 fables hold one or more), 324 in tragedy P01-P16. Test, held back: 137, 152 and 358. The labelers' material, the discovery stories with their target events marked, is in the transcriber-side repository `Story Language/XStudy` (eaf89de), with the prompts of the labeling, grouping and assignment stages, all written before any label exists, and its run file.
SEEN BY THE KEEPER: while checking the material, the first lines of `stories/b2.txt` (fables F007 and F012, their events and marks). No label has been read; none exists.
A FIX BEFORE COMMIT: the labeling prompt's example line first used a real target event (F012, event 7); it was replaced by an invented one (S000) before any run, so that no labeler is handed a label.
