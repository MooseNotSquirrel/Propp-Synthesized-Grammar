#!/usr/bin/env python3
"""
postHoc.py -- after the verdict: where myth sits on the two frame settings resting on
many moves (villainy or lack to liquidation, departure to return), leaving out test and
reaction to the gift, which stands on 10 and 12 myth moves and splits the transcribers
(60% and 25%). Reported, not judged; the frozen result stands.

  python postHoc.py      writes Genre/PostHoc.txt
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import myth as M  # noqa: E402

K = M.K


def main():
    T = K.transcribed()
    dims = [M.FRAME[0], M.FRAME[1]]
    rep = ['# PostHoc.txt -- postHoc.py, after the verdict; reported, not judged.', '']
    for L in 'AB':
        corp = {'myth': K.Moves(M.myth_moves(L))}
        corp.update({g: K.Moves(T[L][g]) for g in ('tale', 'fable', 'tragedy')})
        sh = {g: [mv.test(f, s)['share'] for _, f, s in dims] for g, mv in corp.items()}
        d = {g: math.sqrt(sum((sh['myth'][i] - sh[g][i]) ** 2 for i in range(len(dims)))) for g in ('tale', 'fable', 'tragedy')}
        rep.append('%s: shares (liquidation, return) myth %.2f %.2f, tale %.2f %.2f, fable %.2f %.2f, tragedy %.2f %.2f; '
                   'distance to tale %.3f, fable %.3f, tragedy %.3f; nearest %s'
                   % (L, *sh['myth'], *sh['tale'], *sh['fable'], *sh['tragedy'], d['tale'], d['fable'], d['tragedy'], min(d, key=d.get)))
    open(os.path.join(HERE, 'PostHoc.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
