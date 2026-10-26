# Propp's pairs and groups: a catalog of meanings

**This catalog follows the pairs and groups Propp himself names, not a grammar.**
It is built from the owner's outline (`Propp pairs and groups.txt`, 2026-10-18): Propp's variable scheme, his four kinds of move, the groups and pairs within a move, the links that join functions at a distance, his characters, and the devices the other corpora add.
`ProppEBNF46.txt` and `SemanticCatalog46.md` stay as they are: the grammar is the tested instrument, and this catalog is where the meanings live.
A long-distance link such as departure and return is hard to write as a production rule and easy to state as a relation, so the links have entries of their own here.

## How to read an entry

- **Symbols.** The functions it holds, in Propp's letters; `[ ]` marks one that may be absent. For a device Propp's list lacks, the acts or verbs that carry it.
- **From Propp.** What Propp says of it, with the page of the 1968 English edition (Morphology of the Folktale, second edition, University of Texas Press), checked against the text. For a device Propp's list lacks, "none, not in his list," then the studies and genres it was found in.
- **Links.** The long-distance links it takes part in.
- **Measured.** What this project has counted about it, by a program anyone can rerun. The pair figures are from the frequency analysis (`Ngrams/ConfirmRun.txt`): how many times more often the second half follows the first than in the same stories shuffled, on the half of the stories kept back for confirmation, transcriber A then B; "acts" gives the same for the acts described without Propp's notation. "In stories" gives the share of stories holding the function: Propp's own 45 tales (Appendix III), then transcribers A and B on the wondertales (card U), the animal tales, the fables, the tragedies and the myths, from the normalized tables (`Data/`). Propp's own tables begin at A, so they hold no preparatory functions.
- **Literal meaning.** What it says on its surface. A short phrase, then a few sentences more.
- **Cultural meaning.** A reading of the conduct and values the tale may hold up to its listeners. These readings are speculation, not Propp, set out in `SemanticCatalog46.md`, section "A speculative reading, not from Propp"; they are drafts, and where they cite another scholar, the claim is that scholar's.

**The negative mode.** Propp lets a function fail or turn the other way, and his tables mark it with a minus: E− the hero fails the test, F− the magical agent is not received, and so on (his schemes in Appendix III; in this project's transcriptions, the same sign). A negative function is the same function in another mode, not a new one, which is part of why Propp's list covers so much. Measured (`Data/` tables, 2026-10-21): negative forms are rare in every genre, 3.3% of the wondertales' functions, 2.6% of the animal tales', 6.8% of the fables', 3.4% of the tragedies' and 3.0% of the myths', mostly E− and F−; the fable uses the mode most and over the most functions (F−, E−, θ−, K−, I−).

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

- **Social norm:** Success is earned, not inherited: leave home, pass the tests in their order, and come back to found a household of your own. Rank and marriage reward proven merit, and they are open even to the youngest and the least regarded.

- **Cultural meaning:** This move scheme can be read as a young person's passage away from home, unprotected for a time, until becoming the head of a new home.
  Propp himself later read the tale as a memory of initiation rites (Historical Roots of the Wondertale, 1946).
  The family order is the same in a kingdom as in a peasant household.
  The tale is a cycle: it starts from one family and ends by founding the next, whose child may become the next hero.

  The scheme also holds tests in threes. Propp notes trebling as a common way functions are repeated (p.74). Dundes argues that the pattern of three belongs to the cultures that tell these tales, the first two instances setting a pattern that the third confirms or breaks ("The Number Three in American Culture," 1968). Greimas (1966/1983, Chapter 10) reads the hero's path as three tests: the qualifying test (D E F in Propp's model), the main test (H to K), and the glorifying test (M N). On that reading the sequence validates the hero as a true hero by merit.

## The four kinds of move

**Propp lists the moves of his tales in four kinds** (pp.104-105). Each is a path through the variable scheme.
Measured for all four (`Data/` tables, 2026-10-21): the share of moves of each kind, by whether the move holds H or I, M or N, both, or neither; counted on Propp's own 86 moves (the shared tails counted with their moves), and on transcribers A and B.

### `struggleMove`

- **Symbols:** A B C ↑ D E F G H J I K ↓ Pr Rs o L Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with struggle and victory, or a simple killing of the enemy; a move with H-I is the typical first move.
- **Measured:** struggle without task in Propp 38% of moves; wondertales 30% and 33%; animal tales 15% and 13%; fables 6% and 6%; tragedies 18% and 21%; myths 20% and 31%.
- **Literal meaning:** The fight story.
  The hero wins back what was lost by defeating the one who took it, and comes home.
- **Social norm:** Meet a real threat with courage. A success won by facing the enemy gives the right to lead.
- **Cultural meaning:** This move resolves a problem, whether a lack or a misfortune, through direct force, although the victory can be won in any contest, a game of cards among them.

### `taskMove`

- **Symbols:** A B C ↑ D E F G o L M J N K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.104: the sum of all schemes with difficult tasks; such moves are most often second or repeated, and only once first.
- **Measured:** task without struggle in Propp 12% of moves; wondertales 10% and 12%; animal tales 1% and 0%; fables 3% and 2%; tragedies 1% and 2%; myths 2% and 3%.
- **Literal meaning:** The task story.
  The hero arrives unknown, a rival claims the hero's due, and the hero proves the right by doing what no one else can.
