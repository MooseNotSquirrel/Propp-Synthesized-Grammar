# Semantic catalog for v46

**This catalog lists every group and pair in `ProppEBNF46.txt`, with what it holds, where Propp warrants it, how often the corpus uses it, and what it means.**
It is the catalog `SemanticBundling.md` in the first project was meant to become: every production that is a legitimate pair or group, carrying more meaning than the functions inside it.
Finding FO asked for each entry to say whether it is a group or a pair, a production or a dependency, and at which level it sits, with its page and its meaning. Every entry here does.

**The catalog is checked, not only written.**
A frozen test in `StepTests.txt` requires one entry here for every group in the grammar, at least one tree test for every group, and no entry for a group the grammar lacks.
Each tree test shows the group where the parse puts it, so an entry's claim about what a group holds is tested against the grammar itself.
Run `python runSteps.py 6` to check.

**The dramatis personae close the catalog**: Propp's seven spheres of action as roles, in the owner's order of social rank, each with a literal and a cultural meaning.

**The functions follow the groups, by the owner's decision.**
Individual functions carry meaning too, or they would not be in the model, so the section "Functions" at the end gives each of Propp's thirty-one, with lack as VIIIa, and a second short section gives the two elements Propp names but does not number.

## How to read an entry

- **Kind.** A *pair* is two functions Propp pairs; a *group* is three or more he groups, or a group of groups; a *span* runs between two functions and holds the groups between them; a *choice* is one of several alternatives; *notation* is a device of the grammar and carries no meaning.
- **Level.** Tale or move.
- **Holds.** The functions it can hold, in Propp's symbols.
- **Warrant.** The page where Propp groups or pairs these functions. *Editorial* means no page groups them, and the group is a reading aid only.
- **Name.** Whether the name is Propp's term, v43's, or this grammar's.
- **Corpus.** How many of the 80 accepted move-strings use the group, from `CorpusGroups.txt`. The preparatory groups show 0 because Appendix III prints no preparatory function (p.116), not because the tales lack them.
- **Tree test.** One string from `StepTests.txt` whose parse puts a function in this group.
- **Literal meaning.** What the group or function says on its surface, the sense a reader first takes from it.
- **Cultural meaning.** What it does for the people who tell and hear the tale: the value it teaches, the social passage it marks, or the order it affirms. THE CULTURAL MEANINGS ARE DRAFTS, written on 2026-09-27 for the owner's review, and marked so; where the owner's reading differs, the owner's governs. The task cycle's is the owner's own wording.

## Groups and pairs

### `tale`

- **Kind:** group of the whole. **Level:** tale.
- **Holds:** an optional initial situation α, the preparatory section, then one or more moves separated by `/`.
- **Warrant:** p.92: morphologically, a tale is any development proceeding from villainy or lack, and each new villainy or lack creates a new move.
- **Name:** Propp's. **Corpus:** not measured; the corpus is move-strings. **Tree test:** `A K / a K`, the second move's `a` under `tale`.
- **Literal meaning:** the story as a whole. A misfortune or a want sets it going, and every new one begins a new move inside it.
- **Cultural meaning:** *Draft.* The restoration of order. A household suffers loss, an individual passes through trial, and the reward reintegrates the hero; told again and again, the tale rehearses how misfortune is answered.

### `LaterMoves`

- **Kind:** group. **Level:** tale.
- **Holds:** the moves after the first, in sequence, then optionally a parting and a common ending; or a parting straight after the first move.
- **Warrant:** p.93, method 1: "one move directly follows another".
- **Name:** this grammar's. **Corpus:** 26 of the 45 tales, counting the tale strings of `embedCorpus.py`, where 162's second move sits inside its first. **Tree test:** `A K / a K`, the `a` under `LaterMoves` and the first A not.
- **Literal meaning:** a reading aid: how a tale goes on after its first move. It holds the three ways p.93 lets it go on at tale level.
- **Cultural meaning:** *Draft.* One resolution is rarely the end. New losses follow, and the hero's worth is shown by meeting them in turn.

### `Parting`

- **Kind:** group, a fork. **Level:** tale.
- **Holds:** the road marker <, the signaller Y if there is one, and two branch moves.
- **Warrant:** pp.93-94, method 6: two seekers "part in the middle of the first move ... at a road marker", which Propp designates <, and "often give one another an object: a signaller", which he designates Y. His scheme for tale 155 is "I-II. <Y", with III and IV after it.
- **Name:** Propp's word. **Corpus:** 1 tale, 155. **Tree test:** `A K < Y a K / A K }`, the `a` under `Parting` and the first A not.
- **Literal meaning:** two heroes set out together and part, each to his own adventure, often leaving the other a token by which to know his fate. The tree holds the two branches side by side.
- **Cultural meaning:** *Draft.* Companions who set out together must prove themselves apart. The token exchanged keeps the bond across the distance, so the fork is also a test of loyalty.

### `CommonEnding`

- **Kind:** group. **Level:** tale.
- **Holds:** Propp's closing brace }, then what follows a liquidation: return, the false hero's contest, the task and the endgame.
- **Warrant:** p.93, method 5: "Two moves may have a common ending." Propp draws a single closing brace across both moves, with the ending to its right, in 125 and 155.
- **Name:** Propp's words. **Corpus:** 2 tales, 125 and 155; 155's ending, ↓X, reduces to nothing, so its common ending is empty. **Tree test:** `A up o / A K } L Q W`, the L under `CommonEnding` and the first move's o not.
- **Literal meaning:** one resolution for two undertakings. The tree makes the ending a sibling of the moves it closes, so it belongs to them jointly. The grammar checks that it fits the last of them; that it fits the other is checked at the move level.
- **Cultural meaning:** *Draft.* Separate trials converge on one settlement. A single justice and reward close every thread at once, affirming that the order restored is shared.

### `preparatorySection`

- **Kind:** group of groups. **Level:** tale, before the first move only.
- **Holds:** β, then the pairs γ–δ, ε–ζ and η–λ–θ.
- **Warrant:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Name:** Propp's. **Corpus:** 0, since the appendix prints none. **Tree test:** `β γ δ A`, the β under `preparatorySection`.
- **Literal meaning:** what makes the misfortune possible. The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived. Propp calls the first seven functions the preparatory part (p.30).
- **Cultural meaning:** *Draft.* Misfortune enters where protection lapses. The household's safeguards fail from within before harm comes from without.

### `interdictionViolation`

