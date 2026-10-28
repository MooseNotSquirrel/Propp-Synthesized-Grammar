#!/usr/bin/env python3
"""
storyGrammar.py -- the probabilistic story grammar (StoryGrammar/StoryGrammarProtocol.md, frozen 2026-10-28, the five
recommended decisions taken; the held-out stories in StoryGrammar/HeldOut.txt).

  python storyGrammar.py dry    the data and the alternatives counted, and one transcriber's features timed; no weights fitted
  python storyGrammar.py g1     test G1: planted weights recovered (signs, and a rank correlation of at least 0.9)
  python storyGrammar.py g2     test G2: Blocks/ConstraintWeights-*.txt reproduced by this program's fitting engine
  python storyGrammar.py g3     test G3: the held-out stories' functions replaced by noise give the same weights
  python storyGrammar.py g4     test G4: two fits byte-identical
  python storyGrammar.py run    fit per transcriber, write StoryGrammar/Weights-A.txt, Weights-B.txt and StoryGrammarRun.txt
                                (the record: refused if it exists and would change), and score predictions 1 and 2

The tests g3 and g4 fit on the real stories but print only whether the weights agree, never the weights.

THE MODEL (section 2): contrastive. A story's sequence is scored against alternatives built from it: its functions reordered
within each move, or the same with one function dropped, or one added from its corpus's pool (the units of that corpus's
fitting stories). The loss is constraintGrammar.py's: for each pair of the real story and one alternative, the logistic loss of
the alternative's weighted violations minus the story's, each story weighted 1 over its number of versions and each of its
alternatives 1 over their number, with an L2 penalty of 1.0 on every weight, by L-BFGS-B from zero. Higher weighted violation
is less grammatical.

THE UNITS: a row's keys by tragedyScore.key, those in tragedyScore.NUM, from rows marked Y (every myth row, as the myths carry
no mark), X left out, in the order of the rows; each unit keeps its row's move. The myths are the library's stories (L1- to
L3-), the 126 of section 5, as Blocks/parity.py reads them; the Epitome's stories (E-) are not in the corpus. Stories of fewer than three units are left out,
as constraintGrammar.py leaves them out.

THE FEATURES (section 3), each a violation:
  1. v46: the share of the moves that ProppEBNF46.txt does not accept at `move` (each move built as the tragedy test builds it:
     the first move's preparatory units before its first A, a or B removed), and the repairs per unit, a repair being the
     deletion of the unit where the parse halts (the last unit when it halts at the move's end), repeated until it accepts.
  2, 3. constraintGrammar.py's 45 section orders and its 9 pair orders and 9 pair cohesions, on the whole sequence, unchanged.
  4. Propp's pairs in order within the move, the 12 of Ngrams/ngrams.py: for each pair, its first with no second after it in
     the same move, and its second with no first before it, per unit (CrossCultureProtocol.md section 8's pairing).
  5. The blocks: the share of units outside blocks, by blockStream.py's transform (the blocks reading) and coverage.
  6. The candidate groups (StoryGrammar/Candidates.md) are not included: the threat, the demand, the request and their
     answers have no letter among Propp's functions, so by section 3 they wait.
  7. Length, a control: the number of units and of moves, each over 10.

THE WEIGHTS (section 4): shared weights plus an offset per corpus for each feature, the five corpora as the genres; a story's
weights are the shared plus its corpus's offset. Per transcriber.
"""
import collections
import os
import random
import re
import sys
import time

import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'FailedHero'))
sys.path.insert(0, os.path.join(ROOT, 'Blocks'))
import failedHero as F  # noqa: E402
import parity as BP  # noqa: E402  (changes the working directory to ROOT)
import constraintGrammar as CG  # noqa: E402
import parse  # noqa: E402
import importlib.util  # noqa: E402

C, DT, TS, BS = F.C, F.DT, F.TS, BP.BS
_ng = importlib.util.spec_from_file_location('ngrams', os.path.join(ROOT, 'Ngrams', 'ngrams.py'))
NG = importlib.util.module_from_spec(_ng)
_ng.loader.exec_module(NG)
PAIRS = NG.PROPP_PAIRS
CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'myth']
HELD = os.path.join(HERE, 'HeldOut.txt')
WEIGHTS = os.path.join(HERE, 'Weights-%s.txt')
RECORD = os.path.join(HERE, 'StoryGrammarRun.txt')
ALTS, TEST_ALTS, SEED, L2, FLIPS = 100, 200, 46, 1.0, 10000
FEATURES = (['v46: move not accepted', 'v46: repairs per unit'] + list(CG.FEATURES) +
            ['%s then %s within the move' % p for p in PAIRS] + ['outside blocks'] + ['length: units', 'length: moves'])
