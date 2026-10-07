# Semantic catalog for v46

**This catalog lists every group and pair in the grammar `ProppEBNF46.txt`, with what it holds, where Propp supports it, how often the tales use it, and what it means.**
A few terms first.
Propp's **functions** are the acts of characters he found in the Russian wondertale, thirty-one of them, each with a symbol: A for villainy, K for its undoing, and so on.
A **move** is one run of the story from a misfortune or a lack to its undoing; a tale has one or more.
The **grammar** writes Propp's order of functions as formal rules, in a standard notation called EBNF; each named rule is a **production**, and a **group** is a production that bundles several functions.
The grammar is version 46, **v46**; v43 and v44 are earlier versions, and a **step** is one stage of the work that turned them into v46, recorded in `StepTests.txt`.
The **corpus** is the 80 moves of Propp's Appendix III, his own analyses of 45 tales, that v46 accepts.
This catalog is what `SemanticBundling.md` in the first project was meant to become: every rule that is a real pair or group, and so means more than the functions inside it.
Each entry says whether it is a group or a pair, a production or a dependency, and at which level it sits, with its page and its meaning.

**The catalog is checked, not only written.**
A frozen test in `StepTests.txt` requires one entry here for every group in the grammar, at least one tree test for every group, and no entry for a group the grammar lacks.
A **tree test** feeds the grammar one string of symbols and checks where the grammar's **parse tree**, the way it groups the symbols, puts a given function.
So what an entry says a group holds is tested against the grammar itself.
Run `python runSteps.py 6` to check.

**The dramatis personae close the catalog.**
They are Propp's seven spheres of action, treated as roles, each with a literal and a cultural meaning.
They are ordered by rank, on a speculative reading that is not Propp's.

**The functions follow the groups.**
Single functions carry meaning too, or they would not be in the model.
The section "Functions" near the end gives each of Propp's thirty-one, with lack as VIIIa, and a short section after it gives the two elements Propp names but does not number.

## How to read an entry

- **Kind.** A *pair* is two functions Propp pairs. A *group* is three or more functions he groups, or a group of groups. A *span* runs between two functions and holds the groups between them. A *choice* is one of several alternatives. *Notation* is a device of the grammar and carries no meaning.
- **Level.** Tale or move.
- **Holds.** The functions it can hold, in Propp's symbols.
- **Warrant.** The page where Propp groups or pairs these functions. *Editorial* means no page groups them, and the group is a reading aid only.
- **Name.** Whether the name is Propp's term, v43's, or this grammar's, and, where it was renamed, the name it had before.
  *Early* in a name means before the move's trigger, inside `BeforeTheTrouble`; *Late* means after the liquidation, inside `AfterLiquidation`.
  The two words stand on either side of the A–K span, `TroubleToLiquidation`, the core of every move.
  *First* in `PursuitFirst` and `RescueFirst` is a different matter: which half of a pair comes first.
- **EBNF.** The entry's rule in `ProppEBNF46.txt`, with its comments removed and its lines joined; where an extension replaces the rule, the extension's form follows it.
- **Corpus.** How many of the 80 accepted moves use the group, from `CorpusGroups.txt`. The preparatory groups show 0 because Appendix III prints no preparatory function (p.116), not because the tales lack them.
- **Tree test.** One string from `StepTests.txt` whose parse puts a function in this group.
- **Measured.** Where an entry has one: a finding counted from the corpus by a program in this project, which anyone can rerun, and pinned by a test. It is data, not speculation, and it is kept apart from the cultural meaning for that reason.
- **Literal meaning.** What the group or function says on its surface: the sense a reader first takes from it. A short phrase, then, where needed, a few sentences more.
- **Cultural meaning.** The conduct the tale teaches its young listener, and the value behind that conduct, read from the hero's side. A short phrase, then a few sentences more.
  The cultural meanings rest on a speculative reading, not on Propp; it is set out in the section "A speculative reading, not from Propp", below.
  Unlike the functions and groups, they have nothing in the corpus to anchor them.
  All but the task cycle's are drafts.

## A speculative reading, not from Propp

**Everything in this section is speculation.**
The functions and groups in this catalog are tied to Propp's pages and tested against Appendix III.
The cultural meanings are not, and cannot be until the values they name are studied on their own terms.
They are offered as a reading to be tested, not as a finding.

**The tale reads as a guide for the young.**
It begins when the elders leave the young unprotected, and it ends when the hero marries and takes the throne.
Nothing follows the wedding: there is no function for ruling, for raising heirs or for growing old.
The older figures are present, but the tale gives no guidance for what anyone does after the wedding.

**The hero is the center, and the other roles are nearly an audience.**
Of Propp's thirty-one function headings in Ch. III, eighteen name the hero or the seeker, and none names the princess, her father or the king; even the wedding is the hero's, "married" and taking the throne.
The other roles are defined by what they do to or for the hero.
That much is Propp's own method: he defines characters by the meaning of their deeds "for the hero and for the course of the action" (p.81).
Down the order of rank, the helper is a sidekick, a Sancho Panza to Don Quixote or a Tonto to the Lone Ranger; the false hero is laughed at and often the butt of the joke; and the villain is despised.

**The values read as Western ones.**
The hero is usually the one who chooses and leads, not the follower or the sidekick: the individual who acts on his own account and rises by his own conduct.
Not always: Propp keeps a victimized hero, carried off or driven out, who does not choose and is the hero all the same, because the tale follows that hero's fortunes (p.36).
In his material that hero is rare.
That is set against cultures that value harmony and working together above standing out.
Which Western values the tale carries, and how exactly, is a question still to be studied.

**The family order repeats at every scale and in every generation.**
The same order holds in the kingdom and in a small peasant household; the kingdom is pictured as a family, with the king at its head.
The tale starts from an existing family and ends by founding a new one, whose child will be the next hero, so the pattern repeats through time.
An illustration of the repetition: the Anglo-Saxon Chronicle, in its entry for 855, traces the descent of Alfred's father Æthelwulf back through Woden and Noah to Adam.
It is far too short to be literal, but it is the same founding pattern told generation after generation.

**The outcome is never in doubt.**
The wondertale does not end badly for the hero.
Failures come as setbacks before the success (p.74), and tragedy exists here only as the extension carried over from v43, switched off.
The tale promises success to the young who behave rightly.

**The roles at the edge of the story bend.**
The king may favor the hero or resist him; the princess may choose him at once or need to be won.
The tales vary these freely without changing the end.

## Groups and pairs

### `tale`

- **Kind:** group of the whole. **Level:** tale.
- **Holds:** an optional initial situation α, the preparatory section, then one or more moves separated by `/`.
- **Warrant:** p.92: in terms of form, a tale is any development that starts from a villainy or lack, and each new villainy or lack starts a new move.
- **Name:** Propp's. **Corpus:** not measured; the corpus is made of moves. **Tree test:** `A K / a K`, the second move's `a` under `tale`.
- **EBNF:** `tale = [initialSituation] preparatorySection move FollowingMoves`
- **Literal meaning:** The whole story.
  A misfortune or a want sets it going, and each new one starts a new move inside it.
- **Cultural meaning:** A young person's passage from a home left unprotected to the head of a new home.
  The tale tells this passage as a pattern taken from ancient initiation rites.
  The family order is the same in a kingdom and in a peasant household.
  The tale is a cycle: it starts from one family and ends by founding the next, whose child will be the next hero.

### `FollowingMoves`

- **Kind:** group. **Level:** tale.
- **Holds:** the moves after the first, in sequence, then optionally a parting and a common ending; or a parting straight after the first move.
- **Warrant:** p.93, method 1: "one move directly follows another".
- **Name:** this grammar's; `LaterMoves` before. **Corpus:** 26 of the 45 tales, counting the whole tales of `embedCorpus.py`, where 162's second move sits inside its first. **Tree test:** `A K / a K`, the `a` under `FollowingMoves` and the first A not.
- **EBNF:** `FollowingMoves = [ moveBoundary move {moveBoundary move} [Parting] [CommonEnding] | Parting [CommonEnding] ]`
- **Literal meaning:** How a tale goes on after its first move.
  A reading aid.
  It holds the three ways p.93 lets a tale go on at the level of the whole tale: another move follows, two heroes part, or two moves share one ending.
- **Cultural meaning:** Proof that the hero's success was no accident.
  Each later move raises the stakes and the trials, and makes the hero stronger.
  Each also confirms that the first success showed the hero's true worth.
  Three moves may be an instance of trebling, the magic number three: the first two set the pattern, and the third confirms that the hero is truly a hero.

### `Parting`

- **Kind:** group, a fork. **Level:** tale.
- **Holds:** the road marker <, the signaller Y if there is one, and two branch moves.
- **Warrant:** pp.93-94, method 6: two seekers "part in the middle of the first move ... at a road marker", which Propp writes <, and "often give one another an object: a signaller", which he writes Y. His scheme for tale 155 is "I-II. <Y", with III and IV after it.
- **Name:** Propp's word. **Corpus:** 1 tale, 155. **Tree test:** `A K < Y a K / A K }`, the `a` under `Parting` and the first A not.
- **EBNF:** `Parting = roadMarker [signaller] move moveBoundary move`
- **Literal meaning:** Two heroes set out together, then part.
  Each goes to his own adventure, often leaving the other a token that shows how he fares.
  The tree holds the two branches side by side.
- **Cultural meaning:** Separate paths that still depend on each other.
  The two companions come from one start and go through matching adventures.
  The token links them across the distance.
  So the hero's fate is not his alone: one may win only because the other comes to his rescue when the token warns of disaster.

### `CommonEnding`

- **Kind:** group. **Level:** tale.
- **Holds:** Propp's closing brace }, then what follows a liquidation: return, the false hero's contest, the task and the endgame.
- **Warrant:** p.93, method 5: "Two moves may have a common ending." Propp draws a single closing brace across both moves, with the ending to its right, in 125 and 155.
- **Name:** Propp's words. **Corpus:** 2 tales, 125 and 155; 155's ending, ↓X, reduces to nothing, so its common ending is empty. **Tree test:** `A up o / A K } L Q W`, the L under `CommonEnding` and the first move's o not.
- **EBNF:** `CommonEnding = commonEnding AfterLiquidation`
- **Literal meaning:** One ending for two undertakings.
  The tree makes the ending a sibling of the moves it closes, so it belongs to both.
  The grammar checks that it fits the last of them; that it fits the other is checked at the level of the move.
