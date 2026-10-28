# G1 failed: a draft amendment for the owner's review (2026-10-28; nothing changed yet)

## What happened

`storyGrammar.py g1` planted shared weights drawn from a normal of spread 3 on the 80 features. It drew stories from each of transcriber A's fitting stories and its 100 alternatives in proportion to exp(−w · f), five draws each, and fitted.

- **Result:** a rank correlation of 0.774, short of 0.9, with 52 of 56 signs recovered. **G1 FAILS.**
- **The other tests pass:**
  - G2: the three published constraint-grammar weight files are reproduced line for line.
  - G3: 74 (A) and 77 (B) held-out stories were changed by the noise, and the weights were identical.
  - G4: two fits were byte-identical.
- **Not done:** no fit has been read, and `run` has not been run.

## Why (from a diagnostic in the keeper's scratch, on the planted data only)

The planted weights that were missed belong to constraints that hardly ever differ between a story and its alternatives. For example, "transfer before arrival and claims" changes by 0.0004 on average, against 0.27 for "outside blocks". A weight planted there leaves almost no mark on which sequence is drawn, so no fit could recover it.

The fixed L2 penalty then pulls those weights toward zero. On the raw scale it acts most strongly on exactly these constraints.

- More draws help only partly: 40 a story gave 0.891.
- The fault is in G1's planted design, and in the features' unequal scales. It is not in the fitting engine, which G2 shows reproduces the frozen grammar exactly.

## The amendment proposed (recommended)

1. **Standardise each feature** by its spread over the fitting contrasts: the root mean square of alternative-minus-story, per transcriber, computed on the fitting stories only. The L2 penalty of 1.0 then treats every constraint alike.
   - Weights are reported per unit of that spread, and also converted back to the raw scale.
   - G2 is unaffected: it reproduces the constraint grammar with that grammar's own unscaled design.
2. **Plant G1's weights in those units,** each drawn from a standard normal, so that every planted constraint has an effect of comparable size.
   - The criterion stays as frozen: a rank correlation of at least 0.9.
   - Signs are judged on the planted weights of at least 0.5 in size.

**Tried once in scratch, on the same planted data:**
- rank correlation 0.951, signs 48 of 49 at five draws a story;
- 0.960 and 48 of 49 at twenty draws.

**One sign is still missed.** Rather than move the threshold to pass it, the draft offers two choices:
- (a) signs judged at 1.0 or more in size;
- (b) at least 95% of the signs at 0.5 or more.

**Recommended: (b).** It is stated before the amended test is run.

## The alternative

Keep the raw scale, and judge G1 only on the constraints whose spread is above a threshold. This leaves the model as frozen, but the threshold would be chosen after the failure was seen. It also leaves the penalty uneven across constraints in the real fit.
