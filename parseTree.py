#!/usr/bin/env python3
"""
parseTree.py -- parse with a grammar's LL(1) table and report where each
function lands.

  python parseTree.py GRAMMAR "tokens"        print each token's ancestors
  python parseTree.py GRAMMAR --corpus        which groups the accepted
                                              corpus moves use

It builds the table with parse.py, unchanged, and runs the same predictive
parse, recording for every consumed token the chain of named nonterminals
above it. The helper nonterminals parse.py makes when it expands EBNF carry
'#' in their names, such as StruggleAndOutcome_star#23, and are left out of the chain:
they are notation, not groups. The grammar must be LL(1); parse.py refuses
to build a table for one that is not.

--corpus reads ResolvedMoves.txt with runCorpus.py's derivation, parses
each accepted move at the grammar's `move` symbol, and counts, for every
named group, the moves whose parse contains it. A move carrying a brace is
parsed once per expansion and counted once. This is the raw material for
the catalog SemanticBundling.md was meant to become.

Exit 0 on success, 1 if a string given on the command line is rejected.
"""
import sys
from collections import defaultdict

import parse


def build(path, start=None):
    """The LL(1) table, and the start symbol to parse from."""
    bnf, first, table = parse.build(open(path, encoding='utf-8').read())
    return bnf, (start or first), table


def ancestors(tokens, grammar):
    """[(token, [ancestor names, root first])] or None if rejected."""
    bnf, start, table = grammar
    inp = list(tokens) + ['$']
    # stack entries: (symbol, chain of named ancestors above that symbol)
    stack = [(('t', '$'), []), (('n', start), [])]
    out, pos = [], 0
    while stack:
        (kind, name), chain = stack.pop()
        a = inp[pos]
        if kind == 't':
            if name != a:
                return None
            if a == '$':
                return out
            out.append((a, chain))
            pos += 1
            continue
        if a not in table[name]:
            return None
        here = chain if '#' in name else chain + [name]
        for sym in reversed(table[name][a]):
            stack.append((sym, here))
    return out if inp[pos] == '$' else None


def corpus(path):
    import runCorpus
    grammar = build(path, 'move')
    moves = defaultdict(set)
    accepted = 0
    for m in runCorpus.F.load('ResolvedMoves.txt'):
        parses = [ancestors(x, grammar)
                  for x in runCorpus.expansions(runCorpus.elements(m['canon']))]
        if any(p is None for p in parses):
            continue
        accepted += 1
        label = '%s %s' % (m['tale'], m['move'])
        for p in parses:
            for _tok, chain in p:
                for g in chain:
                    moves[g].add(label)
    print('%s: groups in the %d accepted moves' % (path, accepted))
    for g, ms in sorted(moves.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print('  %-24s %2d' % (g, len(ms)))
    return 0


def main(argv):
    if len(argv) == 2 and argv[1] == '--corpus':
        return corpus(argv[0])
    if len(argv) != 2:
        sys.exit('usage: python parseTree.py GRAMMAR "tokens" | GRAMMAR --corpus')
    res = ancestors(argv[1].split(), build(argv[0]))
    if res is None:
        print('rejected')
        return 1
    for tok, chain in res:
        print('%-5s %s' % (tok, ' > '.join(chain)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
