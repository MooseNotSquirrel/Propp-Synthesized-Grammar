# Does the card write the order in? A pilot: protocol (DRAFT 2026-11-04, for the owner's review; nothing set up or run)

**Asked by the owner on 2026-11-04,** after `LeafReport.md`: the order of the tales sits in the function labels and hardly at all in the acts. Either functions really carry a tale's structure, or readers holding a card that lists functions in Propp's order write his order in. Strings already collected cannot separate these.

**What it does not change.** No earlier verdict, table or string. The new strings go in their own folder and are not built into the tables.

**The caution:** the readers are modern models reading translations, or Russian. They may know Propp from training, whatever the card says. The pilot can lower what the card tells them; it cannot remove what they already know.

## 1. What changed from the keeper's first description, and why

The keeper described the pilot to the owner as new event lists without Propp, plus a scrambled card with definitions tied to significance. Reading the rules afterwards changed two of the three:

- **No relisting.** The East Asian listers' rules (`ActsRoles/eastasian/ListRules.md`) do not name Propp at all. The wondertale listers' file named him in its first lines, and their prompt said his functions played no part and not to read as far as the card. So the existing lists are fair for this test, and the caution in `LeafProtocol.md` overstated the matter for these two corpora. It came from the earlier fables and plays.
- **Definitions unchanged.** Changing the order and the definitions together would leave a difference with two possible causes. Definitions tied to significance belong to card D, at step 7.

## 2. The design

The same tales and the same event lists, coded twice by fresh readers, with one difference: the card.

| Cell | The card | Where |
|---|---|---|
| **H** | `AfanasyevRules-C.md`'s rules and card as they stand: his symbols, in his order | As earlier stages |
| **S** | The same rules and definitions, word for word where possible, with what points to Propp removed | A repository with a neutral name |

