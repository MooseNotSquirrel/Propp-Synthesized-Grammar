#!/usr/bin/env python3
"""
aesopScore.py -- the keeper's derivation and scoring for the Aesop test.
Written and committed before any main transcription was read.

  python aesopScore.py check AESOP_REPO LINEAGE   form only: every sampled
                                                  fable present, every event
                                                  covered, symbols in the
                                                  alphabet, a Y or N mark on
                                                  every entry. Parses nothing.
  python aesopScore.py score AESOP_REPO           the run, both transcribers

AESOP_REPO is the Aesop repository; each transcriber's batches are
transcriptions/<L>/b1..b4. The pilot is not read.

THE DERIVATION, fixed before any main transcription was read:
  1. Notes.txt is the record: one line per entry, eleven fields (fable,
     move, position, event, symbol, performer, undergoer, matters, link,
     doubt, note).
  2. The primary reading keeps only function entries marked Y; entries
     marked N count as X. The secondary reading keeps every function entry.
     Doubtful entries are kept in both; a third reading drops them from the
     primary.
  3. Symbols are read as in the Apollodorus test: varieties and signs
     stripped (a negative I is the defeat I- only with the extensions on),
     KF read as K and w as W, C↑ as C and ↑.
  4. Ties: a fable whose hero line names k heroes is transcribed k times;
     each version weighs 1/k.
THE MEASURES, as AesopPrediction.txt fixes them:
  coverage  the share of events with at least one function entry kept by
            the reading;
  order     within each fable, entries in the fable's event order: the share
            of ordered pairs of functions running backward against Propp's
            numbering, against the same entries shuffled within the fable
            (200 shuffles, random.Random(46));
  pairs     for each of Propp's pairs whose first function occurs at least 10
            times, how often it is followed by the second within the fable,
            against the shuffle.
Reported and not judged: the share of function entries marked N; the share
of fables with a villainy or lack followed by its liquidation; v46
acceptance at `move`, as shipped and extended, against the opener-fixed
shuffle by length band; agreement between the transcribers.
"""
import collections
import glob
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CALLER = os.getcwd()
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import parse  # noqa: E402
import runCorpus as R  # noqa: E402
import runSteps  # noqa: E402
import shuffleBaseline as SB  # noqa: E402

PREP = set('αβγδεζηθλ')
BASES = {'A', 'a', 'B', 'C', '↑', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', '↓', 'Pr', 'Rs', 'o', 'L',
         'M', 'N', 'Q', 'Ex', 'T', 'U', 'W', 'X', 'KF', 'w', 'f', 'C↑'} | PREP
MARKS = re.compile(r'[⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉0-9ⁱᵛˣ*−₋₊⁻^+\-?]')
NUM = {'β': 1, 'γ': 2, 'δ': 3, 'ε': 4, 'ζ': 5, 'η': 6, 'θ': 7, 'λ': 7.5, 'A': 8, 'a': 8, 'B': 9, 'C': 10,
       'up': 11, 'D': 12, 'E': 13, 'F': 14, 'G': 15, 'H': 16, 'J': 17, 'I': 18, 'K': 19, 'down': 20,
       'Pr': 21, 'Rs': 22, 'o': 23, 'L': 24, 'M': 25, 'N': 26, 'Q': 27, 'Ex': 28, 'T': 29, 'U': 30, 'W': 31}
PAIRS = [('γ', 'δ', 'interdiction, violation'), ('ε', 'ζ', 'reconnaissance, delivery'),
         ('η', 'θ', 'trickery, complicity'), ('D', 'E', "test, reaction"),
         ('H', 'I', 'struggle, victory'), ('Pr', 'Rs', 'pursuit, rescue'),
         ('M', 'N', 'task, solution'), ('J', 'Q', 'branding, recognition'),
         ('L', 'Ex', 'false claim, exposure'), ('Aa', 'K', 'villainy or lack, liquidation'),
         ('up', 'down', 'departure, return')]
BANDS = (('1-4', 1, 4), ('5-6', 5, 6), ('7-9', 7, 9), ('10+', 10, 10 ** 6))
GRAMMAR = 'ProppEBNF46.txt'


def base(sym):
    return MARKS.sub('', sym.strip())


def negative(sym):
    return any(c in sym for c in '−₋⁻-')


