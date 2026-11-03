#!/usr/bin/env python3
"""
split.py -- the induction and checking halves (Induction/InductionProtocol.md section 2, frozen 2026-11-03): within each
corpus and layer, the story ids (both transcribers joined) sorted, shuffled with seed 20261103, and halved, the first half
(the larger, where the count is odd) for induction and the second for checking.

  python split.py    write Induction/Split.txt (refused if it exists and would change)

Only the story ids are read; no unit is counted.
"""
import os
import random

import strings as ST

SEED = 20261103


def main():
    lines = ['# Split.txt -- split.py (InductionProtocol.md section 2): seed %d; induction the first half, checking the second' % SEED]
    for layer, corpora in ST.LAYERS.items():
        for g in corpora:
            ids = ST.stories(layer, g)
            random.Random(SEED).shuffle(ids)
            h = (len(ids) + 1) // 2
            for part, xs in (('induction', ids[:h]), ('checking', ids[h:])):
                lines.append('%s %s %s %d: %s' % (layer, g, part, len(xs), ' '.join(sorted(xs))))
    text = '\n'.join(lines) + '\n'
    if os.path.exists(ST.SPLIT) and open(ST.SPLIT, encoding='utf-8').read() != text:
        raise SystemExit('refusing: Split.txt exists and would change')
    open(ST.SPLIT, 'w', encoding='utf-8', newline='\n').write(text)
    for l in lines[1:]:
        print(l[:60])


if __name__ == '__main__':
    main()
