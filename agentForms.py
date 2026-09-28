#!/usr/bin/env python3
"""
agentForms.py -- how the hero receives the magical agent, tested or not.

  python agentForms.py            the table
  python agentForms.py --summary  one line, as StepTests.txt pins it

Counts every F cell in ResolvedMoves.txt and sorts it three ways:
  tested                     a D or an E stands earlier in the move, which
                             is step 6's rule for the tested agent;
  untested, before departure no D or E, and no departure yet: the agent
                             received at home (p.108);
  untested, after departure  no D or E, but the hero has set out.
Within each, it counts Propp's form of receipt, the superscript on F, as he
defines the nine on pp.44-45: 1 transferred, 2 pointed out, 3 prepared,
4 bought, 5 found, 6 appears of its own accord, 7 eaten or drunk, 8 seized,
9 characters place themselves at the hero's service.

THE READING RULES are runCorpus.py's, which are falsify44.py's: its
tokenizer, reducer and alias table, parked cells left of A dropped (so p.107's
pre-crisis donor sequences are not counted), and reading starting where
falsify44.py starts. Each row of a brace is read on its own, with what came
before the brace as its context, and every F in every row is counted.

CAUTIONS: the counts are small; "tested" means a D or E came earlier in the
move, which does not always mean that test earned this agent.
"""
import collections
import re
import sys

import falsify44 as F
import runCorpus as R

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
FORMS = {1: 'transferred', 2: 'pointed out', 3: 'prepared', 4: 'bought', 5: 'found',
         6: 'appears', 7: 'eaten or drunk', 8: 'seized', 9: 'offers service', None: 'no form marked'}
KINDS = ('tested', 'untested, before departure', 'untested, after departure')


def form(tok):
    m = re.search(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', tok)
    return int(m.group(0).translate(SUP)) if m else None


def tally(moves='ResolvedMoves.txt'):
    cells = collections.Counter()
    forms = collections.defaultdict(collections.Counter)
    where = collections.defaultdict(set)

    def walk(tokens, ctx, label):
        for tok in tokens:
            k, r = R.key_of(tok)
            if r is None:
                continue
            if k == 'F':
                kind = KINDS[0] if ctx & {'D', 'E'} else KINDS[1] if 'up' not in ctx else KINDS[2]
                cells[kind] += 1
                forms[kind][form(tok)] += 1
                where[kind].add(label)
            ctx = ctx | {k}
        return ctx

    for m in F.load(moves):
        toks = F.tokenize(m['canon'])
        label = '%s %s' % (m['tale'], m['move'])
        start = 0
        for i, t in enumerate(toks):
            if t == '{':
                start = i
                break
            if t in ('}', '/'):
                continue
            k, _ = R.key_of(t)
            if k in R.OPENERS or k not in F.PRE_CRISIS:
                start = i
                break
        toks, ctx, i = toks[start:], set(), 0
        while i < len(toks):
            t = toks[i]
            if t == '{':
                depth, j, inner = 1, i + 1, []
                while j < len(toks) and depth:
                    depth += {'{': 1, '}': -1}.get(toks[j], 0)
                    if depth:
                        inner.append(toks[j])
                    j += 1
                rows = [[]]
                for x in inner:
                    if x == '/':
                        rows.append([])
                    else:
                        rows[-1].append(x)
                after = set(ctx)
                for row in rows:
                    after |= walk(row, set(ctx), label)
                ctx, i = after, j
                continue
            if t not in ('}', '/'):
                ctx = walk([t], ctx, label)
            i += 1
    return cells, forms, where


def summary():
    cells, forms, where = tally()
    parts = []
    for kind in KINDS:
        fs = ' '.join('%s:%d' % (k if k is not None else '-', n)
                      for k, n in sorted(forms[kind].items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))
        parts.append('%s %d/%d %s' % (kind.split(',')[0] if kind == 'tested' else
                                     'home' if 'before' in kind else 'road',
                                     cells[kind], len(where[kind]), fs))
    return '; '.join(parts)


def main(argv):
    if argv == ['--summary']:
        print(summary())
        return 0
    cells, forms, where = tally()
    for kind in KINDS:
        print('%-28s %2d F cells in %2d moves' % (kind, cells[kind], len(where[kind])))
        for k, n in sorted(forms[kind].items(), key=lambda kv: (kv[0] is None, kv[0] or 0)):
            print('    F%-2s %-16s %d' % (k if k is not None else '', FORMS[k], n))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
