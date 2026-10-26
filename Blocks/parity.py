#!/usr/bin/env python3
"""
parity.py -- the blocks on the animal tales and the myths, as Data/ParityProtocol.md freezes them
(frozen 2026-10-21): predictions 7 and 8, and report 9.

  python parity.py selftest   the table-backed streams must equal the streams blockStream.py and
                              genreOrder.py read, on the corpora they were run on
  python parity.py dry        counts only: stories and functions marked Y, per corpus and transcriber
  python parity.py run        writes Data/Parity/blocks-animal.txt, blocks-myth.txt, blocks-verdict.txt

Predictions 7 and 8 use Tragedy/BlockPrediction.txt's adjacency rule, unchanged: for each transcriber, in the
blocks reading and in the strict reading, the share of functions inside blocks exceeds the shuffled mean, with
at most 10 of 200 shuffles at or above the real (seed 46), by blockStream.py's transform and coverage.
Report 9 is Blocks/GenreOrder.md's concordance gap for each genre's order model and Propp's, on the animal tales.
The myths carry no relevance mark, so every myth entry counts as marked Y, as Animal/agreement.py reads them.
"""
import collections
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Data'))
os.chdir(ROOT)
import blockStream as BS  # noqa: E402
import genreOrder as GO  # noqa: E402
import tables as DT  # noqa: E402

TS, TG = BS.TS, GO.TG
P = os.path.dirname(ROOT)
OUT = os.path.join(ROOT, 'Data', 'Parity')
CORPORA = {'animal': ['AnimalTales/transcriptions/%s/b*/Notes.txt'],
           'myth': ['Apollodorus/Apollodorus/transcriptions/%s/b*/Notes.txt']}


def tstream(patterns, L, idrx, myth=False, out=None):
    """blockStream.stream from the normalized tables: {version: [items]}, in order"""
    out = collections.OrderedDict() if out is None else out
    for r in DT.files('functions', patterns, L):
        s = DT.local(r['story'])
        if not re.match(idrx, s):
            continue
        v = s + ('/' + r['version'] if r['version'] else '')
        keys = TS.key(r['raw'], extended=True)
        y = myth or r['matters'].upper().startswith('Y')
        items = out.setdefault(v, [])
        if not keys:
            items.append('(X)')
        else:
            items += [k if y else '(%s)' % k for k in keys]
    return out


def corpus_stream(corpus, L):
    if corpus == 'myth':
        return tstream(CORPORA['myth'], L, r'^L\d-\d{3}', myth=True)
    return tstream(CORPORA[corpus], L, r'^A\d{3}')


def selftest():
    ok = True
    for L in 'AB':
        old = BS.load_aesop(os.path.join(P, 'Aesop'), L)
        new = tstream(['Aesop/transcriptions/%s/b' + b + '/Notes.txt' for b in ('1', '2', '3', '4')], L, r'^[PF]\d{2}')
        same = list(old.items()) == list(new.items())
        ok &= same
        print('self-test %s blockStream, the fables: %d versions, %d items, %s' % (L, len(new), sum(map(len, new.values())), 'IDENTICAL' if same else 'DIFFERS'))
        old = collections.OrderedDict()
        for b in ('b1', 'b2', 'b3'):
            GO.stream(os.path.join(P, 'Afanasyev', 'transcriptions', 'U', L, b, 'Notes.txt'), old)
        new = tstream(['Afanasyev/transcriptions/U/%s/' + b + '/Notes.txt' for b in ('b1', 'b2', 'b3')], L, r'^[PFA]\d{2}')
        same = list(old.items()) == list(new.items())
        ok &= same
        print('self-test %s genreOrder, the wondertales: %d versions, %d items, %s' % (L, len(new), sum(map(len, new.values())), 'IDENTICAL' if same else 'DIFFERS'))
    print('PARITY SELF-TEST PASSES' if ok else 'PARITY SELF-TEST FAILS')
    return ok


def dry():
    for corpus in CORPORA:
        for L in 'AB':
            vs = corpus_stream(corpus, L)
            y = sum(1 for it in vs.values() for t in it if not BS.transparent(t))
            print('dry run %-6s %s: %d stories, %d functions marked Y, %d items' % (corpus, L, len(vs), y, sum(map(len, vs.values()))))


