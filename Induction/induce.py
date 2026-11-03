#!/usr/bin/env python3
"""
induce.py -- grammar induction (Induction/InductionProtocol.md, frozen 2026-11-03 at the owner's word): a corpus's own order,
pairs, blocks and sections, from its own strings, without Propp's.

  python induce.py i1                      test I1: a planted 10-state grammar recovered; planted pairs confirmed, few others
  python induce.py i2                      test I2: the wondertales shuffled within each move fail the self-test
  python induce.py i3                      test I3: no checking-half story in any induction-half count
  python induce.py t                       test T: two inductions byte-identical (not shown)
  python induce.py induce <layer> <corpus> the induction half: write Induced-<layer>-<corpus>.json and .txt and the grammars
  python induce.py check <layer> <corpus>  the checking half, once the induced files are committed: write Checked-<layer>-<corpus>.txt
                                           (for functions tale, the self-test; for acts tale, the act layer's self-test)

Layers: functions, acts. Every induction and check is per transcriber A and B; the pairs need both.

How the protocol's words are read here:
- P1. A story's count for i, j is the weighted number of pairs of an i and a j in the same move with i first (each version
  weighted 1 over the story's versions); a story votes for i first when its count for i, j is above its count for j, i.
  Functions "in at least 5 stories" are counted on the induction half.
- P2. A relation is dropped from the Hasse list when its second can be reached from its first through other relations.
  The linear order is by Copeland score, ties by Propp's number and then by name.
- Q1. The count of y after x anywhere later in the same move, weighted as in P1; the null shuffles each move 1,000 times
  (seed 46); candidates need both transcribers on the induction half, confirmation both on the checking half. A Propp pair
  "occurs at least 5 times" when its count on the checking half is at least 5 for both transcribers.
- Q2. A block is a maximal clique of three or more in the graph of confirmed pairs whose pairs, each confirmed one way
  only, make no cycle; it is written in that order. Each block is set against Propp's pairs by the share of its ordered
  pairs that are his.
- H1. Each move is a sequence ending in an emitted end symbol; tokens unseen in the induction half are one unknown symbol.
  Baum-Welch stops at a relative gain under 1e-6 or 500 iterations; emissions get 0.01 added to every count.
- H2. The five folds are the induction half's stories, sorted, shuffled with the seed, dealt in turn; each fold's
  log-likelihood per symbol (units and ends) is taken; ties of K go to the smaller.
- H3. A function's section is the state of the largest occupancy times emission. A state's place is the mean relative
  position (0 to 1 within the move) of the units it is credited with, by the posteriors.
- S1. Propp's section of a function is constraintGrammar.SEC's. The states' order agrees with his when Kendall's tau between
  the place of each eligible function's state and its section's index is at least 0.6. The bar: the index above at least
  950 of 1,000 random assignments with the same section sizes (the induced labels permuted).
- S3 needs both transcribers, as Q1 does; so a transcriber passes when its S1 and S2 hold and S3 holds.
- The act layer's self-test: each act token takes the most common section of the function units at its event in the
  functions layer (same transcriber letter, card U, rows marked Y), ties to the earlier section; the act tokens of the
  induction half with a section are scored by S1's index and bar.
"""
import collections
import json
import os
import random
import subprocess
import sys

import networkx as nx
import numpy as np
from scipy.stats import binom, kendalltau
from sklearn.metrics import adjusted_rand_score

import strings as ST

HERE = ST.HERE
CG, TS, DT, S = ST.CG, ST.TS, ST.DT, ST.S
SEED = 20261103
NG_SEED = 46
PERMS = 1000
STARTS = 20
KS = list(range(2, 13))
FOLDS = 5
SMOOTH = 0.01
RULE = 0.05
MIN_STORIES = 5
MAX_IT, TOL = 500, 1e-6
UNK, END = '<unknown>', '<end>'
PROPP = {'functions': S.NG.PROPP_PAIRS, 'acts': S.NG.ACT_PAIRS}


def order_key(t):
    return (TS.NUM.get(t, 99), t)


# ---------------------------------------------------------------- the halves
def halves(layer, g, items_by_L):
    sp = ST.read_split()[(layer, g)]
    ind, chk = sp['induction'], sp['checking']
    assert not ind & chk
    out = {}
    for L, items in items_by_L.items():
        out[L] = ([x for x in items if x[0] in ind], [x for x in items if x[0] in chk])
        assert {x[0] for x in out[L][0]} <= ind and not {x[0] for x in out[L][0]} & chk
    return out


def eligible(items):
    by = collections.defaultdict(set)     # a story's versions count once
    for s, _, moves, _ in items:
        for u in {u for mv in moves for u in mv}:
            by[u].add(s)
    return sorted((t for t in by if len(by[t]) >= MIN_STORIES), key=order_key)


