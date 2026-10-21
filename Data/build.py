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


# ---------------------------------------------------------------- the descriptions (session 2)
AR = 'ActsRoles'
# study, the act files (glob with %s for the reader), the prompt prefix naming each batch's stories
ACT_SOURCES = [('twolayer', ['ActsRoles/tale/acts/%s/*/Notes.txt', 'ActsRoles/fable/acts/%s/*/Notes.txt',
                             'ActsRoles/tragedy/acts/%s/*/Notes.txt'], 'acts'),
               ('problems', ['ActsRoles/problems/acts/%s/*/Notes.txt'], 'pacts'),
               ('animal', ['ActsRoles/animal/acts/%s/*/Notes.txt'], 'aacts')]
SIG_SOURCES = [('significance', 'ActsRoles/sig'), ('problems', 'ActsRoles/problems/sig'),
               ('animal', 'ActsRoles/animal/sig')]
FREE_SOURCES = [('free', 'ActsRoles/free/%s/*/Notes.txt'), ('animal', 'ActsRoles/animal/free/%s/*/Notes.txt')]
HERO_LISTS = [('Afanasyev/Heroes.txt', 'tale'), ('AnimalTales/Heroes.txt', 'animal'), ('Aesop/Heroes.txt', 'fable'),
              ('Fables/Heroes.txt', 'fable'), ('Tragedy/plays/P[0-9][0-9]/Hero.txt', 'tragedy')]
LOCAL = {}      # local id -> global id, from the story table
ALIASES = {}    # (file, alias) -> (story, source)
EID = re.compile(r'^(e\d{4})$')


def resolve(local, corpus=None):
    if corpus:
        return gid(corpus, local)
    return LOCAL.get(local, 'unknown:' + local)


def batch_plays(prefix, L, batch):
    """the plays a tragedy batch was given, in the order its prompt names them"""
    path = os.path.join(P, AR, 'prompts', '%s-%s-%s.txt' % (prefix, L, batch))
    out = []
    if os.path.exists(path):
        for m in re.finditer(r'plays/(P\d{2})', open(path, encoding='utf-8').read()):
            if m.group(1) not in out:
                out.append(m.group(1))
    return out


def speech_numbers(play):
    for base in ('tragedy/plays', 'problems/tragedy/plays', 'held/tragedy/plays'):
        f = os.path.join(P, AR, base, play, 'Events.txt')
        if os.path.exists(f):
            out = {}
            for line in open(f, encoding='utf-8'):
                x = [y.strip() for y in line.split('|')]
                if len(x) >= 3 and x[1].isdigit():
                    out[int(x[1])] = x[2]
            return out
    return {}


class Recover:
    """A departure logged in TwoLayer/KeeperLog.md and Problems/KeeperLog.md: three tragedy batches of describer
    B wrote each event's speech number (S001...) where the play belongs. The play is recovered from the batch's
    two plays, in the order its prompt names them, events restarting at 1 for the second, and every line's speech
    number is checked against that play's event list; a line that does not match is kept, on the play its place
    gives, and flagged."""
    def __init__(self, path, prefix, L):
        self.path = path
        self.plays = batch_plays(prefix, L, os.path.basename(os.path.dirname(path)))
        self.spk = {pl: speech_numbers(pl) for pl in self.plays}
        self.i, self.prev = 0, 0

    def __call__(self, alias, ev):
        if ev < self.prev and ev == 1 and self.i == 0:
            self.i = 1
        self.prev = ev
        pl = self.plays[self.i]
        ALIASES[(rel(self.path), alias)] = (gid('tragedy', pl), 'speech number, recovered by batch order')
        ok = self.spk[pl].get(ev) == alias
        return gid('tragedy', pl), '' if ok else 'speech %s does not match %s event %d' % (alias, pl, ev)


def data_lines(path, nfields):
    """yield (fields, id match) for each data line, and account every other line"""
    kept, dropped, odd = 0, collections.Counter(), []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|', nfields - 1)]
        m = ID.match(f[0]) if len(f) >= min(nfields, 2) else None
        if m:
            kept += 1
            yield f + [''] * (nfields - len(f)), m
        else:
            r = why_dropped(line)
            if r:
                dropped[r] += 1
            else:
                odd.append(i)
    account(path, kept, dropped, odd)


def event_of(field):
    m = re.search(r'\d+', field)
    return int(m.group()) if m else 0


def read_acts(rows):
    for study, pats, prefix in ACT_SOURCES:
        for pat in pats:
            for L in 'AB':
                for path in sorted(glob.glob(os.path.join(P, pat % L))):
                    batch = os.path.basename(os.path.dirname(path))
                    rec, order = None, collections.Counter()
                    for f, m in data_lines(path, 10):
                        ev, flag = event_of(f[1]), ''
                        if m.group(1).startswith('S'):
                            rec = rec or Recover(path, prefix, L)
                            story, flag = rec(m.group(1), ev)
                        else:
                            story = resolve(m.group(1))
                        order[(story, ev)] += 1
                        rows.append((story, L, MODEL[L], study, batch, m.group(2) or '', ev, order[(story, ev)],
                                     f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], flag, rel(path)))


