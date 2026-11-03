#!/usr/bin/env python3
"""
coverage.py -- which descriptive layers each corpus has in the tables: the order of work's step 3 (ProppQueue.md, set by the
owner on 2026-11-02), confirmed before any model that needs a layer. A count, no model, no test.

  python coverage.py    write Data/Coverage.txt

For each corpus and source (stories.tsv's corpus, and the first part of its source), the stories listed, then the stories
with at least one row in each layer's table; for the readers' layers, per transcriber A and B. Rows are read by line, split on
tabs (the notes' quotes break the csv module). characters.tsv is derived and keyed without the corpus prefix; it is counted by
its own corpus column, and its build date is given, since it is not rebuilt with the other tables.
"""
import collections
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(HERE, 'tables')
OUT = os.path.join(HERE, 'Coverage.txt')
READ = ['functions', 'acts', 'free', 'significance', 'heroes', 'problems']


def rows(name):
    text = open(os.path.join(TABLES, name + '.tsv'), encoding='utf-8').read().split('\n')
    head = text[0].split('\t')
    return [dict(zip(head, l.split('\t'))) for l in text[1:] if l]


def main():
    group = {}
    for r in rows('stories'):
        group[r['story']] = (r['corpus'], r['source'].split('/')[0])
    listed = collections.Counter(group.values())
    events = collections.defaultdict(set)
    for r in rows('events'):
        events[group.get(r['story'])].add(r['story'])
    have = collections.defaultdict(set)
    for name in READ:
        for r in rows(name):
            if r['reader'] in 'AB' and r['reader']:
                have[(name, r['reader'], group.get(r['story']))].add(r['story'])
    chars = collections.defaultdict(set)
    for r in rows('characters'):
        chars[(r['reader'], r['corpus'])].add(r['story'])
    built = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(os.path.join(TABLES, 'characters.tsv'))))
    rep = ['# Coverage.txt -- coverage.py: stories with rows in each layer, transcriber A / B; a count, no model', '',
           '%-24s %6s %6s' % ('corpus (source)', 'listed', 'events') + ''.join('%15s' % n for n in READ)
           + '%15s' % 'characters']
    for g in sorted(listed):
        rep.append('%-24s %6d %6d' % ('%s (%s)' % g, listed[g], len(events[g]))
                   + ''.join('%15s' % ('%d / %d' % (len(have[(n, 'A', g)]), len(have[(n, 'B', g)]))) for n in READ)
                   + '%15s' % ('%d / %d' % (len(chars[('A', g[0])]), len(chars[('B', g[0])]))))
    rep += ['', '# characters.tsv was last built %s; its column counts a whole corpus, not a source.' % built,
            '# characters.tsv corpora: %s' % ', '.join(sorted({c for _, c in chars}))]
    text = '\n'.join(rep) + '\n'
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