# ---------------------------------------------------------------- layer 1
def before_counts(seq, idx, V):
    """M[i, j]: pairs of positions p < q in the sequence with token i at p and j at q, for tokens in idx"""
    xs = [idx[u] for u in seq if u in idx]
    M = np.zeros((V, V))
    if len(xs) > 1:
        O = np.zeros((len(xs), V))
        O[np.arange(len(xs)), xs] = 1
        P = np.cumsum(O, 0) - O
        M = P.T @ O
    return M


def precedence(items, toks):
    idx = {t: i for i, t in enumerate(toks)}
    V = len(toks)
    per = collections.defaultdict(lambda: np.zeros((V, V)))
    for s, w, moves, _ in items:
        for mv in moves:
            per[s] += w * before_counts(mv, idx, V)
    tot = sum(per.values()) if per else np.zeros((V, V))
    return tot, per


def relations(items, toks):
    tot, per = precedence(items, toks)
    rel, info = [], {}
    for i, a in enumerate(toks):
        for j, b in enumerate(toks):
            if i == j or tot[i, j] + tot[j, i] == 0:
                continue
            share = tot[i, j] / (tot[i, j] + tot[j, i])
            k = sum(1 for M in per.values() if M[i, j] > M[j, i])
            m = sum(1 for M in per.values() if M[j, i] > M[i, j])
            both = sum(1 for M in per.values() if M[i, j] + M[j, i] > 0)
            p = float(binom.sf(k - 1, k + m, 0.5)) if k + m else 1.0
            info[(a, b)] = (share, both, k, m, p)
            if share >= 0.75 and both >= 10 and p <= 0.05:
                rel.append((a, b))
    return rel, info, tot


def hasse(rel):
    G = nx.DiGraph(rel)
    keep = []
    for a, b in rel:
        G.remove_edge(a, b)
        if not nx.has_path(G, a, b):
            keep.append((a, b))
        G.add_edge(a, b)
    return keep


def copeland(toks, rel):
    sc = collections.Counter()
    for a, b in rel:
        sc[a] += 1
        sc[b] -= 1
    return sorted(toks, key=lambda t: (-sc[t], order_key(t)))


def tau_propp(order):
    xs = [t for t in order if t in TS.NUM]
    if len(xs) < 3:
        return float('nan'), 1.0
    r = kendalltau(list(range(len(xs))), [TS.NUM[t] for t in xs])
    return float(r[0]), float(r[1])


# ---------------------------------------------------------------- layer 2
def flat(items, vocab):
    """the moves concatenated: token indices, move starts per position, weights"""
    idx = {t: i for i, t in enumerate(vocab)}
    X, mid, W = [], [], []
    m = 0
    for s, w, moves, _ in items:
        for mv in moves:
            for u in mv:
                if u in idx:
                    X.append(idx[u])
                    mid.append(m)
                    W.append(w)
            m += 1
    return np.array(X, int), np.array(mid, int), np.array(W, float)


def after_counts(X, mid, W, V, order=None):
    if order is not None:
        X = X[order]
    O = np.zeros((len(X), V))
    O[np.arange(len(X)), X] = 1
    C = np.cumsum(O, 0)
    starts = np.r_[0, np.flatnonzero(np.diff(mid)) + 1]
    base = np.zeros_like(C)
    run = np.repeat(starts, np.diff(np.r_[starts, len(X)]))
    base = np.where(run[:, None] > 0, C[run - 1], 0)
    P = C - O - base
    return P.T @ (O * W[:, None])


def pair_stats(items, vocab):
    """{(x, y): (count, lift, p)} for every ordered pair of the vocabulary, x before y anywhere later in the move"""
    V = len(vocab)
    X, mid, W = flat(items, vocab)
    if not len(X):
        return {}
    obs = after_counts(X, mid, W, V)
    rng = np.random.default_rng(NG_SEED)
    tot, hit = np.zeros((V, V)), np.zeros((V, V))
    for _ in range(PERMS):
        order = np.lexsort((rng.random(len(X)), mid))
        null = after_counts(X, mid, W, V, order)
        tot += null
        hit += null >= obs - 1e-9
    mean = tot / PERMS
    out = {}
    for i, a in enumerate(vocab):
        for j, b in enumerate(vocab):
            if i != j and obs[i, j] > 0:
                out[(a, b)] = (float(obs[i, j]), float(obs[i, j] / mean[i, j]) if mean[i, j] > 0 else float('inf'),
                               float((hit[i, j] + 1) / (PERMS + 1)))
    return out


def candidates(stats_by_L):
    keys = set.intersection(*[set(st) for st in stats_by_L.values()])
    return sorted((k for k in keys if all(st[k][0] >= 5 and st[k][1] >= 1.5 and st[k][2] <= 0.01 for st in stats_by_L.values())),
                  key=lambda k: (order_key(k[0]), order_key(k[1])))


