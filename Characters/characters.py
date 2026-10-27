#!/usr/bin/env python3
"""
characters.py -- the character-set layer (Data/CharacterProtocol.md, frozen 2026-10-26): one row per character,
per story, per reader, built from the normalized tables.

  python characters.py build      write Data/tables/characters.tsv and unjoined.tsv
  python characters.py c1         test C1: every name maps to exactly one character row, or is counted as unjoined
  python characters.py c2         test C2: the table's spheres equal Spheres/explore.py's, SpheresExplore.txt byte for byte
  python characters.py c3         test C3: the kind rule on WordNet's own words (the sample written first, to C3Sample.txt)
  python characters.py c4         test C4: the acts joined by event agree with the name join, where both are English
  python characters.py c5         test C5: the grouping recovers planted roles, and shuffled profiles do not match the spheres
  python characters.py c6         test C6: two builds byte-identical
  python characters.py c7         test C7: the split of several-name fields (Characters/SplitRule.md)
  python characters.py dry        counts only: stories, characters, characters with a sphere, names resolved by kind

The characters are the function layer's, in every corpus. The act and free-verb names are joined to them, by name
where English and by event where Russian; a name that joins none is counted as unjoined, not made a character.
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
COLUMNS = ['story', 'reader', 'corpus', 'character', 'names', 'head', 'kind', 'kind_by', 'group', 'spheres', 'performs',
           'undergoes', 'layers', 'acts', 'relations']
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


def rule_class(h, group):
    """Characters/KindRule.md, adopted 2026-10-27: named, group, collective or common; the rule's kind stands only
    for common, and only while the second name stage's controls pass"""
    s = sense(h)
    if s and (s.instance_hypernyms() or s.lemmas()[0].name()[0].isupper()):
        return 'named'
    if group:
        return 'group'
    if s and s.lexname() == 'noun.group':
        return 'collective'
    return 'common'


def capitalized(names, h):
    """Characters/SenseRule.md, adopted 2026-10-27: the head is written with a capital in some recorded name (the
    table's names field, ' ; ' between names), a possessive 's set aside"""
    for n in names.split(' ; '):
        for w in re.findall(r"[A-Za-z][\w'-]*", n):
            b = w.lower()
            b = b[:-2] if b.endswith("'s") else b
            if h and b == h and w[0].isupper():
                return True
    return False


# ---------------------------------------------------------------- the table
def entries(L, g):
    """{story: [(function, performer key, undergoer key, performer name, undergoer name, event)]}, the first reading
    of each story, its several-name fields split, as Spheres/explore.py's read() takes it"""
    st = collections.OrderedDict()
    for r in DT.files('functions', PATS[g], L):
        base = DT.local(r['story'])
        if not re.match(r'^([PFA]\d{2}|L\d-\d{3})', base):
            continue
        st.setdefault(base, collections.OrderedDict()).setdefault(r['version'] or '1', []).append(
            (TS.base(r['raw']), r['performer'].strip(), r['undergoer'].strip(), r['event']))
    return {s: [e + (ev,) for fn, pr, ur, ev in SX.first_reading(vs) for e in SX.expand(fn, pr, ur)] for s, vs in st.items()}


def layer_rows(name):
    """{(global story, reader): [rows]} of the acts or free-verb table, one study each, the first present"""
    order = ACT_STUDIES if name == 'acts' else ['free', 'animal']
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in DT.rows(name):
        if not r.get('id_flag'):
            by[(r['story'], r['reader'])][r['study']].append(r)
    return {k: v[min(v, key=lambda x: order.index(x) if x in order else len(order))] for k, v in by.items()}


