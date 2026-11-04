"""generators.py -- the generated grammars of rung 1 (GeneralGrammarProtocol.md). No reader data and no real strings.

Each returns (stories, truth). A story is a list of passes; a pass a list of symbols. The grammars' rates are stipulated
here, not read from any corpus. Propp's order and pairs are handed in by the caller (score.py holds them), never to grammar.py.
"""
import numpy as np

CONT, P_INCL, P_PAIR, P_SWAP = 0.45, 0.30, 0.80, 0.10


def n_passes(rng):
    n = 1
    while rng.random() < CONT and n < 6:
        n += 1
    return n


def swap_noise(mv, rng):
    mv = list(mv)
    for i in range(len(mv) - 1):
        if rng.random() < P_SWAP:
            mv[i], mv[i + 1] = mv[i + 1], mv[i]
    return mv


def ordered_pass(slots, pairs, rng, opener=None):
    """slots: list of alternatives-tuples in order; pairs: {x: y}, if x stands then y does at 0.8"""
    on = {}
    for k, alt in enumerate(slots):
        if rng.random() < P_INCL:
            on[k] = alt[rng.integers(len(alt))]
    if opener is not None:
        on[opener] = slots[opener][rng.integers(len(slots[opener]))]
    where = {u: k for k, alt in enumerate(slots) for u in alt}
    for x, y in pairs.items():
        if x in on.values() and y in where and rng.random() < P_PAIR:
            on[where[y]] = y
    return [on[k] for k in sorted(on)]


def g1(propp_slots, propp_pairs, m, rng, opener):
    """Propp's stated order: functions optional, passes, his pairs (A and a one slot, one opening each pass)"""
    pairs = {x: y for x, y in propp_pairs}
    stories = []
    for _ in range(m):
        stories.append([swap_noise(ordered_pass(propp_slots, pairs, rng, opener), rng) for _ in range(n_passes(rng))])
    return stories, {'slots': propp_slots, 'pairs': propp_pairs}


def g8(propp_slots, propp_pairs, m, rng, opener):
    """added at version 2, as v1's G1 proved too easy: unequal rates, some functions rare (Beta(1, 3) a corpus), more slips (0.25),
    about 17 units a story. Rates stipulated, the length taken from the audit's figure for his strings."""
    pairs = {x: y for x, y in propp_pairs}
    where = {u: k for k, alt in enumerate(propp_slots) for u in alt}
    rates = rng.beta(1, 3, len(propp_slots))
    stories = []
    for _ in range(m):
        s = []
        for _ in range(n_passes(rng)):
            on = {}
            for k, alt in enumerate(propp_slots):
                if rng.random() < rates[k]:
                    on[k] = alt[rng.integers(len(alt))]
            on[opener] = propp_slots[opener][rng.integers(len(propp_slots[opener]))]
            for x, y in pairs.items():
                if x in on.values() and y in where and rng.random() < P_PAIR:
                    on[where[y]] = y
            mv = [on[k] for k in sorted(on)]
            for i in range(len(mv) - 1):
                if rng.random() < 0.25:
                    mv[i], mv[i + 1] = mv[i + 1], mv[i]
            s.append(mv)
        stories.append(s)
    return stories, {'slots': propp_slots, 'pairs': propp_pairs}


def relabel(stories, truth, rng):
    syms = sorted({u for alt in truth['slots'] for u in alt})
    perm = list(rng.permutation(syms))
    mp = dict(zip(syms, perm))
    st = [[[mp[u] for u in p] for p in s] for s in stories]
    return st, {'slots': [tuple(mp[u] for u in alt) for alt in truth['slots']], 'pairs': [(mp[x], mp[y]) for x, y in truth['pairs']], 'map': mp}


def names(n, p='s'):
    return ['%s%02d' % (p, i) for i in range(n)]


def g3(m, rng):
    """two exclusive branches: a common head, one branch or the other, a common tail"""
    a = names(22)
    head, x, y, tail = a[:6], a[6:11], a[11:16], a[16:]
    stories = []
    for _ in range(m):
        s = []
        for _ in range(n_passes(rng)):
            br = x if rng.random() < 0.5 else y
            mv = [u for u in head + br + tail if rng.random() < 0.55]
            if mv:
                s.append(swap_noise(mv, rng))
        stories.append(s)
    return stories, {'x': x, 'y': y}


def g4(m, rng):
    """episodes repeated in any order, each with its own inner order; no overall order"""
    a = names(30)
    eps = [a[i:i + 5] for i in range(0, 30, 5)]
    stories = []
    for _ in range(m):
        s = []
        for _ in range(int(rng.integers(3, 6))):
            mv = [u for u in eps[rng.integers(6)] if rng.random() < 0.8]
            if mv:
                s.append(mv)
        stories.append(s)
    return stories, {'episodes': eps}


def g5(m, rng):
    """local links only: each symbol has three successors anywhere in the alphabet"""
    a = names(30)
    succ = [rng.choice(30, 3, replace=False) for _ in range(30)]
    wt = [rng.dirichlet(np.ones(3) * 2) for _ in range(30)]
    stories = []
    for _ in range(m):
        k = int(rng.integers(30))
        mv = []
        for _ in range(60):
            mv.append(a[k])
            if rng.random() < 0.06:
                break
            k = int(succ[k][rng.choice(3, p=wt[k])])
        stories.append([mv])
    return stories, {}


def g6(m, rng):
    """hidden phases, wandering with no order, each with five interchangeable symbols"""
    a = names(30)
    ph = [a[i:i + 5] for i in range(0, 30, 5)]
    A = rng.dirichlet(np.ones(6) * 0.5, 6)
    stories = []
    for _ in range(m):
        k = int(rng.integers(6))
        mv = []
        for _ in range(60):
            mv.append(ph[k][rng.integers(5)])
            if rng.random() < 0.06:
                break
            if rng.random() > 0.5:
                k = int(rng.choice(6, p=A[k]))
        stories.append([mv])
    return stories, {}


def g7(m, rng):
    """no order at all: symbols drawn at random, with unequal shares"""
    a = names(30)
    w = rng.dirichlet(np.ones(30) * 2)
    stories = []
    for _ in range(m):
        n = 3 + int(rng.poisson(14))
        stories.append([[a[i] for i in rng.choice(30, n, p=w)]])
    return stories, {}


def flat(story):
    return [u for p in story for u in p]


def cuts_of(story):
    out, pos = [], 0
    for p in story[:-1]:
        pos += len(p)
        out.append(pos)
    return out
