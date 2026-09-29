#!/usr/bin/env python3
"""
reaction.py -- the hero's reaction E and the transmission F: does the sign
on E carry over to F?

  python reaction.py              the table, and every move where an agent
                                  follows a negative reaction
  python reaction.py --summary    one line, as StepTests.txt pins it
  python reaction.py --breaks     only the moves that break p.46, or '-'

Printed p.46: "in the face of a negative reaction on the part of the hero,
one encounters only F neg. (the transmission does not take place), or F
contr. (the unfortunate hero is severely punished)". The note to p.46 says
Appendix III marks the negative result with a minus, F-, and F contr. as
F=; an unsigned F is therefore a transmission.

It reads the FULL move-strings resolve.py makes from
TaleTokenStreamsV4Utf8.txt, parked and overflow cells kept, because
p.107's inverted sequence parks a D E F before A and the canonical strings
drop it. Each E is paired with the next F after it in the same move, before any
further E; with none, it is paired with nothing. Signed and unsigned E are
counted apart: p.46's claim is about the negative reaction only. A shared ending copied onto two moves holds no E or F, so the
copying over-counts nothing here.
"""
import collections
import re
import sys

import resolve

SOURCE = 'TaleTokenStreamsV4Utf8.txt'
MARKS = re.compile('[⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ⁱᵛˣ₊₋=*]')


def moves(path=SOURCE):
    for tale in resolve.parse_corpus(path):
        for m in resolve.resolve(tale):
            yield m['tale'], m['move'], m['full']


def cells(full):
    for tok in full.split():
        tok = re.sub(r'^(?:overflow|park)\[', '', tok).strip('{}[]/')
        if tok:
            yield MARKS.sub('', tok), tok


def result(tok):
    if '₋' in tok:
        return 'F-'
    if '=' in tok:
        return 'F='
    return 'F+' if '₊' in tok else 'F'


def tally(path=SOURCE):
    pairs = collections.Counter()
    breaks = []
    for tale, mv, full in moves(path):
        cs = list(cells(full))
        for i, (base, tok) in enumerate(cs):
            if base != 'E':
                continue
            sign = 'E-' if '₋' in tok else 'E+' if '₊' in tok else 'E'
            got = 'none'
            for base2, tok2 in cs[i + 1:]:
                if base2 == 'E':
                    break
                if base2.startswith('F'):
                    got = result(tok2)
                    break
            pairs[sign, got] += 1
            if sign == 'E-' and got in ('F', 'F+'):
                breaks.append('%s %s' % (tale, mv))
    return pairs, breaks


def summary():
    pairs, breaks = tally()
    row = lambda s: ' '.join('%s %d' % (f, pairs[s, f]) for f in ('F+', 'F', 'F-', 'F=', 'none'))
    n = lambda s: sum(v for (k, _), v in pairs.items() if k == s)
    return ('E- %d: %s; E+ %d: %s; E unsigned %d: %s'
            % (n('E-'), row('E-'), n('E+'), row('E+'), n('E'), row('E')))


def main(argv):
    pairs, breaks = tally()
    if argv == ['--summary']:
        print(summary())
        return 0
    if argv == ['--breaks']:
        print(', '.join(breaks) or '-')
        return 0
    print('%-4s %4s %4s %4s %4s %5s' % ('', 'F+', 'F', 'F-', 'F=', 'none'))
    for s in ('E-', 'E+', 'E'):
        print('%-4s %4d %4d %4d %4d %5d' % ((s,) + tuple(pairs[s, f] for f in ('F+', 'F', 'F-', 'F=', 'none'))))
    print('an agent after a negative reaction: %s' % (', '.join(breaks) or 'none'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