NF = len(FEATURES)
LENGTH = [NF - 2, NF - 1]
GV = TS.grammar(False)
GB = BS.Grammar()


# ---------------------------------------------------------------- the data
def held_out():
    out = {}
    for line in open(HELD, encoding='utf-8'):
        m = re.match(r'^(\w+) \d+ of \d+: (.*)$', line.strip())
        if m:
            out[m.group(1)] = set(m.group(2).split())
    return out


def load(L, noise=False):
    """{corpus: {'fit': [...], 'held': [...]}}, each item (story, weight, units, moves). With noise, every held-out row's
    function is replaced by a random letter before anything else is done with it (test G3)."""
    H = held_out()
    nr = random.Random(SEED + 1)
    out = {}
    for g in CORPORA:
        seqs = collections.OrderedDict()
        for r in DT.files('functions', C.PATS[g], L):
            s = DT.local(r['story'])
            if g == 'myth' and not re.match(r'^L\d-\d{3}$', s):
                continue
            raw = r['raw']
            if noise and s in H[g]:
                raw = nr.choice(CG.UNITS + ['X'])
                raw = {'up': '↑', 'down': '↓'}.get(raw, raw)
            y = g == 'myth' or r['matters'].upper().startswith('Y')
            us, ms = seqs.setdefault((s, r['version']), ([], []))
            if y:
                for k in TS.key(raw):
                    if k in TS.NUM:
                        us.append(k)
                        ms.append(r['move'])
        n = collections.Counter(s for s, v in seqs)
        part = {'fit': [], 'held': []}
        for (s, v), (us, ms) in seqs.items():
            if len(us) >= 3:
                part['held' if s in H[g] else 'fit'].append((s, 1.0 / n[s], us, ms))
        out[g] = part
    return out


def pool(items):
    return sorted(u for _, _, us, _ in items for u in us)


# ---------------------------------------------------------------- the alternatives
def reorder(us, ms, rng):
    us, out = list(us), list(us)
    for m in sorted(set(ms)):
        at = [i for i, x in enumerate(ms) if x == m]
        p = rng.permutation(len(at))
        for i, j in zip(at, p):
            out[i] = us[at[j]]
    return out, list(ms)


def alternative(us, ms, pl, rng):
    kind = int(rng.integers(3))
    us, ms = list(us), list(ms)
    if kind == 1 and len(us) > 3:
        i = int(rng.integers(len(us)))
        del us[i], ms[i]
    elif kind == 2:
        i = int(rng.integers(len(us) + 1))
        us.insert(i, pl[int(rng.integers(len(pl)))])
        ms.insert(i, ms[i - 1] if i > 0 else ms[0])
    return reorder(us, ms, rng)


def alternatives(us, ms, pl, K, rng):
    return [alternative(us, ms, pl, rng) for _ in range(K)]


# ---------------------------------------------------------------- the features
def moves_of(us, ms):
    by = collections.OrderedDict()
    for u, m in zip(us, ms):
        by.setdefault(m, []).append(u)
    out = list(by.values())
    if out:
        mv = out[0]
        first = next((i for i, u in enumerate(mv) if u in ('A', 'a', 'B')), None)
        if first is None:
            first = 0
            while first < len(mv) and mv[first] in TS.PREP:
                first += 1
        out[0] = [u for i, u in enumerate(mv) if not (i < first and u in TS.PREP)]
    return out


def repairs(toks):
    toks, k = list(toks), 0
    while toks:
        ok, pos, _ = parse.accept(toks, GV.bnf, GV.start, GV.table)
        if ok:
            return k
        del toks[min(pos, len(toks) - 1)]
        k += 1
    return k


def unpaired(us, ms):
    by = collections.defaultdict(list)
    for u, m in zip(us, ms):
        by[m].append(u)
    out = []
    for a, b in PAIRS:
        k = 0
        for fs in by.values():
            for i, f in enumerate(fs):
                k += (f == a and b not in fs[i + 1:]) + (f == b and a not in fs[:i])
        out.append(k / len(us))
    return out


def features(us, ms):
    mvs = [m for m in moves_of(us, ms) if m]
    rep = [repairs(m) for m in mvs]
    v46 = [sum(1 for r in rep if r) / max(1, len(mvs)), sum(rep) / len(us)]
    cg = list(CG.features(np.array([[CG.UI[u] for u in us]]))[0])
    i, t = BS.coverage(BS.transform(list(us), GB, 'blocks'))
    return np.array(v46 + cg + unpaired(us, ms) + [1.0 - i / max(1, t)] + [len(us) / 10.0, len(set(ms)) / 10.0])


