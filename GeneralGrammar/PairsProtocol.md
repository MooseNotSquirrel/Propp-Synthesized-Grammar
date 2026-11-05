# Up the tree: pairs, with the distance between them: protocol (FROZEN 2026-11-04 AT THE OWNER'S WORD, THE SIX RECOMMENDED DECISIONS TAKEN; nothing run)

**Asked by the owner on 2026-11-04,** as the next step of the climb: leaves, then pairs with the distance between them, then groups, with order inferred and allowed to float. The target is a tree of the kind V46 presents, inferred per corpus (`LeafProtocol.md` section 8).

**Why it can go ahead.** The leaf test's "reasonable answer" was not met, and functions cannot yet be recovered without labels. But the labels' order has now survived a neutral card and coding apart, and the same test says no on the tragedies (`CardPilotReport.md`, `ShuffledReport.md`). So pairs are built on the function labels, with that limit stated.

**What it does not change.** No earlier verdict, table or string. No reader is used.

**Not blind.** The keeper knows that adjacent statistics found 6 of 9 of his pairs on the readers' strings (`Induction/Audit-u4.txt`), and that `grammar.py` found 7 of 9 on his own strings (`Rung2-v3.txt`).

## 1. What a pair is here

A **pair** is an ordered link between two symbols, x then y, of any of three kinds. Earlier tools could see only the first, so A and K were out of reach by construction.

| Kind | What it looks like | Where his would stand |
|---|---|---|
| **Tight** | y follows x at once | D-E, Pr-Rs, M-N |
| **Near** | y follows within a few places | Possibly H-I, γ-δ, where others intervene |
| **Spanning** | y follows x at a distance, and no closer than chance, but x comes before y far more than chance | A-K: a harm and its repair, with a tale between them |

**Passes are not given.** The strings are whole stories, without the moves. So a spanning pair must show itself across a story with several passes.

## 2. The measure

For stories of one reader, X left out, every ordered pair with both symbols in at least 5 stories:

- **Distance:** from each x, the places to the next y. Its whole distribution is reported, and its median.
- **Closeness:** the mean of that distance, against 2,000 shuffles within each story, which keep each story's contents.
- **Direction:** of all x and y in a story, the share with x before y, against the same shuffles.
- **Bound:** given x, how often a y follows in the story; given y, how often an x stands before it. This shows whether one calls for the other.

**Kinds, by a rule fixed here:**
- **Tight:** the closeness passes, and the commonest distance is 1.
- **Near:** the closeness passes, and the commonest distance is 2 to 4.
- **Spanning:** the direction passes, the closeness does not, and the bound either way is at least 0.5.

**Multiple tests:** false discovery rate of 0.05 over all the pairs of a corpus and reader.

**Found and confirmed.** Found on the induction half of `Induction/Split.txt`, and confirmed only if the same kind of link passes at p at most 0.05 on the checking half. His own strings are not in the split's readers, and take the same split.

**One tool, knowing no one.** `GeneralGrammar/pairs.py` imports nothing that holds Propp. Renaming symbols gives the same pairs, name for name. `score.py` alone holds his pairs.

## 3. The rungs

**Rung 0.** Hand-worked distances; renaming; byte-identical runs; a source check as in `test_rung0.py`.

**Rung 1. Generated strings, with no real string read.** `generators.py`'s G1, G2, G4, G5, G7 and G8, and one added: **G9,** G8 with spanning pairs planted (an opening function calls for a closing one far along, at 0.8), so that the tool's reach is tried. At 45 stories, 20 corpora for G8, G9 and G2, 10 for the others.

Rung 1 passes when:
- **G9:** at least 80% of the planted spanning pairs are found, in at least 80% of corpora.
- **G2:** the pairs found are the relabelled ones, and at most 5% of corpora reach the bars scored against Propp's pairs.
- **G7:** at most 5% of candidate pairs are called pairs, on average.
- **G4:** the pairs inside episodes are found, and none is called spanning across episodes in more than 5% of pairs on average.

**The bars for rung 2 and after** are each kind's recall at G9's 10th percentile, as with G8 at the last climb. If rung 1 fails, the tool is revised as a numbered version and no real string is read.

**Rung 2. His 45 strings.** Recall of his twelve pairs (`PROPP_PAIRS`), and of the nine of `constraintGrammar.PAIRS`, by kind. A-K and a-K are scored as spanning. Also: the pairs found that are not his, listed in full.

**Rung 3. The readers' wondertales,** A and B. The same scores. **Replication:** the pairs both readers confirm, and the correlation of median distances. Preparatory pairs stand here, as his strings have none.

**Rung 4. The other corpora and the acts,** each its own: animal tales, fables, tragedies, myths, Native American, East Asian. Which pairs replicate between readers, in which corpora; which of his hold and which do not; which are new and shared by several corpora. The act strings are run alike, since those were not read under his card.

A pair confirmed by both readers in at least three corpora, and not his, is listed as **a candidate pair.**

## 4. Order among the pairs

For each corpus, each pair replicating between readers is treated as a unit, placed by the mean relative place of its two ends:
- **The order of pairs:** Kendall tau with his numbering, by reader, on the wondertales and on each corpus.
- **Does it float?** For two pairs, how often one stands wholly before the other, overlaps it, or follows it, across stories. Pairs that overlap or swap often are reported as floating. Trickery's pair is one to watch.
- **Nesting:** whether tight pairs stand inside spanning ones (γ-δ inside A-K?) more than the shuffles allow. This is the first evidence of tree structure, and leads to the next step.

Groups themselves are not built here. They are the next rung of the climb.

## 5. Predictions, recommended

- **P1, from Propp:** on his strings, recall of his pairs reaches the bars, spanning included.
- **P2, the keeper's expectation, *not from Propp*:** on the readers' wondertales, at least half of his pairs are confirmed by both readers.
- **P3, the keeper's expectation, *not from Propp*:** fewer of his pairs replicate in the tragedies than in the wondertales.

## 6. Limits

- **Labels:** every pair rests on readers' labels, read with knowledge of his functions. A pair's two functions may also be read as a pair because their definitions refer to each other (the violation of an interdiction). **So a function pair defined by its partner is weaker evidence than one that is not,** and the acts layer is the check.
- **Size:** 5 stories is little, and small corpora will find few pairs. Rung 1 only says how the tool does at 45.
- **The move rule and content labelling** remain in these strings.

## 7. Decisions for the owner

**Taken 2026-11-04: the owner accepted all six recommendations.**

1. **Three kinds, by the rule in section 2.** Recommended.
2. **Whole stories, no move labels.** Recommended, as in the general grammar. Pairs within moves reported beside, for the corpora that have them.
3. **Bars from G9.** Recommended, by the course you chose for G8.
4. **The three predictions.** Recommended.
5. **The acts layer run alike.** Recommended, as the check on labels.
6. **Stop at nesting.** Recommended: groups come next, under their own protocol, once this shows whether there is structure to group.

## 8. Order of work and cost

1. The owner's decisions; this file frozen (done 2026-11-04).
2. `pairs.py`, G9, rung 0; committed.
3. Rung 1, reported to the owner before any real string is read.
4. Rungs 2 to 4 and section 4, then the report.

**Cost:** no readers; computing here and this session's work. The keeper has no reliable estimate of what a session's work costs, beyond your figures so far: about 3 points for drafting and setup.
