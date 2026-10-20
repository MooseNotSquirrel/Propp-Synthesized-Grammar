# The free verbs grouped by context: the test

**DRAFT, 2026-10-19, to be frozen at the owner's word, before any verb is grouped.** Once frozen, a departure is logged in `Group/KeeperLog.md`, not made here.

## The question

The bottom-up test (`Free/`) took each describer's verb as written, so verbs that say the same thing, ask, beg, pray and urge, count as different tokens, and the counts are spread thin over about 650 verbs.
The owner asked whether the lists were normalized for this redundancy. This test groups the verbs by a program, from the data alone, with no list of acts and no dictionary, and reruns the frequency analysis on the groups.

## The grouping

**The verbs:** both describers' free descriptions of the 159 stories (`Free/`), pooled, so that the classes are shared.
**A verb's context:** the words of its phrases (the first word, the verb itself, left out, and common small words), the verb just before it and the verb just after it in the same story.
**The classes:** the verbs used at least 5 times, each a vector of its three kinds of context, each kind scaled to length one; grouped by average-linkage clustering on cosine distance into **37 classes**, as many as the act list has acts with `other`, fixed in advance so that the two can be compared; each class named by its commonest verb. Verbs used fewer than 5 times keep their own names.
**Checked:** `group.py selftest`, twelve planted acts each said with three synonyms, each with its own objects and place in a sequence: all twelve acts' synonyms land in one class each.

## The analysis

The frequency analysis's discovery and confirmation (`Ngrams/`), unchanged, on the class strings: the same halves of the stories, within-story shuffles, both describers in both halves.
A class's act is the act its verbs meet in at least half of their clean events (one free entry and one act entry), given at least 5, as `Free/` maps a verb.

## The predictions

1. **The requests group.** Of the request verbs ask, beg, pray, urge, plead, implore and entreat that a describer uses at least 10 times, two thirds or more fall in one class, for both describers.
2. **The exchange comes out:** a confirmed pair of classes whose acts are plead and respond.
3. **Grouping does not bring out Propp's pairs:** at most one of the six (interdiction and violation, reconnaissance and delivery, trickery and complicity, test and reaction, struggle and victory, task and solution) comes out as a confirmed pair of classes with the pair's acts. The keeper's reason: the bottom-up test found that the second halves have no verbs of their own, and grouping verbs cannot give them one.

Each is reported HOLDS or FAILS.

## Reported, not judged

The classes with their members and uses (`Classes.txt`); every candidate pair of classes, confirmed or not, with its distance profile and acts; the confirmed pairs whose acts are none of the seven.