def key(sym, extended=False):
    """the grammar key of one symbol, or None for X; C↑ gives two."""
    b = base(sym)
    if b == 'X':
        return []
    if b == 'C↑':
        return ['C', 'up']
    if b in PREP:
        return [b]
    if extended and b == 'I' and negative(sym):
        return ['I-']
    k, r = R.key_of(b)
    return [k if r is not None else b]


def roman(m):
    vals = {'I': 1, 'V': 5, 'X': 10}
    s = re.sub(r'[^IVX]', '', m.upper())
    n = 0
    for i, c in enumerate(s):
        v = vals[c]
        n += -v if i + 1 < len(s) and vals[s[i + 1]] > v else v
    return n or 99


def fables(repo):
    """[(version id, fable id, hero, weight, n events)] for the scored sample."""
    sample = [x.strip() for x in open(os.path.join(repo, 'Sample.txt')) if x.strip()]
    heroes = {}
    for l in open(os.path.join(repo, 'Heroes.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|')]
        heroes[f[0]] = [h.strip() for h in f[1].replace('hero:', '').split(';') if h.strip()]
    nev = collections.Counter(l.split(' | ')[0] for l in open(os.path.join(repo, 'Events.txt'), encoding='utf-8') if l.strip())
    out = []
    for fid in sample:
        if not nev.get(fid):
            continue
        hs = heroes.get(fid) or ['']
        if len(hs) == 1:
            out.append((fid, fid, hs[0], 1.0, nev[fid]))
        else:
            out += [('%s/%d' % (fid, i), fid, h, 1.0 / len(hs), nev[fid]) for i, h in enumerate(hs, 1)]
    return out


def load(repo, lineage):
    ents = collections.defaultdict(list)
    n = 0
    for d in sorted(glob.glob(os.path.join(repo, 'transcriptions', lineage, 'b[0-9]'))):
        p = os.path.join(d, 'Notes.txt')
        if not os.path.exists(p):
            continue
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^F\d{3}', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            pos = re.search(r'\d+', f[2])
            n += 1
            ents[f[0]].append({'move': f[1], 'pos': int(pos.group()) if pos else 0,
                               'ev': int(ev.group()) if ev else None, 'sym': f[4], 'undergoer': f[6],
                               'matters': f[7].upper().startswith('Y'), 'mark': f[7], 'doubt': '?' in f[9],
                               'line': n})
    return ents


def kept(e, reading):
    if base(e['sym']) == 'X':
        return False
    if reading == 'primary':
        return e['matters']
    if reading == 'nodoubt':
        return e['matters'] and not e['doubt']
    return True


def sequence(es, reading):
    """the fable's function keys in event order."""
    out = []
    for e in sorted(es, key=lambda e: (e['ev'] or 0, e['line'])):
        if kept(e, reading):
            out += [k for k in key(e['sym']) if k in NUM]
    return out


def inversions(seqs):
    inv = pairs = 0.0
    for s, w in seqs:
        ns = [NUM[x] for x in s]
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                if ns[i] != ns[j]:
                    pairs += w
                    inv += w * (ns[i] > ns[j])
    return inv / pairs if pairs else None


def match(k, x):
    return k in ('A', 'a') if x == 'Aa' else k == x


def follow(seqs, x, y):
    fx = nx = 0.0
    for s, w in seqs:
        for i, k in enumerate(s):
            if match(k, x):
                nx += w
                fx += w * any(match(j, y) for j in s[i + 1:])
    return (fx / nx if nx else None), nx


def shuffled(seqs, rng):
    out = []
    for s, w in seqs:
        s = list(s)
        rng.shuffle(s)
        out.append((s, w))
    return out


def moves(es, reading, hero, extended):
    """[(keys)] per move, derived as the Apollodorus test derives them."""
    by = collections.OrderedDict()
    for e in sorted(es, key=lambda e: (roman(e['move']), e['pos'], e['line'])):
        by.setdefault(e['move'], []).append(e)
    out = []
    for mi, mv in enumerate(by.values()):
        mv = [e for e in mv if kept(e, reading)]
        if mi == 0:
            first = next((i for i, e in enumerate(mv) if base(e['sym']) in ('A', 'a', 'B')), None)
            if first is None:
                first = 0
                while first < len(mv) and base(mv[first]['sym']) in PREP:
                    first += 1
            mv = [e for i, e in enumerate(mv) if not (i < first and base(e['sym']) in PREP)]
        keys, after_kw, rv = [], False, False
        for e in mv:
            ks = key(e['sym'], extended)
            if extended and not rv and after_kw and ks[:1] and ks[0] in ('U', 'Q', 'Ex') \
                    and hero and hero.lower() in e['undergoer'].lower():
                keys.append('Rv')
                rv = True
            keys += ks
            if any(k in ('K', 'W') for k in ks):
                after_kw = True
        out.append(keys)
    return out


