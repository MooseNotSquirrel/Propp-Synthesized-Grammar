#!/usr/bin/env python3
"""
scoreBod.py -- the published student annotations of tales 151 and 152 (Bod
et al. 2012, Bod2012.txt) scored against Propp exactly as compare.py scores
the model transcribers, beside the four model readings of the same tales.
A stand-in for the human benchmark, reported and not judged: two tales,
students reading English translations after brief training.

  python scoreBod.py
"""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import compare as C  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'Afanasyev')
READINGS = [(a, L) for a in C.ARMS for L in C.LINEAGES]


def keys(s):
    out = []
    for t in C.F.tokenize(s):
        k, r = C.R.key_of(t)
        if r is not None and k in C.VOCAB:
            out.append(k)
    return out


def main():
    P = C.propp()
    H = {}
    for l in open(os.path.join(HERE, 'Bod2012.txt'), encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        t, who, s = [x.strip() for x in l.split('|')]
        H.setdefault(int(t), []).append((who, keys(s)))
    M = {r: C.load(REPO, *r) for r in READINGS}
    for t in (151, 152):
        for label, ref in (("Propp, this project's reading", P[t][0]),) + (
                (("Propp with A for a, as Bod et al. print it", ['A' if k == 'a' else k for k in P[t][0]]),)
                if t == 151 else ()):
            print('TALE %d against %s: %s' % (t, label, ' '.join(ref)))
            for exp in ('I', 'II'):
                hs = [k for w, k in H[t] if w.startswith(exp + '-')]
                print('  students, experiment %-2s (%d): content %.3f, order %.3f' % (
                    exp, len(hs), C.mean(C.dice(k, ref) for k in hs), C.mean(C.order(k, ref) for k in hs)))
            ms = [C.stream(M[r].get(t, [])) for r in READINGS]
            print('  models, four readings:      content %.3f, order %.3f' % (
                C.mean(C.dice(k, ref) for k in ms), C.mean(C.order(k, ref) for k in ms)))
        for exp in ('I', 'II'):
            hs = [k for w, k in H[t] if w.startswith(exp + '-')]
            pairs = list(itertools.combinations(hs, 2))
            print('  students with each other, experiment %-2s: content %.3f, order %.3f' % (
                exp, C.mean(C.dice(a, b) for a, b in pairs), C.mean(C.order(a, b) for a, b in pairs)))
        for arm in C.ARMS:
            a, b = C.stream(M[arm, 'A'].get(t, [])), C.stream(M[arm, 'B'].get(t, []))
            print('  models A with B, arm %s:            content %.3f, order %.3f' % (arm, C.dice(a, b), C.order(a, b)))
        print()


if __name__ == '__main__':
    main()
