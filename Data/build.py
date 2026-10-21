#!/usr/bin/env python3
"""
build.py -- the normalized data set (DataProtocol.md, Plan.md).

  python build.py          writes Data/tables/: stories, events, functions, aliases and census
  python build.py test     runs T1 (nothing lost) and T4 (the ids hold) on the tables written

Session 1 builds the story, event and function tables; the description tables follow in session 2.
The raw files are read and never changed. Every line of every file read is either kept as a row or
dropped with its reason, and the census records both.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
OUT = os.path.join(HERE, 'tables')
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

ID = re.compile(r'^([AFPS]\d{2,3}|L\d-\d{3}|E-\d{3})(?:/(\w+))?$')
MODEL = {'A': 'Opus', 'B': 'Sonnet'}

# corpus, genre, language, repository, the event lists, the function transcriptions as (card, glob with %s for the reader)
CORPORA = [
    ('tale', 'wondertale', 'Russian', 'Afanasyev', ['Afanasyev/Events.txt'],
     [('U', 'Afanasyev/transcriptions/U/%s/*/Notes.txt'), ('C', 'Afanasyev/transcriptions/C/%s/*/Notes.txt')]),
    ('animal', 'animal tale', 'Russian', 'AnimalTales', ['AnimalTales/Events.txt'],
     [('C', 'AnimalTales/transcriptions/%s/*/Notes.txt')]),
    ('fable', 'fable', 'English', 'Aesop', ['Aesop/Events.txt'],
     [('Aesop', 'Aesop/transcriptions/%s/*/Notes.txt')]),
    ('fable', 'fable', 'English', 'Fables', ['Fables/Events.txt'],
     [('Aesop', 'Fables/transcriptions/%s/*/Notes.txt')]),
    ('tragedy', 'tragedy', 'English', 'Tragedy', ['Tragedy/plays/P[0-9][0-9]/Events.txt'],
     [('Tragedy', 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt')]),
    ('myth', 'myth', 'English', 'Apollodorus', ['Apollodorus/Apollodorus/ApollodorusEvents.txt'],
     [('Myth', 'Apollodorus/Apollodorus/transcriptions/%s/*/Notes.txt')]),
]
PROPP = 'SynthesizedProppGrammar/TaleTokenStreamsV4Utf8.txt'
CENSUS = []   # (file, lines, kept, {reason: n}, [unexplained line numbers])


def rel(path):
    return os.path.relpath(path, P).replace(os.sep, '/')


def why_dropped(line):
    s = line.strip()
    if not s:
        return 'blank'
    if s.startswith('#'):
        return 'heading or comment'
    return None


def account(path, kept, dropped, odd):
    n = sum(1 for _ in open(path, encoding='utf-8'))
    CENSUS.append((rel(path), n, kept, dict(dropped), odd))


def gid(corpus, local):
    return '%s:%s' % (corpus, local)


# ---------------------------------------------------------------- reading
def read_events(corpus, path, stories, events):
    kept, dropped, odd = 0, collections.Counter(), []
    tragedy = corpus == 'tragedy'
    myth = corpus == 'myth'
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|')]
        m = ID.match(f[0]) if len(f) >= 3 else None
        if not m or not f[1].isdigit():
            r = why_dropped(line)
            if r:
                dropped[r] += 1
            else:
                odd.append(i)
            continue
        local = m.group(1)
        if tragedy:      # P01 | n | scene | time | text
            text, extra = ' | '.join(f[4:]), 'scene %s, %s' % (f[2], f[3])
        elif myth:       # L1-001 | n | section | text
            text, extra = ' | '.join(f[3:]), 'section %s' % f[2]
        else:            # A093 | n | text
            text, extra = ' | '.join(f[2:]), ''
        events.append((gid(corpus, local), int(f[1]), text, extra, rel(path)))
        stories[gid(corpus, local)]['events'] += 1
        kept += 1
    account(path, kept, dropped, odd)


def read_functions(corpus, card, reader, path, stories, rows):
    kept, dropped, odd = 0, collections.Counter(), []
    myth = corpus == 'myth'
    batch = os.path.basename(os.path.dirname(path))
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|', 10 if not myth else 9)]
        m = ID.match(f[0]) if len(f) >= 9 else None
        if not m:
            r = why_dropped(line)
            if r:
                dropped[r] += 1
            else:
                odd.append(i)
            continue
        local, version = m.group(1), m.group(2) or ''
        if myth:   # id | move | pos | ev | section | function | performer | undergoer | unsure | note
            ev, sym, perf, und, matters, link, unsure, note = f[3], f[5], f[6], f[7], '', '', f[8], f[9] if len(f) > 9 else ''
        else:      # id | move | pos | ev | function | performer | undergoer | matters | link | unsure | note
            ev, sym, perf, und, matters, link, unsure = f[3], f[4], f[5], f[6], f[7], f[8], f[9]
            note = f[10] if len(f) > 10 else ''
        evn = re.search(r'\d+', ev)
        rows.append((gid(corpus, local), reader, MODEL[reader], card, batch, version, f[1], f[2],
                     evn.group() if evn else '', TS.base(sym) or 'X', 'Y' if TS.negative(sym) else '',
                     sym, perf, und, matters, link, unsure, note, '', rel(path)))
        stories[gid(corpus, local)]['seen'] = True
        kept += 1
    account(path, kept, dropped, odd)


COMBINATION = re.compile(r'^(<<\w+>>|<\d+>|<|>|Y)$')


def propp_tokens(text):
    """[(token, mark)]: Propp's cells as printed, each with the markup it stands in.
    overflow[...] and park[...] are cells whose place the table does not fix; [...] a bracketed cell;
    {...} a brace; <<shared>>, <N>, < > and Y are combination apparatus, kept and marked, not functions."""
    out, stack = [], []
    for t in text.split():
        while True:
            m = re.match(r'^(overflow\[|park\[|\[|\{)', t)
            if not m:
                break
            stack.append({'overflow[': 'overflow', 'park[': 'park', '[': 'bracket', '{': 'brace'}[m.group(1)])
            t = t[len(m.group(1)):]
        closes = 0
        while t and t[-1] in ']}':
            closes += 1
            t = t[:-1]
        if t:
            mark = 'combination' if COMBINATION.match(t) else '+'.join(stack)
            out.append((t, mark))
        for _ in range(closes):
            if stack:
                stack.pop()
    return out


def read_propp(stories, rows):
    """Propp's own codes, Appendix III: 'tale: 93', 'name: ...', 'move: I | cells', 'shared: | cells'"""
    path = os.path.join(P, PROPP)
    kept, dropped, odd = 0, collections.Counter(), []
    cur = None
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.strip()
        if s.startswith('tale:'):
            cur = gid('tale', 'A%03d' % int(s.split(':', 1)[1]))
            stories[cur]['propp'] = True
            kept += 1
        elif s.startswith('name:') and cur:
            stories[cur]['title'] = s.split(':', 1)[1].strip()
            kept += 1
        elif (s.startswith('move:') or s.startswith('shared:')) and cur:
            head, _, cells = s.partition('|')
            mv = head.split(':', 1)[1].strip() or 'shared'
            for pos, (t, mark) in enumerate(propp_tokens(cells), 1):
                rows.append((cur, 'Propp', '', 'Propp', '', '', mv, str(pos), '', TS.base(t) or t,
                             'Y' if TS.negative(t) else '', t, '', '', '', '', '', '', mark, rel(path)))
            kept += 1
        else:
            r = why_dropped(line)
            if r:
                dropped[r] += 1
            else:
                odd.append(i)
    account(path, kept, dropped, odd)


