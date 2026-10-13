#!/usr/bin/env python3
"""
baseline.py -- exploratory, before the significance layer is designed: how far
can the layers already transcribed (acts, relations, the judged hero's part)
recover Propp's functions when the mapping is learned rather than written by
hand? Not a frozen test; it reads data already scored (TwoLayer, Heroes).

  python baseline.py     writes Significance/BaselineExplore.txt

The learned mapping: for each feature cell (for example, act and the hero's
part), over the training stories, the share of events holding an entry with
that cell whose original transcription has function f; f is predicted for a
cell whose share is at least one third, from at least 3 events (adding a
prediction raises the agreement figure J when its chance of being right
exceeds J/(1+J), one third at the target J of one half); a rarer cell
backs off to the act and the hero's part, then to the act alone. Two folds by
story, alternating within each genre in sorted order; each fold is trained on
the other; the agreement figure pools both folds. Each transcriber's acts are
trained on and tested against that transcriber's original functions.
"""
import collections
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Heroes'))
sys.path.insert(0, os.path.join(ROOT, 'TwoLayer'))
import withJudgedHeroes as W  # noqa: E402
import twoLayer as T  # noqa: E402

ORIG = {'tale': 'Afanasyev/transcriptions/U/%s/b*/Notes.txt', 'fable': 'Fables/transcriptions/%s/b*/Notes.txt',
        'tragedy': 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'}
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def part(hw, perf, und):
    d, u = W.is_hero(hw, perf), W.is_hero(hw, und)
    return 'both' if d and u else 'does' if d else 'undergoes' if u else 'neither'


def features(J, raw, events):
    """{event: [dict of features per entry]}, with each entry's position against the story's first harm or want."""
    first = {}
    for (s, ev) in sorted(raw):
        if any(a in ('harm', 'want') for a, _, _, _ in raw[(s, ev)]) and s not in first:
            first[s] = ev
    out = {}
    for e in events:
        s, ev = e
        out[e] = [{'act': a, 'part': part(J[s], pf, u), 'rel': r,
                   'pos': 'before' if ev < first.get(s, 10 ** 6) else 'at' if ev == first.get(s) else 'after'}
                  for a, pf, u, r in raw.get(e, [])]
    return out


def learn(F, target, train, keys):
    cells = [tuple(keys), ('act', 'part'), ('act',)]
    stats = {c: collections.defaultdict(lambda: [0, collections.Counter()]) for c in cells}
    for e in train:
        for c in cells:
            seen = {tuple(x[k] for k in c) for x in F[e]}
            for v in seen:
                st = stats[c][v]
                st[0] += 1
                st[1].update(target.get(e, set()))

    def predict(x):
        for c in cells:
            st = stats[c].get(tuple(x[k] for k in c))
            if st and st[0] >= 3:
                return {f for f, k in st[1].items() if k / float(st[0]) >= 1 / 3.0}
        return set()
    return predict


def run(J, F, target, events, keys, gen):
    stories = sorted({e[0] for e in events})
    fold = {}
    for g in T.GENRES:
        for i, s in enumerate(x for x in stories if gen[x] == g):
            fold[s] = i % 2
    both = either = 0
    for k in (0, 1):
        train = [e for e in events if fold[e[0]] != k]
        test = [e for e in events if fold[e[0]] == k]
        pr = learn(F, target, train, keys)
        for e in test:
            p = set().union(*[pr(x) for x in F[e]]) if F[e] else set()
            t = target.get(e, set())
            both += len(p & t)
            either += len(p | t)
    return both / float(either) if either else 0.0


if __name__ == '__main__':
    J = W.judged()
    M = T.material()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    raw, funcs = {}, {}
    for L in 'AB':
        raw[L] = T.read_acts(sorted(glob.glob(os.path.join(T.OUT, '*', 'acts', L, '*', 'Notes.txt'))))
        o = {}
        for g in T.GENRES:
            o.update({e: v for e, v in T.read_functions(glob.glob(os.path.join(P, ORIG[g] % L))).items() if e[0] in gen})
        funcs[L] = o
    events = sorted(e for e in set(funcs['A']) & set(funcs['B']) & set(raw['A']) & set(raw['B']) if e[0] in J)
    say('# BaselineExplore.txt -- baseline.py, exploratory; a learned mapping from the layers already transcribed to Propp\'s functions.')
    say('Events: %d, in %d stories with a judged hero' % (len(events), len({e[0] for e in events})))
    say('')
    variants = [('act alone', ['act']), ('act + hero\'s part', ['act', 'part']), ('act + hero\'s part + relation', ['act', 'part', 'rel']),
                ('act + hero\'s part + position against the first harm or want', ['act', 'part', 'pos']),
                ('act + hero\'s part + relation + position', ['act', 'part', 'rel', 'pos'])]
    for g in list(T.GENRES) + ['all']:
        E = [e for e in events if g == 'all' or gen[e[0]] == g]
        say('%s: %d events; original A against B %.3f' % (g, len(E), T.jaccard(funcs['A'], funcs['B'], E)))
        for name, keys in variants:
            r = []
            for L in 'AB':
                F = features(J, raw[L], E)
                r.append(run(J, F, funcs[L], E, keys, gen))
            say('  %-62s A %.3f  B %.3f  mean %.3f' % (name, r[0], r[1], sum(r) / 2))
    open(os.path.join(HERE, 'BaselineExplore.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')
