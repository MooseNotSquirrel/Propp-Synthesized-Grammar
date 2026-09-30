#!/usr/bin/env python3
"""
blockStream.py -- turn a transcription's token stream into a stream of
catalog entries, and back.

  python blockStream.py test                     run the frozen BlockTests.txt
  python blockStream.py run tragedy TRAGEDY_REPO write Tragedy/BlockStreams.txt
                                                 and Tragedy/BlockPatterns.txt
  python blockStream.py run aesop AESOP_REPO     write Blocks/AesopStreams.txt
                                                 and Blocks/AesopPatterns.txt
  python blockStream.py run fables FABLES_REPO   the held-out fables: write
                                                 Blocks/FablesStreams.txt and
                                                 Blocks/FablesPatterns.txt

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
  4. Three readings: `blocks`, the pairs and groups; `strict`, the pairs and
     groups counted only when their defining functions are present (see
     whole()); `all`, every entry, spans and move included. None uses the
     Early and Late twins or the notation, whose position cannot be judged
     out of context: out of context their unmarked twins stand for them.
  5. In the blocks and strict readings a stretch whose reverse an entry
     covers is a reversed block, Entry~[tokens], the tokens in the stream's
     order; up to 12 functions. At equal length Propp's order wins.
  6. Reversing drops the entry names, marks and brackets, and gives the
     stream back token for token.
  7. Of the tragedies only P01-P04 are read. The plays from P05 are the
     tragedy test's held-out plays, sealed until its block grammar is frozen.
The baseline: each version's Y functions shuffled in place, 200 times, seed
46; reported against the real stream, not judged.
"""
import collections
import glob
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
READINGS = collections.OrderedDict([
    ('blocks', (BLOCKS, False, True)),
    ('strict', ([e for e in BLOCKS if e != 'UntestedAcquisition'], True, True)),
    ('all', (ALL, False, False))])
MAXREV = 12
SHUFFLES, SEED = 200, 46


def whole(e, t):
    """The strict reading: the entry's defining functions are present in t,
    t in Propp's order."""
    s = set(t)
    if e == 'RuleViolation':
        return {'γ', 'δ'} <= s
    if e == 'InformationGathering':
        return {'ε', 'ζ'} <= s
    if e == 'DeceptionTrap':
        return {'η', 'θ'} <= s
    if e == 'complication':
        return t[0] in ('A', 'a', 'B') and any(x in ('B', 'C', 'up') for x in t[1:])
    if e == 'TestedAcquisition':
        return bool(s & {'D', 'E'}) and 'F' in s
    if e == 'StruggleAndOutcome':
        return 'H' in s and bool(s & {'I', 'I-'})
    if e in ('PursuitFirst', 'RescueFirst'):
        return {'Pr', 'Rs'} <= s
    if e == 'FraudPosture':
        return {'o', 'L'} <= s
    if e == 'TaskAndSolution':
        return {'M', 'N'} <= s
    if e == 'Endgame':
        return len(s & {'Q', 'Ex', 'U', 'W'}) >= 2
    if e == 'ReturnJourney':
        return 'down' in s and bool(s & {'Pr', 'Rs'})
    if e == 'Ordeal':
        return bool(s & {'o', 'L'}) and bool(s & {'M', 'N'})
    if e == 'preparatorySection':
        return sum(p <= s for p in ({'γ', 'δ'}, {'ε', 'ζ'}, {'η', 'θ'})) >= 2
    return True


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
        self.cache = {}

    def ends(self, entry, toks):
        """Every length of a prefix of toks the entry derives, by one LL(1) pass."""
        k = (entry, tuple(toks))
        if k in self.cache:
            return self.cache[k]
        start, table = self.tables[entry]
        stack = [('t', '$'), ('n', start)]
        out, pos = [], 0
        while True:
            if pos and self.can_end(stack, table):
                out.append(pos)
            if pos == len(toks):
                break
            a = toks[pos]
            ok = True
            while stack and stack[-1][0] == 'n':
                A = stack.pop()[1]
                if a not in table[A]:
                    ok = False
                    break
                stack.extend(reversed(table[A][a]))
            if not ok or not stack or stack.pop()[1] != a:
                break
            pos += 1
        self.cache[k] = out
        return out

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


