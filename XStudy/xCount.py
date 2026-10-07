#!/usr/bin/env python3
"""
xCount.py -- the X study's stage 4 (XStudyProtocol.md): which kinds become
candidate functions.

  python xCount.py     writes XStudy/CountRun.txt

A kind is a CANDIDATE if (1) the two assigners agree on at least 10 events in
it; (2) those events come from at least two genres, at least 3 in each; and
(3) in at least half of them an original transcription linked the event to
another (Targets.txt). Reported beside it: the assigners' agreement overall,
and every kind's counts.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
X = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'XStudy')
GENRES = ('wondertale', 'fable', 'tragedy')


def assigned(L):
    out = {}
    for b in ('b1', 'b2', 'b3', 'b4'):
        for l in open(os.path.join(X, 'assign', L, b, 'Assign.txt'), encoding='utf-8'):
            f = [x.strip() for x in l.split('|', 2)]
            if len(f) == 3 and f[1].isdigit():
                out[(f[0], int(f[1]))] = f[2] if f[2].lower() != 'none' else None
    return out


def main():
    info = {}
    for l in open(os.path.join(HERE, 'Targets.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|')]
        if len(f) == 5 and f[1].isdigit() and f[3] == 'discovery':
            info[(f[0], int(f[1]))] = (f[2], f[4] == 'link')
    kinds = [l.split('|')[0].strip() for l in open(os.path.join(X, 'group', 'Kinds.txt'), encoding='utf-8') if l.strip()]
    A, B = assigned('A'), assigned('B')
    events = sorted(info)
    agree = [e for e in events if A.get(e) == B.get(e)]
    agree_kind = [e for e in agree if A[e] is not None]
    rep = ['# CountRun.txt -- xCount.py, stage 4 of XStudyProtocol.md.', '',
           'Target events: %d. The assigners agree on %d (%.0f%%), %d of them on a kind and %d on none; '
           'A puts %d in none, B %d.' % (len(events), len(agree), 100.0 * len(agree) / len(events), len(agree_kind),
                                          len(agree) - len(agree_kind), sum(A[e] is None for e in events),
                                          sum(B[e] is None for e in events)), '',
           '%-34s %5s  %s  %6s  %s' % ('kind', 'agreed', '  '.join('%-10s' % g for g in GENRES), 'linked', 'verdict')]
    cands = []
    for k in kinds:
        ev = [e for e in agree_kind if A[e] == k]
        by = collections.Counter(info[e][0] for e in ev)
        linked = sum(info[e][1] for e in ev)
        c1 = len(ev) >= 10
        c2 = sum(1 for g in GENRES if by[g] >= 3) >= 2
        c3 = len(ev) > 0 and linked >= len(ev) / 2.0
        ok = c1 and c2 and c3
        if ok:
            cands.append(k)
        why = 'CANDIDATE' if ok else 'no: ' + ', '.join(x for x, bad in (('under 10', not c1), ('one genre', not c2),
                                                                         ('few links', not c3)) if bad)
        rep.append('%-34s %5d  %s  %3d/%-3d  %s' % (k[:34], len(ev), '  '.join('%-10d' % by[g] for g in GENRES),
                                                   linked, len(ev), why))
    rep += ['', 'CANDIDATES: %d: %s' % (len(cands), '; '.join(cands) if cands else 'none')]
    open(os.path.join(HERE, 'CountRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    sys.exit(main())
