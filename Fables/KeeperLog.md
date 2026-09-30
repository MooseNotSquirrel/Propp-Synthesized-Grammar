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
