"""grammar.py -- the general story grammar, version 3 (GeneralGrammarProtocol.md, frozen 2026-11-04).

It takes stories as lists of symbols and knows nothing of any alphabet. No Propp order, section, pair or move rule is here,
and test_rung0.py fails if this file imports anything that holds them. Symbols are numbered by first appearance, so a
renaming of the symbols gives the same grammar, name for name.

One rule governs every level: a level is kept only if it raises cross-validated likelihood on held-out stories.
"""
import math
import random

import numpy as np

RARE = '*'
MIN_STORIES = 5
FOLDS = 5
BETAS = (0.1, 0.3, 1.0, 3.0, 10.0)
HMM_KS = (2, 4, 6, 8, 10, 12)
HMM_STARTS, HMM_ITERS = 2, 25
ORDER_STARTS, BOOT_STARTS, CV_STARTS, L2_STARTS = 50, 3, 10, 3
BOOTSTRAPS = 200
SUPPORT = 0.95
L2_GAIN, L2_TRIES, L2_MAX = 2.0, 10, 12
LINK_SHUFFLES, LINK_P, LINK_LIFT, LINK_MIN = 500, 0.01, 1.5, 3
FLIPS, ALPHA = 2000, 0.05
COVERAGE, RATIO = 0.7, 0.9
WINDOWS = (0, 2, 4, 8)
L2_GRID = (1.0, 2)
METHODS = (1, 2, 4, 8)    # 1: the likelihood over immediate neighbours; d > 1: precedence among units at most d apart


# ---------------------------------------------------------------- symbols
def canon(stories):
    """symbols in at least MIN_STORIES stories keep their names, the rest become RARE; numbered by first appearance"""
    seen = {}
    for s in stories:
        for u in set(s):
            seen[u] = seen.get(u, 0) + 1
    out = [[u if seen[u] >= MIN_STORIES else RARE for u in s] for s in stories]
    vocab = []
    have = set()
    for s in out:
        for u in s:
            if u not in have:
                have.add(u)
                vocab.append(u)
    return out, vocab


def folds_of(n, seed, k=FOLDS):
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return [sorted(idx[i::k]) for i in range(k)]


# ---------------------------------------------------------------- level 2: joins and merges
def apply_ops(story, ops):
    """(units, member choices): each op is ('join', x, y, name) or ('merge', x, y, name); (class, member) kept for the member term"""
    units = list(story)
    chosen = []
    for kind, x, y, name in ops:
        if kind == 'join':
            out = []
            i = 0
            while i < len(units):
                if i + 1 < len(units) and units[i] == x and units[i + 1] == y:
                    out.append(name)
                    i += 2
                else:
                    out.append(units[i])
                    i += 1
            units = out
        else:
            for i, u in enumerate(units):
                if u == x or u == y:
                    chosen.append((name, u))
                    units[i] = name
    return units, chosen


def spans_of(story, ops):
    """how many base symbols each unit of the parsed story stands for: a join adds, a merge does not"""
    units, n = list(story), [1] * len(story)
    for kind, x, y, name in ops:
        if kind == 'join':
            ou, on, i = [], [], 0
            while i < len(units):
                if i + 1 < len(units) and units[i] == x and units[i + 1] == y:
                    ou.append(name)
                    on.append(n[i] + n[i + 1])
                    i += 2
                else:
                    ou.append(units[i])
                    on.append(n[i])
                    i += 1
            units, n = ou, on
        else:
            units = [name if u == x or u == y else u for u in units]
    return n


def expand(unit, ops):
    """the base symbols a unit stands for; a joined unit's in order"""
    table = {name: (kind, x, y) for kind, x, y, name in ops}

    def go(u):
        if u not in table:
            return [u]
        _, x, y = table[u]
        return go(x) + go(y)
    return go(unit)


