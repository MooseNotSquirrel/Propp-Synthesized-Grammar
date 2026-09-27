# Semantic catalog for v46

**This catalog lists every group and pair in `ProppEBNF46.txt`, with what it holds, where Propp warrants it, how often the corpus uses it, and what it means.**
It is the catalog `SemanticBundling.md` in the first project was meant to become: every production that is a legitimate pair or group, carrying more meaning than the functions inside it.
Finding FO asked for each entry to say whether it is a group or a pair, a production or a dependency, and at which level it sits, with its page and its meaning. Every entry here does.

**The catalog is checked, not only written.**
A frozen test in `StepTests.txt` requires one entry here for every group in the grammar, at least one tree test for every group, and no entry for a group the grammar lacks.
Each tree test shows the group where the parse puts it, so an entry's claim about what a group holds is tested against the grammar itself.
Run `python runSteps.py 6` to check.

**The functions come later, by the owner's decision.**
Individual functions carry meaning too, or they would not be in the model, so the 31 functions will be added in their own section at the end.

## How to read an entry

- **Kind.** A *pair* is two functions Propp pairs; a *group* is three or more he groups, or a group of groups; a *span* runs between two functions and holds the groups between them; a *choice* is one of several alternatives; *notation* is a device of the grammar and carries no meaning.
- **Level.** Tale or move.
- **Holds.** The functions it can hold, in Propp's symbols.
- **Warrant.** The page where Propp groups or pairs these functions. *Editorial* means no page groups them, and the group is a reading aid only.
- **Name.** Whether the name is Propp's term, v43's, or this grammar's.
- **Corpus.** How many of the 80 accepted move-strings use the group, from `CorpusGroups.txt`. The preparatory groups show 0 because Appendix III prints no preparatory function (p.116), not because the tales lack them.
- **Tree test.** One string from `StepTests.txt` whose parse puts a function in this group.

## Groups and pairs

### `tale`

- **Kind:** group of the whole. **Level:** tale.
- **Holds:** an optional initial situation α, the preparatory section, then one or more moves separated by `/`.
- **Warrant:** p.92: morphologically, a tale is any development proceeding from villainy or lack, and each new villainy or lack creates a new move.
- **Name:** Propp's. **Corpus:** not measured; the corpus is move-strings. **Tree test:** `A K / a K`, the second move's `a` under `tale`.
- **Meaning:** the story as a whole. A misfortune or a want sets it going, and every new one begins a new move inside it.

### `preparatorySection`

- **Kind:** group of groups. **Level:** tale, before the first move only.
- **Holds:** β, then the pairs γ–δ, ε–ζ and η–λ–θ.
- **Warrant:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Name:** Propp's. **Corpus:** 0, since the appendix prints none. **Tree test:** `β γ δ A`, the β under `preparatorySection`.
- **Meaning:** what makes the misfortune possible. The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived. Propp calls the first seven functions the preparatory part (p.30).

### `interdictionViolation`

- **Kind:** pair. **Level:** tale.
- **Holds:** γ then δ. An absentation β told after the interdiction nests inside the pair.
- **Warrant:** p.80 writes γ-δ as a pair; p.64 lists prohibition-violation. The β inside it follows tale 113 (pp.96-97) and the wolf and the kids (p.101), both told interdiction first.
- **Name:** this grammar's, from Propp's terms; v43 called it RuleViolation. **Corpus:** 0. **Tree test:** `γ β δ A`, the β under `interdictionViolation`.
- **Meaning:** a prohibition given and broken, the breach through which misfortune enters. When the elders' departure is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.

### `reconnaissanceDelivery`

- **Kind:** pair. **Level:** tale.
- **Holds:** ε then ζ.
- **Warrant:** p.80 writes ε-ζ as a pair; p.64 lists reconnaissance-delivery.
- **Name:** this grammar's, from Propp's terms; v43 called it InformationGathering. **Corpus:** 0. **Tree test:** `ε ζ A`, the ζ under `reconnaissanceDelivery`.
- **Meaning:** the villain seeks information and gets it. The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.

### `trickeryComplicity`

- **Kind:** pair, with λ inside it. **Level:** tale.
- **Holds:** η, then λ, then θ.
- **Warrant:** p.80 writes η-θ as a pair; λ is placed by Appendix I Table II item 44, which confines the preliminary misfortune to the deceptive agreement.
- **Name:** this grammar's, from Propp's terms; v43 called it DeceptionTrap. **Corpus:** 0. **Tree test:** `η λ θ A`, the λ under `trickeryComplicity`.
- **Meaning:** the villain deceives and the victim submits. The preliminary misfortune is what compels the victim's assent.

