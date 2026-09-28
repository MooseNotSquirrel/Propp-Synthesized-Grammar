#!/usr/bin/env python3
"""
dispatch.py -- the dispatcher's one function, mediation B, by form.

  python dispatch.py            the table
  python dispatch.py --summary  one line, as StepTests.txt pins it

Propp gives the dispatcher's sphere the dispatch alone (p.80) and lists
seven forms of it (pp.36-38): a call for help, usually the tsar's, with
the hero sent in answer (B1); a direct dispatch, by command or request
(B2); leave to depart, where the initiative often comes from the hero and
not a dispatcher, and the parents bless (B3); the misfortune announced,
more often by old women or persons met by chance than by parents (B4);
the banished hero transported from home, by the father (B5); the hero
condemned to death secretly freed, by a cook or an archer (B6); a lament
(B7). B1-B4 belong to the seeker, B5-B7 to the victimized hero (p.37).

It reads ResolvedMoves.txt with heroType.py's reading rules, which are the
first project's ConsentClaim.md rules: a move's B is its first, and the
superscript is the form. A cell written with a raised B, at 144 I, 163 I
and 164 II, is function B discharged in another function's form (p.67;
falsify44.py's column tags) and carries no form digit; it is counted
apart. It also reports which moves carrying B the grammar rejects, since
the catalog's Corpus figures count only the moves v46 accepts.
"""
import collections
import sys

import heroType as H
import runCorpus as R

GRAMMAR = 'ProppEBNF46.txt'
FORMS = [('1', 'called'), ('2', 'sent'), ('3', 'allowed'), ('4', 'told'),
         ('5', 'transported'), ('6', 'freed'), ('7', 'lamented')]


def tally(grammar=GRAMMAR):
    forms, other, moves = collections.Counter(), [], set()
    for tale, mv, move in H.load():
        toks = H.parse(move)
        bases = [b for b, _ in toks]
        if 'B' not in bases:
            continue
        moves.add((tale, mv))
        var = toks[bases.index('B')][1]
        if var is None:
            other.append('%s %s' % (tale, mv))
        else:
            forms[var] += 1
    rejected = ['%s %s' % (r[0], r[1]) for r in R.run(grammar, 'move')
                if not r[3] and (r[0], r[1]) in moves]
    return forms, other, rejected, len(moves)


def summary():
    forms, other, rejected, n = tally()
    fs = ', '.join('%s %d' % (name, forms[d]) for d, name in FORMS)
    return ('B in %d moves: %s, in another form %d (%s); v46 accepts %d, rejecting %s'
            % (n, fs, len(other), ', '.join(other), n - len(rejected), ', '.join(rejected)))


def main(argv):
    if argv == ['--summary']:
        print(summary())
        return 0
    forms, other, rejected, n = tally()
    print('moves carrying B: %d' % n)
    for d, name in FORMS:
        print('  B%s %-12s %2d' % (d, name, forms[d]))
    print('  in another form: %s' % ', '.join(other))
    print('rejected by %s: %s' % (GRAMMAR, ', '.join(rejected)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