# ---------------------------------------------------------------- counts
def counts(units_by_story, idx):
    n = len(idx)
    T = [[0] * n for _ in range(n)]
    S, E = [0] * n, [0] * n
    for s in units_by_story:
        if not s:
            continue
        S[idx[s[0]]] += 1
        E[idx[s[-1]]] += 1
        for a, b in zip(s, s[1:]):
            T[idx[a]][idx[b]] += 1
    return T, S, E


# ---------------------------------------------------------------- level 3: the search for the order
class XL:
    """x log x for integer counts, from a table that grows"""
    t = [0.0, 0.0]

    @classmethod
    def upto(cls, n):
        for v in range(len(cls.t), n + 1):
            cls.t.append(v * math.log(v))
        return cls.t


def objective(order, T, S):
    """the likelihood's part that depends on the order, computed whole; the search's running figure must agree with it"""
    pos = {x: i for i, x in enumerate(order)}
    n = len(order)
    b, r = [0] * n, list(S)
    back = 0.0
    tot = sum(map(sum, T)) + sum(S) + 2
    xl = XL.upto(tot)
    for x in range(n):
        for y in range(n):
            if T[x][y] and pos[y] < pos[x]:
                b[x] += T[x][y]
                r[y] += T[x][y]
                back -= xl[T[x][y]]
    return back + sum(xl[v] for v in b) + sum(xl[v] for v in r) - xl[sum(r)]


def climb(order, T, S, rng):
    """insertion moves: each unit walks left and right past its neighbours, the score kept by increments"""
    n = len(order)
    order = list(order)
    pos = {x: i for i, x in enumerate(order)}
    tot = sum(map(sum, T)) + sum(S) + 2
    xl = XL.upto(tot)
    b, r = [0] * n, list(S)
    for x in range(n):
        for y in range(n):
            if T[x][y] and pos[y] < pos[x]:
                b[x] += T[x][y]
                r[y] += T[x][y]
    rs = sum(r)
    for _ in range(30):
        moved = False
        items = list(range(n))
        rng.shuffle(items)
        for x in items:
            i = order.index(x)
            best, bestj = 1e-9, i
            bx, rx, rsum, cum = b[x], r[x], rs, 0.0
            for j in range(i - 1, -1, -1):        # x passes the unit on its left: n->x becomes back, x->n forward
                m = order[j]
                tx, tm = T[x][m], T[m][x]
                nbx, nbm = bx - tx, b[m] + tm
                nrm, nrx = r[m] - tx, rx + tm
                cum += xl[tx] - xl[tm] + xl[nbx] - xl[bx] + xl[nbm] - xl[b[m]] + xl[nrm] - xl[r[m]] + xl[nrx] - xl[rx]
                bx, rx = nbx, nrx
                rsum += tm - tx
                gain = cum - xl[rsum] + xl[rs]
                if gain > best:
                    best, bestj = gain, j
            bx, rx, rsum, cum = b[x], r[x], rs, 0.0
            for j in range(i + 1, n):             # x passes the unit on its right: x->n becomes back, n->x forward
                m = order[j]
                tx, tm = T[x][m], T[m][x]
                nbx, nbm = bx + tx, b[m] - tm
                nrm, nrx = r[m] + tx, rx - tm
                cum += xl[tm] - xl[tx] + xl[nbx] - xl[bx] + xl[nbm] - xl[b[m]] + xl[nrm] - xl[r[m]] + xl[nrx] - xl[rx]
                bx, rx = nbx, nrx
                rsum += tx - tm
                gain = cum - xl[rsum] + xl[rs]
                if gain > best:
                    best, bestj = gain, j
            if bestj != i:
                step = -1 if bestj < i else 1
                for j in range(i + step, bestj + step, step):
                    m = order[j]
                    tx, tm = T[x][m], T[m][x]
                    if step < 0:
                        b[x] -= tx
                        b[m] += tm
                        r[m] -= tx
                        r[x] += tm
                        rs += tm - tx
                    else:
                        b[x] += tx
                        b[m] -= tm
                        r[m] += tx
                        r[x] -= tm
                        rs += tx - tm
                order.pop(i)
                order.insert(bestj, x)
                moved = True
        if not moved:
            break
    return order


