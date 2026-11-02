#!/usr/bin/env python3
"""
levels.py -- the story grammar by levels (StoryGrammar/LevelsProtocol.md, frozen 2026-10-31, the four recommended decisions
taken). The frozen grammar is not refitted or changed: its weights are recomputed by storyGrammar.fit and used only if their
text is byte-identical to the frozen Weights-A.txt and Weights-B.txt.

  python levels.py test    tests L1 to L4 (prints only pass or fail, no figure)
  python levels.py run     the five existing corpora, exploratory: StoryGrammar/LevelsRun.txt (refused if it exists and would
                           change)
  python levels.py new     the Native American and East Asian corpora, and the frozen prediction: refused until their tables
                           exist and the frozen grammar's predictions 3 and 4 are on record (StoryGrammar/Predictions34.txt)

THE LEVELS (section 1), by the frozen feature order of storyGrammar.FEATURES: move 0-1, sections 2-46, pairs 47-76 (the
constraint grammar's 9 pair orders and 9 cohesions, then the 12 Propp's pairs within the move), blocks 77; length 78-79 is left
out of every level and kept only in "all", which reproduces the record.

M1: each held-out version against the 200 alternatives `storyGrammar.py run` drew (the same seed, the same order), scored by
each level's weights alone. M2: each move cut into segments, the longest runs of consecutive functions of one section (in the
move's own order of functions); section shuffles put the segments in a random order, inner shuffles reorder each segment's
functions; 200 of each, by fixed seeds; a version whose moves have no second segment has no section shuffle, one whose segments
are all single functions has no inner shuffle, and each is left out of that measure and counted. M3: for each ordered pair of
sections, the share of pairs of functions in one move, one of each, in which the first comes first, every pair weighted by its
version's weight; each section's place by the mean of its shares against the others; Kendall's tau with Propp's order.
Comparisons of tau between corpora: a permutation of the corpus labels over stories, 1000 times, two-sided, at least 10
stories a side.
"""
import collections
import os
import random
import sys

import numpy as np
from scipy.stats import kendalltau

import storyGrammar as S

HERE = S.HERE
OUT = os.path.join(HERE, 'LevelsRun.txt')
PRED34 = os.path.join(HERE, 'Predictions34.txt')
NEW = ['native', 'eastasian']
LEVELS = collections.OrderedDict([('move', list(range(0, 2))), ('sections', list(range(2, 47))),
                                  ('pairs', list(range(47, 77))), ('blocks', [77])])
assert S.FEATURES[1].startswith('v46') and S.FEATURES[2] == S.CG.FEATURES[0] and S.FEATURES[77] == 'outside blocks'
assert S.FEATURES[76].endswith('within the move') and S.FEATURES[78].startswith('length')
NSEC = len(S.CG.SECTION_NAMES)
SEED_SEC, SEED_INNER, PERMS = S.SEED + 30, S.SEED + 40, 1000
_cache = {}


def feat(us, ms):
    k = (tuple(us), tuple(ms))
    if k not in _cache:
        _cache[k] = S.features(us, ms)
    return _cache[k]


def masked(w):
    out = collections.OrderedDict()
    for name, idx in LEVELS.items():
        m = np.zeros(S.NF)
        m[idx] = 1.0
        out[name] = w * m
    out['all'] = w
    return out


def conc(fr, fa, w):
    sr, sa = fr @ w, fa @ w
    return float(((sa > sr).sum() + 0.5 * (sa == sr).sum()) / len(sa))


# ---------------------------------------------------------------- segments and the two shuffles
def segments(us, ms):
    """{move: [[positions of one segment], ...]} in the move's own order"""
    by = collections.OrderedDict()
    for i, m in enumerate(ms):
        by.setdefault(m, []).append(i)
    out = collections.OrderedDict()
    for m, pos in by.items():
        segs = []
        for i in pos:
            s = S.CG.SEC.get(us[i], -1)
            if segs and S.CG.SEC.get(us[segs[-1][-1]], -1) == s:
                segs[-1].append(i)
            else:
                segs.append([i])
        out[m] = segs
    return out


def rebuild(us, ms, order):
    """order: {move: [unit index, ...]} the move's new order of its units, placed in the positions the move holds"""
    out = list(us)
    for m, pos in segments(us, ms).items():
        slots = [i for seg in pos for i in seg]
        for slot, src in zip(slots, order[m]):
            out[slot] = us[src]
    return out, list(ms)


def section_order(us, ms, rng):
    order = {}
    for m, segs in segments(us, ms).items():
        p = rng.permutation(len(segs))
        order[m] = [i for k in p for i in segs[k]]
    return order


