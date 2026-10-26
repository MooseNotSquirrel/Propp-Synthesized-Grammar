# Session 7: the reader stages, collection protocol (DRAFT, NOT FROZEN)

**Drafted 2026-10-26 for `Plan.md` session 7.** These stages collect layers the parity rule requires (`DataProtocol.md`, decision 4); they test no claim, so the protocol freezes how they are set up and checked, and what is reported, and makes no prediction. Each stage is cleared in Propp-ActsRoles `RUN.md` only after this file is frozen at the owner's word.

## Run 1

**Stage `animal-heroes`: the animal tales' heroes by two readers.**
- **Material:** the 50 tales' event lists and titles, from the normalized tables and Propp-AnimalTales, in two batches of 25 (`heroes/stories/ah1.txt`, `ah2.txt`), in the format of the earlier hero stage.
- **Prompts:** `Heroes/heroes.py`'s own prompt, unchanged but for the batch, its count and the reader (`hero-A-ah1` to `hero-B-ah2`). Reader A on Opus, B on Sonnet, as before.
- **Form check:** each answer file has one line per story, in order, with a hero, a confidence of high, medium or low, and a reason.
- **Reported:** how often the two readers name the same hero. Agreement is reported twice: by `Heroes/withJudgedHeroes.py`'s word rule, unchanged; and by the same rule with its stop list's role words (*man*, *woman*, *son*, *daughter*, *old*, *young*, and the like) kept, since that list hid agreed heroes in five stories (`KeeperLog.md`, 2026-10-25). The animal tales' heroes are often named by role alone ("the Fox", "the old man"), so the first count will undercount. Neither count is a verdict; the judged heroes for the animal tales are those both readers name, as the readers name them.

**Stage `held-acts`: acts for P01 to P08.**
- **Material:** the eight plays already under `held/tragedy/plays/` (each one's `Events.txt` and `Text.txt`, byte for byte the copies in Propp-Tragedy, checked), with the cast lists of P05 to P08 copied beside them.
- **Prompts:** the act stages' prompt (`prompts/pacts-A-g5.txt`), unchanged but for the paths, the plays and the reader; two plays a batch, `g13` (P01, P02), `g14` (P03, P04), `g15` (P05, P06), `g16` (P07, P08). **One difference, recorded:** P01 to P04 have no cast list, so their prompts tell the describers to name performers and undergoers as the text names them, where the others name them as the cast list does.
- **Form check:** `Problems/problems.py`'s act check, unchanged in what it requires: every listed event has an entry, every act and relation is from the lists, every entry is marked Y or N, and a speech number written where the play belongs is recovered by the batch's two plays and checked, or flagged.

## Run 2, set up after run 1 is merged and in form

**Stage `held-sig`: significance for P01 to P08.** Inputs written from run 1's act descriptions and the plays' judged heroes, as `Problems/problems.py`'s `setup-sig` writes them; its prompt and form check unchanged.

**Stage `five-sig`: significance for the five stories that lack it** (A098, F043, F060, F114, F124), with the heroes their readers gave, at the owner's decision of 2026-10-25; inputs written from their existing act descriptions as `Significance/significance.py` writes them; its prompt and form check unchanged; one batch per reader.

## After each run

Merge, run the form checks, add the new folders to `Data/build.py`, rebuild the tables, and rerun T1, T2 and T4; then regenerate `Data/Parity.md` section 1 from the tables. A failed or partial subagent is recorded, as `RUN.md` says, and not rerun without the owner's word.
