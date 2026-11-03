#!/usr/bin/env python3
"""
arcs.py -- the hero's fortune arc (ArcsNetworksProtocol.md section 2, frozen 2026-11-03 at the owner's word): the lister's
hero's fortune act by act, from the significance layer's helps and harms, in the six corpora that have it.

  python arcs.py a1      test A1: write A1Sample.txt, 20 stories' rows and steps, for the hand count against the table
  python arcs.py a2      test A2: planted arcs of every F2 shape, at 10, 30 and 80 acts, classed as built
  python arcs.py a3      test A3: shuffled arcs cluster no tighter than real ones (says only PASS or not; no figure)
  python arcs.py t       test T: two runs byte-identical (written to a scratch folder and not shown)
  python arcs.py run     write StoryModels/Arcs.txt -- at the owner's word only, after the tests pass

How the protocol's words are read here:
- F1. An act scores helps +1, harms -1, neither 0. The arc starts at 0 before the first act; act i of n ends at time i/n,
  and the fortune there is the running sum over n. "Scored acts" are the rows with one of the three values.
- F2. d1 = fortune(1/2) - fortune(0), d2 = fortune(1) - fortune(1/2), the arc read piecewise linearly; a half counts 0
  when |d| < 1/n. Oscillation: the 20-point arc, its three-point moving average (the 18 full windows), changing direction
  4 or more times, steps of no change skipped.
- F3. k-means (k-means++ seeding, 20 starts, a fixed seed) per describer over all six corpora's 20-point arcs.
- The prediction. Per describer, for each other F2 shape S, a one-sided sign test of the fall-then-rise count against
  S's count among the stories of the two shapes, at p at most 0.05: the describer's verdict HOLDS if every test does.
  HOLDS if both describers hold, SPLIT if one, FAILS if neither, as the levels' prediction was put.
"""
import collections
import filecmp
import os
import random
import sys
import tempfile

import numpy as np
from scipy.stats import binom

import common as C

OUT = os.path.join(C.HERE, 'Arcs.txt')
SAMPLE = os.path.join(C.HERE, 'A1Sample.txt')
VALUE = {'helps': 1, 'harms': -1, 'neither': 0}
SHAPES = ['rise', 'fall', 'fall then rise', 'rise then fall', 'flat', 'oscillation']
SIGNS = {('+', '+'): 'rise', ('0', '+'): 'rise', ('+', '0'): 'rise',
         ('-', '-'): 'fall', ('0', '-'): 'fall', ('-', '0'): 'fall',
         ('-', '+'): 'fall then rise', ('+', '-'): 'rise then fall', ('0', '0'): 'flat'}
POINTS = 20
FLOOR = 6
SEED = 20261103
PERMS = 10000
MIN_SIDE = 10
KS = range(2, 7)
EPS = 1e-12


# ---------------------------------------------------------------- F1 and F2
def scores(rows):
    return [VALUE[r['value']] for r in C.in_order(rows) if r['value'] in VALUE]


def arc(vals):
    """[(time, fortune)] from 0 before the first act to 1 after the last, the fortune divided by the scored acts"""
    n, s, pts = len(vals), 0, [(0.0, 0.0)]
    for i, v in enumerate(vals, 1):
        s += v
        pts.append((i / n, s / n))
    return pts


def at(pts, x):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return float(np.interp(x, xs, ys))


def resample(pts):
    return [at(pts, k / (POINTS - 1)) for k in range(POINTS)]


def turns(curve):
    sm = [(curve[i] + curve[i + 1] + curve[i + 2]) / 3 for i in range(len(curve) - 2)]
    steps = [b - a for a, b in zip(sm, sm[1:]) if abs(b - a) > EPS]
    return sum(1 for a, b in zip(steps, steps[1:]) if (a > 0) != (b > 0))


def shape(vals):
    n, pts = len(vals), arc(vals)

    def sign(d):
        return '0' if abs(d) < 1 / n - EPS else ('+' if d > 0 else '-')
    if turns(resample(pts)) >= 4:
        return 'oscillation'
    return SIGNS[(sign(at(pts, .5) - at(pts, 0)), sign(at(pts, 1) - at(pts, .5)))]


