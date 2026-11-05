# The leaves: can a corpus's functions be retrieved from its verbs and acts? Protocol (FROZEN 2026-11-04 AT THE OWNER'S WORD, THE SIX RECOMMENDED DECISIONS TAKEN; nothing built or run)

**Asked by the owner on 2026-11-04.** Stepwise refinement begins with the largest and most basic item. Before any structure, can Propp's functions plus candidates be retrieved from a corpus, from its verbs and acts, with correlation shown? Then up the hierarchy.

**Where this stands in the larger aim.** V46 is at bottom a regular language, mostly, presented as a tree. A tree of that kind, inferred for each corpus, is what is sought (section 8). This protocol takes only its leaves.

**What it does not change.** Every earlier verdict and table stands. No reader is used.

**Caution:** the readers are modern models reading translations. The event lists came from listers whose rules held Propp's card, a limit on everything here. The events' boundaries are not independent of him, even where the descriptions are.

## 1. What is independent of what

| Layer | Read under | So |
|---|---|---|
| **Functions** | Propp's card | The labels to retrieve, and primed by him |
| **Acts** | `ActsRules.md`, which drops his functions; fresh and blind | Independent of the labels, except through the event list |
| **Free verbs** | No list at all; fresh and blind | The least primed of all |
| **Significance** (value, place, problem, link) | Its own rules, on the acts | Independent of the labels likewise |
| **His 45 strings** | Propp himself | The only yardstick not read through our card; by tale, not by event, with no preparatory units |

**The corpora:** the six with every layer: wondertales, animal tales, fables (the 90 of Fables), tragedies, Native American and East Asian. Aesop and the myths have no acts, free verbs or significance, and are left out here (`Data/Coverage.txt`).

**The base:** the functions of `tragedyScore.NUM`, X kept as a class. Candidates: the sixteen of `XStudy/Candidates.md` and oath, prayer and curse. These have coded strings only in the X study's test stories and in the acts layer, so they enter mainly through part L3 and the event-level comparison there.

## 2. The ceilings

Before anything else, what any retrieval could reach:
- **Reader agreement on the function, event by event,** A against B, per corpus, kappa and a hit rate. No feature can be expected to predict A's label better than B's own label does.
- **Tale by tale, against Propp:** each reader's bag of functions per tale against his, leaving out X and preparatory units.

## 3. L1. How much does each kind of evidence tell? (Supervised)

For each event, its features predict its function: a multinomial logistic model, L2 penalty 1.0, stories held out whole in five folds, per reader and per corpus. An event with several functions gives a row for each; a prediction is a hit if it is among them. An event's several acts or verbs are a bag.

**The ladder of features, each added to the one before:**

| Step | Adds | Asks |
|---|---|---|
| **F0** | Nothing: the commonest class | The floor |
| **F1** | The free verb | Is a function a verb? |
| **F2** | The act | Is it an act? |
| **F3** | The relation (kin, above, below, ally, stranger, enemy) | To whom? |
| **F4** | Significance: part, value, place, problem, link | What does it do for the story? |
| **F5** | The neighbouring events' acts and verbs, as a bag within two events either side, with no order | What stands near it? |
| **F6** | Relative place in the story | Only here does position enter. Reported apart, as it brings order in |

**Reported:** the hit rate, macro F1 and normalized mutual information at each step, each as a share of the ceiling, by paired tests over stories; and per function, which features name it best. Also F2 and F1 alone, without the ladder, across readers (A's features for B's labels), since A is Opus and B Sonnet.

**Transfer:** fitted on the wondertales, scored on each other corpus; and fitted on all the others, scored on the wondertales. Is a function the same thing elsewhere?

## 4. L2. Without the labels: clustering from the bottom up

**No function label is read until the clusters are committed.** The items are events, each by its features. Earlier work failed in two ways this must avoid: clustering by context gave one class of nearly every common verb (`Group/GroupRun.txt`), and WordNet's classes mixed several acts (`Group/WordNetRun.txt`).

**The alphabets compared:**
- **A.** The free verb as written.
- **B.** Verbs by thesaurus: WordNet's classes as `Group/wordnetGroup.py` makes them, and a second thesaurus (decision 2).
- **C.** The act as coded.
- **D.** Act plus F3 and F4.
- **E.** D plus the neighbours of F5.