def search(T, S, rng, starts, warm=None):
    n = len(S)
    best, score = None, -float('inf')
    runs = ([list(warm)] if warm is not None else []) + [rng.sample(range(n), n) for _ in range(starts)]
    for o in runs:
        c = climb(o, T, S, rng)
        v = objective(c, T, S)
        if v > score + 1e-9:
            best, score = c, v
    return best


def window_counts(units_by_story, idx, d):
    """W[x][y]: how often x stands before y, at most d places apart, in the same story"""
    n = len(idx)
    W = [[0] * n for _ in range(n)]
    for s in units_by_story:
        ids = [idx[u] for u in s]
        for i, x in enumerate(ids):
            for y in ids[i + 1:i + 1 + d]:
                W[x][y] += 1
    return W


def forward_sum(order, W):
    pos = {x: i for i, x in enumerate(order)}
    n = len(order)
    return sum(W[x][y] for x in range(n) for y in range(n) if pos[x] < pos[y])


def climb_window(order, W, rng):
    """insertion moves on the sum of forward precedence"""
    n = len(order)
    order = list(order)
    for _ in range(30):
        moved = False
        items = list(range(n))
        rng.shuffle(items)
        for x in items:
            i = order.index(x)
            best, bestj = 0, i
            cum = 0
            for j in range(i - 1, -1, -1):
                m = order[j]
                cum += W[x][m] - W[m][x]
                if cum > best:
                    best, bestj = cum, j
            cum = 0
            for j in range(i + 1, n):
                m = order[j]
                cum += W[m][x] - W[x][m]
                if cum > best:
                    best, bestj = cum, j
            if bestj != i:
                order.pop(i)
                order.insert(bestj, x)
                moved = True
        if not moved:
            break
    return order


def order_of(units_by_story, idx, T, S, rng, starts, method, warm=None):
    """the slot order by the given method"""
    if method == 1:
        return search(T, S, rng, starts, warm=warm)
    W = window_counts(units_by_story, idx, method)
    n = len(S)
    best, score = None, -1
    runs = ([list(warm)] if warm is not None else []) + [rng.sample(range(n), n) for _ in range(starts)]
    for o in runs:
        c = climb_window(o, W, rng)
        v = forward_sum(c, W)
        if v > score:
            best, score = c, v
    return best


# ---------------------------------------------------------------- the rival models: each gives a function story -> log likelihood
def unigram_of(T, S, E):
    c = np.array(S, float) + np.array(T, float).sum(0)
    c = np.append(c, float(sum(E)))
    return (c + 0.5) / (c + 0.5).sum()


def score_story(s, idx, start, P):
    """start: first-symbol probabilities; P: matrix with the end in its last column"""
    if not s:
        return 0.0
    ll = math.log(start[idx[s[0]]])
    for a, b in zip(s, s[1:]):
        ll += math.log(P[idx[a]][idx[b]])
    return ll + math.log(P[idx[s[-1]]][-1])


def unigram_model(T, S, E):
    U = unigram_of(T, S, E)
    n = len(S)
    return U[:n] / U[:n].sum() * 1.0, np.tile(U, (n, 1))


def bigram_model(T, S, E, beta):
    n = len(S)
    U = unigram_of(T, S, E)
    A = np.array(T, float)
    C = np.concatenate([A, np.array(E, float)[:, None]], 1)
    P = (C + beta * U) / (C.sum(1, keepdims=True) + beta)
    st = (np.array(S, float) + 0.5) / (sum(S) + 0.5 * n)
    return st, P


