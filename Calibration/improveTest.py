#!/usr/bin/env python3
"""
improveTest.py -- the improvement test of ImproveProtocol.md.

  python improveTest.py dev     the development tales (as often as wanted)
  python improveTest.py test    the test tales, once, after this file and the
                                development figures are committed

THE PIPELINE, chosen on the development tales (KeeperLog, 2026-10-05) and
frozen with this file: the PROPP VIEW of a transcription.
  1. Each tale's function entries marked Y (the primary reading), X and the
     preparatory functions left out, symbols reduced as compare.py reduces
     them, grouped by the transcriber's moves in the order of the notes.
  2. Within each move, each function is written once, where it first
     appears: Propp's scheme records which functions a move holds, and
     writes repetitions (trebling, parallel episodes) once or in braces.
  3. An implicit C: a C is written before a departure (up) that follows a
     villainy, lack or mediation (A, a, B) with no C between, as Propp
     writes C where the hero's decision is not told (p.38).
  It uses the transcription alone and no tale's scheme.
Consensus of the four readings was tried and not chosen: it did no better
than a single reading.

THE TEST, as frozen: for each of the four readings (arm U and C, transcriber
A and B), content and order against Propp, as written and in the Propp view,
per tale; a one-sided paired sign-flip permutation test on the per-tale
differences, 10,000 permutations, seed 46, p = (flips with mean difference
at least the observed + 1) / 10,001. Reported beside them: chance-corrected
figures, (real - chance) / (1 - chance), chance from 1000 derangements of
the tales scored, seed 46; v46 acceptance of the Propp view's moves (the
tragedy test's moves, each projected by steps 2 and 3); the A-B agreement.
ADOPTED, fixed here before the test tales are scored, if for ALL FOUR
readings: (1) content and order each improve with p <= 0.05; (2) each
test-tale improvement is at least half the development-tale improvement;
(3) both still beat the derangements, at most 50 of 1000 at or above.
"""
import collections
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compare as C  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'Afanasyev')
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(HERE, 'Split.txt'), encoding='utf-8') if '|' in l}
READINGS = [(a, L) for a in C.ARMS for L in C.LINEAGES]


def kept_keys(x):
    return [k for k in C.TS.key(x['sym']) if k in C.VOCAB] if C.TS.kept(x, 'primary') else []


def written(es):
    return [k for x in sorted(es, key=lambda x: x['line']) for k in kept_keys(x)]


def once(s):
    out = []
    for k in s:
        if k not in out:
            out.append(k)
    return out


def implicit_c(s):
    out, pending = [], False
    for k in s:
        if k in ('A', 'a', 'B'):
            pending = True
        if k == 'C':
            pending = False
        if k == 'up' and pending:
            out.append('C')
            pending = False
        out.append(k)
    return out


def view_moves(moves):
    """the Propp view of a list of moves (lists of keys)."""
    return [implicit_c(once(m)) for m in moves]


def view(es):
    mv = collections.OrderedDict()
    for x in sorted(es, key=lambda x: x['line']):
        ks = kept_keys(x)
        if ks:
            mv.setdefault(x['move'], []).extend(ks)
    return [k for m in view_moves(list(mv.values())) for k in m]


def per_tale(fn, S, P, tales):
    return [fn(S[t], P[t][0]) for t in tales]


def chance(fn, S, P, tales, D):
    return C.mean(C.mean(fn(S[tales[i]], P[tales[p[i]]][0]) for i in range(len(tales))) for p in D)


def flip_p(d, n=10000, seed=46):
    rng = random.Random(seed)
    obs = sum(d) / len(d)
    hits = sum(1 for _ in range(n) if sum(x if rng.random() < 0.5 else -x for x in d) / len(d) >= obs)
    return (hits + 1) / float(n + 1)