def inner_order(us, ms, rng):
    order = {}
    for m, segs in segments(us, ms).items():
        order[m] = [seg[k] for seg in segs for k in rng.permutation(len(seg))]
    return order


def section_shuffle(us, ms, rng):
    return rebuild(us, ms, section_order(us, ms, rng))


def inner_shuffle(us, ms, rng):
    return rebuild(us, ms, inner_order(us, ms, rng))


def applicable(us, ms):
    segs = segments(us, ms)
    return any(len(s) > 1 for s in segs.values()), any(len(seg) > 1 for s in segs.values() for seg in s)


# ---------------------------------------------------------------- M3, the precedence of sections
def precedence(us, ms):
    """P[a, b]: pairs of functions in one move, a's before b's"""
    P = np.zeros((NSEC, NSEC))
    by = collections.defaultdict(list)
    for u, m in zip(us, ms):
        s = S.CG.SEC.get(u, -1)
        if s >= 0:
            by[m].append(s)
    for ss in by.values():
        for i, a in enumerate(ss):
            for b in ss[i + 1:]:
                if a != b:
                    P[a, b] += 1
    return P


def order_of(P):
    tot = P + P.T
    with np.errstate(invalid='ignore', divide='ignore'):
        share = np.where(tot > 0, P / tot, np.nan)
    present = [i for i in range(NSEC) if (tot[i] > 0).any()]
    place = {i: np.nanmean([share[i, j] for j in present if j != i and tot[i, j] > 0]) for i in present}
    ranked = sorted(present, key=lambda i: (-place[i], i))
    tau = kendalltau([ranked.index(i) for i in present], present).correlation if len(present) > 1 else float('nan')
    return share, ranked, tau


def tau_of(stories):
    P = sum((wt * precedence(us, ms) for _, wt, us, ms in stories), np.zeros((NSEC, NSEC)))
    return order_of(P)[2]


def compare(a, b, seed):
    """two-sided permutation test of the difference in tau with Propp's order, the corpus labels permuted over stories"""
    ga, gb = group(a), group(b)
    if len(ga) < 10 or len(gb) < 10:
        return None
    obs = tau_of([v for g in ga for v in g]) - tau_of([v for g in gb for v in g])
    allg = ga + gb
    r = random.Random(seed)
    hits = 0
    for _ in range(PERMS):
        r.shuffle(allg)
        d = tau_of([v for g in allg[:len(ga)] for v in g]) - tau_of([v for g in allg[len(ga):] for v in g])
        hits += abs(d) >= abs(obs) - 1e-12
    return obs, (hits + 1) / (PERMS + 1.0)


def group(items):
    by = collections.OrderedDict()
    for it in items:
        by.setdefault(it[0], []).append(it)
    return list(by.values())


# ---------------------------------------------------------------- the measures for one corpus and transcriber
def measure(w, items, pl, seed_run=S.SEED + 10):
    """per version: M1 concordances by level, M2 concordances by level against each shuffle (or None)"""
    W = masked(w)
    rng = np.random.default_rng(seed_run)
    rs, ri = np.random.default_rng(SEED_SEC), np.random.default_rng(SEED_INNER)
    out = []
    for s, wt, us, ms in items:
        fr = feat(us, ms)
        fa = np.array([feat(a, b) for a, b in S.alternatives(us, ms, pl, S.TEST_ALTS, rng)])
        fs = np.array([feat(*section_shuffle(us, ms, rs)) for _ in range(S.TEST_ALTS)])
        fi = np.array([feat(*inner_shuffle(us, ms, ri)) for _ in range(S.TEST_ALTS)])
        ok_s, ok_i = applicable(us, ms)
        out.append({'story': s, 'wt': wt,
                    'm1': {k: conc(fr, fa, v) for k, v in W.items()},
                    'sec': {k: conc(fr, fs, v) for k, v in W.items()} if ok_s else None,
                    'inner': {k: conc(fr, fi, v) for k, v in W.items()} if ok_i else None})
    return out


def wmean(rows, key, lev):
    rr = [r for r in rows if r[key] is not None]
    tw = sum(r['wt'] for r in rr)
    return (sum(r['wt'] * r[key][lev] for r in rr) / tw if tw else float('nan')), len(rr)


def flip(d, seed):
    """paired sign-flip test, one-sided, of the mean weighted difference above zero"""
    tw = sum(w for w, _ in d)
    obs = sum(w * x for w, x in d) / tw
    r = random.Random(seed)
    hits = sum(1 for _ in range(S.FLIPS) if sum(w * (x if r.random() < 0.5 else -x) for w, x in d) / tw >= obs - 1e-12)
    return obs, (hits + 1) / (S.FLIPS + 1.0)


