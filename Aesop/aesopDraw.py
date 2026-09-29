#!/usr/bin/env python3
"""
aesopDraw.py -- draw the Aesop sample and pilot as AesopPrediction.txt part 1
fixes them, and write Sample.txt and Pilot.txt into the Aesop repository.

  python aesopDraw.py AESOP_REPO
"""
import os
import random
import sys

repo = sys.argv[1]
ids = [l.split(' | ', 1)[0] for l in open(os.path.join(repo, 'Fables.txt'), encoding='utf-8') if l.strip()]
assert len(ids) == 313, len(ids)
sample = sorted(random.Random(2109).sample(ids, 100))
rest = [i for i in ids if i not in set(sample)]
pilot = sorted(random.Random(2110).sample(rest, 3))
open(os.path.join(repo, 'Sample.txt'), 'w', encoding='utf-8').write('\n'.join(sample) + '\n')
open(os.path.join(repo, 'Pilot.txt'), 'w', encoding='utf-8').write('\n'.join(pilot) + '\n')
print('sample', len(sample), sample[:5], '...', sample[-3:])
print('pilot', pilot)
