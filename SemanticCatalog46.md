# Semantic catalog for v46

**This catalog lists every group and pair in `ProppEBNF46.txt`, with what it holds, where Propp warrants it, how often the corpus uses it, and what it means.**
It is the catalog `SemanticBundling.md` in the first project was meant to become: every production that is a legitimate pair or group, carrying more meaning than the functions inside it.
Finding FO asked for each entry to say whether it is a group or a pair, a production or a dependency, and at which level it sits, with its page and its meaning. Every entry here does.

**The catalog is checked, not only written.**
A frozen test in `StepTests.txt` requires one entry here for every group in the grammar, at least one tree test for every group, and no entry for a group the grammar lacks.
Each tree test shows the group where the parse puts it, so an entry's claim about what a group holds is tested against the grammar itself.
Run `python runSteps.py 6` to check.

**The dramatis personae close the catalog**: Propp's seven spheres of action as roles, ordered by rank on a speculative reading that is not Propp's, each with a literal and a cultural meaning.

**The functions follow the groups, as decided.**
Individual functions carry meaning too, or they would not be in the model, so the section "Functions" at the end gives each of Propp's thirty-one, with lack as VIIIa, and a second short section gives the two elements Propp names but does not number.

## How to read an entry

- **Kind.** A *pair* is two functions Propp pairs; a *group* is three or more he groups, or a group of groups; a *span* runs between two functions and holds the groups between them; a *choice* is one of several alternatives; *notation* is a device of the grammar and carries no meaning.
- **Level.** Tale or move.
- **Holds.** The functions it can hold, in Propp's symbols.
- **Warrant.** The page where Propp groups or pairs these functions. *Editorial* means no page groups them, and the group is a reading aid only.
- **Name.** Whether the name is Propp's term, v43's, or this grammar's, and the name it had before, where it was renamed.
  *Early* in a name means before the move's trigger, inside `BeforeTheTrouble`; *Late* means after the liquidation, inside `AfterLiquidation`. The two words stand on either side of the A–K span, `TroubleToLiquidation`, the core of every move. *First* in `PursuitFirst` and `RescueFirst` is another axis: which half of a pair comes first.
- **EBNF.** The entry's production in `ProppEBNF46.txt`, with its comments removed and its lines joined; where an extension replaces the production, the extension's form follows it.
- **Corpus.** How many of the 80 accepted move-strings use the group, from `CorpusGroups.txt`. The preparatory groups show 0 because Appendix III prints no preparatory function (p.116), not because the tales lack them.
- **Tree test.** One string from `StepTests.txt` whose parse puts a function in this group.
- **Measured.** Where an entry has one: a finding counted from the corpus by a program in this project, reproducible, and pinned by a test. It is data, not speculation, and it is kept apart from the cultural meaning for that reason.
- **Literal meaning.** What the group or function says on its surface, the sense a reader first takes from it.
- **Cultural meaning.** The conduct the tale teaches its young listener, and the value that conduct encodes, read relative to the hero. THE CULTURAL MEANINGS REST ON A SPECULATIVE READING, NOT ON PROPP; it is set out in the section "A speculative reading, not from Propp", below. Unlike the functions and groups, they have no tokens in the corpus to cling to. All but the task cycle's are marked *Draft*.

## A speculative reading, not from Propp

**Everything in this section is speculation.** The functions and groups in this catalog are tied to Propp's pages and tested against Appendix III. The cultural meanings are not, and cannot be until the values they name are studied on their own terms. They are offered as a reading to be tested, not as a finding.

**The tale reads as a guide for the young.** It begins when the elders leave the young unprotected, and it ends when the hero marries and ascends the throne. Nothing follows the wedding: there is no function for ruling, for raising heirs or for growing old. The older figures are present, but the tale gives no guidance for what anyone does after the wedding.

**The hero is the center, and the other roles are nearly an audience.** Of Propp's thirty-one function headings in Ch. III, eighteen name the hero or the seeker, and none names the princess, her father or the king; even the wedding is the hero's, "married" and ascending the throne. The other roles are defined by what they do to or for the hero. That much is Propp's own method: he defines characters by the meaning of their deeds "for the hero and for the course of the action" (p.81). Down the order of rank the helper is a sidekick, a Sancho Panza to Don Quixote or a Tonto to the Lone Ranger, the false hero an object of derision and often the butt of humor, and the villain despised.

**The values read as Western ones.** The hero is usually the chooser and the leader, not the follower or the sidekick: the individual who acts on his own account and rises by his own conduct. Not always: Propp keeps a victimized hero, carried off or driven out, who does not choose and is the hero all the same, because the tale follows that hero's fortunes (p.36). In his material that hero is rare. That is set against cultures that value harmony and collaboration above individual distinction. Which values of Western culture the tale encodes, and how exactly, is a question still to be studied.

**The family order is fractal and cyclical.** The same order holds at the level of the state and of a small peasant household; the state is cast as a family, with the king at its head. The tale starts from an existing family and ends by founding a new one, whose child will be the next hero, so the structure repeats through time. An illustration of the repetition: the Anglo-Saxon Chronicle, in its annal for 855, carries the genealogy of Alfred's father Æthelwulf back through Woden and Noah to Adam. It is far too short to be literal, but it is the same founding structure told generation after generation.

**The outcome is never in doubt.** The magic tale does not end badly for the hero. Failures come as negative results before the success (p.74), and tragedy exists here only as the commented-out extension from v43. The tale promises success to the young who conduct themselves rightly.

**The peripheral roles bend.** The king may favor the hero or resist him; the princess may choose him at once or require to be won. The tales vary these freely without changing the end.

## Groups and pairs

### `tale`

- **Kind:** group of the whole. **Level:** tale.
- **Holds:** an optional initial situation α, the preparatory section, then one or more moves separated by `/`.
- **Warrant:** p.92: morphologically, a tale is any development proceeding from villainy or lack, and each new villainy or lack creates a new move.
- **Name:** Propp's. **Corpus:** not measured; the corpus is move-strings. **Tree test:** `A K / a K`, the second move's `a` under `tale`.
- **EBNF:** `tale = [initialSituation] preparatorySection move FollowingMoves`
- **Literal meaning:** The story as a whole. A misfortune or a want sets it going, and every new one begins a new move inside it.
- **Cultural meaning:** The whole passage of a young person, from a household left unprotected to the head of a new household, told as a narrative blueprint derived from ancient initiation rituals. The family order is the same at the level of the state and the level of a peasant household, and the tale is cyclical: it starts from one family and ends by founding the next, whose child will be the next hero.

### `FollowingMoves`

- **Kind:** group. **Level:** tale.
- **Holds:** the moves after the first, in sequence, then optionally a parting and a common ending; or a parting straight after the first move.
- **Warrant:** p.93, method 1: "one move directly follows another".
- **Name:** this grammar's; `LaterMoves` before. **Corpus:** 26 of the 45 tales, counting the tale strings of `embedCorpus.py`, where 162's second move sits inside its first. **Tree test:** `A K / a K`, the `a` under `FollowingMoves` and the first A not.
- **EBNF:** `FollowingMoves = [ moveBoundary move {moveBoundary move} [Parting] [CommonEnding] | Parting [CommonEnding] ]`
- **Literal meaning:** a reading aid: how a tale goes on after its first move. It holds the three ways p.93 lets it go on at tale level.
- **Cultural meaning:** Status validation. Consecutive moves function as a cumulative ladder of escalation and verification. Each subsequent move increases the narrative stakes and supernatural trials, progressively amplifying the hero’s power, while structurally confirming that the hero’s initial success was a true reflection of their worthiness, not an accident. If there are three moves, they may be an instance of trebling, or using the magic number three, where the first two moves establish the pattern, and the third  move confirms that the hero is truly a hero.

### `Parting`

- **Kind:** group, a fork. **Level:** tale.
- **Holds:** the road marker <, the signaller Y if there is one, and two branch moves.
- **Warrant:** pp.93-94, method 6: two seekers "part in the middle of the first move ... at a road marker", which Propp designates <, and "often give one another an object: a signaller", which he designates Y. His scheme for tale 155 is "I-II. <Y", with III and IV after it.
- **Name:** Propp's word. **Corpus:** 1 tale, 155. **Tree test:** `A K < Y a K / A K }`, the `a` under `Parting` and the first A not.
- **EBNF:** `Parting = roadMarker [signaller] move moveBoundary move`
- **Literal meaning:** two heroes set out together and part, each to his own adventure, often leaving the other a token by which to know his fate. The tree holds the two branches side by side.
- **Cultural meaning:** Divergent destiny and interdependence. The parting of companions split from a single origin establishes parallel, equivalent moves. The exchanged token acts as a supernatural sympathy indicator bridging isolated worlds. Culturally, this branching structure demonstrates that the heroic destiny is not wholly individual: the eventual triumph of one branch relies entirely on the other's capacity to act as a cosmic rescuer when the token signals disaster.

### `CommonEnding`

- **Kind:** group. **Level:** tale.
- **Holds:** Propp's closing brace }, then what follows a liquidation: return, the false hero's contest, the task and the endgame.
- **Warrant:** p.93, method 5: "Two moves may have a common ending." Propp draws a single closing brace across both moves, with the ending to its right, in 125 and 155.
- **Name:** Propp's words. **Corpus:** 2 tales, 125 and 155; 155's ending, ↓X, reduces to nothing, so its common ending is empty. **Tree test:** `A up o / A K } L Q W`, the L under `CommonEnding` and the first move's o not.
- **EBNF:** `CommonEnding = commonEnding AfterLiquidation`
- **Literal meaning:** one resolution for two undertakings. The tree makes the ending a sibling of the moves it closes, so it belongs to them jointly. The grammar checks that it fits the last of them; that it fits the other is checked at the move level.
- **Cultural meaning:** Cosmic realignment and unified truth. This merges parallel sequences of functions into a single settlement and signifies the restoration of a fractured social and cosmic order. Culturally, the common ending establishes absolute discernment: it brings disparate, isolated paths into a single public forum to permanently separate true heroism from false claims. By resolving multiple undertakings into a singular sovereign settlement, the narrative collapses chaos back into a unified, harmonious hierarchy.

### `preparatorySection`