def transform(items, g, reading):
    """items: the stream, transparent tokens in parentheses. Returns block items."""
    entries, strict, rev = READINGS[reading]
    ys = [i for i, it in enumerate(items) if not transparent(it)]
    toks = [items[i] for i in ys]
    rank = {e: (-g.depth.get(e, 0), k) for k, e in enumerate(entries)}
    covered = {}
    i = 0
    while i < len(toks):
        rest = toks[i:]
        best = None
        for e in entries:
            for n in reversed(g.ends(e, rest)):
                if n >= 2 and (not strict or whole(e, rest[:n])):
                    c = (-n, 0, rank[e], e)
                    best = c if best is None or c < best else best
                    break
            if rev:
                seg = rest[:MAXREV]
                for n in range(len(seg), 1, -1):
                    r = seg[:n][::-1]
                    if (best is None or n >= -best[0]) and n in g.ends(e, r) and (not strict or whole(e, r)):
                        c = (-n, 1, rank[e], e)
                        best = c if best is None or c < best else best
                        break
        if best:
            n = -best[0]
            covered[ys[i]] = (ys[i + n - 1], best[3] + ('~' if best[1] else ''))
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
    return re.sub(r'[A-Za-z]\w*~?\[', '', ' '.join(blocks)).replace(']', '').split()