def slot_model(T, S, E, order, beta, restarts, window=0):
    """restarts: (1 - r_x - s_x) F_x + r_x R + s_x L_x, with one R for all, and L a slip back of at most `window` slots;
    otherwise one pass: (1 - e) F_x + e U, with one e for all"""
    n = len(S)
    U = unigram_of(T, S, E)
    A = np.array(T, float)
    rank = np.zeros(n, int)
    rank[order] = np.arange(n)
    fwd = rank[None, :] >= rank[:, None]
    Ef = np.array(E, float)[:, None]
    F_counts = np.concatenate([A * fwd, Ef], 1)
    mask = np.concatenate([fwd, np.ones((n, 1), bool)], 1)
    Uf = U[None, :] * mask
    Uf = Uf / Uf.sum(1, keepdims=True)
    F = (F_counts + beta * Uf) / (F_counts.sum(1, keepdims=True) + beta)
    if not restarts:
        Bt = (A * (~fwd)).sum(1)
        e = (Bt.sum() + 0.5) / (F_counts.sum() + Bt.sum() + 1.0)
        P = (1 - e) * F + e * U[None, :]
        st = (np.array(S, float) + 0.5) / (sum(S) + 0.5 * n)
        return st, P, F, np.full(n, e), U, np.zeros((n, n + 1))
    dist = rank[:, None] - rank[None, :]             # x's rank less y's: positive is a step back
    near = (dist >= 1) & (dist <= window)
    far = (~fwd) & (~near)
    Bfar, Bnear = A * far, A * near
    Nt = F_counts.sum(1) + Bfar.sum(1) + Bnear.sum(1)
    r = (Bfar.sum(1) + 0.5) / (Nt + 1.0)
    Rc = Bfar.sum(0) + np.array(S, float)
    R = (Rc + 0.5) / (Rc.sum() + 0.5 * n)
    Rx = np.append(R, 0.0)
    L = np.zeros((n, n + 1))
    if window:
        d = np.array([(Bnear * (dist == k)).sum() for k in range(1, window + 1)]) + 0.5
        d = d / d.sum()
        for k in range(1, window + 1):
            L[:, :n] += d[k - 1] * (dist == k)
        tot = L.sum(1, keepdims=True)
        L = np.where(tot > 0, L / np.where(tot > 0, tot, 1), 0.0)
        sl = np.where(tot[:, 0] > 0, (Bnear.sum() + 0.5) / (Nt.sum() + 1.0), 0.0)
    else:
        sl = np.zeros(n)
    Fw = np.clip(1 - r - sl, 1e-6, None)
    P = Fw[:, None] * F + r[:, None] * Rx[None, :] + sl[:, None] * L
    tot = P.sum(1, keepdims=True)
    Pfs = (Fw[:, None] * F + sl[:, None] * L) / tot
    P = P / tot
    return R, P, F, r / tot[:, 0], Rx, Pfs


# ---------------------------------------------------------------- the free HMM
def hmm_forward(pi, A, Em, X, lens):
    N, T = X.shape
    K = len(pi)
    alpha = np.zeros((N, T, K))
    c = np.ones((N, T))
    alpha[:, 0] = pi[None, :] * Em[:, X[:, 0]].T
    c[:, 0] = alpha[:, 0].sum(1)
    alpha[:, 0] /= c[:, 0, None]
    for t in range(1, T):
        v = (alpha[:, t - 1] @ A) * Em[:, X[:, t]].T
        s = v.sum(1)
        live = t < lens
        c[live, t] = s[live]
        alpha[live, t] = v[live] / s[live, None]
    return alpha, c


def hmm_fit(seqs, K, V, rng):
    lens = np.array([len(x) for x in seqs])
    T = lens.max()
    X = np.zeros((len(seqs), T), int)
    for n, x in enumerate(seqs):
        X[n, :len(x)] = x
    pi = rng.dirichlet(np.ones(K))
    A = rng.dirichlet(np.ones(K), K)
    Em = rng.dirichlet(np.ones(V), K)
    for _ in range(HMM_ITERS):
        alpha, c = hmm_forward(pi, A, Em, X, lens)
        N = len(seqs)
        beta = np.ones((N, T, K))
        xi = np.zeros((K, K))
        for t in range(T - 2, -1, -1):
            live = t + 1 < lens
            b = Em[:, X[:, t + 1]].T * beta[:, t + 1]
            v = (b @ A.T)
            v = v / c[:, t + 1, None]
            beta[live, t] = v[live]
            if live.any():
                xi += (alpha[live, t].T @ (b[live] / c[live, t + 1, None])) * A
        gamma = alpha * beta
        em = np.zeros((K, V)) + 0.01
        for n in range(N):
            np.add.at(em.T, X[n, :lens[n]], gamma[n, :lens[n]])
        pi = gamma[:, 0].sum(0) + 0.01
        pi = pi / pi.sum()
        A = (xi + 0.01) / (xi + 0.01).sum(1, keepdims=True)
        Em = em / em.sum(1, keepdims=True)
    ll = np.log(np.where(c > 0, c, 1.0)).sum()
    return ll, pi, A, Em


