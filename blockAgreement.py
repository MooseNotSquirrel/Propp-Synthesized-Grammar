#!/usr/bin/env python3
"""
blockAgreement.py -- risk check 3 (Blocks/Agreement.txt): do the two
transcribers find the same blocks in the same story?

  python blockAgreement.py          writes Blocks/AgreementRun.txt

Uses blockStream.py's transform unchanged; a block agrees when the other
transcriber's version of the story has a block of the same entry, the
reversal mark ignored, over at least one of the same events.
"""
import collections
import glob
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402

SHUFFLES, SEED = 200, 46
PARENT = os.path.dirname(ROOT)


def read(paths):
    """{version: (items, events)}: the stream and the event behind each item."""
    out = collections.OrderedDict()
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PF]\d{2}', f[0]):
                continue
            m = re.search(r'\d+', f[3])
            ev = int(m.group()) if m else None
            keys = BS.TS.key(f[4], extended=True)
            y = f[7].upper().startswith('Y')
            items, evs = out.setdefault(f[0], ([], []))
            for k in (keys or ['X']):
                items.append(k if (y and keys) else '(%s)' % k)
                evs.append(ev)
    return out


def blocks(items, evs, g, reading):
    """[(entry, frozenset of events)] for the blocks of one version."""
    out, k = [], 0
    for b in BS.transform(items, g, reading):
        n = len(BS.reverse([b]))
        if '[' in b:
            out.append((b.split('[', 1)[0].rstrip('~'), frozenset(e for e in evs[k:k + n] if e is not None)))
        k += n
    return out


def match(v, other):
    if v in other:
        return v
    if v.endswith('/1') and v[:-2] in other:
        return v[:-2]
    if v + '/1' in other:
        return v + '/1'
    return None


def agreement(ba, bb):
    """Dice share of blocks that find a partner of the same entry over shared events."""
    def hits(xs, ys):
        return sum(1 for e, s in xs if any(e == f and s & t for f, t in ys))
    tot = len(ba) + len(bb)
    return (hits(ba, bb) + hits(bb, ba)) / tot if tot else 0.0, hits(ba, bb), hits(bb, ba), tot


def corpora():
    for name, repo in (('training fables', 'Aesop'), ('held-out fables', 'Fables')):
        yield name, [read(sorted(glob.glob(os.path.join(PARENT, repo, 'transcriptions', L, 'b[1-4]', 'Notes.txt'))))
                     for L in 'AB']
    trag = os.path.join(PARENT, 'Tragedy', 'transcriptions')
    yield 'tragedy P01-P04', [read([os.path.join(trag, L, p, 'Notes.txt') for p in BS.OPEN]) for L in 'AB']


def main():
    g = BS.Grammar()
    rep = ['# AgreementRun.txt -- blockAgreement.py, risk check 3 (Blocks/Agreement.txt).',
           '# Share of all blocks, A\'s and B\'s, that the other transcriber also has in the same story:',
           '# real; mean with B\'s functions shuffled; shuffles at or above the real; the verdict.', '']
    for name, (A, B) in corpora():
        pairs = [(v, match(v, B)) for v in A if match(v, B)]
        for reading in ('blocks', 'strict'):
            rng = random.Random(SEED)
            real_blocks = [(blocks(*A[a], g, reading), blocks(*B[b], g, reading)) for a, b in pairs]
            agree = sum(agreement(x, y)[1] + agreement(x, y)[2] for x, y in real_blocks)
            total = sum(len(x) + len(y) for x, y in real_blocks)
            per = collections.defaultdict(lambda: [0, 0])
            for x, y in real_blocks:
                for side, other in ((x, y), (y, x)):
                    for e, s in side:
                        per[e][1] += 1
                        per[e][0] += any(e == f and s & t for f, t in other)
            shuf = []
            for _ in range(SHUFFLES):
                ag = tot = 0
                for (a, b), (xa, _) in zip(pairs, real_blocks):
                    items, evs = B[b]
                    yp = [k for k, it in enumerate(items) if not BS.transparent(it)]
                    order = list(yp)
                    rng.shuffle(order)
                    it2, ev2 = list(items), list(evs)
                    for k, j in zip(yp, order):
                        it2[k], ev2[k] = items[j], evs[j]
                    yb = blocks(it2, ev2, g, reading)
                    r = agreement(xa, yb)
                    ag, tot = ag + r[1] + r[2], tot + r[3]
                shuf.append(ag / tot if tot else 0.0)
            realv = agree / total if total else 0.0
            mean = sum(shuf) / SHUFFLES
            ge = sum(1 for x in shuf if x >= realv)
            verdict = 'AGREE BEYOND CHANCE' if realv > mean and ge <= 10 else 'DO NOT'
            rep.append('%-16s %-6s %4d versions  %4d blocks  agreement %5.1f%%  shuffled %5.1f%%  at/above %3d of %d  %s'
                       % (name, reading, len(pairs), total, 100 * realv, 100 * mean, ge, SHUFFLES, verdict))
            for e, (h, n) in sorted(per.items(), key=lambda x: -x[1][1]):
                if n >= 5:
                    rep.append('      %-22s %3d of %3d agree (%.0f%%)' % (e, h, n, 100.0 * h / n))
        rep.append('')
    open(os.path.join(ROOT, 'Blocks', 'AgreementRun.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