def read_free(rows):
    for study, pat in FREE_SOURCES:
        for L in 'AB':
            for path in sorted(glob.glob(os.path.join(P, pat % L))):
                batch = os.path.basename(os.path.dirname(path))
                order = collections.Counter()
                for f, m in data_lines(path, 9):
                    ev, story = event_of(f[1]), resolve(m.group(1))
                    order[(story, ev)] += 1
                    rows.append((story, L, MODEL[L], study, batch, m.group(2) or '', ev, order[(story, ev)],
                                 f[2], f[3], f[4], f[5], f[6], f[7], f[8], rel(path)))


def read_sig_input(path):
    """{entry: (story, event, act, performer, undergoer, relation)}, accounting the input file's lines"""
    out, story, ev = {}, None, 0
    kept, dropped, odd = 0, collections.Counter(), []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.strip()
        m = re.match(r'^story:\s*([AFP]\d{2,3})', s)
        e = re.match(r'^ev\s+(\d+)\s*\|', s)
        a = re.match(r'^(e\d{4})\s*\|', s)
        if m:
            story = resolve(m.group(1))
        elif e:
            ev = int(e.group(1))
        elif a and story:
            f = [x.strip() for x in s.split('|')] + [''] * 6
            out[a.group(1)] = (story, ev, f[1], f[2], f[3], f[4])
        else:
            r = why_dropped(line)
            if r:
                dropped[r] += 1
            else:
                odd.append(i)
            continue
        kept += 1
    account(path, kept, dropped, odd)
    return out


def read_sig(sigrows, probrows):
    for study, base in SIG_SOURCES:
        for L in 'AB':
            for path in sorted(glob.glob(os.path.join(P, base, L, '*', 'Significance.txt'))):
                batch = os.path.basename(os.path.dirname(path))
                inp = read_sig_input(os.path.join(P, base, 'input', '%s-%s.txt' % (L, batch)))
                kept, dropped, odd = 0, collections.Counter(), []
                for i, line in enumerate(open(path, encoding='utf-8'), 1):
                    f = [x.strip() for x in line.rstrip('\n').split('|', 8)]
                    pm = ID.match(f[0])
                    if EID.match(f[0]) and len(f) >= 8:
                        f += [''] * (9 - len(f))
                        src = inp.get(f[0], ('unknown:' + f[0], 0, '', '', '', ''))
                        sigrows.append((src[0], L, MODEL[L], study, batch, f[0], src[1], src[2], src[3], src[4],
                                        src[5], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], rel(path)))
                    elif pm and len(f) >= 4 and f[1].lower() == 'problem':
                        probrows.append((resolve(pm.group(1)), L, MODEL[L], study, batch, f[2], ' | '.join(f[3:]),
                                         rel(path)))
                    else:
                        r = why_dropped(line)
                        if r:
                            dropped[r] += 1
                        else:
                            odd.append(i)
                        continue
                    kept += 1
                account(path, kept, dropped, odd)


def read_heroes(rows):
    for L in 'AB':        # the two hero readers
        for path in sorted(glob.glob(os.path.join(P, AR, 'heroes', 'answers', L, '*', 'Heroes.txt'))):
            for f, m in data_lines(path, 4):
                rows.append((resolve(m.group(1)), L, MODEL[L], 'heroes', f[1], f[2], f[3], rel(path)))
    for pat, corpus in HERO_LISTS:      # the event listers' heroes
        for path in sorted(glob.glob(os.path.join(P, pat))):
            for f, m in data_lines(path, 3):
                hero = re.sub(r'^hero:\s*', '', f[1])
                rows.append((resolve(m.group(1), corpus), 'lister', '', 'events', hero, '',
                             f[2].replace('moral: -', '').strip(), rel(path)))
    path = os.path.join(ROOT, 'Heroes', 'JudgedHeroes.txt')     # the heroes the readers agree on, as judged
    for f, m in data_lines(path, 3):
        rows.append((resolve(m.group(1)), 'judged', '', 'heroes', f[1], '', f[2], rel(path)))


