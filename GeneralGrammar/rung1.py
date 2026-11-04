"""rung1.py <version> -- rung 1 of GeneralGrammarProtocol.md, by the rules in Versions.md. No real string is read.
Writes Rung1-<version>.json (every corpus, as it finishes) and Rung1-<version>.txt (the summary)."""
import json
import multiprocessing
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
import grammar as G  # noqa: E402
import generators as X  # noqa: E402
import score as C  # noqa: E402

SEED = 20261104
OPENER = None


def plan():
    out = []
    for g in ('G1', 'G2', 'G8'):
        out += [(g, 45, r) for r in range(20)]
    for g in ('G3', 'G4', 'G5', 'G6', 'G7'):
        out += [(g, 45, r) for r in range(10)]
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'):
        out += [(g, s, r) for s in (20, 100) for r in range(5)]
    return out


def make(g, size, rep, slots, pairs, seed):
    rng = np.random.default_rng([seed, int(g[1]), size, rep])
    opener = next(i for i, alt in enumerate(slots) if len(alt) == 2)
    if g == 'G8':
        return X.g8(slots, pairs, size, rng, opener)
    if g in ('G1', 'G2'):
        st, tr = X.g1(slots, pairs, size, rng, opener)
        if g == 'G2':
            st, tr = X.relabel(st, tr, rng)
        return st, tr
    return {'G3': X.g3, 'G4': X.g4, 'G5': X.g5, 'G6': X.g6, 'G7': X.g7}[g](size, rng)


def work(a):
    (g, size, rep), slots, pairs, seed = a
    t0 = time.time()
    st, tr = make(g, size, rep, slots, pairs, seed)
    flat = [X.flat(s) for s in st]
    keep = [i for i, f in enumerate(flat) if f]
    flat = [flat[i] for i in keep]
    cuts = [X.cuts_of([p for p in st[i] if p]) for i in keep]
    f = G.fit(flat)
    r = {'g': g, 'size': size, 'rep': rep, 'shape': f['shape'], 'ordered': f['ordered'], 'coverage': f['coverage'], 'cv': f['cv'], 'steps': f['steps'],
         'K': f['hmm_K'], 'ops': f['ops'], 'symbols': f['symbols'], 'units': sum(map(len, flat)) / len(flat), 'secs': time.time() - t0}
    if g in ('G1', 'G2', 'G8'):
        num = C.numbering(tr['slots'])
        r['rel_tau'], r['rel_n'] = C.relation_tau(f['relations'], num)
        r['ord_tau'] = C.order_tau(f['order'], num)
        r['recall'] = C.pair_recall(f, tr['pairs'], flat)[0]
        r['F'] = C.boundary_f(f['cuts'], cuts)
        moves = [p for i in keep for p in st[i] if p]
        r['accept'] = C.acceptance(f, moves, np.random.default_rng(rep))
        if g == 'G2':
            pn = C.numbering(slots)
            r['rel_tau_propp'], _ = C.relation_tau(f['relations'], pn)
            r['ord_tau_propp'] = C.order_tau(f['order'], pn)
        syms = sorted(num)
        fl = {tuple(b[:2]) for b in f['branches']}
        r['false_branch'] = len(fl) / max(1, len(syms) * (len(syms) - 1) / 2)
    if g == 'G3':
        cross = {(a_, b_) for a_ in tr['x'] for b_ in tr['y']}
        fl = {tuple(sorted(b[:2])) for b in f['branches']}
        r['branch_recall'] = sum(1 for p in cross if tuple(sorted(p)) in fl) / len(cross)
    return r


def pct(xs, p):
    xs = [x for x in xs if x == x]
    return float(np.percentile(xs, p)) if xs else float('nan')


