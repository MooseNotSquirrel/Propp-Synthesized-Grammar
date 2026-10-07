#!/usr/bin/env python3
"""
xPrepare.py -- the X study's material for the grouping and assignment stages
(XStudyProtocol.md), from the labels.

  python xPrepare.py   writes, in Story Language/XStudy:
                       group/Labels.txt  every label of both labelers, one per line, in a
                                         random order (seed 46), with no story, genre or event
                       assign/b1..b4.txt the stories with their marked events, each marked event
                                         followed by its two labels, in the order A, B
"""
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
X = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'XStudy')
BATCHES = ('b1', 'b2', 'b3', 'b4')


def labels(L, b):
    out = {}
    for l in open(os.path.join(X, 'labels', L, b, 'Labels.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|', 2)]
        if len(f) == 3 and f[1].isdigit():
            out[(f[0], int(f[1]))] = f[2]
    return out


def main():
    pool = []
    for b in BATCHES:
        la, lb = labels('A', b), labels('B', b)
        pool += list(la.values()) + list(lb.values())
        os.makedirs(os.path.join(X, 'assign'), exist_ok=True)
        with open(os.path.join(X, 'assign', '%s.txt' % b), 'w', encoding='utf-8', newline='\n') as out:
            story = None
            for line in open(os.path.join(X, 'stories', '%s.txt' % b), encoding='utf-8'):
                m = re.match(r'^story: (\S+)', line)
                if m:
                    story = m.group(1)
                out.write(line)
                m = re.match(r'^\* (\d+) \|', line)
                if m:
                    key = (story, int(m.group(1)))
                    out.write('      description 1: %s\n' % la[key])
                    out.write('      description 2: %s\n' % lb[key])
    random.Random(46).shuffle(pool)
    os.makedirs(os.path.join(X, 'group'), exist_ok=True)
    with open(os.path.join(X, 'group', 'Labels.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(pool) + '\n')
    print('%d labels pooled; assign material for %s' % (len(pool), ', '.join(BATCHES)))


if __name__ == '__main__':
    sys.exit(main())
