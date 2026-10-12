#!/usr/bin/env python3
"""twoLayerForm.py GENRE -- form check of an act transcription (tale, fable or tragedy): every listed
event has an entry, every act and relation is from Acts.md, every entry is marked Y or N. Judges nothing."""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twoLayer as T  # noqa: E402

RELS = {'kin', 'spouse', 'above', 'below', 'ally', 'enemy', 'stranger', 'divine', 'self', 'none'}
g = sys.argv[1]
ev = collections.defaultdict(set)
paths = [os.path.join(T.OUT, g, 'Events.txt')] if g != 'tragedy' else glob.glob(os.path.join(T.OUT, 'tragedy', 'plays', 'P*', 'Events.txt'))
for p in paths:
    for l in open(p, encoding='utf-8'):
        f = [x.strip() for x in l.split('|')]
        if len(f) >= 3 and f[1].isdigit():
            ev[f[0]].add(int(f[1]))
for d in sorted(glob.glob(os.path.join(T.OUT, g, 'acts', '*', '*'))):
    got = collections.defaultdict(set)
    bad_act, bad_rel, unmarked, n = collections.Counter(), collections.Counter(), 0, 0
    for l in open(os.path.join(d, 'Notes.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|', 9)]
        if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
            continue
        n += 1
        e = re.search(r'\d+', f[1])
        if e:
            got[f[0].split('/')[0]].add(int(e.group()))
        if f[2].lower() not in T.ACTS:
            bad_act[f[2]] += 1
        if f[5].lower() not in RELS:
            bad_rel[f[5]] += 1
        if f[6][:1].upper() not in ('Y', 'N'):
            unmarked += 1
    stories = sorted(got)
    missing = sum(len(ev[s] - got[s]) for s in stories)
    print('%s %s: stories %d, entries %d, events without entry %d, acts not in the list %s, relations not in the list %s, unmarked %d'
          % (g, os.path.relpath(d, os.path.join(T.OUT, g, 'acts')), len(stories), n, missing, dict(bad_act), dict(bad_rel), unmarked))
