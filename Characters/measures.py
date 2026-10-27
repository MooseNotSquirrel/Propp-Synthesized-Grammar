#!/usr/bin/env python3
"""
measures.py -- the measures of Data/CharacterProtocol.md section 4, and the scoring of its predictions 1 to 6 (section 5),
read from tables/characters.tsv through tables.py. Every figure is given for readers A and B separately.

  python measures.py run             write Characters/CharacterRun.txt
  python measures.py run --amended   write Characters/CharacterRun-amended.txt: the same measures on the table amended
                                     after the measures (Characters/SenseRule.md), reported beside the record, not
                                     replacing it (CharacterProtocol.md section 8)

1. Kind by role: for the characters holding each of the seven spheres, and for those holding any, the share of each
   kind; unknown is a share of its own, and a role whose unknown is 10% or more is UNRESOLVED.
2. Roles by two routes. Top-down: the share of sphere-holders holding two spheres or more, and the commonest
   combinations. Bottom-up: characters with at least 3 acts grouped by their act profiles alone (characters.group:
   average linkage, cosine distance, silhouette from 3 to 10), with the COLLAPSED guard of test C5; each group's size,
   commonest acts as performer and as undergoer, commonest kinds, the sphere it matches if any, and the grouping's
   agreement with the spheres (adjusted Rand index). The myths have no acts, and their grouping is reported as not
   possible.
3. Rank by frequency: characters joined across a corpus's stories by head noun, ranked by the stories they appear in
   and by the acts they perform (for the myths, the functions they perform); given by head noun, by kind and by role,
   with each head-noun ranking's top-five share and its slope of log frequency against log rank.

The keeper's operational rules, fixed here before the run (not from Propp, not the owner's):
- a group matches a sphere when at least half its members hold that sphere; a group that matches none is reported as
  a role the corpus has that Propp's seven do not name;
- prediction 6's shuffle test permutes the grouping's labels across characters, 1,000 times with fixed seeds. The
  grouping does not depend on the order of its rows, so regrouping profiles shuffled across characters gives the real
  partition with its characters permuted; permuting the labels is the same test, without 1,000 regroupings. It passes
  when at most 5% of shuffles reach the real agreement;
- prediction 6 holds for a reader when the test passes on every corpus whose grouping does not collapse, and is not
  testable for a reader whose every grouping collapses.
"""
import collections
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import characters as C  # noqa: E402

DT = C.DT
CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'myth']
NAMES = {'tale': 'wondertales', 'animal': 'animal tales', 'fable': 'fables', 'tragedy': 'tragedies', 'myth': 'myths'}
KINDS = ['person', 'animal', 'deity', 'supernatural', 'object', 'unknown']
SPHERES = list(C.SX.SPHERES)
SHUFFLES = 1000
OUT = os.path.join(HERE, 'CharacterRun.txt')
AMENDED = os.path.join(HERE, 'CharacterRun-amended.txt')


def counts(field):
    """{'p:give': 3, ...} from an acts or relations field"""
    out = {}
    for t in field.split('; '):
        if t:
            k, n = t.rsplit(' ', 1)
            out[k] = int(n)
    return out


def spheres(r):
    return [x for x in r['spheres'].split(' + ') if x]


def pct(a, b):
    return 100.0 * a / b if b else 0.0


def kind_share(rows):
    k = collections.Counter(r['kind'] for r in rows)
    return {x: pct(k[x], len(rows)) for x in KINDS}


def fmt_kinds(sh):
    return ', '.join('%s %.0f%%' % (x, sh[x]) for x in KINDS if sh[x] >= 0.5)


# ---------------------------------------------------------------- 1. kind by role
def kind_by_role(rows, out):
    res = {}
    holders = [r for r in rows if spheres(r)]
    for role in SPHERES + ['any sphere']:
        rs = holders if role == 'any sphere' else [r for r in holders if role in spheres(r)]
        if not rs:
            out.append('    %-11s none' % role)
            continue
        sh = kind_share(rs)
        res[role] = sh
        state = 'UNRESOLVED (unknown %.0f%%)' % sh['unknown'] if sh['unknown'] >= 10 else fmt_kinds(sh)
        out.append('    %-11s %4d: %s' % (role, len(rs), state))
    return res


