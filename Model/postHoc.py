#!/usr/bin/env python3
"""
postHoc.py -- after the verdict: does structure add to length? The frozen model left length
out and lost to length alone for transcriber A. Here length (the log of a story's functions)
is added to the full model, and set against length alone. Reported, not judged.

  python postHoc.py      writes Model/PostHoc.txt
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402


def main():
    rep = ['# PostHoc.txt -- postHoc.py, after the verdict; reported, not judged.', '']
    for L in 'AB':
        rows = M.table(M.stories(L))
        sp = M.split(rows)
        fit = [r for r in rows if sp[r[1]] == 'fit']
        test = [r for r in rows if sp[r[1]] == 'test']
        Xf, yf = M.matrix(fit, M.GROUP_SETS['all'])
        Xt, yt = M.matrix(test, M.GROUP_SETS['all'])
        lf = np.array([[np.log(r[3])] for r in fit]); lt = np.array([[np.log(r[3])] for r in test])
        both = M.balanced(yt, M.fit_predict(np.hstack([Xf, lf]), yf, np.hstack([Xt, lt]))[0])
        alone = M.balanced(yt, M.fit_predict(lf, yf, lt)[0])
        rep.append('%s: length alone %.3f; the full model without length %.3f; the full model with length %.3f' % (
            L, alone, M.balanced(yt, M.fit_predict(Xf, yf, Xt)[0]), both))
    open(os.path.join(HERE, 'PostHoc.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
