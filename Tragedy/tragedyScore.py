#!/usr/bin/env python3
"""
tragedyScore.py -- the keeper's derivation and scoring for the tragedy test.
Written and committed before any corpus play's transcription was read.

  python tragedyScore.py check TRAGEDY_REPO LINEAGE   form only, parses nothing
  python tragedyScore.py score TRAGEDY_REPO           the run, both transcribers

TRAGEDY_REPO is the Propp-Tragedy repository. The plays scored are those of
PlayOrder.txt (P01..P32) whose two transcriptions are present; the pilot is
not read.

THE DERIVATION, fixed before any corpus transcription was read, as in the
Aesop test:
  1. Notes.txt is the record, eleven fields per entry.
  2. The primary reading keeps function entries marked Y, doubtful entries
     included; the secondary keeps every function entry; a third drops the
     doubtful entries from the primary.
  3. Symbols are read as in the Apollodorus and Aesop tests.
  4. A play whose Hero.txt names k heroes is transcribed k times; each version
     weighs 1/k.
  5. Moves, for the grammar, are the transcriber's moves in position order;
     preparatory entries before move I's first villainy, lack or mediation
     are removed; with the extensions on, a negative I is the defeat I-, and
     Rv is written before the first U, Q or Ex whose undergoer names the
     hero after a K or W in the same move.
THE MEASURES, as TragedyPrediction.txt fixes them, pooled over the plays:
  coverage        events with a function entry kept by the reading, at least 80%;
  acceptance      moves ProppEBNF46.txt accepts at `move`, at least 85.2%;
  discrimination  in each length band holding at least 10 moves, real minus
                  opener-fixed shuffled acceptance (1000 shuffles, seed 46) at
                  least the Russian gap.
Both grammars are judged; the verdict is given only when all 32 plays are
scored, and is marked interim before that.
Reported and not judged: order against Propp's numbering and Propp's pairs,
against a within-play shuffle (200 shuffles, seed 46); the same order with
events told as past moved first; the share of function entries marked N;
agreement between the transcribers.
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
         ('η', 'θ', 'trickery, complicity'), ('D', 'E', 'test, reaction'),
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


def plays(repo):
    """[(version id, play id, hero, weight, n events, {event: 'past'|'now'})] for the scored plays."""
    order = [l.split(' | ')[0] for l in open(os.path.join(HERE, 'PlayOrder.txt'), encoding='utf-8') if l.strip()]
    out = []
    for pid in order:
        d = os.path.join(repo, 'plays', pid)
        if not all(os.path.exists(os.path.join(repo, 'transcriptions', L, pid, 'Notes.txt')) for L in 'AB'):
            continue
        told = {}
        for l in open(os.path.join(d, 'Events.txt'), encoding='utf-8'):
            f = [x.strip() for x in l.split('|', 4)]
            if len(f) == 5 and f[1].isdigit():
                told[int(f[1])] = f[3]
        hl = open(os.path.join(d, 'Hero.txt'), encoding='utf-8').read().strip()
        hs = [h.strip() for h in hl.split('|', 1)[1].replace('hero:', '').split(';') if h.strip()]
        if len(hs) <= 1:
            out.append((pid, pid, hs[0] if hs else '', 1.0, len(told), told))
        else:
            out += [('%s/%d' % (pid, i), pid, h, 1.0 / len(hs), len(told), told) for i, h in enumerate(hs, 1)]
    return out


def load(repo, lineage):
    ents = collections.defaultdict(list)
    n = 0
    for p in sorted(glob.glob(os.path.join(repo, 'transcriptions', lineage, 'P[0-9][0-9]', 'Notes.txt'))):
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^P\d{2}', f[0]):
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


def sequence(es, reading, told=None):
    """function keys in the play's event order; with told, past events first."""
    def order(e):
        past = 0 if (told is not None and told.get(e['ev']) == 'past') else 1
        return (past if told is not None else 0, e['ev'] or 0, e['line'])
    out = []
    for e in sorted(es, key=order):
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
    return R.Grammar(path, 'move' if not extended else None)


def band_of(n):
    return next(name for name, lo, hi in BANDS if lo <= n <= hi)


def russian():
    rows = SB.tally()
    lens = {(m['tale'], m['move']): min(len(x) for x in R.expansions(R.elements(m['canon'])))
            for m in R.F.load('ResolvedMoves.txt')}
    b = collections.defaultdict(list)
    for r in rows:
        b[band_of(lens[(r[0], r[1])])].append(r)
    real = sum(r[2] for r in rows) / len(rows)
    return real, {k: sum(r[2] for r in v) / len(v) - sum(r[4] for r in v) / len(v) for k, v in b.items()}


def check(repo, lineage):
    ents = load(repo, lineage)
    problems = []
    for vid, pid, hero, w, n, told in plays(repo):
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
    print('transcriber %s: %d play versions with entries, %d problems' % (lineage, len(ents), len(problems)))
    for p in problems:
        print('  ' + p)
    return 0 if not problems else 1