def adjacency(corpus):
    """blockStream.run's measure: per transcriber and reading, functions inside blocks against in-place shuffles"""
    g = BS.Grammar()
    rng = random.Random(BS.SEED)
    rep, res = [], {}
    for L in 'AB':
        versions = list(corpus_stream(corpus, L).items())
        for reading in BS.READINGS:
            real_in = real_tot = 0
            shuf_in = [0] * BS.SHUFFLES
            for v, items in versions:
                b = BS.transform(items, g, reading)
                i, t = BS.coverage(b)
                real_in, real_tot = real_in + i, real_tot + t
                ypos = [k for k, it in enumerate(items) if not BS.transparent(it)]
                for s in range(BS.SHUFFLES):
                    toks = [items[k] for k in ypos]
                    rng.shuffle(toks)
                    sh = list(items)
                    for k, tk in zip(ypos, toks):
                        sh[k] = tk
                    shuf_in[s] += BS.coverage(BS.transform(sh, g, reading))[0]
            mean = sum(shuf_in) / float(BS.SHUFFLES)
            ge = sum(1 for x in shuf_in if x >= real_in)
            res[L, reading] = real_in > mean and ge <= 10
            rep.append('TRANSCRIBER %s, reading %s: functions inside blocks %d of %d (%.1f%%); shuffled mean %.1f (%.1f%%); '
                       'shuffles at or above the real: %d of %d%s' % (
                           L, reading, real_in, real_tot, 100.0 * real_in / max(1, real_tot), mean,
                           100.0 * mean / max(1, real_tot), ge, BS.SHUFFLES, '  ADJACENT' if res[L, reading] else ''))
    held = all(res[L, r] for L in 'AB' for r in ('blocks', 'strict'))
    return rep, held


def genre_order():
    """GenreOrder.md's concordance gap for each model on the animal tales, both transcribers"""
    g = BS.Grammar()
    models = {genre: GO.fit(genre, g) for genre in GO.GENRES}
    rep, gaps = [], {}
    for L in 'AB':
        test = GO.weighted(corpus_stream('animal', L))
        for m in GO.MODELS:
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
            real = c / p if p else float('nan')
            sh = sc / sp
            gaps[L, m] = real - sh.mean()
            rep.append('  %s  %-11s concordance gap %+.3f  (shuffles at or above: %d of %d)' % (
                L, m, gaps[L, m], int((sh >= real).sum()), TG.SHUFFLES))
    best = {L: max(GO.MODELS, key=lambda m: gaps[L, m]) for L in 'AB'}
    return rep, best


def run():
    os.makedirs(OUT, exist_ok=True)
    verdict = ['PARITY PREDICTIONS 7 AND 8, REPORT 9 (Data/ParityProtocol.md)']
    for n, corpus in ((7, 'animal'), (8, 'myth')):
        rep, held = adjacency(corpus)
        head = ['# blocks-%s.txt -- Blocks/parity.py run: Data/ParityProtocol.md, frozen 2026-10-21; blockStream.py\'s transform '
                'and coverage, %d in-place shuffles, seed %d; Tragedy/BlockPrediction.txt\'s adjacency rule.' % (corpus, BS.SHUFFLES, BS.SEED), '']
        if corpus == 'animal':
            orep, best = genre_order()
            rep += ['', 'REPORT 9, reported and not judged: each genre\'s order model and Propp\'s on the animal tales '
                    '(Blocks/GenreOrder.md\'s concordance gap, %d shuffles, seed %d)' % (TG.SHUFFLES, TG.SEED)] + orep
            rep.append('  best fit: A %s, B %s' % (best['A'], best['B']))
        open(os.path.join(OUT, 'blocks-%s.txt' % corpus), 'w', encoding='utf-8', newline='\n').write('\n'.join(head + rep) + '\n')
        print('\n'.join(head + rep))
        verdict.append('  %d. %s: blocks told together more than chance, both transcribers, blocks and strict readings: %s' % (
            n, 'animal tales' if corpus == 'animal' else 'myths', 'HOLDS' if held else 'FAILS'))
    verdict.append('  9. reported: the order model that fits the animal tales best, A %s, B %s' % (best['A'], best['B']))
    open(os.path.join(OUT, 'blocks-verdict.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(verdict) + '\n')
    print('\n'.join(verdict))


if __name__ == '__main__':
    a = sys.argv[1:]
    cmds = {'selftest': selftest, 'dry': dry, 'run': run}
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
