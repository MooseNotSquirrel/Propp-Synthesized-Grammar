# Social hierarchy in Propp's character set: protocol (DRAFT 2026-10-28, FOR THE OWNER'S REVIEW, NOT FROZEN)

**Drafted 2026-10-28 at the owner's word, for `ProppQueue.md` item (k).** Nothing here is built. No figure it tests has been read, apart from the exploratory first look named in section 1.

## 1. The question

**The owner's claim:** the relations of the acts layer (kin, above, below, ally, stranger, enemy) are a generic version of Propp's characters, and social hierarchy is embedded in his character set. Much of it is shared cultural understanding that an automated reader may not surmise: the hero above the helper, the false hero below everyone.

**Three kinds of rank** (the keeper's design note in item (k)). This protocol tests only the first and reports the second:
1. **Stated rank:** the rank the text states, caught by the relation field. In each act, `above` means the performer rules, owns, commands or employs the undergoer, and `below` means the performer serves, obeys or is ruled by the undergoer (`ActsRoles/ActsRules.md`).
2. **Narrative rank:** whom the story raises and brings down. Reported here from the outcomes, not tested.
3. **Cultural rank:** shared understanding, not coded. The readers are language models whose shared understanding is largely modern and Western.

**Caution:** a low share of above and below means little *stated* hierarchy, not little hierarchy.

**Already seen:** a first look (2026-10-21, exploratory, both transcribers pooled) found that:
- villain events are enemy in 41%;
- donor events are stranger in 37% and ally in 17%;
- the dispatcher holds the most stated hierarchy (above and below 21%);
- above and below are 2% to 12% in every sphere.

Prediction 3 below repeats part of this, and is labelled a replication.

## 2. The material

- **The acts** (`tables/acts.tsv`), joined to the characters of the character table exactly as `Characters/characters.py` joins them: by name where the names are English, and by event where they are Russian, under test C4. An act counts where both its performer and its undergoer are characters of the story.
- **Spheres:** from the character table.
- **The hero:** the judged hero, as mended on 2026-10-28; stories whose readers named no single hero are left out.
- **Corpora:** the wondertales, animal tales, fables and tragedies, per transcriber. The myths have no acts and take no part.

## 3. Tests and self-tests, before any result is read

- **K1. Invented stories:** a small file with known answers, written first. It holds a hero commanding a helper (above), a helper obeying (below), a villain's hostile act (enemy), and an act with no undergoer (not counted).
- **K2. The join is the table's:** for every character, the relation counts the program assigns to it as performer must equal the table's `relations` column.
- **K3. The same answer twice.**
- **Dry run:** counts only, for each corpus and transcriber: acts, acts with both ends a character, and acts between the hero and each sphere's holders. No share and no comparison.

## 4. The measures, per corpus and per transcriber

1. **Relations by sphere:** for the acts performed by each sphere's holders, the share of each relation.
2. **Rank between pairs:** for acts from one sphere's holder to another's, the counts of above and below, in each direction. The pairs are hero to helper, helper to hero, hero to false hero, false hero to hero, dispatcher to hero, hero to dispatcher, villain to hero, and princess to hero.
3. **Stated hierarchy:** the share of all acts between characters that are above or below.
4. **The relation predicts the sphere:** each sphere-holder with at least 3 acts as performer, described by the shares of its ten relations. Each is assigned the sphere whose mean profile is nearest, leaving it out of the means. The accuracy is set against 1,000 shuffles of the sphere labels.
5. **Narrative rank, reported:** for each sphere, the share of its holders who undergo punishment (U), and the share who perform the wedding or reward (W).

## 5. Predictions, to be frozen with this file

Each is tested per transcriber: HOLDS if for both, SPLIT if for one, FAILS if for neither. The tests are fixed below, all at p at most 0.05. A comparison needs at least 10 counted acts, or 10 stories a side, else it is NOT TESTABLE.

**From the owner's claim:**
1. **The hero above the helper,** in the wondertales: in acts from the hero to a helper, above outnumbers below; and in acts from a helper to the hero, below outnumbers above. Each direction is tested by a one-sided binomial sign test on the above and below counts, ties and other relations set aside. Both directions must hold.
2. **The false hero below:** in acts between the false hero and the hero, in either direction, the false hero stands below more often than above, all four corpora pooled. The false hero is rare everywhere, so this may be NOT TESTABLE, and it is stated now that it would be reported so.

**Proposed by the keeper, not from Propp and not the owner's:**

3. **The villain's enmity (a replication):** the acts of the villain's sphere are enemy in a higher share than those of any other sphere. Each comparison is a permutation test of the sphere labels over characters, in the wondertales and the tragedies.
4. **The relation predicts the sphere:** the accuracy of measure 4 exceeds that of the shuffles, with at most 5% of shuffles reaching it, in each corpus that has at least 30 sphere-holders with 3 acts.
5. **Stated hierarchy by genre:** the share of above and below is higher in the tragedies than in the wondertales and in the fables. Each comparison is a permutation test of the corpus labels over stories.

**Reported, not tested:**
- every measure for every corpus;
- the pairs of measure 2 in the animal tales, fables and tragedies;
- narrative rank (measure 5) beside stated rank, sphere by sphere;
- how the two transcribers differ on the relations themselves.

## 6. Decisions for the owner before the freeze

1. **Where prediction 1 is tested:** in the wondertales only, Propp's own corpus (recommended, the other corpora reported); or in all four.
2. **Prediction 3:** keep it as a labelled replication (recommended), or drop it, since the first look has already shown it.
3. **Which relations are rank:** above and below only (recommended). Kin and spouse carry rank in many cultures (a father, a husband), but the field does not say who is above. Counting them would be the keeper's assumption.
4. **Narrative rank:** reported only (recommended), or tested now with its own prediction. Testing it, for instance "the false hero is punished more than he is rewarded", would need a frozen measure of outcome written first.

## 7. After the freeze

1. Commit this file frozen.
2. Write and commit the invented stories of K1 and the program `Hierarchy/hierarchy.py`; pass K1 to K3.
3. Dry-run, and show the counts.
4. Run into `Hierarchy/HierarchyRun.txt`, score, log, and enter the finding in `PreliminaryFindings.md` at the owner's word.