def characters(L, g, s, ents, acts=(), free=()):
    """the story's characters: names joined as Spheres/explore.py joins them, each with its names, spheres and
    counts; the act and free-verb layers' names joined to them by name where English and by event where Russian
    (CharacterProtocol.md, decision 2). A name that joins none is set apart as unjoined, counted and not made a
    character (the owner's decision of 2026-10-26); returns (rows, unjoined)"""
    canon = SX.merge([e[:3] for e in ents])
    names = {k for e in ents for k in e[1:3] if k}
    links = {a: c for a, (c, _) in event_join(g, L, s, ents, acts).items()}
    ch = collections.OrderedDict()

    def new(c):
        return ch.setdefault(c, {'names': collections.Counter(), 'spheres': set(), 'performs': 0, 'undergoes': 0,
                                 'layers': set(), 'acts': collections.Counter(), 'relations': collections.Counter()})

    def add(k, raw):
        d = new(canon.get(k, k))
        d['names'][raw] += 1
        d['layers'].add('functions')
        return d

    def who(raw):
        k = SX.key(raw)
        if not k:
            return None
        if CYR.search(raw):
            return links.get(k)
        return name_join(k, names, canon)
    for fn, p, u, pr, ur, _ in ents:
        if p:
            d = add(p, pr)
            d['performs'] += 1
            for name, fs in SX.SPHERES.items():
                if fn in fs:
                    d['spheres'].add(name)
        if u:
            add(u, ur)['undergoes'] += 1
    unjoined = collections.Counter()
    for layer, rs in (('acts', acts), ('free', free)):
        for r in rs:
            for side, field in (('p', 'performer'), ('u', 'undergoer')):
              for part in SX.split_field(r[field]):
                c = who(part)
                if c is None:
                    unjoined[(layer, side, part)] += 1
                    continue
                d = new(c)
                d['layers'].add(layer)
                if layer == 'acts':
                    d['acts']['%s:%s' % (side, r['act'].lower())] += 1
                    if side == 'p':
                        d['relations'][r['relation'].lower()] += 1
    rows = []
    for c, d in ch.items():
        nm = sorted(d['names'], key=lambda n: (-d['names'][n], n))
        # the kind is read from the character's longest name, the one the others joined
        full = max(nm, key=lambda n: (len(SX.key(n)), d['names'][n], n))
        h = head(full)
        k, by = kind(full), 'wordnet'
        if k == 'unknown' or (g, s, ' '.join(c)) in second_stage():
            # the kind both readers of the name stage gave (Data/NamesProtocol.md), where they agree; for a character
            # of the second stage (KindRule.md), in place of the rule's
            k = reader_kinds().get((g, s, ' '.join(c)), 'unknown')
            by = 'readers' if k != 'unknown' else 'unknown'
        rows.append([s, L, g, ' '.join(c), ' ; '.join(nm), h, k, by,
                     'Y' if is_group(full, h) else '', ' + '.join(n for n in SX.SPHERES if n in d['spheres']),
                     str(d['performs']), str(d['undergoes']), ' '.join(x for x in ('functions', 'acts', 'free') if x in d['layers']),
                     '; '.join('%s %d' % kv for kv in sorted(d['acts'].items())),
                     '; '.join('%s %d' % kv for kv in sorted(d['relations'].items()))])
    return rows, [[s, L, g, layer, side, name, str(n)] for (layer, side, name), n in sorted(unjoined.items())]


def table():
    out, un = [], []
    A, Fr = layer_rows('acts'), layer_rows('free')
    for g in PATS:
        for L in 'AB':
            for s, ents in entries(L, g).items():
                rows, u = characters(L, g, s, ents, A.get((g + ':' + s, L), []), Fr.get((g + ':' + s, L), []))
                out += rows
                un += u
    UNJOINED[:] = un
    text = '\t'.join(COLUMNS) + '\n' + ''.join('\t'.join(x.replace('\t', ' ') for x in r) + '\n' for r in out)
    return text, out


def build():
    text, out = table()
    open(os.path.join(DT.TABLES, 'characters.tsv'), 'w', encoding='utf-8', newline='\n').write(text)
    cols = ['story', 'reader', 'corpus', 'layer', 'side', 'name', 'count']
    open(os.path.join(DT.TABLES, 'unjoined.tsv'), 'w', encoding='utf-8', newline='\n').write(
        '\t'.join(cols) + '\n' + ''.join('\t'.join(x.replace('\t', ' ') for x in r) + '\n' for r in UNJOINED))
    print('characters.tsv: %d rows; unjoined.tsv: %d names, %d mentions'
          % (len(out), len(UNJOINED), sum(int(r[6]) for r in UNJOINED)))


