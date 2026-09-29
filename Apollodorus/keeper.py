#!/usr/bin/env python3
"""
keeper.py -- the keeper's steps for the Apollodorus test. It transcribes
nothing and reads no transcription except to check its form.

  python keeper.py merge WORK        merge WORK/census/{L1,L2,L3,E} into
                                     ApollodorusCensus.txt and
                                     ApollodorusEvents.txt here, and check
                                     that every episode's count matches its
                                     events and every section is covered
  python keeper.py pilot             draw the three pilot episodes

The pilot draw is fixed before the census exists: from the episodes with
five events or more that are not variants, sorted by identifier,
random.Random(PILOT_SEED).sample(..., 3).
"""
import random
import re
import sys

PARTS = ('L1', 'L2', 'L3', 'E')
PILOT_SEED = 93


def census_rows(path='ApollodorusCensus.txt'):
    rows = []
    for line in open(path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|')]
        if len(f) >= 7 and re.match(r'^(L[123]|E)-\d+', f[0]):
            rows.append({'id': f[0], 'span': f[1], 'figure': f[2], 'n': int(re.match(r'\d+', f[3]).group()),
                         'hero': f[4].replace('hero:', '').strip(), 'connected': f[5],
                         'variant': f[6].replace('variant of:', '').strip()})
    return rows


def merge(work):
    census, events, problems = [], [], []
    for part in PARTS:
        c = open('%s/census/%s/Census.txt' % (work, part), encoding='utf-8').read().splitlines()
        e = open('%s/census/%s/Events.txt' % (work, part), encoding='utf-8').read().splitlines()
        census += [l for l in c if l.strip()]
        events += [l for l in e if l.strip()]
    open('ApollodorusCensus.txt', 'w', encoding='utf-8').write('\n'.join(census) + '\n')
    open('ApollodorusEvents.txt', 'w', encoding='utf-8').write('\n'.join(events) + '\n')
    rows = census_rows()
    per = {}
    for l in events:
        f = [x.strip() for x in l.split('|')]
        per[f[0]] = per.get(f[0], 0) + 1
    for r in rows:
        if per.get(r['id'], 0) != r['n']:
            problems.append('%s: census says %d events, events file has %d' % (r['id'], r['n'], per.get(r['id'], 0)))
    unknown = set(per) - {r['id'] for r in rows}
    problems += ['events for unlisted episode %s' % u for u in sorted(unknown)]
    cited = set()
    for l in events:
        f = [x.strip() for x in l.split('|')]
        cited.add(f[2])
    sections = [l.split('|')[0].strip() for src in ('Library.txt', 'Epitome.txt')
                for l in open(src, encoding='utf-8')]
    uncited = [s for s in sections if s not in cited]
    long5 = [r for r in rows if r['n'] >= 5 and r['variant'] in ('', '-')]
    print('episodes %d, events %d, five or more and not a variant %d' % (len(rows), len(events), len(long5)))
    print('sections with no event cited: %d (genealogy or etiology only, or missed)' % len(uncited))
    print(' '.join(uncited))
    for p in problems:
        print('PROBLEM', p)
    return 0 if not problems else 1


def pilot():
    rows = census_rows()
    pool = sorted(r['id'] for r in rows if r['n'] >= 5 and r['variant'] in ('', '-'))
    print(' '.join(random.Random(PILOT_SEED).sample(pool, 3)))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['merge'] and len(a) == 2:
        sys.exit(merge(a[1]))
    if a == ['pilot']:
        sys.exit(pilot())
    sys.exit(__doc__)
