"""leaves.py -- the leaves (LeafProtocol.md, frozen 2026-11-04). Commands: ceil, l1, cluster, l2, l3, l4. No reader is used.

Details the protocol left open, fixed here before any figure is read:
- Rows. Functions: every row, X kept as a class; the wondertales on card U, as the induction read them; first version only.
  Acts and significance: each story and reader has one study (StoryModels/common.py), whichever it is. A first run left the
  'problems' study out, in error, and so lost about half of the tales, plays and fables; build_features now checks the counts.
- An event's primary label is its first function that is not X, or else X.
- Judged measure: "share of the ceiling" (P1, the reasonable answer) is macro F1 over the ceiling's macro F1, because the hit rate
  has a high floor from X. Hit rate and normalized mutual information stand beside it. P2: F5 against F2, per-story hit, one-sided
  paired sign-flip, p at most 0.05. P3: fails if some thesaurus alone beats the act alone so, in either reader.
- The ceiling: each reader's primary label as the prediction of the other's, both ways, on events both cover.
- WordNet classes: Group/wordnetGroup.py's rule (first verb sense, second level). Moby: verbs used at least 5 times, as their
  synonym sets, spherical k-means with as many classes as WordNet gives them. Unknown verbs keep their own name.
  VerbNet is left out: the package's readme shows no license, so the protocol's condition is not met.
- L2: k of 32 (31 plus X, as the base's size) and k by held-out mixture likelihood over 8, 16, 24, 32, 48, 64, 96. Replication
  is judged against 200 permutations of one reader's clusters, p at most 0.05.
- L3: an event is X for a reader when all its rows are X. A cluster replicates when its best match in the other reader has a
  Jaccard of at least 0.3 over events both left X, and it stands in at least 10 stories.
"""
import collections
import json
import math
import multiprocessing
import os
import pickle
import random
import sys
import tempfile

import numpy as np
from scipy import sparse
from scipy.stats import kendalltau

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, f1_score, normalized_mutual_info_score, v_measure_score  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20261104
CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'native', 'eastasian']
READERS = 'AB'
CACHE = os.path.join(tempfile.gettempdir(), 'leaves-cache-%d.pkl' % SEED)
WORDNET = 'C:/Users/Steve1/nltk_wordnet'
MOBY = 'C:/Users/Steve1/moby_thesaurus/x/files/mthesaur.txt'
ACT_STUDIES = ['twolayer', 'problems', 'held', 'animal', 'native', 'eastasian']
SIG_STUDIES = ['significance', 'problems', 'five', 'held', 'animal', 'native', 'eastasian']
EXPECT = {'tale': 45, 'animal': 50, 'fable': 90, 'tragedy': 32, 'native': 50, 'eastasian': 50}  # Data/Coverage.txt
KS = (8, 16, 24, 32, 48, 64, 96)
PREP = set('βγδεζηθλ')
STEPS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
ALONE = ['act', 'wordnet', 'moby']
OUT = []


def say(s):
    OUT.append(s)
    print(s, flush=True)