def hmm_score(seqs, model):
    _, pi, A, Em = model
    out = []
    for x in seqs:
        alpha, c = hmm_forward(pi, A, Em, x[None, :], np.array([len(x)]))
        out.append(float(np.log(c[0]).sum()))
    return out


# ---------------------------------------------------------------- level 2's candidates
def links(stories, vocab, seed):
    """adjacent pairs far above within-story shuffles: {(x, y): (count, lift, p)}"""
    idx = {u: i for i, u in enumerate(vocab)}
    n = len(vocab)
    seqs = [np.array([idx[u] for u in s], int) for s in stories if len(s) > 1]
    def count(ss):
        M = np.zeros((n, n), int)
        for x in ss:
            np.add.at(M, (x[:-1], x[1:]), 1)
        return M
    obs = count(seqs)
    rng = np.random.default_rng(seed)
    ge = np.zeros((n, n), int)
    tot = np.zeros((n, n), float)
    for _ in range(LINK_SHUFFLES):
        M = count([rng.permutation(x) for x in seqs])
        ge += M >= obs
        tot += M
    out = {}
    for i in range(n):
        for j in range(n):
            e = tot[i, j] / LINK_SHUFFLES
            if obs[i, j] >= LINK_MIN and e > 0:
                lift, p = obs[i, j] / e, (ge[i, j] + 1) / (LINK_SHUFFLES + 1)
                if p <= LINK_P and lift >= LINK_LIFT and vocab[i] != RARE and vocab[j] != RARE:
                    out[(vocab[i], vocab[j])] = (int(obs[i, j]), float(lift), float(p))
    return out


def merge_candidates(units, vocab):
    """pairs by the likeness of their left and right neighbours"""
    idx = {u: i for i, u in enumerate(vocab)}
    n = len(vocab)
    C = np.zeros((n, 2 * n))
    occ = np.zeros(n)
    for s in units:
        for t, u in enumerate(s):
            occ[idx[u]] += 1
            if t > 0:
                C[idx[u], idx[s[t - 1]]] += 1
            if t + 1 < len(s):
                C[idx[u], n + idx[s[t + 1]]] += 1
    norm = np.linalg.norm(C, axis=1)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            if occ[i] >= 5 and occ[j] >= 5 and norm[i] > 0 and norm[j] > 0 and RARE not in (vocab[i], vocab[j]):
                out.append((-float(C[i] @ C[j] / (norm[i] * norm[j])), i, j))
    out.sort()
    return [(vocab[i], vocab[j]) for _, i, j in out[:L2_TRIES]]


def vocab_of(units):
    v, have = [], set()
    for s in units:
        for u in s:
            if u not in have:
                have.add(u)
                v.append(u)
    return v


def member_terms(chosen_train, chosen_test):
    """log P(member | class), from the training stories, for each test story"""
    c = {}
    for ch in chosen_train:
        for k, m in ch:
            c.setdefault(k, {})
            c[k][m] = c[k].get(m, 0) + 1
    out = []
    for ch in chosen_test:
        ll = 0.0
        for k, m in ch:
            d = c.get(k, {})
            ll += math.log((d.get(m, 0) + 0.5) / (sum(d.values()) + 1.0))
        out.append(ll)
    return out