- **Cultural meaning:** Order restored, and the truth made public.
  The common ending joins separate paths into one settlement and repairs the order that was broken.
  It brings the separate paths to one public place, where true heroism is told apart from false claims for good.
  Many undertakings end in one settlement, and the community returns to one orderly rank.

### `preparatorySection`

- **Kind:** group of groups. **Level:** tale, before the first move only.
- **Holds:** β, then the pairs γ–δ, ε–ζ and η–λ–θ.
- **Warrant:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Name:** Propp's. **Corpus:** 0, since the appendix prints none. **Tree test:** `β γ δ A`, the β under `preparatorySection`.
- **EBNF:** `preparatorySection = {absentation} RuleViolation InformationGathering DeceptionTrap`
- **Literal meaning:** What makes the misfortune possible.
  The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived.
  Propp calls the first seven functions the preparatory part (p.30).
- **Cultural meaning:** The end of safety at home.
  The opening shows that the young must leave home sooner or later.
  The safety of home is fragile and does not last, and innocence falls to the deceptions of the wider world.
  The opening is a threshold: it ends the safety of childhood, sometimes violently, and pushes the young person into the trials of growing up.

### `RuleViolation`

- **Kind:** pair. **Level:** tale.
- **Holds:** γ then δ. An absentation β told after the interdiction nests inside the pair.
- **Warrant:** p.80 writes γ-δ as a pair; p.64 lists prohibition-violation. The β inside it follows tale 113 (pp.96-97) and the wolf and the kids (p.101), both told interdiction first.
- **Name:** v43's, restored; this grammar's `interdictionViolation` before, from Propp's terms. **Corpus:** 0. **Tree test:** `γ β δ A`, the β under `RuleViolation`.
- **EBNF:** `RuleViolation = [ interdiction {interdiction} {absentation} ] {violation}`
- **Literal meaning:** A rule given and broken.
  This is the breach through which misfortune enters.
  When the elders' leaving is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.
- **Cultural meaning:** The broken rule that starts the story.
  In the tale, the prohibition is there to be broken.
  Breaking it is an act of self-harm that ends the false safety of childhood.
  It brings danger at once, but it is also what moves the young person out of standing still and into a life of his own.

### `InformationGathering`

- **Kind:** pair. **Level:** tale.
- **Holds:** ε then ζ.
- **Warrant:** p.80 writes ε-ζ as a pair; p.64 lists reconnaissance-delivery.
- **Name:** v43's, restored; this grammar's `reconnaissanceDelivery` before, from Propp's terms. **Corpus:** 0. **Tree test:** `ε ζ A`, the ζ under `InformationGathering`.
- **EBNF:** `InformationGathering = {reconnaissance} {delivery}`
- **Literal meaning:** The villain asks for information and gets it.
  The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Cultural meaning:** Secrets get out.
  No household can keep its weak points hidden for ever.
  The household gives the villain what he wants because it is innocent and cannot imagine his intent.
  How easily he learns it shows a rule of the tale: hidden weaknesses come out, and the young person's weak points must be exposed to the world before the journey can begin.

### `DeceptionTrap`

- **Kind:** pair, with λ inside it. **Level:** tale.
- **Holds:** η, then λ, then θ.
- **Warrant:** p.80 writes η-θ as a pair; λ is placed by Appendix I Table II item 44, which confines the preliminary misfortune to the deceptive agreement.
- **Name:** v43's, restored; this grammar's `trickeryComplicity` before, from Propp's terms. **Corpus:** 0. **Tree test:** `η λ θ A`, the λ under `DeceptionTrap`.
- **EBNF:** `DeceptionTrap = {trickery} {preliminaryMisfortune} {complicity}`
- **Literal meaning:** The villain deceives, and the victim gives in.
  The preliminary misfortune is what forces the victim to agree.
- **Cultural meaning:** Good judgment fails.
  A child's instinct is no match for deliberate malice.
  The villain's disguise shows that danger often looks like a harmless part of home life.
  When a preliminary misfortune forces the victim to agree, the tale shows that instinct alone cannot protect the inexperienced: the victim's own will gives way, and the hero's journey grows out of the wreckage.

### `move`

- **Kind:** group of the move. **Level:** move.
- **Holds:** the span from the crisis to its liquidation, then everything after the liquidation.
- **Warrant:** p.92: a move is any development from villainy or lack, through intermediary functions, to a denouement.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `α A`, where the α is *not* under `move`.
- **EBNF:** `move = BeforeTheTrouble TroubleToLiquidation AfterLiquidation`; with `+reversal`, `move = BeforeTheTrouble TroubleToLiquidation AfterLiquidation [LateFall]`
- **Literal meaning:** One misfortune and its undoing.
  A tale has as many moves as it has new villainies or lacks.
- **Cultural meaning:** Life goes on through loss and repair.
  A move is a pattern for getting through a crisis.
  It shows that collapse is not final: a misfortune sets off a known way of putting things right.
  The hero keeps to the culture's rules, and the community's misfortune or lack is fully mended.
  This tells the listener that balance can always be won back, while the repeating pattern admits that life is a series of upsets and renewals.

### `BeforeTheTrouble`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a T, then a departure, then a donor sequence, each optional.
- **Warrant:** p.107: the elements DEF often stand before A, which is "not a new, but rather an inverted sequence".
- **Name:** this grammar's; `BeforeTheCrisis` before. **Corpus:** 0; the corpus reading drops the cells Propp parks to the left of A, as decided, so the corpus does not use it. **Tree test:** `up D E F A K`, the ↑ under `BeforeTheTrouble`.
- **EBNF:** `BeforeTheTrouble = EarlyTransfiguration [EarlyLeaving] [EarlyHelp]`
- **Literal meaning:** What the hero has or does before the misfortune strikes.
  It lies outside the A-K span, since the crisis has not yet come.
- **Cultural meaning:** The hero marked out in advance.
  Changes and helpers that come before any crisis show that the hero stands apart from ordinary home life.
  They also suggest a balance in the world: even as the household grows weak, the means of its rescue is already in place.
  So the misfortune does not destroy the young person; it wakes a power that was already there.

### `EarlyLeaving`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** one or more departures.
- **Warrant:** p.107: the exit from home comes first, the hero learning of the misfortune when already on the road.
- **Name:** this grammar's; `LeavingFirst` before. **Corpus:** 0, as above. **Tree test:** `up D E F A K`, the ↑ under `EarlyLeaving`.
- **EBNF:** `EarlyLeaving = departure EarlyTransfiguration {departure EarlyTransfiguration}`
- **Literal meaning:** The hero already on the road when the misfortune comes.
  He set out with no particular aim, and the misfortune finds him on the way.
- **Cultural meaning:** Growing up can start from within.
  Leaving home is itself the hero's awakening.
  Each departure can bring a change in the hero, so moving away from the safety of childhood keeps reshaping who he is.
  When the misfortune meets him on the open road, the tale shows that a grown person finds his task by stepping out to meet the world's troubles, not by staying home.

### `EarlyHelp`

- **Kind:** group. **Level:** move, before the opener.
- **Holds:** a donor sequence: tested when it opens on D or E, untested when it is F alone.
- **Warrant:** p.107: the receipt of a helper first, and then the misfortune the helper undoes.
- **Name:** this grammar's; `HelperFirst` before, from Propp's wording. **Corpus:** 0, as above; the parked regions it would cover are 104 I, 105 II, 125 I, 126 II, 137 I, 156 III, 162 I and 166 I. **Tree test:** `D E F A K`, the F under `EarlyHelp` and not under `TroubleToLiquidation`.
- **EBNF:** `EarlyHelp = firstDonorFunction EarlyTransfiguration {firstDonorFunction EarlyTransfiguration} {heroReaction EarlyTransfiguration} {receiptOfMagicalAgent EarlyTransfiguration} | heroReaction EarlyTransfiguration {heroReaction EarlyTransfiguration} {receiptOfMagicalAgent EarlyTransfiguration} | receiptOfMagicalAgent EarlyTransfiguration {receiptOfMagicalAgent EarlyTransfiguration}`
- **Literal meaning:** The hero equipped before he is needed.
  The helper is already in hand when the misfortune comes, and the move is shorter for it.
- **Cultural meaning:** Help that comes from respecting the old ways.
  Winning an ally or a magical agent before a crisis shows that a young person who honors his elders and keeps the basic rules of his society is given strong support.
  Each step of the donor exchange may come with a change in the hero, so the help raises his standing for good.
  When the misfortune comes, he does not face it with bare human weakness but with all the strength his culture has built up.

### `EarlyTransfiguration`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T, at the head of a move, inside `BeforeTheTrouble` since step 9.
- **Warrant:** p.108: T is the most unstable function in its position. As decided, T may stand anywhere in a move.
- **Name:** this grammar's; `FloatingT` before. **Corpus:** 0; no T stands before an opener in the corpus. **Tree test:** `T A K`, the T under `EarlyTransfiguration`.
- **EBNF:** `EarlyTransfiguration = {transfiguration}`
- **Literal meaning:** None claimed.
  Since step 7 it holds only a T that comes before a move's opener; a T after a function stands in `Digression`.
  Where a T hangs in the tree is only where the parser happens to meet it.
  T's own meaning, transfiguration, is given under the function in the section "Functions".
- **Cultural meaning:** None of its own, apart from `transfiguration`.
  Because a T can stand at many points, the hero's rise is not one final event; it can happen in stages as the young person goes through the stages of preparation.

### `Digression`

- **Kind:** notation. **Level:** move.
- **Holds:** any number of T and of interrupting moves, in any order, after any function.
- **Warrant:** p.108 for T; p.93 for the pause, methods 2 and 3.
- **Name:** this grammar's; `Between` before. **Corpus:** 6, all of them T's; the corpus of single moves has no interruption, since its reading removes the markers. **Tree test:** `A K T`, the T under `Digression`.
- **EBNF:** `Digression = { transfiguration | EmbeddedMove }`
- **Literal meaning:** A pause between functions.
  A slot in the notation between any two functions.
  The tale can pause there for a change in the hero's appearance, or for a whole separate move told inside it.
