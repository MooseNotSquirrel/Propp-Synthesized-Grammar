"""tragedyApart.py -- TragedyApartProtocol.md (frozen 2026-11-04). Commands: setup, test, score. Six batches, as frozen. The key stays here."""
import collections
import csv
import json
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'Induction'))
import pilot as P  # noqa: E402
import shuffled as S  # noqa: E402

TC = S.TC
SEED = 20261104
PER_PLAY, BATCHES = 15, 6
csv.field_size_limit(10 ** 9)
KEYF = os.path.join(HERE, 'TragedyKey.json')


def rows(t):
    with open(os.path.join(ROOT, 'Data/tables/%s.tsv' % t), encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)


def old_labels():
    import strings as ST
    TS = ST.TS
    old = {'A': collections.defaultdict(lambda: collections.defaultdict(list)), 'B': collections.defaultdict(lambda: collections.defaultdict(list))}
    for r in rows('functions'):
        if r['story'].startswith('tragedy:') and r['reader'] in old and r['version'] in ('', '1'):
            try:
                e = int(r['event'])
            except ValueError:
                continue
            ks = ['X'] if r['function'] == 'X' else [k for k in TS.key(r['function']) if k in TS.NUM]
            old[r['reader']][r['story'].split(':', 1)[1]][e].extend(ks)
    return old


def setup():
    old = old_labels()
    text, hero = {}, {}
    for r in rows('events'):
        if r['story'].startswith('tragedy:'):
            try:
                text[(r['story'].split(':', 1)[1], int(r['event']))] = r['text']
            except ValueError:
                pass
    for r in rows('heroes'):
        if r['story'].startswith('tragedy:') and r['reader'] == 'lister':
            hero[r['story'].split(':', 1)[1]] = r['hero']
    rng = random.Random(SEED)
    ids = rng.sample(range(10000, 99999), 600)
    key, bat, pos = {}, [[] for _ in range(BATCHES)], 0
    plays = sorted(set(old['A']) & set(old['B']))
    for s in plays:
        ev = sorted(e for e in set(old['A'][s]) & set(old['B'][s]) if (s, e) in text)
        pick = []
        for i in range(PER_PLAY):
            a, b = i * len(ev) // PER_PLAY, (i + 1) * len(ev) // PER_PLAY
            pick.append(ev[rng.randrange(a, b)])
        st = rng.randrange(BATCHES)
        for i, e in enumerate(pick):
            eid = 'e%05d' % ids[pos]
            pos += 1
            key[eid] = ['tragedy', s, e]
            bat[(st + i) % BATCHES].append('%s | hero: %s | %s' % (eid, hero.get(s, '-'), text[(s, e)]))
    for b, lines in enumerate(bat):
        rng.shuffle(lines)
        S_wr(os.path.join(TC, 'lines/tragedy/batch%d.txt' % (b + 1)), '\n'.join(lines) + '\n')
        for r in 'AB':
            S_wr(os.path.join(TC, 'prompts/lines-tragedy-%s%d.txt' % (r, b + 1)),
                 "You are coding single events from tales with a card. You start with no background on the project, and you should not look for any.\n\n"
                 "Read lines/Rules.md in this repository in full and follow it exactly. Your lines are in lines/tragedy/batch%d.txt. Open only those two files and your own output folder. Do not open, list or search anything else in this repository, and do not search the web.\n\n"
                 "Write one file, and nothing else, lines/tragedy/coded/%s/b%d/Coded.txt (create the folder), in the rules' format, one line for each of your lines.\n\n"
                 "Then reply with: the identifiers of any lines you could not code; then one line saying whether the card reminded you of any published scheme, and if so whose; then one line saying whether you could tell where events fell in their stories.\n" % (b + 1, r, b + 1))
    run = open(os.path.join(TC, 'RUN.md'), encoding='utf-8').read()
    if 'lines-tragedy' not in run:
        row = "| `lines-tragedy` | `prompts/lines-tragedy-A1.txt` to `-A6`, `-B1` to `-B6` | `-A`: Opus; `-B`: Sonnet | `lines/tragedy/coded/<A or B>/b<N>/Coded.txt` | `Report.md` in that folder | `run-lines-tragedy` |"
        a = run.index('\n\n1. Work from')
        S_wr(os.path.join(TC, 'RUN.md'), run[:a] + '\n' + row + run[a:])
    json.dump(key, open(KEYF, 'w', encoding='utf-8'), indent=0)
    print('plays', len(plays), 'events', len(key), [len(b) for b in bat])