- **Social norm:** Prove your worth by skill and wit before those who judge. The deserving one can do what the boaster cannot.
- **Cultural meaning:** This move resolves a problem through actions other than direct force.

### `bothStruggleAndTaskMove`

- **Symbols:** A B C ↑ F H I K ↓ L M N Q Ex U W*
- **From Propp:** p.105: tales with both pairs follow the upper branch and then, without coming to an end, the lower; H-I come before M-N, L stands between them, and no pursuit occurs in the cases Propp examined.
- **Measured:** both in Propp 1% of moves; wondertales 4% and 5%; animal tales 1% and 0%; fables 0% and 0%; tragedies 3% and 1%; myths 4% and 9%.
- **Literal meaning:** The fight, then the proof.
  The hero wins the fight, but a false claimant takes the credit, and the hero must win again by the task.
- **Social norm:** Doing the deed is not enough; you must be able to prove it. Whoever steals the credit for another's deed will be found out.
- **Cultural meaning:** As a story device, this move adds surprise to the struggle: the hero is recognized only after the task is done, and the false hero is exposed. The false claim is a lie, and the tale treats it as gravely wrong; one reading, the owner's and still to be tested (`ProppQueue.md` item (k)), is that it puts the false hero at the bottom of the tale's social order.

### `neitherStruggleNorTaskMove`

- **Symbols:** A B C ↑ D E F G K ↓ Pr Rs Q Ex T U W*
- **From Propp:** p.105: the schemes with neither struggle nor tasks; they bypass the distinctive elements of each and present no construction of their own.
- **Measured:** neither in Propp 49% of moves; wondertales 55% and 50%; animal tales 83% and 87%; fables 92% and 92%; tragedies 78% and 77%; myths 74% and 57%. The short genres are mostly moves of this kind.
- **Literal meaning:** The quest without a contest.
  What was lost is found or won back with the help gained on the way, with no fight and no test of right.
- **Social norm:** Courtesy, hospitality and kindness to strangers are rewarded. Good conduct alone can carry you to success.
- **Cultural meaning:** This move holds only Greimas's qualifying test (D E F in Propp's model), where the hero may perform an act of courtesy, such as sharing bread with an old man, and is given what he needs. The test can be read as valuing solidarity and the customs of hospitality. The move may also reflect a wish that relief can come without painful struggle, a comfort for the listener.

## The opening

### `initialSituation`

- **Symbols:** α
- **From Propp:** p.25: not a function, but an important element of form: the members of the family are introduced, or the hero is introduced by name or status.
- **Measured:** in stories, as coded by the transcribers, who most often leave α unmarked: wondertales 2% and 2%; animal tales 0% and 2%; fables 2% and 3%; tragedies 19% and 19%; myths 9% and 11%. These figures say how often α was coded, not how often a tale opens with one.
- **Literal meaning:** Who is there at the start.
  The family and its circumstances are set out before anything happens.
- **Social norm:** Know what a good household looks like, with order, plenty and each member in place, and do not take it for granted.
- **Cultural meaning:** The initial situation often describes a state of prosperity, with peace, abundance and harmony. It sets the community's ideal baseline, and implies what a working household should look like. But the peace is fragile, and the opening signals without comment that calm also holds vulnerability.

### `preparatorySection`

- **Symbols:** β γ δ ε ζ η [λ] θ
- **From Propp:** Appendix I Table II, p.121, is titled The Preparatory Section; p.80 writes it as (β, γ-δ, ε-ζ, η-θ).
- **Measured:** its pairs are measured in their own entries below.
- **Literal meaning:** What makes the misfortune possible.
  The household is left unguarded, a prohibition is broken, the villain learns what he needs, and the victim is deceived.
  Propp calls the first seven functions the preparatory part (p.30).
- **Social norm:** Heed warnings, guard the household, and beware of strangers' words. Carelessness at home invites disaster.
- **Cultural meaning:** The end of safety at home.
  The opening shows that the young must leave home sooner or later.
  The safety of home is fragile and does not last, and innocence falls to the deceptions of the wider world.
  The opening is a threshold: it ends the safety of childhood, sometimes violently, and pushes the young person into the trials of growing up.

### `absentation`

- **Symbols:** β
- **From Propp:** p.26: one of the family leaves home, or dies; the one preparatory function outside every pair.
- **Measured:** in stories, wondertales 38% and 22%; animal tales 20% and 8%; fables 1% and 1%; tragedies 75% and 75%; myths 6% and 5%. Tragedy opens with an absence, a death or a departure, in three plays of four.
- **Literal meaning:** The protectors leave.
  Whether they go out or die, the household is left unguarded, and that opens the way for the misfortune.
- **Social norm:** When the protectors are gone, the young must guard themselves and the household. Responsibility passes to the next generation sooner than it expects.
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
- **Social norm:** Obey the prohibitions of your elders. Breaking a rule brings misfortune on you and on those close to you.
- **Cultural meaning:** The broken rule that starts the story.
  In the tale, the prohibition is there to be broken.
  Breaking it harms the one who breaks it and ends the false safety of childhood.
  It brings danger at once, but it is also what moves the young person out of standing still and into a life of his own.

