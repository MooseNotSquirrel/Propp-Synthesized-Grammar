#!/usr/bin/env python3
"""
benchmark.py -- the human benchmark's scoring, as Readme.md fixes it.

  python benchmark.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import compare as C  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'Afanasyev')
TALES = [93, 131, 133, 145, 151]
READINGS = [(a, L) for a in C.ARMS for L in C.LINEAGES]
# Plain-keyboard names the owner may type, added before any annotation was
# written: without them "up" and "down" would read as U and D.
TYPED = {'up': '↑', 'down': '↓', 'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
         'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'lambda': 'λ'}


def owner(t):
    """(stream, move count, events left blank)"""
    lines = open(os.path.join(HERE, 'Benchmark-A%03d.txt' % t), encoding='utf-8').read().split('\n')
    s, moves, blank = [], 0, 0
    for l in lines:
        m = re.match(r'^\s+fn:(.*?)move:(.*)$', l)
        if not m:
            continue
        syms, mv = m.group(1).split(), m.group(2).strip()
        if mv:
            moves += 1
        if not syms:
            blank += 1
        for sym in syms:
            sym = TYPED.get(sym.lower(), sym)
            s += [k for k in C.TS.key(sym) if k in C.VOCAB]
    return s, max(moves, 1), blank


def main():
    P = C.propp()
    O = {t: owner(t) for t in TALES}
    M = {r: C.load(REPO, *r) for r in READINGS}
    S = {r: {t: C.stream(M[r].get(t, [])) for t in TALES} for r in READINGS}
    print('THE HUMAN BENCHMARK')
    print('  tale  owner: content order moves blank | Propp moves | models against Propp (U/A U/B C/A C/B), content')
    for t in TALES:
        s, mv, blank = O[t]
        print('  %3d   %.3f %.3f %d %d | %d | %s' % (
            t, C.dice(s, P[t][0]), C.order(s, P[t][0]), mv, blank, P[t][1],
            ' '.join('%.3f' % C.dice(S[r][t], P[t][0]) for r in READINGS)))
    oc = C.mean(C.dice(O[t][0], P[t][0]) for t in TALES)
    oo = C.mean(C.order(O[t][0], P[t][0]) for t in TALES)
    mc = C.mean(C.mean(C.dice(S[r][t], P[t][0]) for t in TALES) for r in READINGS)
    mo = C.mean(C.mean(C.order(S[r][t], P[t][0]) for t in TALES) for r in READINGS)
    print('\n  owner against Propp: content %.3f, order %.3f' % (oc, oo))
    print('  models against Propp, mean of four readings: content %.3f, order %.3f' % (mc, mo))
    for r in READINGS:
        print('  owner against %s/%s: content %.3f, order %.3f' % (
            r[0], r[1], C.mean(C.dice(O[t][0], S[r][t]) for t in TALES), C.mean(C.order(O[t][0], S[r][t]) for t in TALES)))
    d = oc - mc
    print('\n  READING: %s (owner minus models, content %+.3f)' % (
        'the models are near the task\'s ceiling' if d <= 0.05 else
        'the models are the weak point' if d >= 0.10 else 'unsettled', d))
    return 0


if __name__ == '__main__':
    sys.exit(main())