def acceptance(es, g):
    ok = tot = 0
    for k in view_moves(C.TS.moves(es, 'primary', '', False)):
        if k:
            tot += 1
            ok += C.parse.accept(list(k), g.bnf, g.start, g.table)[0]
    return ok, tot


def run(part):
    tales = SPLIT[part]
    P = C.propp()
    D = C.derangements(len(tales), 1000, 46)
    g = C.TS.grammar(False)
    E = {r: C.load(REPO, *r) for r in READINGS}
    W = {r: {t: written(E[r].get(t, [])) for t in tales} for r in READINGS}
    V = {r: {t: view(E[r].get(t, [])) for t in tales} for r in READINGS}
    print('IMPROVEMENT TEST, %s tales (%d): %s' % (part, len(tales), ' '.join(map(str, tales))))
    out = {}
    for r in READINGS:
        print('\nREADING %s/%s' % r)
        res = {}
        for name, fn in (('content', C.dice), ('order', C.order)):
            w, v = per_tale(fn, W[r], P, tales), per_tale(fn, V[r], P, tales)
            d = [b - a for a, b in zip(w, v)]
            cw, cv = chance(fn, W[r], P, tales, D), chance(fn, V[r], P, tales, D)
            mw, mv = C.mean(w), C.mean(v)
            above = sum(1 for p in D if C.mean(fn(V[r][tales[i]], P[tales[p[i]]][0]) for i in range(len(tales))) >= mv)
            p = flip_p(d)
            res[name] = (mv - mw, p, above)
            print('  %-7s written %.3f (cc %.2f)  view %.3f (cc %.2f)  gain %+.3f  p %.4f  derangements at or above %d of 1000'
                  % (name, mw, (mw - cw) / (1 - cw), mv, (mv - cv) / (1 - cv), mv - mw, p, above))
        acc = [acceptance(E[r].get(t, []), g) for t in tales]
        ok, tot = sum(a[0] for a in acc), sum(a[1] for a in acc)
        print('  v46 accepts %d of %d view moves (%.1f%%)' % (ok, tot, 100.0 * ok / max(1, tot)))
        out[r] = res
    for arm in C.ARMS:
        print('\nA-B, arm %s: written content %.3f order %.3f; view content %.3f order %.3f' % (
            arm,
            C.mean(C.dice(W[arm, 'A'][t], W[arm, 'B'][t]) for t in tales),
            C.mean(C.order(W[arm, 'A'][t], W[arm, 'B'][t]) for t in tales),
            C.mean(C.dice(V[arm, 'A'][t], V[arm, 'B'][t]) for t in tales),
            C.mean(C.order(V[arm, 'A'][t], V[arm, 'B'][t]) for t in tales)))
    return out


DEV_GAINS = {  # from the committed development run (ImproveDev.txt), before the test
    ('U', 'A'): {'content': 0.120, 'order': 0.111},
    ('U', 'B'): {'content': 0.126, 'order': 0.101},
    ('C', 'A'): {'content': 0.134, 'order': 0.111},
    ('C', 'B'): {'content': 0.093, 'order': 0.088},
}


def main(argv):
    if argv == ['dev']:
        run('dev')
        return 0
    if argv == ['test']:
        if not DEV_GAINS:
            sys.exit('the development gains are not yet committed in DEV_GAINS')
        res = run('test')
        adopted = True
        print('\nTHE DECISION')
        for r in READINGS:
            for name in ('content', 'order'):
                gain, p, above = res[r][name]
                half = DEV_GAINS[r][name] / 2.0
                ok = p <= 0.05 and gain >= half and above <= 50
                adopted = adopted and ok
                print('  %s/%s %-7s gain %+.3f (needs >= %.3f), p %.4f, derangements %d: %s'
                      % (r[0], r[1], name, gain, half, p, above, 'holds' if ok else 'FAILS'))
        print('VERDICT: %s' % ('ADOPTED' if adopted else 'NOT ADOPTED'))
        return 0
    sys.exit(__doc__)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