def build_descriptions(meta):
    for s in sorted(meta):
        LOCAL.setdefault(s.split(':', 1)[1], s)
    acts, free, sig, probs, heroes = [], [], [], [], []
    read_acts(acts)
    read_free(free)
    read_sig(sig, probs)
    read_heroes(heroes)
    tsv('acts.tsv', ['story', 'reader', 'model', 'study', 'batch', 'version', 'event', 'entry', 'act', 'performer',
                     'undergoer', 'relation', 'matters', 'link', 'unsure', 'note', 'id_flag', 'file'], acts)
    tsv('free.tsv', ['story', 'reader', 'model', 'study', 'batch', 'version', 'event', 'entry', 'verb', 'phrase',
                     'performer', 'undergoer', 'matters', 'unsure', 'note', 'file'], free)
    tsv('significance.tsv', ['story', 'reader', 'model', 'study', 'batch', 'entry', 'event', 'act', 'performer',
                             'undergoer', 'relation', 'part', 'value', 'place', 'problem', 'link', 'target',
                             'unsure', 'note', 'file'], sig)
    tsv('problems.tsv', ['story', 'reader', 'model', 'study', 'batch', 'problem', 'text', 'file'], probs)
    tsv('heroes.tsv', ['story', 'reader', 'model', 'study', 'hero', 'confidence', 'basis', 'file'], heroes)
    print('acts %d, free %d, significance %d, problems %d, heroes %d'
          % (len(acts), len(free), len(sig), len(probs), len(heroes)))
    return [(a, st, '%s; %s' % (src, f)) for (f, a), (st, src) in sorted(ALIASES.items())]


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
    # the fables' whole collection, from which both fable repositories drew: every fable is a story, listed or not
    path = os.path.join(P, 'Aesop', 'Fables.txt')
    for f, m in data_lines(path, 3):
        s = gid('fable', m.group(1))
        stories[s]['title'] = f[1]
        meta.setdefault(s, ('fable', 'fable', 'English', 'Aesop/Fables.txt'))
    aliases = build_descriptions(meta)
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


# T2: each stage's form check, rerun and kept in Data/forms/, against the tables. (form file, table, study,
# the count the line reports: 'entries' or 'described'). Problem lines are checked against problems.tsv.
FORMS = [('twolayer.txt', 'acts.tsv', 'twolayer', 'entries'), ('pacts.txt', 'acts.tsv', 'problems', 'entries'),
         ('aacts.txt', 'acts.tsv', 'animal', 'entries'), ('free.txt', 'free.tsv', 'free', 'entries'),
         ('cand.txt', 'free.tsv', 'free', 'entries'), ('afree.txt', 'free.tsv', 'animal', 'entries'),
         ('sig.txt', 'significance.tsv', 'significance', 'described'),
         ('psig.txt', 'significance.tsv', 'problems', 'described'),
         ('asig.txt', 'significance.tsv', 'animal', 'described')]
# Recorded where a form check cannot count what was merged: two batches whose every line carries a speech number,
# which the two-layer form check reads as nothing (TwoLayer/KeeperLog.md, acts-2: 311 lines in g1, 164 in g3).
RECORDED = {('acts.tsv', 'twolayer', 'B', 'g1'): 311, ('acts.tsv', 'twolayer', 'B', 'g3'): 164}


def test2():
    fails = []
    tables = {}
    for _, t, _, _ in FORMS:
        if t not in tables:
            tables[t] = collections.Counter()
            for r in read_tsv(t):
                if not r.get('id_flag'):
                    tables[t][(r['study'], r['reader'], r['batch'])] += 1
    probs = collections.Counter((r['study'], r['reader'], r['batch']) for r in read_tsv('problems.tsv'))
    for name, t, study, what in FORMS:
        for line in open(os.path.join(HERE, 'forms', name), encoding='utf-8'):
            m = re.match(r'^(?:\w+ )?([AB])[ \\]+(\w+):?\s.*?\b%s\s+(\d+)' % what, line)
            if not m:
                continue
            L, b, n = m.group(1), m.group(2), int(m.group(3))
            n = RECORDED.get((t, study, L, b), n)
            got = tables[t][(study, L, b)]
            if got != n:
                fails.append('T2 %s %s %s %s: form check %d, table %d' % (name, study, L, b, n, got))
            pm = re.search(r'problem lines\s+(\d+)', line)
            if pm and probs[(study, L, b)] != int(pm.group(1)):
                fails.append('T2 %s %s %s %s problem lines: form check %s, table %d'
                             % (name, study, L, b, pm.group(1), probs[(study, L, b)]))
    return fails


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
    for name in ('events.tsv', 'functions.tsv', 'acts.tsv', 'free.tsv', 'significance.tsv', 'problems.tsv',
                 'heroes.tsv', 'aliases.tsv'):
        bad = sorted({r['story'] for r in read_tsv(name)} - known)
        if bad:
            fails.append('T4 %s: %d ids not in stories.tsv: %s' % (name, len(bad), ', '.join(bad[:8])))
    for r in read_tsv('aliases.tsv'):
        if r['story'] in ('', 'unmapped'):
            fails.append('T4 alias %s unmapped' % r['alias'])
    fails += test2()
    print('\n'.join(fails) if fails else 'T1, T2 and T4 PASS')
    print('%d failure(s)' % len(fails))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        build()
    elif a == ['test']:
        test()
    else:
        sys.exit(__doc__)
