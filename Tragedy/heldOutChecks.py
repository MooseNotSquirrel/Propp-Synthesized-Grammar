#!/usr/bin/env python3
"""
heldOutChecks.py -- risk checks 2 and 3 (Blocks/PositionNull.txt,
Blocks/Agreement.txt) on the held-out tragedies, P05-P32, now the seal is
lifted: the same programs and frozen rules, with the corpus list replaced by
the held-out plays and the output written beside the P01-P04 runs.

  python heldOutChecks.py position    writes Tragedy/PositionNullHeldOut.txt
  python heldOutChecks.py agreement   writes Tragedy/AgreementHeldOut.txt
  python heldOutChecks.py position-open  P01-P04 only, to check that the bounded
                                      cache reproduces Blocks/PositionNullRun.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

HELD = tuple('P%02d' % i for i in range(5, 33))
TRAG = os.path.join(os.path.dirname(ROOT), 'Tragedy')


CACHE_CAP = 200000


def bound_cache():
    """blockStream.Grammar.ends caches every stretch it is asked about and never
    clears; over the held-out plays and their shuffles that grew past 14 GB. The
    cache is pure, so clearing it when it passes CACHE_CAP entries changes no
    result, only the memory used (checked: `position-open` reproduces the
    committed P01-P04 lines of Blocks/PositionNullRun.txt)."""
    orig = BS.Grammar.ends

    def ends(self, entry, toks):
        if len(self.cache) > CACHE_CAP:
            self.cache.clear()
        return orig(self, entry, toks)
    BS.Grammar.ends = ends


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
    bound_cache()
    if sys.argv[1:] == ['position-open']:
        import positionNull as M
        run(M, lambda: [('tragedy P01-P04', {L: [(v, it) for p in BS.OPEN for v, it in BS.load(TRAG, L, p).items()]
                                              for L in 'AB'})],
            os.path.join(ROOT, 'Blocks', 'PositionNullRun.txt'), os.path.join(HERE, 'PositionNullOpenCheck.txt'))
        sys.exit(0)
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
