"""tragedyNoise.py -- for TragedyApartProtocol.md: the tragedies' old strings, sampled to a few hundred events, evenly across plays; existing strings only."""
import collections, csv, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Induction'))
import numpy as np, pilot as P, score as C
import strings as ST
slots, _ = C.propp(); num = C.numbering(slots); TS = ST.TS
csv.field_size_limit(10**9)
old = {'A': collections.defaultdict(lambda: collections.defaultdict(list)), 'B': collections.defaultdict(lambda: collections.defaultdict(list))}
for r in csv.DictReader(open(os.path.join(os.path.dirname(HERE), 'Data/tables/functions.tsv'), encoding='utf-8', newline=''), delimiter='\t', quoting=csv.QUOTE_NONE):
    if r['story'].startswith('tragedy:') and r['reader'] in old and r['version'] in ('', '1'):
        try: e = int(r['event'])
        except ValueError: continue
        ks = ['X'] if r['function'] == 'X' else [k for k in TS.key(r['function']) if k in TS.NUM]
        old[r['reader']][r['story']][e].extend(ks)
ev = {s: sorted(set(old['A'][s]) & set(old['B'][s])) for s in old['A']}
out = ['# TragedyNoise.txt -- %d plays, %d events' % (len(ev), sum(map(len, ev.values())))]
rng = random.Random(20261104)
for r in 'AB':
    full = P.tau(list(P.strings_of(old[r], num).values()), num)
    out.append('%s all events: tau %.3f on %d functions' % (r, *full))
    for m in (300, 400, 600):
        ts, ns = [], []
        for _ in range(500):
            per = m // len(ev)
            sub = {}
            for s, es in ev.items():
                pick = sorted(rng.sample(es, min(per, len(es))))
                sub[s] = collections.OrderedDict((e, old[r][s][e]) for e in pick)
            a, n = P.tau(list(P.strings_of(sub, num).values()), num)
            if a == a: ts.append(a); ns.append(n)
        out.append('%s %d events, even across plays: tau %.2f [%.2f, %.2f] on %.0f functions' % (r, m, np.mean(ts), np.percentile(ts, 5), np.percentile(ts, 95), np.mean(ns)))
open(os.path.join(HERE, 'TragedyNoise.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('\n'.join(out))
