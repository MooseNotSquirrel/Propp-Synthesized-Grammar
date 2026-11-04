# How the stories are built, and the story grammar's controls: protocol (FROZEN 2026-11-04 AT THE OWNER'S WORD, THE SIX RECOMMENDED DECISIONS TAKEN; nothing built or run)

**Asked by the owner on 2026-11-02** (the order of work, step 6). Two parts, no readers:
- **Part A,** the rest of ProppQueue.md item (s): move architecture, predictability, openings and endings, and families of tales.
- **Part B,** item (q)'s two controls and its composition features, all on the existing transcriptions under card C. Card D and the story grammar's version 2 remain step 7.

**What it does not change.** No earlier verdict is rescored, no table is rebuilt, and the frozen grammar's weights are not touched. The grammar-induction tool is not used: its self-test failed (`Induction/Checked-functions-tale.txt`).

**The caution that goes with every figure:** the readers are modern models reading translations, and the moves and functions are theirs.

## 1. The stories

- **Function strings:** `Induction/strings.py`, the seven corpora, stories of at least three units.
- **Act strings:** the same module, the six corpora with acts.
- **Halves:** where a measure is fitted, `Induction/Split.txt` (already committed): fit on the induction half, score on the checking half. Those halves have been read by the induction, so they are not unseen by the keeper; nothing here is tuned to them.
- **Readers:** every figure per transcriber, A and B, and their agreement reported.
- **Tests:** comparisons between corpora are permutations of the corpus labels over stories, 10,000 times, a fixed seed, two-sided, at p at most 0.05 with at least 10 stories a side. They are many, so a lone p near 0.05 is reported and not read.

## PART A. How the stories are built

## 2. Move architecture

From the functions table's move labels, which are the transcribers' own.

**A1. Moves per story.** The mean and distribution per corpus, with units per move.

**A2. Sequence or nesting.** A story *nests* when a move resumes after another has begun (I, II, I, in the order of the rows). The share of readings that nest per corpus, and how far the transcribers agree story by story. The rows' brace and bracket marks are rare (under 200 rows) and are counted beside it.

**A3. Trebling.** Two moves are *alike* when the normalized edit distance of their function strings is at most 0.34. A story *trebles* when it has three consecutive alike moves, and *repeats* when it has two. The null shuffles the moves among the corpus's stories, keeping each story's number of moves, 1,000 times: how often the same count of alike neighbours arises by chance.

**A4. Episodic stringing.** For consecutive moves, whether they share a performer, by the names of `common.same`. A story is *strung* when it has at least three moves and fewer than half its consecutive pairs share one. The same null as A3. The Russian tales' names are compared within the function layer's names, which are English.

## 3. Predictability

**B1. One number for how formulaic a tradition is.** A bigram model of each corpus's strings, fitted on the induction half and scored on the checking half:
- **Interpolation:** next-symbol probability = λ bigram + (1 − λ) unigram, with λ set by five-fold cross-validation inside the induction half, because an unsmoothed bigram loses to the unigram on small corpora (`Checked-*.txt`).
- **The number:** bits per symbol saved over the unigram.
- **Beside it:** top-one accuracy against always guessing the commonest symbol.

**B2. Made comparable.** Corpora differ in size and alphabet, so each is also fitted on a common training size: the smallest induction half's symbol count, by 200 random draws of whole stories, and the mean reported. Each move's end is a symbol, as in the induction.

**B3. Null.** The checking half's strings shuffled within the move, 1,000 times: the saving that composition alone would give.

**B4. Corpora compared.** By the permutation test above on per-story savings, per layer.

## 4. Openings and endings

**C1. Openings and endings by function and act.** For each corpus, the distribution of a story's first and last unit, and the first and last three.
- **The measures:** the commonest item's share, the entropy, and the total-variation distance between corpora, by the permutation test.
- **Null for position:** whether an item stands at the opening or close more than its overall share allows, by shuffles within the story.

**C2. The etiological close.** Propp's scheme has no place for it.
- **The rule, fixed here:** a story closes etiologically when one of its last two listed events (`Data/tables/events.tsv`, in English for every corpus) matches, ignoring case:
  `ever since | since then | to this day | that is why | this is why | that is how | this is how | from that (day|time) | to the present | until now | is (now )?called | are (now )?called | is named | are named | names? (it|them|him|her) | became the | gives? .* name | origin of | hence`