def slot_cv(stories, ops, folds, seed, starts, grid=(L2_GRID,), restarts=True, method=1):
    """per-story held-out likelihood of the slot grammar over these units, for each (beta, window) in the grid"""
    parsed = [apply_ops(s, ops) for s in stories]
    units = [p[0] for p in parsed]
    chosen = [p[1] for p in parsed]
    vocab = vocab_of(units)
    idx = {u: i for i, u in enumerate(vocab)}
    res = {g: np.zeros(len(stories)) for g in grid}
    for f, test in enumerate(folds):
        ts = set(test)
        train = [i for i in range(len(stories)) if i not in ts]
        T, S, E = counts([units[i] for i in train], idx)
        order = order_of([units[i] for i in train], idx, T, S, random.Random(seed + f), starts, method)
        mem = member_terms([chosen[i] for i in train], [chosen[i] for i in test])
        for g in res:
            m = slot_model(T, S, E, order, g[0], restarts, g[1])
            for k, i in enumerate(test):
                res[g][i] = score_story(units[i], idx, m[0], m[1]) + mem[k]
    return res


def level2(stories, vocab, folds, seed):
    """greedy joins and merges, each kept only if held-out likelihood rises by L2_GAIN and by a paired test over stories"""
    ops = []
    cur = slot_cv(stories, ops, folds, seed, L2_STARTS)[L2_GRID]
    tried = set()
    for _ in range(L2_MAX):
        units = [apply_ops(s, ops)[0] for s in stories]
        v = vocab_of(units)
        lk = links(units, v, seed)
        cand = sorted(lk, key=lambda p: (lk[p][2], -lk[p][1], v.index(p[0]), v.index(p[1])))[:L2_TRIES]
        options = [('join', x, y) for x, y in cand] + [('merge', x, y) for x, y in merge_candidates(units, v)]
        best, bestv = None, None
        for kind, x, y in options:
            if (kind, x, y) in tried:
                continue
            tried.add((kind, x, y))
            name = ('%s+%s' if kind == 'join' else '%s|%s') % (x, y)
            val = slot_cv(stories, ops + [(kind, x, y, name)], folds, seed, L2_STARTS)[L2_GRID]
            if val.sum() > cur.sum() + L2_GAIN and flip_p(val, cur, seed) <= ALPHA and (bestv is None or val.sum() > bestv.sum()):
                best, bestv = (kind, x, y, name), val
        if best is None:
            break
        ops.append(best)
        cur = bestv
    return ops


# ---------------------------------------------------------------- the rivals on held-out stories
def flip_p(a, b, seed):
    """one-sided paired sign-flip: a beats b"""
    d = np.asarray(a) - np.asarray(b)
    if d.mean() <= 0:
        return 1.0
    rng = np.random.default_rng(seed)
    s = rng.choice([-1.0, 1.0], size=(FLIPS, len(d)))
    return float((((s * d).mean(1) >= d.mean() - 1e-12).sum() + 1) / (FLIPS + 1))


