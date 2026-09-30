#!/usr/bin/env python3
"""
blockStream.py -- turn a transcription's token stream into a stream of
catalog entries, and back.

  python blockStream.py test                  run the frozen BlockTests.txt
  python blockStream.py run TRAGEDY_REPO      write Tragedy/BlockStreams.txt
                                              and Tragedy/BlockPatterns.txt

THE TRANSFORM, fixed with BlockTests.txt before this program was written:
  1. The stream is a transcription's Notes.txt in order, move lines ignored,
     since the transcribers draw them differently. Functions marked Y are
     matched; an X, or a function marked N, is transparent: kept in place in
     parentheses and skipped for matching, so it never breaks a block and is
     never lost. Symbols are reduced as the tragedy scoring reduces them.
  2. The grammar is ProppEBNF46.txt with +tragedy,reversal. An entry covers a
     stretch when the grammar derives the stretch from the entry's production.
  3. From the left, the longest stretch any entry covers becomes a block,
     written Entry[tokens], with the transparent tokens inside it kept; a
     block needs at least two functions, and a function no block takes stays
     bare. Among entries covering the same stretch the one deepest in the
     grammar wins, the most specific; then the catalog's order.
  4. Two readings: `blocks`, the pairs and groups; `all`, every entry, spans
     and move included. Neither uses the Early and Late twins or the
     notation, whose position cannot be judged out of context: out of
     context their unmarked twins stand for them.
  5. Reversing drops the entry names and brackets, and gives the stream back
     token for token.
  6. Only P01-P04 are read. The plays from P05 are the tragedy test's
     held-out plays, sealed until the tragedy block grammar is frozen.
The baseline: each version's Y functions shuffled in place, 200 times, seed
46; reported against the real stream, not judged.
"""
import collections
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import parse  # noqa: E402
import runSteps  # noqa: E402
import tragedyScore as TS  # noqa: E402  (chdirs to ROOT; its loader is not used)

OPEN = ('P01', 'P02', 'P03', 'P04')
GRAMMAR = os.path.join(ROOT, 'ProppEBNF46.txt')
EXTENSIONS = ['tragedy', 'reversal']
BLOCKS = ['preparatorySection', 'RuleViolation', 'InformationGathering', 'DeceptionTrap',
          'complication', 'UntestedAcquisition', 'TestedAcquisition', 'StruggleAndOutcome',
          'ReturnJourney', 'PursuitFirst', 'RescueFirst', 'Ordeal', 'FraudPosture',
          'TaskAndSolution', 'Endgame']
ALL = ['tale', 'move', 'TroubleToLiquidation', 'Development', 'AfterLiquidation', 'BeforeTheTrouble',
       'MoveTrigger', 'Evasion'] + BLOCKS
SHUFFLES, SEED = 200, 46


class Grammar:
    def __init__(self):
        path = runSteps.switched(GRAMMAR, EXTENSIONS, None)
        self.text = open(path, encoding='utf-8').read()
        prods, order = parse.load(self.text)
        self.depth = {'tale': 0}
        frontier = ['tale']
        while frontier:
            nxt = []
            for n in frontier:
                for r in re.findall(r'[A-Za-z_]\w*', prods[n]):
                    if r in prods and r not in self.depth:
                        self.depth[r] = self.depth[n] + 1
                        nxt.append(r)
            frontier = nxt
        self.tables = {}
        for e in ALL:
            bnf, start, table = parse.build('startHere = %s\n' % e + self.text)
            self.tables[e] = (start, table)

    def longest(self, entry, toks):
        """The longest prefix of toks the entry derives, by one LL(1) pass."""
        start, table = self.tables[entry]
        stack = [('t', '$'), ('n', start)]
        best, pos = 0, 0
        while True:
            if pos and self.can_end(stack, table):
                best = pos
            if pos == len(toks):
                return best
            a = toks[pos]
            while stack and stack[-1][0] == 'n':
                A = stack.pop()[1]
                if a not in table[A]:
                    return best
                stack.extend(reversed(table[A][a]))
            if not stack or stack.pop()[1] != a:
                return best
            pos += 1

    @staticmethod
    def can_end(stack, table):
        st = list(stack)
        while st:
            top = st.pop()
            if top[0] == 't':
                return top[1] == '$'
            if '$' not in table[top[1]]:
                return False
            st.extend(reversed(table[top[1]]['$']))
        return False


def transparent(item):
    return item.startswith('(')


def transform(items, g, entries):
    """items: the stream, transparent tokens in parentheses. Returns block items."""
    ys = [i for i, it in enumerate(items) if not transparent(it)]
    toks = [items[i] for i in ys]
    rank = {e: (-g.depth.get(e, 0), k) for k, e in enumerate(entries)}
    covered = {}
    i = 0
    while i < len(toks):
        found = [(g.longest(e, toks[i:]), e) for e in entries]
        n = max(f[0] for f in found)
        if n >= 2:
            e = min((f[1] for f in found if f[0] == n), key=lambda x: rank[x])
            covered[ys[i]] = (ys[i + n - 1], e)
            i += n
        else:
            i += 1
    out, k = [], 0
    while k < len(items):
        if k in covered:
            end, e = covered[k]
            out.append('%s[%s]' % (e, ' '.join(items[k:end + 1])))
            k = end + 1
        else:
            out.append(items[k])
            k += 1
    return out