def low(pts):
    """the depth of the arc's lowest point and the time it is first reached"""
    m = min(y for _, y in pts)
    return m, next(x for x, y in pts if y == m)


# ---------------------------------------------------------------- the stories
def stories():
    """[(story, reader, corpus, rows in order, scores)] for every story and describer the significance table holds"""
    out = []
    for (s, L), rows in C.by_story('significance').items():
        out.append((s, L, C.corpus(s), C.in_order(rows), scores(rows)))
    return out


# ---------------------------------------------------------------- F3
def kmeans(X, k, rng):
    best = None
    for _ in range(20):
        cent = [X[rng.integers(len(X))]]
        while len(cent) < k:
            d = np.min([((X - c) ** 2).sum(1) for c in cent], 0)
            cent.append(X[rng.choice(len(X), p=d / d.sum())] if d.sum() > 0 else X[rng.integers(len(X))])
        cent = np.array(cent)
        for _ in range(300):
            lab = np.argmin(((X[:, None, :] - cent[None]) ** 2).sum(2), 1)
            new = np.array([X[lab == j].mean(0) if (lab == j).any() else cent[j] for j in range(k)])
            if np.allclose(new, cent):
                break
            cent = new
        inertia = ((X - cent[lab]) ** 2).sum()
        if best is None or inertia < best[0] - EPS:
            best = (inertia, lab, cent)
    return best[1], best[2]


def silhouette(X, lab):
    D = np.sqrt(((X[:, None, :] - X[None]) ** 2).sum(2))
    s = []
    for i in range(len(X)):
        own = lab == lab[i]
        if own.sum() < 2:
            s.append(0.0)
            continue
        a = D[i, own].sum() / (own.sum() - 1)
        b = min(D[i, lab == j].mean() for j in set(lab.tolist()) if j != lab[i])
        s.append((b - a) / max(a, b) if max(a, b) > 0 else 0.0)
    return float(np.mean(s))


def clusters(X):
    """the k of 2 to 6 with the highest mean silhouette, its labels, centres and silhouette"""
    res = []
    for k in KS:
        lab, cent = kmeans(X, k, np.random.default_rng(SEED + k))
        res.append((silhouette(X, lab), k, lab, cent))
    sil, k, lab, cent = max(res, key=lambda r: (r[0], -r[1]))
    return k, lab, cent, sil, [(r[1], r[0]) for r in res]


def shuffled(items):
    rnd = random.Random(SEED)
    out = []
    for vals in items:
        v = list(vals)
        rnd.shuffle(v)
        out.append(v)
    return out


def a3_verdict(kept):
    """per describer: (real silhouette, shuffled silhouette at the same k, PASS)"""
    out = {}
    for L in C.READERS:
        vals = [v for s, r, g, rows, v in kept if r == L]
        X = np.array([resample(arc(v)) for v in vals])
        k, lab, cent, sil, _ = clusters(X)
        Y = np.array([resample(arc(v)) for v in shuffled(vals)])
        slab, _ = kmeans(Y, k, np.random.default_rng(SEED + k))
        ssil = silhouette(Y, slab)
        out[L] = (sil, ssil, ssil < sil)
    return out


# ---------------------------------------------------------------- F4 and the tests between corpora
def tv(a, b):
    ca, cb = collections.Counter(a), collections.Counter(b)
    return 0.5 * sum(abs(ca[s] / len(a) - cb[s] / len(b)) for s in SHAPES)


def perm_test(a, b, rng):
    obs, pool, n = tv(a, b), list(a) + list(b), len(a)
    hit = 0
    for _ in range(PERMS):
        p = rng.permutation(len(pool))
        x = [pool[i] for i in p]
        hit += tv(x[:n], x[n:]) >= obs - EPS
    return obs, (hit + 1) / (PERMS + 1)


def sign_p(k, m):
    """one-sided: the chance of k or more of k + m under even odds"""
    return float(binom.sf(k - 1, k + m, 0.5)) if k + m else 1.0


