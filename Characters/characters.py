#!/usr/bin/env python3
"""
characters.py -- the character-set layer (Data/CharacterProtocol.md, frozen 2026-10-26): one row per character,
per story, per reader, built from the normalized tables.

  python characters.py build      write Data/tables/characters.tsv
  python characters.py c1         test C1: every function name maps to exactly one character row
  python characters.py c2         test C2: the table's spheres equal Spheres/explore.py's, SpheresExplore.txt byte for byte
  python characters.py c3         test C3: the kind rule on WordNet's own words (the sample written first, to C3Sample.txt)
  python characters.py c6         test C6: two builds byte-identical
  python characters.py dry        counts only: stories, characters, characters with a sphere, names resolved by kind

This first part builds the table from the function layer, in every corpus. The act profile (the acts joined by
event, test C4) and the bottom-up grouping (test C5) are not built yet; their columns are not in the table, and
C1 covers the function layer only until they are.
"""
import collections
import io
import os
import random
import re
import sys
import tempfile
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Data'))
import tables as DT  # noqa: E402
import parityReports as PR  # noqa: E402

SX = PR.SX
TS = PR.TS
WORDNET = r'C:/Users/Steve1/nltk_wordnet'
# the function layer of each corpus, as Spheres/explore.py reads it (the wondertales on card U), with the animal tales
PATS = collections.OrderedDict([('tale', ['Afanasyev/transcriptions/U/%s/b*/Notes.txt']),
                                ('animal', ['AnimalTales/transcriptions/%s/b*/Notes.txt']),
                                ('fable', ['Aesop/transcriptions/%s/b*/Notes.txt', 'Fables/transcriptions/%s/b*/Notes.txt']),
                                ('tragedy', ['Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt']),
                                ('myth', ['Apollodorus/Apollodorus/transcriptions/%s/b*/Notes.txt'])])
COLUMNS = ['story', 'reader', 'corpus', 'character', 'names', 'head', 'kind', 'kind_by', 'group', 'spheres', 'performs', 'undergoes']
CUT = re.compile(r"\b(?:of|with|from|in|at|on|to|for)\b|,|;|\(|/|\band\b|\bor\b")
HEAD_STOP = SX.STOP | {'two', 'three', 'four', 'other', 'its', 'my', 'your', 'our', 'own'}
_WN = []


def wordnet():
    if not _WN:
        import nltk
        nltk.data.path.insert(0, WORDNET)
        from nltk.corpus import wordnet as wn
        _WN.append(wn)
    return _WN[0]


# ---------------------------------------------------------------- the kind rule (protocol section 3)
def head(name):
    """the head noun: the last word, after possessives and phrases with of, with, from and the like are cut away"""
    n = name.lower().replace('\u2019', "'")
    n = CUT.split(n)[0]
    if "'s " in n + ' ':
        n = (n + ' ').split("'s ")[-1] or n
    ws = [w for w in re.findall(r"[a-z]+(?:-[a-z]+)*", n) if w not in HEAD_STOP]
    return ws[-1] if ws else ''


def sense(h):
    wn = wordnet()
    if not h:
        return None
    for w in (h, h.replace('-', '_')):
        ss = wn.synsets(w, pos='n')
        if ss:
            return ss[0]
    base = wn.morphy(h, 'n')
    ss = wn.synsets(base, pos='n') if base else []
    return ss[0] if ss else None


def kind_of(syn):
    if syn is None:
        return 'unknown'
    up = {x.name() for path in syn.hypernym_paths() for x in path}
    if 'deity.n.01' in up:
        return 'deity'
    if up & {'spiritual_being.n.01', 'imaginary_being.n.01'}:
        return 'supernatural'
    if syn.lexname() == 'noun.person':
        return 'person'
    if syn.lexname() == 'noun.animal':
        return 'animal'
    return 'object'


def kind(name):
    return kind_of(sense(head(name)))


def is_group(name, h):
    wn = wordnet()
    base = wn.morphy(h, 'n') if h else None
    return bool(h) and (base not in (None, h) or bool(re.search(r'\band\b|&', name.lower())))