### `ReconnaissanceAndDelivery`

- **Symbols:** ε ζ
- **From Propp:** p.28 and p.29: the villain tries to learn something about the victim, and receives it; "Once again we are confronted with paired functions" (p.29).
- **Measured:** ε ζ 7.4 and 10.0; acts seek-information, reveal-information 4.4 and 3.9.
- **Literal meaning:** The villain asks for information and gets it.
  The second half may stand alone (p.29): a careless act can give the villain what he did not ask for.
- **Social norm:** Guard your tongue and your household's secrets. Do not tell a stranger what he asks about you or yours.
- **Cultural meaning:** Secrets do not remain secret.
  No household can keep its weak points hidden for ever.
  The household gives the villain what he wants because it is innocent and cannot imagine his intent.
  How easily he learns it shows a rule of the tale: hidden weaknesses come out, and the young person's weak points must be exposed to the world before the journey can begin.

### `TrickeryAndComplicity`

- **Symbols:** η [λ] θ
- **From Propp:** p.29 and p.30: the villain tries to deceive the victim, and the victim is taken in; λ, a preliminary misfortune, can stand between them.
- **Measured:** η θ 4.0 and 5.2; acts deceive, be-taken-in 6.3 and 6.0. Then the harm: θ A 1.7 and 1.9; acts be-taken-in, harm 2.5 and 2.8, and deceive, harm two places apart 1.3 and 1.4, the trick's success between them.
- **Literal meaning:** The villain deceives, and the victim gives in.
  The preliminary misfortune is what forces the victim to agree.
- **Social norm:** Do not trust appearances or flattering offers. Look past the disguise before you agree to anything.
- **Cultural meaning:** Good judgment often fails.
  A child's instinct is no match for deliberate malice.
  The villain's disguise shows that danger often looks like a harmless part of home life.
  When a preliminary misfortune forces the victim to agree, the tale shows that instinct alone cannot protect the inexperienced: the victim's own will gives way, and the hero's journey grows out of the wreckage.

## Groups and pairs within a move

### `complication`

- **Symbols:** (A or a) B C ↑
- **From Propp:** pp.64-65: villainy, dispatch, decision for counteraction and departure "(ABC↑), constitute the complication". The untested agent inside it is step 6's placement, as decided.
- **Links:** A or a to K; ↑ to ↓.
- **Measured:** its steps follow each other: A B 2.0 and 1.6; B C 5.6 and 3.8; C ↑ 4.5 and 4.9; B ↑ two to four apart 1.7 and 2.1.
- **Literal meaning:** The misfortune made known, and the hero setting out.
  Since step 6 it also holds what the hero takes with him, or picks up on the road, without earning it.
- **Social norm:** When harm comes to your people, answer the call. The one who acts, not the one who waits, becomes the hero.
- **Cultural meaning:** The community calls one of its own to act.
  The complication draws a young person out of the home to answer a need of the community.
  Going from seeing the misfortune to crossing the threshold shows that private peace cannot last while a public harm goes unanswered.
  The traveler may pick up unearned help along the road: setting out seems by itself to bring support from forebears and the natural world, and it turns a victim who stays put into someone who acts to set things right.

### `TestAndReaction`

- **Symbols:** D E
- **From Propp:** p.39 and p.42: the hero is tested, questioned or attacked by one who may then help, and reacts.
- **Links:** D and E to F.
- **Measured:** D E 6.8 and 5.9, and D E− 5.3 and 5.6; acts test, respond 4.7 and 5.3. E F was not confirmed within four places.
- **Literal meaning:** Someone tests the hero, and the hero answers.
  The answer, kind or unkind, decides whether help will follow.
- **Social norm:** Treat strangers, the old and the weak with courtesy and respect. How you answer a test shows what you are.
- **Cultural meaning:** Showing that one knows the ways of one's culture.
  This is not a loose lesson in kindness or fair dealing; it is a strict test of readiness.
  Passing it shows that the young person has the manners, the respect for elders, or the quick wits needed to survive away from home.

### `receiptOfMagicalAgent`

- **Symbols:** F
- **From Propp:** p.43: the hero acquires the use of a magical agent.
- **Links:** D and E to F.
- **Measured:** in stories, Propp 64%; wondertales 78% and 91%; animal tales 44% and 40%; fables 18% and 16%; tragedies 84% and 97%; myths 35% and 43%. F− is the commonest negative form in every genre but the myths.
- **Literal meaning:** The means to undo the misfortune.
  Earned from a donor, it is a reward; received with no test, from a father or by finding it, it comes with the setting out.
- **Social norm:** Help comes to those who have earned it. Repay kindness, and honor what you owe to those who equip you.
- **Cultural meaning:** The hero earns the help he seeks.
  Those who behave rightly are equipped by others, and what was promised in return is paid. The agent may be a reward for honoring the duty to give in return, or it may be taken by a trick from a hostile donor.
  Either way, power does not come at random: it goes to those who have learned the rules of their world.

### `spatialTransference`