def score(repo):
    real_ru, gaps = russian()
    floor = real_ru - 0.10
    pv = plays(repo)
    done = len({p[1] for p in pv})
    final = done == 32
    print('Plays scored: %d of 32 (%s)' % (done, 'final' if final else 'interim: reported, not judged'))
    print('Plays: ' + ', '.join(sorted({p[1] for p in pv})))
    for lineage in ('A', 'B'):
        ents = load(repo, lineage)
        print('\nTRANSCRIBER %s' % lineage)
        allf = [e for p in pv for e in ents.get(p[0], []) if base(e['sym']) != 'X']
        wN = sum(1 for e in allf if not e['matters'])
        print('  function entries marked N (incidental): %d of %d (%.1f%%)' % (wN, len(allf), 100.0 * wN / max(1, len(allf))))
        for reading in ('primary', 'secondary', 'nodoubt'):
            cn = cd = 0.0
            for vid, pid, hero, w, n, told in pv:
                covered = {e['ev'] for e in ents.get(vid, []) if kept(e, reading)}
                cn += w * len([i for i in range(1, n + 1) if i in covered])
                cd += w * n
            print('  reading %s: coverage %.1f%% (threshold 80%%)' % (reading, 100 * cn / cd if cd else 0))
        for label, told_first in (('order as told', False), ('past events first', True)):
            seqs = [(sequence(ents.get(vid, []), 'primary', told if told_first else None), w)
                    for vid, pid, hero, w, n, told in pv]
            inv = inversions(seqs)
            rng = random.Random(46)
            sh = [x for x in (inversions(shuffled(seqs, rng)) for _ in range(200)) if x is not None]
            print('  %s: %s of function pairs backward against Propp, shuffled %s' % (
                label, 'n/a' if inv is None else '%.1f%%' % (100 * inv), '%.1f%%' % (100 * sum(sh) / len(sh)) if sh else 'n/a'))
        seqs = [(sequence(ents.get(vid, []), 'primary'), w) for vid, pid, hero, w, n, told in pv]
        print('  pairs (primary):')
        for x, y, name in PAIRS:
            f, nx = follow(seqs, x, y)
            if not nx:
                continue
            rng = random.Random(46)
            fs = [v for v in (follow(shuffled(seqs, rng), x, y)[0] for _ in range(200)) if v is not None]
            print('    %-32s n=%5.1f follow %5.1f%% shuffled %5.1f%%' % (name, nx, 100 * f, 100 * sum(fs) / max(1, len(fs))))
        for extended in (False, True):
            g = grammar(extended)
            rng = random.Random(46)
            ms = []
            for vid, pid, hero, w, n, told in pv:
                for k in moves(ents.get(vid, []), 'primary', hero, extended):
                    if not k:
                        continue
                    ok = parse.accept(list(k), g.bnf, g.start, g.table)[0]
                    hits = sum(parse.accept(SB.fixed(rng, list(k)), g.bnf, g.start, g.table)[0] for _ in range(1000))
                    ms.append((k, w, ok, hits / 1000.0))
            wsum = sum(m[1] for m in ms)
            acc = sum(m[1] * m[2] for m in ms) / wsum if wsum else 0
            disc_ok = True
            lines = []
            for name, lo, hi in BANDS:
                b = [m for m in ms if lo <= len(m[0]) <= hi]
                if not b:
                    continue
                bw = sum(m[1] for m in b)
                real = sum(m[1] * m[2] for m in b) / bw
                shf = sum(m[1] * m[3] for m in b) / bw
                judged = len(b) >= 10
                if judged and real - shf < gaps.get(name, 0):
                    disc_ok = False
                lines.append('    %-4s n=%3d real %5.1f%% shuffled %5.1f%% gap %5.1f (Russian gap %.1f)%s' % (
                    name, len(b), 100 * real, 100 * shf, 100 * (real - shf), 100 * gaps.get(name, 0),
                    '' if judged else ' (too few, not judged)'))
            cn = cd = 0.0
            for vid, pid, hero, w, n, told in pv:
                covered = {e['ev'] for e in ents.get(vid, []) if kept(e, 'primary')}
                cn += w * len([i for i in range(1, n + 1) if i in covered])
                cd += w * n
            cov = cn / cd if cd else 0
            verdict = cov >= 0.80 and acc >= floor and disc_ok
            print('  v46 %s: acceptance %.1f%% of %d moves (threshold %.1f%%)' % (
                'with extensions' if extended else 'as shipped', 100 * acc, len(ms), 100 * floor))
            for l in lines:
                print(l)
            print('    VERDICT%s: %s' % ('' if final else ' (interim, not judged)',
                                        'the claim holds' if verdict else 'the claim does not hold'))
    ea, eb = load(repo, 'A'), load(repo, 'B')
    same = tot = both = agree = rs = rt = 0
    for vid, pid, hero, w, n, told in pv:
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
                rt += 1
                rs += (True in rA[i]) == (True in rB[i])
    print('\nAGREEMENT')
    print('  events given the same symbols: %d of %d (%.1f%%)' % (same, tot, 100.0 * same / max(1, tot)))
    print('  events both gave a function, sharing one: %d of %d (%.1f%%)' % (agree, both, 100.0 * agree / max(1, both)))
    print('  events given the same relevance mark: %d of %d (%.1f%%)' % (rs, rt, 100.0 * rs / max(1, rt)))
    return 0


if __name__ == '__main__':
    a = [os.path.join(CALLER, x) if i == 1 else x for i, x in enumerate(sys.argv[1:])]
    if a[:1] == ['check'] and len(a) == 3:
        sys.exit(check(a[1], a[2]))
    if a[:1] == ['score'] and len(a) == 2:
        sys.exit(score(a[1]))
    sys.exit(__doc__)
