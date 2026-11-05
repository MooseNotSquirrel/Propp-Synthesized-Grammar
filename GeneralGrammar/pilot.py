"""pilot.py -- the measure of CardPilotProtocol.md. Reads coded files, maps cell S back by the key, reports by the frozen reading.
Primary: mean-position tau with Propp's numbering, no preparatory units, functions in at least 3 stories.
Usage: python pilot.py <corpus> <H folder> <S folder>; each folder holds A/ and B/, with Streams.txt and Notes.txt."""
import collections
import json
import os
import sys

import numpy as np
from scipy.stats import kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = set('βγδεζηθλ')
MINUS = '−'
SYM = {'↑': 'up', '↓': 'down'}


def norm(sym):
    s = sym.strip().rstrip(MINUS)
    return SYM.get(s, s)


def parse_notes(path, code=None, tales=None):
    """{story: {event: [function]}} in file order, each story's first version; X kept. code: S's code -> symbol; tales: S's id -> id"""
    out = collections.OrderedDict()
    for line in open(path, encoding='utf-8'):
        p = [x.strip() for x in line.split(' | ')]
        if len(p) < 5 or not p[3].startswith('ev'):
            continue
        t, ver = p[0], ''
        if '/' in t:
            t, ver = t.split('/', 1)
        if ver not in ('', '1'):
            continue
        if tales:
            t = tales.get(t, t)
        try:
            e = int(p[3].split()[1])
        except (IndexError, ValueError):
            continue
        s = p[4].rstrip(MINUS).strip()
        if code is not None and s != 'X':
            s = code.get(s, '?' + s)
        out.setdefault(t, collections.OrderedDict()).setdefault(e, []).append(norm(s))
    return out


def strings_of(notes, num):
    """units per story, in event order, no X, no preparatory units"""
    out = {}
    for t, ev in notes.items():
        x = [u for e in ev for u in ev[e] if u in num and u not in PREP]
        if len(x) >= 2:
            out[t] = x
    return out


def places(strs):
    t, n, st = collections.Counter(), collections.Counter(), collections.Counter()
    for x in strs:
        for u in set(x):
            st[u] += 1
        for i, u in enumerate(x):
            t[u] += i / (len(x) - 1)
            n[u] += 1
    return {u: t[u] / n[u] for u in n}, st


def tau(strs, num, only=None, minn=3):
    pl, st = places(strs)
    fs = [u for u in pl if st[u] >= minn and (only is None or u in only)]
    if len(fs) < 4:
        return float('nan'), len(fs)
    return float(kendalltau([pl[u] for u in fs], [num[u] for u in fs])[0]), len(fs)


def paired(H, S, num, draws=2000, seed=20261104):
    """H minus S on the functions both cells have, and its 90% interval by paired bootstrap of tales"""
    ks = sorted(set(H) & set(S))
    _, sh = places([H[k] for k in ks])
    _, ss = places([S[k] for k in ks])
    both = {u for u in sh if sh[u] >= 3 and ss.get(u, 0) >= 3}
    base = tau([H[k] for k in ks], num, both)[0] - tau([S[k] for k in ks], num, both)[0]
    rng = np.random.default_rng(seed)
    v = []
    for _ in range(draws):
        pick = rng.integers(0, len(ks), len(ks))
        a = tau([H[ks[i]] for i in pick], num, both)[0]
        b = tau([S[ks[i]] for i in pick], num, both)[0]
        if a == a and b == b:
            v.append(a - b)
    return base, float(np.percentile(v, 5)), float(np.percentile(v, 95)), len(both)


def primary(ls):
    for x in ls:
        if x != 'X':
            return x
    return 'X'


def kappa(a, b):
    xs, ys = [], []
    for t in set(a) & set(b):
        for e in set(a[t]) & set(b[t]):
            xs.append(primary(a[t][e]))
            ys.append(primary(b[t][e]))
    n = len(xs)
    if not n:
        return float('nan'), 0
    po = sum(x == y for x, y in zip(xs, ys)) / n
    pe = sum(xs.count(k) / n * ys.count(k) / n for k in set(xs) | set(ys))
    return (po - pe) / (1 - pe), n


def covered(notes):
    v = [primary(ls) != 'X' for ev in notes.values() for ls in ev.values()]
    return float(np.mean(v)) if v else float('nan')


def cosine(a, b):
    ks = set(a) | set(b)
    x = np.array([a.get(k, 0) for k in ks], float)
    y = np.array([b.get(k, 0) for k in ks], float)
    return float(x @ y / np.linalg.norm(x) / np.linalg.norm(y)) if x.any() and y.any() else float('nan')


def reading(h, s, d, lo, hi, kh, ks, ch=None, cs=None):
    """the frozen reading of section 5, for one corpus and reader"""
    if ks < kh - 0.10 or (ch is not None and cs is not None and cs < ch - 0.10):
        return 'UNREADABLE'
    if s >= 0.5 and abs(h - s) <= 0.10:
        return 'SURVIVES'
    if d >= 0.30 and lo > 0:
        return 'WRITTEN IN'
    return 'IN PART'


