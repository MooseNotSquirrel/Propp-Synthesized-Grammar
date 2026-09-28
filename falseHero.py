#!/usr/bin/env python3
"""
falseHero.py -- how the tales treat the false hero.

  python falseHero.py            the table
  python falseHero.py --summary  one line, as StepTests.txt pins it

The false hero's one specific function is L, unfounded claims (p.80). For
every tale in ResolvedMoves.txt with an L, it reports whether the claim
stands in the tale's last move, and whether the moves holding it also hold
punishment U, the wedding W, recognition Q and exposure Ex; and, over the
move-strings holding an L, how many also hold the unrecognized arrival o,
the o-L pairing of p.104.

Tales 125 and 155 carry a shared ending, which resolve.py copies onto each
sharing move; 125's L stands in that ending, so it is counted once, for the
tale. Moves are read as runCorpus.py reads them, every brace expanded.
"""
import collections
import sys

import runCorpus as R


def tally(moves='ResolvedMoves.txt'):
    tales = collections.OrderedDict()
    strings_with_l = strings_with_o = 0
    for m in R.F.load(moves):
        keys = set(k for x in R.expansions(R.elements(m['canon'])) for k in x)
        tales.setdefault(m['tale'], []).append(keys)
        if 'L' in keys:
            strings_with_l += 1
            strings_with_o += 'o' in keys
    rows = []
    for tale, mv in tales.items():
        with_l = [k for k in mv if 'L' in k]
        if not with_l:
            continue
        held = set().union(*with_l)
        rows.append((tale, 'L' in mv[-1], *[f in held for f in ('U', 'W', 'Q', 'Ex')]))
    return rows, strings_with_l, strings_with_o


def summary():
    rows, sl, so = tally()
    n = len(rows)
    count = lambda i: sum(r[i] for r in rows)
    return ('tales %d (%s): last move %d, U %d, W %d, Q %d, Ex %d; o with L in %d of %d move-strings'
            % (n, ' '.join(r[0] for r in rows), count(1), count(2), count(3), count(4), count(5), so, sl))


def main(argv):
    if argv == ['--summary']:
        print(summary())
        return 0
    rows, sl, so = tally()
    print('tale  last-move  U  W  Q  Ex')
    for r in rows:
        print('%-5s %-10s %s' % (r[0], 'yes' if r[1] else 'no',
                                 '  '.join('y' if x else '-' for x in r[2:])))
    print('o with L in %d of %d move-strings' % (so, sl))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
