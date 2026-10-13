#!/usr/bin/env python3
"""
diagnose.py -- after the verdict: why the significance mapping does not recover
Propp's functions. Reported, not judged; written after SignificanceRun.txt was read.

  python diagnose.py     writes Significance/Diagnostics.txt

1. Whether the verdict depends on P18, which describer B-s6 wrote without reading the play's text.
2. Whether an event carries a function at all: derived against original, and A against B.
3. Precision and recall of the derived functions, two layers and three.
4. The functions the significance mapping adds most often where the original has none, and misses most often.
"""
import collections
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import significance as S  # noqa: E402

T, W, BL = S.T, S.W, S.BL
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def main():
    M = T.material()
    J = W.judged()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    funcs, D = {}, {}
    for L in 'AB':
        o = {}
        for g in T.GENRES:
            o.update({e: v for e, v in T.read_functions(glob.glob(os.path.join(S.P, BL.ORIG[g] % L))).items() if e[0] in gen})
        funcs[L] = o
        D[L] = S.described(L)
    events = sorted(e for e in set(funcs['A']) & set(funcs['B']) & set(D['A']) & set(D['B']) if e[0] in J)
    d2 = {L: {e: set().union(*[{S.derive2(x['act'], x['part'])} - {None} for x in D[L][e]]) for e in events} for L in 'AB'}
    d3 = {L: {e: set().union(*[S.derive3(x['act'], x['part'], x['value'], x['place'], x['after']) for x in D[L][e]]) for e in events}
          for L in 'AB'}
    say('# Diagnostics.txt -- diagnose.py, after the verdict; reported, not judged.')
    say('')
    E = [e for e in events if e[0] != 'P18']
    jab = T.jaccard(funcs['A'], funcs['B'], E)
    r2 = [T.jaccard(d2[L], funcs[L], E) for L in 'AB']
    r3 = [T.jaccard(d3[L], funcs[L], E) for L in 'AB']
    say('1. WITHOUT P18 (%d events): original A against B %.3f; two layers mean %.3f; three layers mean %.3f; gap closed %.0f%%'
        % (len(E), jab, sum(r2) / 2, sum(r3) / 2, 100 * (sum(r3) - sum(r2)) / 2 / (jab - sum(r2) / 2)))
    say('')
    say('2. WHETHER AN EVENT CARRIES A FUNCTION AT ALL (events with at least one; agreement = both / either)')
    fa = {e for e in events if funcs['A'][e]}
    fb = {e for e in events if funcs['B'][e]}
    say('  original A %d, original B %d; A against B %.3f' % (len(fa), len(fb), len(fa & fb) / float(len(fa | fb))))
    for L in 'AB':
        o = {e for e in events if funcs[L][e]}
        for name, d in (('two layers', d2), ('three layers', d3)):
            x = {e for e in events if d[L][e]}
            say('  %s %-12s derived %4d; against original %s %.3f' % (L, name, len(x), L, len(x & o) / float(len(x | o))))
    say('')
    say('3. PRECISION AND RECALL of the derived functions against the same letter\'s original, summed over events')
    for L in 'AB':
        for name, d in (('two layers', d2), ('three layers', d3)):
            hit = sum(len(d[L][e] & funcs[L][e]) for e in events)
            pred = sum(len(d[L][e]) for e in events)
            true = sum(len(funcs[L][e]) for e in events)
            say('  %s %-12s predicted %4d, original %4d, both %4d: precision %.2f, recall %.2f' % (L, name, pred, true, hit, hit / float(pred), hit / float(true)))
    say('')
    say('4. THE SIGNIFICANCE MAPPING\'S ERRORS, both describers together')
    add, miss = collections.Counter(), collections.Counter()
    for L in 'AB':
        for e in events:
            add.update(d3[L][e] - funcs[L][e])
            miss.update(funcs[L][e] - d3[L][e])
    say('  added where the original has not: ' + ', '.join('%s %d' % kv for kv in add.most_common(12)))
    say('  missed where the original has:    ' + ', '.join('%s %d' % kv for kv in miss.most_common(12)))
    # what the describers made of the acts behind the most missed functions
    say('')
    say('5. THE MOST MISSED FUNCTIONS: the acts and places the describers gave in those events, both describers together')
    for f, _ in miss.most_common(5):
        c = collections.Counter()
        for L in 'AB':
            for e in events:
                if f in funcs[L][e] and f not in d3[L][e]:
                    for x in D[L][e]:
                        c['%s/%s/%s' % (x['act'], x['part'], x['place'])] += 1
        say('  %s: %s' % (f, ', '.join('%s %d' % kv for kv in c.most_common(6))))
    open(os.path.join(HERE, 'Diagnostics.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
