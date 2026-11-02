#!/usr/bin/env python3
"""
predict34.py -- the frozen story grammar's predictions 3 and 4 (StoryGrammarProtocol.md section 7), on the Native American and
East Asian tales; written and committed before those tales' tables were built or read.

  python predict34.py dry    the new corpora's stories, versions and units counted from the tables; no concordance computed
  python predict34.py run    write StoryGrammar/Predictions34.txt (the record: refused if it exists and would change)

THE GRAMMAR: frozen (section 11). Its weights are recomputed by storyGrammar.fit and used only if their text is byte-identical
to the frozen Weights-A.txt and Weights-B.txt. Prediction 3 says "under the shared weights": the shared weights alone, on the
raw scale (each over its spread), no genre's offset.

THE STORIES: every story of each new corpus with functions, from the tables (the functions rows of its repository's
transcriptions), its units as storyGrammar.load takes them: the keys of rows marked Y that tragedyScore.NUM knows, in order, each
keeping its move; versions weighted 1 over their number; fewer than three units left out. None was seen in fitting.

THE ALTERNATIVES: 200 for each version, of storyGrammar's three kinds, drawn by a fixed seed for each corpus; the pool for an
added function is the corpus's own units, as each existing corpus drew from its own.

PREDICTION 3: in each new corpus, the concordance under the shared weights is above 0.5, by storyGrammar's sign-flip test at p
at most 0.05. For a transcriber it holds if it holds in both corpora; HOLDS if for both transcribers, SPLIT if for one, FAILS if
for neither. Each corpus's own verdict is reported too.

PREDICTION 4 (the owner's (l), restated): the Native American tales' concordance is lower than the East Asian tales'. Each
story's concordance is the weighted mean of its versions'; the difference, East Asian minus Native American, is tested by a
permutation of the corpus labels over stories, 10000 times, one-sided, at p at most 0.05, with at least 10 stories a side.

REPORTED, NOT TESTED: the concordance of each new corpus under each existing genre's weights (shared plus offset), on the same
alternatives; the genre whose weights fit each new culture best.
"""
import collections
import os
import random
import re
import sys

import numpy as np

import storyGrammar as S

HERE = S.HERE
OUT = os.path.join(HERE, 'Predictions34.txt')
NEW = collections.OrderedDict([('native', 'NativeAmerican'), ('eastasian', 'EastAsian')])
SEED34 = S.SEED + 50


def load_new(c, L):
    """[(story, weight, units, moves)] for a new corpus and transcriber, from the tables"""
    seqs = collections.OrderedDict()
    for r in S.DT.files('functions', ['%s/transcriptions/%%s/*/Notes.txt' % NEW[c]], L):
        if not r['story'].startswith(c + ':'):
            continue
        s = S.DT.local(r['story'])
        us, ms = seqs.setdefault((s, r['version']), ([], []))
        if r['matters'].upper().startswith('Y'):
            for k in S.TS.key(r['raw']):
                if k in S.TS.NUM:
                    us.append(k)
                    ms.append(r['move'])
    n = collections.Counter(s for s, v in seqs)
    return [(s, 1.0 / n[s], us, ms) for (s, v), (us, ms) in seqs.items() if len(us) >= 3]


def frozen(L):
    w = S.fit(L)
    if S.weights_text(L, w) != open(S.WEIGHTS % L, encoding='utf-8').read():
        raise SystemExit('the recomputed weights for %s differ from the frozen Weights-%s.txt; nothing scored' % (L, L))
    return w


def shared(fitted):
    w, sd = fitted
    return w[:S.NF] / sd


def present():
    return all(load_new(c, L) for c in NEW for L in 'AB')


def dry():
    for L in 'AB':
        for c in NEW:
            items = load_new(c, L)
            print('dry %s %-9s %3d stories, %3d versions, %5d units' % (L, c, len({x[0] for x in items}), len(items),
                                                                       sum(len(x[2]) for x in items)))


def story_means(vals):
    by = collections.OrderedDict()
    for s, wt, x in vals:
        by.setdefault(s, []).append((wt, x))
    return [(s, sum(w * x for w, x in v) / sum(w for w, _ in v)) for s, v in by.items()]


