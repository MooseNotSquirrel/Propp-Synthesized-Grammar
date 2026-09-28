#!/usr/bin/env python3
"""
villainy.py -- what the villain does, and what becomes of him.

  python villainy.py            the tables
  python villainy.py --summary  one line, as StepTests.txt pins it

For every move in ResolvedMoves.txt it finds the opener, the first A, a or
B, as falsify44.py does. For the moves opened by villainy it counts Propp's
form of villainy, the arabic superscript on A, of the nineteen he gives on
pp.30-34; forms written in roman superscripts are counted apart and not
decoded. For the moves opened by villainy and by lack it counts how many
hold struggle H, victory I, liquidation K, pursuit Pr, punishment U and
the wedding W, every brace expanded.

CAUTIONS: U does not record who is punished, and Propp gives punishment to
the sphere of the princess and her father as "punishment of a second
villain" (pp.79-80), the false hero. A dragon killed in combat is a victory,
I, not a punishment. Appendix III records functions, not performers.
"""
import collections
import re
import sys

import runCorpus as R

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
NAMES = {1: 'abducts a person', 2: 'seizes a magical agent', 3: 'spoils the crops',
         4: 'seizes the daylight', 5: 'plunders', 6: 'maims', 7: 'causes a disappearance',
         8: 'demands or entices', 9: 'expels', 10: 'casts into the sea', 11: 'casts a spell',
         12: 'substitution', 13: 'orders a murder', 14: 'murders', 15: 'imprisons',
         16: 'forced marriage', 17: 'cannibalism', 18: 'torments at night', 19: 'declares war'}
OUTCOMES = ('H', 'I', 'K', 'Pr', 'U', 'W')


def tally(moves='ResolvedMoves.txt'):
    forms, outcome = collections.Counter(), {'A': collections.Counter(), 'a': collections.Counter()}
    n = collections.Counter()
    roman = 0
    for m in R.F.load(moves):
        opener = None
        for t in R.F.tokenize(m['canon']):
            k, _ = R.key_of(t)
            if k in ('A', 'a', 'B'):
                opener = (k, t)
                break
        if not opener or opener[0] == 'B':
            continue
        kind, tok = opener
        n[kind] += 1
        keys = set(k for x in R.expansions(R.elements(m['canon'])) for k in x)
        for f in OUTCOMES:
            outcome[kind][f] += f in keys
        if kind == 'A':
            mm = re.search(r'A[₀-₉]*([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', tok)
            if mm:
                forms[int(mm.group(1).translate(SUP))] += 1
            elif re.search(r'[ⁱᵛˣ]', tok):
                roman += 1
            else:
                forms[None] += 1
    return forms, roman, outcome, n


def summary():
    forms, roman, outcome, n = tally()
    fs = ' '.join('%s:%d' % (k if k is not None else '-', v)
                  for k, v in sorted(forms.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))
    oc = lambda k: ' '.join('%s %d' % (f, outcome[k][f]) for f in OUTCOMES)
    return 'villainy %d: %s roman %d; outcomes %s; lack %d: %s' % (n['A'], fs, roman, oc('A'), n['a'], oc('a'))


def main(argv):
    if argv == ['--summary']:
        print(summary())
        return 0
    forms, roman, outcome, n = tally()
    print('moves opened by villainy: %d, by lack: %d' % (n['A'], n['a']))
    for k, v in sorted(forms.items(), key=lambda kv: -kv[1]):
        print('  A%-3s %-24s %d' % (k if k else '', NAMES.get(k, 'no form marked'), v))
    print('  roman-numeral subforms, not decoded: %d' % roman)
    for f in OUTCOMES:
        print('  %-3s villainy %2d/%d   lack %2d/%d' % (f, outcome['A'][f], n['A'], outcome['a'][f], n['a']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
