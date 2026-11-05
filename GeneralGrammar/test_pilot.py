"""test_pilot.py -- CardPilotProtocol.md section 6, before any reader runs. Run after pilotSetup.py."""
import glob
import json
import os
import random
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pilot as P  # noqa: E402
import pilotSetup as U  # noqa: E402

bad = 0


def ok(name, cond, extra=''):
    global bad
    print('%-5s %s %s' % ('PASS' if cond else 'FAIL', name, extra))
    bad += 0 if cond else 1


key = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
sy = key['symbols']
ok('the codes map one to one onto his symbols', len(set(sy.values())) == len(sy) == 34, str(len(sy)))
ok('no code is a symbol of his', not (set(sy.values()) & set(sy)))
num = {u: i for i, u in enumerate('A a B C up D E F G H I K down'.split())}
num['a'] = num['A']

# the S tree holds nothing that points to him
files = [f for f in glob.glob(U.SREPO + '/**/*', recursive=True) if os.path.isfile(f) and '.git' not in f]
hits = {}
for f in files:
    t = open(f, encoding='utf-8').read()
    for w in ('Propp ', "Propp'", 'Afanasyev', 'Афанасьев', 'p.21', 'p.67', 'p.92', 'folklorist', 'morpholog', 'Morpholog'):
        if w in t:
            hits.setdefault(w, []).append(os.path.basename(f))
ok('no S file names him, his source or his pages', not hits, str({k: v[:3] for k, v in hits.items()}))
for name in U.CORPORA:
    r = open(os.path.join(U.SREPO, name, 'Rules.md'), encoding='utf-8').read()
    ok('%s: no Greek or arrow symbol' % name, not re.search(r'[α-ωΑ-Ω↑↓]', r))
    ok('%s: the word function is gone' % name, not re.search(r'[Ff]unction', r))
    table = r[r.index('| Symbol | What happens |'):r.index('## Transcription formats')]
    ok('%s: every code stands on the card once, in its first column' % name, all(len(re.findall(r'^\| %s \|' % c, table, re.M)) == 1 for c in sy.values()) and len(re.findall(r'^\| [A-Z][a-z]{2} \|', table, re.M)) == 34)
    ok('%s: the card has no order of his: the first row is not his first' % name, '| %s |' % sy['α'] != re.search(r'\| Symbol.*\n\|---.*\n(\| \w+ \|)', r).group(1))
    # his letters as symbols, outside the card: a capital standing alone, or with a minus
    body = r
    body = re.sub(r'Number moves I, II, III|move: I+\s|\| I \||to move I,|belong to move I|U\+2212|Y or N|Write N when|\| N \|', ' ', body)
    left = sorted(set(re.findall(r'(?<![\w\'])(?:A|B|C|D|E|F|G|H|J|I|K|L|M|N|Q|T|U|W|Pr|Rs|Ex)(?:−)?(?![\w\'])', body)) - {'A'})
    ok('%s: no symbol of his left in the rules' % name, not left, str(left))
    d = sorted(x for x in glob.glob(os.path.join(U.SREPO, name, 'tales', '*.txt')))
    ok('%s: 15 tales' % name, len(d) == 15)
    head = [open(f, encoding='utf-8').readline() for f in d]
    ok('%s: headers carry no source' % name, all(h.rstrip().endswith('| -') for h in head))
    ev = open(os.path.join(U.SREPO, name, 'Events.txt'), encoding='utf-8').read().splitlines()
    ids = {l.split(' | ')[0] for l in ev}
    ok('%s: the events cover exactly the coded ids' % name, ids == set(key['tales'][name].values()), str(len(ids)))
    for rd in 'AB':
        pr = open(os.path.join(HERE, 'PilotH', '%s-%s.txt' % (name, rd)), encoding='utf-8').read()
        ok('%s %s: H prompt lists its 15 tales and its own folder' % (name, rd), all(t in pr for t in key['tales'][name]) and 'PilotH/%s/' % rd in pr and pr.count('.txt, ') >= 14)

# the round trip: a tale coded by hand in his symbols, to S's and back
inv = {v: k for k, v in sy.items()}
hand = ['a', 'F', 'A', 'B', 'C', '↑', 'D', 'E', 'H', 'I', 'K', '↓', 'W']
tmp = tempfile.mkdtemp()
pa = os.path.join(tmp, 'n.txt')
some = list(key['tales']['wonder'].items())[0]
with open(pa, 'w', encoding='utf-8') as f:
    for i, u in enumerate(hand):
        f.write('%s | I | %d | ev %d | %s | x | y | Y | - |  | "q"\n' % (some[1], i + 1, i + 1, sy[u]))
    f.write('%s | I | 99 | ev 99 | %s− | x | y | Y | - |  | "q"\n' % (some[1], sy['F']))
    f.write('%s | I | 100 | ev 100 | X | x | y | N | - |  | "q"\n' % some[1])
code = {v: P.norm(k) for k, v in sy.items()}
n = P.parse_notes(pa, code, {v: k for k, v in key['tales']['wonder'].items()})
got = [u for e in n[some[0]] for u in n[some[0]][e]]
ok('a tale coded in his symbols maps to S and back', got == [P.norm(u) for u in hand] + ['F', 'X'], str(got[:4]))

# the measure
rng = random.Random(1)
order = 'A B C up D E F G H I K down'.split()
num = {u: i for i, u in enumerate(order)}
planted = {str(i): [u for u in order if rng.random() < .7] for i in range(30)}
t, _ = P.tau(list(planted.values()), num)
ok('strings in his order give a tau near 1', t > .95, '%.3f' % t)
shuf = {k: rng.sample(v, len(v)) for k, v in planted.items()}
t2, _ = P.tau(list(shuf.values()), num)
ok('shuffled strings give about 0', abs(t2) < .5, '%.3f' % t2)
d, lo, hi, nn = P.paired(planted, shuf, num)
ok('the bootstrap covers a planted difference', lo <= d <= hi and lo > .3, '%.3f [%.3f, %.3f]' % (d, lo, hi))
d0, lo0, hi0, _ = P.paired(planted, planted, num)
ok('no difference gives zero', abs(d0) < 1e-9 and lo0 <= 0 <= hi0)
a = P.paired(planted, shuf, num)
ok('two runs identical', a == (d, lo, hi, nn))
ok('reading: survives', P.reading(.75, .70, .05, -.1, .2, .6, .58) == 'SURVIVES')
ok('reading: written in', P.reading(.75, .35, .40, .2, .6, .6, .58) == 'WRITTEN IN')
ok('reading: in part', P.reading(.75, .55, .20, .0, .4, .6, .58) == 'IN PART')
ok('reading: unreadable when kappa falls', P.reading(.75, .35, .40, .2, .6, .6, .45) == 'UNREADABLE')
print('pilot tests: %s' % ('all pass' if not bad else '%d FAILED' % bad))
sys.exit(1 if bad else 0)
