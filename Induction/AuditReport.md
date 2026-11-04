# The audit of the failed self-test: report (2026-11-04)

**The verdict stands.** The self-test of `InductionProtocol.md` FAILS for both transcribers. Nothing here replaces it, and nothing here is a pass. The plan and its fixed readings are in `AuditPlan.md`; the figures are in `Audit-u0.txt` to `Audit-u6.txt` and `Audit-prep.txt`, from `audit.py`.

**What was not blind.** The keeper knew the self-test's figures and the n-gram study's result before the plan. U6 and the preparatory count were added after earlier parts were read, and are labelled so. U4 is exploratory and many.

## The short answer

The one word FAILS covers three different things.

| Bar | What the failure means | Main evidence |
|---|---|---|
| **S1,** sections | **A real finding about the strings.** The tool had the power to find sections with a strict order at this size, and the real strings did not give them. | S1 holds in 20 of 20 corpora with a strict order (U6b). Real ARI 0.008 and 0.157; every one of the 40 generated corpora is higher, the lowest 0.207. |
| **S2,** order | **An instrument that could not pass.** It says little about order. | S2 holds in 0 of 40 generated corpora, sections true and order strict included. By mean position the same strings show order at p 0.007 and 0.002. |
| **S3,** pairs | **A design choice.** | Any-distance recall 0.20. Adjacent recall 0.67 (6 of 9), a bar this choice would have met. |

## The six explanations, by the readings fixed beforehand

**1. A fault in the code: does not stand.** U0 reproduced the record's K, sections and relations. Plain-loop counts matched for every pair.

**2. The bars could not be met: for S2, stands; for S1, does not, with a qualification.**
- **S2:** at sixteen times the size the order test reached at most 0.487 under U1's chain. Under the strict chain A reached at most 0.567, and B reached 0.6 in 3 of 5 (at most 0.624). So the bar is out of reach or barely in reach at sixteen times the real data.
- **S1:** with real places, 56 to 75 of the 84 to 126 mergings at K of 4 to 6 reach tau 0.6, so the U5 reading is not withdrawn.
- **The qualification:** Propp's ten sections handed over exactly would have FAILED S1 on the readers' strings (tau 0.429 and 0.423; ARI 1.000). The record's taus were 0.42 and 0.44. U5 as first run hid this, because it ranked by Propp's index and not by place.

**3. Underpowered: stands, in the strong form, for the two bars together.** S1 and S2 together hold in 0 of 20 corpora under U1's chain and 0 of 20 under the strict chain. The self-test could not have passed even had Propp's order been strictly true. S2 is what makes that so:
- With the readers' transitions, S1 holds in 2 of 20.
- With a strict order, S1 holds in 20 of 20 (ARI 0.82 and 0.78; tau 0.86 and 0.87).

**A limit on that:** the generators have order between sections only, none inside them, and the strict chain's moves are shorter (5.9 and 6.4 units against 8.8 and 10.8). They give 0 to 10 relations where the real strings gave 18 and 36. So S2's power may be understated. It is not shown to be zero, only unshown at any size near the real one.

**4. The transcriptions: loses as the account of the failure; a difference remains.** By the fixed rule, Propp's own strings fail S1 and S2 too (ARI 0.056; order tau 0.426), so the readers' strings alone are not the cause. But they do not fail alike:
- Propp's strings hold S3 (0.57), reach state-section tau 0.737, and give mean-position order 0.824 against 0.376 and 0.431.
- They run 16.6 units a story against 28.9 and 32.0, and 1.87 moves against 3.18 and 2.87.
- A and B stand 0.40 apart story by story, and each about 0.70 from Propp, where another story is 0.83. The readers agree with each other far more than with him.
- A higher order in Propp's strings does not by itself favour them. He coded his tales with his scheme in hand, and the keeper cannot separate that from noise in the readers.