- **Kind:** pair. **Level:** tale.
- **Holds:** γ then δ. An absentation β told after the interdiction nests inside the pair.
- **Warrant:** p.80 writes γ-δ as a pair; p.64 lists prohibition-violation. The β inside it follows tale 113 (pp.96-97) and the wolf and the kids (p.101), both told interdiction first.
- **Name:** this grammar's, from Propp's terms; v43 called it RuleViolation. **Corpus:** 0. **Tree test:** `γ β δ A`, the β under `interdictionViolation`.
- **Literal meaning:** a prohibition given and broken, the breach through which misfortune enters. When the elders' departure is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.
- **Cultural meaning:** *Draft.* The tale's first moral lesson: prohibitions exist for a reason, and breaking them lets danger in. The breach is also what sets a young hero's story going.

### `reconnaissanceDelivery`

- **Kind:** pair. **Level:** tale.
- **Holds:** ε then ζ.
- **Warrant:** p.80 writes ε-ζ as a pair; p.64 lists reconnaissance-delivery.
- **Name:** this grammar's, from Propp's terms; v43 called it InformationGathering. **Corpus:** 0. **Tree test:** `ε ζ A`, the ζ under `reconnaissanceDelivery`.
- **Literal meaning:** the villain seeks information and gets it. The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Cultural meaning:** *Draft.* Knowledge is power. Carelessness with what one knows or says hands the enemy the opening.

### `trickeryComplicity`

- **Kind:** pair, with λ inside it. **Level:** tale.
- **Holds:** η, then λ, then θ.
- **Warrant:** p.80 writes η-θ as a pair; λ is placed by Appendix I Table II item 44, which confines the preliminary misfortune to the deceptive agreement.
- **Name:** this grammar's, from Propp's terms; v43 called it DeceptionTrap. **Corpus:** 0. **Tree test:** `η λ θ A`, the λ under `trickeryComplicity`.
- **Literal meaning:** the villain deceives and the victim submits. The preliminary misfortune is what compels the victim's assent.
- **Cultural meaning:** *Draft.* Appearances deceive, and the victim's own consent completes the harm; a warning against trusting the stranger's offer.

### `move`

- **Kind:** group of the move. **Level:** move.
- **Holds:** the span from the crisis to its liquidation, then everything after the liquidation.
- **Warrant:** p.92: a move is any development from villainy or lack, through intermediary functions, to a denouement.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `α A`, where the α is *not* under `move`.
- **Literal meaning:** one episode of misfortune and its undoing. A tale has as many moves as it has new villainies or lacks.
- **Cultural meaning:** *Draft.* A complete cycle of loss and restoration, the tale's unit of meaning: the world is disturbed and set right.

### `BeforeTheCrisis`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a T, then a departure, then a donor sequence, each optional.
- **Warrant:** p.107: elements DEF often stand before A, which is "not a new, but rather an inverted sequence".
- **Name:** this grammar's. **Corpus:** 0; the corpus derivation drops the parked cells left of A, by the owner's decision, so the corpus does not exercise it. **Tree test:** `up D E F A K`, the ↑ under `BeforeTheCrisis`.
- **Literal meaning:** what the hero has or does before the misfortune strikes. It lies outside the A-K span, since the crisis has not yet come.
- **Cultural meaning:** *Draft.* Readiness before the call. A hero already equipped or already travelling when misfortune strikes is shown as prepared for fate rather than merely reacting to it.

### `LeavingFirst`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** one or more departures.
- **Warrant:** p.107: the exit from home comes first, the hero learning of the misfortune when already on the road.
- **Name:** this grammar's. **Corpus:** 0, as above. **Tree test:** `up D E F A K`, the ↑ under `LeavingFirst`.
- **Literal meaning:** the hero already on the road, setting out aimlessly, when the misfortune finds him.
- **Cultural meaning:** *Draft.* The road calls the hero. Setting out without purpose and meeting one's task on the way says that the journey itself leads to destiny.

### `HelperFirst`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a donor sequence: tested when it opens on D or E, untested when it is F alone.
- **Warrant:** p.107: the receipt of a helper first, and then the misfortune the helper liquidates.
- **Name:** this grammar's, from Propp's wording. **Corpus:** 0, as above; the parked regions it would cover are 104 I, 105 II, 125 I, 126 II, 137 I, 156 III, 162 I and 166 I. **Tree test:** `D E F A K`, the F under `HelperFirst` and not under `CrisisToLiquidation`.
- **Literal meaning:** the hero equipped before he is needed. The helper is in hand when the misfortune comes, and the move is shorter for it.
- **Cultural meaning:** *Draft.* Favor that precedes need. Help in hand before the misfortune marks the hero as already chosen; the misfortune only reveals what the hero was prepared for.

### `FloatingT`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T, at the head of a move, inside `BeforeTheCrisis` since step 9.
- **Warrant:** p.108: T is the most unstable function in relation to its position. By the owner's decision, T may stand anywhere in a move.
- **Name:** this grammar's. **Corpus:** 0; no T stands before an opener in the corpus. **Tree test:** `T A K`, the T under `FloatingT`.
- **Literal meaning:** none claimed. Since step 7 it holds only the T before a move's opener; after a function, a T stands in `Between`. Where a T hangs in the tree is only where the parser meets it. T's own meaning, transfiguration, belongs to the functions section when it is written.
- **Cultural meaning:** *Draft.* None of its own; this is notation. Transfiguration's cultural meaning is given under `transfiguration`.

### `Between`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T and of interrupting moves, in any order, after any function.
- **Warrant:** p.108 for T; p.93 for the pause, methods 2 and 3.
- **Name:** this grammar's. **Corpus:** 6, all of them T's; the move-level corpus has no interruption, since its derivation removes the markers. **Tree test:** `A K T`, the T under `Between`.
- **Literal meaning:** none claimed of its own. It is the slot between two functions where the two things that can come between them stand: a transfiguration, whose place is free, and another move.
- **Cultural meaning:** *Draft.* None of its own. It marks the points where a story can pause, for a change of appearance or for another story.

### `InterruptingMove`

- **Kind:** group, the one recursive production. **Level:** move, inside a move.
- **Holds:** a whole move, bracketed ⟨ ... ⟩, which may itself hold interrupting moves to any depth.
- **Warrant:** p.93: "a development which has begun pauses, and a new move is inserted" (method 2), and "an episode may also be interrupted in its turn" (method 3). Ch. IX n.4 designates the interruption by dots with an indication of which move breaks the thread.
- **Name:** this grammar's. **Corpus:** 4 interruptions in 3 of the 45 tales, from `embedCorpus.py`: move III inside 138 II, move II inside 159 I, move IV inside 159 III, and move II inside 162 I. **Tree test:** `A ⟨ a K ⟩ K`, the `a` under `InterruptingMove` and the last K not.
- **Literal meaning:** a story told inside a story. The hero's first undertaking stops, a new misfortune is met and resolved in full, and the first undertaking resumes where it stopped. It is the one place the grammar is not regular: a move can hold a move.
- **Cultural meaning:** *Draft.* A story within a story. The hero's own quest may be suspended while another misfortune is met in full, and the resumed quest shows perseverance; lessons are nested inside lessons.

