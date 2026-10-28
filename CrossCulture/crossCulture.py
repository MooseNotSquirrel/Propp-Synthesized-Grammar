#!/usr/bin/env python3
"""
crossCulture.py -- Propp's devices across cultures (CrossCulture/CrossCultureProtocol.md, frozen 2026-10-28, amended in
section 8 before any new tale was read).

  python crossCulture.py ref    write CrossCulture/Reference.txt on the existing corpora (refused if it exists)
  python crossCulture.py x1     test X1: Reference.txt reproduced exactly; single functions within a point of the first look
  python crossCulture.py x2     test X2: the block shares of the animal tales and myths equal the published counts
  python crossCulture.py x3     test X3: two runs byte-identical

The definitions are section 8's, written out there. Every figure per transcriber. The new corpora are added to CORPORA
when their tables exist; the predictions are scored by a later command, written and committed before their tales are read.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'FailedHero'))
sys.path.insert(0, os.path.join(ROOT, 'Blocks'))
import failedHero as F  # noqa: E402
import parity as BP  # noqa: E402  (changes the working directory to ROOT)
import importlib.util  # noqa: E402

C, DT, SX, TS = F.C, F.DT, F.SX, F.TS
_ng = importlib.util.spec_from_file_location('ngrams', os.path.join(ROOT, 'Ngrams', 'ngrams.py'))
NG = importlib.util.module_from_spec(_ng)
_ng.loader.exec_module(NG)
PAIRS = NG.PROPP_PAIRS
EXISTING = ['tale', 'animal', 'fable', 'myth', 'tragedy']
NAMES = dict(F.NAMES)
# the first look of 2026-10-21, single functions, the share not X (ProppQueue.md item (l))
FIRST_LOOK = {('tale', 'A'): 68, ('tale', 'B'): 78, ('animal', 'A'): 62, ('animal', 'B'): 57, ('fable', 'A'): 58, ('fable', 'B'): 57,
              ('myth', 'A'): 59, ('myth', 'B'): 70, ('tragedy', 'A'): 45, ('tragedy', 'B'): 48}
# Data/Parity/blocks-animal.txt and blocks-myth.txt, the blocks reading
PUBLISHED_BLOCKS = {('animal', 'A'): (577, 952), ('animal', 'B'): (495, 803), ('myth', 'A'): (575, 1200), ('myth', 'B'): (597, 1419)}
HELPING = ('give', 'guide', 'repair')
REF = os.path.join(HERE, 'Reference.txt')


def rows(g, L):
    return list(DT.files('functions', C.PATS[g], L))


def coverage(rs):
    fn = [TS.base(r['raw']) for r in rs]
    return sum(1 for f in fn if f != 'X'), len(fn)


def paired(rs):
    """section 8: a row is paired when its function opens one of Propp's pairs and the second follows in the same move, or
    closes one and the first precedes it; counted among the rows that are not X"""
    first, second = collections.defaultdict(set), collections.defaultdict(set)
    for a, b in PAIRS:
        first[a].add(b)
        second[b].add(a)
    seq = collections.defaultdict(list)
    for r in rs:
        seq[(r['story'], r['version'], r['move'])].append(TS.base(r['raw']))
    n = k = 0
    for fs in seq.values():
        for i, f in enumerate(fs):
            if f == 'X':
                continue
            n += 1
            k += bool(first[f] & set(fs[i + 1:])) or bool(second[f] & set(fs[:i]))
    return k, n


def blocks(g, L):
    """the functions inside blocks, the blocks reading, by blockStream.py's transform and coverage as Blocks/parity.py
    applies them"""
    if g in ('animal', 'myth'):
        vs = BP.corpus_stream(g, L)
    else:
        vs = BP.tstream(C.PATS[g], L, r'^([PFA]\d{2}|L\d-\d{3})')
    gr = BP.BS.Grammar()
    i = t = 0
    for v, items in vs.items():
        a, b = BP.BS.coverage(BP.BS.transform(items, gr, 'blocks'))
        i, t = i + a, t + b
    return i, t


def punished(rs):
    st = collections.defaultdict(list)
    for r in rs:
        st[r['story']].append(TS.base(r['raw']))
    return sum(1 for fs in st.values() if 'U' in fs), len(st)


def helping(g, L):
    """section 8: among the acts whose performer is the judged hero, those of the kind give, guide or repair whose undergoer
    is a character other than the hero"""
    A = C.act_rows()
    T, J = F.table(), F.judged()
    k = n = 0
    for s, ents in C.entries(L, g).items():
        chars = T.get((g, L, s), {})
        hero, how = F.heroes(g, L, s, chars, J)
        if hero is None or g == 'myth':
            continue
        acts = A.get((g + ':' + s, L), [])
        canon = SX.merge([e[:3] for e in ents])
        names = {x for e in ents for x in e[1:3] if x}
        links = {a: c for a, (c, _) in C.event_join(g, L, s, ents, acts).items()}

        def who(raw):
            key = SX.key(raw)
            if not key:
                return None
            c = links.get(key) if C.CYR.search(raw) else C.name_join(key, names, canon)
            return ' '.join(c) if c else None
        for r in acts:
            ps = {who(x) for x in SX.split_field(r['performer'])}
            if hero not in ps:
                continue
            n += 1
            us = {who(x) for x in SX.split_field(r['undergoer'])} - {None, hero}
            k += r['act'].lower() in HELPING and bool(us)
    return k, n


def reference():
    out = ['# Reference.txt -- crossCulture.py ref: CrossCultureProtocol.md section 8\'s definitions on the existing corpora, written '
           'before any Native American or East Asian tale was read; per transcriber']
    for g in EXISTING:
        for L in 'AB':
            rs = rows(g, L)
            c, n = coverage(rs)
            pk, pn = paired(rs)
            bi, bt = blocks(g, L)
            us, ns = punished(rs)
            hk, hn = helping(g, L)
            out.append('%-8s %s: function rows %5d; single functions %5d (%.1f%%); paired %5d of %5d (%.1f%%); inside blocks %5d of %5d (%.1f%%); '
                       'stories with U %3d of %3d (%.1f%%); the hero\'s acts helping another %4d of %4d (%.1f%%)'
                       % (g, L, n, c, 100.0 * c / n, pk, pn, 100.0 * pk / max(1, pn), bi, bt, 100.0 * bi / max(1, bt), us, ns, 100.0 * us / max(1, ns),
                          hk, hn, 100.0 * hk / max(1, hn)))
    return '\n'.join(out) + '\n'


def ref():
    if os.path.exists(REF):
        raise SystemExit('refusing to overwrite %s' % REF)
    text = reference()
    open(REF, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


def x1():
    ok = True
    if not os.path.exists(REF):
        print('X1 FAIL: Reference.txt not yet written')
        return False
    same = open(REF, encoding='utf-8').read() == reference()
    print('X1 Reference.txt reproduced exactly: %s' % ('pass' if same else 'FAIL'))
    ok &= same
    for g in EXISTING:
        for L in 'AB':
            c, n = coverage(rows(g, L))
            near = abs(100.0 * c / n - FIRST_LOOK[(g, L)]) <= 1.0
            ok &= near
            print('X1 %-8s %s single functions %.1f%% against the first look\'s %d%%: %s' % (g, L, 100.0 * c / n, FIRST_LOOK[(g, L)], 'pass' if near else 'FAIL'))
    print('X1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def x2():
    ok = True
    for (g, L), want in sorted(PUBLISHED_BLOCKS.items()):
        got = blocks(g, L)
        good = got == want
        ok &= good
        print('X2 %-6s %s inside blocks %d of %d, published %d of %d: %s' % (g, L, got[0], got[1], want[0], want[1], 'pass' if good else 'FAIL'))
    print('X2 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def x3():
    ok = reference() == reference()
    print('X3 two runs byte-identical: %s' % ('PASS' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    cmds = {'ref': ref, 'x1': x1, 'x2': x2, 'x3': x3}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
