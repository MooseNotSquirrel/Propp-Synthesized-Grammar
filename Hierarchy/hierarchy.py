#!/usr/bin/env python3
"""
hierarchy.py -- social hierarchy in Propp's character set (Hierarchy/HierarchyProtocol.md, frozen 2026-10-28).

  python hierarchy.py k1    test K1: the invented stories of K1Stories.txt give their known answers
  python hierarchy.py k2    test K2: each character's relations as performer equal the character table's
  python hierarchy.py k3    test K3: two runs byte-identical
  python hierarchy.py dry   counts only: acts, acts between characters, acts between the hero and each sphere's holders
  python hierarchy.py run   write Hierarchy/HierarchyRun.txt

The acts are joined to the characters exactly as Characters/characters.py joins them: by name where English, by event
where Russian; a relation is the performer's to the undergoer. Rank is above and below only (decision 3). The hero is the
judged hero, mended (FailedHero/failedHero.py). Every figure per transcriber; the myths have no acts.

The keeper's operational rules, fixed here before the run (not from Propp, not the owner's): measure 4 uses the
characters holding exactly one sphere, so that each has one label; prediction 3 compares the villain's holders with the
holders of each other sphere, a character holding both being left out of that comparison.
"""
import collections
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'FailedHero'))
import failedHero as F  # noqa: E402

C, DT, SX = F.C, F.DT, F.SX
CORPORA = ['tale', 'animal', 'fable', 'tragedy']
NAMES = F.NAMES
RELATIONS = ['kin', 'spouse', 'above', 'below', 'ally', 'enemy', 'stranger', 'divine', 'self', 'none']
SPHERES = list(SX.SPHERES)
PAIRS = [('hero', 'helper'), ('helper', 'hero'), ('hero', 'false hero'), ('false hero', 'hero'), ('dispatcher', 'hero'),
         ('hero', 'dispatcher'), ('villain', 'hero'), ('princess', 'hero')]
PERMS, SEED, FLOOR, SHUFFLES = 10000, 20261028, 10, 1000
OUT = os.path.join(HERE, 'HierarchyRun.txt')


# ---------------------------------------------------------------- the join, as characters.py makes it
def story_acts(L, g):
    """{story: (performer acts [(character, relation)], pair acts [(performer, undergoer, relation)])}"""
    A = C.act_rows()
    out = {}
    for s, ents in C.entries(L, g).items():
        acts = A.get((g + ':' + s, L), [])
        canon = SX.merge([e[:3] for e in ents])
        names = {k for e in ents for k in e[1:3] if k}
        links = {a: c for a, (c, _) in C.event_join(g, L, s, ents, acts).items()}

        def who(raw):
            k = SX.key(raw)
            if not k:
                return None
            if C.CYR.search(raw):
                c = links.get(k)
            else:
                c = C.name_join(k, names, canon)
            return ' '.join(c) if c else None
        perf, pairs = [], []
        for r in acts:
            rel = r['relation'].lower()
            ps = [c for c in (who(x) for x in SX.split_field(r['performer'])) if c]
            us = [c for c in (who(x) for x in SX.split_field(r['undergoer'])) if c]
            perf += [(p, rel) for p in ps]
            pairs += [(p, u, rel) for p in ps for u in us]
        out[s] = (perf, pairs)
    return out


def spheres_table():
    by = collections.defaultdict(dict)
    for r in DT.rows('characters'):
        by[(r['corpus'], r['reader'], r['story'])][r['character']] = r
    return by


# ---------------------------------------------------------------- the measures of one story
def holders(sph, name):
    return {c for c, ss in sph.items() if name in ss}


def pair_counts(pairs, sph, hero):
    """{(sphere a, sphere b): Counter(relation)}, the hero standing for 'hero'"""
    def who(name):
        return {hero} if name == 'hero' else holders(sph, name) - {hero}
    out = {}
    for a, b in PAIRS:
        A, B = who(a), who(b)
        out[(a, b)] = collections.Counter(rel for p, u, rel in pairs if p in A and u in B and p != u)
    return out