def blocks(confirmed):
    G = nx.Graph()
    G.add_edges_from(confirmed)
    D = set(confirmed)
    out = []
    for cl in sorted(nx.find_cliques(G), key=lambda c: sorted(c, key=order_key)):
        if len(cl) < 3:
            continue
        sub = [(a, b) for a in cl for b in cl if (a, b) in D]
        if any((b, a) in D for a, b in sub):
            continue
        H = nx.DiGraph(sub)
        if nx.is_directed_acyclic_graph(H):
            out.append(list(nx.lexicographical_topological_sort(H, key=order_key)))
    return out


# ---------------------------------------------------------------- layer 3: the HMM
def encode(items, vocab):
    idx = {t: i for i, t in enumerate(vocab)}
    u, e = idx[UNK], idx[END]
    return [(np.array([idx.get(x, u) for x in mv] + [e], int), w, s) for s, w, moves, _ in items for mv in moves]


def batch(seqs):
    T = max(len(x) for x, _, _ in seqs)
    X = np.zeros((len(seqs), T), int)
    lens = np.array([len(x) for x, _, _ in seqs])
    for n, (x, _, _) in enumerate(seqs):
        X[n, :len(x)] = x
    return X, lens, np.array([w for _, w, _ in seqs], float)


def forward_backward(pi, A, E, X, lens, w, need_beta=True):
    N, T = X.shape
    K = len(pi)
    Bx = E[:, X].transpose(1, 2, 0)
    alpha = np.zeros((N, T, K))
    c = np.ones((N, T))
    a = pi[None] * Bx[:, 0]
    c[:, 0] = a.sum(1)
    alpha[:, 0] = a / c[:, 0, None]
    for t in range(1, T):
        valid = t < lens
        a = (alpha[:, t - 1] @ A) * Bx[:, t]
        ct = np.where(valid, a.sum(1), 1.0)
        alpha[:, t] = np.where(valid[:, None], a / ct[:, None], 0.0)
        c[:, t] = ct
    ll = np.log(c).sum(1)
    if not need_beta:
        return ll, None, None
    beta = np.ones((N, T, K))
    xi = np.zeros((K, K))
    for t in range(T - 2, -1, -1):
        valid = t + 1 < lens
        nb = Bx[:, t + 1] * beta[:, t + 1] / c[:, t + 1, None]
        beta[:, t] = np.where(valid[:, None], nb @ A.T, 1.0)
        ww = w * valid
        xi += A * ((alpha[:, t] * ww[:, None]).T @ nb)
    mask = (np.arange(T)[None] < lens[:, None])
    gamma = alpha * beta * mask[..., None]
    return ll, gamma, xi


def mstep(gamma, xi, X, lens, w, M):
    K = gamma.shape[2]
    pi = (w[:, None] * gamma[:, 0]).sum(0)
    pi /= pi.sum()
    A = xi / np.where(xi.sum(1, keepdims=True) > 0, xi.sum(1, keepdims=True), 1)
    A[xi.sum(1) == 0] = 1.0 / K
    mask = np.arange(X.shape[1])[None] < lens[:, None]
    Ec = np.zeros((M, K))
    np.add.at(Ec, X[mask], (gamma * w[:, None, None])[mask])
    E = Ec.T + SMOOTH
    E /= E.sum(1, keepdims=True)
    return pi, A, E


def fit_once(seqs, K, M, rng):
    X, lens, w = batch(seqs)
    pi = rng.dirichlet(np.ones(K))
    A = rng.dirichlet(np.ones(K), K)
    E = rng.dirichlet(np.ones(M), K)
    prev = -np.inf
    for _ in range(MAX_IT):
        ll, gamma, xi = forward_backward(pi, A, E, X, lens, w)
        tot = float((w * ll).sum())
        if tot - prev < TOL * abs(tot):
            break
        prev = tot
        pi, A, E = mstep(gamma, xi, X, lens, w, M)
    ll, _, _ = forward_backward(pi, A, E, X, lens, w, need_beta=False)
    return float((w * ll).sum()), pi, A, E


_POOL = []


def _start(args):
    seqs, K, M, seed, st = args
    return fit_once(seqs, K, M, np.random.default_rng([seed, K, st]))


def fit(seqs, K, M, seed):
    """the best of the starts, taken in start order (the starts run in parallel; the choice does not depend on it)"""
    if not _POOL:
        import multiprocessing
        _POOL.append(multiprocessing.Pool(min(4, os.cpu_count() or 1)))
    best = None
    for r in _POOL[0].map(_start, [(seqs, K, M, seed, st) for st in range(STARTS)]):
        if best is None or r[0] > best[0] + 1e-9:
            best = r
    return best


def loglik(model, seqs):
    _, pi, A, E = model
    X, lens, w = batch(seqs)
    ll, _, _ = forward_backward(pi, A, E, X, lens, w, need_beta=False)
    return float((w * ll).sum()), float((w * lens).sum())