def save(name):
    open(os.path.join(HERE, 'Leaf-%s.txt' % name), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


# ---------------------------------------------------------------- the data
def tables():
    sys.path.insert(0, os.path.join(ROOT, 'Data'))
    import tables as DT
    return DT


def pick_study(rows, order):
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        by[(r['story'], r['reader'])][r['study']].append(r)
    out = {}
    for k, v in by.items():
        for s in order:
            if s in v:
                out[k] = v[s]
                break
    return out


def to_int(x):
    try:
        return int(x)
    except ValueError:
        return None


def build_features():
    """{(corpus, reader): [(story, [event dicts in order])]}; no function label is touched here"""
    DT = tables()
    keep = lambda r: r['reader'] in READERS and r['reader'] and r['story'].split(':')[0] in CORPORA
    acts = pick_study([r for r in DT.rows('acts') if keep(r) and not r.get('id_flag')], ACT_STUDIES)
    sig = pick_study([r for r in DT.rows('significance') if keep(r)], SIG_STUDIES)
    free = collections.defaultdict(list)
    for r in DT.rows('free'):
        if keep(r):
            free[(r['story'], r['reader'])].append(r)
    text = {}
    for r in DT.rows('events'):
        text[(r['story'], to_int(r['event']))] = r['text']
    out = collections.defaultdict(list)
    for k in sorted(set(acts) & set(sig) & set(free)):
        story, reader = k
        ev = collections.defaultdict(lambda: {'verb': [], 'act': [], 'rel': [], 'sig': []})
        for r in free[k]:
            e = to_int(r['event'])
            if e is not None and r['verb']:
                ev[e]['verb'].append(r['verb'].strip().lower())
        for r in acts[k]:
            e = to_int(r['event'])
            if e is not None:
                if r['act']:
                    ev[e]['act'].append(r['act'])
                if r['relation']:
                    ev[e]['rel'].append(r['relation'])
        for r in sig[k]:
            e = to_int(r['event'])
            if e is not None:
                p = r['problem'] if r['problem'] in ('p1', 'p2') else ('p3+' if r['problem'].startswith('p') else '-')
                ev[e]['sig'] += ['part=' + r['part'], 'value=' + r['value'], 'place=' + r['place'], 'link=' + r['link'], 'problem=' + p]
        events = [dict(e=e, **ev[e]) for e in sorted(ev)]
        out[(story.split(':')[0], reader)].append((story, events))
    for c, n in EXPECT.items():
        for r in READERS:
            got = len(out.get((c, r), []))
            if got != n:
                raise SystemExit('leaves: %s reader %s has %d stories, Coverage.txt says %d' % (c, r, got, n))
    return {'features': dict(out), 'text': text}


def build_labels():
    """{(story, reader): {event: [labels in row order]}}, and Propp's bags"""
    DT = tables()
    sys.path.insert(0, os.path.join(ROOT, 'Induction'))
    cwd = os.getcwd()
    import strings as ST
    os.chdir(cwd)
    TS = ST.TS
    lab = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in DT.rows('functions'):
        c = r['story'].split(':')[0]
        if r['reader'] not in ('A', 'B') or c not in CORPORA or r['version'] not in ('', '1'):
            continue
        if c == 'tale' and r['card'] != 'U':
            continue
        e = to_int(r['event'])
        if e is None:
            continue
        f = r['function']
        if f == 'X':
            lab[(r['story'], r['reader'])][e].append('X')
        else:
            ks = [k for k in TS.key(f) if k in TS.NUM]
            lab[(r['story'], r['reader'])][e] += ks
    propp = collections.defaultdict(collections.Counter)
    for r in DT.rows('resolved'):
        for s in r['string'].split():
            for k in TS.key(s):
                if k in TS.NUM:
                    propp[r['story']][k] += 1
    return {k: dict(v) for k, v in lab.items()}, dict(propp), sorted(TS.NUM)


def load():
    if not os.path.exists(CACHE):
        d = build_features()
        d['labels'], d['propp'], d['num'] = build_labels()
        pickle.dump(d, open(CACHE, 'wb'))
    return pickle.load(open(CACHE, 'rb'))


def primary(ls):
    for x in ls:
        if x != 'X':
            return x
    return 'X'


def neighbours(evs, i):
    out = []
    for j in range(max(0, i - 2), min(len(evs), i + 3)):
        if j != i:
            out += ['n:' + a for a in evs[j]['act']] + ['n:' + v for v in evs[j]['verb']]
    return out


def tokens(evs, i, step, thes=None):
    """the feature bag of one event at one step of the ladder, or for one alphabet alone"""
    e = evs[i]
    if step == 'act':
        return ['a:' + a for a in e['act']]
    if step in ('wordnet', 'moby'):
        return ['c:' + thes[step].get(v, v) for v in e['verb']]
    t = ['v:' + v for v in e['verb']]
    if step in ('F2', 'F3', 'F4', 'F5', 'F6'):
        t += ['a:' + a for a in e['act']]
    if step in ('F3', 'F4', 'F5', 'F6'):
        t += ['r:' + a for a in e['rel']]
    if step in ('F4', 'F5', 'F6'):
        t += ['s:' + a for a in e['sig']]
    if step in ('F5', 'F6'):
        t += neighbours(evs, i)
    if step == 'F6':
        t.append('pos:%d' % min(4, int(5 * i / max(1, len(evs)))))
    return t


# ---------------------------------------------------------------- L1's engine
def matrix(bags, index=None, min_count=2):
    if index is None:
        c = collections.Counter(t for b in bags for t in set(b))
        index = {}
        for b in bags:
            for t in b:
                if t not in index and c[t] >= min_count:
                    index[t] = len(index)
    rows, cols = [], []
    for i, b in enumerate(bags):
        for t in set(b):
            if t in index:
                rows.append(i)
                cols.append(index[t])
    return sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(bags), max(1, len(index)))), index


def fit_predict(train_bags, train_y, test_bags):
    """the logistic model: L2 penalty 1.0; one row per label; the labels numbered by first appearance"""
    Xtr, idx = matrix(train_bags)
    Xte, _ = matrix(test_bags, idx)
    names, y = {}, []
    for l in train_y:
        y.append(names.setdefault(l, len(names)))
    inv = {v: k for k, v in names.items()}
    if len(names) == 1:
        return [inv[0]] * len(test_bags)
    m = LogisticRegression(C=1.0, max_iter=300)
    m.fit(Xtr, y)
    return [inv[int(i)] for i in m.predict(Xte)]


def folds_of(n, k=5):
    idx = list(range(n))
    random.Random(SEED).shuffle(idx)
    return [sorted(idx[i::k]) for i in range(k)]


def evaluate(story_rows):
    """story_rows: [[(prediction, label list)]] per story: hit, macro F1, NMI, per-story hit"""
    true, pred, per = [], [], []
    for rows in story_rows:
        h = 0
        for p, ls in rows:
            t = p if p in ls else primary(ls)
            true.append(t)
            pred.append(p)
            h += p in ls
        per.append(h / len(rows) if rows else float('nan'))
    hits = np.mean([t == p for t, p in zip(true, pred)])
    return {'hit': float(hits), 'f1': float(f1_score(true, pred, average='macro', zero_division=0)),
            'nmi': float(normalized_mutual_info_score(true, pred)), 'per': per, 'true': true, 'pred': pred}


