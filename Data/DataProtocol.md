# The normalized data set: protocol (DECISIONS TAKEN; TESTS T1 TO T4 FROZEN 2026-10-21 AT THE OWNER'S WORD)

**Drafted 2026-10-21 at the owner's request, in two parts.** First, a full normalized data set for each corpus. Second, parity: whatever has been collected or measured for one narrative type should exist for each of them, so that the same analyses (functions, pairs and groups, character sets, and the rest) can be run on every corpus. Nothing here is built yet. The tests in section 5 are to be frozen before any builder is written.

## 1. Why: what the audit found

**There is no normalized data set for any corpus.** Every reading lives in the raw file its reader wrote, in seven repositories, and every study parses those files with its own reader code. Measured on 2026-10-21:

- **Each study carries its own list of paths.** `Model/model.py`, `Links/links.py`, `Ngrams/ngrams.py`, `Spheres/explore.py`, `Animal/layers.py` and about fifteen others each name the corpora's files by glob and parse them themselves.
- **The function code is not in one field.** It is the fifth field in the tale, fable and tragedy transcriptions and the sixth in the myths' (`Model/model.py`, `CORPORA`).
- **The ids are not one scheme.** Tales and animal tales both use `A` with Afanasyev's 1984 numbers (wondertales 93 and up, animal tales 1 to 50); fables `F`, plays `P`, myths `L1-001`. Nothing enforces that the two `A` ranges stay apart.
- **One describer renamed stories.** Describer B's act descriptions of six plays carry `S001` to `S00n` in place of `P17`, `P18`, `P21`, `P22`, `P27` and `P28`; the keeper's programs map them back (`TwoLayer/KeeperLog.md`, acts-2, "one recovery"). A naive count finds 18 plays with both describers' acts instead of 24.
- **Stories with more than one version.** The joint model keeps each story's first reading only; whether every program does the same is not checked.
- **The card is not one card.** The wondertales were transcribed under two cards (`U`, uncorrected, and `C`, corrected for refusals); the published analyses use `U`, the animal tales have only `C`, and the fables and plays have their own cards (`AesopRules.md`, `TragedyRules.md`).
- **The descriptions live in two places.** The animal tales' are copied to Propp-AnimalTales; every other corpus's acts, significance and free verbs live only in Propp-ActsRoles.

## 2. What exists, by corpus and layer

