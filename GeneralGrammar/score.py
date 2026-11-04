"""score.py -- scores a fitted grammar against a stated model. The only program here that knows Propp; grammar.py never imports it.

propp() reads his numbering and pairs from the project's tables of them. Everything else takes the truth as an argument.
"""
import os
import sys

import numpy as np
from scipy.stats import kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))


def propp():
    """(slots in his order, with A and a one slot; his pairs)"""
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Induction'))
    cwd = os.getcwd()
    import strings as ST
    os.chdir(cwd)
    NUM = ST.TS.NUM
    by = {}
    for k, v in NUM.items():
        by.setdefault(v, []).append(k)
    return [tuple(sorted(by[v])) for v in sorted(by)], list(ST.S.NG.PROPP_PAIRS)


def numbering(slots):
    return {u: i for i, alt in enumerate(slots) for u in alt}


def relation_tau(rel, num):
    """(concordant - discordant) / (concordant + discordant), over the relations between symbols of different slots"""
    c = d = 0
    for x, y in rel:
        if x in num and y in num and num[x] != num[y]:
            if num[x] < num[y]:
                c += 1
            else:
                d += 1
    return ((c - d) / (c + d) if c + d else float('nan')), c + d


def order_tau(order, num):
    seen, xs = set(), []
    for u in order:
        if u in num and u not in seen:
            seen.add(u)
            xs.append(u)
    if len(xs) < 3:
        return float('nan')
    return float(kendalltau(list(range(len(xs))), [num[u] for u in xs])[0])


def pair_recall(g, pairs, stories):
    """his pairs whose two symbols both stand in at least 5 stories: found among the links or joins"""
    from collections import Counter
    n = Counter()
    for s in stories:
        for u in set(s):
            n[u] += 1
    live = [p for p in pairs if n[p[0]] >= 5 and n[p[1]] >= 5]
    if not live:
        return float('nan'), 0, 0
    joins = {(o[1], o[2]) for o in g['ops'] if o[0] == 'join'}
    found = {tuple(x) for x in g['links']} | joins
    k = sum(1 for p in live if p in found)
    return k / len(live), k, len(live)


def boundary_f(pred, true):
    tp = fp = fn = 0
    for p, t in zip(pred, true):
        p, t = set(p), set(t)
        tp += len(p & t)
        fp += len(p - t)
        fn += len(t - p)
    if tp == 0:
        return 0.0
    pr, rc = tp / (tp + fp), tp / (tp + fn)
    return 2 * pr * rc / (pr + rc)


def breaks(mv, relset):
    for i in range(len(mv)):
        for j in range(i + 1, len(mv)):
            if (mv[j], mv[i]) in relset:
                return True
    return False


def acceptance(g, moves, rng, shuffles=20):
    """moves breaking no relation of the partial order, and the same of shuffled moves"""
    rel = {tuple(r) for r in g['relations']}
    real = sum(1 for m in moves if not breaks(m, rel))
    null = []
    for m in moves:
        null.append(np.mean([not breaks(list(rng.permutation(m)), rel) for _ in range(shuffles)]))
    return real, len(moves), float(np.mean(null)) if null else float('nan')
