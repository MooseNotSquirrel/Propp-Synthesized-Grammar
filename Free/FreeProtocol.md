# Acts in the describers' own words: the bottom-up test

**Frozen 2026-10-14 at the owner's word, before any description under it.** Once frozen, a departure is logged in `Free/KeeperLog.md`, not made here.

## The question

The frequency analysis (`Ngrams/`) found six of Propp's pairs standing out unaided in acts described without his notation: interdiction and violation, reconnaissance and delivery, trickery and complicity, test and reaction, struggle and victory, task and solution; and a pair of its own, the request and its answer.
But the list of acts the describers chose from was made by taking the roles off Propp's functions, so it divides acts where he did: struggle and victory are two acts because they are two of his functions.
This test removes the list. Describers say what is done in one plain everyday English verb of their own choosing, and the question is whether Propp's units and pairs come out of their verbs.

## The instrument

**The rules:** `FreeRules.md`, written from the act rules with the list of acts and relations removed. Each act gets one plain English verb in its base form, the commonest everyday verb that says what is done, in the active voice, with a phrase of up to six words; its performer and undergoer; and whether it matters. Their examples use only everyday verbs (kill, ask, give, sell, buy); words for kinds of story events and for characters' parts are forbidden.
**The describers:** fresh instances, A on Opus and B on Sonnet, blind to each other and to every earlier transcription.
**The stories:** the 159 of the two earlier act tests, 45 tales, 90 fables, 24 tragedies, with the same event lists, so each free description sits beside the act description of the same event. The event lists came from listers whose rules file held Propp's definitions card; that limit stays.
**Five stages** in Propp-ActsRoles, each in a fresh cloud session: `free-1` the tales, `free-2` the fables, `free-3` to `free-5` the plays, eight describers each.

## The measures

**The verbs:** the first word of the verb field, lowercased; an initial "to" dropped.
**Clean events:** those with exactly one free entry and exactly one act entry from the same letter's act describer; there a verb and an act describe the same act.
**The units:** for each of the six pairs, in clean events whose act is one of its halves, how well the verb tells which half: each token's half is guessed from the other tokens with the same verb, and the gain is (accuracy − chance) / (1 − chance), chance being the larger half's share. The halves are **apart** for a describer when the gain is at least 0.5 over at least 10 tokens.
**The pairs:** the frequency analysis's discovery and confirmation, unchanged (`Ngrams/ngrams.py`: the same halves of the stories, within-story shuffles, both describers in both halves), run on the verb strings. A verb's act is the act it meets in at least half of its clean events, given at least 5; a confirmed pair of verbs counts for a pair of acts when both describers' verbs map to that pair's acts.

## The predictions

1. The describers' own verbs keep apart the halves of at least four of the six pairs, for both describers.
2. At least four of the six pairs come out as a confirmed pair of verbs whose acts are the pair's.
3. The request and its answer (plead, respond) comes out so.

Each is reported HOLDS or FAILS; there is no overall verdict. Together they say whether Propp's units and pairs are found in the stories by readers given no units at all.

## Checked before the freeze

`free.py score` on two sets of synthetic descriptions of the same events, in a scratch folder: describers who give each act one of two synonyms pass all three predictions (gain 1.00 on every pair); describers who pick verbs at random fail all three (gain 0.00). A first criterion, accuracy of at least 0.8, counted a pair as apart under random verbs when one half was nine tenths of its events; it was replaced by the gain over chance before anything was described.

## Reported, not judged

Each describer's vocabulary: its size, the verbs used once, the forty commonest with the act each meets most often; the verbs written for each half of the six pairs; every candidate pair of verbs, confirmed or not, with its distance profile and its acts; and the confirmed pairs of verbs whose acts are none of the seven.
