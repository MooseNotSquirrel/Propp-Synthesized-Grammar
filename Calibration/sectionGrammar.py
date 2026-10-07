#!/usr/bin/env python3
"""
sectionGrammar.py -- Propp's large sections and their order.

  python sectionGrammar.py explore   the exploration of 2026-10-06, over all 45 tales
                                     (writes SectionOrderExplore.txt); not frozen
  python sectionGrammar.py fit       the scored section grammar, fitted on the 22
                                     development tales (writes SectionGrammar01.txt)
  python sectionGrammar.py test      the frozen test of SectionGrammar.md, on the 23
                                     test tales (writes SectionGrammarRun.txt)

THE SECTIONS, Propp's large divisions of a move, in his order:
  1 complication A a B C ↑   2 donor D E F   3 transfer G   4 struggle H J I
  5 liquidation K   6 return ↓ Pr Rs   7 arrival and claims o L   8 task M N
  9 endgame Q Ex T U W
The preparatory functions are left out, as Propp's schemes print none.
A move's section string is its functions, marked Y, in the order of the
notes, each replaced by its section; the transcriber's own moves.
"""
import collections
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'Benchmark'))
import compare as C  # noqa: E402
import embedCorpus as E  # noqa: E402

import numpy as np  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'Afanasyev')
NAMES = ['complication', 'donor', 'transfer', 'struggle', 'liquidation', 'return',
         'arrival and claims', 'task', 'endgame']
GROUPS = [['A', 'a', 'B', 'C', 'up'], ['D', 'E', 'F'], ['G'], ['H', 'J', 'I'], ['K'],
          ['down', 'Pr', 'Rs'], ['o', 'L'], ['M', 'N'], ['Q', 'Ex', 'T', 'U', 'W']]
SEC = {k: i for i, ks in enumerate(GROUPS, 1) for k in ks}
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(HERE, 'Split.txt'), encoding='utf-8') if '|' in l}
MODEL = os.path.join(HERE, 'SectionGrammar01.txt')
SHUFFLES, SEED = 1000, 46


def moves(es):
    """the transcriber's moves, each a list of function keys marked Y, in the order of the notes."""
    mv = collections.OrderedDict()
    for x in sorted(es, key=lambda x: x['line']):
        if C.TS.kept(x, 'primary'):
            mv.setdefault(x['move'], []).extend(k for k in C.TS.key(x['sym']) if k in C.VOCAB)
    return list(mv.values())


def sections(keys):
    return [SEC[k] for k in keys if k in SEC]


def propp_moves():
    """Propp's moves: each move's own functions, braces flattened in printed order, embedded moves left out."""
    out = []
    for tale, top, elems, strings, part, tail in E.derive():
        for lab, el in elems.items():
            s = []
            for e in el:
                if isinstance(e, tuple):
                    continue
                if isinstance(e, list):
                    s += [k for row in e for k in row if isinstance(k, str)]
                else:
                    s.append(e)
            out.append([k for k in s if k in C.VOCAB])
    return out


def backward(seqs, drop=()):
    b = p = 0
    inv = collections.Counter()
    for s in seqs:
        sec = [x for x in sections(s) if x not in drop]
        for i in range(len(sec)):
            for j in range(i + 1, len(sec)):
                if sec[i] != sec[j]:
                    p += 1
                    if sec[i] > sec[j]:
                        b += 1
                        inv[(sec[j], sec[i])] += 1
    return (b / p if p else 0.0), p, inv


