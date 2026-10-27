# Semantic catalog

**THE MASTER CATALOG, approved by the owner on 2026-10-25, merged from three files.**
`ProppPairsAndGroups.md` is the core: its order, its entries and its fields stand as the owner wrote them.
Into each of its entries are folded, labeled by source, the v46 grammar's data for the same group (`SemanticCatalog46.md`) and the semantic bundle and value for the same pair or group (`SemanticBundling.md`, the first project).
What has no counterpart in the core is placed whole: the argument for semantic bundling (Part I), the speculative reading the cultural meanings rest on (Part II), the functions one by one (in Part III), and the v46 grammar's own groups, its dependencies, extensions and lessons (Part V).
Every passage is copied from its source unchanged; only the connecting sentences and the source labels are new. Duplicates were then cut at the owner's word (2026-10-25): superseded earlier wordings, the meanings of the eleven function entries that have entries of their own, repeated reading-guide fields, and the J–Q passages, gathered under the link "J to Q".
`ProppPairsAndGroups.md` and `SemanticCatalog46.md` are retired, their last state in the repository's history (commit a8a7827); the frozen catalog tests (`StepTests.txt`, steps 6, 8, 10 and 11) read this file. `SemanticBundling.md` stays in the first project until the owner decides how to retire it there, since its published files cite it.

**Terms used throughout.**
A few terms first.
Propp's **functions** are the acts of characters he found in the Russian wondertale, thirty-one of them, each with a symbol: A for villainy, K for its undoing, and so on.
A **move** is one run of the story from a misfortune or a lack to its undoing; a tale has one or more.
The **grammar** writes Propp's order of functions as formal rules, in a standard notation called EBNF; each named rule is a **production**, and a **group** is a production that bundles several functions.
The grammar is version 46, **v46**; v43 and v44 are earlier versions, and a **step** is one stage of the work that turned them into v46, recorded in `StepTests.txt`.
The **corpus** is the 80 moves of Propp's Appendix III, his own analyses of 45 tales, that v46 accepts.
This catalog is what `SemanticBundling.md` in the first project was meant to become: every rule that is a real pair or group, and so means more than the functions inside it.
Each entry says whether it is a group or a pair, a production or a dependency, and at which level it sits, with its page and its meaning.

Terms peculiar to this file, with the rest in `Readme.md` §Terms used throughout.
A **semantic bundle** is what a unit means that its parts do not mean separately.
A **group** is Propp's own mid-level unit, a run of functions he names as belonging together, such as the complication `ABC↑`.
The **empty structure charge** is Lévi-Strauss's objection that abstracting form from content leaves a schema carrying no meaning.

## How to read an entry

- **Symbols.** The functions it holds, in Propp's letters; `[ ]` marks one that may be absent. For a device Propp's list lacks, the acts or verbs that carry it.
- **From Propp.** What Propp says of it, with the page of the 1968 English edition (Morphology of the Folktale, second edition, University of Texas Press), checked against the text. For a device Propp's list lacks, "none, not in his list," then the studies and genres it was found in.
- **Links.** The long-distance links it takes part in.
- **Measured.** What this project has counted about it, by a program anyone can rerun. The pair figures are from the frequency analysis (`Ngrams/ConfirmRun.txt`): how many times more often the second half follows the first than in the same stories shuffled, on the half of the stories kept back for confirmation, transcriber A then B; "acts" gives the same for the acts described without Propp's notation. "In stories" gives the share of stories holding the function: Propp's own 45 tales (Appendix III), then transcribers A and B on the wondertales (card U), the animal tales, the fables, the tragedies and the myths, from the normalized tables (`Data/`). Propp's own tables begin at A, so they hold no preparatory functions.
- **Literal meaning.** What it says on its surface. A short phrase, then a few sentences more.
- **Cultural meaning.** A reading of the conduct and values the tale may hold up to its listeners. These readings are speculation, not Propp, set out in `SemanticCatalog46.md`, section "A speculative reading, not from Propp"; they are drafts, and where they cite another scholar, the claim is that scholar's.

**The negative mode.** Propp lets a function fail or turn the other way, and his tables mark it with a minus: E− the hero fails the test, F− the magical agent is not received, and so on (his schemes in Appendix III; in this project's transcriptions, the same sign). A negative function is the same function in another mode, not a new one, which is part of why Propp's list covers so much. Measured (`Data/` tables, 2026-10-21): negative forms are rare in every genre, 3.3% of the wondertales' functions, 2.6% of the animal tales', 6.8% of the fables', 3.4% of the tragedies' and 3.0% of the myths', mostly E− and F−; the fable uses the mode most and over the most functions (F−, E−, θ−, K−, I−).
- **In v46.** Where the entry's group is a group of the grammar `ProppEBNF46.txt`: its kind, what it holds, Propp's warrant, its name, how many of the 80 accepted moves use it, its tree test and its rule, from `SemanticCatalog46.md`.
- **Semantic bundle.** Where `SemanticBundling.md` treats the same pair or group: what the unit means that its parts do not mean separately, the value it encodes, and its count in Propp's own tables.

# Part I: The argument, that Propp's structures carry meaning

**From `SemanticBundling.md`, Part I, unchanged.** Its file references (`Readme.md`, `ProppMidLevelGroupsEbnf.txt`, `ResolvedMoves.txt`) are to the first project, `Story Language/Project Files`. Its own opening read:

> This file is a draft, and Part III explains why it cannot be finished inside this project.
> It argues that Propp's structures carry meaning, against the charge that his method leaves an empty schema.
> Citations to Propp give printed pages in *Morphology of the Folktale*, 2nd ed., trans. Laurence Scott (Texas, 1968).

## 1. Propp gives three levels, not one

**The received picture of Propp is a flat list of 31 functions, but his text is not flat.**
Immediately after listing the pairs he writes (p.64–65):

> *"Other functions may be arranged according to groups. Thus villainy,
> dispatch, decision for counteraction, and departure from home (ABC↑),
> constitute the complication. Elements DEF also form something of a
> whole."*

So he names three levels:

| level | unit | examples | citation |
|---|---|---|---|
| fine | **pairs** | H–I, Pr–Rs, M–N, β–δ, ε–ζ | p.64, p.108 |
| **mid** | **groups** | `ABC↑` = the complication; `DEF` = the donor sequence | p.64–65 |
| top | **tale classes** | development through H–I / M–N / both / neither | p.102 |

**The mid level is the one that carries most cultural content, and it is Propp's own.**
It has been largely ignored because his readers inherited the flat list.

## 2. The decisive distinction: constituency is semantic, not syntactic

**An earlier grammar in this project, v43, encoded these groups as EBNF productions and was falsified.**
The reason matters, because it is the whole methodological key.

EBNF concatenation does two jobs at once: it imposes order and obligation.
Propp asserts order (Thesis III, p.22) and explicitly denies obligation, by the Law of Omission at p.22: *"The absence of certain functions does not change the order of the rest."*
So every production rule silently manufactured a constraint he never claimed.
Eight of nine such axioms were refuted by his own tales.

**But grouping and obligation are separable.**
The shape of the separation is sketched below.
This is a sketch and not the grammar.
The authoritative form is `ProppMidLevelGroupsEbnf.txt`; where the two differ, that file governs and this one is to be corrected.

```ebnf
move         = preparatoryGroup complicationGroup donorGroup
               struggleGroup taskGroup pursuitRescuePair
complicationGroup = opener { 'B' } { 'C' } { 'up' }
opener            = 'A' | 'a' | 'B'
donorGroup        = { 'D' } { 'E' } { 'F' }
```

**A third correction, and it is the file's own rule applied to itself.**
This sketch once named a `branch` and a `denouement` nonterminal.
`ProppMidLevelGroupsEbnf.txt` carries neither.
It says so expressly under a heading reading why there is no branch nonterminal: a branch has a warrant, but this notation cannot carry it.
The slot layer a denouement belonged to has been removed as well.
Since this file declares that where the two differ the other governs and this one is to be corrected, both are gone.
The sketch still omits the individual functions the authoritative file leaves loose between the groups, which is a simplification rather than a disagreement.

**Two things this sketch must get right, and an earlier version of it got both wrong.**
First, the opener is not optional.
v44 makes `opener`, at `'A' | 'a' | 'B'`, the sole surviving axiom, the one obligation Propp states.
A sketch with an optional opener would accept a move beginning on D and would accept the empty string, both of which v44 rejects.
Second, `{ }` is zero-or-more and `[ ]` is zero-or-one, and the braces here are load-bearing: three moves in `ResolvedMoves.txt` repeat a function outside any Propp brace, so a bracketed form would reject them.

**The grouping therefore adds no falsifiable claim beyond v44's own.**
It inherits v44's opener obligation unchanged and asserts nothing further about what must occur.

That is not a defect.
It is the point.

**The grouping is a claim about meaning, not about well-formedness.**
It says what belongs with what, not what must occur.
Stating it in EBNF is legitimate precisely because it adds nothing the corpus could refute.
It is not that kind of claim.

**`preparatoryGroup` is the one place where this needs qualifying.**
It rests on Propp's own text and not on the corpus.
Two warrants carry it.
Appendix I Table II is titled The Preparatory Section, which is Propp naming the unit in a heading.
And p.80 gives the section in a parenthesis, in his own notation, inside a passage about how the preparatory functions are distributed among the seven dramatis personae.
The pairing rests on the parenthesis alone, since Table II's headings are single functions and it pairs nothing.
Neither warrant faces the corpus: no Appendix III tale carries a preparatory function, so nothing in that group can be exercised by the material.
v44 omits the section deliberately for that reason (p.116), and the mid-level grammar's only constraint here is that it must not contradict v44.

This gives us the mid-level production rules without reintroducing v43's error.

## 3. Why "empty structure" is refuted by Propp's own text

**Lévi-Strauss's charge (*Structure and Form*, 1960) is that Propp abstracted form from content and was left with a schema empty of meaning.**
The charge has become conventional wisdom.
It is wrong, and the evidence is in Propp's own words.

**The linkage passage, p.109:**

> *"H¹ (fight in an open field) is always connected with I¹ (victory in an open
> field), and a connection with, for example, I⁸ (winning at cards) is
> completely impossible and devoid of sense."*

