"""test_shuffled.py -- ShuffledProtocol.md section 6, before any reader runs."""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shuffled as S  # noqa: E402
import pilot as P  # noqa: E402

TC = S.TC
bad = 0


def ok(n, c, x=''):
    global bad
    print('%-5s %s %s' % ('PASS' if c else 'FAIL', n, x))
    bad += 0 if c else 1


key = json.load(open(os.path.join(HERE, 'ShuffledKey.json'), encoding='utf-8'))
pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
for name, n in (('wonder', 488), ('east', 376)):
    seen = {}
    sizes = []
    for b in range(1, 7):
        ls = open(os.path.join(TC, 'lines', name, 'batch%d.txt' % b), encoding='utf-8').read().splitlines()
        sizes.append(len(ls))
        for l in ls:
            eid = l.split(' | ')[0]
            ok_id = re.fullmatch(r'e\d{4}', eid)
            if not ok_id or eid in seen:
                ok('bad id', False, eid)
            seen[eid] = b
    ok('%s: every event in exactly one batch' % name, len(seen) == n and all(key[e][0] == name for e in seen), str(sizes))
    ok('%s: batches about equal' % name, max(sizes) - min(sizes) <= 15)
    by = collections.defaultdict(list)
    for e, b in seen.items():
        by[key[e][1]].append((key[e][2], b))
    gap = 99
    for t, v in by.items():
        v.sort()
        last = {}
        for i, (_, b) in enumerate(v):
            if b in last:
                gap = min(gap, i - last[b])
            last[b] = i
    ok('%s: events sharing a batch stand at least six apart' % name, gap >= 6, str(gap))
    # the key restores story order
    ev = {}
    for l in open(os.path.join(TC, name, 'Events.txt'), encoding='utf-8'):
        p = l.rstrip('\n').split(' | ', 2)
        ev[(p[0], int(p[1]))] = p[2]
    back = pk['tales'][name]
    good = 0
    for b in range(1, 7):
        for l in open(os.path.join(TC, 'lines', name, 'batch%d.txt' % b), encoding='utf-8'):
            p = l.rstrip('\n').split(' | ', 2)
            _, t, e = key[p[0]]
            good += ev[(back[t], e)] == p[2]
    ok('%s: the key returns each line to its tale and place' % name, good == n, str(good))
texts = [f for f in glob.glob(TC + '/lines/**/*.txt', recursive=True) + glob.glob(TC + '/prompts/lines-*.txt') + [TC + '/lines/Rules.md']]
hits = collections.Counter()
for f in texts:
    t = open(f, encoding='utf-8').read()
    for w in ('Propp', 'Afanasyev', 'Morpholog', 'folktale', 'function', 'Function', 'tale identifier', ' T01', ' E01'):
        if w in t and not (w == 'folktale'):
            hits[w] += 1
    if re.search(r'[α-ωΑ-Ω↑↓]', t) and 'Rules' in f:
        hits['greek'] += 1
ok('nothing points to him, his terms, or a tale id', not hits, str(dict(hits)))
r = open(TC + '/lines/Rules.md', encoding='utf-8').read()
ok('every code on the card once', all(len(re.findall(r'^\| %s \|' % c, r, re.M)) == 1 for c in pk['symbols'].values()))
ok('24 prompts', len(glob.glob(TC + '/prompts/lines-*.txt')) == 24)
num = {u: i for i, u in enumerate('A B C up D E F G H I K down'.split())}
whole = collections.OrderedDict()
for i in range(15):
    whole[str(i)] = collections.OrderedDict((j, [u]) for j, u in enumerate(num))
lo, hi = S.noisy_range(whole, 0.0, num, draws=20)
ok('no noise gives the whole figure', lo > .95)
lo2, _ = S.noisy_range(whole, 0.8, num, draws=100)
ok('heavy noise lowers it', lo2 < lo - .3, '%.2f' % lo2)
n95 = S.null95([list(num)] * 15, num, draws=200)
ok('the null stands well below', n95 < .7, '%.2f' % n95)
ok('reading: in the events', S.reading(.7, .5, .5, .4, .3) == 'IN THE EVENTS')
ok('reading: needs the sequence', S.reading(.2, .5, .5, .4, .3) == 'NEEDS THE SEQUENCE')
ok('reading: in part', S.reading(.35, .5, .5, .4, .3) == 'IN PART')
ok('reading: too poor', S.reading(.7, .2, .5, .4, .3) == 'TOO POOR')
print('shuffled tests: %s' % ('all pass' if not bad else '%d FAILED' % bad))
sys.exit(1 if bad else 0)