- **Its check:** the keeper reads every match in the sampled 50 (a fixed seed) and a sample of 50 non-matches and reports the rule's precision and misses. The rule is not changed after that reading; a mended rule would be reported beside it.
- **Beside it:** the share of stories whose lister recorded a moral (the Heroes lists' moral field). The rule reads the lister's paraphrase, not the teller's words, so a formula may be lost.

**C3. Closing fortune.** Reported from `StoryModels/Arcs.txt`, not recomputed.

## 5. Families of tales

**D1. Distance.** Between every two stories of a layer, within one transcriber, the Levenshtein distance of their whole strings (moves joined; the first version), over the longer length.

**D2. Replication.** A Mantel test of A's distances against B's (10,000 permutations of the stories).

**D3. By culture or by genre.** Corpora are labelled two ways:
- **Culture:** Russian (wondertales, animal tales); Greek and Latin (fables, tragedies, myths); Native American; East Asian.
- **Genre:** each corpus its own.

The mean distance is taken over three kinds of pair: within a corpus; between corpora of one culture; between cultures. The statistics are the differences of those means, by permutation of the labels over stories. So: a same-culture pair closer than a different-culture pair, with genre differing in both, is the culture signal. Within-corpus against same-culture is the genre signal.

**D4. Controls.** Length alone separates fables from tragedies, so:
- **Length:** a partial Mantel test, with the absolute difference of log length partialled out.
- **Order or contents:** the same statistics on strings shuffled within each story. What survives is composition, not order.

**D5. Families.** Average-linkage clustering, k from 2 to 20 by the mean silhouette, against the same statistic on the D4 shuffles. Clusters are reported with their corpus make-up and the adjusted Rand index against culture and against genre, by permutation; only if they beat the shuffles are they called families.

## PART B. The story grammar's controls and composition

## 6. The two controls

Their reason: the frozen grammar's stories outscore their shuffles in every corpus, but that does not show the order is Propp's rather than narrative order in general.

**E1. Propp's plain numerical order.** A story's score is the share of its within-move pairs out of `tragedyScore.NUM` order. No weights, nothing fitted. It is scored against the same 200 alternatives `storyGrammar.py run` drew, on the same held-out stories, and set beside the record's concordance by a paired sign-flip test per corpus and transcriber.

**E2. Scrambled sections.**
- **The scramble:** the functions are assigned to ten sections at random, with the true sections' sizes, 200 times (a fixed seed).
- **The fit:** for each, the 45 section-order weights alone, shared plus corpus offsets, are refitted by `storyGrammar.py`'s engine on the fitting stories (`StoryGrammar/HeldOut.txt`'s complement).
- **The real one:** the true sections fitted the same way, section orders alone.
- **The score:** the held-out concordance under each.
- **Why refit:** any grouping of the functions, fitted, may capture narrative order. The control measures how much better Propp's grouping does.

**The new corpora:** E1 on all their stories; E2's weights, fitted on the five, scored on all their stories.

## 7. Composition

**F1. Each section's share of a story** (`StoryGrammar/composition.py`'s measure, per story).

**F2. Does composition name the corpus?** A multinomial logistic classifier of the seven corpora, fitted on the induction half and scored by balanced accuracy on the checking half:
- on the ten shares alone;
- on length alone (units and moves), the control that beat the grammar in prediction 2 (0.539 against 0.363 on five corpora);
- on both.

Compared by a permutation test (the labels of the checking half, 10,000 times) and by a paired test of shares-and-length against length. The L2 penalty is 1.0, as the story grammar's.

**F3. What is not done here:** composition features are not added to the frozen grammar, which stays as it is. They go into version 2, at step 7.

## 8. Tests, before any figure is read

- **X1. Planted structure.**
  - **A2:** planted resumed moves are found.
  - **A3:** a planted treble is found, and shuffled moves give about the null's rate.
  - **A4:** planted shared performers are counted.
- **X2. Predictability.** A planted first-order chain gives its known saving within 10%; an order-free string gives about zero; B3's null covers zero on shuffled strings.
- **X3. The close rule.** Fixed sentences written first (matching and not) are classed as written.
- **X4. Families.**
  - **D1:** hand-worked distances agree.
  - **D2:** a matrix against itself gives a Mantel r of 1; a shuffled one, about 0.
  - **D3:** planted cultures are found.
  - **D5:** random strings are not called families.
- **X5. The controls.**
  - **E1:** a story in NUM order scores no violation, and its reverse scores all.
  - **E2:** the true sections' assignment passed as a "scramble" gives the real figure, and each scramble keeps the sizes.
  - **The record:** `storyGrammar.py`'s alternatives are reproduced draw for draw.
- **X6. Composition.** Shares sum to 1; planted corpora of different composition are named; label-shuffled data give chance.
- **T.** Two runs byte-identical.

## 9. Decisions for the owner

**Taken 2026-11-04: the owner accepted all six recommendations.** The three predictions of decision 1 are now frozen. The keeper had seen three random closing events per corpus and a total count of resumed moves before this file was frozen, and said so to the owner; the close prediction is not fully blind.

1. **Reported only, or with predictions.** Recommended: Part A reported only, and three predictions frozen, the three questions these models exist to ask:
   - *E2: in the wondertales, the true sections' held-out concordance is above at least 95% of the scrambles,* per transcriber (HOLDS, SPLIT or FAILS). If it fails, the backbone cannot be called Propp's in particular. This follows from Propp's sections being his claim about the wondertale.
   - *F2: shares and length together name the corpus better than length alone,* by the paired test, p at most 0.05, per transcriber. The keeper's expectation, *not from Propp*, from `Composition.txt`.
   - *C2: the etiological close is more common in the Native American tales than in the wondertales,* by the permutation test, per transcriber. The keeper's expectation, *not from Propp*, which item (s) prompted.
2. **The alike threshold (A3):** 0.34, about one function in three differing (recommended), or another.
3. **Predictability's fairness:** the common training size reported beside the full fit (recommended), or the full fit alone.
4. **The close rule:** as written, read once and not changed (recommended), or a reader stage to judge the closes, which would cost budget and belongs later.
5. **The culture labels:** the four of D3 (recommended). The Greek and Latin group joins fables, tragedies and myths; another grouping can be named. Native American and East Asian are large areas, not single cultures, and their figures should be read so.
6. **The scrambles:** 200 (recommended), or fewer if the fits prove slow.

## 10. Order of work, and the cost

1. The owner's review and decisions; this file frozen (done 2026-11-04).
2. **The programs,** `StoryModels/architecture.py`, `predictability.py`, `openings.py` and `families.py`, and `StoryGrammar/controls.py`, written and committed, and X1 to X6 and T passed, before any figure is read.
3. **The run,** at the owner's word, in parts if the owner wishes: Part A's four, then Part B.

**The cost:** no readers. Part A takes minutes. E2's 200 refits are the largest piece, likely under an hour.
