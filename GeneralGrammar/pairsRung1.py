"""pairsRung1.py <test|run> -- rungs 0 and 1 of PairsProtocol.md. No real string is read."""
import json
import multiprocessing
import os
import random
import re
import sys

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pairs as Q  # noqa: E402
import generators as X  # noqa: E402
import score as C  # noqa: E402

SEED = 20261107 + 3  # version 3's fresh draws
EXTRA = [('C', 'W'), ('G', 'U')]        # G9's planted spanning pairs, beside A-K and a-K in his list
SPAN = {('A', 'K'), ('a', 'K'), ('C', 'W'), ('G', 'U')}


def corpus(g, rep, slots, pairs):
    rng = np.random.default_rng([SEED, int(g[1]), rep])
    opener = next(i for i, alt in enumerate(slots) if len(alt) == 2)
    if g == 'G8':
        return X.g8(slots, pairs, 45, rng, opener)
    if g == 'G9':
        return X.g8(slots, list(pairs) + EXTRA, 45, rng, opener)
    if g in ('G1', 'G2'):
        st, tr = X.g1(slots, pairs, 45, rng, opener)
        return X.relabel(st, tr, rng) if g == 'G2' else (st, tr)
    return {'G4': X.g4, 'G5': X.g5, 'G7': X.g7}[g](45, rng)


def fit(flat):
    a, b = Q.halves(len(flat))
    found, cands, _, _ = Q.analyse([flat[i] for i in a])
    return found, Q.dependent(Q.confirm(found, [flat[i] for i in b]), flat), cands


def eligible(flat, ps):
    """pairs both of whose symbols stand together in at least 5 stories of the corpus"""
    return [p for p in ps if sum(1 for s in flat if p[0] in s and p[1] in s) >= 5]


def recalls(conf, truth_pairs, span):
    span = [p for p in span if p in truth_pairs]
    close = [p for p in truth_pairs if p not in span]
    r1 = sum(1 for p in close if p in conf and conf[p]['kind'] in ('tight', 'near')) / max(1, len(close))
    r2 = sum(1 for p in span if p in conf and conf[p]['kind'] == 'spanning') / max(1, len(span))
    return r1, r2


def work(a):
    g, rep, slots, pairs = a
    st, tr = corpus(g, rep, slots, pairs)
    flat = [f for f in (X.flat(s) for s in st) if f]
    found, conf, cands = fit(flat)
    r = {'g': g, 'rep': rep, 'found': len(found), 'confirmed': len(conf), 'cands': cands, 'kinds': {}}
    for f in conf.values():
        r['kinds'][f['kind']] = r['kinds'].get(f['kind'], 0) + 1
    tp = [tuple(p) for p in pairs]
    if g in ('G1', 'G8', 'G9'):
        allp = tp + (EXTRA if g == 'G9' else [])
        r['close'], r['span'] = recalls(conf, eligible(flat, allp), set(EXTRA) if g == 'G9' else set())
        r['ak'] = sum(1 for p in (('A', 'K'), ('a', 'K')) if p in conf and conf[p]['kind'] == 'spanning')
        known = set(allp)
        r['other_spanning'] = sum(1 for p, f in conf.items() if f['kind'] == 'spanning' and p not in known)
        r['other_close'] = sum(1 for p, f in conf.items() if f['kind'] != 'spanning' and p not in known)
    if g == 'G2':
        mp = tr['map']
        own = [(mp[x], mp[y]) for x, y in tp]
        sp = {(mp[x], mp[y]) for x, y in SPAN if x in mp and y in mp and (x, y) in tp}
        r['close'], r['span'] = recalls(conf, eligible(flat, own), set())
        r['close_propp'], r['span_propp'] = recalls(conf, eligible(flat, tp), set())
    if g == 'G4':
        ep = {u: i for i, e in enumerate(tr['episodes']) for u in e}
        ins = {(e[i], e[j]) for e in tr['episodes'] for i in range(5) for j in range(i + 1, 5)}
        r['inside'] = sum(1 for p in conf if p in ins) / len(ins)
        r['across_span'] = sum(1 for p, f in conf.items() if f['kind'] == 'spanning' and ep[p[0]] != ep[p[1]]) / max(1, cands)
    return r


