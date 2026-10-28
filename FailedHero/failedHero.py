#!/usr/bin/env python3
"""
failedHero.py -- the failed hero as Propp's own apparatus (FailedHero/FailedHeroProtocol.md, frozen 2026-10-28).

  python failedHero.py h1     test H1: the invented stories of H1Stories.txt give their known answers
  python failedHero.py h2     test H2: the fused hero-villain characters equal the character table's spheres
  python failedHero.py h3     test H3: every judged hero found once or listed as not found
  python failedHero.py h4     test H4: two runs byte-identical
  python failedHero.py dry    counts only: stories, judged heroes found, stories with a U, stories with a negative mark
  python failedHero.py run    write FailedHero/FailedHeroRun.txt (the record; refused if it would change)
  python failedHero.py run --mended   write FailedHero/FailedHeroRun-mended.txt, after the mend of 2026-10-28, beside the record

Every figure is given for transcribers A and B separately. The hero is the judged hero (Heroes/JudgedHeroes.txt), found
as the character of its story whose key it joins; for the myths, which have none, the hero-sphere holder with the most
functions, marked as a different rule and kept out of predictions 2 and 3 (decision 1). "Late" is the last third of
the story's functions by position (decision 2): function i of n is late when 3i >= 2n.
"""
import collections
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Characters'))
import characters as C  # noqa: E402

DT, SX, TS = C.DT, C.SX, C.TS
CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'myth']
NAMES = {'tale': 'wondertales', 'animal': 'animal tales', 'fable': 'fables', 'tragedy': 'tragedies', 'myth': 'myths'}
PERMS = 10000
SEED = 20261028
FLOOR = 10
OUT = os.path.join(HERE, 'FailedHeroRun.txt')


# ---------------------------------------------------------------- one story's measures
def late(i, n):
    return 3 * i >= 2 * n


def measures(funcs, hero, spheres):
    """funcs: [(function, negative, performer, undergoer)] in order; hero: the hero's character; spheres: the hero's
    spheres. Returns fused, (late negative, late), (early negative, early), punished hero (True, False or None), open"""
    n = len(funcs)
    ln = lt = en = et = 0
    for i, (fn, neg, p, u) in enumerate(funcs):
        if hero in (p, u):
            if late(i, n):
                lt += 1
                ln += bool(neg)
            else:
                et += 1
                en += bool(neg)
    us = [u for i, (fn, neg, p, u) in enumerate(funcs) if fn == 'U' and late(i, n)]
    punished = (us[-1] == hero) if us else None
    last_a = max([i for i, f in enumerate(funcs) if f[0] in ('A', 'a')], default=None)
    opened = last_a is not None and not any(f[0] == 'K' for f in funcs[last_a + 1:])
    fused = 'hero' in spheres and 'villain' in spheres
    return fused, (ln, lt), (en, et), punished, opened


def spheres_of(funcs, who):
    return {n for fn, neg, p, u in funcs if p == who for n, fs in SX.SPHERES.items() if fn in fs}


# ---------------------------------------------------------------- the tables
def stories(L, g):
    """{story: [(function, negative, performer character, undergoer character)]}, the first reading, several-name fields
    split as characters.entries() splits them, each part keeping the function's position"""
    st = collections.OrderedDict()
    for r in DT.files('functions', C.PATS[g], L):
        base = DT.local(r['story'])
        if not C.re.match(r'^([PFA]\d{2}|L\d-\d{3})', base):
            continue
        st.setdefault(base, collections.OrderedDict()).setdefault(r['version'] or '1', []).append(
            (TS.base(r['raw']), r['performer'].strip(), r['undergoer'].strip(), bool(r['negative'].strip())))
    out = collections.OrderedDict()
    for s, vs in st.items():
        rows = SX.first_reading(vs)
        ents = [(i,) + e + (neg,) for i, (fn, pr, ur, neg) in enumerate(rows) for e in SX.expand(fn, pr, ur)]
        canon = SX.merge([e[1:4] for e in ents])
        name = lambda k: ' '.join(canon.get(k, k)) if k else ''
        # one entry per part; the position is the function's own, so that a split field does not stretch the story
        out[s] = (len(rows), [(i, fn, neg, name(pk), name(uk)) for i, fn, pk, uk, pn, un, neg in ents])
    return out


def positioned(n, ents):
    """the entries as funcs for measures(): the position is carried by repeating the function's index"""
    return n, [(fn, neg, p, u) for i, fn, neg, p, u in ents], [i for i, *_ in ents]


def table():
    by = collections.defaultdict(dict)
    for r in DT.rows('characters'):
        by[(r['corpus'], r['reader'], r['story'])][r['character']] = r
    return by