**Not *ungrammatical*, but senseless.**
Propp grounds the constraint in meaning.
A purely formal schema could not distinguish H¹–I¹ from H¹–I⁸: both are well-formed sequences of two functions.
What forbids the second is semantic content: a fight in a field is answered by winning a fight, not by winning at cards.

**And p.64:** one function develops out of another *"with logical and artistic necessity."*

**The empirical confirmation.**
Testing this against Propp's own 45-tale corpus:

```
   H–I pairs found: 25    varieties corresponding: 25    mismatched: 0
```

If the structure were an empty combinatorial schema, any variety could pair with any other.
It cannot.
The constraint is real, exceptionless in the corpus, and Propp himself says what enforces it: sense.

**This is the argument.**
Not that Propp's schema *might* carry meaning, but that its combinatorial restrictions are *inexplicable without* meaning, and that Propp said so explicitly, in the sentence Lévi-Strauss's followers have not answered.

## 4. The comparative dimension

The conjecture that these structures encode inherited Indo-European values is not speculative, and the external evidence is now quantitative.

**Da Silva & Tehrani (2016)**, *Royal Society Open Science* 3(1): 150645, applied phylogenetic methods to 275 Magic Tale types across 50 Indo-European-speaking populations from the ATU index.
They found strong correlations between folktale distribution and phylogenetic, but not spatial, association among populations, which is consistent with *vertical* cultural inheritance rather than horizontal borrowing between neighbors.
They date the traditions well before the literary record, with one tale ("The Smith and the Devil") traced to the Bronze Age.

Vertical transmission down language lineages is exactly the mechanism required for Propp's structures to be culturally inherited rather than independently reinvented.

**The literary corroboration is direct.**
The closing movement of the *Odyssey* is Propp's second-move sequence almost cell for cell:

| Propp | *Odyssey* |
|---|---|
| `o` unrecognized arrival | Odysseus returns to Ithaca disguised |
| `L` unfounded claims | the suitors press their claim to Penelope |
| `M–N` difficult task and solution | the stringing of the bow |
| `Q` recognition | Eurycleia knows the scar |
| `Ex` exposure | the suitors are revealed as usurpers |
| `U` punishment | the slaughter in the hall |
| `W` wedding | reunion with Penelope |

That an eighth-century BCE Greek epic and a nineteenth-century Russian peasant tale share this sequence is not a coincidence of plot; it is a shared structural inheritance.

**What our corpus can and cannot do.**
Forty-five Afanasyev tales establish what the structures encode *in this tradition*, with Propp's own citations.
They cannot by themselves demonstrate Indo-European scope; that argument rests on the comparative and phylogenetic literature.
What the catalog below provides is the instrument: a structure-by-structure account of semantic content, stated precisely enough to be compared against other corpora.
Propp remains the only hard, data-driven model at this granularity, which is exactly why it is worth making the semantics explicit.

# Part II: A speculative reading, not from Propp

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

# Part III: The catalog

## The variable scheme

```text
α β γ δ ε ζ η [λ] θ A B C ↑ D E F G [ (H J I K ↓ Pr Rs o L) / (o L M J N K ↓ Pr Rs) ] Q Ex T U W*
```

### `variableScheme`

- **Symbols:** the line above; the upper branch for moves with struggle and victory, the lower for moves with a difficult task

- **From Propp:** pp.104-105: adding up the schemes of his tales, Propp finds that struggle and victory (H-I) and the difficult task and its solution (M-N) hold the same place in the series, and only the unrecognized arrival and the false claim (o-L) shift, after the fight but before the tasks. All the tales of his material follow this one variable scheme. The preparatory section is added here; Propp's line begins at A.

- **Measured:** the v46 grammar, which writes this scheme as productions, accepts 80 of Propp's 84 moves and 41 of his 45 whole tales.

- **Literal meaning:** The whole story.
  A misfortune or a want sets it going, and each new one starts a new move inside it.

- **Social lesson:** Success is earned, not inherited: leave home, pass the tests in their order, and come back to found a household of your own. Rank and marriage reward proven merit, and they are open even to the youngest and the least regarded.

- **Cultural meaning:** This move scheme can be read as a young person's passage away from home, unprotected for a time, until becoming the head of a new home.
  Propp himself later read the tale as a memory of initiation rites (Historical Roots of the Wondertale, 1946).
  The family order is the same in a kingdom as in a peasant household.
  The tale is a cycle: it starts from one family and ends by founding the next, whose child may become the next hero.

  The scheme also holds tests in threes. Propp notes trebling as a common way functions are repeated (p.74). Dundes argues that the pattern of three belongs to the cultures that tell these tales, the first two instances setting a pattern that the third confirms or breaks ("The Number Three in American Culture," 1968). Greimas (1966/1983, Chapter 10) reads the hero's path as three tests: the qualifying test (D E F in Propp's model), the main test (H to K), and the glorifying test (M N). On that reading the sequence validates the hero as a true hero by merit.
- **In v46, `tale`** (from `SemanticCatalog46.md`):
  - **Kind:** group of the whole. **Level:** tale.
  - **Holds:** an optional initial situation α, the preparatory section, then one or more moves separated by `/`.
  - **Warrant:** p.92: in terms of form, a tale is any development that starts from a villainy or lack, and each new villainy or lack starts a new move.
  - **Name:** Propp's. **Corpus:** not measured; the corpus is made of moves. **Tree test:** `A K / a K`, the second move's `a` under `tale`.
  - **EBNF:** `tale = [initialSituation] preparatorySection move FollowingMoves`

## The four kinds of move

**Propp lists the moves of his tales in four kinds** (pp.104-105). Each is a path through the variable scheme.
Measured for all four (`Data/` tables, 2026-10-21): the share of moves of each kind, by whether the move holds H or I, M or N, both, or neither; counted on Propp's own 86 moves (the shared tails counted with their moves), and on transcribers A and B. These counts and the table under "The two branches" below are on different bases: here a move counts as a struggle move if it holds H or I and neither M nor N, over 86 moves; there, a move counts if it holds the pair H–I, over 83 moves, tale 136 IV held out. So 38% struggle-only here and 30% H–I there are both right.

### `struggleMove`

- **Symbols:** A B C ↑ D E F G H J I K ↓ Pr Rs o L Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with struggle and victory, or a simple killing of the enemy; a move with H-I is the typical first move.
- **Measured:** struggle without task in Propp 38% of moves; wondertales 30% and 33%; animal tales 15% and 13%; fables 6% and 6%; tragedies 18% and 21%; myths 20% and 31%.
- **Literal meaning:** The fight story.
  The hero wins back what was lost by defeating the one who took it, and comes home.
- **Social lesson:** Meet a real threat with courage. A success won by facing the enemy gives the right to lead.
- **Cultural meaning:** This move resolves a problem, whether a lack or a misfortune, through direct force, although the victory can be won in any contest, a game of cards among them.

### `taskMove`

- **Symbols:** A B C ↑ D E F G o L M J N K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with difficult tasks; such moves are most often second or repeated, and only once first.
- **Measured:** task without struggle in Propp 12% of moves; wondertales 10% and 12%; animal tales 1% and 0%; fables 3% and 2%; tragedies 1% and 2%; myths 2% and 3%.
- **Literal meaning:** The task story.
  The hero arrives unknown, a rival claims the hero's due, and the hero proves the right by doing what no one else can.
- **Social lesson:** Prove your worth by skill and wit before those who judge. The deserving one can do what the boaster cannot.
- **Cultural meaning:** This move resolves a problem through actions other than direct force.

### `bothStruggleAndTaskMove`

- **Symbols:** A B C ↑ F H I K ↓ L M N Q Ex U W*
- **From Propp:** p.105: tales with both pairs follow the upper branch and then, without coming to an end, the lower; H-I come before M-N, L stands between them, and no pursuit occurs in the cases Propp examined.
- **Measured:** both in Propp 1% of moves; wondertales 4% and 5%; animal tales 1% and 0%; fables 0% and 0%; tragedies 3% and 1%; myths 4% and 9%.
- **Literal meaning:** The fight, then the proof.
  The hero wins the fight, but a false claimant takes the credit, and the hero must win again by the task.
- **Social lesson:** Doing the deed is not enough; you must be able to prove it. Whoever steals the credit for another's deed will be found out.
- **Cultural meaning:** As a story device, this move adds surprise to the struggle: the hero is recognized only after the task is done, and the false hero is exposed. The false claim is a lie, and the tale treats it as gravely wrong; one reading, the owner's and still to be tested (`ProppQueue.md` item (k)), is that it puts the false hero at the bottom of the tale's social order.

### `neitherStruggleNorTaskMove`

- **Symbols:** A B C ↑ D E F G K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.105: the schemes with neither struggle nor tasks; they bypass the distinctive elements of each and present no construction of their own.
- **Measured:** neither in Propp 49% of moves; wondertales 55% and 50%; animal tales 83% and 87%; fables 92% and 92%; tragedies 78% and 77%; myths 74% and 57%. The short genres are mostly moves of this kind.
- **Literal meaning:** The quest without a contest.
  What was lost is found or won back with the help gained on the way, with no fight and no test of right.
- **Social lesson:** Courtesy, hospitality and kindness to strangers are rewarded. Good conduct alone can carry you to success.
- **Cultural meaning:** This move holds only Greimas's qualifying test (D E F in Propp's model), where the hero may perform an act of courtesy, such as sharing bread with an old man, and is given what he needs. The test can be read as valuing solidarity and the customs of hospitality. The move may also reflect a wish that relief can come without painful struggle, a comfort for the listener.

### The two branches: the sharpest cultural finding

**From `SemanticBundling.md`, Part II, unchanged.** Each entry gives the structure, its Propp citation, the semantic bundle (what the unit means that its parts do not mean separately), and the value encoded.

Propp, p.102:

> *"These two pairs are the struggle with the villain and victory over him
> (H–I), and the difficult task and its resolution (M–N). In 100 tales the first
> pair is encountered 41 times, the second pair 33 times, and the two combined
> into one move three times."*

And the four classes (p.102): development through H–I, through M–N, through both, through neither.

**These two pairs occupy the same structural slot.**
Propp's Appendix III shares their columns: H/M in one column, I/N in the next.
A move that uses both cannot be printed, which is why he excluded tale 123 from his corpus entirely (*"creates a motley"*, commentary p.146) and described tale 136's fourth move in prose instead.

