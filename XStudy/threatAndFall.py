#!/usr/bin/env python3
"""
threatAndFall.py -- two explorations after the X study, 2026-10-12, not frozen.

  python threatAndFall.py     writes XStudy/ThreatAndFall.txt

1. What precedes and follows a threat (xThr) in the stage 5 transcriptions,
   against 200 shuffles of each story's functions (seed 46).
2. The owner's FailedHero: stories in which the hero succeeds (I, K, W or N,
   the hero performing or undergoing), and then (a) is exposed or punished
   (Ex, U on the hero) or defeated (I-), or (b) suffers a villainy (A on the
   hero) that no later liquidation (K) undoes. The hero is the event lists'
   hero; a name matches by its first word, a crude test.
"""
import collections
import glob
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
sys.path.insert(0, HERE)
import tragedyScore as TS  # noqa: E402
import xTest as T  # noqa: E402

OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def entries(paths):
    st = collections.OrderedDict()
    for p in paths:
        for l in open(p, encoding='utf-8'):
            f = [x.strip() for x in l.split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]) or f[7][:1].upper() != 'Y':
                continue
            st.setdefault(f[0], []).append((f[4], f[5], f[6]))
    return st


def threats():
    say('1. THREATS (stage 5 transcriptions, functions and candidate acts marked Y)')
    for L in 'AB':
        S = []
        for g in T.GENRES:
            for ents in entries(sorted(glob.glob(os.path.join(T.XT, g, 'transcriptions', L, 't*', 'Notes.txt')))).values():
                s = [e[0] if e[0] in T.CANDS else TS.base(e[0]) for e in ents]
                S.append([k for k in s if k != 'X'])
        nxt, prv, n = collections.Counter(), collections.Counter(), 0
        for s in S:
            for i, k in enumerate(s):
                if k == 'xThr':
                    n += 1
                    if i + 1 < len(s):
                        nxt[s[i + 1]] += 1
                    if i:
                        prv[s[i - 1]] += 1
        rng, sh = random.Random(46), collections.Counter()
        for _ in range(200):
            for s in S:
                t = s[:]
                rng.shuffle(t)
                for i, k in enumerate(t):
                    if k == 'xThr' and i + 1 < len(t):
                        sh[t[i + 1]] += 1
        say('  transcriber %s, %d threats' % (L, n))
        say('    followed by: ' + ', '.join('%s %d (chance %.1f)' % (k, c, sh[k] / 200.0) for k, c in nxt.most_common(8)))
        say('    preceded by: ' + ', '.join('%s %d' % kv for kv in prv.most_common(5)))


def heroes(paths):
    h = {}
    for path in paths:
        for l in open(path, encoding='utf-8'):
            if '|' in l:
                s, rest = l.split('|', 1)
                h[s.strip()] = [x.strip() for x in rest.replace('hero:', '').split(';') if x.strip()]
    return h


def failed_hero():
    say('')
    say('2. THE FAILED HERO')
    th = heroes(glob.glob(os.path.join(P, 'Tragedy', 'plays', 'P*', 'Hero.txt')))
    ah = heroes([os.path.join(P, 'Afanasyev', 'Heroes.txt')])
    for L in 'AB':
        for label, pat, hmap in (('tragedy', os.path.join(P, 'Tragedy', 'transcriptions', L, 'P[0-9][0-9]', 'Notes.txt'), th),
                                 ('Russian tales', os.path.join(P, 'Afanasyev', 'transcriptions', 'U', L, 'b*', 'Notes.txt'), ah)):
            n = won = fa = fb = 0
            exa, exb = set(), set()
            for v, ents in entries(sorted(glob.glob(pat))).items():
                hs = hmap.get(v.split('/')[0], [])
                k = int(v.split('/')[1]) - 1 if '/' in v else 0
                hero = (hs[k] if k < len(hs) else (hs[0] if hs else '')).split('(')[0].strip().split()
                if not hero:
                    continue
                h = hero[0].lower()
                n += 1
                w = next((i for i, (s, p_, u) in enumerate(ents) if TS.base(s) in ('I', 'K', 'W', 'N')
                          and not TS.negative(s) and (h in p_.lower() or h in u.lower())), None)
                if w is None:
                    continue
                won += 1
                rest = ents[w + 1:]
                if any((TS.base(s) in ('Ex', 'U') and h in u.lower()) or (TS.base(s) == 'I' and TS.negative(s) and h in p_.lower())
                       for s, p_, u in rest):
                    fa += 1
                    exa.add(v.split('/')[0])
                j = next((i for i, (s, p_, u) in enumerate(rest) if TS.base(s) == 'A' and h in u.lower()), None)
                if j is not None and not any(TS.base(s) == 'K' for s, _, _ in rest[j + 1:]):
                    fb += 1
                    exb.add(v.split('/')[0])
            say('  %s, transcriber %s: %d stories; the hero succeeds in %d; then (a) exposed, punished or defeated %d %s; '
                '(b) a villainy on the hero never undone %d %s' % (label, L, n, won, fa, ' '.join(sorted(exa)), fb, ' '.join(sorted(exb))))


if __name__ == '__main__':
    threats()
    failed_hero()
    open(os.path.join(HERE, 'ThreatAndFall.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')
