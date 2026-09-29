#!/usr/bin/env python3
"""
scoreApollodorus.py -- the keeper's derivation and scoring for the
Apollodorus test. Written and committed before any transcription was read.

  python scoreApollodorus.py check WORK LINEAGE   form only: every scored
                                                  episode present, every
                                                  census event covered by an
                                                  entry, symbols in the
                                                  alphabet, Notes and Streams
                                                  agreeing. Parses nothing.
  python scoreApollodorus.py score WORK           the run: both lineages, both
                                                  grammars, both doubt corpora

WORK is the ApollodorusWork folder. Each lineage's batches are its folders
b01..b09; the pilot is not read.

THE DERIVATION, fixed before any transcription was read:
  1. Notes.txt is the record: one line per entry, with its move, position,
     census event, symbol, performer, undergoer and doubt mark. Streams.txt
     is checked against it.
  2. Preparatory entries (alpha to theta, lambda) in move I that stand
     before the move's first villainy, lack or mediation are v46's
     tale-level preparatory section; they are removed from the move string
     and counted. If move I has none of the three, its leading run of
     preparatory and X entries is removed. A preparatory entry anywhere
     else stays, and the move grammar judges it.
  3. X is removed and counted.
  4. Notation variants are read as the rules' notation: a variety number in
     plain digits (A15) or after a caret (A^15) as a superscript, a superscript minus as the minus,
     Propp's lowercase f as F, and C↑, Propp's combined sign in his own
     analyses, as the two functions C and ↑.
  5. Every other entry is reduced to its key by runCorpus.py's own
     reduction, varieties and signs stripped, KF read as K and w as W, as
     the Russian moves are. Nothing before the opener is dropped: in the
     Russian corpus that drop answers Propp's table layout, and Greek order
     is narrative order.
  6. With the extensions on (+tragedy,reversal), I with a minus is the
     defeat I-, and Rv is written before the first U, Q or Ex in a move
     whose undergoer names the hero and which follows a K or W in the same
     move.
  7. Doubt: the primary corpus keeps the entries marked '?'; the second
     drops them. Both are scored; the verdict is read on the primary.
  8. Weights: each episode weighs 1; an episode with k heroes is
     transcribed k times and each version weighs 1/k. Within a version,
     every move counts, and coverage counts every census event.
THE MEASUREMENTS, as ApollodorusPrediction.txt fixes them: coverage, the
share of census events with at least one function entry; acceptance, the
share of moves the grammar accepts at `move`; discrimination, in each
length band (1-4, 5-6, 7-9, 10+ keys) holding at least 10 Greek moves,
real acceptance minus opener-fixed shuffled acceptance (1000 shuffles per
move, one random.Random(46) drawn in corpus order), against the Russian
gap in the same band from shuffleBaseline.py.
"""
import collections
import glob
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
os.chdir(ROOT)

import keeper  # noqa: E402  (Apollodorus/keeper.py, via HERE below)
import runCorpus as R  # noqa: E402
import runSteps  # noqa: E402
import shuffleBaseline as SB  # noqa: E402

PREP = set('αβγδεζηθλ')
BASES = {'A', 'a', 'B', 'C', '↑', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', '↓', 'Pr', 'Rs', 'o', 'L',
         'M', 'N', 'Q', 'Ex', 'T', 'U', 'W', 'X', 'KF', 'w', 'f', 'C↑'} | PREP
MARKS = re.compile(r'[⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉0-9ⁱᵛˣ*−₋₊⁻^+\-]')
GRAMMAR = 'ProppEBNF46.txt'
BANDS = (('1-4', 1, 4), ('5-6', 5, 6), ('7-9', 7, 9), ('10+', 10, 10 ** 6))
PILOT = {'L2-028', 'L3-044', 'L3-083'}


def base(sym):
    return MARKS.sub('', sym.strip())


def negative(sym):
    return any(c in sym for c in '−₋⁻-')


def scored_episodes():
    here = os.getcwd()
    os.chdir(HERE)
    try:
        rows = keeper.census_rows()
    finally:
        os.chdir(here)
    out = []
    for r in rows:
        if r['n'] >= 5 and r['variant'] in ('', '-') and r['id'] not in PILOT:
            heroes = [h.strip() for h in r['hero'].split(';') if h.strip()]
            out.append((r['id'], r['n'], heroes))
    return out


