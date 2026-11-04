"""rung2.py <version> -- rung 2 of GeneralGrammarProtocol.md: Propp's own 45 strings under the tool, with G8's bars (the owner, 2026-11-04).
grammar.py sees the strings without their moves; his moves and order are used only here, to score."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Induction'))
import grammar as G  # noqa: E402
import generators as X  # noqa: E402
import score as C  # noqa: E402
import audit as U  # noqa: E402

BARS = {'relation tau': 0.993, 'order tau': 0.971, 'pair recall': 0.541, 'pass F': 0.835}


def run(version):
    out = ['# Rung2-%s.txt -- Propp\'s own strings, the tool unchanged, the bars G8\'s' % version]
    slots, pairs = C.propp()
    num = C.numbering(slots)
    items = U.propp_items()
    stories = [X.flat(i[2]) for i in items]
    cuts = [X.cuts_of(i[2]) for i in items]
    moves = [m for i in items for m in i[2]]
    f = G.fit(stories)
    rt, rn = C.relation_tau(f['relations'], num)
    ot = C.order_tau(f['order'], num)
    rec, k, n = C.pair_recall(f, pairs, stories)
    F = C.boundary_f(f['cuts'], cuts)
    acc = C.acceptance(f, moves, np.random.default_rng(1))
    out.append('stories %d, moves %d, symbols modelled %d, units per story %.1f' % (len(stories), len(moves), f['symbols'], np.mean([len(s) for s in stories])))
    out.append('SHAPE: %s (ordered: %s); coverage %.2f; order method d=%s; (beta, window) %s; steps %s' % (f['shape'], f['ordered'], f['coverage'], f['method'], f['beta_window'], {a: round(b, 4) for a, b in f['steps'].items()}))
    base = f['cv']['unigram']
    out.append('held-out gain over the unigram, nats per story: ' + ', '.join('%s %.2f' % (a, (b - base) / len(stories)) for a, b in f['cv'].items()))
    vals = {'relation tau': rt, 'order tau': ot, 'pair recall': rec, 'pass F': F}
    for a in BARS:
        out.append('%-13s %.3f against the bar %.3f: %s' % (a, vals[a], BARS[a], 'HOLDS' if vals[a] >= BARS[a] else 'FAILS'))
    out.append('relations scored %d; pairs found %d of %d' % (rn, k, n))
    out.append('acceptance %d of %d moves break no relation; shuffled %.3f (not comparable to V46\'s 80 of 84, Versions.md)' % acc)
    out.append('order: ' + ' '.join(f['order']))
    out.append('level 2: ' + '; '.join('%s %s %s' % (o[0], o[1], o[2]) for o in f['ops']))
    out.append('links: ' + ' '.join('%s-%s' % tuple(x) for x in f['links']))
    out.append('branches: ' + ' '.join('%s/%s' % (b[0], b[1]) for b in f['branches']))
    sp = U.ST.read_split()[('functions', 'tale')]
    ind = [X.flat(i[2]) for i in items if i[0] in sp['induction']]
    g = G.fit(ind)
    chk = [m for i in items if i[0] in sp['checking'] for m in i[2]]
    out.append('## beside it, fitted on the induction half (%d stories): shape %s, order tau %.3f, relation tau %.3f; checking half: %d of %d moves accepted, shuffled %.3f'
               % (len(ind), g['shape'], C.order_tau(g['order'], num), C.relation_tau(g['relations'], num)[0], *C.acceptance(g, chk, np.random.default_rng(2))))
    open(os.path.join(HERE, 'Rung2-%s.txt' % version), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    run(sys.argv[1])