| | H–I branch | M–N branch |
|---|---|---|
| **bundle** | opponent confronted, opponent defeated | task imposed, task accomplished |
| **proof of worth** | force | competence |
| **who validates** | the villain, by being beaten | a task-setter, by being satisfied |
| **frequency** | 41/100 | 33/100 |

**Value encoded: a culture offering two competing models of how worth is proven, by strength or by capability, and requiring a move to choose one.**

**Measured against our corpus.**
The corpus here is 45 tales and 83 moves, with tale 136 Move IV held out; it is the one move recovered from Propp's commentary rather than the printed table, and exactly the kind of move the table cannot print.

|          | Propp, per 100 tales | ours, per tale | ours, per move |
|---|---|---|---|
| H–I      | 41%                  | 47% (21/45)    | 30% (25/83)    |
| M–N      | 33%                  | 22% (10/45)    | 12% (10/83)    |
| both     | 3%                   | **0%**         | **0%**         |
| neither  | —                    | —              | 58% (48/83)    |

**The M–N per-tale cell read 24% (11/45) until it was measured against the table's own basis.**
Eleven tales carry M–N only if 136 is among them, and 136's sole M–N is in move IV, the move this table declares held out.
Excluding it, as the per-move column already does, gives ten tales.
The `both` row is the proof: 136 IV carries H–I *and* M–N, so a per-tale column that counted it could not read 0%.
H–I is unaffected at 21 either way, 136 III carrying it too.

**Both branches come in under Propp's rates, M–N far more sharply than H–I**: 12% against his 33%, versus 30% against his 41%.
*Both* is absent entirely.

**Both discrepancies have the same cause, and it is not sampling: Appendix III systematically under-represents the task branch.**
Its shared H/M and I/N columns cannot print a move using both branches, so Propp excluded tale 123 outright and relegated tale 136's fourth move to prose.
A table that cannot print a structure will under-count the tales that use it.

**Propp's 41/33/3 comes from his analysis of 100 tales; his printed table is a lossier record.**
This is worth stating plainly, because it is a caution for anyone comparing corpora at this granularity.
The instrument shaped the sample.
Comparative work should use his rates, not the table's.

**The typography is the argument.**
Propp did not merely observe that tales use one or the other; his table *cannot represent* a move using both, and he found only three such moves in a hundred tales.
The alternation is structural, not incidental.

## The opening

### `initialSituation`

- **Symbols:** α
- **From Propp:** p.25: not a function, but an important element of form: the members of the family are introduced, or the hero is introduced by name or status.
- **Measured:** in stories, as coded by the transcribers, who most often leave α unmarked: wondertales 2% and 2%; animal tales 0% and 2%; fables 2% and 3%; tragedies 19% and 19%; myths 9% and 11%. These figures say how often α was coded, not how often a tale opens with one.
- **Literal meaning:** Who is there at the start.
  The family and its circumstances are set out before anything happens.
- **Social lesson:** Know what a good household looks like, with order, plenty and each member in place, and do not take it for granted.
- **Cultural meaning:** The initial situation often describes a state of prosperity, with peace, abundance and harmony. It sets the community's ideal baseline, and implies what a working household should look like. But the peace is fragile, and the opening signals without comment that calm also holds vulnerability.

### `preparatorySection`

- **Symbols:** β γ δ ε ζ η [λ] θ
- **From Propp:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Measured:** its pairs are measured in their own entries below.
- **Literal meaning:** What makes the misfortune possible.
  The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived.
  Propp calls the first seven functions the preparatory part (p.30).
- **Social lesson:** Heed warnings, guard the household, and beware of strangers' words. Carelessness at home invites disaster.
- **Cultural meaning:** The end of safety at home.
  The opening shows that the young must leave home sooner or later.
  The safety of home is fragile and does not last, and innocence falls to the deceptions of the wider world.
  The opening is a threshold: it ends the safety of childhood, sometimes violently, and pushes the young person into the trials of growing up.
- **In v46, `preparatorySection`** (from `SemanticCatalog46.md`):
  - **Kind:** group of groups. **Level:** tale, before the first move only.
  - **Holds:** β, then the pairs γ–δ, ε–ζ and η–λ–θ.
  - **Warrant:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
  - **Name:** Propp's. **Corpus:** 0, since the appendix prints none. **Tree test:** `β γ δ A`, the β under `preparatorySection`.
  - **EBNF:** `preparatorySection = {absentation} RuleViolation InformationGathering DeceptionTrap`

### `absentation`

- **Symbols:** β
- **From Propp:** p.26: one of the family leaves home, or dies; the one preparatory function outside every pair.
- **Measured:** in stories, wondertales 38% and 22%; animal tales 20% and 8%; fables 1% and 1%; tragedies 75% and 75%; myths 6% and 5%. Tragedy opens with an absence, a death or a departure, in three plays of four.
- **Literal meaning:** The protectors leave.
  Whether they go out or die, the household is left unguarded, and that opens the way for the misfortune.
- **Social lesson:** When the protectors are gone, the young must guard themselves and the household. Responsibility passes to the next generation sooner than it expects.
- **Cultural meaning:** The end of childhood shelter.
  The elders' leaving or death can be read as the first stage of a rite of passage.
  It exposes the young to the world, sometimes violently, and forces them out of dependence, so that they can in time cross into the wild, where the trials of growing up take place.

### `InterdictionAndViolation`

- **Symbols:** γ δ
- **From Propp:** p.26 and p.27: an interdiction is addressed to the hero, and it is violated; "Functions II and III form a paired element" (p.27).
- **Measured:** γ δ 6.6 and 4.6; acts forbid, disobey 6.8 and 4.5.
- **Literal meaning:** A rule given and broken.
  This is the breach through which misfortune enters.
  When the elders' leaving is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.
- **Social lesson:** Obey the prohibitions of your elders. Breaking a rule brings misfortune on you and on those close to you.
- **Cultural meaning:** The broken rule that starts the story.
  In the tale, the prohibition is there to be broken.
  Breaking it harms the one who breaks it and ends the false safety of childhood.
  It brings danger at once, but it is also what moves the young person out of standing still and into a life of his own.
- **In v46, `RuleViolation`** (from `SemanticCatalog46.md`):
  - **Kind:** pair. **Level:** tale.
  - **Holds:** γ then δ. An absentation β told after the interdiction nests inside the pair.
  - **Warrant:** p.80 writes γ-δ as a pair; p.64 lists prohibition-violation. The β inside it follows tale 113 (pp.96-97) and the wolf and the kids (p.101), both told interdiction first.
  - **Name:** v43's, restored; this grammar's `interdictionViolation` before, from Propp's terms. **Corpus:** 0. **Tree test:** `γ β δ A`, the β under `RuleViolation`.
  - **EBNF:** `RuleViolation = [ interdiction {interdiction} {absentation} ] {violation}`
- **Semantic bundle** (from `SemanticBundling.md`, γ–δ · interdiction and violation):
  *Propp: II–III, pp.26–27.*
  **Bundle:** a prohibition issued, then broken.
  **Value:** **the narrative requires transgression.**
  Nothing happens unless the rule is broken, which is an unusually candid structural admission that order alone generates no story.
  *Untestable from Appendix III: preparatory functions are omitted from every scheme for lack of space (p.116).*

### `ReconnaissanceAndDelivery`

- **Symbols:** ε ζ
- **From Propp:** p.28 and p.29: the villain tries to learn something about the victim, and receives it; "Once again we are confronted with paired functions" (p.29).
- **Measured:** ε ζ 7.4 and 10.0; acts seek-information, reveal-information 4.4 and 3.9.
- **Literal meaning:** The villain asks for information and gets it.
  The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Social lesson:** Guard your tongue and your household's secrets. Do not tell a stranger what he asks about you or yours.
- **Cultural meaning:** Secrets do not remain secret.
  No household can keep its weak points hidden for ever.
  The household gives the villain what he wants because it is innocent and cannot imagine his intent.
  How easily he learns it shows a rule of the tale: hidden weaknesses come out, and the young person's weak points must be exposed to the world before the journey can begin.
- **In v46, `InformationGathering`** (from `SemanticCatalog46.md`):
  - **Kind:** pair. **Level:** tale.
  - **Holds:** ε then ζ.
  - **Warrant:** p.80 writes ε-ζ as a pair; p.64 lists reconnaissance-delivery.
  - **Name:** v43's, restored; this grammar's `reconnaissanceDelivery` before, from Propp's terms. **Corpus:** 0. **Tree test:** `ε ζ A`, the ζ under `InformationGathering`.
  - **EBNF:** `InformationGathering = {reconnaissance} {delivery}`

### `TrickeryAndComplicity`

- **Symbols:** η [λ] θ
- **From Propp:** p.29 and p.30: the villain tries to deceive the victim, and the victim is taken in; λ, a preliminary misfortune, can stand between them.
- **Measured:** η θ 4.0 and 5.2; acts deceive, be-taken-in 6.3 and 6.0. Then the harm: θ A 1.7 and 1.9; acts be-taken-in, harm 2.5 and 2.8, and deceive, harm two places apart 1.3 and 1.4, the trick's success between them.
- **Literal meaning:** The villain deceives, and the victim gives in.
  The preliminary misfortune is what forces the victim to agree.
- **Social lesson:** Do not trust appearances or flattering offers. Look past the disguise before you agree to anything.
- **Cultural meaning:** Good judgment often fails.
  A child's instinct is no match for deliberate malice.
  The villain's disguise shows that danger often looks like a harmless part of home life.
  When a preliminary misfortune forces the victim to agree, the tale shows that instinct alone cannot protect the inexperienced: the victim's own will gives way, and the hero's journey grows out of the wreckage.
- **In v46, `DeceptionTrap`** (from `SemanticCatalog46.md`):
  - **Kind:** pair, with λ inside it. **Level:** tale.
  - **Holds:** η, then λ, then θ.
  - **Warrant:** p.80 writes η-θ as a pair; λ is placed by Appendix I Table II item 44, which confines the preliminary misfortune to the deceptive agreement.
  - **Name:** v43's, restored; this grammar's `trickeryComplicity` before, from Propp's terms. **Corpus:** 0. **Tree test:** `η λ θ A`, the λ under `DeceptionTrap`.
  - **EBNF:** `DeceptionTrap = {trickery} {preliminaryMisfortune} {complicity}`

## Groups and pairs within a move