def explore():
    rng = random.Random(SEED)
    rows = [('Propp, Appendix III, his moves', propp_moves())]
    for L in 'AB':
        e = C.load(REPO, 'U', L)
        rows.append(('machine U/%s, its own moves' % L, [m for t in sorted(e) for m in moves(e[t])]))
    import benchmark as Bm
    rows.append(('the owner, five tales', [Bm.owner(t)[0] for t in Bm.TALES]))
    out = ['# SectionOrderExplore.txt -- sectionGrammar.py explore: an exploration, not frozen.',
           '# Share of pairs of functions in different sections that run against Propp\'s section order.', '']
    for name, seqs in rows:
        b, n, inv = backward(seqs)
        sh = sum(backward([rng.sample(s, len(s)) for s in seqs])[0] for _ in range(200)) / 200
        out.append('%-34s %5.1f%% of %5d pairs backward; shuffled %5.1f%%; without the donor %5.1f%%'
                   % (name, 100 * b, n, 100 * sh, 100 * backward(seqs, (2,))[0]))
        out.append('    most often reversed: ' + ', '.join('%s before %s %d' % (NAMES[j - 1], NAMES[i - 1], c)
                                                       for (i, j), c in inv.most_common(4)))
    open(os.path.join(HERE, 'SectionOrderExplore.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


def corpus(part, arm, L):
    e = C.load(REPO, arm, L)
    return [m for t in SPLIT[part] for m in moves(e.get(t, []))]


def fit():
    pos = collections.defaultdict(list)
    for L in 'AB':
        for m in corpus('dev', 'U', L):
            sec = sections(m)
            for i, x in enumerate(sec):
                pos[x].append(i / float(len(sec) - 1) if len(sec) > 1 else 0.5)
    rows = sorted((sum(v) / len(v), k, len(v)) for k, v in pos.items())
    with open(MODEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# SectionGrammar01.txt -- the scored section grammar, sectionGrammar.py fit, from the 22\n'
                '# development tales, arm U, both transcribers. rank | section | number | occurrences\n')
        for r, k, n in rows:
            f.write('%.3f | %s | %d | %d\n' % (r, NAMES[k - 1], k, n))
    print(open(MODEL, encoding='utf-8').read())


def load_model():
    return {int(l.split('|')[2]): float(l.split('|')[0]) for l in open(MODEL, encoding='utf-8')
            if not l.startswith('#') and l.strip()}


def counts(R):
    """(concordant, pairs) for one rank array."""
    a, b = R[:, None], R[None, :]
    n = len(R)
    up = np.triu(np.ones((n, n), bool), 1)
    valid = up & (a != b)
    return int((valid & (a < b)).sum()), int(valid.sum())


def test():
    fitted = load_model()
    out = ['# SectionGrammarRun.txt -- sectionGrammar.py test, as SectionGrammar.md freezes it.', '']
    fitted_order = sorted(fitted, key=fitted.get)
    out.append('Fitted order: ' + ' < '.join(NAMES[k - 1] for k in fitted_order))
    out.append('Propp\'s order: ' + ' < '.join(NAMES))
    out.append('')
    verdicts = {}
    for arm in ('U', 'C'):
        for L in 'AB':
            ms = [sections(m) for m in corpus('test', arm, L)]
            ms = [m for m in ms if len(set(m)) >= 2]
            rng = np.random.default_rng(SEED)
            tot = {}
            d = []
            for key, rank in (('fitted', fitted), ('Propp', {k: k for k in range(1, 10)})):
                c = p = 0
                sc = np.zeros(SHUFFLES)
                sp = np.zeros(SHUFFLES)
                per = []
                for m in ms:
                    R = np.array([rank[x] for x in m], float)
                    cc, pp = counts(R)
                    c, p = c + cc, p + pp
                    per.append((cc, pp))
                tot[key] = (c, p, per)
            rng = np.random.default_rng(SEED)
            gaps = {}
            for key, rank in (('fitted', fitted), ('Propp', {k: k for k in range(1, 10)})):
                c, p, per = tot[key]
                sh = []
                for _ in range(SHUFFLES):
                    cs = ps = 0
                    for m in ms:
                        R = np.array([rank[x] for x in rng.permutation(m)], float)
                        cc, pp = counts(R)
                        cs, ps = cs + cc, ps + pp
                    sh.append(cs / ps)
                gaps[key] = (c / p, float(np.mean(sh)), c / p - float(np.mean(sh)))
            diffs = [f[0] - q[0] for f, q in zip(tot['fitted'][2], tot['Propp'][2])]
            pairs_total = tot['Propp'][1]
            obs = sum(diffs) / pairs_total
            r2 = random.Random(SEED)
            hits = sum(1 for _ in range(10000)
                       if abs(sum(x if r2.random() < 0.5 else -x for x in diffs) / pairs_total) >= abs(obs) - 1e-12)
            p_val = (hits + 1) / 10001.0
            delta = gaps['fitted'][2] - gaps['Propp'][2]
            if arm == 'U':
                verdicts[L] = (delta, p_val)
            out.append('ARM %s, TRANSCRIBER %s: %d moves of two or more sections' % (arm, L, len(ms)))
            for key in ('fitted', 'Propp'):
                out.append('  %-7s concordance %.3f, shuffled %.3f, gap %+.3f' % ((key,) + gaps[key]))
            out.append('  fitted minus Propp: %+.3f; paired sign-flip over moves, two-sided p %.4f%s'
                       % (delta, p_val, '' if arm == 'U' else ' (reported, not judged)'))
            out.append('')
    better = all(v[0] >= 0.02 and v[1] <= 0.05 for v in verdicts.values())
    worse = all(v[0] <= -0.02 and v[1] <= 0.05 for v in verdicts.values())
    out.append('VERDICT (arm U, both transcribers): %s' % (
        'THE FITTED ORDER IS BETTER' if better else 'PROPP\'S ORDER IS BETTER' if worse else
        'PROPP\'S ORDER SUFFICES: the fitted order does not do better'))
    open(os.path.join(HERE, 'SectionGrammarRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['explore']:
        explore()
    elif a == ['fit']:
        fit()
    elif a == ['test']:
        test()
    else:
        sys.exit(__doc__)