def ladder_cv(stories, step, thes=None, labels_of=None):
    """stories: [(story, events)]; labels_of(story, event) -> label list or None. Held out whole, five folds"""
    data = []
    for st, evs in stories:
        rows = []
        for i, e in enumerate(evs):
            ls = labels_of(st, e['e'])
            if ls:
                rows.append((tokens(evs, i, step, thes) if step != 'F0' else [], ls))
        data.append(rows)
    out = [[] for _ in data]
    for test in folds_of(len(data)):
        ts = set(test)
        trb, try_ = [], []
        for i, rows in enumerate(data):
            if i not in ts:
                for b, ls in rows:
                    for l in ls:
                        trb.append(b)
                        try_.append(l)
        if step == 'F0':
            common = collections.Counter(try_).most_common(1)[0][0]
        for i in test:
            bags = [b for b, _ in data[i]]
            ps = [common] * len(bags) if step == 'F0' else (fit_predict(trb, try_, bags) if bags else [])
            out[i] = [(p, ls) for p, (_, ls) in zip(ps, data[i])]
    return evaluate(out)


def flip_p(a, b, seed=SEED, flips=5000):
    d = np.array(a, float) - np.array(b, float)
    d = d[~np.isnan(d)]
    if len(d) == 0 or d.mean() <= 0:
        return 1.0
    rng = np.random.default_rng(seed)
    s = rng.choice([-1.0, 1.0], size=(flips, len(d)))
    return float((((s * d).mean(1) >= d.mean() - 1e-12).sum() + 1) / (flips + 1))


# ---------------------------------------------------------------- thesauruses
def thesauri(d):
    verbs = collections.Counter(v for st in d['features'].values() for _, evs in st for e in evs for v in e['verb'])
    import nltk
    nltk.data.path.insert(0, WORDNET)
    from nltk.corpus import wordnet as wn
    wnc = {}
    for v in verbs:
        ss = wn.synsets(v, pos='v')
        if ss:
            path = ss[0].hypernym_paths()[0]
            wnc[v] = path[min(2, len(path)) - 1].lemma_names()[0] + '~'
    common = [v for v in sorted(verbs, key=lambda x: (-verbs[x], x)) if verbs[v] >= 5]
    syn = {}
    for line in open(MOBY, encoding='latin-1'):
        p = line.rstrip('\n').split(',')
        syn[p[0].lower()] = set(x.lower() for x in p[1:])
    have = [v for v in common if v in syn]
    words = {}
    rows, cols = [], []
    for i, v in enumerate(have):
        for w in syn[v] | {v}:
            rows.append(i)
            cols.append(words.setdefault(w, len(words)))
    k = len({wnc[v] for v in common if v in wnc})
    M = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(have), len(words)))
    M = sparse.diags(1 / np.sqrt(np.asarray(M.multiply(M).sum(1)).ravel())) @ M
    km = KMeans(n_clusters=min(k, len(have)), n_init=20, random_state=SEED).fit(M)
    mob = {v: 'moby%03d~' % c for v, c in zip(have, km.labels_)}
    return {'wordnet': wnc, 'moby': mob, 'note': {'common verbs': len(common), 'wordnet classes': k, 'moby knows': len(have)}}


# ---------------------------------------------------------------- ceilings
def ceilings(d):
    """{corpus: dict}; and each reader's bags against Propp"""
    lab = d['labels']
    out = {}
    for c in CORPORA:
        rowsA, rowsB, pa, pb = [], [], [], []
        stories = [s for s, _ in d['features'].get((c, 'A'), [])]
        for s in stories:
            a, b = lab.get((s, 'A'), {}), lab.get((s, 'B'), {})
            ra, rb = [], []
            for e in sorted(set(a) & set(b)):
                if a[e] and b[e]:
                    ra.append((primary(b[e]), a[e]))
                    rb.append((primary(a[e]), b[e]))
                    pa.append(primary(a[e]))
                    pb.append(primary(b[e]))
            rowsA.append(ra)
            rowsB.append(rb)
        ea, eb = evaluate(rowsA), evaluate(rowsB)
        names = sorted(set(pa) | set(pb))
        n = len(pa)
        po = sum(x == y for x, y in zip(pa, pb)) / n
        pe = sum(pa.count(x) / n * pb.count(x) / n for x in names)
        covA = np.mean([x != 'X' for x in pa])
        covB = np.mean([x != 'X' for x in pb])
        both = [(x, y) for x, y in zip(pa, pb) if x != 'X' and y != 'X']
        out[c] = {'hit': (ea['hit'] + eb['hit']) / 2, 'f1': (ea['f1'] + eb['f1']) / 2, 'nmi': (ea['nmi'] + eb['nmi']) / 2, 'kappa': (po - pe) / (1 - pe),
                  'events': n, 'covered': (covA + covB) / 2, 'agreed': float(np.mean([x == y for x, y in both])) if both else float('nan')}
    return out


def cosine(a, b):
    keys = set(a) | set(b)
    x = np.array([a.get(k, 0) for k in keys], float)
    y = np.array([b.get(k, 0) for k in keys], float)
    if not x.any() or not y.any():
        return float('nan')
    return float(x @ y / np.linalg.norm(x) / np.linalg.norm(y))


def reader_bag(lab, s, r):
    c = collections.Counter()
    for ls in lab.get((s, r), {}).values():
        for x in ls:
            if x != 'X' and x not in PREP:
                c[x] += 1
    return c


def bags_vs_propp(d):
    out = {}
    pr = {s: collections.Counter({k: v for k, v in b.items() if k not in PREP}) for s, b in d['propp'].items()}
    ss = sorted(pr)
    for r in READERS:
        same = [cosine(reader_bag(d['labels'], s, r), pr[s]) for s in ss]
        other = [cosine(reader_bag(d['labels'], s, r), pr[t]) for s in ss for t in ss if t != s]
        out[r] = (float(np.nanmean(same)), float(np.nanmean(other)))
    return out