def reverse(blocks):
    return re.sub(r'[A-Za-z]\w*\[', '', ' '.join(blocks)).replace(']', '').split()


def stream(notes_path):
    """{version: [items]} from one Notes.txt, in order."""
    out = collections.OrderedDict()
    for line in open(notes_path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
        if len(f) < 10 or not re.match(r'^P\d{2}', f[0]):
            continue
        keys = TS.key(f[4], extended=True)
        y = f[7].upper().startswith('Y')
        items = out.setdefault(f[0], [])
        if not keys:
            items.append('(X)')
        else:
            items += [k if y else '(%s)' % k for k in keys]
    return out


def load(repo, lineage, pid):
    if pid not in OPEN:
        raise PermissionError('%s is sealed: only %s are read' % (pid, ', '.join(OPEN)))
    return stream(os.path.join(repo, 'transcriptions', lineage, pid, 'Notes.txt'))


def coverage(blocks):
    inside = sum(1 for b in blocks if '[' in b for t in reverse([b]) if not transparent(t))
    total = sum(1 for t in reverse(blocks) if not transparent(t))
    return inside, total


def counts(blocks):
    return collections.Counter(b.split('[', 1)[0] for b in blocks if '[' in b)


def test(repo=None):
    g = Grammar()
    repo = repo or os.path.join(os.path.dirname(ROOT), 'Tragedy')
    passed = failed = 0
    for n, line in enumerate(open(os.path.join(ROOT, 'BlockTests.txt'), encoding='utf-8'), 1):
        if line.startswith('#') or '|' not in line:
            continue
        kind, inp, want, _src = [x.strip() for x in line.split('|', 3)]
        if kind in ('blocks', 'all'):
            got = ' '.join(transform(inp.split(), g, BLOCKS if kind == 'blocks' else ALL))
            ok = got == want
        elif kind == 'roundtrip':
            bad = []
            for pid in inp.split():
                for L in 'AB':
                    for v, items in load(repo, L, pid).items():
                        for entries in (BLOCKS, ALL):
                            if reverse(transform(items, g, entries)) != items:
                                bad.append('%s %s' % (L, v))
            got, ok = ('exact' if not bad else 'differs: ' + ', '.join(bad)), not bad
        elif kind == 'sealed':
            try:
                load(repo, 'A', inp)
                got = 'read'
            except PermissionError:
                got = 'refused'
            ok = got == want
        else:
            continue
        passed += ok
        failed += not ok
        print('%s line %d %-9s %s%s' % ('PASS' if ok else 'FAIL', n, kind, inp,
                                        '' if ok else '\n     want: %s\n     got:  %s' % (want, got)))
    print('%d passed, %d failed' % (passed, failed))
    return 1 if failed else 0


def run(repo):
    g = Grammar()
    rng = random.Random(SEED)
    lines = ['# BlockStreams.txt -- written by blockStream.py from P01-P04; see its header.', '']
    report = ['# BlockPatterns.txt -- written by blockStream.py: blocks in the real streams against',
              '# the same Y functions shuffled in place, %d times, seed %d. Reported, not judged.' % (SHUFFLES, SEED), '']
    for L in 'AB':
        for reading, entries in (('blocks', BLOCKS), ('all', ALL)):
            real_in = real_tot = 0
            shuf_in = [0] * SHUFFLES
            real_c, shuf_c = collections.Counter(), collections.Counter()
            for pid in OPEN:
                for v, items in load(repo, L, pid).items():
                    b = transform(items, g, entries)
                    lines.append('%s %s %s | %s' % (L, reading, v, ' '.join(b)))
                    i, t = coverage(b)
                    real_in, real_tot = real_in + i, real_tot + t
                    real_c.update(counts(b))
                    ypos = [k for k, it in enumerate(items) if not transparent(it)]
                    for s in range(SHUFFLES):
                        toks = [items[k] for k in ypos]
                        rng.shuffle(toks)
                        sh = list(items)
                        for k, tk in zip(ypos, toks):
                            sh[k] = tk
                        sb = transform(sh, g, entries)
                        shuf_in[s] += coverage(sb)[0]
                        shuf_c.update(counts(sb))
            mean = sum(shuf_in) / SHUFFLES
            ge = sum(1 for x in shuf_in if x >= real_in)
            report.append('TRANSCRIBER %s, reading %s: functions inside blocks %d of %d (%.1f%%); '
                          'shuffled mean %.1f (%.1f%%); shuffles at or above the real: %d of %d'
                          % (L, reading, real_in, real_tot, 100.0 * real_in / real_tot, mean,
                             100.0 * mean / real_tot, ge, SHUFFLES))
            for e in entries:
                if real_c[e] or shuf_c[e]:
                    report.append('  %-22s real %3d   shuffled mean %6.2f'
                                  % (e, real_c[e], shuf_c[e] / SHUFFLES))
            report.append('')
            lines.append('')
    here = os.path.join(ROOT, 'Tragedy')
    open(os.path.join(here, 'BlockStreams.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
    open(os.path.join(here, 'BlockPatterns.txt'), 'w', encoding='utf-8').write('\n'.join(report))
    print('\n'.join(report))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['test']:
        sys.exit(test())
    if a[:1] == ['run'] and len(a) == 2:
        sys.exit(run(os.path.abspath(os.path.join(TS.CALLER, a[1]))))
    sys.exit(__doc__)
