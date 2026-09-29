#!/usr/bin/env python3
"""
driftApollodorus.py -- EXPLORATORY, written after the Apollodorus test ran.
It revises no verdict. It measures how far the Greek moves stand from the
Russian ones, three ways:

  inventory  the share of each function among all entries, Russian against
             Greek, and the Jensen-Shannon divergence between them;
  order      the inversion rate of each move against Propp's numbering of
             the functions (beta 1 ... W 31, A and a 8): the share of
             ordered pairs that run backward, Russian, Greek, and each
             Greek move shuffled with its opener kept first;
  deletions  the fewest entries that must be deleted before
             ProppEBNF46.txt accepts the move (up to 4), and which
             functions are deleted most often. A move with no villainy,
             lack or mediation cannot be repaired by deletion and is
             counted apart.

  python driftApollodorus.py WORK
Russian moves are ResolvedMoves.txt, each brace expansion counted with
weight 1/k; Greek moves are the primary derivation of scoreApollodorus.py
(doubtful entries kept, grammar as shipped), weighted as it weighs them.
"""
import collections
import itertools
import math
import random
import sys

import scoreApollodorus as S  # sets the path to the grammar tools
import parse  # noqa: E402
import runCorpus as R  # noqa: E402
import shuffleBaseline as SB  # noqa: E402

NUM = {'β': 1, 'γ': 2, 'δ': 3, 'ε': 4, 'ζ': 5, 'η': 6, 'θ': 7, 'λ': 7.5, 'A': 8, 'a': 8, 'B': 9, 'C': 10,
       'up': 11, 'D': 12, 'E': 13, 'F': 14, 'G': 15, 'H': 16, 'J': 17, 'I': 18, 'K': 19, 'down': 20,
       'Pr': 21, 'Rs': 22, 'o': 23, 'L': 24, 'M': 25, 'N': 26, 'Q': 27, 'Ex': 28, 'T': 29, 'U': 30, 'W': 31}


def russian():
    out = []
    for m in R.F.load('ResolvedMoves.txt'):
        exps = [list(x) for x in R.expansions(R.elements(m['canon']))]
        out += [(x, 1.0 / len(exps)) for x in exps]
    return out


def greek(work, lineage):
    ents, _ = S.load_notes(work, lineage)
    out = []
    for ep, n, heroes in S.scored_episodes():
        for vid, hero, w in S.versions(ep, heroes):
            out += [(k, w) for k, st in S.derive(ents.get(vid, []), hero, False, False) if k]
    return out


def inventory(moves):
    c = collections.Counter()
    for k, w in moves:
        for x in k:
            c[x] += w
    tot = sum(c.values())
    return {x: v / tot for x, v in c.items()}


def jsd(p, q):
    keys = set(p) | set(q)
    m = {k: (p.get(k, 0) + q.get(k, 0)) / 2 for k in keys}
    kl = lambda a: sum(a.get(k, 0) * math.log2(a.get(k, 0) / m[k]) for k in keys if a.get(k, 0))
    return (kl(p) + kl(q)) / 2


def inversions(moves):
    inv = pairs = 0.0
    for k, w in moves:
        ns = [NUM[x] for x in k if x in NUM]
        for i, j in itertools.combinations(range(len(ns)), 2):
            if ns[i] != ns[j]:
                pairs += w
                inv += w * (ns[i] > ns[j])
    return inv / pairs if pairs else 0.0


def deletions(moves, g, cap=4):
    dist = collections.Counter()
    deleted = collections.Counter()
    for k, w in moves:
        if not any(x in ('A', 'a', 'B') for x in k):
            dist['no opener'] += w
            continue
        found = None
        for d in range(0, cap + 1):
            for drop in itertools.combinations(range(len(k)), d):
                keep = [x for i, x in enumerate(k) if i not in drop]
                if parse.accept(keep, g.bnf, g.start, g.table)[0]:
                    found = drop
                    break
            if found is not None:
                break
        if found is None:
            dist['more than %d' % cap] += w
        else:
            dist[len(found)] += w
            for i in found:
                deleted[k[i]] += w / max(1, 1)
    return dist, deleted


def shuffled(moves, seed=46):
    rng = random.Random(seed)
    return [(SB.fixed(rng, list(k)), w) for k, w in moves]


def show_dist(name, dist):
    tot = sum(dist.values())
    order = [0, 1, 2, 3, 4, 'more than 4', 'no opener']
    print('  %-22s %s' % (name, '  '.join('%s: %4.1f%%' % (o, 100 * dist.get(o, 0) / tot) for o in order)))


def main(work):
    g = S.grammar_for(False)
    ru = russian()
    gr = {L: greek(work, L) for L in 'AB'}
    pr = inventory(ru)
    print('INVENTORY: share of entries per function (Russian | Greek A | Greek B)')
    ga, gb = inventory(gr['A']), inventory(gr['B'])
    keys = sorted(set(pr) | set(ga) | set(gb), key=lambda x: NUM.get(x, 99))
    for x in keys:
        print('  %-5s %5.1f%% | %5.1f%% | %5.1f%%' % (x, 100 * pr.get(x, 0), 100 * ga.get(x, 0), 100 * gb.get(x, 0)))
    print('  Jensen-Shannon divergence (bits, 0 same, 1 disjoint): Russian-A %.3f, Russian-B %.3f, A-B %.3f'
          % (jsd(pr, ga), jsd(pr, gb), jsd(ga, gb)))
    print('ORDER: share of ordered pairs running backward against Propp\'s numbering')
    print('  Russian %.1f%%; Greek A %.1f%%, shuffled %.1f%%; Greek B %.1f%%, shuffled %.1f%%; Russian shuffled %.1f%%'
          % (100 * inversions(ru), 100 * inversions(gr['A']), 100 * inversions(shuffled(gr['A'])),
             100 * inversions(gr['B']), 100 * inversions(shuffled(gr['B'])), 100 * inversions(shuffled(ru))))
    print('DELETIONS: fewest entries deleted before v46 accepts the move')
    for name, mv in (('Russian', ru), ('Greek A', gr['A']), ('Greek A shuffled', shuffled(gr['A'])),
                     ('Greek B', gr['B']), ('Greek B shuffled', shuffled(gr['B']))):
        dist, deleted = deletions(mv, g)
        show_dist(name, dist)
        if not name.endswith('shuffled') and name != 'Russian':
            tot = sum(deleted.values())
            print('      most deleted: %s' % ', '.join('%s %.0f%%' % (x, 100 * v / tot) for x, v in deleted.most_common(10)))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
