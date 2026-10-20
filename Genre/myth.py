#!/usr/bin/env python3
"""
myth.py -- the genre model's predictions for Greek myth (MythProtocol.md).

  python myth.py count    the Apollodorus moves read, and nothing measured
  python myth.py score    writes Genre/MythRun.txt

Written in full before any link was counted on the myths.
"""
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Links'))
import links as K  # noqa: E402

TS = K.TS
TIGHT = [('H -> I', ('H',), 'I'), ('M -> N', ('M',), 'N'), ('Pr -> Rs', ('Pr',), 'Rs'), ('L -> Ex', ('L',), 'Ex')]
FRAME = [('A or a -> K', ('A|a',), 'K'), ('↑ -> ↓', ('↑',), '↓'), ('D and E -> F', ('D', 'E'), 'F')]


def myth_moves(L):
    """the Apollodorus transcriptions, by their moves: [list of base functions, one a move]; the symbol stands in
    the sixth field, after the Library's locator"""
    moves = {}
    order = []
    for path in sorted(glob.glob(os.path.join(P, 'Apollodorus', 'Apollodorus', 'transcriptions', L, 'b*', 'Notes.txt'))):
        for line in open(path, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^L\d-\d{3}', f[0]):
                continue
            k = (f[0], f[1])
            if k not in moves:
                moves[k] = []
                order.append(k)
            b = TS.base(f[5])
            if b not in ('X', 'α', ''):
                moves[k].append(b)
    return [moves[k] for k in order if moves[k]]


def count():
    for L in 'AB':
        m = myth_moves(L)
        print('%s: %d moves, %d functions' % (L, len(m), sum(len(x) for x in m)))


def score():
    T = K.transcribed()
    rep = ['# MythRun.txt -- myth.py score, as MythProtocol.md freezes it.', '']
    res = {}
    for L in 'AB':
        corp = {'myth': K.Moves(myth_moves(L))}
        corp.update({g: K.Moves(T[L][g]) for g in ('tale', 'fable', 'tragedy')})
        for name, firsts, second in TIGHT + FRAME:
            for g, mv in corp.items():
                res[name, g, L] = mv.test(firsts, second)
    for name, _, _ in TIGHT + FRAME:
        rep.append(name)
        for g in ('myth', 'tale', 'fable', 'tragedy'):
            for L in 'AB':
                r = res[name, g, L]
                rep.append('  %-8s %s  %s%s' % (g, L, K.fmt(r), '  HOLDS' if K.holds(r) else ''))
        rep.append('')
    # prediction 1: the core
    elig = [n for n, _, _ in TIGHT if all(res[n, 'myth', L]['with first'] >= K.MIN_MOVES for L in 'AB')]
    held = [n for n in elig if all(K.holds(res[n, 'myth', L]) for L in 'AB')]
    ok1 = len(elig) > 0 and len(held) >= len(elig) - 1
    # prediction 2
    ak = [(res['A or a -> K', 'myth', L]['share'], res['A or a -> K', 'tale', L]['share']) for L in 'AB']
    ok2 = all(m < t for m, t in ak)
    # prediction 3: the nearest genre on the frame shares
    dims = [n for n, _, _ in FRAME if all(res[n, 'myth', L]['with first'] >= K.MIN_MOVES for L in 'AB')]
    near, lines = [], []
    for L in 'AB':
        d = {g: math.sqrt(sum((res[n, 'myth', L]['share'] - res[n, g, L]['share']) ** 2 for n in dims)) for g in ('tale', 'fable', 'tragedy')}
        near.append(min(d, key=d.get))
        lines.append('%s: distance to tale %.3f, fable %.3f, tragedy %.3f; nearest %s' % (L, d['tale'], d['fable'], d['tragedy'], near[-1]))
    ok3 = all(n == 'tragedy' for n in near)
    rep += ['PREDICTIONS (MythProtocol.md)',
            '  1. the core: of the tight links whose first function stands in at least %d myth moves for both transcribers, all but at most one hold: %d of %d (%s) -> %s'
            % (K.MIN_MOVES, len(held), len(elig), ', '.join(held) or '-', 'HOLDS' if ok1 else 'FAILS'),
            '  2. villainy or lack is followed by liquidation in a smaller share of myth moves than tale moves, for both transcribers: myth %.0f%% and %.0f%%, tales %.0f%% and %.0f%% -> %s'
            % (100 * ak[0][0], 100 * ak[1][0], 100 * ak[0][1], 100 * ak[1][1], 'HOLDS' if ok2 else 'FAILS'),
            '  3. on the frame shares (%s), myth lies nearest tragedy, for both transcribers -> %s' % (', '.join(dims), 'HOLDS' if ok3 else 'FAILS')]
    rep += ['     ' + x for x in lines]
    open(os.path.join(HERE, 'MythRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    cmds = {'count': count, 'score': score}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
