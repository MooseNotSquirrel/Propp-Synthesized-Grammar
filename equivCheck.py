#!/usr/bin/env python3
"""
equivCheck.py -- decide whether two Propp EBNF grammars accept the same strings.

  python equivCheck.py GRAMMAR_A GRAMMAR_B [options]

  --start-a NAME   start nonterminal of A (default: its first production)
  --start-b NAME   start nonterminal of B (default: its first production)
  --shared         compare only strings over the terminals BOTH grammars use
  --map X=Y,...    rename terminals in both grammars before comparing,
                   e.g. --map "↑=up,↓=down" to read v43's arrows as v44's
  --optional-a     make every item of A optional before comparing
  --optional-b     the same for B
  --drop-a N,...   treat A's productions named N as matching nothing, so
                   every alternative that needs one falls away
  --drop-b N,...   the same for B
  --probe "X Y Z"  also report whether each grammar accepts this string;
                   may be given more than once

WHY IT EXISTS. A grammar whose named productions never refer back to
themselves generates a regular language, and equality of two regular
languages is decidable. So a regrouping of v44 can be PROVED to accept
exactly v44's strings, rather than sampled on the 84 move-strings. This
program is that proof. It is the first tool of the second project
(ProppFindings.md, FO and its continuation).

HOW. Each grammar is read by parse.py's own reader, so a file means here what
it means to the acceptor. Every nonterminal is expanded in place into a
nondeterministic automaton, that is made deterministic over the compared
alphabet, and the pair of automata is searched breadth first for a state
where one accepts and the other does not. Breadth first means that any
witness printed is a SHORTEST string on which the two grammars disagree.

WHAT IT REFUSES. A grammar in which a named production refers to itself,
directly or through others, is refused and the cycle is named. Some such
grammars are still regular, but this program does not decide which; the
interruption layer of the second project will need a different instrument.

--shared RESTRICTS rather than erases. With it, a string containing a
terminal only one grammar knows is dropped from both languages. Comparing
ProppMidLevelGroupsEbnf.txt with v44 under --shared therefore asks whether
the two agree on every string with no preparatory function in it.

--optional-a and --optional-b wrap every item of every sequence in [ ],
nonterminals and terminals alike. They model "every item made optional",
and nothing subtler.

--drop-a and --drop-b remove a production from a grammar before it is
compared. A grammar that refers back to itself only through a dropped
production is no longer recursive, so it can be compared: v46's step 7 is
proved to be step 6 plus embedding by dropping InterruptingMove.

--probe answers membership without parse.py's LL(1) table, which v44 cannot
build because of its conflict on J. --map applies to probes too. A probe
token outside the compared alphabet is reported as rejected by both.

Exit 0 equivalent, 1 not equivalent, 2 unreadable, recursive or bad usage.
"""
import sys
from collections import deque

import parse


def fail(msg):
    print(msg)
    sys.exit(2)


def children(node):
    """The sub-nodes of a parse.RP node; none for a terminal or nonterminal."""
    if node[0] in ('alt', 'seq'):
        return node[1]
    if node[0] in ('opt', 'star', 'group'):
        return [node[1]]
    return []


def walk(node, kind, out):
    """Collect the names of every node of one kind ('term' or 'nt')."""
    if node[0] == kind:
        out.add(node[1])
    for x in children(node):
        walk(x, kind, out)
    return out


