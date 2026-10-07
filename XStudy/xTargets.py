#!/usr/bin/env python3
"""
xTargets.py -- the X study's target events (XStudyProtocol.md).

  python xTargets.py     writes XStudy/Targets.txt (keeper side: every target event,
                         discovery and test, with its genre and link) and the
                         labelers' material, Story Language/XStudy/stories/b1..b4.txt
                         (discovery only)

A target event: in the original transcriptions, both transcribers wrote only
X for it, and both marked it as mattering (Y). Its link: at least one
transcriber named another event it depends on or leads to.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARENT = os.path.dirname(ROOT)
OUT = os.path.join(PARENT, 'XStudy')
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(ROOT, 'Calibration', 'Split.txt'), encoding='utf-8') if '|' in l}


def notes(paths):
    """{story: {event: [(symbol, mark, link)]}}"""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            if ev:
                out[f[0].split('/')[0]][int(ev.group())].append(
                    (f[4].strip(), f[7][:1].upper(), bool(re.search(r'\d', f[8]))))
    return out


def events(path, story_field=0, text_field=-1):
    """{story: [(event number, text)]} from an event list."""
    out = collections.OrderedDict()
    for line in open(path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|')]
        if len(f) >= 3 and re.match(r'^[PFA]\d{2}', f[0]) and f[1].isdigit():
            out.setdefault(f[0], []).append((int(f[1]), f[text_field]))
    return out


def corpora():
    """(genre, part, story list or None, notes A, notes B, event lists)"""
    af = os.path.join(PARENT, 'Afanasyev')
    ev_af = events(os.path.join(af, 'Events.txt'))
    nA = notes(glob.glob(os.path.join(af, 'transcriptions', 'U', 'A', 'b*', 'Notes.txt')))
    nB = notes(glob.glob(os.path.join(af, 'transcriptions', 'U', 'B', 'b*', 'Notes.txt')))
    for part, key in (('discovery', 'dev'), ('test', 'test')):
        yield 'wondertale', part, ['A%03d' % t for t in SPLIT[key]], nA, nB, ev_af
    for part, repo in (('discovery', 'Aesop'), ('test', 'Fables')):
        d = os.path.join(PARENT, repo)
        yield ('fable', part, None, notes(glob.glob(os.path.join(d, 'transcriptions', 'A', 'b*', 'Notes.txt'))),
               notes(glob.glob(os.path.join(d, 'transcriptions', 'B', 'b*', 'Notes.txt'))), events(os.path.join(d, 'Events.txt')))
    tr = os.path.join(PARENT, 'Tragedy')
    for part, rng in (('discovery', range(1, 17)), ('test', range(17, 33))):
        plays = ['P%02d' % i for i in rng]
        ev = collections.OrderedDict()
        for p in plays:
            ev.update(events(os.path.join(tr, 'plays', p, 'Events.txt')))
        yield ('tragedy', part, plays,
               notes([os.path.join(tr, 'transcriptions', 'A', p, 'Notes.txt') for p in plays]),
               notes([os.path.join(tr, 'transcriptions', 'B', p, 'Notes.txt') for p in plays]), ev)


def targets(nA, nB, story):
    out = []
    for e in sorted(set(nA.get(story, {})) & set(nB.get(story, {}))):
        a, b = nA[story][e], nB[story][e]
        if all(s == 'X' for s, _, _ in a) and all(s == 'X' for s, _, _ in b) \
                and any(m == 'Y' for _, m, _ in a) and any(m == 'Y' for _, m, _ in b):
            out.append((e, any(l for _, _, l in a + b)))
    return out


def main():
    rows, material = [], collections.OrderedDict()
    for genre, part, stories, nA, nB, ev in corpora():
        for s in (stories if stories is not None else sorted(set(nA) & set(nB) & set(ev))):
            t = targets(nA, nB, s)
            for e, link in t:
                rows.append('%s | %d | %s | %s | %s' % (s, e, genre, part, 'link' if link else '-'))
            if part == 'discovery' and t:
                if genre == 'wondertale':
                    batch = 'b1'
                elif genre == 'fable':
                    batch = 'b2'
                else:
                    batch = 'b3' if int(s[1:]) <= 8 else 'b4'
                material.setdefault(batch, []).append((s, ev[s], {e for e, _ in t}))
    with open(os.path.join(HERE, 'Targets.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Targets.txt -- xTargets.py: story | event | genre | part | link\n')
        f.write('\n'.join(rows) + '\n')
    os.makedirs(os.path.join(OUT, 'stories'), exist_ok=True)
    for b, items in material.items():
        with open(os.path.join(OUT, 'stories', '%s.txt' % b), 'w', encoding='utf-8', newline='\n') as f:
            for s, evs, marked in items:
                f.write('story: %s\n' % s)
                for n, text in evs:
                    f.write('%s %d | %s\n' % ('*' if n in marked else ' ', n, text))
                f.write('\n')
    c = collections.Counter((r.split(' | ')[2], r.split(' | ')[3]) for r in rows)
    for k in sorted(c):
        print('%-10s %-9s %4d target events' % (k[0], k[1], c[k]))
    for b, items in material.items():
        print('%s: %d stories, %d target events' % (b, len(items), sum(len(m) for _, _, m in items)))


if __name__ == '__main__':
    sys.exit(main())
