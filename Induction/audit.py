#!/usr/bin/env python3
"""
audit.py -- the audit of the failed self-test (Induction/AuditPlan.md, 2026-11-04, at the owner's word). The verdict of
record stands; everything here is reported beside it.

  python audit.py u0     the code: the record reproduced; counts recomputed by plain loops
  python audit.py u5     the bars: Propp's sections merged into K consecutive groups, taken as perfect K-state answers
  python audit.py u2     Propp's own strings under the frozen tool; the closeness of the strings
  python audit.py u3     do the strings fit Propp's sections? the true partition against 10,000 random ones
  python audit.py u4     the tool's choices, one at a time
  python audit.py u1     the power of the test: strings generated from a chain over Propp's sections

Each writes Induction/Audit-<part>.txt. induce.py's functions are called unchanged.
"""
import collections
import itertools
import json
import multiprocessing
import os
import random
import sys

import numpy as np
from rapidfuzz.distance import Levenshtein
from scipy.stats import kendalltau

import induce as I

ST, CG, TS, DT = I.ST, I.CG, I.TS, I.DT
HERE = I.HERE
SEED = I.SEED
NSEC = len(CG.SECTION_NAMES)
FUNCS = sorted(CG.SEC, key=I.order_key)
READ = ['A', 'B', 'Propp']
OUT = []


def say(s=''):
    OUT.append(s)
    print(s, flush=True)


