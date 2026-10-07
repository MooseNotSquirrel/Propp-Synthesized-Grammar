#!/usr/bin/env python3
"""
constraintGrammar.py -- Propp's rules of order as weighted constraints, one
model for every genre, as Blocks/ConstraintGrammar.md freezes it.

  python constraintGrammar.py     fits each genre on its training stories, writes the
                                  weights to Blocks/ConstraintWeights-<genre>.txt, then
                                  tests on the held-out stories (Blocks/ConstraintGrammarRun.txt)

A story's units are its functions marked Y, in the order of its notes, X left
out. A story's violations are counted by the constraints below and divided by
the number of pairs of functions in it. Lower total weighted violation is more
grammatical.
"""
import collections
import glob
import os
import random
import re
import sys

import numpy as np
from scipy.optimize import minimize

ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
sys.path.insert(0, os.path.join(ROOT, 'Calibration'))
sys.path.insert(0, os.path.join(ROOT, 'Calibration', 'Benchmark'))
import tragedyScore as TS  # noqa: E402

GENRES = ('wondertale', 'fable', 'tragedy')
SECTION_NAMES = ['preparatory', 'complication', 'donor', 'transfer', 'struggle', 'liquidation',
                 'return', 'arrival and claims', 'task', 'endgame']
SECTION_GROUPS = [['β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'λ'], ['A', 'a', 'B', 'C', 'up'], ['D', 'E', 'F'], ['G'],
                  ['H', 'J', 'I'], ['K'], ['down', 'Pr', 'Rs'], ['o', 'L'], ['M', 'N'], ['Q', 'Ex', 'T', 'U', 'W']]
SEC = {k: i for i, ks in enumerate(SECTION_GROUPS) for k in ks}
PAIRS = [('γ', 'δ'), ('ε', 'ζ'), ('η', 'θ'), ('D', 'E'), ('E', 'F'), ('H', 'I'), ('Pr', 'Rs'), ('M', 'N'), ('o', 'L')]
PF = sorted({x for p in PAIRS for x in p})
PFI = {k: i for i, k in enumerate(PF)}
UNITS = sorted(TS.NUM, key=lambda k: TS.NUM[k])
UI = {k: i for i, k in enumerate(UNITS)}
NS, NP = len(SECTION_NAMES), len(PF)
SEC_PAIRS = [(i, j) for i in range(NS) for j in range(i + 1, NS)]
FEATURES = (['%s before %s' % (SECTION_NAMES[i], SECTION_NAMES[j]) for i, j in SEC_PAIRS] +
            ['%s before %s' % (x, y) for x, y in PAIRS] +
            ['%s next to %s' % (x, y) for x, y in PAIRS])
FIT_PERMS, TEST_PERMS, SEED, L2 = 200, 1000, 46, 1.0
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(ROOT, 'Calibration', 'Split.txt'), encoding='utf-8') if '|' in l}


def read(paths):
    """{version: [keys]} from Notes files, functions marked Y, X left out."""
    out = collections.OrderedDict()
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]) or not f[7].upper().startswith('Y'):
                continue
            out.setdefault(f[0], []).extend(k for k in TS.key(f[4]) if k in TS.NUM)
    return out


def stories(genre, part, L):
    if genre == 'wondertale':
        paths = sorted(glob.glob(os.path.join(PARENT, 'Afanasyev', 'transcriptions', 'U', L, 'b*', 'Notes.txt')))
        keep = {'A%03d' % t for t in SPLIT['dev' if part == 'fit' else 'test']}
        vs = {v: s for v, s in read(paths).items() if v.split('/')[0] in keep}
    elif genre == 'fable':
        repo = 'Aesop' if part == 'fit' else 'Fables'
        vs = read(sorted(glob.glob(os.path.join(PARENT, repo, 'transcriptions', L, 'b*', 'Notes.txt'))))
    else:
        plays = ['P%02d' % i for i in (range(1, 5) if part == 'fit' else range(5, 33))]
        vs = read([os.path.join(PARENT, 'Tragedy', 'transcriptions', L, p, 'Notes.txt') for p in plays])
    n = collections.Counter(v.split('/')[0] for v in vs)
    return [(v, 1.0 / n[v.split('/')[0]], s) for v, s in vs.items() if len(s) >= 3]


def onehot(idx, n_cols):
    """idx: (K, n) int array, -1 for none. Returns (K, n, n_cols) float."""
    K, n = idx.shape
    E = np.zeros((K, n, n_cols))
    k, q = np.nonzero(idx >= 0)
    E[k, q, idx[k, q]] = 1.0
    return E


def before_counts(E):
    """M[k, a, b]: pairs with a at an earlier position than b."""
    C = np.cumsum(E, axis=1) - E
    return np.einsum('kqa,kqb->kab', C, E)


def features(seqs):
    """seqs: (K, n) arrays of unit indices into UNITS. Returns (K, F) violation shares."""
    K, n = seqs.shape
    sec = np.vectorize(lambda u: SEC.get(UNITS[u], -1))(seqs)
    pf = np.vectorize(lambda u: PFI.get(UNITS[u], -1))(seqs)
    Ms = before_counts(onehot(sec, NS))
    Ep = onehot(pf, NP)
    Mp = before_counts(Ep)
    adj = np.einsum('kqa,kqb->kab', Ep[:, :-1, :], Ep[:, 1:, :])
    cols = [Ms[:, j, i] for i, j in SEC_PAIRS]
    cols += [Mp[:, PFI[y], PFI[x]] for x, y in PAIRS]
    cols += [Mp[:, PFI[x], PFI[y]] - adj[:, PFI[x], PFI[y]] for x, y in PAIRS]
    return np.stack(cols, axis=1) / (n * (n - 1) / 2.0)