### `CrisisToLiquidation`

- **Kind:** span, the A–K pair as a constituent. **Level:** move.
- **Holds:** the complication, the donor episode and the fight, then the liquidation.
- **Warrant:** p.53: liquidation, together with villainy, constitutes a pair, and the narrative reaches its peak in it. Finding FP: a distant pair can be a constituent one level up.
- **Name:** this grammar's; the owner proposed VillainyToLiquidation, and the span also covers a lack and a move opened on B. **Corpus:** 80. **Tree test:** `A B C up D E F G H I K`, both A and K under `CrisisToLiquidation`.
- **Literal meaning:** the misfortune and its undoing, the core of every move. Everything inside it is the hero's way from the one to the other.
- **Cultural meaning:** *Draft.* The central promise of the wonder tale: harm once done can be undone. Justice here is restorative, and the arc from loss to its reversal is what the listener waits for.

### `complication`

- **Kind:** group. **Level:** move.
- **Holds:** the opener, dispatch B, counteraction C and departure ↑, and an untested agent on either side of the departure.
- **Warrant:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, by the owner's decision.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `A B C up`, both B and ↑ under `complication`.
- **Literal meaning:** the misfortune made known and the hero setting out. Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Cultural meaning:** *Draft.* The call to action. A loss becomes known and someone must answer it; deciding to act and leaving home mark the passage from a member of a household to an agent.

### `MoveOpener`

- **Kind:** choice. **Level:** move.
- **Holds:** one of A, a or B.
- **Warrant:** p.92 for villainy and lack; p.37: where no villainy occurs, the connective incident opens the move.
- **Name:** this grammar's; v43 split at the root instead, and the owner kept the choice here. **Corpus:** 80: villainy in 53, lack in 26, the connective incident in one, 133 II. **Tree test:** `B C up`, the B under `MoveOpener`, and `A B C`, where the later B is not.
- **Literal meaning:** the kind of move. A villainy is harm done from outside; a lack is something missing from within. The type is read off every tree as this group's child.
- **Cultural meaning:** *Draft.* The two engines of story: the world attacked from outside, and the self incomplete from within.

### `UntestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** a run of F with no donor's test before it.
- **Warrant:** p.108: the transference of a magical agent sometimes occurs before the hero leaves home, "cudgels, ropes, maces, and so forth, given by the father". Step 6's merge adds the agent that comes to hand on the road with no test.
- **Name:** v43's. **Corpus:** 17. **Tree test:** `A C F up K`, the F under `UntestedAcquisition` and under `complication`.
- **Literal meaning:** an agent received without being earned. It is a father's gift or a find, and it belongs to setting out rather than to a donor episode.
- **Cultural meaning:** *Draft.* Fortune and inheritance. A father's gift or a lucky find marks the hero as favored, not only deserving.

### `Development`

- **Kind:** span. **Level:** move.
- **Holds:** the donor episode, spatial transference G and the fight.
- **Warrant:** editorial. No page groups these; the span is what lies between the complication and the liquidation.
- **Name:** this grammar's. **Corpus:** 65. **Tree test:** `A D E F G H I K`, the G under `Development` and the K not.
- **Literal meaning:** a reading aid: the hero's way from setting out to the undoing of the misfortune. It claims nothing about Propp.
- **Cultural meaning:** *Draft.* A reading aid; culturally, the journey into the other realm, where the means of restoration are found and the adversary is met.

### `TestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** the donor's test D, the hero's reaction E, and the agent F they earn.
- **Warrant:** p.65: DEF "also form something of a whole".
- **Name:** v43's; before step 6, Vetting. **Corpus:** 32. **Tree test:** `A D E F`, the F under `TestedAcquisition` and not under `UntestedAcquisition`.
- **Literal meaning:** the agent earned. A donor tests the hero, the hero responds, and the agent is his reward. It opens on the test, or on the hero's reaction when the test is omitted.
- **Cultural meaning:** *Draft.* Help is earned by right conduct. The hero who answers the donor rightly, with kindness, courage or wit, receives the power to prevail; the tale rewards character.

### `Combat`

- **Kind:** group, around the pair H–I. **Level:** move.
- **Holds:** struggle H, branding J and victory I.
- **Warrant:** p.104, the struggle scheme H J I; p.64 lists struggle-victory as a pair.
- **Name:** this grammar's. **Corpus:** 32. **Tree test:** `A H J I K`, the J under `Combat`.
- **Literal meaning:** the hero fights the villain, is marked, and wins. The mark is what will identify him later (see J–Q under Dependencies).
- **Cultural meaning:** *Draft.* Proof by force. The hero confronts the adversary directly, and the mark received is lasting proof of the deed.

### `AfterLiquidation`

- **Kind:** span. **Level:** move.
- **Holds:** the return journey, the ordeal and the endgame.
- **Warrant:** editorial.
- **Name:** this grammar's. **Corpus:** 68. **Tree test:** `A K down`, the ↓ under `AfterLiquidation`.
- **Literal meaning:** a reading aid: what follows once the misfortune is undone, as the hero comes home and his claim is settled.
- **Cultural meaning:** *Draft.* A reading aid; culturally, the return from the other realm and the settling of the hero's standing at home.

### `ReturnJourney`

- **Kind:** group. **Level:** move.
- **Holds:** return ↓, then pursuit and rescue.
- **Warrant:** editorial; the pursuit–rescue pair inside it has a page.
- **Name:** v43's. **Corpus:** 43. **Tree test:** `A K down Pr Rs`, the Pr under `ReturnJourney`.
- **Literal meaning:** the way home and its dangers.
- **Cultural meaning:** *Draft.* The return is not safe. What was won must be carried home against pursuit, and the passage back reintegrates the hero.

### `Evasion`

- **Kind:** choice between two orders of a pair. **Level:** move.
- **Holds:** pursuit and rescue, in either order.
- **Warrant:** p.64 lists pursuit-deliverance as a pair; p.147 gives the inverted order.
- **Name:** v43's. **Corpus:** 14. **Tree test:** `A K down Pr Rs`, the Rs under `Evasion`.
- **Literal meaning:** the hero is chased and escapes. The two orders are the two ways Propp's corpus tells it.
- **Cultural meaning:** *Draft.* The past threatens to reclaim what was won, and escape shows cunning and help as much as strength.

### `PursuitFirst`

