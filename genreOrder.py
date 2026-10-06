#!/usr/bin/env python3
"""
genreOrder.py -- each genre's order of blocks, tested on every genre, as
Blocks/GenreOrder.md freezes it.

  python genreOrder.py     fits the wondertale and fable models (Blocks/GenreOrder-*.txt),
                           then writes the table to Blocks/GenreOrderRun.txt
"""
import collections
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import blockStream as BS  # noqa: E402
import tragedyGrammar as TG  # noqa: E402

TS = BS.TS
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(ROOT, 'Calibration', 'Split.txt'), encoding='utf-8') if '|' in l}
GENRES = ('wondertale', 'fable', 'tragedy')
MODELS = GENRES + ('Propp',)


def stream(path, out):
    """blockStream.stream, with the wondertales' A-numbers admitted."""
    for line in open(path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
        if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
            continue
        keys = TS.key(f[4], extended=True)
        y = f[7].upper().startswith('Y')
        items = out.setdefault(f[0], [])
        if not keys:
            items.append('(X)')
        else:
            items += [k if y else '(%s)' % k for k in keys]
    return out


def weighted(vs):
    n = collections.Counter(v.split('/')[0] for v in vs)
    return [(v, 1.0 / n[v.split('/')[0]], it) for v, it in vs.items()]


def corpus(genre, part, L):
    out = collections.OrderedDict()
    if genre == 'wondertale':
        for b in ('b1', 'b2', 'b3'):
            stream(os.path.join(PARENT, 'Afanasyev', 'transcriptions', 'U', L, b, 'Notes.txt'), out)
        keep = {'A%03d' % t for t in SPLIT['dev' if part == 'fit' else 'test']}
        out = collections.OrderedDict((v, it) for v, it in out.items() if v.split('/')[0] in keep)
    elif genre == 'fable':
        repo = 'Aesop' if part == 'fit' else 'Fables'
        for b in ('b1', 'b2', 'b3', 'b4'):
            stream(os.path.join(PARENT, repo, 'transcriptions', L, b, 'Notes.txt'), out)
    else:
        plays = BS.OPEN if part == 'fit' else TG.SEALED
        for p in plays:
            stream(os.path.join(PARENT, 'Tragedy', 'transcriptions', L, p, 'Notes.txt'), out)
    return weighted(out)


def fit(genre, g):
    if genre == 'tragedy':
        return TG.load_model()
    pos = collections.defaultdict(list)
    for L in 'AB':
        for v, w, items in corpus(genre, 'fit', L):
            u = TG.units(items, g)
            for i, (name, _) in enumerate(u):
                pos[name].append(i / float(len(u) - 1) if len(u) > 1 else 0.5)
    model = {n: sum(p) / len(p) for n, p in pos.items() if len(p) >= TG.MINCOUNT}
    with open(os.path.join(ROOT, 'Blocks', 'GenreOrder-%s.txt' % genre), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GenreOrder-%s.txt -- the %s order model, genreOrder.py, fitted on its training part,\n'
                '# both transcribers, by tragedyGrammar.py\'s recipe. rank | unit | occurrences\n' % (genre, genre))
        for n in sorted(model, key=model.get):
            f.write('%.3f | %s | %d\n' % (model[n], n, len(pos[n])))
    return model


def spearman(m1, m2):
    common = sorted(set(m1) & set(m2))
    if len(common) < 3:
        return float('nan'), len(common)
    r1 = np.argsort(np.argsort([m1[n] for n in common]))
    r2 = np.argsort(np.argsort([m2[n] for n in common]))
    return float(np.corrcoef(r1, r2)[0, 1]), len(common)


def main():
    g = BS.Grammar()
    models = {genre: fit(genre, g) for genre in GENRES}
    rep = ['# GenreOrderRun.txt -- genreOrder.py, as Blocks/GenreOrder.md freezes it.',
           '# Concordance gap over 1000 in-place shuffles (seed 46); in brackets, shuffles at or above.', '']
    gaps = {}
    for L in 'AB':
        rep.append('TRANSCRIBER %s' % L)
        rep.append('  %-12s' % 'model' + ''.join('%-24s' % ('on %s' % t) for t in GENRES))
        tests = {t: corpus(t, 'test', L) for t in GENRES}
        for m in MODELS:
            row = '  %-12s' % m
            for t in GENRES:
                rng = np.random.default_rng(TG.SEED)
                c = p = 0.0
                sc = np.zeros(TG.SHUFFLES)
                sp = np.zeros(TG.SHUFFLES)
                for v, w, items in tests[t]:
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
                gap = real - sh.mean()
                gaps[L, m, t] = gap
                row += '%+.3f (%4d)          ' % (gap, int((sh >= real).sum()))
            rep.append(row)
        rep.append('')
    rep.append('THE PREDICTIONS')
    p1 = all(max(MODELS, key=lambda m: gaps[L, m, t]) == t for L in 'AB' for t in GENRES)
    for t in GENRES:
        best = {L: max(MODELS, key=lambda m: gaps[L, m, t]) for L in 'AB'}
        rep.append('  on %-11s best: A %s, B %s' % (t, best['A'], best['B']))
    rep.append('  1. each genre\'s own order fits it best: %s' % ('HOLDS' if p1 else 'FAILS'))
    p2 = all(gaps[L, 'Propp', 'wondertale'] >= max(gaps[L, 'fable', 'wondertale'], gaps[L, 'tragedy', 'wondertale'])
             for L in 'AB')
    rep.append('  2. the wondertale follows Propp at least as well as the fable and tragedy orders: %s'
               % ('HOLDS' if p2 else 'FAILS'))
    rep.append('')
    rep.append('RANK CORRELATION between fitted models (Spearman, over shared units; reported)')
    for a, b in (('wondertale', 'fable'), ('wondertale', 'tragedy'), ('fable', 'tragedy')):
        r, n = spearman(models[a], models[b])
        rep.append('  %-10s %-8s %+.2f over %d units' % (a, b, r, n))
    open(os.path.join(ROOT, 'Blocks', 'GenreOrderRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    sys.exit(main())
