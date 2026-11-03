# The hero's fortune arc and the character networks: protocol (FROZEN 2026-11-03 AT THE OWNER'S WORD, THE FIVE RECOMMENDED DECISIONS TAKEN; nothing built or run)

**Asked by the owner on 2026-11-02** (ProppQueue.md item (s), 1 and 2; the order of work, step 4). Two models built on data already collected, with no readers:
- the hero's fortune over a story, act by act;
- the web of who acts on whom.

Neither model assumes Propp's functions. Both are read from the act and significance layers, which were not built on his card.

**What it does not change.** No earlier verdict is rescored, and no table is rebuilt. The figures are reported beside the story grammar's, not in place of them.

## 1. The stories and the layers

**Which corpora.** These six corpora have the acts, significance and a hero for every story they describe (`Data/Coverage.txt`, step 3):

| Corpus | Stories |
|---|---|
| wondertales (Afanasyev) | 45 |
| animal tales | 50 |
| Fables | 90 |
| tragedies | 32 |
| Native American | 50 |
| East Asian | 50 |

**Which are left out.** The myths and Aesop have no acts or significance, so they are left out. They are named in every report as left out, not as failing.

**All the stories are used.** Nothing here is fitted, so there is nothing to hold out.

**Each describer apart.** Acts and significance are read per describer, A (Opus) and B (Sonnet). Every figure is given for A and B separately, and their agreement is reported.

**Whose fortune.** The significance layer's value is the act's value *for the hero named in its input*, the event lister's hero (`SigRules.md`). So the arc is that hero's.
- The heroes stage's readers sometimes name another hero, or none. Those stories are kept.
- The figures are also reported on the stories where both heroes-stage readers name the lister's hero. This is a check, not a filter (decision 3).

## 2. The fortune arc

**F1. The arc.**
- **Each act is scored:** helps +1, harms −1, neither 0, in the order of the story's events (and, within an event, in the order of its entries).
- **The arc** is the running sum, on a time axis from 0 (the first act) to 1 (the last).
- **Resampling:** each arc is resampled to 20 points by linear interpolation, and divided by the story's number of scored acts. Arcs of long and short stories then compare by shape, not by length.
- **Exclusion:** stories with fewer than 6 scored acts are left out of F2 to F4, and their number is reported.

**F2. The shape, by a fixed rule.** The arc is cut into halves.
- **The halves:** d1 is its net change over the first half, d2 over the second.
- **Each half's sign** is +, − or 0, counted as 0 when its net change is within one act (|d| < 1 / n, n the story's scored acts).

| Shape | Signs (d1, d2) |
|---|---|
| **rise** | (+, +), (0, +), (+, 0) |
| **fall** | (−, −), (0, −), (−, 0) |
| **fall then rise** | (−, +) |
| **rise then fall** | (+, −) |
| **flat** | (0, 0) |
| **oscillation** | any of the above whose arc, after a three-point moving average, changes direction 4 or more times; this class takes precedence |

**F3. Shapes without a rule.**
- **The method:** k-means over the 20-point arcs of all corpora together, for k from 2 to 6. The k is chosen by the mean silhouette, and the seed is fixed.
- **Reporting:** each cluster's mean arc is drawn and named by the F2 shape most of its members take. A cluster whose largest F2 shape holds under half its members is named "mixed".
- **Purpose:** this shows whether the rule's classes are the data's own.

**F4. The corpora compared.** Each corpus's share of each F2 shape is reported.
- **Mean fortune at the end:** the arc's last point.
- **The depth of the lowest point,** and where it falls on the time axis.
- **The test:** shares are compared between corpora by a permutation of the corpus labels over stories (10,000 permutations, a fixed seed). The statistic is the total-variation distance between the two corpora's shape shares, at p at most 0.05 with at least 10 stories a side.

**F5. The problems' course.** The significance layer also gives each act's place in a problem: opens, worsens, serves, repairs, rewards, punishes or none.
- **The figures:** per corpus, the share of problems that are ever repaired, and the mean number of problems a story opens.
- **Where the first repair falls:** the point on the time axis.
- **Purpose:** this separates a story that ends low because its problem is never solved from one that ends low because a new harm comes at the end.

## 3. The character networks

**The network is built from the acts layer alone,** one per story and describer.
- **Nodes:** the acts' performers and undergoers. The names are normalized and split as `characters.py` does (its `head` key and `SplitRule.md`), and "none", "self" and empty names are dropped.
- **Edges:** from performer to undergoer, weighted by the number of acts, and labelled by act and relation.
- **Why not join to the functions' characters:** the networks do not need that join (`characters.tsv`). That join leaves half the East Asian act names unjoined (KeeperLog, 2026-11-03), and a network built on it would lose them. `characters.tsv` is used only to give a node its kind where its name joins (decision 4).

