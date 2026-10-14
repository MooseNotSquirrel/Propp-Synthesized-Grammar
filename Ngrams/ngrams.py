#!/usr/bin/env python3
"""
ngrams.py -- the frequency analysis of function and act strings (NgramProtocol.md).

  python ngrams.py discover   the discovery half: writes Ngrams/Discovery.txt and the candidate
                              list Ngrams/Candidates.txt
  python ngrams.py confirm    the confirmation half, on the committed candidate list:
                              writes Ngrams/ConfirmRun.txt
  python ngrams.py describe   all stories: rank and frequency, entropy against shuffles, and
                              frequency against genre; writes Ngrams/DescribeRun.txt
  python ngrams.py selftest   the statistics on planted strings, to prove them

Written in full before any string was counted.
"""
import collections
import glob
import math
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
sys.path.insert(0, os.path.join(ROOT, 'TwoLayer'))
sys.path.insert(0, os.path.join(ROOT, 'Problems'))
import tragedyScore as TS  # noqa: E402
import twoLayer as T  # noqa: E402
import problems as Pm  # noqa: E402

GENRES = ('tale', 'fable', 'tragedy')
SEED = 46
SHUFFLES = 1000
MAX_GAP = 6
NEAR = (2, 3, 4)
# discovery thresholds, and confirmation's
MIN_COUNT, MIN_LIFT, DISCOVER_P, CONFIRM_P = 5, 1.5, 0.01, 0.05

# Propp's pairs, as the v46 grammar's blocks and the move's frame bind them, and their counterparts among the acts
PROPP_PAIRS = [('γ', 'δ'), ('ε', 'ζ'), ('η', 'θ'), ('D', 'E'), ('E', 'F'), ('H', 'I'), ('Pr', 'Rs'), ('M', 'N'),
               ('A', 'K'), ('a', 'K'), ('Q', 'Ex'), ('Ex', 'U')]
ACT_PAIRS = [('forbid', 'disobey'), ('seek-information', 'reveal-information'), ('deceive', 'be-taken-in'),
             ('test', 'respond'), ('respond', 'give'), ('fight', 'win'), ('pursue', 'escape'), ('set-task', 'do-task'),
             ('harm', 'repair'), ('want', 'repair'), ('recognize', 'expose'), ('expose', 'punish')]


# ---------------------------------------------------------------- the strings
def function_token(sym):
    b = TS.base(sym)
    if b in ('X', 'α', ''):
        return None
    return b + ('−' if TS.negative(sym) else '')