- **Kind:** group, the usual order. **Level:** move.
- **Holds:** pursuit, then rescue, then an optional fight after the pursuit.
- **Warrant:** p.64 for the pair; p.107 for the fight after it.
- **Name:** this grammar's. **Corpus:** 13. **Tree test:** `A K Pr Rs`, the Pr under `PursuitFirst`.
- **Literal meaning:** the villain pursues the hero and the hero is saved.
- **Cultural meaning:** *Draft.* The adversary's last attempt to recover what was lost, and the hero's deliverance from it.

### `RescueFirst`

- **Kind:** group, the inverted order. **Level:** move.
- **Holds:** rescue, then pursuit, then an optional fight after the pursuit.
- **Warrant:** p.147, on tale 150: "Humorous inversion: the villain runs away instead of the hero; the hero pursues [Rs-Pr]".
- **Name:** this grammar's. **Corpus:** 1, 150 II. **Tree test:** `A K Rs Pr`, the Rs under `RescueFirst`.
- **Literal meaning:** the roles reversed, with the villain fleeing and the hero giving chase. Built into the grammar, it holds for every tale, not only humorous ones.
- **Cultural meaning:** *Draft.* Reversal as comedy. The villain flees and the hero chases; the inversion mocks the villain and marks a comic register.

### `CombatAfterPursuit`

- **Kind:** group. **Level:** move.
- **Holds:** struggle H, branding J and victory I, after a pursuit.
- **Warrant:** p.107: "In tales 93 and 159 the fight with the villain takes place only after pursuit."
- **Name:** this grammar's. **Corpus:** 1, 93 III. **Tree test:** `A K down Pr J`, the J under `CombatAfterPursuit`.
- **Literal meaning:** the fight displaced to the end: the villain is defeated only when he has chased the hero home.
- **Cultural meaning:** *Draft.* The reckoning deferred. The villain is defeated only when pursuing too far.

### `Ordeal`

- **Kind:** group. **Level:** move.
- **Holds:** the false hero's posture, then the task.
- **Warrant:** editorial.
- **Name:** v43's, less the recognition, which exchanges in the endgame since step 3. **Corpus:** 13. **Tree test:** `A K o L M N`, the M under `Ordeal`, and `A K o L M N Q`, where the Q is not.
- **Literal meaning:** a reading aid: the trial of the hero's claim after he returns.
- **Cultural meaning:** *Draft.* A reading aid; culturally, the trial of the hero's claim at home, where status is contested and must be proven.

### `FraudPosture`

- **Kind:** pair. **Level:** move.
- **Holds:** unrecognized arrival o, then unfounded claims L.
- **Warrant:** p.104: unrecognized arrival and unfounded claims shift between the two summed schemes together.
- **Name:** v43's. **Corpus:** 7. **Tree test:** `A K o L`, the L under `FraudPosture`.
- **Literal meaning:** the hero arrives unknown and a false hero claims his deed. The question of who the hero is gets opened.
- **Cultural meaning:** *Draft.* Merit is not automatically recognized. The humble or unrecognized hero is displaced by an impostor, and recognition must be won.

### `TaskCycle`

- **Kind:** group, around the pair M–N. **Level:** move.
- **Holds:** difficult task M, branding J and solution N. The J comes only after a task.
- **Warrant:** p.104, the task scheme M J N, set in the position H J I holds in the other scheme. The J only after M is the repair v44's own comment names, applied at step 5.
- **Name:** v43's. **Corpus:** 9. **Tree test:** `A K M J N`, the J under `TaskCycle` and not under `Combat`.
- **Literal meaning:** the hero is set a hard task and solves it. The task is the other road to the same end as the fight, and p.104 sets the two schemes in the same position.
- **Cultural meaning:** A demonstration of successful problem solving by the hero: the solution validates the hero's status as the hero. (The owner's wording, not a draft.)

### `Endgame`

- **Kind:** group of four exchangeable functions. **Level:** move.
- **Holds:** recognition Q, exposure Ex, punishment U and wedding W, in any order.
- **Warrant:** p.108: "Recognition and exposure, marriage and punishment may also exchange positions", on finding FN's reading that the four exchange among themselves.
- **Name:** v44's word for the span. **Corpus:** 38. **Tree test:** `A K U Q W`, both U and Q under `Endgame`.
- **Literal meaning:** the settling of accounts. The hero is recognized, the false hero exposed and punished, and the hero rewarded. The order of the settling is free.
- **Cultural meaning:** *Draft.* Justice distributed. The true hero is recognized and rewarded, the false exposed and punished, and the social order is restored with the hero raised within it.

## Dependencies, not productions

**J–Q: the mark and the recognition.**
Branding J (XVII) falls inside `CrisisToLiquidation`, and recognition Q (XXVII) falls outside it, so the two spans cross, and a single tree cannot hold both (finding FP).
A–K is the constituent, and J–Q is carried as a dependency: the J in `Combat` marks the hero whom the Q in `Endgame` recognizes.
Its meaning is the thread across the move: the wound or ring of the fight is the proof that settles the hero's claim at the end.

## Extensions, commented out

Two extensions from v43 are overlaid on v46 and shipped commented out, by the owner's decision (step 10). They are not part of the grammar as it stands, so they have no entries above; switched on, they add these.

- **`TragicFall`, with `CombatEnd` and the defeat sign I-.** *Literal meaning:* the combat ends not in victory but in the hero's defeat, exposure and punishment. *Cultural meaning, v43's reading:* tragedy is not a separate genre but the shadow of the warrior tale, the same rising action with force failing; to lose the conflict is to be revealed as not the hero one claimed. *Warrant:* v43's proposal, not Propp's; no page licenses it and no corpus tests it.
- **`consequenceTale`, with `DundesMove`, `DundesEvent` and `consequence`.** *Literal meaning:* a tale of another genre, in which no lack or villainy drives the action and no hero undoes it: a prohibition broken or an irreversible act, then a consequence, a punishment or a permanent change to the world, and perhaps an attempted escape from it. *Cultural meaning, draft:* the explanation of how things came to be as they are, and a warning that some acts cannot be undone. *Warrant:* Dundes (1964) for Interdiction, Violation, Consequence and Attempted Escape, in that order; the irreversible act and the environmental shift are v43's editorial additions.

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

**Every license of pp.107-108 is now in the grammar.**
The last, p.107's inverted sequence, lets the departure or the donor sequence come before the crisis. The corpus does not exercise it, because its reading still drops the cells Propp parks left of A; the grammar states what Propp allows, and the corpus test is unchanged.

**T is the one function the tree cannot place.**
Its position is free by p.108, so its place in the tree carries no meaning.

**Three of p.93's six methods of combining moves are tale-level, and two of them are forks and joins.**
Method 1 is sequence. Method 6 is a fork, two branches from one trunk, and a tree holds it naturally. Method 5 is a join, one ending for two moves, which no tree can share; the grammar makes the ending a sibling of both moves, which is the nearest a tree comes. Method 4, two villainies at once, is not built: its two A-K spans cross.

