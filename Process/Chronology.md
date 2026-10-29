# Chronology: what was done, in order, and why

**Built 2026-10-20 from the commit records of the ten repositories, the keeper logs and the queue.** Dates are commit dates. Each step gives its question, why it came then, what it found, and where it lives. Results are stated as the frozen tests gave them; the keeper's readings are marked as such in the files named.

**The aim, as the owner put it on 2026-10-19:** an honest account of the story language people learn by hearing stories, as they learn their native tongue; Propp's model is its first example.

## Before 2026-09-12: the first project, in the web Projects interface

**Propp's own data made exact.** Appendix III's 45 tales and 84 moves transcribed into a grid (`PublicationGridMaster.txt`) and token streams, every cell checked against the printed page.
**Grammars of Propp's order.** v43 and v44 in EBNF, v44 frozen and falsified against the 84 moves (`FalsificationResult.md`); v45C, a competence grammar that marks rather than rejects (`CompetenceResult.md`: the tight pairs H–I, M–N and Pr–Rs unbroken in Propp's own moves, J–Q marked).
**A record kept as rulings and findings** (`ProppRulings.md`, `ProppFindings.md`), the queue as the handoff between sessions.

## 2026-09-12 to 09-27: the record, and readiness to publish

**09-12:** the work moves to Claude Code and git.
**09-13 to 09-26:** the record levelled (locators as content anchors, struck text deleted, the one-sentence-per-line reflow), then the clarity rework of all fifteen published files, each approved by the owner (ruling 99).
**09-27:** copyright decided by the owner for publication; publication then held back while the second project began.

## 2026-09-27 to 09-29: the second project and its grammar

**Why:** v44's failures on Propp's own moves showed what a better grammar of his order needed.
**09-27:** v46 built in eleven steps, test first (`StepTests.txt`, `runSteps.py`): context-free and LL(1), accepting 80 of 84 moves and 41 of 45 tales. Its semantic catalog drafted (`SemanticCatalog46.md`).
**09-29:** step 12, the groups' permanent names.

## 2026-09-28 to 10-06: Propp's model tested on other genres

**Why:** to see whether Propp's morphology holds beyond the Russian wondertale.
**09-28 to 09-29, Greek myth (Apollodorus):** the claim fails: coverage 57% to 70%, acceptance low, order little better than shuffled (`Story Language/Projects/Apollodorus`).
**09-29, Aesop's fables:** the claim fails; the fable's kernel is want, trick, complicity, harm (`Story Language/Projects/Aesop`).
**09-29 to 10-06, Greek tragedy, 32 plays:** run one play at a time, sealed until the model was frozen; the tragedy order model holds on unseen plays, about twice as strong as Propp's; tragedy covers far fewer events with Propp's functions (`Tragedy/`).
**09-30, blocks:** Propp's pairs and groups are told together beyond chance in every genre (`Blocks/`); the fable grammar fails its held-out test on coverage while its order holds; the claim that order inside a block is near obligatory withdrawn (the definitions card fixes it).

## 2026-10-03 to 10-06: is the instrument sound?