def function_strings():
    """{L: {story: [function tokens in text order]}}, the original transcriptions: the 45 tales (arm U), the
    199 fables (Propp-Aesop and Propp-Fables), the 32 tragedies"""
    pats = ['Afanasyev/transcriptions/U/%s/b*/Notes.txt', 'Aesop/transcriptions/%s/b*/Notes.txt',
            'Fables/transcriptions/%s/b*/Notes.txt', 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt']
    out = {}
    for L in 'AB':
        st = collections.OrderedDict()
        for pat in pats:
            for path in sorted(glob.glob(os.path.join(P, pat % L))):
                for line in open(path, encoding='utf-8'):
                    f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
                    if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
                        continue
                    s = f[0].split('/')[0]
                    st.setdefault(s, [])
                    tok = function_token(f[4])
                    if tok:
                        st[s].append(tok)
        out[L] = st
    return out


def act_strings():
    """{L: {story: [acts in text order]}}, `other` left out: the two-layer test's stories and the problem test's"""
    out = {}
    for L in 'AB':
        st = collections.OrderedDict()
        raw = T.read_acts(sorted(p for g in GENRES for p in glob.glob(os.path.join(T.OUT, g, 'acts', L, '*', 'Notes.txt'))))
        for (s, ev) in sorted(raw):
            st.setdefault(s, []).extend(a for a, _, _, _ in raw[(s, ev)] if a in T.ACTS and a != 'other')
        for g, bs in Pm.material().items():
            for b in bs:
                rows, _ = Pm.act_lines(L, b)
                for r in rows:
                    if r[2] in T.ACTS and r[2] != 'other':
                        st.setdefault(r[0], []).append(r[2])
        out[L] = st
    return out


def genre(s):
    return 'tale' if s.startswith('A') else 'fable' if s.startswith('F') else 'tragedy'


def split(stories):
    """{story: 'discovery' or 'confirmation'}: within each genre, sorted, shuffled with SEED, the first half discovery"""
    out = {}
    for g in GENRES:
        ids = sorted(s for s in stories if genre(s) == g)
        random.Random(SEED).shuffle(ids)
        h = (len(ids) + 1) // 2
        for i, s in enumerate(ids):
            out[s] = 'discovery' if i < h else 'confirmation'
    return out


# ---------------------------------------------------------------- the counts
class Corpus:
    """a set of strings coded as integers, with within-story shuffles"""

    def __init__(self, strings):
        self.stories = [s for s in strings if strings[s]]
        self.vocab = sorted({t for s in self.stories for t in strings[s]})
        self.index = {t: i for i, t in enumerate(self.vocab)}
        self.V = len(self.vocab)
        seq, sid = [], []
        for k, s in enumerate(self.stories):
            seq += [self.index[t] for t in strings[s]]
            sid += [k] * len(strings[s])
        self.seq = np.array(seq, dtype=np.int64)
        self.sid = np.array(sid, dtype=np.int64)

    def pair_counts(self, seq, d):
        """counts of (x, y) with y exactly d places after x in the same story, as a V*V array"""
        if len(seq) <= d:
            return np.zeros((self.V, self.V))
        same = self.sid[:-d] == self.sid[d:]
        idx = seq[:-d][same] * self.V + seq[d:][same]
        return np.bincount(idx, minlength=self.V * self.V).reshape(self.V, self.V).astype(float)

    def shuffled(self, rng):
        keys = self.sid * 2.0 + rng.random(len(self.seq))
        return self.seq[np.argsort(keys, kind='stable')]

    def gap_stats(self, gaps, shuffles, seed):
        """{gap class: (observed, null mean, p upper)} for the classes 1..MAX_GAP and 'near'"""
        classes = {d: (d,) for d in gaps}
        classes['near'] = NEAR
        obs = {c: sum(self.pair_counts(self.seq, d) for d in ds) for c, ds in classes.items()}
        tot = {c: np.zeros_like(o) for c, o in obs.items()}
        ge = {c: np.zeros_like(o) for c, o in obs.items()}
        rng = np.random.default_rng(seed)
        for _ in range(shuffles):
            sh = self.shuffled(rng)
            per = {d: self.pair_counts(sh, d) for d in set(d for ds in classes.values() for d in ds)}
            for c, ds in classes.items():
                n = sum(per[d] for d in ds)
                tot[c] += n
                ge[c] += n >= obs[c]
        return {c: (obs[c], tot[c] / shuffles, (ge[c] + 1) / (shuffles + 1)) for c in classes}


def stats_for(strings, part, gaps=(1,), shuffles=SHUFFLES):
    """{L: (Corpus, gap stats)} for the stories in one half ('discovery', 'confirmation' or 'all')"""
    out = {}
    for L in 'AB':
        sp = split(strings[L])
        sub = {s: v for s, v in strings[L].items() if part == 'all' or sp[s] == part}
        c = Corpus(sub)
        out[L] = (c, c.gap_stats(gaps, shuffles, SEED))
    return out


def cell(st, L, c, x, y):
    corpus, gs = st[L]
    if x not in corpus.index or y not in corpus.index:
        return 0.0, 0.0, 1.0
    i, j = corpus.index[x], corpus.index[y]
    o, m, p = gs[c]
    return o[i, j], m[i, j], p[i, j]


def lift(o, m):
    return o / m if m > 0 else float('inf') if o > 0 else 0.0


# ---------------------------------------------------------------- discovery and confirmation
LAYERS = (('functions', function_strings), ('acts', act_strings))


def discover():
    rep = ['# Discovery.txt -- ngrams.py discover: the discovery half of every corpus, as NgramProtocol.md freezes it.', '']
    cands = []
    for layer, reader in LAYERS:
        strings = reader()
        st = stats_for(strings, 'discovery')
        rep.append('%s: discovery stories A %d, B %d; vocabulary A %d, B %d'
                   % (layer, len(st['A'][0].stories), len(st['B'][0].stories), st['A'][0].V, st['B'][0].V))
        for c in (1, 'near'):
            found = []
            vocab = sorted(set(st['A'][0].vocab) & set(st['B'][0].vocab))
            for x in vocab:
                for y in vocab:
                    if x == y:
                        continue
                    ok, cells = True, []
                    for L in 'AB':
                        o, m, p = cell(st, L, c, x, y)
                        ok = ok and o >= MIN_COUNT and lift(o, m) >= MIN_LIFT and p <= DISCOVER_P
                        cells.append((o, lift(o, m), p))
                    if ok:
                        found.append((x, y, cells))
            name = 'adjacent' if c == 1 else 'near (2 to 4 apart)'
            rep.append('  %s: %d candidates' % (name, len(found)))
            for x, y, cells in sorted(found, key=lambda f: -min(f[2][0][1], f[2][1][1])):
                rep.append('    %s -> %s   %s' % (x, y, '; '.join('%s n %d lift %.2f p %.4f' % (L, o, l, p) for L, (o, l, p) in zip('AB', cells))))
                cands.append('%s | %s | %s | %s' % (layer, 'adjacent' if c == 1 else 'near', x, y))
        rep.append('')
    open(os.path.join(HERE, 'Discovery.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    open(os.path.join(HERE, 'Candidates.txt'), 'w', encoding='utf-8', newline='\n').write(
        '# Candidates.txt -- ngrams.py discover; the confirmation reads this list, committed before it runs.\n' + '\n'.join(cands) + '\n')
    print('\n'.join(rep))


def gap_profile(st, x, y):
    """lift at gaps 1..MAX_GAP, the mean of A and B"""
    out = []
    for d in range(1, MAX_GAP + 1):
        ls = [lift(*cell(st, L, d, x, y)[:2]) for L in 'AB']
        out.append(sum(ls) / 2)
    return out


def shape(prof):
    peak = max(range(len(prof)), key=lambda i: prof[i]) + 1
    if prof[-1] >= MIN_LIFT:
        return 'long (lift %.1f still at %d apart)' % (prof[-1], MAX_GAP)
    return 'adjacent' if peak == 1 else 'spaced (peak %d apart)' % peak


def confirm():
    cands = [tuple(x.strip() for x in l.split('|')) for l in open(os.path.join(HERE, 'Candidates.txt'), encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    rep = ['# ConfirmRun.txt -- ngrams.py confirm: the confirmation half, on the committed candidates, as NgramProtocol.md freezes it.', '']
    confirmed = {layer: set() for layer, _ in LAYERS}
    stats = {}
    for layer, reader in LAYERS:
        strings = reader()
        st = stats_for(strings, 'confirmation', gaps=tuple(range(1, MAX_GAP + 1)))
        stats[layer] = st
        rep.append('%s: confirmation stories A %d, B %d' % (layer, len(st['A'][0].stories), len(st['B'][0].stories)))
        for lay, cls, x, y in cands:
            if lay != layer:
                continue
            c = 1 if cls == 'adjacent' else 'near'
            cells = [cell(st, L, c, x, y) for L in 'AB']
            ok = all(lift(o, m) > 1 and p <= CONFIRM_P for o, m, p in cells)
            if ok:
                confirmed[layer].add((x, y))
            prof = gap_profile(st, x, y)
            rep.append('  %-9s %s -> %s  %s   %s   profile %s, %s' % (
                cls, x, y, 'CONFIRMED' if ok else 'not confirmed',
                '; '.join('%s n %d lift %.2f p %.4f' % (L, o, lift(o, m), p) for L, (o, m, p) in zip('AB', cells)),
                ' '.join('%.1f' % v for v in prof), shape(prof)))
        rep.append('')
    rep.append('PREDICTIONS (NgramProtocol.md)')
    for i, (layer, pairs, what) in enumerate((('functions', PROPP_PAIRS, "Propp's pairs among the functions"),
                                              ('acts', ACT_PAIRS, "their counterparts among the acts")), 1):
        st = stats[layer]
        eligible = [pr for pr in pairs if all(cell(st, L, 1, *pr)[0] + sum(cell(st, L, d, *pr)[0] for d in NEAR) >= MIN_COUNT for L in 'AB')]
        hit = [pr for pr in eligible if pr in confirmed[layer]]
        ok = len(eligible) > 0 and 2 * len(hit) >= len(eligible)
        rep.append('  %d. at least half of %s that occur at least %d times (adjacent or near) for both transcribers are confirmed: '
                   '%d of %d -> %s' % (i, what, MIN_COUNT, len(hit), len(eligible), 'HOLDS' if ok else 'FAILS'))
        rep.append('     confirmed: %s; not: %s' % (', '.join('%s->%s' % p for p in hit) or '-',
                                                     ', '.join('%s->%s' % p for p in eligible if p not in hit) or '-'))
    new = sorted(confirmed['acts'] - set(ACT_PAIRS))
    rep.append('  3. at least one confirmed pair of acts is not a counterpart of Propp\'s pairs: %d -> %s'
               % (len(new), 'HOLDS' if new else 'FAILS'))
    rep.append('     %s' % (', '.join('%s->%s' % p for p in new) or '-'))
    open(os.path.join(HERE, 'ConfirmRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


# ---------------------------------------------------------------- description: frequency, entropy, genre
def ngram_counts(strings, n):
    c = collections.Counter()
    for s, seq in strings.items():
        for i in range(len(seq) - n + 1):
            c[tuple(seq[i:i + n])] += 1
    return c


def zipf_slope(counts):
    f = sorted(counts.values(), reverse=True)
    if len(f) < 3:
        return float('nan')
    xs = [math.log(r) for r in range(1, len(f) + 1)]
    ys = [math.log(v) for v in f]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)


def cond_entropy(strings):
    """H(next | current) in bits, over adjacent pairs within stories"""
    pc = ngram_counts(strings, 2)
    first = collections.Counter()
    for (x, _), n in pc.items():
        first[x] += n
    tot = float(sum(pc.values()))
    return -sum(n / tot * math.log2(n / first[x]) for (x, _), n in pc.items()) if tot else float('nan')


def shuffle_strings(strings, rnd):
    out = {}
    for s, seq in strings.items():
        q = list(seq)
        rnd.shuffle(q)
        out[s] = q
    return out


def specificity(strings, n, labels):
    """{n-gram: (count, over-representation in its most common genre)}"""
    by = {g: collections.Counter() for g in GENRES}
    for s, seq in strings.items():
        for i in range(len(seq) - n + 1):
            by[labels[s]][tuple(seq[i:i + n])] += 1
    tot = {g: float(sum(c.values())) for g, c in by.items()}
    alltot = sum(tot.values())
    out = {}
    for k in set().union(*by.values()):
        cnt = sum(by[g][k] for g in GENRES)
        out[k] = (cnt, max((by[g][k] / cnt) / (tot[g] / alltot) for g in GENRES if tot[g]))
    return out


def describe():
    rep = ['# DescribeRun.txt -- ngrams.py describe: all stories; the frequency analysis as NgramProtocol.md freezes it.', '']
    p4, p5 = [], []
    for layer, reader in LAYERS:
        strings = reader()
        for L in 'AB':
            S = strings[L]
            rnd = random.Random(SEED)
            rep.append('%s, transcriber %s: %d stories, %d tokens' % (layer, L, len(S), sum(len(v) for v in S.values())))
            for n in (1, 2, 3):
                real = zipf_slope(ngram_counts(S, n))
                sh = [zipf_slope(ngram_counts(shuffle_strings(S, rnd), n)) for _ in range(20)] if n > 1 else [real]
                rep.append('  %d-grams: %d kinds; rank-frequency slope %.2f, shuffled %.2f' % (
                    n, len(ngram_counts(S, n)), real, sum(sh) / len(sh)))
            for g in list(GENRES) + ['all']:
                sub = {s: v for s, v in S.items() if g == 'all' or genre(s) == g}
                if not sub:
                    continue
                h = cond_entropy(sub)
                hs = [cond_entropy(shuffle_strings(sub, rnd)) for _ in range(200)]
                p = (sum(x <= h for x in hs) + 1) / float(len(hs) + 1)
                rep.append('  %-8s next-token entropy %.3f bits, shuffled %.3f, p %.4f' % (g, h, sum(hs) / len(hs), p))
                p4.append(p <= 0.05)
            # the owner's hypothesis: rare items more genre-specific than chance, frequent ones not
            labels = {s: genre(s) for s in S}
            for n in (1, 2):
                obs = {k: v for k, v in specificity(S, n, labels).items() if v[0] >= 3}
                if len(obs) < 9:
                    continue
                null = collections.defaultdict(list)
                ids = list(S)
                for _ in range(200):
                    gl = [labels[s] for s in ids]
                    rnd.shuffle(gl)
                    sp = specificity(S, n, dict(zip(ids, gl)))
                    for k in obs:
                        null[k].append(sp.get(k, (0, 1.0))[1])
                excess = {k: obs[k][1] - sum(null[k]) / len(null[k]) for k in obs}
                ranked = sorted(obs, key=lambda k: obs[k][0])
                third = len(ranked) // 3
                rare, freq = ranked[:third], ranked[-third:]
                er, ef = sum(excess[k] for k in rare) / len(rare), sum(excess[k] for k in freq) / len(freq)
                rep.append('  %d-grams seen 3 times or more: %d; genre over-representation beyond chance, rarest third %+.2f, commonest third %+.2f'
                           % (n, len(obs), er, ef))
                p5.append(er > ef)
            rep.append('')
    rep.append('PREDICTIONS (NgramProtocol.md)')
    rep.append('  4. next-token entropy below the shuffled strings, p <= 0.05, in every genre and all together, both layers and transcribers: %d of %d -> %s'
               % (sum(p4), len(p4), 'HOLDS' if all(p4) else 'FAILS'))
    rep.append('  5. the rarest third more over-represented in one genre beyond chance than the commonest third, for single tokens and pairs, both layers and transcribers: %d of %d -> %s'
               % (sum(p5), len(p5), 'HOLDS' if p5 and all(p5) else 'FAILS'))
    open(os.path.join(HERE, 'DescribeRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


# ---------------------------------------------------------------- the self-test
def planted(seed, n=120):
    """strings of random letters with x always followed by y, and z two places before w"""
    rnd = random.Random(seed)
    letters = list('abcdefghij')
    strings = {}
    for k in range(n):
        seq = [rnd.choice(letters) for _ in range(20)]
        i = rnd.randrange(0, 15)
        seq[i:i + 2] = ['X', 'Y']
        j = rnd.randrange(0, 15)
        if j not in (i - 2, i - 1, i, i + 1):
            seq[j], seq[j + 2] = 'Z', 'W'
        strings['A%03d' % k] = seq
    return strings


def selftest():
    """planted strings, two transcribers' worth for discovery and two for confirmation, each with its own random
    filler: the two-stage filter must keep exactly the planted pairs, with their shapes"""
    def st_of(a, b, gaps):
        out = {}
        for L, s in (('A', a), ('B', b)):
            c = Corpus(s)
            out[L] = (c, c.gap_stats(gaps, 200, SEED))
        return out
    disc = st_of(planted(1), planted(2), (1,))
    conf = st_of(planted(3), planted(4), tuple(range(1, MAX_GAP + 1)))
    vocab = disc['A'][0].vocab
    found = []
    for x in vocab:
        for y in vocab:
            if x == y:
                continue
            for cl in (1, 'near'):
                if all(cell(disc, L, cl, x, y)[0] >= MIN_COUNT and lift(*cell(disc, L, cl, x, y)[:2]) >= MIN_LIFT
                       and cell(disc, L, cl, x, y)[2] <= DISCOVER_P for L in 'AB'):
                    ok = all(lift(*cell(conf, L, cl, x, y)[:2]) > 1 and cell(conf, L, cl, x, y)[2] <= CONFIRM_P for L in 'AB')
                    found.append((x, y, cl, 'confirmed' if ok else 'not confirmed', shape(gap_profile(conf, x, y))))
    for f in found:
        print('%s -> %s, %s: %s; %s' % f)
    print('want: X -> Y adjacent, confirmed, adjacent; Z -> W near, confirmed, spaced (peak 2 apart); nothing else confirmed')


if __name__ == '__main__':
    cmds = {'discover': discover, 'confirm': confirm, 'describe': describe, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