**The clustering (B's thesaurus aside):** spherical k-means, 50 seeded starts, on scaled feature blocks, no block allowed to dominate. Number of clusters both fixed at the base's size (31 plus X) and chosen by held-out likelihood of a mixture. A cluster holding more than a third of the events marks the run as degenerate.

**The scores:**
- **Against the functions:** adjusted mutual information and V-measure, with shuffled labels within stories as the null, and precision by majority function per cluster, on held-out stories.
- **Replication:** the same clustering on A's and on B's descriptions, adjusted Rand index over events.
- **Against his strings:** clusters named by majority on half of the stories, then the other half's bags of named clusters against his tale by tale, beside the readers' own bags from section 2.

## 5. L3. Leaves his list may lack

The events the readers left X, per corpus, clustered as in L2.
- **Kept as a candidate leaf only if** it replicates between A and B and appears in at least ten stories.
- **Compared with** the sixteen X-study candidates and oath, prayer and curse, by the acts and verbs each holds.
- **The check on bias:** a new genre or culture may have leaves the base lacks. Clusters found only in one corpus are listed by corpus. The keeper reads a sample of 20 events per cluster and reports them, marked as the keeper's reading.

## 6. L4. The instrument: does an alphabet carry structure?

Each alphabet, as a string per story, goes to `grammar.py` version 3, unchanged:
- **The verdict and the coverage,** per corpus, reader by reader.
- **Whether A and B agree** on shape and order.
- **For the wondertales,** beside the readers' functions as an alphabet.

This judges a leaf without an answer key, which is the only judgment the other corpora allow. It is exploratory, as rung 3 is not yet run, and the tool has so far been shown only on generated strings and his own.

## 7. Predictions, tests and bars

**Predictions recommended (decision 1).** All per reader, on the wondertales, on held-out stories:
- **P1,** the keeper's expectation, *not from Propp*: the verb alone (F1) reaches less than half of the ceiling.
- **P2,** from Propp's definition of a function by its significance for the course of the action: adding significance and neighbours (F4, F5) beats the act alone (F2), paired over stories, p at most 0.05.
- **P3,** the keeper's expectation, *not from Propp*: no thesaurus's classes predict the function better than the act does. If this fails, the owner's suggestion that the thesaurus was the wrong one gains.

**The owner's speculation, marked as such:** that Propp's functions plus candidates are about 80% correct for nearly all corpora. "Correct" has no one meaning here, so three readings are reported per corpus, none as a verdict unless the owner names one (decision 3):
- **Covered:** the share of events given a function or candidate rather than X.
- **Agreed:** of events both readers cover, the share where they agree.
- **Transferred:** the wondertale model's hit rate on that corpus, as a share of its ceiling.

**"A reasonable answer," before moving up (decision 4).** Recommended: on the wondertales, for both readers, the best of F2 to F5 reaches at least 80% of the ceiling, the clusters of D or E beat the shuffles and replicate between readers, and they agree with his strings at least half as closely as the readers' own bags do. If not, the next step is the cards, not the hierarchy.

**Tests, before any figure is read:**
- Planted events with known functions and features give the planted ladder.
- Shuffled labels give chance.
- Degenerate clusters are flagged.
- A renaming of acts and verbs changes nothing.
- Two runs are byte-identical.

## 8. What this leads to: the tree (not in this protocol)

The target is a probabilistic, inferred version of what V46 is, for each corpus: leaves, then pairs with the distance between them, then groups, then a move, then a tale.
- **One rule:** each merge kept only if it raises held-out likelihood.
- **Order floats:** alternatives and floating items stand as V46 has them (its `FloatingT`, and `LeavingFirst` against `HelperFirst`).
- **The limit:** a regular language has many trees that accept the same strings. V46's tree was chosen with Propp's text beside it. Strings alone may not pick out one tree, so an inferred tree would be judged by its constituents against V46's named groups, by held-out prediction, and by the two readers' agreement, not by acceptance alone.
- **Acceptance:** with a tree, comparison with V46's 80 of 84 becomes direct.

## 9. Decisions for the owner

**Taken 2026-11-04: the owner accepted all six recommendations.**

1. **The three predictions.** Recommended: frozen as written.
2. **The second thesaurus.** Your question is whether the wrong one was chosen. Recommended: add the public-domain Moby Thesaurus, the alternative you were offered in October, downloaded at your word, and report VerbNet's classes too if its license allows.
3. **The 80%.** Recommended: reported three ways, none a verdict, until the figures can be seen.
4. **"A reasonable answer."** Recommended: as in section 7. The bars are the keeper's judgment, and are set before any figure is read.
5. **The corpora.** Recommended: the six above, the wondertales read first.
6. **Moving on.** Recommended: this comes ahead of rung 3 and the tree; rung 3 is left until the leaves have answered, though it takes a minute if you want it sooner.

## 10. Order of work and cost

1. The owner's review and decisions; this file frozen (done 2026-11-04).
2. The program `GeneralGrammar/leaves.py` and its tests, committed before anything is run.
3. Section 2 and L1, then L2, with the clusters committed before any label is read, then L3 and L4.

**Cost:** no readers. The keeper's estimate is minutes per part, unmeasured. If the cards prove wrong, recollecting the data is a separate decision, with its cost sized then.
