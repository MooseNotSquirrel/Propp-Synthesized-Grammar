#!/usr/bin/env python3
"""
fableGrammar.py -- the fable grammar: write it, and measure it and v46 on a
set of transcribed fables.

  python fableGrammar.py write                 write FableEBNF01.txt from RANKS
  python fableGrammar.py measure AESOP_REPO BATCH...
        acceptance of FableEBNF01.txt and of v46 on the fables of the named
        batches, real against shuffled, by length band

THE FABLE GRAMMAR, drawn from the drawn Aesop sample's order (FableShapes.txt
in the Aesop repository, both transcribers): a fable is one or more
episodes; an episode runs through five ranks in order, each rank optional
and repeatable; after the first, an episode opens only on a lead or a want.
The first may also open on a scheme (η, ε, L) or a harm (A).

THE STREAMS are blockStream.py's: the whole fable, moves ignored, functions
marked Y only.

v46, READ AS FAVORABLY AS IT CAN BE: a fable passes if its stream splits
into consecutive stretches that v46 (+tragedy,reversal) accepts at `move`,
the first also at `tale`, so a preparatory section may lead it.

THE BASELINE: each fable's stream shuffled in place, 1000 times, seed 46.
"""
import collections
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import parse  # noqa: E402
import blockStream as BS  # noqa: E402

RANKS = [
    ('lead', ['α', 'up', 'β']),
    ('want', ['a', 'B']),
    ('scheme', ['ε', 'ζ', 'η', 'λ', 'θ', 'L', 'H', 'Pr', 'Rs', 'D', 'E', 'C', 'M', 'J', 'o', 'δ']),
    ('result', ['A', 'F', 'G', 'I', 'I-', 'K', 'N', 'down']),
    ('close', ['Ex', 'U', 'Q', 'W', 'T', 'γ']),
]
FIRST_ONLY = {'scheme': ['η', 'ε', 'L'], 'result': ['A']}
FILE = os.path.join(ROOT, 'FableEBNF01.txt')
SHUFFLES, SEED = 1000, 46
BANDS = (('2', 2, 2), ('3-4', 3, 4), ('5+', 5, 10 ** 6))


def alt(ts):
    return ' | '.join("'%s'" % t for t in ts)


def grammar_text():
    r = dict(RANKS)
    lines = [
        '# FableEBNF01.txt -- the fable grammar, written by fableGrammar.py; see its header.',
        '# A fable is one or more episodes. An episode opens on one lead or want, then',
        '# runs through three ranks in order, each optional and repeatable: scheme,',
        '# result, close. A second lead or want opens a new episode; the first episode',
        '# may also open on a scheme (η, ε, L) or a harm (A). Tokens are v46\'s.',
        '',
        'fable        = FirstEpisode {Episode}',
        'FirstEpisode = LeadOpen | WantOpen | SchemeOpen | HarmOpen',
        'Episode      = LeadOpen | WantOpen',
        'LeadOpen     = lead Scheme Result Close',
        'WantOpen     = want Scheme Result Close',
        'SchemeOpen   = schemeOpener Scheme Result Close',
        'HarmOpen     = harmOpener Result Close',
        'Scheme       = {scheme}',
        'Result       = {result}',
        'Close        = {close}',
    ]
    for name, ts in RANKS:
        lines.append('%-12s = %s' % (name, alt(ts)))
    lines.append('%-12s = %s' % ('schemeOpener', alt(FIRST_ONLY['scheme'])))
    lines.append('%-12s = %s' % ('harmOpener', alt(FIRST_ONLY['result'])))
    return '\n'.join(lines) + '\n'


class Parser:
    def __init__(self, text, start=None):
        if start:
            text = 'startHere = %s\n' % start + text
        self.bnf, self.start, self.table = parse.build(text)

    def ok(self, toks):
        return bool(toks) and parse.accept(toks, self.bnf, self.start, self.table)[0]


def v46():
    import runSteps
    text = open(runSteps.switched(BS.GRAMMAR, BS.EXTENSIONS, None), encoding='utf-8').read()
    return Parser(text, 'tale'), Parser(text, 'move')


def v46_ok(toks, tale, move, memo=None):
    """Some split of toks into stretches: the first accepted at tale or move,
    the rest at move."""
    n = len(toks)
    can = [False] * (n + 1)   # can[i]: toks[:i] splits well
    for j in range(1, n + 1):
        if tale.ok(toks[:j]) or move.ok(toks[:j]):
            can[j] = True
    for i in range(1, n):
        if not can[i]:
            continue
        for j in range(i + 1, n + 1):
            if not can[j] and move.ok(toks[i:j]):
                can[j] = True
    return can[n]


def streams(repo, batches):
    out = []
    for L in 'AB':
        for v, items in BS.load_aesop(repo, L, batches).items():
            out.append((L, v, [t for t in items if not BS.transparent(t)]))
    return out


def measure(repo, batches):
    fg = Parser(open(FILE, encoding='utf-8').read())
    tale, move = v46()
    rng = random.Random(SEED)
    rows = collections.defaultdict(lambda: [0, 0, 0.0, 0.0])   # (L, band) -> n, fable ok, fable shuffled, v46 ok, ...
    res = {}
    for L, v, toks in streams(repo, batches):
        n = len(toks)
        band = next((b for b, lo, hi in BANDS if lo <= n <= hi), None)
        if band is None:
            continue
        real_f, real_v = fg.ok(toks), v46_ok(toks, tale, move)
        sf = sv = 0
        for _ in range(SHUFFLES):
            s = list(toks)
            rng.shuffle(s)
            sf += fg.ok(s)
            sv += v46_ok(s, tale, move)
        for key in ((L, band), (L, 'all')):
            r = res.setdefault(key, [0, 0, 0, 0.0, 0.0])
            r[0] += 1
            r[1] += real_f
            r[2] += real_v
            r[3] += sf / SHUFFLES
            r[4] += sv / SHUFFLES
    print('fables of %d+ functions, whole stream; fable grammar and v46 (free move breaks)' % BANDS[0][1])
    print('%-3s %-5s %4s  %-26s  %-26s' % ('', 'band', 'n', 'fable: real / shuffled / gap', 'v46: real / shuffled / gap'))
    for L in 'AB':
        for band in [b for b, _, _ in BANDS] + ['all']:
            if (L, band) not in res:
                continue
            n, f, vv, sf, sv = res[(L, band)]
            print('%-3s %-5s %4d  %5.1f%% / %5.1f%% / %+5.1f     %5.1f%% / %5.1f%% / %+5.1f'
                  % (L, band, n, 100 * f / n, 100 * sf / n, 100 * (f - sf) / n,
                     100 * vv / n, 100 * sv / n, 100 * (vv - sv) / n))
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['write']:
        open(FILE, 'w', encoding='utf-8').write(grammar_text())
        Parser(grammar_text())
        print('wrote', FILE, 'LL(1): ok')
        sys.exit(0)
    if a[:1] == ['measure'] and len(a) >= 3:
        measure(os.path.abspath(os.path.join(BS.TS.CALLER, a[1])), tuple(a[2:]))
        sys.exit(0)
    sys.exit(__doc__)
