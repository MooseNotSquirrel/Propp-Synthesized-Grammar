# The story grammar by levels: protocol (DRAFT 2026-10-31, for the owner's review; nothing built or run)

**Asked by the owner on 2026-10-31.** The frozen story grammar adds all its constraints into one score. A culture might use Propp's devices, his pairs and his blocks, and still order the large sections of a tale in its own way; one blended score would hide that. This protocol separates the grammar's levels, so that each can be read on its own, in the existing corpora and in the new ones.

**What it does not change.** The frozen grammar (`StoryGrammarProtocol.md` sections 10 and 11) is not refitted, retuned or reweighted, and predictions 3 and 4 are scored on it exactly as fixed. Everything here is reported beside them.

## 1. The four levels

The grammar's 80 constraints (`StoryGrammarDesign.md` section 4) fall into four levels, and a fifth group that is left out:

| Level | Constraints | Count |
|---|---|---|
| **Sections:** the order of Propp's ten sections | the 45 section orders | 45 |
| **Pairs:** paired functions in order, and close together | the 9 pair orders and 9 pair cohesions of the constraint grammar, and the 12 Propp's pairs within the move | 30 |
| **Blocks:** functions told in Propp's blocks | outside blocks | 1 |
| **Move:** the whole move against v46 | move not accepted, repairs per unit | 2 |
| *Left out: length, a control* | units, moves | 2 |

## 2. The measures

**M1. A concordance for each level.**
- **What it does:** each story is scored against the same 200 alternatives as `storyGrammar.py run` drew, under the frozen weights of one level only, the other levels' weights set to zero. That gives four concordances per corpus and transcriber, and the record's single figure besides.
- **What it shows:** which levels tell a story's real order from its shuffles, and which do not.

**M2. Shuffles that move one level at a time.**
- **How a story is cut:** each move is cut into *segments*, the longest runs of consecutive functions of one section.
- **Two kinds of alternative,** 200 of each per story, drawn by a fixed seed:
  - **Section shuffles:** the segments of each move are put in a random order, each keeping its own order inside.
  - **Inner shuffles:** the functions inside each segment are put in a random order, and the segments keep their order.
- **The measure:** each story's concordance against each kind, under the whole frozen grammar and under each level.
- **What it shows:** a corpus that uses Propp's devices but its own large-scale order beats the inner shuffles and not the section shuffles. A corpus that uses neither beats neither.
- **Where they say nothing:** a story with one segment has no section shuffle, and a story whose segments are all single functions has no inner shuffle. These are reported as not applicable and left out of that measure's figure, and their number is reported.

**M3. Each corpus's own section order, with no model.**
- **The table:** for each corpus and transcriber, a 10 × 10 table of precedence. Cell (i, j) is the share of pairs of functions, one of section i and one of section j in the same move, in which the section i function comes first. Each story is weighted 1 over its number of versions, as in the record.
- **The order:** each corpus's own order of the sections, by how often each comes before the others.
- **Against Propp:** its rank correlation (Kendall) with Propp's order.
- **What it shows:** the frozen grammar cannot learn a new culture's order, because it is not refitted on the new tales. This table shows what that order is.

## 3. The stories

- **The five existing corpora:** the held-out stories only (`HeldOut.txt`), as the record scored them. The fitting stories would favour the weights that were fitted on them. M3, which uses no weights, is also reported on all the stories.
- **The Native American and East Asian tales:** all of them. None was seen in fitting.

## 4. Tests, before any figure is read

- **L1. The record reproduced.** With all four levels and length together, M1 must give each corpus's concordance exactly as `StoryGrammarRun.txt` gives it.
- **L2. The shuffles are what they say.**
  - Every section shuffle keeps each segment's functions and their order.
  - Every inner shuffle keeps the order of the segments.
  - Both keep each function in its move.
- **L3. A planted culture.** A corpus is built from the wondertales' held-out stories, with the order of their segments permuted the same way in every story. It must score high on the inner shuffles and low on the section shuffles. M3's order for it must show the permutation.
- **L4. The same answer twice.** Two runs are byte-identical.

## 5. Decisions for the owner

1. **The levels:** the four of section 1, length left out (recommended), or another grouping.
2. **The stories:** held-out only for the existing corpora (recommended), or all of them.
3. **Reported only, or with one prediction for the new corpora.**
   - Recommended: reported only for the existing corpora.
   - For the new corpora, one prediction, the owner's question put as a test: *in each new corpus, the concordance against inner shuffles is higher than against section shuffles.* That would mean Propp's devices travel further than his large-scale order.
   - It is tested per transcriber, by a paired sign-flip test over stories, at p at most 0.05 with at least 10 stories: HOLDS, SPLIT or FAILS. It must be frozen before the new corpora's tables are built.
   - This is a reading offered by the keeper, prompted by the owner's question; it is not from Propp.
4. **Comparing the section orders:** a corpus's correlation with Propp's order, compared with another corpus's by a permutation of the corpus labels over stories, at p at most 0.05 with at least 10 stories a side (recommended), or reported without a test.

## 6. Order of work, and the cost

1. The owner's review and decisions; this file frozen.
2. The program, `StoryGrammar/levels.py`, written and committed, and L1 to L4 passed, all before any figure is read. Its commands score the existing corpora now, and the new corpora later, by one command each.
3. Run on the five existing corpora (exploratory), at the owner's word. Planned for after the weekly budget resets.
4. **On the new corpora:** run only after the frozen grammar's predictions 3 and 4 are scored, and only from tables built after this file and the program are committed.

**The cost:** no readers. The keeper's work, and a few minutes of computing per corpus. M1 and M2 rescore the alternatives; M3 is a count.