- **Symbols:** G
- **From Propp:** p.50: the hero is transferred, delivered or led to where the object of the search is.
- **Measured:** E G 4.0 and 3.8. In stories, Propp 36%; wondertales 29% and 40%; animal tales 4% and 4%; fables 1% and 1%; tragedies 50% and 41%; myths 11% and 28%.
- **Literal meaning:** The passage to the other kingdom.
  It is where the misfortune can be undone.
- **Social norm:** Be willing to go beyond the familiar, and accept guidance. The answer may lie far from home.
- **Cultural meaning:** This function can be read as a crossing, in mind and in place, into a world away from home. It tells the listener that the answers to the deepest troubles lie beyond ordinary boundaries. When the passage relies on a magical agent or an animal, it suggests a new alignment with nature or the divine.

### `StruggleAndVictory`

- **Symbols:** H I

- **From Propp:** p.51 and p.53: the hero and the villain join in direct combat, and the villain is defeated; struggle and victory are among the pairs Propp names (p.64).

- **Links:** H to I.

- **Measured:** H I 5.8 and 5.8, and still above chance six places apart; acts fight, win 9.1 and 7.0.

- **Literal meaning:** The fight and the victory.
  The hero fights the enemy, in combat or in a contest, is often marked, and wins.
  The mark won here is what lets the hero be recognized later.

- **Social norm:** Stand and fight when the threat is real. Courage in the face of danger earns standing.

- **Cultural meaning:** This sequence is a direct, high-stakes confrontation with a real threat, and it is the fight that makes a ruler.
  The fight changes the young person for good, as it ends the passive child. Victory means something because the danger was real, and it gives the hero moral and physical standing.

  It can also be read as saying that justice must be fought for.

### `branding`

- **Symbols:** J
- **From Propp:** p.52: the hero is branded, wounded or given a token.
- **Links:** J to Q.
- **Measured:** in stories, Propp 7%; wondertales 9% and 11%; animal tales 0% and 0%; fables 1% and 0%; tragedies 19% and 16%; myths 1% and 3%.
- **Literal meaning:** The sign by which the hero will be known.
  It is rare in the corpus but central to the end, since it is what the recognition reads.
- **Social norm:** Honorable scars are proof of service. Carry the marks of the struggle without shame; they will speak for you.
- **Cultural meaning:** The mark is lasting proof that the hero went into the wild or the underworld and came back, and is what lets the hero be recognized later.
  Because the mark comes with the victory, the tale suggests that the right to lead and protect belongs to those who carry the scars of the struggle. The mark shows that the struggle has changed the hero for good.

### `liquidation`

- **Symbols:** K
- **From Propp:** p.53: the initial misfortune or lack is liquidated; "This function, together with villainy (A), constitutes a pair. The narrative reaches its peak in this function" (p.53).
- **Links:** A or a to K.
- **Measured:** A K and a K were not confirmed within four places, their halves standing far apart; at any distance, see the link "A or a to K". In the acts (`Problems/`), tales repair nearly all their problems and tragedies far fewer than their length gives.
- **Literal meaning:** The misfortune undone.
  It is the point every move is heading for.
- **Social norm:** A wrong can and should be set right. Persevere until what was lost is restored.
- **Cultural meaning:** This function sets right what was wrong and restores what was lost. It can be read as the healing of the tale's world, and as the assurance that suffering has an end. Propp calls it the tale's peak (p.53).

### `return`

- **Symbols:** ↓
- **From Propp:** p.55: the hero returns.
- **Links:** ↑ to ↓.
- **Measured:** in stories, Propp 71%; wondertales 71% and 71%; animal tales 32% and 16%; fables 4% and 3%; tragedies 59% and 44%; myths 17% and 10%. At any distance from departure, see the link "↑ to ↓".
- **Literal meaning:** The way home.
  It opens the second half of the move.
- **Social norm:** Bring home what you gained. A success counts when it serves the people you return to.
- **Cultural meaning:** A journey matters to the community only if the traveler brings back what was gained. The return begins the hero's acceptance in a new, higher standing. The hero comes home with something of value, wisdom, a cure, or a rescued member of the family, and puts what he has become in the service of his people.

### `PursuitAndRescue`

- **Symbols:** Pr Rs
- **From Propp:** p.56 and p.57: the hero is pursued, and rescued from pursuit; pursuit and deliverance are among the pairs Propp names (p.64).
- **Links:** Pr to Rs.
- **Measured:** as an adjacent pair, Pr Rs was too rare to confirm, and acts pursue, escape were not confirmed; at any distance in the move, Pr is followed by Rs in most tale moves (the link "Pr to Rs"). The two measures differ because the rescue often comes several functions after the pursuit.
- **Literal meaning:** Escaping capture on the way home.
  It allows the two orders found in the corpus: a pursuit that a rescue answers, or a rescue that comes first and heads off the pursuit.
- **Social norm:** Victory invites revenge. Stay watchful after success, and accept help to escape danger.
- **Cultural meaning:** Closing the border between the wild and home.
  The two paths show that getting past a backlash takes adaptability more than strength.
  The hero survives by hiding, by changing shape, and by the help others give, not by fighting.
  Growing up means knowing when to face an enemy and when to slip out of reach of past danger.

### `unrecognizedArrival`

