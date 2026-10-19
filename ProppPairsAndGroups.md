# Propp's pairs and groups: a catalog of meanings

**This catalog follows the pairs and groups Propp himself names, not a grammar.**
It is built from the owner's outline (`Propp pairs and groups.txt`, 2026-10-18): Propp's variable scheme, his four kinds of move, the groups and pairs within a move, and the links that join functions at a distance.
`ProppEBNF46.txt` and `SemanticCatalog46.md` stay as they are: the grammar is the tested instrument, and this catalog is where the meanings live.
A long-distance link such as departure and return is hard to write as a production rule and easy to state as a relation, so the links have entries of their own here.

## How to read an entry

- **Symbols.** The functions it holds, in Propp's letters; `[ ]` marks one that may be absent.
- **From Propp.** What Propp says of it, with the page where it has been checked against the text.
- **Links.** The long-distance links it takes part in.
- **Measured.** What this project has counted about it, by a program anyone can rerun. The pair figures are from the frequency analysis (`Ngrams/ConfirmRun.txt`): how many times more often the second half follows the first than in the same stories shuffled, on the half of the stories kept back for confirmation, transcriber A then B; "acts" gives the same for the acts described without Propp's notation.
- **Literal meaning.** What it says on its surface. A short phrase, then a few sentences more.
- **Cultural meaning.** The conduct the tale teaches its young listener, and the value behind it. These rest on a speculative reading, not on Propp, set out in `SemanticCatalog46.md`, section "A speculative reading, not from Propp"; they are drafts.
- **Carried from.** The entry of `SemanticCatalog46.md` a meaning was taken from, word for word. "Not yet written" marks a meaning still to be discussed.

## The variable scheme

```text
α β γ δ ε ζ η [λ] θ A B C ↑ D E F G [ (H J I K ↓ Pr Rs o L) / (o L M J N K ↓ Pr Rs) ] Q Ex T U W*
```

### `variableScheme`

- **Symbols:** the line above; the upper branch for moves with struggle and victory, the lower for moves with a difficult task
- **From Propp:** pp.104-105: adding up the schemes of his tales, Propp finds that struggle and victory (H-I) and the difficult task and its solution (M-N) hold the same place in the series, and only the unrecognized arrival and the false claim (o-L) shift, after the fight but before the tasks. All the tales of his material follow this one variable scheme. The preparatory section is added here; Propp's line begins at A.
- **Measured:** not yet measured.
- **Literal meaning:** The whole story.
  A misfortune or a want sets it going, and each new one starts a new move inside it.
- **Cultural meaning:** A young person's passage from a home left unprotected to the head of a new home.
  The tale tells this passage as a pattern taken from ancient initiation rites.
  The family order is the same in a kingdom and in a peasant household.
  The tale is a cycle: it starts from one family and ends by founding the next, whose child will be the next hero.
- **Carried from:** `tale` in `SemanticCatalog46.md`, which describes the whole tale.

## The four kinds of move

**Propp adds up the moves of his tales in four kinds** (pp.104-105). Each is a path through the variable scheme.

### `struggleMove`

- **Symbols:** A B C ↑ D E F G H J I K ↓ Pr Rs o L Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with struggle and victory, or a simple killing of the enemy; a move with H-I is the typical first move.
- **Measured:** not yet measured.
- **Literal meaning:** The fight story.
  The hero wins back what was lost by defeating the one who took it, and comes home.
- **Cultural meaning:** not yet written.

### `taskMove`

- **Symbols:** A B C ↑ D E F G o L M J N K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with difficult tasks; such moves are most often second or repeated, and only once first.
- **Measured:** not yet measured.
- **Literal meaning:** The task story.
  The hero arrives unknown, a rival claims the hero's due, and the hero proves the right by doing what no one else can.
- **Cultural meaning:** not yet written.

### `bothStruggleAndTaskMove`

- **Symbols:** A B C ↑ F H I K ↓ L M N Q Ex U W*
- **From Propp:** p.105: tales with both pairs follow the upper branch and then, without coming to an end, the lower; H-I come before M-N, L stands between them, and no pursuit occurs in the cases Propp examined.
- **Measured:** not yet measured.
- **Literal meaning:** The fight, then the proof.
  The hero wins the fight, but a false claimant takes the credit, and the hero must win again by the task.
- **Cultural meaning:** not yet written.

### `neitherStruggleNorTaskMove`

