# A model of genres: a shared core and each genre's settings

**Drafted 2026-10-19 from the findings already tested; nothing here is new data.** Each claim names the study it rests on; every one was frozen before its data or replicated on unseen stories, and its limits are in `PreliminaryFindings.md`.

## The claim

**A story of these genres is built from one shared set of relations between acts, and a genre is a setting of a few parameters on that core.**
The core is what every genre does alike wherever it uses it. The settings are where the genres part: whether the story's trouble is set right, who causes it, whether the one who leaves comes back, and in what order the large blocks run.
Measured on three genres: the Russian wondertale (45 tales), the fable (Aesop, about 200), Greek tragedy (32 plays).

## The shared core

**The tight relations.** Where the first act appears, the second follows in the same move in every genre (`Links/LinksRun.txt`, the share of moves, transcribers A and B):
- struggle, then victory: tales 86% and 86%, fables 64% and 70%, tragedies 85% and 64%, all of Propp's own moves;
- a difficult task, then its solution: tales 81% and 86%, fables about 60%, all of Propp's;
- pursuit, then rescue: tales 80% and 75%, Propp's 93%;
- a false claim, then exposure: tales 44% and 57%, fables 74% and 43%, Propp's 67%.

**The close pairs stand out unaided** (`Ngrams/ConfirmRun.txt`): interdiction and violation, reconnaissance and delivery, trickery and complicity, test and reaction, struggle and victory, task and solution, both in Propp's notation and in acts described without it.

**They are relations, not pairs of act types** (`Free/FreeRun.txt`): readers given no list of acts name the first half of each pair with a verb of its own, and the second only as whatever act breaks or fulfils the first.

**The exchange, a pair Propp does not list.** A request or an offer, then its answer, most often a refusal: the commonest pair of acts (`Ngrams/`), the only structure readers find with no list (`Free/`), and, for threats, an exchange of threat and counter-threat (`XStudy/ThreatAndFall.txt`).

**Tragedy's own acts, which Propp's list lacks: oath, prayer and curse.** Tested on eight plays no describer had described in free verbs (`Cand/CandRun.txt`): together four to five times their share in the tales, each in six to eight of the eight plays.

**One act Propp's list lacks: the threat or demand**, the only recurring act in the events his functions leave empty to pass its frozen threshold in every genre (`XStudy/`).

## The settings

| Setting | Tale | Fable | Tragedy | Source |
|---|---|---|---|---|
| Villainy or lack followed by liquidation (share of moves) | 40%, 40% | 16%, 16% | 22%, 18% | `Links/` |
| Departure followed by return | 32%, 39% | 10%, 7% | 14%, 14%, not above chance | `Links/` |
| Test and reaction followed by the gift | 68%, 76% | 17%, 8% | 67%, 50% | `Links/` |
| Problems repaired, beyond what length gives | about as length gives | about as length gives | far fewer | `Problems/` |
| Problems the hero opens | about one in fifteen | about half | about a fifth | `Problems/` |
| Acts that help the hero | about 60% | about a quarter | 37% to 44% | `Problems/` |
| Order of the blocks | Propp's | Propp's, as well as a fable order | an order of its own | `Blocks/GenreOrder.md`, `Tragedy/` |
| Its own kernel | | want, trick, complicity, harm | | `Blocks/`, the Aesop audit |
| Oath, prayer and curse (share of free verbs) | about 1% | | 5% to 7%, in eight unseen plays 4.6% and 5.4% | `Cand/` |

**Read as profiles:** the tale is trouble from outside, put right, the hero helped home; the fable is trouble the hero brings on, left standing; the tragedy is trouble that outruns repair, its frame left open. This reading is the keeper's, not Propp's.

## What the model does not yet cover

- **A candidate act, not yet tested:** lament (2% to 4% of acts, most in fables); and the acts no category fits, 4% to 16%, most in fables.
- **Redundancy among the free verbs** (ask, beg, pray, urge, all requests), not yet grouped.
- **Other genres and other cultures:** all three genres are European, and the readers are language models.

## The test

`MythProtocol.md`: the model's predictions for a genre it has not measured, Greek myth in Apollodorus's Library, frozen before the measuring.
**Result, 2026-10-19 (`MythRun.txt`): two of three predictions hold, so the model does not pass as frozen.** The core holds in myth (struggle and victory, task and solution, pursuit and rescue); myth's frame closes as seldom as tragedy's (liquidation in 22% and 27% of moves, against the tale's 40%). That myth is set like tragedy fails: one transcriber's myths lie nearest tragedy, the other's nearest the fable, the split coming from a frame share that stands on a dozen moves; on the two shares resting on many moves both lie nearest tragedy, a check made after the result (`PostHoc.txt`).
**Retest on order, 2026-10-19 (`MythOrderProtocol.md`, `MythOrderRun.txt`): fails.** Tragedy's order of the blocks is the worst fit of four to the myths; the fable's and Propp's fit best, all weakly. Myth shares tragedy's open frame but not its order, which belongs to the play. **So the settings are separate dimensions:** a genre is not one profile that another genre resembles as a whole; some settings follow the matter, others the form of telling.
