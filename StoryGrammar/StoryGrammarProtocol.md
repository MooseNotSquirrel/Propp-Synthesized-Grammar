# The probabilistic story grammar: protocol (DRAFT 2026-10-28, FOR THE OWNER'S REVIEW, NOT FROZEN)

**Drafted 2026-10-28 at the owner's word**, `ProppQueue.md` item (n), step 5 of the road, moved ahead of the cross-cultural analysis. It is to be built, fitted on the five existing corpora, and frozen before any Native American or East Asian transcription is read, so that those corpora remain an unseen test. Nothing here is built or fitted.

## 1. What it is

**The name** (item (n)): a *probabilistic story grammar*, in linguistics a maximum-entropy grammar, a grammar of weighted constraints. It is not "constraint grammar", which names an unrelated parsing method.

**What it joins:**
- the v46 grammar (`ProppEBNF46.txt`), which accepts or rejects a move;
- the soft grammar of weighted constraints (`Blocks/ConstraintGrammar.md`, frozen 2026-10-06), in which each of Propp's rules of order is a constraint a story may break at a cost, the cost learned from a genre's own stories;
- the joint model (`Model/`), which told the genres apart on unseen stories, and whose lesson is that length alone nearly does as well. Length must be in the model, not left to masquerade as structure.

**What it should do:**
- give any sequence of Propp's functions a score;
- give the genres their own weights, so that the weights are each genre's grammar;
- be tested, frozen, on stories it was not fitted on: first held-out stories of the existing corpora, then the unseen cultures.

## 2. The model (decision 1)

**Recommended, contrastive, as the constraint grammar was:** a story's function sequence is scored against alternatives built from the same functions. The alternatives are reorderings of its functions within each move, and the same with one function dropped or one added from the genre's own pool. The weights are fitted so that real stories outscore their alternatives, by conditional log-likelihood with an L2 penalty whose strength is fixed now.

The alternative is a generative model: the probability of the whole sequence, function by function. It is closer to "a grammar that writes stories", but needs far more data than 45 to 198 stories a corpus give.

## 3. The features, fixed now (decision 2)

Each feature is a constraint a story keeps or breaks, counted per move:
1. **The v46 grammar:** whether the move parses, and how many repairs the nearest parse needs.
2. **The order of sections:** the 45 section-order constraints of `constraintGrammar.py`, unchanged.
3. **The order inside sections:** as in `constraintGrammar.py`, unchanged.
4. **Propp's pairs in order:** each pair of `Ngrams/ngrams.py`, its second following its first in the move, as `CrossCulture/CrossCultureProtocol.md` section 8 defines it.
5. **The blocks:** each of Propp's blocks told together, by `blockStream.py`'s transform, as the parity runs counted them.
6. **The candidate groups** (`StoryGrammar/Candidates.md`): the threat group (threat or demand, then the answer, then the consequence) and the request group. These are included only as far as Propp's letters express them; otherwise they wait.
7. **Length, as a control:** the number of functions and of moves. Its weight is reported apart, and no structural claim may rest on it.

## 4. The weights (decision 3)

**Recommended: shared weights plus a genre offset for each feature.** One grammar for the story language, and each genre's departures from it, with the offsets penalised so that a genre departs only where its stories demand it.

The alternative is separate weights for each genre, which is simpler but cannot say what all the genres share.

The weights are fitted for each transcriber apart, as every earlier layer was.

## 5. The data and the held-out stories (decision 4)

- **Fitting:** the five corpora, every story with functions, per transcriber: wondertales 45, animal tales 50, fables 198, tragedies 32, myths 126.
- **Held out:** a fifth of each corpus's stories, drawn by a fixed seed and written to `StoryGrammar/HeldOut.txt` before any fit. They are never seen in fitting or in tuning.
- **The unseen cultures:** the Native American and East Asian tales, scored only after the grammar is frozen.

## 6. Tests and self-tests, before any fit is read

- **G1. A planted grammar recovered.** Function sequences are generated from known weights. The fit must recover their signs, and their order, with a rank correlation of at least 0.9.
- **G2. The frozen constraint grammar reproduced.** With only features 2 and 3, separate weights, and the 2026-10-06 data and settings, the program must reproduce the published weights (`Blocks/ConstraintWeights-*.txt`).
- **G3. The held-out stories untouched.** The fit is run with the held-out stories' functions replaced by noise, and must give the same weights. This shows that they were not read.
- **G4. The same answer twice.**

## 7. Predictions, to be frozen with this file

Each is tested per transcriber: HOLDS if for both, SPLIT if for one, FAILS if for neither. All are at p at most 0.05 by permutation, with the seeds fixed.

1. **Held-out stories:** in each corpus, the frozen grammar ranks a held-out story above its alternatives more often than chance. The measure is the concordance; chance is 0.5.
2. **The genre, beyond length:** the genre whose weights score a held-out story best names its genre with a balanced accuracy above chance, and above that of length alone. This is the joint model's lesson, written in.
3. **The unseen cultures, after the freeze:** the concordance of the Native American and East Asian tales, under the shared weights, is above chance. The story language would then extend beyond the corpora it was fitted on.
4. **The owner's prediction (l), restated for the grammar:** that concordance is lower for the Native American tales than for the East Asian.

**Reported, not tested:**
- the weights and the genre offsets, feature by feature;
- which genre's weights fit each new culture best;
- a few sequences sampled from each genre's weights, as illustration only;
- the length control's weight.

## 8. Decisions for the owner before the freeze

1. **The model:** contrastive (recommended) or generative.
2. **The features:** the seven of section 3 (recommended), or fewer, for instance without the candidate groups until they are frozen in `Candidates.md`.
3. **The weights:** shared plus genre offsets (recommended), or separate for each genre.
4. **The held-out fraction:** a fifth (recommended), or another.
5. **Sampled stories:** reported as illustration (recommended), or left out.

## 9. After the freeze, and the cost

1. Commit this file frozen.
2. Write `StoryGrammar/HeldOut.txt` by the fixed seed, and commit it.
3. Write and commit the program and tests G1 to G4, and pass them.
4. Fit, and score predictions 1 and 2. Freeze the fitted grammar.
5. Only then are the cross-cultural transcriptions read, and predictions 3 and 4 scored.

**The cost** is the keeper's work alone, with no readers: perhaps one session for steps 1 to 4. The G2 reproduction and the alternatives' number are the slow parts.