- **Symbols:** A B C ↑ D E F G K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.105: the schemes with neither struggle nor tasks; they bypass the distinctive elements of each and present no construction of their own.
- **Measured:** not yet measured.
- **Literal meaning:** The quest without a contest.
  What was lost is found or won back with the help gained on the way, with no fight and no test of right.
- **Cultural meaning:** not yet written.

## The opening

### `initialSituation`

- **Symbols:** α
- **From Propp:** p.25: not a function, but an important element of form: the members of the family are introduced, or the hero is introduced by name or status.
- **Measured:** not yet measured.
- **Literal meaning:** Who is there at the start.
  The family and its circumstances are set out before anything happens.
- **Cultural meaning:** not yet written.

### `preparatorySection`

- **Symbols:** β γ δ ε ζ η [λ] θ
- **From Propp:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Measured:** not yet measured.
- **Literal meaning:** What makes the misfortune possible.
  The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived.
  Propp calls the first seven functions the preparatory part (p.30).
- **Cultural meaning:** The end of safety at home.
  The opening shows that the young must leave home sooner or later.
  The safety of home is fragile and does not last, and innocence falls to the deceptions of the wider world.
  The opening is a threshold: it ends the safety of childhood, sometimes violently, and pushes the young person into the trials of growing up.
- **Carried from:** `preparatorySection` in `SemanticCatalog46.md`.

### `absentation`

- **Symbols:** β
- **From Propp:** p.26: one of the family leaves home, or dies; the one preparatory function outside every pair.
- **Measured:** not yet measured.
- **Literal meaning:** The protectors leave.
  Whether they go out or die, the household is left unguarded, and that opens the way for the misfortune.
- **Cultural meaning:** The end of childhood shelter.
  The elders' leaving or death is the first stage of a rite of passage.
  It exposes the young to the real world, sometimes violently, and forces them out of dependence, so that they can in time cross into the wild, where the trials of growing up take place.
- **Carried from:** `absentation` in `SemanticCatalog46.md`.

### `InterdictionAndViolation`

- **Symbols:** γ δ
- **From Propp:** p.26 and p.27: an interdiction is addressed to the hero, and it is violated; the two are a pair.
- **Measured:** γ δ 6.6 and 4.6; acts forbid, disobey 6.8 and 4.5.
- **Literal meaning:** A rule given and broken.
  This is the breach through which misfortune enters.
  When the elders' leaving is told between the two, it sits inside the breach: the warning is given, the protectors leave, and the warning is broken.
- **Cultural meaning:** The broken rule that starts the story.
  In the tale, the prohibition is there to be broken.
  Breaking it is an act of self-harm that ends the false safety of childhood.
  It brings danger at once, but it is also what moves the young person out of standing still and into a life of his own.
- **Carried from:** `RuleViolation` in `SemanticCatalog46.md`.

### `ReconnaissanceAndDelivery`

- **Symbols:** ε ζ
- **From Propp:** p.28: the villain tries to learn something about the victim, and receives it.
- **Measured:** ε ζ 7.4 and 10.0; acts seek-information, reveal-information 4.4 and 3.9.
- **Literal meaning:** The villain asks for information and gets it.
  The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Cultural meaning:** Secrets get out.
  No household can keep its weak points hidden for ever.
  The household gives the villain what he wants because it is innocent and cannot imagine his intent.
  How easily he learns it shows a rule of the tale: hidden weaknesses come out, and the young person's weak points must be exposed to the world before the journey can begin.
- **Carried from:** `InformationGathering` in `SemanticCatalog46.md`.

### `TrickeryAndComplicity`

- **Symbols:** η [λ] θ
- **From Propp:** p.29 and p.30: the villain tries to deceive the victim, and the victim is taken in; λ, a preliminary misfortune, can stand between them.
- **Measured:** η θ 4.0 and 5.2; acts deceive, be-taken-in 6.3 and 6.0. Then the harm: θ A 1.7 and 1.9; acts be-taken-in, harm 2.5 and 2.8, and deceive, harm two places apart 1.3 and 1.4, the trick's success between them.
- **Literal meaning:** The villain deceives, and the victim gives in.
  The preliminary misfortune is what forces the victim to agree.
- **Cultural meaning:** Good judgment fails.
  A child's instinct is no match for deliberate malice.
  The villain's disguise shows that danger often looks like a harmless part of home life.
  When a preliminary misfortune forces the victim to agree, the tale shows that instinct alone cannot protect the inexperienced: the victim's own will gives way, and the hero's journey grows out of the wreckage.
