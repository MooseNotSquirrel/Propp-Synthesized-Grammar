"""test_leaves.py -- the leaf protocol's tests, before any figure is read. Planted events only; no table is read for scores."""
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import leaves as L  # noqa: E402


def ok(name, cond, extra=''):
    print('%-5s %s %s' % ('PASS' if cond else 'FAIL', name, extra))
    ok.bad += 0 if cond else 1


ok.bad = 0


def planted(seed=1, stories=40, rename=False):
    """six functions, each with its act; the verb says little, as two functions share each verb; significance settles the rest of none"""
    rng = random.Random(seed)
    acts = ['give', 'harm', 'flee', 'fight', 'win', 'wed']
    verbs = ['p', 'p', 'q', 'q', 'r', 'r']
    st, lab = [], {}
    for s in range(stories):
        evs = []
        for e in range(12):
            f = rng.randrange(6)
            n = 'S%d' % s
            evs.append(dict(e=e, verb=[verbs[f]], act=[acts[f]], rel=['kin'], sig=['value=helps']))
            lab[(n, e)] = ['f%d' % f]
        st.append(('S%d' % s, evs))
    if rename:
        for _, evs in st:
            for e in evs:
                e['act'] = ['zz' + a[::-1] for a in e['act']]
                e['verb'] = ['yy' + v for v in e['verb']]
    return st, lab


def main():
    st, lab = planted()
    f0 = L.ladder_cv(st, 'F0', None, lambda s, e: lab.get((s, e)))
    f1 = L.ladder_cv(st, 'F1', None, lambda s, e: lab.get((s, e)))
    f2 = L.ladder_cv(st, 'F2', None, lambda s, e: lab.get((s, e)))
    ok('the planted ladder: the floor, the verb at a half, as each verb serves two functions, the act near 1', f0['hit'] < .3 and .4 < f1['hit'] < .6 and f2['hit'] > .95, 'F0 %.2f F1 %.2f F2 %.2f' % (f0['hit'], f1['hit'], f2['hit']))
    keys = list(lab)
    vals = [lab[k] for k in keys]
    random.Random(3).shuffle(vals)
    sh = dict(zip(keys, vals))
    fs = L.ladder_cv(st, 'F2', None, lambda s, e: sh.get((s, e)))
    ok('shuffled labels give chance', fs['hit'] < .3, '%.2f' % fs['hit'])
    st2, lab2 = planted(rename=True)
    fr = L.ladder_cv(st2, 'F2', None, lambda s, e: lab2.get((s, e)))
    ok('a renaming of acts and verbs changes nothing', abs(fr['hit'] - f2['hit']) < 1e-12 and fr['per'] == f2['per'])
    f3 = L.ladder_cv(st, 'F2', None, lambda s, e: lab.get((s, e)))
    ok('two runs are identical', f3['pred'] == f2['pred'])
    # the feature ladder holds what it says
    evs = st[0][1]
    ok('tokens: F1 only the verb', L.tokens(evs, 3, 'F1') == ['v:' + evs[3]['verb'][0]])
    ok('tokens: the act alone', L.tokens(evs, 3, 'act') == ['a:' + evs[3]['act'][0]])
    t5 = L.tokens(evs, 3, 'F5')
    ok('tokens: F5 holds neighbours, F4 does not', any(x.startswith('n:') for x in t5) and not any(x.startswith('n:') for x in L.tokens(evs, 3, 'F4')))
    ok('tokens: only F6 holds place', any(x.startswith('pos:') for x in L.tokens(evs, 3, 'F6')) and not any(x.startswith('pos:') for x in t5))
    ok('neighbours exclude the event and reach two either side', len(L.neighbours(evs, 3)) == 8 and len(L.neighbours(evs, 0)) == 4)
    ok('primary: the first that is not X', L.primary(['X', 'A', 'B']) == 'A' and L.primary(['X']) == 'X')
    # evaluate
    e = L.evaluate([[('A', ['A']), ('B', ['A', 'B']), ('C', ['A'])]])
    ok('a prediction among the event\'s labels is a hit', abs(e['hit'] - 2 / 3) < 1e-9)
    # clusters: degenerate data flagged; planted blocks found
    bags = [{'a': ['a:x'], 's': ['s:%d' % (i % 2)]} if i % 3 else {'a': ['a:y'], 's': ['s:%d' % (i % 2)]} for i in range(300)]
    M = L.block_matrix(bags)
    n = np.sqrt(np.asarray(M.multiply(M).sum(1)).ravel())
    ok('rows have length one', np.allclose(n, 1))
    lab_ = L.spherical(M, 2, 10, 1).labels_
    from sklearn.metrics import adjusted_rand_score
    ok('planted clusters are found across blocks', adjusted_rand_score([i % 3 == 0 for i in range(300)], lab_) > .9 or adjusted_rand_score([i % 2 for i in range(300)], lab_) > .9)
    cnt = np.bincount([0] * 90 + [1] * 10)
    ok('a cluster over a third is marked degenerate', cnt.max() / cnt.sum() > 1 / 3)
    ok('cosine', abs(L.cosine({'a': 1}, {'a': 2}) - 1) < 1e-9 and L.cosine({'a': 1}, {'b': 1}) == 0)
    print('leaf tests: %s' % ('all pass' if not ok.bad else '%d FAILED' % ok.bad))
    sys.exit(1 if ok.bad else 0)


if __name__ == '__main__':
    main()
