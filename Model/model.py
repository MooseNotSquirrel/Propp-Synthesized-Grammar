#!/usr/bin/env python3
"""
model.py -- one model of the genres: each story described by its devices, their relations and
their order, and the genre learned from half the stories and guessed on the other half
(ModelProtocol.md).

  python model.py score      writes Model/ModelRun.txt
  python model.py selftest   the model on planted genres and on shuffled labels

Written in full before any story was fitted.
"""
import collections
import glob
import os
import random
import re
import sys

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

GENRES = ('tale', 'fable', 'tragedy', 'myth')
SEED, PERMS, MIN_FUNCTIONS = 46, 1000, 3
CORPORA = {'tale': (['Afanasyev/transcriptions/U/%s/b*/Notes.txt'], 4),
           'fable': (['Aesop/transcriptions/%s/b*/Notes.txt', 'Fables/transcriptions/%s/b*/Notes.txt'], 4),
           'tragedy': (['Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'], 4),
           'myth': (['Apollodorus/Apollodorus/transcriptions/%s/b*/Notes.txt'], 5)}
FUNCS = ['β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'A', 'a', 'B', 'C', '↑', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'K', '↓',
         'Pr', 'Rs', 'o', 'L', 'M', 'N', 'Q', 'Ex', 'T', 'U', 'W']
RANK = {f: i for i, f in enumerate(FUNCS)}
PAIRS = [('γ', 'δ'), ('ε', 'ζ'), ('η', 'θ'), ('D', 'E'), ('H', 'I'), ('M', 'N'), ('Pr', 'Rs')]
LINKS = [(('A', 'a'), 'K'), (('↑',), '↓'), (('J',), 'Q'), (('L',), 'Ex'), (('E',), 'F')]


# ---------------------------------------------------------------- the stories
def stories(L):
    """{genre: {story: [(move, function or 'X', negative)]}}, each story's first reading only"""
    out = {}
    for g, (pats, sf) in CORPORA.items():
        st = collections.OrderedDict()
        for pat in pats:
            for path in sorted(glob.glob(os.path.join(P, pat % L))):
                for line in open(path, encoding='utf-8'):
                    f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
                    if len(f) < 10 or not re.match(r'^([PFA]\d{2}|L\d-\d{3})', f[0]):
                        continue
                    base, _, ver = f[0].partition('/')
                    st.setdefault(base, collections.OrderedDict()).setdefault(ver or '1', []).append(
                        (f[1], TS.base(f[sf]) or 'X', TS.negative(f[sf])))
        out[g] = {s: vs[sorted(vs, key=lambda v: (len(v), v))[0]] for s, vs in st.items()}
    return out


# ---------------------------------------------------------------- the features
GROUPS = collections.OrderedDict()


def features(entries):
    """the story's features, by group: lexicon, relations, order, outside"""
    fs = [e for e in entries if e[1] in RANK]
    n = float(len(fs)) or 1.0
    c = collections.Counter(e[1] for e in fs)
    lex = [c[f] / n for f in FUNCS]
    seq = [e[1] for e in fs]
    rel = []
    for x, y in PAIRS:
        i = seq.index(x) if x in seq else None
        rel.append(0.0 if i is None else (1.0 if y in seq[i + 1:] else -1.0))
    moves = collections.defaultdict(list)
    for m, b, _ in fs:
        moves[m].append(b)
    for xs, y in LINKS:
        val = 0.0
        for seqm in moves.values():
            idx = [k for k, b in enumerate(seqm) if b in xs]
            if idx:
                val = 1.0 if y in seqm[idx[0] + 1:] else (val if val == 1.0 else -1.0)
        rel.append(val)
    pairs = [(RANK[a], RANK[b]) for i, a in enumerate(seq) for b in seq[i + 1:] if a != b]
    back = sum(1 for a, b in pairs if a > b) / float(len(pairs)) if pairs else 0.5
    order = [back]
    outside = [sum(1 for e in entries if e[1] not in RANK) / float(len(entries)) if entries else 0.0]
    return {'lexicon': lex, 'relations': rel, 'order': order, 'outside': outside}, len(fs)


