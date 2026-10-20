# Lessons: the faults found along the way, and what each changed

**Written 2026-10-20 from the keeper logs.** Most of these are the keeper's own faults, found before or after a verdict; each is recorded in its study's log.

## In the instrument

**A placeholder can be copied as data.** The rules' format example used `S000` for the story; two describers wrote speech numbers where the play belongs (`TwoLayer/`), and it recurred later. The reader learned to recover such lines against the event list, and the free-verb rules said plainly that the field is the story's identifier; no describer did it again.
**Names in two languages do not match.** Russian names in the act descriptions against English hero lists failed every hero match in the tales (`TwoLayer/`); later tests had the describers mark the hero's part themselves.
**A first-word match splits names.** "The little prince" and "the prince" did not match (`Heroes/`).
**A reducer may name things its own way.** Propp's departure and return came back as `up` and `down`, so the links test found no departure in his moves (`Links/`). Read the reducer's whole vocabulary before trusting a count.
**A folder pattern can reach into a new folder.** A reader's pattern built for one test also matched the next test's folder and would have read its stories twice (`Ngrams/`).

**Check what a cleaner throws away.** The Wikisource extraction dropped every template with its contents; on the calibration's pages that cost two tales their verse, and on the animal tales' pages it would have cost whole paragraphs. Count the words a cleaning step removes before trusting it.

## In the design

**Measures can follow length.** A long story described at random almost surely has a repair; a short fable often has none. Random descriptions passed 8 of 16 predictions until each story was scored against a random description of its own acts (`Problems/`).
**A threshold must beat chance, not a fixed number.** Accuracy of 0.8 counted a pair as told apart by random verbs when one half was nine tenths of its events; the gain over chance replaced it (`Free/`).
**A difference of nothing can be significant.** When both groups sit at zero, a shuffle test calls a vanishing difference significant; a minimum effect was added (`Problems/`).
**A thin measure can decide a distance.** A setting standing on a dozen moves split the transcribers and failed a prediction the well-supported settings would have passed (`Genre/`); set a minimum count for every dimension.
**A self-test can be too clean.** Planted synonyms with their own objects passed a grouping that then put almost every real verb in one class (`Group/`); test the degenerate case too.
**An example can prime the readers.** The free-verb rules' first example was a trick followed by its victim's act, the very pair under test; it was replaced before any describer saw it (`Free/`).
**A cutoff can be too strict for the measure.** Predicting a function only where it held half the time understated a mapping, since the agreement measure rewards a prediction right a third of the time (`Significance/`).
**A mapping must follow the card it claims to follow.** The significance mapping withheld trickery and villainy from the hero against the card's rule that a function is assigned whoever performs it; mended after the verdict, it changed little (`Significance/`).

## In the claims

**The card can make an order look like a finding.** That the order inside Propp's blocks is near obligatory was withdrawn when the definitions card was found to fix most of it (`Blocks/DefinitionCheck.md`).
**A reading is not a result.** That a third layer of significance would recover Propp's functions was the keeper's reading; tested, it failed, and the reading was marked not supported (`Significance/`).
**"Most of the gap is bookkeeping"** was withdrawn after the held-out test (`Calibration/`).

## In the running

**Stage files by name.** A commit of everything swept in the owner's unfinished catalog edits; it was reverted, and the rule is now to stage by name.
**Bound every cache.** An unbounded cache in the block machinery froze the owner's machine and killed a cloud run; bounded, the outputs were checked identical.
**A long batch can be cut short.** One describer's file ended mid-tale at its length limit, unreported; batches of more than about 700 entries are at risk.
**A clearing line works.** A runner asked to run a stage its `RUN.md` had not cleared refused, as it should.
**Ask before downloading.** The synonym dictionary was fetched only at the owner's word, with its license stated, and kept outside the repositories.
