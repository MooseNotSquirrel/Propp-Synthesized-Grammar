#!/usr/bin/env python3
"""
revealedVillain.py -- the revealed villain, route (a), from the tables (FailedHero/RevealedVillainProtocol.md, frozen
2026-10-28).

  python revealedVillain.py r1    test R1: the invented stories of R1Stories.txt give their known answers
  python revealedVillain.py r4    test R4: two runs byte-identical
  python revealedVillain.py dry   counts only: stories, judged heroes found, stories with an Ex, stories with a Q
  python revealedVillain.py run   write FailedHero/RevealedVillainTables.txt

A story counts when its judged hero is the undergoer of an exposure (Ex), or of a recognition (Q) that follows a
villainy (A) in the same story. The hero is the judged hero as failedHero.py finds it (mended 2026-10-28); stories whose
readers named no single hero, or none, are left out, and the myths take no part. Every figure per transcriber. The
route's known false positive, recorded in R1: a hero recognized after another's villainy counts.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import failedHero as F  # noqa: E402

CORPORA = ['tale', 'animal', 'fable', 'tragedy']
OUT = os.path.join(HERE, 'RevealedVillainTables.txt')


def revealed(funcs, hero):
    """funcs: [(function, performer, undergoer)] in order"""
    seen_a = False
    for fn, p, u in funcs:
        if fn == 'A':
            seen_a = True
        if u == hero and (fn == 'Ex' or (fn == 'Q' and seen_a)):
            return True
    return False


def r1():
    ok, cur, out = True, None, []
    for l in open(os.path.join(HERE, 'R1Stories.txt'), encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('story '):
            w = l.split()
            cur = [w[1], w[3], []]
        elif l.startswith('expect ') and cur:
            got = 'Y' if revealed(cur[2], cur[1]) else 'N'
            want = l.split('=')[1].strip()
            good = got == want
            ok &= good
            print('R1 %-40s %s' % (cur[0], 'pass' if good else 'FAIL: expected %s, got %s' % (want, got)))
        elif ' | ' in l and cur:
            cur[2].append(tuple(x.strip() for x in l.split('|')))
    print('R1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def per_story(L, g, T, J):
    out = []
    for s, (n, ents) in F.stories(L, g).items():
        chars = T.get((g, L, s), {})
        h, how = F.heroes(g, L, s, chars, J)
        if h is None:
            out.append((s, None, how, None))
            continue
        # one function a position: the parts of a split field keep their function's place
        funcs = [(fn, p, u) for i, fn, neg, p, u in ents]
        out.append((s, h, how, revealed(funcs, h)))
    return out


def dry():
    T, J = F.table(), F.judged()
    for g in CORPORA:
        for L in 'AB':
            st = F.stories(L, g)
            ps = per_story(L, g, T, J)
            print('%-8s %s stories %3d, judged hero found %3d, stories with an Ex %3d, with a Q %3d'
                  % (g, L, len(st), sum(1 for x in ps if x[1]), sum(1 for n, ents in st.values() if any(e[1] == 'Ex' for e in ents)),
                     sum(1 for n, ents in st.values() if any(e[1] == 'Q' for e in ents))))


def report():
    T, J = F.table(), F.judged()
    out = ['# RevealedVillainTables.txt -- revealedVillain.py: route (a) of FailedHero/RevealedVillainProtocol.md (frozen 2026-10-28), per transcriber',
           '# the hero revealed: the undergoer of an Ex, or of a Q after an A; the hero the judged hero, mended; the myths take no part']
    M = {}
    for g in CORPORA:
        for L in 'AB':
            ps = per_story(L, g, T, J)
            M[(g, L)] = ps
            ms = [x for x in ps if x[1]]
            yes = sorted(s for s, h, how, r in ms if r)
            out.append('%-12s %s: judged heroes %3d, revealed %3d (%.0f%%): %s' % (F.NAMES[g], L, len(ms), len(yes),
                       100 * F.share([bool(r) for s, h, how, r in ms]), ' '.join(yes) or 'none'))
    out.append('')
    out.append('== prediction 2 (route a): permutation test, %d permutations, p at most 0.05; floor %d stories a side' % (F.PERMS, F.FLOOR))
    held = {}
    for L in 'AB':
        t = [bool(r) for s, h, how, r in M[('tragedy', L)] if h]
        w = [bool(r) for s, h, how, r in M[('tale', L)] if h]
        if len(t) < F.FLOOR or len(w) < F.FLOOR:
            held[L] = None
            out.append('  2. %s: NOT TESTABLE (floor): tragedies %d, wondertales %d' % (L, len(t), len(w)))
            continue
        d, p = F.perm_p(t, w, lambda a, b: F.share(a) - F.share(b))
        held[L] = d > 0 and p <= 0.05
        out.append('  2. %s: revealed, tragedies %.0f%% (%d) against wondertales %.0f%% (%d): difference %+.0f points, p %.4f: %s'
                   % (L, 100 * F.share(t), len(t), 100 * F.share(w), len(w), 100 * d, p, 'holds' if held[L] else 'does not hold'))
    out.append('  2. by the tables, the hero revealed in more tragedies than wondertales: %s' % F.verdict(held['A'], held['B']))
    return '\n'.join(out) + '\n'


def r4():
    ok = report() == report()
    print('R4 two runs byte-identical: %s' % ('PASS' if ok else 'FAIL'))
    return ok


def run():
    text = report()
    if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        raise SystemExit('refusing to overwrite the record %s' % OUT)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'r1': r1, 'r4': r4, 'dry': dry, 'run': run}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