### `move`

- **Kind:** group of the move. **Level:** move.
- **Holds:** the span from the crisis to its liquidation, then everything after the liquidation.
- **Warrant:** p.92: a move is any development from villainy or lack, through intermediary functions, to a denouement.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `α A`, where the α is *not* under `move`.
- **Meaning:** one episode of misfortune and its undoing. A tale has as many moves as it has new villainies or lacks.

### `FloatingT`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T, before the move's opener.
- **Warrant:** p.108: T is the most unstable function in relation to its position. By the owner's decision, T may stand anywhere in a move.
- **Name:** this grammar's. **Corpus:** 0; no T stands before an opener in the corpus. **Tree test:** `T A K`, the T under `FloatingT`.
- **Meaning:** none claimed. Since step 7 it holds only the T before a move's opener; after a function, a T stands in `Between`. Where a T hangs in the tree is only where the parser meets it. T's own meaning, transfiguration, belongs to the functions section when it is written.

### `Between`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T and of interrupting moves, in any order, after any function.
- **Warrant:** p.108 for T; p.93 for the pause, methods 2 and 3.
- **Name:** this grammar's. **Corpus:** 6, all of them T's; the move-level corpus has no interruption, since its derivation removes the markers. **Tree test:** `A K T`, the T under `Between`.
- **Meaning:** none claimed of its own. It is the slot between two functions where the two things that can come between them stand: a transfiguration, whose place is free, and another move.

### `InterruptingMove`

- **Kind:** group, the one recursive production. **Level:** move, inside a move.
- **Holds:** a whole move, bracketed ⟨ ... ⟩, which may itself hold interrupting moves to any depth.
- **Warrant:** p.93: "a development which has begun pauses, and a new move is inserted" (method 2), and "an episode may also be interrupted in its turn" (method 3). Ch. IX n.4 designates the interruption by dots with an indication of which move breaks the thread.
- **Name:** this grammar's. **Corpus:** 4 interruptions in 3 of the 45 tales, from `embedCorpus.py`: move III inside 138 II, move II inside 159 I, move IV inside 159 III, and move II inside 162 I. **Tree test:** `A ⟨ a K ⟩ K`, the `a` under `InterruptingMove` and the last K not.
- **Meaning:** a story told inside a story. The hero's first undertaking stops, a new misfortune is met and resolved in full, and the first undertaking resumes where it stopped. It is the one place the grammar is not regular: a move can hold a move.

### `CrisisToLiquidation`

- **Kind:** span, the A–K pair as a constituent. **Level:** move.
- **Holds:** the complication, the donor episode and the fight, then the liquidation.
- **Warrant:** p.53: liquidation, together with villainy, constitutes a pair, and the narrative reaches its peak in it. Finding FP: a distant pair can be a constituent one level up.
- **Name:** this grammar's; the owner proposed VillainyToLiquidation, and the span also covers a lack and a move opened on B. **Corpus:** 80. **Tree test:** `A B C up D E F G H I K`, both A and K under `CrisisToLiquidation`.
- **Meaning:** the misfortune and its undoing, the core of every move. Everything inside it is the hero's way from the one to the other.

### `complication`

- **Kind:** group. **Level:** move.
- **Holds:** the opener, dispatch B, counteraction C and departure ↑, and an untested agent on either side of the departure.
- **Warrant:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, by the owner's decision.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `A B C up`, both B and ↑ under `complication`.
- **Meaning:** the misfortune made known and the hero setting out. Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.

### `MoveOpener`

- **Kind:** choice. **Level:** move.
- **Holds:** one of A, a or B.
- **Warrant:** p.92 for villainy and lack; p.37: where no villainy occurs, the connective incident opens the move.
- **Name:** this grammar's; v43 split at the root instead, and the owner kept the choice here. **Corpus:** 80: villainy in 53, lack in 26, the connective incident in one, 133 II. **Tree test:** `B C up`, the B under `MoveOpener`, and `A B C`, where the later B is not.
- **Meaning:** the kind of move. A villainy is harm done from outside; a lack is something missing from within. The type is read off every tree as this group's child.