def cmd_ceil():
    d = load()
    say('# Leaf-ceil.txt -- the ceilings (LeafProtocol.md section 2) and the owner\'s 80% read two of three ways (speculation, reported, no verdict)')
    cs = ceilings(d)
    say('corpus      events  hit    macroF1  NMI    kappa   covered  agreed where both cover')
    for c in CORPORA:
        x = cs[c]
        say('%-10s %6d  %.3f  %.3f    %.3f  %.3f   %.3f    %.3f' % (c, x['events'], x['hit'], x['f1'], x['nmi'], x['kappa'], x['covered'], x['agreed']))
    b = bags_vs_propp(d)
    for r in READERS:
        say('reader %s: functions of a tale against Propp\'s (no X, no preparatory), cosine: same tale %.3f; another tale %.3f' % (r, b[r][0], b[r][1]))
    t = thesauri(d)
    say('thesauruses: %s' % t['note'])
    save('ceil')


# ---------------------------------------------------------------- L1
def l1_job(a):
    c, r, step, kind = a
    d = load()
    th = pickle.load(open(CACHE + '.th', 'rb'))
    lab = d['labels']
    stories = d['features'].get((c, r), [])
    reader_lab = r
    if kind == 'cross':
        reader_lab = 'B' if r == 'A' else 'A'
    res = ladder_cv(stories, step, th, lambda s, e: lab.get((s, reader_lab), {}).get(e))
    return (c, r, step, kind), {k: res[k] for k in ('hit', 'f1', 'nmi', 'per', 'true', 'pred')}


def transfer_job(a):
    """fitted on some corpora, scored on one, at F5 and with the act alone"""
    target, sources, r, step = a
    d = load()
    th = pickle.load(open(CACHE + '.th', 'rb'))
    lab = d['labels']
    trb, try_ = [], []
    for c in sources:
        for s, evs in d['features'].get((c, r), []):
            for i, e in enumerate(evs):
                for l in lab.get((s, r), {}).get(e['e'], []):
                    trb.append(tokens(evs, i, step, th))
                    try_.append(l)
    out = []
    for s, evs in d['features'].get((target, r), []):
        rows = [(tokens(evs, i, step, th), lab[(s, r)][e['e']]) for i, e in enumerate(evs) if lab.get((s, r), {}).get(e['e'])]
        ps = fit_predict(trb, try_, [b for b, _ in rows]) if rows else []
        out.append([(p, ls) for p, (_, ls) in zip(ps, rows)])
    res = evaluate(out)
    return (target, tuple(sources), r, step), {k: res[k] for k in ('hit', 'f1', 'nmi')}


