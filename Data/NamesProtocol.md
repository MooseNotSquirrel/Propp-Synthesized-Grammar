# The name stage: collection protocol (FROZEN 2026-10-26 AT THE OWNER'S WORD)

**Drafted 2026-10-26 for `CharacterProtocol.md`, decision 1 (a), and frozen the same day at the owner's word**, taken by the owner on 2026-10-26: names the WordNet rule cannot sort go to two readers. Like `Session7Protocol.md`, this stage collects a layer and tests no claim. This file fixes how the stage is set up and checked and what is reported, and it makes no prediction. The stage is cleared in Propp-ActsRoles `RUN.md` only after this file is frozen at the owner's word.

## What the readers get

- **Material:** every character in `tables/characters.tsv` whose kind the rule leaves unknown and that has a function-layer name. Recounted at the freeze, after the split of several-name fields was adopted (`CharacterProtocol.md` section 8), from the table as built on 2026-10-26:

  | Corpus | Rows (story, reader, character) | Items (story, character) | Distinct names |
  |---|---|---|---|
  | Wondertales | 220 | 131 | 91 |
  | Animal tales | 4 | 3 | 3 |
  | Fables | 34 | 26 | 14 |
  | Tragedies | 416 | 216 | 155 |
  | Myths | 892 | 498 | 371 |
  | **All** | **1,566** | **874** | |

- **One item per story and name**, the two transcribers' rows merged where they name the same character. Each item gives:
  - the story's identifier and title;
  - the character's names as the table gives them;
  - up to three of the story's events that name it, from `events.tsv`.

  The readers see no sphere, no role and no function code, so their answer about kind cannot draw on the role being measured.
- **Batches by corpus, at most 150 items a batch** (the counts recounted at the freeze):
  - `n1`: the wondertales;
  - `n2`: the fables and animal tales together;
  - `n3` and `n4`: the tragedies;
  - `n5` to `n8`: the myths.

  That is eight batches per reader. Within a corpus, items go in story order, split evenly across that corpus's batches. Reader A runs on Opus and reader B on Sonnet, as in every stage so far.
- **The control set:** 50 characters whose kind the rule does give, drawn from the same table by a fixed seed. They are spread over the eight batches, and each is placed at a seeded position among that batch's items. Which items are controls is kept on the keeper's side, in `Characters/NameControls.txt`, and is never copied to the readers' repository.
- **The task:** for each item, give one kind from *person*, *animal*, *deity*, *supernatural* (a being of the other world that is not a god: a witch, a monster, a spirit) or *object*, a confidence of high, medium or low, and a reason of one sentence. Answer from the story, not from general knowledge of the name.

## Form check

- **The answer file:** one line per item, in order, as `item | kind | confidence | reason`.
- **Each line:** a kind from the five, a confidence from the three, and a reason that is not empty.
- **Placeholders:** a placeholder or a speech number where an identifier belongs is recovered by order and checked, or flagged, as the act stages' check does.

## Reported, not judged

- **Agreement:** how often the two readers give the same kind, by corpus, and how often both give high confidence.
- **The kinds used** (`CharacterProtocol.md`): the kind where both readers agree. Where they disagree, the kind stays unknown and is counted as unknown.
- **The readers' kinds beside WordNet's** on a control set: 50 names the rule *does* sort, drawn by a seeded rule and mixed into the batches unmarked. Their agreement with the rule is reported as a check on the readers.

## Settled before the freeze

**The names found only in the act and free-verb layers.** As first drafted, the table made a character of every such name that joined no function name. The dry run of 2026-10-26 counts a great many of these in the wondertales: 580 and 375 characters from the acts alone, mostly Russian names the event join did not link, and 378 and 576 from the free verbs alone. Many are probably the same characters as function-layer ones, named differently. Of those with unknown kind, 951 wondertale rows and 52 animal-tale rows are Russian, and 245 rows across the corpora are English.

**Decided by the owner, 2026-10-26:** such names are set apart as unjoined, counted and not made characters (`CharacterProtocol.md` section 8), and their kinds are not collected. This stage takes only characters with a function-layer name, as drafted.

## Amendment at the owner's word, after the freeze

**2026-10-26, smaller batches.** The batches are cut smaller than the freeze said: each corpus group (the wondertales; the fables and animal tales together; the tragedies; the myths) is cut into as few batches of at most 75 items as hold it, numbered on across the groups. That gives:
- `n1` and `n2`: the wondertales;
- `n3`: the fables and animal tales;
- `n4` to `n6`: the tragedies;
- `n7` to `n13`: the myths.

That is thirteen batches per reader, twenty-six readers in all. With the controls (three or four a batch), the batches hold 33 to 76 items. Nothing else changes.
