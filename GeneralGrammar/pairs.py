"""pairs.py -- pairs with the distance between them (PairsProtocol.md, frozen 2026-11-04), version 1. It takes stories as lists of symbols
and knows no alphabet. Symbols are numbered by first appearance, so a renaming gives the same pairs, name for name.

Tight: closeness passes, commonest distance 1. Near: closeness passes, commonest distance 2 to 4.
Spanning: direction passes, closeness does not, bound either way at least 0.5. False discovery rate 0.05 per test.
A pair found on one half is confirmed when the same test passes at p at most 0.05 on the other."""
import numpy as np

MIN_STORIES = 5
SHUFFLES = 2000
FDR = 0.05
CONFIRM_P = 0.05
BOUND = 0.5


def number(stories):
    idx = {}
    for s in stories:
        for u in s:
            idx.setdefault(u, len(idx))
    return idx


def tally(seqs, n):
    """dist[x,y]: sum of places from each x to the next y; cnt[x,y]: how many x have a y after them; before[x,y]: pairs of x before y"""
    dist = np.zeros((n, n))
    cnt = np.zeros((n, n))
    before = np.zeros((n, n))
    for s in seqs:
        nxt = np.full(n, -1)
        seen = np.zeros(n)
        for i in range(len(s) - 1, -1, -1):
            x = s[i]
            live = nxt >= 0
            dist[x, live] += nxt[live] - i
            cnt[x, live] += 1
            before[x] += seen
            nxt[x] = i
            seen[x] += 1
    return dist, cnt, before


def bh(ps, q=FDR):
    """the indices that pass Benjamini-Hochberg at q"""
    ps = np.asarray(ps)
    if not len(ps):
        return np.zeros(0, bool)
    o = np.argsort(ps, kind='stable')
    m = len(ps)
    ok = ps[o] <= q * (np.arange(m) + 1) / m
    out = np.zeros(m, bool)
    if ok.any():
        out[o[:np.nonzero(ok)[0].max() + 1]] = True
    return out


def stats(stories, idx, seed, shuffles=SHUFFLES):
    """the tests for every ordered pair of symbols standing together in at least MIN_STORIES stories"""
    n = len(idx)
    seqs = [np.array([idx[u] for u in s if u in idx], int) for s in stories]
    seqs = [s for s in seqs if len(s)]
    has = np.zeros((len(seqs), n), bool)
    for i, s in enumerate(seqs):
        has[i, s] = True
    both = (has[:, :, None] & has[:, None, :]).sum(0)
    dist, cnt, before = tally(seqs, n)
    occ = np.zeros(n)
    for s in seqs:
        np.add.at(occ, s, 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        mean = np.where(cnt > 0, dist / cnt, np.inf)
        share = before / (before + before.T)
    rng = np.random.default_rng(seed)
    lc, ld = np.zeros((n, n)), np.zeros((n, n))
    for _ in range(shuffles):
        d2, c2, b2 = tally([rng.permutation(s) for s in seqs], n)
        with np.errstate(divide='ignore', invalid='ignore'):
            m2 = np.where(c2 > 0, d2 / c2, np.inf)
            s2 = b2 / (b2 + b2.T)
        lc += m2 <= mean + 1e-12
        ld += np.nan_to_num(s2, nan=0.0) >= np.nan_to_num(share, nan=1.0) - 1e-12
    pc, pd = (lc + 1) / (shuffles + 1), (ld + 1) / (shuffles + 1)
    # the commonest distance, and the bound
    modes = {}
    for s in seqs:
        nxt = {}
        for i in range(len(s) - 1, -1, -1):
            x = int(s[i])
            for y, j in nxt.items():
                modes.setdefault((x, y), {}).setdefault(j - i, 0)
                modes[(x, y)][j - i] += 1
            nxt[x] = i
    with np.errstate(divide='ignore', invalid='ignore'):
        bound_x = np.where(occ[:, None] > 0, cnt / occ[:, None], 0.0)
    cnt_y = np.zeros((n, n))
    for s in seqs:
        last = {}
        for i, y in enumerate(s):
            y = int(y)
            for x in last:
                cnt_y[x, y] += 1
            last[y] = i
    with np.errstate(divide='ignore', invalid='ignore'):
        bound_y = np.where(occ[None, :] > 0, cnt_y / occ[None, :], 0.0)
    return dict(pc=pc, pd=pd, mean=mean, share=share, modes=modes, bx=bound_x, by=bound_y, both=both)


def mode_of(h):
    return min(h, key=lambda d: (-h[d], d))


def analyse(stories, seed=20261104, shuffles=SHUFFLES):
    """{(x, y): dict} of the pairs found, with kind, on these stories"""
    idx = number(stories)
    inv = {i: u for u, i in idx.items()}
    n = len(idx)
    st = stats(stories, idx, seed, shuffles)
    cand = [(x, y) for x in range(n) for y in range(n) if x != y and st['both'][x, y] >= MIN_STORIES]
    close = bh([st['pc'][p] for p in cand])
    direct = bh([st['pd'][p] for p in cand])
    out = {}
    for k, (x, y) in enumerate(cand):
        h = st['modes'].get((x, y), {})
        m = mode_of(h) if h else None
        kind = None
        if close[k] and m == 1:
            kind = 'tight'
        elif close[k] and m is not None and 2 <= m <= 4:
            kind = 'near'
        elif direct[k] and not close[k] and max(st['bx'][x, y], st['by'][x, y]) >= BOUND:
            kind = 'spanning'
        if kind:
            out[(inv[x], inv[y])] = dict(kind=kind, mode=m, mean=float(st['mean'][x, y]), share=float(st['share'][x, y]), bx=float(st['bx'][x, y]), by=float(st['by'][x, y]), stories=int(st['both'][x, y]))
    return out, len(cand), st, idx


def confirm(found, stories, seed=20261105, shuffles=SHUFFLES):
    """those pairs whose test passes at CONFIRM_P on these other stories"""
    idx = number(stories)
    st = stats(stories, idx, seed, shuffles)
    out = {}
    for (a, b), f in found.items():
        if a in idx and b in idx:
            x, y = idx[a], idx[b]
            p = st['pd'][x, y] if f['kind'] == 'spanning' else st['pc'][x, y]
            if p <= CONFIRM_P:
                out[(a, b)] = dict(f, p=float(p))
    return out


def halves(n, seed=20261104):
    o = np.random.default_rng(seed).permutation(n)
    return sorted(int(i) for i in o[:(n + 1) // 2]), sorted(int(i) for i in o[(n + 1) // 2:])
