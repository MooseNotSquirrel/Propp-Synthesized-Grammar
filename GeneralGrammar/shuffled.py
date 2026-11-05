"""shuffled.py -- the measure and reading of ShuffledProtocol.md section 4 and 5. Usage: python shuffled.py <wonder or east>"""
import collections
import glob
import json
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pilot as P  # noqa: E402

TC = 'C:/Users/Steve1/TaleCoding'
STORY = {'wonder': 'tale', 'east': 'eastasian'}


def parse(name, reader, key, code):
    """{tale: {event: [labels]}} in story order"""
    got = {}
    bad = 0
    for f in glob.glob(os.path.join(TC, 'lines', name, 'coded', reader, 'b*', 'Coded.txt')):
        for line in open(f, encoding='utf-8'):
            p = [x.strip() for x in line.split(' | ')]
            if len(p) < 2 or p[0] not in key:
                continue
            labs = []
            for u in p[1].split():
                s = u.rstrip(P.MINUS)
                if s == 'X':
                    labs.append('X')
                elif s in code:
                    labs.append(code[s])
                else:
                    bad += 1
            if labs:
                _, t, e = key[p[0]]
                got[(t, e)] = labs
    out = collections.OrderedDict()
    for (t, e) in sorted(got):
        out.setdefault(t, collections.OrderedDict())[e] = got[(t, e)]
    return out, bad


def agreement(a, b):
    xs = [(P.primary(a[t][e]), P.primary(b[t][e])) for t in set(a) & set(b) for e in set(a[t]) & set(b[t])]
    return float(np.mean([x == y for x, y in xs])) if xs else float('nan')


def noisy_range(whole, p, num, draws=1000, seed=20261104):
    rng = random.Random(seed)
    pool = [P.primary(ls) for t in whole.values() for ls in t.values()]
    v = []
    for _ in range(draws):
        strs = []
        for t in whole.values():
            x = []
            for ls in t.values():
                u = P.primary(ls)
                if rng.random() < p:
                    u = rng.choice(pool)
                if u in num and u not in P.PREP:
                    x.append(u)
            if len(x) >= 2:
                strs.append(x)
        v.append(P.tau(strs, num)[0])
    v = [a for a in v if a == a]
    return float(np.percentile(v, 5)), float(np.percentile(v, 95))


def null95(strs, num, draws=1000, seed=20261104):
    rng = random.Random(seed)
    v = [P.tau([rng.sample(x, len(x)) for x in strs], num)[0] for _ in range(draws)]
    v = [a for a in v if a == a]
    return float(np.percentile(v, 95))


def reading(tau, k_whole, k_ab, lo, n95):
    if k_whole < 0.25 or k_ab < 0.25:
        return 'TOO POOR'
    if tau >= 0.5 and tau > n95 and tau >= lo:
        return 'IN THE EVENTS'
    if tau <= lo - 0.15:
        return 'NEEDS THE SEQUENCE'
    return 'IN PART'


def words_give_place(name):
    """relative position from a line's words alone, on held-out tales: R squared"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import Ridge
    by = collections.defaultdict(list)
    for l in open(os.path.join(TC, name, 'Events.txt'), encoding='utf-8'):
        p = l.rstrip('\n').split(' | ', 2)
        by[p[0]].append((int(p[1]), p[2]))
    ts = sorted(by)
    y, X, g = [], [], []
    for i, t in enumerate(ts):
        ev = sorted(by[t])
        for j, (_, text) in enumerate(ev):
            y.append(j / max(1, len(ev) - 1))
            X.append(text)
            g.append(i % 5)
    y, g = np.array(y), np.array(g)
    pred = np.zeros(len(y))
    for f in range(5):
        v = TfidfVectorizer(min_df=2)
        tr = g != f
        m = Ridge(alpha=1.0).fit(v.fit_transform([x for x, b in zip(X, tr) if b]), y[tr])
        pred[~tr] = m.predict(v.transform([x for x, b in zip(X, tr) if not b]))
    return 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def main(name):
    import score as C
    slots, _ = C.propp()
    num = C.numbering(slots)
    pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    code = {c: P.norm(s) for s, c in pk['symbols'].items()}
    allkey = json.load(open(os.path.join(HERE, 'ShuffledKey.json'), encoding='utf-8'))
    key = {k: v for k, v in allkey.items() if v[0] == name}
    tales = {v: k for k, v in pk['tales'][name].items()}
    out = ['# Shuffled-%s.txt -- ShuffledProtocol.md, the frozen reading; %d events' % (name, len(key))]
    L, whole = {}, {}
    for r in 'AB':
        L[r], bad = parse(name, r, key, code)
        n = sum(len(v) for v in L[r].values())
        out.append('%s: %d of %d events coded; codes not on the card %d' % (r, n, len(key), bad))
        if name == 'wonder':
            whole[r] = P.parse_notes(os.path.join(TC, 'wonder/coded', r, 'Notes.txt'), code, tales)
        else:
            whole[r] = P.old_notes(STORY[name], r, set(pk['tales'][name]))
    kab = P.kappa(L['A'], L['B'])[0]
    out.append('kappa A with B, coded apart: %.3f' % kab)
    for r in 'AB':
        s = P.strings_of(L[r], num)
        t, nf = P.tau(list(s.values()), num)
        kw = P.kappa(L[r], whole[r])[0]
        ag = agreement(L[r], whole[r])
        lo, hi = noisy_range(whole[r], 1 - ag, num)
        n95 = null95(list(s.values()), num)
        tw = P.tau(list(P.strings_of(whole[r], num).values()), num)[0]
        out.append('%s: tau %.3f on %d functions; whole-tale %.3f; kappa with whole-tale %.3f (agreement %.3f); expected at that rate [%.3f, %.3f]; null 95th %.3f: %s' % (r, t, nf, tw, kw, ag, lo, hi, n95, reading(t, kw, kab, lo, n95)))
    out.append('## beside the reading, not deciding')
    out.append('place from the words alone, held-out tales, R squared %.3f' % words_give_place(name))
    for r in 'AB':
        wp = P.with_prep(L[r], num)
        out.append('%s: with preparatory units tau %.3f (%d); given a symbol %.3f, whole-tale %.3f' % (r, *P.tau(list(wp.values()), num), P.covered(L[r]), P.covered(whole[r])))
        pl, st = P.places(list(wp.values()))
        wpl, wst = P.places(list(P.with_prep(whole[r], num).values()))
        out.append('   mean place apart / whole-tale: ' + ' '.join('%s %.2f/%.2f' % (u, pl[u], wpl.get(u, float('nan'))) for u in sorted(P.PREP | {'A', 'a', 'K', 'W'}) if u in pl and st[u] >= 3))
    open(os.path.join(HERE, 'Shuffled-%s.txt' % name), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1])