def summary(rows, version):
    out = ['# Rung1-%s.txt -- generated grammars only; no real string read. Rules in Versions.md.' % version]
    req = {'G1': 'ordered', 'G2': 'ordered', 'G3': 'ordered', 'G4': 'not ordered', 'G5': 'bigram', 'G6': 'not ordered', 'G7': 'unigram', 'G8': 'ordered'}
    def met(r):
        q = req[r['g']]
        return r['ordered'] if q == 'ordered' else (not r['ordered']) if q == 'not ordered' else r['shape'] == q
    allok = True
    for size in (45, 20, 100):
        out.append('## %d stories' % size)
        for g in req:
            rs = [r for r in rows if r['g'] == g and r['size'] == size]
            sh = {}
            for r in rs:
                sh[r['shape']] = sh.get(r['shape'], 0) + 1
            share = sum(map(met, rs)) / max(1, len(rs))
            if size == 45 and share < 0.8:
                allok = False
            out.append('%s required %-11s met %2d of %2d | shapes %s | mean coverage %.2f | units %.1f, symbols %.0f, level-2 ops %.1f, %.0fs'
                       % (g, req[g], sum(map(met, rs)), len(rs), sorted(sh.items()), np.mean([r['coverage'] for r in rs]), np.mean([r['units'] for r in rs]), np.mean([r['symbols'] for r in rs]), np.mean([len(r['ops']) for r in rs]), np.mean([r['secs'] for r in rs])))
    g1 = [r for r in rows if r['g'] == 'G1' and r['size'] == 45]
    g2 = [r for r in rows if r['g'] == 'G2' and r['size'] == 45]
    g3 = [r for r in rows if r['g'] == 'G3' and r['size'] == 45]
    out.append('## the bars (G1, 45 stories, 10th percentile), and medians')
    bars = {}
    for k in ('rel_tau', 'ord_tau', 'recall', 'F'):
        bars[k] = pct([r[k] for r in g1], 10)
        out.append('%-8s bar %.3f; G1 median %.3f; G2 own median %.3f' % (k, bars[k], pct([r[k] for r in g1], 50), pct([r[k] for r in g2], 50)))
    out.append('G1 relations scored: median %.0f; acceptance %s; shuffled %s' % (pct([r['rel_n'] for r in g1], 50), '%.2f' % np.mean([r['accept'][0] / r['accept'][1] for r in g1]), '%.3f' % np.mean([r['accept'][2] for r in g1])))
    own = np.mean([r['rel_tau'] >= bars['rel_tau'] and r['ord_tau'] >= bars['ord_tau'] for r in g2])
    false = np.mean([r['rel_tau_propp'] >= bars['rel_tau'] or r['ord_tau_propp'] >= bars['ord_tau'] for r in g2])
    out.append('G2 reach the tau bars on their own order: %.0f%% (need 80%%)' % (100 * own))
    out.append('G2 reach the tau bars on Propp\'s order: %.0f%% (need at most 5%%); ord tau against Propp, median %.3f, max %.3f' % (100 * false, pct([r['ord_tau_propp'] for r in g2], 50), max(r['ord_tau_propp'] for r in g2)))
    br = np.mean([r['branch_recall'] >= 0.5 for r in g3])
    fb = np.mean([r['false_branch'] for r in g1])
    out.append('G3 corpora flagging at least half the cross-branch pairs: %.0f%% (need 80%%); G1 mean share of pairs falsely flagged %.3f (need at most 0.05)' % (100 * br, fb))
    allok = allok and own >= .8 and false <= .05 and br >= .8 and fb <= .05
    g8 = [r for r in rows if r['g'] == 'G8' and r['size'] == 45]
    out.append('## G8, the harder Propp, 45 stories, beside G1: 10th percentile and median')
    for k in ('rel_tau', 'ord_tau', 'recall', 'F'):
        out.append('%-8s %.3f; %.3f' % (k, pct([r[k] for r in g8], 10), pct([r[k] for r in g8], 50)))
    ratio = lambda g_: pct([r['steps']['ratio'] for r in rows if r['g'] == g_ and r['size'] == 45], 50)
    out.append('G8 acceptance %.2f; shuffled %.3f; ratio of slot to bigram gain, medians: G1 %.3f, G3 %.3f, G4 %.3f, G5 %.3f, G6 %.3f, G8 %.3f'
               % (np.mean([r['accept'][0] / r['accept'][1] for r in g8]), np.mean([r['accept'][2] for r in g8]), ratio('G1'), ratio('G3'), ratio('G4'), ratio('G5'), ratio('G6'), ratio('G8')))
    out.append('RUNG 1: %s' % ('PASSES' if allok else 'FAILS'))
    return out


if __name__ == '__main__':
    version = sys.argv[1]
    slots, pairs = C.propp()
    seed = SEED + int(version[1:])  # fresh draws each version
    jobs = [(p, slots, pairs, seed) for p in plan()]
    rows = []
    path = os.path.join(HERE, 'Rung1-%s.json' % version)
    with multiprocessing.Pool(4) as pool:
        for r in pool.imap_unordered(work, jobs):
            rows.append(r)
            print(len(rows), r['g'], r['size'], r['rep'], r['shape'], '%.2f' % r['coverage'], '%.0fs' % r['secs'], flush=True)
            json.dump(sorted(rows, key=lambda r: (r['g'], r['size'], r['rep'])), open(path, 'w', encoding='utf-8'), indent=0)
    lines = summary(rows, version)
    open(os.path.join(HERE, 'Rung1-%s.txt' % version), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
