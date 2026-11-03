#!/usr/bin/env python3
"""
networks.py -- the character networks (ArcsNetworksProtocol.md section 3, frozen 2026-11-03 at the owner's word): who acts
on whom, one network per story and describer, from the acts layer alone, in the six corpora that have it.

  python networks.py na     test N-a: planted networks (a star, a ring, a hero who does every act)
  python networks.py nb     test N-b: every performer and undergoer name read is a node or counted as dropped, with its reason
  python networks.py t      test T: two runs byte-identical (written to a scratch folder and not shown)
  python networks.py run    write StoryModels/Networks.txt -- at the owner's word only, after the tests pass

How the protocol's words are read here:
- A name is a part of a performer or undergoer field as Spheres/explore.py splits it (Characters/SplitRule.md); a part
  with no letters, or only pronoun-like words, or "none" or "self", is dropped and counted. A story's names are joined as
  explore.merge joins them, and each joined name is a node.
- A node's degree is the number of acts it performs plus the number it undergoes, each act counted once on each side.
  An edge is a performer and undergoer pair, weighted by its acts.
- The hero's nodes are those whose name is the same as one of the lister's hero names (common.same). A story with none
  is "hero not found", left out of N1 to N3 and counted.
- N1: the hero is the most central when the nodes of highest degree are all the hero's (1), half when they share the top
  with others (0.5). N4: each story's top nodes share its one count, by their head word (explore.head).
- N6: two-sided permutation tests of the mean difference, the corpus labels permuted over stories, 10,000 times.
"""
import collections
import filecmp
import os
import sys
import tempfile

import numpy as np

import common as C

SX = C.SX
OUT = os.path.join(C.HERE, 'Networks.txt')
DECEIVE = {'deceive', 'claim-falsely', 'be-taken-in'}
DECEIVING = {'deceive', 'claim-falsely'}
NONE = {('none',), ('self',)}
SEED = 20261103
PERMS = 10000
MIN_SIDE = 10
EPS = 1e-12


# ---------------------------------------------------------------- names
def parts(raw):
    """[(name, None)] for the names a field holds, [(part, reason)] for the parts dropped"""
    out = []
    for p in (x.strip() for x in SX.SPLIT.split(SX.PAREN.sub(' ', raw or ''))):
        k = SX.key(p)
        if not k:
            out.append((p, 'no letters'))
        elif set(k) <= SX.PRONOUNS:
            out.append((p, 'pronoun-like'))
        elif k in NONE:
            out.append((p, 'none or self'))
        else:
            out.append((p, None))
    return out


# ---------------------------------------------------------------- one story's network
def network(acts, hero):
    """acts: [(act, performer field, undergoer field)]; hero: the lister's hero names.
    A dict of the story's measures, its names and drops (for N-b)."""
    rows, dropped, read = [], collections.Counter(), []
    for act, praw, uraw in acts:
        ps, us = parts(praw), parts(uraw)
        read += ps + us
        for p, why in ps + us:
            if why:
                dropped[why] += 1
        rows.append((act.lower(), [SX.key(p) for p, why in ps if not why], [SX.key(u) for u, why in us if not why]))
    canon = SX.merge([(a, p, u) for a, pp, uu in rows for p in pp or [()] for u in uu or [()]])
    out_d, in_d, edges = collections.Counter(), collections.Counter(), collections.Counter()
    node_rows = []
    for a, pp, uu in rows:
        P = sorted({canon.get(p, p) for p in pp})
        U = sorted({canon.get(u, u) for u in uu})
        for p in P:
            out_d[p] += 1
        for u in U:
            in_d[u] += 1
        for p in P:
            for u in U:
                if p != u:
                    edges[(p, u)] += 1
        node_rows.append((a, set(P), set(U)))
    nodes = sorted(set(out_d) | set(in_d))
    deg = {n: out_d[n] + in_d[n] for n in nodes}
    top = [n for n in nodes if deg[n] == max(deg.values())] if nodes else []
    hnodes = {n for n in nodes if any(C.same(' '.join(n), h) for h in hero)}
    m = {'acts': len(rows), 'nodes': len(nodes), 'edges': len(edges),
         'density': len(edges) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0.0,
         'dropped': dropped, 'read': read, 'canon': canon, 'node_set': set(nodes),
         'top_heads': [SX.head(n) for n in top], 'hero_found': bool(hnodes),
         'deception': sum(1 for a, _, _ in node_rows if a in DECEIVE) / len(rows) if rows else 0.0}
    if hnodes:
        m['central'] = 1.0 if set(top) <= hnodes else (0.5 if set(top) & hnodes else 0.0)
        m['hero_share'] = sum(1 for _, P, U in node_rows if (P | U) & hnodes) / len(rows)
        done = sum(1 for _, P, _ in node_rows if P & hnodes)
        under = sum(1 for _, _, U in node_rows if U & hnodes)
        m['agency'] = done / (done + under) if done + under else None
        dd = sum(1 for a, P, _ in node_rows if a in DECEIVING and P & hnodes)
        du = sum(1 for a, _, U in node_rows if a in DECEIVING and U & hnodes)
        m['deceives'] = dd > 0
        m['deceiver'] = dd / (dd + du) if dd + du else None
    return m