- **Carried from:** `DeceptionTrap` in `SemanticCatalog46.md`.

## Groups and pairs within a move

### `complication`

- **Symbols:** (A or a) B C ↑
- **From Propp:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
- **Links:** A or a to K; ↑ to ↓.
- **Measured:** its steps follow each other: A B 2.0 and 1.6; B C 5.6 and 3.8; C ↑ 4.5 and 4.9; B ↑ two to four apart 1.7 and 2.1.
- **Literal meaning:** The misfortune made known, and the hero setting out.
  Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Cultural meaning:** The community calls one of its own to act.
  The complication draws a young person out of the home to answer a need of the community.
  Going from seeing the misfortune to crossing the threshold shows that private peace cannot last while a public harm goes unanswered.
  The traveler may pick up unearned help along the road: setting out by itself seems to bring support from forebears and the natural world, and it turns a victim who stays put into someone who acts to set things right.
- **Carried from:** `complication` in `SemanticCatalog46.md`.

### `TestAndReaction`

- **Symbols:** D E
- **From Propp:** p.39 and p.42: the hero is tested, questioned or attacked by one who may then help, and reacts.
- **Links:** D and E to F.
- **Measured:** D E 6.8 and 5.9, and D E− 5.3 and 5.6; acts test, respond 4.7 and 5.3. E F was not confirmed within four places.
- **Literal meaning:** Someone tests the hero, and the hero answers.
  The answer, kind or unkind, decides whether help will follow.
- **Cultural meaning:** Showing that one knows the ways of one's culture.
  This is not a loose lesson in kindness or fair dealing; it is a strict test of readiness.
  Passing it shows that the young person has the manners, the respect for elders, or the quick wits needed to survive away from home.
  The agent may be a reward for honoring the duty to give in return, or it may be taken by a trick from a hostile donor.
  Either way, power does not come at random: it goes to those who have learned the rules of their world.
- **Carried from:** the cultural meaning from `TestedAcquisition` in `SemanticCatalog46.md`, which holds D E and F together; the literal meaning is new.

### `receiptOfMagicalAgent`

- **Symbols:** F
- **From Propp:** p.43: the hero acquires the use of a magical agent.
- **Links:** D and E to F.
- **Measured:** not yet measured.
- **Literal meaning:** The means to undo the misfortune.
  Earned from a donor, it is a reward; received with no test, from a father or by finding it, it comes with the setting out.
- **Cultural meaning:** *Draft.* Help earned is power.
  Those who behave rightly are equipped by others, and what was promised in return is paid.
- **Carried from:** `receiptOfMagicalAgent` in `SemanticCatalog46.md`.

### `spatialTransference`

- **Symbols:** G
- **From Propp:** p.50: the hero is transferred, delivered or led to where the object of the search is.
- **Measured:** E G 4.0 and 3.8.
- **Literal meaning:** The passage to the other kingdom.
  It is where the misfortune can be undone.
- **Cultural meaning:** *Draft.* Go where the task is.
  However far it is.
- **Carried from:** `spatialTransference` in `SemanticCatalog46.md`.

### `StruggleAndVictory`

- **Symbols:** H I
- **From Propp:** p.51 and p.53: the hero and the villain join in direct combat, and the villain is defeated.
- **Links:** H to I.
- **Measured:** H I 5.8 and 5.8, and still above chance six places apart; acts fight, win 9.1 and 7.0.
- **Literal meaning:** The fight, the mark, and the victory.
  The hero fights the enemy, in combat or in a contest, is marked, and wins.
  The mark won here is what lets the hero be recognized later.
- **Cultural meaning:** The fight that makes a ruler, and the mark it leaves.
  The fight changes the young person for good: it ends the passive child.
  The mark is lasting proof that the hero went into the wild or the underworld and came back.
  Because the mark comes with the victory, the tale says that the right to lead and protect belongs to those who carry the scars of the struggle.
- **Carried from:** `StruggleAndOutcome` in `SemanticCatalog46.md`, which held H J I; branding now has its own entry.

### `branding`

- **Symbols:** J
- **From Propp:** p.52: the hero is branded, wounded or given a token.
- **Links:** J to Q.
- **Measured:** not yet measured.
- **Literal meaning:** The sign by which the hero will be known.
  It is rare in the corpus but central to the end, since it is what the recognition reads.
- **Cultural meaning:** *Draft.* Your deeds leave marks.
  Bear the marks of what you have done; they will vouch for you.
- **Carried from:** `branding` in `SemanticCatalog46.md`.

