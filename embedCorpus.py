#!/usr/bin/env python3
"""
embedCorpus.py -- the second derivation of the corpus: whole tales, with
Propp's interruptions kept as embedded moves, and a runner over them.

  python embedCorpus.py --check              calibrate the derivation
  python embedCorpus.py GRAMMAR [--fails]    parse every tale with GRAMMAR

Stage 1 of the first project, resolve.py, discharges every combination
marker and emits one flat string per move. This derivation keeps the
interruptions, so a grammar in which a move can contain a move can meet the
corpus (ruling 48's plan, stage 4; finding BJ's second derivation).

THE DERIVATION RULES, frozen before the first run.

  1. A tale is its moves in printed order, separated by '/'.
  2. An interruption marker <N> in a move's row (p.93, methods 2 and 3;
     Ch. IX n.4) is replaced by move N itself, bracketed ⟨ ... ⟩, and move
     N is not repeated at top level. Four markers carry a numeral: 138 II's
     <III>, 159 I's <II>, 159 III's <IV>, inside a brace row, and 162 I's
     <II>. Nesting is followed if a marker ever stands inside an inserted
     move.
  3. Interruption dots with no numeral, in 155 III, 155 IV and 167 I, name
     no move to insert. They are removed, as resolve.py removes them, and
     stay unresolved: Propp prints no indication of which move breaks the
     thread there.
  4. A shared ending (125 and 155, p.93 method 5) is attached once, to the
     last move that shares it, which is where Propp prints it. resolve.py
     copies it onto every sharing move so each can be parsed alone; a tale
     string needs it only once.
  5. Everything else is read exactly as runCorpus.py reads a move, which is
     falsify44.py's reading: its tokenizer, reducer and alias table,
     overflow and parked cells dropped, parked pre-crisis cells dropped, a
     brace passing only if every expansion passes, and a brace's rows
     sharing the move's opener.

CALIBRATION (--check): every move of the 84 appears exactly once, at top
level or embedded, and each move's string, with its markers removed and the
shared-ending rule allowed for, is resolve.py's canonical string.

Exit 0 on success; --check exits 1 if the calibration fails.
"""
import itertools
import re
import sys

import falsify44 as F
import resolve
import runCorpus

TOKENS = 'TaleTokenStreamsV4Utf8.txt'
OPEN, CLOSE, SEP = '⟨', '⟩', '/'
MARK = re.compile(r'^<([IVX]+)>$')


def move_strings(tale):
    """{label: canonical string with <N> markers kept}, in printed order."""
    sharers = [m['label'] for m in tale['moves'] if '<<shared>>' in m['raw']]
    out = {}
    for mv in tale['moves']:
        s = mv['raw'].replace('<<shared>>', ' ')
        s = re.sub(r'\.\.\.', ' ', s)                          # rule 3
        if tale['shared'] and sharers and mv['label'] == sharers[-1]:
            s += ' ' + tale['shared']                           # rule 4
        canon, _full = resolve.split_overflow(re.sub(r'\s+', ' ', s).strip())
        out[mv['label']] = canon
    return out


def elements(canon):
    """runCorpus.elements, with a marker kept as ('embed', label)."""
    toks = F.tokenize(canon)
    start = 0
    for idx, t in enumerate(toks):
        if t == '{':
            start = idx
            break
        if t in ('}', '/') or MARK.match(t):
            continue
        k, _ = runCorpus.key_of(t)
        if k in runCorpus.OPENERS or k not in F.PRE_CRISIS:
            start = idx
            break

    def item(t):
        m = MARK.match(t)
        if m:
            return ('embed', m.group(1))
        k, r = runCorpus.key_of(t)
        return k if r is not None else None

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
                elif item(x) is not None:
                    cur.append(item(x))
            rows.append(cur)
            out.append(rows)
            i = j
            continue
        if t not in ('}', '/') and item(t) is not None:
            out.append(item(t))
        i += 1
    ops = runCorpus.OPENERS
    for e in out:                                               # rule 5, shared opener
        if isinstance(e, list):
            with_op = [row for row in e if any(k in ops for k in row)]
            if with_op:
                op = next(k for k in with_op[0] if k in ops)
                for n, row in enumerate(e):
                    if not any(k in ops for k in row):
                        e[n] = [op] + row
            break
        if e in ops:
            break
    return out