- **Cultural meaning:** None of its own, apart from its contents.
  The slot shows how much give there is in life and in duty.
  A tale can pause for a transformation or stretch to take in a new crisis, so a life is rarely a straight line.
  Much growing up happens in between, and great quests often have to stop for the needs of others.

### `EmbeddedMove`

- **Kind:** group, the one rule that contains itself. **Level:** move, inside a move.
- **Holds:** a whole move, bracketed ⟨ ... ⟩, which may itself hold interrupting moves to any depth.
- **Warrant:** p.93: "a development which has begun pauses, and a new move is inserted" (method 2), and "an episode may also be interrupted in its turn" (method 3). Ch. IX n.4 marks the interruption by dots, with an indication of which move breaks the thread.
- **Name:** this grammar's; `InterruptingMove` before. **Corpus:** 4 interruptions in 3 of the 45 tales, from `embedCorpus.py`: move III inside 138 II, move II inside 159 I, move IV inside 159 III, and move II inside 162 I. **Tree test:** `A ⟨ a K ⟩ K`, the `a` under `EmbeddedMove` and the last K not.
- **EBNF:** `EmbeddedMove = interruptionBegins move interruptionEnds`
- **Literal meaning:** A story told inside a story.
  The main quest stops while a separate misfortune or lack runs its own full course, from trial to undoing.
  The main move picks up again only when that one is done.
  This is the one place where the grammar lets a move hold a move, to any depth, which makes it a grammar that can nest (context-free) rather than a simple left-to-right pattern.
- **Cultural meaning:** One trouble leads to another.
  Nested moves show that one crisis is tied up with others.
  A great quest must give way to the troubles met on the road.
  The nested misfortune has to be settled in full before the quest goes on, so the larger repair cannot happen without first meeting the small, nearby duties of the road.

### `TroubleToLiquidation`

- **Kind:** span, the A–K pair as one unit. **Level:** move.
- **Holds:** the complication, the donor episode and the fight, then the liquidation.
- **Warrant:** p.53: liquidation, together with villainy, makes a pair, and the story reaches its peak in it. Two functions far apart in the string can still form one unit one level up in the tree.
- **Name:** this grammar's; `CrisisToLiquidation` before, itself widened from VillainyToLiquidation because the span also covers a lack and a move opened on B. **Corpus:** 80. **Tree test:** `A B C up D E F G H I K`, both A and K under `TroubleToLiquidation`.
- **EBNF:** `TroubleToLiquidation = complication Development {liquidation Digression}`
- **Literal meaning:** The misfortune and its undoing, the core of every move.
  Everything inside it is the hero's way from the one to the other.
- **Cultural meaning:** Every crisis has an end.
  The span ties each misfortune to its undoing.
  It shows that a crisis is limited and orderly, and that harm can be healed by keeping to the culture's ways.
  It promises the community that no chaos lasts and that balance will come back.

### `complication`

- **Kind:** group. **Level:** move.
- **Holds:** the opener, dispatch B, counteraction C and departure ↑, and an untested agent on either side of the departure.
- **Warrant:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
- **Name:** Propp's. **Corpus:** 80. **Tree test:** `A B C up`, both B and ↑ under `complication`.
- **EBNF:** `complication = MoveTrigger Digression {mediation Digression} {beginningCounteraction Digression} [UntestedAcquisition] [ departure Digression {departure Digression} [UntestedAcquisition] ]`
- **Literal meaning:** The misfortune made known, and the hero setting out.
  Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Cultural meaning:** The community calls one of its own to act.
  The complication draws a young person out of the home to answer a need of the community.
  Going from seeing the misfortune to crossing the threshold shows that private peace cannot last while a public harm goes unanswered.
  The traveler may pick up unearned help along the road: setting out by itself seems to bring support from forebears and the natural world, and it turns a victim who stays put into someone who acts to set things right.

### `MoveTrigger`

- **Kind:** choice. **Level:** move.
- **Holds:** one of A, a or B.
- **Warrant:** p.92 for villainy and lack; p.37: where no villainy occurs, the connective incident opens the move.
- **Name:** this grammar's; `MoveOpener` before; v43 split at the root instead, and the choice is kept here. **Corpus:** 80: villainy in 53, lack in 26, the connective incident in one, 133 II. **Tree test:** `B C up`, the B under `MoveTrigger`, and `A B C`, where the later B is not.
- **EBNF:** `MoveTrigger = villainy | lack | mediation`
- **Literal meaning:** What opens a move.
  A villainy is harm done from outside; a lack is something missing from within.
  When neither happens, the move opens with a call or a sending, Propp's connective incident.
- **Cultural meaning:** The two dangers every community faces.
  Harm from outside (*villainy*) shows that no household can shut itself away from ill will.
  A need from within (*lack*) shows that a community will wither unless it reaches beyond its own borders for what it needs to grow.

### `UntestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** a run of F with no donor's test before it.
- **Warrant:** p.108: the transference of a magical agent sometimes occurs before the hero leaves home, "cudgels, ropes, maces, and so forth, given by the father". Step 6's merge adds the agent that comes to hand on the road with no test.
- **Name:** v43's. **Corpus:** 17. **Tree test:** `A C F up K`, the F under `UntestedAcquisition` and under `complication`.
- **EBNF:** `UntestedAcquisition = receiptOfMagicalAgent Digression {receiptOfMagicalAgent Digression}`
- **Measured:** Counted by `agentForms.py` and pinned by a test. At home, before the departure, 12 cells in 11 moves: transferred 6, prepared 5, bought 1; none found, appearing, seized or offering service. On the road, 10 cells in 10 moves: transferred 4, appears 3, pointed out 1, prepared 1, offers service 1. The agent at home comes by ordinary human means; on the road, luck may bring it.
- **Literal meaning:** An agent received without being earned.
  It is a father's gift or a find, and it belongs to setting out, not to a meeting with a donor.
- **Cultural meaning:** What the young inherit.
  This help comes from family and from surroundings.
  Receiving a magical agent with no trial shows that the young person is carried by the strength and knowledge of earlier generations.
  Whether it is an elder's gift or a lucky find on the road, setting out brings some support with it, so the hero is equipped before he is ever tested.

### `Development`

- **Kind:** span. **Level:** move.
- **Holds:** the donor episode, spatial transference G and the fight.
- **Warrant:** editorial. No page groups these; the span is what lies between the complication and the liquidation.
- **Name:** this grammar's. **Corpus:** 65. **Tree test:** `A D E F G H I K`, the G under `Development` and the K not.
- **EBNF:** `Development = [TestedAcquisition] {spatialTransference Digression} StruggleAndOutcome`
- **Literal meaning:** The hero's road through the other world.
  A reading aid.
  It runs from earning a magical agent, through the long journey, to the fight with the source of the misfortune.
- **Cultural meaning:** The dangerous middle, where childhood is left behind.
  The order is fixed: first win a helper, then cross into the danger, and only then face the enemy.
  Plain effort is not enough against a great harm.
  A person must first be changed, tested and equipped by his culture before he can face real evil and beat it.

### `TestedAcquisition`

- **Kind:** group. **Level:** move.
- **Holds:** the donor's test D, the hero's reaction E, and the agent F they earn.
- **Warrant:** p.65: DEF "also form something of a whole".
- **Name:** v43's; before step 6, Vetting. **Corpus:** 32. **Tree test:** `A D E F`, the F under `TestedAcquisition` and not under `UntestedAcquisition`.
- **EBNF:** `TestedAcquisition = firstDonorFunction Digression {firstDonorFunction Digression} {heroReaction Digression} {receiptOfMagicalAgent Digression} | heroReaction Digression {heroReaction Digression} {receiptOfMagicalAgent Digression}`
- **Measured:** Counted by `agentForms.py` and pinned by a test. 35 cells in 28 moves: transferred 8, offers service 7, pointed out 4, seized 3, appears 3, found 2, prepared 1, bought 1, and 6 with no form marked. Every seizure in the corpus falls here, 3 of 3, and 7 of the 8 offers of service.
- **Literal meaning:** The magical agent earned.
  A donor guarding the way tests the hero, the hero responds, and the agent follows from the response.
  The sequence opens on the test, or straight on the hero's response when the test is left out.
- **Cultural meaning:** Showing that one knows the ways of one's culture.
  This is not a loose lesson in kindness or fair dealing; it is a strict test of readiness.
  Passing it shows that the young person has the manners, the respect for elders, or the quick wits needed to survive away from home.
  The agent may be a reward for honoring the duty to give in return, or it may be taken by a trick from a hostile donor.
  Either way, power does not come at random: it goes to those who have learned the rules of their world.

### `StruggleAndOutcome`

