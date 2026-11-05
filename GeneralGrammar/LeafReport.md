# The leaves: report (2026-11-04)

The protocol is `LeafProtocol.md`; the figures are in `Leaf-ceil.txt`, `Leaf-L1.txt`, `Leaf-clusters.txt`, `Leaf-L2.txt`, `Leaf-L3.txt`, `Leaf-L3-samples.txt` and `Leaf-L4.txt`, from `leaves.py`.

**The verdict by the frozen rule: "a reasonable answer" is NOT met.** So, by section 7, the next step is the cards, not the hierarchy.

**Departures, and errors, on record:**
- **Two false starts.** The first run left out the `problems` study, and so about half of the tales, plays and fables. The commit that called a rerun "on every story" was wrong, as a stale cache kept the old data (corrected at c37aaab). These figures are from the true rerun (f10f3a6 for the clusters). P2 failed on the half data and holds on all of it. No choice was changed between them.
- **VerbNet left out.** Its package shows no license, so the protocol's condition is not met. Moby and WordNet ran.
- **Clusters and labels.** The clusters were committed before being scored, but after L1 and the first run had shown labels and figures. They read no label in the making.

## The ceilings

Each reader's label as a prediction of the other's.

| Corpus | Events | Hit | Macro F1 | Kappa | Given a function | Agreed where both give one |
|---|---|---|---|---|---|---|
| Wondertales | 1632 | 0.70 | 0.69 | 0.62 | 67% | 75% |
| Animal tales | 1282 | 0.78 | 0.57 | 0.71 | 57% | 86% |
| Fables | 432 | 0.75 | 0.63 | 0.67 | 58% | 78% |
| Tragedies | 3243 | 0.75 | 0.57 | 0.62 | 46% | 81% |
| Native American | 1795 | 0.78 | 0.67 | 0.66 | 47% | 80% |
| East Asian | 1054 | 0.79 | 0.62 | 0.70 | 52% | 85% |

**Against Propp, tale by tale** (no X, no preparatory units): cosine 0.72 and 0.70 with the same tale, 0.49 and 0.51 with another.

## L1: what tells the function

Wondertales, macro F1 as a share of the ceiling, reader A and B.

| Evidence | A | B |
|---|---|---|
| Commonest class | 2% | 2% |
| Verb | 20% | 19% |
| WordNet classes alone | 17% | 18% |
| Moby classes alone | 17% | 19% |
| Act alone | 40% | 43% |
| Verb and act | 46% | 48% |
| + relation | 53% | 52% |
| **+ significance** | **63%** | **59%** |
| + neighbours | 54% | 51% |
| + place | 56% | 50% |

**Every other corpus has the same pattern, with significance the peak:** animal tales 58%, 42%; tragedies 40%, 37%; Native American 42%, 33%; East Asian 36%, 37%; fables 29%, 20%.

**Predictions, all HOLD:**
- **P1,** the verb under half the ceiling: 20%, 19%.
- **P2,** significance and neighbours beat the act, by hit: p 0.011, 0.004. Significance alone gave the peak; neighbours lowered it, at this size.
- **P3,** no thesaurus beats the act. **The thesaurus was not the main trouble.** Grouping verbs by either dictionary does no better than the raw verb, and much worse than the act.

**By function** (F1 with significance, A, B). Named well: W 0.78, 0.81; A 0.74, 0.71; I 0.71, 0.79; η 0.59, 0.70; down 0.68, 0.51. Named badly: ε 0.07, 0.06; B 0.23, 0.21; a 0.34, 0.37; Rs 0.33, 0.26; C 0.38, 0.36.

**Transfer,** fitted on the wondertales, as a share of the target's ceiling: animal tales 47%, East Asian 38%, fables 37%, Native American 36%, tragedies 33%. From the others to the wondertales: 50%.

## L2: without the labels

Adjusted mutual information with the functions, wondertales, k of 32:

| Alphabet | AMI A, B | Shuffles' 95th |
|---|---|---|
| Verb as written | 0.10, 0.09 | 0.01 |
| WordNet | 0.09, 0.09 | 0.01 |
| Moby | 0.08, 0.10 | 0.01 |
| **Act as coded** | **0.24, 0.24** | 0.01 |
| Act, relation, significance | 0.19, 0.21 | 0.01 |
| The same with neighbours | 0.18, 0.21 | 0.01 |

All beat the shuffles and replicate between readers, modestly (ARI 0.18 to 0.34 for act-based clusters). **The clustering does not recover the functions:** an AMI of about 0.2 is real but small. The context that helped the supervised model did not help the clusters. No cluster set was better than the act list itself.

