#!/usr/bin/env python3
"""
positionNull.py -- risk check 2 (Blocks/PositionNull.txt): block coverage
against the plain shuffle and against the positional null.

  python positionNull.py          writes Blocks/PositionNullRun.txt

Uses blockStream.py's transform unchanged. The positional null: each Y
function draws a sort key from the relative positions the same function
takes in the other stories of the same corpus and transcriber (its own story
left out), and the functions are sorted by key into the Y positions.
"""
import collections
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

SHUFFLES, SEED = 200, 46
PARENT = os.path.dirname(ROOT)


def story(v):
    return v.split('/', 1)[0]


def corpora():
    yield 'training fables', {L: list(BS.load_aesop(os.path.join(PARENT, 'Aesop'), L).items()) for L in 'AB'}
    yield 'held-out fables', {L: list(BS.load_aesop(os.path.join(PARENT, 'Fables'), L).items()) for L in 'AB'}
    trag = os.path.join(PARENT, 'Tragedy')
    yield 'tragedy P01-P04', {L: [(v, it) for p in BS.OPEN for v, it in BS.load(trag, L, p).items()] for L in 'AB'}


def positions(versions):
    """{story: {function: [relative positions]}} for each story's own functions."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for v, items in versions:
        ys = [t for t in items if not BS.transparent(t)]
        for i, t in enumerate(ys):
            out[story(v)][t].append((i + 0.5) / len(ys))
    return out


def main():
    g = BS.Grammar()
    rep = ['# PositionNullRun.txt -- positionNull.py, risk check 2 (Blocks/PositionNull.txt).',
           '# Share of Y functions inside blocks: real, plain shuffle mean, positional null mean;',
           '# the count of positional-null shuffles at or above the real; the verdict by the frozen rule.', '']
    for name, vers in corpora():
        for L in 'AB':
            pos = positions(vers[L])
            for reading in ('blocks', 'strict'):
                rng = random.Random(SEED)
                real = tot = 0
                plain = [0] * SHUFFLES
                posn = [0] * SHUFFLES
                for v, items in vers[L]:
                    b = BS.transform(items, g, reading)
                    i, t = BS.coverage(b)
                    real, tot = real + i, tot + t
                    ypos = [k for k, it in enumerate(items) if not BS.transparent(it)]
                    toks = [items[k] for k in ypos]
                    pool = collections.defaultdict(list)
                    for s, d in pos.items():
                        if s != story(v):
                            for f, ps in d.items():
                                pool[f].extend(ps)
                    for s in range(SHUFFLES):
                        a = list(toks)
                        rng.shuffle(a)
                        sh = list(items)
                        for k, tk in zip(ypos, a):
                            sh[k] = tk
                        plain[s] += BS.coverage(BS.transform(sh, g, reading))[0]
                        keyed = sorted(toks, key=lambda f: (rng.choice(pool[f]) if pool[f] else rng.random(), rng.random()))
                        sh = list(items)
                        for k, tk in zip(ypos, keyed):
                            sh[k] = tk
                        posn[s] += BS.coverage(BS.transform(sh, g, reading))[0]
                pm, qm = sum(plain) / SHUFFLES, sum(posn) / SHUFFLES
                ge = sum(1 for x in posn if x >= real)
                verdict = 'GONE' if real <= qm else ('SURVIVES' if ge <= 10 else 'WEAKENED')
                rep.append('%-16s %s %-6s real %5.1f%%  plain %5.1f%%  positional %5.1f%%  at/above %3d of %d  %s'
                           % (name, L, reading, 100.0 * real / tot, 100.0 * pm / tot, 100.0 * qm / tot, ge, SHUFFLES, verdict))
        rep.append('')
    open(os.path.join(ROOT, 'Blocks', 'PositionNullRun.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