### `UntestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** a run of F with no donor's test before it.
- **Warrant:** p.108: the transference of a magical agent sometimes occurs before the hero leaves home, "cudgels, ropes, maces, and so forth, given by the father". Step 6's merge adds the agent that comes to hand on the road with no test.
- **Name:** v43's. **Corpus:** 17. **Tree test:** `A C F up K`, the F under `UntestedAcquisition` and under `complication`.
- **Meaning:** an agent received without being earned. It is a father's gift or a find, and it belongs to setting out rather than to a donor episode.

### `Development`

- **Kind:** span. **Level:** move.
- **Holds:** the donor episode, spatial transference G and the fight.
- **Warrant:** editorial. No page groups these; the span is what lies between the complication and the liquidation.
- **Name:** this grammar's. **Corpus:** 65. **Tree test:** `A D E F G H I K`, the G under `Development` and the K not.
- **Meaning:** a reading aid: the hero's way from setting out to the undoing of the misfortune. It claims nothing about Propp.

### `TestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** the donor's test D, the hero's reaction E, and the agent F they earn.
- **Warrant:** p.65: DEF "also form something of a whole".
- **Name:** v43's; before step 6, Vetting. **Corpus:** 32. **Tree test:** `A D E F`, the F under `TestedAcquisition` and not under `UntestedAcquisition`.
- **Meaning:** the agent earned. A donor tests the hero, the hero responds, and the agent is his reward. It opens on the test, or on the hero's reaction when the test is omitted.

### `Combat`

- **Kind:** group, around the pair H–I. **Level:** move.
- **Holds:** struggle H, branding J and victory I.
- **Warrant:** p.104, the struggle scheme H J I; p.64 lists struggle-victory as a pair.
- **Name:** this grammar's. **Corpus:** 32. **Tree test:** `A H J I K`, the J under `Combat`.
- **Meaning:** the hero fights the villain, is marked, and wins. The mark is what will identify him later (see J–Q under Dependencies).

### `AfterLiquidation`

- **Kind:** span. **Level:** move.
- **Holds:** the return journey, the ordeal and the endgame.
- **Warrant:** editorial.
- **Name:** this grammar's. **Corpus:** 68. **Tree test:** `A K down`, the ↓ under `AfterLiquidation`.
- **Meaning:** a reading aid: what follows once the misfortune is undone, as the hero comes home and his claim is settled.

### `ReturnJourney`

- **Kind:** group. **Level:** move.
- **Holds:** return ↓, then pursuit and rescue.
- **Warrant:** editorial; the pursuit–rescue pair inside it has a page.
- **Name:** v43's. **Corpus:** 43. **Tree test:** `A K down Pr Rs`, the Pr under `ReturnJourney`.
- **Meaning:** the way home and its dangers.

### `Evasion`

- **Kind:** choice between two orders of a pair. **Level:** move.
- **Holds:** pursuit and rescue, in either order.
- **Warrant:** p.64 lists pursuit-deliverance as a pair; p.147 gives the inverted order.
- **Name:** v43's. **Corpus:** 14. **Tree test:** `A K down Pr Rs`, the Rs under `Evasion`.
- **Meaning:** the hero is chased and escapes. The two orders are the two ways Propp's corpus tells it.

### `PursuitFirst`

- **Kind:** group, the usual order. **Level:** move.
- **Holds:** pursuit, then rescue, then an optional fight after the pursuit.
- **Warrant:** p.64 for the pair; p.107 for the fight after it.
- **Name:** this grammar's. **Corpus:** 13. **Tree test:** `A K Pr Rs`, the Pr under `PursuitFirst`.
- **Meaning:** the villain pursues the hero and the hero is saved.

### `RescueFirst`

- **Kind:** group, the inverted order. **Level:** move.
- **Holds:** rescue, then pursuit, then an optional fight after the pursuit.
- **Warrant:** p.147, on tale 150: "Humorous inversion: the villain runs away instead of the hero; the hero pursues [Rs-Pr]".
- **Name:** this grammar's. **Corpus:** 1, 150 II. **Tree test:** `A K Rs Pr`, the Rs under `RescueFirst`.
- **Meaning:** the roles reversed, with the villain fleeing and the hero giving chase. Built into the grammar, it holds for every tale, not only humorous ones.

### `CombatAfterPursuit`

- **Kind:** group. **Level:** move.
- **Holds:** struggle H, branding J and victory I, after a pursuit.
- **Warrant:** p.107: "In tales 93 and 159 the fight with the villain takes place only after pursuit."
- **Name:** this grammar's. **Corpus:** 1, 93 III. **Tree test:** `A K down Pr J`, the J under `CombatAfterPursuit`.
- **Meaning:** the fight displaced to the end: the villain is defeated only when he has chased the hero home.

