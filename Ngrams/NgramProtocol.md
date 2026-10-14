# Frequencies of functions and acts: the analysis

**DRAFT, 2026-10-14, to be frozen at the owner's word, before any pair or n-gram is counted.** Once frozen, a departure is logged in `Ngrams/KeeperLog.md`, not made here.

## The questions

The owner's proposal (2026-10-13): count the frequencies of sequences in the strings already transcribed, as word frequencies are counted in language, and see whether Propp's pairs stand out, whether new pairs appear, how pairs with other functions between their halves behave (struggle and victory, task and solution), and whether frequent items frame the narrative while rare ones carry what is particular.
1. **Pairs.** Which ordered pairs of functions, and of acts, follow each other more often than chance, next to each other or a few places apart; and do Propp's pairs stand out among them unaided?
2. **Distance.** For each pair that stands out, how its strength changes with the distance between its halves.
3. **Frequency and information.** Whether the strings' sequences are more predictable than shuffled strings, and whether rare items belong to one genre beyond chance while frequent ones are shared.

## The strings

**Function strings:** the original transcriptions under Propp's functions, in text order, X and α left out, a negative result kept as its own token (F−): the 45 Russian tales (Propp-Afanasyev, arm U), the 198 fables (Propp-Aesop and Propp-Fables), the 32 tragedies (Propp-Tragedy); transcribers A (Opus) and B (Sonnet) apart. About 3,600 tokens each, 44 kinds.
**Act strings:** the act transcriptions under `ActsRules.md`, in text order, `other` left out: the 45 tales, 90 fables and 24 tragedies of the two-layer and problem-structure tests; describers A and B apart. About 5,600 tokens each, 36 kinds.
**What the act strings are and are not free of.** Their describers were never told of Propp, his functions or the definitions card, and classed each act whoever did it; but the list of acts was made by taking the roles off Propp's functions, adding a few acts found in the stories (threaten, plead, lament), so it divides acts where he did, and the event lists they worked on came from listers whose rules file held the card. A pair of acts standing out shows that the stories put those acts together; it cannot show that the units are natural, and a pair can appear only among acts the list names.

## The split

Within each genre and layer, the stories are sorted, shuffled with seed 46, and halved; the first half is for discovery, the second for confirmation. Nothing from the confirmation half is read before the candidate list is committed.

## The statistic

For an ordered pair x, y and a distance d, the count of places where y stands d places after x in the same story. The null shuffles each story's tokens within the story, 1,000 times (seed 46), keeping each story's contents and length; the lift is the count over the null's mean, and p is the share of shuffles with a count at least the observed (plus one, over 1,001). Two classes: **adjacent** (d = 1), and **near** (d = 2, 3 or 4, summed).

## Discovery and confirmation

**A candidate:** on the discovery half, for both transcribers, a count of at least 5, a lift of at least 1.5, and p at most 0.01; pairs of a token with itself are left out. `ngrams.py discover` writes the list to `Candidates.txt`, which is committed before `ngrams.py confirm` runs.
**Confirmed:** on the confirmation half, for both transcribers, a lift above 1 and p at most 0.05, in the class it was found in.
**The distance profile** of each candidate on the confirmation half: the lift at distances 1 to 6, the mean of the two transcribers; it is adjacent if it peaks at 1, spaced if it peaks further out, long if the lift is still at least 1.5 at 6.
**Chance:** about 1,900 ordered pairs of functions and 1,300 of acts, in two classes; requiring both transcribers in both halves keeps chance confirmations to about one. `ngrams.py selftest` plants an adjacent pair and a pair two apart in random strings with independent filler for each transcriber and half: both are found and confirmed with the right shapes, and the two chance pairs that pass discovery fail confirmation.

## Propp's pairs

Among the functions, the pairs the v46 grammar's blocks and the move's frame bind: γ δ, ε ζ, η θ, D E, E F, H I, Pr Rs, M N, A K, a K, Q Ex, Ex U.
Among the acts, their counterparts: forbid disobey, seek-information reveal-information, deceive be-taken-in, test respond, respond give, fight win, pursue escape, set-task do-task, harm repair, want repair, recognize expose, expose punish.

## The predictions

1. At least half of Propp's pairs that occur at least 5 times, adjacent or near, for both transcribers in the confirmation half are confirmed among the functions.
2. At least half of their counterparts, so counted, are confirmed among the acts.
3. At least one pair of acts is confirmed that is not a counterpart of Propp's pairs.
4. On all the stories, the next token is more predictable than in shuffled strings (the entropy of the next token given the current one, 200 shuffles, p at most 0.05), in every genre and all together, for both layers and transcribers.
5. The owner's hypothesis: tokens and adjacent pairs seen at least 3 times are ranked by frequency; a token's over-representation in its most common genre is measured against 200 reassignments of the genres among the stories; the rarest third is more over-represented beyond chance than the commonest third, for single tokens and pairs, both layers and transcribers.

Predictions 1 to 3 are scored by `ngrams.py confirm`, 4 and 5 by `ngrams.py describe`; each is reported HOLDS or FAILS, and there is no overall verdict.

## Reported, not judged

All candidates with their discovery figures; every candidate's confirmation figures and distance profile, confirmed or not; the slope of rank against frequency for single tokens, pairs and triples, real and shuffled; the entropies; the over-representation figures.