def judged():
    """{story: the judged hero's name}: Heroes/JudgedHeroes.txt, and the animal tales' heroes of session 7
    (Data/Parity/heroes-animal.txt) where the two readers' names give the same key"""
    path = os.path.join(ROOT, 'Heroes', 'JudgedHeroes.txt')
    out = {l.split(' | ')[0]: l.split(' | ')[1].strip() for l in open(path, encoding='utf-8') if not l.startswith('#') and ' | ' in l}
    for l in open(os.path.join(ROOT, 'Data', 'Parity', 'heroes-animal.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split(' | ')]
        if len(f) == 3 and f[0].startswith('A') and f[0][1:].isdigit() and tuple(SX.key(f[1])) == tuple(SX.key(f[2])):
            out[f[0]] = f[1]
    return out


def no_single(name):
    return name.lower().startswith('no single hero')


def find_hero(name, chars):
    """the character of the story the judged hero's name joins: an exact key first, else the one joined; None when none
    or more than one, and None for an entry the readers marked "no single hero" (mended 2026-10-28, KeeperLog)"""
    if no_single(name):
        return None
    k = tuple(SX.key(name))
    exact = [c for c in chars if tuple(c.split()) == k]
    if len(exact) == 1:
        return exact[0]
    cand = [c for c in chars if SX.joins(k, tuple(c.split())) or SX.joins(tuple(c.split()), k)]
    return cand[0] if len(cand) == 1 else None


def heroes(g, L, s, chars, J):
    """(hero character or None, how found)"""
    if g == 'myth':
        hs = [r for r in chars.values() if 'hero' in r['spheres'].split(' + ')]
        if not hs:
            return None, 'no hero-sphere holder'
        return max(hs, key=lambda r: (int(r['performs']), r['character']))['character'], 'hero-sphere rule'
    if s not in J:
        return None, 'no judged hero'
    if no_single(J[s]):
        return None, 'the readers named no single hero'
    h = find_hero(J[s], chars)
    return (h, 'judged') if h else (None, 'judged hero not found')


def per_story(L, g, T, J):
    """[(story, hero, how, measures or None)]"""
    out = []
    for s, (n, ents) in stories(L, g).items():
        chars = T.get((g, L, s), {})
        h, how = heroes(g, L, s, chars, J)
        if h is None:
            out.append((s, None, how, None))
            continue
        funcs = [(fn, neg, p, u) for i, fn, neg, p, u in ents]
        idx = [i for i, *_ in ents]
        sph = set(chars[h]['spheres'].split(' + ')) - {''} if h in chars else set()
        out.append((s, h, how, measures_at(funcs, idx, n, h, sph)))
    return out


def measures_at(funcs, idx, n, hero, spheres):
    """measures() with each entry's own position i of n, for split fields"""
    ln = lt = en = et = 0
    seen = set()
    for (fn, neg, p, u), i in zip(funcs, idx):
        if hero in (p, u) and i not in seen:
            seen.add(i)
            if late(i, n):
                lt += 1
                ln += bool(neg)
            else:
                et += 1
                en += bool(neg)
    us = [(i, u) for (fn, neg, p, u), i in zip(funcs, idx) if fn == 'U' and late(i, n)]
    punished = None
    if us:
        last = max(i for i, u in us)
        punished = any(u == hero for i, u in us if i == last)
    a = [i for (fn, *_), i in zip(funcs, idx) if fn in ('A', 'a')]
    opened = bool(a) and not any(fn == 'K' and i > max(a) for (fn, *_), i in zip(funcs, idx))
    return 'hero' in spheres and 'villain' in spheres, (ln, lt), (en, et), punished, opened


# ---------------------------------------------------------------- the tests
def h1():
    path = os.path.join(HERE, 'H1Stories.txt')
    ok, stories_, cur = True, [], None
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('story '):
            w = l.split()
            cur = [w[1], w[3], []]
        elif l.startswith('expect '):
            cur.append(dict(x.split('=') for x in l.split()[1:]))
            stories_.append(cur)
        elif ' | ' in l and cur:
            fn, neg, p, u = [x.strip() for x in l.split('|')]
            cur[2].append((fn, neg == 'Y', p, u))
    for name, hero, funcs, exp in stories_:
        fused, (ln, lt), (en, et), pun, opened = measures(funcs, hero, spheres_of(funcs, hero))
        got = {'fused': 'Y' if fused else 'N', 'late_neg': '%d/%d' % (ln, lt), 'early_neg': '%d/%d' % (en, et),
               'punished_hero': '-' if pun is None else ('Y' if pun else 'N'), 'open': 'Y' if opened else 'N'}
        # the split-field route must give the same answers
        got2 = measures_at(funcs, list(range(len(funcs))), len(funcs), hero, spheres_of(funcs, hero))
        same = got2 == (fused, (ln, lt), (en, et), pun, opened)
        good = got == exp and same
        ok &= good
        print('H1 %-20s %s%s' % (name, 'pass' if good else 'FAIL: expected %s, got %s' % (exp, got), '' if same else ' (the two routes differ)'))
    print('H1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def h2():
    T = table()
    ok = True
    for g in CORPORA:
        for L in 'AB':
            mine, theirs = set(), set()
            for s, (n, ents) in stories(L, g).items():
                funcs = [(fn, neg, p, u) for i, fn, neg, p, u in ents]
                for c in {p for f, ng, p, u in funcs if p}:
                    if {'hero', 'villain'} <= spheres_of(funcs, c):
                        mine.add((s, c))
                for c, r in T.get((g, L, s), {}).items():
                    if {'hero', 'villain'} <= set(r['spheres'].split(' + ')):
                        theirs.add((s, c))
            good = mine == theirs
            ok &= good
            print('H2 %-8s %s fused characters: from the functions %d, from the table %d, differing %d: %s'
                  % (g, L, len(mine), len(theirs), len(mine ^ theirs), 'pass' if good else 'FAIL'))
    print('H2 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def h3():
    T, J = table(), judged()
    ok = True
    for g in CORPORA[:-1]:
        for L in 'AB':
            found = missing = twice = nosingle = given = 0
            for s, (n, ents) in stories(L, g).items():
                if s not in J:
                    continue
                chars = T.get((g, L, s), {})
                # an entry marked "no single hero" must give no hero (the fault of 2026-10-28)
                if no_single(J[s]):
                    nosingle += 1
                    given += heroes(g, L, s, chars, J)[0] is not None
                    continue
                k = tuple(SX.key(J[s]))
                exact = [c for c in chars if tuple(c.split()) == k]
                cand = [c for c in chars if SX.joins(k, tuple(c.split())) or SX.joins(tuple(c.split()), k)]
                twice += len(exact) > 1
                h = find_hero(J[s], chars)
                found += h is not None
                missing += h is None
            good = not twice and not given
            ok &= good
            print('H3 %-8s %s judged heroes found %d, listed as not found %d, matched to two exact keys %d; "no single hero" %d, given a hero %d: %s'
                  % (g, L, found, missing, twice, nosingle, given, 'pass' if good else 'FAIL'))
    print('H3 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def h4():
    a, b = report(), report()
    ok = a == b
    print('H4 two runs byte-identical: %s' % ('PASS' if ok else 'FAIL'))
    return ok


def dry():
    T, J = table(), judged()
    for g in CORPORA:
        for L in 'AB':
            st = stories(L, g)
            ps = per_story(L, g, T, J)
            print('%-8s %s stories %3d, hero found %3d (%s), stories with a U %3d, with a negative mark %3d'
                  % (g, L, len(st), sum(1 for x in ps if x[1]), 'hero-sphere rule' if g == 'myth' else 'judged',
                     sum(1 for n, ents in st.values() if any(e[1] == 'U' for e in ents)),
                     sum(1 for n, ents in st.values() if any(e[2] for e in ents))))


# ---------------------------------------------------------------- the run
def perm_p(xs, ys, stat):
    """one-sided: the share of label permutations whose statistic reaches the real one"""
    real = stat(xs, ys)
    pool = xs + ys
    rnd = random.Random(SEED)
    hit = 0
    for _ in range(PERMS):
        rnd.shuffle(pool)
        hit += stat(pool[:len(xs)], pool[len(xs):]) >= real - 1e-12
    return real, (hit + 1.0) / (PERMS + 1)


def share(xs):
    return sum(xs) / float(len(xs)) if xs else 0.0


def pooled(ms, part):
    n = sum(m[part][0] for m in ms)
    d = sum(m[part][1] for m in ms)
    return n / float(d) if d else 0.0


def within_p(ms):
    """prediction 2 (a): within each story, the hero's functions' late and early labels shuffled, the pooled late share
    minus the early share"""
    def stat(units):
        ln = sum(u[0] for u in units)
        lt = sum(u[1] for u in units)
        en = sum(u[2] for u in units)
        et = sum(u[3] for u in units)
        return (ln / float(lt) if lt else 0.0) - (en / float(et) if et else 0.0)
    units = [(m[1][0], m[1][1], m[2][0], m[2][1]) for m in ms]
    real = stat(units)
    rnd = random.Random(SEED)
    hit = 0
    for _ in range(PERMS):
        sim = []
        for ln, lt, en, et in units:
            marks = [1] * (ln + en) + [0] * (lt + et - ln - en)
            rnd.shuffle(marks)
            sim.append((sum(marks[:lt]), lt, sum(marks[lt:]), et))
        hit += stat(sim) >= real - 1e-12
    return real, (hit + 1.0) / (PERMS + 1)


def verdict(a, b):
    if a is None or b is None:
        return 'NOT TESTABLE'
    return 'HOLDS' if a and b else ('SPLIT' if a or b else 'FAILS')


def report():
    T, J = table(), judged()
    out = ['# FailedHeroRun.txt -- failedHero.py: FailedHero/FailedHeroProtocol.md (frozen 2026-10-28), every figure per transcriber',
           '# the hero: the judged hero, the myths by the hero-sphere rule (not tested); late: the last third of the functions']
    M = {}
    for g in CORPORA:
        for L in 'AB':
            ps = per_story(L, g, T, J)
            M[(g, L)] = ps
            ms = [x[3] for x in ps if x[3]]
            pun = [m[3] for m in ms if m[3] is not None]
            comp = [m[0] and (m[3] is True or m[4]) for m in ms]
            out.append('%-12s %s: stories %3d, hero %3d (%s); fused %3d (%.0f%%); hero\'s functions negative, late %d/%d (%.1f%%), early %d/%d (%.1f%%); '
                       'late U %3d, punished the hero %3d (%.0f%%); frame open %3d (%.0f%%); failed by Propp\'s apparatus %3d (%.0f%%)'
                       % (NAMES[g], L, len(ps), len(ms), 'hero-sphere rule' if g == 'myth' else 'judged', sum(m[0] for m in ms), 100 * share([m[0] for m in ms]),
                          sum(m[1][0] for m in ms), sum(m[1][1] for m in ms), 100 * pooled(ms, 1), sum(m[2][0] for m in ms), sum(m[2][1] for m in ms), 100 * pooled(ms, 2),
                          len(pun), sum(pun), 100 * share(pun), sum(m[4] for m in ms), 100 * share([m[4] for m in ms]), sum(comp), 100 * share(comp)))
            miss = collections.Counter(x[2] for x in ps if not x[1])
            if miss:
                out.append('             %s: no hero: %s' % (L, ', '.join('%s %d' % kv for kv in sorted(miss.items()))))
    # negative marks by function, reported
    for g in CORPORA:
        for L in 'AB':
            c = collections.Counter(e[1] + '-' for n, ents in stories(L, g).values() for e in ents if e[2])
            out.append('negative marks, %-12s %s: %s' % (NAMES[g], L, ', '.join('%s %d' % kv for kv in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))) or 'none'))
    # the plays whose two heroes the readers divided
    for s in ('P01', 'P04', 'P06', 'P08'):
        for L in 'AB':
            x = [y for y in M[('tragedy', L)] if y[0] == s][0]
            out.append('divided play %s, %s: judged hero %s; %s' % (s, L, x[1] or '(%s)' % x[2],
                       'fused %s, punished %s, frame open %s' % (x[3][0], x[3][3], x[3][4]) if x[3] else 'not measured'))
    # beside the hero study's failed hero (Heroes/WithJudgedHeroes.txt)
    hs = {}
    for l in open(os.path.join(ROOT, 'Heroes', 'WithJudgedHeroes.txt'), encoding='utf-8'):
        w = l.split()
        if len(w) > 2 and w[0] == 'tragedy' and w[1] in ('A:', 'B:') and 'never undone' in l:
            hs[w[1][0]] = {x for x in w if x.startswith('P') and x[1:].isdigit()}
    for L in 'AB':
        mine = {s for s, h, how, m in M[('tragedy', L)] if m and m[0] and (m[3] is True or m[4])}
        theirs = hs.get(L, set())
        out.append('the failed hero beside the hero study, tragedies %s: by Propp\'s apparatus %d, by the hero study %d, both %d (%s), the hero study\'s only %s'
                   % (L, len(mine), len(theirs), len(mine & theirs), ' '.join(sorted(mine & theirs)) or 'none', ' '.join(sorted(theirs - mine)) or 'none'))
    # the predictions
    out.append('')
    out.append('== predictions (FailedHeroProtocol.md section 5): permutation test, %d permutations, p at most 0.05; floor %d stories a side' % (PERMS, FLOOR))
    held = {1: {}, 2: {}, 3: {}}
    diff = lambda a, b: share(a) - share(b)
    for L in 'AB':
        t = [m[0] for s, h, how, m in M[('tragedy', L)] if m]
        res = []
        for g in ('tale', 'animal', 'fable'):
            o = [m[0] for s, h, how, m in M[(g, L)] if m]
            if len(t) < FLOOR or len(o) < FLOOR:
                res.append(None)
                out.append('  1. %s: tragedies %.0f%% against %s %.0f%%: NOT TESTABLE (floor)' % (L, 100 * share(t), NAMES[g], 100 * share(o)))
                continue
            d, p = perm_p(t, o, diff)
            res.append(d > 0 and p <= 0.05)
            out.append('  1. %s: fused, tragedies %.0f%% (%d) against %s %.0f%% (%d): difference %+.0f points, p %.4f: %s'
                       % (L, 100 * share(t), len(t), NAMES[g], 100 * share(o), len(o), 100 * d, p, 'holds' if res[-1] else 'does not hold'))
        held[1][L] = None if None in res else all(res)
        tm = [m for s, h, how, m in M[('tragedy', L)] if m]
        a_units = [m for m in tm if m[1][1] and m[2][1]]
        wm = [m for s, h, how, m in M[('tale', L)] if m]
        tl = [m for m in tm if m[1][1]]
        wl = [m for m in wm if m[1][1]]
        if len(a_units) < FLOOR or len(tl) < FLOOR or len(wl) < FLOOR:
            held[2][L] = None
            out.append('  2. %s: NOT TESTABLE (floor): tragedies with hero functions early and late %d, late %d; wondertales late %d' % (L, len(a_units), len(tl), len(wl)))
        else:
            da, pa = within_p(a_units)
            stat = lambda xs, ys: pooled(xs, 1) - pooled(ys, 1)
            db, pb = perm_p(tl, wl, stat)
            ok_a, ok_b = da > 0 and pa <= 0.05, db > 0 and pb <= 0.05
            held[2][L] = ok_a and ok_b
            out.append('  2. %s: tragic hero negative late %.1f%% against early %.1f%% (%d plays), p %.4f: %s; late, tragedies %.1f%% against wondertales %.1f%% (%d and %d), p %.4f: %s'
                       % (L, 100 * pooled(a_units, 1), 100 * pooled(a_units, 2), len(a_units), pa, 'holds' if ok_a else 'does not hold',
                          100 * pooled(tl, 1), 100 * pooled(wl, 1), len(tl), len(wl), pb, 'holds' if ok_b else 'does not hold'))
        tp = [m[3] for m in tm if m[3] is not None]
        wp = [m[3] for m in wm if m[3] is not None]
        if len(tp) < FLOOR or len(wp) < FLOOR:
            held[3][L] = None
            out.append('  3. %s: NOT TESTABLE (floor): tragedies with a late U %d, wondertales %d' % (L, len(tp), len(wp)))
        else:
            d, p = perm_p(tp, wp, diff)
            held[3][L] = d > 0 and p <= 0.05
            out.append('  3. %s: the late punishment falls on the hero, tragedies %.0f%% (%d) against wondertales %.0f%% (%d): difference %+.0f points, p %.4f: %s'
                       % (L, 100 * share(tp), len(tp), 100 * share(wp), len(wp), 100 * d, p, 'holds' if held[3][L] else 'does not hold'))
    out.append('  1. fusion higher in the tragedies than in the wondertales, animal tales and fables (a replication): %s' % verdict(held[1]['A'], held[1]['B']))
    out.append('  2. the tragic hero\'s late functions negative more than the early, and more than the wondertale hero\'s: %s' % verdict(held[2]['A'], held[2]['B']))
    out.append('  3. the late punishment falls on the hero in more tragedies than wondertales: %s' % verdict(held[3]['A'], held[3]['B']))
    return '\n'.join(out) + '\n'


MENDED = os.path.join(HERE, 'FailedHeroRun-mended.txt')


def run(mended=False):
    text = report()
    if mended:
        text = ('# FailedHeroRun-mended.txt -- the same run after the mend of 2026-10-28 (KeeperLog): a judged-hero entry marked "no single '
                'hero" gives no hero; reported beside the record FailedHeroRun.txt, not replacing it\n') + text
    elif os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        # FailedHeroRun.txt is the run of record: a run that would change it is refused
        raise SystemExit('refusing to overwrite the record %s; use run --mended' % OUT)
    open(MENDED if mended else OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4, 'dry': dry, 'run': run}
    a = sys.argv[1:]
    if a == ['run', '--mended']:
        run(mended=True)
        sys.exit(0)
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