def choose_k(seqs, M, seed):
    ids = sorted({s for _, _, s in seqs})
    random.Random(seed).shuffle(ids)
    fold = {s: i % FOLDS for i, s in enumerate(ids)}
    table = []
    for K in KS:
        per = []
        for f in range(FOLDS):
            tr = [x for x in seqs if fold[x[2]] != f]
            te = [x for x in seqs if fold[x[2]] == f]
            if not tr or not te:
                continue
            ll, n = loglik(fit(tr, K, M, seed + f), te)
            per.append(ll / n)
        table.append((K, float(np.mean(per))))
    best = max(table, key=lambda r: (round(r[1], 12), -r[0]))
    return best[0], table


def sections(model, seqs, vocab):
    """{token: state} for the units, and the states' places (mean relative position of the units credited to them)"""
    _, pi, A, E = model
    X, lens, w = batch(seqs)
    _, gamma, _ = forward_backward(pi, A, E, X, lens, w)
    K = len(pi)
    occ = np.zeros(K)
    place, mass = np.zeros(K), np.zeros(K)
    for n in range(len(seqs)):
        nu = lens[n] - 1
        for t in range(nu):
            g = gamma[n, t] * w[n]
            occ += g
            place += g * (t / (nu - 1) if nu > 1 else 0.0)
            mass += g
    pos = np.where(mass > 0, place / np.where(mass > 0, mass, 1), 1.0)
    rank = {k: r for r, k in enumerate(sorted(range(K), key=lambda k: (pos[k], k)))}
    assign = {}
    for i, t in enumerate(vocab):
        if t not in (UNK, END):
            assign[t] = rank[int(np.argmax(occ * E[:, i]))]
    return assign, [float(pos[k]) for k in sorted(range(K), key=lambda k: (pos[k], k))], rank


def grammar_text(model, vocab, rank, title):
    _, pi, A, E = model
    K = len(pi)
    inv = {r: k for k, r in rank.items()}
    name = lambda r: 'S%d' % (r + 1)
    lines = ['(* %s *)' % title, '(* states in order of their place in the move; rules of probability at least %.2f *)' % RULE]
    lines.append('move = %s ;' % ' | '.join('%s (* %.2f *)' % (name(rank[k]), pi[k]) for k in sorted(range(K), key=lambda k: rank[k]) if pi[k] >= RULE))
    e = vocab.index(END)
    for r in range(K):
        k = inv[r]
        emits = [(vocab[i], E[k, i]) for i in np.argsort(-E[k]) if E[k, i] >= RULE and i != e]
        nxt = [(name(rank[j]), A[k, j]) for j in sorted(range(K), key=lambda j: rank[j]) if A[k, j] >= RULE]
        end = E[k, e]
        lines.append('%s = ( %s ) , ( %s%s ) ;' % (
            name(r), ' | '.join('%s (* %.2f *)' % kv for kv in emits) or '?',
            ' | '.join('%s (* %.2f *)' % kv for kv in nxt), ' | end (* %.2f *)' % end if end >= RULE else ''))
    return '\n'.join(lines) + '\n'


def baselines(train, test, vocab):
    """log-likelihood per symbol on test of the unigram and the bigram, fitted on train, 0.01 added to every count"""
    M = len(vocab)
    uni = np.full(M, SMOOTH)
    bi = np.full((M + 1, M), SMOOTH)
    for x, w, _ in train:
        prev = M
        for t in x:
            uni[t] += w
            bi[prev, t] += w
            prev = t
    uni /= uni.sum()
    bi /= bi.sum(1, keepdims=True)
    lu = lb = n = 0.0
    for x, w, _ in test:
        prev = M
        for t in x:
            lu += w * np.log(uni[t])
            lb += w * np.log(bi[prev, t])
            prev = t
        n += w * len(x)
    return lu / n, lb / n


# ---------------------------------------------------------------- one induction
def vocab_of(items_by_L, layer):
    return {L: sorted({u for _, _, moves, _ in items for mv in moves for u in mv}, key=order_key) + [UNK, END]
            for L, items in items_by_L.items()}


def induce_half(layer, ind_by_L, seed=SEED):
    """everything the induction half gives, per transcriber, as plain data"""
    voc = vocab_of(ind_by_L, layer)
    res = {}
    stats = {}
    for L, items in ind_by_L.items():
        toks = eligible(items)
        rel, info, _ = relations(items, toks)
        order = copeland(toks, rel)
        seqs = encode(items, voc[L])
        K, table = choose_k(seqs, len(voc[L]), seed)
        model = fit(seqs, K, len(voc[L]), seed)
        assign, places, rank = sections(model, seqs, voc[L])
        stats[L] = pair_stats(items, voc[L][:-2])
        res[L] = {'vocab': voc[L], 'eligible': toks, 'relations': rel, 'hasse': hasse(rel), 'order': order,
                  'tau': tau_propp(order) if layer == 'functions' else None,
                  'K': K, 'cv': table, 'loglik': model[0], 'pi': model[1].tolist(), 'A': model[2].tolist(),
                  'E': model[3].tolist(), 'assign': assign, 'places': places,
                  'rank': {str(k): v for k, v in rank.items()}}
    cands = candidates(stats)
    for L in res:
        res[L]['candidates'] = [[a, b] + list(stats[L][(a, b)]) for a, b in cands]
    return res