- **Symbols:** o
- **From Propp:** p.60: the hero, unrecognized, arrives home or in another country.
- **Measured:** in stories, Propp 13%; wondertales 22% and 22%; animal tales 0% and 0%; fables 1% and 1%; tragedies 25% and 25%; myths 4% and 1%.
- **Literal meaning:** The hero without his due.
  Present, but not known.
- **Social norm:** Worth does not depend on fine clothes or rank. Humility and patience come before recognition.
- **Cultural meaning:** The unrecognized arrival can be read as the difficulty of coming home changed. The hero cannot walk through the gates expecting to be acclaimed; the community still sees the weak child, the outcast, or the victim who left. Disguise or anonymity protects the hero while he watches how home runs without him. It tells the listener that true merit cannot stay hidden for ever.

### `unfoundedClaims`

- **Symbols:** L
- **From Propp:** p.60: a false hero presents unfounded claims.
- **Links:** L to Ex.
- **Measured:** in stories, Propp 11%; wondertales 13% and 16%; animal tales 6% and 2%; fables 10% and 4%; tragedies 12% and 6%; myths 2% and 4%.
- **Literal meaning:** The hero's deed stolen.
  The end of the tale must set it right.
- **Social norm:** Do not claim credit for another's deeds. Boasting and lying to take a reward are among the worst of wrongs.
- **Cultural meaning:** This function shows how easily deception can win over merit for a time. It voices the fear that the court will reward the boaster and pass over the one who did the deed, and it cautions against trusting the claimant who talks best. In the tale, the one who did the work is rarely the one who speaks up for himself, while the one who seeks reward unearned is skilled at appearances; the end of the tale puts this right.

### `TaskAndSolution`

- **Symbols:** M N
- **From Propp:** p.60 and p.62: a difficult task is proposed to the hero, and it is resolved.
- **Links:** M to N.
- **Measured:** M N 8.9 and 9.1, falling steadily with distance (9.0, 4.9, 3.4, 2.7 at one to four apart); acts set-task, do-task 4.6 and 6.3.
- **Literal meaning:** A hard task, set and done.
  The candidate faces a very hard trial and succeeds.
  The task does at court what the fight does in the wild: it checks the claimant's deeds.
- **Social norm:** Accept hard challenges, and prove yourself by deeds before those who judge.
- **Cultural meaning:** This structural pair is a fair test of real ability.
  The tale treats the task as the equal of a battle, because leadership means living by the culture's basic rules. By carrying out the task, the hero shows the elders that he has made the rules and values of his culture his own.

## The denouement

### `denouement`

- **Symbols:** Q Ex T U W*
- **From Propp:** p.92: a tale runs from villainy or lack to the wedding, or to other functions employed as a denouement; the denouement is whatever ends the move, in the full scheme this run, in a shorter move K, Rs or a reward.
- **Measured:** its parts are measured in their own entries.
- **Literal meaning:** The final settling of accounts.
  The true hero is recognized, the false one is exposed and punished, and the hero marries and comes to power.
  These may come in any order.
- **Social norm:** In the end the truth prevails: the good are rewarded, the wicked punished, and order is restored. Live so that the settling of accounts will favor you.
- **Cultural meaning:** The social order put back together.
  The endgame ends the illusions and steadies the community.
  Recognition and exposure together clear out the false and put the truth back at the top of the kingdom.
  The wedding and the hero's rise close the cycle: a sound family stands again at the head of the people, ready for the next generation of heroes.

### `RecognitionAndExposure`

- **Symbols:** Q Ex
- **From Propp:** p.62: "The hero is recognized" (XXVII, Q), by a mark or brand, by a thing given him, by the accomplishment of a difficult task, or after a long separation; "The false hero or villain is exposed" (XXVIII, Ex), a function "in most cases, connected with the one preceding."
- **Links:** J to Q; L to Ex.
- **Measured:** Q Ex was too rare to test.
- **Literal meaning:** The truth comes out.
  The true hero is known for who he is, and the one who lied is shown up.
- **Social norm:** Do not lie or bear false witness. The truth will come out, and the liar will be exposed and punished.
- **Cultural meaning:** This structural pair answers a wish for justice made plain. In everyday life, bad behavior often goes unnoticed and good deeds go unrewarded; in the tale, the truth comes out in the end, the deserving are seen for what they are, and the false lose what they took.

### `transfiguration`

- **Symbols:** T
- **From Propp:** pp.62-63: the hero is given a new appearance.
- **Measured:** in stories, Propp 16%; wondertales 9% and 9%; animal tales 0% and 0%; fables 2% and 1%; tragedies 3% and 3%; myths 1% and 4%.
- **Literal meaning:** The hero's new standing made visible.
  Its free place is itself a finding: it is the one function whose position means nothing.
- **Social norm:** Be worthy, and in time your worth will show. Outward standing follows inner merit.
- **Cultural meaning:** It can be read as saying that a change won through struggle will show in the end: the hero's outward life comes to match his inner worth.

### `punishment`

- **Symbols:** U
- **From Propp:** p.63: the villain is punished.
- **Measured:** in stories, Propp 27%; wondertales 40% and 27%; animal tales 10% and 6%; fables 8% and 7%; tragedies 59% and 38%; myths 23% and 34%.
- **Literal meaning:** The wrong answered.
- **Social norm:** Wrongdoing will be punished. Justice is owed to the community, and no one is above it.
- **Cultural meaning:** For the tale's world to be at peace again, the source of the harm must be removed. Punishment holds up accountability and limits, and the rules that keep the community safe.

