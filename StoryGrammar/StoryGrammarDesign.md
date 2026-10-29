# The probabilistic story grammar: how it works

*A plain-language account of the grammar built and frozen on 2026-10-28, for a reader who is not a specialist. The exact decisions are in `StoryGrammarProtocol.md`, the code in `storyGrammar.py`, the fitted grammar in `Weights-A.txt` and `Weights-B.txt`, and its scores in `StoryGrammarRun.txt`.*

## 1. The idea in one paragraph

Vladimir Propp found that Russian wondertales are built from a small stock of plot events, which he called *functions*: a villain does harm, the hero sets out, a donor tests the hero and gives a magic gift, the hero fights the villain and wins, and so on. Each has a letter. He also found that the functions come in a fairly fixed order.

Our earlier grammar (`ProppEBNF46.txt`) states that order as hard rules: a sequence of letters is either allowed or not. Real stories, though, bend the rules. Fables are short, tragedies end badly, and myths wander.

The probabilistic story grammar replaces "allowed or not" with "how well-formed". Each of Propp's rules becomes a **constraint** that a story may break, at a **cost**. The cost of breaking each rule is not decided by us; it is learned from the stories themselves. A rule the stories almost never break gets a high cost; a rule they break freely gets a low cost, or even a negative one. The set of costs *is* the grammar.

Linguists call this a *maximum-entropy grammar*, or a grammar of weighted constraints. The same idea is used for sound patterns in languages, where some combinations are common, some rare, and none strictly forbidden.

## 2. What the grammar reads

**A story is turned into a string of Propp's letters.** Two blind transcribers, A (Claude Opus) and B (Claude Sonnet), each wrote down, for every event in every story, which of Propp's functions it fulfils. They did this separately, without seeing each other's work. The grammar is fitted for each transcriber apart, so that every result can be checked twice.

**Only the functions that matter are kept.** The transcribers marked each entry Y or N, for whether it matters to the course of the tale; the grammar keeps the Y entries, and drops events that fulfil no function (marked X). The myths carry no such mark, so all their entries are kept.

**The string is divided into moves.** A *move* is Propp's word for one complete round of plot, from a harm or a lack to its repair. Many tales have more than one. Each letter keeps the move it belongs to.

**Stories of fewer than three functions are left out,** as the earlier constraint grammar left them out: there is too little order in them to judge.

**The corpora:**

| Corpus | Stories with functions |
|---|---|
| Russian wondertales (Afanasyev) | 45 |
| Russian animal tales (Afanasyev) | 50 |
| Aesop's fables | 198 |
| Greek tragedies | 32 |
| Greek myths (Apollodorus's *Library*) | 126 |

**Two choices about the data:**
- *The myths* are the 126 stories of the *Library* proper. The *Epitome*'s stories, which also sit in the tables, are not part of this corpus, as the protocol counted it.
- *Versions:* where a transcriber gave a story more than one version (for instance, one per possible hero), each version counts, but the versions of one story share one story's weight between them.

## 3. The central trick: a story against its own shuffles

How can one learn what makes a story well-formed, when there are only a few hundred stories?

The grammar does not try to learn how to write a story from nothing, letter by letter. That would need far more stories than exist in these corpora. Instead it asks a narrower question:

> Given the functions this story actually has, why are they in *this* order and not another?

For each real story, the program makes **alternatives**: near-copies of the story that are a little wrong. There are three kinds, chosen at random with equal chances:
1. **A reordering:** the same functions, shuffled within each move. A move's functions stay in that move; only their order changes.
2. **A reordering with one function dropped.**
3. **A reordering with one function added,** drawn from the functions that occur in that corpus's stories.

Each story gets 100 alternatives in fitting, and 200 when it is tested. The random choices come from fixed seeds, so that the same run always makes the same alternatives.

The grammar's costs are then fitted so that **the real story looks better-formed than its alternatives**, as often and as clearly as possible. This kind of model is called *contrastive*: it learns by contrast with what the story could have been. It is the method the earlier constraint grammar used (2026-10-06), extended.

## 4. The constraints: what the grammar measures

Each constraint is a way of counting how much a sequence breaks one of Propp's rules. A sequence gets a number for each, its **violation**: zero if it keeps the rule perfectly, larger the more it breaks it. Most are shares, so that long stories are not penalised merely for being long.

There are 80 constraints in seven groups.

**Group 1. The hard grammar (2 constraints).** Each move is checked against `ProppEBNF46.txt`, our formal grammar of Propp's move:
- *Move not accepted:* the share of the story's moves the grammar rejects.
- *Repairs per function:* if a move is rejected, the program deletes the function where the check fails, and tries again, until the move is accepted. The number of deletions, per function in the story, says how far the move is from a grammatical one.

  As the tragedy test did, the first move's opening scene-setting functions (Propp's "preparatory" functions, before the first harm or lack) are set aside before this check.

**Group 2. The order of the sections (45 constraints).** Propp's 31 functions fall into ten broad sections, in this order:

| Section | Functions |
|---|---|
| 1. Preparatory | absentation, interdiction and its violation, reconnaissance, delivery, trickery, complicity, the preliminary misfortune (β to θ, λ) |
| 2. Complication | villainy (A), lack (a), mediation (B), the hero's decision to act (C), departure (↑) |
| 3. Donor | the donor's test (D), the hero's reaction (E), the gift of a magic agent (F) |
| 4. Transfer | the hero led to the object of the search (G) |
| 5. Struggle | struggle (H), branding (J), victory (I) |
| 6. Liquidation | the harm or lack repaired (K) |
| 7. Return | return (↓), pursuit (Pr), rescue (Rs) |
| 8. Arrival and claims | unrecognised arrival (o), a false hero's claims (L) |
| 9. Task | a difficult task (M), its solution (N) |
| 10. Endgame | recognition (Q), exposure (Ex), transfiguration (T), punishment (U), wedding (W) |

For every pair of sections, one constraint counts how often a function of the later section comes *before* a function of the earlier one. Ten sections make 45 pairs. "Struggle before return", for instance, is broken each time a return comes before a struggle.

**Group 3. Order inside the sections (18 constraints).** Nine of Propp's pairs, each counted two ways:
- *Order:* the second before the first, as when the victory comes before the struggle.
- *Cohesion:* the two in the right order but not next to each other, as when the struggle and the victory are separated by other events.

Groups 2 and 3 are exactly the earlier constraint grammar, unchanged.

**Group 4. Propp's pairs within the move (12 constraints).** Twelve pairs that Propp says belong together:
- interdiction then violation;
- reconnaissance then delivery;
- trickery then complicity;
- test then reaction;
- reaction then gift;
- struggle then victory;
- pursuit then rescue;
- task then solution;
- villainy then repair;
- lack then repair;
- recognition then exposure;
- exposure then punishment.

For each pair, the constraint counts a first with no second after it in the same move, and a second with no first before it.

**Group 5. The blocks (1 constraint).** Propp's blocks are runs of functions that are told together as a unit, such as the donor sequence. The program finds them with the earlier `blockStream.py`, and counts the share of functions that fall outside any block.

**Group 6. The candidate groups (none, for now).** The owner proposed two new groupings: a threat or demand, then the answer, then the consequence; and the same for a request. They are waiting in `Candidates.md`. Propp's letters have no symbol for a threat, a demand or a request, so they cannot be counted from the functions. The protocol said they would be included only as far as the letters express them, so for now they wait.

**Group 7. Length (2 constraints), as a control.**
- the number of functions, divided by 10;
- the number of moves, divided by 10.

These are not claims about structure. They are in the model so that length cannot pass itself off as structure. An earlier model showed that length alone tells the genres apart almost as well as anything else.

## 5. The weights: one grammar shared, and each genre's departures

Each constraint gets a **weight**: how much breaking it costs.
- **A positive weight** means stories keep the rule: a sequence that breaks it scores as less well-formed.
- **A negative weight** means stories tend to break it.
- **Zero** means the rule makes no difference.

A sequence's **score** is the sum, over the 80 constraints, of weight times violation. Lower is better-formed.

**Shared weights plus offsets.** Each constraint has one **shared weight**, the grammar of the story language as a whole, plus an **offset** for each of the five corpora: how far that genre departs from the shared grammar. A fable's weights are the shared weights plus the fable offsets.

The offsets are penalised, so a genre departs from the shared grammar only where its own stories clearly demand it. That makes 80 shared weights and 5 × 80 offsets: 480 numbers for each transcriber.

**How the weights are fitted.** For each real story and each of its alternatives, the model gives the chance that the real story is the better-formed of the two. The chance depends on the difference in their scores, through the logistic curve: a large difference gives a chance near certainty, and no difference gives one half.

The weights are chosen to make these chances as high as possible across all the stories, a method called maximum likelihood. A fixed penalty, set before any fit, keeps any weight from growing larger than the evidence supports.

## 6. A design choice made along the way: putting the constraints on one scale

The first version failed its own self-test (test G1, section 8). Some constraints hardly ever differ between a story and its alternatives. For example, the order of the "transfer" section against the "arrival and claims" section differs by 0.0004 on average, against 0.27 for the blocks constraint.

On such a constraint, a weight can be large and still make almost no difference to any score. The fixed penalty then pushed those weights toward zero, and the self-test could not recover them.