- **Kind:** group of groups. **Level:** tale, before the first move only.
- **Holds:** β, then the pairs γ–δ, ε–ζ and η–λ–θ.
- **Warrant:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Name:** Propp's. **Corpus:** 0, since the appendix prints none. **Tree test:** `β γ δ A`, the β under `preparatorySection`.
- **EBNF:** `preparatorySection = {absentation} RuleViolation InformationGathering DeceptionTrap`
- **Literal meaning:** what makes the misfortune possible. The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived. Propp calls the first seven functions the preparatory part (p.30).
- **Cultural meaning:** The collapse of home security. The preparatory section establishes the structural inevitability of leaving home. The sequence demonstrates that the protective domestic bubble is inherently fragile and temporary. By showing that innocence naturally falls prey to worldly deception, the opening functions as a narrative threshold: violently dissolving childhood security to force the initiate into the trials of maturity.

### `RuleViolation`

- **Kind:** pair. **Level:** tale.
- **Holds:** γ then δ. An absentation β told after the interdiction nests inside the pair.
- **Warrant:** p.80 writes γ-δ as a pair; p.64 lists prohibition-violation. The β inside it follows tale 113 (pp.96-97) and the wolf and the kids (p.101), both told interdiction first.
- **Name:** v43's, restored; this grammar's `interdictionViolation` before, from Propp's terms. **Corpus:** 0. **Tree test:** `γ β δ A`, the β under `RuleViolation`.
- **EBNF:** `RuleViolation = [ interdiction {interdiction} {absentation} ] {violation}`
- **Literal meaning:** a prohibition given and broken, the breach through which misfortune enters. When the elders' departure is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.
- **Cultural meaning:** The Catalyst of Transgression. Rule violation represents the structural necessity of breaking boundaries. The interdiction exists solely to be violated; it is the inevitable act of self-sabotage that dissolves the artificial safety of childhood. While the breach invites immediate peril, it serves as the essential cosmic mechanism that forces the youth out of passive stagnation and launches them into the trials of their own individual destiny.

### `InformationGathering`

- **Kind:** pair. **Level:** tale.
- **Holds:** ε then ζ.
- **Warrant:** p.80 writes ε-ζ as a pair; p.64 lists reconnaissance-delivery.
- **Name:** v43's, restored; this grammar's `reconnaissanceDelivery` before, from Propp's terms. **Corpus:** 0. **Tree test:** `ε ζ A`, the ζ under `InformationGathering`.
- **EBNF:** `InformationGathering = {reconnaissance} {delivery}`
- **Literal meaning:** the villain seeks information and gets it. The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Cultural meaning:** The leak of vulnerability. This sequence exposes the structural impossibility of maintaining absolute secrecy. Culturally, the delivery of information represents the tragic naivety of the uninitiated domestic sphere, which cannot comprehend predatory intent. The mechanical ease with which the villain extracts this knowledge demonstrates a cosmic rule: hidden weaknesses cannot remain concealed, and the initiate's specific vulnerabilities must be exposed to the outside world before the journey can truly begin.

### `DeceptionTrap`

- **Kind:** pair, with λ inside it. **Level:** tale.
- **Holds:** η, then λ, then θ.
- **Warrant:** p.80 writes η-θ as a pair; λ is placed by Appendix I Table II item 44, which confines the preliminary misfortune to the deceptive agreement.
- **Name:** v43's, restored; this grammar's `trickeryComplicity` before, from Propp's terms. **Corpus:** 0. **Tree test:** `η λ θ A`, the λ under `DeceptionTrap`.
- **EBNF:** `DeceptionTrap = {trickery} {preliminaryMisfortune} {complicity}`
- **Literal meaning:** the villain deceives and the victim submits. The preliminary misfortune is what compels the victim's assent.
- **Cultural meaning:** The Eclipse of Discernment. This sequence exposes the fatal inadequacy of childhood intuition when facing systemic malice. Culturally, the villain’s disguise proves that predatory threats naturally masquerade as benign elements of the domestic world. By using a preliminary misfortune to coerce the victim's mechanical assent, the narrative demonstrates that survival instincts alone cannot protect the uninitiated, forcing a total collapse of personal autonomy so that the true heroic journey can rise from the wreckage.

### `move`

- **Kind:** group of the move. **Level:** move.
- **Holds:** the span from the crisis to its liquidation, then everything after the liquidation.
- **Warrant:** p.92: a move is any development from villainy or lack, through intermediary functions, to a denouement.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `α A`, where the α is *not* under `move`.
- **EBNF:** `move = BeforeTheTrouble TroubleToLiquidation AfterLiquidation`; with `+reversal`, `move = BeforeTheTrouble TroubleToLiquidation AfterLiquidation [LateFall]`
- **Literal meaning:** one episode of misfortune and its undoing. A tale has as many moves as it has new villainies or lacks.
- **Cultural meaning:** The engine of social regeneration. A single move serves as a structural blueprint for overcoming systemic crisis. Culturally, the progression from misfortune to liquidation demonstrates that societal collapse is never final; instead, it triggers a predictable, renewable ritual of restoration. By linking the hero's alignment with cultural laws to the absolute mending of a communal lack or misfortune, the move reassures the culture that equilibrium can always be reclaimed, while its repeatable structure acknowledges that life is an ongoing series of disruptions and renewals.

### `BeforeTheTrouble`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a T, then a departure, then a donor sequence, each optional.
- **Warrant:** p.107: elements DEF often stand before A, which is "not a new, but rather an inverted sequence".
- **Name:** this grammar's; `BeforeTheCrisis` before. **Corpus:** 0; the corpus derivation drops the parked cells left of A, as decided, so the corpus does not exercise it. **Tree test:** `up D E F A K`, the ↑ under `BeforeTheTrouble`.
- **EBNF:** `BeforeTheTrouble = EarlyTransfiguration [EarlyLeaving] [EarlyHelp]`
- **Literal meaning:** what the hero has or does before the misfortune strikes. It lies outside the A-K span, since the crisis has not yet come.
- **Cultural meaning:** Latent destiny and preemptive balance. This early sequence establishes the hero’s inherent and predestined status. Culturally, by introducing transformations or helpers before a crisis even manifests, the narrative demonstrates that the hero is distinct from the ordinary domestic sphere. It signals a law of cosmic equilibrium: even as the household collapses into vulnerability, the universe has already seeded a latent antidote, ensuring that the eventual misfortune does not destroy the initiate but merely activates their latent power.

### `EarlyLeaving`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** one or more departures.
- **Warrant:** p.107: the exit from home comes first, the hero learning of the misfortune when already on the road.
- **Name:** this grammar's; `LeavingFirst` before. **Corpus:** 0, as above. **Tree test:** `up D E F A K`, the ↑ under `EarlyLeaving`.
- **EBNF:** `EarlyLeaving = departure EarlyTransfiguration {departure EarlyTransfiguration}`
- **Literal meaning:** the hero already on the road, setting out aimlessly, when the misfortune finds him.
- **Cultural meaning:** Proactive autonomy and iterative transformation. Early departure demonstrates that the impulse toward maturity can be self-generating. Culturally, the act of leaving home is itself the heroic awakening. By structurally anchoring each departure to an immediate transfiguration, the narrative shows that moving away from childhood security is an iterative process that continually reshapes identity. When the misfortune inevitably strikes the hero on the open road, it reveals a profound cultural law: the task of the mature individual is found not by isolating within the home, but by stepping forward to meet the world’s wider crises.

### `EarlyHelp`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a donor sequence: tested when it opens on D or E, untested when it is F alone.
- **Warrant:** p.107: the receipt of a helper first, and then the misfortune the helper liquidates.
- **Name:** this grammar's; `HelperFirst` before, from Propp's wording. **Corpus:** 0, as above; the parked regions it would cover are 104 I, 105 II, 125 I, 126 II, 137 I, 156 III, 162 I and 166 I. **Tree test:** `D E F A K`, the F under `EarlyHelp` and not under `TroubleToLiquidation`.
- **EBNF:** `EarlyHelp = firstDonorFunction EarlyTransfiguration {firstDonorFunction EarlyTransfiguration} {heroReaction EarlyTransfiguration} {receiptOfMagicalAgent EarlyTransfiguration} | heroReaction EarlyTransfiguration {heroReaction EarlyTransfiguration} {receiptOfMagicalAgent EarlyTransfiguration} | receiptOfMagicalAgent EarlyTransfiguration {receiptOfMagicalAgent EarlyTransfiguration}`
- **Literal meaning:** the hero equipped before he is needed. The helper is in hand when the misfortune comes, and the move is shorter for it.
- **Cultural meaning:** Foundational alliance and structural elevation. This sequence demonstrates the protective power of systemic alignment. Culturally, winning an ally or receiving a magical agent before a crisis strikes shows that the initiate who respects ancestral heritage or fundamental social contracts is automatically granted cosmic backing. By structurally locking each step of the donor exchange to an optional transfiguration, the narrative proves that acquiring these protective forces permanently elevates the hero's status, ensuring that when misfortune inevitably lands, the individual does not face it with raw human fragility, but with the full weight of their culture's accumulated power.

### `EarlyTransfiguration`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T, at the head of a move, inside `BeforeTheTrouble` since step 9.
- **Warrant:** p.108: T is the most unstable function in relation to its position. As decided, T may stand anywhere in a move.
- **Name:** this grammar's; `FloatingT` before. **Corpus:** 0; no T stands before an opener in the corpus. **Tree test:** `T A K`, the T under `EarlyTransfiguration`.
- **EBNF:** `EarlyTransfiguration = {transfiguration}`
- **Literal meaning:** none claimed. Since step 7 it holds only the T before a move's opener; after a function, a T stands in `Digression`. Where a T hangs in the tree is only where the parser meets it. T's own meaning, transfiguration, belongs to the functions section when it is written.
- **Cultural meaning:** None independent of `transfiguration`. As a structural mechanism, its fluid distribution simply demonstrates that the process of heroic elevation is not confined to a single concluding event, but can manifest incrementally as the initiate moves through different stages of preparation.