def table(S):
    """rows of (genre, story, feature groups, functions), stories of at least MIN_FUNCTIONS functions"""
    rows = []
    for g in GENRES:
        for s, e in S[g].items():
            f, n = features(e)
            if n >= MIN_FUNCTIONS:
                rows.append((g, s, f, n))
    return rows


def split(rows):
    """{story: 'fit' or 'test'}, within each genre, sorted and shuffled with SEED, the first half fit"""
    out = {}
    for g in GENRES:
        ids = sorted(s for gg, s, _, _ in rows if gg == g)
        random.Random(SEED).shuffle(ids)
        for i, s in enumerate(ids):
            out[s] = 'fit' if i < (len(ids) + 1) // 2 else 'test'
    return out


def matrix(rows, groups):
    X = np.array([sum((f[k] for k in groups), []) for _, _, f, _ in rows], float)
    y = np.array([GENRES.index(g) for g, _, _, _ in rows])
    return X, y


def balanced(y, p):
    rec = [np.mean(p[y == k] == k) for k in range(len(GENRES)) if np.any(y == k)]
    return float(np.mean(rec))


def fit_predict(Xf, yf, Xt):
    sc = StandardScaler().fit(Xf)
    m = LogisticRegression(C=1.0, class_weight='balanced', max_iter=5000).fit(sc.transform(Xf), yf)
    return m.predict(sc.transform(Xt)), m, sc


def evaluate(fit_rows, test_rows, groups, perms=PERMS, seed=SEED):
    Xf, yf = matrix(fit_rows, groups)
    Xt, yt = matrix(test_rows, groups)
    p, m, sc = fit_predict(Xf, yf, Xt)
    acc = balanced(yt, p)
    rng = np.random.default_rng(seed)
    null = [balanced(yt, fit_predict(Xf, rng.permutation(yf), Xt)[0]) for _ in range(perms)]
    pv = (sum(1 for v in null if v >= acc) + 1) / float(perms + 1)
    return acc, pv, p, yt, m


GROUP_SETS = collections.OrderedDict([('all', ['lexicon', 'relations', 'order', 'outside']), ('lexicon', ['lexicon']),
                                      ('relations', ['relations']), ('order', ['order']), ('outside', ['outside'])])


