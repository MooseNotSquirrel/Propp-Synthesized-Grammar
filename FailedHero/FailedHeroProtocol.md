# The failed hero as Propp's own apparatus: protocol (FROZEN 2026-10-28 AT THE OWNER'S WORD, THE FOUR RECOMMENDED DECISIONS TAKEN)

**Drafted 2026-10-28 at the owner's word, for `ProppQueue.md` item (j); frozen the same day at the owner's word**, with every decision in section 6 taken as recommended. Nothing here is built and no figure it tests has been read for this purpose. The tests come first (section 3), and every program they check is committed before it runs.

## 1. The question

**The keeper's reading, speculation and not Propp's, which the owner prefers:** the tragic failed hero is not a new character and not "the hero in negative mode". It is one character holding both the hero's and the villain's sphere, which Propp allows (one character may hold several spheres), in a story whose frame does not close.

The protocol asks whether Propp's own apparatus, applied to the tables, picks out the tragedies' heroes this way more than it picks out the heroes of the other four corpora.

**Already known, and why it matters.** Two figures were seen before this draft:
- `PreliminaryFindings.md` section 5 (exploratory, `Spheres/`): one character holds both spheres in two thirds to three quarters of the tragedies, about a fifth to a quarter of the tales and myths, and almost no fables.
- The same file, section 4 (`Heroes/WithJudgedHeroes.txt`): the "failed hero", a success followed by an unrepaired villainy, occurs in about one tragedy in five against 7% of tales.

So prediction 1 below is a replication on the new table, not a blind test, and is labelled so. Predictions 2 and 3 use measures not taken before: the negative marks of the hero's late functions, and who undergoes the closing punishment.

## 2. The material

All from the normalized tables through `tables.py`, both describers kept apart, as in every earlier layer:
- `tables/functions.tsv`: each function's story, reader, move, position, `negative` mark, performer and undergoer;
- `tables/characters.tsv`: each character's spheres, built by `Spheres/explore.py`'s grouping (hero: C, ↑, E, W; villain: A, H, Pr);
- `Heroes/JudgedHeroes.txt`: the hero both readers named, for 40 wondertales, 45 animal tales, 158 fables and 27 tragedies. The myths have none.

**The corpora:** wondertales (card U), animal tales, fables, tragedies, myths.

**Which hero (decision 1).** Recommended: the judged hero, found in the character table as `measures.py` finds it (the character of its story whose key it joins). Stories without a judged hero are left out, never filled by the keeper. The myths have no judged heroes, so for them choose one of:
- **(a) recommended:** the myths take no part in predictions 2 and 3, and their figures are reported with the hero taken as the hero-sphere holder with the most functions, marked as a different rule;
- **(b)** a reader stage naming the myths' heroes, as the hero study did for the others (126 stories, two readers; it costs a stage).

## 3. Tests and self-tests, written and passed before any result is read

- **H1. Made-up stories.** A small file of invented stories, written before the program runs, in which the right answers are known: a hero who also performs A; a hero punished in the last third; a hero whose late E and F are negative; a villain punished and the hero not. The program must give each answer exactly.
- **H2. The table's spheres are explore.py's.** The fused hero–villain count per corpus and reader must equal what the character table's spheres column gives, character for character.
- **H3. The judged heroes found.** Every judged hero is found in the table or listed as not found; no hero is matched to two characters.
- **H4. The same answer twice.** Two runs give byte-identical output, all seeds fixed.
- **Dry run before the run:** counts only, for each corpus and reader: stories, stories with a judged hero found, stories with any U, stories with any negative mark. No share, no comparison, no p.

## 4. The measures, per corpus and per reader

1. **Fusion.** The share of stories in which the hero holds the villain's sphere as well as the hero's.
2. **Negative marks late.** "Late" is the last third of the story's functions by position (decision 2). The measure is the share of the hero's functions, as performer or undergoer, that carry a negative mark, in the last third against the first two thirds.
3. **The closing punishment.** Among stories with a punishment (U) in the last third, the share whose punished character (the undergoer of that U) is the hero. The spheres script credits a function only to its performer, so the undergoer of punishment is the new measure here.
4. **The frame.** The share of stories whose last villainy or lack (A or a) is followed by no liquidation (K) later in the story. Reported beside the others; it is the "frame that does not close" of the reading.
5. **The failed hero by Propp's apparatus.** A story counts when the hero is fused (measure 1) and either is punished at the close (measure 3) or the frame does not close (measure 4). It is set beside the hero study's failed hero, a success followed by an unrepaired villainy, as a table of agreement.

## 5. Predictions, to be frozen with this file

Each is tested per reader. It **HOLDS** only if it holds for both, **SPLIT** if for one, and **FAILS** if for neither.

**The test (decision 3):** a corpus difference counts only if a permutation test of the corpus labels gives p at most 0.05 (10,000 permutations, seed fixed). **The floor:** a comparison is tested only where each side has at least 10 stories on which the measure is defined. Otherwise it is reported as NOT TESTABLE, never loosened.

1. **Fusion (a replication, labelled so):** the tragedies' fusion share is higher than that of each of the wondertales, animal tales and fables.
2. **Negative marks late:** in the tragedies, the hero's functions carry a negative mark more often in the last third than in the first two thirds, and more often in the last third than the wondertales' heroes' do.
3. **The closing punishment:** the punished character in the last third is the hero in a higher share of tragedies than of wondertales.

**Reported, not tested:**
- measures 1 to 5 for every corpus, the myths by the rule of decision 1;
- the agreement between measure 5 and the hero study's failed hero, since the hero study counts only about six tragedies, too few to test;
- the counts of negative marks by function (the design note in `ProppQueue.md` found them rare, mostly E− and F−; tragedy has few I−);
- the plays whose two heroes the hero study's readers divided (P01, P04, P06, P08), each pair shown.

**Not in this protocol:** social hierarchy (item (k)), narrative rank, and the cross-cultural corpora.

## 6. Decisions for the owner before the freeze

**Taken 2026-10-28: the owner accepted all four recommendations.**

1. **The myths' hero: DECIDED, (a).** The myths are left out of predictions 2 and 3, and their figures are reported by the hero-sphere rule, marked as a different rule. Not taken: (b), a reader stage to judge them.
2. **"Late": DECIDED, the last third of the story's functions by position.** Not taken: the last move only. The last third gives every story a late part; the last move is truer to Propp's moves, but many fables have one move only.
3. **The test: DECIDED, the permutation test and the floor of 10 stories,** as in section 5. Not taken: plain shares with no test.
4. **Prediction 1: DECIDED, kept as a labelled replication.** Not taken: dropping it and reporting fusion only.

## 7. After the freeze

1. Commit this file frozen (done 2026-10-28).
2. Write and commit the made-up stories of H1, then the program `FailedHero/failedHero.py` and tests H1 to H4.
3. Pass the tests.
4. Dry-run, and show the counts.
5. Run, into `FailedHero/FailedHeroRun.txt`.
6. Write the keeper's account in `Data/KeeperLog.md`, and the finding in `PreliminaryFindings.md` at the owner's word.
