#!/usr/bin/env python3
"""
heldOutChecks.py -- risk checks 2 and 3 (Blocks/PositionNull.txt,
Blocks/Agreement.txt) on the held-out tragedies, P05-P32, now the seal is
lifted: the same programs and frozen rules, with the corpus list replaced by
the held-out plays and the output written beside the P01-P04 runs.

  python heldOutChecks.py position    writes Tragedy/PositionNullHeldOut.txt
  python heldOutChecks.py agreement   writes Tragedy/AgreementHeldOut.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

HELD = tuple('P%02d' % i for i in range(5, 33))
TRAG = os.path.join(os.path.dirname(ROOT), 'Tragedy')


def run(mod, corpora, target, out):
    mod.corpora = corpora
    real_open = open

    def redirect(path, *a, **k):
        if os.path.abspath(str(path)) == os.path.abspath(target):
            path = out
        return real_open(path, *a, **k)
    mod.open = redirect
    mod.main()


if __name__ == '__main__':
    BS.OPEN = HELD
    if sys.argv[1:] == ['position']:
        import positionNull as M
        run(M, lambda: [('tragedy P05-P32', {L: [(v, it) for p in HELD for v, it in BS.load(TRAG, L, p).items()]
                                              for L in 'AB'})],
            os.path.join(ROOT, 'Blocks', 'PositionNullRun.txt'), os.path.join(HERE, 'PositionNullHeldOut.txt'))
    elif sys.argv[1:] == ['agreement']:
        import blockAgreement as M
        t = os.path.join(TRAG, 'transcriptions')
        run(M, lambda: [('tragedy P05-P32', [M.read([os.path.join(t, L, p, 'Notes.txt') for p in HELD]) for L in 'AB'])],
            os.path.join(ROOT, 'Blocks', 'AgreementRun.txt'), os.path.join(HERE, 'AgreementHeldOut.txt'))
    else:
        sys.exit(__doc__)