def grammar(extended):
    path = runSteps.switched(GRAMMAR, ['tragedy', 'reversal'], 'move') if extended else GRAMMAR
    g = R.Grammar(path, 'move' if not extended else None)
    return g


def band_of(n):
    return next(name for name, lo, hi in BANDS if lo <= n <= hi)


def russian_gaps():
    rows = SB.tally()
    lens = {(m['tale'], m['move']): min(len(x) for x in R.expansions(R.elements(m['canon'])))
            for m in R.F.load('ResolvedMoves.txt')}
    b = collections.defaultdict(list)
    for r in rows:
        b[band_of(lens[(r[0], r[1])])].append(r)
    return {k: sum(r[2] for r in v) / len(v) - sum(r[4] for r in v) / len(v) for k, v in b.items()}


def check(repo, lineage):
    ents = load(repo, lineage)
    problems = []
    for vid, fid, hero, w, n in fables(repo):
        es = ents.get(vid)
        if not es:
            problems.append('%s: missing' % vid)
            continue
        missing = [i for i in range(1, n + 1) if i not in {e['ev'] for e in es}]
        if missing:
            problems.append('%s: events without an entry %s' % (vid, missing))
        bad = sorted({e['sym'] for e in es if base(e['sym']) not in BASES})
        if bad:
            problems.append('%s: symbols outside the alphabet %s' % (vid, bad))
        nomark = [e['ev'] for e in es if e['mark'][:1].upper() not in ('Y', 'N')]
        if nomark:
            problems.append('%s: entries without a Y or N mark at events %s' % (vid, nomark))
    print('transcriber %s: %d fable versions with entries, %d problems' % (lineage, len(ents), len(problems)))
    for p in problems:
        print('  ' + p)
    return 0 if not problems else 1


