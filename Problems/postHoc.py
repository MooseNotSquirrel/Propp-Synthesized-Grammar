#!/usr/bin/env python3
"""
postHoc.py -- after the verdict: the frozen scoring without the plays a describer
did not read in full (P13 and P14, describer B-q8; P26, describer B-q10), dropped
for both describers, and for describer B only. Reported, not judged; the frozen verdict stands.

  python postHoc.py      writes Problems/PostHoc.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import problems as Pm  # noqa: E402

DROP = {'P13', 'P14', 'P26'}


def main():
    gen = {s: g for s, g in Pm.genre_of().items() if s not in DROP}
    D = Pm.described()
    rep, held, _, _ = Pm.evaluate(D, gen, '# PostHoc.txt -- postHoc.py, after the verdict: without P13, P14 and P26; reported, not judged.',
                                  Pm.PREDICTIONS)
    rep += ['', 'Without the three plays: %d of %d predictions hold -> %s' % (held, len(Pm.PREDICTIONS), Pm.verdict(held, len(Pm.PREDICTIONS)))]
    D2 = {'A': D['A'], 'B': {s: xs for s, xs in D['B'].items() if s not in DROP}}
    rep2, held2, _, _ = Pm.evaluate(D2, Pm.genre_of(), '# The same with the three plays dropped for describer B only, who did not read them in full.',
                                    Pm.PREDICTIONS)
    rep += ['', ''] + rep2 + ['', 'Without the three plays for B only: %d of %d predictions hold -> %s'
                              % (held2, len(Pm.PREDICTIONS), Pm.verdict(held2, len(Pm.PREDICTIONS)))]
    open(os.path.join(HERE, 'PostHoc.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep[-14:]))


if __name__ == '__main__':
    main()