# ---------------------------------------------------------------- F5
def problems(rows, n_scored):
    """(problems opened, problems repaired, time of the first repair or None), time by the act's place among the scored"""
    labels, fixed, first, i = set(), set(), None, 0
    for r in rows:
        if r['value'] in VALUE:
            i += 1
        if r['problem'] not in ('-', '') and r['place'] not in ('none', '-', ''):
            labels.add(r['problem'])
            if r['place'] == 'repairs':
                fixed.add(r['problem'])
                if first is None and n_scored:
                    first = i / n_scored
    return len(labels), len(fixed), first


# ---------------------------------------------------------------- the report
BARS = '▁▂▃▄▅▆▇█'


def spark(curve, lo, hi):
    return ''.join(BARS[min(len(BARS) - 1, int((y - lo) / (hi - lo) * len(BARS)))] if hi > lo else BARS[0] for y in curve)


def report():
    rep = ['# Arcs.txt -- arcs.py: the hero\'s fortune arc (ArcsNetworksProtocol.md, frozen 2026-11-03); EXPLORATORY but for the',
           '#  one frozen prediction. Every figure per describer, A (Opus) / B (Sonnet).',
           '#  Left out: ' + C.LEFT_OUT + '.', '']
    lister, readers = C.heroes()
    good = C.agreed(lister, readers)
    allst = stories()
    kept = [x for x in allst if len(x[4]) >= FLOOR]
    rep.append('## The stories')
    rep.append('%-16s %18s %18s %18s' % ('corpus', 'arcs', 'under %d acts' % FLOOR, 'agreed hero'))
    for g in C.ORDER:
        f = lambda L, xs: sum(1 for x in xs if x[2] == g and x[1] == L)
        rep.append('%-16s %18s %18s %18s' % (C.NAMES[g], '%d / %d' % (f('A', kept), f('B', kept)),
                                             '%d / %d' % (f('A', allst) - f('A', kept), f('B', allst) - f('B', kept)),
                                             '%d' % len({x[0] for x in kept if x[2] == g and x[0] in good})))
    shp = {(x[0], x[1]): shape(x[4]) for x in kept}

    rep += ['', '## F2. The shapes, per cent of each corpus\'s arcs (agreed-hero stories in brackets)']
    rep.append('%-16s' % 'shape' + ''.join('%22s' % C.NAMES[g] for g in C.ORDER))
    for sname in SHAPES:
        row = '%-16s' % sname
        for g in C.ORDER:
            cell = []
            for L in C.READERS:
                xs = [shp[(x[0], L)] for x in kept if x[2] == g and x[1] == L]
                ys = [shp[(x[0], L)] for x in kept if x[2] == g and x[1] == L and x[0] in good]
                cell.append('%.0f (%s)' % (100 * xs.count(sname) / len(xs) if xs else 0,
                                           '%.0f' % (100 * ys.count(sname) / len(ys)) if ys else '-'))
            row += '%22s' % ' / '.join(cell)
        rep.append(row)

    rep += ['', '## F4. The fortune at the end, and the lowest point (means; agreed-hero stories in brackets)']
    rep.append('%-16s %30s %30s %30s' % ('corpus', 'end', 'lowest point', 'time of lowest point'))
    for g in C.ORDER:
        cells = [[], [], []]
        for L in C.READERS:
            for sub in (None, good):
                xs = [x for x in kept if x[2] == g and x[1] == L and (sub is None or x[0] in sub)]
                pts = [arc(x[4]) for x in xs]
                ends = [p[-1][1] for p in pts]
                lows = [low(p) for p in pts]
                for j, v in enumerate((ends, [l[0] for l in lows], [l[1] for l in lows])):
                    cells[j].append('%+.2f' % np.mean(v) if v else '-')
        rep.append('%-16s' % C.NAMES[g] + ''.join('%31s' % ('%s (%s) / %s (%s)' % tuple(c)) for c in cells))

    rep += ['', '## F4. The mean arc, 20 points from the first act to the last (the scale shared by every row)']
    curves = {}
    for g in C.ORDER:
        for L in C.READERS:
            xs = [resample(arc(x[4])) for x in kept if x[2] == g and x[1] == L]
            curves[(g, L)] = np.mean(xs, 0) if xs else np.zeros(POINTS)
    lo = min(float(c.min()) for c in curves.values())
    hi = max(float(c.max()) for c in curves.values())
    for g in C.ORDER:
        for L in C.READERS:
            c = curves[(g, L)]
            rep.append('%-16s %s  %s  %s' % (C.NAMES[g], L, spark(c, lo, hi), ' '.join('%+.2f' % y for y in c[::3])))
    rep.append('#  scale %+.2f to %+.2f; the figures are every third point' % (lo, hi))

    rep += ['', '## F4. The corpora compared: total-variation distance between shape shares, permutation p (%d, fixed seed)' % PERMS]
    rng = np.random.default_rng(SEED)
    for L in C.READERS:
        for i, g in enumerate(C.ORDER):
            for h in C.ORDER[i + 1:]:
                a = [shp[(x[0], L)] for x in kept if x[2] == g and x[1] == L]
                b = [shp[(x[0], L)] for x in kept if x[2] == h and x[1] == L]
                if min(len(a), len(b)) < MIN_SIDE:
                    rep.append('%s  %-16s %-16s  fewer than %d stories a side' % (L, C.NAMES[g], C.NAMES[h], MIN_SIDE))
                    continue
                d, p = perm_test(a, b, rng)
                rep.append('%s  %-16s %-16s  distance %.2f  p %.4f%s' % (L, C.NAMES[g], C.NAMES[h], d, p, '  *' if p <= .05 else ''))

    rep += ['', '## F3. Shapes without a rule: k-means over the 20-point arcs, all corpora together']
    a3 = a3_verdict(kept)
    for L in C.READERS:
        xs = [x for x in kept if x[1] == L]
        X = np.array([resample(arc(x[4])) for x in xs])
        k, lab, cent, sil, tried = clusters(X)
        rep.append('%s: k = %d, mean silhouette %.3f (tried: %s); shuffled arcs at the same k %.3f: %s'
                   % (L, k, sil, ', '.join('%d %.3f' % t for t in tried), a3[L][1],
                      'clusters reported' if a3[L][2] else 'F3 FINDS NO SHAPES (A3)'))
        if not a3[L][2]:
            continue
        for j in range(k):
            mem = [shp[(x[0], L)] for x, l in zip(xs, lab) if l == j]
            top, cnt = collections.Counter(mem).most_common(1)[0]
            name = top if cnt >= len(mem) / 2 else 'mixed'
            byg = collections.Counter(x[2] for x, l in zip(xs, lab) if l == j)
            rep.append('  cluster %d, %-15s %3d arcs  %s  %s' % (j + 1, name, len(mem), spark(cent[j], lo, hi),
                                                               ', '.join('%s %d' % (C.NAMES[g], byg[g]) for g in C.ORDER if byg[g])))

    rep += ['', '## F5. The problems\' course (all the stories with significance)']
    rep.append('%-16s %26s %26s %26s' % ('corpus', 'problems per story', 'share repaired', 'time of first repair'))
    for g in C.ORDER:
        cells = [[], [], []]
        for L in C.READERS:
            ps = [problems(x[3], len(x[4])) for x in allst if x[2] == g and x[1] == L]
            opened, fixed = sum(p[0] for p in ps), sum(p[1] for p in ps)
            firsts = [p[2] for p in ps if p[2] is not None]
            cells[0].append('%.2f' % (opened / len(ps)) if ps else '-')
            cells[1].append('%.0f%%' % (100 * fixed / opened) if opened else '-')
            cells[2].append('%.2f' % np.mean(firsts) if firsts else '-')
        rep.append('%-16s' % C.NAMES[g] + ''.join('%27s' % ' / '.join(c) for c in cells))

    rep += ['', '## THE PREDICTION (frozen 2026-11-03): the wondertales\' most common F2 shape is fall then rise']
    held = 0
    for L in C.READERS:
        xs = collections.Counter(shp[(x[0], L)] for x in kept if x[2] == 'tale' and x[1] == L)
        k = xs['fall then rise']
        tests = [(s, xs[s], sign_p(k, xs[s])) for s in SHAPES if s != 'fall then rise']
        ok = all(p <= .05 for _, _, p in tests)
        held += ok
        rep.append('%s: fall then rise %d; %s: %s' % (L, k, '; '.join('%s %d, p %.4f' % t for t in tests), 'HOLDS' if ok else 'FAILS'))
    rep.append('VERDICT: %s' % ('HOLDS' if held == 2 else 'SPLIT' if held == 1 else 'FAILS'))
    return '\n'.join(rep) + '\n'


