# Propp's devices across cultures: protocol (DRAFT 2026-10-28, FOR THE OWNER'S REVIEW, NOT FROZEN)

**Drafted 2026-10-28 at the owner's word, for `ProppQueue.md` items (l) and (e).** These hypotheses must be frozen before any Native American or East Asian tale is read, and none has been. Nothing here is built. The figures quoted in section 1 are the exploratory first look on the corpora we already have.

## 1. The hypotheses and the metric

**The owner's hypothesis (l):** the Native American and East Asian tales will show many of Propp's devices put to different cultural purposes.

**The owner's metric (l):** what share of all events the catalog covers. It is counted at three lengths:
- single functions (1-grams);
- the pairs (2-grams);
- the longer groups (n-grams).

**The owner's prediction (l):** coverage very low for the Native American tales, better for the East Asian.

**The owner's hypothesis (e):** East Asian tales stress harmony and collaboration. Their troubles close more by reconciliation and reward than by punishment, and the hero's acts help others more.

**Already seen, on the corpora we have** (first look, 2026-10-21, transcribers A and B):

| | Wondertales | Animal tales | Fables | Myths | Tragedies |
|---|---|---|---|---|---|
| Single functions, the share not X | 68%, 78% | 62%, 57% | 58%, 57% | 59%, 70% | 45%, 48% |
| Of those, the share with the pair partner in the same move | 49% | 54%, 52% | 37%, 33% | 36%, 35% | 31%, 29% |

**The keeper's note:**
- The animal tales, short like Dundes's, are built more of pairs than any other corpus.
- Dundes found little of Propp's long sequence but re-cut his pairs. So the owner's prediction may hold for single functions and groups and fail for pairs.
- The readers are language models whose shared understanding is largely modern and Western. That is a risk to every cross-cultural reading here, stated now and reported with every result.

## 2. The corpora (decision 1)

Each new corpus gets every layer from the start: event lists, Propp's functions on card C, role-free acts, significance, free verbs, and heroes by two readers. These are the same instruments, unchanged, two blind transcribers each, A on Opus and B on Sonnet. Public domain only, the status of each source checked and recorded before use. Fifty tales each, as for the animal tales.

- **Native American, recommended:** Dundes's own sources, the tales of the types he names most:
  - the Star Husband, Orpheus, the Eye-Juggler, Lodge-Boy and Thrown-Away, the Earth-Diver, the Bungling Host and the Dog Husband;
  - the Coyote, Manabozho and Raven cycles;
  - taken in order from the public-domain collections he cites (`Dundes/DundesSources.md`), the Bureau of American Ethnology series first, one version per type and collection, up to 50.

  The alternative is the first 50 tales of one collection, for instance Boas, *Tsimshian Mythology* (1916). That is simpler and blind to type, but it is one culture area.
- **East Asian, the keeper's candidates, to be checked:** English translations published by 1930 of folk tales, not literary tales. For example: Mitford, *Tales of Old Japan* (1871); Ozaki, *Japanese Fairy Book* (1908); Allen, *Korean Tales* (1889); Griffis, *Korean Fairy Tales* (1911). Giles's *Strange Stories from a Chinese Studio* (1880) is literary, a recommended exclusion. The owner chooses. The rule recommended: the first 50 tales of the collections chosen, in their printed order.
- **A caution:** these are English translations, often by Western collectors of their day. The text the readers judge is the translator's, as Afanasyev's is read in English for the animal tales.

## 3. The catalog the metric counts (decision 2)

**Recommended: Propp's functions only, for the test.** Single functions, Propp's pairs, and his blocks, as the first look and the parity runs counted them. This keeps the new corpora comparable with the five already transcribed.

**Dundes's added motifemes** (Consequence, Attempted Escape, the Explanatory Motif) are reported on the new corpora only, from the act layer and the events. Adding them to the card would mean transcribing the old corpora again before any comparison.

## 4. Tests and self-tests, before any new tale is read

- **X1. The first look reproduced.** On the five existing corpora, the program must give the first look's single-function and pair shares of section 1. This is the self-test against figures already published.
- **X2. Blocks as the parity runs counted them.** The program must reproduce the published share of functions inside blocks (`Data/Parity.md`) for the animal tales and the myths.
- **X3. The same answer twice.**
- **X4. Each source's public-domain status** recorded before its tales are set up.

## 5. Predictions, to be frozen with this file

Each is tested per transcriber: HOLDS if for both, SPLIT if for one, FAILS if for neither. Every comparison is a permutation test of the corpus labels over stories, at p at most 0.05, with at least 10 stories a side.

**The owner's (l):**
1. **Native American coverage very low:** their single-function coverage is lower than that of each of the five existing corpora. That includes the tragedies, the lowest now at 45% and 48%.
2. **East Asian better:** their single-function coverage is higher than the Native American.
3. **Groups:** the share of covered functions inside one of Propp's blocks is lower in the Native American tales than in the wondertales.

**The keeper's, not from Propp and not the owner's, from the note above:**

4. **Pairs survive:** among covered functions, the Native American share with the pair partner in the same move is higher than that of the fables, the myths and the tragedies, as the animal tales' is.

**The owner's (e), East Asian against the wondertales:**

5. **Less punishment:** a smaller share of stories contain a punishment (U).
6. **The hero helps:** a larger share of the hero's acts have, in the significance layer, the value of helping a character other than the hero.

**Reported, not tested:**
- the owner's hypothesis (l) itself, devices put to different purposes. For each function found in both a new corpus and the wondertales, its significance profile in each: whom it helps and whom it harms.
- Dundes's added motifemes on the new corpora;
- every measure for every corpus;
- the character table of each new corpus (`CharacterProtocol.md`) and its kinds, under the four name-stage rules now in force.

## 6. Decisions for the owner before the freeze

1. **The corpora:** the Native American rule (Dundes's types, recommended, or one collection), and which East Asian collections.
2. **The catalog for the test:** Propp's functions only (recommended), or with Dundes's motifemes added to the card, which would mean transcribing the old corpora again.
3. **The thresholds:** prediction 1's "very low" as lower than every existing corpus (recommended), or a fixed figure, for instance below 40%.
4. **Prediction 6's significance rule:** to be fixed exactly once the significance layer's values are listed for the program. Recommended: helping means the act's value is to the advantage of its target, and the target is not the hero.

## 7. After the freeze, and the cost

1. Commit this file frozen, before any tale of either corpus is opened.
2. Write and commit the program and tests X1 to X3; pass them on the existing corpora.
3. Choose and check the sources (X4); set up the event-list stage for each corpus.
4. Run the layers stage by stage, at the owner's word, as the animal tales were run.

**The cost** is large. The animal tales took about ten reader stages for 50 tales. Two corpora of 50 tales each would be about twenty stages, several million tokens, run over several sessions. Only steps 1 and 2 fit in one session.