def frozen(L):
    w = S.fit(L)
    if S.weights_text(L, w) != open(S.WEIGHTS % L, encoding='utf-8').read():
        raise SystemExit('the recomputed weights for %s differ from the frozen Weights-%s.txt; nothing reported' % (L, L))
    return w


def recorded():
    import re
    out, L = {}, None
    for line in open(S.RECORD, encoding='utf-8'):
        m = re.match(r'^TRANSCRIBER (\w)', line)
        if m:
            L = m.group(1)
        m = re.match(r'^\s+(\w+)\s+\d+ versions: concordance ([\d.]+)', line)
        if m and L:
            out[(m.group(1), L)] = float(m.group(2))
    return out


# ---------------------------------------------------------------- the report
def report(weights, datas, corpora, part, title):
    rep = [title, '']
    m3 = {}
    for L in 'AB':
        w, data = weights[L], datas[L]
        rep.append('TRANSCRIBER %s' % L)
        rep.append('  M1, concordance by level against the run\'s 200 alternatives (%s stories):' % part)
        rep.append('    %-9s %4s %7s %9s %7s %7s %7s' % ('corpus', 'n', 'move', 'sections', 'pairs', 'blocks', 'all'))
        m2 = []
        for g in corpora:
            items = data[g][part]
            rows = measure(S.weights_of(w, g), items, S.pool(data[g]['fit']))
            rep.append('    %-9s %4d ' % (g, len(rows)) + ' '.join('%7.3f' % wmean(rows, 'm1', k)[0] if k != 'sections' else '%9.3f' % wmean(rows, 'm1', k)[0]
                                                         for k in list(LEVELS) + ['all']))
            m2.append((g, rows))
        rep.append('  M2, concordance against section shuffles / inner shuffles, by level (versions applicable, of n):')
        rep.append('    %-9s %13s %15s %15s %15s %15s %15s' % ('corpus', 'applicable', 'move', 'sections', 'pairs', 'blocks', 'all'))
        for g, rows in m2:
            ns, ni = wmean(rows, 'sec', 'all')[1], wmean(rows, 'inner', 'all')[1]
            cells = ['%6.3f / %6.3f' % (wmean(rows, 'sec', k)[0], wmean(rows, 'inner', k)[0]) for k in list(LEVELS) + ['all']]
            rep.append('    %-9s %5d / %-5d of %3d ' % (g, ns, ni, len(rows)) + ' '.join(cells))
        rep.append('  inner minus section, the whole grammar, versions where both apply (paired sign-flip, one-sided):')
        for g, rows in m2:
            d = [(r['wt'], r['inner']['all'] - r['sec']['all']) for r in rows if r['sec'] is not None and r['inner'] is not None]
            stories = len({r['story'] for r in rows if r['sec'] is not None and r['inner'] is not None})
            if stories < 10:
                rep.append('    %-9s %3d stories: fewer than 10, not tested' % (g, stories))
                continue
            obs, p = flip(d, S.SEED)
            rep.append('    %-9s %3d stories: mean %+.3f (p %.4f)' % (g, stories, obs, p))
        rep.append('  M3, each corpus\'s order of the sections (all stories), and Kendall\'s tau with Propp\'s order:')
        for g in corpora:
            allst = data[g]['fit'] + data[g]['held'] if part == 'held' else data[g][part]
            P = sum((wt * precedence(us, ms) for _, wt, us, ms in allst), np.zeros((NSEC, NSEC)))
            share, ranked, tau = order_of(P)
            m3[(g, L)] = allst
            rep.append('    %-9s tau %+.3f: %s' % (g, tau, ' < '.join(S.CG.SECTION_NAMES[i] for i in ranked)))
            rep.append('    %-9s precedence (row before column, %%): ' % '' + '; '.join(
                '%s %s' % (S.CG.SECTION_NAMES[i][:4], ' '.join('--' if i == j or np.isnan(share[i, j]) else '%2.0f' % (99 if share[i, j] > .995 else 100 * share[i, j])
                                                              for j in range(NSEC))) for i in range(NSEC)))
        ref = corpora[0]
        rep.append('  M3, tau compared with the %s (permutation of the corpus labels over stories, two-sided):' % ref)
        for g in corpora[1:]:
            c = compare(m3[(g, L)], m3[(ref, L)], S.SEED)
            rep.append('    %-9s %s' % (g, 'fewer than 10 stories a side, not tested' if c is None else 'difference %+.3f (p %.4f)' % c))
        rep.append('')
    return '\n'.join(rep) + '\n'


