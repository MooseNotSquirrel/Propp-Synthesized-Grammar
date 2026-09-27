#!/usr/bin/env python3
"""
runCorpus.py -- run a grammar file over the 84 resolved move-strings.

  python runCorpus.py GRAMMAR [--start NAME] [--moves FILE] [--fails]

  --start NAME   the grammar's move symbol (default: its first production)
  --moves FILE   default ResolvedMoves.txt
  --fails        print only the failing moves, comma-separated

The runner of ruling 48's plan, stage 3: a thin driver, not a new engine.
Membership is decided by the grammar itself, through equivCheck.py's
automaton, so the verdict is the grammar's and not a rank table's.

THE DERIVATION RULES, frozen before the first run. They follow
falsify44.py exactly, so that with v44 this runner must reproduce its
verdicts, and with any other grammar a changed verdict is the grammar's
doing and not the derivation's.

  1. Tokens are read with falsify44.py's own tokenizer and reducer.
     Unorderable tokens (X, Y, and apparatus that reduces to no function)
     are skipped. A key falsify44.py files under another function's slot,
     by its ALIAS table, is read as that function: KF, liquidation in the
     form of F, as K, and w, the reward, as W.
     THE FIRST RUN, 2026-09-27, OMITTED THE ALIAS TABLE, and the frozen
     calibration test caught it: with v44 the runner failed eleven moves
     falsify44.py passes, every one on a KF or a w.
  2. Parked pre-crisis cells before the opener are dropped, and reading
     starts at a brace that opens before the opener, both as falsify44.py
     does (logic doc S9).
  3. A brace { X1 / X2 / ... } is repetition in various aspects (p.116,
     Ch. IX n.4). The move passes only if EVERY expansion passes, the
     string with the brace replaced by one of its rows.
  4. The opener is the move's, not a row's. If the move's opener stands
     inside a brace row, any other row of that brace with no opener of
     its own is read with the opener before it. Only 163 I and 164 II
     open inside a brace.

Exit 0 always: a failing move is a finding, not an error.
"""
import itertools
import sys

import equivCheck
import falsify44 as F

OPENERS = ('A', 'a', 'B')
TERMINAL = {alias: key for key, aliases in F.ALIAS.items() for alias in aliases}


def key_of(tok):
    k, r = F.reduce(tok)
    return (TERMINAL.get(k, k), r)


def elements(canon):
    """The move as a list of keys and brace groups (lists of rows)."""
    toks = F.tokenize(canon)
    start = 0
    for idx, t in enumerate(toks):
        if t == '{':
            start = idx
            break
        if t in ('}', '/'):
            continue
        k, _ = key_of(t)
        if k in OPENERS or k not in F.PRE_CRISIS:
            start = idx
            break
    out, i = [], start
    while i < len(toks):
        t = toks[i]
        if t == '{':
            depth, j, inner = 1, i + 1, []
            while j < len(toks) and depth:
                depth += {'{': 1, '}': -1}.get(toks[j], 0)
                if depth:
                    inner.append(toks[j])
                j += 1
            rows, cur = [], []
            for x in inner:
                if x == '/':
                    rows.append(cur)
                    cur = []
                else:
                    k, r = key_of(x)
                    if r is not None:
                        cur.append(k)
            rows.append(cur)
            out.append(rows)
            i = j
            continue
        if t not in ('}', '/'):
            k, r = key_of(t)
            if r is not None:
                out.append(k)
        i += 1
    # Rule 4: the move's opener is shared by the rows of the brace it stands in.
    for e in out:
        if isinstance(e, list):
            with_op = [row for row in e if any(k in OPENERS for k in row)]
            if with_op:
                op = next(k for k in with_op[0] if k in OPENERS)
                for n, row in enumerate(e):
                    if not any(k in OPENERS for k in row):
                        e[n] = [op] + row
            break
        if e in OPENERS:
            break
    return out


def expansions(elems):
    groups = [e if isinstance(e, list) else [[e]] for e in elems]
    for choice in itertools.product(*groups):
        yield [k for part in choice for k in part]


class Grammar:
    def __init__(self, path, start=None):
        ast, self.start = equivCheck.read(path, start, False, {})
        self.sigma = sorted(set().union(*(equivCheck.walk(v, 'term', set())
                                          for v in ast.values())))
        self.trans, self.accept = equivCheck.dfa(ast, self.start, self.sigma)

    def accepts(self, keys):
        q = 1
        for k in keys:
            if k not in self.trans[q]:
                return False
            q = self.trans[q][k]
        return self.accept[q]


def run(path, start=None, moves='ResolvedMoves.txt'):
    """[(tale, move, canon, ok, first failing expansion or None)]"""
    g = Grammar(path, start)
    out = []
    for m in F.load(moves):
        bad = next((x for x in expansions(elements(m['canon']))
                    if not g.accepts(x)), None)
        out.append((m['tale'], m['move'], m['canon'], bad is None, bad))
    return out


def main(argv):
    opts, pos, fails_only, i = {'--start': None, '--moves': 'ResolvedMoves.txt'}, [], False, 0
    while i < len(argv):
        if argv[i] in opts and i + 1 < len(argv):
            opts[argv[i]] = argv[i + 1]
            i += 2
            continue
        if argv[i] == '--fails':
            fails_only = True
        elif argv[i].startswith('-'):
            sys.exit('runCorpus.py: unknown option %s' % argv[i])
        else:
            pos.append(argv[i])
        i += 1
    if len(pos) != 1:
        sys.exit('usage: python runCorpus.py GRAMMAR [--start NAME] [--moves FILE] [--fails]')
    res = run(pos[0], opts['--start'], opts['--moves'])
    failed = [r for r in res if not r[3]]
    if fails_only:
        print(','.join('%s %s' % (r[0], r[1]) for r in failed))
        return 0
    print('%s (start = %s) vs %d resolved move-strings' % (pos[0], opts['--start'] or 'first production', len(res)))
    print('  PASS: %d' % (len(res) - len(failed)))
    print('  FAIL: %d' % len(failed))
    for tale, move, canon, ok, bad in failed:
        print('  %4s %-5s %s' % (tale, move, canon))
        print('             refused: %s' % ' '.join(bad))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
