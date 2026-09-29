#!/usr/bin/env python3
"""
agreeApollodorus.py -- how far the two transcriptions agree.

  python agreeApollodorus.py WORK

Written after the scoring run, since scoreApollodorus.py left the agreement
the protocol asks for uncomputed; it reads the same Notes.txt records and
touches no verdict. For each scored episode version it compares transcriber
A's and B's entries: identical sequences, normalized edit distance, shared
identical move strings, and, event by event, whether the two gave the same
set of symbols and, where both gave a function, whether they share one.
"""
import sys

import scoreApollodorus as S


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def main(work):
    EA, _ = S.load_notes(work, 'A')
    EB, _ = S.load_notes(work, 'B')
    order = lambda es: sorted(es, key=lambda e: (S.roman(e['move']), e['pos']))
    same = 0
    dists, mA, mB, mSame = [], 0, 0, 0
    ev_same = ev_tot = both = agree = 0
    for ep, n, heroes in S.scored_episodes():
        for vid, hero, w in S.versions(ep, heroes):
            a = [S.base(e['sym']) for e in order(EA[vid])]
            b = [S.base(e['sym']) for e in order(EB[vid])]
            same += a == b
            dists.append(ed(a, b) / max(len(a), len(b), 1))
            ma = {tuple(S.base(e['sym']) for e in m) for m in S.moves_of(EA[vid])}
            mb = {tuple(S.base(e['sym']) for e in m) for m in S.moves_of(EB[vid])}
            mA, mB, mSame = mA + len(ma), mB + len(mb), mSame + len(ma & mb)
            byA, byB = {}, {}
            for e in EA[vid]:
                byA.setdefault(e['ev'], set()).add(S.base(e['sym']))
            for e in EB[vid]:
                byB.setdefault(e['ev'], set()).add(S.base(e['sym']))
            for i in range(1, n + 1):
                sa, sb = byA.get(i, set()), byB.get(i, set())
                ev_tot += 1
                ev_same += sa == sb
                fa, fb = sa - {'X'}, sb - {'X'}
                if fa and fb:
                    both += 1
                    agree += bool(fa & fb)
    print('episode versions with identical entry sequences: %d of %d' % (same, len(dists)))
    print('mean normalized edit distance per episode: %.2f' % (sum(dists) / len(dists)))
    print('moves: A %d, B %d; identical move strings shared: %d' % (mA, mB, mSame))
    print('events with the same set of symbols: %d of %d (%.1f%%)' % (ev_same, ev_tot, 100.0 * ev_same / ev_tot))
    print('events both gave a function: %d; of those, sharing a symbol: %d (%.1f%%)' % (both, agree, 100.0 * agree / both))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