### `wedding`

- **Symbols:** W*
- **From Propp:** p.63: the hero is married and ascends the throne.
- **Measured:** in stories, Propp 58%; wondertales 82% and 80%; animal tales 6% and 2%; fables 2% and 2%; tragedies 62% and 44%; myths 30% and 33%.
- **Literal meaning:** The hero given his due.
  It is the most common close of a move, and the ending p.92 names first.
- **Social norm:** The reward of proven merit is marriage and an honored place. Found a household and carry the line forward.
- **Cultural meaning:** This is a sign of continuity and renewal. A wedding promises the next generation, and an accession promises a stable rule.

## Characters: Propp's spheres of action

**Propp joins the functions into seven spheres of action, each the part a character plays** (pp.79-80): "the tale evidences seven dramatis personae." A sphere and a character need not coincide: a sphere may correspond exactly to one character, one character may hold several spheres, or one sphere may be shared among several characters (p.80). The functions of the preparatory section are spread over the same characters (p.80).
Measured for the spheres together (`Spheres/explore.py`, exploratory, not a frozen test; each function credited to the character who performs it): all seven spheres occur in every genre. One character holds both the hero's and the villain's sphere in 18% and 29% of the wondertales, 4% and 3% of the fables, 66% and 72% of the tragedies, and 28% and 28% of the myths. A first look at the relations recorded for the acts in each sphere's events (2026-10-21, exploratory) finds villain events mostly enemy (41%), donor events mostly stranger (37%, ally 17%), and the most stated rank in the dispatcher's (above and below together 21%, kin 20%).

### `villain`

- **Symbols:** A H Pr
- **From Propp:** p.79: villainy, a fight or other struggle with the hero, pursuit.
- **Measured:** see above.
- **Literal meaning:** The one who does the harm, fights the hero, and gives chase.
- **Social norm:** Do not harm, steal or deceive. Whoever does becomes the enemy and will be defeated.
- **Cultural meaning:**

### `donor`

- **Symbols:** D F
- **From Propp:** p.79: the preparation for the transmission of a magical agent, and the provision of the hero with it.
- **Measured:** see above; donor events are mostly between strangers, before the gift.
- **Literal meaning:** The one who tests the hero and gives the means.
- **Social norm:** Those older or stranger than you may be testing you; meet them well. Those who have the means should reward the worthy generously.
- **Cultural meaning:**

### `helper`

- **Symbols:** G K Rs N T
- **From Propp:** p.79: spatial transference of the hero, liquidation of misfortune or lack, rescue from pursuit, the solution of difficult tasks, transfiguration of the hero.
- **Measured:** see above.
- **Literal meaning:** The one who carries, saves and does what the hero cannot.
- **Social norm:** No one succeeds alone. Loyal help is the duty of friends and allies, and it is given to those who deserve it.
- **Cultural meaning:**

### `princessAndFather`

- **Symbols:** M J Ex Q U W
- **From Propp:** pp.79-80: the assignment of difficult tasks, branding, exposure, recognition, punishment of a second villain, marriage; the princess and her father cannot be exactly told apart by functions, and most often it is the father who sets the tasks, from hostility to the suitor, and who punishes the false hero.
- **Measured:** see above.
- **Literal meaning:** The sought-for person, and the one who rules over her.
- **Social norm:** Those in power must test claimants fairly, reward true merit, and punish impostors. The hand of the princess goes to the deserving, not the boastful.
- **Cultural meaning:**

### `dispatcher`

- **Symbols:** B
- **From Propp:** p.80: dispatch, the connective incident.
- **Measured:** see above; the sphere with the most stated rank and kinship.
- **Literal meaning:** The one who sends the hero out.
- **Social norm:** Those in authority should call on the able to serve the community, and the able should answer when called.
- **Cultural meaning:**

### `hero`

- **Symbols:** C ↑ E W*
- **From Propp:** p.80: departure on a search, reaction to the demands of the donor, wedding; departure is characteristic of the seeker-hero, and the victim-hero performs only the rest.
- **Measured:** see above.
- **Literal meaning:** The one the tale follows.
- **Social norm:** Be the one who goes out, behaves well, and earns success. The humble and the overlooked may rise.
- **Cultural meaning:**

### `falseHero`

- **Symbols:** C ↑ E L
- **From Propp:** p.80: departure on a search, followed by the reaction to the donor and, as his own function, unfounded claims.
- **Measured:** see above; rare in every genre (2% to 16% of stories), commonest in the wondertales.
- **Literal meaning:** The one who claims the hero's due.
- **Social norm:** Do not pretend to be what you are not. The impostor is exposed and falls lowest of all.
- **Cultural meaning:**

## Elements that are not functions

**Propp names elements of form that are not functions of the dramatis personae** (chapters IV, V, VII and VIII). They are not coded as functions in this project's transcriptions; where the transcribers met them, they mostly coded X.

### `assimilation`

