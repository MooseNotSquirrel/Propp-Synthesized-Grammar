#!/usr/bin/env python3
"""
animal.py -- the frozen models' predictions for Afanasyev's animal tales (AnimalProtocol.md).

  python animal.py count      the animal transcriptions read, and nothing measured
  python animal.py score      writes Animal/AnimalRun.txt
  python animal.py selftest   the whole scorer with held-out wondertales, then held-out fables, standing in for the animal tales

Written in full before any animal tale was transcribed.
"""
import collections
import glob
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
for d in ('Model', 'Links', 'Spheres'):
    sys.path.insert(0, os.path.join(ROOT, d))
import model as M  # noqa: E402
import links as K  # noqa: E402
import explore as SX  # noqa: E402

TS = M.TS
ANIMAL = 'AnimalTales/transcriptions/%s/b*/Notes.txt'
SF = 4  # the function stands in the fifth field, as in the calibration's transcriptions
TIGHT = [('H -> I', ('H',), 'I'), ('M -> N', ('M',), 'N'), ('Pr -> Rs', ('Pr',), 'Rs'), ('L -> Ex', ('L',), 'Ex')]
FRAME = ('A or a -> K', ('A|a',), 'K')
HERO, VILLAIN = {'C', '↑', 'E', 'W'}, {'A', 'Pr'}  # the strict reading: struggle left out of the villain's sphere
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


# ---------------------------------------------------------------- reading
def read_animal(L):
    """{story: [(move, function or 'X', negative, performer key, undergoer key)]}, each story's first reading"""
    st = collections.OrderedDict()
    for r in M.DT.files('functions', [ANIMAL], L):     # from the normalized tables (Data/tables.py)
        base = M.DT.local(r['story'])
        if not re.match(r'^A\d{3}', base):
            continue
        st.setdefault(base, collections.OrderedDict()).setdefault(r['version'] or '1', []).append(
            (r['move'], TS.base(r['raw']) or 'X', TS.negative(r['raw']), SX.key(r['performer']), SX.key(r['undergoer'])))
    return {s: vs[sorted(vs, key=lambda v: (len(v), v))[0]] for s, vs in st.items()}


def moves_of(stories):
    """[list of base functions, one list a move], X, α and blanks left out, as Links/ reads a corpus"""
    out = []
    for s, es in stories.items():
        mv = collections.OrderedDict()
        for e in es:
            mv.setdefault(e[0], [])
            if e[1] not in ('X', 'α', ''):
                mv[e[0]].append(e[1])
        out += [m for m in mv.values() if m]
    return out


# ---------------------------------------------------------------- the measures
def place(fit_rows, new_rows, groups=None, length=False):
    """the genre the model fitted on fit_rows gives each new story: Counter of genres"""
    groups = M.GROUP_SETS['all'] if groups is None else groups
    if not groups:
        Xf, Xn = np.array([[np.log(r[3])] for r in fit_rows]), np.array([[np.log(r[3])] for r in new_rows])
        p, _, _ = M.fit_predict(Xf, M.matrix(fit_rows, ['order'])[1], Xn)
        return collections.Counter(M.GENRES[k] for k in p)
    Xf, yf = M.matrix(fit_rows, groups)
    Xn = np.array([sum((f[k] for k in groups), []) for _, _, f, _ in new_rows], float)
    if length:
        Xf = np.hstack([Xf, [[np.log(r[3])] for r in fit_rows]])
        Xn = np.hstack([Xn, [[np.log(r[3])] for r in new_rows]])
    p, _, _ = M.fit_predict(Xf, yf, Xn)
    return collections.Counter(M.GENRES[k] for k in p)


def fused(stories):
    """share of stories in which one character holds both the hero's and the villain's sphere (strict reading)"""
    flags = []
    for s, es in stories.items():
        canon = SX.merge([(fn, p, u) for fn, p, u in es])
        sph = collections.defaultdict(set)
        for fn, p, _ in es:
            if p:
                p = canon.get(p, p)
                if fn in HERO:
                    sph[p].add('hero')
                if fn in VILLAIN:
                    sph[p].add('villain')
        flags.append(any(v == {'hero', 'villain'} for v in sph.values()))
    n, hit = len(flags), sum(flags)
    return hit / float(n) if n else float('nan'), hit, n, flags