def score():
    rep = ['# ModelRun.txt -- model.py score, as ModelProtocol.md freezes it.', '',
           'Balanced accuracy: the mean, over the four genres, of the share of a genre\'s held-out stories guessed right; chance is 0.25.',
           'p: the share of %d refits with the fitting labels shuffled that score at least as high.' % PERMS, '']
    res, data = {}, {}
    for L in 'AB':
        rows = table(stories(L))
        sp = split(rows)
        fit = [r for r in rows if sp[r[1]] == 'fit']
        test = [r for r in rows if sp[r[1]] == 'test']
        data[L] = (fit, test)
        cnt = collections.Counter((r[0], sp[r[1]]) for r in rows)
        rep.append('transcriber %s: stories of at least %d functions: %s' % (L, MIN_FUNCTIONS, ', '.join(
            '%s %d fit / %d test' % (g, cnt[(g, 'fit')], cnt[(g, 'test')]) for g in GENRES)))
        for name, groups in GROUP_SETS.items():
            acc, pv, p, yt, m = evaluate(fit, test, groups)
            res[L, name] = (acc, pv)
            rep.append('  %-10s balanced accuracy %.3f, p %.4f' % (name, acc, pv))
            if name == 'all':
                conf = np.zeros((4, 4), int)
                for a, b in zip(yt, p):
                    conf[a, b] += 1
                rep.append('    confusion (rows true, columns guessed; %s):' % ', '.join(GENRES))
                for k, g in enumerate(GENRES):
                    rep.append('      %-8s %s' % (g, ' '.join('%4d' % v for v in conf[k])))
                names = ['%s' % f for f in FUNCS] + ['%s>%s' % pr for pr in PAIRS] + ['%s>>%s' % ('/'.join(xs), y) for xs, y in LINKS] + ['backward', 'outside']
                for k, g in enumerate(GENRES):
                    w = m.coef_[k]
                    top = sorted(range(len(w)), key=lambda i: -w[i])[:5]
                    rep.append('    %s marked most by: %s' % (g, ', '.join('%s %+.2f' % (names[i], w[i]) for i in top)))
        # length alone, for comparison
        lf = np.array([[np.log(r[3])] for r in fit]); lt = np.array([[np.log(r[3])] for r in test])
        yf = np.array([GENRES.index(r[0]) for r in fit]); yt = np.array([GENRES.index(r[0]) for r in test])
        res[L, 'length'] = (balanced(yt, fit_predict(lf, yf, lt)[0]), None)
        rep.append('  length alone (reported for comparison, not a feature of the model): balanced accuracy %.3f' % res[L, 'length'][0])
        rep.append('')
    cross = {}
    for a, b in (('A', 'B'), ('B', 'A')):
        acc, pv, _, _, _ = evaluate(data[a][0], data[b][1], GROUP_SETS['all'], perms=200)
        cross[a, b] = (acc, pv)
        rep.append('fitted on %s\'s stories, tested on %s\'s held-out stories: balanced accuracy %.3f, p %.4f' % (a, b, acc, pv))
    ok1 = all(res[L, 'all'][0] >= 0.60 and res[L, 'all'][1] <= 0.01 for L in 'AB')
    ok2 = all(res[L, 'relations'][1] <= 0.05 for L in 'AB')
    ok3 = all(res[L, 'all'][0] > res[L, 'length'][0] for L in 'AB')
    ok4 = all(cross[k][0] >= 0.50 for k in cross)
    rep += ['', 'PREDICTIONS (ModelProtocol.md)',
            '  1. the full model guesses the genre of held-out stories with balanced accuracy at least 0.60, p at most 0.01, for both transcribers: %s' % ('HOLDS' if ok1 else 'FAILS'),
            '  2. the relations alone, pairs and links, guess the genre above chance, p at most 0.05, for both transcribers: %s' % ('HOLDS' if ok2 else 'FAILS'),
            '  3. the full model does better than length alone, for both transcribers: %s' % ('HOLDS' if ok3 else 'FAILS'),
            '  4. a model fitted on one transcriber guesses the other\'s held-out stories with balanced accuracy at least 0.50, both ways: %s' % ('HOLDS' if ok4 else 'FAILS')]
    open(os.path.join(HERE, 'ModelRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def selftest():
    """planted genres: four kinds of random story differing only in which pair they complete; the model must find them.
    Then the same stories with their genres shuffled: the model must not."""
    rnd = random.Random(2)
    rows = []
    for k, g in enumerate(GENRES):
        for s in range(40):
            seq = [rnd.choice(FUNCS) for _ in range(12)]
            x, y = PAIRS[k]
            i = rnd.randrange(8)
            seq[i], seq[i + 2] = x, y
            entries = [('I', b, False) for b in seq]
            f, n = features(entries)
            rows.append((g, '%s%03d' % (g, s), f, n))
    sp = split(rows)
    fit = [r for r in rows if sp[r[1]] == 'fit']
    test = [r for r in rows if sp[r[1]] == 'test']
    acc, pv, _, _, _ = evaluate(fit, test, ['relations'], perms=200)
    print('planted genres, relations only: balanced accuracy %.3f, p %.4f (want well above 0.25, p small)' % (acc, pv))
    labels = [r[0] for r in rows]
    random.Random(3).shuffle(labels)
    rows2 = [(lab,) + r[1:] for lab, r in zip(labels, rows)]
    sp2 = split(rows2)
    acc2, pv2, _, _, _ = evaluate([r for r in rows2 if sp2[r[1]] == 'fit'], [r for r in rows2 if sp2[r[1]] == 'test'], GROUP_SETS['all'], perms=200)
    print('shuffled genres, all features: balanced accuracy %.3f, p %.4f (want near 0.25, p large)' % (acc2, pv2))


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