- **From Propp:** ch. IV, p.66: cases where one act has the double morphological meaning of two functions, and is read by its consequences.
- **Measured:** not measured.
- **Literal meaning:** One act doing the work of two.
- **Social norm:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `connective`

- **From Propp:** ch. V A, p.71: auxiliary elements that tie functions together, such as the information that passes between characters; the dispatch is the connective incident (p.36).
- **Measured:** not measured as such; part of the events coded X.
- **Literal meaning:** How one function leads to the next.
- **Social norm:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `trebling`

- **From Propp:** ch. V B, p.74: the repetition of a function or a sequence three times, with its own auxiliary elements.
- **Measured:** not measured.
- **Literal meaning:** The same thing done three times.
- **Social norm:** Persevere: success often comes on the third attempt, and the youngest of three, or the third to try, is the one who succeeds.
- **Cultural meaning:** See the variable scheme above, and Dundes on the number three.

### `motivation`

- **From Propp:** ch. V C, p.75: the reasons and aims of the characters that cause them to act.
- **Measured:** not measured.
- **Literal meaning:** Why a character acts.
- **Social norm:** The tale judges acts by their motives: greed, envy and malice lead to villainy, need and loyalty to heroism.
- **Cultural meaning:**

### `entranceOfCharacters`

- **From Propp:** ch. VII, p.85: the ways in which each character is introduced into the course of action.
- **Measured:** not measured.
- **Literal meaning:** How each character comes on stage.
- **Social norm:** None of its own: a device of telling, not of conduct.
- **Cultural meaning:**

### `attributes`

- **From Propp:** ch. VIII: the attributes of the dramatis personae, their appearance, age, sex, situation and the like, which vary while the functions stay.
- **Measured:** not measured.
- **Literal meaning:** What a character is like, apart from what it does.
- **Social norm:** Do not judge by appearance. The humble, the youngest, or the fool may prove to be the hero.
- **Cultural meaning:**

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
- **Social norm:** Do not yield to bullying, but take warnings seriously: a threat ignored may be carried out. Resisting together is safer than giving in alone.
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
- **Social norm:** Answer a request as your place requires: grant what those in need ask, obey a rightful superior, and deal fairly with equals. Refusal and evasion have consequences.
- **Cultural meaning:** The cultural meaning depends on the characters involved, but it ends in cooperation, resistance, or evasion. Cooperation can hold up the ideal of noble clemency, cooperation among equals, or obedience to a superior, outcomes that keep the social order as it stands. Resistance gives a reason for conflict. Evasion looks like delay but can become a defection and lead to conflict.

### `oath`, `prayer`, `curse`

- **Symbols:** the free verbs swear and vow, pray, and curse; in the act layer most fall under `decide`, `plead` and `harm`.
- **From Propp:** none, not in his list. Found in tragedy alone (`Cand/`, the free verbs of the Greek tragedies); not tested in the other genres.
- **Links:** not measured.
- **Measured:** in tragedy's free verbs four to five times their share in the tales, on eight plays never described before (`Cand/`); each in six to eight of the eight plays. Tragedy's own devices: a vow binds the future, a prayer appeals to the gods, a curse calls harm down.
- **Literal meaning:** An oath is a declaration of intent to follow a single course.

  A prayer is a way around the ordinary order, seeking an outside intervention, not from a helper but from a god.

  A curse is a hidden, slow-burning form of villainy, which promises a future lack or punishment.

- **Social norm:** Keep your word. Humble yourself before the gods. Harm done to the helpless calls down retribution.

- **Cultural meaning:** An oath can be read as putting honor above personal safety. A broken oath can upset the social balance and bring ruin on later generations.

  A prayer can be read as the last appeal of the helpless, and as saying that earthly rank is not final.

  A curse can be read as the victim's voice made lasting: a warning that harm done will have consequences in the future.

## Candidates, not yet tested

**Devices proposed from other scholars' work or from this project's first looks, kept here until a frozen test admits or rejects them.** Their productions, where written, are in `StoryGrammar/Candidates.md`.

### `Consequence`, `AttemptedEscape`, `ExplanatoryMotif`

- **From:** Dundes, The Morphology of North American Indian Folktales (dissertation, 1962; published 1964), whose motifemes otherwise re-cut Propp's pairs and say so: Lack and Lack Liquidated (Propp's a and K), Interdiction and Violation (γ δ), Task and Task Accomplished (M N), Deceit and Deception (η θ). These three are his own: the Consequence of a violation, an optional Attempted Escape from it, and the Explanatory Motif, a closing "that is why" that ends many tales.
- **Measured:** not measured; the Native American corpus is not yet assembled (`ProppQueue.md`).
- **Literal meaning:**
- **Social norm:** Every violation has its consequence, and escape seldom succeeds. The world is as it is because of what was done in the beginning.
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
- **Social norm:** Do not rest until the wrong is set right.
- **Cultural meaning:** This sequence runs from the misfortune that sets the story going to the restoring of order. It can be read as assuring the community that it has the values and the heroes it needs to heal itself after a misfortune, and as holding up the ideal that individual strength must in the end serve the group.

### ↑ to ↓