# ---------------------------------------------------------------- the stories
def stories():
    """[(story, reader, corpus, measures, agency by the significance layer's part)]"""
    lister, _ = C.heroes()
    sig = C.by_story('significance')
    out = []
    for (s, L), rows in C.by_story('acts').items():
        acts = [(r['act'], r['performer'], r['undergoer']) for r in C.in_order(rows)]
        m = network(acts, lister.get(s, []))
        parts_ = collections.Counter(r['part'] for r in sig.get((s, L), []))
        d, u = parts_['does'] + parts_['both'], parts_['undergoes'] + parts_['both']
        out.append((s, L, C.corpus(s), m, d / (d + u) if d + u else None))
    return out


def perm_test(a, b, rng):
    obs, pool, n = abs(np.mean(a) - np.mean(b)), np.array(list(a) + list(b), float), len(a)
    hit = 0
    for _ in range(PERMS):
        x = pool[rng.permutation(len(pool))]
        hit += abs(x[:n].mean() - x[n:].mean()) >= obs - EPS
    return float(np.mean(a) - np.mean(b)), (hit + 1) / (PERMS + 1)


def fmt(v, pc=False):
    v = [x for x in v if x is not None]
    if not v:
        return '-'
    return '%.0f%%' % (100 * np.mean(v)) if pc else '%.2f' % np.mean(v)


# ---------------------------------------------------------------- the report
def report():
    lister, readers = C.heroes()
    good = C.agreed(lister, readers)
    st = stories()
    rep = ['# Networks.txt -- networks.py: the character networks (ArcsNetworksProtocol.md, frozen 2026-11-03); EXPLORATORY.',
           '#  Every figure per describer, A (Opus) / B (Sonnet); agreed-hero stories in brackets where given.',
           '#  Left out: ' + C.LEFT_OUT + '.', '']

    def sel(g, L, sub=None, found=False):
        return [x for x in st if x[2] == g and x[1] == L and (sub is None or x[0] in sub) and (not found or x[3]['hero_found'])]

    def cell(f, g, pc=False, sub=True):
        out = []
        for L in C.READERS:
            a = fmt([f(x) for x in sel(g, L, found=True)], pc)
            out.append('%s (%s)' % (a, fmt([f(x) for x in sel(g, L, good, True)], pc)) if sub else a)
        return ' / '.join(out)

    rep.append('## N5. Size, and the hero found')
    rep.append('%-16s %14s %14s %14s %14s %16s %18s' % ('corpus', 'networks', 'acts', 'nodes', 'edges', 'density', 'hero not found'))
    for g in C.ORDER:
        c = lambda f: ' / '.join(fmt([f(x) for x in sel(g, L)]) for L in C.READERS)
        rep.append('%-16s %14s %14s %14s %14s %16s %18s' % (
            C.NAMES[g], ' / '.join(str(len(sel(g, L))) for L in C.READERS), c(lambda x: x[3]['acts']),
            c(lambda x: x[3]['nodes']), c(lambda x: x[3]['edges']), c(lambda x: x[3]['density']),
            ' / '.join(str(sum(1 for x in sel(g, L) if not x[3]['hero_found'])) for L in C.READERS)))
    drops = collections.Counter()
    for x in st:
        drops.update(x[3]['dropped'])
    rep.append('#  names dropped, all corpora and describers: %s' % ', '.join('%s %d' % kv for kv in sorted(drops.items())))

    rep += ['', '## N1. Centrality: the hero the most central character; the hero\'s share of the story\'s acts']
    rep.append('%-16s %30s %30s' % ('corpus', 'hero most central', 'hero\'s share of acts'))
    for g in C.ORDER:
        rep.append('%-16s %30s %30s' % (C.NAMES[g], cell(lambda x: x[3]['central'], g, True), cell(lambda x: x[3]['hero_share'], g, True)))

    rep += ['', '## N2. Agency: acts done over acts done and undergone, from the acts layer and from the significance layer\'s part']
    rep.append('%-16s %30s %30s' % ('corpus', 'acts layer', 'significance part'))
    for g in C.ORDER:
        rep.append('%-16s %30s %30s' % (C.NAMES[g], cell(lambda x: x[3]['agency'], g), cell(lambda x: x[4], g)))

    rep += ['', '## N3. Deception: its share of acts; stories in which the hero deceives; the hero as deceiver over deceived']
    rep.append('%-16s %30s %30s %30s' % ('corpus', 'deception share', 'hero deceives', 'hero deceiver share'))
    for g in C.ORDER:
        rep.append('%-16s %30s %30s %30s' % (C.NAMES[g], cell(lambda x: x[3]['deception'], g, True),
                                             cell(lambda x: float(x[3]['deceives']), g, True), cell(lambda x: x[3]['deceiver'], g, True)))

    rep += ['', '## N4. One figure across a cycle: the heads of each story\'s most central characters']
    for g in C.ORDER:
        for L in C.READERS:
            cnt = collections.Counter()
            xs = sel(g, L)
            for x in xs:
                hs = x[3]['top_heads']
                for h in hs:
                    cnt[h] += 1 / len(hs)
            tot = sum(cnt.values())
            if not tot:
                continue
            share = {h: v / tot for h, v in cnt.items()}
            best = sorted(share.items(), key=lambda kv: (-kv[1], kv[0]))
            rep.append('%-16s %s  stories %2d  top head %.0f%%  Herfindahl %.3f  heads %d: %s' % (
                C.NAMES[g], L, len(xs), 100 * best[0][1], sum(v * v for v in share.values()), len(share),
                ', '.join('%s %.1f' % (h, cnt[h]) for h, _ in best[:5])))

    rep += ['', '## N6. The corpora compared: mean difference (row corpus minus column corpus), two-sided permutation p (%d)' % PERMS]
    rng = np.random.default_rng(SEED)
    for label, f in (('N1 hero most central', lambda x: x[3].get('central')),
                     ('N2 agency, acts layer', lambda x: x[3].get('agency')),
                     ('N3 deception share', lambda x: x[3]['deception'] if x[3]['hero_found'] else None)):
        rep.append(label)
        for L in C.READERS:
            for i, g in enumerate(C.ORDER):
                for h in C.ORDER[i + 1:]:
                    a = [f(x) for x in sel(g, L) if f(x) is not None]
                    b = [f(x) for x in sel(h, L) if f(x) is not None]
                    if min(len(a), len(b)) < MIN_SIDE:
                        rep.append('  %s %-16s %-16s  fewer than %d stories a side' % (L, C.NAMES[g], C.NAMES[h], MIN_SIDE))
                        continue
                    d, p = perm_test(a, b, rng)
                    rep.append('  %s %-16s %-16s  %+.3f  p %.4f%s' % (L, C.NAMES[g], C.NAMES[h], d, p, '  *' if p <= .05 else ''))
    return '\n'.join(rep) + '\n'


