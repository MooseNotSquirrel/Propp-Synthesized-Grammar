#!/usr/bin/env python3
"""
runSteps.py -- run the frozen step tests of SynthesizedProppGrammar.

  python runSteps.py STEP

Reads StepTests.txt. Every test names the steps over which it binds: N
means step N onward, N-M steps N to M. The grammar is one file that every
step changes, so a test a later step is planned to break is written with
a closing step when it is frozen, not retired after it fails. Tests for
later steps are counted as pending and tests already closed are counted
as closed; neither can fail the run. A test is written, with its source,
BEFORE the step it tests is built, and is never edited to fit a result.

Kinds, one test per line as  step | kind | arguments | source :

  equivalent A B [options]  equivCheck.py finds A and B equivalent; any
                            options are passed to it unchanged
  includes A B [options]    every string A accepts, B accepts too
                            (equivCheck.py; options passed unchanged)
  accept G "x y z"          G accepts the string
  reject G "x y z"          G rejects the string
  ll1 G T1 T2 ...           G's LL(1) conflicts fall on exactly the listed
                            terminals; '-' means G must be LL(1)
  corpusfails G S "t m,..." run over ResolvedMoves.txt by runCorpus.py
                            with start symbol S, G fails exactly the listed
                            moves; '-' means it fails none

A grammar's start symbol is its first production. A token outside a
grammar's alphabet makes the string rejected. An argument written
TAG:FILE names FILE as it stood at git tag TAG, so a test can compare the
grammar with an earlier step of itself, e.g. step4:ProppEBNF46.txt.

Exit 0 every binding test passes, 1 otherwise, 2 on a malformed test file.
"""
import os
import re
import shlex
import subprocess
import sys
import tempfile

import equivCheck
import parse
import runCorpus

TESTS = 'StepTests.txt'
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')


def conflicts(path):
    """Terminals on which the grammar's LL(1) table has a conflict."""
    prods, order = parse.load(open(path, encoding='utf-8').read())
    bnf, start = parse.desugar(prods, order)
    nullable = set()
    changed = True
    while changed:
        changed = False
        for a, ps in bnf.items():
            if a not in nullable and any(
                    all(s[0] == 'n' and s[1] in nullable for s in p) for p in ps):
                nullable.add(a)
                changed = True

    first = {a: set() for a in bnf}

    def fseq(seq):
        out = set()
        for s in seq:
            out |= {s[1]} if s[0] == 't' else first[s[1]]
            if not (s[0] == 'n' and s[1] in nullable):
                break
        return out

    def nullseq(seq):
        return all(s[0] == 'n' and s[1] in nullable for s in seq)

    changed = True
    while changed:
        changed = False
        for a, ps in bnf.items():
            n = len(first[a])
            for p in ps:
                first[a] |= fseq(p)
            changed |= len(first[a]) != n
    follow = {a: set() for a in bnf}
    follow[start].add('$')
    changed = True
    while changed:
        changed = False
        for a, ps in bnf.items():
            for p in ps:
                for i, s in enumerate(p):
                    if s[0] != 'n':
                        continue
                    n = len(follow[s[1]])
                    follow[s[1]] |= fseq(p[i + 1:])
                    if nullseq(p[i + 1:]):
                        follow[s[1]] |= follow[a]
                    changed |= len(follow[s[1]]) != n
    found = set()
    for a, ps in bnf.items():
        seen = set()
        for p in ps:
            pred = fseq(p) | (follow[a] if nullseq(p) else set())
            found |= pred & seen
            seen |= pred
    return found


def accepts(path, toks):
    ast, start = equivCheck.read(path, None, False, {})
    sigma = sorted(set().union(*(equivCheck.walk(v, 'term', set())
                                 for v in ast.values())))
    if any(t not in sigma for t in toks):
        return False
    trans, accept = equivCheck.dfa(ast, start, sigma)
    q = 1
    for t in toks:
        q = trans[q][t]
    return accept[q]


