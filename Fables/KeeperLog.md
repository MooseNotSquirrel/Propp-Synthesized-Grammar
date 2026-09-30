# Keeper log: the held-out fable test

**2026-09-30. The grammar and the test frozen first.**
`FableEBNF01.txt`, `fableGrammar.py`, `FablePrediction.txt` and `fableDraw.py` were committed before the draw (second project c7ac5c1).

**The draw.**
`fableDraw.py` drew 100 of the 210 undrawn fables with seed 3401 into the new repository's `Sample.txt` (`Story Language/Fables`, GitHub Propp-Fables).

**F001 dropped before any run, as a flaw of the instrument, not a result.**
`AesopRules.md` uses F001, "The Lion And The Mouse", as its worked example: its first event, its hero ("the Mouse") and two sample transcription lines. In the first Aesop run F001 was not drawn; here it was, and a lister or transcriber would be copying the rules' example rather than reading the fable.
Rewriting the example would change the instrument, and a redraw is a step the frozen test does not name, so F001 is left out of the prompts and the test is run on 99 fables. `Sample.txt` keeps the draw as it fell.

**The transcriber repository holds only the transcriber half.**
`AesopRules.md` is byte-identical to the Aesop test's; the event-listing prompts are the Aesop prompts' rules word for word, regenerated with the new fables (the method was checked by regenerating the original e1 prompt exactly); the transcription prompts are the Aesop prompts with the fable lists and output folders changed.
Neither the grammar, the prediction nor the Aesop result is in that repository.

**The events stage, from master at 15f11e3: in form.**
99 fables, 462 events, every fable with events numbered from 1 and one hero line. The replies were split into `Events.txt` and `Heroes.txt` by line format; the one merge change of the first Aesop run was applied, sixteen ties the second report names written "X; Y". No fable dropped.
The second lister counted the one addressed by a speech act as taking part, so most two-character dialogue fables came out as ties; the first lister counted the same way and wrote its ties with a semicolon. Ties mean two heroes and two transcriptions of those fables, as the rules provide.

**The main stage, from master at 904c8a4: both transcriptions in form.**
Transcriber A covers all 128 versions (99 fables, the ties twice) in 572 entries; B covers them in 580, labelling three single-hero fables F269/1, F304/1 and F308/1, which cover all their events. Transcriber A kept its working script, `build.py`, in its own output folder, as the prompt allows.

**THE VERDICT, as FablePrediction.txt defines it: THE CLAIM FAILS.**
`fableGrammar.py measure ../Fables b1 b2 b3 b4`, output in `FableRun.txt`, versions of two or more functions marked Y:

                   acceptance   shuffled   gap     v46's gap
  transcriber A    55.6%        28.1%      +27.4   +10.6
  transcriber B    61.7%        31.9%      +29.8   +15.1

1. Acceptance at least 65%: not met by either transcriber (55.6%, 61.7%). This alone fails the claim.
2. Gap at least 20 points: met by both.
3. Gap above v46's: met by both, by 16.8 and 14.7 points.

REPORTED, NOT JUDGED. The grammar's order held on fables it had never seen: its gap over shuffled shrank only from +31.6 and +33.7 in training to +27.4 and +29.8, while its acceptance fell from 74.7% and 75.9% to 55.6% and 61.7%. Shuffled acceptance fell too, from about 43% to 28% and 32%, so the held-out streams are harder to accept in any order; the grammar's coverage of fables was overfitted, its order was not. Its margin over v46 grew rather than shrank (from about 12 points in training to about 15 to 17). What fails is the claim that the grammar describes most fables; what survives is that where fables are ordered, they are ordered its way, better than Propp's way.

**The block analysis of the held-out fables, reported and not judged, as FablePrediction.txt provides.**
`blockStream.py run fables ../Fables`, output in `Blocks/FablesStreams.txt` and `Blocks/FablesPatterns.txt`; the round trip holds on every held-out transcription (BlockTests.txt, 48 passed).
It replicates the training findings. Functions fall inside Propp's blocks above chance in every reading for both transcribers (strict: 26.8% against 21.2%, and 24.4% against 17.4%; 1 and 0 shuffles of 200 as high). Reversed blocks are again at or below chance: none of any kind for B, and for A only two reversed complications against about five by chance. DeceptionTrap again stands out, 9 and 11 against about 3 by chance and never reversed, and is followed by the harm A 8 times in 20 (10 in 27 in training).
New in the held-out fables: the trick is also followed by its defeat, victory I or rescue Rs, 6 times in 20, often with an exposure after; and TaskAndSolution rises above chance (7 and 3 against 2.2 and 0.7).

**A cursory look at the X events, 2026-09-30, on the held-out fables only.**
Asked for a quick look at the X events, the keeper looked at the held-out fables, not at the X study's discovery material: the training fables, Apollodorus and tragedy P01-P04 stay unread for the frozen method item 3 (b2) of the queue requires. Of the 462 held-out events, 160 were X for both transcribers and marked as mattering. Two kinds stand out: a spoken verdict or lesson (a rebuke, a retort, a character stating the moral), the largest group, which no function of Propp's covers; and harm that comes from the sufferer's own act with no villain, close to Dundes's consequence. The rest are mostly setting-up acts and moments of misperception. This is an impression, not a count by a frozen method.
