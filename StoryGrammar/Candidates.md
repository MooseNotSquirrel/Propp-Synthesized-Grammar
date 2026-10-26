# Candidate productions for the probabilistic story grammar

**A holding file, not a grammar.** Productions proposed for the probabilistic story grammar (a weighted-constraint grammar), kept here until that grammar is designed and frozen. Nothing here is in `ProppEBNF46.txt`, by the owner's decision of 2026-10-21: v46 stays Propp's grammar with its two commented-out extensions (Dundes's and tragedy's), and new parts wait for the probabilistic grammar. Each entry gives the productions, where they came from, what the data shows so far, and what a frozen test must settle. The productions say what can occur; how often belongs to the grammar's weights.

## The threat group

**Proposed 2026-10-21 by the owner and the keeper** (the catalog's `ThreatAndDemand`, `SemanticCatalog.md`).

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

## The request group, and the threat as one of its forms

**Proposed 2026-10-22 by the owner** (the catalog's `RequestAndAnswer`): a request comes from a higher-status character, between equals, or from a lower-status one, and has the same three answers as a threat.

```
RequestGroup = Request , Answer , [ Consequence ] ;
Request      = Command | Proposal | Plea ;      (* from above, between equals, from below *)
Answer       = Accept | Reject | Evade ;
Consequence  = CarriedOut | Averted ;
```

- **Status as a condition on the weights, not a production of its own:** the three requests share one shape; who asks shifts how often each answer and each consequence follows.
- **The threat as a request with its sanction stated:** a demand is a request from above, and a threat names what follows refusal, so `ThreatGroup` above may be this group with a stated `Consequence`, the owner's two pairs one device. To be settled by the frozen test, not assumed.
- **Exploratory, 2026-10-22** (the tables; `plead` acts, by the relation the describers recorded; the next act by the one asked, within five acts, matched by name): between equals or with no rank recorded, 964 pleas, answered by respond 33%, no reply 29%, give 5%; from below, 101, respond 30%, no reply 17%, forbid 10%, give 8%, harm 6%; from above, only 33. **The act list already splits requests by status:** a request from above is mostly coded as an order (`send`, `forbid`, `set-task`), not as `plead`, so a test must gather all three acts as requests and use the relation for status.
- **For a frozen test:** as for the threat group, `respond` holds both acceptance and refusal, so the answer is coded from the free verbs.