**The hero.** The hero's node is the one whose name joins the lister's hero, by the same key. Where none joins, the story is counted as "hero not found" and left out of N2 and N3, and the number is reported.

**N1. Centrality.**
- **The measure:** each node's weighted degree, in and out.
- **Per corpus:** the share of stories in which the hero is the most central character (ties counted as a half), and the hero's mean share of all the story's acts.

**N2. Agency.** Does the hero act or is the hero acted on?
- **The measure:** acts done ÷ (acts done + acts undergone), per story, and the corpus mean.
- **Against the significance layer:** the same figure from the layer's part field (does, undergoes, both). The two are reported side by side as a check.

**N3. Deception.**
- **The measure:** the share of a story's acts that are deceive, claim-falsely or be-taken-in.
- **The hero's side:** whether the hero is more often deceiver or deceived (the hero's share of deceive and claim-falsely acts done, against those undergone).
- **Per corpus:** the share of stories in which the hero deceives at least once.

**N4. One figure across a cycle.** Across a corpus's stories, the heads of each story's most central character are counted (Raven, Coyote, the fox and the like).
- **The concentration:** the share of stories held by the most common head, and the Herfindahl index of the heads.
- **What it shows:** a trickster culture would have one head holding many stories; the wondertales would have many heads.
- **The rule:** names are taken as their head only. Two Ravens of different tellers are one figure; a raven that is a different animal in another tale is not told apart. This is reported, not mended.

**N5. Size.** The figures given beside each measure, which a reader needs to judge it:
- nodes and edges per story;
- the density;
- the number of names the split and normalization dropped.

**N6. The corpora compared.** N1 to N3 are compared between corpora by the same permutation test as F4, on the per-story figures. Each test has the mean difference as its statistic.

## 4. Tests, before any figure is read

- **A1. The arc is what the layer says.** For 20 stories drawn by a fixed seed, the arc's steps equal the significance rows' values in event and entry order, counted by hand against the table and written to a sample file first.
- **A2. Planted shapes.** Ten arcs of each F2 shape, built by rule at three lengths (10, 30 and 80 acts), are classed as built, every one.
- **A3. Shuffled arcs.** The acts' values shuffled within each story make F3's clusters no tighter than real arcs. If its mean silhouette is not lower, F3 is reported as finding no shapes.
- **N-a. Planted networks.**
  - A star, in which one node is in every act, gives N1 = 1 and N4's head.
  - A ring gives no single centre.
  - Acts all done by the hero give N2 = 1.
- **N-b. Every name accounted for.** Every performer and undergoer of the acts rows read is either a node or counted as dropped, with its reason (as `characters.py` C1).
- **T. The same answer twice.** Two runs are byte-identical.

## 5. Decisions for the owner

**Taken 2026-11-03: the owner accepted all five recommendations.**
- Reported only, with one prediction, now frozen: *the wondertales' most common F2 shape is fall then rise*, tested per describer by a sign test of fall-then-rise against each other shape's count, at p at most 0.05.
- F2's halves and thresholds as written.
- All the stories, with the agreed-hero subset reported beside them.
- The networks' names from the acts layer alone.
- 6 scored acts the minimum for an arc.

1. **Reported only, or with predictions.**
   - **Recommended:** reported only (exploratory) for every corpus, with one prediction frozen before the program is written:
     - *the wondertales' most common F2 shape is fall then rise*;
     - tested per describer by a sign test of fall-then-rise against each other shape's count, at p at most 0.05.
   - **Where it comes from:** Propp's tale opens with a villainy or lack and ends with its liquidation and the wedding, so the hero's fortune falls and then rises.
   - **Other expectations are left as readings, not tests.** They are the keeper's speculation, *not from Propp*:
     - the tragedies falling at the end (from Aristotle, not Propp);
     - the trickster cycles oscillating.
2. **The shape rule:** F2's halves and thresholds as written (recommended), or thirds, which would tell rise then fall then rise apart but leave fewer acts in each part.
3. **The hero check:** all the stories, with the agreed-hero subset reported beside them (recommended), or the agreed-hero subset only.
4. **The network's names:** the acts layer alone (recommended), or joined to `characters.tsv`, which would bring the functions' characters in but lose the unjoined names.
5. **The minimum story:** 6 scored acts for an arc (recommended), or another floor.

## 6. Order of work, and the cost

1. The owner's review and decisions; this file frozen (done 2026-11-03).
2. **The program,** `StoryModels/arcs.py` and `StoryModels/networks.py`. Written and committed, with A1 to A3, N-a, N-b and T passed, before any figure is read.
3. **The run** on the six corpora, at the owner's word: `Arcs.txt` and `Networks.txt`, with the arcs' mean curves drawn per corpus.

**The cost:** no readers. The keeper's work and a few minutes of computing. The 20-story hand count in A1 is the largest piece of work.