### `Digression`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T and of interrupting moves, in any order, after any function.
- **Warrant:** p.108 for T; p.93 for the pause, methods 2 and 3.
- **Name:** this grammar's; `Between` before. **Corpus:** 6, all of them T's; the move-level corpus has no interruption, since its derivation removes the markers. **Tree test:** `A K T`, the T under `Digression`.
- **EBNF:** `Digression = { transfiguration | EmbeddedMove }`
- **Literal meaning:**  A notation level structural slot between functions that accommodates the narrative's capacity to pause, allowing either a fluid shift in the hero's appearance or the nesting of an entirely separate, interrupting move.
- **Cultural meaning:** None independent of its contents. As a structural framework, it maps the inherent elasticity of human life and duty. By allowing the narrative to pause for a transformation or bend to absorb a nested crisis, it demonstrates that destiny is rarely linear; instead, it is an interlocking web where major personal growth occurs in transitional spaces, and grand quests must frequently bend to answer immediate communal needs.

### `EmbeddedMove`

- **Kind:** group, the one recursive production. **Level:** move, inside a move.
- **Holds:** a whole move, bracketed ⟨ ... ⟩, which may itself hold interrupting moves to any depth.
- **Warrant:** p.93: "a development which has begun pauses, and a new move is inserted" (method 2), and "an episode may also be interrupted in its turn" (method 3). Ch. IX n.4 designates the interruption by dots with an indication of which move breaks the thread.
- **Name:** this grammar's; `InterruptingMove` before. **Corpus:** 4 interruptions in 3 of the 45 tales, from `embedCorpus.py`: move III inside 138 II, move II inside 159 I, move IV inside 159 III, and move II inside 162 I. **Tree test:** `A ⟨ a K ⟩ K`, the `a` under `EmbeddedMove` and the last K not.
- **EBNF:** `EmbeddedMove = interruptionBegins move interruptionEnds`
- **Literal meaning:** A story told inside a story. A narrative-level recursion where the primary quest is suspended to process a nested crisis. A separate misfortune or lack is introduced, tracked through its own complete cycle of trial and liquidation, and closed before the parent move resumes. This node introduces context-free depth to the grammar, allowing moves to stack inside moves.
- **Cultural meaning:**  The web of interconnected crisis. The recursive embedding of moves maps the interconnected nature of societal crisis. Culturally, it demonstrates that destiny is non-linear and that a grand quest must remain subordinate to immediate communal fractures encountered along the way. By demanding that the nested misfortune be resolved in full before progress can resume, the structure proves that macro-level restoration is impossible without first answering the localized, immediate obligations of the road.

### `TroubleToLiquidation`

- **Kind:** span, the A–K pair as a constituent. **Level:** move.
- **Holds:** the complication, the donor episode and the fight, then the liquidation.
- **Warrant:** p.53: liquidation, together with villainy, constitutes a pair, and the narrative reaches its peak in it. Finding FP: a distant pair can be a constituent one level up.
- **Name:** this grammar's; `CrisisToLiquidation` before, itself widened from VillainyToLiquidation because the span also covers a lack and a move opened on B. **Corpus:** 80. **Tree test:** `A B C up D E F G H I K`, both A and K under `TroubleToLiquidation`.
- **EBNF:** `TroubleToLiquidation = complication Development {liquidation Digression}`
- **Literal meaning:** the misfortune and its undoing, the core of every move. Everything inside it is the hero's way from the one to the other.
- **Cultural meaning:** This overarching span demonstrates the structural certainty of cosmic and communal restoration. Culturally, the binding of misfortune directly to its liquidation proves that crisis is inherently finite and orderly. By showcasing that systemic injuries can be systematically healed through alignment with foundational cultural protocols, the sequence serves as an absolute guarantee to the community that no chaos is permanent and that equilibrium will always be reclaimed.

### `complication`

- **Kind:** group. **Level:** move.
- **Holds:** the opener, dispatch B, counteraction C and departure ↑, and an untested agent on either side of the departure.
- **Warrant:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `A B C up`, both B and ↑ under `complication`.
- **EBNF:** `complication = MoveTrigger Digression {mediation Digression} {beginningCounteraction Digression} [UntestedAcquisition] [ departure Digression {departure Digression} [UntestedAcquisition] ]`
- **Literal meaning:** the misfortune made known and the hero setting out. Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Cultural meaning:** 
- **The Mechanics of Communal Mobilization.** The complication represents the systemic process of extracting a member from the domestic sphere to answer a communal deficit. Culturally, the progression from witnessing a misfortune to physically crossing the threshold demonstrates that private equilibrium cannot be maintained while a public injury remains unaddressed. By allowing the traveler to gather unearned provisions along the road, the structure shows that the act of moving forward automatically unlocks baseline ancestral or ecological support, transforming a stationary victim into an active agent of restoration.

### `MoveTrigger`

- **Kind:** choice. **Level:** move.
- **Holds:** one of A, a or B.
- **Warrant:** p.92 for villainy and lack; p.37: where no villainy occurs, the connective incident opens the move.
- **Name:** this grammar's; `MoveOpener` before; v43 split at the root instead, and the choice is kept here. **Corpus:** 80: villainy in 53, lack in 26, the connective incident in one, 133 II. **Tree test:** `B C up`, the B under `MoveTrigger`, and `A B C`, where the later B is not.
- **EBNF:** `MoveTrigger = villainy | lack | mediation`
- **Literal meaning:** The structural trigger that opens a move. A villainy is an injury inflicted from the outside; a lack is a structural deficit missing from within. When neither occurs, the move is initiated directly by a connective dispatch.
- **Cultural meaning:** The move trigger establishes the two fundamental vulnerabilities of any human community. Culturally, an external injury (*villainy*) demonstrates that absolute isolation cannot protect a household from external malice, while an internal deficit (*lack*) proves that a community will stagnate and decay unless it actively reaches beyond its borders to secure the elements necessary for its next stage of evolution.

### `UntestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** a run of F with no donor's test before it.
- **Warrant:** p.108: the transference of a magical agent sometimes occurs before the hero leaves home, "cudgels, ropes, maces, and so forth, given by the father". Step 6's merge adds the agent that comes to hand on the road with no test.
- **Name:** v43's. **Corpus:** 17. **Tree test:** `A C F up K`, the F under `UntestedAcquisition` and under `complication`.
- **EBNF:** `UntestedAcquisition = receiptOfMagicalAgent Digression {receiptOfMagicalAgent Digression}`
- **Measured:** Counted by `agentForms.py` and pinned by a test. At home, before the departure, 12 cells in 11 moves: transferred 6, prepared 5, bought 1; none found, appearing, seized or offering service. On the road, 10 cells in 10 moves: transferred 4, appears 3, pointed out 1, prepared 1, offers service 1. The agent at home comes by ordinary human means; on the road, fortune may bring it.
- **Literal meaning:** an agent received without being earned. It is a father's gift or a find, and it belongs to setting out rather than to a donor episode.
- **Cultural meaning:** The endowment of ancestral and environmental heritage. This sequence represents the foundational capital provided by lineage and environment. Culturally, receiving a magical agent without a trial demonstrates that the initiate is fundamentally sustained by the accumulated strength and wisdom of previous generations. Whether manifested as an elder’s blessing or a fortunate discovery along the road, this endowment proves that the act of stepping forward into crisis automatically unlocks a baseline of historical and cosmic support, ensuring the hero is structurally equipped before their merit is ever tested.

### `Development`

- **Kind:** span. **Level:** move.
- **Holds:** the donor episode, spatial transference G and the fight.
- **Warrant:** editorial. No page groups these; the span is what lies between the complication and the liquidation.
- **Name:** this grammar's. **Corpus:** 65. **Tree test:** `A D E F G H I K`, the G under `Development` and the K not.
- **EBNF:** `Development = [TestedAcquisition] {spatialTransference Digression} StruggleAndOutcome`
- **Literal meaning:** A macro-level structural container mapping the hero's progression through the supernatural or foreign realm. It tracks the sequence from earning a magical asset and traversing vast distances to the ultimate confrontation with the source of misfortune.
- **Cultural meaning:** The arena of liminal transformation. This macro-sequence represents the dangerous, transitional wilderness where childhood is permanently stripped away. Culturally, the strict linear progression, requiring an initiate to first secure spiritual alliance, then cross into the heart of foreign peril, and only then engage the adversary. It demonstrates that raw human effort is useless against systemic crisis. It proves that a person must be systematically transformed, tested, and structurally re-equipped by their cultural heritage before they possess the capacity to face and neutralize absolute malice.

### `TestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** the donor's test D, the hero's reaction E, and the agent F they earn.
- **Warrant:** p.65: DEF "also form something of a whole".
- **Name:** v43's; before step 6, Vetting. **Corpus:** 32. **Tree test:** `A D E F`, the F under `TestedAcquisition` and not under `UntestedAcquisition`.
- **EBNF:** `TestedAcquisition = firstDonorFunction Digression {firstDonorFunction Digression} {heroReaction Digression} {receiptOfMagicalAgent Digression} | heroReaction Digression {heroReaction Digression} {receiptOfMagicalAgent Digression}`
- **Measured:** Counted by `agentForms.py` and pinned by a test. 35 cells in 28 moves: transferred 8, offers service 7, pointed out 4, seized 3, appears 3, found 2, prepared 1, bought 1, and 6 with no form marked. Every seizure in the corpus falls here, 3 of 3, and 7 of the 8 offers of service.
- **Literal meaning:** The magical agent earned. A threshold guardian tests the hero, the hero responds to the encounter, and the agent is secured as a direct consequence. The sequence opens either on the formal test or directly on the hero's reaction when the initial testing is omitted.
- **Cultural meaning:** The verification of cultural competency. Rather than a flexible lesson in secular kindness or conditional contract honesty, the tested acquisition represents a rigid examination of ritual readiness. Culturally, navigating the donor sequence proves that the initiate possesses the deep traditional etiquette, ancestral respect, or adaptive intelligence required to survive outside the domestic sphere. Whether the agent is granted as a reward for honoring sacred reciprocity or seized via guile from an adversarial guardian, this verification demonstrates that spiritual and structural power is never random. It is exclusively unlocked by those who master the foundational laws of their environment

### `StruggleAndOutcome`