- **Kind:** group, around the pair H–I. **Level:** move.
- **Holds:** struggle H, branding J and victory I.
- **Warrant:** p.104, the struggle scheme H J I; p.64 lists struggle-victory as a pair.
- **Name:** this grammar's; `Combat` before. **Corpus:** 32. **Tree test:** `A H J I K`, the J under `StruggleAndOutcome`.
- **EBNF:** `StruggleAndOutcome = {struggle Digression} {branding Digression} {victory Digression}`; (or conditional `+tragedy` `StruggleAndOutcome = {struggle Digression} {branding Digression} StruggleOutcome`
- **Literal meaning:** The fight, the mark, and the victory.
  The hero fights the enemy, in combat or in a contest, is marked, and wins.
  The mark won here is what lets the hero be recognized later.
- **Cultural meaning:** The fight that makes a ruler, and the mark it leaves.
  The fight changes the young person for good: it ends the passive child.
  The mark is lasting proof that the hero went into the wild or the underworld and came back.
  Because the mark comes with the victory, the tale says that the right to lead and protect belongs to those who carry the scars of the struggle.

### `AfterLiquidation`

- **Kind:** span. **Level:** move.
- **Holds:** the return journey, the ordeal and the endgame.
- **Warrant:** editorial.
- **Name:** this grammar's. **Corpus:** 68. **Tree test:** `A K down`, the ↓ under `AfterLiquidation`.
- **EBNF:** `AfterLiquidation = ReturnJourney Ordeal Endgame`
- **Literal meaning:** What happens after the misfortune is undone.
  A reading aid.
  It covers the way home, the public tests of who the hero really is, and the final settling of his place.
- **Cultural meaning:** A private victory made public.
  The way home is dangerous, a public test follows, and then a final settlement.
  Beating the enemy alone is not enough to lead.
  Before a young person can take a place in the community or found a new household, his hidden deeds must be brought into the open, checked, and cleared of false claims.

### `ReturnJourney`

- **Kind:** group. **Level:** move.
- **Holds:** return ↓, then pursuit and rescue.
- **Warrant:** editorial; the pursuit–rescue pair inside it has a page.
- **Name:** v43's. **Corpus:** 43. **Tree test:** `A K down Pr Rs`, the Pr under `ReturnJourney`.
- **EBNF:** `ReturnJourney = {return Digression} Evasion`
- **Literal meaning:** The way home.
  It includes the flight from the other world, the enemy's pursuit, and the rescue.
- **Cultural meaning:** Bringing the prize safely home.
  The hero must hold on to what he won against a backlash.
  The pursuit shows that beating a danger stirs up the forces of the wild against him.
  A weakened hero has to rely on transformation and on those who rescue him, so success on one's own is fragile.
  It takes others' help to carry the prize across the threshold of home.

### `Evasion`

- **Kind:** choice between two orders of a pair. **Level:** move.
- **Holds:** pursuit and rescue, in either order.
- **Warrant:** p.64 lists pursuit-deliverance as a pair; p.147 gives the inverted order.
- **Name:** v43's. **Corpus:** 14. **Tree test:** `A K down Pr Rs`, the Rs under `Evasion`.
- **EBNF:** `Evasion = [ PursuitFirst | RescueFirst ]`
- **Literal meaning:** Escaping capture on the way home.
  It allows the two orders found in the corpus: a pursuit that a rescue answers, or a rescue that comes first and heads off the pursuit.
- **Cultural meaning:** Closing the border between the wild and home.
  The two paths show that getting past a backlash takes adaptability more than strength.
  The hero survives by hiding, by changing shape, and by the help others give, not by fighting.
  Growing up means knowing when to face an enemy and when to slip out of reach of past danger.

### `PursuitFirst`

- **Kind:** group, the usual order. **Level:** move.
- **Holds:** pursuit, then rescue, then an optional fight after the pursuit.
- **Warrant:** p.64 for the pair; p.107 for the fight after it.
- **Name:** this grammar's. **Corpus:** 13. **Tree test:** `A K Pr Rs`, the Pr under `PursuitFirst`.
- **EBNF:** `PursuitFirst = pursuit Digression {pursuit Digression} {rescue Digression} LateStruggle`
- **Literal meaning:** The enemy chases, and the hero is rescued.
  The forces of the other world chase the hero on his way home; a rescue follows, and sometimes a last fight at the border before he is safe.
- **Cultural meaning:** Danger that keeps coming.
  A great upset in life carries on after it seems over.
  The chase shows that the effects of a beaten danger can follow a person across thresholds.
  They can be beaten with quick use of the help at hand and a last fight at the border, which tells the young listener that past trouble can be cut off for good before he returns to the community.

### `RescueFirst`

- **Kind:** group, the inverted order. **Level:** move.
- **Holds:** rescue, then pursuit, then an optional fight after the pursuit.
- **Warrant:** p.147, on tale 150: "Humorous inversion: the villain runs away instead of the hero; the hero pursues [Rs-Pr]".
- **Name:** this grammar's. **Corpus:** 1, 150 II. **Tree test:** `A K Rs Pr`, the Rs under `RescueFirst`.
- **EBNF:** `RescueFirst = rescue Digression {rescue Digression} [ pursuit Digression {pursuit Digression} LateStruggle ]`
- **Literal meaning:** The roles reversed: the villain flees and the hero gives chase.
  The hero takes the lead right after the misfortune is undone, and the villain runs.
  The grammar allows this order in any move of the corpus.
- **Cultural meaning:** The enemy's power wholly broken.
  Rescue before pursuit shows the enemy's power suddenly gone.
  Undoing the misfortune does more than stop the danger: it leaves the enemy unable to act, and hunter and hunted change places.
  The hero becomes the one who drives the trouble out, and the goal of growing up shows as taking charge, not only surviving.

### `LateStruggle`

- **Kind:** group. **Level:** move.
- **Holds:** struggle H, branding J and victory I, after a pursuit.
- **Warrant:** p.107: "In tales 93 and 159 the fight with the villain takes place only after pursuit."
- **Name:** this grammar's; `CombatAfterPursuit` before. **Corpus:** 1, 93 III. **Tree test:** `A K down Pr J`, the J under `LateStruggle`.
- **EBNF:** `LateStruggle = {struggle Digression} {branding Digression} {victory Digression}`
- **Literal meaning:** The main fight, put off until after the chase.
  The enemy is beaten only after he has chased the hero back to the threshold of home.
- **Cultural meaning:** Defending the doorstep.
  Some dangers cannot be outrun or dodged; they have to be met in a last fight at the edge of the community.
  A victory and a mark won at the very doorstep show everyone the hero's power to protect them, and past trouble is cut off before the new order is founded.

### `Ordeal`

- **Kind:** group. **Level:** move.
- **Holds:** the false hero's posture, then the task.
- **Warrant:** editorial.
- **Name:** v43's, less the recognition, which moves freely in the endgame since step 3. **Corpus:** 13. **Tree test:** `A K o L M N`, the M under `Ordeal`, and `A K o L M N Q`, where the Q is not.
- **EBNF:** `Ordeal = FraudPosture TaskAndSolution`
- **Literal meaning:** The public test of the hero's claims.
  A reading aid.
  It sets the false hero's claims beside a hard task meant to test the candidates fairly.
- **Cultural meaning:** Exposing fraud.
  The ordeal is a society's defense against corruption from within.
  The false hero shows that a home can be spoiled by lies and by claims to power that were never earned.
  Making every claimant face a fair, hard task shows that a healthy community trusts real tests over talk to tell true ability from pretense before power is handed on.

### `FraudPosture`

- **Kind:** pair. **Level:** move.
- **Holds:** unrecognized arrival o, then unfounded claims L.
- **Warrant:** p.104: unrecognized arrival and unfounded claims shift together between the two combined schemes.
- **Name:** v43's. **Corpus:** 7. **Tree test:** `A K o L`, the L under `FraudPosture`.
- **EBNF:** `FraudPosture = {unrecognizedArrival Digression} {unfoundedClaims Digression}`
- **Literal meaning:** The hero comes back unknown, while an impostor claims his deeds.
  The pairing opens a crisis over who the hero is and who will be recognized.
- **Cultural meaning:** The true hero at the bottom, the fraud at the top.
  This is not a sermon on patience or humility.
  Being unknown shields the hero from attack by those in power, while the false claims show how blind a ranking is when nobody has checked it.
  The tale puts real merit at the bottom and fraud at the top, a contrast that cannot last.
  It shows that appearances at home deceive, and it sets a trap that springs once the truth is tested.

### `TaskAndSolution`

- **Kind:** group, around the pair M–N. **Level:** move.
- **Holds:** difficult task M, branding J and solution N. The J comes only after a task.
- **Warrant:** p.104, the task scheme M J N, set in the place H J I holds in the other scheme. The J only after M is the repair v44's own comment names, made at step 5.
- **Name:** this grammar's; v43's `TaskCycle` before. **Corpus:** 9. **Tree test:** `A K M J N`, the J under `TaskAndSolution` and not under `StruggleAndOutcome`.
- **EBNF:** `TaskAndSolution = [ difficultTask Digression {difficultTask Digression} {branding Digression} ] {solution Digression}`
- **Literal meaning:** A hard task, set and done.
  The candidate faces a very hard trial and succeeds.
  The task does at court what the fight does in the wild: it checks the claimant's deeds.
- **Cultural meaning:** A fair test of real ability.
  The tale treats the task as the equal of a battle, because leadership means living by the culture's basic rules.
  The candidates must show real results, by calling on the bonds with forebears and the natural world they have built up.
  That strips away the false hero's empty talk and makes the true hero's right to rule plain to all.

### `Endgame`

- **Kind:** group of four functions that may come in any order. **Level:** move.
- **Holds:** recognition Q, exposure Ex, punishment U and wedding W, in any order.
- **Warrant:** p.108: "Recognition and exposure, marriage and punishment may also exchange positions", read as letting all four change places among themselves.
- **Name:** v44's word for the span. **Corpus:** 38. **Tree test:** `A K U Q W`, both U and Q under `Endgame`.
- **EBNF:** `Endgame = { ( recognition | exposure | punishment | wedding ) Digression }`
- **Literal meaning:** The final settling of accounts.
  The true hero is recognized, the false one is exposed and punished, and the hero marries and comes to power.
  These may come in any order.
- **Cultural meaning:** The social order put back together.
  The endgame ends the illusions and steadies the community.
  Recognition and exposure together clear out the false and put the truth back at the top of the kingdom.
  The wedding and the hero's rise close the cycle: a sound family stands again at the head of the people, ready for the next generation of heroes.

## Dependencies, not productions

**J–Q: the mark and the recognition.**
Branding J (XVII) falls inside `TroubleToLiquidation`, and recognition Q (XXVII) falls outside it, so the two spans cross, and a single tree cannot hold both.
A–K is kept as the unit, and J–Q is carried as a dependency: the J in `StruggleAndOutcome` marks the hero whom the Q in `Endgame` recognizes.
Its meaning is the thread that runs across the move: the wound or the ring from the fight is the proof that settles the hero's claim at the end.

## Extensions, commented out

**Three extensions are written into v46 but switched off.**
Two come from v43 and were carried over switched off, as decided (step 10); a second tragic variant joined them (step 11).
They are not part of the grammar as it stands, so they have no entries above; switched on, they add these.

- **`TragicFall`, with `StruggleOutcome` and the defeat sign I-.**
  - *Literal meaning:* The fight ends in defeat.
    The combat ends not in victory but in the hero's defeat, exposure and punishment.
  - *Cultural meaning, v43's reading:* Tragedy is the warrior tale's shadow.
    Tragedy is not a separate genre but the same rising action with strength failing; to lose the fight is to be shown not to be the hero one claimed to be.
  - *Warrant:* v43's proposal, not Propp's; no page supports it and no corpus tests it.
- **`LateFall`, with the reversal sign Rv (step 11).**
  - *Literal meaning:* Success, then the fall.
    A move succeeds, the lack undone or the task solved and the queen married, and then turns: recognition, exposure and punishment fall on the hero.
  - *Cultural meaning, draft:* Success is not safe from its own consequences.
    A hero who has taken what was forbidden, as Prometheus took the fire, or who has unknowingly done what may not be done, as Oedipus did, is brought down after his triumph.
    It is the tragic ending of the Greek myths that end in punishment, reached by the same road as the triumphant tale.
  - *Warrant:* Aristotle's reversal and recognition (*peripeteia* and *anagnorisis*, *Poetics*), not Propp.
    The fall in the fight of `TragicFall` and the fall after success are the two tragic variants: in one, strength fails; in the other, success itself is overturned.
  - *Success depends on whose side the tale takes.*
    Propp defines each function by its meaning for the hero (p.81).
    So from Prometheus's side, taking the fire undoes humanity's lack and the punishment is a reversal; from Zeus's side, the same events are a villainy and the villain's punishment, an ordinary tale that v46 already accepts.
    The reversal sign marks the choice to tell the fallen figure's tale, which is why the grammar does not require a success before it.
  - *Scope, untested:* Together the two variants are meant to cover the endings of Greek myth, of myth in general, and of any genre not bound to a happy ending: Propp's pattern at the core, with the ending turned.
    This is speculation until a corpus of such tales is transcribed and run.
- **`consequenceTale`, with `DundesMove`, `DundesEvent` and `consequence`.**
  - *Literal meaning:* A rule broken, and a consequence that cannot be undone.
    A tale of another genre, in which no lack or villainy drives the action and no hero undoes it: a prohibition broken or an act that cannot be taken back, then a consequence, a punishment or a lasting change to the world, and perhaps an attempt to escape it.
  - *Cultural meaning, draft:* Why things are as they are.
    It explains how things came to be as they are, and warns that some acts cannot be undone.
  - *Warrant:* Dundes (1964) for Interdiction, Violation, Consequence and Attempted Escape, in that order; the irreversible act and the change to the world are v43's editorial additions.

## What the catalog teaches

**The father's gift is an untested agent.**
p.108 treats the agent given before departure as a case of its own, and step 4 followed it, splitting agents by whether a departure came after them.
No grammar that reads left to right can draw that split, since a run of F's looks the same until it ends.
The split it can draw is at the test: an agent earned from a donor is tested, and every other agent is untested.
On that reading, the father's gift and an agent found on the road are the same kind of thing, and the tree puts both with the setting out.
In the corpus, the tested agent appears in 32 moves and the untested in 17.

**Two of Propp's pairs dissolve when their order is freed.**
Recognition with exposure, and punishment with wedding, were groups until step 3 let the four change places.
Once U Q W is allowed, the pairs are no longer next to each other in every tale, so the grammar keeps one group of four.
The pairing survives in the meaning, and the order is free.

**How the hero receives the agent carries meaning, and it is measured, not read in.**
Sorting every agent in the corpus by step 6's split, which the grammar's own reading rules forced, gives three findings (`agentForms.py`).
An agent received at home is always given, made or bought, never found, appearing or seized.
Seizure comes only after a test, where Propp ties it to a hostile donor.
And an offer of service comes after a test 7 times in 8, the donor repaying the hero's kindness.
Here meaning falls out of the form, which is the kind of evidence needed to answer the charge that Propp's structure is empty.

**Four groups are reading aids only.**
`Development`, `AfterLiquidation`, `ReturnJourney` and `Ordeal` have no page behind them.
They make the tree readable, and they are candidates for testing against Propp's text, not claims about it.

**Every permission of pp.107-108 is now in the grammar.**
The last, p.107's inverted sequence, lets the departure or the donor sequence come before the crisis.
The corpus does not use it, because its reading still drops the cells Propp parks to the left of A; the grammar states what Propp allows, and the corpus test is unchanged.

**T is the one function the tree cannot place.**
Its position is free by p.108, so its place in the tree carries no meaning.

**Three of p.93's six ways of combining moves work at the level of the whole tale, and two of them are forks and joins.**
Method 1 is sequence.
Method 6 is a fork, two branches from one trunk, and a tree holds it naturally.
Method 5 is a join, one ending for two moves, which no tree can share; the grammar makes the ending a sibling of both moves, which is as near as a tree comes.
Method 4, two villainies at once, is not built: its two A-K spans cross.

**A move can hold a move, and the markers keep it readable.**
Since step 7, a move may pause after any function for a whole inserted move, to any depth, as p.93's methods 2 and 3 describe.
That makes the grammar one that can nest (context-free) rather than a simple left-to-right pattern (regular).
Yet a program can still read it in one pass, left to right, deciding each step by the next symbol alone (the property called LL(1)), because each inserted move is bracketed by its own markers.
Without the pause, the grammar is exactly step 6's.
The corpus has four such insertions, in tales 138, 159 and 162; three further places carry Propp's dots with no numeral, 155 III, 155 IV and 167 I, and name no move to insert.

## Functions

**Every function carries meaning of its own, or it would not be in the model; this section records it.**
Propp's thirty-one functions of Ch. III, pp.26-63, are listed in his order, with lack as VIIIa (p.35), thirty-two entries in all.
Each gives Propp's number and sign, the page where he defines it, the name he gives it, what happens in it in a sentence, the group that holds it in v46, the pairs it belongs to, and how many of the 80 accepted moves use it, from `CorpusGroups.txt`.
Each then gives its literal meaning and a draft of its cultural meaning.
The descriptions are paraphrases; Propp's own wording is on the page cited.
The preparatory functions I-VII show 0 in the corpus because Appendix III prints none (p.116), not because the tales lack them.

### `absentation`

- **Number and sign:** I, β. **Page:** p.26. **Propp's name:** absentation.
- **What happens:** A member of the family leaves home: the elders go out to work, to war, or to trade. The death of the parents is its strongest form.
- **Group:** `preparatorySection`, or inside `RuleViolation` when told after the interdiction. **Pairs:** none; it is the one preparatory function outside every pair. **Corpus:** 0.
- **Literal meaning:** The protectors leave.
  Whether they go out or die, the household is left unguarded, and that opens the way for the misfortune.
- **Cultural meaning:** The end of childhood shelter.
  The elders' leaving or death is the first stage of a rite of passage.
  It exposes the young to the real world, sometimes violently, and forces them out of dependence, so that they can in time cross into the wild, where the trials of growing up take place.

### `interdiction`

- **Number and sign:** II, γ. **Page:** p.26. **Propp's name:** interdiction.
- **What happens:** the hero is forbidden something; in the inverted form, he is ordered or advised to do something.
- **Group:** `RuleViolation`. **Pairs:** with violation, γ-δ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** A rule laid down at home.
  The rule sets up a condition: if it is broken, the household is open to misfortune.
- **Cultural meaning:** The line that must not be crossed.
  The prohibition marks the line between the safety of childhood and the dangers of independence.
  It marks how far the home's protection reaches.
  In the tale the rule is there to be broken, and that is what draws the young person, in the end, across the threshold of the known world.

### `violation`

- **Number and sign:** III, δ. **Page:** p.27. **Propp's name:** violation.
- **What happens:** the interdiction is broken; in the inverted form, the order is carried out.
- **Group:** `RuleViolation`. **Pairs:** with interdiction; it may stand without it (p.27). **Corpus:** 0.
- **Literal meaning:** The forbidden act is done.
  It opens the breach through which danger, or the villain, enters the story.
- **Cultural meaning:** Taking one's first step on one's own.
  This is not a lesson in obedience.
  Breaking the rule is the necessary break from childhood safety, and it is what starts a person growing up; staying safe at home leads nowhere.
  By crossing the line, the young person stops being only the object of the parents' care and becomes the one who shapes his own life, accepting the world's dangers as the price.

### `reconnaissance`

- **Number and sign:** IV, ε. **Page:** p.28. **Propp's name:** reconnaissance.
- **What happens:** the villain tries to find something out, such as where the children are or where a precious object is kept.
- **Group:** `InformationGathering`. **Pairs:** with delivery, ε-ζ (p.80; p.64). **Corpus:** 0.
- **Literal meaning:** The villain looks for a weak point.
  He comes into the tale, in person or by stealth, to find out where the household can be hurt.
- **Cultural meaning:** Someone is watching with ill intent.
  The home is surrounded by people who mean it harm.
  The villain's scouting shows that the household's safety is always being watched by those who do not share its values.
  It marks the moment when innocence becomes a target, and shows that the world will find and test every blind spot.

### `delivery`

- **Number and sign:** V, ζ. **Page:** p.28. **Propp's name:** delivery.
- **What happens:** the villain receives information about his victim.
- **Group:** `InformationGathering`. **Pairs:** with reconnaissance; it may stand without it, as a careless act (p.29). **Corpus:** 0.
- **Literal meaning:** The villain learns what he needs.
  The knowledge reaches him, and the victim or the household is left open to attack.
- **Cultural meaning:** No home can stay sealed.
  How easily information gets out, whether by the villain's cunning or by a careless act, shows that a home cannot stay closed off for ever.
  The young person's weak points, hidden assets or simple naivety will come to light sooner or later, and a private weakness becomes the start of a public crisis.

### `trickery`

- **Number and sign:** VI, η. **Page:** p.29. **Propp's name:** trickery.
- **What happens:** the villain, often disguised, tries to deceive the victim in order to take possession of him or his belongings.
- **Group:** `DeceptionTrap`. **Pairs:** with complicity, η-θ (p.80). **Corpus:** 0.
- **Literal meaning:** The villain uses a disguise or a lie.
  The false front is meant to get past the victim's guard before any open attack.
- **Cultural meaning:** Danger rarely looks like danger.
  A harmless-looking disguise or a kindly offer shows that ill will often comes looking safe, familiar or helpful.
  The trick works on what the young person was taught at home: to trust, to obey, to accept a gift.
  It teaches a hard truth: someone without experience cannot tell real kindness from manipulation by looks alone.

### `complicity`

- **Number and sign:** VII, θ. **Page:** p.30. **Propp's name:** complicity.
- **What happens:** the victim is taken in by the deception and so unwittingly helps the enemy.
- **Group:** `DeceptionTrap`. **Pairs:** with trickery; it may stand without it, as falling asleep unprompted (p.30). **Corpus:** 0.
- **Literal meaning:** The victim falls for it.
  By agreeing, or by giving up his guard, the victim supplies the last step that turns the villain's trick into real harm.
- **Cultural meaning:** Innocence is no protection.
  The victim's unknowing surrender, whether by accepting a poisoned gift or by falling asleep with no prompting, shows that a child's innocence gives no defense against deliberate deceit.
  This is the low point of life at home: the young person is left helpless, which shows that naive trust alone is not enough to survive.

### `villainy`

- **Number and sign:** VIII, A. **Page:** p.30; its forms run to p.34. **Propp's name:** villainy.
- **What happens:** the villain causes harm or injury to a member of the family.
- **Group:** `MoveTrigger`, in the complication. **Pairs:** with liquidation, A-K, the pair that spans the move (p.53). **Corpus:** 53, the opener of each.
- **Measured:** Counted by `villainy.py` and pinned by a test. Of the 55 moves opened by villainy, the villain abducts a person in 19, expels someone in 6, torments at night in 4, spoils the crops and declares war in 3 each, maims, plunders, murders, casts into the sea and casts a spell in 2 each, and seven other forms occur once; 4 are written in roman subforms not decoded here. The typical crime is taking a person, often a daughter, sister or bride. Expulsion, the second most frequent, is Propp's own example of the villain inside the family: a stepmother drives out her stepdaughter (p.33). He also marks two forms, forced marriage and cannibalism, with subforms among relatives (p.34).
- **Literal meaning:** Harm from outside that sets a move going.
  Propp calls this function extremely important, since the real movement of the tale begins with it (p.30).
- **Cultural meaning:** *Draft.* A wrong that demands an answer.
  Harm done to the family must be met.

### `lack`

- **Number and sign:** VIIIa, a. **Page:** p.35. **Propp's name:** lack.
- **What happens:** a member of the family lacks something or wants something: a bride, a magical agent, a marvel.
- **Group:** `MoveTrigger`, in the complication. **Pairs:** with liquidation, as villainy does. **Corpus:** 26, the opener of each.
- **Literal meaning:** Trouble from within.
  It does the work of villainy and leads to a quest in the same way (p.34), and a move begun from it is undone by the same liquidation.
- **Cultural meaning:** *Draft.* A rightful want.
  A bride, a wonder, the means of life: a reason to go out and win it.

### `mediation`

- **Number and sign:** IX, B. **Page:** p.36. **Propp's name:** mediation, the connective incident.
- **What happens:** the misfortune or lack is made known; the hero is asked or commanded, and is allowed to go or is sent.
- **Group:** `complication`, as the dispatch; `MoveTrigger`, where no villainy occurs and it opens the move (p.37). **Pairs:** none. **Corpus:** 41, one of them, 133 II, as an opener.
- **Measured:** Counted by `dispatch.py` and pinned by a test. Of the 43 moves carrying B, the hero is called in 6 (B1), sent in 9 (B2), allowed to go in 8 (B3) and told of the misfortune in 12 (B4); the victimized hero is taken away from home in 4 (B5) and lamented in 1 (B7), and never secretly freed (B6). Three more carry B in another function's form, at 144 I, 163 I and 164 II (p.67). Only B2, 9 of the 40 moves with a form, is plain sending by command or request. The Corpus figure of 41 counts the moves v46 accepts; the other two, 126 II and 137 II, are among the four it rejects.
- **Literal meaning:** The hero is drawn in.
  It links the misfortune to the one who will act on it.
- **Cultural meaning:** *Draft.* The need made known.
  The need is made known and the way out is opened; answering it is up to the hero.
  In most forms, the one who brings the news or gives leave does not give orders, and the young one volunteers.

### `beginningCounteraction`

- **Number and sign:** X, C. **Page:** p.38. **Propp's name:** beginning counteraction.
- **What happens:** the seeker agrees to act, or decides to.
- **Group:** `complication`. **Pairs:** none. **Corpus:** 61.
- **Literal meaning:** The hero decides to act.
  It is the moment the tale turns from suffering to seeking.
- **Cultural meaning:** *Draft.* Taking responsibility.
  Accept the task and decide to act; the hero chooses.

### `departure`

- **Number and sign:** XI, ↑. **Page:** p.39. **Propp's name:** departure.
- **What happens:** the hero leaves home.
- **Group:** `complication`, which it closes; or `EarlyLeaving`, before the crisis (p.107). **Pairs:** none named, though it faces the return. **Corpus:** 66.
- **Literal meaning:** Setting out.
  With villainy, dispatch and counteraction, it completes the complication (pp.64-65).
- **Cultural meaning:** *Draft.* Leaving home.
  Leave home to make one's own way.

### `firstDonorFunction`

- **Number and sign:** XII, D. **Page:** p.39. **Propp's name:** the first function of the donor.
- **What happens:** the hero is tested, questioned or attacked, which prepares the way for his receiving a magical agent or helper.
- **Group:** `TestedAcquisition`, which it opens; or `EarlyHelp`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of F (pp.46-47). **Corpus:** 31.
- **Literal meaning:** The test.
  The donor checks whether the hero deserves help.
- **Cultural meaning:** *Draft.* One is always being tested.
  Be courteous and kind to strangers, the old, the weak and animals.

### `heroReaction`

- **Number and sign:** XIII, E. **Page:** p.42. **Propp's name:** the hero's reaction.
- **What happens:** the hero reacts to what the future donor does, well or badly.
- **Group:** `TestedAcquisition`, which it opens when the test is left out; or `EarlyHelp`, before the crisis (p.107). **Pairs:** with the test it answers. **Corpus:** 32.
- **Literal meaning:** The hero's answer to the test.
  It decides whether help is given.
- **Cultural meaning:** *Draft.* The right response.
  Politeness, compassion, sharing, a promise kept: here the tale teaches its ethics most plainly.

### `receiptOfMagicalAgent`

- **Number and sign:** XIV, F. **Page:** p.43. **Propp's name:** provision or receipt of a magical agent.
- **What happens:** the hero gains the use of a magical agent: an animal, an object, a quality.
- **Group:** `TestedAcquisition` after a test or reaction; `UntestedAcquisition` otherwise, in the complication (step 6); or `EarlyHelp`, before the crisis (p.107). **Pairs:** its forms are bound to the forms of D (pp.46-47). **Corpus:** 40; the tested agent appears in 32 moves and the untested in 17.
- **Measured:** Counted by `agentForms.py` over the 84 moves, the parked cells left of A excluded, and pinned by a test. Of 57 F cells, 35 are tested (after a D or E), 12 untested before the departure, and 10 untested on the road. Three findings. (1) An agent received at home never comes by chance or by magic: all 12 are transferred (6), prepared (5) or bought (1), and none is found, appears, is seized or offers service. (2) Seizure follows a test every time, 3 of 3, as Propp ties seizure to a hostile donor (pp.46-47). (3) An offer of service follows a test 7 times in 8, the grateful creature repaying the hero's mercy. On the road, 3 of 10 untested agents appear of their own accord. The counts are small, and "tested" means a D or E came earlier in the move.
- **Literal meaning:** The means to undo the misfortune.
  Earned from a donor, it is a reward; received with no test, from a father or by finding it, it comes with the setting out.
- **Cultural meaning:** *Draft.* Help earned is power.
  Those who behave rightly are equipped by others, and what was promised in return is paid.

### `spatialTransference`

- **Number and sign:** XV, G. **Page:** p.50. **Propp's name:** spatial transference between two kingdoms, guidance.
- **What happens:** the hero is carried, delivered or led to where the object of his search is.
- **Group:** `Development`. **Pairs:** none. **Corpus:** 25.
- **Literal meaning:** The passage to the other kingdom.
  It is where the misfortune can be undone.
- **Cultural meaning:** *Draft.* Go where the task is.
  However far it is.

### `struggle`

- **Number and sign:** XVI, H. **Page:** p.51. **Propp's name:** struggle.
- **What happens:** the hero and the villain meet in direct combat.
- **Group:** `StruggleAndOutcome`, or `LateStruggle` after a pursuit (p.107). **Pairs:** with victory, H-I (p.64). **Corpus:** 25.
- **Literal meaning:** The face-off with the villain himself.
- **Cultural meaning:** *Draft.* Face the enemy.

### `branding`

- **Number and sign:** XVII, J. **Page:** p.52. **Propp's name:** branding, marking.
- **What happens:** the hero is marked: wounded in the fight, or given a ring or a towel.
- **Group:** `StruggleAndOutcome` in the fight; `TaskAndSolution` after a task (p.104; step 5); `LateStruggle` after a pursuit. **Pairs:** with recognition, J-Q, the one crossing pair, carried as a dependency. **Corpus:** 2.
- **Literal meaning:** The sign by which the hero will be known.
  It is rare in the corpus but central to the end, since it is what the recognition reads.
- **Cultural meaning:** *Draft.* Your deeds leave marks.
  Bear the marks of what you have done; they will vouch for you.

### `victory`

- **Number and sign:** XVIII, I. **Page:** p.53. **Propp's name:** victory.
- **What happens:** the villain is defeated, in combat, in a contest, or by other means.
- **Group:** `StruggleAndOutcome`, or `LateStruggle`. **Pairs:** with struggle; it may stand without it (p.29). **Corpus:** 33.
- **Literal meaning:** The villain's power broken.
- **Cultural meaning:** *Draft.* Right wins.

### `liquidation`

- **Number and sign:** XIX, K. **Page:** p.53. **Propp's name:** none given; he writes it K and describes it as the liquidation of the initial misfortune or lack.
- **What happens:** the first misfortune or lack is undone: the object seized, the spell broken, the dead revived, the captive freed.
- **Group:** `TroubleToLiquidation`, which it closes. **Pairs:** with villainy, A-K; Propp says the story reaches its peak in it (p.53). **Corpus:** 47.
- **Literal meaning:** The misfortune undone.
  It is the point every move is heading for.
- **Cultural meaning:** *Draft.* Setting things right.
  Right what was wronged and restore what was lost; Propp calls it the tale's peak (p.53).

### `return`

- **Number and sign:** XX, ↓. **Page:** p.55. **Propp's name:** return.
- **What happens:** the hero returns.
- **Group:** `ReturnJourney`. **Pairs:** none named, though it faces the departure. **Corpus:** 42.
- **Literal meaning:** The way home.
  It opens the second half of the move.
- **Cultural meaning:** *Draft.* Bring home what you won.
  The achievement serves the family.

### `pursuit`

- **Number and sign:** XXI, Pr. **Page:** p.56. **Propp's name:** pursuit, chase.
- **What happens:** the hero is pursued.
- **Group:** `Evasion`, first in `PursuitFirst` and second in `RescueFirst`. **Pairs:** with rescue, Pr-Rs (p.64); reversed in the humorous tale (p.147). **Corpus:** 14.
- **Literal meaning:** The villain's last attempt.
  What was undone is threatened again.
- **Cultural meaning:** *Draft.* Success invites revenge.

### `rescue`

- **Number and sign:** XXII, Rs. **Page:** p.57. **Propp's name:** rescue.
- **What happens:** the hero is rescued from pursuit.
- **Group:** `Evasion`. **Pairs:** with pursuit. **Corpus:** 14.
- **Literal meaning:** The danger escaped.
  Many tales end here (p.92 lists it among the endings).
- **Cultural meaning:** *Draft.* Help earned earlier saves you later.

### `unrecognizedArrival`

- **Number and sign:** XXIII, o. **Page:** p.60. **Propp's name:** unrecognized arrival.
- **What happens:** the hero arrives home or in another country without being recognized.
- **Group:** `FraudPosture`. **Pairs:** with unfounded claims, as they move together between the two schemes (p.104). **Corpus:** 5.
- **Literal meaning:** The hero without his due.
  Present, but not known.
- **Cultural meaning:** *Draft.* Merit may go unnoticed for a time.
  Be patient and humble.

### `unfoundedClaims`

- **Number and sign:** XXIV, L. **Page:** p.60. **Propp's name:** unfounded claims.
- **What happens:** a false hero claims the hero's deed without right.
- **Group:** `FraudPosture`. **Pairs:** with unrecognized arrival; and it prepares exposure. **Corpus:** 6.
- **Literal meaning:** The hero's deed stolen.
  The end of the tale must set it right.
- **Cultural meaning:** *Draft.* Do not take credit you have not earned.
  The braggart who claims another's deed will be shamed.

### `difficultTask`

- **Number and sign:** XXV, M. **Page:** p.60. **Propp's name:** difficult task.
- **What happens:** a hard task is set for the hero: an ordeal, a riddle, a test of strength or endurance.
- **Group:** `TaskAndSolution`. **Pairs:** with solution, M-N, set in the scheme where H-I stands in the other (p.104). **Corpus:** 9.
- **Literal meaning:** The hero's worth tested by trial, not by combat.
  Propp finds it typical of a second move (p.104).
- **Cultural meaning:** *Draft.* Prove yourself worthy.
  Worthy of the bride and of the position.

### `solution`

- **Number and sign:** XXVI, N. **Page:** p.62. **Propp's name:** solution.
- **What happens:** the task is accomplished; a solution that comes before the task is set Propp writes *N (p.62).
- **Group:** `TaskAndSolution`. **Pairs:** with difficult task; it may stand without it, as the preliminary solution (commentary p.145). **Corpus:** 9.
- **Literal meaning:** The trial passed.
- **Cultural meaning:** *Draft.* Ability proven.
  Success confirms the hero's standing, as the task cycle shows.

### `recognition`

- **Number and sign:** XXVII, Q. **Page:** p.62. **Propp's name:** recognition.
- **What happens:** the hero is recognized: by a mark, by a thing given him, by a task accomplished, or after a long separation.
- **Group:** `Endgame`, where it may change places with exposure, punishment and wedding (p.108). **Pairs:** with branding, J-Q, as a dependency; with exposure. **Corpus:** 7.
- **Literal meaning:** The hero known for who he is.
  It undoes the unrecognized arrival.
- **Cultural meaning:** *Draft.* True worth is seen in the end.

### `exposure`

- **Number and sign:** XXVIII, Ex. **Page:** p.62. **Propp's name:** exposure.
- **What happens:** the false hero or the villain is exposed.
- **Group:** `Endgame`. **Pairs:** with recognition; it answers the unfounded claims. **Corpus:** 5.
- **Literal meaning:** The false claim undone.
- **Cultural meaning:** *Draft.* Lies are found out.

### `transfiguration`

- **Number and sign:** XXIX, T. **Page:** pp.62-63. **Propp's name:** transfiguration.
- **What happens:** the hero is given a new appearance: new clothes, a palace, a handsome form.
- **Group:** none; it stands in `EarlyTransfiguration` before an opener or in `Digression` after any function, since Propp calls it the most unstable function in its position (p.108). **Pairs:** none. **Corpus:** 6.
- **Literal meaning:** The hero's new standing made visible.
  Its free place is itself a finding: it is the one function whose position means nothing.
- **Cultural meaning:** *Draft.* Worth made visible.
  The hero comes to look like who the hero is.

### `punishment`

- **Number and sign:** XXX, U. **Page:** p.63. **Propp's name:** punishment.
- **What happens:** the villain or the false hero is punished; a generous pardon is its negative form.
- **Group:** `Endgame`. **Pairs:** with wedding, the two changing places (p.108). **Corpus:** 15.
- **From Propp:** punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and the father often punishes the false hero (pp.79-80). The first villain usually ends by being beaten in combat, victory I, in the hero's sphere of action.
- **Literal meaning:** The wrong answered.
- **Cultural meaning:** *Draft.* Wrongdoers get what they deserve.
  Or, in the pardon, the victor shows mercy.

### `wedding`

- **Number and sign:** XXXI, W. **Page:** p.63. **Propp's name:** wedding.
- **What happens:** the hero marries and takes the throne; a reward without marriage counts as a form of it.
- **Group:** `Endgame`. **Pairs:** with punishment. **Corpus:** 34.
- **Literal meaning:** The hero given his due.
  It is the most common close of a move, and the ending p.92 names first.
- **Cultural meaning:** *Draft.* The goal of the passage.
  Marriage and the founding of a new household, which begins the next cycle.

## Elements that are not functions

**Two symbols of v46 are elements Propp names but does not number, so they stand outside the functions above.**

- **`initialSituation`, α.** p.25: the tale usually begins with some initial situation, the members of a family listed or the future hero introduced; it is not a function, but it is an important element of form. In v46 it stands at the beginning of the tale only, outside every move. **Corpus:** 0, since the moves of the corpus carry none.
- **`preliminaryMisfortune`, λ.** Appendix I Table II item 44, p.121: a misfortune that forces the victim to agree, within the deceitful bargain. In v46 it stands inside `DeceptionTrap`, between trickery and complicity. **Corpus:** 0.

The six remaining symbols, `/`, `⟨`, `⟩`, `<`, `Y` and `}`, are signs of how moves combine, and their meaning is given under `tale`, `FollowingMoves`, `EmbeddedMove`, `Parting` and `CommonEnding`.

## Dramatis personae

**Propp's seven spheres of action, entered as roles, as decided for now.**
p.79: many functions "logically join together into certain spheres", which "correspond to their respective performers"; p.80 concludes that the tale has seven dramatis personae.
A sphere is a role, not a person: one character may fill several spheres, and one sphere may be spread across several characters (pp.80-81).
The father who sends his son off and gives him a cudgel is dispatcher and donor at once (p.81).
The preparatory functions are spread among the same characters, but too unevenly to define them (p.80), so they appear in no entry below.

**The order is one of social rank, and it is speculation, not Propp.**
Highest standing goes to the hero, then the princess and her father, the dispatcher, the donor, the helper, the false hero, and the villain.
Propp does not order the spheres.
On the speculative reading set out above, they outline the social ranks of Indo-European culture, the same from the kingdom down to the family, the kingdom being pictured as a family.
Each entry's "place in the social order" line applies that reading, and the cultural meanings are drafted with it in mind.
Both are drafts.

Each entry gives Propp's sphere and page, the functions he assigns it, the groups of v46 where they act, how many of the 80 accepted moves use at least one of them, its place in the social order, and its literal and cultural meaning.

### `hero`

- **Propp's sphere:** 6, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), `wedding` (W*). Propp: C is characteristic of the seeker-hero; the victim-hero performs only the rest.
- **Acts in:** `complication`, `TestedAcquisition` and `EarlyHelp`, `Endgame`. **Corpus:** 79.
- **From Propp:** p.81: characters are defined not by what they want or feel but by "their deeds as such, evaluated and defined from the viewpoint of their meaning for the hero and for the course of the action". To that extent the hero-centered reading is Propp's own method, not speculation.
- **From Propp:** pp.36-38: after a villainy the story follows either the one who goes in search, a seeker, or the one seized or driven out, a victimized hero, and no tale in Propp's material follows both (p.36). The forms of mediation tell which: B1-B4 refer to the seeker and B5-B7 to the victimized hero (p.37), and the decision to act, C, belongs only to tales whose hero is a seeker (p.38).
- **Measured:** Counted by `heroType.py` and pinned by a test; it reproduces two findings of the first project. Of the 32 tales carrying B, 26 follow a seeker and 3 a victimized hero, tales 95, 98 and 101; 3 carry B only in forms without a variety digit, and none follows both, as p.36 says. Of the 37 moves in which B and the departure stand together, 30 are seeker moves and 4 victim moves. The decision to act divides less cleanly than p.38 says: C stands in 27 of the 30 seeker moves and in 3 of the 4 victim moves. The seeker is the usual hero, 26 tales to 3; the victimized hero is Propp's own, and rare.
- **Place in the social order:** *Draft.* Highest, and the center. Every other role is defined by what it does to or for the hero, and ends as an audience for the hero's story.
- **Literal meaning:** The one whose fortunes the tale follows (p.36).
  Usually a seeker, who decides to act and sets out, answers the donor's test, and is married at the end.
  Sometimes a victim of the villainy, carried off or driven out, who, Propp says, performs all the hero's functions except the decision to act (p.38).
- **Cultural meaning:** *Draft.* The model for the young listener.
  The one who listens, chooses, dares, keeps faith and endures, and so rises from a dependent youth to the head of a household.
  The hero is usually, but not always, the one who chooses and leads: the victimized hero does not choose, and is the hero all the same, because the tale follows that hero's fortunes.

### `princessAndFather`

- **Propp's sphere:** 4, pp.79-80. **Functions:** `difficultTask` (M), `branding` (J), `exposure` (Ex), `recognition` (Q), `punishment` (U), `wedding` (W). Propp: the princess and her father "cannot be exactly delineated from each other according to functions"; most often the father sets the tasks, from hostility to the suitor, and punishes the false hero.
- **Acts in:** `TaskAndSolution`, `StruggleAndOutcome` for the branding, `Endgame`. **Corpus:** 38.
- **Place in the social order:** *Draft.* Second, and at the edge of the hero's story. The king is the head of the kingdom and of the family, holding the place until the next generation takes over; he sets the tasks and grants the kingdom. The princess chooses the hero, but is defined by her role as his wife and the mother of his line.
- **Literal meaning:** The sought-for person and her father.
  They set the hard task, mark the hero, recognize the true hero and expose the false one, punish the impostor, and grant the marriage.
- **Cultural meaning:** *Draft.* The house the hero joins.
  The king sets the tasks and grants, the princess chooses, and the outcome is never in doubt.
  The tales bend both roles freely: the king may favor or resist the hero, and the princess may choose at once or need to be won.
  Two earlier readings survive as the range within which the tales vary.
  One is *succession and exchange*: the father controls who marries into the house, and so who inherits.
  The other is *judgment and agency*: the princess marks, recognizes and exposes, so that the true hero is known through her judgment.

### `dispatcher`

- **Propp's sphere:** 5, p.80. **Functions:** `mediation` (B), the dispatch.
- **Acts in:** `complication`, and `MoveTrigger` when the connective incident opens a move. **Corpus:** 41.
- **From Propp:** the dispatcher's sphere holds the dispatch alone (p.80), and its seven forms name who fills it (pp.36-38). The call for help usually comes from the tsar (B1). With leave to depart, the push often comes from the hero, not from a dispatcher, and the parents give their blessing (B3). The misfortune is announced more often by old women or people met by chance than by parents (B4). The banished daughter is taken to the forest by her father, whose act Propp calls logically unnecessary: the tale demands parents as senders (B5, p.37). The hero condemned to death is freed by a cook or an archer (B6), and the lament is sung by a surviving brother (B7).
- **Measured:** Counted by `dispatch.py` and pinned by a test; the forms are tallied under `mediation`. In 31 of the 40 moves where B carries a form, the dispatcher calls, permits, announces, transports or laments; only in 9 is the hero sent outright, by command or request.
- **Place in the social order:** *Draft.* Third as a role, but of mixed rank as a person. The role is filled by the tsar, by parents, by old women and strangers met on the road, by a cook or an archer, and by a brother. A role filled from so wide a range of rank marks the dispatcher as a minor character: a role defined by one moment, the push out of the door, not by who performs it.
- **Literal meaning:** The one who makes the need known and opens the way out.
  The dispatcher calls for help, sends, permits, announces, transports or frees.
  Only the direct dispatch is plain sending; in most forms the dispatcher informs or permits, and the hero decides.
- **Cultural meaning:** *Draft.* Authority opens the way, and the young one chooses to take it.
  The elder proclaims, announces or blesses, and the hero volunteers, just as the king sets the task and grants the prize.
  The tale wants the push to come from home, since Propp finds it demanding parents as senders even where the action needs none (p.37); yet the news comes more often from strangers than from parents.
  What matters is less who sends than that the hero answers.

### `donor`

- **Propp's sphere:** 2, p.79. **Functions:** `firstDonorFunction` (D), `receiptOfMagicalAgent` (F).
- **Acts in:** `TestedAcquisition`, `EarlyHelp`, and, when the agent comes with no test, `UntestedAcquisition`. **Corpus:** 45.
- **Place in the social order:** *Draft.* Fourth. The elder, or the powerful outsider, who judges the hero and gives him what he needs.
- **Measured:** From the donor's side, counted by `agentForms.py` and pinned by a test: the tested agent is the donor's gift, 35 cells in 28 moves. The father's gift at home, where the father is dispatcher and donor at once (p.81), is always given, made or bought, 12 of 12. Seizure, 3 of 3, comes only after a test, which is where Propp ties it to a hostile donor (pp.46-47). An offer of service comes after a test 7 times in 8: the donor repays the hero's kindness.
- **Literal meaning:** The one who tests the hero and provides the magical agent.
- **Cultural meaning:** *Draft.* The test of character.
  Honor the donor and keep the bargain: the hero never cheats a friendly donor of what was agreed.
  Against a hostile or deceitful donor, trickery is allowed, since good faith is owed only to good faith (pp.46-47).
  The father's gift, where the father is dispatcher and donor at once (p.81), comes by right of family, not by test.

### `helper`

- **Propp's sphere:** 3, p.79. **Functions:** `spatialTransference` (G), `liquidation` (K), `rescue` (Rs), `solution` (N), `transfiguration` (T).
- **Acts in:** `Development`, `TroubleToLiquidation`, `Evasion`, `TaskAndSolution`, and `EarlyTransfiguration` or `Digression` for T. **Corpus:** 68.
- **From Propp:** p.82: living things, objects and qualities "function in exactly the same manner"; Propp calls the living ones magical helpers and the objects and qualities magical agents. A carpet that carries the hero is, in form, the same as a horse that does, and so is the hero's own acquired power to turn into a falcon. He distinguishes three kinds: universal helpers, which can perform all five functions, and in his material only the steed; partial helpers, such as animals, spirits appearing out of rings, and what the English translation calls "various tempters"; and specific helpers, which perform one function and are objects only. Helpers can be people: the little iron peasant who rewards Ivan and then helps kill the dragon is donor and helper at once (p.80), and the "tempters" of the English may render a Russian word for skilled or wonder-working people, which has still to be checked against the Russian.
- **Measured:** Counted by `agentForms.py --helper` and pinned by a test. Of the 84 moves, 43 receive an agent and 41 do not. Transference follows the gift: it occurs in 16 of the 43 (37%) against 9 of the 41 (22%), as in Propp's own example of the flying horse and carpet. The other helper functions show no such difference, and liquidation is less common where an agent is received, 24 of 43 against 27 of 41. Appendix III records functions, not who performs them, so the corpus cannot say who performed a helper's function, the helper or the hero; that would take reading the tales.
- **Place in the social order:** *Draft.* Fifth. The sidekick: a Sancho Panza to Don Quixote, a Tonto to the Lone Ranger.
- **Literal meaning:** The one who does the hero's work for him.
  The helper carries the hero, undoes the misfortune, rescues him from pursuit, solves the tasks and transforms him.
  The horse that does all of these is Propp's pure helper (p.80).
- **Cultural meaning:** *Draft.* Loyal service, which the hero earns and commands.
  The helper may do much of the work, but the credit goes to the hero, who chooses and leads.

### `falseHero`

- **Propp's sphere:** 7, p.80. **Functions:** `beginningCounteraction` (C), `departure` (↑), `heroReaction` (E), and, as his own function, `unfoundedClaims` (L).
- **Acts in:** `complication`, `TestedAcquisition`, `FraudPosture`. **Corpus:** 6 by his own function L; the rest he shares with the hero, and 77 moves hold one of C, ↑ or E.
- **From Propp:** the false hero is the "second villain" whose punishment belongs to the sphere of the princess and her father, the father often punishing him or ordering him punished (pp.79-80).
- **Place in the social order:** *Draft.* Sixth. Laughed at, and often the butt of the joke.
- **Measured:** Counted by `falseHero.py` and pinned by a test. The false hero's claim L appears in 5 tales, 125, 132, 139, 155 and 156, and in every one of them it stands in the tale's last move; in 125, in the shared ending that closes both moves. In all 5 the false hero is punished (U) and the tale ends in the wedding (W). The true hero is recognized (Q) in 4, all but 156, and the false hero is exposed by name (Ex) in 3, 125, 132 and 155. In 4 of the 6 moves holding an L, the hero's unrecognized arrival (o) stands beside it, the o-L pairing of p.104. He never appears early, never in a middle move, and never escapes.
- **Literal meaning:** The one who sets out like the hero and meets the donor, but claims the hero's deed without right.
- **Cultural meaning:** *Draft.* The liar, and the tale's scapegoat.
  The false hero breaks a basic Indo-European rule, do not tell lies, and that puts him at the bottom of the order beside the villain.
  The Old Persian inscriptions name the Lie as the root of evil; Herodotus says Persian boys were taught to ride, to shoot and to speak the truth; and the Avestan asha against druj and the Vedic ṛta against anṛta set truth against the lie as order against disorder.
  He is the hero's counterfeit: he sets out and meets the donor as the hero does, but fails the test, so he has no deed and can only claim one.
  The mark from the fight (J) is what the recognition reads (Q) to tell the true hero from him.
  His exposure moves from anger through punishment to ridicule.
  The surprise of the unmasking is where the humor lies, and once found out he becomes the butt of the joke, like the boastful soldier of Plautus's Miles Gloriosus, Falstaff at Gad's Hill, or the frauds who were tarred and feathered in nineteenth-century rural America.
  He is judged by the head of the house, not fought like the villain, and he is never let go.

### `villain`

- **Propp's sphere:** 1, p.79. **Functions:** `villainy` (A), `struggle` (H), `pursuit` (Pr).
- **Acts in:** `MoveTrigger`, `StruggleAndOutcome` and `LateStruggle`, `Evasion`. **Corpus:** 62.
- **From Propp:** the villain's sphere is villainy, struggle and pursuit (A, H, Pr; p.79), and it does not include punishment. Punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and Propp adds that the father "frequently punishes (or orders punished) the false hero" (pp.79-80). So the first villain is met by the hero in combat and beaten; the liar inside the order is judged by its head.
- **Measured:** Counted by `villainy.py` and pinned by a test. Of the 84 moves, 55 open on villainy and 28 on lack. In the villainy moves the harm is undone (K) in 65%, the villain is fought (H) in 35% and defeated (I) in 42%, he pursues (Pr) in 20%, and punishment (U) stands in 20%; lack moves run lower on combat, 21% struggle and 36% victory. The tale's business with the villain is undoing the harm, and his own end is often not marked. U does not say who is punished, and a dragon killed in combat is a victory, not a punishment.
- **Place in the social order:** *Draft.* Lowest. Despised: the enemy of the order.
- **Literal meaning:** The one who does harm, fights the hero, and gives chase.
- **Cultural meaning:** *Draft.* Evil to be opposed.
  The listener is meant to cheer the villain's defeat.
  When the villain is inside the family, a stepmother or envious sisters, the tale shows where the household order can fail.
