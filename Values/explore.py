#!/usr/bin/env python3
"""
explore.py -- a first look at the owner's principle that structure does not dictate content:
the same device, used across genres, with different values attached. Exploratory, not a frozen
test; it reads the significance layer already scored (Significance/, Problems/).

  python explore.py    writes Values/ValuesExplore.txt

For each act common enough in every genre: whom it helps or harms, whether the hero does it,
and what place it takes in a problem; per genre, both describers apart. Then the acts whose
values differ most between genres, and two cases the owner named: harm used to set things right,
and deception by the hero.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Problems'))
import problems as Pm  # noqa: E402

S, T = Pm.S, Pm.T
GENRES = ('tale', 'fable', 'tragedy')
MIN = 15
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def entries():
    """{L: {genre: [entry dicts]}}: the 75 development stories and the 79 test stories"""
    gen = {s: g for g, bs in T.material().items() for b in bs.values() for s in b}
    gen.update(Pm.genre_of())
    out = {L: {g: [] for g in GENRES} for L in 'AB'}
    test = Pm.described()
    for L in 'AB':
        for (s, ev), xs in S.described(L).items():
            out[L][gen[s]] += xs
        for s, xs in test[L].items():
            out[L][gen[s]] += xs
    return out


def dist(xs, key, cats):
    c = collections.Counter(x[key] for x in xs)
    n = float(len(xs)) or 1.0
    return {k: c[k] / n for k in cats}


def tv(p, q):
    return 0.5 * sum(abs(p[k] - q[k]) for k in p)


def main():
    E = entries()
    say('# ValuesExplore.txt -- explore.py, exploratory; the significance layer of 154 stories, read for the values each device carries.')
    say('')
    for L in 'AB':
        say('describer %s: acts per genre %s' % (L, ', '.join('%s %d' % (g, len(E[L][g])) for g in GENRES)))
    say('')
    acts = sorted({x['act'] for L in 'AB' for g in GENRES for x in E[L][g]})
    rows = []
    for a in acts:
        ok = all(sum(1 for x in E[L][g] if x['act'] == a) >= MIN for L in 'AB' for g in GENRES)
        if not ok:
            continue
        spread = []
        for L in 'AB':
            d = {g: dist([x for x in E[L][g] if x['act'] == a], 'value', S.VALUES) for g in GENRES}
            spread.append(max(tv(d[g], d[h]) for g in GENRES for h in GENRES))
        rows.append((min(spread), a))
    say('THE DEVICES WHOSE VALUE FOR THE HERO DIFFERS MOST BETWEEN GENRES (each in every genre at least %d times for both describers;'
        ' the spread is the largest gap between two genres in the shares of helps, harms and neither, the smaller of the two describers)' % MIN)
    for sp, a in sorted(rows, reverse=True):
        cells = []
        for g in GENRES:
            ab = []
            for L in 'AB':
                xs = [x for x in E[L][g] if x['act'] == a]
                v = dist(xs, 'value', S.VALUES)
                hd = sum(1 for x in xs if x['part'] in ('does', 'both')) / float(len(xs))
                ab.append('helps %2.0f harms %2.0f, hero does %2.0f' % (100 * v['helps'], 100 * v['harms'], 100 * hd))
            cells.append('%s [%s | %s]' % (g, ab[0], ab[1]))
        say('  %-19s spread %.2f   %s' % (a, sp, '   '.join(cells)))
    say('')
    say('HARM USED TO SET THINGS RIGHT: of all harms, the share placed as repairing a problem or punishing for one, and of those, the share the hero does')
    for g in GENRES:
        cells = []
        for L in 'AB':
            hs = [x for x in E[L][g] if x['act'] == 'harm']
            right = [x for x in hs if x['place'] in ('repairs', 'punishes')]
            cells.append('%s %d harms, %2.0f%% set things right, the hero doing %2.0f%% of those'
                         % (L, len(hs), 100.0 * len(right) / max(1, len(hs)), 100.0 * sum(1 for x in right if x['part'] in ('does', 'both')) / max(1, len(right))))
        say('  %-8s %s' % (g, '; '.join(cells)))
    say('')
    say('DECEPTION: the share of deceptions the hero performs, and of those, the share that help the hero')
    for g in GENRES:
        cells = []
        for L in 'AB':
            ds = [x for x in E[L][g] if x['act'] == 'deceive']
            hd = [x for x in ds if x['part'] in ('does', 'both')]
            cells.append('%s %d deceptions, the hero deceives in %2.0f%%, helping the hero in %2.0f%% of those'
                         % (L, len(ds), 100.0 * len(hd) / max(1, len(ds)), 100.0 * sum(1 for x in hd if x['value'] == 'helps') / max(1, len(hd))))
        say('  %-8s %s' % (g, '; '.join(cells)))
    open(os.path.join(HERE, 'ValuesExplore.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
