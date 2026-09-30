#!/usr/bin/env python3
"""
fableDraw.py -- draw the held-out fables as FablePrediction.txt fixes them.

  python fableDraw.py AESOP_REPO OUT_REPO

Reads Fables.txt, Sample.txt and Pilot.txt from the Aesop repository and
writes Sample.txt (100 identifiers, sorted) into the held-out repository.
"""
import os
import random
import sys

aesop, out = sys.argv[1], sys.argv[2]
ids = [l.split(' | ', 1)[0] for l in open(os.path.join(aesop, 'Fables.txt'), encoding='utf-8') if l.strip()]
used = set()
for f in ('Sample.txt', 'Pilot.txt'):
    used |= {l.strip() for l in open(os.path.join(aesop, f), encoding='utf-8') if l.strip()}
rest = [i for i in ids if i not in used]
assert len(ids) == 313 and len(rest) == 210, (len(ids), len(rest))
held = sorted(random.Random(3401).sample(rest, 100))
open(os.path.join(out, 'Sample.txt'), 'w', encoding='utf-8').write('\n'.join(held) + '\n')
print('held-out', len(held), held[:5], '...', held[-3:])