### `complication`

- **Symbols:** (A or a) B C ↑
- **From Propp:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
- **Links:** A or a to K; ↑ to ↓.
- **Measured:** its steps follow each other: A B 2.0 and 1.6; B C 5.6 and 3.8; C ↑ 4.5 and 4.9; B ↑ two to four apart 1.7 and 2.1.
- **Literal meaning:** The misfortune made known, and the hero setting out.
  Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Social lesson:** When harm comes to your people, answer the call. The one who acts, not the one who waits, becomes the hero.
- **Cultural meaning:** The community calls one of its own to act.
  The complication draws a young person out of the home to answer a need of the community.
  Going from seeing the misfortune to crossing the threshold shows that private peace cannot last while a public harm goes unanswered.
  The traveler may pick up unearned help along the road: setting out seems by itself to bring support from forebears and the natural world, and it turns a victim who stays put into someone who acts to set things right.
- **In v46, `complication`** (from `SemanticCatalog46.md`):
  - **Kind:** group. **Level:** move.
  - **Holds:** the opener, dispatch B, counteraction C and departure ↑, and an untested agent on either side of the departure.
  - **Warrant:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
  - **Name:** Propp's. **Corpus:** 80. **Tree test:** `A B C up`, both B and ↑ under `complication`.
  - **EBNF:** `complication = MoveTrigger Digression {mediation Digression} {beginningCounteraction Digression} [UntestedAcquisition] [ departure Digression {departure Digression} [UntestedAcquisition] ]`
- **Semantic bundle** (from `SemanticBundling.md`, ABC↑ · the complication):
  *Propp, p.64–65, his own grouping and his own name for it.*
  **Bundle:** harm occurs (A), it becomes known (B), someone assumes responsibility (C), and departs (↑).
  **Value:** **misfortune becomes a social matter through mediation, and where counteraction is consented to, the consent falls between the call and the departure.**
  The `C` function, "the seeker agrees to or decides upon counteraction", fixes the position of the hero's volition, not its occurrence.
  He is not merely dispatched; where he assents, he assents there.
  **Corpus:** the order holds 60/60.
  Presence does not: 33/37 unqualified, and 28/34 under Propp's own seeker-hero restriction at pp.37–38, which makes the claim more falsified rather than less.
  `ConsentResult.md` reports the run.

  **This is the most culturally loaded of the groups, and the least remarked on.**
  A tradition that gives *consent* a fixed place between the call and the departure, without requiring it to occur, is encoding something about agency.
  The claim stands on the position, which is exceptionless, rather than on the occurrence, which is not.
  The cited pages support exactly this.
  Propp's p.64–65 grouping is a statement about which functions cluster and in what order; it asserts no obligation, and the earlier wording here attached one to it.

### `TestAndReaction`

- **Symbols:** D E
- **From Propp:** p.39 and p.42: the hero is tested, questioned or attacked by one who may then help, and reacts.
- **Links:** D and E to F.
- **Measured:** D E 6.8 and 5.9, and D E− 5.3 and 5.6; acts test, respond 4.7 and 5.3. E F was not confirmed within four places.
- **Literal meaning:** Someone tests the hero, and the hero answers.
  The answer, kind or unkind, decides whether help will follow.
  The sequence opens on the test, or straight on the hero's response when the test is left out.
- **Social lesson:** Treat strangers, the old and the weak with courtesy and respect. How you answer a test shows what you are.
- **Cultural meaning:** Showing that one knows the ways of one's culture.
  This is not a loose lesson in kindness or fair dealing; it is a strict test of readiness.
  Passing it shows that the young person has the manners, the respect for elders, or the quick wits needed to survive away from home.
- **In v46, `TestedAcquisition`** (from `SemanticCatalog46.md`):
  - **Kind:** group. **Level:** move.
  - **Holds:** the donor's test D, the hero's reaction E, and the agent F they earn.
  - **Warrant:** p.65: DEF "also form something of a whole".
  - **Name:** v43's; before step 6, Vetting. **Corpus:** 32. **Tree test:** `A D E F`, the F under `TestedAcquisition` and not under `UntestedAcquisition`.
  - **EBNF:** `TestedAcquisition = firstDonorFunction Digression {firstDonorFunction Digression} {heroReaction Digression} {receiptOfMagicalAgent Digression} | heroReaction Digression {heroReaction Digression} {receiptOfMagicalAgent Digression}`
  - **Measured:** Counted by `agentForms.py` and pinned by a test. 35 cells in 28 moves: transferred 8, offers service 7, pointed out 4, seized 3, appears 3, found 2, prepared 1, bought 1, and 6 with no form marked. Every seizure in the corpus falls here, 3 of 3, and 7 of the 8 offers of service.
- **Semantic bundle** (from `SemanticBundling.md`, DEF · the donor sequence):
  *Propp, p.64–65: "Elements DEF also form something of a whole."*
  **Bundle:** a stranger tests (D), the hero responds (E), and receives or fails to receive an agent (F).
  **Value:** **conduct toward a stranger determines aid.**
  The magical agent is not seized or earned by strength.
  It is *given*, conditionally, in response to how the hero behaves toward an unknown party.
  And Propp's notation carries the negative case: `E₋` and `F₋`, a bad reaction and no agent.

  **This is a reciprocity norm with a sanction attached, encoded in the notation itself.**
  Tales 93 and 98 in the corpus show both outcomes side by side: the brothers react badly and get nothing; the hero reacts well and is equipped.

  ---

### `receiptOfMagicalAgent`

- **Symbols:** F
- **From Propp:** p.43: the hero acquires the use of a magical agent.
- **Links:** D and E to F.
- **Measured:** in stories, Propp 64%; wondertales 78% and 91%; animal tales 44% and 40%; fables 18% and 16%; tragedies 84% and 97%; myths 35% and 43%. F− is the commonest negative form in every genre but the myths.
- **Literal meaning:** The means to undo the misfortune.
  Earned from a donor, it is a reward; received with no test, from a father or by finding it, it comes with the setting out.
- **Social lesson:** Help comes to those who have earned it. Repay kindness, and honor what you owe to those who equip you.
- **Cultural meaning:** The hero earns the help he seeks.
  Those who behave rightly are equipped by others, and what was promised in return is paid. The agent may be a reward for honoring the duty to give in return, or it may be taken by a trick from a hostile donor.
  Either way, power does not come at random: it goes to those who have learned the rules of their world.

### `spatialTransference`

- **Symbols:** G
- **From Propp:** p.50: the hero is transferred, delivered or led to where the object of the search is.
- **Measured:** E G 4.0 and 3.8. In stories, Propp 36%; wondertales 29% and 40%; animal tales 4% and 4%; fables 1% and 1%; tragedies 50% and 41%; myths 11% and 28%.
- **Literal meaning:** The passage to the other kingdom.
  It is where the misfortune can be undone.
- **Social lesson:** Be willing to go beyond the familiar, and accept guidance. The answer may lie far from home.
- **Cultural meaning:** This function can be read as a crossing, in mind and in place, into a world away from home. It tells the listener that the answers to the deepest troubles lie beyond ordinary boundaries. When the passage relies on a magical agent or an animal, it suggests a new alignment with nature or the divine.

### `StruggleAndVictory`

- **Symbols:** H I

- **From Propp:** p.51 and p.53: the hero and the villain join in direct combat, and the villain is defeated; struggle and victory are among the pairs Propp names (p.64).

- **Links:** H to I.

- **Measured:** H I 5.8 and 5.8, and still above chance six places apart; acts fight, win 9.1 and 7.0.

- **Literal meaning:** The fight and the victory.
  The hero fights the enemy, in combat or in a contest, is often marked, and wins.
  The mark won here is what lets the hero be recognized later.

- **Social lesson:** Stand and fight when the threat is real. Courage in the face of danger earns standing.

- **Cultural meaning:** This sequence is a direct, high-stakes confrontation with a real threat, and it is the fight that makes a ruler.
  The fight changes the young person for good, as it ends the passive child. Victory means something because the danger was real, and it gives the hero moral and physical standing.

  It can also be read as saying that justice must be fought for.
