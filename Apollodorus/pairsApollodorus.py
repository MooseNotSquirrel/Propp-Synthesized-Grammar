#!/usr/bin/env python3
"""
pairsApollodorus.py -- EXPLORATORY, after the Apollodorus test. Propp's
pairs, Russian against Greek.

  python pairsApollodorus.py WORK

For each pair x -> y it gives, within a unit:
  follow   the share of x's that have a y somewhere after them;
  precede  the share of y's that have an x somewhere before them;
and the same two figures for the unit's entries shuffled (200 shuffles,
random.Random(46)), so that a figure can be read against chance.
Units are the move and the whole tale or episode. Russian tales are the
moves of ResolvedMoves.txt in order, each move's first brace expansion;
Greek episodes are the primary derivation of scoreApollodorus.py
(doubtful entries kept), weighted as it weighs them. Propp's move schemes
omit the preparatory functions, so the Russian corpus cannot show the
preparatory pairs; they are marked n/a.
"""
import collections
import random
import sys

import scoreApollodorus as S  # sets the path to the grammar tools
import runCorpus as R  # noqa: E402

PAIRS = [('γ', 'δ', 'interdiction, violation'), ('ε', 'ζ', 'reconnaissance, delivery'),
         ('η', 'θ', 'trickery, complicity'), ('D', 'E', "donor's test, hero's reaction"),
         ('H', 'I', 'struggle, victory'), ('Pr', 'Rs', 'pursuit, rescue'),
         ('M', 'N', 'difficult task, solution'), ('J', 'Q', 'branding, recognition'),
         ('L', 'Ex', 'false claim, exposure'), ('Aa', 'K', 'villainy or lack, liquidation'),
         ('up', 'down', 'departure, return')]
SHUFFLES = 200


def match(k, x):
    return k in ('A', 'a') if x == 'Aa' else k == x


def stats(units, x, y):
    fx = nx = py = ny = 0.0
    for keys, w in units:
        for i, k in enumerate(keys):
            if match(k, x):
                nx += w
                fx += w * any(match(j, y) for j in keys[i + 1:])
            if match(k, y):
                ny += w
                py += w * any(match(j, x) for j in keys[:i])
    return (fx / nx if nx else None, nx, py / ny if ny else None, ny)


def shuffled_stats(units, x, y, rng):
    acc = [0.0, 0.0]
    cnt = [0, 0]
    for _ in range(SHUFFLES):
        sh = []
        for keys, w in units:
            k = list(keys)
            rng.shuffle(k)
            sh.append((k, w))
        f, nx, p, ny = stats(sh, x, y)
        if f is not None:
            acc[0] += f
            cnt[0] += 1
        if p is not None:
            acc[1] += p
            cnt[1] += 1
    return (acc[0] / cnt[0] if cnt[0] else None, acc[1] / cnt[1] if cnt[1] else None)


def russian():
    moves, tales = [], collections.OrderedDict()
    for m in R.F.load('ResolvedMoves.txt'):
        k = next(iter(R.expansions(R.elements(m['canon']))))
        k = list(k)
        moves.append((k, 1.0))
        tales.setdefault(m['tale'], []).extend(k)
    return moves, [(k, 1.0) for k in tales.values()]


def greek(work, lineage):
    ents, _ = S.load_notes(work, lineage)
    moves, eps = [], []
    for ep, n, heroes in S.scored_episodes():
        for vid, hero, w in S.versions(ep, heroes):
            ks = [k for k, st in S.derive(ents.get(vid, []), hero, False, False) if k]
            moves += [(k, w) for k in ks]
            eps.append(([x for k in ks for x in k], w))
    return moves, eps


def pct(v):
    return '  n/a' if v is None else '%4.0f%%' % (100 * v)


def main(work):
    corpora = [('Russian', russian())] + [('Greek ' + L, greek(work, L)) for L in 'AB']
    for level, idx in (('WITHIN A MOVE', 0), ('WITHIN A TALE OR EPISODE', 1)):
        print(level)
        print('  %-32s %-9s %6s %6s %8s %8s %6s' % ('pair', 'corpus', 'x', 'follow', 'shuffled', 'precede', 'shuf.'))
        for x, y, name in PAIRS:
            for cname, units in corpora:
                u = units[idx]
                f, nx, p, ny = stats(u, x, y)
                if not nx and not ny:
                    print('  %-32s %-9s %6s %6s %8s %8s %6s' % (name, cname, '0', 'n/a', '', 'n/a', ''))
                    continue
                sf, sp = shuffled_stats(u, x, y, random.Random(46))
                print('  %-32s %-9s %6.0f %6s %8s %8s %6s' % (name, cname, nx, pct(f), pct(sf), pct(p), pct(sp)))
                name = ''
        print()
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
