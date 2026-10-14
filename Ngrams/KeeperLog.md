# Keeper log: frequencies of functions and acts

**2026-10-14. Drafted, not yet frozen** (`NgramProtocol.md`, `ngrams.py`), at the owner's proposal of 2026-10-13 and word to proceed. Nothing counted but the corpora's sizes: function strings 275 stories (A 3,582 tokens, B 3,941; 44 and 42 kinds), act strings 159 stories (A 5,995, B 5,519; 36 kinds each), halved within each genre.
**The self-test** (`ngrams.py selftest`): in random strings with an adjacent pair and a pair two apart planted, and independent filler for each transcriber and half, discovery finds both and two chance pairs; confirmation keeps the two planted pairs, with the shapes adjacent and spaced (peak 2 apart), and rejects the chance pairs.
**A reader fault found and fixed before any count:** `twoLayer.read_acts` was given the folder pattern `*/acts/`, which since the problem test also matches `problems/acts/` and would have read those stories twice; the act reader now names the three genre folders.
**2026-10-14. Frozen at the owner's word** (`NgramProtocol.md`, `ngrams.py` as committed at 851cc28), nothing counted.