# ---------------------------------------------------------------- the table
def entries(L, g):
    """{story: [(function, performer key, undergoer key, performer name, undergoer name)]}, the first reading of
    each story, as Spheres/explore.py's read() takes it"""
    st = collections.OrderedDict()
    for r in DT.files('functions', PATS[g], L):
        base = DT.local(r['story'])
        if not re.match(r'^([PFA]\d{2}|L\d-\d{3})', base):
            continue
        st.setdefault(base, collections.OrderedDict()).setdefault(r['version'] or '1', []).append(
            (TS.base(r['raw']), SX.key(r['performer']), SX.key(r['undergoer']), r['performer'].strip(), r['undergoer'].strip()))
    return {s: vs[sorted(vs, key=lambda v: (len(v), v))[0]] for s, vs in st.items()}


def characters(L, g, s, ents):
    """the story's characters: names joined as Spheres/explore.py joins them, each with its names, spheres and counts"""
    canon = SX.merge([(fn, p, u) for fn, p, u, _, _ in ents])
    ch = collections.OrderedDict()

    def add(k, raw):
        c = canon.get(k, k)
        d = ch.setdefault(c, {'names': collections.Counter(), 'spheres': set(), 'performs': 0, 'undergoes': 0})
        d['names'][raw] += 1
        return d
    for fn, p, u, pr, ur in ents:
        if p:
            d = add(p, pr)
            d['performs'] += 1
            for name, fs in SX.SPHERES.items():
                if fn in fs:
                    d['spheres'].add(name)
        if u:
            add(u, ur)['undergoes'] += 1
    rows = []
    for c, d in ch.items():
        names = sorted(d['names'], key=lambda n: (-d['names'][n], n))
        # the kind is read from the character's longest name, the one the others joined
        full = max(names, key=lambda n: (len(SX.key(n)), d['names'][n], n))
        h = head(full)
        k = kind(full)
        rows.append([s, L, g, ' '.join(c), ' ; '.join(names), h, k, 'unknown' if k == 'unknown' else 'wordnet',
                     'Y' if is_group(full, h) else '', ' + '.join(n for n in SX.SPHERES if n in d['spheres']),
                     str(d['performs']), str(d['undergoes'])])
    return rows


def table():
    out = []
    for g in PATS:
        for L in 'AB':
            for s, ents in entries(L, g).items():
                out += characters(L, g, s, ents)
    text = '\t'.join(COLUMNS) + '\n' + ''.join('\t'.join(x.replace('\t', ' ') for x in r) + '\n' for r in out)
    return text, out


def build():
    text, out = table()
    open(os.path.join(DT.TABLES, 'characters.tsv'), 'w', encoding='utf-8', newline='\n').write(text)
    print('characters.tsv: %d rows' % len(out))


# ---------------------------------------------------------------- the tests
def c1():
    """every non-empty function performer and undergoer of the readings the table takes maps to exactly one row"""
    _, out = table()
    have = collections.Counter((r[0], r[1], r[3]) for r in out)
    dup = [k for k, n in have.items() if n > 1]
    lost = 0
    for g in PATS:
        for L in 'AB':
            for s, ents in entries(L, g).items():
                canon = SX.merge([(fn, p, u) for fn, p, u, _, _ in ents])
                for _, p, u, _, _ in ents:
                    for k in (p, u):
                        if k and have.get((s, L, ' '.join(canon.get(k, k)))) != 1:
                            lost += 1
    ok = not dup and not lost
    print('C1 %d rows; names without exactly one row %d; character rows twice %d: %s' % (len(out), lost, len(dup), 'PASS' if ok else 'FAIL'))
    return ok


def c2():
    """the four corpora of Spheres/explore.py: the table's spheres equal explore's for every character, and explore's
    report rerun on the tables' entries equals the committed SpheresExplore.txt byte for byte"""
    _, out = table()
    mine = {(r[0], r[1], r[3]): set(r[9].split(' + ')) - {''} for r in out}
    diff = n = 0
    for L in 'AB':
        raw = SX.read(L)
        for g in SX.CORPORA:
            for s, ents in raw[g].items():
                canon = SX.merge(ents)
                sph = collections.defaultdict(set)
                for fn, p, u in ents:
                    if p:
                        for name, fs in SX.SPHERES.items():
                            if fn in fs:
                                sph[canon.get(p, p)].add(name)
                for c, v in sph.items():
                    n += 1
                    diff += mine.get((s, L, ' '.join(c))) != v
    saved_read, saved_here = SX.read, SX.HERE
    tmp = tempfile.mkdtemp()
    try:
        SX.read = lambda L: {g: {s: [e[:3] for e in es] for s, es in entries(L, g).items()} for g in SX.CORPORA}
        SX.HERE = tmp
        del SX.OUT[:]
        with contextlib.redirect_stdout(io.StringIO()):
            SX.main()
        got = open(os.path.join(tmp, 'SpheresExplore.txt'), 'rb').read()
    finally:
        SX.read, SX.HERE = saved_read, saved_here
        del SX.OUT[:]
    want = open(os.path.join(ROOT, 'Spheres', 'SpheresExplore.txt'), 'rb').read()
    ok = diff == 0 and got == want
    print('C2 characters in a sphere %d, spheres differing %d; SpheresExplore.txt from the tables %s: %s'
          % (n, diff, 'IDENTICAL' if got == want else 'DIFFERS', 'PASS' if ok else 'FAIL'))
    return ok