# ---------------------------------------------------------------- the fit
def engine(D, W, l2=L2):
    """constraintGrammar.py's fit: the logistic loss of D @ w, weighted by W, with an L2 penalty, by L-BFGS-B from zero"""
    def loss(w):
        z = D @ w
        l = np.logaddexp(0, -z)
        g = -(W * (1 / (1 + np.exp(z))))[:, None] * D
        return (W * l).sum() + 0.5 * l2 * w @ w, g.sum(axis=0) + l2 * w
    return minimize(loss, np.zeros(D.shape[1]), jac=True, method='L-BFGS-B').x


def design(diffs, genre):
    """shared columns, then one block of offset columns per corpus, the story's own filled"""
    X = np.zeros((diffs.shape[0], NF * (1 + len(CORPORA))))
    X[:, :NF] = diffs
    j = 1 + CORPORA.index(genre)
    X[:, NF * j:NF * (j + 1)] = diffs
    return X


def contrasts(data, K=ALTS, seed=SEED):
    """the fitting design for one transcriber: rows of alternative-minus-story features, with weights"""
    rng = np.random.default_rng(seed)
    Ds, Ws = [], []
    for g in CORPORA:
        pl = pool(data[g]['fit'])
        for s, w, us, ms in data[g]['fit']:
            fr = features(us, ms)
            fa = np.array([features(a, b) for a, b in alternatives(us, ms, pl, K, rng)])
            Ds.append(design(fa - fr, g))
            Ws.append(np.full(K, w / K))
    return np.vstack(Ds), np.concatenate(Ws)


def fit(L, noise=False):
    D, W = contrasts(load(L, noise))
    return engine(D, W)


def weights_of(w, g):
    j = 1 + CORPORA.index(g)
    return w[:NF] + w[NF * j:NF * (j + 1)]