**A move can hold a move, and the markers keep it readable.**
Since step 7, a move may pause after any function for a whole inserted move, to any depth, as p.93's methods 2 and 3 describe.
That makes the grammar context-free rather than regular, yet it stays LL(1), because each inserted move is bracketed by its own markers.
Without the pause, the grammar is exactly step 6's.
The corpus has four such insertions, in tales 138, 159 and 162; three further sites carry Propp's dots with no numeral, 155 III, 155 IV and 167 I, and name no move to insert.

## Functions

**Every function carries meaning of its own, or it would not be in the model; this section records it.**
Propp's thirty-one functions of Ch. III, pp.26-63, are listed in his order, with lack as VIIIa (p.35), thirty-two entries in all.
Each gives Propp's number and sign, the page where he defines it, the name he gives it, what happens in it in a sentence, the group that holds it in v46, the pairs it belongs to, how many of the 80 accepted move-strings use it, from `CorpusGroups.txt`, its literal meaning, and a draft of its cultural meaning.
The descriptions are paraphrases; Propp's own wording is on the page cited.
The preparatory functions I-VII show 0 in the corpus because Appendix III prints none (p.116), not because the tales lack them.

### `absentation`

- **Number and sign:** I, β. **Page:** p.26. **Propp's name:** absentation.
- **What happens:** a member of the family leaves home, the elders going out to work or to trade; the death of parents is its intensified form.
- **Group:** `preparatorySection`, or inside `interdictionViolation` when told after the interdiction. **Pairs:** none; it is the one preparatory function outside every pair. **Corpus:** 0.
- **Literal meaning:** the protection of the home is withdrawn. Propp notes that the elders' absence itself prepares the misfortune (p.27).
- **Cultural meaning:** *Draft.* The absence of elders exposes the young to danger; the step from protected child to exposed individual.

### `interdiction`

- **Number and sign:** II, γ. **Page:** p.26. **Propp's name:** interdiction.
- **What happens:** the hero is forbidden something; in the inverted form, he is ordered or advised to do something.
- **Group:** `interdictionViolation`. **Pairs:** with violation, γ-δ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** a rule is laid down whose breaking will let harm in.
- **Cultural meaning:** *Draft.* The voice of authority and tradition: a rule whose purpose the listener learns by its breaking.

### `violation`

- **Number and sign:** III, δ. **Page:** p.27. **Propp's name:** violation.
- **What happens:** the interdiction is broken; in the inverted form, the order is carried out.
- **Group:** `interdictionViolation`. **Pairs:** with interdiction; it may stand without it (p.27). **Corpus:** 0.
- **Literal meaning:** the breach through which the villain enters. Propp observes that interdictions are always broken (p.30).
- **Cultural meaning:** *Draft.* Transgression, which is also the beginning of independence; the story needs the breach in order to begin.

### `reconnaissance`

- **Number and sign:** IV, ε. **Page:** p.28. **Propp's name:** reconnaissance.
- **What happens:** the villain tries to find something out, such as where the children are or where a precious object is kept.
- **Group:** `reconnaissanceDelivery`. **Pairs:** with delivery, ε-ζ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** the villain enters the tale and looks for his way in.
- **Cultural meaning:** *Draft.* The threat that watches and probes: the world outside the home is attentive to its weaknesses.

### `delivery`

- **Number and sign:** V, ζ. **Page:** p.28. **Propp's name:** delivery.
- **What happens:** the villain receives information about his victim.
- **Group:** `reconnaissanceDelivery`. **Pairs:** with reconnaissance; it may stand without it, as a careless act (p.29). **Corpus:** 0.
- **Literal meaning:** the victim is laid open to the villain.
- **Cultural meaning:** *Draft.* Loose talk or careless revelation betrays the household.

### `trickery`

- **Number and sign:** VI, η. **Page:** p.29. **Propp's name:** trickery.
- **What happens:** the villain, often disguised, tries to deceive the victim in order to take possession of him or his belongings.
- **Group:** `trickeryComplicity`. **Pairs:** with complicity, η-θ (p.80). **Corpus:** 0.
- **Literal meaning:** deceit, the villain's instrument before force.
- **Cultural meaning:** *Draft.* Evil hides behind a friendly face; the adversary's weapons are disguise and false persuasion.

### `complicity`

- **Number and sign:** VII, θ. **Page:** p.30. **Propp's name:** complicity.
- **What happens:** the victim is taken in by the deception and so unwittingly helps the enemy.
- **Group:** `trickeryComplicity`. **Pairs:** with trickery; it may stand without it, as falling asleep unprompted (p.30). **Corpus:** 0.
- **Literal meaning:** the victim's own act opens the way to harm. Propp observes that deceitful proposals are always accepted (p.30).
- **Cultural meaning:** *Draft.* Credulity completes the harm; responsibility is shared by the one deceived.

### `villainy`

- **Number and sign:** VIII, A. **Page:** p.30; its forms run to p.34. **Propp's name:** villainy.
- **What happens:** the villain causes harm or injury to a member of the family.
- **Group:** `MoveOpener`, in the complication. **Pairs:** with liquidation, A-K, the pair that spans the move (p.53). **Corpus:** 53, the opener of each.
- **Literal meaning:** the misfortune from outside that sets a move going. Propp calls the function exceptionally important, since the actual movement of the tale is created by it (p.30).
- **Cultural meaning:** *Draft.* Evil breaking into ordered life, abduction, theft or murder: the injury a community cannot leave unanswered.

### `lack`

- **Number and sign:** VIIIa, a. **Page:** p.35. **Propp's name:** lack.
- **What happens:** a member of the family lacks something or desires to have something: a bride, a magical agent, a marvel.
- **Group:** `MoveOpener`, in the complication. **Pairs:** with liquidation, as villainy does. **Corpus:** 26, the opener of each.
- **Literal meaning:** the misfortune from within. It does the work of villainy, leading to a quest in the same way (p.34), and a move begun from it is undone by the same liquidation.
- **Cultural meaning:** *Draft.* Incompleteness from within, the need for a bride, a wonder or the means of life: desire as the motor of the quest.

### `mediation`

- **Number and sign:** IX, B. **Page:** p.36. **Propp's name:** mediation, the connective incident.
- **What happens:** the misfortune or lack is made known; the hero is asked or commanded, and is allowed to go or is sent.
- **Group:** `complication`, as the dispatch; `MoveOpener`, where no villainy occurs and it opens the move (p.37). **Pairs:** none. **Corpus:** 41, one of them, 133 II, as an opener.
- **Literal meaning:** the hero is drawn in. It connects the misfortune to the one who will act on it.
- **Cultural meaning:** *Draft.* The community's call: the misfortune is made known and someone is summoned to answer it.