def c3_sample():
    """the seeded sample: 100 person nouns, 100 animal, every single-word deity, 50 artifact and 50 plant"""
    wn = wordnet()
    rnd = random.Random(20261026)
    under = lambda syn, names: bool({x.name() for path in syn.hypernym_paths() for x in path} & names)
    spirit = {'spiritual_being.n.01', 'imaginary_being.n.01'}

    def drawn(lexname, k):
        cands = sorted({l.name() for syn in wn.all_synsets('n') if syn.lexname() == lexname for l in syn.lemmas()
                        if re.fullmatch(r'[a-z]+', l.name())})
        return rnd.sample(cands, k)
    deities = sorted({l.name().lower() for syn in wn.synset('deity.n.01').closure(lambda x: x.hyponyms() + x.instance_hyponyms())
                      for l in syn.lemmas() if re.fullmatch(r'[A-Za-z]+', l.name())})
    sample = [(w, 'person') for w in drawn('noun.person', 100)] + [(w, 'animal') for w in drawn('noun.animal', 100)]
    sample += [(w, 'deity') for w in deities]
    sample += [(w, 'object') for w in drawn('noun.artifact', 50)] + [(w, 'object') for w in drawn('noun.plant', 50)]
    rows = []
    for w, cls in sample:
        first = wn.synsets(w, pos='n')[0]
        if cls == 'deity':
            fits = under(first, {'deity.n.01'})
        elif cls == 'object':
            fits = first.lexname() in ('noun.artifact', 'noun.plant') and not under(first, spirit)
        else:
            fits = first.lexname() == 'noun.' + cls and not under(first, spirit | {'deity.n.01'})
        rows.append((w, cls, 'kept' if fits else 'left out: first sense %s %s' % (first.name(), first.lexname())))
    return rows


def c3():
    rows = c3_sample()
    path = os.path.join(HERE, 'C3Sample.txt')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# C3Sample.txt -- characters.py c3: the seeded sample (seed 20261026), written before the rule runs\n')
        f.writelines('%s\t%s\t%s\n' % r for r in rows)
    kept = [(w, c) for w, c, why in rows if why == 'kept']
    wrong = [(w, c, kind(w)) for w, c in kept if kind(w) != c]
    by = collections.Counter(c for _, c in kept)
    print('C3 sample %d, left out %d (first sense of another class), kept %s; wrong %d: %s'
          % (len(rows), len(rows) - len(kept), dict(by), len(wrong), 'PASS' if not wrong else 'FAIL'))
    for w in wrong[:20]:
        print('   wrong: %s drawn %s, rule gives %s' % w)
    return not wrong


def c6():
    a, _ = table()
    DT._CACHE.clear()
    b, _ = table()
    ok = a.encode('utf-8') == b.encode('utf-8')
    print('C6 two builds %s: %s' % ('byte-identical' if ok else 'DIFFER', 'PASS' if ok else 'FAIL'))
    return ok


def dry():
    """counts only: no kind by role, no grouping, no ranking"""
    _, out = table()
    c = collections.defaultdict(lambda: [set(), 0, 0, 0])
    for r in out:
        x = c[(r[2], r[1])]
        x[0].add(r[0])
        x[1] += 1
        x[2] += bool(r[9])
        x[3] += r[6] != 'unknown'
    for (g, L), (st, n, sp, kn) in sorted(c.items(), key=lambda kv: (list(PATS).index(kv[0][0]), kv[0][1])):
        print('%-8s %s stories %3d, characters %5d, with a sphere %5d, kind resolved %3.0f%%' % (g, L, len(st), n, sp, 100.0 * kn / max(1, n)))


if __name__ == '__main__':
    cmds = {'build': build, 'c1': c1, 'c2': c2, 'c3': c3, 'c6': c6, 'dry': dry}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