def k1():
    ok, cur = True, None
    for l in open(os.path.join(HERE, 'K1Stories.txt'), encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('story '):
            w = l.split()
            cur = {'name': w[1], 'hero': w[3], 'sph': {}, 'pairs': [], 'perf': []}
        elif l.startswith('sphere ') and cur:
            c, ss = l[7:].split(':')
            cur['sph'][c.strip()] = set(ss.split())
        elif l.startswith('expect ') and cur:
            exp = dict(x.split('=') for x in l.split()[1:])
            pc = pair_counts(cur['pairs'], cur['sph'], cur['hero'])
            vil = holders(cur['sph'], 'villain')
            vrel = [rel for p, rel in cur['perf'] if p in vil]
            got = {'counted': str(len(cur['pairs'])),
                   'hero>helper': '%d/%d' % (pc[('hero', 'helper')]['above'], pc[('hero', 'helper')]['below']),
                   'helper>hero': '%d/%d' % (pc[('helper', 'hero')]['above'], pc[('helper', 'hero')]['below']),
                   'villain_enemy': '%d/%d' % (vrel.count('enemy'), len(vrel))}
            good = got == exp
            ok &= good
            print('K1 %-20s %s' % (cur['name'], 'pass' if good else 'FAIL: expected %s, got %s' % (exp, got)))
        elif ' | ' in l and cur:
            act, p, u, rel = [x.strip() for x in l.split('|')]
            cur['perf'].append((p, rel))
            if u != '-':
                cur['pairs'].append((p, u, rel))
    print('K1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def k2():
    T = spheres_table()
    ok = True
    for g in CORPORA:
        for L in 'AB':
            diff = n = 0
            for s, (perf, pairs) in story_acts(L, g).items():
                mine = collections.defaultdict(collections.Counter)
                for c, rel in perf:
                    mine[c][rel] += 1
                for c, r in T.get((g, L, s), {}).items():
                    theirs = collections.Counter({k: int(v) for k, v in (t.rsplit(' ', 1) for t in r['relations'].split('; ') if t)})
                    n += 1
                    diff += mine.get(c, collections.Counter()) != theirs
            good = diff == 0
            ok &= good
            print('K2 %-8s %s characters %4d, relation counts differing from the table %d: %s' % (g, L, n, diff, 'pass' if good else 'FAIL'))
    print('K2 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def collect():
    """{(g, L): [(story, hero, spheres {character: set}, performer acts, pair acts, U undergone, W performed)]}"""
    T, J = spheres_table(), F.judged()
    out = {}
    for g in CORPORA:
        for L in 'AB':
            ents = C.entries(L, g)
            rows = []
            for s, (perf, pairs) in story_acts(L, g).items():
                chars = T.get((g, L, s), {})
                sph = {c: set(r['spheres'].split(' + ')) - {''} for c, r in chars.items()}
                hero, how = F.heroes(g, L, s, chars, J)
                canon = SX.merge([e[:3] for e in ents[s]])
                nm = lambda k: ' '.join(canon.get(k, k))
                U = {nm(e[2]) for e in ents[s] if e[0] == 'U' and e[2]}
                W = {nm(e[1]) for e in ents[s] if e[0] == 'W' and e[1]}
                rows.append((s, hero, sph, perf, pairs, U, W))
            out[(g, L)] = rows
    return out


def dry():
    M = collect()
    for g in CORPORA:
        for L in 'AB':
            rows = M[(g, L)]
            line = ', '.join('%s>%s %d' % (a, b, sum(sum(pair_counts(r[4], r[2], r[1])[(a, b)].values()) for r in rows if r[1]))
                             for a, b in PAIRS)
            print('%-8s %s stories %3d, acts as performer %5d, acts between characters %5d; %s'
                  % (g, L, len(rows), sum(len(r[3]) for r in rows), sum(len(r[4]) for r in rows), line))


# ---------------------------------------------------------------- the run
def binom_p(k, n):
    """one-sided: P(X >= k) for X ~ Binomial(n, 1/2)"""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2.0 ** n if n else 1.0


def perm_units(xs, ys, stat):
    real = stat(xs, ys)
    pool = xs + ys
    rnd = random.Random(SEED)
    hit = 0
    for _ in range(PERMS):
        rnd.shuffle(pool)
        hit += stat(pool[:len(xs)], pool[len(xs):]) >= real - 1e-12
    return real, (hit + 1.0) / (PERMS + 1)


def pooled(units):
    n = sum(u[0] for u in units)
    d = sum(u[1] for u in units)
    return n / float(d) if d else 0.0


def nearest_centroid(X, y):
    """leave-one-out accuracy of the nearest class mean (Euclidean)"""
    labels = sorted(set(y))
    sums = {l: [0.0] * len(X[0]) for l in labels}
    cnt = collections.Counter(y)
    for x, l in zip(X, y):
        sums[l] = [a + b for a, b in zip(sums[l], x)]
    right = 0
    for x, l in zip(X, y):
        best = None
        for m in labels:
            n = cnt[m] - (m == l)
            if n == 0:
                continue
            mean = [(a - (b if m == l else 0.0)) / n for a, b in zip(sums[m], x)]
            d = sum((a - b) ** 2 for a, b in zip(x, mean))
            if best is None or d < best[0] - 1e-12:
                best = (d, m)
        right += best is not None and best[1] == l
    return right / float(len(X))


def report():
    M = collect()
    out = ['# HierarchyRun.txt -- hierarchy.py: Hierarchy/HierarchyProtocol.md (frozen 2026-10-28), every figure per transcriber; rank is above and below',
           '# the keeper\'s operational rules are in hierarchy.py\'s header']
    res = {}
    for g in CORPORA:
        for L in 'AB':
            rows = M[(g, L)]
            out.append('')
            out.append('== %s, transcriber %s: %d stories' % (NAMES[g], L, len(rows)))
            # 1. relations by sphere, as performer
            for sp in SPHERES:
                rel = collections.Counter(r for s, h, sph, perf, pairs, U, W in rows for c, r in perf if sp in sph.get(c, ()))
                n = sum(rel.values())
                if n:
                    out.append('  1. %-10s acts %4d: %s' % (sp, n, ', '.join('%s %.0f%%' % (k, 100.0 * rel[k] / n) for k in RELATIONS if rel[k])))
            # 2. pairs
            for a, b in PAIRS:
                c = collections.Counter()
                for s, h, sph, perf, pairs, U, W in rows:
                    if h:
                        c.update(pair_counts(pairs, sph, h)[(a, b)])
                if sum(c.values()):
                    out.append('  2. %-10s > %-10s acts %3d: above %d, below %d; %s' % (a, b, sum(c.values()), c['above'], c['below'],
                               ', '.join('%s %d' % kv for kv in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))))
            # 3. stated hierarchy
            units = [(sum(1 for p, u, rel in pairs if rel in ('above', 'below')), len(pairs)) for s, h, sph, perf, pairs, U, W in rows if pairs]
            out.append('  3. stated hierarchy: %.1f%% of %d acts between characters (%d stories)' % (100 * pooled(units), sum(u[1] for u in units), len(units)))
            # 4. the relation predicts the sphere
            X, y = [], []
            for s, h, sph, perf, pairs, U, W in rows:
                prof = collections.defaultdict(collections.Counter)
                for c, rel in perf:
                    prof[c][rel] += 1
                for c, ss in sph.items():
                    n = sum(prof[c].values())
                    if len(ss) == 1 and n >= 3:
                        X.append([prof[c][k] / float(n) for k in RELATIONS])
                        y.append(next(iter(ss)))
            acc4 = reach = None
            if len(X) >= 30 and len(set(y)) > 1:
                acc4 = nearest_centroid(X, y)
                reach = 0
                for i in range(SHUFFLES):
                    yy = y[:]
                    random.Random(i).shuffle(yy)
                    reach += nearest_centroid(X, yy) >= acc4 - 1e-12
                out.append('  4. the relation predicts the sphere: %d single-sphere holders with 3 acts, accuracy %.1f%%, %d of %d shuffles reach it'
                           % (len(X), 100 * acc4, reach, SHUFFLES))
            else:
                out.append('  4. the relation predicts the sphere: %d single-sphere holders with 3 acts, too few (30 needed)' % len(X))
            # 5. narrative rank, reported
            for sp in SPHERES:
                hs = [(c, s) for s, h, sph, perf, pairs, U, W in rows for c in holders(sph, sp)]
                if hs:
                    pu = sum(1 for s, h, sph, perf, pairs, U, W in rows for c in holders(sph, sp) if c in U)
                    pw = sum(1 for s, h, sph, perf, pairs, U, W in rows for c in holders(sph, sp) if c in W)
                    out.append('  5. %-10s holders %4d: punished (U) %d (%.0f%%), rewarded or wed (W) %d (%.0f%%)'
                               % (sp, len(hs), pu, 100.0 * pu / len(hs), pw, 100.0 * pw / len(hs)))
            res[(g, L)] = (rows, units, acc4, reach, len(X))
    out.append('')
    out.append('== predictions (HierarchyProtocol.md section 5): p at most 0.05; floor %d acts or stories a side' % FLOOR)
    held = {i: {} for i in range(1, 6)}
    for L in 'AB':
        rows = res[('tale', L)][0]
        tot = {k: collections.Counter() for k in PAIRS}
        for s, h, sph, perf, pairs, U, W in rows:
            if h:
                for k, c in pair_counts(pairs, sph, h).items():
                    tot[k].update(c)
        hh, he = tot[('hero', 'helper')], tot[('helper', 'hero')]
        n1, n2 = hh['above'] + hh['below'], he['above'] + he['below']
        if n1 < FLOOR or n2 < FLOOR:
            held[1][L] = None
            out.append('  1. %s: NOT TESTABLE (floor): hero>helper above %d below %d; helper>hero above %d below %d' % (L, hh['above'], hh['below'], he['above'], he['below']))
        else:
            pa, pb = binom_p(hh['above'], n1), binom_p(he['below'], n2)
            held[1][L] = pa <= 0.05 and pb <= 0.05
            out.append('  1. %s: wondertales, hero>helper above %d below %d (p %.4f); helper>hero below %d above %d (p %.4f): %s'
                       % (L, hh['above'], hh['below'], pa, he['below'], he['above'], pb, 'holds' if held[1][L] else 'does not hold'))
        lo = hi = 0
        for g in CORPORA:
            for s, h, sph, perf, pairs, U, W in res[(g, L)][0]:
                if h:
                    pc = pair_counts(pairs, sph, h)
                    lo += pc[('false hero', 'hero')]['below'] + pc[('hero', 'false hero')]['above']
                    hi += pc[('false hero', 'hero')]['above'] + pc[('hero', 'false hero')]['below']
        if lo + hi < FLOOR:
            held[2][L] = None
            out.append('  2. %s: NOT TESTABLE (floor): the false hero below %d, above %d, all corpora' % (L, lo, hi))
        else:
            p = binom_p(lo, lo + hi)
            held[2][L] = p <= 0.05
            out.append('  2. %s: the false hero below %d, above %d, all corpora, p %.4f: %s' % (L, lo, hi, p, 'holds' if held[2][L] else 'does not hold'))
        res3 = []
        for g in ('tale', 'tragedy'):
            rows = res[(g, L)][0]
            for sp in SPHERES:
                if sp == 'villain':
                    continue
                vil, oth = [], []
                for s, h, sph, perf, pairs, U, W in rows:
                    prof = collections.defaultdict(list)
                    for c, rel in perf:
                        prof[c].append(rel)
                    for c, ss in sph.items():
                        rs = prof.get(c)
                        if not rs:
                            continue
                        unit = (rs.count('enemy'), len(rs))
                        if 'villain' in ss and sp not in ss:
                            vil.append(unit)
                        elif sp in ss and 'villain' not in ss:
                            oth.append(unit)
                if len(vil) < FLOOR or len(oth) < FLOOR:
                    out.append('  3. %s %-12s villain against %-10s: NOT TESTABLE (floor: %d and %d characters)' % (L, NAMES[g], sp, len(vil), len(oth)))
                    res3.append(None)
                    continue
                d, p = perm_units(vil, oth, lambda a, b: pooled(a) - pooled(b))
                res3.append(d > 0 and p <= 0.05)
                out.append('  3. %s %-12s villain enemy %.0f%% against %-10s %.0f%% (%d and %d characters), p %.4f: %s'
                           % (L, NAMES[g], 100 * pooled(vil), sp, 100 * pooled(oth), len(vil), len(oth), p, 'holds' if res3[-1] else 'does not hold'))
        tested = [x for x in res3 if x is not None]
        held[3][L] = None if not tested else all(tested)
        res4 = [(g, res[(g, L)][2], res[(g, L)][3]) for g in CORPORA if res[(g, L)][2] is not None]
        held[4][L] = None if not res4 else all(r <= SHUFFLES // 20 for g, a, r in res4)
        out.append('  4. %s: %s' % (L, '; '.join('%s accuracy %.1f%%, %d shuffles reach it' % (NAMES[g], 100 * a, r) for g, a, r in res4) or 'none testable'))
        t = res[('tragedy', L)][1]
        r5 = []
        for g in ('tale', 'fable'):
            o = res[(g, L)][1]
            if len(t) < FLOOR or len(o) < FLOOR:
                r5.append(None)
                out.append('  5. %s: tragedies against %s: NOT TESTABLE (floor)' % (L, NAMES[g]))
                continue
            d, p = perm_units(t, o, lambda a, b: pooled(a) - pooled(b))
            r5.append(d > 0 and p <= 0.05)
            out.append('  5. %s: stated hierarchy, tragedies %.1f%% (%d) against %s %.1f%% (%d), p %.4f: %s'
                       % (L, 100 * pooled(t), len(t), NAMES[g], 100 * pooled(o), len(o), p, 'holds' if r5[-1] else 'does not hold'))
        held[5][L] = None if None in r5 else all(r5)
    texts = {1: 'the hero above the helper, in the wondertales', 2: 'the false hero below', 3: 'the villain\'s enmity (a replication)',
             4: 'the relation predicts the sphere', 5: 'stated hierarchy higher in the tragedies'}
    for i in range(1, 6):
        out.append('  %d. %s: %s' % (i, texts[i], F.verdict(held[i]['A'], held[i]['B'])))
    return '\n'.join(out) + '\n'


def k3():
    ok = report() == report()
    print('K3 two runs byte-identical: %s' % ('PASS' if ok else 'FAIL'))
    return ok


def run():
    text = report()
    if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        raise SystemExit('refusing to overwrite the record %s' % OUT)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'k1': k1, 'k2': k2, 'k3': k3, 'dry': dry, 'run': run}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
