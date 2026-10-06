#!/usr/bin/env python3
"""
compare.py -- the Afanasyev calibration's comparison, as CalibrationProtocol.md
freezes it. Written and committed before either arm's transcriptions or the
probe's recall were read.

  python compare.py AFANASYEV_REPO

AFANASYEV_REPO is the transcriber repository (Propp-Afanasyev). Output goes
to standard output; the keeper saves it as Calibration/CompareRun.txt.

THE STREAMS, as the protocol fixes them, and the readings it leaves open,
fixed here:
  1. Ours: per tale, the function entries of Notes.txt marked Y (doubtful
     ones included, the primary reading of the earlier tests), in the order
     of the notes, X and the preparatory functions left out, each symbol
     reduced by tragedyScore.key without the extensions (so C↑ is C up, KF is
     K, w is W, and A and a stay apart).
  2. Propp's: embedCorpus.derive() for the tale, its moves in printed order
     with embedded moves expanded where they stand and each brace flattened,
     every row in printed order. derive() applies runCorpus's shared-opener
     rule, so in 163 I and 164 II a brace row without the opener carries it;
     that is derive()'s reading and is kept, as the protocol names derive().
  3. Our move count: the distinct move labels the transcriber wrote for the
     tale in Notes.txt. Propp's: the tale's moves, embedded ones included
     (84 in all).
  4. Acceptance: our moves built as the tragedy test builds them
     (tragedyScore.moves, primary reading, no extensions: preparatory
     entries before move I's first villainy, lack or mediation removed),
     each nonempty move parsed by ProppEBNF46.txt at `move`.
THE MEASURES, per tale, averaged over the 45 tales, unweighted:
  content  Dice of the two multisets of symbols, 2|a∩b|/(|a|+|b|); 1 if both
           are empty, 0 if one is.
  order    1 - Levenshtein(a, b) / max(|a|, |b|); 1 if both are empty.
  moves    the share of tales whose two move counts are equal.
THE YARDSTICK: content, order and moves between transcriber A and B of the
same arm. THE BASELINE: content and order with each tale's transcription set
against Propp's scheme for another tale, over 1000 random derangements of
the 45 tales, seed 46, the same derangements for every arm and transcriber;
"at or above" counts derangements whose mean is at least the real mean.
THE VERDICT, per arm and transcriber, as frozen: CALIBRATED if content and
order are each at least 0.8 of that arm's A-B figure, both beat the baseline
with at most 50 of 1000 derangements at or above, and v46 accepts at least
75% of the moves; PARTLY CALIBRATED if the baseline criterion holds and
another fails; NOT CALIBRATED if the baseline criterion fails.
REPORTED AND NOT JUDGED: arm C against arm U per measure; each transcriber's
arm C against its own arm U, beside the A-B figure of each arm (if C-U far
exceeds A-B, contact between the arms cannot be ruled out: KeeperLog); the
per-tale figures, with the four tales where the hero rule picks a character
other than Propp's hero marked (149, 151, 163, 164).
THE MEMORY PROBE: probe/<Opus|Sonnet>/Recall.txt, one line per tale, "A093
| scheme or unknown | confidence". A scheme is read with falsify44's
tokenizer and runCorpus.key_of, keeping the same symbols as ours. An
"unknown" recalls nothing and is scored as an empty scheme (content 0,
order 0) over all 45 tales; this reading was fixed after the probe's form
check had shown how many answers were "unknown", and before any
transcription or recalled scheme was read. Scores over the answered tales
alone are reported beside it and not judged. MEMORY IMPLAUSIBLE if, for each
model, recall content is at least 0.15 below its transcriber's arm U content
(Opus: A, Sonnet: B); otherwise MEMORY POSSIBLE.
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
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
os.chdir(ROOT)

import embedCorpus as E  # noqa: E402
import falsify44 as F  # noqa: E402
import parse  # noqa: E402
import runCorpus as R  # noqa: E402
import tragedyScore as TS  # noqa: E402

VOCAB = set(TS.NUM) - TS.PREP
HERO_RULE = {149, 151, 163, 164}
ARMS, LINEAGES = ('U', 'C'), ('A', 'B')
MODELS = (('Opus', 'A'), ('Sonnet', 'B'))


def propp():
    """{tale number: (flat keys, move count)}"""
    def flat(x, elems):
        if isinstance(x, tuple):
            return [k for e in elems[x[1]] for k in flat(e, elems)]
        if isinstance(x, list):
            return [k for row in x for e in row for k in flat(e, elems)]
        return [x] if x in VOCAB else []
    out = {}
    for tale, top, elems, strings, _part, _tail in E.derive():
        keys = [k for lab in top for e in elems[lab] for k in flat(e, elems)]
        out[int(tale)] = (keys, len(strings))
    return out


def load(repo, arm, lineage):
    """{tale number: [entries]} in the order of the notes."""
    ents = collections.defaultdict(list)
    n = 0
    for p in sorted(glob.glob(os.path.join(repo, 'transcriptions', arm, lineage, 'b[0-9]', 'Notes.txt'))):
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^A\d{3}$', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            pos = re.search(r'\d+', f[2])
            n += 1
            ents[int(f[0][1:])].append({'move': f[1], 'pos': int(pos.group()) if pos else 0,
                                        'ev': int(ev.group()) if ev else None, 'sym': f[4],
                                        'undergoer': f[6], 'matters': f[7].upper().startswith('Y'),
                                        'mark': f[7], 'doubt': '?' in f[9], 'line': n})
    return ents


def stream(es):
    return [k for e in sorted(es, key=lambda e: e['line']) if TS.kept(e, 'primary')
            for k in TS.key(e['sym']) if k in VOCAB]


def recall(repo, model):
    """{tale number: keys or None for unknown}"""
    out = {}
    for line in open(os.path.join(repo, 'probe', model, 'Recall.txt'), encoding='utf-8'):
        f = [x.strip() for x in line.split('|')]
        if len(f) != 3 or not re.match(r'^A\d{3}$', f[0]):
            continue
        if f[1].lower() == 'unknown' or not f[1]:
            out[int(f[0][1:])] = None
            continue
        keys = []
        for t in F.tokenize(f[1]):
            if t in ('{', '}', '/'):
                continue
            k, r = R.key_of(t)
            if r is not None and k in VOCAB:
                keys.append(k)
        out[int(f[0][1:])] = keys
    return out


def dice(a, b):
    if not a and not b:
        return 1.0
    ca, cb = collections.Counter(a), collections.Counter(b)
    return 2.0 * sum((ca & cb).values()) / (len(a) + len(b))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def order(a, b):
    if not a and not b:
        return 1.0
    return 1.0 - lev(a, b) / float(max(len(a), len(b)))


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float('nan')


def derangements(n, k, seed):
    rng = random.Random(seed)
    out = []
    while len(out) < k:
        p = list(range(n))
        rng.shuffle(p)
        if all(p[i] != i for i in range(n)):
            out.append(p)
    return out


def accept_share(ents, tales, g):
    ok = tot = 0
    for t in tales:
        for k in TS.moves(ents.get(t, []), 'primary', '', False):
            if not k:
                continue
            tot += 1
            ok += parse.accept(list(k), g.bnf, g.start, g.table)[0]
    return ok, tot


def main(repo):
    P = propp()
    tales = sorted(int(x) for x in open(os.path.join(repo, 'Sample.txt'), encoding='utf-8').read().split())
    assert tales == sorted(P), 'the sample is not the 45 Appendix III tales'
    g = TS.grammar(False)
    pr_ok = sum(R.run(TS.GRAMMAR, 'move')[i][3] for i in range(84))
    D = derangements(len(tales), 1000, 46)
    S, MV, ENTS = {}, {}, {}
    for arm in ARMS:
        for L in LINEAGES:
            e = load(repo, arm, L)
            ENTS[arm, L] = e
            S[arm, L] = {t: stream(e.get(t, [])) for t in tales}
            MV[arm, L] = {t: len({x['move'] for x in e.get(t, [])}) for t in tales}
    print('THE AFANASYEV CALIBRATION: compare.py on %s' % os.path.basename(os.path.normpath(repo)))
    print('Tales: %d. Propp\'s moves: %d; v46 at `move` accepts %d of 84 of his (the protocol: 80).'
          % (len(tales), sum(P[t][1] for t in tales), pr_ok))
    missing = [(a, L, t) for (a, L) in S for t in tales if not ENTS[a, L].get(t)]
    print('Tales without entries: %s' % (missing or 'none'))

    AB = {}
    for arm in ARMS:
        a, b = S[arm, 'A'], S[arm, 'B']
        AB[arm] = (mean(dice(a[t], b[t]) for t in tales), mean(order(a[t], b[t]) for t in tales),
                   mean(MV[arm, 'A'][t] == MV[arm, 'B'][t] for t in tales))
        print('\nYARDSTICK, arm %s, A against B: content %.3f, order %.3f, moves %.1f%%'
              % (arm, AB[arm][0], AB[arm][1], 100 * AB[arm][2]))

    R_ = {}
    for arm in ARMS:
        for L in LINEAGES:
            s = S[arm, L]
            c = mean(dice(s[t], P[t][0]) for t in tales)
            o = mean(order(s[t], P[t][0]) for t in tales)
            m = mean(MV[arm, L][t] == P[t][1] for t in tales)
            bc, bo = [], []
            for p in D:
                bc.append(mean(dice(s[tales[i]], P[tales[p[i]]][0]) for i in range(len(tales))))
                bo.append(mean(order(s[tales[i]], P[tales[p[i]]][0]) for i in range(len(tales))))
            nc, no = sum(x >= c for x in bc), sum(x >= o for x in bo)
            ok, tot = accept_share(ENTS[arm, L], tales, g)
            acc = ok / float(tot) if tot else 0.0
            c1 = c >= 0.8 * AB[arm][0]
            c2 = o >= 0.8 * AB[arm][1]
            c3 = c > mean(bc) and nc <= 50 and o > mean(bo) and no <= 50
            c4 = acc >= 0.75
            verdict = ('CALIBRATED' if c1 and c2 and c3 and c4 else
                       'PARTLY CALIBRATED' if c3 else 'NOT CALIBRATED')
            R_[arm, L] = (c, o, m, acc)
            print('\nARM %s, TRANSCRIBER %s (%s)' % (arm, L, 'Opus' if L == 'A' else 'Sonnet'))
            print('  1. content %.3f against A-B %.3f: ratio %.2f (needs 0.80) %s'
                  % (c, AB[arm][0], c / AB[arm][0] if AB[arm][0] else 0, 'holds' if c1 else 'FAILS'))
            print('  2. order   %.3f against A-B %.3f: ratio %.2f (needs 0.80) %s'
                  % (o, AB[arm][1], o / AB[arm][1] if AB[arm][1] else 0, 'holds' if c2 else 'FAILS'))
            print('  3. baseline: content %.3f, %d of 1000 at or above; order %.3f, %d of 1000 (at most 50) %s'
                  % (mean(bc), nc, mean(bo), no, 'holds' if c3 else 'FAILS'))
            print('  4. v46 accepts %d of %d moves, %.1f%% (needs 75%%) %s'
                  % (ok, tot, 100 * acc, 'holds' if c4 else 'FAILS'))
            print('  moves equal to Propp\'s: %.1f%% (A-B %.1f%%)' % (100 * m, 100 * AB[arm][2]))
            print('  VERDICT: %s' % verdict)

    print('\nARM C AGAINST ARM U (reported, not judged)')
    for L in LINEAGES:
        u, cc = R_['U', L], R_['C', L]
        print('  %s: content %.3f -> %.3f, order %.3f -> %.3f, moves %.1f%% -> %.1f%%, acceptance %.1f%% -> %.1f%%'
              % (L, u[0], cc[0], u[1], cc[1], 100 * u[2], 100 * cc[2], 100 * u[3], 100 * cc[3]))
    print('CONTACT CHECK: each transcriber\'s arm C against its own arm U, beside A-B')
    for L in LINEAGES:
        u, cc = S['U', L], S['C', L]
        print('  %s: C-U content %.3f, order %.3f (A-B: arm U %.3f, %.3f; arm C %.3f, %.3f)'
              % (L, mean(dice(u[t], cc[t]) for t in tales), mean(order(u[t], cc[t]) for t in tales),
                 AB['U'][0], AB['U'][1], AB['C'][0], AB['C'][1]))

    print('\nTHE MEMORY PROBE')
    implausible = True
    for model, L in MODELS:
        rc = recall(repo, model)
        answered = [t for t in tales if rc.get(t)]
        c = mean(dice(rc.get(t) or [], P[t][0]) for t in tales)
        o = mean(order(rc.get(t) or [], P[t][0]) for t in tales)
        ca = mean(dice(rc[t], P[t][0]) for t in answered)
        oa = mean(order(rc[t], P[t][0]) for t in answered)
        below = R_['U', L][0] - c
        implausible = implausible and below >= 0.15
        print('  %s: %d of 45 answered; over all 45, content %.3f, order %.3f; over the answered, content %s, order %s'
              % (model, len(answered), c, o, 'n/a' if not answered else '%.3f' % ca,
                 'n/a' if not answered else '%.3f' % oa))
        print('    its transcriber %s, arm U, content %.3f: recall %.3f below (needs 0.15)' % (L, R_['U', L][0], below))
    print('  VERDICT: %s' % ('MEMORY IMPLAUSIBLE' if implausible else 'MEMORY POSSIBLE'))

    print('\nPER TALE: content and order against Propp (* the hero rule picks another hero)')
    print('  tale  Propp  ' + '  '.join('%s/%s       ' % k for k in sorted(S)))
    for t in tales:
        cells = ['%.2f %.2f' % (dice(S[k][t], P[t][0]), order(S[k][t], P[t][0])) for k in sorted(S)]
        print('  %3d%s  %2d/%d   %s' % (t, '*' if t in HERO_RULE else ' ', len(P[t][0]), P[t][1], '  '.join(cells)))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(os.path.join(CALLER, sys.argv[1])))