**Why:** the genre failures meant nothing until the instrument was checked on Propp's own tales.
**10-04 to 10-05, the Afanasyev calibration:** the 45 tales Propp analysed, read in Russian by the same instrument: partly calibrated, reading the tale but agreeing with Propp less than the transcribers agree with each other (`Calibration/`). An improvement test not adopted. The owner's human benchmark of five tales.
**10-05 to 10-06:** a section grammar (Propp's order suffices for the tales); a constraint grammar, one soft grammar for every genre (holds for tales and tragedy, fails on fables); the genre order test (only tragedy has an order of its own); a paper drafted (`Calibration/Paper/`).

## 2026-10-06 to 10-12: what Propp's list lacks

**Why:** the events Propp's functions leave empty might hold devices his list misses.
**10-06 to 10-11, the X study:** of sixteen candidate acts, only threats and demands recur by the frozen threshold; the others are Propp's functions with other roles (`XStudy/`). Trickery measured: mostly after the villainy.
**10-12:** the FailedHero, falling by unrepaired villainy in about one tragedy in five; judged heroes, readers agreeing almost always in tales, less in fables and tragedy (`Heroes/`).
**10-12, a catalog of role-free acts and relations:** describes more than Propp's functions and is agreed on better, but cannot recover them (`TwoLayer/`). **The owner's decision, option B:** the act catalog becomes the primary instrument.
**10-12, delivery:** two packages built for SourceForge and the publication gate cleared (`Story Language/Delivery`).

## 2026-10-13 to 10-14: meaning and genre with the act catalog

**10-13, the significance layer:** a layer of each act's meaning for the hero and the story's problems, reliable between readers, does not recover Propp's functions: what transcribers share is largely the card's conventions (`Significance/`).
**10-13 to 10-14, the genres' problem structures:** distinct (10 of 11 predictions), once length is removed: the tale's trouble comes from outside and is put right, the fable's hero brings it on, tragedy's trouble outruns repair (`Problems/`).
**10-14, the owner's frequency analysis:** Propp's pairs stand out unaided in his notation and in acts described without it; one pair of the stories' own, the request and its answer (`Ngrams/`).

## 2026-10-14 to 10-19: the devices without Propp's vocabulary

**10-14 to 10-19, the bottom-up test:** readers given no list of acts name the first half of each pair with a verb of its own and the second only as whatever act completes it: Propp's pairs are relations, not pairs of act types (`Free/`).
**10-18, a new catalog:** the owner's outline of the pairs and groups Propp names, with meanings carried from the old catalog (`ProppPairsAndGroups.md`); v46 left as the tested grammar.
**10-19, the links at a distance:** the tight links near certain in every genre, the frame links (villainy to liquidation, departure to return) loose and weakest in tragedy and fable (`Links/`).

## 2026-10-19: a model of genres, and its first tests

**The model stated:** a shared core of relations and each genre's settings (`Genre/GenreModel.md`).
**Tested on myth:** the core holds and myth's frame closes as seldom as tragedy's; that myth is set like tragedy fails, and a retest on the order of the blocks fails too: a genre's settings are separate dimensions (`Genre/`).
**The owner's steps in order:** the free verbs grouped (by context, degenerate; by WordNet, the exchange still the one pair; `Group/`); oath, prayer and curse confirmed as tragedy's own devices on eight unseen plays (`Cand/`), entered in the catalog with the threat and the exchange.

## 2026-10-20: the aim stated, the long-term question set

The owner's aim recorded, and the long-term question: is the catalog and model valid across other cultures, measuring overlaps and differences alike. Queued: Shakespeare, Dundes's corpus, a better ancient source, corpora outside the Indo-European family, the harmony hypothesis, and these process documents.

**10-20, Afanasyev's animal tales, the first new corpus:** the 50 tales Propp left out, fetched from Russian Wikisource, listed and transcribed in Propp-ActsRoles because cloud sessions open only there, and kept in Propp-AnimalTales. The frozen instruments' four predictions, scored: placement as fable fails (the transcribers split, fable and tale), hero and villain fused no more than in the wondertales, liquidation below the tale-fable midpoint holds, the tight links not tested. A check of the transcribers' agreement found it ordinary but A marking a third more functions a tale (`Animal/`).

**10-20 to 21, the animal tales' follow-ups:** the reading that the transcribers' split on placement follows how much A marks was frozen as a test and failed, and withdrawn (`Animal/LengthProtocol.md`). The tales were then described afresh in role-free acts, free verbs and significance, the three stages run in a local session moved into Propp-ActsRoles and copied to Propp-AnimalTales; the frozen layers test held one of four predictions, the hero opening the trouble as in the fable, while repair and the acts' value for the hero differ from the tale only as far as length gives (`Animal/LayersProtocol.md`, `LayersRun.txt`).

## 2026-10-21 to 25: one data set, one catalog, and parity

The owner asked whether each corpus had a full normalized data set; none had, every study reading the raw files with its own parser. A protocol and a plan in seven sessions followed (`Data/`), with four decisions of the owner's: Apollodorus described no further, the 90 described fables the sample, the animal tales compared with the wondertales on the corrected card, and the tables to become the only reader, with the parity rule. Tests were frozen before any builder was written; the builder made nine tables from 423 raw files, and every program that the published results rest on was moved onto them and reproduced its run file byte for byte (sessions 1 to 4). The owner then merged the three catalogs of meaning into one master, `SemanticCatalog.md`, with the frozen catalog tests pointed at it, and retired the first project's `SemanticBundling.md` by ruling 105. The parity runs followed, frozen first (session 5): the animal tales keep Propp's blocks and the tight link of pursuit and rescue but drop most of his pairs, and sit between tale and fable on every measure; the myths keep his pairs and blocks (`Data/Parity.md`).