def run(path=OUT, show=True):
    text = report()
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
    if show:
        print(text, end='')


# ---------------------------------------------------------------- the tests
def na():
    ok = []
    star = network([('harm', 'the Fox', 'leaf %s' % w) for w in ('one', 'two', 'three', 'four', 'five')], ['the Fox'])
    ok.append(('star: the hub the most central', star['central'] == 1.0))
    ok.append(('star: N4 head the hub\'s', star['top_heads'] == ['fox']))
    ring = network([('harm', 'Ant', 'Bee'), ('harm', 'Bee', 'Cat'), ('harm', 'Cat', 'Dog'), ('harm', 'Dog', 'Ant')], ['Ant'])
    ok.append(('ring: no single centre', len(ring['top_heads']) == 4 and ring['central'] == 0.5))
    solo = network([('give', 'Ivan', 'the old woman'), ('fight', 'Ivan', 'the serpent'), ('leave', 'Ivan', '')], ['Ivan'])
    ok.append(('hero doing every act: N2 = 1', solo['agency'] == 1.0))
    trick = network([('deceive', 'Raven', 'the chief'), ('deceive', 'the chief', 'Raven'), ('deceive', 'Raven', 'Gull')], ['Raven'])
    ok.append(('deceiver share 2 of 3', abs(trick['deceiver'] - 2 / 3) < EPS and trick['deception'] == 1.0))
    for name, v in ok:
        print('N-a %-40s %s' % (name, 'PASS' if v else 'FAIL'))
    print('N-a: %s' % ('PASS' if all(v for _, v in ok) else 'FAIL'))


def nb():
    lister, _ = C.heroes()
    read = dropped = kept = lost = 0
    for (s, L), rows in C.by_story('acts').items():
        m = network([(r['act'], r['performer'], r['undergoer']) for r in rows], lister.get(s, []))
        for p, why in m['read']:
            read += 1
            if why:
                dropped += 1
            else:
                kept += 1
                if m['canon'].get(SX.key(p), SX.key(p)) not in m['node_set']:
                    lost += 1
    fields = sum(2 for rows in C.by_story('acts').values() for _ in rows)
    print('N-b fields %d, name parts read %d: nodes %d, dropped with a reason %d, neither %d: %s'
          % (fields, read, kept, dropped, lost, 'PASS' if lost == 0 and kept + dropped == read else 'FAIL'))


def t():
    d = tempfile.mkdtemp()
    a, b = os.path.join(d, 'one.txt'), os.path.join(d, 'two.txt')
    run(a, False)
    run(b, False)
    same = filecmp.cmp(a, b, shallow=False)
    print('T two runs byte-identical: %s (in %s, not shown)' % ('PASS' if same else 'FAIL', d))


if __name__ == '__main__':
    cmd = sys.argv[1:]
    fns = {'na': na, 'nb': nb, 't': t, 'run': run}
    if len(cmd) != 1 or cmd[0] not in fns:
        sys.exit(__doc__)
    fns[cmd[0]]()
