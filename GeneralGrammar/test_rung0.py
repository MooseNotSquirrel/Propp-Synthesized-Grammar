"""test_rung0.py -- rung 0 of GeneralGrammarProtocol.md: the tool's honesty. Exits non-zero on any failure."""
import itertools
import json
import math
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grammar as G  # noqa: E402
import generators as X  # noqa: E402


def small(seed, m=25):
    rng = np.random.default_rng(seed)
    slots = [(s,) for s in X.names(12, 'q')]
    st, _ = X.g1(slots, [('q02', 'q03')], m, rng, 0)
    return [X.flat(s) for s in st]


def ok(name, cond, extra=''):
    print('%-5s %s %s' % ('PASS' if cond else 'FAIL', name, extra))
    if not cond:
        ok.bad += 1


ok.bad = 0


def source_check():
    src = open(os.path.join(HERE, 'grammar.py'), encoding='utf-8').read()
    imports = re.findall(r'^\s*(?:from|import)\s+([\w.]+)', src, re.M)
    ok('source: imports only the standard kit', set(imports) <= {'math', 'random', 'numpy', 'scipy.stats'}, str(sorted(set(imports))))
    for w in ('tragedyScore', 'constraintGrammar', 'storyGrammar', 'PROPP', 'SECTION', 'TS.NUM', "'up'", "'A'", 'β'):
        ok('source: no %s' % w, w not in src)


def objective_check():
    rng = random.Random(1)
    n = 7
    for trial in range(5):
        T = [[rng.randrange(0, 6) for _ in range(n)] for _ in range(n)]
        S = [rng.randrange(0, 4) for _ in range(n)]
        best = max(itertools.permutations(range(n)), key=lambda o: G.objective(list(o), T, S))
        got = G.search(T, S, random.Random(trial), 30)
        ok('search reaches the brute-force optimum, trial %d' % trial, abs(G.objective(got, T, S) - G.objective(list(best), T, S)) < 1e-9)
    # the running increments against the whole figure: a climb never lowers it
    o = list(range(n))
    v0 = G.objective(o, T, S)
    v1 = G.objective(G.climb(o, T, S, random.Random(2)), T, S)
    ok('a climb never lowers the objective', v1 >= v0 - 1e-9)
    # hand-worked: x->y once, y->x once, order x y: one forward, one back
    T = [[0, 1], [1, 0]]
    S = [1, 0]
    # back: y->x (count 1): -xl(1)=0; b=[0,1]; r=[1+1,0]=[2,0]; xl(1)+xl(2)-xl(2)=0
    ok('hand-worked objective', abs(G.objective([0, 1], T, S)) < 1e-12)


def probability_check():
    rng = random.Random(3)
    n = 6
    T = [[rng.randrange(0, 5) for _ in range(n)] for _ in range(n)]
    S = [rng.randrange(0, 4) for _ in range(n)]
    E = [rng.randrange(0, 4) for _ in range(n)]
    order = [3, 1, 0, 5, 2, 4]
    for name, m in (('slots', G.slot_model(T, S, E, order, 1.0, True)), ('slots with slips', G.slot_model(T, S, E, order, 1.0, True, 3)), ('one pass', G.slot_model(T, S, E, order, 1.0, False)), ('bigram', G.bigram_model(T, S, E, 1.0)), ('unigram', G.unigram_model(T, S, E))):
        ok('%s: rows and start sum to 1' % name, np.allclose(m[1].sum(1), 1) and abs(m[0].sum() - 1) < 1e-9)