def p4_test(na, ea):
    obs = np.mean([x for _, x in ea]) - np.mean([x for _, x in na])
    allv = [x for _, x in na] + [x for _, x in ea]
    r = random.Random(S.SEED)
    hits = 0
    for _ in range(S.FLIPS):
        r.shuffle(allv)
        hits += np.mean(allv[len(na):]) - np.mean(allv[:len(na)]) >= obs - 1e-12
    return obs, (hits + 1) / (S.FLIPS + 1.0)


def run():
    if not present():
        raise SystemExit('refused: the new corpora have no function rows in the tables yet')
    rep = ['# Predictions34.txt -- predict34.py run: the frozen story grammar\'s predictions 3 and 4 (StoryGrammarProtocol.md '
           'section 7) on the Native American and East Asian tales, per transcriber; the grammar frozen, unchanged', '']
    p3, p3c, p4 = {}, collections.defaultdict(dict), {}
    for L in 'AB':
        fitted = frozen(L)
        ws = shared(fitted)
        genres = collections.OrderedDict((g, S.weights_of(fitted, g)) for g in S.CORPORA)
        rep.append('TRANSCRIBER %s' % L)
        rep.append('Prediction 3: each new corpus against 200 alternatives a version, under the shared weights')
        per = {}
        for i, c in enumerate(NEW):
            items = load_new(c, L)
            pl = S.pool(items)
            rng = np.random.default_rng(SEED34 + i)
            vals, fits = [], collections.defaultdict(list)
            for s, wt, us, ms in items:
                fr = S.features(us, ms)
                fa = np.array([S.features(a, b) for a, b in S.alternatives(us, ms, pl, S.TEST_ALTS, rng)])

                def conc(w):
                    sr, sa = fr @ w, fa @ w
                    return float(((sa > sr).sum() + 0.5 * (sa == sr).sum()) / S.TEST_ALTS)
                vals.append((s, wt, conc(ws)))
                for g, w in genres.items():
                    fits[g].append((wt, conc(w)))
            m, p = S.flip_test([(wt, x) for _, wt, x in vals])
            cell = m > 0.5 and p <= 0.05
            p3c[c][L] = cell
            per[c] = story_means(vals)
            rep.append('  %-9s %3d stories, %3d versions: concordance %.3f (p %.4f) %s'
                       % (c, len(per[c]), len(vals), m, p, 'holds' if cell else 'does not hold'))
            gm = collections.OrderedDict((g, sum(w * x for w, x in v) / sum(w for w, _ in v)) for g, v in fits.items())
            rep.append('    reported: under each genre\'s weights: %s; best fit %s'
                       % ('; '.join('%s %.3f' % kv for kv in gm.items()), max(gm, key=gm.get)))
        p3[L] = all(p3c[c][L] for c in NEW)
        rep.append('  prediction 3 for %s: %s in both corpora' % (L, 'holds' if p3[L] else 'does not hold'))
        na, ea = per['native'], per['eastasian']
        if len(na) < 10 or len(ea) < 10:
            p4[L] = False
            rep.append('Prediction 4: fewer than 10 stories a side, not tested')
        else:
            d, p = p4_test(na, ea)
            p4[L] = d > 0 and p <= 0.05
            rep.append('Prediction 4: East Asian minus Native American, story means %.3f against %.3f: difference %+.3f '
                       '(p %.4f) -> %s' % (np.mean([x for _, x in ea]), np.mean([x for _, x in na]), d, p,
                                           'holds' if p4[L] else 'does not hold'))
        rep.append('')
    v = S.verdict
    rep.append('VERDICTS')
    for c in NEW:
        rep.append('  prediction 3 in the %s tales: %s' % (c, v(p3c[c]['A'], p3c[c]['B'])))
    rep.append('  prediction 3, the unseen cultures: %s' % v(p3['A'], p3['B']))
    rep.append('  prediction 4, Native American lower than East Asian: %s' % v(p4['A'], p4['B']))
    text = '\n'.join(rep) + '\n'
    if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        raise SystemExit('refusing to overwrite the record %s with different content' % OUT)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'dry': dry, 'run': run}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    cmds[a[0]]()