# ---------------------------------------------------------------- the tests
def tests():
    ok = True
    weights = {L: frozen(L) for L in 'AB'}
    datas = {L: S.load(L) for L in 'AB'}
    rec = recorded()
    good = True
    for L in 'AB':
        for g in S.CORPORA:
            rows = measure(S.weights_of(weights[L], g), datas[L][g]['held'], S.pool(datas[L][g]['fit']))
            m = wmean(rows, 'm1', 'all')[0]
            good &= abs(m - rec[(g, L)]) <= 0.0005
    print('L1 the record\'s concordances reproduced with all levels and length: %s' % ('pass' if good else 'FAIL'))
    ok &= good
    good, n = True, 0
    rng = np.random.default_rng(7)
    for L in 'AB':
        for g in S.CORPORA:
            for s, wt, us, ms in datas[L][g]['held']:
                segs = segments(us, ms)
                for kind in ('section', 'inner'):
                    order = (section_order if kind == 'section' else inner_order)(us, ms, rng)
                    a, b = rebuild(us, ms, order)
                    n += 1
                    # both: every function stays in its move, the move's functions are the same
                    good &= b == ms and sorted(zip(a, b)) == sorted(zip(us, ms))
                    for m, sg in segs.items():
                        o = order[m]
                        if kind == 'section':
                            # the new order is whole segments, each in its own order, end to end
                            k, pieces = 0, []
                            while k < len(o):
                                seg = next(x for x in sg if x[0] == o[k])
                                good &= o[k:k + len(seg)] == seg
                                pieces.append(tuple(seg))
                                k += len(seg)
                            good &= sorted(pieces) == sorted(tuple(x) for x in sg)
                        else:
                            # the segments keep their order, each holding its own functions
                            k = 0
                            for seg in sg:
                                good &= sorted(o[k:k + len(seg)]) == sorted(seg)
                                k += len(seg)
    print('L2 %d shuffles keep moves, segments and their order as defined: %s' % (n, 'pass' if good else 'FAIL'))
    ok &= good
    rev = {i: NSEC - 1 - i for i in range(NSEC)}
    planted = []
    for s, wt, us, ms in datas['A']['tale']['held']:
        order = {m: [i for seg in sorted(segs, key=lambda sg: (rev[S.CG.SEC.get(us[sg[0]], 0)], sg[0])) for i in seg]
                 for m, segs in segments(us, ms).items()}
        a, b = rebuild(us, ms, order)
        planted.append((s, wt, a, b))
    rows = measure(S.weights_of(weights['A'], 'tale'), planted, S.pool(datas['A']['tale']['fit']))
    sec, inner = wmean(rows, 'sec', 'all')[0], wmean(rows, 'inner', 'all')[0]
    tau = tau_of(planted)
    good = inner >= 0.7 and sec <= 0.3 and tau <= -0.8
    print('L3 a planted culture, the wondertales with their sections reversed: inner high, section low, M3 reversed: %s' % ('pass' if good else 'FAIL'))
    ok &= good
    t = 'L4'
    a = report(weights, datas, S.CORPORA[:2], 'held', t)
    b = report(weights, datas, S.CORPORA[:2], 'held', t)
    good = a == b
    print('L4 two reports byte-identical: %s' % ('pass' if good else 'FAIL'))
    ok &= good
    print('LEVELS TESTS %s' % ('PASS' if ok else 'FAIL'))
    return ok


def run():
    weights = {L: frozen(L) for L in 'AB'}
    datas = {L: S.load(L) for L in 'AB'}
    text = report(weights, datas, S.CORPORA, 'held',
                  '# LevelsRun.txt -- levels.py run: LevelsProtocol.md on the five existing corpora, EXPLORATORY, reported only; the '
                  'frozen grammar unchanged.\n# M1 and M2 on the held-out stories; M3 on all stories; per transcriber.')
    if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        raise SystemExit('refusing to overwrite %s with different content' % OUT)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


def new():
    if not os.path.exists(PRED34) or any(g not in S.C.PATS for g in NEW):
        raise SystemExit('refused: the new corpora are scored only after predictions 3 and 4 are on record (%s) and their '
                         'tables exist' % os.path.basename(PRED34))
    raise SystemExit('the new corpora\'s command is to be completed, and committed, when their tables exist')


if __name__ == '__main__':
    cmds = {'test': tests, 'run': run, 'new': new}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
