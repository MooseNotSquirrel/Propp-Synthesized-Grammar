# The character-set layer: protocol (DRAFT 2026-10-26, NOT FROZEN; the owner's decisions 1, 2 and 4 recorded)

**Drafted 2026-10-26 at the owner's request, for `ProppQueue.md` item (m)** and `DataProtocol.md`'s added layer: one character table per corpus, giving each character's name, kind, spheres and act profile, built from the normalized tables. The owner's aim is that each corpus's character set be **inferred, not presupposed**. Nothing here is built. The tests come first (section 2), and every program they check is committed before it runs. The run itself waits for the owner to freeze this file. Three of the four decisions in section 6 are taken; predictions 3 to 6 are still open.

## 1. What is measured on the tables today (counts only, no result)

These are counted on 2026-10-26 from the tables, to size the problem. They are not findings.

- **Names in English and in Russian.** The function and free-verb layers name characters in English in every corpus. The role-free acts, and the significance layer copied from them, name characters in Russian:
  - wondertales: 99% of act performers and undergoers;
  - animal tales: about a third of reader A's names and two thirds of reader B's.

  So the act layer cannot be joined to the functions by name in the Russian corpora.
- **Names WordNet can sort.** The rule in section 3, run on the function performers, resolves:

  | Corpus | Mentions resolved | Mostly unresolved |
  |---|---|---|
  | Fables | 98% | compounds such as *milk-woman* and *charcoal-burner* |
  | Animal tales | 99% | |
  | Tragedies | 69% | proper names: Clytaemestra, Eteocles, Hecuba |
  | Myths | 63% | proper names: Melampus, Aegeus, Eurystheus |
  | Wondertales | 62% | proper names: Ivan-tsarevich, Ivan, Baba Yaga, Koshchei |

  The proper names fall where the owner's question is sharpest.
- **The size of the name stage** (decision 1 (a)). This counts the function layer's performers and undergoers that the kind rule leaves unknown, as pairs of a story and a name key. It is the reader stage's material, counted on 2026-10-26:

  | Corpus | Story-name pairs | Distinct names | Stories with one |
  |---|---|---|---|
  | Wondertales | 282 | 225 | 40 of 45 |
  | Animal tales | 3 | 3 | 3 of 50 |
  | Fables | 38 | 25 | 34 of 201 |
  | Tragedies | 270 | 205 | 32 of 32 |
  | Myths | 830 | 641 | 154 of 172 |
  | **All** | **1,423** | **1,008** | |

  The myths hold more than half of it. Names that appear only in the act or free-verb layers are not in these counts; most of them should join a function's name, and the dry run counts any that do not.
- **WordNet 3.0** is at `C:/Users/Steve1/nltk_wordnet`, read through nltk as `Group/wordnetGroup.py` reads it. Its noun classes separate person (`noun.person`) from animal (`noun.animal`). The gods it knows (Zeus, Athena, Apollo, Hermes, the Muses, the nymphs) sit under `deity.n.01`. Some figures sit under `spiritual_being.n.01` without being deities: *god*, and *devil*, whose first sense is Satan.

## 2. Tests and self-tests, written and passed before any result is read

Each test is a program, committed before it runs. A test that fails stops the run until the owner decides; it is not loosened after the fact.