### `liquidation`

- **Symbols:** K
- **From Propp:** p.53: the initial misfortune or lack is liquidated.
- **Links:** A or a to K.
- **Measured:** A K and a K were not confirmed within four places, their halves standing far apart. In the acts (`Problems/`), tales repair nearly all their problems and tragedies far fewer than their length gives.
- **Literal meaning:** The misfortune undone.
  It is the point every move is heading for.
- **Cultural meaning:** *Draft.* Setting things right.
  Right what was wronged and restore what was lost; Propp calls it the tale's peak (p.53).
- **Carried from:** `liquidation` in `SemanticCatalog46.md`.

### `return`

- **Symbols:** ↓
- **From Propp:** p.55: the hero returns.
- **Links:** ↑ to ↓.
- **Measured:** not yet measured.
- **Literal meaning:** The way home.
  It opens the second half of the move.
- **Cultural meaning:** *Draft.* Bring home what you won.
  The achievement serves the family.
- **Carried from:** `return` in `SemanticCatalog46.md`.

### `PursuitAndRescue`

- **Symbols:** Pr Rs
- **From Propp:** p.56 and p.57: the hero is pursued, and rescued from pursuit.
- **Links:** Pr to Rs.
- **Measured:** Pr Rs was too rare to confirm; acts pursue, escape not confirmed.
- **Literal meaning:** Escaping capture on the way home.
  It allows the two orders found in the corpus: a pursuit that a rescue answers, or a rescue that comes first and heads off the pursuit.
- **Cultural meaning:** Closing the border between the wild and home.
  The two paths show that getting past a backlash takes adaptability more than strength.
  The hero survives by hiding, by changing shape, and by the help others give, not by fighting.
  Growing up means knowing when to face an enemy and when to slip out of reach of past danger.
- **Carried from:** `Evasion` in `SemanticCatalog46.md`.

### `unrecognizedArrival`

- **Symbols:** o
- **From Propp:** p.60: the hero, unrecognized, arrives home or in another country.
- **Measured:** not yet measured.
- **Literal meaning:** The hero without his due.
  Present, but not known.
- **Cultural meaning:** *Draft.* Merit may go unnoticed for a time.
  Be patient and humble.
- **Carried from:** `unrecognizedArrival` in `SemanticCatalog46.md`.

### `unfoundedClaims`

- **Symbols:** L
- **From Propp:** p.60: a false hero presents unfounded claims.
- **Links:** L to Ex.
- **Measured:** not yet measured.
- **Literal meaning:** The hero's deed stolen.
  The end of the tale must set it right.
- **Cultural meaning:** *Draft.* Do not take credit you have not earned.
  The braggart who claims another's deed will be shamed.
- **Carried from:** `unfoundedClaims` in `SemanticCatalog46.md`.

### `TaskAndSolution`

- **Symbols:** M N
- **From Propp:** p.60 and p.62: a difficult task is proposed to the hero, and it is resolved.
- **Links:** M to N.
- **Measured:** M N 8.9 and 9.1, falling steadily with distance (9.0, 4.9, 3.4, 2.7 at one to four apart); acts set-task, do-task 4.6 and 6.3.
- **Literal meaning:** A hard task, set and done.
  The candidate faces a very hard trial and succeeds.
  The task does at court what the fight does in the wild: it checks the claimant's deeds.
- **Cultural meaning:** A fair test of real ability.
  The tale treats the task as the equal of a battle, because leadership means living by the culture's basic rules.
  The candidates must show real results, by calling on the bonds with forebears and the natural world they have built up.
  That strips away the false hero's empty talk and makes the true hero's right to rule plain to all.
- **Carried from:** `TaskAndSolution` in `SemanticCatalog46.md`.

## The denouement

### `denouement`

- **Symbols:** Q Ex T U W*
- **From Propp:** p.92: a tale runs from villainy or lack to the wedding, or to other functions employed as a denouement; the denouement is whatever ends the move, in the full scheme this run, in a shorter move K, Rs or a reward.
- **Measured:** not yet measured.
- **Literal meaning:** The final settling of accounts.
  The true hero is recognized, the false one is exposed and punished, and the hero marries and comes to power.
  These may come in any order.
- **Cultural meaning:** The social order put back together.
  The endgame ends the illusions and steadies the community.
  Recognition and exposure together clear out the false and put the truth back at the top of the kingdom.
  The wedding and the hero's rise close the cycle: a sound family stands again at the head of the people, ready for the next generation of heroes.