- **Kind:** group, around the pair H–I. **Level:** move.
- **Holds:** struggle H, branding J and victory I.
- **Warrant:** p.104, the struggle scheme H J I; p.64 lists struggle-victory as a pair.
- **Name:** this grammar's; `Combat` before. **Corpus:** 32. **Tree test:** `A H J I K`, the J under `StruggleAndOutcome`.
- **EBNF:** `StruggleAndOutcome = {struggle Digression} {branding Digression} {victory Digression}`; (or conditional `+tragedy` `StruggleAndOutcome = {struggle Digression} {branding Digression} StruggleOutcome`
- **Literal meaning:** The physical or symbolic clash with the adversary, the receipt of a identifying mark, and the resulting victory. The brand secured during this encounter serves as the foundational structural link for public recognition later in the narrative.
- **Cultural meaning:** The somatic ordination of the sovereign. The struggle and branding represent the irreversible transformation of the initiate's identity through direct confrontation with chaos. Culturally, the direct clash marks the final death of the passive childhood persona, while the brand serves as an indelible physical credential proving the hero has traversed the underworld or wild and survived. By structurally pairing the receipt of this permanent mark with absolute victory, the sequence demonstrates that true authority and the right to protect the community are exclusively earned by those who carry the literal scars of systemic conflict.

### `AfterLiquidation`

- **Kind:** span. **Level:** move.
- **Holds:** the return journey, the ordeal and the endgame.
- **Warrant:** editorial.
- **Name:** this grammar's. **Corpus:** 68. **Tree test:** `A K down`, the ↓ under `AfterLiquidation`.
- **EBNF:** `AfterLiquidation = ReturnJourney Ordeal Endgame`
- **Literal meaning:** A macro-level structural container mapping the narrative events following the undoing of the misfortune. It tracks the hero's reentry into the domestic sphere, the public tests verifying their true identity, and the final settlement of their status.
- **Cultural meaning:** The social integration of sovereign authority. This macro-sequence represents the perilous transition from private achievement to public legitimacy. Culturally, the progression through a hazardous return, a public trial, and a final political settlement demonstrates that conquering chaos in isolation is insufficient for leadership. It establishes a strict social law: before an initiate can be integrated into the communal hierarchy or found a new household, their hidden deeds must be brought into the light of a public forum, systematically verified, and thoroughly cleansed of false or predatory claims.

### `ReturnJourney`

- **Kind:** group. **Level:** move.
- **Holds:** return ↓, then pursuit and rescue.
- **Warrant:** editorial; the pursuit–rescue pair inside it has a page.
- **Name:** v43's. **Corpus:** 43. **Tree test:** `A K down Pr Rs`, the Pr under `ReturnJourney`.
- **EBNF:** `ReturnJourney = {return Digression} Evasion`
- **Literal meaning:** The spatial movement back toward the domestic sphere, encompassing the flight from the other world, the enemy's pursuit, and the final rescue.
- **Cultural meaning:** The Domestication of Supernatural Capital. The return journey represents the perilous task of maintaining a newly won equilibrium against a systemic backlash. Culturally, the sequence of pursuit demonstrates that conquering chaos triggers an immediate, predatory reaction from the displaced forces of the wild. By forcing a weakened hero to rely on transformation and external rescuers to survive the journey home, the narrative proves that individual triumph is highly fragile. The restoration of the community requires a collaborative, ecological shield to successfully carry the fruits of victory across the threshold of the domestic world.

### `Evasion`

- **Kind:** choice between two orders of a pair. **Level:** move.
- **Holds:** pursuit and rescue, in either order.
- **Warrant:** p.64 lists pursuit-deliverance as a pair; p.147 gives the inverted order.
- **Name:** v43's. **Corpus:** 14. **Tree test:** `A K down Pr Rs`, the Rs under `Evasion`.
- **EBNF:** `Evasion = [ PursuitFirst | RescueFirst ]`
- **Literal meaning:** The structural sequence of avoiding capture by the displaced forces of the other world. It accounts for the two variations in the corpus: where a pursuit triggers a reactive rescue, or where a preemptive rescue mechanism neutralizes an incoming pursuit.
- **Cultural meaning:** The Preservation of the Threshold. This sequence maps the essential requirement of sealing the border between the sacred wild and the domestic world. Culturally, the dual structural pathways demonstrate that navigating a systemic backlash requires complete adaptability over raw might. By forcing the hero to survive not through direct combat, but through environmental concealment, transformation, and systemic safety nets, the narrative proves that a successful transition to maturity demands knowing when to fight an adversary face-to-face and when to fluidly dissolve the self to escape the lingering reach of past chaos.

### `PursuitFirst`

- **Kind:** group, the usual order. **Level:** move.
- **Holds:** pursuit, then rescue, then an optional fight after the pursuit.
- **Warrant:** p.64 for the pair; p.107 for the fight after it.
- **Name:** this grammar's. **Corpus:** 13. **Tree test:** `A K Pr Rs`, the Pr under `PursuitFirst`.
- **EBNF:** `PursuitFirst = pursuit Digression {pursuit Digression} {rescue Digression} LateStruggle`
- **Literal meaning:** The reactive sequence where the forces of the other world pursue a returning hero, triggering a defensive rescue operation and an optional final boundary clash before safe passage is secured.
- **Cultural meaning:** The lingering momentum of crisis. This sequence demonstrates that major life disruptions possess a hazardous, lingering momentum. Culturally, the reactive chase proves that the consequences of a neutralized threat will actively hunt an individual across transitional thresholds. By showing that this sudden, terrifying resurgence can be dynamically defeated through improvisational environmental protection and a final defensive boundary clash, the structure reassures the initiate that the lingering ripples of past trauma can be permanently severed before re-entering the community.

### `RescueFirst`

- **Kind:** group, the inverted order. **Level:** move.
- **Holds:** rescue, then pursuit, then an optional fight after the pursuit.
- **Warrant:** p.147, on tale 150: "Humorous inversion: the villain runs away instead of the hero; the hero pursues [Rs-Pr]".
- **Name:** this grammar's. **Corpus:** 1, 150 II. **Tree test:** `A K Rs Pr`, the Rs under `RescueFirst`.
- **EBNF:** `RescueFirst = rescue Digression {rescue Digression} [ pursuit Digression {pursuit Digression} LateStruggle ]`
- **Literal meaning:** A total role reversal where the hero captures or rescues the initiative immediately following the liquidation, forcing the villain into flight while the hero gives chase. The grammar ensures this pathway is available across the entire corpus, tracking the hero as the pursuer and the villain as the fleeing target.
- **Cultural meaning:** The absolute reversal of sovereignty. The placement of rescue before pursuit represents the complete, sudden collapse of the adversary’s power. Culturally, this structural path demonstrates that true liquidation does not merely stop a threat. It strips the threat of all agency, completely reversing the roles of predator and prey. By converting the hero into an active pursuer who drives chaos out of the world, the sequence proves that the ultimate goal of maturation is not just reactive survival, but the total assumption of assertive, sovereign authority over the environment.

### `LateStruggle`

- **Kind:** group. **Level:** move.
- **Holds:** struggle H, branding J and victory I, after a pursuit.
- **Warrant:** p.107: "In tales 93 and 159 the fight with the villain takes place only after pursuit."
- **Name:** this grammar's; `CombatAfterPursuit` before. **Corpus:** 1, 93 III. **Tree test:** `A K down Pr J`, the J under `LateStruggle`.
- **EBNF:** `LateStruggle = {struggle Digression} {branding Digression} {victory Digression}`
- **Literal meaning:** The primary combat sequence structurally displaced to the end of the return journey, where the definitive defeat of the adversary occurs only after they have pursued the hero back to the threshold of the domestic world.
- **Cultural meaning:** The absolute defense of the threshold. The late struggle represents the mandatory, defensive annihilation of a lingering threat before re-entering civilization. Culturally, this displacement demonstrates that certain systemic crises cannot be outrun or bypassed through clever evasion—they must be met in a final, symmetry-breaking clash at the border of the community. By securing victory and an identifying brand at the literal doorstep of home, the sequence serves as a public validation of the hero's protective power, ensuring that past chaos is permanently severed before the new order can be founded.

### `Ordeal`

- **Kind:** group. **Level:** move.
- **Holds:** the false hero's posture, then the task.
- **Warrant:** editorial.
- **Name:** v43's, less the recognition, which exchanges in the endgame since step 3. **Corpus:** 13. **Tree test:** `A K o L M N`, the M under `Ordeal`, and `A K o L M N Q`, where the Q is not.
- **EBNF:** `Ordeal = FraudPosture TaskAndSolution`
- **Literal meaning:** A macro-level structural container tracking the public verification of the hero's achievements. It pairs the fraudulent claims made by internal pretenders with the execution of a difficult task designed to objectively test the candidates.
- **Cultural meaning:** The institutional unmasking of fraud. The ordeal represents a society's defense against internal moral corruption. Culturally, the presence of a false hero demonstrates that the domestic sphere can be compromised by political deception and unearned claims to power. By forcing all claimants to submit to an impartial, difficult task, the narrative proves that a healthy community must rely on objective testing rather than empty rhetoric, using the trial as a structural filter to separate true capability from fraudulent postures before power can be safely inherited.

### `FraudPosture`

- **Kind:** pair. **Level:** move.
- **Holds:** unrecognized arrival o, then unfounded claims L.
- **Warrant:** p.104: unrecognized arrival and unfounded claims shift between the two summed schemes together.
- **Name:** v43's. **Corpus:** 7. **Tree test:** `A K o L`, the L under `FraudPosture`.
- **EBNF:** `FraudPosture = {unrecognizedArrival Digression} {unfoundedClaims Digression}`
- **Literal meaning:** The phase where the hero reenters the domestic space incognito while a false claimant aggressively asserts authorship over the hero's deeds. This juxtaposition opens a fundamental crisis of identity and recognition within the community.
- **Cultural meaning:** The staging of structural contrast. Rather than a moralistic lecture on passive humility or patience, this sequence represents the strategic necessity of liminal anonymity. Culturally, the hero's unrecognized arrival functions as a protective shield against immediate political reprisal, while the false hero's unfounded claims expose the inherent blindness of an unverified social hierarchy. By deliberately driving true merit to the absolute bottom of society while elevating fraudulence to the top, the structure creates an intense, unsustainable contrast—proving that domestic appearances are dangerously deceptive and setting a high-stakes trap that will inevitably collapse under the weight of objective truth.

### `TaskAndSolution`

- **Kind:** group, around the pair M–N. **Level:** move.
- **Holds:** difficult task M, branding J and solution N. The J comes only after a task.
- **Warrant:** p.104, the task scheme M J N, set in the position H J I holds in the other scheme. The J only after M is the repair v44's own comment names, applied at step 5.
- **Name:** this grammar's; v43's `TaskCycle` before. **Corpus:** 9. **Tree test:** `A K M J N`, the J under `TaskAndSolution` and not under `StruggleAndOutcome`.
- **EBNF:** `TaskAndSolution = [ difficultTask Digression {difficultTask Digression} {branding Digression} ] {solution Digression}`
- **Literal meaning:** The sequence where the candidate is presented with an extraordinarily difficult trial and successfully executes it. This institutional test acts as the structural equivalent to the primary wilderness combat, serving as a civilized arena to verify the claimant's achievements.
- **Cultural meaning:** **The Institutional Filter of Objective Capability.** The task and solution function as an impartial, institutional filter. Culturally, by treating the civil trial as the precise structural equivalent of a physical battle, the narrative proves that leadership requires real-world alignment with fundamental cultural and cosmic laws. By forcing candidates to produce tangible results through the activation of their accumulated ancestral or environmental alliances, the sequence completely strips away the false hero's empty rhetoric, making the true hero’s legitimacy visible and undeniable to the entire collective.

### `Endgame`

- **Kind:** group of four exchangeable functions. **Level:** move.
- **Holds:** recognition Q, exposure Ex, punishment U and wedding W, in any order.
- **Warrant:** p.108: "Recognition and exposure, marriage and punishment may also exchange positions", on finding FN's reading that the four exchange among themselves.
- **Name:** v44's word for the span. **Corpus:** 38. **Tree test:** `A K U Q W`, both U and Q under `Endgame`.
- **EBNF:** `Endgame = { ( recognition | exposure | punishment | wedding ) Digression }`
- **Literal meaning:** The final settlement of accounts closing the move. It encompasses the public recognition of the true hero, the systematic exposure and punishment of the false claimant, and the hero's ascension to power and marriage. The fluid ordering allows these elements to execute interchangeably to resolve the remaining narrative tension.
- **Cultural meaning:** The reconstitution of social order. The endgame represents the permanent collapse of illusion and the total stabilization of the community. Culturally, the interlocking of recognition and exposure functions as a systemic purge, permanently separating true capability from deceptive rhetoric to restore absolute truth to the state hierarchy. By culminating in a sovereign wedding and ascension, the narrative successfully closes the macro-cycle, reestablishing a pure, uncorrupted family order at the head of the collective and securing the foundation for the next generation of heroes.

## Dependencies, not productions

**J–Q: the mark and the recognition.**
Branding J (XVII) falls inside `TroubleToLiquidation`, and recognition Q (XXVII) falls outside it, so the two spans cross, and a single tree cannot hold both (finding FP).
A–K is the constituent, and J–Q is carried as a dependency: the J in `StruggleAndOutcome` marks the hero whom the Q in `Endgame` recognizes.
Its meaning is the thread across the move: the wound or ring of the fight is the proof that settles the hero's claim at the end.

## Extensions, commented out

Two extensions from v43 are overlaid on v46 and shipped commented out, as decided (step 10), and a second tragic variant joined them (step 11). They are not part of the grammar as it stands, so they have no entries above; switched on, they add these.

- **`TragicFall`, with `StruggleOutcome` and the defeat sign I-.** *Literal meaning:* the combat ends not in victory but in the hero's defeat, exposure and punishment. *Cultural meaning, v43's reading:* tragedy is not a separate genre but the shadow of the warrior tale, the same rising action with force failing; to lose the conflict is to be revealed as not the hero one claimed. *Warrant:* v43's proposal, not Propp's; no page licenses it and no corpus tests it.
- **`LateFall`, with the reversal sign Rv (step 11).** *Literal meaning:* a move that succeeds, the lack liquidated or the task solved and the queen married, and then turns: recognition, exposure and punishment fall on the hero. *Cultural meaning, draft:* success is not safe from its own consequences; a hero who has taken what was forbidden, like Prometheus the fire, or who has done unknowingly what may not be done, like Oedipus, is brought down after triumph. It is the tragic ending of the Greek myths that end in punishment, reached by the same Proppian road as the triumphant tale. *Warrant:* Aristotle's reversal and recognition (*peripeteia* and *anagnorisis*, *Poetics*), not Propp. The combat fall of `TragicFall` and the fall after success are the two tragic variants: one where force fails, one where success itself is overturned. *Success is a matter of perspective:* Propp defines each function by its meaning for the hero (p.81), so from Prometheus's side taking the fire liquidates humanity's lack and the punishment is a reversal, while from Zeus's side the same events are a villainy and the villain's punishment, an ordinary Proppian tale v46 already accepts. The reversal sign marks the choice to tell the fallen figure's tale, which is why the grammar does not require a success before it. *Scope, untested:* together the two variants are meant to cover the endings of Greek myth, of myth generally, and of any genre not bound to a happy ending, Proppian at the core with the ending turned; this is speculation until a corpus of such tales is transcribed and run.
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

**How the hero receives the agent carries meaning, and it is measured, not read in.**
Sorting every agent in the corpus by step 6's split, which the grammar's own LL(1) constraint forced, gives three findings (`agentForms.py`). An agent received at home is always given, made or bought, never found or appearing or seized. Seizure comes only after a test, where Propp binds it to a hostile donor. And an offer of service comes after a test 7 times in 8, the donor repaying the hero's kindness. Meaning falls out of the form here, which is the kind of evidence an answer to the charge that Propp's structure is empty needs.

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
- **What happens:** A member of the family leaves home, the elders going out to work, to war, or to trade; the death of parents is its intensified form.
- **Group:** `preparatorySection`, or inside `RuleViolation` when told after the interdiction. **Pairs:** none; it is the one preparatory function outside every pair. **Corpus:** 0.
- **Literal meaning:** The physical or symbolic withdrawal of domestic protection. The removal of the guardians leaves the initial household structurally unguarded, preparing the vulnerability required for the incoming misfortune.
- **Cultural meaning:** The dissolution of domestic shielding. Absentation represents the mandatory collapse of childhood safety. Culturally, the departure or death of the elders serves as the initial phase of a rite of passage—violently exposing the young to reality and forcing them out of passive dependency so they can eventually cross into the wild zone where the trials of maturity must take place.

### `interdiction`

- **Number and sign:** II, γ. **Page:** p.26. **Propp's name:** interdiction.
- **What happens:** the hero is forbidden something; in the inverted form, he is ordered or advised to do something.
- **Group:** `RuleViolation`. **Pairs:** with violation, γ-δ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** A verbal rule or boundary is established within the household, creating a structural condition where a specific transgression will invite vulnerability or misfortune.
- **Cultural meaning:** The delineation of the taboo. The interdiction establishes the artificial boundary separating childhood security from dangerous autonomy. Culturally, this verbal prohibition defines the absolute limit of domestic protection; it sets up a structural taboo that exists solely to be violated, functioning as the necessary psychological catalyst that will eventually lure the youth across the threshold of the known world.

### `violation`

- **Number and sign:** III, δ. **Page:** p.27. **Propp's name:** violation.
- **What happens:** the interdiction is broken; in the inverted form, the order is carried out.
- **Group:** `RuleViolation`. **Pairs:** with interdiction; it may stand without it (p.27). **Corpus:** 0.
- **Literal meaning:** The execution of the forbidden act, opening the structural breach through which vulnerability or the villain enters the narrative.
- **Cultural meaning:** The activation of transgressive agency. Rather than a moralizing lesson on the consequences of disobedience, the violation represents the necessary step of breaking away from childhood security. Culturally, the breaking of the taboo is the inevitable catalyst for individual maturity; it demonstrates that staying safe inside the domestic sphere yields no progress or growth. By deliberately crossing the forbidden boundary, the youth shifts from a passive object of parental protection to an active subject of their own destiny, accepting the immediate perils of the world as the price of maturation.

### `reconnaissance`

- **Number and sign:** IV, ε. **Page:** p.28. **Propp's name:** reconnaissance.
- **What happens:** the villain tries to find something out, such as where the children are or where a precious object is kept.
- **Group:** `InformationGathering`. **Pairs:** with delivery, ε-ζ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** The physical or strategic intrusion of the villain into the tale to locate an exploitable vulnerability.
- **Cultural meaning:** The intrusion of predatory Intent. Reconnaissance represents the tragic realization that the domestic world is surrounded by calculated malice. Culturally, the villain's scouting phase proves that the safety of the household is constantly under surveillance by forces that do not share its values. It marks the precise moment where passive innocence is targeted by predatory intellect, demonstrating that structural blind spots will inevitably be sought out and tested by the wider world.

------

### `delivery`

- **Number and sign:** V, ζ. **Page:** p.28. **Propp's name:** delivery.
- **What happens:** the villain receives information about his victim.
- **Group:** `InformationGathering`. **Pairs:** with reconnaissance; it may stand without it, as a careless act (p.29). **Corpus:** 0.
- **Literal meaning:** The transmission of vital knowledge to the villain, leaving the victim or the household fully exposed and vulnerable to target selection.
- **Cultural meaning:** The shattering of domestic insularity. Delivery represents the tragic, structural impossibility of absolute isolation. Culturally, the ease with which information leaks to the outside world—whether through active manipulation or a careless act—reveals that the domestic sphere cannot remain a sealed ecosystem forever. It demonstrates that the initiate's vulnerabilities, hidden assets, or baseline naivety will inevitably be pulled into the light of external reality, turning a private household weakness into a catalyst for public crisis.

### `trickery`

- **Number and sign:** VI, η. **Page:** p.29. **Propp's name:** trickery.
- **What happens:** the villain, often disguised, tries to deceive the victim in order to take possession of him or his belongings.
- **Group:** `DeceptionTrap`. **Pairs:** with complicity, η-θ (p.80). **Corpus:** 0.
- **Literal meaning:** The deployment of a fraudulent appearance or false premise by the villain, designed to systematically bypass the victim's defenses before any physical assault occurs.
- **Cultural meaning:** The subversion of domestic codes. Trickery represents the terrifying reality that threat models are rarely obvious. Culturally, the villain's use of a benign disguise or an empathetic offer demonstrates that malice naturally masquerades as something safe, familiar, or helpful. By exploiting the initiate's domestic programming—such as their baseline inclination to trust, obey, or accept a gift—the trickery sequence exposes a harsh truth: the uninitiated mind cannot distinguish true benevolence from strategic manipulation based on appearances alone.

### `complicity`

- **Number and sign:** VII, θ. **Page:** p.30. **Propp's name:** complicity.
- **What happens:** the victim is taken in by the deception and so unwittingly helps the enemy.
- **Group:** `DeceptionTrap`. **Pairs:** with trickery; it may stand without it, as falling asleep unprompted (p.30). **Corpus:** 0.
- **Literal meaning:** The victim’s mechanical assent or surrender of autonomy, providing the final link that translates the villain's deceptive premise into a physical breach.
- **Cultural meaning:** The eclipse of personal autonomy. Complicity represents the tragic but necessary failure of uninitiated intuition. Culturally, the victim’s unwitting submission—whether by accepting a poisoned gift or falling into an unprompted sleep—demonstrates that raw childhood innocence possesses zero structural immunity against calculated manipulation. This total collapse of personal agency functions as the absolute lowest point of the domestic state, leaving the youth utterly helpless to prove that they cannot survive on naive trust alone.

### `villainy`

- **Number and sign:** VIII, A. **Page:** p.30; its forms run to p.34. **Propp's name:** villainy.
- **What happens:** the villain causes harm or injury to a member of the family.
- **Group:** `MoveTrigger`, in the complication. **Pairs:** with liquidation, A-K, the pair that spans the move (p.53). **Corpus:** 53, the opener of each.
- **Measured:** Counted by `villainy.py` and pinned by a test. Of the 55 moves opened by villainy, the villain abducts a person in 19, expels someone in 6, torments at night in 4, spoils the crops and declares war in 3 each, maims, plunders, murders, casts into the sea and casts a spell in 2 each, and seven other forms occur once; 4 are written in roman subforms not decoded here. The typical crime is taking a person, often a daughter, sister or bride. Expulsion, the second most frequent, is Propp's own example of the villain inside the family: a stepmother drives out her stepdaughter (p.33), and he marks two forms, forced marriage and cannibalism, with subforms among relatives (p.34).
- **Literal meaning:** the misfortune from outside that sets a move going. Propp calls the function exceptionally important, since the actual movement of the tale is created by it (p.30).
- **Cultural meaning:** *Draft.* A wrong that demands an answer: injury to the family must be met.

### `lack`

- **Number and sign:** VIIIa, a. **Page:** p.35. **Propp's name:** lack.
- **What happens:** a member of the family lacks something or desires to have something: a bride, a magical agent, a marvel.
- **Group:** `MoveTrigger`, in the complication. **Pairs:** with liquidation, as villainy does. **Corpus:** 26, the opener of each.
- **Literal meaning:** the misfortune from within. It does the work of villainy, leading to a quest in the same way (p.34), and a move begun from it is undone by the same liquidation.
- **Cultural meaning:** *Draft.* A legitimate want, a bride, a wonder, the means of life, as a reason to go out and win it.

### `mediation`

- **Number and sign:** IX, B. **Page:** p.36. **Propp's name:** mediation, the connective incident.
- **What happens:** the misfortune or lack is made known; the hero is asked or commanded, and is allowed to go or is sent.
- **Group:** `complication`, as the dispatch; `MoveTrigger`, where no villainy occurs and it opens the move (p.37). **Pairs:** none. **Corpus:** 41, one of them, 133 II, as an opener.
- **Measured:** Counted by `dispatch.py` and pinned by a test. Of the 43 moves carrying B, the hero is called in 6 (B1), sent in 9 (B2), allowed to go in 8 (B3) and told of the misfortune in 12 (B4); the victimized hero is transported from home in 4 (B5) and lamented in 1 (B7), and never secretly freed (B6). Three more carry B in another function's form, at 144 I, 163 I and 164 II (p.67). Only B2, 9 of the 40 moves with a form, is plain sending by command or request. The Corpus figure of 41 counts the moves v46 accepts; the other two, 126 II and 137 II, are among the four it rejects.
- **Literal meaning:** the hero is drawn in. It connects the misfortune to the one who will act on it.
- **Cultural meaning:** *Draft.* The need is made known and the way out is opened; the answering is the hero's. In most forms the one who brings the news or gives leave does not command, and the young one volunteers.

### `beginningCounteraction`

- **Number and sign:** X, C. **Page:** p.38. **Propp's name:** beginning counteraction.
- **What happens:** the seeker agrees to or decides on counteraction.
- **Group:** `complication`. **Pairs:** none. **Corpus:** 61.
- **Literal meaning:** the hero's decision to act, the moment the tale turns from suffering to seeking.
- **Cultural meaning:** *Draft.* Accept responsibility and decide to act; the hero chooses.

### `departure`

- **Number and sign:** XI, ↑. **Page:** p.39. **Propp's name:** departure.
- **What happens:** the hero leaves home.
- **Group:** `complication`, which it closes; or `EarlyLeaving`, before the crisis (p.107). **Pairs:** none named, though it faces the return. **Corpus:** 66.
- **Literal meaning:** setting out. With villainy, dispatch and counteraction it completes the complication (pp.64-65).
- **Cultural meaning:** *Draft.* Leave home to make one's own way.

### `firstDonorFunction`

- **Number and sign:** XII, D. **Page:** p.39. **Propp's name:** the first function of the donor.
- **What happens:** the hero is tested, questioned or attacked, which prepares the way for his receiving a magical agent or helper.
- **Group:** `TestedAcquisition`, which it opens; or `EarlyHelp`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of F (pp.46-47). **Corpus:** 31.
- **Literal meaning:** the test. The donor probes whether the hero is worthy of help.
- **Cultural meaning:** *Draft.* Be courteous and kind to strangers, the old, the weak and animals: one is always being tested.

### `heroReaction`

- **Number and sign:** XIII, E. **Page:** p.42. **Propp's name:** the hero's reaction.
- **What happens:** the hero reacts to the actions of the future donor, well or badly.
- **Group:** `TestedAcquisition`, which it opens when the test is omitted; or `EarlyHelp`, before the crisis (p.107). **Pairs:** with the test it answers. **Corpus:** 32.
- **Literal meaning:** the hero's answer to the test, which decides whether help is given.
- **Cultural meaning:** *Draft.* The right response to the test, politeness, compassion, sharing, a kept word; here the tale's ethics are taught most plainly.

### `receiptOfMagicalAgent`

- **Number and sign:** XIV, F. **Page:** p.43. **Propp's name:** provision or receipt of a magical agent.
- **What happens:** the hero acquires the use of a magical agent: an animal, an object, a quality.
- **Group:** `TestedAcquisition` after a test or reaction; `UntestedAcquisition` otherwise, in the complication (step 6); or `EarlyHelp`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of D (pp.46-47). **Corpus:** 40; the tested agent appears in 32 moves and the untested in 17.
- **Measured:** Counted by `agentForms.py` over the 84 move-strings, the parked cells left of A excluded, and pinned by a test. Of 57 F cells, 35 are tested (after a D or E), 12 untested before the departure, and 10 untested on the road. THREE FINDINGS: (1) an agent received at home never comes by chance or by magic: all 12 are transferred (6), prepared (5) or bought (1), and none is found, appears, is seized or offers service; (2) seizure follows a test every time, 3 of 3, as Propp binds seizure to a hostile preparation (pp.46-47); (3) an offer of service follows a test 7 times in 8, the grateful creature repaying the hero's mercy. On the road, 3 of 10 untested agents appear of their own accord. The counts are small, and "tested" means a D or E came earlier in the move.
- **Literal meaning:** the means of undoing the misfortune. Earned from a donor, it is a reward; received without a test, from a father or by finding, it comes with the setting out.
- **Cultural meaning:** *Draft.* Help earned is power. Those who behave rightly are equipped by others, and what was promised in return is paid.

### `spatialTransference`

- **Number and sign:** XV, G. **Page:** p.50. **Propp's name:** spatial transference between two kingdoms, guidance.
- **What happens:** the hero is carried, delivered or led to where the object of his search is.
- **Group:** `Development`. **Pairs:** none. **Corpus:** 25.
- **Literal meaning:** the passage to the other kingdom, where the misfortune can be undone.
- **Cultural meaning:** *Draft.* Go where the task is, however far.

### `struggle`

- **Number and sign:** XVI, H. **Page:** p.51. **Propp's name:** struggle.
- **What happens:** the hero and the villain join in direct combat.
- **Group:** `StruggleAndOutcome`, or `LateStruggle` after a pursuit (p.107). **Pairs:** with victory, H-I (p.64). **Corpus:** 25.
- **Literal meaning:** the confrontation with the villain himself.
- **Cultural meaning:** *Draft.* Face the adversary.

### `branding`

- **Number and sign:** XVII, J. **Page:** p.52. **Propp's name:** branding, marking.
- **What happens:** the hero is marked: wounded in the fight, or given a ring or a towel.
- **Group:** `StruggleAndOutcome` in the fight; `TaskAndSolution` after a task (p.104; step 5); `LateStruggle` after a pursuit. **Pairs:** with recognition, J-Q, the one crossing pair, carried as a dependency. **Corpus:** 2.
- **Literal meaning:** the sign by which the hero will be known. It is rare in the corpus and central to the end, since it is what recognition reads.
- **Cultural meaning:** *Draft.* Bear the marks of what you have done; they will vouch for you.

### `victory`

- **Number and sign:** XVIII, I. **Page:** p.53. **Propp's name:** victory.
- **What happens:** the villain is defeated, in combat, in a contest, or by other means.
- **Group:** `StruggleAndOutcome`, or `LateStruggle`. **Pairs:** with struggle; it may stand without it (p.29). **Corpus:** 33.
- **Literal meaning:** the villain's power broken.
- **Cultural meaning:** *Draft.* Right prevails.

### `liquidation`

- **Number and sign:** XIX, K. **Page:** p.53. **Propp's name:** none given; he designates it K and describes it as the liquidation of the initial misfortune or lack.
- **What happens:** the initial misfortune or lack is undone: the object seized, the spell broken, the dead revived, the captive freed.
- **Group:** `TroubleToLiquidation`, which it closes. **Pairs:** with villainy, A-K; Propp says the narrative reaches its peak in it (p.53). **Corpus:** 47.
- **Literal meaning:** the undoing of the misfortune, the point every move is heading for.
- **Cultural meaning:** *Draft.* Set right what was wronged and restore what was lost; Propp calls it the tale's peak (p.53).

### `return`

- **Number and sign:** XX, ↓. **Page:** p.55. **Propp's name:** return.
- **What happens:** the hero returns.
- **Group:** `ReturnJourney`. **Pairs:** none named, though it faces the departure. **Corpus:** 42.
- **Literal meaning:** the way home, opening the second half of the move.
- **Cultural meaning:** *Draft.* Bring home what you won; the achievement serves the family.

### `pursuit`

- **Number and sign:** XXI, Pr. **Page:** p.56. **Propp's name:** pursuit, chase.
- **What happens:** the hero is pursued.
- **Group:** `Evasion`, first in `PursuitFirst` and second in `RescueFirst`. **Pairs:** with rescue, Pr-Rs (p.64); inverted in the humorous tale (p.147). **Corpus:** 14.
- **Literal meaning:** the villain's last attempt: what was undone is threatened again.
- **Cultural meaning:** *Draft.* Success invites reprisal.

### `rescue`

- **Number and sign:** XXII, Rs. **Page:** p.57. **Propp's name:** rescue.
- **What happens:** the hero is rescued from pursuit.
- **Group:** `Evasion`. **Pairs:** with pursuit. **Corpus:** 14.
- **Literal meaning:** the threat escaped, and many tales end here (p.92 lists it among the denouements).
- **Cultural meaning:** *Draft.* Help earned earlier saves you later.

### `unrecognizedArrival`

- **Number and sign:** XXIII, o. **Page:** p.60. **Propp's name:** unrecognized arrival.
- **What happens:** the hero arrives home or in another country unrecognized.
- **Group:** `FraudPosture`. **Pairs:** with unfounded claims, as they move together between the two schemes (p.104). **Corpus:** 5.
- **Literal meaning:** the hero without his due: present, but not known.
- **Cultural meaning:** *Draft.* Merit may go unrecognized for a time; be patient and humble.

### `unfoundedClaims`

- **Number and sign:** XXIV, L. **Page:** p.60. **Propp's name:** unfounded claims.
- **What happens:** a false hero presents unfounded claims to the hero's deed.
- **Group:** `FraudPosture`. **Pairs:** with unrecognized arrival; and it prepares exposure. **Corpus:** 6.
- **Literal meaning:** the hero's deed usurped, which the end of the tale must correct.
- **Cultural meaning:** *Draft.* The braggart who claims another's deed will be shamed; do not take credit you have not earned.

### `difficultTask`

- **Number and sign:** XXV, M. **Page:** p.60. **Propp's name:** difficult task.
- **What happens:** a difficult task is proposed to the hero: an ordeal, a riddle, a test of strength or endurance.
- **Group:** `TaskAndSolution`. **Pairs:** with solution, M-N, set in the scheme where H-I stands in the other (p.104). **Corpus:** 9.
- **Literal meaning:** the hero's worth tested by trial rather than by combat. Propp finds it typical of a second move (p.104).
- **Cultural meaning:** *Draft.* Prove yourself worthy of the bride and the position.

### `solution`

- **Number and sign:** XXVI, N. **Page:** p.62. **Propp's name:** solution.
- **What happens:** the task is accomplished; a solution before the task is set Propp designates *N (p.62).
- **Group:** `TaskAndSolution`. **Pairs:** with difficult task; it may stand without it, as the preliminary solution (commentary p.145). **Corpus:** 9.
- **Literal meaning:** the trial passed.
- **Cultural meaning:** *Draft.* Competence proven: success validates the hero's status, as the task cycle shows.

### `recognition`

- **Number and sign:** XXVII, Q. **Page:** p.62. **Propp's name:** recognition.
- **What happens:** the hero is recognized, by a mark, a thing given him, a task accomplished, or after long separation.
- **Group:** `Endgame`, exchangeable with exposure, punishment and wedding (p.108). **Pairs:** with branding, J-Q, as a dependency; with exposure. **Corpus:** 7.
- **Literal meaning:** the hero known for who he is, the undoing of the unrecognized arrival.
- **Cultural meaning:** *Draft.* True worth is acknowledged in the end.

### `exposure`

- **Number and sign:** XXVIII, Ex. **Page:** p.62. **Propp's name:** exposure.
- **What happens:** the false hero or villain is exposed.
- **Group:** `Endgame`. **Pairs:** with recognition; it answers the unfounded claims. **Corpus:** 5.
- **Literal meaning:** the false claim undone.
- **Cultural meaning:** *Draft.* Lies are found out.

### `transfiguration`

- **Number and sign:** XXIX, T. **Page:** pp.62-63. **Propp's name:** transfiguration.
- **What happens:** the hero is given a new appearance: new garments, a palace, a handsome form.
- **Group:** none; it stands in `EarlyTransfiguration` before an opener or in `Digression` after any function, since Propp calls it the most unstable function in relation to its position (p.108). **Pairs:** none. **Corpus:** 6.
- **Literal meaning:** the hero's new estate made visible. Its free place is itself a finding: it is the one function whose position means nothing.
- **Cultural meaning:** *Draft.* Worth made visible: the hero comes to look like what the hero is.

### `punishment`

- **Number and sign:** XXX, U. **Page:** p.63. **Propp's name:** punishment.
- **What happens:** the villain or false hero is punished; the magnanimous pardon is its negative form.
- **Group:** `Endgame`. **Pairs:** with wedding, the two exchanging (p.108). **Corpus:** 15.
- **From Propp:** punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and the father often punishes the false hero (pp.79-80). The first villain's end is usually his defeat in combat, victory I, in the hero's sphere of action.
- **Literal meaning:** the wrong answered.
- **Cultural meaning:** *Draft.* Wrongdoers get what they deserve, or, in the pardon, receive the victor's magnanimity.

### `wedding`

- **Number and sign:** XXXI, W. **Page:** p.63. **Propp's name:** wedding.
- **What happens:** the hero marries and ascends the throne; the reward without marriage folds into it.
- **Group:** `Endgame`. **Pairs:** with punishment. **Corpus:** 34.
- **Literal meaning:** the hero's due given, the most common close of a move, and the denouement p.92 names first.
- **Cultural meaning:** *Draft.* The goal of the passage: marriage and the founding of a new household, which begins the next cycle.

## Elements that are not functions

Two terminals of v46 are elements Propp names but does not number, so they stand outside the functions above.

- **`initialSituation`, α.** p.25: the tale usually begins with some initial situation, the members of a family enumerated or the future hero introduced; it is not a function, but an important morphological element. In v46 it stands at the beginning of the tale only, outside every move. **Corpus:** 0, since the move-strings carry none.
- **`preliminaryMisfortune`, λ.** Appendix I Table II item 44, p.121: a misfortune that compels the victim's assent within the deceitful agreement. In v46 it stands inside `DeceptionTrap`, between trickery and complicity. **Corpus:** 0.

The six remaining terminals, `/`, `⟨`, `⟩`, `<`, `Y` and `}`, are signs of how moves combine, and their meaning is given under `tale`, `FollowingMoves`, `EmbeddedMove`, `Parting` and `CommonEnding`.

## Dramatis personae

**Propp's seven spheres of action, entered as roles, as decided for now.**
p.79: many functions "logically join together into certain spheres", which "correspond to their respective performers"; p.80 concludes that the tale has seven dramatis personae.
A sphere is a role, not a person: one character may fill several spheres, and one sphere may be spread across several characters (pp.80-81). The father who dispatches his son and gives him a cudgel is dispatcher and donor at once (p.81).
The preparatory functions are distributed among the same characters, but too unequally to define them (p.80), so they appear in no entry below.

**THE ORDER IS ONE OF SOCIAL RANK, AND IT IS SPECULATION, NOT PROPP.**
Highest status goes to the hero, then the princess and her father, the dispatcher, the donor, the helper, the false hero, and the villain.
Propp does not order the spheres. On the speculative reading set out above, they outline the social hierarchy of Indo-European culture, recursive from the state down to the family group, the state being cast as a family.
Each entry's "place in the social order" line applies that reading, and the cultural meanings are drafted with it in mind. Both are drafts.

Each entry gives Propp's sphere and page, the functions he assigns it, the groups of v46 where they act, how many of the 80 accepted move-strings use at least one of them, its place in the social order, and its literal and cultural meaning.

### `hero`

- **Propp's sphere:** 6, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), `wedding` (W*). Propp: C is characteristic of the seeker-hero; the victim-hero performs only the rest.
- **Acts in:** `complication`, `TestedAcquisition` and `EarlyHelp`, `Endgame`. **Corpus:** 79.
- **From Propp:** p.81: characters are defined not by what they want or feel but by "their deeds as such, evaluated and defined from the viewpoint of their meaning for the hero and for the course of the action". To that extent the hero-centered reading is Propp's own method, not speculation.
- **From Propp:** pp.36-38: after a villainy the narrative follows either the one who goes in search, a seeker, or the one seized or driven out, a victimized hero, and no tale in Propp's material follows both (p.36). The forms of mediation tell which: B1-B4 refer to the seeker and B5-B7 to the victimized hero (p.37), and the decision to act, C, belongs only to tales whose hero is a seeker (p.38).
- **Measured:** Counted by `heroType.py` and pinned by a test; it reproduces the first project's findings BM and BO. Of the 32 tales carrying B, 26 follow a seeker and 3 a victimized hero, tales 95, 98 and 101; 3 carry B only in forms without a variety digit, and none follows both, as p.36 says. Of the 37 moves in which B and the departure stand together, 30 are seeker moves and 4 victim moves. The decision to act divides less cleanly than p.38 says: C stands in 27 of the 30 seeker moves and in 3 of the 4 victim moves. The seeker is the usual hero, 26 tales to 3; the victimized hero is Propp's own, and rare.
- **Place in the social order:** *Draft.* Highest, and the center. Every other role is defined by what it does to or for the hero, and ends as an audience for the hero's story.
- **Literal meaning:** the one whose fortunes the tale follows (p.36). Usually a seeker, who decides to act and sets out, answers the donor's test, and is married at the end; sometimes a victim of the villainy, carried off or driven out, who, Propp says, performs all the hero's functions except the decision to act (p.38).
- **Cultural meaning:** *Draft.* The model for the young listener: the one who heeds, chooses, dares, keeps faith and endures, and so rises from dependent youth to the head of a household. The hero is usually, but not always, the chooser and the leader: the victimized hero does not choose, and is the hero all the same, because the tale follows that hero's fortunes.

### `princessAndFather`

- **Propp's sphere:** 4, pp.79-80. **Functions:** `difficultTask` (M), `branding` (J), `exposure` (Ex), `recognition` (Q), `punishment` (U), `wedding` (W). Propp: the princess and her father "cannot be exactly delineated from each other according to functions"; most often the father assigns the tasks, from hostility to the suitor, and punishes the false hero.
- **Acts in:** `TaskAndSolution`, `StruggleAndOutcome` for the branding, `Endgame`. **Corpus:** 38.
- **Place in the social order:** *Draft.* Second, and peripheral to the hero's story. The king is the head of state and of the family, a placeholder until the next generation succeeds, who assigns the tasks and grants the kingdom. The princess chooses the hero, but is defined by her role as his mate and the mother of his line.
- **Literal meaning:** the sought-for person and her father, who set the hard task, mark the hero, recognize the true hero and expose the false one, punish the impostor, and give the marriage.
- **Cultural meaning:** *Draft.* The house the hero joins. The king assigns and grants, the princess chooses, and the outcome is never in doubt. The tales bend both roles freely: the king may favor or resist the hero, and the princess may choose at once or require to be won. Two earlier readings survive as the range within which the tales vary: *succession and exchange*, the father controlling who marries into the house and so who inherits, and *judgment and agency*, the princess marking, recognizing and exposing, so that the true hero is known through her discernment.

### `dispatcher`

- **Propp's sphere:** 5, p.80. **Functions:** `mediation` (B), the dispatch.
- **Acts in:** `complication`, and `MoveTrigger` when the connective incident opens a move. **Corpus:** 41.
- **From Propp:** the dispatcher's sphere holds the dispatch alone (p.80), and its seven forms name who fills it (pp.36-38). The call for help usually comes from the tsar (B1). With leave to depart the initiative often comes from the hero, not from a dispatcher, and the parents bless (B3). The misfortune is announced more often by old women or persons met by chance than by parents (B4). The banished daughter is taken to the forest by her father, whose act Propp calls logically unnecessary: the tale demands parent-senders (B5, p.37). The hero condemned to death is freed by a cook or an archer (B6), and the lament is sung by a surviving brother (B7).
- **Measured:** Counted by `dispatch.py` and pinned by a test; the forms are tallied under `mediation`. In 31 of the 40 moves where B carries a form, the dispatcher calls, permits, announces, transports or laments; only in 9 is the hero sent outright, by command or request.
- **Place in the social order:** *Draft.* Third as a role, but mixed in rank as a person. The sphere is filled by the tsar, by parents, by old women and strangers met on the road, by a cook or an archer, and by a brother. A role filled from so wide a range of rank marks the dispatcher as a minor character: a role defined by one moment, the push out of the door, rather than by who performs it.
- **Literal meaning:** the one who makes the need known and opens the way out: calls for help, sends, permits, announces, transports or frees. Only the direct dispatch is plain sending; in most forms the dispatcher informs or permits, and the hero decides.
- **Cultural meaning:** *Draft.* Authority opens the way, and the young one chooses to take it. The elder proclaims, announces or blesses, and the hero volunteers, as with the king who assigns and grants. The tale wants the push to come from home, since Propp finds it demanding parent-senders even where the action needs none (p.37); yet the news comes more often from strangers than from parents. What matters is less who sends than that the hero answers.

### `donor`

- **Propp's sphere:** 2, p.79. **Functions:** `firstDonorFunction` (D), `receiptOfMagicalAgent` (F).
- **Acts in:** `TestedAcquisition`, `EarlyHelp`, and, when the agent comes with no test, `UntestedAcquisition`. **Corpus:** 45.
- **Place in the social order:** *Draft.* Fourth. The elder or the outsider of power who judges the hero and endows him.
- **Measured:** From the donor's side, counted by `agentForms.py` and pinned by a test: the tested agent is the donor's gift, 35 cells in 28 moves. The father's gift at home, where the father is dispatcher and donor at once (p.81), is always given, made or bought, 12 of 12. Seizure, 3 of 3, comes only after a test, which is where Propp binds it to a hostile donor (pp.46-47). An offer of service comes after a test 7 times in 8: the donor repays the hero's kindness.
- **Literal meaning:** the one who tests the hero and provides the magical agent.
- **Cultural meaning:** *Draft.* The test of character. Honor the donor and keep the bargain: the hero never cheats a friendly donor of what was agreed. Against a hostile or deceitful donor guile is allowed, good faith being owed to good faith (pp.46-47). The father's gift, where the father is dispatcher and donor at once (p.81), comes by right of family and not by test.

### `helper`

- **Propp's sphere:** 3, p.79. **Functions:** `spatialTransference` (G), `liquidation` (K), `rescue` (Rs), `solution` (N), `transfiguration` (T).
- **Acts in:** `Development`, `TroubleToLiquidation`, `Evasion`, `TaskAndSolution`, and `EarlyTransfiguration` or `Digression` for T. **Corpus:** 68.
- **From Propp:** p.82: living things, objects and qualities "function in exactly the same manner"; Propp calls the living ones magical helpers and the objects and qualities magical agents. A carpet that carries the hero is the same, morphologically, as a horse that does, and so is the hero's own acquired ability to become a falcon. He distinguishes three kinds: universal helpers, which can perform all five functions, and in his material only the steed; partial helpers, such as animals, spirits appearing out of rings, and what the English translation calls "various tempters"; and specific helpers, performing one function, which are objects only. HELPERS CAN BE PEOPLE: the little iron peasant who rewards Ivan and then helps kill the dragon is donor and helper at once (p.80), and the "tempters" of the English may render a Russian word for skilled or wonder-working people, which has still to be checked against the Russian.
- **Measured:** Counted by `agentForms.py --helper` and pinned by a test. Of the 84 moves, 43 receive an agent and 41 do not. Transference follows the gift: it occurs in 16 of the 43 (37%) against 9 of the 41 (22%), as in Propp's own example of the flying horse and carpet. The other helper functions show no such difference, and liquidation is less common where an agent is received, 24 of 43 against 27 of 41. APPENDIX III RECORDS FUNCTIONS, NOT PERFORMERS, so the corpus cannot say who performed a helper's function, the helper or the hero; that would take reading the tales.
- **Place in the social order:** *Draft.* Fifth. The sidekick: a Sancho Panza to Don Quixote, a Tonto to the Lone Ranger.
- **Literal meaning:** the one who carries the hero, undoes the misfortune, rescues from pursuit, solves the tasks and transforms the hero. The horse that does all of these is Propp's pure helper (p.80).
- **Cultural meaning:** *Draft.* Loyal service, which the hero earns and commands. The helper may do much of the work, but the credit rises to the hero, who chooses and leads.

### `falseHero`

- **Propp's sphere:** 7, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), and, as his specific function, `unfoundedClaims` (L).
- **Acts in:** `complication`, `TestedAcquisition`, `FraudPosture`. **Corpus:** 6 by his specific function L; the rest he shares with the hero, and 77 moves hold one of C, ↑ or E.
- **From Propp:** the false hero is the "second villain" whose punishment belongs to the sphere of the princess and her father, the father frequently punishing him or ordering him punished (pp.79-80).
- **Place in the social order:** *Draft.* Sixth. An object of derision, and often the butt of humor.
- **Measured:** Counted by `falseHero.py` and pinned by a test. The false hero's claim L appears in 5 tales, 125, 132, 139, 155 and 156, and in every one of them it stands in the tale's last move; for 125, in the shared ending that closes both moves. In all 5 the false hero is punished (U) and the tale ends in the wedding (W). The true hero is recognized (Q) in 4, all but 156, and the false hero is exposed by name (Ex) in 3, 125, 132 and 155. In 4 of the 6 move-strings holding an L, the hero's unrecognized arrival (o) stands beside it, the o-L pairing of p.104. He never appears early, never in a middle move, and never escapes.
- **Literal meaning:** the one who sets out as the hero does and meets the donor, but claims the hero's deed without right.
- **Cultural meaning:** *Draft.* The liar, and the tale's scapegoat. The false hero breaks a cardinal Indo-European rule, do not tell lies, and that puts him at the bottom of the order beside the villain: the Old Persian inscriptions name the Lie as the root of evil, Herodotus says Persian boys were taught to ride, to shoot and to speak the truth, and the Avestan asha against druj and the Vedic ṛta against anṛta set truth against the lie as order against disorder. He is the counterfeit of the hero, setting out and meeting the donor as the hero does but failing the test, so he has no deed and can only claim one; the mark from the fight (J) is what the recognition reads (Q) to tell the true hero from him. His exposure moves from anger through punishment to derision: the surprise of the unmasking is where the humor lies, and once found out he becomes the butt of the joke, as the boastful soldier of Plautus's Miles Gloriosus and Falstaff at Gad's Hill are, and as frauds were tarred and feathered in nineteenth-century rural America. He is judged by the head of the house, not fought like the villain, and he is never let go.

### `villain`

- **Propp's sphere:** 1, p.79. **Functions:** `villainy` (A), `struggle` (H), `pursuit` (Pr).
- **Acts in:** `MoveTrigger`, `StruggleAndOutcome` and `LateStruggle`, `Evasion`. **Corpus:** 62.
- **From Propp:** the villain's sphere is villainy, struggle and pursuit (A, H, Pr; p.79), and it does not include punishment. Punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and Propp adds that the father "frequently punishes (or orders punished) the false hero" (pp.79-80). So the first villain is met by the hero in combat and defeated; the liar inside the order is judged by its head.
- **Measured:** Counted by `villainy.py` and pinned by a test. Of the 84 moves, 55 open on villainy and 28 on lack. In the villainy moves the harm is undone (K) in 65%, the villain fought (H) in 35%, defeated (I) in 42%, pursues (Pr) in 20%, and punishment (U) stands in 20%; lack moves run lower on combat, 21% struggle and 36% victory. The tale's business with the villain is undoing the harm, and his own end is often not marked. U does not say who is punished, and a dragon killed in combat is a victory, not a punishment.
- **Place in the social order:** *Draft.* Lowest. Despised: the enemy of the order.
- **Literal meaning:** the one who does harm, fights the hero, and pursues.
- **Cultural meaning:** *Draft.* Evil to be opposed, whose defeat the listener is meant to cheer. When the villain is inside the family, a stepmother or envious sisters, the tale shows where the household order can fail.