def above(a, b, shuffles=K.SHUFFLES, seed=K.SEED):
    """one-sided permutation p that stories a hold the property more often than stories b, labels shuffled"""
    x = np.array(a + b, dtype=float)
    obs = x[:len(a)].mean() - x[len(a):].mean()
    rng = np.random.default_rng(seed)
    null = np.empty(shuffles)
    for k in range(shuffles):
        y = rng.permutation(x)
        null[k] = y[:len(a)].mean() - y[len(a):].mean()
    return (np.sum(null >= obs - 1e-12) + 1) / (shuffles + 1.0)


# ---------------------------------------------------------------- the test
def run(new, ref_rows, ref_moves, ref_spheres, shuffles=K.SHUFFLES, label='animal'):
    """new: {L: {story: entries as read_animal gives}}; ref_rows: {L: model rows to fit on};
    ref_moves: {L: {'tale': moves, 'fable': moves}}; ref_spheres: {L: {'tale': stories, 'fable': stories}}.
    Returns the four verdicts."""
    v = {}
    say('1. WHERE THE FROZEN MODEL PLACES THEM')
    ok1 = True
    for L in 'AB':
        rows = []
        for s, es in new[L].items():
            f, n = M.features([(m, b, neg) for m, b, neg, _, _ in es])
            if n >= M.MIN_FUNCTIONS:
                rows.append(('?', s, f, n))
        c = place(ref_rows[L], rows)
        lead = c['fable'] > max(c[g] for g in M.GENRES if g != 'fable')
        ok1 &= lead
        say('  %s: %d of %d %s stories of at least %d functions placed: %s; fable ahead of every other genre: %s'
            % (L, len(rows), len(new[L]), label, M.MIN_FUNCTIONS, ', '.join('%s %d' % (g, c[g]) for g in M.GENRES), 'yes' if lead else 'no'))
        for name, kw in (('with length added', dict(length=True)), ('length alone', dict(groups=[], length=True)),
                         ('lexicon alone', dict(groups=['lexicon'])), ('relations alone', dict(groups=['relations']))):
            c2 = place(ref_rows[L], rows, **kw)
            say('     reported: %-18s %s' % (name, ', '.join('%s %d' % (g, c2[g]) for g in M.GENRES)))
    v[1] = ok1
    say('')
    say('2. WHETHER ONE CHARACTER HOLDS BOTH THE HERO\'S AND THE VILLAIN\'S SPHERE (strict reading: villainy and pursuit)')
    ok2 = True
    for L in 'AB':
        a = fused({s: [(b, p, u) for _, b, _, p, u in es] for s, es in new[L].items()})
        t = fused(ref_spheres[L]['tale'])
        fb = fused(ref_spheres[L]['fable'])
        pv = above(a[3], t[3], shuffles=shuffles)
        ok = a[0] > t[0] and pv <= 0.05
        ok2 &= ok
        say('  %s: %s %d of %d (%.0f%%); wondertales %d of %d (%.0f%%); fables %d of %d (%.0f%%); above the wondertales, one-sided p %.4f: %s'
            % (L, label, a[1], a[2], 100 * a[0], t[1], t[2], 100 * t[0], fb[1], fb[2], 100 * fb[0], pv, 'yes' if ok else 'no'))
    v[2] = ok2
    say('')
    say('3. WHETHER THEIR TROUBLE IS PUT RIGHT: villainy or lack followed by liquidation, share of moves')
    ok3 = True
    name, firsts, second = FRAME
    for L in 'AB':
        a = K.Moves(moves_of(new[L])).test(firsts, second, shuffles=shuffles)
        t = K.Moves(ref_moves[L]['tale']).test(firsts, second, shuffles=shuffles)
        fb = K.Moves(ref_moves[L]['fable']).test(firsts, second, shuffles=shuffles)
        mid = (t['share'] + fb['share']) / 2
        ok = a['share'] < mid
        ok3 &= ok
        say('  %s %-8s %s' % (L, label, K.fmt(a)))
        say('  %s %-8s %s' % (L, 'tale', K.fmt(t)))
        say('  %s %-8s %s' % (L, 'fable', K.fmt(fb)))
        say('  %s: %.0f%% against the midpoint %.0f%% of the tale\'s %.0f%% and the fable\'s %.0f%%: below it: %s'
            % (L, 100 * a['share'], 100 * mid, 100 * t['share'], 100 * fb['share'], 'yes' if ok else 'no'))
    v[3] = ok3
    say('')
    say('4. WHETHER THE TIGHT PAIRS HOLD')
    res = {}
    for name, firsts, second in TIGHT:
        for L in 'AB':
            r = K.Moves(moves_of(new[L])).test(firsts, second, shuffles=shuffles)
            res[name, L] = r
            say('  %-9s %s  %s%s' % (name, L, K.fmt(r), '  HOLDS' if K.holds(r) else ''))
    testable = [n for n, _, _ in TIGHT if all(res[n, L]['with first'] >= K.MIN_MOVES for L in 'AB')]
    held = [n for n in testable if all(K.holds(res[n, L]) for L in 'AB')]
    if len(testable) < 2:
        v[4] = None
        say('  testable for both transcribers: %s; fewer than two: NOT TESTED' % (', '.join(testable) or 'none'))
    else:
        v[4] = len(held) >= len(testable) - 1
        say('  testable for both transcribers: %s; holding for both: %s' % (', '.join(testable), ', '.join(held) or 'none'))
    say('')
    word = {True: 'HOLDS', False: 'FAILS', None: 'NOT TESTED'}
    say('PREDICTIONS (AnimalProtocol.md)')
    say('  1. the frozen model places more of them as fable than as any other genre, for both transcribers: %s' % word[v[1]])
    say('  2. one character holds both the hero\'s and the villain\'s sphere in a larger share of them than of the wondertales, one-sided p at most 0.05, for both transcribers: %s' % word[v[2]])
    say('  3. villainy or lack is followed by liquidation in a share of their moves below the midpoint of the tale\'s and the fable\'s, for both transcribers: %s' % word[v[3]])
    say('  4. of the tight links whose first function stands in at least 5 of their moves for both transcribers, all but at most one hold for both: %s' % word[v[4]])
    return v