def hmm_check():
    # the forward likelihood against enumeration of the state paths
    rng = np.random.default_rng(1)
    K, V = 3, 4
    pi = rng.dirichlet(np.ones(K))
    A = rng.dirichlet(np.ones(K), K)
    Em = rng.dirichlet(np.ones(V), K)
    x = np.array([0, 2, 1, 3, 3])
    tot = 0.0
    for path in itertools.product(range(K), repeat=len(x)):
        p = pi[path[0]] * Em[path[0], x[0]]
        for t in range(1, len(x)):
            p *= A[path[t - 1], path[t]] * Em[path[t], x[t]]
        tot += p
    got = G.hmm_score([x], (0, pi, A, Em))[0]
    ok('HMM forward agrees with enumeration', abs(got - math.log(tot)) < 1e-9)
    # EM does not lower the likelihood
    seqs = [rng.integers(0, V, 8) for _ in range(10)]
    a = G.HMM_ITERS
    G.HMM_ITERS = 2
    l2 = G.hmm_fit(seqs, 3, V, np.random.default_rng(5))[0]
    G.HMM_ITERS = 20
    l20 = G.hmm_fit(seqs, 3, V, np.random.default_rng(5))[0]
    G.HMM_ITERS = a
    ok('HMM training raises the likelihood', l20 >= l2 - 1e-6, '%.3f %.3f' % (l2, l20))


def ops_check():
    u, ch = G.apply_ops(['a', 'b', 'c', 'a', 'b'], [('join', 'a', 'b', 'a+b')])
    ok('a join parses', u == ['a+b', 'c', 'a+b'] and ch == [])
    u, ch = G.apply_ops(['a', 'b', 'c'], [('merge', 'a', 'c', 'a|c')])
    ok('a merge parses', u == ['a|c', 'b', 'a|c'] and ch == [('a|c', 'a'), ('a|c', 'c')])
    ok('expansion', G.expand('a+b', [('join', 'a', 'b', 'a+b')]) == ['a', 'b'])
    ok('spans: a join adds, a merge does not', G.spans_of(['a', 'b', 'c', 'd'], [('join', 'a', 'b', 'a+b'), ('merge', 'c', 'd', 'c|d')]) == [2, 1, 1])


def planted_check():
    # a strict order with restarts must be found, and the order read off must be it
    st = small(11, 40)
    g = G.fit(st, boots=30, starts=20)
    names = X.names(12, 'q')
    from scipy.stats import kendalltau
    num = {u: i for i, u in enumerate(names)}
    xs = [u for u in g['order'] if u in num]
    ok('planted order retrieved', kendalltau(range(len(xs)), [num[u] for u in xs])[0] > 0.85, 'shape %s coverage %.2f' % (g['shape'], g['coverage']))
    return st


def rename_check(st):
    g1 = G.fit(st, boots=20, starts=10)
    # a renaming that reverses any alphabetical order the program might lean on
    syms = sorted({u for s in st for u in s})
    mp = dict(zip(syms, ['zz%03d' % (999 - i) for i in range(len(syms))]))
    g2 = G.fit([[mp[u] for u in s] for s in st], boots=20, starts=10)
    def back(obj):
        t = json.dumps(obj, sort_keys=True)
        return t
    inv = {v: k for k, v in mp.items()}
    def tr(g):
        return {'order': [inv.get(u, u) for u in g['order']], 'shape': g['shape'], 'coverage': round(g['coverage'], 9), 'cuts': g['cuts'],
                'rel': sorted([inv.get(a, a), inv.get(b, b)] for a, b in g['relations']), 'links': sorted([inv.get(a, a), inv.get(b, b)] for a, b in g['links']), 'cv': {k: round(v, 6) for k, v in g['cv'].items()}}
    a = {'order': g1['order'], 'shape': g1['shape'], 'coverage': round(g1['coverage'], 9), 'cuts': g1['cuts'],
         'rel': sorted(list(r) for r in g1['relations']), 'links': sorted(list(r) for r in g1['links']), 'cv': {k: round(v, 6) for k, v in g1['cv'].items()}}
    ok('renamed symbols give the identical grammar', back(a) == back(tr(g2)))


def byte_check(st):
    a = json.dumps(G.fit(st, boots=20, starts=10), sort_keys=True)
    b = json.dumps(G.fit(st, boots=20, starts=10), sort_keys=True)
    ok('two runs byte-identical', a == b)


if __name__ == '__main__':
    source_check()
    objective_check()
    probability_check()
    hmm_check()
    ops_check()
    st = planted_check()
    rename_check(st)
    byte_check(st)
    print('rung 0: %s' % ('all pass' if ok.bad == 0 else '%d FAILED' % ok.bad))
    sys.exit(1 if ok.bad else 0)
