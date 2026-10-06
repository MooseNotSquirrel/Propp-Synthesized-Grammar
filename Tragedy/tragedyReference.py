#!/usr/bin/env python3
"""
tragedyReference.py -- the tragedies against the transcribed wondertales, as
ReferenceComparison.md freezes it.

  python tragedyReference.py TRAGEDY_REPO AFANASYEV_REPO            P01-P04, for form
  python tragedyReference.py TRAGEDY_REPO AFANASYEV_REPO --lifted   all 32, once the seal lifts

Per story: coverage, v46 acceptance at `move` (as shipped), and the share of
function pairs backward against Propp's numbering, each as tragedyScore.py
computes it. A play with k heroes is the mean of its k versions. The test:
difference of means, tragedy minus wondertale, against 10,000 relabellings,
seed 46, two-sided; DIFFER if p <= 0.05 for both transcribers in the same
direction, DO NOT DIFFER if p > 0.05 for both, UNSETTLED otherwise.
"""
import collections
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CALLER = os.getcwd()
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Calibration'))
import tragedyScore as TS  # noqa: E402
import compare as C  # noqa: E402

OPEN = ('P01', 'P02', 'P03', 'P04')
MEASURES = ('coverage', 'acceptance', 'backward')


def story(es, n_events, g):
    """{measure: value or None} for one transcription of one story."""
    covered = {e['ev'] for e in es if TS.kept(e, 'primary')}
    cov = len([i for i in range(1, n_events + 1) if i in covered]) / float(n_events) if n_events else None
    ms = [k for k in TS.moves(es, 'primary', '', False) if k]
    acc = (sum(TS.parse.accept(list(k), g.bnf, g.start, g.table)[0] for k in ms) / float(len(ms))) if ms else None
    back = TS.inversions([(TS.sequence(es, 'primary'), 1.0)])
    return {'coverage': cov, 'acceptance': acc, 'backward': back}


def load(repo, lineage, lifted):
    """TS.load, opening no sealed play's transcription unless the seal is lifted."""
    ents = collections.defaultdict(list)
    n = 0
    for pid in sorted(os.listdir(os.path.join(repo, 'transcriptions', lineage))):
        if not re.match(r'^P\d{2}$', pid) or (not lifted and pid not in OPEN):
            continue
        p = os.path.join(repo, 'transcriptions', lineage, pid, 'Notes.txt')
        if not os.path.exists(p):
            continue
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


def tragedy(repo, lineage, lifted, g):
    ents = load(repo, lineage, lifted)
    per = collections.defaultdict(list)
    for vid, pid, hero, w, n, told in TS.plays(repo):
        if not lifted and pid not in OPEN:
            continue
        per[pid].append(story(ents.get(vid, []), n, g))
    out = {}
    for pid, vs in per.items():
        out[pid] = {m: (C.mean(v[m] for v in vs if v[m] is not None)
                        if any(v[m] is not None for v in vs) else None) for m in MEASURES}
    return out


def tales(repo, lineage, g):
    n = collections.Counter()
    for l in open(os.path.join(repo, 'Events.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|', 2)]
        if len(f) == 3 and re.match(r'^A\d{3}$', f[0]) and f[1].isdigit():
            n[int(f[0][1:])] += 1
    ents = C.load(repo, 'U', lineage)
    return {t: story(ents.get(t, []), n[t], g) for t in sorted(n)}


def relabel_p(a, b, n=10000, seed=46):
    rng = random.Random(seed)
    obs = C.mean(a) - C.mean(b)
    pool = list(a) + list(b)
    hits = 0
    for _ in range(n):
        rng.shuffle(pool)
        d = C.mean(pool[:len(a)]) - C.mean(pool[len(a):])
        hits += abs(d) >= abs(obs) - 1e-12
    return obs, (hits + 1) / float(n + 1)


def main(argv):
    lifted = '--lifted' in argv
    argv = [a for a in argv if a != '--lifted']
    if len(argv) != 2:
        sys.exit(__doc__)
    trepo, arepo = (os.path.join(CALLER, a) for a in argv)
    g = TS.grammar(False)
    print('THE TRAGEDIES AGAINST THE TRANSCRIBED WONDERTALES (%s)'
          % ('all plays' if lifted else 'P01-P04 only, for form: NOT JUDGED'))
    res = {}
    for L in ('A', 'B'):
        tr, wt = tragedy(trepo, L, lifted, g), tales(arepo, L, g)
        print('\nTRANSCRIBER %s: %d plays, %d tales' % (L, len(tr), len(wt)))
        for m in MEASURES:
            a = [v[m] for v in tr.values() if v[m] is not None]
            b = [v[m] for v in wt.values() if v[m] is not None]
            d, p = relabel_p(a, b)
            res[L, m] = (d, p)
            print('  %-10s tragedy %.3f (n %d)  wondertale %.3f (n %d)  difference %+.3f  p %.4f'
                  % (m, C.mean(a), len(a), C.mean(b), len(b), d, p))
    print('\nVERDICTS%s' % ('' if lifted else ' (form only, not judged)'))
    for m in MEASURES:
        (da, pa), (db, pb) = res['A', m], res['B', m]
        if pa <= 0.05 and pb <= 0.05 and (da > 0) == (db > 0):
            v = 'DIFFER (%s)' % ('tragedy higher' if da > 0 else 'tragedy lower')
        elif pa > 0.05 and pb > 0.05:
            v = 'DO NOT DIFFER'
        else:
            v = 'UNSETTLED'
        print('  %-10s %s' % (m, v))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