# ---------------------------------------------------------------- the tests
def c1():
    """every non-empty performer and undergoer of the function, act and free-verb readings the table takes maps to
    exactly one row"""
    _, out = table()
    have = collections.Counter((r[0], r[1], r[3]) for r in out)
    dup = [k for k, n in have.items() if n > 1]
    lost = layer_names = apart = 0
    A, Fr = layer_rows('acts'), layer_rows('free')
    for g in PATS:
        for L in 'AB':
            for s, ents in entries(L, g).items():
                canon = SX.merge([e[:3] for e in ents])
                for _, p, u, _, _, _ in ents:
                    for k in (p, u):
                        if k and have.get((s, L, ' '.join(canon.get(k, k)))) != 1:
                            lost += 1
                # the act and free-verb names, by the join the table makes
                names = {k for e in ents for k in e[1:3] if k}
                acts, free = A.get((g + ':' + s, L), []), Fr.get((g + ':' + s, L), [])
                links = {a: c for a, (c, _) in event_join(g, L, s, ents, acts).items()}
                for r in list(acts) + list(free):
                    for field in ('performer', 'undergoer'):
                      for part in SX.split_field(r[field]):
                        k = SX.key(part)
                        layer_names += 1
                        c = links.get(k) if CYR.search(part) else name_join(k, names, canon)
                        if c is None:
                            apart += 1
                        elif have.get((s, L, ' '.join(c))) != 1:
                            lost += 1
    counted = sum(int(r[6]) for r in UNJOINED)
    ok = not dup and not lost and counted == apart
    print('C1 %d rows; act and free-verb names checked %d, set apart as unjoined %d (counted in the table %d); '
          'names without exactly one row %d; character rows twice %d: %s'
          % (len(out), layer_names, apart, counted, lost, len(dup), 'PASS' if ok else 'FAIL'))
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


# ---------------------------------------------------------------- the act layer joined to the characters
UNJOINED = []   # the act and free-verb names that join no character, as the last table() set them apart
_READERS = []


def reader_kinds():
    """{(corpus, story, character): kind} from the name stage's answers where both readers agree (names.agreed());
    empty until the answers exist"""
    if not _READERS:
        if HERE not in sys.path:
            sys.path.append(HERE)   # Tragedy/tragedyScore.py changes the working directory when imported
        try:
            import names as N
            _READERS.append(N.agreed()[0])
        except (OSError, IndexError):
            _READERS.append({})
    return _READERS[0]


_SECOND = []


def second_stage():
    """{(corpus, story, character)} the second name stage asked, in batches both readers have answered (names.asked())"""
    if not _SECOND:
        if HERE not in sys.path:
            sys.path.append(HERE)
        try:
            import names as N
            _SECOND.append(N.asked())
        except (OSError, IndexError):
            _SECOND.append(set())
    return _SECOND[0]
ACT_STUDIES = ['twolayer', 'problems', 'held', 'animal']   # one act study per story and reader, the first present
CYR = re.compile('[Ѐ-ӿ]')


def act_rows():
    """{(global story, reader): [act rows]}, one study each"""
    return layer_rows('acts')


def name_join(a, names, canon):
    """an act name's character by the name join: the name itself, or the one longer name it may join, by
    Spheres/explore.py's joins()"""
    if a in canon:
        return canon[a]
    sup = [m for m in names if SX.joins(a, m)]
    if len(sup) == 1 or (sup and len({tuple(sorted(x)) for x in sup}) == 1):
        m = max(sup, key=lambda x: (len(x), x))
        return canon.get(m, m)
    return None


def event_join(g, L, s, ents, acts):
    """{act name key: (character by event, character by name)}: within an event with exactly one function performer
    and exactly one act performer, the two are linked; each act name takes its commonest link"""
    canon = SX.merge([e[:3] for e in ents])
    names = {k for e in ents for k in e[1:3] if k}
    fun, act = collections.defaultdict(set), collections.defaultdict(set)
    for fn, p, u, _, _, ev in ents:
        if p:
            fun[ev].add(canon.get(p, p))
    for r in acts:
        for part in SX.split_field(r['performer']):
            act[r['event']].add(SX.key(part))
    links = collections.defaultdict(collections.Counter)
    for ev, a in act.items():
        if len(a) == 1 and len(fun.get(ev, ())) == 1:
            links[next(iter(a))][next(iter(fun[ev]))] += 1
    out = {}
    for a, c in links.items():
        best = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        out[a] = (best, name_join(a, names, canon))
    return out