def references():
    rows = {L: M.table(M.stories(L)) for L in 'AB'}
    T = K.transcribed()
    moves = {L: {g: T[L][g] for g in ('tale', 'fable')} for L in 'AB'}
    sp = {}
    for L in 'AB':
        d = SX.read(L)
        sp[L] = {g: {s: [(fn, p, u) for fn, p, u in es] for s, es in d[g].items()} for g in ('tale', 'fable')}
    return rows, moves, sp


def count():
    for L in 'AB':
        st = read_animal(L)
        n = sum(len(es) for es in st.values())
        print('%s: %d stories, %d entries, %d moves; nothing measured' % (L, len(st), n, len(moves_of(st))))


def score():
    new = {L: read_animal(L) for L in 'AB'}
    if not all(new.values()):
        sys.exit('no animal transcriptions under %s' % (ANIMAL % '?'))
    say('# AnimalRun.txt -- animal.py score, as AnimalProtocol.md freezes it.')
    say('')
    rows, moves, sp = references()
    for L in 'AB':
        say('%s: animal tales %d; the model fitted on all stories of at least %d functions: %s'
            % (L, len(new[L]), M.MIN_FUNCTIONS, ', '.join('%s %d' % (g, sum(1 for r in rows[L] if r[0] == g)) for g in M.GENRES)))
    say('')
    run(new, rows, moves, sp, label='animal')
    open(os.path.join(HERE, 'AnimalRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


def selftest():
    """Held-out stories of a known genre stand in for the animal tales: the model is fitted only on the other half,
    and the stand-ins are removed from the reference corpora they came from. With wondertales standing in,
    predictions 1, 2 and 3 should fail (the stand-ins are wondertales); with fables standing in, 1 and 3 should hold."""
    rows, moves, sp = references()
    allrows = {L: M.table(M.stories(L)) for L in 'AB'}
    for g in ('tale', 'fable'):
        say('=== SELF-TEST: held-out %ss standing in for the animal tales (1,000 shuffles a link)' % g)
        new, fit, mv, sph = {}, {}, {}, {}
        for L in 'AB':
            spl = M.split(allrows[L])
            test_ids = {r[1] for r in allrows[L] if r[0] == g and spl[r[1]] == 'test'}
            fit[L] = [r for r in allrows[L] if spl[r[1]] == 'fit']
            S = M.stories(L)[g]
            d = SX.read(L)[g]
            new[L] = {s: [(m, b, neg, p, u) for (m, b, neg), (_, p, u) in zip(S[s], d[s])] for s in test_ids if s in S and s in d}
            rest = {s: es for s, es in S.items() if s not in test_ids}
            mv[L] = dict(moves[L])
            mv[L][g] = moves_of({s: [(m, b, neg, None, None) for m, b, neg in es] for s, es in rest.items()})
            sph[L] = dict(sp[L])
            sph[L][g] = {s: es for s, es in sp[L][g].items() if s not in test_ids}
        run(new, fit, mv, sph, shuffles=1000, label=g)
        say('')


if __name__ == '__main__':
    cmds = {'count': count, 'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
