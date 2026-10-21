#!/usr/bin/env python3
"""
links.py -- the links at a distance (LinksProtocol.md).

  python links.py score      writes Links/LinksRun.txt
  python links.py selftest   the statistic on planted and on random moves

Written in full before any link was counted.
"""
import collections
import glob
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, 'Data'))
import tables as DT  # noqa: E402

SEED, SHUFFLES = 46, 10000
# (name, the first function or functions, all of which must be present, and the second)
LINKS = [('A or a -> K', ('A|a',), 'K'), ('↑ -> ↓', ('↑',), '↓'), ('H -> I', ('H',), 'I'), ('M -> N', ('M',), 'N'),
         ('J -> Q', ('J',), 'Q'), ('L -> Ex', ('L',), 'Ex'), ('D and E -> F', ('D', 'E'), 'F'), ('Pr -> Rs', ('Pr',), 'Rs')]
MIN_MOVES = 5


# ---------------------------------------------------------------- the moves
def transcribed():
    """{reader: {genre: [list of base functions, one list a move]}}: the original transcriptions, signs dropped;
    read from the normalized tables (Data/tables.py), the files these patterns name"""
    pats = {'tale': ['Afanasyev/transcriptions/U/%s/b*/Notes.txt'],
            'fable': ['Aesop/transcriptions/%s/b*/Notes.txt', 'Fables/transcriptions/%s/b*/Notes.txt'],
            'tragedy': ['Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt']}
    out = {}
    for L in 'AB':
        out[L] = {}
        for g, ps in pats.items():
            moves = collections.OrderedDict()
            for r in DT.files('functions', ps, L):
                s = DT.local(r['story'])
                if not re.match(r'^[PFA]\d{2}', s):
                    continue
                b = TS.base(r['raw'])
                k = (s, r['move'])
                moves.setdefault(k, [])
                if b not in ('X', 'α', ''):
                    moves[k].append(b)
            out[L][g] = [m for m in moves.values() if m]
    return out


def propp_moves():
    """Propp's own 84 moves of Appendix III, through the corpus runner's reducer; a brace's rows in turn; the
    resolved moves read from the normalized tables (Data/tables.py, resolved)"""
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        import runCorpus as RC
        out = []
        for r in DT.rows('resolved'):
            keys = []
            for e in RC.elements(r['string']):
                if isinstance(e, list):
                    for row in e:
                        keys += row
                else:
                    keys.append(e)
            out.append([TS.base(k) for k in keys if k])
    finally:
        os.chdir(cwd)
    return out


# ---------------------------------------------------------------- the statistic
class Moves:
    def __init__(self, moves):
        self.moves = [m for m in moves if m]
        self.vocab = sorted({t for m in self.moves for t in m})
        self.index = {t: i for i, t in enumerate(self.vocab)}
        self.tok = np.array([self.index[t] for m in self.moves for t in m], dtype=np.int64)
        lens = np.array([len(m) for m in self.moves])
        self.starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
        self.pos = np.arange(len(self.tok))

    def hits(self, tok, firsts, second):
        """per move, whether the second function stands after every first one has appeared at least once"""
        big = len(tok) + 1
        anchor = np.full(len(self.moves), -1)
        present = np.ones(len(self.moves), dtype=bool)
        for alts in firsts:
            ids = [self.index[a] for a in alts.split('|') if a in self.index]
            is_x = np.isin(tok, ids) if ids else np.zeros(len(tok), dtype=bool)
            first = np.minimum.reduceat(np.where(is_x, self.pos, big), self.starts)
            present &= first < big
            anchor = np.maximum(anchor, first)
        if second not in self.index:
            return present, np.zeros(len(self.moves), dtype=bool)
        is_y = tok == self.index[second]
        last = np.maximum.reduceat(np.where(is_y, self.pos, -1), self.starts)
        return present, present & (last > anchor)

    def test(self, firsts, second, shuffles=SHUFFLES, seed=SEED):
        present, hit = self.hits(self.tok, firsts, second)
        obs = int(hit.sum())
        rng = np.random.default_rng(seed)
        null = np.empty(shuffles)
        for k in range(shuffles):
            null[k] = self.hits(rng.permutation(self.tok), firsts, second)[1].sum()
        p = (np.sum(null >= obs) + 1) / (shuffles + 1)
        return {'moves': len(self.moves), 'with first': int(present.sum()), 'hits': obs,
                'share': obs / present.sum() if present.sum() else float('nan'),
                'expected': null.mean(), 'lift': obs / null.mean() if null.mean() > 0 else float('nan'), 'p': p}