def propp_backward(seqs):
    """function pairs out of Propp's numbering, per row."""
    num = np.array([TS.NUM[u] for u in UNITS])
    ranks = num[seqs]
    a, b = ranks[:, :, None], ranks[:, None, :]
    n = seqs.shape[1]
    up = np.triu(np.ones((n, n), bool), 1)[None]
    return ((a > b) & up).sum(axis=(1, 2)).astype(float)


def perms(seq, K, rng):
    idx = np.array([UI[u] for u in seq])
    return np.array([idx[rng.permutation(len(idx))] for _ in range(K)]), idx[None, :]


def fit(genre):
    rng = np.random.default_rng(SEED)
    D, W = [], []
    for L in 'AB':
        for v, w, s in stories(genre, 'fit', L):
            P, real = perms(s, FIT_PERMS, rng)
            D.append(features(P) - features(real))
            W.append(np.full(FIT_PERMS, w / FIT_PERMS))
    D, W = np.vstack(D), np.concatenate(W)

    def loss(w):
        z = D @ w
        l = np.logaddexp(0, -z)
        g = -(W * (1 / (1 + np.exp(z))))[:, None] * D
        return (W * l).sum() + 0.5 * L2 * w @ w, g.sum(axis=0) + L2 * w
    res = minimize(loss, np.zeros(len(FEATURES)), jac=True, method='L-BFGS-B')
    w = res.x
    with open(os.path.join(ROOT, 'Blocks', 'ConstraintWeights-%s.txt' % genre), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ConstraintWeights-%s.txt -- constraintGrammar.py, fitted on the %s training stories.\n'
                '# weight | constraint: positive, the genre keeps the rule; negative, it prefers to break it.\n'
                % (genre, genre))
        for i in np.argsort(-np.abs(w)):
            f.write('%+8.2f | %s\n' % (w[i], FEATURES[i]))
    return w


def shares(score_fn, seq, rng):
    P, real = perms(seq, TEST_PERMS, rng)
    sp, sr = score_fn(P), score_fn(real)[0]
    return float(((sp > sr).sum() + 0.5 * (sp == sr).sum()) / TEST_PERMS)


def evaluate(score_fn, items):
    rng = np.random.default_rng(SEED)
    vals = [(w, shares(score_fn, s, rng)) for v, w, s in items]
    tw = sum(w for w, _ in vals)
    mean = sum(w * x for w, x in vals) / tw
    d = [(w, x - 0.5) for w, x in vals]
    obs = sum(w * x for w, x in d) / tw
    r = random.Random(SEED)
    hits = sum(1 for _ in range(10000) if sum(w * (x if r.random() < 0.5 else -x) for w, x in d) / tw >= obs - 1e-12)
    return mean, (hits + 1) / 10001.0, len(vals)


def main():
    weights = {g: fit(g) for g in GENRES}
    rep = ['# ConstraintGrammarRun.txt -- constraintGrammar.py, as Blocks/ConstraintGrammar.md freezes it.',
           '# Share of 1000 reorderings of each held-out story that the model scores worse than the real order.', '']
    ok, failing = True, []
    cross = {}
    for g in GENRES:
        for L in 'AB':
            items = stories(g, 'test', L)
            m, p, n = evaluate(lambda X: features(X) @ weights[g], items)
            mp, _, _ = evaluate(propp_backward, items)
            cell = m > 0.5 and p <= 0.05 and m >= mp - 0.02
            ok = ok and cell
            if not cell:
                failing.append('%s/%s' % (g, L))
            rep.append('%-10s %s: %3d stories  constraint model %.1f%% (p %.4f)  Propp\'s plain order %.1f%%  %s'
                       % (g, L, n, 100 * m, p, 100 * mp, 'holds' if cell else 'FAILS'))
            for g2 in GENRES:
                cross[g2, g, L] = evaluate(lambda X: features(X) @ weights[g2], items)[0]
    rep.append('')
    rep.append('VERDICT: %s' % ('THE CONSTRAINT MODEL SERVES EVERY GENRE' if ok else
                                'IT DOES NOT; failing: ' + ', '.join(failing)))
    rep.append('')
    rep.append('ACROSS GENRES (reported): the model fitted on the row\'s genre, tested on the column\'s held-out stories, A / B')
    rep.append('  %-10s' % '' + ''.join('%-18s' % ('on ' + g) for g in GENRES))
    for g2 in GENRES:
        rep.append('  %-10s' % g2 + ''.join('%5.1f%% / %5.1f%%    ' % (100 * cross[g2, g, 'A'], 100 * cross[g2, g, 'B'])
                                             for g in GENRES))
    rep.append('')
    rep.append('THE STRONGEST CONSTRAINTS (reported; full lists in Blocks/ConstraintWeights-<genre>.txt)')
    for g in GENRES:
        w = weights[g]
        top = np.argsort(-w)[:6]
        low = np.argsort(w)[:3]
        rep.append('  %s keeps: %s' % (g, '; '.join('%s %+.1f' % (FEATURES[i], w[i]) for i in top)))
        rep.append('  %s breaks: %s' % (g, '; '.join('%s %+.1f' % (FEATURES[i], w[i]) for i in low)))
    import benchmark as Bm
    own = [('A%03d' % t, 1.0, [k for k in Bm.owner(t)[0] if k in TS.NUM]) for t in Bm.TALES]
    own = [x for x in own if len(x[2]) >= 3]
    m, p, n = evaluate(lambda X: features(X) @ weights['wondertale'], own)
    rep.append('')
    rep.append('THE OWNER\'S FIVE TALES under the wondertale model (reported): %.1f%% (%d tales)' % (100 * m, n))
    open(os.path.join(ROOT, 'Blocks', 'ConstraintGrammarRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    sys.exit(main())