def load_notes(work, lineage):
    entries = collections.defaultdict(list)
    streams = {}
    for d in sorted(glob.glob(os.path.join(work, 'transcriber' + lineage, 'b[0-9][0-9]'))):
        if not (os.path.exists(os.path.join(d, 'Notes.txt')) and os.path.exists(os.path.join(d, 'Streams.txt'))):
            continue
        for line in open(os.path.join(d, 'Notes.txt'), encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 9)]
            if len(f) < 9 or not re.match(r'^(L[123]|E)-\d+', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            pos = re.search(r'\d+', f[2])
            entries[f[0]].append({'move': f[1], 'pos': int(pos.group()) if pos else 0,
                                  'ev': int(ev.group()) if ev else None, 'sym': f[5],
                                  'performer': f[6], 'undergoer': f[7], 'doubt': '?' in f[8]})
        tale, cur = None, None
        for line in open(os.path.join(d, 'Streams.txt'), encoding='utf-8'):
            m = re.match(r'^tale:\s*(\S+)', line)
            if m:
                tale = m.group(1)
                continue
            m = re.match(r'^move:\s*([^|]+)\|(.*)$', line)
            if m and tale:
                streams[(tale, m.group(1).strip())] = m.group(2).split()
    return entries, streams


def roman(m):
    vals = {'I': 1, 'V': 5, 'X': 10}
    s = re.sub(r'[^IVX]', '', m.upper())
    n = 0
    for i, c in enumerate(s):
        v = vals[c]
        n += -v if i + 1 < len(s) and vals[s[i + 1]] > v else v
    return n or 99


def versions(ep, heroes):
    if len(heroes) <= 1:
        return [(ep, heroes[0] if heroes else '', 1.0)]
    return [('%s/%d' % (ep, i), h, 1.0 / len(heroes)) for i, h in enumerate(heroes, 1)]


def moves_of(ents):
    by = collections.OrderedDict()
    for e in sorted(ents, key=lambda e: (roman(e['move']), e['pos'])):
        by.setdefault(e['move'], []).append(e)
    return list(by.values())


def derive(ents, hero, extended, drop_doubt):
    """[(keys, stats)] for each move of one version."""
    out = []
    for mi, mv in enumerate(moves_of(ents)):
        mv = [e for e in mv if not (drop_doubt and e['doubt'])]
        removed_prep = 0
        if mi == 0:
            first = next((i for i, e in enumerate(mv) if base(e['sym']) in ('A', 'a', 'B')), None)
            if first is None:
                first = 0
                while first < len(mv) and base(mv[first]['sym']) in PREP | {'X'}:
                    first += 1
            removed_prep = sum(1 for e in mv[:first] if base(e['sym']) in PREP)
            mv = [e for i, e in enumerate(mv) if not (i < first and base(e['sym']) in PREP)]
        keys, xs, after_kw, rv_done = [], 0, False, False
        for e in mv:
            b = base(e['sym'])
            if b == 'X':
                xs += 1
                continue
            if b in PREP:
                keys.append(b)
                continue
            if b == 'C↑':
                keys += ['C', 'up']
                continue
            if extended and b == 'I' and negative(e['sym']):
                keys.append('I-')
                continue
            k, r = R.key_of(b if b not in ('↑', '↓') else b)
            if r is None:
                keys.append(b)
                continue
            if extended and not rv_done and after_kw and k in ('U', 'Q', 'Ex') \
                    and hero and hero.lower() in e['undergoer'].lower():
                keys.append('Rv')
                rv_done = True
            keys.append(k)
            if k in ('K', 'W'):
                after_kw = True
        out.append((keys, {'x': xs, 'prep_removed': removed_prep}))
    return out


def check(work, lineage):
    entries, streams = load_notes(work, lineage)
    problems = []
    for ep, n, heroes in scored_episodes():
        for vid, hero, w in versions(ep, heroes):
            ents = entries.get(vid)
            if not ents:
                problems.append('%s: missing' % vid)
                continue
            evs = {e['ev'] for e in ents}
            missing = [i for i in range(1, n + 1) if i not in evs]
            if missing:
                problems.append('%s: events without an entry %s' % (vid, missing))
            bad = sorted({e['sym'] for e in ents if base(e['sym']) not in BASES})
            if bad:
                problems.append('%s: symbols outside the alphabet %s' % (vid, bad))
            for mv in moves_of(ents):
                key = (vid, mv[0]['move'])
                st = streams.get(key)
                if st is not None and [base(s) for s in st] != [base(e['sym']) for e in mv]:
                    problems.append('%s move %s: Streams and Notes differ' % key)
    extra = sorted(set(entries) - {v for ep, n, h in scored_episodes() for v, _, _ in versions(ep, h)})
    if extra:
        problems.append('entries for episodes not assigned: %s' % ' '.join(extra))
    print('transcriber %s: %d episodes with entries, %d problems' % (lineage, len(entries), len(problems)))
    for p in problems:
        print('  ' + p)
    return 0 if not problems else 1


def band_of(n):
    return next(name for name, lo, hi in BANDS if lo <= n <= hi)


def russian_gaps():
    rows = SB.tally()
    lens = {}
    for m in R.F.load('ResolvedMoves.txt'):
        lens[(m['tale'], m['move'])] = min(len(x) for x in R.expansions(R.elements(m['canon'])))
    b = collections.defaultdict(list)
    for r in rows:
        b[band_of(lens[(r[0], r[1])])].append(r)
    real = sum(r[2] for r in rows) / len(rows)
    return real, {k: (sum(r[2] for r in v) / len(v) - sum(r[4] for r in v) / len(v), len(v)) for k, v in b.items()}


def score_one(entries, grammar, extended, drop_doubt, seed_rng):
    moves, events_cov = [], []
    for ep, n, heroes in scored_episodes():
        for vid, hero, w in versions(ep, heroes):
            ents = entries.get(vid, [])
            covered = {e['ev'] for e in ents if base(e['sym']) != 'X' and not (drop_doubt and e['doubt'])}
            events_cov.append((w, n, len([i for i in range(1, n + 1) if i in covered])))
            for keys, st in derive(ents, hero, extended, drop_doubt):
                ok, pos, _ = __import__('parse').accept(list(keys), grammar.bnf, grammar.start, grammar.table)
                hits = 0
                for _ in range(SB.SHUFFLES):
                    s = SB.fixed(seed_rng, list(keys))
                    hits += __import__('parse').accept(s, grammar.bnf, grammar.start, grammar.table)[0]
                moves.append({'vid': vid, 'w': w, 'keys': keys, 'ok': ok, 'pos': pos,
                              'shuf': hits / SB.SHUFFLES, **st})
    cov = sum(w * c for w, n, c in events_cov) / sum(w * n for w, n, c in events_cov)
    acc = sum(m['w'] * m['ok'] for m in moves) / sum(m['w'] for m in moves)
    return cov, acc, moves


def grammar_for(extended):
    path = runSteps.switched(GRAMMAR, ['tragedy', 'reversal'], 'move') if extended else GRAMMAR
    g = R.Grammar(path, 'move' if not extended else None)
    if g.table is None:
        import parse
        g.bnf, first, g.table = parse.build(open(path, encoding='utf-8').read())
        g.start = 'move' if not extended else first
    return g


def score(work):
    r_real, r_gaps = russian_gaps()
    print('Russian: real acceptance %.1f%%; gaps by band %s' % (
        100 * r_real, ', '.join('%s %.1f (n=%d)' % (k, 100 * v[0], v[1]) for k, v in sorted(r_gaps.items()))))
    acc_floor = r_real - 0.10
    for lineage in ('A', 'B'):
        entries, _ = load_notes(work, lineage)
        for extended in (False, True):
            g = grammar_for(extended)
            for drop in (False, True):
                rng = random.Random(46)
                cov, acc, moves = score_one(entries, g, extended, drop, rng)
                bands = collections.defaultdict(list)
                for m in moves:
                    if m['keys']:
                        bands[band_of(len(m['keys']))].append(m)
                disc, disc_ok = [], True
                for name, lo, hi in BANDS:
                    ms = bands.get(name, [])
                    if not ms:
                        continue
                    wsum = sum(m['w'] for m in ms)
                    real = sum(m['w'] * m['ok'] for m in ms) / wsum
                    sh = sum(m['w'] * m['shuf'] for m in ms) / wsum
                    gap = real - sh
                    qualifies = len(ms) >= 10
                    passes = gap >= r_gaps.get(name, (0, 0))[0]
                    if qualifies and not passes:
                        disc_ok = False
                    disc.append('%s n=%d real %.1f%% shuffled %.1f%% gap %.1f vs %.1f%s' % (
                        name, len(ms), 100 * real, 100 * sh, 100 * gap, 100 * r_gaps.get(name, (0, 0))[0],
                        '' if qualifies else ' (too few, not judged)'))
                empty = sum(1 for m in moves if not m['keys'])
                verdict = cov >= 0.80 and acc >= acc_floor and disc_ok
                print('\nTRANSCRIBER %s, %s, doubtful entries %s%s' % (
                    lineage, 'with extensions' if extended else 'as shipped',
                    'dropped' if drop else 'kept', '' if drop else ' (primary)'))
                print('  coverage %.1f%% (threshold 80%%)' % (100 * cov))
                print('  acceptance %.1f%% of %d moves (threshold %.1f%%); %d moves empty after X removed' % (
                    100 * acc, len(moves), 100 * acc_floor, empty))
                for d in disc:
                    print('  ' + d)
                print('  preparatory entries removed from move I: %d; X removed: %d' % (
                    sum(m['prep_removed'] for m in moves), sum(m['x'] for m in moves)))
                fails = collections.Counter()
                for m in moves:
                    if not m['ok']:
                        k = m['keys'][m['pos']] if m['pos'] < len(m['keys']) else 'end'
                        fails[(m['pos'] if m['pos'] < 3 else '3+', k)] += 1
                print('  rejections by (position, key), most common: %s' % ', '.join(
                    '%s@%s x%d' % (k, p, n) for (p, k), n in fails.most_common(12)))
                print('  VERDICT: %s' % ('the claim holds' if verdict else 'the claim does not hold'))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['check'] and len(a) == 3:
        sys.exit(check(a[1], a[2]))
    if a[:1] == ['score'] and len(a) == 2:
        sys.exit(score(a[1]))
    sys.exit(__doc__)