def c4():
    """the join by event agrees with the name join where both layers name characters in English"""
    A = act_rows()
    ok = True
    for g in ('fable', 'tragedy', 'animal'):
        for L in 'AB':
            linked = comparable = agree = 0
            for s, ents in entries(L, g).items():
                acts = [r for r in A.get((g + ':' + s, L), []) if not CYR.search(r['performer'])]
                for a, (by_event, by_name) in event_join(g, L, s, ents, acts).items():
                    linked += 1
                    if by_name is not None:
                        comparable += 1
                        agree += by_event == by_name
            share = 100.0 * agree / max(1, comparable)
            ok &= share >= 90
            print('C4 %-8s %s act names linked %4d, comparable %4d, agreeing %4d (%.1f%%): %s'
                  % (g, L, linked, comparable, agree, share, 'pass' if share >= 90 else 'FAIL'))
    print('C4 %s' % ('PASS' if ok else 'FAIL'))
    return ok


# ---------------------------------------------------------------- the bottom-up grouping (protocol section 4, route 2)
def group(X, kmin=3, kmax=10):
    """average linkage on cosine distance, the number of groups chosen by silhouette from kmin to kmax"""
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.metrics import silhouette_score
    Z = linkage(X, 'average', metric='cosine')
    best = None
    for k in range(kmin, kmax + 1):
        lab = fcluster(Z, k, 'maxclust')
        if len(set(lab)) < 2:
            continue
        sc = silhouette_score(X, lab, metric='cosine')
        if best is None or sc > best[0] + 1e-12:
            best = (sc, k, lab)
    return best[2]


def features():
    acts = sorted({r['act'].lower() for r in DT.rows('acts') if not r['id_flag']})
    return ['p:' + a for a in acts] + ['u:' + a for a in acts]


PLANTED = {'trickster': ['p:deceive', 'p:escape', 'p:be-taken-in', 'u:pursue'],
           'villain': ['p:harm', 'p:threaten', 'p:pursue', 'u:punish', 'u:fight'],
           'helper': ['p:give', 'p:guide', 'p:repair', 'p:reveal-information'],
           'victim': ['u:harm', 'p:lament', 'p:plead', 'u:repair']}


def real_profiles():
    """act profiles of the characters with at least 3 acts, where the acts are named in English and joined by name,
    and each one's spheres: [(vector, spheres)]"""
    import numpy as np
    F = features()
    ix = {f: i for i, f in enumerate(F)}
    A = act_rows()
    out = []
    for g in ('fable', 'tragedy', 'animal'):
        for L in 'AB':
            for s, ents in entries(L, g).items():
                canon = SX.merge([e[:3] for e in ents])
                names = {k for e in ents for k in e[1:3] if k}
                sph = collections.defaultdict(set)
                for fn, p, u, _, _, _ in ents:
                    if p:
                        for n, fs in SX.SPHERES.items():
                            if fn in fs:
                                sph[canon.get(p, p)].add(n)
                prof = collections.defaultdict(lambda: np.zeros(len(F)))
                for r in A.get((g + ':' + s, L), []):
                    for side, field in (('p:', 'performer'), ('u:', 'undergoer')):
                        for part in SX.split_field(r[field]):
                            if CYR.search(part):
                                continue
                            c = name_join(SX.key(part), names, canon)
                            if c is not None and side + r['act'].lower() in ix:
                                prof[c][ix[side + r['act'].lower()]] += 1
                for c, v in sorted(prof.items()):
                    if v.sum() >= 3:
                        out.append((v, ' + '.join(sorted(sph.get(c, ()))) or 'none'))
    return out