### `Ordeal`

- **Kind:** group. **Level:** move.
- **Holds:** the false hero's posture, then the task.
- **Warrant:** editorial.
- **Name:** v43's, less the recognition, which exchanges in the endgame since step 3. **Corpus:** 13. **Tree test:** `A K o L M N`, the M under `Ordeal`, and `A K o L M N Q`, where the Q is not.
- **Meaning:** a reading aid: the trial of the hero's claim after he returns.

### `FraudPosture`

- **Kind:** pair. **Level:** move.
- **Holds:** unrecognized arrival o, then unfounded claims L.
- **Warrant:** p.104: unrecognized arrival and unfounded claims shift between the two summed schemes together.
- **Name:** v43's. **Corpus:** 7. **Tree test:** `A K o L`, the L under `FraudPosture`.
- **Meaning:** the hero arrives unknown and a false hero claims his deed. The question of who the hero is gets opened.

### `TaskCycle`

- **Kind:** group, around the pair M–N. **Level:** move.
- **Holds:** difficult task M, branding J and solution N. The J comes only after a task.
- **Warrant:** p.104, the task scheme M J N, set in the position H J I holds in the other scheme. The J only after M is the repair v44's own comment names, applied at step 5.
- **Name:** v43's. **Corpus:** 9. **Tree test:** `A K M J N`, the J under `TaskCycle` and not under `Combat`.
- **Meaning:** the hero is set a hard task and solves it. The task is the other road to the same end as the fight, and p.104 sets the two schemes in the same position.

### `Endgame`

- **Kind:** group of four exchangeable functions. **Level:** move.
- **Holds:** recognition Q, exposure Ex, punishment U and wedding W, in any order.
- **Warrant:** p.108: "Recognition and exposure, marriage and punishment may also exchange positions", on finding FN's reading that the four exchange among themselves.
- **Name:** v44's word for the span. **Corpus:** 38. **Tree test:** `A K U Q W`, both U and Q under `Endgame`.
- **Meaning:** the settling of accounts. The hero is recognized, the false hero exposed and punished, and the hero rewarded. The order of the settling is free.

## Dependencies, not productions

**J–Q: the mark and the recognition.**
Branding J (XVII) falls inside `CrisisToLiquidation`, and recognition Q (XXVII) falls outside it, so the two spans cross, and a single tree cannot hold both (finding FP).
A–K is the constituent, and J–Q is carried as a dependency: the J in `Combat` marks the hero whom the Q in `Endgame` recognizes.
Its meaning is the thread across the move: the wound or ring of the fight is the proof that settles the hero's claim at the end.

## What the catalog teaches

**The father's gift is an untested agent.**
p.108 treats the agent given before departure as its own case, and step 4 followed it, splitting agents by whether a departure followed.
No grammar that reads left to right can draw that split, since a run of F's looks the same until it ends.
The split it can draw is at the test: an agent earned from a donor is tested, and every other agent is untested.
On that reading the father's gift and an agent found on the road are the same kind of thing, and the tree places both with the setting out.
In the corpus, the tested agent appears in 32 moves and the untested in 17.

**Two of Propp's pairs dissolve when their order is freed.**
Recognition with exposure, and punishment with wedding, were groups until step 3 let the four exchange.
Once U Q W is allowed, the pairs are no longer next to each other in every tale, so the grammar keeps one group of four.
The pairing survives as meaning, and the order is free.

**Four groups are reading aids only.**
`Development`, `AfterLiquidation`, `ReturnJourney` and `Ordeal` have no page behind them.
They make the tree readable, and they are candidates for testing against Propp's text rather than claims about it.

**T is the one function the tree cannot place.**
Its position is free by p.108, so its place in the tree carries no meaning.

**A move can hold a move, and the markers keep it readable.**
Since step 7, a move may pause after any function for a whole inserted move, to any depth, as p.93's methods 2 and 3 describe.
That makes the grammar context-free rather than regular, yet it stays LL(1), because each inserted move is bracketed by its own markers.
Without the pause, the grammar is exactly step 6's.
The corpus has four such insertions, in tales 138, 159 and 162; three further sites carry Propp's dots with no numeral, 155 III, 155 IV and 167 I, and name no move to insert.

## Functions

*Reserved for the 31 functions, to be added at the end by the owner's decision. The catalog check requires every entry here to name one of the grammar's single-function productions.*