**Stories with the layer from both describers (A and B), counted from the files on 2026-10-21** (a scratch census; the builder's census in section 5 replaces it):

| Layer | Wondertale | Animal tale | Fable | Tragedy | Myth |
|---|---|---|---|---|---|
| Source texts and event lists | 45 | 50 | 201 | 32 | 299 units listed |
| Propp's functions | 45 | 50 | 198 | 32 | 126 |
| Role-free acts | 45 | 50 | 90 | 24 (18 by id, see above) | 0 |
| Significance | 44 | 50 | 86 | 24 | 0 |
| Free verbs | 45 | 50 | 90 | 32 | 0 |
| Hero, two readers | 45 | 0 (one lister's hero) | 198 | 32 | 0 |
| Hero, judged agreed | 40 | 0 | 158 | 27 | 0 |

Propp's own codes for his 45 tales (Appendix III, `TaleTokenStreamsV4Utf8.txt`) are a third reading of the same wondertales, in functions only.

**And by analysis, which corpora each has been run on:**

| Analysis | Wondertale | Animal tale | Fable | Tragedy | Myth |
|---|---|---|---|---|---|
| Function frequencies, order, placement (`Model/`) | yes | placed only | yes | yes | yes |
| Pairs: Propp's pairs as n-grams (`Ngrams/`) | yes | no | yes | yes | no |
| Links at a distance (`Links/`, `Genre/`) | yes | pursuit-rescue only | yes | yes | yes |
| Groups: Propp's blocks (`Blocks/`, `Genre/mythOrder.py`) | yes | no | yes | yes | order only |
| Spheres of action (`Spheres/`, exploratory) | yes | no | yes | yes | yes |
| Heroes and hero types (`Heroes/`) | yes | no | yes | yes | no |
| Problem structure (`Problems/`, `Animal/layers.py`) | yes | yes | yes | yes | no |
| Free verbs, the bottom-up test (`Free/`) | yes | reported | yes | yes | no |
| Values (`Values/`, exploratory) | yes | no | yes | yes | no |

## 3. The data set

**One builder, `Data/build.py`, reads the raw files and writes the tables; the raw files stay untouched as the record.** The tables are UTF-8, LF, tab-separated, one row per item, with a header row. They live in `Data/tables/` and are regenerated, never edited by hand.

- **`stories.tsv`:** `story` (the global id, section 4), `corpus`, `genre`, `local_id` (as the raw files spell it), `source` (repository and path of the text), `language`, `title`, `events` (count).
- **`events.tsv`:** `story`, `event`, `text`, `lister`.
- **`functions.tsv`:** `story`, `reader` (A, B, or Propp), `model`, `card` (U, C, Aesop, Tragedy, Myth), `version`, `move`, `event`, `position`, `function` (base code, or X), `negative`, `raw` (the field as written).
- **`acts.tsv`:** `story`, `reader`, `model`, `event`, `entry`, `act`, `performer`, `undergoer`, `relation`, `matters`, `link`, `unsure`, `note`.
- **`significance.tsv`:** `story`, `reader`, `model`, `entry` (the act it describes), `part`, `value`, `place`, `problem`, `link`, `target`, `unsure`.
- **`problems.tsv`:** `story`, `reader`, `problem`, `text`.
- **`free.tsv`:** `story`, `reader`, `model`, `event`, `entry`, `verb`, `performer`, `undergoer`, `matters`, `unsure`, `note`.
- **`heroes.tsv`:** `story`, `reader` (A, B, lister, judged), `hero`, `basis`.
- **`census.txt`:** every raw file read, its line count, rows kept and rows dropped with the reason.

**What is decided in the tables, and what is left to the analysis.** The tables keep every version of a story and every card, marked; they decide nothing an analysis decides. An analysis chooses its version and card by a filter, and states it.

## 4. Ids

**Every story gets one global id, `<corpus>:<local id>`:** `tale:A093`, `animal:A001`, `fable:F127`, `tragedy:P17`, `myth:L1-001`. The local id is the one the raw files use, so every published figure can still be traced. A describer's private ids (the `S00n` plays) are mapped in one table, `Data/aliases.tsv`, with the source of each mapping, and nowhere else.

## 5. Tests, to be frozen before the builder is written

**T1, nothing lost.** For every raw file, the rows kept plus the rows dropped equal its lines, and every dropped row is a blank line, a heading or a comment. Any other drop fails the build.

**T2, the form checks agree.** For each stage, the entries per describer and batch in the tables equal what the stage's form check printed when it was merged (the keeper logs and the stage programs' `form-*` commands, rerun).

**T3, the published figures come back.** The programs named here are given a table-backed reader in place of their own, and their run files must come out identical, byte for byte, to the committed ones:
`Model/ModelRun.txt`, `Links/LinksRun.txt`, `Ngrams/ConfirmRun.txt`, `Problems/ProblemsRun.txt`, `Free/FreeRun.txt`, `Heroes/HeroRun.txt`, `Animal/AnimalRun.txt`, `Animal/AgreementCheck.txt`, `Animal/LayersRun.txt`.
Where a program's output differs, the difference is attributed before anything is changed: either the old reader or the table is wrong, and the finding says which.

**T4, the ids hold.** No global id repeats; every id in every layer table is in `stories.tsv`; every alias is used.

## 6. Parity: what would fill the gaps

**Two kinds of gap, with different costs.** Analyses not yet run on a corpus whose data exist cost only program time once the tables stand. Layers not yet collected cost new reader stages.

**Analyses to run on data that exist (no new readers):**
- The animal tales: pairs as n-grams, the links, the blocks, spheres, values.
- The myths: pairs as n-grams, the blocks beyond their order.

**Layers to collect (new reader stages, each frozen first like the others):**
- **Animal tales, heroes by two readers:** 50 stories, one small stage.
- **Fables:** none; the 90 described fables are the sample (decision 2).
- **Tragedy, acts and significance for the 8 plays without them** (P01 to P08, which have functions and free verbs): two stages.
- **Myths:** none for Apollodorus (decision 1); the next ancient corpus gets every layer from the start.

## 7. Decisions, taken by the owner on 2026-10-21, each as recommended

**1. Whether to fill the myths. DECIDED: Apollodorus is not described further; a better ancient corpus will be found, and Apollodorus may be returned to if needed.** The queue already judges Apollodorus "a chatty handbook" and seeks a better ancient source. Recommendation: do not describe Apollodorus further; give the next ancient corpus every layer from the start, and mark myth's gaps as such.

**2. Whether the fables are filled to all 198. DECIDED: the 90 described fables stand as the sample.** Recommendation: stand on the 90, which were drawn by rule, and say so; fill only if an analysis needs the held-out fables.

**3. Which card is the wondertales' reading for comparison with the animal tales. DECIDED: the corrected card, `C`.** Both exist for the wondertales; the animal tales have only `C`. Recommendation: keep both in the tables, leave every published figure on `U` as frozen, and compare the animal tales with the wondertales on `C`.

**4. Whether the tables become the only reader. DECIDED: yes, and the parity rule below is approved.** Recommendation: yes, once T1 to T4 pass: new programs read only `Data/tables/`, and old programs are moved over one at a time, each passing T3.

**The parity rule, going forward:** a new corpus is not called collected until it has every layer in section 3, and a new analysis is not called done until it has been run on every corpus that has the layers it needs.
