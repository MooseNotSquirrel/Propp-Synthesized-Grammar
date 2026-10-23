# Candidate productions for the probabilistic story grammar

**A holding file, not a grammar.** Productions proposed for the probabilistic story grammar (a weighted-constraint grammar), kept here until that grammar is designed and frozen. Nothing here is in `ProppEBNF46.txt`, by the owner's decision of 2026-10-21: v46 stays Propp's grammar with its two commented-out extensions (Dundes's and tragedy's), and new parts wait for the probabilistic grammar. Each entry gives the productions, where they came from, what the data shows so far, and what a frozen test must settle. The productions say what can occur; how often belongs to the grammar's weights.

## The threat group

**Proposed 2026-10-21 by the owner and the keeper** (the catalog's `ThreatAndDemand`, `ProppPairsAndGroups.md`).

```
ThreatGroup = Threat , Answer , [ Consequence ] ;
Threat      = threaten | demand ;
Answer      = Comply | Defy | Evade ;
Defy        = harm | fight | refuse | ThreatGroup ;
Consequence = CarriedOut | Averted ;
```

- **Why three steps:** the owner's point that a threat or demand implies a follow-up. `Consequence` is kept in Dundes's sense, what follows the answer (the threat made good or averted), so that the group stays comparable with his Interdiction, Violation and Consequence; the answer itself is `Answer`.
- **Why `Defy` can be a new `ThreatGroup`:** threats answer threats (`XStudy/ThreatAndFall.txt`; 7% of the replies below), and the nesting is escalation.
- **Weights, not productions:** that defiance usually brings the threat carried out and compliance usually brings none is a tendency, for the grammar's weights.
- **Exploratory, 2026-10-21** (the tables, all described stories; the next act by the one threatened, within five acts, matched by name): of 488 threats, no reply 25%; plead 9%, respond 9%, threaten back 7%, harm 5%, deceive 5%, decide 4%, lose, escape, reveal-information and lament 2% to 3% each. So comply or submit (plead, lose, lament, part of respond), defy (threaten back, harm, part of respond) and evade (deceive, escape).
- **For a frozen test:** the act list's `respond` covers both yes and no, so the answer cannot be split into compliance and defiance from the act layer; code it from the free-verb layer (agree, obey, refuse).