# ---------------------------------------------------------------- writing
def tsv(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as w:
        w.write('\t'.join(header) + '\n')
        for r in rows:
            w.write('\t'.join(str(x).replace('\t', ' ') for x in r) + '\n')


def build():
    stories = collections.defaultdict(lambda: {'events': 0, 'title': '', 'seen': False, 'propp': False})
    meta, events, funcs = {}, [], []
    for corpus, genre, lang, repo, evs, trs in CORPORA:
        for pat in evs:
            for path in sorted(glob.glob(os.path.join(P, pat))):
                read_events(corpus, path, stories, events)
        for card, pat in trs:
            for L in 'AB':
                for path in sorted(glob.glob(os.path.join(P, pat % L))):
                    read_functions(corpus, card, L, path, stories, funcs)
        for s in stories:
            if s.startswith(corpus + ':') and s not in meta:
                meta[s] = (corpus, genre, lang, repo)
    read_propp(stories, funcs)
    aliases = [(s, 'unmapped') for s in stories if s.split(':')[1].startswith('S')]
    tsv('stories.tsv', ['story', 'corpus', 'genre', 'local_id', 'source', 'language', 'title', 'events', 'propp'],
        [(s, m[0], m[1], s.split(':', 1)[1], m[3], m[2], stories[s]['title'], stories[s]['events'],
          'Y' if stories[s]['propp'] else '') for s, m in sorted(meta.items())])
    tsv('events.tsv', ['story', 'event', 'text', 'detail', 'file'], events)
    tsv('functions.tsv', ['story', 'reader', 'model', 'card', 'batch', 'version', 'move', 'position', 'event',
                          'function', 'negative', 'raw', 'performer', 'undergoer', 'matters', 'link', 'unsure',
                          'note', 'mark', 'file'], funcs)
    tsv('aliases.tsv', ['alias', 'story', 'source'], aliases)
    with open(os.path.join(OUT, 'census.txt'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('# census.txt -- every raw file read: lines, rows kept, lines dropped by reason, lines unexplained\n')
        for f, n, k, d, odd in CENSUS:
            w.write('%s\tlines %d\tkept %d\t%s\tunexplained %d%s\n' % (
                f, n, k, ', '.join('%s %d' % kv for kv in sorted(d.items())) or '-', len(odd),
                (' (lines %s)' % ', '.join(map(str, odd[:10]))) if odd else ''))
    print('stories %d, events %d, function rows %d, files %d' % (len(meta), len(events), len(funcs), len(CENSUS)))


# ---------------------------------------------------------------- the frozen tests
def read_tsv(name):
    rows = list(open(os.path.join(OUT, name), encoding='utf-8'))
    head = rows[0].rstrip('\n').split('\t')
    return [dict(zip(head, r.rstrip('\n').split('\t'))) for r in rows[1:]]


def test():
    fails = []
    # T1: for every file, kept plus dropped equals its lines, and nothing is dropped unexplained
    for line in open(os.path.join(OUT, 'census.txt'), encoding='utf-8'):
        if line.startswith('#'):
            continue
        f = line.rstrip('\n').split('\t')
        n, k = int(f[1].split()[1]), int(f[2].split()[1])
        d = sum(int(x.rsplit(' ', 1)[1]) for x in f[3].split(', ')) if f[3] != '-' else 0
        u = int(f[4].split()[1])
        if k + d + u != n or u:
            fails.append('T1 %s: lines %d, kept %d, dropped %d, unexplained %d' % (f[0], n, k, d, u))
    # T4: no id repeats, every id in every table is a story, every alias used
    st = read_tsv('stories.tsv')
    ids = [r['story'] for r in st]
    for s, c in collections.Counter(ids).items():
        if c > 1:
            fails.append('T4 repeated id %s' % s)
    known = set(ids)
    for name in ('events.tsv', 'functions.tsv'):
        bad = sorted({r['story'] for r in read_tsv(name)} - known)
        if bad:
            fails.append('T4 %s: %d ids not in stories.tsv: %s' % (name, len(bad), ', '.join(bad[:8])))
    for r in read_tsv('aliases.tsv'):
        if r['story'] in ('', 'unmapped'):
            fails.append('T4 alias %s unmapped' % r['alias'])
    print('\n'.join(fails) if fails else 'T1 and T4 PASS')
    print('%d failure(s)' % len(fails))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        build()
    elif a == ['test']:
        test()
    else:
        sys.exit(__doc__)