**5. The strings do not carry his sections: split.** True sections against random partitions: A above 99.78% (carries), B above 85.18% (does not), Propp's own above 89.75% (does not). The best random partition beats the true sections in all three. The rule asks for A and B together, so it neither gains nor falls. This measure's own power was not tested.

**6. A design choice: gains for S3.** Recall is 0.67 by the adjacent class; all of it is adjacent, and the near class confirmed none for A and B. Other choices did not rescue S1: K 10 free and forward-only all fail for A and B. Mean position beats Copeland for S2 on every string set, but A and B stay at or below 0.52.

## The finding the plan did not anticipate: the preparatory units

In the readers' strings Propp's first section stands in the middle of the move, at mean place 0.54 and 0.55, after the complication at 0.20 and 0.26 (U6a).
- **80% of A's preparatory units (192 of 241) and 87% of B's (246 of 282) come after the first A or a of their move.** Only 15 moves in each opens with one (`Audit-prep.txt`).
- **With them removed, S1 holds for both** (ARI 0.220 and 0.188; tau 0.766 and 0.754; U4d). One exploratory figure among many, but the only change that did this for A and B.

**Why is not known.** It could be how the readers label moves (a later move's preparation filed in the move before), how they use the symbols, or the tales themselves. `resolved.tsv` has no preparatory units to compare. Nobody has read the moves yet.

## An interpretation, not a result

Real ARI lies under every generated corpus, and on Propp's own strings the tool splits his sections into ordered runs (`A a` / `B` / `C` / `up` / `D o` / `E L` ...). Bigrams far outpredict the section chain on those strings (−1.72 against −2.49). This suggests that an HMM state, a set of interchangeable functions, is the wrong shape for a Propp section, which has an order inside it. If so, ARI against the ten sections was the wrong target. It is the keeper's reading and nothing here tests it.

## What this does to the other runs

- **The 11 other induced grammars:** K and sections should not be read as findings about those corpora. K is pulled low at this size (3.4 and 4.4 where 10 are true; 10 is reached only near four times the size), and those corpora are mostly smaller. That sections replicate poorly between transcribers is partly what low power would give. Their "unverified" label is now too mild.
- **Order relations:** few, but they held on checking. Those stand as counts.
- **The n-gram study's adjacent pairs:** supported here.
- **The fortune arcs:** they do not read function order. Unaffected, and not rechecked.
- **Anything assuming the preparatory units open the move.** The programs that handle the functions layer are named here because they read these strings (a text match, none of them rechecked): `Animal/agreement.py`, `Animal/animal.py`, `Blocks/parity.py`, `Characters/characters.py`, `Characters/measures.py`, `CrossCulture/crossCulture.py`, `FailedHero/failedHero.py`, `Links/links.py`, `Model/model.py`, `Ngrams/ngrams.py`, `StoryGrammar/storyGrammar.py`, `StoryGrammar/exploreConcordance.py`, `StoryGrammar/predict34.py`.
- **The story grammar:** its stories outscoring their shuffles agrees with the order found here. Whether that order is Propp's in particular remains the open question of step 6's E2. **The E2 prediction is no longer fully blind:** U3 is a related measure, and it came out split. The frozen prediction stands unchanged, and this should be said when it is read.

## What a modified tool would need (none adopted)

Each is a lead from seen data, and would need its own protocol frozen by the owner:
1. **Power simulated before the freeze,** with the bars set from it. I1's planted grammar was too easy and nothing tested the bars. That was the keeper's design fault.
2. **Order by mean position,** tested against shuffles, not Copeland ties against a fixed 0.6.
3. **Pairs by the adjacent class.**
4. **The preparatory units handled by a stated rule,** once it is known why they stand where they do.
5. **A state shape that allows order inside a section,** or a target other than ARI against the ten sections.
6. **Unseen stories.** The wondertales and Propp's strings have been seen, and so have the other corpora's outputs. Validation would likely need new tales transcribed by readers.
