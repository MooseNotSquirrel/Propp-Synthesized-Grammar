#!/usr/bin/env python3
"""
fableShapes.py -- EXPLORATORY, after the Aesop test: what order do the
fables follow, if not Propp's? It revises no verdict.

  python fableShapes.py AESOP_REPO

On the primary reading (function entries marked Y), for each transcriber:
the mean relative position of each function within its fable (0 first, 1
last) and the order this gives, set against Propp's numbering by rank
correlation; what opens and what closes a fable; the transitions from one
function to the next that occur more often than chance (observed against
expected from the functions' frequencies); the most common whole shapes,
with repeats collapsed; and, for the tragedy extensions, how often a fight
is lost by the hero (I-) and how often the hero undergoes punishment,
recognition or exposure after a liquidation or wedding.
"""
import collections
import sys

import aesopScore as S


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx) ** .5
    vy = sum((b - my) ** 2 for b in ry) ** .5
    return cov / (vx * vy)


def main(repo):
    fv = S.fables(repo)
    for L in 'AB':
        ents = S.load(repo, L)
        seqs = [(S.sequence(ents.get(vid, []), 'primary'), w) for vid, fid, hero, w, n in fv]
        pos, cnt = collections.defaultdict(float), collections.Counter()
        first, last = collections.Counter(), collections.Counter()
        big, uni = collections.Counter(), collections.Counter()
        shapes = collections.Counter()
        for s, w in seqs:
            if not s:
                first['(none)'] += w
                continue
            for i, k in enumerate(s):
                p = i / (len(s) - 1) if len(s) > 1 else 0.5
                pos[k] += w * p
                cnt[k] += w
            first[s[0]] += w
            last[s[-1]] += w
            for a, b in zip(s, s[1:]):
                big[(a, b)] += w
            for k in s:
                uni[k] += w
            c = [s[0]] + [b for a, b in zip(s, s[1:]) if b != a]
            shapes[' '.join(c)] += w
        print('TRANSCRIBER %s' % L)
        keys = [k for k in cnt if cnt[k] >= 5]
        mean = {k: pos[k] / cnt[k] for k in keys}
        order = sorted(keys, key=lambda k: mean[k])
        print('  the fables\' own order (functions occurring 5+ times, by mean position):')
        print('    ' + '  '.join('%s %.2f' % (k, mean[k]) for k in order))
        rho = spearman([mean[k] for k in keys], [S.NUM[k] for k in keys])
        print('  rank correlation with Propp\'s numbering: %.2f' % rho)
        tot = sum(first.values())
        print('  opens with: ' + ', '.join('%s %.0f%%' % (k, 100 * v / tot) for k, v in first.most_common(6)))
        tot = sum(last.values())
        print('  closes with: ' + ', '.join('%s %.0f%%' % (k, 100 * v / tot) for k, v in last.most_common(6)))
        nb = sum(big.values())
        nu = sum(uni.values())
        lifts = []
        for (a, b), v in big.items():
            exp = nb * (uni[a] / nu) * (uni[b] / nu)
            if v >= 4:
                lifts.append((v / exp, v, a, b))
        lifts.sort(reverse=True)
        print('  transitions more common than chance (4+ cases): ' + ', '.join(
            '%s->%s x%.0f (%.1f times chance)' % (a, b, v, l) for l, v, a, b in lifts[:12]))
        print('  commonest shapes: ' + '; '.join('%s (%.0f)' % (k, v) for k, v in shapes.most_common(12)))
        lost = rv = 0
        for vid, fid, hero, w, n in fv:
            es = ents.get(vid, [])
            lost += sum(1 for e in es if S.kept(e, 'primary') and S.base(e['sym']) == 'I' and S.negative(e['sym']))
            rv += sum(1 for k in S.moves(es, 'primary', hero, True) if 'Rv' in k)
        print('  tragedy extensions: hero loses a fight (I-) %d times; hero punished, recognized or exposed after a liquidation or wedding in %d moves' % (lost, rv))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main(S.os.path.join(S.CALLER, sys.argv[1])))