def model_of(r):
    return (r['loglik'], np.array(r['pi']), np.array(r['A']), np.array(r['E']))


def s1(assign, toks, rng_seed=SEED):
    """(ARI with Propp's sections, the share of 1,000 permuted assignments below it, tau of state place and section)"""
    xs = [t for t in toks if t in assign and t in CG.SEC]
    if len(xs) < 3:
        return float('nan'), 0.0, float('nan')
    lab, prop = [assign[t] for t in xs], [CG.SEC[t] for t in xs]
    ari = adjusted_rand_score(prop, lab)
    rng = np.random.default_rng(rng_seed)
    below = sum(adjusted_rand_score(prop, list(rng.permutation(lab))) < ari - 1e-12 for _ in range(1000)) / 1000
    tau = float(kendalltau(lab, prop)[0])
    return float(ari), float(below), tau


def s1_holds(v):
    return v[1] >= 0.95 and v[2] >= 0.6


def s2_holds(t):
    return t[0] >= 0.6 and t[1] <= 0.05


# ---------------------------------------------------------------- the commands
def files(layer, g):
    base = os.path.join(HERE, '%s-%s-%s' % ('%s', layer, g))
    return base % 'Induced' + '.json', base % 'Induced' + '.txt', base % 'Checked' + '.txt'


def data(layer, g):
    return halves(layer, g, {L: ST.strings(layer, g, L) for L in ST.READERS})


def induced_report(layer, g, res):
    rep = ['# Induced-%s-%s.txt -- induce.py induce: the induction half only (InductionProtocol.md, frozen 2026-11-03)' % (layer, g),
           '#  per transcriber A (Opus) and B (Sonnet)', '']
    for L, r in res.items():
        rep.append('## %s' % L)
        rep.append('P1. eligible (in at least %d stories): %d: %s' % (MIN_STORIES, len(r['eligible']), ' '.join(r['eligible'])))
        rep.append('P2. relations %d; the Hasse list: %s' % (len(r['relations']), ', '.join('%s<%s' % tuple(x) for x in r['hasse'])))
        rep.append('P2. the linear order (Copeland): %s' % ' '.join(r['order']))
        if r['tau']:
            rep.append('P3. Kendall tau with Propp\'s numbering %.3f, p %.4f' % tuple(r['tau']))
        rep.append('H2. K = %d; cross-validated log-likelihood per symbol: %s' % (r['K'], ', '.join('%d %.4f' % tuple(x) for x in r['cv'])))
        bys = collections.defaultdict(list)
        for t, k in r['assign'].items():
            bys[k].append(t)
        for k in range(r['K']):
            rep.append('H3. S%d (place %.2f): %s' % (k + 1, r['places'][k], ' '.join(sorted(bys[k], key=order_key))))
        if layer == 'functions':
            v = s1(r['assign'], r['eligible'])
            rep.append('S1. against Propp\'s sections: ARI %.3f, above %.1f%% of permuted assignments; tau of place and section %.3f: %s'
                       % (v[0], 100 * v[1], v[2], 'holds' if s1_holds(v) else 'does not hold'))
            rep.append('S2. P2\'s order against Propp\'s numbering: %s' % ('holds' if r['tau'] and s2_holds(r['tau']) else 'does not hold'))
        rep.append('')
    L0 = next(iter(res))
    rep.append('Q1. candidate pairs, both transcribers (count, lift, p for A; then B): %d' % len(res[L0]['candidates']))
    for i, c in enumerate(res[L0]['candidates']):
        others = [res[L]['candidates'][i] for L in res]
        rep.append('  %s then %s  %s' % (c[0], c[1], '  '.join('%.1f %.2f %.4f' % tuple(o[2:]) for o in others)))
    ab = [set(map(tuple, res[L]['relations'])) for L in res]
    rep.append('P3. relations in both transcribers over relations in either: %d of %d' % (len(ab[0] & ab[1]), len(ab[0] | ab[1])))
    return '\n'.join(rep) + '\n'