### `beginningCounteraction`

- **Number and sign:** X, C. **Page:** p.38. **Propp's name:** beginning counteraction.
- **What happens:** the seeker agrees to or decides on counteraction.
- **Group:** `complication`. **Pairs:** none. **Corpus:** 61.
- **Literal meaning:** the hero's decision to act, the moment the tale turns from suffering to seeking.
- **Cultural meaning:** *Draft.* Assent to responsibility: the moment of choosing to act.

### `departure`

- **Number and sign:** XI, ↑. **Page:** p.39. **Propp's name:** departure.
- **What happens:** the hero leaves home.
- **Group:** `complication`, which it closes; or `LeavingFirst`, before the crisis (p.107). **Pairs:** none named, though it faces the return. **Corpus:** 66.
- **Literal meaning:** setting out. With villainy, dispatch and counteraction it completes the complication (pp.64-65).
- **Cultural meaning:** *Draft.* Leaving home, the threshold of the passage into the unknown.

### `firstDonorFunction`

- **Number and sign:** XII, D. **Page:** p.39. **Propp's name:** the first function of the donor.
- **What happens:** the hero is tested, questioned or attacked, which prepares the way for his receiving a magical agent or helper.
- **Group:** `TestedAcquisition`, which it opens; or `HelperFirst`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of F (pp.46-47). **Corpus:** 31.
- **Literal meaning:** the test. The donor probes whether the hero is worthy of help.
- **Cultural meaning:** *Draft.* The world tests character before it grants power; courtesy, compassion and wit are examined.

### `heroReaction`

- **Number and sign:** XIII, E. **Page:** p.42. **Propp's name:** the hero's reaction.
- **What happens:** the hero reacts to the actions of the future donor, well or badly.
- **Group:** `TestedAcquisition`, which it opens when the test is omitted; or `HelperFirst`, before the crisis (p.107). **Pairs:** with the test it answers. **Corpus:** 32.
- **Literal meaning:** the hero's answer to the test, which decides whether help is given.
- **Cultural meaning:** *Draft.* Conduct under test decides the outcome; the tale's ethics are concentrated here.

### `receiptOfMagicalAgent`

- **Number and sign:** XIV, F. **Page:** p.43. **Propp's name:** provision or receipt of a magical agent.
- **What happens:** the hero acquires the use of a magical agent: an animal, an object, a quality.
- **Group:** `TestedAcquisition` after a test or reaction; `UntestedAcquisition` otherwise, in the complication (step 6); or `HelperFirst`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of D (pp.46-47). **Corpus:** 40; the tested agent appears in 32 moves and the untested in 17.
- **Literal meaning:** the means of undoing the misfortune. Earned from a donor, it is a reward; received without a test, from a father or by finding, it comes with the setting out.
- **Cultural meaning:** *Draft.* Power comes from outside the hero, given in return for right conduct or by favor: the hero succeeds with help, not alone.

### `spatialTransference`

- **Number and sign:** XV, G. **Page:** p.50. **Propp's name:** spatial transference between two kingdoms, guidance.
- **What happens:** the hero is carried, delivered or led to where the object of his search is.
- **Group:** `Development`. **Pairs:** none. **Corpus:** 25.
- **Literal meaning:** the passage to the other kingdom, where the misfortune can be undone.
- **Cultural meaning:** *Draft.* Passage to another realm beyond ordinary space, where the decisive encounter happens.

### `struggle`

- **Number and sign:** XVI, H. **Page:** p.51. **Propp's name:** struggle.
- **What happens:** the hero and the villain join in direct combat.
- **Group:** `Combat`, or `CombatAfterPursuit` after a pursuit (p.107). **Pairs:** with victory, H-I (p.64). **Corpus:** 25.
- **Literal meaning:** the confrontation with the villain himself.
- **Cultural meaning:** *Draft.* The confrontation of good and evil in person.

### `branding`

- **Number and sign:** XVII, J. **Page:** p.52. **Propp's name:** branding, marking.
- **What happens:** the hero is marked: wounded in the fight, or given a ring or a towel.
- **Group:** `Combat` in the fight; `TaskCycle` after a task (p.104; step 5); `CombatAfterPursuit` after a pursuit. **Pairs:** with recognition, J-Q, the one crossing pair, carried as a dependency. **Corpus:** 2.
- **Literal meaning:** the sign by which the hero will be known. It is rare in the corpus and central to the end, since it is what recognition reads.
- **Cultural meaning:** *Draft.* The mark carried from the ordeal, proof of identity and deed, and later a seal of truth.

### `victory`

- **Number and sign:** XVIII, I. **Page:** p.53. **Propp's name:** victory.
- **What happens:** the villain is defeated, in combat, in a contest, or by other means.
- **Group:** `Combat`, or `CombatAfterPursuit`. **Pairs:** with struggle; it may stand without it (p.29). **Corpus:** 33.
- **Literal meaning:** the villain's power broken.
- **Cultural meaning:** *Draft.* Evil can be overcome.

### `liquidation`

- **Number and sign:** XIX, K. **Page:** p.53. **Propp's name:** none given; he designates it K and describes it as the liquidation of the initial misfortune or lack.
- **What happens:** the initial misfortune or lack is undone: the object seized, the spell broken, the dead revived, the captive freed.
- **Group:** `CrisisToLiquidation`, which it closes. **Pairs:** with villainy, A-K; Propp says the narrative reaches its peak in it (p.53). **Corpus:** 47.
- **Literal meaning:** the undoing of the misfortune, the point every move is heading for.
- **Cultural meaning:** *Draft.* Restoration: what was taken is returned and the harm undone. Propp calls it the tale's peak (p.53).

### `return`

- **Number and sign:** XX, ↓. **Page:** p.55. **Propp's name:** return.
- **What happens:** the hero returns.
- **Group:** `ReturnJourney`. **Pairs:** none named, though it faces the departure. **Corpus:** 42.
- **Literal meaning:** the way home, opening the second half of the move.
- **Cultural meaning:** *Draft.* Reintegration: the hero brings what was won back into the community.

### `pursuit`

- **Number and sign:** XXI, Pr. **Page:** p.56. **Propp's name:** pursuit, chase.
- **What happens:** the hero is pursued.
- **Group:** `Evasion`, first in `PursuitFirst` and second in `RescueFirst`. **Pairs:** with rescue, Pr-Rs (p.64); inverted in the humorous tale (p.147). **Corpus:** 14.
- **Literal meaning:** the villain's last attempt: what was undone is threatened again.
- **Cultural meaning:** *Draft.* The defeated power strives to recover what it lost; the past does not let go easily.

