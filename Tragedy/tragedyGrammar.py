#!/usr/bin/env python3
"""
tragedyGrammar.py -- the tragedy block grammar, in scored form: an order
model over the catalog's blocks, fitted on P01-P04 and tested on P05-P32.

  python tragedyGrammar.py fit TRAGEDY_REPO              write TragedyOrder01.txt from P01-P04
  python tragedyGrammar.py measure TRAGEDY_REPO          the training figures, P01-P04
  python tragedyGrammar.py measure TRAGEDY_REPO --lifted the held-out test, P05-P32, once
                                                         the seal is lifted

WHY A SCORED MODEL, NOT A YES-OR-NO GRAMMAR: a play's stream runs 30 to 61
functions; neither the fable grammar nor v46 (moves split freely) accepts
any of the eight P01-P04 versions, even unshuffled, and four plays cannot
fit a yes-or-no grammar for streams that long. The fable test found the
order between blocks to be a strong preference, not a rule, and named a
scored model of block order as the right instrument (PreliminaryFindings,
section 3). This is that model for tragedy.

THE UNITS: blockStream.py's `blocks` reading of each version's Notes.txt;
transparent items (X, and functions marked N) dropped; a block,
reversed or not, is one unit named by its catalog entry; a function no block
takes is a unit named by its symbol.
THE MODEL (TragedyOrder01.txt): each unit name's mean relative position in
the P01-P04 versions, both transcribers pooled, (index / (units - 1));
names seen fewer than 3 times are left unranked. A held-out play follows
the model where, of its pairs of ranked units with different ranks, the
earlier unit has the lower rank.
PROPP'S ORDER, the comparison: a unit's rank is Propp's number of its first
function (tragedyScore.NUM; I- as I); units without a number are unranked.
THE MEASURE, per transcriber, pooled over versions, a play with k heroes
weighing 1/k per version: concordance, the weighted share of pairs in model
order; against 1000 in-place shuffles of each version's units (blocks kept
whole), seed 46: the gap, real minus the shuffled mean, and the count of
shuffles at or above the real.
"""
import collections
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CALLER = os.getcwd()
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

TS = BS.TS
MODEL = os.path.join(HERE, 'TragedyOrder01.txt')
MINCOUNT, SHUFFLES, SEED = 3, 1000, 46
SEALED = ['P%02d' % i for i in range(5, 33)]


def units(items, g):
    out = []
    for b in BS.transform(items, g, 'blocks'):
        if BS.transparent(b):
            continue
        m = re.match(r'^([^\[~]+)~?\[(.*)\]$', b)
        if m:
            first = next((t for t in m.group(2).split() if not BS.transparent(t)), None)
            out.append((m.group(1), first))
        else:
            out.append((b, b))
    return out


def versions(repo, lineage, plays):
    out = []
    for pid in plays:
        p = os.path.join(repo, 'transcriptions', lineage, pid, 'Notes.txt')
        vs = BS.stream(p)
        for v, items in vs.items():
            out.append((pid, v, 1.0 / len(vs), items))
    return out


def fit(repo):
    g = BS.Grammar()
    pos = collections.defaultdict(list)
    for L in 'AB':
        for pid, v, w, items in versions(repo, L, BS.OPEN):
            u = units(items, g)
            for i, (name, _) in enumerate(u):
                pos[name].append(i / float(len(u) - 1) if len(u) > 1 else 0.5)
    rows = sorted(((sum(p) / len(p), n, len(p)) for n, p in pos.items() if len(p) >= MINCOUNT))
    with open(MODEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# TragedyOrder01.txt -- the tragedy order model, written by tragedyGrammar.py fit\n'
                '# from P01-P04, both transcribers; see its header. rank | unit | occurrences\n')
        for r, n, c in rows:
            f.write('%.3f | %s | %d\n' % (r, n, c))
    print('wrote %s: %d ranked units of %d seen' % (MODEL, len(rows), len(pos)))


def load_model():
    return {l.split('|')[1].strip(): float(l.split('|')[0]) for l in open(MODEL, encoding='utf-8')
            if not l.startswith('#') and l.strip()}


def propp_rank(first):
    if first is None:
        return None
    k = 'I' if first == 'I-' else first
    return TS.NUM.get(k)


def concordance(R, perms=None):
    """R: array of ranks (nan for unranked). Returns (concordant, pairs), or arrays over perms."""
    if perms is None:
        perms = np.arange(len(R))[None, :]
    X = R[perms]                                   # (S, n)
    a, b = X[:, :, None], X[:, None, :]
    n = X.shape[1]
    upper = np.triu(np.ones((n, n), bool), 1)[None]
    valid = upper & ~np.isnan(a) & ~np.isnan(b) & (a != b)
    conc = (valid & (a < b)).sum(axis=(1, 2))
    return conc, valid.sum(axis=(1, 2))


def measure(repo, lifted):
    g = BS.Grammar()
    model = load_model()
    plays = SEALED if lifted else list(BS.OPEN)
    print('TRAGEDY ORDER MODEL, %s: %s' % ('held-out plays' if lifted else 'training plays (overstate the model)',
                                           ' '.join(plays)))
    res = {}
    for L in 'AB':
        rng = np.random.default_rng(SEED)
        tot = {k: [0.0, 0.0, np.zeros(SHUFFLES), np.zeros(SHUFFLES)] for k in ('tragedy', 'Propp')}
        nv = 0
        for pid, v, w, items in versions(repo, L, plays):
            u = units(items, g)
            if len(u) < 2:
                continue
            nv += 1
            perms = np.array([rng.permutation(len(u)) for _ in range(SHUFFLES)])
            for key, R in (('tragedy', np.array([model.get(n, np.nan) for n, _ in u], float)),
                           ('Propp', np.array([propp_rank(f) if propp_rank(f) is not None else np.nan
                                               for _, f in u], float))):
                c, p = concordance(R)
                sc, sp = concordance(R, perms)
                t = tot[key]
                t[0] += w * c[0]
                t[1] += w * p[0]
                t[2] += w * sc
                t[3] += w * sp
        print('\nTRANSCRIBER %s: %d versions' % (L, nv))
        for key in ('tragedy', 'Propp'):
            c, p, sc, sp = tot[key]
            real = c / p
            sh = sc / sp
            gap = real - sh.mean()
            above = int((sh >= real).sum())
            res[L, key] = (real, sh.mean(), gap, above)
            print('  %-8s order: concordance %.3f, shuffled %.3f, gap %+.3f, shuffles at or above %d of %d'
                  % (key, real, sh.mean(), gap, above, SHUFFLES))
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['fit'] and len(a) == 2:
        fit(os.path.join(CALLER, a[1]))
        sys.exit(0)
    if a[:1] == ['measure'] and len(a) in (2, 3) and (len(a) == 2 or a[2] == '--lifted'):
        measure(os.path.join(CALLER, a[1]), len(a) == 3)
        sys.exit(0)
    sys.exit(__doc__)