def do_induce(layer, g):
    h = data(layer, g)
    res = induce_half(layer, {L: h[L][0] for L in h})
    j, t, _ = files(layer, g)
    open(j, 'w', encoding='utf-8', newline='\n').write(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=1) + '\n')
    text = induced_report(layer, g, res)
    open(t, 'w', encoding='utf-8', newline='\n').write(text)
    for L, r in res.items():
        open(os.path.join(HERE, 'Grammar-%s-%s-%s.txt' % (g, layer, L)), 'w', encoding='utf-8', newline='\n').write(
            grammar_text(model_of(r), r['vocab'], {int(k): v for k, v in r['rank'].items()},
                         'induced grammar, %s, %s layer, transcriber %s (induce.py, the induction half)' % (g, layer, L)))
    print(text, end='')


def committed(path):
    rel = os.path.relpath(path, ST.ROOT)
    a = subprocess.run(['git', 'ls-files', '--error-unmatch', rel], cwd=ST.ROOT, capture_output=True)
    b = subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', rel], cwd=ST.ROOT)
    return a.returncode == 0 and b.returncode == 0


def event_sections(L):
    """{(story, event): Propp section} from the wondertales' functions, card U, rows marked Y"""
    c = collections.defaultdict(collections.Counter)
    for r in DT.files('functions', S.C.PATS['tale'], L):
        if r['matters'].upper().startswith('Y'):
            for k in TS.key(r['raw']):
                if k in CG.SEC:
                    c[(DT.local(r['story']), int(r['event']))][CG.SEC[k]] += 1
    return {k: sorted(v.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] for k, v in c.items()}


def act_selftest(res, ind_by_L):
    out = {}
    for L, items in ind_by_L.items():
        sec = event_sections(L)
        lab, prop = [], []
        for s, _, moves, evs in items:
            for mv, ev in zip(moves, evs):
                for u, e in zip(mv, ev):
                    if (s, e) in sec and u in res[L]['assign']:
                        lab.append(res[L]['assign'][u])
                        prop.append(sec[(s, e)])
        ari = adjusted_rand_score(prop, lab)
        rng = np.random.default_rng(SEED)
        below = sum(adjusted_rand_score(prop, list(rng.permutation(lab))) < ari - 1e-12 for _ in range(1000)) / 1000
        out[L] = (float(ari), float(below), len(lab))
    return out


