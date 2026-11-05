"""shuffleNoise.py -- for ShuffledProtocol.md, from existing strings only. How much order is lost through worse coding alone?
Each event's label is replaced at rate p by a draw from the same reader's labels; the tau falls with p though the sequence is untouched.
Also: how well two whole-tale codings of one reader agree (the top of what a shuffled coding could reach), and the event counts."""
import collections
import json
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pilot as P  # noqa: E402
import score as C  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(HERE))
TC = 'C:/Users/Steve1/TaleCoding'
OUT = []


def say(s):
    OUT.append(s)
    print(s)


key = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
slots, _ = C.propp()
num = C.numbering(slots)
code = {c: P.norm(s) for s, c in key['symbols'].items()}
say('# ShuffleNoise.txt -- existing strings only')
for name in ('wonder', 'east'):
    ev = open(os.path.join(TC, name, 'Events.txt'), encoding='utf-8').read().splitlines()
    by = collections.Counter(l.split(' | ')[0] for l in ev)
    words = np.mean([len(l.split(' | ', 2)[2].split()) for l in ev])
    say('%s: %d events in %d tales; per tale %d to %d; %.1f words an event' % (name, len(ev), len(by), min(by.values()), max(by.values()), words))
stories = {'wonder': 'tale', 'east': 'eastasian'}
rng = random.Random(20261104)
say('## tau with his order (no preparatory units), when labels are replaced at rate p; 300 draws of the replacement')
for name in ('wonder', 'east'):
    tales = set(key['tales'][name])
    for r in 'AB':
        O = P.old_notes(stories[name], r, tales)
        pool = [P.primary(ls) for t in O.values() for ls in t.values()]
        cells = []
        for p in (0, .2, .4, .6, .8):
            ts = []
            for _ in range(300 if p else 1):
                strs = []
                for t in O.values():
                    x = []
                    for ls in t.values():
                        u = P.primary(ls)
                        if rng.random() < p:
                            u = rng.choice(pool)
                        if u in num and u not in P.PREP:
                            x.append(u)
                    if len(x) >= 2:
                        strs.append(x)
                ts.append(P.tau(strs, num)[0])
            ts = [a for a in ts if a == a]
            cells.append('p %.1f: %.2f [%.2f, %.2f]' % (p, np.mean(ts), np.percentile(ts, 5), np.percentile(ts, 95)))
        say('%-6s %s  %s' % (name, r, '  '.join(cells)))
say('## two whole-tale codings of the same 15 wondertales: kappa, event by event')
tales = {v: k for k, v in key['tales']['wonder'].items()}
H, S, O = {}, {}, {}
for r in 'AB':
    H[r] = P.parse_notes(os.path.join(PROJ, 'Afanasyev/transcriptions/PilotH', r, 'Notes.txt'))
    S[r] = P.parse_notes(os.path.join(TC, 'wonder/coded', r, 'Notes.txt'), code, tales)
    O[r] = P.old_notes('tale', r, set(key['tales']['wonder']))
    say('reader %s: H with S %.3f; old with H %.3f; old with S %.3f' % (r, P.kappa(H[r], S[r])[0], P.kappa(O[r], H[r])[0], P.kappa(O[r], S[r])[0]))
say('A with B: H %.3f; S %.3f; A under H with B under S %.3f' % (P.kappa(H['A'], H['B'])[0], P.kappa(S['A'], S['B'])[0], P.kappa(H['A'], S['B'])[0]))
open(os.path.join(HERE, 'ShuffleNoise.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')
