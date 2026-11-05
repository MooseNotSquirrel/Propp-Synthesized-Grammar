"""pilotNoise.py -- how noisy is the order measure at pilot sizes? mean relative place per function, tau with Propp, no preparatory units, on the old strings"""
import sys, random, collections
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = []
def say(s):
    OUT.append(s)
    print(s)
import numpy as np
from scipy.stats import kendalltau
import leaves as L, score as C
d = L.load()
slots, _ = C.propp(); num = C.numbering(slots)
lab = d['labels']
def strings(c, r):
    out = {}
    for s, evs in d['features'][(c, r)]:
        x = [L.primary(lab[(s, r)][e['e']]) for e in evs if lab.get((s, r), {}).get(e['e'])]
        x = [u for u in x if u in num and u not in L.PREP]
        if len(x) >= 3:
            out[s] = x
    return out
def tau(strs, minn=3):
    t, n = collections.Counter(), collections.Counter()
    st = collections.Counter()
    for x in strs:
        for u in set(x):
            st[u] += 1
        for i, u in enumerate(x):
            t[u] += i / (len(x) - 1); n[u] += 1
    fs = [u for u in n if st[u] >= minn]
    if len(fs) < 4:
        return float('nan'), len(fs)
    return float(kendalltau([t[u] / n[u] for u in fs], [num[u] for u in fs])[0]), len(fs)
rng = random.Random(20261104)
for c in ('tale', 'eastasian', 'tragedy', 'native'):
    for r in 'AB':
        S = strings(c, r)
        ks = sorted(S)
        full = tau([S[k] for k in ks])
        line = '%-10s %s all %d: tau %.3f (%d functions);' % (c, r, len(ks), full[0], full[1])
        for m in (10, 15, 20, 30):
            if m >= len(ks):
                continue
            v = [tau([S[k] for k in rng.sample(ks, m)]) for _ in range(500)]
            ts = [a for a, _ in v if a == a]
            line += '  %d tales %.2f [%.2f, %.2f] sd %.2f, %.0f fn' % (m, np.mean(ts), np.percentile(ts, 5), np.percentile(ts, 95), np.std(ts), np.mean([b for _, b in v]))
        say(line)
# a shuffled baseline: the same with units shuffled within each story
for c in ('tale', 'eastasian'):
    S = strings(c, 'A'); ks = sorted(S)
    v = []
    for _ in range(300):
        pick = rng.sample(ks, 10)
        v.append(tau([rng.sample(S[k], len(S[k])) for k in pick])[0])
    v = [a for a in v if a == a]
    say('shuffled within story %s A, 10 tales: %.2f [%.2f, %.2f]' % (c, np.mean(v), np.percentile(v, 5), np.percentile(v, 95)))
open(os.path.join(HERE, 'PilotNoise.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')