def do_check(layer, g):
    j, _, out = files(layer, g)
    if not committed(j):
        raise SystemExit('refusing: %s is not committed as it stands' % os.path.relpath(j, ST.ROOT))
    res = json.load(open(j, encoding='utf-8'))
    h = data(layer, g)
    ind = {L: h[L][0] for L in h}
    chk = {L: h[L][1] for L in h}
    rep = ['# Checked-%s-%s.txt -- induce.py check: the checking half against what the induction half gave' % (layer, g), '']
    stats = {L: pair_stats(chk[L], res[L]['vocab'][:-2]) for L in chk}
    cands = [tuple(c[:2]) for c in res['A']['candidates']]
    conf = [k for k in cands if all(k in stats[L] and stats[L][k][1] > 1 and stats[L][k][2] <= 0.05 for L in stats)]
    rep.append('Q1. confirmed on the checking half, both transcribers: %d of %d candidates' % (len(conf), len(cands)))
    for a, b in conf:
        rep.append('  %s then %s  %s' % (a, b, '  '.join('%.1f %.2f %.4f' % stats[L][(a, b)] for L in stats)))
    pp = PROPP[layer]
    occur = [p for p in pp if all(p in stats[L] and stats[L][p][0] >= 5 for L in stats)]
    found = [p for p in occur if p in conf]
    recall = len(found) / len(occur) if occur else float('nan')
    rep.append('Q3. Propp\'s pairs occurring at least 5 times: %d; confirmed %d (%s); recall %.2f; precision %s'
               % (len(occur), len(found), ', '.join('%s %s' % p for p in found), recall,
                  '%.2f' % (len(found) / len(conf)) if conf else '-'))
    bl = blocks(conf)
    rep.append('Q2. blocks: %d' % len(bl))
    for b in bl:
        prs = [(x, y) for i, x in enumerate(b) for y in b[i + 1:]]
        rep.append('  %s  (Propp\'s pairs %d of %d)' % (' '.join(b), sum(1 for p in prs if p in pp), len(prs)))
    rep.append('')
    verdict = {}
    for L in chk:
        r = res[L]
        ci, _ = precedence(chk[L], r['eligible'])
        idx = {t: i for i, t in enumerate(r['eligible'])}
        held = [(a, b) for a, b in r['relations'] if ci[idx[a], idx[b]] + ci[idx[b], idx[a]] > 0]
        ok = [(a, b) for a, b in held if ci[idx[a], idx[b]] > ci[idx[b], idx[a]]]
        rep.append('## %s' % L)
        rep.append('P3. relations holding again on the checking half: %d of %d with data (%d relations)' % (len(ok), len(held), len(r['relations'])))
        V = r['vocab']
        tr, te = encode(ind[L], V), encode(chk[L], V)
        ll, n = loglik(model_of(r), te)
        lu, lb = baselines(tr, te, V)
        rep.append('H5. log-likelihood per symbol on the checking half: HMM %.4f, unigram %.4f, bigram %.4f: %s'
                   % (ll / n, lu, lb, 'a grammar (beats the unigram)' if ll / n > lu else 'NOT A GRAMMAR (does not beat the unigram)'))
        if layer == 'functions':
            v = s1(r['assign'], r['eligible'])
            verdict[L] = (s1_holds(v), bool(r['tau']) and s2_holds(r['tau']))
            rep.append('S1 %s; S2 %s' % ('holds' if verdict[L][0] else 'does not hold', 'holds' if verdict[L][1] else 'does not hold'))
        rep.append('')
    both = [t for t in res['A']['assign'] if t in res['B']['assign']]
    rep.append('H5. A and B sections agree: ARI %.3f over %d units' % (
        adjusted_rand_score([res['A']['assign'][t] for t in both], [res['B']['assign'][t] for t in both]), len(both)))
    if layer == 'functions' and g == 'tale':
        s3 = recall >= 0.5
        n = sum(1 for L in verdict if verdict[L][0] and verdict[L][1] and s3)
        rep += ['', '## THE SELF-TEST (frozen 2026-11-03): S1 sections, S2 order, S3 pairs',
                'S3: recall %.2f: %s' % (recall, 'holds' if s3 else 'does not hold')]
        for L in verdict:
            rep.append('%s: S1 %s, S2 %s, S3 %s' % (L, *('holds' if x else 'fails' for x in (verdict[L][0], verdict[L][1], s3))))
        rep.append('VERDICT: %s' % ('PASSES' if n == 2 else 'SPLIT' if n == 1 else 'FAILS'))
    elif layer == 'acts' and g == 'tale':
        v = act_selftest(res, ind)
        rep += ['', '## THE ACT LAYER\'S SELF-TEST (reported, not a gate): act states against the sections of the functions at their events']
        for L, (ari, below, n) in v.items():
            rep.append('%s: %d act tokens; ARI %.3f, above %.1f%% of permuted assignments: %s'
                       % (L, n, ari, 100 * below, 'falls into Propp\'s sections' if below >= 0.95 else 'does not'))
    else:
        st = os.path.join(HERE, 'Checked-functions-tale.txt')
        v = [l for l in open(st, encoding='utf-8') if l.startswith('VERDICT')] if os.path.exists(st) else []
        rep += ['', '# the self-test: %s%s' % (v[0].strip() if v else 'NOT YET RUN',
                                              '' if v and 'PASSES' in v[0] else '; THESE ARE THE OUTPUTS OF AN UNVERIFIED TOOL')]
    text = '\n'.join(rep) + '\n'
    open(out, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


# ---------------------------------------------------------------- the tests
def planted(order_free, seed, n=45, length=80):
    """[story items] per transcriber from a 10-state model of 30 tokens (state k emits t{3k..3k+2} with 0.9), and the true
    state of each token. Ordered: the states in turn, staying with 0.875. Order-free: uniform transitions, a fixed length,
    and two planted pairs in each story, p0 just before p1, p2 two before p3."""
    rng = random.Random(seed)
    toks = ['t%02d' % i for i in range(30)]
    true = {t: i // 3 for i, t in enumerate(toks)}
    stories = []
    for s in range(n):
        seq, k = [], 0
        while True:
            seq.append(rng.choice(toks[3 * k:3 * k + 3]) if rng.random() < 0.9 else rng.choice(toks))
            if order_free:
                if len(seq) >= length:
                    break
                k = rng.randrange(10)
            elif rng.random() >= 0.875:
                k += 1
                if k == 10:
                    break
        if order_free:
            i = rng.randrange(len(seq) - 1)
            seq[i:i] = ['p0', 'p1']
            i = rng.randrange(len(seq) - 1)
            seq[i:i] = ['p2', rng.choice(toks), 'p3']
        stories.append(('S%02d' % s, seq))
    out = {}
    for L, ns in (('A', seed + 1), ('B', seed + 2)):
        r = random.Random(ns)
        out[L] = [(s, 1.0, [[u if r.random() >= 0.1 or u.startswith('p') else r.choice(toks) for u in seq]], None) for s, seq in stories]
    return out, true


def i1():
    ok = []
    items, true = planted(False, SEED)
    ind = {L: x[:23] for L, x in items.items()}
    res = induce_half('planted', ind)
    for L, r in res.items():
        xs = [t for t in r['assign'] if t in true]
        ari = adjusted_rand_score([true[t] for t in xs], [r['assign'][t] for t in xs])
        tau = kendalltau(list(range(len([t for t in r['order'] if t in true]))), [true[t] for t in r['order'] if t in true])[0]
        ok += [('%s K %d within 2 of 10' % (L, r['K']), abs(r['K'] - 10) <= 2), ('%s ARI %.3f at least 0.8' % (L, ari), ari >= 0.8),
               ('%s P2 tau %.3f at least 0.8' % (L, tau), tau >= 0.8)]
    items, _ = planted(True, SEED + 7)
    ind = {L: x[:23] for L, x in items.items()}
    chk = {L: x[23:] for L, x in items.items()}
    voc = vocab_of(ind, 'planted')
    st = {L: pair_stats(ind[L], voc[L][:-2]) for L in ind}
    cands = candidates(st)
    sc = {L: pair_stats(chk[L], voc[L][:-2]) for L in chk}
    conf = [k for k in cands if all(k in sc[L] and sc[L][k][1] > 1 and sc[L][k][2] <= 0.05 for L in sc)]
    planted_pairs = {('p0', 'p1'), ('p2', 'p3')}
    others = [k for k in conf if k not in planted_pairs]
    ok += [('Q1 both planted pairs confirmed', planted_pairs <= set(conf)),
           ('Q1 others confirmed %d, at most 2' % len(others), len(others) <= 2)]
    for name, v in ok:
        print('I1 %-40s %s' % (name, 'PASS' if v else 'FAIL'))
    print('I1: %s' % ('PASS' if all(v for _, v in ok) else 'FAIL'))


def i2():
    h = data('functions', 'tale')
    rng = random.Random(SEED)

    def shuf(items):
        out = []
        for s, w, moves, ev in items:
            ms = []
            for mv in moves:
                mv = list(mv)
                rng.shuffle(mv)
                ms.append(mv)
            out.append((s, w, ms, ev))
        return out
    ind = {L: shuf(h[L][0]) for L in h}
    chk = {L: shuf(h[L][1]) for L in h}
    res = induce_half('functions', ind)
    ok = []
    for L, r in res.items():
        v = s1(r['assign'], r['eligible'])
        ok += [('%s S1 fails (ARI above %.1f%%, tau %.2f)' % (L, 100 * v[1], v[2]), not s1_holds(v)),
               ('%s S2 fails (tau %.2f, p %.3f)' % (L, *r['tau']), not s2_holds(r['tau']))]
    cands = [tuple(c[:2]) for c in res['A']['candidates']]
    sc = {L: pair_stats(chk[L], res[L]['vocab'][:-2]) for L in chk}
    conf = [k for k in cands if all(k in sc[L] and sc[L][k][1] > 1 and sc[L][k][2] <= 0.05 for L in sc)]
    ok.append(('Q1 confirms %d, at most 2' % len(conf), len(conf) <= 2))
    for name, v in ok:
        print('I2 %-45s %s' % (name, 'PASS' if v else 'FAIL'))
    print('I2: %s' % ('PASS' if all(v for _, v in ok) else 'FAIL'))


def i3():
    ok = []
    sp = ST.read_split()
    for (layer, g), d in sorted(sp.items()):
        ids = set(ST.stories(layer, g))
        ok.append(('%s %s halves disjoint and whole' % (layer, g), not d['induction'] & d['checking'] and d['induction'] | d['checking'] == ids))
    h = data('functions', 'tale')
    mark = {L: h[L][0] + [(s, w, [['CHECK'] * len(mv) for mv in moves], ev) for s, w, moves, ev in h[L][1]] for L in h}
    split = halves('functions', 'tale', mark)
    seen = any('CHECK' in u for L in split for _, _, moves, _ in split[L][0] for mv in moves for u in mv)
    ok.append(('no checking-half unit in the induction half', not seen))
    voc = vocab_of({L: split[L][0] for L in split}, 'functions')
    ok.append(('no checking-half unit in the vocabulary', all('CHECK' not in v for v in voc.values())))
    bad = [n for n, v in ok if not v]
    print('I3 %d checks, failed %d: %s' % (len(ok), len(bad), 'PASS' if not bad else 'FAIL %s' % bad))


def t():
    h = data('functions', 'tale')
    a = json.dumps(induce_half('functions', {L: h[L][0] for L in h}), ensure_ascii=False, sort_keys=True)
    b = json.dumps(induce_half('functions', {L: h[L][0] for L in h}), ensure_ascii=False, sort_keys=True)
    print('T two inductions of the wondertales byte-identical: %s (not shown)' % ('PASS' if a == b else 'FAIL'))


if __name__ == '__main__':
    a = sys.argv[1:]
    fns = {'i1': i1, 'i2': i2, 'i3': i3, 't': t}
    if len(a) == 1 and a[0] in fns:
        fns[a[0]]()
    elif len(a) == 3 and a[0] in ('induce', 'check') and a[1] in ST.LAYERS and a[2] in ST.LAYERS[a[1]]:
        (do_induce if a[0] == 'induce' else do_check)(a[1], a[2])
    else:
        sys.exit(__doc__)