- **C1. The table holds every name** (the character table's T1). Every non-empty performer and undergoer in `functions.tsv`, `acts.tsv` and `free.tsv` maps to exactly one character row of its story and reader. Nothing is lost and nothing is counted twice.
- **C2. The table-backed join equals the published one.** On the wondertales on card U, both readers, the characters and spheres the table gives equal `Spheres/explore.py`'s, so that `SpheresExplore.txt` is reproduced byte for byte. This is the self-test the parity reports already passed for the spheres reader (`KeeperLog.md`, 2026-10-25), rerun against the new table.
- **C3. The kind rule on WordNet's own words.** Take a fixed sample, drawn by a seeded rule and written to a file before the rule runs: 100 nouns from `noun.person`, 100 from `noun.animal`, every hyponym of `deity.n.01` with a single-word lemma, and 100 from `noun.artifact` and `noun.plant`. The rule must return each word's class in every case. Where a word's first sense differs from the class it was drawn from, it is listed and left out, not counted as a failure.
- **C4. Joining the act layer by event, tested where the answer is known.** This test applies only if decision 2 takes the event route.
  - **The rule:** within an event, a function's performer is linked to the performer of that event's acts when there is exactly one.
  - **Where it is tested:** on the fables, the tragedies and the English half of the animal tales. There both layers use English names, so the name join gives the right answer.
  - **The threshold:** the links must agree with the name join in at least 90% of linked pairs, for each corpus and each reader.
  - **If it falls short:** the Russian corpora's act profiles are reported as missing, not joined by a weaker rule.
- **C5. The grouping recovers planted roles and does not collapse** (see section 4, route 2).
  - **Planted roles:** generate 400 characters from four planted profiles, with the seed fixed: a trickster (deceives as performer, is deceived), a villain (harms, is punished), a helper (gives, rescues) and a victim (undergoes harm, is rescued). Add noise of 30% random acts. The grouping must recover the planted roles with an adjusted Rand index of at least 0.8.
  - **Shuffled profiles:** with the profiles shuffled across characters, its agreement with Propp's spheres must fall to an adjusted Rand index of at most 0.05.
  - **On the real data:** if the largest group holds more than 60% of characters, or fewer than three groups have five or more members, the grouping is reported as COLLAPSED and not read further. This guard exists because the verb grouping in `Group/` collapsed into one class.
- **C6. The same answer twice.** Two runs give byte-identical output, with the hash seed and every random seed fixed. This guards against the run-to-run differences seen in `DescribeRun`.
- **Dry run before the run:** counts only, for each corpus and reader: stories, characters, characters with a sphere, the share of names resolved by kind, and the share of acts joined to a character. It prints no kind-by-role figure, no grouping and no ranking.

## 3. The character table

**Built by `Data/build.py`** as a derived table, `tables/characters.tsv`, after T1 to T4 pass, and read only through `tables.py`. It has one row per character, per story, per reader. Its columns:
- the story and the reader;
- the character key;
- every name the layers give it;
- its kind, and how the kind was set (WordNet, a reader, or unknown);
- its spheres (the Propp functions it performs, grouped as `Spheres/explore.py` groups them);
- its act profile: counts of each role-free act performed and undergone, and of each relation it stands in;
- the number of events it appears in.

**Names within a story** are joined as `Spheres/explore.py` joins them, unchanged. Articles and the stop words *the*, *a*, *his*, *old*, *young*, *little* and the like are dropped. A name whose words all stand in one longer name of the same story joins it.

**Names across stories** are joined by the head noun of the key (*the fox*, *the old man*, *Ivan*), and only for the frequency ranking. The table keeps each story's characters apart.

**The kind rule.**
1. Take the head noun of the name: the last word, after possessives and phrases such as *of*, *with* and *from* are cut away, so *the old man's daughter* gives *daughter*.
2. Look up its first WordNet noun sense, or failing that the first sense of its base form (morphy).
3. The kind is:
   - **deity** if any hypernym path passes through `deity.n.01`;
   - **supernatural** if a path passes through `spiritual_being.n.01` or `imaginary_being.n.01` but not `deity.n.01`;
   - **person** for `noun.person`;
   - **animal** for `noun.animal`;
   - **object** for every other noun class;
   - **unknown** when there is no sense.
4. Plurals and groups (*the Trojan women*, *the Argive army*) take their head noun's kind and are marked as groups.

## 4. What is measured, per corpus and per reader

Every measure is reported for readers A and B separately, as every earlier layer was. How often the two readers give the same kind to a story's characters is reported beside it.

1. **Kind by role.** For the characters holding each of Propp's seven spheres, the share that are person, animal, deity, supernatural or object. For example: what share of heroes, villains, helpers and donors are people, animals or gods. Unknown is reported as a share of its own, never spread among the others. A role's kind figures are read only where unknown is below 10% of its characters; otherwise they are reported as UNRESOLVED.
2. **Roles, by two routes.**
   - **Top-down:** Propp's seven spheres and how they combine, as the spheres script gives them. This is the share of characters holding two spheres, and the commonest combinations.
   - **Bottom-up:** characters grouped by their act profiles alone, with no sphere and no name given. The method is average-linkage clustering on cosine distance, the number of groups chosen by silhouette from 3 to 10 (decision 4). Only characters with at least 3 acts are grouped.
   - **What is reported:** each group's size, its five commonest acts as performer and as undergoer, its commonest kinds, and its agreement with the spheres (adjusted Rand index).
   - A group that matches no sphere is reported as **a role the corpus has that Propp's seven do not name**. Whether it is one is left to the reading.
3. **Rank by frequency (the owner's addition).** Characters are ranked within each corpus across stories, by two counts:
   - the stories a character appears in;
   - the acts it performs, or for the myths the functions it performs.

   Each ranking is given by head noun, by kind and by role. Corpora are compared on how concentrated each ranking is: the share of the top five, and the slope of log rank against log frequency. A genre of recurring stock actors shows a high share and a steep slope; a genre of unique individuals shows the reverse.
4. **The myths** have functions but no acts, so they get kind by role, the top-down route and the ranking by functions. Their bottom-up grouping is reported as not possible, not left out silently.

## 5. Predictions, to be frozen with this file

Written before any figure in section 4 is read. Each is tested per reader; it **HOLDS** only if it holds for both, **SPLIT** if for one, and **FAILS** if for neither.

**From the owner's expectations (2026-10-21):**
1. In the wondertales, most characters holding any of Propp's seven spheres are people (person over half).
2. In the fables, most characters holding any sphere are animals (animal over half).

**Proposed by the keeper, not from Propp and not the owner's. Kept, changed or struck at the freeze:**

3. In the animal tales, most characters holding any sphere are animals.
4. The share of deities among sphere-holders is higher in the myths and the tragedies than in the wondertales and the fables.
5. Stock actors: the top-five share of the ranking by stories is higher in the fables and the animal tales than in the tragedies.
6. The bottom-up grouping, on the corpora where it does not collapse, agrees with Propp's spheres better than shuffled profiles do. A shuffle test of 1,000 is passed if at most 5% of shuffles reach the real agreement.

**Reported, not tested:**
- the readers' agreement on kind;
- how the two heroes of P01, P04, P06 and P08 fall in the table (run 2's readers could not tell whose good sets the value, `KeeperLog.md`, 2026-10-26). The sphere layer credits functions to their performers, so each of the two holds the spheres of its own functions;
- the fables' heroes beside the figure in `PreliminaryFindings.md` section 5 (about 71% animal, 22% human, 4% gods), with any difference above 5 points explained.

**Not in this protocol:** narrative rank (item (k)), the failed hero (item (j)), the trickster count, and the Native American and East Asian corpora. The table serves all of them, and each gets its own frozen predictions when it is taken up.

## 6. Decisions for the owner before the freeze

**Taken 2026-10-26: the owner agreed with the recommendations.** Decision 1 takes (a), decision 2 takes (a), and decision 4 takes the method as drafted. Decision 3, predictions 3 to 6, is still open.

1. **Names WordNet does not know** (31% to 38% of mentions in the wondertales, tragedies and myths).
   - **(a) DECIDED, as recommended:** a small reader stage, two readers, run only on the unresolved names. Each gets the story's title and the name, and gives a kind from the five, with a reason. Agreement is reported. The kind is used where both readers agree, and is unknown otherwise.
   - **(b)** Leave them unknown. Kind by role would then be UNRESOLVED for the wondertales' heroes, which are mostly Ivan.
   - **(c)** A list written by the keeper. Not recommended: it is hand coding by a model, and these are the names where modern and Western assumptions would enter.
2. **The Russian act names.**
   - **(a) DECIDED, as recommended:** join the acts by event, under test C4.
   - **(b)** Build the act profile from the free verbs, which are in English in every corpus but are not a closed list. The grouping would then need its own vocabulary rule, frozen first.
3. **Predictions 3 to 6:** keep, change or strike.
4. **The grouping method: DECIDED, as drafted:** average linkage on cosine distance, with silhouette from 3 to 10.

## 7. After the freeze

1. Commit this file frozen.
2. Write and commit the programs: the builder step, `Characters/characters.py`, and the tests C1 to C6.
3. Pass the tests.
4. Dry-run.
5. Set up the name reader stage (decision 1 (a)) in Propp-ActsRoles under its own short collection protocol. That protocol fixes the batches and what each reader sees with a name: the story's title and the events that name it. Then clear it in `RUN.md`.
6. Run.
7. Write the results to `Characters/` and the keeper's account to `KeeperLog.md`.
8. Add the layer to `Parity.md` section 1.