def c5():
    import numpy as np
    from sklearn.metrics import adjusted_rand_score as ari
    F = features()
    ix = {f: i for i, f in enumerate(F)}
    rnd = random.Random(20261026)
    X, truth = [], []
    for role, typical in PLANTED.items():
        for _ in range(100):
            v = np.zeros(len(F))
            for _ in range(10):
                v[ix[rnd.choice(typical)] if rnd.random() < 0.7 else rnd.randrange(len(F))] += 1
            X.append(v)
            truth.append(role)
    planted = ari(truth, group(np.array(X)))
    real = real_profiles()
    V = np.array([v for v, _ in real])
    S = [x for _, x in real]
    shuffled = []
    for i in range(20):
        perm = list(range(len(V)))
        random.Random(i).shuffle(perm)
        shuffled.append(ari(S, group(V[perm])))
    mean = sum(shuffled) / len(shuffled)
    ok = planted >= 0.8 and mean <= 0.05
    print('C5 planted roles recovered, ARI %.3f (needs 0.8): %s' % (planted, 'pass' if planted >= 0.8 else 'FAIL'))
    print('C5 shuffled profiles against the spheres, %d characters, 20 shuffles: mean ARI %.3f, highest %.3f (mean needs at most 0.05): %s'
          % (len(V), mean, max(shuffled), 'pass' if mean <= 0.05 else 'FAIL'))
    print('C5 %s' % ('PASS' if ok else 'FAIL'))
    return ok


# ---------------------------------------------------------------- the split of several-name fields
def c7():
    """the split (Characters/SplitRule.md, adopted 2026-10-26; Spheres/explore.py's split_field): no field with a name
    loses every name but its reciprocal and pronoun names, no name keeps a separator, and the parts dropped are
    counted"""
    several = re.compile(r';|/|,|\band\b')
    fields = parts = lost = left = dropped = 0
    for g in PATS:
        for L in 'AB':
            for r in DT.files('functions', PATS[g], L):
                for raw in (r['performer'], r['undergoer']):
                    raw = raw.strip()
                    if not SX.key(raw):
                        continue
                    fields += 1
                    ps = SX.split_field(raw)
                    parts += len(ps)
                    whole = [x for x in SX.SPLIT.split(SX.PAREN.sub(' ', raw)) if SX.key(x.strip())]
                    dropped += len(whole) - len(ps)
                    # a field is lost only if it held a name that is not a reciprocal or pronoun name
                    lost += not ps and any(not set(SX.key(x)) <= SX.PRONOUNS for x in whole)
                    left += sum(bool(several.search(x)) for x in ps)
    ok = not lost and not left
    print('C7 fields %d, names after the split %d, pronoun-like parts dropped %d; fields that lose every name %d; '
          'names still holding a separator %d: %s' % (fields, parts, dropped, lost, left, 'PASS' if ok else 'FAIL'))
    return ok


def dry():
    """counts only: no kind by role, no grouping, no ranking"""
    _, out = table()
    c = collections.defaultdict(collections.Counter)
    for r in out:
        x = c[(r[2], r[1])]
        x['stories:' + r[0]] = 1
        x['characters'] += 1
        x['with a sphere'] += bool(r[9])
        x['kind resolved'] += r[6] != 'unknown'
        x['with acts'] += 'acts' in r[12]
        x['acts only'] += 'functions' not in r[12] and 'acts' in r[12]
        x['free only'] += r[12] == 'free'
    for r in UNJOINED:
        c[(r[2], r[1])]['unjoined ' + r[3]] += int(r[6])
    for (g, L), x in sorted(c.items(), key=lambda kv: (list(PATS).index(kv[0][0]), kv[0][1])):
        n = x['characters']
        print('%-8s %s stories %3d, characters %5d, with a sphere %5d, kind resolved %3.0f%%, with acts %5d; '
              'unjoined mentions, acts %5d, free verbs %5d' % (g, L, sum(1 for k in x if k.startswith('stories:')), n, x['with a sphere'],
                                                              100.0 * x['kind resolved'] / max(1, n), x['with acts'],
                                                              x['unjoined acts'], x['unjoined free']))


if __name__ == '__main__':
    cmds = {'build': build, 'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4, 'c5': c5, 'c6': c6, 'c7': c7, 'dry': dry}
    a = sys.argv[1:]
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
