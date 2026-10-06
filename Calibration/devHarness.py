#!/usr/bin/env python3
"""
devHarness.py -- development of the improvement test (ImproveProtocol.md):
scores candidate transforms on the 22 development tales only. Refuses to
read the test tales.

  python devHarness.py
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compare as C  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'Afanasyev')
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(HERE, 'Split.txt'), encoding='utf-8') if '|' in l}
DEV = SPLIT['dev']
READINGS = [(a, L) for a in C.ARMS for L in C.LINEAGES]


def entries():
    out = {}
    for a, L in READINGS:
        e = C.load(REPO, a, L)
        out[a, L] = {t: e.get(t, []) for t in DEV}
    return out


def kept_keys(x):
    return [k for k in C.TS.key(x['sym']) if k in C.VOCAB] if C.TS.kept(x, 'primary') else []


def by_event(es):
    """[(event, [keys])] in event order, entries within an event in note order."""
    ev = collections.OrderedDict()
    for x in sorted(es, key=lambda x: (x['ev'] or 0, x['line'])):
        ks = kept_keys(x)
        if ks:
            ev.setdefault(x['ev'], []).extend(ks)
    return list(ev.items())


# ---- transforms on a flat stream --------------------------------------
def collapse_cycles(s, maxk=4):
    """an immediately repeated run of k symbols (k <= maxk) is written once."""
    s = list(s)
    changed = True
    while changed:
        changed = False
        for k in range(1, maxk + 1):
            i = 0
            out = []
            while i < len(s):
                if i + 2 * k <= len(s) and s[i:i + k] == s[i + k:i + 2 * k]:
                    j = i + k
                    while j + k <= len(s) and s[j:j + k] == s[i:i + k]:
                        j += k
                    out += s[i:i + k]
                    i = j
                    changed = True
                else:
                    out.append(s[i])
                    i += 1
            s = out
    return s


def implicit_c(s):
    """C written before a departure that follows a villainy, lack or mediation with no C between."""
    out, open_ = [], False
    for k in s:
        if k in ('A', 'a', 'B'):
            open_ = True
        if k == 'C':
            open_ = False
        if k == 'up' and open_:
            out.append('C')
            open_ = False
        out.append(k)
    return out


def score(streams, label):
    P = C.propp()
    c = C.mean(C.dice(streams[t], P[t][0]) for t in DEV)
    o = C.mean(C.order(streams[t], P[t][0]) for t in DEV)
    D = C.derangements(len(DEV), 200, 46)
    bc = C.mean(C.mean(C.dice(streams[DEV[i]], P[DEV[p[i]]][0]) for i in range(len(DEV))) for p in D)
    bo = C.mean(C.mean(C.order(streams[DEV[i]], P[DEV[p[i]]][0]) for i in range(len(DEV))) for p in D)
    n = sum(len(streams[t]) for t in DEV)
    print('%-44s len %4d  content %.3f (cc %.2f)  order %.3f (cc %.2f)'
          % (label, n, c, (c - bc) / (1 - bc), o, (o - bo) / (1 - bo)))
    return c, o


def consensus(E, k):
    out = {}
    for t in DEV:
        per = {}
        for r in READINGS:
            for ev, ks in by_event(E[r][t]):
                per.setdefault(ev, []).append(collections.Counter(ks))
        s = []
        for ev in sorted(per, key=lambda v: v or 0):
            cs = per[ev]
            first = []
            for cnt in cs:
                for key in cnt:
                    if key not in first:
                        first.append(key)
            for key in first:
                votes = sum(1 for cnt in cs if key in cnt)
                if votes >= k:
                    m = sorted((cnt[key] for cnt in cs if key in cnt), reverse=True)[k - 1]
                    s += [key] * m
        out[t] = s
    return out


def main():
    E = entries()
    P = C.propp()
    print('Propp, dev tales: %d symbols' % sum(len(P[t][0]) for t in DEV))
    for r in READINGS:
        notes = {t: [k for x in sorted(E[r][t], key=lambda x: x['line']) for k in kept_keys(x)] for t in DEV}
        evord = {t: [k for _, ks in by_event(E[r][t]) for k in ks] for t in DEV}
        print('--- %s/%s' % r)
        score(notes, 'as written (note order)')
        score(evord, 'event order')
        score({t: collapse_cycles(notes[t], 1) for t in DEV}, 'collapse repeats k=1')
        score({t: collapse_cycles(notes[t]) for t in DEV}, 'collapse cycles k<=4')
        score({t: implicit_c(notes[t]) for t in DEV}, 'implicit C')
        score({t: implicit_c(collapse_cycles(notes[t])) for t in DEV}, 'cycles + implicit C')
    print('--- consensus of the four readings')
    for k in (1, 2, 3, 4):
        cs = consensus(E, k)
        score(cs, 'consensus >= %d of 4' % k)
        score({t: implicit_c(collapse_cycles(cs[t])) for t in DEV}, '  + cycles + implicit C')


if __name__ == '__main__':
    main()
