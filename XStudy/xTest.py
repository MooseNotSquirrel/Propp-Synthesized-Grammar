#!/usr/bin/env python3
"""
xTest.py -- the X study's stage 5 verdicts (XStudyProtocol.md), written before
any test transcription existed.

  python xTest.py      writes XStudy/TestRun.txt

Per event (a story's event number, all hero versions together), each
transcriber's set of symbols: candidate acts by their symbols, Propp's
functions by their base symbols, X left out.
A candidate HOLDS if:
  1. its agreement, events where both transcribers write it / events where
     either does, is at least the pooled agreement on Propp's functions in the
     same stories (the sum over functions of events where both write the
     function, over the sum of events where either does);
  2. at least 75% of the events where either writes it were left X by both
     transcribers in the original transcriptions; and
  3. either transcriber writes it in at least two genres.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARENT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

XT = os.path.join(PARENT, 'XStudy', 'test')
CANDS = [l.split('|')[1].strip() for l in open(os.path.join(HERE, 'Candidates.md'), encoding='utf-8')
         if l.startswith('| x')]
GENRES = ('tale', 'fable', 'tragedy')
ORIGINAL = {'tale': ('Afanasyev/transcriptions/U/%s/b*/Notes.txt',),
            'fable': ('Fables/transcriptions/%s/b*/Notes.txt',),
            'tragedy': ('Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt',)}


def symbols(paths):
    """{(story, event): set of symbols}"""
    out = collections.defaultdict(set)
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            if not ev:
                continue
            key = (f[0].split('/')[0], int(ev.group()))
            s = f[4].strip()
            out[key]  # the event exists, even if X
            if s in CANDS:
                out[key].add(s)
            elif TS.base(s) != 'X':
                out[key].add(TS.base(s))
    return out


def main():
    new, orig = {}, {}
    for g in GENRES:
        for L in 'AB':
            new[g, L] = symbols(sorted(glob.glob(os.path.join(XT, g, 'transcriptions', L, 't*', 'Notes.txt'))))
            orig[g, L] = symbols(sorted(glob.glob(os.path.join(PARENT, ORIGINAL[g][0] % L))))
    both = collections.Counter()
    either = collections.Counter()
    genres_used = collections.defaultdict(set)
    on_x = collections.Counter()
    for g in GENRES:
        A, B = new[g, 'A'], new[g, 'B']
        stories = {k[0] for k in A} & {k[0] for k in B}
        for e in set(A) | set(B):
            if e[0] not in stories:
                continue
            sa, sb = A.get(e, set()), B.get(e, set())
            for s in sa | sb:
                either[s] += 1
                both[s] += s in sa and s in sb
                if s in CANDS:
                    genres_used[s].add(g)
                    oa, ob = orig[g, 'A'].get(e), orig[g, 'B'].get(e)
                    on_x[s] += oa is not None and ob is not None and not oa and not ob
    propp = [s for s in either if s not in CANDS]
    pooled = sum(both[s] for s in propp) / float(sum(either[s] for s in propp) or 1)
    rep = ['# TestRun.txt -- xTest.py, stage 5 of XStudyProtocol.md.', '',
           'Agreement on Propp\'s functions, pooled over the test stories: %.3f' % pooled, '',
           '%-6s %7s %7s %10s %12s %8s  %s' % ('act', 'either', 'both', 'agreement', 'on X events', 'genres', 'verdict')]
    held = []
    for c in CANDS:
        ag = both[c] / float(either[c]) if either[c] else 0.0
        share = on_x[c] / float(either[c]) if either[c] else 0.0
        ok1, ok2, ok3 = either[c] > 0 and ag >= pooled, either[c] > 0 and share >= 0.75, len(genres_used[c]) >= 2
        v = 'HOLDS' if ok1 and ok2 and ok3 else 'fails: ' + ', '.join(
            x for x, bad in (('agreement', not ok1), ('takes Propp\'s events', not ok2), ('one genre', not ok3)) if bad)
        if v == 'HOLDS':
            held.append(c)
        rep.append('%-6s %7d %7d %10.3f %11.0f%% %8d  %s' % (c, either[c], both[c], ag, 100 * share, len(genres_used[c]), v))
    rep += ['', 'HOLD: %d of %d: %s' % (len(held), len(CANDS), ', '.join(held) or 'none')]
    open(os.path.join(HERE, 'TestRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    sys.exit(main())