def fmt(r):
    return 'moves %4d, with the first %3d, second after it %3d (%.0f%%), expected %.1f, lift %.2f, p %.4f' % (
        r['moves'], r['with first'], r['hits'], 100 * r['share'] if r['with first'] else 0, r['expected'], r['lift'], r['p'])


def holds(r):
    return r['with first'] >= MIN_MOVES and r['lift'] > 1 and r['p'] <= 0.05


# ---------------------------------------------------------------- scoring
def score():
    T = transcribed()
    PR = Moves(propp_moves())
    rep = ['# LinksRun.txt -- links.py score, as LinksProtocol.md freezes it.', '',
           'For each link: the moves holding the first function (all of them, where two are named), the moves where the second stands after it, '
           'and the count expected when the genre\'s functions are shuffled across its moves, each move keeping its length (%d shuffles, seed %d).' % (SHUFFLES, SEED), '']
    res = {}
    for name, firsts, second in LINKS:
        rep.append(name)
        for g in ('tale', 'fable', 'tragedy'):
            for L in 'AB':
                r = Moves(T[L][g]).test(firsts, second)
                res[name, g, L] = r
                rep.append('  %-8s %s  %s%s' % (g, L, fmt(r), '  HOLDS' if holds(r) else ''))
        r = PR.test(firsts, second)
        res[name, 'propp'] = r
        rep.append('  %-8s %s  %s%s' % ('Propp', '-', fmt(r), '  HOLDS' if holds(r) else ''))
        rep.append('')
    n1 = sum(all(holds(res[name, 'tale', L]) for L in 'AB') for name, _, _ in LINKS)
    eligible = [name for name, _, _ in LINKS if res[name, 'propp']['with first'] >= MIN_MOVES]
    n3 = sum(holds(res[name, 'propp']) for name in eligible)
    akt = [res['A or a -> K', 'tale', L]['share'] for L in 'AB']
    akg = [res['A or a -> K', 'tragedy', L]['share'] for L in 'AB']
    rep += ['PREDICTIONS (LinksProtocol.md)',
            '  1. in the tales, at least six of the eight links hold for both transcribers: %d of 8 -> %s' % (n1, 'HOLDS' if n1 >= 6 else 'FAILS'),
            '  2. villainy or lack is followed by liquidation in a smaller share of moves in the tragedies than in the tales, for both transcribers: '
            'tales %.0f%% and %.0f%%, tragedies %.0f%% and %.0f%% -> %s' % (100 * akt[0], 100 * akt[1], 100 * akg[0], 100 * akg[1],
                                                                            'HOLDS' if all(akg[i] < akt[i] for i in range(2)) else 'FAILS'),
            '  3. in Propp\'s own moves, every link whose first function stands in at least %d moves holds: %d of %d -> %s'
            % (MIN_MOVES, n3, len(eligible), 'HOLDS' if eligible and n3 == len(eligible) else 'FAILS')]
    open(os.path.join(HERE, 'LinksRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def selftest():
    """planted: x and later y in half the moves; random: letters only. The planted link must hold and the random one not."""
    import random
    rnd = random.Random(3)
    letters = list('abcdefgh')
    planted, plain = [], []
    for k in range(80):
        m = [rnd.choice(letters) for _ in range(rnd.randint(4, 12))]
        plain.append(list(m))
        if k % 2 == 0:
            i = rnd.randrange(len(m))
            j = rnd.randrange(i, len(m))
            m.insert(i, 'X')
            m.insert(j + 2, 'Y')
        planted.append(m)
    r1 = Moves(planted).test(('X',), 'Y', shuffles=2000)
    r2 = Moves(plain).test(('a',), 'b', shuffles=2000)
    r3 = Moves(planted).test(('X', 'a'), 'Y', shuffles=2000)
    print('planted X -> Y:', fmt(r1), 'HOLDS' if holds(r1) else 'does not hold', '(want HOLDS)')
    print('random a -> b: ', fmt(r2), 'HOLDS' if holds(r2) else 'does not hold', '(want does not hold)')
    print('X and a -> Y:  ', fmt(r3), '(two firsts: counted only where both stand before Y)')
    print('Propp\'s moves read:', len(propp_moves()))


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
