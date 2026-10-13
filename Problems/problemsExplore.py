#!/usr/bin/env python3
"""
problemsExplore.py -- exploratory, the development half of a genre comparison of
problem structure: the measures, per genre and describer, on the 75 stories the
significance test described. Their figures are seen; the test of any prediction
drawn from them is on stories not yet described.

  python problemsExplore.py    writes Problems/ProblemsExplore.txt

Per problem (a story's label with at least one act placed in it): whether it is
repaired, punished, rewarded, or left open (none of the three); whether the act
that opens it is the hero's own (the hero does it); whether that act harms the
hero. Per story: problems, whether its last-opened problem is repaired, and the
share of its acts helping and harming the hero.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Significance'))
import significance as S  # noqa: E402

T = S.T
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def stories(L):
    """{story: [entry dicts in order]}"""
    out = collections.defaultdict(list)
    for (s, ev), xs in sorted(S.described(L).items(), key=lambda kv: (kv[0][0], kv[0][1])):
        for x in xs:
            out[s].append(x)
    for s in out:
        out[s].sort(key=lambda x: x['id'])
    return out


def main():
    M = T.material()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    say('# ProblemsExplore.txt -- problemsExplore.py, exploratory; the development stories of a genre comparison.')
    say('')
    head = ('genre', 'L', 'stories', 'probs/story', 'repaired', 'punished', 'rewarded', 'open', 'hero opens', 'opener harms',
            'last repaired', 'acts help', 'acts harm', 'acts none')
    say('%-8s %s %7s %11s %8s %8s %8s %6s %10s %12s %13s %9s %9s %9s' % head)
    for g in T.GENRES:
        for L in 'AB':
            st = {s: xs for s, xs in stories(L).items() if gen.get(s) == g}
            probs = collections.OrderedDict()
            last_rep = 0
            acts = collections.Counter()
            for s, xs in st.items():
                order = []
                for x in xs:
                    acts['all'] += 1
                    acts[x['value']] += 1
                    acts['none'] += x['place'] == 'none'
                    if x['place'] == 'none' or x['problem'] in ('-', ''):
                        continue
                    k = (s, x['problem'])
                    p = probs.setdefault(k, {'places': set(), 'opener': None})
                    p['places'].add(x['place'])
                    if x['place'] == 'opens' and p['opener'] is None:
                        p['opener'] = x
                        order.append(k)
                if order:
                    last_rep += 'repairs' in probs[order[-1]]['places']
            n = len(probs)
            ns = len(st)
            ops = [p['opener'] for p in probs.values() if p['opener']]
            say('%-8s %s %7d %11.1f %7.0f%% %7.0f%% %7.0f%% %5.0f%% %9.0f%% %11.0f%% %12.0f%% %8.0f%% %8.0f%% %8.0f%%' % (
                g, L, ns, n / float(ns),
                100.0 * sum('repairs' in p['places'] for p in probs.values()) / n,
                100.0 * sum('punishes' in p['places'] for p in probs.values()) / n,
                100.0 * sum('rewards' in p['places'] for p in probs.values()) / n,
                100.0 * sum(not p['places'] & {'repairs', 'punishes', 'rewards'} for p in probs.values()) / n,
                100.0 * sum(o['part'] in ('does', 'both') for o in ops) / max(1, len(ops)),
                100.0 * sum(o['value'] == 'harms' for o in ops) / max(1, len(ops)),
                100.0 * last_rep / ns,
                100.0 * acts['helps'] / acts['all'], 100.0 * acts['harms'] / acts['all'], 100.0 * acts['none'] / acts['all']))
    open(os.path.join(HERE, 'ProblemsExplore.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
