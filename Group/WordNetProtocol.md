# The free verbs grouped by WordNet: the test

**Frozen 2026-10-19 at the owner's word, before any of the stories' verbs is looked up.** Once frozen, a departure is logged in `Group/KeeperLog.md`, not made here.

## Why

The grouping by context (`GroupProtocol.md`) degenerated: one class took almost every common verb, and its predictions mean nothing. The owner's question, whether the free verbs can be normalized for redundancy (ask, beg, pray, urge), is still open. The owner allowed a synonym dictionary; this test groups the verbs by WordNet.

## The dictionary

WordNet 3.0 (Princeton University), read through the `nltk` library, downloaded on 2026-10-19 at the owner's word to `C:/Users/Steve1/nltk_wordnet`, outside the repositories. Its license allows use for any purpose with its copyright notice kept; nothing of WordNet is committed, only the classes derived from it, credited to it.

## The rule, fixed before any of the stories' verbs was looked up

A verb's class is its **first WordNet verb sense** (the most frequent), cut at the **second level from the top** of that sense's first path through WordNet's tree of broader senses. The top level was judged too coarse in advance: it would put telling, asking and ordering under one sense of communicating. The verbs used at least 5 times are classed; a verb WordNet does not know as a verb, and every verb used fewer times, keeps its own name.

## The analysis

As in `GroupProtocol.md`, unchanged: the frequency analysis's discovery and confirmation (`Ngrams/`) on the class strings, both describers in both halves; a class's act is the act its verbs meet in at least half of their clean events, given at least 5.

## The predictions

0. **The grouping does not degenerate:** no class holds more than a third of all uses.
1. **The requests group.** Of the request verbs ask, beg, pray, urge, plead, implore and entreat that a describer uses at least 10 times, two thirds or more fall in one class, for both describers.
2. **The exchange comes out:** a confirmed pair of classes whose acts are plead and respond.
3. **Grouping does not bring out Propp's pairs:** at most one of the six comes out as a confirmed pair of classes with the pair's acts.

Each is reported HOLDS or FAILS; if 0 fails, 1 to 3 are void in meaning, as in the grouping by context.

## Checked before the freeze

`wordnetGroup.py selftest`: words sharing a first sense share a class (3 of 3 synsets with two or more such words); eight varied verbs (walk, eat, think, build, sing, sleep, buy, see) fall in eight classes.

## Reported, not judged

The classes with their members and uses (`WordNetClasses.txt`), every candidate pair of classes, and the confirmed pairs whose acts are none of the seven.