- **Carried from:** `Endgame` in `SemanticCatalog46.md`.

### `RecognitionAndExposure`

- **Symbols:** Q Ex
- **From Propp:** p.62: the hero is recognized, and the false hero or villain is exposed.
- **Links:** J to Q; L to Ex.
- **Measured:** Q Ex was too rare to test.
- **Literal meaning:** The truth comes out.
  The true hero is known for who they are, and the one who lied is shown up.
- **Cultural meaning:** not yet written.

### `transfiguration`

- **Symbols:** T
- **From Propp:** pp.62-63: the hero is given a new appearance.
- **Measured:** not yet measured.
- **Literal meaning:** The hero's new standing made visible.
  Its free place is itself a finding: it is the one function whose position means nothing.
- **Cultural meaning:** *Draft.* Worth made visible.
  The hero comes to look like who the hero is.
- **Carried from:** `transfiguration` in `SemanticCatalog46.md`.

### `punishment`

- **Symbols:** U
- **From Propp:** p.63: the villain is punished.
- **Measured:** not yet measured.
- **Literal meaning:** The wrong answered.
- **Cultural meaning:** *Draft.* Wrongdoers get what they deserve.
  Or, in the pardon, the victor shows mercy.
- **Carried from:** `punishment` in `SemanticCatalog46.md`.

### `wedding`

- **Symbols:** W*
- **From Propp:** p.63: the hero is married and ascends the throne.
- **Measured:** not yet measured.
- **Literal meaning:** The hero given his due.
  It is the most common close of a move, and the ending p.92 names first.
- **Cultural meaning:** *Draft.* The goal of the passage.
  Marriage and the founding of a new household, which begins the next cycle.
- **Carried from:** `wedding` in `SemanticCatalog46.md`.

## Links at a distance

**A link joins two functions that can stand far apart, with any number of others between them, and the second may never come.**
It is a relation, not a rule: the first tends to bring the second later in the same move.
The bottom-up test (`Free/`, 2026-10-19) found the same of the close pairs: readers given no list of acts name the first half of each pair with a verb of its own, but the second half only as whatever act breaks or fulfils the first, so the pairs are relations too.
These links come from the outline this catalog follows; which of them Propp states, and on which page, is still to be marked.
Their strength at any distance is not yet measured; the frequency analysis looked only up to four places apart, and its findings are given.

### A or a to K

- **Joins:** villainy or lack, and its liquidation.
- **Measured:** not confirmed within four places, the halves standing far apart.
- **Literal meaning:** The trouble that is set right.
  Whatever is lost or lacking at the start is what the move works to restore; everything between is the way there.
- **Cultural meaning:** not yet written.

### ↑ to ↓

- **Joins:** departure and return.
- **Measured:** not yet tested.
- **Literal meaning:** Going out and coming back.
  The hero who leaves is expected home again, though a hero may stay where the quest led.
- **Cultural meaning:** not yet written.

### H to I

- **Joins:** struggle and victory.
- **Measured:** H I confirmed adjacent, and still above chance six places apart.
- **Literal meaning:** The fight is won.
  A fight once begun is expected to end in the villain's defeat, however long it takes.
- **Cultural meaning:** not yet written.

### M to N

- **Joins:** difficult task and solution.
- **Measured:** M N confirmed, its strength falling steadily over one to four places.
- **Literal meaning:** The task is done.
  A task once set is expected to be solved, with other acts between.
- **Cultural meaning:** not yet written.

### J to Q

- **Joins:** branding and recognition.
- **Measured:** not yet tested.
- **Literal meaning:** The mark that proves.
  The wound or token the hero receives is what later shows who the hero is.
- **Cultural meaning:** not yet written.

### L to Ex

- **Joins:** unfounded claims and exposure.
- **Measured:** not yet tested.
- **Literal meaning:** The lie found out.
  A false claim is expected to be exposed before the end.
- **Cultural meaning:** not yet written.

### D and E to F

- **Joins:** test and reaction, and the gift.
- **Measured:** D E confirmed; E F not confirmed within four places.
- **Literal meaning:** The answer earns the gift.
  How the hero meets the test decides whether help is given.
- **Cultural meaning:** not yet written.

### Pr to Rs

- **Joins:** pursuit and rescue.
- **Measured:** too rare to confirm.
- **Literal meaning:** The chase ends in escape.
  A pursuit is expected to end with the hero saved.
- **Cultural meaning:** not yet written.
