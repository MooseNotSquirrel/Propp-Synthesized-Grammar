# The kind rule's errors: the amendment (ADOPTED 2026-10-27 AT THE OWNER'S WORD: CHOICE (b))

**Adopted 2026-10-27, choice (b)**, and recorded in `CharacterProtocol.md` section 8. That entry fixes the number of fresh controls at 60 and the threshold at 54 of 60. The draft below is kept as it was written.

**Drafted 2026-10-27 at the owner's word.** This draft follows the finding logged on 2026-10-26: on the name stage's 49 controls, the readers gave the WordNet kind rule's kind to only 35. Nothing here is built, and the table is unchanged. The counts below come from `tables/characters.tsv` as it stands at ee27edc. They were made with scratch scripts that write nothing into the project.

## 1. Where the rule fails

The rule (`CharacterProtocol.md` section 3) takes the first WordNet noun sense of a character's head noun. This draft splits the characters whose kind the rule sets into four classes. The test for each class is mechanical:

- **named:** the head's first sense is an instance (*Zeus*, *Achilles*) or a capitalized lemma (*Greek*, the language);
- **group:** marked as a group by the table already (a plural, or *and*);
- **collective:** a singular head whose first sense is in WordNet's `noun.group` (*people*, *men* as "work force", *army*, *household* as "family");
- **common:** everything else.

**The 49 controls, by class.** A control counts as a fault when both readers gave the same kind and it was not the rule's kind.

| Class | Controls | Readers agree with the rule | Rule's faults |
|---|---|---|---|
| named | 14 | 7 | 7: Greeks, Jupiter, Achilles, the lords of Delphi, Tantalus, Europa, Jocasta |
| group | 13 | 11 | 2: Minyans, wild beasts |
| collective | 3 | 0 | 3: the land force, men, household |
| common | 19 | 17 | 2: satyr (first sense "lecher"), Truth (the readers split) |

(*The land force* falls here by the meaning of its key, though *force*'s first sense is `noun.attribute`; it fails either way.)

So the rule is unreliable on names and collectives, and fair on common nouns and plurals. But 19 and 13 controls are too few to show that the rule holds even on those.

## 2. How many characters each class holds

These are unique items, counted as a corpus, a story and a character key across both transcribers, the way the name stage counted them. They are kinds set by the rule; the readers never saw them.

| Class | Items | Wondertales | Animal tales | Fables | Tragedies | Myths | Commonest heads |
|---|---|---|---|---|---|---|---|
| named | 879 | 28 | 3 | 37 | 358 | 453 | Zeus, Apollo, Athena, Hera, Hermes, Poseidon |
| group | 641 | 168 | 52 | 115 | 130 | 176 | sons, daughters, servants, children, brothers, women |
| collective | 124 | 41 | 9 | 20 | 24 | 30 | people, men, army, household |
| common | 1,622 | 472 | 254 | 489 | 202 | 205 | |

**Cost**, at the name stage's rate (75 items a batch, two readers, about 62,000 tokens a reader):

- named, group and collective together: 1,644 items, 22 batches, 44 readers, about 2.7 million tokens;
- all four classes: 3,266 items, 44 batches, 88 readers, about 5.5 million tokens.

The name stage itself was 1,556 items and about 1.6 million tokens.

## 3. The choices

- **(a) Readers for every character.** All 3,266 rule-set items go to the two readers. The rule's kind is kept as a column for comparison. This is clean, but it costs the most.
- **(b) Readers for named, group and collective characters; the rule kept for common nouns, on a test.** The 1,644 items go to the readers, and the batches carry fresh controls drawn from the 1,622 common items by a seeded rule. If both readers give the rule's kind to at least 90% of those controls, the rule stands for common nouns. Otherwise the common nouns go to the readers too, which turns (b) into (a). The threshold is fixed now, before any control is read.
- **(c) Amend the rule** to treat a mythical being under `noun.person` as a person, `noun.group` as a group of people, and so on. Not recommended. Each patch is fitted to the controls already seen, so those controls can no longer test it. And no patch reaches the named class's real fault: WordNet gives a name its dictionary sense (Jupiter the planet, Europa the moon), not the story's.

**Recommended: (b).** It sends the readers the classes where the rule is shown to fail. It keeps the rule only where a fresh test, set in advance, can still reject it. And it costs half of (a). The four-way split is drawn after seeing the controls, and that is the reason the common class must pass fresh controls rather than the old ones.

**Unchanged under every choice:**
- a kind is used only where the two readers agree, and is unknown otherwise (decision 1 (a));
- phrase-names are counted apart and given no kind;
- readers' agreement is reported, and is consistency between two models, not proof of the right kind.

## 4. What would change, once a choice is adopted

- **`names.py`:** a `setup2` command writes the second stage's items and controls (for (b): the named, group and collective classes, with about 60 seeded common-noun controls). It runs dry first.
- **`characters.py`:** `reader_kinds()` also reads the second stage's answers. The kind_by column then gains no new value; it stays `readers` or `wordnet`. The table is rebuilt after T1, T2 and T4 pass, then C1 to C7 are rerun.
- **`CharacterProtocol.md` section 8:** the adopted choice is entered as an amendment, with the date and the reason (this file).
- **ActsRoles:** the stage runs in portions, as names-1 to names-4 did, each ending in a stop.