### `rescue`

- **Number and sign:** XXII, Rs. **Page:** p.57. **Propp's name:** rescue.
- **What happens:** the hero is rescued from pursuit.
- **Group:** `Evasion`. **Pairs:** with pursuit. **Corpus:** 14.
- **Literal meaning:** the threat escaped, and many tales end here (p.92 lists it among the denouements).
- **Cultural meaning:** *Draft.* Deliverance by wit or help, affirming that the hero is protected.

### `unrecognizedArrival`

- **Number and sign:** XXIII, o. **Page:** p.60. **Propp's name:** unrecognized arrival.
- **What happens:** the hero arrives home or in another country unrecognized.
- **Group:** `FraudPosture`. **Pairs:** with unfounded claims, as they move together between the two schemes (p.104). **Corpus:** 5.
- **Literal meaning:** the hero without his due: present, but not known.
- **Cultural meaning:** *Draft.* True worth hidden under a humble appearance.

### `unfoundedClaims`

- **Number and sign:** XXIV, L. **Page:** p.60. **Propp's name:** unfounded claims.
- **What happens:** a false hero presents unfounded claims to the hero's deed.
- **Group:** `FraudPosture`. **Pairs:** with unrecognized arrival; and it prepares exposure. **Corpus:** 6.
- **Literal meaning:** the hero's deed usurped, which the end of the tale must correct.
- **Cultural meaning:** *Draft.* The impostor takes credit for another's deed; deceit set against truth.

### `difficultTask`

- **Number and sign:** XXV, M. **Page:** p.60. **Propp's name:** difficult task.
- **What happens:** a difficult task is proposed to the hero: an ordeal, a riddle, a test of strength or endurance.
- **Group:** `TaskCycle`. **Pairs:** with solution, M-N, set in the scheme where H-I stands in the other (p.104). **Corpus:** 9.
- **Literal meaning:** the hero's worth tested by trial rather than by combat. Propp finds it typical of a second move (p.104).
- **Cultural meaning:** *Draft.* Society tests worth, often a suitor's: the hero must prove fit for the bride and the position.

### `solution`

- **Number and sign:** XXVI, N. **Page:** p.62. **Propp's name:** solution.
- **What happens:** the task is accomplished; a solution before the task is set Propp designates *N (p.62).
- **Group:** `TaskCycle`. **Pairs:** with difficult task; it may stand without it, as the preliminary solution (commentary p.145). **Corpus:** 9.
- **Literal meaning:** the trial passed.
- **Cultural meaning:** *Draft.* Competence proven: success validates the hero's status. (After the owner's reading of the task cycle.)

### `recognition`

- **Number and sign:** XXVII, Q. **Page:** p.62. **Propp's name:** recognition.
- **What happens:** the hero is recognized, by a mark, a thing given him, a task accomplished, or after long separation.
- **Group:** `Endgame`, exchangeable with exposure, punishment and wedding (p.108). **Pairs:** with branding, J-Q, as a dependency; with exposure. **Corpus:** 7.
- **Literal meaning:** the hero known for who he is, the undoing of the unrecognized arrival.
- **Cultural meaning:** *Draft.* Truth revealed: the community acknowledges who the hero is and what the hero did.

### `exposure`

- **Number and sign:** XXVIII, Ex. **Page:** p.62. **Propp's name:** exposure.
- **What happens:** the false hero or villain is exposed.
- **Group:** `Endgame`. **Pairs:** with recognition; it answers the unfounded claims. **Corpus:** 5.
- **Literal meaning:** the false claim undone.
- **Cultural meaning:** *Draft.* Falsehood unmasked: the impostor's claim collapses.

### `transfiguration`

- **Number and sign:** XXIX, T. **Page:** pp.62-63. **Propp's name:** transfiguration.
- **What happens:** the hero is given a new appearance: new garments, a palace, a handsome form.
- **Group:** none; it stands in `FloatingT` before an opener or in `Between` after any function, since Propp calls it the most unstable function in relation to its position (p.108). **Pairs:** none. **Corpus:** 6.
- **Literal meaning:** the hero's new estate made visible. Its free place is itself a finding: it is the one function whose position means nothing.
- **Cultural meaning:** *Draft.* New status made visible: the hero's appearance changes to match the hero's worth.

### `punishment`

- **Number and sign:** XXX, U. **Page:** p.63. **Propp's name:** punishment.
- **What happens:** the villain or false hero is punished; the magnanimous pardon is its negative form.
- **Group:** `Endgame`. **Pairs:** with wedding, the two exchanging (p.108). **Corpus:** 15.
- **Literal meaning:** the wrong answered.
- **Cultural meaning:** *Draft.* Justice done upon evil, restoring balance by sanction, or, in the pardon, by magnanimity.

### `wedding`

- **Number and sign:** XXXI, W. **Page:** p.63. **Propp's name:** wedding.
- **What happens:** the hero marries and ascends the throne; the reward without marriage folds into it.
- **Group:** `Endgame`. **Pairs:** with punishment. **Corpus:** 34.
- **Literal meaning:** the hero's due given, the most common close of a move, and the denouement p.92 names first.
- **Cultural meaning:** *Draft.* Reward and integration: marriage and the throne complete the passage into adult standing in the community.

## Elements that are not functions

Two terminals of v46 are elements Propp names but does not number, so they stand outside the functions above.

- **`initialSituation`, α.** p.25: the tale usually begins with some initial situation, the members of a family enumerated or the future hero introduced; it is not a function, but an important morphological element. In v46 it stands at the beginning of the tale only, outside every move. **Corpus:** 0, since the move-strings carry none.
- **`preliminaryMisfortune`, λ.** Appendix I Table II item 44, p.121: a misfortune that compels the victim's assent within the deceitful agreement. In v46 it stands inside `trickeryComplicity`, between trickery and complicity. **Corpus:** 0.

The six remaining terminals, `/`, `⟨`, `⟩`, `<`, `Y` and `}`, are signs of how moves combine, and their meaning is given under `tale`, `LaterMoves`, `InterruptingMove`, `Parting` and `CommonEnding`.

## Dramatis personae

**Propp's seven spheres of action, entered as roles, by the owner's decision for now.**
p.79: many functions "logically join together into certain spheres", which "correspond to their respective performers"; p.80 concludes that the tale has seven dramatis personae.
A sphere is a role, not a person: one character may fill several spheres, and one sphere may be spread across several characters (pp.80-81). The father who dispatches his son and gives him a cudgel is dispatcher and donor at once (p.81).
The preparatory functions are distributed among the same characters, but too unequally to define them (p.80), so they appear in no entry below.