def weights_text(L, w):
    out = ['# Weights-%s.txt -- storyGrammar.py, transcriber %s: the shared weight and each corpus\'s offset, per feature.' % (L, L),
           '# positive, the stories keep the constraint; negative, they prefer to break it. The length weights are a control.',
           '%-48s %8s ' % ('feature', 'shared') + ' '.join('%8s' % g for g in CORPORA)]
    for i, f in enumerate(FEATURES):
        out.append('%-48s %+8.3f ' % (f, w[i]) + ' '.join('%+8.3f' % w[NF * (1 + j) + i] for j in range(len(CORPORA))))
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- the tests
def g1():
    """planted shared weights, drawn by a fixed seed; for each of transcriber A's fitting stories, its story and ALTS
    alternatives are the candidates, and REPLICATES sequences are drawn from them in proportion to exp(-w . f); the fit, on
    each drawn sequence against the other candidates, must recover the planted weights' signs (those of at least 1 in size)
    and their order, a rank correlation of at least 0.9 over all the shared weights"""
    REPLICATES, SCALE = 5, 3.0
    rng = np.random.default_rng(SEED + 2)
    planted = rng.normal(0, SCALE, NF)
    data = load('A')
    Ds, Ws = [], []
    for g in CORPORA:
        pl = pool(data[g]['fit'])
        for s, w, us, ms in data[g]['fit']:
            cand = np.array([features(us, ms)] + [features(a, b) for a, b in alternatives(us, ms, pl, ALTS, rng)])
            e = -(cand @ planted)
            p = np.exp(e - e.max())
            p /= p.sum()
            for _ in range(REPLICATES):
                c = int(rng.choice(len(cand), p=p))
                rest = np.delete(cand, c, axis=0)
                Ds.append(design(rest - cand[c], g))
                Ws.append(np.full(len(rest), w / len(rest)))
    w = engine(np.vstack(Ds), np.concatenate(Ws))[:NF]
    rho = spearmanr(planted, w).correlation
    big = np.abs(planted) >= 1.0
    signs = int((np.sign(w[big]) == np.sign(planted[big])).sum())
    ok = rho >= 0.9 and signs == int(big.sum())
    print('G1 planted weights: rank correlation %.3f (at least 0.9); signs recovered %d of %d planted at 1 or more' % (rho, signs, int(big.sum())))
    print('G1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def g2():
    """constraintGrammar.py's fit, its data, alternatives and features, through this program's engine; compared with the
    published weights file line by line (constraintGrammar.fit is not called, as it writes those files)"""
    ok = True
    for genre in CG.GENRES:
        rng = np.random.default_rng(CG.SEED)
        D, W = [], []
        for L in 'AB':
            for v, w, s in CG.stories(genre, 'fit', L):
                P, real = CG.perms(s, CG.FIT_PERMS, rng)
                D.append(CG.features(P) - CG.features(real))
                W.append(np.full(CG.FIT_PERMS, w / CG.FIT_PERMS))
        w = engine(np.vstack(D), np.concatenate(W), CG.L2)
        got = ['%+8.2f | %s' % (w[i], CG.FEATURES[i]) for i in np.argsort(-np.abs(w))]
        path = os.path.join(ROOT, 'Blocks', 'ConstraintWeights-%s.txt' % genre)
        want = [l.rstrip('\n') for l in open(path, encoding='utf-8') if '|' in l and not l.startswith('#')]
        same = sorted(got) == sorted(want)
        ok &= same
        print('G2 %-10s %d weights against %s: %s' % (genre, len(got), os.path.basename(path), 'identical' if same else 'DIFFER'))
    print('G2 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def g3():
    ok = True
    for L in 'AB':
        same = weights_text(L, fit(L)) == weights_text(L, fit(L, noise=True))
        changed = sum(1 for g, d in load(L).items() for x, y in zip(d['held'], load(L, True)[g]['held']) if x[2] != y[2])
        ok &= same
        print('G3 %s held-out stories changed by the noise: %d; weights with and without the noise: %s' % (L, changed, 'identical' if same else 'DIFFER'))
    print('G3 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def g4():
    ok = True
    for L in 'AB':
        same = weights_text(L, fit(L)) == weights_text(L, fit(L))
        ok &= same
        print('G4 %s two fits: %s' % (L, 'byte-identical' if same else 'DIFFER'))
    print('G4 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def dry():
    for L in 'AB':
        data = load(L)
        for g in CORPORA:
            f, h = data[g]['fit'], data[g]['held']
            print('dry %s %-8s fitting %3d stories (%3d versions, %5d units); held out %2d stories (%2d versions); %d alternatives each'
                  % (L, g, len({x[0] for x in f}), len(f), sum(len(x[2]) for x in f), len({x[0] for x in h}), len(h), ALTS))
    data = load('A')
    t = time.time()
    n = 0
    for g in CORPORA:
        for s, w, us, ms in data[g]['fit'][:5]:
            features(us, ms)
            n += 1
    print('dry %d feature vectors in %.2f s; %d features; %d weights per transcriber' % (n, time.time() - t, NF, NF * (1 + len(CORPORA))))


# ---------------------------------------------------------------- the run: predictions 1 and 2
def concordance(w, us, ms, pl, rng, K=TEST_ALTS):
    """the share of the story's alternatives it outscores (lower weighted violation), ties a half; and the mean log
    likelihood of the story against them"""
    fr = features(us, ms) @ w
    fa = np.array([features(a, b) for a, b in alternatives(us, ms, pl, K, rng)]) @ w
    c = float(((fa > fr).sum() + 0.5 * (fa == fr).sum()) / K)
    return c, float(-np.logaddexp(0, -(fa - fr)).mean())


def flip_test(vals):
    """constraintGrammar.evaluate's sign-flip test on the weighted concordances"""
    tw = sum(w for w, _ in vals)
    d = [(w, x - 0.5) for w, x in vals]
    obs = sum(w * x for w, x in d) / tw
    r = random.Random(SEED)
    hits = sum(1 for _ in range(FLIPS) if sum(w * (x if r.random() < 0.5 else -x) for w, x in d) / tw >= obs - 1e-12)
    return sum(w * x for w, x in vals) / tw, (hits + 1) / (FLIPS + 1.0)


def balanced(pred, true):
    return float(np.mean([np.mean([p == g for p, t in zip(pred, true) if t == g]) for g in CORPORA if g in true]))


def length_classifier(data):
    """length alone: per corpus, a normal on the log of the units and the log of the moves of its fitting versions; equal priors"""
    par = {}
    for g in CORPORA:
        X = np.array([[np.log(len(us)), np.log(len(set(ms)))] for _, _, us, ms in data[g]['fit']])
        par[g] = (X.mean(axis=0), X.std(axis=0) + 0.05)

    def cls(story_versions):
        x = np.mean([[np.log(len(us)), np.log(len(set(ms)))] for us, ms in story_versions], axis=0)
        return max(CORPORA, key=lambda g: -(((x - par[g][0]) / par[g][1]) ** 2 / 2 + np.log(par[g][1])).sum())
    return cls


def verdict(a, b):
    return 'HOLDS' if a and b else 'SPLIT' if a or b else 'FAILS'


def run():
    rep = ['# StoryGrammarRun.txt -- storyGrammar.py run, StoryGrammarProtocol.md section 7: predictions 1 and 2 on the held-out stories '
           '(HeldOut.txt), per transcriber; the weights in Weights-A.txt and Weights-B.txt', '']
    p1, p2, texts = {}, {}, {}
    for L in 'AB':
        data = load(L)
        w = fit(L)
        texts[L] = weights_text(L, w)
        rep.append('TRANSCRIBER %s' % L)
        rep.append('Prediction 1: held-out stories against %d alternatives each, under their own corpus\'s weights' % TEST_ALTS)
        cells = []
        for g in CORPORA:
            rng = np.random.default_rng(SEED + 10)
            pl = pool(data[g]['fit'])
            vals = [(wt, concordance(weights_of(w, g), us, ms, pl, rng)[0]) for s, wt, us, ms in data[g]['held']]
            m, p = flip_test(vals)
            cell = m > 0.5 and p <= 0.05
            cells.append(cell)
            rep.append('  %-8s %2d versions: concordance %.3f (p %.4f) %s' % (g, len(vals), m, p, 'holds' if cell else 'does not hold'))
        p1[L] = all(cells)
        rep.append('  prediction 1 for %s: %s in every corpus' % (L, 'holds' if p1[L] else 'does not hold'))
        allpool = sorted(u for g in CORPORA for u in pool(data[g]['fit']))
        cls = length_classifier(data)
        true, pred, plen = [], [], []
        for g in CORPORA:
            by = collections.OrderedDict()
            for s, wt, us, ms in data[g]['held']:
                by.setdefault(s, []).append((us, ms))
            for s, vs in by.items():
                ll = {}
                for h in CORPORA:
                    rng = np.random.default_rng(SEED + 20)
                    ll[h] = np.mean([concordance(weights_of(w, h), us, ms, allpool, rng)[1] for us, ms in vs])
                true.append(g)
                pred.append(max(CORPORA, key=lambda h: ll[h]))
                plen.append(cls(vs))
        ba, bl = balanced(pred, true), balanced(plen, true)
        r = random.Random(SEED)
        hit_c = hit_l = 0
        for _ in range(FLIPS):
            t = list(true)
            r.shuffle(t)
            hit_c += balanced(pred, t) >= ba - 1e-12
            sw = [(b, a) if r.random() < 0.5 else (a, b) for a, b in zip(pred, plen)]
            hit_l += balanced([a for a, _ in sw], true) - balanced([b for _, b in sw], true) >= ba - bl - 1e-12
        pc, pl_ = (hit_c + 1) / (FLIPS + 1.0), (hit_l + 1) / (FLIPS + 1.0)
        p2[L] = pc <= 0.05 and ba > bl and pl_ <= 0.05
        rep.append('Prediction 2: the genre named by the best-scoring weights, %d held-out stories, five corpora (chance 0.2)' % len(true))
        rep.append('  balanced accuracy %.3f (p %.4f against chance); length alone %.3f; the grammar beyond length p %.4f -> %s'
                   % (ba, pc, bl, pl_, 'holds' if p2[L] else 'does not hold'))
        conf = collections.Counter(zip(true, pred))
        rep.append('  named (rows the corpus, columns the genre named): ' + '; '.join(
            '%s %s' % (g, ' '.join('%d' % conf[g, h] for h in CORPORA)) for g in CORPORA))
        rep.append('  length weights (reported, a control): units %+.3f, moves %+.3f, shared' % (w[LENGTH[0]], w[LENGTH[1]]))
        rep.append('')
    rep.append('VERDICTS')
    rep.append('  prediction 1, the held-out stories: %s' % verdict(p1['A'], p1['B']))
    rep.append('  prediction 2, the genre beyond length: %s' % verdict(p2['A'], p2['B']))
    text = '\n'.join(rep) + '\n'
    for path, t in [(WEIGHTS % 'A', texts['A']), (WEIGHTS % 'B', texts['B']), (RECORD, text)]:
        if os.path.exists(path) and open(path, encoding='utf-8').read() != t:
            raise SystemExit('refusing to overwrite the record %s with different content' % path)
    for path, t in [(WEIGHTS % 'A', texts['A']), (WEIGHTS % 'B', texts['B']), (RECORD, text)]:
        open(path, 'w', encoding='utf-8', newline='\n').write(t)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'dry': dry, 'g1': g1, 'g2': g2, 'g3': g3, 'g4': g4, 'run': run}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    res = cmds[a[0]]()
    sys.exit(0 if res in (None, True) else 1)