def cmd_l1():
    d = load()
    th = thesauri(d)
    pickle.dump(th, open(CACHE + '.th', 'wb'))
    cs = ceilings(d)
    say('# Leaf-L1.txt -- how much does each kind of evidence tell? Stories held out whole. Labels under Propp\'s card; acts, verbs and significance read without it, on event lists that were not')
    jobs = [(c, r, s, 'ladder') for c in CORPORA for r in READERS for s in ['F0'] + STEPS + ALONE]
    jobs += [(c, r, s, 'cross') for c in CORPORA for r in READERS for s in ('F1', 'act')]
    with multiprocessing.Pool(4) as pool:
        res = dict(pool.imap_unordered(l1_job, jobs))
        res2 = {}
        tj = [(c, ['tale'], r, s) for c in CORPORA if c != 'tale' for r in READERS for s in ('F5', 'act')]
        tj += [('tale', [c for c in CORPORA if c != 'tale'], r, s) for r in READERS for s in ('F5', 'act')]
        res2 = dict(pool.imap_unordered(transfer_job, tj))
    names = ['F0'] + STEPS + ALONE
    for c in CORPORA:
        say('## %s: ceiling hit %.3f, macro F1 %.3f, NMI %.3f, kappa %.3f' % (c, cs[c]['hit'], cs[c]['f1'], cs[c]['nmi'], cs[c]['kappa']))
        say('step      ' + ''.join('%-24s' % ('reader ' + r + ': hit  F1  NMI  share') for r in READERS))
        for s in names:
            cell = ''
            for r in READERS:
                x = res[(c, r, s, 'ladder')]
                cell += '%.3f %.3f %.3f %4.0f%%     ' % (x['hit'], x['f1'], x['nmi'], 100 * x['f1'] / cs[c]['f1'])
            say('%-9s %s' % (s, cell))
        for r in READERS:
            x, y = res[(c, r, 'F1', 'cross')], res[(c, r, 'act', 'cross')]
            say('across readers, %s\'s features for the other\'s labels: verb F1 %.3f, act F1 %.3f' % (r, x['f1'], y['f1']))
    say('## per function, wondertales: F1 by the verb, the act, F4 and F5 (reader A; reader B)')
    fs = collections.Counter(res[('tale', 'A', 'F5', 'ladder')]['true']).most_common(24)
    def per_f(key, f):
        x = res[key]
        t = [a == f for a in x['true']]
        p = [a == f for a in x['pred']]
        return f1_score(t, p, zero_division=0)
    for f, n in fs:
        say('%-5s n %4d  ' % (f, n) + '  '.join('%s %.2f %.2f' % (lab_, per_f(('tale', 'A', s, 'ladder'), f), per_f(('tale', 'B', s, 'ladder'), f)) for s, lab_ in (('F1', 'verb'), ('act', 'act'), ('F4', 'F4'), ('F5', 'F5'))))
    say('## transfer: macro F1, as a share of the target\'s ceiling')
    for c in CORPORA:
        src = 'tale' if c != 'tale' else 'the others'
        srcs = ('tale',) if c != 'tale' else tuple(x for x in CORPORA if x != 'tale')
        say('%-10s from %-10s ' % (c, src) + '  '.join('%s %s F1 %.3f (%3.0f%%) hit %.3f' % (r, s, res2[(c, srcs, r, s)]['f1'], 100 * res2[(c, srcs, r, s)]['f1'] / cs[c]['f1'], res2[(c, srcs, r, s)]['hit']) for r in READERS for s in ('F5', 'act')))
    say('## the predictions (wondertales, per reader, held-out stories)')
    t = cs['tale']['f1']
    p1 = {r: res[('tale', r, 'F1', 'ladder')]['f1'] / t for r in READERS}
    say('P1 the verb alone under half the ceiling: A %.0f%%, B %.0f%%: %s' % (100 * p1['A'], 100 * p1['B'], verdict(p1['A'] < .5, p1['B'] < .5)))
    p2 = {r: flip_p(res[('tale', r, 'F5', 'ladder')]['per'], res[('tale', r, 'F2', 'ladder')]['per']) for r in READERS}
    say('P2 significance and neighbours beat the act: hit F5 %.3f %.3f against F2 %.3f %.3f; p A %.4f, B %.4f: %s' % (res[('tale', 'A', 'F5', 'ladder')]['hit'], res[('tale', 'B', 'F5', 'ladder')]['hit'], res[('tale', 'A', 'F2', 'ladder')]['hit'], res[('tale', 'B', 'F2', 'ladder')]['hit'], p2['A'], p2['B'], verdict(p2['A'] <= .05, p2['B'] <= .05)))
    good = {}
    for r in READERS:
        ps = {s: flip_p(res[('tale', r, s, 'ladder')]['per'], res[('tale', r, 'act', 'ladder')]['per']) for s in ('wordnet', 'moby')}
        good[r] = all(v > .05 for v in ps.values())
        say('P3 reader %s: act hit %.3f F1 %.3f; wordnet hit %.3f F1 %.3f (p %.4f); moby hit %.3f F1 %.3f (p %.4f)' % (r, res[('tale', r, 'act', 'ladder')]['hit'], res[('tale', r, 'act', 'ladder')]['f1'], res[('tale', r, 'wordnet', 'ladder')]['hit'], res[('tale', r, 'wordnet', 'ladder')]['f1'], ps['wordnet'], res[('tale', r, 'moby', 'ladder')]['hit'], res[('tale', r, 'moby', 'ladder')]['f1'], ps['moby']))
    say('P3 no thesaurus beats the act: %s' % verdict(good['A'], good['B']))
    say('## the reasonable answer, first part: best of F2 to F5, macro F1 as a share of the wondertales\' ceiling')
    best = {r: max(res[('tale', r, s, 'ladder')]['f1'] for s in ('F2', 'F3', 'F4', 'F5')) / t for r in READERS}
    say('A %.0f%%, B %.0f%% (needs 80%% for both): %s' % (100 * best['A'], 100 * best['B'], 'met' if min(best.values()) >= .8 else 'NOT met'))
    say('## the owner\'s 80%, speculation, read three ways, no verdict')
    for c in CORPORA:
        tr = 'tale' if c != 'tale' else None
        if c == 'tale':
            srcs = tuple(x for x in CORPORA if x != 'tale')
        else:
            srcs = ('tale',)
        say('%-10s covered %.0f%%; agreed %.0f%%; transferred %.0f%% of its ceiling (macro F1, mean of A and B)' % (c, 100 * cs[c]['covered'], 100 * cs[c]['agreed'], 100 * np.mean([res2[(c, srcs, r, 'F5')]['f1'] for r in READERS]) / cs[c]['f1']))
    save('L1')


def verdict(a, b):
    return 'HOLDS' if a and b else ('SPLIT' if a or b else 'FAILS')


# ---------------------------------------------------------------- L2: no function label is read in cmd_cluster
def alphabet_bags(evs, name, th):
    out = []
    for i, e in enumerate(evs):
        if name == 'A':
            b = {'v': ['v:' + v for v in e['verb']]}
        elif name == 'C':
            b = {'a': ['a:' + a for a in e['act']]}
        else:
            b = {'a': ['a:' + a for a in e['act']], 'r': ['r:' + a for a in e['rel']], 's': ['s:' + a for a in e['sig']]}
            if name == 'E':
                b['n'] = neighbours(evs, i)
        out.append(b)
    return out


def block_matrix(bags, min_count=2):
    """each block scaled to length one per event, then the row to length one: no block dominates"""
    blocks = sorted({k for b in bags for k in b})
    ms = []
    for k in blocks:
        m, _ = matrix([b.get(k, []) for b in bags], None, min_count)
        n = np.sqrt(np.asarray(m.multiply(m).sum(1)).ravel())
        n[n == 0] = 1
        ms.append(sparse.diags(1 / n) @ m)
    M = sparse.hstack(ms).tocsr()
    n = np.sqrt(np.asarray(M.multiply(M).sum(1)).ravel())
    n[n == 0] = 1
    return sparse.diags(1 / n) @ M


def spherical(M, k, starts, seed):
    k = min(k, M.shape[0] - 1)
    return KMeans(n_clusters=k, n_init=starts, random_state=seed).fit(M)


