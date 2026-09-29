#!/usr/bin/env python3
"""
shuffleBaseline.py -- how often does the grammar accept a move whose
functions are put in random order?

  python shuffleBaseline.py            the figures, and the moves most often
                                       accepted when shuffled
  python shuffleBaseline.py --summary  one line, as StepTests.txt pins it

A grammar that accepts 80 of 84 real moves says something about their
order only if it refuses most orderings of the same functions. This is the
baseline ApollodorusProtocol.md requires, with the parameters frozen in
ApollodorusPrediction.txt before it was written: ProppEBNF46.txt at
`move`, the 84 moves of ResolvedMoves.txt derived as runCorpus.py derives
them, 1000 shuffles per move from one random.Random(46) drawn in corpus
order. Each brace expansion of a move is shuffled independently, and the
shuffled move is accepted when every shuffled expansion is.

Two nulls. FULL shuffles every symbol. OPENER-FIXED keeps the expansion's
first A, a or B at the front and shuffles the rest; it is the harder test,
since a string that does not open on A, a or B fails trivially.
"""
import random
import sys

import runCorpus as R

GRAMMAR, START, SHUFFLES, SEED = 'ProppEBNF46.txt', 'move', 1000, 46
OPENERS = ('A', 'a', 'B')


def fixed(rng, x):
    i = next((n for n, k in enumerate(x) if k in OPENERS), None)
    if i is None:
        return full(rng, x)
    rest = x[:i] + x[i + 1:]
    rng.shuffle(rest)
    return [x[i]] + rest


def full(rng, x):
    x = list(x)
    rng.shuffle(x)
    return x


def tally():
    g = R.Grammar(GRAMMAR, START)
    memo = {}

    def ok(keys):
        k = tuple(keys)
        if k not in memo:
            memo[k] = g.accepts(list(k))
        return memo[k]

    rng = random.Random(SEED)
    rows = []
    for m in R.F.load('ResolvedMoves.txt'):
        exps = [list(x) for x in R.expansions(R.elements(m['canon']))]
        real = all(ok(x) for x in exps)
        hits = {'full': 0, 'fixed': 0}
        for _ in range(SHUFFLES):
            for name, how in (('full', full), ('fixed', fixed)):
                shuffled = [how(rng, list(x)) for x in exps]
                hits[name] += all(ok(x) for x in shuffled)
        rows.append((m['tale'], m['move'], real, hits['full'] / SHUFFLES, hits['fixed'] / SHUFFLES))
    return rows


def summary(rows=None):
    rows = rows or tally()
    n = len(rows)
    real = sum(r[2] for r in rows)
    mf = sum(r[3] for r in rows) / n
    mx = sum(r[4] for r in rows) / n
    return ('real %d/%d = %.1f%%; shuffled full %.1f%%, opener-fixed %.1f%%'
            % (real, n, 100.0 * real / n, 100 * mf, 100 * mx))


def main(argv):
    rows = tally()
    if argv == ['--summary']:
        print(summary(rows))
        return 0
    print(summary(rows))
    print('moves most often accepted when shuffled, opener fixed:')
    for r in sorted(rows, key=lambda r: -r[4])[:12]:
        print('  %4s %-10s real %-5s full %5.1f%%  opener-fixed %5.1f%%'
              % (r[0], r[1], r[2], 100 * r[3], 100 * r[4]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