**The amendment (section 10 of the protocol, at the owner's word):** each constraint is divided by its typical size, the average size of its difference between a story and its alternatives, measured on the fitting stories. This puts all 80 constraints on one scale, so the penalty treats them alike.

Weights are reported in these units, "per unit of spread", and also converted back to the raw scale. After the amendment the self-test passed. The failure stays in the record.

## 7. Fair testing: stories held back

**A fifth held out.** Before anything was fitted, a fifth of each corpus's stories was drawn at random by a fixed seed and set aside (`HeldOut.txt`). The grammar never saw them in fitting:

| Corpus | Held out |
|---|---|
| wondertales | 9 |
| animal tales | 10 |
| fables | 40 |
| tragedies | 6 |
| myths | 25 |

The grammar is then judged on how it handles stories it has never seen. A grammar that merely memorised its stories would fail this.

**The unseen cultures.** A larger test is still to come: 50 Native American and 50 East Asian tales. They are being transcribed now, after the grammar was frozen, so they are unseen by it in the strongest sense.

## 8. The self-tests, run before any result was read

- **G1. Can it find a grammar we planted?** We invented weights, generated stories that obey them, and fitted. The fit must recover the planted weights' order, with a rank correlation of at least 0.9, and at least 95% of their signs.
  - First run: 0.774, a FAIL (section 6).
  - After the amendment: 0.934, and 48 of 49 signs. PASS.
- **G2. Does it reproduce the earlier grammar?** Using only groups 2 and 3 and the 2026-10-06 data and settings, the program must reproduce the published weights of the constraint grammar exactly. PASS: all three genres, line for line.
- **G3. Were the held-out stories really unseen?** Their functions were replaced with random letters and the fit run again. The weights must come out identical, and they did. PASS.
- **G4. Is it repeatable?** Two runs gave byte-identical weights. PASS.

## 9. What it found

**Prediction 1, the held-out stories: HOLDS.** For each held-out story, the measure is the share of its 200 alternatives that score worse than the real story, called the **concordance**. Chance is 0.5.

| Corpus | Transcriber A | Transcriber B |
|---|---|---|
| wondertales | 0.986 | 0.994 |
| animal tales | 0.975 | 0.936 |
| fables | 0.849 | 0.885 |
| tragedies | 0.982 | 0.784 |
| myths | 0.799 | 0.855 |

In every corpus, for both transcribers, unseen real stories look better-formed than their shuffles. Every result is significant (p at most 0.031).

**Prediction 2, the genre beyond length: FAILS.** For each held-out story, we asked which genre's weights fit it best, and whether that names its genre.

| | The grammar | Length alone | Chance |
|---|---|---|---|
| A | 0.322 | 0.533 | 0.2 |
| B | 0.363 | 0.539 | 0.2 |

The grammar names the genre better than chance, but much worse than story length alone does. So the genres' weights do not tell the genres apart.

**What the strongest shared weights are** (reported, not tested): for both transcribers, Propp's pairs within the move (trickery then complicity, lack then repair, test then reaction, villainy then repair), the hard grammar's repairs, and keeping functions inside blocks. The length weights are small.

**A reading, not from Propp, and to be held loosely.** The story language looks like *one* grammar that all five corpora keep, rather than five genre grammars. What sets the genres apart is mostly how long their stories are.

## 10. What it is not, and what was not done

- **It does not write stories from scratch.** It judges an order against nearby alternatives. The protocol allowed a few sequences sampled from each genre's weights, as illustration only; the run did not produce them.
- **It has not been compared with Propp's plain numerical order.** The earlier constraint grammar was. So the high concordances show that the grammar beats shuffled versions of each story, not that it beats Propp's numbering.
- **One of its constraints disagrees with the transcription card.**
  - The card counts an order that is *obeyed* as an interdiction (γ) with no violation (δ), but Propp counts the obeyed order as the violation's inverted form (p. 27).
  - So the constraint "interdiction then violation" counts every obeyed order against a story. This is why one transcriber's reading of Euripides' *Helen*, full of commands that are obeyed, scores below its own shuffles.
  - The card is kept, at the owner's word, so that all the corpora stay comparable. The mend waits for a later version of the grammar.
- **Its readers are language models.** Their shared understanding is largely modern and Western. That is a risk to every cross-cultural reading here, and it is reported with every result.
- **It is frozen** (protocol section 11): the program at commit 422dff8, and the two weight files fixed by their hashes. No weight may be refitted or tuned. Its two remaining predictions will be scored on the new tales by a command written before their transcriptions are read:
  - 3: the unseen cultures' stories outscore their alternatives;
  - 4: the Native American tales less so than the East Asian, the owner's prediction.

## 11. The design choices, in one list

| Choice | Taken | Where |
|---|---|---|
| Contrastive, not generative | a story against its own reorderings, drops and additions | protocol §2, decision 1 |
| The seven groups of constraints | 80 constraints; the candidate groups wait | §3, decision 2 |
| Shared weights plus a penalised offset per genre | 480 weights per transcriber | §4, decision 3 |
| A fifth of each corpus held out, by a fixed seed | 90 stories | §5, decision 4; `HeldOut.txt` |
| Sampled stories as illustration only | allowed, not yet produced | decision 5 |
| Each transcriber fitted apart | A and B | §4 |
| Alternatives | 100 a story to fit, 200 to test; three kinds, equally likely | `storyGrammar.py` |
| The penalty's strength | 1.0, fixed before any fit | §2 |
| The myths | the *Library*'s 126, not the *Epitome* | the program's notes |
| Constraints standardised to one scale | after G1 first failed | §10 (amendment) |
| G1's sign rule | at least 95% of the planted weights of 0.5 or more | §10 |
| The fitted grammar frozen | program and weights by hash | §11 |