**What S changes, and nothing more:**
- **The order:** the card's rows shuffled by a fixed seed.
- **The symbols:** neutral codes standing in for his, throughout the rules and examples. The key is kept by the keeper, outside the readers' repository, until the strings are committed.
- **The names:** the column of function names dropped (villainy, donor and so on stay only where a definition's own words need them).
- **Propp:** his name, page references and the title dropped. His quoted sentences stay as plain rules, unattributed.

**The owner reads the S card before anything runs,** beside the H card, to judge that the meaning is unchanged.

**Why both cells are run new:** a difference between new S strings and old strings could come from the run itself. H and S run at the same time, on the same models, so only the card differs. The old strings stand beside them as a third figure.

**The readers:** A on Opus, B on Sonnet, fresh and blind to each other, as before. Each reader's report ends with one question, asked after the work is committed: whether they recognized the scheme, and whose. It is reported, not scored.

## 3. The tales, and how many

**15 wondertales and 15 East Asian tales,** drawn by seed 20261104 from those with at least three function units in both old readers' strings, the draw written to a file before any coding.

**Why 15.** The noise was measured on the old strings before this draft (`pilotNoise.py`, `PilotNoise.txt`): mean-position tau with Propp's numbering, no preparatory units, 500 random subsets.

| | All | 10 tales, 90% range | 15 tales | 20 tales |
|---|---|---|---|---|
| Wondertales, A | 0.78 | 0.63 to 0.86 | 0.67 to 0.87 | 0.70 to 0.86 |
| Wondertales, B | 0.77 | 0.63 to 0.86 | 0.69 to 0.86 | 0.71 to 0.86 |
| East Asian, A | 0.74 | 0.48 to 0.86 | 0.55 to 0.82 | 0.59 to 0.83 |
| East Asian, B | 0.60 | 0.44 to 0.88 | 0.50 to 0.86 | 0.52 to 0.84 |

Strings shuffled within the story give about 0 (−0.40 to 0.33 at 10 tales). So 10 tales would show a collapse but not a moderate drop, and 20 cost a third more for little gain. A paired comparison on the same tales should be tighter than these ranges.

**Why these two corpora.** The wondertales are where the order is expected, and where the readers' strings can be set against his. The East Asian tales have the strong result that most needs checking. `LeafReport.md` gave 0.96 and 0.95 by the order tool on 16 functions; the simple measure gives 0.74 and 0.60 on about 20. Both are carried forward, and the higher figures should not be leaned on.

## 4. What is measured

**Primary: mean-position tau with Propp's numbering,** no preparatory units, functions in at least 3 stories, per corpus, reader and cell. It is chosen over the tool because its noise is measured and it needs no fitting at this size.

**The comparison:** the difference H minus S, per corpus and reader, on the functions both cells have, with a 90% interval by 2,000 paired bootstrap draws of tales.

**Beside it, not deciding:**
- The same with preparatory units, as they may float.
- `grammar.py` version 3's verdict and order tau, with the warning that 15 stories is below its tested 20.
- Adjacent pairs of his found, as `Leaf-L2` and the audit counted them.

**Whether the coding held up** (needed to read a drop at all):
- Agreement of A and B within each cell (kappa).
- The share of events given a function.
- For the wondertales, each tale's bag of functions against his strings (cosine), which needs no order.

## 5. How it will be read, fixed now

Per corpus, for both readers:

| Reading | Rule |
|---|---|
| **The order survives** | S's tau is at least 0.5 and within 0.10 of H's |
| **The card writes it in** | H minus S is at least 0.30, and its interval excludes 0 |
| **In part** | Anything between; the size is reported, and neither is claimed |
| **Unreadable** | S's kappa falls more than 0.10 below H's, or its cosine with his strings falls more than 0.10: the coding got worse, and a drop could be that alone |

Corpora may differ, and readers may split: each is reported as it falls.

**What follows** (for the owner to decide then, not bound here):
- **Survives:** the functions' order is not the card's, and the work goes up to pairs, with more confidence in the old strings.
- **Written in:** the old strings cannot be used for order. The cards are redone, with collection again as the owner has offered, and the 13 programs named in `Induction/AuditReport.md` are reread.
- **In part:** a larger S collection before going up.

**A limit in advance:** survival does not rule out priming from what the readers already know. Against it stands one earlier result: on near the same card the tragedies come out at tau about 0.2, so a card does not by itself impose his order.

## 6. Tests

**Before any reader runs:**
- The S rules' symbols map one to one onto H's, and a tale coded by hand in H's symbols maps to S's and back unchanged.
- No S file holds "Propp", a page reference, or any of his symbols outside its code.
- The measure on planted strings gives the planted tau; shuffled strings give about 0; the bootstrap covers a planted difference.
- Two runs are byte-identical.

## 7. Decisions for the owner

1. **Two cells, H and S.** Recommended. S alone would cost half, but could not tell a card effect from a run effect.
2. **15 tales in each corpus.** Recommended, on the table above. 10 would save a third and could show only a collapse.
3. **The reading rule's numbers (0.5, 0.10, 0.30).** Recommended as written. They are the keeper's judgment from the noise table, and set before any new string.
4. **A new neutral repository for cell S.** Recommended, as the name Propp-ActsRoles would tell a reader what the card hides. It needs a new private remote, created at the owner's word.
5. **In parts.** Recommended: the wondertales' H and S first, then the East Asian tales, so the budget can be watched and the second part dropped if the first is plain.
6. **Its place.** Recommended: ahead of step 6 and of pairs.

## 8. Order of work and cost

1. The owner's review and decisions; this file frozen.
2. The S rules, the key, the draw, the prompts, the measure and the tests; the owner reads the S card.
3. Part 1, then part 2, at the owner's word.
4. The strings committed; the key applied; the measure run; the report.

**Cost:** readers, unlike the last several steps. 30 tales, in 2 cells, by 2 readers, is 120 tale codings, in 8 subagents of up to 15 tales. Earlier, one arm of 45 tales by 2 readers was 90 tale codings, in 6 subagents, so this is about 1.3 arms of that kind, on tales of about the same mix of lengths. No relisting. The keeper has found no record of an arm's share of the weekly budget, so part 1 (60 codings, 4 subagents, about two thirds of an arm) would also give the first real measure.