- **In v46, `StruggleAndOutcome`** (from `SemanticCatalog46.md`):
  - **Kind:** group, around the pair H–I. **Level:** move.
  - **Holds:** struggle H, branding J and victory I.
  - **Warrant:** p.104, the struggle scheme H J I; p.64 lists struggle-victory as a pair.
  - **Name:** this grammar's; `Combat` before. **Corpus:** 32. **Tree test:** `A H J I K`, the J under `StruggleAndOutcome`.
  - **EBNF:** `StruggleAndOutcome = {struggle Digression} {branding Digression} {victory Digression}`; (or conditional `+tragedy` `StruggleAndOutcome = {struggle Digression} {branding Digression} StruggleOutcome`
- **Semantic bundle** (from `SemanticBundling.md`, H–I · struggle and victory):
  *Propp: XVI, XVIII, pp.51–53; p.109 on variety linkage.*
  **Bundle:** direct confrontation, resolved by defeat of the opponent.
  **Value:** worth proven by force, and crucially the mode of victory must match the mode of struggle (H¹→I¹, never H¹→I⁸).
  A fight is answered by winning a fight.
  The culture does not permit a hero to enter a contest of one kind and prevail by another.
  **Corpus:** 25 occurrences, never unpaired, varieties matching 25/25.

### `branding`

- **Symbols:** J
- **From Propp:** p.52: the hero is branded, wounded or given a token.
- **Links:** J to Q.
- **Measured:** in stories, Propp 7%; wondertales 9% and 11%; animal tales 0% and 0%; fables 1% and 0%; tragedies 19% and 16%; myths 1% and 3%.
- **Literal meaning:** The sign by which the hero will be known.
  It is rare in the corpus but central to the end, since it is what the recognition reads.
- **Social lesson:** Honorable scars are proof of service. Carry the marks of the struggle without shame; they will speak for you.
- **Cultural meaning:** The mark is lasting proof that the hero went into the wild or the underworld and came back, and is what lets the hero be recognized later.
  Because the mark comes with the victory, the tale suggests that the right to lead and protect belongs to those who carry the scars of the struggle. The mark shows that the struggle has changed the hero for good.
- **Semantic bundle:** see the link "J to Q".

### `liquidation`

- **Symbols:** K
- **From Propp:** p.53: the initial misfortune or lack is liquidated; "This function, together with villainy (A), constitutes a pair. The narrative reaches its peak in this function" (p.53).
- **Links:** A or a to K.
- **Measured:** A K and a K were not confirmed within four places, their halves standing far apart; at any distance, see the link "A or a to K". In the acts (`Problems/`), tales repair nearly all their problems and tragedies far fewer than their length gives.
- **Literal meaning:** The misfortune undone.
  It is the point every move is heading for.
- **Social lesson:** A wrong can and should be set right. Persevere until what was lost is restored.
- **Cultural meaning:** This function sets right what was wrong and restores what was lost. It can be read as the healing of the tale's world, and as the assurance that suffering has an end. Propp calls it the tale's peak (p.53).
- **Semantic bundle** (from `SemanticBundling.md`, A–K · villainy and liquidation):
  *Propp: VIII, XIX, pp.30, 53.
  "This function, together with villainy (A), constitutes a pair."*
  **Bundle:** disruption of order, and its repair.
  **Value:** **equilibrium is recoverable.**
  Propp names stable correspondences, murder answered by resuscitation and enchantment by the breaking of a spell (p.109), so the repair must be *of the same kind* as the harm.
  **Corpus:** the correspondences Propp names hold 4/4 where testable; for 28 of the 49 co-occurrences he supplies no mapping at all.
  That read 58% until `akScan.py` was built.
  The figures were then corrected and the percentage withdrawn, because it rested on a 30 and a 52 that do not reproduce; `AKResult.md` reports the run.

### `return`

- **Symbols:** ↓
- **From Propp:** p.55: the hero returns.
- **Links:** ↑ to ↓.
- **Measured:** in stories, Propp 71%; wondertales 71% and 71%; animal tales 32% and 16%; fables 4% and 3%; tragedies 59% and 44%; myths 17% and 10%. At any distance from departure, see the link "↑ to ↓".
- **Literal meaning:** The way home.
  It opens the second half of the move.
- **Social lesson:** Bring home what you gained. A success counts when it serves the people you return to.
- **Cultural meaning:** A journey matters to the community only if the traveler brings back what was gained. The return begins the hero's acceptance in a new, higher standing. The hero comes home with something of value, wisdom, a cure, or a rescued member of the family, and puts what he has become in the service of his people.

### `PursuitAndRescue`

- **Symbols:** Pr Rs
- **From Propp:** p.56 and p.57: the hero is pursued, and rescued from pursuit; pursuit and deliverance are among the pairs Propp names (p.64).
- **Links:** Pr to Rs.
- **Measured:** as an adjacent pair, Pr Rs was too rare to confirm, and acts pursue, escape were not confirmed; at any distance in the move, Pr is followed by Rs in most tale moves (the link "Pr to Rs"). The two measures differ because the rescue often comes several functions after the pursuit.
- **Literal meaning:** Escaping capture on the way home.
  It allows the two orders found in the corpus: a pursuit that a rescue answers, or a rescue that comes first and heads off the pursuit.
- **Social lesson:** Victory invites revenge. Stay watchful after success, and accept help to escape danger.
- **Cultural meaning:** Closing the border between the wild and home.
  The two paths show that getting past a backlash takes adaptability more than strength.
  The hero survives by hiding, by changing shape, and by the help others give, not by fighting.
  Growing up means knowing when to face an enemy and when to slip out of reach of past danger.
- **In v46, `Evasion`** (from `SemanticCatalog46.md`):
  - **Kind:** choice between two orders of a pair. **Level:** move.
  - **Holds:** pursuit and rescue, in either order.
  - **Warrant:** p.64 lists pursuit-deliverance as a pair; p.147 gives the inverted order.
  - **Name:** v43's. **Corpus:** 14. **Tree test:** `A K down Pr Rs`, the Rs under `Evasion`.
  - **EBNF:** `Evasion = [ PursuitFirst | RescueFirst ]`
- **Semantic bundle** (from `SemanticBundling.md`, Pr–Rs · pursuit and rescue):
  *Propp: XXI–XXII, pp.56–58; named a pair p.64.*
  **Bundle:** the threat persists past the victory; deliverance is separate from winning.
  **Value:** **success is not final until the return is secured.**
  Achievement and its retention are distinct accomplishments.
  **Corpus:** 15 occurrences, never unpaired.

### `unrecognizedArrival`

- **Symbols:** o
- **From Propp:** p.60: the hero, unrecognized, arrives home or in another country.
- **Measured:** in stories, Propp 13%; wondertales 22% and 22%; animal tales 0% and 0%; fables 1% and 1%; tragedies 25% and 25%; myths 4% and 1%.
- **Literal meaning:** The hero without his due.
  Present, but not known.
- **Social lesson:** Worth does not depend on fine clothes or rank. Humility and patience come before recognition.
- **Cultural meaning:** The unrecognized arrival can be read as the difficulty of coming home changed. The hero cannot walk through the gates expecting to be acclaimed; the community still sees the weak child, the outcast, or the victim who left. Disguise or anonymity protects the hero while he watches how home runs without him. It tells the listener that true merit cannot stay hidden for ever.

### `unfoundedClaims`

- **Symbols:** L
- **From Propp:** p.60: a false hero presents unfounded claims.
- **Links:** L to Ex.
- **Measured:** in stories, Propp 11%; wondertales 13% and 16%; animal tales 6% and 2%; fables 10% and 4%; tragedies 12% and 6%; myths 2% and 4%.
- **Literal meaning:** The hero's deed stolen.
  The end of the tale must set it right.
- **Social lesson:** Do not claim credit for another's deeds. Boasting and lying to take a reward are among the worst of wrongs.
- **Cultural meaning:** This function shows how easily deception can win over merit for a time. It voices the fear that the court will reward the boaster and pass over the one who did the deed, and it cautions against trusting the claimant who talks best. In the tale, the one who did the work is rarely the one who speaks up for himself, while the one who seeks reward unearned is skilled at appearances; the end of the tale puts this right.

### `TaskAndSolution`

- **Symbols:** M N
- **From Propp:** p.60 and p.62: a difficult task is proposed to the hero, and it is resolved.
- **Links:** M to N.
- **Measured:** M N 8.9 and 9.1, falling steadily with distance (9.0, 4.9, 3.4, 2.7 at one to four apart); acts set-task, do-task 4.6 and 6.3.
- **Literal meaning:** A hard task, set and done.
  The candidate faces a very hard trial and succeeds.
  The task does at court what the fight does in the wild: it checks the claimant's deeds.
- **Social lesson:** Accept hard challenges, and prove yourself by deeds before those who judge.
- **Cultural meaning:** This structural pair is a fair test of real ability.
  The tale treats the task as the equal of a battle, because leadership means living by the culture's basic rules. By carrying out the task, the hero shows the elders that he has made the rules and values of his culture his own.
  That strips away the false hero's empty talk and makes the true hero's right to rule plain to all.
- **In v46, `TaskAndSolution`** (from `SemanticCatalog46.md`):
  - **Kind:** group, around the pair M–N. **Level:** move.
  - **Holds:** difficult task M, branding J and solution N. The J comes only after a task.
  - **Warrant:** p.104, the task scheme M J N, set in the place H J I holds in the other scheme. The J only after M is the repair v44's own comment names, made at step 5.
  - **Name:** this grammar's; v43's `TaskCycle` before. **Corpus:** 9. **Tree test:** `A K M J N`, the J under `TaskAndSolution` and not under `StruggleAndOutcome`.
  - **EBNF:** `TaskAndSolution = [ difficultTask Digression {difficultTask Digression} {branding Digression} ] {solution Digression}`
- **Semantic bundle** (from `SemanticBundling.md`, M–N · difficult task and solution):
  *Propp: XXV–XXVI, pp.60–62; named as a pair p.102.*
  **Bundle:** a demand is set by another party, and met.
  **Value:** worth is demonstrated by capability, and it is adjudicated by someone else.
  The task-setter defines what success looks like; the hero does not define it for himself.
  This is a social validation of competence.
  **Corpus:** 10 occurrences, never unpaired.

## The denouement

### `denouement`

- **Symbols:** Q Ex T U W*
- **From Propp:** p.92: a tale runs from villainy or lack to the wedding, or to other functions employed as a denouement; the denouement is whatever ends the move, in the full scheme this run, in a shorter move K, Rs or a reward.
- **Measured:** its parts are measured in their own entries.
- **Literal meaning:** The final settling of accounts.
  The true hero is recognized, the false one is exposed and punished, and the hero marries and comes to power.
  These may come in any order.
- **Social lesson:** In the end the truth prevails: the good are rewarded, the wicked punished, and order is restored. Live so that the settling of accounts will favor you.
- **Cultural meaning:** The social order put back together.
  The endgame ends the illusions and steadies the community.
  Recognition and exposure together clear out the false and put the truth back at the top of the kingdom.
  The wedding and the hero's rise close the cycle: a sound family stands again at the head of the people, ready for the next generation of heroes.
- **In v46, `Endgame`** (from `SemanticCatalog46.md`):
  - **Kind:** group of four functions that may come in any order. **Level:** move.
  - **Holds:** recognition Q, exposure Ex, punishment U and wedding W, in any order.
  - **Warrant:** p.108: "Recognition and exposure, marriage and punishment may also exchange positions", read as letting all four change places among themselves.
  - **Name:** v44's word for the span. **Corpus:** 38. **Tree test:** `A K U Q W`, both U and Q under `Endgame`.
  - **EBNF:** `Endgame = { ( recognition | exposure | punishment | wedding ) Digression }`
- **Semantic bundle** (from `SemanticBundling.md`, Ex, U · exposure and punishment):
  *Propp: XXVIII, XXX, pp.62, 63.*
  **Bundle:** the false claimant unmasked, then penalized.
  **Value:** **deception does not hold, and the community enacts the consequence.**
  Exposure precedes punishment: the truth must be made public before it is acted on.

### `RecognitionAndExposure`

- **Symbols:** Q Ex
- **From Propp:** p.62: "The hero is recognized" (XXVII, Q), by a mark or brand, by a thing given him, by the accomplishment of a difficult task, or after a long separation; "The false hero or villain is exposed" (XXVIII, Ex), a function "in most cases, connected with the one preceding."
- **Links:** J to Q; L to Ex.
- **Measured:** Q Ex was too rare to test.
- **Literal meaning:** The truth comes out.
  The true hero is known for who he is, and the one who lied is shown up.
- **Social lesson:** Do not lie or bear false witness. The truth will come out, and the liar will be exposed and punished.
- **Cultural meaning:** This structural pair answers a wish for justice made plain. In everyday life, bad behavior often goes unnoticed and good deeds go unrewarded; in the tale, the truth comes out in the end, the deserving are seen for what they are, and the false lose what they took.

### `transfiguration`

- **Symbols:** T
- **From Propp:** pp.62-63: the hero is given a new appearance.
- **Measured:** in stories, Propp 16%; wondertales 9% and 9%; animal tales 0% and 0%; fables 2% and 1%; tragedies 3% and 3%; myths 1% and 4%.
- **Literal meaning:** The hero's new standing made visible.
  Its free place is itself a finding: it is the one function whose position means nothing.
- **Social lesson:** Be worthy, and in time your worth will show. Outward standing follows inner merit.
- **Cultural meaning:** It can be read as saying that a change won through struggle will show in the end: the hero's outward life comes to match his inner worth.

### `punishment`

- **Symbols:** U
- **From Propp:** p.63: the villain is punished; "in parallel with this we sometimes have a magnanimous pardon (U neg.)."
- **Measured:** in stories, Propp 27%; wondertales 40% and 27%; animal tales 10% and 6%; fables 8% and 7%; tragedies 59% and 38%; myths 23% and 34%.
- **Literal meaning:** The wrong answered, or, in a pardon, forgiven.
- **Social lesson:** Wrongdoing will be punished. Justice is owed to the community, and no one is above it.
- **Cultural meaning:** For the tale's world to be at peace again, the source of the harm must be removed. Punishment holds up accountability and limits, and the rules that keep the community safe.

### `wedding`

- **Symbols:** W*
- **From Propp:** p.63: the hero is married and ascends the throne.
- **Measured:** in stories, Propp 58%; wondertales 82% and 80%; animal tales 6% and 2%; fables 2% and 2%; tragedies 62% and 44%; myths 30% and 33%.
- **Literal meaning:** The hero given his due.
  It is the most common close of a move, and the ending p.92 names first.
- **Social lesson:** The reward of proven merit is marriage and an honored place. Found a household and carry the line forward.
- **Cultural meaning:** This is a sign of continuity and renewal. A wedding promises the next generation, and an accession promises a stable rule.

## Characters: Propp's spheres of action

**Propp joins the functions into seven spheres of action, each the part a character plays** (pp.79-80): "the tale evidences seven dramatis personae." A sphere and a character need not coincide: a sphere may correspond exactly to one character, one character may hold several spheres, or one sphere may be shared among several characters (p.80). The functions of the preparatory section are spread over the same characters (p.80).
Measured for the spheres together (`Spheres/explore.py`, exploratory, not a frozen test; each function credited to the character who performs it): all seven spheres occur in every genre. One character holds both the hero's and the villain's sphere in 22% and 24% of the wondertales, 4% and 3% of the fables, 66% and 72% of the tragedies, and 27% and 26% of the myths (the strict reading, struggle left out of the villain's sphere; fields naming several characters split, and names joined only by a shared head noun, a title or an "of" phrase, 2026-10-26). A first look at the relations recorded for the acts in each sphere's events (2026-10-21, exploratory) finds villain events mostly enemy (41%), donor events mostly stranger (37%, ally 17%), and the most stated rank in the dispatcher's (above and below together 21%, kin 20%).

**From `SemanticCatalog46.md`, its introduction to the dramatis personae, unchanged:**

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

The entries follow the order of social rank set out in the paragraph from `SemanticCatalog46.md` above, the hero first and the villain last; the frozen test `catalogspheres` (`StepTests.txt`, step 10) checks that order.

### `hero`

- **Symbols:** C ↑ E W*
- **From Propp:** p.80: departure on a search, reaction to the demands of the donor, wedding; departure is characteristic of the seeker-hero, and the victim-hero performs only the rest.
- **Measured:** see above.
- **Social lesson:** Be the one who goes out, behaves well, and earns success. The humble and the overlooked may rise.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** M J Ex Q U W
- **From Propp:** pp.79-80: the assignment of difficult tasks, branding, exposure, recognition, punishment of a second villain, marriage; the princess and her father cannot be exactly told apart by functions, and most often it is the father who sets the tasks, from hostility to the suitor, and who punishes the false hero.
- **Measured:** see above.
- **Social lesson:** Those in power must test claimants fairly, reward true merit, and punish impostors. The hand of the princess goes to the deserving, not the boastful.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** B
- **From Propp:** p.80: dispatch, the connective incident.
- **Measured:** see above; the sphere with the most stated rank and kinship.
- **Social lesson:** Those in authority should call on the able to serve the community, and the able should answer when called.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** D F
- **From Propp:** p.79: the preparation for the transmission of a magical agent, and the provision of the hero with it.
- **Measured:** see above; donor events are mostly between strangers, before the gift.
- **Social lesson:** Those older or stranger than you may be testing you; meet them well. Those who have the means should reward the worthy generously.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** G K Rs N T
- **From Propp:** p.79: spatial transference of the hero, liquidation of misfortune or lack, rescue from pursuit, the solution of difficult tasks, transfiguration of the hero.
- **Measured:** see above.
- **Social lesson:** No one succeeds alone. Loyal help is the duty of friends and allies, and it is given to those who deserve it.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** C ↑ E L
- **From Propp:** p.80: departure on a search, followed by the reaction to the donor and, as his own function, unfounded claims.
- **Measured:** see above; rare in every genre (2% to 16% of stories), commonest in the wondertales.
- **Social lesson:** Do not pretend to be what you are not. The impostor is exposed and falls lowest of all.
- **From `SemanticCatalog46.md`:**
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

- **Symbols:** A H Pr
- **From Propp:** p.79: villainy, a fight or other struggle with the hero, pursuit.
- **Measured:** see above.
- **Social lesson:** Do not harm, steal or deceive. Whoever does becomes the enemy and will be defeated.
- **From `SemanticCatalog46.md`:**
  - **Propp's sphere:** 1, p.79. **Functions:** `villainy` (A), `struggle` (H), `pursuit` (Pr).
  - **Acts in:** `MoveTrigger`, `StruggleAndOutcome` and `LateStruggle`, `Evasion`. **Corpus:** 62.
  - **From Propp:** the villain's sphere is villainy, struggle and pursuit (A, H, Pr; p.79), and it does not include punishment. Punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and Propp adds that the father "frequently punishes (or orders punished) the false hero" (pp.79-80). So the first villain is met by the hero in combat and beaten; the liar inside the order is judged by its head.
  - **Measured:** Counted by `villainy.py` and pinned by a test. Of the 84 moves, 55 open on villainy and 28 on lack. In the villainy moves the harm is undone (K) in 65%, the villain is fought (H) in 35% and defeated (I) in 42%, he pursues (Pr) in 20%, and punishment (U) stands in 20%; lack moves run lower on combat, 21% struggle and 36% victory. The tale's business with the villain is undoing the harm, and his own end is often not marked. U does not say who is punished, and a dragon killed in combat is a victory, not a punishment.
  - **Place in the social order:** *Draft.* Lowest. Despised: the enemy of the order.
  - **Literal meaning:** The one who does harm, fights the hero, and gives chase.
  - **Cultural meaning:** *Draft.* Evil to be opposed.
    The listener is meant to cheer the villain's defeat.
    When the villain is inside the family, a stepmother or envious sisters, the tale shows where the household order can fail.

## Elements that are not functions

**Propp names elements of form that are not functions of the dramatis personae** (chapters IV, V, VII and VIII). They are not coded as functions in this project's transcriptions; where the transcribers met them, they mostly coded X.

### `assimilation`

- **From Propp:** ch. IV, p.66: cases where one act has the double morphological meaning of two functions, and is read by its consequences.
- **Measured:** not measured.
- **Literal meaning:** One act doing the work of two.
- **Social lesson:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `connective`

- **From Propp:** ch. V A, p.71: auxiliary elements that tie functions together, such as the information that passes between characters; the dispatch is the connective incident (p.36).
- **Measured:** not measured as such; part of the events coded X.
- **Literal meaning:** How one function leads to the next.
- **Social lesson:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `trebling`

- **From Propp:** ch. V B, p.74: the repetition of a function or a sequence three times, with its own auxiliary elements.
- **Measured:** not measured.
- **Literal meaning:** The same thing done three times.
- **Social lesson:** Persevere: success often comes on the third attempt, and the youngest of three, or the third to try, is the one who succeeds.
- **Cultural meaning:** See the variable scheme above, and Dundes on the number three.

### `motivation`

- **From Propp:** ch. V C, p.75: the reasons and aims of the characters that cause them to act.
- **Measured:** not measured.
- **Literal meaning:** Why a character acts.
- **Social lesson:** The tale judges acts by their motives: greed, envy and malice lead to villainy, need and loyalty to heroism.
- **Cultural meaning:**

### `entranceOfCharacters`

- **From Propp:** ch. VII, p.85: the ways in which each character is introduced into the course of action.
- **Measured:** not measured.
- **Literal meaning:** How each character comes on stage.
- **Social lesson:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `attributes`

- **From Propp:** ch. VIII: the attributes of the dramatis personae, their appearance, age, sex, situation and the like, which vary while the functions stay.
- **Measured:** not measured.
- **Literal meaning:** What a character is like, apart from what it does.
- **Social lesson:** Do not judge by appearance. The humble, the youngest, or the fool may prove to be the hero.
- **Cultural meaning:**

**From `SemanticCatalog46.md`, the two unnumbered symbols of v46 and the signs of combination, unchanged:**

**Two symbols of v46 are elements Propp names but does not number, so they stand outside the functions above.**

- **`preliminaryMisfortune`, λ.** Appendix I Table II item 44, p.121: a misfortune that forces the victim to agree, within the deceitful bargain. In v46 it stands inside `DeceptionTrap`, between trickery and complicity. **Corpus:** 0.

The six remaining symbols, `/`, `⟨`, `⟩`, `<`, `Y` and `}`, are signs of how moves combine, and their meaning is given under `tale`, `FollowingMoves`, `EmbeddedMove`, `Parting` and `CommonEnding`.

## The functions, one by one

**From `SemanticCatalog46.md`, unchanged.** Where a function has an entry of its own above (absentation, the magical agent, transference, branding, liquidation, return, unrecognized arrival, unfounded claims, transfiguration, punishment, wedding), both stand for now; which to keep is for the owner.

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
- **Meanings:** see the entry `absentation` above.

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
- **Meanings:** see the entry `receiptOfMagicalAgent` above.

### `spatialTransference`

- **Number and sign:** XV, G. **Page:** p.50. **Propp's name:** spatial transference between two kingdoms, guidance.
- **What happens:** the hero is carried, delivered or led to where the object of his search is.
- **Group:** `Development`. **Pairs:** none. **Corpus:** 25.
- **Meanings:** see the entry `spatialTransference` above.

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
- **Meanings:** see the entry `branding` above.

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
- **Meanings:** see the entry `liquidation` above.

### `return`

- **Number and sign:** XX, ↓. **Page:** p.55. **Propp's name:** return.
- **What happens:** the hero returns.
- **Group:** `ReturnJourney`. **Pairs:** none named, though it faces the departure. **Corpus:** 42.
- **Meanings:** see the entry `return` above.

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
- **Meanings:** see the entry `unrecognizedArrival` above.

### `unfoundedClaims`

- **Number and sign:** XXIV, L. **Page:** p.60. **Propp's name:** unfounded claims.
- **What happens:** a false hero claims the hero's deed without right.
- **Group:** `FraudPosture`. **Pairs:** with unrecognized arrival; and it prepares exposure. **Corpus:** 6.
- **Meanings:** see the entry `unfoundedClaims` above.

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
- **Meanings:** see the entry `transfiguration` above.

### `punishment`

- **Number and sign:** XXX, U. **Page:** p.63. **Propp's name:** punishment.
- **What happens:** the villain or the false hero is punished; a generous pardon is its negative form.
- **Group:** `Endgame`. **Pairs:** with wedding, the two changing places (p.108). **Corpus:** 15.
- **From Propp:** punishment belongs to the sphere of the princess and her father, as "punishment of a second villain", and the father often punishes the false hero (pp.79-80). The first villain usually ends by being beaten in combat, victory I, in the hero's sphere of action.
- **Meanings:** see the entry `punishment` above.

### `wedding`

- **Number and sign:** XXXI, W. **Page:** p.63. **Propp's name:** wedding.
- **What happens:** the hero marries and takes the throne; a reward without marriage counts as a form of it.
- **Group:** `Endgame`. **Pairs:** with punishment. **Corpus:** 34.
- **Meanings:** see the entry `wedding` above.

## Devices Propp's list lacks

**Acts and pairs the stories use that Propp's catalog has no place for, each found by a frozen test.**

### `ThreatAndDemand`

- **Symbols:** the act `threaten` and the orders `send`, `forbid`, `set-task` in the act layer; threaten, demand and order in the free verbs.
- **From Propp:** none, not in his list. Found in the X study (`XStudy/`) on the wondertales, the fables and the tragedies, most in tragedy.
- **Links:** not measured.
- **Measured:** the one recurring act in the events Propp's functions leave empty to pass its frozen threshold in every genre (`XStudy/`); 2% to 4.5% of acts, most in tragedy; threats come in exchanges, threat answering threat.
- **Measured, exploratory, 2026-10-21:** of 488 threats in the described stories, the one threatened replies within five acts in three quarters: plead 9%, respond 9%, threaten back 7%, harm 5%, deceive 5%, decide 4%, lose, escape, reveal-information and lament 2% to 3% each; no reply 25%. The act list's `respond` holds both yes and no, so compliance and defiance are to be coded from the free verbs.
- **Structure proposed, 2026-10-21 (owner and keeper):** a group of three, threat or demand, then the answer (comply, defy or evade), then, mostly after defiance, the consequence (the threat carried out or averted), in Dundes's sense of Consequence; defiance can itself be a new threat, which is escalation. The productions wait for the probabilistic story grammar, in `StoryGrammar/Candidates.md`; v46 is left unchanged.
- **Literal meaning:** This structural pair works as a branch that holds the action still. It sets an ultimatum: if the demand is not met, the threat is carried out. It opens a window of time in which the characters must decide to comply or defy.
- **Social lesson:** Do not yield to bullying, but take warnings seriously: a threat ignored may be carried out. Resisting together is safer than giving in alone.
- **Cultural meaning:** This structural pair shows that conflict often begins with words: a warning, a boundary drawn, pressure put on the weaker side, before any blow is struck. The tale can teach the listener to recognize the moment peaceful dealings turn hostile, as when a tyrant's ultimatum reaches a household or a kingdom.

  The sequence shows whether a community holds together under pressure or breaks apart. It can be read as warning that giving in to a tyrant's demand only puts off the harm.

### `RequestAndAnswer`

- **Symbols:** the acts `plead` and `respond` in the act layer, with `send`, `forbid` and `set-task` when the request comes from above; ask, beg, offer, then answer or refuse, in the free verbs.
- **From Propp:** none, not in his list. Found in the frequency analysis (`Ngrams/`), the bottom-up test (`Free/`) and the WordNet grouping (`Group/`), on the wondertales, the fables and the tragedies, and reported in the animal tales.
- **Links:** not measured.
- **Measured:** the commonest pair of acts (plead, respond, 3 to 4.5 times chance; `Ngrams/`), the only structure readers find with no list of acts (ask, beg, offer, then answer or refuse; `Free/`), and the only pairs left when the readers' verbs are grouped by WordNet (`Group/`). In every genre. The structure students of conversation call an adjacency pair.
- **Measured, exploratory, 2026-10-22:** pleas between equals or with no rank recorded, 964, answered by respond 33%, no reply 29%, give 5%; from below, 101, respond 30%, no reply 17%, forbid 10%, give 8%, harm 6%; from above, 33. A request from above is mostly coded as an order (send, forbid, set-task) rather than plead, so the act list already splits requests by status.
- **Structure proposed, 2026-10-22 (the owner):** the request comes from above, between equals or from below, and has three answers, accept, reject or evade, then, sometimes, a consequence; the same shape as the threat group, which may be this group with its sanction stated. Productions in `StoryGrammar/Candidates.md`, waiting for the probabilistic story grammar.
- **Literal meaning:** The structural framework for social transactions and their outcomes.
- **Social lesson:** Answer a request as your place requires: grant what those in need ask, obey a rightful superior, and deal fairly with equals. Refusal and evasion have consequences.
- **Cultural meaning:** The cultural meaning depends on the characters involved, but it ends in cooperation, resistance, or evasion. Cooperation can hold up the ideal of noble clemency, cooperation among equals, or obedience to a superior, outcomes that keep the social order as it stands. Resistance gives a reason for conflict. Evasion looks like delay but can become a defection and lead to conflict.

### `oath`, `prayer`, `curse`

- **Symbols:** the free verbs swear and vow, pray, and curse; in the act layer most fall under `decide`, `plead` and `harm`.
- **From Propp:** none, not in his list. Found in tragedy alone (`Cand/`, the free verbs of the Greek tragedies); not tested in the other genres.
- **Links:** not measured.
- **Measured:** in tragedy's free verbs four to five times their share in the tales, on eight plays never described before (`Cand/`); each in six to eight of the eight plays. Tragedy's own devices: a vow binds the future, a prayer appeals to the gods, a curse calls harm down.
- **Literal meaning:** An oath is a declaration of intent to follow a single course.

  A prayer is a way around the ordinary order, seeking an outside intervention, not from a helper but from a god.

  A curse is a hidden, slow-burning form of villainy, which promises a future lack or punishment.

- **Social lesson:** Keep your word. Humble yourself before the gods. Harm done to the helpless calls down retribution.

- **Cultural meaning:** An oath can be read as putting honor above personal safety. A broken oath can upset the social balance and bring ruin on later generations.

  A prayer can be read as the last appeal of the helpless, and as saying that earthly rank is not final.

  A curse can be read as the victim's voice made lasting: a warning that harm done will have consequences in the future.

## Candidates, not yet tested

**Devices proposed from other scholars' work or from this project's first looks, kept here until a frozen test admits or rejects them.** Their productions, where written, are in `StoryGrammar/Candidates.md`.

### `Consequence`, `AttemptedEscape`, `ExplanatoryMotif`

- **From:** Dundes, The Morphology of North American Indian Folktales (dissertation, 1962; published 1964), whose motifemes otherwise re-cut Propp's pairs and say so: Lack and Lack Liquidated (Propp's a and K), Interdiction and Violation (γ δ), Task and Task Accomplished (M N), Deceit and Deception (η θ). These three are his own: the Consequence of a violation, an optional Attempted Escape from it, and the Explanatory Motif, a closing "that is why" that ends many tales.
- **Measured:** not measured; the Native American corpus is not yet assembled (`ProppQueue.md`).
- **Literal meaning:**
- **Social lesson:** Every violation has its consequence, and escape seldom succeeds. The world is as it is because of what was done in the beginning.
- **Cultural meaning:**

### `RequestGroup` and `ThreatGroup` as one device

- **From:** the owner and the keeper, 2026-10-21 and 22; see `RequestAndAnswer` and `ThreatAndDemand` above. The threat may be a request from above with its sanction stated.
- **Measured:** exploratory only, as given in those entries.

### `failedHero` as two spheres held by one character

- **From:** the owner's failed hero, read in Propp's terms (p.80: one character may hold several spheres); `ProppQueue.md` item (j).
- **Measured:** exploratory: one character holds the hero's and the villain's sphere in about two thirds of the tragedies; tragedy has only 13 defeats (I−) in 3,214 functions, so the failed hero is not mainly the hero in negative mode.

## Links at a distance

**A link joins two functions that can stand far apart, with any number of others between them, and the second may never come.**
It is a relation, not a rule: the first tends to bring the second later in the same move.
The bottom-up test (`Free/`, 2026-10-19) found the same of the close pairs: readers given no list of acts name the first half of each pair with a verb of its own, but the second half only as whatever act breaks or fulfils the first, so the pairs are relations too.
These links come from the outline this catalog follows. Where Propp states a link, its entry gives the page; where he does not, the entry says so.
Their strength at any distance was measured on 2026-10-19 (`Links/`): the share of moves holding the first function in which the second follows, anywhere later in the move, for transcribers A and B and for Propp's own moves.

### A or a to K

- **Joins:** villainy or lack, and its liquidation.
- **From Propp:** p.53: liquidation "together with villainy (A), constitutes a pair."
- **Measured:** followed by K in 40% and 40% of tale moves (A and B), 16% and 16% of fable moves, 22% and 18% of tragedy moves, and 60% of Propp's own; above chance in all (`Links/LinksRun.txt`).
- **Literal meaning:** The trouble that is set right.
  Whatever is lost or lacking at the start is what the move works to restore; everything between is the way there.
- **Social lesson:** Do not rest until the wrong is set right.
- **Cultural meaning:** This sequence runs from the misfortune that sets the story going to the restoring of order. It can be read as assuring the community that it has the values and the heroes it needs to heal itself after a misfortune, and as holding up the ideal that individual strength must in the end serve the group.

### ↑ to ↓

- **Joins:** departure and return.
- **From Propp:** not stated as a link. He describes the return (p.55) and adds that it is generally made in the same forms as the hero's arrival, but he does not name departure and return a pair.
- **Measured:** followed by ↓ in 32% and 39% of tale moves, above chance; 10% and 7% of fable moves; 14% and 14% of tragedy moves, not above chance; 57% of Propp's own (`Links/PostHoc.txt`, the reader mended).
- **Literal meaning:** Going out and coming back.
  The hero who leaves is expected home again, though a hero may stay where the quest led.
- **Social lesson:** Go out into the world, but come back to serve your own people.
- **Cultural meaning:** These passages can be read as the shape of growing up: real change asks for a time away from the comfort of home. In some tales the return never comes, and that is the start of a new life in a new home.

### H to I

- **Joins:** struggle and victory.
- **From Propp:** p.64: struggle and victory are among the functions "arranged in pairs."
- **Measured:** followed by I in 86% and 86% of tale moves, 64% and 70% of fable moves, 85% and 64% of tragedy moves, and all of Propp's; above chance in all.
- **Literal meaning:** The fight is won.
  A fight once begun is expected to end in the villain's defeat, however long it takes.
- **Social lesson:** Once you take up a fight, see it through.
- **Cultural meaning:** This sequence is the direct, high-stakes confrontation with the source of the harm. Some troubles cannot be met by cleverness or by giving way; the struggle is the moment the hero must face the threat head on. The victory means something because the danger was real. It can be read as a trial like those of the old initiation rites, turning the hero from a protected child into a protector of the community.

### M to N

- **Joins:** difficult task and solution.
- **From Propp:** not in his list of pairs (p.64); he defines the task (p.60) and the solution (p.62) and places them together in the variable scheme (pp.104-105).
- **Measured:** followed by N in 81% and 86% of tale moves, 62% and 60% of fable moves, 50% and 67% of the few tragedy moves (6 and 3), and all of Propp's.
- **Literal meaning:** The task is done.
  A task once set is expected to be solved, with other acts between.
- **Social lesson:** Finish what you undertake.
- **Cultural meaning:** This sequence matches Greimas's glorifying test of the hero. He shows, sometimes for the third time, that he has the wit to be a hero. Accepting the task shows his willingness to be tested, and the solution shows him ready for what comes. Because the test is public, the community can see that the hero has earned his place.

### J to Q

- **Joins:** branding and recognition.
- **From Propp:** p.62: when the hero is recognized by a mark, a brand or a thing given him, "recognition serves as a function corresponding to branding and marking."
- **Measured:** too rare to test in the transcriptions (2 to 6 moves with J); in Propp's own, 3 of 3.
- **Literal meaning:** The mark that proves.
  The wound or token the hero receives is what later shows who the hero is.
- **Social lesson:** Your deeds identify you; true worth will be recognized.
- **Cultural meaning:** This sequence shows that the scars or tokens of the struggle identify the hero, and set him apart from the false hero. The mark can also be read as a sign of higher standing, like the marks of old initiation rites, showing that the hero has passed into a later stage of life.
- **Semantic bundle** (from `SemanticBundling.md`, J–Q · branding and recognition):
  *Propp: XVII, XXVII, pp.52, 62; p.108.*
  **Bundle:** a mark received in the ordeal, read later by others.
  **Value:** **identity persists through disguise and must be socially validated.**
  The hero's claim is not self-authenticating: it requires a witness and a token.
  **Corpus:** 5 occurrences, 3 unpaired.
  It is the loosest pair, and the one whose halves sit furthest apart in the tale.

### L to Ex

- **Joins:** unfounded claims and exposure.
- **From Propp:** not stated as a link. He says exposure is "in most cases, connected with the one preceding" (p.62), that is, with recognition, not with the false claim.
- **Measured:** followed by Ex in 44% and 57% of tale moves, 74% and 43% of fable moves, and 67% of Propp's; too rare in tragedy.
- **Literal meaning:** The lie found out.
  A false claim is expected to be exposed before the end.
- **Social lesson:** Lies are found out. Do not claim what is not yours.
- **Cultural meaning:** This sequence, and the false hero as a sphere of action, hold up the injunction against lying and bearing false witness. One reading, the owner's and still to be tested (`ProppQueue.md` item (k)), is that the false hero stands even lower in the tale's social order than the villain.

### D and E to F

- **Joins:** test and reaction, and the gift.
- **From Propp:** p.65: "Elements DEF also form something of a whole."
- **Measured:** followed by F in 68% and 76% of tale moves, 17% and 8% of fable moves, 67% and 50% of tragedy moves (6 each), and 84% of Propp's.
- **Literal meaning:** The answer earns the gift.
  How the hero meets the test decides whether help is given.
- **Social lesson:** Kindness and respect toward a benefactor are rewarded. Keep faith with those who help you.
- **Cultural meaning:** This group holds the qualifying test (D E F in Propp's model), where the hero may perform an act of courtesy, such as sharing bread with an old man, and is given what he needs. It can be read as showing the importance of keeping faith with the donor: to cheat the donor would make the hero a villain.

### Pr to Rs

- **Joins:** pursuit and rescue.
- **From Propp:** p.64: pursuit and deliverance are among the functions "arranged in pairs."
- **Measured:** followed by Rs in 80% and 75% of tale moves, 44% and 14% of fable moves, 45% and 38% of tragedy moves, and 93% of Propp's.
- **Literal meaning:** The chase that ends in escape.
  A pursuit is expected to end with the hero saved.
- **Social lesson:** Danger follows success. Accept help and keep moving until you are safe.
- **Cultural meaning:** This structural pair can be read as saying that the upheaval of the struggle brings a reaction of its own. The pursuit is the backlash against the hero, and warns the listener that the moment of greatest danger may come after the victory seems won.

# Part IV: What would make the argument publishable

**From `SemanticBundling.md`, Part III, unchanged.**

**The draft marker is structural, not a backlog.**
The three items below were examined against the set.
Item 2's measurement half is discharged, and its figures are verified against `consentScan.py`: 4 violations of 37 unqualified, and 6 of 34 once Propp's seeker-hero restriction applies, both exact.
What remains of items 1 and 2 is comparative.
It needs a second corpus structurally coded at Propp's granularity, which this project does not hold and which is handed on to a second project, `SynthesizedProppGrammar`.
Item 3 is an argument still owed, and the file records that Propp declined it too.

**So this file cannot be promoted out of draft by work inside this set, at any budget.**
The publication choice is to carry it as a marked draft with this section intact, which is honest, or to exclude it.
That choice belongs to whoever publishes the set, and nothing here is waiting on an instrument.

**The strong claims, already supported:**
1. Propp's system has three structural levels, all named by him.
2. Its combinatorial restrictions are semantic, by his own statement ("devoid of sense") and by measurement (25/25 variety linkage).
3. The two branches encode alternative models of proven worth, with his own frequencies (41/33/3 per 100) and a typographic constraint that enforces the choice.

**What is needed next:**
1. **Comparative application.**
   The catalog is an instrument; its value is in being run against non-Slavic Indo-European corpora and, as a control, against a non-Indo-European one.
   Da Silva & Tehrani supply the phylogenetic frame; what is missing is structural coding at Propp's granularity.
2. **The `C` finding has had its own treatment, and what it yielded is an order claim.**
   `ConsentClaim.md` froze three predicates, `consentScan.py` ran them, and `ConsentResult.md` reports them.
   Consent is invariant in position, 60 of 60, and is not required in presence: absent from 4 of 37 moves under the unqualified claim, and from 6 of 34 once Propp's own seeker-hero restriction is applied, which worsens the fit rather than improving it.
   What is still needed is comparative: whether a fixed consent position is unusual across traditions is untested here and needs a second corpus.
3. **An answer to the strongest form of Lévi-Strauss.**
   His objection was not only that the schema is empty but that meaning lies in oppositions and their mediation.
   The two-branch finding is arguably an *opposition* (force vs competence) with the tale-move as its *mediation*, which would meet him on his own ground rather than merely rejecting him.
   Propp answered the other charge himself and not this one: his 1966 reply denies that form can be divided from content, and says twice that he will not take up all of Lévi-Strauss's objections.
   This item is therefore still owed.
   See `ProppGrammarResearchFinalReport.md` §13 and the `References.md` row.

# Part V: The v46 grammar's groups

**From `SemanticCatalog46.md`, unchanged: how the catalog is checked against the grammar, how to read a grammar entry, the groups of the grammar that have no entry of their own above, then its dependencies, extensions and lessons.** The groups folded into the catalog above are not repeated here.

**The catalog is checked, not only written.**
A frozen test in `StepTests.txt` requires one entry here for every group in the grammar, at least one tree test for every group, and no entry for a group the grammar lacks.
A **tree test** feeds the grammar one string of symbols and checks where the grammar's **parse tree**, the way it groups the symbols, puts a given function.
So what an entry says a group holds is tested against the grammar itself.
Run `python runSteps.py 6` to check.

## How to read a grammar entry

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

## The grammar's other groups

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

## Dependencies, not productions

**J–Q: the mark and the recognition.**
Branding J (XVII) falls inside `TroubleToLiquidation`, and recognition Q (XXVII) falls outside it, so the two spans cross, and a single tree cannot hold both.
A–K is kept as the unit, and J–Q is carried as a dependency: the J in `StruggleAndOutcome` marks the hero whom the Q in `Endgame` recognizes.
Its meaning is given under the link "J to Q", in Part III.

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
