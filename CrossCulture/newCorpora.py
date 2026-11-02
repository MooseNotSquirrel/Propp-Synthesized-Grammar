#!/usr/bin/env python3
"""
newCorpora.py -- the Native American and East Asian transcriptions, from Propp-ActsRoles to their corpus repositories and the
tables, as the animal tales' were (Animal/KeeperLog.md, 2026-10-20).

  python newCorpora.py form              the form check of ActsRoles/<native, eastasian>/transcriptions/ (reads no note's text)
  python newCorpora.py copy              copy Events.txt, Heroes.txt and transcriptions/ byte for byte to NativeAmerican/ and
                                         EastAsian/ (refused if a file there differs)
  python newCorpora.py snapshot <dir>    copy Data/tables/*.tsv to <dir>, before the tables are rebuilt
  python newCorpora.py compare <dir>     after the rebuild: every row of every table in <dir> is still present, in order, and
                                         every new row belongs to the new corpora

THE FORM CHECK, per corpus, transcriber and batch: the folder holds exactly Streams.txt, Notes.txt and Report.md; every line of
Notes.txt is an entry, blank, or a heading; an entry has eleven fields; its tale is one of the batch's; its move is a roman
numeral and its position a number; its event is one of the tale's listed events; its function is a symbol tragedyScore reads,
or X; its flag is Y or N. Every listed event of every tale in the batch has an entry, in every version: a tale is either
transcribed once, or in two or more versions /1, /2, ... each of which covers every event.
"""
import collections
import filecmp
import glob
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
AR = os.path.join(P, 'ActsRoles')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402
import setupTranscribe as ST  # noqa: E402

REPO = {'native': 'NativeAmerican', 'eastasian': 'EastAsian'}
ROMAN = re.compile(r'^[IVXL]+$')
ENTRY = re.compile(r'^([TOCJ]\d{2})(?:/(\d+))?$')


def events(c):
    out = collections.defaultdict(set)
    for line in open(os.path.join(AR, c, 'Events.txt'), encoding='utf-8'):
        f = [x.strip() for x in line.split('|')]
        if len(f) >= 3 and f[1].isdigit():
            out[f[0]].add(int(f[1]))
    return out


def form():
    ok = True
    for c, d in ST.CORPORA.items():
        evs = events(c)
        for L in 'AB':
            for k, (a, b) in enumerate(ST.BATCHES[c], 1):
                tales = d['ids'][a:b]
                folder = os.path.join(AR, c, 'transcriptions', L, 'b%d' % k)
                faults = []
                if sorted(os.listdir(folder)) != ['Notes.txt', 'Report.md', 'Streams.txt']:
                    faults.append('folder holds %s' % sorted(os.listdir(folder)))
                if os.path.getsize(os.path.join(folder, 'Streams.txt')) == 0:
                    faults.append('Streams.txt is empty')
                seen = collections.defaultdict(set)
                n = 0
                for i, line in enumerate(open(os.path.join(folder, 'Notes.txt'), encoding='utf-8'), 1):
                    s = line.strip()
                    if not s or s.startswith('#'):
                        continue
                    f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
                    m = ENTRY.match(f[0])
                    if len(f) < 11 or not m:
                        faults.append('line %d is not an entry' % i)
                        continue
                    n += 1
                    t, v = m.group(1), m.group(2) or ''
                    ev = re.match(r'^ev (\d+)$', f[3])
                    if t not in tales:
                        faults.append('line %d: tale %s not in the batch' % (i, t))
                    if not ROMAN.match(f[1]) or not f[2].isdigit():
                        faults.append('line %d: move or position malformed' % i)
                    if not ev or int(ev.group(1)) not in evs[t]:
                        faults.append('line %d: event %s not listed for %s' % (i, f[3], t))
                    else:
                        seen[(t, v)].add(int(ev.group(1)))
                    if not (TS.base(f[4]) or f[4] == 'X'):
                        faults.append('line %d: function %s unread' % (i, f[4]))
                    if f[7] not in ('Y', 'N'):
                        faults.append('line %d: flag %s' % (i, f[7]))
                versions = collections.defaultdict(list)
                for t, v in seen:
                    versions[t].append(v)
                for t in tales:
                    vs = sorted(versions.get(t, []))
                    if not vs or (vs != [''] and ('' in vs or len(vs) < 2)):
                        faults.append('%s: versions %s' % (t, vs))
                    for v in vs:
                        missing = sorted(evs[t] - seen[(t, v)])
                        if missing:
                            faults.append('%s%s: %d events without an entry' % (t, '/' + v if v else '', len(missing)))
                split = sorted(t for t in tales if versions.get(t, [''])[0] != '')
                print('%-9s %s b%d: %4d entries, %2d tales%s: %s' % (c, L, k, n, len(tales),
                      ' (in versions: %s)' % ', '.join(split) if split else '', 'in form' if not faults else 'FAULTS'))
                for x in faults[:20]:
                    print('    ' + x)
                ok &= not faults
    print('FORM CHECK %s' % ('PASSES' if ok else 'FAILS'))
    return ok


def copy():
    pairs = []
    for c, repo in REPO.items():
        src, dst = os.path.join(AR, c), os.path.join(P, repo)
        for name in ('Events.txt', 'Heroes.txt'):
            pairs.append((os.path.join(src, name), os.path.join(dst, name)))
        for f in glob.glob(os.path.join(src, 'transcriptions', '*', '*', '*')):
            pairs.append((f, os.path.join(dst, os.path.relpath(f, src))))
    clash = [d for s, d in pairs if os.path.exists(d) and not filecmp.cmp(s, d, shallow=False)]
    if clash:
        raise SystemExit('refusing: these exist with different content: %s' % clash)
    for s, d in pairs:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)
    bad = [d for s, d in pairs if not filecmp.cmp(s, d, shallow=False)]
    print('copied %d files byte for byte; %s' % (len(pairs), 'all identical' if not bad else 'DIFFER: %s' % bad))
    return not bad


def snapshot(d):
    os.makedirs(d, exist_ok=True)
    fs = glob.glob(os.path.join(ROOT, 'Data', 'tables', '*.tsv'))
    for f in fs:
        shutil.copyfile(f, os.path.join(d, os.path.basename(f)))
    print('%d tables copied to %s' % (len(fs), d))


def compare(d):
    ok = True
    for old in sorted(glob.glob(os.path.join(d, '*.tsv'))):
        name = os.path.basename(old)
        a = open(old, encoding='utf-8').read().split('\n')
        b = open(os.path.join(ROOT, 'Data', 'tables', name), encoding='utf-8').read().split('\n')
        new = [x for x in b if x.split('\t')[0].split(':')[0] in REPO]
        rest = [x for x in b if x.split('\t')[0].split(':')[0] not in REPO]
        same = rest == a
        ok &= same
        print('%-18s rows before %6d, after %6d: the new corpora\'s %5d; every other row unchanged and in order: %s'
              % (name, len(a), len(b), len(new), 'yes' if same else 'NO'))
    print('TABLES COMPARE %s' % ('PASSES' if ok else 'FAILS'))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['form']:
        sys.exit(0 if form() else 1)
    if a == ['copy']:
        sys.exit(0 if copy() else 1)
    if len(a) == 2 and a[0] == 'snapshot':
        snapshot(a[1])
    elif len(a) == 2 and a[0] == 'compare':
        sys.exit(0 if compare(a[1]) else 1)
    else:
        sys.exit(__doc__)
