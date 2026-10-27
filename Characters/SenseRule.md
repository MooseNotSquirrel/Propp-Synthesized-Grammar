# Names and wrong senses in the common class: the amendment (ADOPTED 2026-10-27 AT THE OWNER'S WORD: CHOICES (a) AND (i))

**Adopted 2026-10-27, choices (a) and (i)**, and recorded in `CharacterProtocol.md` section 8. The draft below is kept as it was written.

**Drafted 2026-10-27 at the owner's word.** Nothing here is built; the character table, `CharacterRun.txt` and the verdicts are unchanged. The counts were made from `tables/characters.tsv` at 34c5f94 by scratch scripts that write nothing into the project. A row is one character as one transcriber gives it; an item is one story and character key across both, as the name stages count them.

## 1. The fault

Under `KindRule.md` choice (b), the WordNet rule keeps the kind of the *common* class: characters whose head's first sense is not an instance, not a capitalized lemma, not a group and not `noun.group`. The class passed its test, 54 of 60 fresh controls, at the threshold exactly. The measures' output then showed two faults the test let through:

- **Proper names whose first sense is a common word** (about 58 rows). Telamon (a column), Rhesus (the monkey), Ion (the particle), Pan (a cooking pan), Nisus (striving), Phoebe, Iris, Agave, Bias, Andromeda (the constellation), Python, Side, Althaea, Arete, Hyacinth, Mercury (the metal), Anna; and the Sphinx and a Harpy as person.
- **Common words whose first sense is not the story's** (about 75 rows). Chorus as object (48), the Ass as object (WordNet's first sense is the buttocks, 11), Cock, Swallow, Kite, Partridge, Sprat, Thrush, Grouse, Tanner.

The sorting into faults is the keeper's reading of the list, not a rule. Personified forces (Truth, Dawn, Night, Death, the Sea) are not counted as faults: object is defensible for them.

**It touches a verdict.** Among the fables' sphere-holders, beasts and birds read as object are 14 rows for transcriber A and 15 for B, most of them the Ass. Counted as animals, the fables' animal share would be 54.0% and 53.2% in place of 49.1% and 47.9%, and prediction 2 would hold.

## 2. The choices

| Choice | What goes to the readers | Items | Readers, at 75 a batch | Tokens, about |
|---|---|---|---|---|
| (a) | every common-class character whose head is capitalized in some recorded name, with fresh controls from the rest | 685 | 11 batches, 22 | 1.3 million |
| (b) | none: the rule takes the first sense that is not an object | 0 | 0 | 0 |
| (c) | the whole common class | 1,622 | about 24 batches, 48 | 2.9 million |
| (d) | none: the table stands, the faults are reported beside the results | 0 | 0 | 0 |

- **(a)** By corpus: wondertales 16, animal tales 180, fables 344, tragedies 117, myths 28. The trigger is mechanical. A capital marks a name or a personification, and the fables and animal tales capitalize their beasts ("the Ass", "the Cock"). It catches 184 of the 192 rows on the keeper's fault list. Sixty fresh controls are drawn by a fixed seed from the common items left out, and scored as before: if both readers give the rule's kind to at least 54, the rule stands for those; otherwise they go to the readers too, which turns (a) into (c).
- **(b) Not recommended.** It costs nothing but makes new faults. WordNet's second sense of *ass* is a fool, so the Ass becomes a person (30 rows); a stone, honey and a ram become persons. It changes 120 items, and on the second stage's 60 controls it agrees with both readers 55 times against the first sense's 54: no real gain. It is also a rule fitted after the errors were seen.
- **(c)** Clean but costly. The rule's kind then stands for no character, and is kept as a column for comparison.
- **(d)** Cheapest. The faults stay in the kinds, and prediction 2's verdict rests on them.

**Recommended: (a).** It sends the readers the rows where the faults are, by a test that does not use the fault list, and it keeps the rule only where fresh controls can still reject it, at less than half the cost of (c).

## 3. Whether prediction 2 is rescored

The protocol scores each prediction once, on the table as frozen and amended before the measures ran. This amendment comes after the measures, and it was prompted partly by the faults behind prediction 2's figures. Three ways:

- **(i) Recommended: both kept.** The verdicts of 2026-10-27 stand as the verdicts of record, prediction 2 FAILS. After the amendment, all six predictions are rescored on the amended table and reported beside them, marked as after a post-measure amendment, with this file named as the reason. Not prediction 2 alone: rescoring only the prediction that was found wanting would be choosing where to look.
- **(ii) Replaced.** The amended table's verdicts replace the first. Not recommended: the record would no longer show that the first scoring failed.
- **(iii) Not rescored.** The verdicts stand, and the faults are reported beside them only. This goes with choice (d).

Under (i), the fables' heroes beside `PreliminaryFindings.md` section 5 are also reported again, since the Ass and the Cock are among them.

## 4. What would change, once a choice is adopted

- **`names.py`:** a `setup3` command for the third stage, batches numbered on from `n38`, the same prompt and form, with 60 seeded controls from the uncapitalized common items. It runs dry first.
- **`characters.py`:** `second_stage()` also reads the third stage's items, so a character asked takes the readers' agreed kind or unknown. The table is rebuilt after T1, T2 and T4 pass, and C1 to C7 are rerun.
- **`measures.py`:** run again on the amended table into a second file, `CharacterRun-amended.txt`. `CharacterRun.txt` is kept as it is.
- **`CharacterProtocol.md` section 8:** the adopted choice entered, with the date and this file as the reason.
- **ActsRoles:** the stage run in portions, each ending in a stop.
