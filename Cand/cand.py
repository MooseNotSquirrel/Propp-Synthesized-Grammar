#!/usr/bin/env python3
"""
cand.py -- the candidate acts of oath, prayer and curse, tested on eight plays no describer
has described in free verbs (CandProtocol.md).

  python cand.py setup    copies P01-P08 into StoryLanguage/Projects/ActsRoles/held/ and writes the prompts
  python cand.py form     checks the descriptions' form
  python cand.py score    writes Cand/CandRun.txt

The describers work under Free/FreeRules.md, unchanged. Written in full before any of the
eight plays was described.
"""
import collections
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Free'))
import free as F  # noqa: E402

OUT = F.OUT
HELD = os.path.join(OUT, 'held')
BATCHES = collections.OrderedDict([('g13', ['P01', 'P02']), ('g14', ['P03', 'P04']), ('g15', ['P05', 'P06']), ('g16', ['P07', 'P08'])])
CANDIDATES = collections.OrderedDict([('oath', ['promise', 'swear', 'vow']), ('prayer', ['pray']), ('curse', ['curse'])])
ALL = [v for vs in CANDIDATES.values() for v in vs]


def has_cast(p):
    return os.path.exists(os.path.join(P, 'Tragedy', 'plays', p, 'Cast.txt'))


def setup():
    names = F.Pm.play_names()
    for b, plays in BATCHES.items():
        for p in plays:
            d = os.path.join(HELD, 'tragedy', 'plays', p)
            os.makedirs(d, exist_ok=True)
            for f in ('Text.txt', 'Events.txt', 'Cast.txt'):
                src = os.path.join(P, 'Tragedy', 'plays', p, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(d, f))
        cast = all(has_cast(p) for p in plays)
        where = ("Each play is in its folder under held/tragedy/plays/: Text.txt, one speech per line; Events.txt, its events%s. %s Write the two plays one after the other, each line beginning with its play's identifier."
                 % ('; and Cast.txt, its cast' if cast else '',
                    "Name every performer and undergoer exactly as the play's Cast.txt names them." if cast
                    else 'These plays have no cast list; name every performer and undergoer as the text names them.'))
        files = ', '.join('held/tragedy/plays/%s/Text.txt%s' % (p, ', Events.txt and Cast.txt' if cast else ' and Events.txt') for p in plays)
        for L in 'AB':
            text = F.PROMPT.format(what='two Greek plays, %s, in English translation' % ' and '.join('%s (%s)' % (names[p], p) for p in plays),
                                   L=L, b=b, where=where, files=files, orig='')
            open(os.path.join(OUT, 'prompts', 'free-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
    print({b: v for b, v in BATCHES.items()})


def read(L, b):
    """[(play, event, verb)] and faults, as Free/free.py reads a batch"""
    path = os.path.join(OUT, 'free', L, b, 'Notes.txt')
    if not os.path.exists(path):
        return [], ['%s %s: no file' % (L, b)]
    out, faults = [], []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|', 8)]
        if len(f) < 9:
            continue
        ev = re.search(r'\d+', f[1])
        if not ev or not re.match(r'^[A-Z]\d+', f[0]):
            continue
        s = f[0].split('/')[0]
        if s not in BATCHES[b]:
            faults.append('%s %s line %d: story %s not in the batch' % (L, b, i, s))
            continue
        v = F.verb_of(f[2])
        if not v or f[6][:1].upper() not in 'YN':
            faults.append('%s %s line %d: verb or mark missing' % (L, b, i))
            continue
        out.append((s, int(ev.group()), v))
    return out, faults


def events(p):
    return [int(l.split('|')[1]) for l in open(os.path.join(P, 'Tragedy', 'plays', p, 'Events.txt'), encoding='utf-8')
            if l.count('|') >= 2 and l.split('|')[1].strip().isdigit()]


def form():
    total = 0
    for L in 'AB':
        for b, plays in BATCHES.items():
            rows, faults = read(L, b)
            unc = [(p, k) for p in plays for k in events(p) if not any(r[0] == p and r[1] == k for r in rows)]
            print('%s %-3s plays %s, entries %4d, uncovered events %3d, faults %d' % (L, b, ' '.join(plays), len(rows), len(unc), len(faults)))
            for x in faults[:5] + ['   uncovered: %s ev %d' % u for u in unc[:5]]:
                print('   ' + x)
            total += len(unc) + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def shares(verbs):
    n = float(len(verbs)) or 1.0
    c = collections.Counter(verbs)
    out = {k: sum(c[v] for v in vs) / n for k, vs in CANDIDATES.items()}
    out['all'] = sum(c[v] for v in ALL) / n
    return out


def score():
    rep = ['# CandRun.txt -- cand.py score, as CandProtocol.md freezes it.', '',
           'Shares of all verbs: oath (%s), prayer (%s), curse (%s), and the three together.' % tuple(', '.join(v) for v in CANDIDATES.values()), '']
    ok1, ok2 = True, True
    for L in 'AB':
        tales = [r[2] for b in ('t1', 't2', 't3', 't4') for r in F.read_free(L, b)[0]]
        seen = [r[2] for b in ['g%d' % i for i in range(1, 13)] for r in F.read_free(L, b)[0]]
        rows = [r for b in BATCHES for r in read(L, b)[0]]
        new = [r[2] for r in rows]
        st, ss, sn = shares(tales), shares(seen), shares(new)
        rep.append('describer %s: %d verbs in the 45 tales, %d in the 24 plays already described, %d in the eight new plays' % (L, len(tales), len(seen), len(new)))
        for k in list(CANDIDATES) + ['all']:
            rep.append('  %-7s tales %.2f%%, the 24 plays %.2f%%, the eight new plays %.2f%%' % (k, 100 * st[k], 100 * ss[k], 100 * sn[k]))
        ok1 = ok1 and sn['all'] >= 3 * st['all']
        per = collections.defaultdict(collections.Counter)
        for p, _, v in rows:
            for k, vs in CANDIDATES.items():
                per[k][p] += v in vs
        plays = [p for ps in BATCHES.values() for p in ps]
        for k in CANDIDATES:
            n = sum(1 for p in plays if per[k][p])
            ok2 = ok2 and n >= 4
            rep.append('  %-7s in %d of the 8 new plays: %s' % (k, n, ', '.join('%s %d' % (p, per[k][p]) for p in plays)))
        lam = sum(1 for v in new if v in ('lament', 'mourn', 'weep')) / float(len(new) or 1)
        rep.append('  reported: lament, mourn and weep together, %.2f%% of the new plays\' verbs' % (100 * lam))
        rep.append('')
    rep += ['PREDICTIONS (CandProtocol.md)',
            '  1. in the eight new plays the three candidates together are at least three times their share in the tales, for both describers: %s' % ('HOLDS' if ok1 else 'FAILS'),
            '  2. each of oath, prayer and curse occurs in at least four of the eight new plays, for both describers: %s' % ('HOLDS' if ok2 else 'FAILS')]
    open(os.path.join(HERE, 'CandRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    cmds = {'setup': setup, 'form': form, 'score': score}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