def stream(notes_path, out=None):
    """{version: [items]} from one Notes.txt, in order."""
    out = collections.OrderedDict() if out is None else out
    for line in open(notes_path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
        if len(f) < 10 or not re.match(r'^[PF]\d{2}', f[0]):
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


def load_aesop(repo, lineage, batches=('b1', 'b2', 'b3', 'b4')):
    out = collections.OrderedDict()
    for b in batches:
        stream(os.path.join(repo, 'transcriptions', lineage, b, 'Notes.txt'), out)
    return out


def coverage(blocks):
    inside = sum(1 for b in blocks if '[' in b for t in reverse([b]) if not transparent(t))
    total = sum(1 for t in reverse(blocks) if not transparent(t))
    return inside, total


def counts(blocks):
    return collections.Counter(b.split('[', 1)[0] for b in blocks if '[' in b)


def shape(blocks):
    return ' '.join(b.split('[', 1)[0] if '[' in b else b for b in blocks if not transparent(b))


def test():
    g = Grammar()
    trag = os.path.join(os.path.dirname(ROOT), 'Tragedy')
    aesop = os.path.join(os.path.dirname(ROOT), 'Aesop')
    fables = os.path.join(os.path.dirname(ROOT), 'Fables')
    passed = failed = 0
    for n, line in enumerate(open(os.path.join(ROOT, 'BlockTests.txt'), encoding='utf-8'), 1):
        if line.startswith('#') or '|' not in line:
            continue
        kind, inp, want, _src = [x.strip() for x in line.split('|', 3)]
        if kind in READINGS:
            got = ' '.join(transform(inp.split(), g, kind))
            ok = got == want
        elif kind in ('roundtrip', 'roundtrip3', 'aesoproundtrip', 'fablesroundtrip'):
            bad = []
            for src in inp.split():
                for L in 'AB':
                    if kind == 'aesoproundtrip':
                        vs = load_aesop(aesop, L, (src,))
                    elif kind == 'fablesroundtrip':
                        vs = load_aesop(fables, L, (src,))
                    else:
                        vs = load(trag, L, src)
                    for v, items in vs.items():
                        for reading in READINGS:
                            if reverse(transform(items, g, reading)) != items:
                                bad.append('%s %s %s' % (L, v, reading))
            got, ok = ('exact' if not bad else 'differs: ' + ', '.join(bad[:10])), not bad
        elif kind == 'sealed':
            try:
                load(trag, 'A', inp)
                got = 'read'
            except PermissionError:
                got = 'refused'
            ok = got == want
        else:
            continue
        passed += ok
        failed += not ok
        print('%s line %d %-14s %s%s' % ('PASS' if ok else 'FAIL', n, kind, inp,
                                         '' if ok else '\n     want: %s\n     got:  %s' % (want, got)))
    print('%d passed, %d failed' % (passed, failed))
    return 1 if failed else 0


def run(corpus, repo):
    g = Grammar()
    rng = random.Random(SEED)
    if corpus == 'tragedy':
        versions = {L: [(v, it) for pid in OPEN for v, it in load(repo, L, pid).items()] for L in 'AB'}
        here, sname, pname = os.path.join(ROOT, 'Tragedy'), 'BlockStreams.txt', 'BlockPatterns.txt'
    else:
        versions = {L: list(load_aesop(repo, L).items()) for L in 'AB'}
        stem = 'Aesop' if corpus == 'aesop' else 'Fables'
        here, sname, pname = os.path.join(ROOT, 'Blocks'), stem + 'Streams.txt', stem + 'Patterns.txt'
        os.makedirs(here, exist_ok=True)
    lines = ['# %s -- written by blockStream.py (%s); see its header.' % (sname, corpus), '']
    report = ['# %s -- written by blockStream.py (%s): blocks in the real streams against' % (pname, corpus),
              '# the same Y functions shuffled in place, %d times, seed %d. Reported, not judged.'
              % (SHUFFLES, SEED), '']
    for L in 'AB':
        for reading in READINGS:
            entries = READINGS[reading][0]
            real_in = real_tot = 0
            shuf_in = [0] * SHUFFLES
            real_c, shuf_c, shapes = collections.Counter(), collections.Counter(), collections.Counter()
            for v, items in versions[L]:
                b = transform(items, g, reading)
                lines.append('%s %s %s | %s' % (L, reading, v, ' '.join(b)))
                i, t = coverage(b)
                real_in, real_tot = real_in + i, real_tot + t
                real_c.update(counts(b))
                shapes[shape(b)] += 1
                ypos = [k for k, it in enumerate(items) if not transparent(it)]
                for s in range(SHUFFLES):
                    toks = [items[k] for k in ypos]
                    rng.shuffle(toks)
                    sh = list(items)
                    for k, tk in zip(ypos, toks):
                        sh[k] = tk
                    sb = transform(sh, g, reading)
                    shuf_in[s] += coverage(sb)[0]
                    shuf_c.update(counts(sb))
            mean = sum(shuf_in) / SHUFFLES
            ge = sum(1 for x in shuf_in if x >= real_in)
            report.append('TRANSCRIBER %s, reading %s: functions inside blocks %d of %d (%.1f%%); '
                          'shuffled mean %.1f (%.1f%%); shuffles at or above the real: %d of %d'
                          % (L, reading, real_in, real_tot, 100.0 * real_in / max(1, real_tot), mean,
                             100.0 * mean / max(1, real_tot), ge, SHUFFLES))
            for e in entries:
                for name in (e, e + '~'):
                    if real_c[name] or shuf_c[name] >= 0.5 * SHUFFLES / 100:
                        report.append('  %-22s real %3d   shuffled mean %6.2f'
                                      % (name, real_c[name], shuf_c[name] / SHUFFLES))
            if corpus in ('aesop', 'fables'):
                report.append('  the commonest shapes (blocks named, X and N left out):')
                for sh, c in shapes.most_common(15):
                    report.append('    %3d  %s' % (c, sh or '(nothing kept)'))
            report.append('')
            lines.append('')
    open(os.path.join(here, sname), 'w', encoding='utf-8').write('\n'.join(lines))
    open(os.path.join(here, pname), 'w', encoding='utf-8').write('\n'.join(report))
    print('\n'.join(report))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['test']:
        sys.exit(test())
    if a[:1] == ['run'] and len(a) == 3 and a[1] in ('tragedy', 'aesop', 'fables'):
        sys.exit(run(a[1], os.path.abspath(os.path.join(TS.CALLER, a[2]))))
    sys.exit(__doc__)