def run(path=OUT, show=True):
    text = report()
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
    if show:
        print(text, end='')


# ---------------------------------------------------------------- the tests
def a1():
    allst = stories()
    pick = sorted(random.Random(SEED).sample(range(len(allst)), 20))
    lines = ['# A1Sample.txt -- arcs.py a1: 20 story-describers drawn by a fixed seed; each row of the significance table in',
             '#  the story\'s order (event, entry), its value, the step and the running sum, for the hand count against the table']
    for i in pick:
        s, L, g, rows, vals = allst[i]
        lines.append('story %s reader %s study %s rows %d scored %d' % (s, L, rows[0]['study'], len(rows), len(vals)))
        tot = 0
        for r in rows:
            st = VALUE.get(r['value'])
            tot += st or 0
            lines.append('  ev %s %s %s step %s sum %d' % (r['event'], r['entry'], r['value'], '-' if st is None else '%+d' % st, tot))
    open(SAMPLE, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('A1: %d story-describers written to %s for the hand count' % (len(pick), SAMPLE))


def planted(name, n, rnd):
    """an arc built to have the shape: each half (each fifth, for oscillation) all of its part's sign; in the
    two-part shapes about a fifth of the acts, drawn at random, are neither"""
    parts = {'rise': [1, 1], 'fall': [-1, -1], 'fall then rise': [-1, 1], 'rise then fall': [1, -1], 'flat': [0, 0],
             'oscillation': [1, -1, 1, -1, 1]}[name]
    vals = []
    for i in range(n):
        sgn = parts[i * len(parts) // n]
        vals.append(0 if len(parts) == 2 and rnd.random() < .2 else sgn)
    return vals


def a2():
    rnd, bad, n_all = random.Random(SEED), [], 0
    for name in SHAPES:
        for n in (10, 30, 80):
            for _ in range(10):
                v = planted(name, n, rnd)
                n_all += 1
                if shape(v) != name:
                    bad.append((name, n, shape(v), v))
    print('A2 planted arcs %d, classed otherwise %d: %s' % (n_all, len(bad), 'PASS' if not bad else 'FAIL'))
    for b in bad[:10]:
        print('  built %s at %d acts, classed %s: %s' % b)
    return not bad


def a3():
    kept = [x for x in stories() if len(x[4]) >= FLOOR]
    v = a3_verdict(kept)
    for L in C.READERS:
        print('A3 %s: shuffled arcs cluster less tightly than real: %s' % (L, 'PASS' if v[L][2] else 'NOT SO; F3 will be reported as finding no shapes'))


def t():
    d = tempfile.mkdtemp()
    a, b = os.path.join(d, 'one.txt'), os.path.join(d, 'two.txt')
    run(a, False)
    run(b, False)
    same = filecmp.cmp(a, b, shallow=False)
    print('T two runs byte-identical: %s (in %s, not shown)' % ('PASS' if same else 'FAIL', d))
    return same


if __name__ == '__main__':
    cmd = sys.argv[1:]
    fns = {'a1': a1, 'a2': a2, 'a3': a3, 't': t, 'run': run}
    if len(cmd) != 1 or cmd[0] not in fns:
        sys.exit(__doc__)
    fns[cmd[0]]()