def tagged(args):
    """Replace each TAG:FILE argument with a temporary copy of that version."""
    out = []
    for a in args:
        m = re.match(r'^(step\d+):(.+)$', a)
        if not m:
            out.append(a)
            continue
        text = subprocess.run(['git', 'show', '%s:%s' % m.groups()], capture_output=True,
                              check=True).stdout
        fd, path = tempfile.mkstemp(suffix='_' + m.group(1) + '.txt')
        with os.fdopen(fd, 'wb') as fh:
            fh.write(text)
        out.append(path)
    return out


def run(kind, args):
    """Return (passed, detail)."""
    args = tagged(args)
    if kind == 'equivalent':
        p = subprocess.run([sys.executable, 'equivCheck.py'] + args,
                           capture_output=True, encoding='utf-8', env=ENV)
        last = [x for x in p.stdout.split('\n') if x.strip()]
        detail = ' / '.join(x.strip() for x in last[-3:]) if p.returncode else last[-1]
        return p.returncode == 0, detail
    if kind == 'includes':
        p = subprocess.run([sys.executable, 'equivCheck.py'] + args,
                           capture_output=True, encoding='utf-8', env=ENV)
        ok = p.returncode == 0 or 'every string A accepts, B accepts too.' in p.stdout
        last = [x.strip() for x in p.stdout.splitlines() if x.strip()]
        return ok, ' / '.join(last[-2:])
    if kind in ('accept', 'reject'):
        got = accepts(args[0], args[1].split())
        return got == (kind == 'accept'), 'accepted' if got else 'rejected'
    if kind == 'll1':
        want = set() if args[1:] == ['-'] else set(args[1:])
        got = conflicts(args[0])
        return got == want, 'conflicts on: %s' % (' '.join(sorted(got)) or 'none')
    if kind == 'corpusfails':
        want = set() if args[2] == '-' else {x.strip() for x in args[2].split(',')}
        got = {'%s %s' % (r[0], r[1]) for r in runCorpus.run(args[0], args[1]) if not r[3]}
        detail = 'fails %d' % len(got)
        if got != want:
            detail += '; unexpected: %s; expected but passing: %s' % (
                ', '.join(sorted(got - want)) or 'none',
                ', '.join(sorted(want - got)) or 'none')
        return got == want, detail
    raise ValueError('unknown kind %r' % kind)


def main(argv):
    if len(argv) != 1 or not argv[0].isdigit():
        print('usage: python runSteps.py STEP')
        return 2
    upto = int(argv[0])
    tests = []
    for n, line in enumerate(open(TESTS, encoding='utf-8'), 1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        cells = [c.strip() for c in line.split(' | ')]
        span = cells[0].split('-') if len(cells) == 4 else []
        if not span or len(span) > 2 or not all(s.isdigit() for s in span):
            print('%s line %d: not  step | kind | arguments | source' % (TESTS, n))
            return 2
        first, last = int(span[0]), int(span[-1]) if len(span) == 2 else None
        tests.append((n, first, last, cells[1], shlex.split(cells[2]), cells[3]))
    failed = pending = closed = 0
    for n, step, last, kind, args, source in tests:
        if step > upto:
            pending += 1
            continue
        if last is not None and last < upto:
            closed += 1
            continue
        try:
            ok, detail = run(kind, args)
        except (OSError, ValueError, IndexError) as e:
            ok, detail = False, 'ERROR %s' % e
        except SystemExit:
            ok, detail = False, 'ERROR grammar not readable'
        failed += not ok
        print('%-4s step %d  line %-3d %-10s %s' % (
            'PASS' if ok else 'FAIL', step, n, kind, ' '.join(args)))
        print('                         %s' % detail)
        if not ok:
            print('                         source: %s' % source)
    print()
    print('%d binding, %d failed, %d pending for later steps, '
          '%d closed by an earlier step'
          % (len(tests) - pending - closed, failed, pending, closed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
