# Splitting several-name fields: a draft rule (DRAFT 2026-10-26, NOT ADOPTED)

**Drafted 2026-10-26 at the owner's request, for review.** The code is in `characters.py` (`split_field`, `split_entries`, test `c7`). Nothing here changes the character table or `Spheres/explore.py`; each would change only at the owner's word, as an amendment to `CharacterProtocol.md` (section 8).

## The problem

A function's performer or undergoer field often names several characters, for example "Ivan-tsarevich; the witch", "the Lion, the Fox and the Ass" or "Zeus/Io". The name join that `Spheres/explore.py` uses, and that the protocol takes unchanged, makes one character of such a field. A shorter name whose words stand in the longer one then joins it too, so in A093 (transcriber A) Ivan and the witch become one character holding four spheres.

**How common.** Of the 34,908 non-empty function fields, enough hold several names that splitting them yields 36,762 names: 1,854 more.

| Corpus | Fields with `;` | Fields with `,` | Fields with *and* | Fields with `/` |
|---|---|---|---|---|
| Wondertales | 116 | 492 | 290 | 0 |
| Myths | 149 | 286 | 165 | 79 |
| Animal tales | 33 | 268 | 164 | 0 |
| Tragedies | 190 | 96 | 33 | 0 |
| Fables | 20 | 45 | 134 | 1 |

## The rule

1. **Drop notes in parentheses** first: "(unnamed; the labours are Eurystheus's)" and "Ulysses (with Helen)".
2. **Split** at a semicolon, a slash, a comma, or the word *and*. Each part that keeps a name after the stop words is one character's name.
3. **Leave *with* alone.** It mostly describes ("the man with firewood"), and where it joins two characters a comma usually stands before it ("Peleus, with Jason and the Dioscuri"), which rule 2 already splits.
4. **The parts are joined within the story** as `explore.py` joins names, unchanged. So "the Fox" in one field and "Fox" in another still meet.
5. **Crediting the function.** A field naming several characters does not say which of them performs the function. Three ways, for the owner to choose:
   - **(all)** every name in the field performs it;
   - **(first)** only the first name performs it, and the others are characters without the function;
   - **(none)** none of them is credited with it, and all are kept as characters; the function counts as performed by no character.

   A several-name undergoer field gives the function to each name as undergoer under all three.

## Test C7 (run 2026-10-26, PASSES)

- **No field loses every name** (0 fields), and **no name still holds a separator** (0).
- **For review, not failing:** 14 distinct fields split into a bare generic word, such as "Cepheus, Ancaeus and others", "Ivan, his men", "women and children" and "the land, cattle and people". As drafted, *others*, *people* and the like become characters of their own; they could instead be dropped.

## What the split would change, counted only (characters; characters holding both the hero's and the villain's sphere, full reading)

| Corpus, transcriber | Now | Split, all | Split, first | Split, none |
|---|---|---|---|---|
| Wondertales A | 691; 19 | 645; 29 | 645; 26 | 645; 18 |
| Wondertales B | 663; 33 | 682; 33 | 682; 32 | 682; 28 |
| Animal tales A | 267; 16 | 291; 19 | 291; 16 | 291; 14 |
| Animal tales B | 278; 10 | 286; 12 | 286; 11 | 286; 9 |
| Fables A | 556; 8 | 581; 8 | 581; 7 | 581; 6 |
| Fables B | 554; 8 | 585; 8 | 585; 7 | 585; 7 |
| Tragedies A | 829; 34 | 831; 36 | 831; 34 | 831; 33 |
| Tragedies B | 837; 33 | 843; 35 | 843; 34 | 843; 32 |
| Myths A | 1,150; 42 | 1,206; 47 | 1,206; 41 | 1,206; 36 |
| Myths B | 1,023; 47 | 1,069; 49 | 1,069; 44 | 1,069; 40 |

**What this shows.** Splitting alone does not remove the fusion; crediting every name raises it, because a joint struggle ("Ivan; the dragon" fighting) then gives the hero the villain's sphere. Even with no credit, the drop is small: one to seven characters in each corpus and transcriber. **A correction to the keeper's note of 2026-10-26:** several-name fields account for only a small part of the hero-villain fusion. Most of the gap between the full reading and the strict one comes from struggle being in the villain's sphere, which the strict reading already handles.

## For the owner

1. **Adopt the split or not.** If adopted, choose a way of crediting: (all), (first) or (none).
2. **Generic parts** (*others*, *people*): keep them as characters, or drop them.
3. **Where it applies:** the character table only, or `Spheres/explore.py` too. If Spheres, it would be regenerated, and C2 would compare against the new file.