def pct(xs, p):
    return float(np.percentile(xs, p))


def run(version):
    slots, pairs = C.propp()
    plan = [(g, r) for g in ('G9', 'G2', 'G8') for r in range(20)] + [(g, r) for g in ('G1', 'G4', 'G5', 'G7') for r in range(10)]
    with multiprocessing.Pool(4) as pool:
        rows = []
        for r in pool.imap_unordered(work, [(g, k, slots, pairs) for g, k in plan]):
            rows.append(r)
            print(len(rows), r['g'], r['rep'], r['confirmed'], flush=True)
    json.dump(sorted(rows, key=lambda r: (r['g'], r['rep'])), open(os.path.join(HERE, 'PairsRung1-%s.json' % version), 'w', encoding='utf-8'), indent=0)
    by = lambda g: [r for r in rows if r['g'] == g]
    out = ['# PairsRung1-%s.txt -- generated strings only; no real string read. Rules in PairsProtocol.md section 3' % version]
    for g in ('G1', 'G2', 'G4', 'G5', 'G7', 'G8', 'G9'):
        rs = by(g)
        kk = {}
        for r in rs:
            for k, v in r['kinds'].items():
                kk[k] = kk.get(k, 0) + v / len(rs)
        out.append('%s: candidates %.0f; found %.1f; confirmed %.1f; by kind %s' % (g, np.mean([r['cands'] for r in rs]), np.mean([r['found'] for r in rs]), np.mean([r['confirmed'] for r in rs]), {k: round(v, 1) for k, v in sorted(kk.items())}))
    g9 = by('G9')
    bars = {'close': pct([r['close'] for r in g9], 10), 'span': pct([r['span'] for r in g9], 10)}
    s9 = np.mean([r['span'] >= .8 for r in g9])
    out.append('G9: close recall median %.3f, spanning median %.3f; BARS (10th percentile) close %.3f, spanning %.3f; other spanning called per corpus, mean %.1f, of about %.0f candidates' % (pct([r['close'] for r in g9], 50), pct([r['span'] for r in g9], 50), bars['close'], bars['span'], np.mean([r['other_spanning'] for r in g9]), np.mean([r['cands'] for r in g9])))
    out.append('G9: other close pairs per corpus, mean %.1f; A-K and a-K found as spanning, mean of 2: %.2f (planted beside the other opener of K, so not gated)' % (np.mean([r['other_close'] for r in g9]), np.mean([r['ak'] for r in g9])))
    out.append('gate G9: corpora finding at least 80%% of planted spanning pairs: %.0f%% (need 80%%)' % (100 * s9))
    g2 = by('G2')
    own = np.mean([r['close'] >= bars['close'] for r in g2])
    false = np.mean([r['close_propp'] >= bars['close'] for r in g2])
    out.append('gate G2: reach the bars on their own pairs %.0f%%; on Propp\'s pairs %.0f%% (need at most 5%%); recall of his pairs, median close %.3f, span %.3f' % (100 * own, 100 * false, pct([r['close_propp'] for r in g2], 50), pct([r['span_propp'] for r in g2], 50)))
    g7 = np.mean([r['confirmed'] / max(1, r['cands']) for r in by('G7')])
    out.append('gate G7: share of candidates called pairs %.3f (need at most 0.05)' % g7)
    g4 = by('G4')
    ac = np.mean([r['across_span'] for r in g4])
    out.append('gate G4: inside-episode pairs found, mean %.3f; spanning across episodes, share of candidates %.3f (need at most 0.05)' % (np.mean([r['inside'] for r in g4]), ac))
    g8 = by('G8')
    out.append('beside: G8 close %.3f, spanning %.3f; G1 close %.3f, spanning %.3f; other spanning per corpus G1 %.1f, G8 %.1f' % (pct([r['close'] for r in g8], 50), pct([r['span'] for r in g8], 50), pct([r['close'] for r in by('G1')], 50), pct([r['span'] for r in by('G1')], 50), np.mean([r['other_spanning'] for r in by('G1')]), np.mean([r['other_spanning'] for r in g8])))
    ok = s9 >= .8 and false <= .05 and g7 <= .05 and ac <= .05
    out.append('RUNG 1: %s' % ('PASSES' if ok else 'FAILS'))
    open(os.path.join(HERE, 'PairsRung1-%s.txt' % version), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


def test():
    bad = 0

    def ok(n, c, x=''):
        nonlocal bad
        print('%-5s %s %s' % ('PASS' if c else 'FAIL', n, x))
        bad += 0 if c else 1
    src = open(os.path.join(HERE, 'pairs.py'), encoding='utf-8').read()
    imports = re.findall(r'^\s*(?:from|import)\s+([\w.]+)', src, re.M)
    ok('source: numpy and math only', set(imports) == {'numpy', 'math'}, str(imports))
    ok('source: no Propp', 'Propp' not in src and 'PROPP' not in src)
    d, c, b = Q.tally([np.array([0, 1, 2, 1])], 3)
    ok('hand-worked: 0 to next 1 is 1, 0 to next 2 is 2', d[0, 1] == 1 and d[0, 2] == 2 and c[0, 1] == 1)
    ok('hand-worked: first 1 to next 1 is 2, 2 to next 1 is 1', d[1, 1] == 2 and d[2, 1] == 1)
    ok('hand-worked: pairs before', b[0, 1] == 2 and b[1, 2] == 1 and b[2, 1] == 1 and b[1, 0] == 0)
    p = Q.bh([.001, .002, .5, .9])
    ok('false discovery rate', list(p) == [True, True, False, False])
    rng = random.Random(1)
    st = []
    for _ in range(40):
        s = rng.sample(list('abcdefgh'), 6)
        if 'p' or True:
            s = [u for u in s]
        i = rng.randrange(len(s) + 1)
        s[i:i] = ['x', 'y']
        st.append(s)
    f, cands, _, _ = Q.analyse(st, shuffles=300)
    ok('a planted tight pair is found as tight', f.get(('x', 'y'), {}).get('kind') == 'tight', str(f.get(('x', 'y'))))
    st2 = []
    for _ in range(40):
        m = rng.sample(list('abcdefgh'), 8)
        st2.append(['s'] + m + ['t'] if rng.random() < .9 else m)
    f2, _, _, _ = Q.analyse(st2, shuffles=300)
    ok('a planted spanning pair is found as spanning', f2.get(('s', 't'), {}).get('kind') == 'spanning', str(f2.get(('s', 't'))))
    st3 = [rng.sample(list('abcdefgh'), 6) for _ in range(40)]
    st3 += [rng.sample(list('abcdefgh'), 6) for _ in range(40)]
    dep = Q.dependent({('p', 'q'): {}, ('p', 'r'): {}}, [['p', 'q']] * 10 + [['r', 'z']] * 10)
    ok('dependence: p with q, not p with r', ('p', 'q') in dep and ('p', 'r') not in dep)
    f3, c3, _, _ = Q.analyse(st3[:40], shuffles=300)
    k3 = Q.confirm(f3, st3[40:], shuffles=300)
    ok('shuffled stories give few pairs, over both halves', len(k3) <= .05 * c3, '%d of %d' % (len(k3), c3))
    mp = {u: 'zz' + u[::-1] for s in st for u in s}
    f4, _, _, _ = Q.analyse([[mp[u] for u in s] for s in st], shuffles=300)
    ok('renaming gives the same pairs', {(mp[a], mp[b]): v for (a, b), v in f.items()} == f4)
    f5, _, _, _ = Q.analyse(st, shuffles=300)
    ok('two runs identical', f == f5)
    slots, pairs = C.propp()
    s9, _ = corpus('G9', 0, slots, pairs)
    ok('G9 is plain strings', isinstance(X.flat(s9[0])[0], str))
    print('rung 0: %s' % ('all pass' if not bad else '%d FAILED' % bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        test()
    else:
        run(sys.argv[2])
