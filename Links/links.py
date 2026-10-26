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


# ---------------------------------------------------------------- parity (Data/ParityProtocol.md, frozen 2026-10-21)
PARITY = {'tale-U': ['Afanasyev/transcriptions/U/%s/b*/Notes.txt'], 'tale-C': ['Afanasyev/transcriptions/C/%s/b*/Notes.txt'],
          'animal': ['AnimalTales/transcriptions/%s/b*/Notes.txt']}
TIGHT = ('H -> I', 'M -> N', 'D and E -> F', 'Pr -> Rs')
FRAME = ('A or a -> K', '↑ -> ↓')
PARITY_OUT = os.path.join(ROOT, 'Data', 'Parity')


def parity_moves(corpus):
    """{reader: [list of base functions, one list a move]} for one corpus, read as transcribed() reads the others"""
    out = {}
    for L in 'AB':
        moves = collections.OrderedDict()
        for r in DT.files('functions', PARITY[corpus], L):
            s = DT.local(r['story'])
            if not re.match(r'^[PFA]\d{2}', s):
                continue
            b = TS.base(r['raw'])
            k = (s, r['move'])
            moves.setdefault(k, [])
            if b not in ('X', 'α', ''):
                moves[k].append(b)
        out[L] = [m for m in moves.values() if m]
    return out


def parity_selftest():
    """the parity reader on the wondertales on card U must give exactly the moves the published run read"""
    T, P = transcribed(), parity_moves('tale-U')
    ok = all(P[L] == T[L]['tale'] for L in 'AB')
    for L in 'AB':
        print('self-test %s: %d moves, %d functions, %s' % (L, len(P[L]), sum(map(len, P[L])), 'IDENTICAL' if P[L] == T[L]['tale'] else 'DIFFERS'))
    print('PARITY SELF-TEST PASSES' if ok else 'PARITY SELF-TEST FAILS')


def parity_dry():
    """counts only: moves, and the moves holding each link's first function; no statistic"""
    for corpus in ('animal', 'tale-C'):
        P = parity_moves(corpus)
        for L in 'AB':
            mv = Moves(P[L])
            firsts = []
            for name, fs, second in LINKS:
                present, _ = mv.hits(mv.tok, fs, second)
                firsts.append('%s %d' % (name, present.sum()))
            print('dry run %-7s %s: %d moves; moves with the first: %s' % (corpus, L, len(P[L]), '; '.join(firsts)))


def parity():
    os.makedirs(PARITY_OUT, exist_ok=True)
    res = {}
    for corpus in ('animal', 'tale-C'):
        P = parity_moves(corpus)
        rep = ['# links-%s.txt -- links.py parity: Data/ParityProtocol.md, frozen 2026-10-21; the statistic of LinksProtocol.md, unchanged '
               '(%d shuffles, seed %d, a link tested where its first function stands in at least %d moves).' % (corpus, SHUFFLES, SEED, MIN_MOVES), '']
        for name, firsts, second in LINKS:
            rep.append(name + ('  (tight)' if name in TIGHT else '  (frame)' if name in FRAME else ''))
            for L in 'AB':
                r = Moves(P[L]).test(firsts, second)
                res[corpus, name, L] = r
                rep.append('  %s  %s%s' % (L, fmt(r), '  HOLDS' if holds(r) else ''))
            rep.append('')
        open(os.path.join(PARITY_OUT, 'links-%s.txt' % corpus), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
        print('\n'.join(rep))
    tested = [n for n in TIGHT if all(res['animal', n, L]['with first'] >= MIN_MOVES for L in 'AB')]
    untested = [n for n in TIGHT if n not in tested]
    held = [n for n in tested if all(holds(res['animal', n, L]) for L in 'AB')]
    ok = bool(tested) and len(held) == len(tested)
    pct = lambda c, n, L: 100 * res[c, n, L]['share'] if res[c, n, L]['with first'] else float('nan')
    lines = ['PARITY PREDICTION 5 AND REPORT 6 (Data/ParityProtocol.md)',
             '  5. animal tales, every tight link tested holds for both transcribers: %d of %d tested hold -> %s' % (
                 len(held), len(tested), ('HOLDS' if ok else 'FAILS') if tested else 'NOT TESTED'),
             '     tested: %s; held: %s; too rare to test (first function in fewer than %d moves for a transcriber): %s' % (
                 ', '.join(tested) or '-', ', '.join(held) or '-', MIN_MOVES, ', '.join(untested) or '-'),
             '  6. reported, the frame links, share of moves with the first in which the second follows (A, B):']
    for n in FRAME:
        lines.append('     %-12s animal tales %.0f%% and %.0f%%; wondertales on card C %.0f%% and %.0f%%' % (
            n, pct('animal', n, 'A'), pct('animal', n, 'B'), pct('tale-C', n, 'A'), pct('tale-C', n, 'B')))
    open(os.path.join(PARITY_OUT, 'links-verdict.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


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
    cmds = {'score': score, 'selftest': selftest, 'parity-selftest': parity_selftest, 'parity-dry': parity_dry, 'parity': parity}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