def report(corpus, hdir, sdir, num, propp=None):
    key = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    code = {v: k for k, v in key['symbols'].items()}
    code = {c: norm(s) for c, s in code.items()}
    tales = {v: k for k, v in key['tales'][corpus].items()}
    out = ['# Pilot-%s.txt -- CardPilotProtocol.md, the frozen reading' % corpus]
    H = {r: parse_notes(os.path.join(hdir, r, 'Notes.txt')) for r in 'AB'}
    S = {r: parse_notes(os.path.join(sdir, r, 'Notes.txt'), code, tales) for r in 'AB'}
    kh, ks = kappa(H['A'], H['B'])[0], kappa(S['A'], S['B'])[0]
    out.append('kappa A with B: H %.3f, S %.3f; given a function: H %.3f %.3f, S %.3f %.3f' % (kh, ks, covered(H['A']), covered(H['B']), covered(S['A']), covered(S['B'])))
    bad = sorted({u for r in 'AB' for ev in S[r].values() for ls in ev.values() for u in ls if u.startswith('?')})
    out.append('codes not on the card: %s' % (bad or 'none'))
    for r in 'AB':
        hs, ss = strings_of(H[r], num), strings_of(S[r], num)
        d, lo, hi, n = paired(hs, ss, num)
        th = tau(list(hs.values()), num)
        ts = tau(list(ss.values()), num)
        ch = cs = None
        if propp:
            bag = lambda x: collections.Counter(x)
            ch = float(np.nanmean([cosine(bag(hs[t]), propp[t]) for t in hs if t in propp]))
            cs = float(np.nanmean([cosine(bag(ss[t]), propp[t]) for t in ss if t in propp]))
        out.append('%s: tau H %.3f (%d), S %.3f (%d); H minus S on %d shared functions %.3f [%.3f, %.3f]%s: %s' % (r, th[0], th[1], ts[0], ts[1], n, d, lo, hi, '; cosine with his strings H %.3f, S %.3f' % (ch, cs) if propp else '', reading(th[0], ts[0], d, lo, hi, kh, ks, ch, cs)))
    return out


def old_notes(corpus_story, reader, tales):
    """the old strings of the same tales (card C, tables), as a third figure"""
    import csv
    csv.field_size_limit(10 ** 9)
    out = collections.OrderedDict()
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Induction'))
    import strings as ST
    TS = ST.TS
    for r in csv.DictReader(open(os.path.join(os.path.dirname(HERE), 'Data/tables/functions.tsv'), encoding='utf-8', newline=''), delimiter='\t', quoting=csv.QUOTE_NONE):
        c, _, t = r['story'].partition(':')
        if c != corpus_story or r['card'] != 'C' or r['reader'] != reader or t not in tales or r['version'] not in ('', '1'):
            continue
        try:
            e = int(r['event'])
        except ValueError:
            continue
        ks = ['X'] if r['function'] == 'X' else [k for k in TS.key(r['function']) if k in TS.NUM]
        out.setdefault(t, collections.OrderedDict()).setdefault(e, []).extend(ks)
    return out


def with_prep(notes, num):
    out = {}
    for t, ev in notes.items():
        x = [u for e in ev for u in ev[e] if u in num]
        if len(x) >= 2:
            out[t] = x
    return out


def adjacent_pairs(strs, pairs):
    """his pairs seen adjacent in at least 2 stories"""
    n = collections.Counter()
    for x in strs:
        for p in set(zip(x, x[1:])):
            n[p] += 1
    live = [p for p in pairs if n[p] >= 1]
    return sorted('%s-%s' % p for p in pairs if n[p] >= 2), len(live)


def extra(corpus_story, H, S, num, pairs, tales):
    """beside the reading, not deciding"""
    import grammar as G
    out = ['## beside the reading, not deciding']
    for r in 'AB':
        O = old_notes(corpus_story, r, tales)
        os_, hs, ss = strings_of(O, num), strings_of(H[r], num), strings_of(S[r], num)
        out.append('%s: tau on the old strings of these tales %.3f (%d); given a function, old %.3f' % (r, *tau(list(os_.values()), num), covered(O)))
        hp, sp = with_prep(H[r], num), with_prep(S[r], num)
        out.append('%s: with preparatory units: H %.3f (%d), S %.3f (%d)' % (r, *tau(list(hp.values()), num), *tau(list(sp.values()), num)))
        for lab, x in (('H', hp), ('S', sp)):
            f = G.fit(list(x.values()), boots=200)
            ot = None
            seen = [u for u in f['order'] if u in num and u not in PREP]
            ot = kendalltau(range(len(seen)), [num[u] for u in seen])[0] if len(seen) > 3 else float('nan')
            ap, _ = adjacent_pairs(list(x.values()), pairs)
            out.append('%s %s: tool (15 stories, below its tested 20): %s, coverage %.2f, order tau %.3f; his pairs adjacent in 2 stories or more: %s' % (r, lab, f['shape'], f['coverage'], ot, ' '.join(ap)))
        out.append('%s: units per story: old %.1f, H %.1f, S %.1f' % (r, np.mean([len(v) for v in os_.values()]), np.mean([len(v) for v in hs.values()]), np.mean([len(v) for v in ss.values()])))
    return out


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    import score as C
    slots, pairs = C.propp()
    num = C.numbering(slots)
    corpus, hdir, sdir = sys.argv[1:4]
    key = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    propp = None
    story = {'wonder': 'tale', 'east': 'eastasian'}[corpus]
    if corpus == 'wonder':
        import leaves as L
        d = L.load()
        propp = {}
        for s, b in d['propp'].items():
            t = s.split(':', 1)[1]
            propp[t] = collections.Counter({k: v for k, v in b.items() if k not in PREP})
    lines = report(corpus, hdir, sdir, num, propp)
    code = {c: norm(s) for s, c in key['symbols'].items()}
    tales = {v: k for k, v in key['tales'][corpus].items()}
    H = {r: parse_notes(os.path.join(hdir, r, 'Notes.txt')) for r in 'AB'}
    S = {r: parse_notes(os.path.join(sdir, r, 'Notes.txt'), code, tales) for r in 'AB'}
    lines += extra(story, H, S, num, pairs, set(key['tales'][corpus]))
    open(os.path.join(HERE, 'Pilot-%s.txt' % corpus), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