- **Joins:** departure and return.
- **From Propp:** not stated as a link. He describes the return (p.55) and adds that it is generally made in the same forms as the hero's arrival, but he does not name departure and return a pair.
- **Measured:** followed by ↓ in 32% and 39% of tale moves, above chance; 10% and 7% of fable moves; 14% and 14% of tragedy moves, not above chance; 57% of Propp's own (`Links/PostHoc.txt`, the reader mended).
- **Literal meaning:** Going out and coming back.
  The hero who leaves is expected home again, though a hero may stay where the quest led.
- **Social norm:** Go out into the world, but come back to serve your own people.
- **Cultural meaning:** These passages can be read as the shape of growing up: real change asks for a time away from the comfort of home. In some tales the return never comes, and that is the start of a new life in a new home.

### H to I

- **Joins:** struggle and victory.
- **From Propp:** p.64: struggle and victory are among the functions "arranged in pairs."
- **Measured:** followed by I in 86% and 86% of tale moves, 64% and 70% of fable moves, 85% and 64% of tragedy moves, and all of Propp's; above chance in all.
- **Literal meaning:** The fight is won.
  A fight once begun is expected to end in the villain's defeat, however long it takes.
- **Social norm:** Once you take up a fight, see it through.
- **Cultural meaning:** This sequence is the direct, high-stakes confrontation with the source of the harm. Some troubles cannot be met by cleverness or by giving way; the struggle is the moment the hero must face the threat head on. The victory means something because the danger was real. It can be read as a trial like those of the old initiation rites, turning the hero from a protected child into a protector of the community.

### M to N

- **Joins:** difficult task and solution.
- **From Propp:** not in his list of pairs (p.64); he defines the task (p.60) and the solution (p.62) and places them together in the variable scheme (pp.104-105).
- **Measured:** followed by N in 81% and 86% of tale moves, 62% and 60% of fable moves, 50% and 67% of the few tragedy moves (6 and 3), and all of Propp's.
- **Literal meaning:** The task is done.
  A task once set is expected to be solved, with other acts between.
- **Social norm:** Finish what you undertake.
- **Cultural meaning:** This sequence matches Greimas's glorifying test of the hero. He shows, sometimes for the third time, that he has the wit to be a hero. Accepting the task shows his willingness to be tested, and the solution shows him ready for what comes. Because the test is public, the community can see that the hero has earned his place.

### J to Q

- **Joins:** branding and recognition.
- **From Propp:** p.62: when the hero is recognized by a mark, a brand or a thing given him, "recognition serves as a function corresponding to branding and marking."
- **Measured:** too rare to test in the transcriptions (2 to 6 moves with J); in Propp's own, 3 of 3.
- **Literal meaning:** The mark that proves.
  The wound or token the hero receives is what later shows who the hero is.
- **Social norm:** Your deeds identify you; true worth will be recognized.
- **Cultural meaning:** This sequence shows that the scars or tokens of the struggle identify the hero, and set him apart from the false hero. The mark can also be read as a sign of higher standing, like the marks of old initiation rites, showing that the hero has passed into a later stage of life.

### L to Ex

- **Joins:** unfounded claims and exposure.
- **From Propp:** not stated as a link. He says exposure is "in most cases, connected with the one preceding" (p.62), that is, with recognition, not with the false claim.
- **Measured:** followed by Ex in 44% and 57% of tale moves, 74% and 43% of fable moves, and 67% of Propp's; too rare in tragedy.
- **Literal meaning:** The lie found out.
  A false claim is expected to be exposed before the end.
- **Social norm:** Lies are found out. Do not claim what is not yours.
- **Cultural meaning:** This sequence, and the false hero as a sphere of action, hold up the injunction against lying and bearing false witness. One reading, the owner's and still to be tested (`ProppQueue.md` item (k)), is that the false hero stands even lower in the tale's social order than the villain.

### D and E to F

- **Joins:** test and reaction, and the gift.
- **From Propp:** p.65: "Elements DEF also form something of a whole."
- **Measured:** followed by F in 68% and 76% of tale moves, 17% and 8% of fable moves, 67% and 50% of tragedy moves (6 each), and 84% of Propp's.
- **Literal meaning:** The answer earns the gift.
  How the hero meets the test decides whether help is given.
- **Social norm:** Kindness and respect toward a benefactor are rewarded. Keep faith with those who help you.
- **Cultural meaning:** This group holds the qualifying test (D E F in Propp's model), where the hero may perform an act of courtesy, such as sharing bread with an old man, and is given what he needs. It can be read as showing the importance of keeping faith with the donor: to cheat the donor would make the hero a villain.

### Pr to Rs

- **Joins:** pursuit and rescue.
- **From Propp:** p.64: pursuit and deliverance are among the functions "arranged in pairs."
- **Measured:** followed by Rs in 80% and 75% of tale moves, 44% and 14% of fable moves, 45% and 38% of tragedy moves, and 93% of Propp's.
- **Literal meaning:** The chase that ends in escape.
  A pursuit is expected to end with the hero saved.
- **Social norm:** Danger follows success. Accept help and keep moving until you are safe.
- **Cultural meaning:** This structural pair can be read as saying that the upheaval of the struggle brings a reaction of its own. The pursuit is the backlash against the hero, and warns the listener that the moment of greatest danger may come after the victory seems won.