**Against his strings** (the readers' own bags 0.74, 0.72): act clusters at the chosen k 0.53, 0.49; act, relation and significance at k 96, 0.43, 0.51; WordNet 0.43, 0.46; Moby 0.47, 0.41.

## The reasonable answer

| Part | Result | |
|---|---|---|
| Best of F2 to F5 reaches 80% of the ceiling, both readers | 63%, 59% | **Not met** |
| Clusters beat the shuffles and replicate | Yes | Met |
| Clusters at least half as close to his strings as the readers' own bags | k 96: 0.58, 0.71. k 32: 0.48, 0.61 | Met at the chosen k, not at k 32 |

The 80% was the keeper's judgment. By hit rate the same models reach 84% and 76%, but that measure has a high floor from X.

## The owner's 80% (speculation, reported three ways, no verdict)

| Corpus | Covered | Agreed | Transferred |
|---|---|---|---|
| Wondertales | 67% | 75% | 50% |
| Animal tales | 57% | 86% | 47% |
| Fables | 58% | 78% | 37% |
| Tragedies | 46% | 81% | 33% |
| Native American | 47% | 80% | 36% |
| East Asian | 52% | 85% | 38% |

**The "agreed" column stands at about 80% in all six.** Where both readers apply a function, they usually apply the same one. Agreement is not correctness, and both read the same card. The coverage is the gap: about half of events outside the wondertales receive no function.

## L3: leaves his list may lack

Clustered on acts, relation and significance, with verbs not among the features. Reading the samples is the keeper's judgment.

**Tragedies: the clear result.** 24 clusters replicate, and the verbs inside them, not used to make them, name:
- **Threats** (threaten: two clusters).
- **Curses** (curse: two clusters, with some strays).
- **Prayer and invocation** (pray).
- **Begging and supplication** (ask, beg, urge).
- **Lament** (mourn).
- **Vows and promises** (promise, vow, swear).
- **Foretelling and reports** (foretell, tell).
- **Arrival and return,** **orders,** **sending and summoning,** **plans and decisions.**
- **Three mixed clusters of the act `other`** (birth and descent, staging, gods and events).

**These are very largely candidates already on the record.** Threats is the one X-study candidate that held. Oath, prayer and curse are the `Cand` study's. Begging, sending and arriving were X-study candidates that took Propp's events. They were found again here without being looked for, from events his alphabet left unnamed, by two readers.

**Native American:** going off and camping; coming home; repeated tries that fail; a mixed deception cluster. **East Asian:** two mixed `other` clusters (scenes, growth, names); sending; finding. **Animal tales:** getting and eating. **Wondertales:** two only, harms left X and finding a lodging. **Fables:** none, at this size.

**Outside tragedy these look less like new functions than like narrative connective tissue,** though that is a reading of samples and not a test.

## L4: does an alphabet carry structure?

| Corpus | Functions: verdict A, B | Order tau A with B | Order tau with Propp, no preparatory, A, B | Acts: verdict A, B |
|---|---|---|---|---|
| Wondertales | bigram, ordered passes | 0.79 | 0.76, 0.79 | unigram, unigram |
| East Asian | bigram, bigram | 0.87 | **0.96, 0.95** | unigram, unigram |
| Fables | bigram, bigram | 0.51 | 0.70, 0.70 | bigram, bigram |
| Native American | bigram, bigram | 0.57 | 0.45, 0.73 | unigram, unigram |
| Animal tales | bigram, bigram | 0.12 | 0.73, 0.11 | bigram, HMM |
| Tragedies | HMM, HMM | 0.46 | 0.01, −0.26 | unigram, HMM |

- **In the wondertales the readers' functions come close to his order.** Order floats: η θ and ε ζ stand after the villainy in both readers, as the owner said.
- **The corpora differ, as the owner expected.** The tragedies have no Propp order, and their readers barely agree. The East Asian tales have a very strong one.
- **The acts carry almost no sequence, in any corpus, the wondertales included.** Nor do the clusters built on them.
- **So the order lives in the function labels, not in the acts. This has two readings the data cannot separate:** functions are what carries a tale's structure, and acts are too low a level; or the readers, holding a card that lists functions in his order, write his order in. The East Asian figure of 0.96 needs this caution most.

The tool has so far been shown only on generated strings and his own, so all of L4 is exploratory.

## What this says

1. **A function is not a verb, and not an act.** The verb gives a fifth of what a second reader gives. Significance adds most. Propp's definition of a function by its significance for the action has support here.
2. **A better thesaurus will not fix it.**
3. **Functions cannot yet be recovered blind.** With the labels to learn from, about 60% of the ceiling; without them, little.
4. **The candidates are real in tragedy,** and found from below.
5. **The most important open question is priming,** and strings alone cannot answer it. It takes data collected differently.

## Corrections, 2026-11-04, after this report

- **The event lists.** `LeafProtocol.md` and the keeper's account said the lists came from listers whose rules held Propp's card. That is so of the earlier fables and plays. The East Asian listers' rules do not name him (`ActsRoles/eastasian/ListRules.md`), and the wondertale listers' file named him in its first lines, with a prompt saying his functions played no part and not to read as far as the card.
- **The East Asian order.** The 0.96 and 0.95 above are from the order tool on 16 functions. The simple mean-position measure on about 20 functions gives 0.74 and 0.60 (`PilotNoise.txt`). The wondertales are steadier: 0.76, 0.79 by the tool, 0.78, 0.77 by mean position. "Very strong" overstates the East Asian result.
