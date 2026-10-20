# Oath, prayer and curse: the test of the candidate acts

**Frozen 2026-10-19 at the owner's word, before any of the eight plays is described.** Once frozen, a departure is logged in `Cand/KeeperLog.md`, not made here.

## The question

The genre model (`Genre/GenreModel.md`) lists acts Propp's catalog has no place for, not yet tested. The strongest came from the bottom-up test's free verbs: oaths and vows (promise, swear, vow), prayer (pray) and curse (curse), each 1% to 3% of the verbs in the 24 plays described, and near none in the tales.
Those figures were counted after the bottom-up test, on its data, so they cannot test themselves. This test asks whether they recur in plays no describer has described in free verbs.

## What is already known

From the bottom-up test's descriptions, counted by the keeper: the three together are about 1.15% of the verbs in the 45 tales, and 5.4% (describer B) to 6.7% (describer A) in the 24 plays, about five times as much.

## The test plays

**P01 to P08**, the eight plays of the 32 that no describer has described in free verbs: Rhesus, Heracleidae, Oedipus at Colonus, Ion, Hecuba, Antigone, Suppliants, Electra, with their event lists from the tragedy run. P01 to P04 have no cast list; their describers name characters as the text names them, as the rules allow.
**The instrument:** `Free/FreeRules.md` unchanged, fresh describers A (Opus) and B (Sonnet), two plays a batch (`g13` to `g16`), one cloud stage, `free-6`, in Propp-ActsRoles.

## The measures

A verb is read as `Free/free.py` reads it. **Oath:** promise, swear, vow. **Prayer:** pray. **Curse:** curse. Each is counted as a share of all the verbs a describer writes, in the eight new plays and in the 45 tales already described.

## The predictions

1. **The three together recur in tragedy:** in the eight new plays they are at least three times their share in the tales, for both describers.
2. **Each recurs:** each of oath, prayer and curse occurs in at least four of the eight new plays, for both describers.

Each is reported HOLDS or FAILS. If both hold, oath, prayer and curse enter the genre model as acts that mark tragedy, Propp's catalog having no place for them; if not, they stay candidates.

## Checked before the freeze

`cand.py` run end to end on synthetic descriptions of the eight plays in a scratch folder: setup, form check and scorer.

## Reported, not judged

Each candidate's share in the tales, the 24 plays already described and the eight new plays; its count in each new play; lament, mourn and weep together, in the new plays.