def rivals(stories, vocab, ops, folds, seed):
    n = len(stories)
    idx = {u: i for i, u in enumerate(vocab)}
    uni = np.zeros(n)
    bi = {b: np.zeros(n) for b in BETAS}
    for f, test in enumerate(folds):
        ts = set(test)
        tr = [stories[i] for i in range(n) if i not in ts]
        T, S, E = counts(tr, idx)
        st, P = unigram_model(T, S, E)
        for i in test:
            uni[i] = score_story(stories[i], idx, st, P)
        for b in BETAS:
            st, P = bigram_model(T, S, E, b)
            for i in test:
                bi[b][i] = score_story(stories[i], idx, st, P)
    out = {'unigram': uni, 'bigram': max(bi.values(), key=lambda v: v.sum())}
    by = {m: slot_cv(stories, ops, folds, seed, CV_STARTS, method=m)[L2_GRID].sum() for m in METHODS}
    method = max(METHODS, key=lambda m: (by[m], -m))
    sr = slot_cv(stories, ops, folds, seed, CV_STARTS, grid=[(b, w) for b in BETAS for w in WINDOWS], restarts=True, method=method)
    s1 = slot_cv(stories, ops, folds, seed, CV_STARTS, grid=[(b, 0) for b in BETAS], restarts=False, method=method)
    bestg = max(sr, key=lambda g: (sr[g].sum(), -g[0], -g[1]))
    out['slots'] = sr[bestg]
    out['one pass'] = max(s1.values(), key=lambda v: v.sum())
    # the HMM: base symbols and an end symbol; K by the same held-out score (slightly in its favour)
    V = len(vocab) + 1
    enc = [np.array([idx[u] for u in s] + [V - 1], int) for s in stories]
    bestK, bestv, bestk = None, None, None
    for K in HMM_KS:
        res = np.zeros(n)
        for f, test in enumerate(folds):
            ts = set(test)
            tr = [enc[i] for i in range(n) if i not in ts]
            rng = np.random.default_rng([seed, K, f])
            fits = [hmm_fit(tr, K, V, rng) for _ in range(HMM_STARTS)]
            m = max(fits, key=lambda x: x[0])
            sc = hmm_score([enc[i] for i in test], m)
            for k, i in enumerate(test):
                res[i] = sc[k]
        if bestv is None or res.sum() > bestv.sum():
            bestK, bestv = K, res
    out['hmm'] = bestv
    return out, bestK, bestg, method


def shape_of(cv, seed, coverage):
    """Is there an order? and, apart from that, which shape predicts? The bigram holds the slot grammar inside it, so it will
    always win with enough data: beating it cannot be the test of order. Ordered means: the slots beat the unigram, keep at
    least RATIO of what the bigram gains, and the bootstrap's partial order covers at least COVERAGE of the pairs."""
    steps = {'slots over one pass': flip_p(cv['slots'], cv['one pass'], seed)}
    slot = 'slots' if steps['slots over one pass'] <= ALPHA else 'one pass'
    gain_s = cv[slot].sum() - cv['unigram'].sum()
    gain_b = cv['bigram'].sum() - cv['unigram'].sum()
    steps['slots over unigram'] = flip_p(cv[slot], cv['unigram'], seed)
    steps['ratio'] = float(gain_s / gain_b) if gain_b > 0 else 0.0
    if steps['slots over unigram'] <= ALPHA and gain_b > 0 and steps['ratio'] >= RATIO and coverage >= COVERAGE:
        return ('ordered passes' if slot == 'slots' else 'one ordered pass'), True, steps
    cur = 'unigram'
    for c in ('bigram', 'hmm'):
        p = flip_p(cv[c], cv[cur], seed)
        steps['%s over %s' % (c, cur)] = p
        if p <= ALPHA:
            cur = c
    p = flip_p(cv[slot], cv[cur], seed)
    steps['slots over %s' % cur] = p
    if p <= ALPHA:
        cur = 'local order'
    return cur, False, steps


# ---------------------------------------------------------------- level 4
def bootstrap_order(units, idx, order, seed, boots=BOOTSTRAPS, method=1):
    n = len(idx)
    before = np.zeros((n, n))
    both = np.zeros((n, n))
    rng = random.Random(seed)
    m = len(units)
    for _ in range(boots):
        pick = [units[rng.randrange(m)] for _ in range(m)]
        T, S, E = counts(pick, idx)
        o = order_of(pick, idx, T, S, rng, BOOT_STARTS, method, warm=order)
        present = {i for s in pick for i in (idx[u] for u in s)}
        rank = {x: r for r, x in enumerate(o)}
        for x in present:
            for y in present:
                if x != y:
                    both[x, y] += 1
                    if rank[x] < rank[y]:
                        before[x, y] += 1
    return before, both


def passes_of(units, idx, model):
    """where a restart is the likelier reading of a step than going forward or slipping back: cuts, as unit positions"""
    _, _, _, r, Rx, Pfs = model
    out = []
    for s in units:
        cuts = []
        for t, (a, b) in enumerate(zip(s, s[1:])):
            i, j = idx[a], idx[b]
            if r[i] * Rx[j] > Pfs[i, j]:
                cuts.append(t + 1)
        out.append(cuts)
    return out