def derive():
    """[(tale, [top-level labels], {label: elements}, {label: canonical})]"""
    out = []
    for tale in resolve.parse_corpus(TOKENS):
        strings = move_strings(tale)
        elems = {lab: elements(s) for lab, s in strings.items()}
        embedded = {m.group(1) for s in strings.values() for m in
                    (MARK.match(t) for t in F.tokenize(s)) if m}
        top = [lab for lab in strings if lab not in embedded]
        out.append((tale['tale'], top, elems, strings))
    return out


def expand_move(label, elems):
    def options(e):
        if isinstance(e, tuple):
            return [[OPEN] + x + [CLOSE] for x in expand_move(e[1], elems)]
        if isinstance(e, list):                                 # a brace: its rows
            return [sum(choice, []) for row in e
                    for choice in itertools.product(*[options(x) for x in row])]
        return [[e]]
    return [sum(choice, []) for choice in itertools.product(*[options(e) for e in elems[label]])]


def expand_tale(top, elems):
    per = [expand_move(lab, elems) for lab in top]
    for choice in itertools.product(*per):
        toks = []
        for n, part in enumerate(choice):
            toks += ([SEP] if n else []) + part
        yield toks


def calibrate():
    """(ok, detail): the derivation against resolve.py."""
    problems, nmoves, nembedded = [], 0, 0
    for tale, top, elems, strings in derive():
        refs = [m.group(1) for s in strings.values() for m in
                (MARK.match(t) for t in F.tokenize(s)) if m]
        for r in refs:
            if r not in strings:
                problems.append('%s: <%s> names no move' % (tale, r))
        if len(refs) != len(set(refs)):
            problems.append('%s: a move is inserted twice' % tale)
        nmoves += len(strings)
        nembedded += len(refs)
        src = [t for t in resolve.parse_corpus(TOKENS) if t['tale'] == tale][0]
        flat = {m['move']: m['canonical'] for m in resolve.resolve(src)}
        sharers = [m['label'] for m in src['moves'] if '<<shared>>' in m['raw']]
        for lab, s in strings.items():
            mine = re.sub(r'\s+', ' ', re.sub(r'<[IVX]+>', ' ', s)).strip()
            theirs = flat[lab]
            if lab in sharers[:-1] and src['shared']:
                theirs = resolve.split_overflow(theirs[:len(theirs) - len(src['shared'])].strip())[0]
            if mine != theirs:
                problems.append('%s %s: %r differs from resolve.py %r' % (tale, lab, mine, theirs))
    detail = '%d moves, %d embedded' % (nmoves, nembedded)
    if nmoves != 84:
        problems.append('expected 84 moves')
    return not problems, detail + ('; ' + '; '.join(problems) if problems else '; every move string agrees with resolve.py')


def run(path):
    """[(tale, ok, first rejected expansion or None)]"""
    import parse
    bnf, start, table = parse.build(open(path, encoding='utf-8').read())
    out = []
    for tale, top, elems, _s in derive():
        bad = next((x for x in expand_tale(top, elems)
                    if not parse.accept(x, bnf, start, table)[0]), None)
        out.append((tale, bad is None, bad))
    return out


def main(argv):
    if argv == ['--check']:
        ok, detail = calibrate()
        print(('CALIBRATED: ' if ok else 'NOT CALIBRATED: ') + detail)
        return 0 if ok else 1
    if not argv or len(argv) > 2:
        sys.exit('usage: python embedCorpus.py --check | GRAMMAR [--fails]')
    res = run(argv[0])
    failed = [r for r in res if not r[1]]
    if argv[1:] == ['--fails']:
        print(','.join(r[0] for r in failed))
        return 0
    print('%s vs %d tales: PASS %d, FAIL %d' % (argv[0], len(res), len(res) - len(failed), len(failed)))
    for tale, _ok, bad in failed:
        print('  %s refused: %s' % (tale, ' '.join(bad)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