def heldout_k(M, seed):
    """k by the held-out likelihood of a mixture over the rows, four parts to fit and one to score"""
    n = M.shape[0]
    idx = np.random.default_rng(seed).permutation(n)
    te, tr = idx[:n // 5], idx[n // 5:]
    best, bestv, table = None, -float('inf'), {}
    B = (M > 0).astype(float).tocsr()
    for k in KS:
        if k >= len(tr):
            continue
        km = spherical(M[tr], k, 5, seed)
        lab = km.labels_
        K = lab.max() + 1
        pi = (np.bincount(lab, minlength=K) + 1) / (len(lab) + K)
        theta = np.zeros((K, B.shape[1]))
        for j in range(K):
            theta[j] = (np.asarray(B[tr][lab == j].sum(0)).ravel() + 0.1) / ((lab == j).sum() + 0.2)
        ll = B[te] @ np.log(theta).T + (1 - B[te].toarray()) @ np.log(1 - theta).T + np.log(pi)
        m = ll.max(1, keepdims=True)
        v = float((m[:, 0] + np.log(np.exp(ll - m).sum(1))).mean())
        table[k] = round(v, 3)
        if v > bestv:
            best, bestv = k, v
    return best, table


def cluster_job(a):
    c, r, name = a
    d = load()
    th = pickle.load(open(CACHE + '.th', 'rb'))
    stories = d['features'].get((c, r), [])
    keys, bags = [], []
    for s, evs in stories:
        bb = alphabet_bags(evs, name, th) if name in 'ACDE' else None
        for i, e in enumerate(evs):
            keys.append((s, e['e']))
            if name in 'ACDE':
                bags.append(bb[i])
            else:
                bags.append(th[name].get(e['verb'][0], e['verb'][0]) if e['verb'] else '-')
    out = {}
    if name in ('wordnet', 'moby'):
        names = {}
        out['given'] = [names.setdefault(b, len(names)) for b in bags]
        table, kbest = {}, len(names)
    else:
        M = block_matrix(bags)
        kbest, table = heldout_k(M, SEED)
        for k in sorted({32, kbest}):
            out[str(k)] = [int(x) for x in spherical(M, k, 50, SEED).labels_]
    return (c, r, name), {'keys': keys, 'clusters': out, 'kbest': kbest, 'table': table}


def cmd_cluster():
    d = load()
    th = thesauri(d)
    pickle.dump(th, open(CACHE + '.th', 'wb'))
    jobs = [(c, r, n) for c in CORPORA for r in READERS for n in ('A', 'C', 'D', 'E', 'wordnet', 'moby')]
    with multiprocessing.Pool(4) as pool:
        res = dict(pool.imap_unordered(cluster_job, jobs))
    out = {'%s|%s|%s' % k: v for k, v in sorted(res.items())}
    json.dump(out, open(os.path.join(HERE, 'Clusters.json'), 'w', encoding='utf-8'), separators=(',', ':'))
    say('# Clusters written before any function label was read; see Clusters.json')
    for k in sorted(out):
        v = out[k]
        for kk, lab in v['clusters'].items():
            n = np.bincount(lab)
            say('%-26s k %-6s largest %.2f%s; k by held-out %s' % (k, kk, n.max() / n.sum(), ' DEGENERATE' if n.max() / n.sum() > 1 / 3 else '', v['kbest']))
    save('clusters')


def cmd_l2():
    d = load()
    lab = d['labels']
    C = json.load(open(os.path.join(HERE, 'Clusters.json'), encoding='utf-8'))
    say('# Leaf-L2.txt -- the clusters, committed before any label was read, against the functions; replication; his strings')
    rng = np.random.default_rng(SEED)
    pr = {s: collections.Counter({k: v for k, v in b.items() if k not in PREP}) for s, b in d['propp'].items()}
    rows = {}
    for c in CORPORA:
        say('## %s' % c)
        say('%-3s %-8s %-7s %-6s %-7s %-7s %-7s %-7s %-7s %-7s' % ('r', 'alphabet', 'k', 'large', 'AMI', 'null95', 'V', 'prec', 'ARI', 'p'))
        for name in ('A', 'wordnet', 'moby', 'C', 'D', 'E'):
            for r in READERS:
                v = C['%s|%s|%s' % (c, r, name)]
                o = C['%s|%s|%s' % (c, 'B' if r == 'A' else 'A', name)]
                keys = [tuple(k) for k in v['keys']]
                for kk, cl in v['clusters'].items():
                    pairs = [(x, primary(lab[(s, r)][e])) for (s, e), x in zip(keys, cl) if lab.get((s, r), {}).get(e)]
                    stories = [s for (s, e), x in zip(keys, cl) if lab.get((s, r), {}).get(e)]
                    xs = [p[0] for p in pairs]
                    ys = [p[1] for p in pairs]
                    ami = adjusted_mutual_info_score(ys, xs)
                    vm = v_measure_score(ys, xs)
                    # the null: labels shuffled within stories
                    by = collections.defaultdict(list)
                    for i, s in enumerate(stories):
                        by[s].append(i)
                    nulls = []
                    for _ in range(100):
                        sh = list(ys)
                        for s, ii in by.items():
                            pp = rng.permutation(ii)
                            for a_, b_ in zip(ii, pp):
                                sh[a_] = ys[b_]
                        nulls.append(adjusted_mutual_info_score(sh, xs))
                    # named by majority on one half of the stories, precision on the other
                    ss = sorted(by)
                    random.Random(SEED).shuffle(ss)
                    half = set(ss[:len(ss) // 2])
                    maj = collections.defaultdict(collections.Counter)
                    for x, y, s in zip(xs, ys, stories):
                        if s in half:
                            maj[x][y] += 1
                    name_of = {x: m.most_common(1)[0][0] for x, m in maj.items()}
                    te = [(name_of.get(x), y) for x, y, s in zip(xs, ys, stories) if s not in half]
                    prec = np.mean([a_ == b_ for a_, b_ in te])
                    # replication over events both readers have
                    okey = {tuple(k): i for i, k in enumerate(o['keys'])}
                    ocl = o['clusters'].get(kk) or (o['clusters'].get('given') if name in ('wordnet', 'moby') else None)
                    ari, p = float('nan'), float('nan')
                    if ocl is not None:
                        ca, cb = [], []
                        for key, x in zip(keys, cl):
                            if key in okey:
                                ca.append(x)
                                cb.append(ocl[okey[key]])
                        ari = adjusted_rand_score(ca, cb)
                        nl = [adjusted_rand_score(rng.permutation(ca), cb) for _ in range(200)]
                        p = (sum(n >= ari for n in nl) + 1) / 201
                    n = np.bincount(cl)
                    large = n.max() / n.sum()
                    say('%-3s %-8s %-7s %.2f   %.3f   %.3f   %.3f   %.3f   %.3f   %.3f' % (r, name, kk, large, ami, float(np.percentile(nulls, 95)), vm, prec, ari, p))
                    rows[(c, r, name, kk)] = dict(ami=ami, null=float(np.percentile(nulls, 95)), prec=float(prec), ari=ari, p=p, large=large)
                    if c == 'tale':
                        # the other half's bags of named clusters against his strings, beside the reader's own bags
                        sim, own = [], []
                        for s in by:
                            if s in half or s not in pr:
                                continue
                            bag = collections.Counter()
                            for x, st in zip(xs, stories):
                                if st == s:
                                    nm = name_of.get(x)
                                    if nm and nm != 'X' and nm not in PREP:
                                        bag[nm] += 1
                            sim.append(cosine(bag, pr[s]))
                            own.append(cosine(reader_bag(lab, s, r), pr[s]))
                        rows[(c, r, name, kk)]['sim'] = float(np.nanmean(sim))
                        rows[(c, r, name, kk)]['own'] = float(np.nanmean(own))
    say('## against his strings, tale by tale, on the half not used for naming (cosine; no X, no preparatory): clusters; the reader\'s own bags; the ratio')
    for k, x in sorted(rows.items()):
        if 'sim' in x:
            say('%s %-8s k %-6s %.3f  %.3f  %.2f' % (k[1], k[2], k[3], x['sim'], x['own'], x['sim'] / x['own']))
    say('## the reasonable answer, second and third parts (D or E, wondertales, both readers)')
    for name in ('D', 'E'):
        for kk in sorted({k[3] for k in rows if k[0] == 'tale' and k[2] == name}, key=str):
            cells = [rows.get(('tale', r, name, kk)) for r in READERS]
            if None in cells:
                continue
            ok1 = all(x['ami'] > x['null'] and x['p'] <= .05 for x in cells)
            ok2 = all(x['sim'] / x['own'] >= .5 for x in cells)
            say('%s k %s: beats the shuffles and replicates: %s (ARI %.3f, %.3f); at least half as close to his strings as the readers\' own: %s (%.2f, %.2f)' % (name, kk, ok1, cells[0]['ari'], cells[1]['ari'], ok2, cells[0]['sim'] / cells[0]['own'], cells[1]['sim'] / cells[1]['own']))
    save('L2')


# ---------------------------------------------------------------- L3
def cmd_l3():
    d = load()
    lab = d['labels']
    th = None
    say('# Leaf-L3.txt -- leaves his list may lack: the events the readers left X, clustered per corpus and reader; a cluster replicates at Jaccard 0.3 or more and stands in at least 10 stories')
    samples = ['# Leaf-L3-samples.txt -- 20 events from each replicating cluster (seeded), for the keeper\'s reading']
    profiles = []
    for c in CORPORA:
        got = {}
        for r in READERS:
            keys, bags, acts, verbs = [], [], [], []
            for s, evs in d['features'].get((c, r), []):
                bb = alphabet_bags(evs, 'D', th)
                for i, e in enumerate(evs):
                    ls = lab.get((s, r), {}).get(e['e'])
                    if ls and all(x == 'X' for x in ls):
                        keys.append((s, e['e']))
                        bags.append(bb[i])
                        acts.append(e['act'])
                        verbs.append(e['verb'])
            M = block_matrix(bags)
            k, _ = heldout_k(M, SEED)
            cl = spherical(M, k, 20, SEED).labels_
            got[r] = dict(keys=keys, cl=cl, acts=acts, verbs=verbs, k=k)
        A, B = got['A'], got['B']
        setsA = collections.defaultdict(set)
        setsB = collections.defaultdict(set)
        for key, x in zip(A['keys'], A['cl']):
            setsA[x].add(key)
        for key, x in zip(B['keys'], B['cl']):
            setsB[x].add(key)
        common = set(A['keys']) & set(B['keys'])
        say('## %s: X events A %d, B %d, both %d; k %d, %d' % (c, len(A['keys']), len(B['keys']), len(common), A['k'], B['k']))
        rng = random.Random(SEED)
        for x, sx in sorted(setsA.items(), key=lambda kv: -len(kv[1])):
            sc = sx & common
            bestj, besty = 0, None
            for y, sy in setsB.items():
                sy = sy & common
                j = len(sc & sy) / max(1, len(sc | sy))
                if j > bestj:
                    bestj, besty = j, y
            stories = {s for s, _ in sx}
            if bestj >= .3 and len(stories) >= 10:
                ia = [i for i, v in enumerate(A['cl']) if v == x]
                ib = [i for i, v in enumerate(B['cl']) if v == besty]
                ta = collections.Counter(a for i in ia for a in A['acts'][i])
                tv = collections.Counter(a for i in ia for a in A['verbs'][i]) + collections.Counter(a for i in ib for a in B['verbs'][i])
                say('kept A%d~B%d: Jaccard %.2f, %d events in %d stories; acts %s; verbs %s' % (x, besty, bestj, len(sx), len(stories), ta.most_common(5), tv.most_common(10)))
                profiles.append((c, x, ta))
                pick = sorted(sc & setsB[besty]) or sorted(sx)
                rng.shuffle(pick)
                samples.append('## %s A%d~B%d: %s' % (c, x, besty, ta.most_common(3)))
                for key in pick[:20]:
                    samples.append('%s ev %d: %s' % (key[0], key[1], d['text'].get(key, '')[:140]))
    say('## found in one corpus only: a kept cluster whose acts are unlike (cosine under 0.5) every kept cluster of the other corpora')
    for c, x, ta in profiles:
        others = [cosine(ta, tb) for c2, _, tb in profiles if c2 != c]
        if not others or max(others) < .5:
            say('%s A%d: %s (closest elsewhere %.2f)' % (c, x, ta.most_common(4), max(others) if others else float('nan')))
    open(os.path.join(HERE, 'Leaf-L3-samples.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(samples) + '\n')
    save('L3')


# ---------------------------------------------------------------- L4
def l4_job(a):
    sys.path.insert(0, HERE)
    import grammar as G
    c, r, name, kk = a
    d = load()
    lab = d['labels']
    strs = []
    if name == 'functions':
        for s, evs in d['features'].get((c, r), []):
            x = [primary(lab[(s, r)][e['e']]) for e in evs if lab.get((s, r), {}).get(e['e'])]
            x = [u for u in x if u != 'X']
            if len(x) >= 3:
                strs.append(x)
    elif name == 'acts':
        for s, evs in d['features'].get((c, r), []):
            x = [e['act'][0] for e in evs if e['act'] and e['act'][0] != 'other']
            if len(x) >= 3:
                strs.append(x)
    else:
        C = json.load(open(os.path.join(HERE, 'Clusters.json'), encoding='utf-8'))
        v = C['%s|%s|%s' % (c, r, name)]
        by = collections.OrderedDict()
        for (s, e), x in zip(v['keys'], v['clusters'][kk]):
            by.setdefault(s, []).append('c%03d' % x)
        strs = [x for x in by.values() if len(x) >= 3]
    f = G.fit(strs)
    return a, {k: f[k] for k in ('shape', 'ordered', 'coverage', 'order', 'symbols', 'method')} | {'n': len(strs), 'len': float(np.mean([len(x) for x in strs])), 'ratio': f['steps']['ratio'], 'cv': f['cv']}


def cmd_l4():
    say('# Leaf-L4.txt -- each alphabet through grammar.py version 3, unchanged. Exploratory; the tool has been shown only on generated strings and his own')
    jobs = [(c, r, n, '32' if n in 'DE' else '') for c in CORPORA for r in READERS for n in ('functions', 'acts', 'D', 'E')]
    with multiprocessing.Pool(4) as pool:
        res = {}
        for a, v in pool.imap_unordered(l4_job, jobs):
            res[a] = v
            print(a, v['shape'], flush=True)
    for c in CORPORA:
        say('## %s' % c)
        for n in ('functions', 'acts', 'D', 'E'):
            kk = '32' if n in 'DE' else ''
            x, y = res[(c, 'A', n, kk)], res[(c, 'B', n, kk)]
            tau = float('nan')
            if n in ('functions', 'acts'):
                common = [u for u in x['order'] if u in y['order']]
                if len(common) >= 3:
                    tau = float(kendalltau([x['order'].index(u) for u in common], [y['order'].index(u) for u in common])[0])
            say('%-10s A %-17s cov %.2f ratio %.2f d%d | B %-17s cov %.2f ratio %.2f d%d | same verdict: %-5s order tau A,B %s | %d stories, %.0f units' % (n, x['shape'], x['coverage'], x['ratio'], x['method'], y['shape'], y['coverage'], y['ratio'], y['method'], x['shape'] == y['shape'], '%.2f' % tau if tau == tau else '-', x['n'], x['len']))
        for r in READERS:
            say('  %s functions order: %s' % (r, ' '.join(res[(c, r, 'functions', '')]['order'])))
    save('L4')


if __name__ == '__main__':
    fns = {'ceil': cmd_ceil, 'l1': cmd_l1, 'cluster': cmd_cluster, 'l2': cmd_l2, 'l3': cmd_l3, 'l4': cmd_l4}
    if len(sys.argv) != 2 or sys.argv[1] not in fns:
        sys.exit(__doc__)
    fns[sys.argv[1]]()