def branches(pass_lists, vocab):
    """units that share a pass far less than chance; pass_lists: passes of units"""
    from scipy.stats import hypergeom
    P = len(pass_lists)
    has = {u: set() for u in vocab}
    for i, p in enumerate(pass_lists):
        for u in p:
            has[u].add(i)
    out = []
    for a in range(len(vocab)):
        for b in range(a + 1, len(vocab)):
            x, y = vocab[a], vocab[b]
            if RARE in (x, y) or len(has[x]) < 5 or len(has[y]) < 5:
                continue
            k = len(has[x] & has[y])
            e = len(has[x]) * len(has[y]) / P
            p = hypergeom.cdf(k, P, len(has[x]), len(has[y]))
            if p <= 0.01 and k <= 0.25 * e:
                out.append((x, y, k, round(e, 2), float(p)))
    return out


# ---------------------------------------------------------------- the whole
def fit(raw, seed=20261104, boots=BOOTSTRAPS, starts=ORDER_STARTS):
    stories, vocab = canon(raw)
    stories = [s for s in stories if s]
    folds = folds_of(len(stories), seed)
    ops = level2(stories, vocab, folds, seed)
    cv, K, grid, method = rivals(stories, vocab, ops, folds, seed)
    parsed = [apply_ops(s, ops) for s in stories]
    units = [p[0] for p in parsed]
    uv = vocab_of(units)
    idx = {u: i for i, u in enumerate(uv)}
    T, S, E = counts(units, idx)
    order = order_of(units, idx, T, S, random.Random(seed), starts, method)
    before, both = bootstrap_order(units, idx, order, seed, boots, method)
    rel = []
    n = len(uv)
    with np.errstate(divide='ignore', invalid='ignore'):
        share = np.where(both > 0, before / both, 0.0)
    for x in range(n):
        for y in range(n):
            if x != y and RARE not in (uv[x], uv[y]) and both[x, y] >= 0.5 * boots and share[x, y] >= SUPPORT:
                rel.append((uv[x], uv[y]))
    real = [u for u in uv if u != RARE]
    pairs = len(real) * (len(real) - 1) / 2
    coverage = len(rel) / pairs if pairs else 0.0
    shape, ordered, steps = shape_of(cv, seed, coverage)
    model = slot_model(T, S, E, order, grid[0], True, grid[1])
    cuts = passes_of(units, idx, model)
    plist = []
    for s, c in zip(units, cuts):
        e = [0] + c + [len(s)]
        plist += [s[e[i]:e[i + 1]] for i in range(len(e) - 1)]
    # base-level results, for whoever scores them
    base_rel = set()
    for x, y in rel:
        for a in expand(x, ops):
            for b in expand(y, ops):
                if a != b:
                    base_rel.add((a, b))
    for kind, x, y, name in ops:
        if kind == 'join':
            for a in expand(x, ops):
                for b in expand(y, ops):
                    if a != b:
                        base_rel.add((a, b))
    base_order = []
    for x in order:
        base_order += [u for u in expand(uv[x], ops) if u != RARE]
    base_cuts = []
    for s0, s, c in zip(stories, units, cuts):
        pos, k, out = 0, set(c), []
        sp = spans_of(s0, ops)
        for t, u in enumerate(s):
            if t in k:
                out.append(pos)
            pos += sp[t]
        base_cuts.append(out)
    lk = links(stories, vocab, seed)
    return {
        'shape': shape, 'ordered': bool(ordered), 'coverage': coverage, 'steps': steps, 'hmm_K': K, 'beta_window': list(grid), 'method': method,
        'cv': {k: float(v.sum()) for k, v in cv.items()},
        'symbols': len(real), 'units': [u for u in uv], 'ops': [list(o) for o in ops],
        'order': base_order, 'relations': sorted(base_rel), 'links': sorted((x, y) for x, y in lk),
        'branches': branches(plist, uv), 'cuts': base_cuts, 'stories': len(stories),
    }