**THE ORDER IS THE OWNER'S, AND IT IS AN ORDER OF SOCIAL RANK.**
Highest status goes to the hero, then the princess and her father, the dispatcher, the donor, the helper, the false hero, and the villain.
Propp does not say so, but on the owner's reading he has outlined the social hierarchy of Indo-European culture, and it is recursive from the state down to the family group; in fact the state is cast as a family group.
Each entry's "place in the social order" line applies that reading, and the cultural meanings are drafted with it in mind. Both are drafts for discussion.

Each entry gives Propp's sphere and page, the functions he assigns it, the groups of v46 where they act, how many of the 80 accepted move-strings use at least one of them, its place in the social order, and its literal and cultural meaning.

### `hero`

- **Propp's sphere:** 6, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), `wedding` (W*). Propp: C is characteristic of the seeker-hero; the victim-hero performs only the rest.
- **Acts in:** `complication`, `TestedAcquisition` and `HelperFirst`, `Endgame`. **Corpus:** 79.
- **Place in the social order:** *Draft.* Highest. The hero ends at the head of a new household and of the state, marrying and ascending the throne, and every other role acts for or against that rise.
- **Literal meaning:** the one who decides to act and sets out, answers the donor's test, and is married at the end; a seeker, or a victim who suffers the villainy.
- **Cultural meaning:** *Draft.* The member of the household who proves fitness to rule. The hero often begins low, the youngest son, the stepdaughter, the fool, is tested, and ends at the head of a family and a kingdom. The tale legitimizes succession by proven worth within the family order, the state being the family written large.

### `princessAndFather`

- **Propp's sphere:** 4, pp.79-80. **Functions:** `difficultTask` (M), `branding` (J), `exposure` (Ex), `recognition` (Q), `punishment` (U), `wedding` (W). Propp: the princess and her father "cannot be exactly delineated from each other according to functions"; most often the father assigns the tasks, from hostility to the suitor, and punishes the false hero.
- **Acts in:** `TaskCycle`, `Combat` for the branding, `Endgame`. **Corpus:** 38.
- **Place in the social order:** *Draft.* Second. The ruling house: the father as head of both state and family, the princess as the one through whom rule passes.
- **Literal meaning:** the sought-for person and her father, who set the hard task, mark the hero, recognize the true hero and expose the false one, punish the impostor, and give the marriage.
- **Cultural meaning:** *Draft.* TWO READINGS ARE KEPT, BY THE OWNER'S DECISION.
  - *Succession and exchange.* The father, as sovereign and head of the family, controls who marries into the house and so who inherits. The princess is the reward and the channel of succession, the tasks screen the suitor, and the wedding transfers rule to the hero.
  - *Judgment and agency.* The princess is the tale's judge. She sets or shares in the tasks, marks the hero, recognizes him and exposes the impostor. The true hero is known through her discernment, so the order is restored by her choice and not only by her father's grant.

### `dispatcher`

- **Propp's sphere:** 5, p.80. **Functions:** `mediation` (B), the dispatch.
- **Acts in:** `complication`, and `MoveOpener` when the connective incident opens a move. **Corpus:** 41.
- **Place in the social order:** *Draft.* Third. The authority that sends: a king, a father, a parent within the household.
- **Literal meaning:** the one who makes the misfortune known and sends the hero out, or allows the hero to go.
- **Cultural meaning:** *Draft.* The head of the household delegating the family's task to one of its members. Authority acts through commission, and the hierarchy is enacted in the act of sending.

### `donor`

- **Propp's sphere:** 2, p.79. **Functions:** `firstDonorFunction` (D), `receiptOfMagicalAgent` (F).
- **Acts in:** `TestedAcquisition`, `HelperFirst`, and, when the agent comes with no test, `UntestedAcquisition`. **Corpus:** 45.
- **Place in the social order:** *Draft.* Fourth. The elder or the outsider of power, a witch, an old man, a grateful animal, who is not of the household but can endow it: a patron.
- **Literal meaning:** the one who tests the hero and provides the magical agent.
- **Cultural meaning:** *Draft.* The patron who judges worth and grants power. Step 6 of the grammar gives this a sharper edge: an agent earned from a donor is tested and comes from outside the household, while the father's gift of p.108, where the father is dispatcher and donor at once (p.81), is untested and comes by right of family. Favor from outside is earned by conduct; favor from within is inherited.

### `helper`

- **Propp's sphere:** 3, p.79. **Functions:** `spatialTransference` (G), `liquidation` (K), `rescue` (Rs), `solution` (N), `transfiguration` (T).
- **Acts in:** `Development`, `CrisisToLiquidation`, `Evasion`, `TaskCycle`, and `FloatingT` or `Between` for T. **Corpus:** 68.
- **Place in the social order:** *Draft.* Fifth. The servant or ally who acts at the hero's command: power in service. Grateful animals begin as donors and become helpers (pp.80-81).
- **Literal meaning:** the one who carries the hero, undoes the misfortune, rescues from pursuit, solves the tasks and transforms the hero. The horse that does all of these is Propp's pure helper (p.80).
- **Cultural meaning:** *Draft.* The loyal servant whose power is exercised on the master's behalf. Much of what the hero is credited with, the helper does, and the order assigns the credit upward; the hero commands, the helper accomplishes.

### `falseHero`

- **Propp's sphere:** 7, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), and, as his specific function, `unfoundedClaims` (L).
- **Acts in:** `complication`, `TestedAcquisition`, `FraudPosture`. **Corpus:** 6 by his specific function L; the rest he shares with the hero, and 77 moves hold one of C, ↑ or E.
- **Place in the social order:** *Draft.* Sixth. The rival claimant inside the order: elder brothers, a general, a courtier.
- **Literal meaning:** the one who sets out as the hero does and meets the donor, but claims the hero's deed without right.
- **Cultural meaning:** *Draft.* Illegitimate ambition within the family or the court: a claimant who seeks rank without merit. Exposure and punishment defend the order's rule that rank follows proven worth, and the false hero's likeness to the hero is the point: the order must tell the two apart.

### `villain`

- **Propp's sphere:** 1, p.79. **Functions:** `villainy` (A), `struggle` (H), `pursuit` (Pr).
- **Acts in:** `MoveOpener`, `Combat` and `CombatAfterPursuit`, `Evasion`. **Corpus:** 62.
- **Place in the social order:** *Draft.* Lowest. The enemy of the order, usually outside it, a dragon, Koshchei, a witch; sometimes inside it, a stepmother or envious sisters.
- **Literal meaning:** the one who does harm, fights the hero, and pursues.
- **Cultural meaning:** *Draft.* The threat to the household and the state that the order exists to repel; the hero's rise is its defeat. When the villain comes from inside the family, the tale shows where the recursive order is weakest: the household itself.