def S_wr(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(t)


def test():
    bad = 0

    def ok(n, c, x=''):
        nonlocal bad
        print('%-5s %s %s' % ('PASS' if c else 'FAIL', n, x))
        bad += 0 if c else 1
    key = json.load(open(KEYF, encoding='utf-8'))
    seen, sizes = {}, []
    for b in range(1, BATCHES + 1):
        ls = open(os.path.join(TC, 'lines/tragedy/batch%d.txt' % b), encoding='utf-8').read().splitlines()
        sizes.append(len(ls))
        for l in ls:
            p = l.split(' | ', 2)
            if p[0] in seen:
                ok('duplicate', False, p[0])
            seen[p[0]] = (b, p[2])
    ok('every sampled event in exactly one batch', len(seen) == len(key) == 480, str(sizes))
    by = collections.defaultdict(list)
    for e, (b, _) in seen.items():
        by[key[e][1]].append((key[e][2], b))
    ok('15 events a play, 32 plays', len(by) == 32 and all(len(v) == 15 for v in by.values()))
    gap = 10 ** 6
    for v in by.values():
        v.sort()
        last = {}
        for i, (e, b) in enumerate(v):
            if b in last:
                gap = min(gap, e - last[b])
            last[b] = e
    ok('events sharing a batch stand far apart in their play', gap >= 6, 'nearest %d events' % gap)
    text = {}
    for r in rows('events'):
        if r['story'].startswith('tragedy:'):
            try:
                text[(r['story'].split(':', 1)[1], int(r['event']))] = r['text']
            except ValueError:
                pass
    ok('the key returns each line to its play and place', all(text[(key[e][1], key[e][2])] == t for e, (_, t) in seen.items()))
    hits = [f for f in os.listdir(os.path.join(TC, 'prompts')) if 'tragedy' in f and re.search(r'Propp|[Tt]ragedy of|function', open(os.path.join(TC, 'prompts', f), encoding='utf-8').read())]
    ok('no prompt points to him', not hits, str(hits))
    ok('no line carries a play id', not any(re.search(r'\bP\d\d\b', t) for _, t in seen.values()))
    ok('12 prompts', len([f for f in os.listdir(os.path.join(TC, 'prompts')) if f.startswith('lines-tragedy')]) == 12)
    ok('reading: says no', reading(.3, .1, -.1, .3, .5, .5) == 'THE TEST SAYS NO')
    ok('reading: labels carry', reading(.6, .3, .1, .5, .5, .5) == 'THE LABELS CARRY THE ORDER')
    ok('reading: in part', reading(.47, .1, -.1, .3, .5, .5) == 'IN PART')
    ok('reading: too poor', reading(.6, .3, .1, .5, .2, .5) == 'TOO POOR')
    print('tragedy tests: %s' % ('all pass' if not bad else '%d FAILED' % bad))
    sys.exit(1 if bad else 0)


def reading(t, d, lo, hi, kw, kab):
    if kw < .25 or kab < .25:
        return 'TOO POOR'
    if t < .45 and d < .20:
        return 'THE TEST SAYS NO'
    if t >= .5 and d >= .20 and lo > 0:
        return 'THE LABELS CARRY THE ORDER'
    return 'IN PART'


def boot_diff(a, b, num, draws=2000, seed=SEED):
    """tau of a minus tau of b, with independent bootstraps of stories; a and b: lists of strings"""
    rng = np.random.default_rng(seed)
    v = []
    for _ in range(draws):
        x = P.tau([a[i] for i in rng.integers(0, len(a), len(a))], num)[0]
        y = P.tau([b[i] for i in rng.integers(0, len(b), len(b))], num)[0]
        if x == x and y == y:
            v.append(x - y)
    return float(np.percentile(v, 5)), float(np.percentile(v, 95))


def score():
    import score as C
    slots, _ = C.propp()
    num = C.numbering(slots)
    pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    code = {c: P.norm(s) for s, c in pk['symbols'].items()}
    key = json.load(open(KEYF, encoding='utf-8'))
    sk = json.load(open(os.path.join(HERE, 'ShuffledKey.json'), encoding='utf-8'))
    old = old_labels()
    out = ['# TragedyApart.txt -- TragedyApartProtocol.md, the frozen reading; %d events' % len(key)]
    L, W = {}, {}
    for r in 'AB':
        L[r], bad = S.parse('tragedy', r, key, code)
        W[r] = collections.OrderedDict()
        for _, s, e in key.values():
            W[r].setdefault(s, {})[e] = old[r][s][e]
        W[r] = collections.OrderedDict((s, collections.OrderedDict(sorted(v.items()))) for s, v in W[r].items())
        out.append('%s: %d of %d coded; codes off the card %d' % (r, sum(map(len, L[r].values())), len(key), bad))
    kab = P.kappa(L['A'], L['B'])[0]
    out.append('kappa A with B, coded apart: %.3f' % kab)
    for r in 'AB':
        a, w = P.strings_of(L[r], num), P.strings_of(W[r], num)
        t, n = P.tau(list(a.values()), num)
        tw, nw = P.tau(list(w.values()), num)
        d, lo, hi, ns = P.paired(a, w, num)
        kw = P.kappa(L[r], W[r])[0]
        out.append('%s: coded apart tau %.3f (%d); whole-play, same events, %.3f (%d); D %.3f [%.3f, %.3f] on %d shared; kappa with whole-play %.3f; null 95th %.3f: %s' % (r, t, n, tw, nw, d, lo, hi, ns, kw, S.null95(list(a.values()), num), reading(t, d, lo, hi, kw, kab)))
    out.append('## beside the reading, not deciding')
    for r in 'AB':
        a = list(P.strings_of(L[r], num).values())
        for name in ('wonder', 'east'):
            kk = {k: v for k, v in sk.items() if v[0] == name}
            o, _ = S.parse(name, r, kk, code)
            b = list(P.strings_of(o, num).values())
            lo, hi = boot_diff(b, a, num)
            out.append('%s: %s coded apart %.3f, tragedies %.3f; difference 90%% interval [%.3f, %.3f]' % (r, name, P.tau(b, num)[0], P.tau(a, num)[0], lo, hi))
        wp = P.with_prep(L[r], num)
        out.append('%s: with preparatory units tau %.3f (%d); given a symbol %.3f, whole-play %.3f' % (r, *P.tau(list(wp.values()), num), P.covered(L[r]), P.covered(W[r])))
        pl, st = P.places(list(wp.values()))
        out.append('   mean place: ' + ' '.join('%s %.2f' % (u, pl[u]) for u in sorted(pl, key=lambda x: pl[x]) if st[u] >= 3))
    open(os.path.join(HERE, 'TragedyApart.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    {'setup': setup, 'test': test, 'score': score}[sys.argv[1]]()
