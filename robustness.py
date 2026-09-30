#!/usr/bin/env python3
"""
robustness.py -- risk check 5 (Blocks/Robustness.txt): the block effect under
three input readings, primary, secondary and nodoubt.

  python robustness.py          writes Blocks/RobustnessRun.txt
"""
import collections
import glob
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

SHUFFLES, SEED = 200, 46
PARENT = os.path.dirname(ROOT)


def read(paths, reading):
    """{version: items}, the functions the input reading keeps matched."""
    out = collections.OrderedDict()
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PF]\d{2}', f[0]):
                continue
            keys = BS.TS.key(f[4], extended=True)
            y = f[7].upper().startswith('Y')
            keep = {'primary': y, 'secondary': True, 'nodoubt': y and '?' not in f[9]}[reading]
            items = out.setdefault(f[0], [])
            if not keys:
                items.append('(X)')
            else:
                items += [k if keep else '(%s)' % k for k in keys]
    return out


def corpora():
    for name, repo in (('training fables', 'Aesop'), ('held-out fables', 'Fables')):
        yield name, {L: sorted(glob.glob(os.path.join(PARENT, repo, 'transcriptions', L, 'b[1-4]', 'Notes.txt')))
                     for L in 'AB'}
    trag = os.path.join(PARENT, 'Tragedy', 'transcriptions')
    yield 'tragedy P01-P04', {L: [os.path.join(trag, L, p, 'Notes.txt') for p in BS.OPEN] for L in 'AB'}


def main():
    g = BS.Grammar()
    rep = ['# RobustnessRun.txt -- robustness.py, risk check 5 (Blocks/Robustness.txt).',
           '# Share of matched functions inside blocks: real, shuffled mean, shuffles at or above; HOLDS or not.', '']
    held = {}
    for name, paths in corpora():
        for L in 'AB':
            for inp in ('primary', 'secondary', 'nodoubt'):
                vers = read(paths[L], inp)
                for reading in ('blocks', 'strict'):
                    rng = random.Random(SEED)
                    real = tot = 0
                    sh = [0] * SHUFFLES
                    for v, items in vers.items():
                        i, t = BS.coverage(BS.transform(items, g, reading))
                        real, tot = real + i, tot + t
                        yp = [k for k, it in enumerate(items) if not BS.transparent(it)]
                        for s in range(SHUFFLES):
                            toks = [items[k] for k in yp]
                            rng.shuffle(toks)
                            it2 = list(items)
                            for k, tk in zip(yp, toks):
                                it2[k] = tk
                            sh[s] += BS.coverage(BS.transform(it2, g, reading))[0]
                    mean = sum(sh) / SHUFFLES
                    ge = sum(1 for x in sh if x >= real)
                    ok = real > mean and ge <= 10
                    held[(name, L, reading, inp)] = ok
                    rep.append('%-16s %s %-6s %-9s %4d functions  real %5.1f%%  shuffled %5.1f%%  at/above %3d  %s'
                               % (name, L, reading, inp, tot, 100.0 * real / tot, 100.0 * mean / tot, ge,
                                  'HOLDS' if ok else 'does not hold'))
        rep.append('')
    bad = ['%s %s %s %s' % k for k, ok in held.items()
           if k[3] != 'primary' and held[(k[0], k[1], k[2], 'primary')] and not ok]
    rep.append('ROBUST: every cell that holds in the primary reading holds in the other two.' if not bad else
               'NOT ROBUST in: ' + '; '.join(bad))
    open(os.path.join(ROOT, 'Blocks', 'RobustnessRun.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
