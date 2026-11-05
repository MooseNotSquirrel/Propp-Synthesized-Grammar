"""shuffledSubset.py -- exploratory, added after the reading: tau from the batches whose readers said no scheme came to mind (B1, B2, B3, B6), and the others (B4, B5). A self-report, with 4 and 2 batches; events in a tale are thinned, not lost at random from a tale's order."""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, pilot as P, shuffled as S, score as C
slots, _ = C.propp(); num = C.numbering(slots)
pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
code = {c: P.norm(s) for s, c in pk['symbols'].items()}
key = {k: v for k, v in json.load(open(os.path.join(HERE, 'ShuffledKey.json'), encoding='utf-8')).items() if v[0] == 'wonder'}
def read(batches, r='B'):
    got = {}
    for b in batches:
        for line in open(os.path.join(S.TC, 'lines/wonder/coded', r, 'b%d' % b, 'Coded.txt'), encoding='utf-8'):
            p = [x.strip() for x in line.split(' | ')]
            if len(p) >= 2 and p[0] in key:
                labs = ['X' if u.rstrip(P.MINUS) == 'X' else code.get(u.rstrip(P.MINUS)) for u in p[1].split()]
                _, t, e = key[p[0]]
                got[(t, e)] = [u for u in labs if u]
    out = collections.OrderedDict()
    for (t, e) in sorted(got):
        out.setdefault(t, collections.OrderedDict())[e] = got[(t, e)]
    return out
lines = ['# ShuffledSubset.txt -- exploratory, after the reading']
for lab, bs in (('B, said no scheme (b1 b2 b3 b6)', (1, 2, 3, 6)), ('B, named Propp (b4 b5)', (4, 5))):
    L = read(bs); s = P.strings_of(L, num)
    t = P.tau(list(s.values()), num, minn=2)
    lines.append('%s: tau %.3f on %d functions (in at least 2 tales); null 95th %.3f; events %d' % (lab, t[0], t[1], np.percentile([P.tau([__import__('random').Random(i).sample(x, len(x)) for x in s.values()], num, minn=2)[0] for i in range(500)], 95), sum(len(v) for v in L.values())))
open(os.path.join(HERE, 'ShuffledSubset.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
