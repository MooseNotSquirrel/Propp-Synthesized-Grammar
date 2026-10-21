#!/usr/bin/env python3
"""
lengthCheck.py -- the length-matched placement test (LengthProtocol.md): does transcriber A's
placement of the animal tales as tale follow from A marking more functions than B?

  python lengthCheck.py selftest   the plumbing, and whether thinning alone moves held-out wondertales to fable
  python lengthCheck.py score      writes Animal/LengthRun.txt

THE ARMS, both on A's animal tales, placed by the frozen joint model fitted on all of A's four genres
(animal.py's place, unchanged):
  thinned   each tale with more of Propp's functions than B's transcription of it is thinned to B's count,
            function entries removed at random (X entries and order kept), 100 draws, seed 46
  shared    each tale keeps only the entries on events where B also wrote one of Propp's functions
Reported, not judged: B's tales on the events A also marked; the unthinned placement.
"""
import collections
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import animal as AN  # noqa: E402

M, TS = AN.M, AN.TS
DRAWS, SEED = 100, 46
PLURAL = {'tale': 'wondertales', 'tragedy': 'tragedies', 'myth': 'myths'}
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def read(L):
    """{story: [(move, function or 'X', negative, event)]}, each story's first reading, as animal.py reads it"""
    st = collections.OrderedDict()
    for path in sorted(AN.glob.glob(os.path.join(AN.P, AN.ANIMAL % L))):
        for line in open(path, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^A\d{3}', f[0]):
                continue
            base, _, ver = f[0].partition('/')
            ev = re.search(r'\d+', f[3])
            st.setdefault(base, collections.OrderedDict()).setdefault(ver or '1', []).append(
                (f[1], TS.base(f[AN.SF]) or 'X', TS.negative(f[AN.SF]), int(ev.group()) if ev else None))
    return {s: vs[sorted(vs, key=lambda v: (len(v), v))[0]] for s, vs in st.items()}


def is_fn(e):
    return e[1] in M.RANK


def rows_of(stories):
    out = []
    for s, es in stories.items():
        f, n = M.features([(m, b, neg) for m, b, neg, _ in es])
        if n >= M.MIN_FUNCTIONS:
            out.append(('?', s, f, n))
    return out


def thin(es, k, rnd):
    """es with function entries removed at random until k remain"""
    idx = [i for i, e in enumerate(es) if is_fn(e)]
    if len(idx) <= k:
        return list(es)
    drop = set(rnd.sample(idx, len(idx) - k))
    return [e for i, e in enumerate(es) if i not in drop]


def counts(stories):
    return {s: sum(1 for e in es if is_fn(e)) for s, es in stories.items()}


def lead(c):
    return c['fable'] > max(c[g] for g in M.GENRES if g != 'fable')


def fmt(c):
    return ', '.join('%s %d' % (g, c[g]) for g in M.GENRES)


def thinned_arm(fit, stories, target, label):
    rnd = random.Random(SEED)
    leads, tot = 0, collections.Counter()
    for _ in range(DRAWS):
        new = {s: thin(es, target.get(s, len(es)), rnd) for s, es in stories.items()}
        c = AN.place(fit, rows_of(new))
        leads += lead(c)
        tot.update(c)
    say('  %s: fable ahead of every other genre in %d of %d draws; placements summed over the draws: %s'
        % (label, leads, DRAWS, fmt(tot)))
    return leads


def score():
    say('# LengthRun.txt -- lengthCheck.py score, as LengthProtocol.md freezes it.')
    say()
    A, B = read('A'), read('B')
    fit = M.table(M.stories('A'))
    nA, nB = counts(A), counts(B)
    say('A marks more functions than B in %d of 50 tales; functions, A %d, B %d'
        % (sum(nA[s] > nB.get(s, 0) for s in A), sum(nA.values()), sum(nB.values())))
    say('  unthinned (the frozen score): %s' % fmt(AN.place(fit, rows_of(A))))
    say()
    k1 = thinned_arm(fit, A, nB, 'T1 thinned to B\'s count')
    evB = {s: {e[3] for e in es if is_fn(e)} for s, es in B.items()}
    shared = {s: [e for e in es if not is_fn(e) or e[3] in evB.get(s, set())] for s, es in A.items()}
    c2 = AN.place(fit, rows_of(shared))
    say('  T2 kept to the events B also marked: %d tales placed: %s; fable ahead: %s'
        % (len(rows_of(shared)), fmt(c2), 'yes' if lead(c2) else 'no'))
    evA = {s: {e[3] for e in es if is_fn(e)} for s, es in A.items()}
    sharedB = {s: [e for e in es if not is_fn(e) or e[3] in evA.get(s, set())] for s, es in B.items()}
    say('  reported: B kept to the events A also marked, B\'s own model: %s'
        % fmt(AN.place(M.table(M.stories('B')), rows_of(sharedB))))
    say()
    say('PREDICTIONS (LengthProtocol.md)')
    say('  1. thinned to B\'s count, A\'s animal tales are placed as fable ahead of every other genre in at least %d of %d draws: %s'
        % (DRAWS // 2 + 1, DRAWS, 'HOLDS' if k1 > DRAWS // 2 else 'FAILS'))
    say('  2. kept to the events B also marked, A\'s animal tales are placed as fable ahead of every other genre: %s'
        % ('HOLDS' if lead(c2) else 'FAILS'))
    open(os.path.join(HERE, 'LengthRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


def selftest():
    """1. Plumbing: thinning each A tale to its own count reproduces the frozen placement.
    2. Validity: held-out wondertales (the model fitted on the other half) thinned to the animal tales' lengths in B,
    drawn at random: if they too go to fable, thinning alone moves stories to fable and prediction 1 cannot tell."""
    A, B = read('A'), read('B')
    fit = M.table(M.stories('A'))
    nA, nB = counts(A), counts(B)
    say('1. A thinned to its own count: %s (the frozen score: tale 26, fable 12, tragedy 3, myth 7)'
        % fmt(AN.place(fit, rows_of({s: thin(es, nA[s], random.Random(SEED)) for s, es in A.items()}))))
    lens = sorted(nB.values())
    for L in 'AB':
        allrows = M.table(M.stories(L))
        spl = M.split(allrows)
        fitL = [r for r in allrows if spl[r[1]] == 'fit']
        S = M.stories(L)
        for g in ('tale', 'tragedy', 'myth'):
            test = {s: [(m, b, neg, i) for i, (m, b, neg) in enumerate(es)] for s, es in S[g].items() if spl.get(s) == 'test'}
            say('2. %s, held-out %s (%d), unthinned: %s' % (L, PLURAL[g], len(rows_of(test)), fmt(AN.place(fitL, rows_of(test)))))
            rnd = random.Random(SEED)
            target = {s: rnd.choice(lens) for s in test}
            thinned_arm(fitL, test, target, '   %s, held-out %s thinned to B\'s animal lengths' % (L, PLURAL[g]))


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