def read(path, start, optional, rename, drop=()):
    try:
        text = open(path, encoding='utf-8').read()
    except OSError as e:
        fail("cannot read %s: %s" % (path, e))
    prods, order = parse.load(text)
    if not order:
        fail("%s: no productions" % path)
    try:
        ast = {n: parse.RP(parse.tokenize(prods[n])).alt() for n in order}
    except (ValueError, AssertionError, IndexError) as e:
        fail("%s: production not readable: %s" % (path, e))
    start = start or order[0]
    if start not in ast:
        fail("%s: no production named %s" % (path, start))

    graph = {n: walk(ast[n], 'nt', set()) for n in ast}
    undef = sorted({r for rs in graph.values() for r in rs if r not in ast}
                   | {d for d in drop if d not in ast})
    if undef:
        fail("%s: undefined nonterminals: %s" % (path, ', '.join(undef)))
    # A dropped production is not entered, so it cannot close a cycle.
    graph = {n: {m for m in rs if m not in drop} for n, rs in graph.items()}

    # Only what the start symbol reaches is the grammar being compared.
    # A reference cycle among those productions is recursion; refuse it.
    colour = {}

    def visit(n, trail):
        colour[n] = 1
        for m in sorted(graph[n]):
            if colour.get(m) == 1:
                cyc = trail[trail.index(m):] + [m]
                fail("%s: recursive production, refused: %s"
                     % (path, ' -> '.join(cyc)))
            if m not in colour:
                visit(m, trail + [m])
        colour[n] = 2

    visit(start, [start])

    def rewrite(node):
        k = node[0]
        if k == 'term':
            return ('term', rename.get(node[1], node[1]))
        if k == 'nt':
            return ('void',) if node[1] in drop else node
        if k == 'alt':
            return ('alt', [rewrite(x) for x in node[1]])
        if k == 'seq':
            items = [rewrite(x) for x in node[1]]
            if optional:
                items = [x if x[0] == 'opt' else ('opt', ('alt', [('seq', [x])]))
                         for x in items]
            return ('seq', items)
        return (k, rewrite(node[1]))

    ast = {n: rewrite(ast[n]) for n in colour}
    return ast, start


class NFA:
    def __init__(self):
        self.eps, self.sym = [], []

    def state(self):
        self.eps.append([])
        self.sym.append([])
        return len(self.eps) - 1

    def build(self, node, ast):
        """Thompson construction, expanding each nonterminal in place."""
        k = node[0]
        s, e = self.state(), self.state()
        if k == 'void':
            return s, e                      # matches nothing: no path s to e
        if k == 'term':
            self.sym[s].append((node[1], e))
        elif k == 'nt':
            a, b = self.build(ast[node[1]], ast)
            self.eps[s].append(a)
            self.eps[b].append(e)
        elif k == 'seq':
            cur = s
            for x in node[1]:
                a, b = self.build(x, ast)
                self.eps[cur].append(a)
                cur = b
            self.eps[cur].append(e)
        else:
            # alt, group, opt, star: each child runs from s to e.
            for x in children(node):
                a, b = self.build(x, ast)
                self.eps[s].append(a)
                self.eps[b].append(e)
                if k == 'star':
                    self.eps[b].append(a)
            if k in ('opt', 'star'):
                self.eps[s].append(e)
        return s, e


def dfa(ast, start, sigma):
    """Subset construction over sigma. State 0 is the dead state, 1 the start."""
    n = NFA()
    s, f = n.build(('nt', start), ast)

    def closure(states):
        stack, seen = list(states), set(states)
        while stack:
            for t in n.eps[stack.pop()]:
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
        return frozenset(seen)

    first = closure([s])
    index = {frozenset(): 0, first: 1}
    trans = [{c: 0 for c in sigma}, None]
    accept = [False, f in first]
    q = deque([first])
    while q:
        S = q.popleft()
        row = {}
        for c in sigma:
            T = closure([t for x in S for (a, t) in n.sym[x] if a == c])
            if T not in index:
                index[T] = len(trans)
                trans.append(None)
                accept.append(f in T)
                q.append(T)
            row[c] = index[T]
        trans[index[S]] = row
    return trans, accept


def minimal_size(trans, accept, sigma):
    """States in the minimal automaton, the dead state included (Moore)."""
    part = [int(a) for a in accept]
    while True:
        ids = {}
        new = [ids.setdefault((part[i],) + tuple(part[trans[i][c]] for c in sigma),
                              len(ids))
               for i in range(len(trans))]
        if len(ids) == len(set(part)):
            return len(ids)
        part = new