# ---------------------------------------------------------------- 2. roles, top-down and bottom-up
def top_down(rows, out):
    holders = [r for r in rows if spheres(r)]
    two = [r for r in holders if len(spheres(r)) >= 2]
    combos = collections.Counter(r['spheres'] for r in two)
    out.append('    sphere-holders %d, holding two spheres or more %d (%.0f%%); commonest combinations: %s'
               % (len(holders), len(two), pct(len(two), len(holders)),
                  '; '.join('%s %d' % kv for kv in sorted(combos.items(), key=lambda kv: (-kv[1], kv[0]))[:5]) or 'none'))


def bottom_up(rows, out):
    """the grouping's figures; returns (ari, shuffles reaching it, collapsed) or None where there are no acts"""
    import numpy as np
    from sklearn.metrics import adjusted_rand_score as ari
    F = C.features()
    ix = {f: i for i, f in enumerate(F)}
    chars = []
    for r in rows:
        a = {k: v for k, v in counts(r['acts']).items() if k in ix}
        if sum(a.values()) >= 3:
            chars.append((r, a))
    if not chars:
        out.append('    bottom-up: not possible (no character has 3 acts)')
        return None
    X = np.zeros((len(chars), len(F)))
    for i, (_, a) in enumerate(chars):
        for k, v in a.items():
            X[i, ix[k]] = v
    lab = list(C.group(X))
    S = [r['spheres'] or 'none' for r, _ in chars]
    size = collections.Counter(lab)
    collapsed = max(size.values()) > 0.6 * len(chars) or sum(1 for v in size.values() if v >= 5) < 3
    real = ari(S, lab)
    out.append('    bottom-up: %d characters with 3 acts or more, %d groups, agreement with the spheres ARI %.3f%s'
               % (len(chars), len(size), real, ' -- COLLAPSED, not read further' if collapsed else ''))
    if not collapsed:
        for g in sorted(size, key=lambda g: (-size[g], g)):
            mem = [chars[i] for i in range(len(chars)) if lab[i] == g]
            p, u = collections.Counter(), collections.Counter()
            for _, a in mem:
                for k, v in a.items():
                    (p if k.startswith('p:') else u)[k[2:]] += v
            held = collections.Counter(x for r, _ in mem for x in spheres(r))
            match = [x for x in SPHERES if held[x] >= 0.5 * len(mem)]
            top = lambda c: ', '.join('%s %d' % kv for kv in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:5]) or 'none'
            out.append('      group %d, %d characters; matches %s' % (g, len(mem), ' + '.join(match) if match else
                                                                       'no sphere: a role the corpus has that Propp\'s seven do not name'))
            out.append('        performs: %s' % top(p))
            out.append('        undergoes: %s' % top(u))
            out.append('        kinds: %s' % fmt_kinds(kind_share([r for r, _ in mem])))
            out.append('        spheres held: %s' % (', '.join('%s %d' % kv for kv in sorted(held.items(), key=lambda kv: (-kv[1], kv[0]))) or 'none'))
    reach = 0
    for i in range(SHUFFLES):
        perm = lab[:]
        random.Random(i).shuffle(perm)
        reach += ari(S, perm) >= real
    out.append('    shuffle test: %d of %d shuffles reach the real agreement (passes at %d or fewer): %s'
               % (reach, SHUFFLES, SHUFFLES // 20, 'pass' if reach <= SHUFFLES // 20 else 'FAIL'))
    return real, reach, collapsed


# ---------------------------------------------------------------- 3. rank by frequency
def concentration(freq):
    """the top-five share and the slope of log frequency against log rank"""
    fs = sorted((f for f in freq if f > 0), reverse=True)
    if len(fs) < 2:
        return 0.0, 0.0
    xs = [math.log(i) for i in range(1, len(fs) + 1)]
    ys = [math.log(f) for f in fs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return pct(sum(fs[:5]), sum(fs)), slope


def ranking(rows, g, out):
    by = {'head': collections.defaultdict(lambda: [set(), 0]), 'kind': collections.defaultdict(lambda: [set(), 0]),
          'role': collections.defaultdict(lambda: [set(), 0])}
    for r in rows:
        n = int(r['performs']) if g == 'myth' else sum(v for k, v in counts(r['acts']).items() if k.startswith('p:'))
        keys = {'head': [r['head'] or r['character']], 'kind': [r['kind']], 'role': spheres(r) or ['no sphere']}
        for unit, ks in keys.items():
            for k in ks:
                by[unit][k][0].add(r['story'])
                by[unit][k][1] += n
    res = {}
    what = 'functions' if g == 'myth' else 'acts'
    for i, count in ((0, 'stories'), (1, what)):
        f = {k: (len(v[0]) if i == 0 else v[1]) for k, v in by['head'].items()}
        share, slope = concentration(list(f.values()))
        res[count if i == 0 else 'acts'] = share
        top = sorted(f.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        out.append('    by %s, head nouns %d: top-five share %.1f%%, slope %.2f; top ten: %s'
                   % (count, len(f), share, slope, ', '.join('%s %d' % kv for kv in top)))
        for unit in ('kind', 'role'):
            f2 = {k: (len(v[0]) if i == 0 else v[1]) for k, v in by[unit].items()}
            out.append('      by %s, by %s: %s' % (count, unit, ', '.join('%s %d' % kv for kv in sorted(f2.items(), key=lambda kv: (-kv[1], kv[0])))))
    return res


# ---------------------------------------------------------------- the run
def verdict(a, b):
    if a is None or b is None:
        return 'NOT TESTABLE'
    return 'HOLDS' if a and b else ('SPLIT' if a or b else 'FAILS')


def run(amended=False):
    rows = DT.rows('characters')
    cell = collections.defaultdict(list)
    for r in rows:
        cell[(r['corpus'], r['reader'])].append(r)
    if amended:
        out = ['# CharacterRun-amended.txt -- measures.py run --amended: the measures of Data/CharacterProtocol.md section 4, and '
               'predictions 1 to 6, on the table AMENDED AFTER THE MEASURES (Characters/SenseRule.md, CharacterProtocol.md section 8)',
               '# reported beside the verdicts of record in CharacterRun.txt, not replacing them; the amendment was prompted partly by '
               'faults seen in prediction 2\'s figures',
               '# every figure for readers A and B separately; the keeper\'s operational rules are in measures.py\'s header']
    else:
        out = ['# CharacterRun.txt -- measures.py: the measures of Data/CharacterProtocol.md section 4, and predictions 1 to 6',
               '# every figure for readers A and B separately; the keeper\'s operational rules are in measures.py\'s header']
    K, B, R = {}, {}, {}
    for g in CORPORA:
        for L in 'AB':
            rs = cell[(g, L)]
            out.append('')
            out.append('== %s, reader %s: %d characters in %d stories' % (NAMES[g], L, len(rs), len({r['story'] for r in rs})))
            out.append('  1. kind by role')
            K[(g, L)] = kind_by_role(rs, out)
            out.append('  2. roles')
            top_down(rs, out)
            if g == 'myth':
                out.append('    bottom-up: not possible (the myths have functions but no acts)')
                B[(g, L)] = None
            else:
                B[(g, L)] = bottom_up(rs, out)
            out.append('  3. rank by frequency')
            R[(g, L)] = ranking(rs, g, out)

    out.append('')
    out.append('== reported, not tested')
    for g in CORPORA:
        a = {(r['story'], r['character']): r['kind'] for r in cell[(g, 'A')]}
        b = {(r['story'], r['character']): r['kind'] for r in cell[(g, 'B')]}
        both = sorted(set(a) & set(b))
        out.append('  readers\' agreement on kind, %s: %d characters in both readers\' tables, the same kind %d (%.0f%%)'
                   % (NAMES[g], len(both), sum(a[k] == b[k] for k in both), pct(sum(a[k] == b[k] for k in both), len(both))))
    for s in ('P01', 'P04', 'P06', 'P08'):
        for L in 'AB':
            hs = [r for r in cell[('tragedy', L)] if r['story'] == s and 'hero' in spheres(r)]
            out.append('  heroes of %s, reader %s: %s' % (s, L, '; '.join('%s (%s; %s)' % (r['character'], r['kind'], r['spheres']) for r in hs) or 'none'))
    ref = {'animal': 71, 'person': 22, 'deity': 4}
    for L in 'AB':
        sh = K[('fable', L)].get('hero')
        if sh:
            diff = ', '.join('%s %.0f%% against %d%%%s' % (k, sh[k], v, ' (DIFFERS BY MORE THAN 5 POINTS: to be explained)' if abs(sh[k] - v) > 5 else '')
                             for k, v in ref.items())
            out.append('  fables\' heroes, reader %s, beside PreliminaryFindings.md section 5: %s' % (L, diff))

    out.append('')
    out.append('== predictions (CharacterProtocol.md section 5): HOLDS if for both readers, SPLIT if for one, FAILS if for neither')
    share = lambda g, L, k: K[(g, L)].get('any sphere', {}).get(k, 0.0)
    for n, g, k, text in ((1, 'tale', 'person', 'in the wondertales, person over half of sphere-holders'),
                          (2, 'fable', 'animal', 'in the fables, animal over half of sphere-holders'),
                          (3, 'animal', 'animal', 'in the animal tales, animal over half of sphere-holders')):
        a, b = share(g, 'A', k) > 50, share(g, 'B', k) > 50
        out.append('  %d. %s: A %.1f%%, B %.1f%%: %s' % (n, text, share(g, 'A', k), share(g, 'B', k), verdict(a, b)))
    p4 = {}
    for L in 'AB':
        d = {g: share(g, L, 'deity') for g in CORPORA}
        p4[L] = min(d['myth'], d['tragedy']) > max(d['tale'], d['fable'])
        out.append('  4. reader %s, deity share of sphere-holders: myths %.1f%%, tragedies %.1f%%, wondertales %.1f%%, fables %.1f%%: %s'
                   % (L, d['myth'], d['tragedy'], d['tale'], d['fable'], 'holds' if p4[L] else 'does not hold'))
    out.append('  4. the deity share higher in the myths and the tragedies than in the wondertales and the fables: %s' % verdict(p4['A'], p4['B']))
    p5 = {}
    for L in 'AB':
        s = {g: R[(g, L)]['stories'] for g in ('fable', 'animal', 'tragedy')}
        p5[L] = min(s['fable'], s['animal']) > s['tragedy']
        out.append('  5. reader %s, top-five share of the ranking by stories: fables %.1f%%, animal tales %.1f%%, tragedies %.1f%%: %s'
                   % (L, s['fable'], s['animal'], s['tragedy'], 'holds' if p5[L] else 'does not hold'))
    out.append('  5. stock actors, the top-five share higher in the fables and the animal tales than in the tragedies: %s' % verdict(p5['A'], p5['B']))
    p6 = {}
    for L in 'AB':
        res = {g: B[(g, L)] for g in CORPORA if B[(g, L)] is not None}
        open_ = {g: x for g, x in res.items() if not x[2]}
        p6[L] = None if not open_ else all(x[1] <= SHUFFLES // 20 for x in open_.values())
        out.append('  6. reader %s: %s' % (L, '; '.join('%s %s' % (NAMES[g], 'COLLAPSED' if x[2] else 'ARI %.3f, %d of %d shuffles reach it' % (x[0], x[1], SHUFFLES))
                                                    for g, x in res.items())))
    out.append('  6. the grouping agrees with the spheres better than shuffled profiles do, where it does not collapse: %s' % verdict(p6['A'], p6['B']))
    text = '\n'.join(out) + '\n'
    open(AMENDED if amended else OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a not in (['run'], ['run', '--amended']):
        sys.exit(__doc__)
    run(amended=a == ['run', '--amended'])
