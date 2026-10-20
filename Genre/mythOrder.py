#!/usr/bin/env python3
"""
mythOrder.py -- where myth sits, retested on the order of its blocks (MythOrderProtocol.md).

  python mythOrder.py score      writes Genre/MythOrderRun.txt
  python mythOrder.py selftest   the held-out tragedies standing in for the myths

The four order models and the measure are Blocks/GenreOrder.md's, unchanged: the wondertale
and fable models as fitted (Blocks/GenreOrder-*.txt), the tragedy model as frozen
(Tragedy/TragedyOrder01.txt), and Propp's order. Written in full before any myth was scored.
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
import genreOrder as GO  # noqa: E402

BS, TG, TS = GO.BS, GO.TG, GO.TS
MODELS = ('wondertale', 'fable', 'tragedy', 'Propp')


def load(genre):
    if genre == 'tragedy':
        return TG.load_model()
    out = {}
    for line in open(os.path.join(ROOT, 'Blocks', 'GenreOrder-%s.txt' % genre), encoding='utf-8'):
        if line.startswith('#') or '|' not in line:
            continue
        r, n, _ = [x.strip() for x in line.split('|')]
        out[n] = float(r)
    return out


def myth_stream(L):
    """the Apollodorus transcriptions as genreOrder.stream reads the others; the symbol stands in the sixth field, and
    the rules there had no mark of whether an entry matters, so every entry is read as mattering"""
    out = collections.OrderedDict()
    for path in sorted(glob.glob(os.path.join(P, 'Apollodorus', 'Apollodorus', 'transcriptions', L, 'b*', 'Notes.txt'))):
        for line in open(path, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^L\d-\d{3}', f[0]):
                continue
            keys = TS.key(f[5], extended=True)
            items = out.setdefault(f[0], [])
            items += keys if keys else ['(X)']
    return GO.weighted(out)


def gaps(test, models, g):
    """{model: (gap over in-place shuffles, shuffles at or above)} on one test set, as genreOrder.main computes it"""
    out = {}
    for m in MODELS:
        rng = np.random.default_rng(TG.SEED)
        c = p = 0.0
        sc = np.zeros(TG.SHUFFLES)
        sp = np.zeros(TG.SHUFFLES)
        for v, w, items in test:
            u = TG.units(items, g)
            if len(u) < 2:
                continue
            if m == 'Propp':
                R = np.array([TG.propp_rank(f) if TG.propp_rank(f) is not None else np.nan for _, f in u], float)
            else:
                R = np.array([models[m].get(n, np.nan) for n, _ in u], float)
            perms = np.array([rng.permutation(len(u)) for _ in range(TG.SHUFFLES)])
            a, b = TG.concordance(R)
            x, y = TG.concordance(R, perms)
            c, p, sc, sp = c + w * a[0], p + w * b[0], sc + w * x, sp + w * y
        real = c / p
        sh = sc / sp
        out[m] = (real - sh.mean(), int((sh >= real).sum()))
    return out


def run(tests, title, out_path):
    g = BS.Grammar()
    models = {m: load(m) for m in MODELS if m != 'Propp'}
    rep = [title, '# Concordance gap over %d in-place shuffles (seed %d); in brackets, shuffles at or above.' % (TG.SHUFFLES, TG.SEED), '']
    best = {}
    for L in 'AB':
        r = gaps(tests[L], models, g)
        best[L] = max(MODELS, key=lambda m: r[m][0])
        rep.append('transcriber %s: %s; best %s' % (L, ', '.join('%s %+.3f (%d)' % (m, r[m][0], r[m][1]) for m in MODELS), best[L]))
    ok = all(best[L] == 'tragedy' for L in 'AB')
    rep += ['', 'PREDICTION (MythOrderProtocol.md)',
            '  tragedy\'s order fits myth better than the wondertale\'s, the fable\'s and Propp\'s, for both transcribers: %s' % ('HOLDS' if ok else 'FAILS')]
    if out_path:
        open(out_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def score():
    run({L: myth_stream(L) for L in 'AB'}, '# MythOrderRun.txt -- mythOrder.py score, as MythOrderProtocol.md freezes it.',
        os.path.join(HERE, 'MythOrderRun.txt'))


def selftest():
    run({L: GO.corpus('tragedy', 'test', L) for L in 'AB'}, '# selftest: the held-out tragedies standing in for the myths; tragedy must be best.', None)


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