def main(argv):
    opts = {'--start-a': None, '--start-b': None, '--map': '',
            '--drop-a': '', '--drop-b': ''}
    flags = {'--shared': False, '--optional-a': False, '--optional-b': False}
    pos, probes = [], []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--probe':
            if i + 1 >= len(argv):
                fail("equivCheck.py: --probe needs a value")
            probes.append(argv[i + 1].split())
            i += 2
            continue
        if a in opts:
            if i + 1 >= len(argv):
                fail("equivCheck.py: %s needs a value" % a)
            opts[a] = argv[i + 1]
            i += 2
            continue
        if a in flags:
            flags[a] = True
        elif a.startswith('-'):
            fail("equivCheck.py: unknown option %s" % a)
        else:
            pos.append(a)
        i += 1
    if len(pos) != 2:
        fail("usage: python equivCheck.py GRAMMAR_A GRAMMAR_B [options]")
    rename = {}
    for pair in filter(None, opts['--map'].split(',')):
        if '=' not in pair:
            fail("equivCheck.py: --map entry %r is not X=Y" % pair)
        x, y = pair.split('=', 1)
        rename[x.strip()] = y.strip()

    drops = {g: set(filter(None, opts['--drop-' + g].split(','))) for g in 'ab'}
    A, sa = read(pos[0], opts['--start-a'], flags['--optional-a'], rename, drops['a'])
    B, sb = read(pos[1], opts['--start-b'], flags['--optional-b'], rename, drops['b'])
    ta = set().union(*(walk(v, 'term', set()) for v in A.values()))
    tb = set().union(*(walk(v, 'term', set()) for v in B.values()))

    for g, path, start, ts, opt in (
            ('A', pos[0], sa, ta, flags['--optional-a']),
            ('B', pos[1], sb, tb, flags['--optional-b'])):
        print("grammar %s: %s  (start = %s%s)" % (
            g, path, start, ", every item optional" if opt else ""))
        print("  terminals (%d): %s" % (len(ts), ' '.join(sorted(ts))))
    if rename:
        print("renamed in both: %s"
              % ', '.join('%s=%s' % kv for kv in sorted(rename.items())))
    if flags['--shared']:
        sigma = sorted(ta & tb)
        print("compared over the SHARED alphabet, %d terminals" % len(sigma))
        for g, only in (('A', ta - tb), ('B', tb - ta)):
            if only:
                print("  dropped, %s only: %s" % (g, ' '.join(sorted(only))))
    else:
        sigma = sorted(ta | tb)
        print("compared over the union alphabet, %d terminals" % len(sigma))

    da, aa = dfa(A, sa, sigma)
    db, ab = dfa(B, sb, sigma)
    print("minimal automaton states, dead state included: A %d, B %d"
          % (minimal_size(da, aa, sigma), minimal_size(db, ab, sigma)))

    def accepts(trans, accept, toks):
        q = 1
        for c in toks:
            if c not in trans[q]:
                return False
            q = trans[q][c]
        return accept[q]

    for toks in probes:
        toks = [rename.get(c, c) for c in toks]
        print("probe  %-24s A %-8s B %s" % (
            ' '.join(toks) or '(empty)',
            'accepts' if accepts(da, aa, toks) else 'rejects',
            'accepts' if accepts(db, ab, toks) else 'rejects'))

    # Breadth-first search of the product automaton. The first disagreement
    # met in each direction is a shortest witness for that direction.
    back = {(1, 1): None}
    q = deque([(1, 1)])
    only = {'A': None, 'B': None}
    while q and not (only['A'] and only['B']):
        p = q.popleft()
        if aa[p[0]] and not ab[p[1]] and only['A'] is None:
            only['A'] = p
        if ab[p[1]] and not aa[p[0]] and only['B'] is None:
            only['B'] = p
        for c in sigma:
            r = (da[p[0]][c], db[p[1]][c])
            if r not in back:
                back[r] = (p, c)
                q.append(r)

    def word(p):
        out = []
        while back[p] is not None:
            p, c = back[p]
            out.append(c)
        return ' '.join(reversed(out)) or '(the empty string)'

    print()
    if only['A'] is None and only['B'] is None:
        print("EQUIVALENT: A and B accept exactly the same strings over the "
              "compared alphabet.")
        return 0
    print("NOT EQUIVALENT.")
    for g, h in (('A', 'B'), ('B', 'A')):
        if only[g] is None:
            print("  every string %s accepts, %s accepts too." % (g, h))
        else:
            print("  shortest string %s accepts and %s rejects: %s"
                  % (g, h, word(only[g])))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