def save(part):
    open(os.path.join(HERE, 'Audit-%s.txt' % part), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


# ---------------------------------------------------------------- the strings
def propp_items():
    """Propp's own strings as items: tragedyScore.key's functions, the markup dropped, alternatives in the order written"""
    moves = collections.OrderedDict()
    for r in DT.rows('resolved'):
        ks = [k for s in r['string'].split() for k in TS.key(s) if k in TS.NUM]
        moves.setdefault(DT.local(r['story']), []).append(ks)
    return [(s, 1.0, ms, None) for s, ms in moves.items() if sum(map(len, ms)) >= 3]


def strings_of():
    """{reader: (induction items, checking items)}"""
    sp = ST.read_split()[('functions', 'tale')]
    out = {}
    for L in 'AB':
        x = ST.strings('functions', 'tale', L)
        out[L] = ([i for i in x if i[0] in sp['induction']], [i for i in x if i[0] in sp['checking']])
    x = propp_items()
    out['Propp'] = ([i for i in x if i[0] in sp['induction']], [i for i in x if i[0] in sp['checking']])
    return out


def record():
    return json.load(open(os.path.join(HERE, 'Induced-functions-tale.json'), encoding='utf-8'))


def core(items, seed=SEED, k_fixed=None):
    """the tool's sections and order on one reader's strings, as induce_half computes them, without the pairs"""
    toks = I.eligible(items)
    rel, _, _ = I.relations(items, toks)
    voc = sorted({u for _, _, ms, _ in items for mv in ms for u in mv}, key=I.order_key) + [I.UNK, I.END]
    seqs = I.encode(items, voc)
    table = None
    if k_fixed:
        K = k_fixed
    else:
        K, table = I.choose_k(seqs, len(voc), seed)
    model = I.fit(seqs, K, len(voc), seed)
    assign, places, rank = I.sections(model, seqs, voc)
    v = I.s1(assign, toks)
    t = I.tau_propp(toks, rel)
    return {'toks': toks, 'rel': rel, 'voc': voc, 'K': K, 'cv': table, 'model': model, 'assign': assign, 'places': places,
            's1': v, 'tau': t, 'S1': I.s1_holds(v), 'S2': I.s2_holds(t)}


def line(c):
    v, t = c['s1'], c['tau']
    return ('K %2d  ARI %+.3f (above %5.1f%%)  state-section tau %+.3f  S1 %-5s  order tau %+.3f (p %.3f)  S2 %-5s  relations %d'
            % (c['K'], v[0], 100 * v[1], v[2], 'holds' if c['S1'] else 'fails', t[0], t[1], 'holds' if c['S2'] else 'fails', len(c['rel'])))


# ---------------------------------------------------------------- U0
def u0():
    say('# Audit-u0.txt -- the code: does the program compute what the protocol says?')
    rec = record()['A']
    x = strings_of()['A'][0]
    c = core(x)
    say('A: K %d, record %d: %s' % (c['K'], rec['K'], 'agree' if c['K'] == rec['K'] else 'DIFFER'))
    say('A: sections %s' % ('agree' if c['assign'] == rec['assign'] else 'DIFFER'))
    same = {tuple(r) for r in c['rel']} == {tuple(r) for r in rec['relations']}
    say('A: relations %s' % ('agree' if same else 'DIFFER'))
    say('A: S1 recomputed ARI %.3f, tau %.3f; S2 tau %.3f (Induced-functions-tale.txt gives 0.008, 0.422, 0.226)' % (c['s1'][0], c['s1'][2], c['tau'][0]))
    # plain loops, independent of the matrix code
    voc = rec['vocab'][:-2]
    X, mid, W = I.flat(x, voc)
    M = I.after_counts(X, mid, W, len(voc))
    bad = 0
    for a, b in [('A', 'B'), ('A', 'F'), ('F', 'K'), ('a', 'F'), ('M', 'N'), ('D', 'E'), ('H', 'I'), ('γ', 'δ')]:
        n = 0.0
        for _, w, ms, _ in x:
            for mv in ms:
                for i, u in enumerate(mv):
                    if u == a:
                        n += w * sum(1 for y in mv[i + 1:] if y == b)
        m = M[voc.index(a), voc.index(b)]
        bad += abs(n - m) > 1e-9
        say('  %s then %s: plain loops %.1f, matrix %.1f' % (a, b, n, m))
    tot, _ = I.precedence(x, rec['eligible'])
    idx = {t: i for i, t in enumerate(rec['eligible'])}
    for a, b in [('A', 'F'), ('η', 'θ')]:
        n = sum(w * sum(1 for i, u in enumerate(mv) if u == a for y in mv[i + 1:] if y == b) for _, w, ms, _ in x for mv in ms)
        bad += abs(n - tot[idx[a], idx[b]]) > 1e-9
        say('  precedence %s, %s: plain loops %.1f, matrix %.1f' % (a, b, n, tot[idx[a], idx[b]]))
    unknown = [t for t in rec['eligible'] if t not in CG.SEC]
    say('  eligible functions with no Propp section: %d' % len(unknown))
    # the function strings against the table
    rows = [r for r in DT.files('functions', ST.S.C.PATS['tale'], 'A') if DT.local(r['story']) == x[0][0]]
    say('  %s: units read %d, table rows %d, of them marked Y %d' % (x[0][0], sum(map(len, x[0][2])), len(rows), sum(1 for r in rows if r['matters'].upper().startswith('Y'))))
    say('U0: count mismatches %d' % bad)
    save('u0')


# ---------------------------------------------------------------- U5
def u5():
    say('# Audit-u5.txt -- the bars: every merging of Propp\'s ten sections into K consecutive groups, a perfect K-state answer')
    rec = record()
    toks = {'A': rec['A']['eligible'], 'B': rec['B']['eligible'], 'Propp': I.eligible(strings_of()['Propp'][0])}
    from sklearn.metrics import adjusted_rand_score
    for L in READ:
        say('## %s: %d eligible functions' % (L, len(toks[L])))
        for K in range(2, NSEC + 1):
            res = []
            for cuts in itertools.combinations(range(1, NSEC), K - 1):
                bounds = [0] + list(cuts) + [NSEC]
                grp = {s: g for g in range(K) for s in range(bounds[g], bounds[g + 1])}
                assign = {t: grp[CG.SEC[t]] for t in toks[L]}
                if len(set(assign.values())) < 2:
                    continue
                lab = [assign[t] for t in toks[L]]
                prop = [CG.SEC[t] for t in toks[L]]
                res.append((adjusted_rand_score(prop, lab), float(kendalltau(lab, prop)[0]), assign))
            best = max(res, key=lambda r: r[0])
            mean_a, mean_t = np.mean([r[0] for r in res]), np.mean([r[1] for r in res])
            v = I.s1(best[2], toks[L])
            say('K %2d, %3d mergings: best ARI %.3f (above %5.1f%%, tau %.3f; S1 %s); mean ARI %.3f, mean tau %.3f'
                % (K, len(res), v[0], 100 * v[1], v[2], 'holds' if I.s1_holds(v) else 'fails', mean_a, mean_t))
    save('u5')


# ---------------------------------------------------------------- U2
def pair_check(ind_by, chk_by, voc_by):
    """Q1 and Q3 with the any-distance count, as induce.py does it"""
    st = {L: I.pair_stats(ind_by[L], voc_by[L]) for L in ind_by}
    cands = I.candidates(st)
    sc = {L: I.pair_stats(chk_by[L], voc_by[L]) for L in chk_by}
    conf = [k for k in cands if all(k in sc[L] and sc[L][k][1] > 1 and sc[L][k][2] <= 0.05 for L in sc)]
    occur = [p for p in I.PROPP['functions'] if all(p in sc[L] and sc[L][p][0] >= 5 for L in sc)]
    found = [p for p in occur if p in conf]
    return cands, conf, occur, found


def chars(items):
    """one string per story: the first reading, functions as characters"""
    idx = {t: chr(0x100 + i) for i, t in enumerate(FUNCS)}
    out = {}
    for s, _, ms, _ in items:
        out.setdefault(s, ''.join(idx[u] for mv in ms for u in mv if u in idx))
    return out


def u2():
    say('# Audit-u2.txt -- Propp\'s own strings under the frozen tool, unchanged, on the same split')
    h = strings_of()
    ind, chk = h['Propp']
    say('stories %d + %d; moves %d; units %d' % (len(ind), len(chk), sum(len(x[2]) for x in ind + chk), sum(len(m) for x in ind + chk for m in x[2])))
    c = core(ind)
    say(line(c))
    say('H3 sections:')
    by = collections.defaultdict(list)
    for t, k in c['assign'].items():
        by[k].append(t)
    for k in range(c['K']):
        say('  S%d (place %.2f): %s' % (k + 1, c['places'][k], ' '.join(sorted(by[k], key=I.order_key))))
    say('H2: %s' % ', '.join('%d %.4f' % x for x in c['cv']))
    say('P2 order: %s' % ' '.join(I.copeland(c['toks'], c['rel'])))
    voc = c['voc'][:-2]
    cands, conf, occur, found = pair_check({'P': ind}, {'P': chk}, {'P': voc})
    say('Q1: candidates %d, confirmed %d' % (len(cands), len(conf)))
    recall = len(found) / len(occur) if occur else float('nan')
    say('Q3: Propp\'s pairs occurring at least 5 times %d (%s); confirmed %d (%s); recall %.2f; S3 %s'
        % (len(occur), ', '.join('%s %s' % p for p in occur), len(found), ', '.join('%s %s' % p for p in found), recall, 'holds' if recall >= .5 else 'fails'))
    say('ALL THREE: %s (reported beside the record; this replaces nothing)' % ('hold' if c['S1'] and c['S2'] and recall >= .5 else 'do not all hold'))
    say('')
    say('## The closeness of the strings: normalized edit distance by story, on all the stories')
    st = {L: chars(h[L][0] + h[L][1]) for L in READ}
    ids = sorted(set(st['A']) & set(st['B']) & set(st['Propp']))
    rnd = random.Random(SEED)

    def dist(a, b):
        return Levenshtein.distance(a, b) / max(len(a), len(b), 1)
    for x, y in (('A', 'B'), ('A', 'Propp'), ('B', 'Propp')):
        d = [dist(st[x][s], st[y][s]) for s in ids]
        other = []
        for s in ids:
            for t in rnd.sample([i for i in ids if i != s], 5):
                other.append(dist(st[x][s], st[y][t]))
        say('%s and %s: same story %.3f; another story %.3f' % (x, y, float(np.mean(d)), float(np.mean(other))))
    prep = {t for t, k in CG.SEC.items() if k == 0}
    for L in READ:
        items = h[L][0] + h[L][1]
        us = [u for x in items for mv in x[2] for u in mv]
        ws = {}
        for x in items:
            ws.setdefault(x[0], sum(map(len, x[2])))
        secs = collections.Counter(CG.SEC[u] for u in us)
        say('%s: units per story %.1f; moves per story %.2f; preparatory %.0f%%; sections %s' % (
            L, float(np.mean(list(ws.values()))), float(np.mean([len(x[2]) for x in items])),
            100 * sum(1 for u in us if u in prep) / len(us), ' '.join('%.0f' % (100 * secs[k] / len(us)) for k in range(NSEC))))
    save('u2')


# ---------------------------------------------------------------- U3
def counts(items):
    """function-level counts for the section chain: starts, transitions, ends, per (weighted) moves"""
    V = len(FUNCS)
    ix = {t: i for i, t in enumerate(FUNCS)}
    s, T, e, n = np.zeros(V), np.zeros((V, V)), np.zeros(V), np.zeros(V)
    moves = 0.0
    syms = 0.0
    for _, w, ms, _ in items:
        for mv in ms:
            xs = [ix[u] for u in mv if u in ix]
            if not xs:
                continue
            s[xs[0]] += w
            e[xs[-1]] += w
            for a, b in zip(xs, xs[1:]):
                T[a, b] += w
            for a in xs:
                n[a] += w
            moves += w
            syms += w * (len(xs) + 1)
    return s, T, e, n, syms


def chain_score(partition, train, test):
    """log-likelihood per symbol on test of the section chain with this partition (an array: function -> section)"""
    K = int(partition.max()) + 1
    O = np.eye(K)[partition]
    s, T, e, n, _ = train
    ss, TT, ee = O.T @ s, O.T @ T @ O, O.T @ e
    n_sec = O.T @ n
    start = (ss + I.SMOOTH) / (ss + I.SMOOTH).sum()
    row = np.concatenate([TT, ee[:, None]], 1) + I.SMOOTH
    row /= row.sum(1, keepdims=True)
    size = O.sum(0)
    em = (n + I.SMOOTH) / (n_sec[partition] + I.SMOOTH * size[partition])
    s2, T2, e2, n2, syms = test
    sec_t = O.T @ T2 @ O
    ll = (O.T @ s2) @ np.log(start) + (sec_t * np.log(row[:, :K])).sum() + (O.T @ e2) @ np.log(row[:, K]) + n2 @ np.log(em)
    return float(ll / syms)


def u3():
    say('# Audit-u3.txt -- do the strings fit Propp\'s sections? a chain over sections; log-likelihood per symbol on the checking half')
    h = strings_of()
    rec = record()
    true = np.array([CG.SEC[t] for t in FUNCS])
    for L in READ:
        ind, chk = h[L]
        tr, te = counts(ind), counts(chk)
        real = chain_score(true, tr, te)
        rng = np.random.default_rng(SEED)
        null = np.array([chain_score(rng.permutation(true), tr, te) for _ in range(10000)])
        below = float((null < real).mean())
        say('## %s' % L)
        say('true sections %.4f; random partitions mean %.4f, 95th %.4f, best %.4f; true above %.2f%% of them: %s'
            % (real, null.mean(), np.quantile(null, .95), null.max(), 100 * below, 'above the 95%% line' if below >= .95 else 'NOT above the 95% line'))
        voc = sorted({u for _, _, ms, _ in ind for mv in ms for u in mv}, key=I.order_key) + [I.UNK, I.END]
        lu, lb = I.baselines(I.encode(ind, voc), I.encode(chk, voc), voc)
        one = chain_score(np.zeros(len(FUNCS), int), tr, te)
        say('unigram %.4f; bigram %.4f; a one-section chain %.4f' % (lu, lb, one))
        if L in rec:
            r = rec[L]
            ll, n = I.loglik(I.model_of(r), I.encode(chk, r['vocab']))
            say('the record\'s HMM %.4f (K %d)' % (ll / n, r['K']))
    save('u3')


# ---------------------------------------------------------------- U4
def near_stats(items, voc, dists):
    """{(x, y): (count, lift, p)}: y stands d places after x in the same move, d in dists, against 1,000 within-move shuffles"""
    V = len(voc)
    X, mid, W = I.flat(items, voc)
    pos = []
    for d in dists:
        ok = np.flatnonzero(mid[:-d] == mid[d:])
        pos.append((ok, ok + d))
    i0 = np.concatenate([p[0] for p in pos])
    i1 = np.concatenate([p[1] for p in pos])

    def cnt(x):
        M = np.zeros(V * V)
        np.add.at(M, x[i0] * V + x[i1], W[i0])
        return M.reshape(V, V)
    obs = cnt(X)
    rng = np.random.default_rng(I.NG_SEED)
    tot, hit = np.zeros((V, V)), np.zeros((V, V))
    for _ in range(I.PERMS):
        m = cnt(X[np.lexsort((rng.random(len(X)), mid))])
        tot += m
        hit += m >= obs - 1e-9
    mean = tot / I.PERMS
    return {(a, b): (float(obs[i, j]), float(obs[i, j] / mean[i, j]) if mean[i, j] > 0 else float('inf'), float((hit[i, j] + 1) / (I.PERMS + 1)))
            for i, a in enumerate(voc) for j, b in enumerate(voc) if i != j and obs[i, j] > 0}


def pairs_by_class(h, group):
    """Q1 and Q3 per class, for a group of readers needing all of them"""
    voc = {L: sorted({u for x in h[L][0] for mv in x[2] for u in mv}, key=I.order_key) for L in group}
    for name, ds in (('adjacent', [1]), ('near', [2, 3, 4])):
        st = {L: near_stats(h[L][0], voc[L], ds) for L in group}
        keys = set.intersection(*[set(s) for s in st.values()])
        cands = [k for k in keys if all(s[k][0] >= 5 and s[k][1] >= 1.5 and s[k][2] <= 0.01 for s in st.values())]
        sc = {L: near_stats(h[L][1], voc[L], ds) for L in group}
        conf = {k for k in cands if all(k in sc[L] and sc[L][k][1] > 1 and sc[L][k][2] <= 0.05 for L in group)}
        yield name, st, sc, conf


def u4a(h):
    say('## a. Pairs: the n-gram study\'s classes, within the move')
    for group in (['A', 'B'], ['Propp']):
        res = list(pairs_by_class(h, group))
        all_conf = set().union(*[r[3] for r in res])
        occur = [p for p in I.PROPP['functions'] if any(all(p in r[2][L] and r[2][L][p][0] >= 5 for L in group) for r in res)]
        found = [p for p in occur if p in all_conf]
        say('%s: Propp\'s pairs occurring at least 5 times, adjacent or near, on the checking half: %d; confirmed %d (%s): recall %.2f; S3\'s bar of 0.5 %s'
            % ('+'.join(group), len(occur), len(found), ', '.join('%s %s' % p for p in found), len(found) / len(occur) if occur else float('nan'),
               'met' if occur and len(found) / len(occur) >= .5 else 'not met'))
        for name, _, _, conf in res:
            prs = [p for p in conf if p in I.PROPP['functions']]
            say('  %-9s confirmed %2d, of them Propp\'s %d (%s); others: %s' % (name, len(conf), len(prs), ', '.join('%s %s' % p for p in prs),
                ', '.join('%s %s' % p for p in sorted(conf - set(prs), key=lambda k: (I.order_key(k[0]), I.order_key(k[1]))))))


def mean_position(items, toks):
    ix = {t: i for i, t in enumerate(toks)}
    tot, w_ = np.zeros(len(toks)), np.zeros(len(toks))
    for _, w, ms, _ in items:
        for mv in ms:
            n = len(mv)
            for p, u in enumerate(mv):
                if u in ix:
                    tot[ix[u]] += w * (p / (n - 1) if n > 1 else 0.5)
                    w_[ix[u]] += w
    return tot / np.where(w_ > 0, w_, 1)


def u4b(h):
    say('## b. Order: S2\'s tau under other ways of reading the order')
    for L in READ:
        ind, chk = h[L]
        for name, items in (('induction half', ind), ('all stories', ind + chk)):
            toks = I.eligible(items)
            rel, info, _ = I.relations(items, toks)
            loose = [k for k, (share, both, _, _, p) in info.items() if share >= .6 and both >= 5 and p <= .1]
            t1, t2 = I.tau_propp(toks, rel), I.tau_propp(toks, loose)
            zeros = sum(1 for v in I.scores(toks, rel).values() if v == 0)
            mp = mean_position(items, toks)
            num = [TS.NUM[t] for t in toks]
            t3 = kendalltau(mp, num)
            rng = random.Random(SEED)
            null = []
            for _ in range(1000):
                sh = [(s, w, [rng.sample(m, len(m)) for m in ms], e) for s, w, ms, e in items]
                null.append(kendalltau(mean_position(sh, toks), num)[0])
            say('%-6s %-15s functions %2d: as frozen tau %+.3f (relations %3d, score 0: %2d); looser tau %+.3f (relations %3d); mean position tau %+.3f (p %.4f), shuffles 95th %+.3f'
                % (L, name, len(toks), t1[0], len(rel), zeros, t2[0], len(loose), t3[0], t3[1], float(np.quantile(null, .95))))


def _start_fw(args):
    seqs, K, M, st, forward = args
    rng = np.random.default_rng([SEED, K, st])
    X, lens, w = I.batch(seqs)
    pi = rng.dirichlet(np.ones(K))
    A = rng.dirichlet(np.ones(K), K)
    if forward:
        A = np.triu(A)
        A /= A.sum(1, keepdims=True)
    E = rng.dirichlet(np.ones(M), K)
    prev = -np.inf
    for _ in range(I.MAX_IT):
        ll, gamma, xi = I.forward_backward(pi, A, E, X, lens, w)
        tot = float((w * ll).sum())
        if tot - prev < I.TOL * abs(tot):
            break
        prev = tot
        pi, A, E = I.mstep(gamma, xi, X, lens, w, M)
    ll, _, _ = I.forward_backward(pi, A, E, X, lens, w, need_beta=False)
    return float((w * ll).sum()), pi, A, E


def fit_variant(items, K, forward, pool):
    toks = I.eligible(items)
    voc = sorted({u for _, _, ms, _ in items for mv in ms for u in mv}, key=I.order_key) + [I.UNK, I.END]
    seqs = I.encode(items, voc)
    best = None
    for r in pool.map(_start_fw, [(seqs, K, len(voc), st, forward) for st in range(I.STARTS)]):
        if best is None or r[0] > best[0] + 1e-9:
            best = r
    assign, _, _ = I.sections(best, seqs, voc)
    return I.s1(assign, toks), best, voc


def u4c(h, pool):
    say('## c. States: S1 under other model shapes, the induction half; log-likelihood per symbol on the checking half beside it')
    rec = record()
    for L in READ:
        ind, chk = h[L]
        Ks = [10]
        rk = rec[L]['K'] if L in rec else None
        for K, forward, name in ((10, False, 'K 10 free'), (10, True, 'K 10 forward-only')) + (((rk, True, 'K %d forward-only' % rk),) if rk else ()):
            v, m, voc = fit_variant(ind, K, forward, pool)
            ll, n = I.loglik(m, I.encode(chk, voc))
            say('%-6s %-20s ARI %+.3f (above %5.1f%%), state-section tau %+.3f: S1 %-5s; checking %.4f' % (L, name, v[0], 100 * v[1], v[2], 'holds' if I.s1_holds(v) else 'fails', ll / n))


def u4d(h):
    say('## d. Data: the tool on all 45 stories (S1 and S2 only); and with the preparatory units removed')
    prep = {t for t, k in CG.SEC.items() if k == 0}
    for L in READ:
        ind, chk = h[L]
        say('%-6s all stories:      %s' % (L, line(core(ind + chk))))
    for L in 'AB':
        ind, _ = h[L]
        x = [(s, w, [[u for u in mv if u not in prep] for mv in ms], e) for s, w, ms, e in ind]
        x = [(s, w, [m for m in ms if m], e) for s, w, ms, e in x if sum(map(len, ms)) >= 3]
        say('%-6s no preparatory:   %s' % (L, line(core(x))))


def u4():
    say('# Audit-u4.txt -- the tool\'s choices, one at a time. EXPLORATORY and many: a lone good figure means little; none of this is a pass')
    h = strings_of()
    u4a(h)
    save('u4')
    u4b(h)
    save('u4')
    pool = multiprocessing.Pool(min(4, os.cpu_count() or 1))
    u4c(h, pool)
    save('u4')
    u4d(h)
    save('u4')


# ---------------------------------------------------------------- U1
def chain_params(items):
    s, T, e, n, _ = counts(items)
    sec = np.array([CG.SEC[t] for t in FUNCS])
    O = np.eye(NSEC)[sec]
    ss, TT, ee, nn = O.T @ s, O.T @ T @ O, O.T @ e, O.T @ n
    row = np.concatenate([TT, ee[:, None]], 1)
    row = row / np.where(row.sum(1, keepdims=True) > 0, row.sum(1, keepdims=True), 1)
    row[row.sum(1) == 0, NSEC] = 1.0
    em = [np.array([n[i] for i in range(len(FUNCS)) if sec[i] == k]) for k in range(NSEC)]
    mem = [[FUNCS[i] for i in range(len(FUNCS)) if sec[i] == k] for k in range(NSEC)]
    return ss / ss.sum(), row, em, mem


def generate(items, m, rng):
    """as many stories times m, each with its model's number of moves, from the chain over the true sections"""
    start, row, em, mem = chain_params(items)
    out = []
    for c in range(m):
        for s, w, ms, _ in items:
            moves = []
            for _ in ms:
                k = rng.choice(NSEC, p=start)
                mv = []
                while len(mv) < 500:
                    if em[k].sum() > 0:
                        mv.append(mem[k][rng.choice(len(mem[k]), p=em[k] / em[k].sum())])
                    nx = rng.choice(NSEC + 1, p=row[k])
                    if nx == NSEC:
                        break
                    k = nx
                moves.append(mv)
            moves = [mv for mv in moves if mv]
            if sum(map(len, moves)) >= 3:
                out.append(('%s-%d' % (s, c), 1.0, moves, None))
    return out


def u1():
    say('# Audit-u1.txt -- the power of the test: strings generated from a chain over Propp\'s TRUE sections; the tool unchanged')
    say('#  the sections are true by construction, so a tool with power should satisfy S1 and S2 here')
    h = strings_of()
    plan = [('A', 1, 10), ('B', 1, 10), ('A', 2, 5), ('A', 4, 3)]
    for L, m, reps in plan:
        ind = h[L][0]
        rows = []
        for r in range(reps):
            rng = np.random.default_rng([SEED, ord(L), m, r])
            c = core(generate(ind, m, rng))
            rows.append(c)
            say('%s x%d #%2d: %s' % (L, m, r + 1, line(c)))
            save('u1')
        both = sum(1 for c in rows if c['S1'] and c['S2'])
        say('%s x%d: S1 holds %d of %d; S2 holds %d of %d; both %d of %d; mean K %.1f, ARI %.3f, state-section tau %.3f, order tau %.3f'
            % (L, m, sum(c['S1'] for c in rows), reps, sum(c['S2'] for c in rows), reps, both, reps, np.mean([c['K'] for c in rows]),
               np.mean([c['s1'][0] for c in rows]), np.mean([c['s1'][2] for c in rows]), np.nanmean([c['tau'][0] for c in rows])))
        save('u1')
    say('## order only, sixteen times the size')
    for L in 'AB':
        ind = h[L][0]
        ts = []
        for r in range(5):
            x = generate(ind, 16, np.random.default_rng([SEED, ord(L), 16, r]))
            toks = I.eligible(x)
            rel, _, _ = I.relations(x, toks)
            ts.append((I.tau_propp(toks, rel)[0], len(rel)))
        say('%s x16: order tau %s (relations %s)' % (L, ' '.join('%+.3f' % t[0] for t in ts), ' '.join(str(t[1]) for t in ts)))
    save('u1')


if __name__ == '__main__':
    fns = {'u0': u0, 'u1': u1, 'u2': u2, 'u3': u3, 'u4': u4, 'u5': u5}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in fns:
        sys.exit(__doc__)
    fns[a[0]]()