def score(repo):
    gaps = russian_gaps()
    fv = fables(repo)
    print('Scored: %d fable versions of %d fables' % (len(fv), len({f[1] for f in fv})))
    for lineage in ('A', 'B'):
        ents = load(repo, lineage)
        print('\nTRANSCRIBER %s' % lineage)
        allf = [e for vid, *_ in fv for e in ents.get(vid, []) if base(e['sym']) != 'X']
        wN = sum(1 for e in allf if not e['matters'])
        print('  function entries marked N (incidental): %d of %d (%.1f%%)' % (wN, len(allf), 100.0 * wN / max(1, len(allf))))
        for reading in ('primary', 'secondary', 'nodoubt'):
            cov_n = cov_d = 0.0
            seqs = []
            complete = cw = 0.0
            for vid, fid, hero, w, n in fv:
                es = ents.get(vid, [])
                covered = {e['ev'] for e in es if kept(e, reading)}
                cov_n += w * len([i for i in range(1, n + 1) if i in covered])
                cov_d += w * n
                s = sequence(es, reading)
                seqs.append((s, w))
                cw += w
                complete += w * any(k in ('A', 'a') and 'K' in s[i + 1:] for i, k in enumerate(s))
            cov = cov_n / cov_d
            inv = inversions(seqs)
            rng = random.Random(46)
            sh = [inversions(shuffled(seqs, rng)) for _ in range(200)]
            sh = [x for x in sh if x is not None]
            inv_sh = sum(sh) / len(sh) if sh else None
            pair_lines, pairs_ok = [], True
            for x, y, name in PAIRS:
                f, nx = follow(seqs, x, y)
                if not nx:
                    continue
                rng = random.Random(46)
                fs = [follow(shuffled(seqs, rng), x, y)[0] for _ in range(200)]
                fsh = sum(v for v in fs if v is not None) / max(1, sum(1 for v in fs if v is not None))
                judged = nx >= 10
                ok = (f - fsh) >= 0.20
                if judged and not ok:
                    pairs_ok = False
                pair_lines.append('    %-32s n=%5.1f follow %5.1f%% shuffled %5.1f%%%s' % (
                    name, nx, 100 * f, 100 * fsh, '' if judged else '  (under 10, not judged)'))
            order_ok = inv is not None and inv_sh is not None and inv <= 0.15 and (inv_sh - inv) >= 0.20
            verdict = cov >= 0.60 and order_ok and pairs_ok
            print('  reading: %s' % {'primary': 'primary (functions marked Y)',
                                     'secondary': 'secondary (all functions)',
                                     'nodoubt': 'primary, doubtful entries dropped'}[reading])
            print('    coverage %.1f%% (threshold 60%%)' % (100 * cov))
            print('    order: %s backward, shuffled %s (threshold 15%%, and 20 points below shuffled)' % (
                'n/a' if inv is None else '%.1f%%' % (100 * inv), 'n/a' if inv_sh is None else '%.1f%%' % (100 * inv_sh)))
            print('    pairs:')
            for pl in pair_lines:
                print(pl)
            print('    fables with a villainy or lack followed by its liquidation: %.1f%%' % (100 * complete / cw))
            if reading == 'primary':
                print('    VERDICT: %s' % ('the claim holds' if verdict else 'the claim does not hold'))
        for extended in (False, True):
            g = grammar(extended)
            rng = random.Random(46)
            ms = []
            for vid, fid, hero, w, n in fv:
                for k in moves(ents.get(vid, []), 'primary', hero, extended):
                    if not k:
                        continue
                    ok = parse.accept(list(k), g.bnf, g.start, g.table)[0]
                    hits = sum(parse.accept(SB.fixed(rng, list(k)), g.bnf, g.start, g.table)[0] for _ in range(1000))
                    ms.append((k, w, ok, hits / 1000.0))
            wsum = sum(m[1] for m in ms)
            acc = sum(m[1] * m[2] for m in ms) / wsum if wsum else 0
            print('  v46 %s: acceptance %.1f%% of %d moves (primary reading)' % (
                'with extensions' if extended else 'as shipped', 100 * acc, len(ms)))
            for name, lo, hi in BANDS:
                b = [m for m in ms if lo <= len(m[0]) <= hi]
                if not b:
                    continue
                bw = sum(m[1] for m in b)
                real = sum(m[1] * m[2] for m in b) / bw
                shf = sum(m[1] * m[3] for m in b) / bw
                print('    %-4s n=%3d real %5.1f%% shuffled %5.1f%% gap %5.1f (Russian gap %.1f)' % (
                    name, len(b), 100 * real, 100 * shf, 100 * (real - shf), 100 * gaps.get(name, 0)))
    ea, eb = load(repo, 'A'), load(repo, 'B')
    same = tot = both = agree = rel_same = rel_tot = 0
    for vid, fid, hero, w, n in fv:
        byA, byB, rA, rB = {}, {}, {}, {}
        for e in ea.get(vid, []):
            byA.setdefault(e['ev'], set()).add(base(e['sym']))
            rA.setdefault(e['ev'], set()).add(e['matters'])
        for e in eb.get(vid, []):
            byB.setdefault(e['ev'], set()).add(base(e['sym']))
            rB.setdefault(e['ev'], set()).add(e['matters'])
        for i in range(1, n + 1):
            sa, sb = byA.get(i, set()), byB.get(i, set())
            tot += 1
            same += sa == sb
            fa, fb = sa - {'X'}, sb - {'X'}
            if fa and fb:
                both += 1
                agree += bool(fa & fb)
            if i in rA and i in rB:
                rel_tot += 1
                rel_same += (True in rA[i]) == (True in rB[i])
    print('\nAGREEMENT')
    print('  events given the same symbols: %d of %d (%.1f%%)' % (same, tot, 100.0 * same / max(1, tot)))
    print('  events both gave a function, sharing one: %d of %d (%.1f%%)' % (agree, both, 100.0 * agree / max(1, both)))
    print('  events given the same relevance mark: %d of %d (%.1f%%)' % (rel_same, rel_tot, 100.0 * rel_same / max(1, rel_tot)))
    return 0


if __name__ == '__main__':
    a = [os.path.join(CALLER, x) if i == 1 else x for i, x in enumerate(sys.argv[1:])]
    if a[:1] == ['check'] and len(a) == 3:
        sys.exit(check(a[1], a[2]))
    if a[:1] == ['score'] and len(a) == 2:
        sys.exit(score(a[1]))
    sys.exit(__doc__)
