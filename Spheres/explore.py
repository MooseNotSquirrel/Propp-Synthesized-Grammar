#!/usr/bin/env python3
"""
explore.py -- a first look at Propp's spheres of action in the four genres. Exploratory, not a
frozen test. Each function in the original transcriptions is credited to the character who
performs it; a character's spheres are those whose functions it performs (Propp, ch. VI);
names are matched within a story (articles and punctuation left out; a name whose words all
stand in one longer name of the same story joins it), after a field naming several characters
is split into their names (Characters/SplitRule.md).

  python explore.py           writes Spheres/SpheresExplore.txt
  python explore.py strict    writes Spheres/SpheresExplore-strict.txt, struggle left out of the villain's sphere
"""
import collections
import glob
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

CORPORA = {'tale': (['Afanasyev/transcriptions/U/%s/b*/Notes.txt'], 4),
           'fable': (['Aesop/transcriptions/%s/b*/Notes.txt', 'Fables/transcriptions/%s/b*/Notes.txt'], 4),
           'tragedy': (['Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'], 4),
           'myth': (['Apollodorus/Apollodorus/transcriptions/%s/b*/Notes.txt'], 5)}
SPHERES = collections.OrderedDict([('villain', {'A', 'H', 'Pr'}), ('donor', {'D', 'F'}), ('helper', {'G', 'K', 'Rs', 'N', 'T'}),
                                   ('princess', {'M', 'J', 'Q', 'Ex', 'U'}), ('dispatcher', {'B'}), ('hero', {'C', '↑', 'E', 'W'}),
                                   ('false hero', {'L'})])
STOP = {'the', 'a', 'an', 'his', 'her', 'their', 'and', 'old', 'young', 'little'}
# *of* is kept in a name's key so that the head of an "of" phrase can be found (the owner, 2026-10-26)
TITLES = {'tsar', 'tsaritsa', 'tsarevich', 'tsarevna', 'korol', 'korolevich', 'korolevna', 'knyaz', 'knyazhna',
          'king', 'queen', 'prince', 'princess', 'emperor', 'empress', 'lord', 'lady', 'khan', 'sultan'}
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def key(name):
    return tuple(w for w in re.findall(r'[^\W\d_]+', name.lower()) if w not in STOP)


# A field naming several characters is split before the join (Characters/SplitRule.md, adopted by the owner
# 2026-10-26): notes in parentheses dropped, then split at a semicolon, a slash, a comma or *and*; a part that is
# only a pronoun-like word is dropped, group nouns kept; a function is credited to every name its performer holds.
PAREN = re.compile(r'\([^)]*\)')
SPLIT = re.compile(r'\s*(?:;|/|,|\band\b)\s*')
DROP = {'others', 'other', 'all', 'both', 'everyone', 'everybody', 'they', 'some', 'many', 'rest'}
# reciprocal and pronoun names are no characters (the owner, 2026-10-26): a part whose every word is one of these
PRONOUNS = DROP | {'each', 'one', 'another', 'himself', 'herself', 'itself', 'themselves', 'oneself', 'him', 'them',
                   'he', 'she', 'it', 'we', 'us', 'you', 'me', 'together', 'two', 'three', 'four', 'five', 'six', 'seven',
                   'of'}


def split_field(raw):
    """a performer or undergoer field as the names of the characters it holds"""
    parts = [p.strip() for p in SPLIT.split(PAREN.sub(' ', raw))]
    return [p for p in parts if key(p) and not set(key(p)) <= PRONOUNS]


def expand(fn, praw, uraw):
    """one function entry as one entry per pair of the names its two fields hold: (function, performer key,
    undergoer key, performer name, undergoer name)"""
    return [(fn, key(a), key(b), a, b) for a in split_field(praw) or [''] for b in split_field(uraw) or ['']]


def first_reading(vs):
    """the first reading of a story: the version with the fewest entries, then the lowest name"""
    return vs[sorted(vs, key=lambda v: (len(v), v))[0]]


def read(L):
    """{genre: {story: [(function, performer key, undergoer key)]}}, first reading of each story"""
    out = {}
    for g, (pats, sf) in CORPORA.items():
        st = collections.OrderedDict()
        for pat in pats:
            for path in sorted(glob.glob(os.path.join(P, pat % L))):
                for line in open(path, encoding='utf-8'):
                    f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
                    if len(f) < 10 or not re.match(r'^([PFA]\d{2}|L\d-\d{3})', f[0]):
                        continue
                    base, _, ver = f[0].partition('/')
                    st.setdefault(base, collections.OrderedDict()).setdefault(ver or '1', []).append(
                        (TS.base(f[sf]), f[sf + 1], f[sf + 2]))
        out[g] = {s: [e[:3] for x in first_reading(vs) for e in expand(*x)] for s, vs in st.items()}
    return out


def head(k):
    """a name key's head noun: the word before its first *of*, or else its last word"""
    return k[k.index('of') - 1] if 'of' in k[1:] else k[-1]


def joins(n, m):
    """may the name n join the longer name m (the owner's conditions, 2026-10-26)? Its words must stand in m, and
    either the two share a head noun ("sons" and "sons of Hippocoon", but not "the Camel" and "the Camel-driver", nor
    "Agamemnon" and "Agamemnon's servants"), or m only adds titles to n ("Ivan" and "Ivan-tsarevich"), or n is a
    title that m begins with ("tsar" and "Tsar Zmiulan")"""
    if m == n or not set(n) <= set(m):
        return False
    if head(n) == head(m):
        return True
    if set(m) - set(n) <= TITLES:
        return True
    return set(n) <= TITLES and m[:len(n)] == n


def merge(entries):
    """map each name to the longest name of the story it may join (joins()), where that is unique"""
    names = {n for _, p, u in entries for n in (p, u) if n}
    canon = {}
    for n in names:
        sup = [m for m in names if joins(n, m)]
        # ties among the longer names broken by the name itself, so the join does not move with Python's hash seed
        canon[n] = max(sup, key=lambda m: (len(m), m)) if len(sup) == 1 or (sup and len({tuple(sorted(s)) for s in sup}) == 1) else n
    return canon


def main(out_name='SpheresExplore.txt',
         header='# SpheresExplore.txt -- explore.py, exploratory; Propp\'s spheres of action counted in the original transcriptions.'):
    say(header)
    say('')
    for L in 'AB':
        data = read(L)
        say('TRANSCRIBER %s' % L)
        for g in CORPORA:
            stories = data[g]
            filled = collections.Counter()
            combos = collections.Counter()
            chars = multi = merged_hv = 0
            fallen = hero_stories = 0
            outside_only = acting = 0
            for s, entries in stories.items():
                canon = merge(entries)
                sph = collections.defaultdict(set)
                acts = collections.Counter()
                for fn, p, u in entries:
                    if not p:
                        continue
                    p = canon.get(p, p)
                    acts[p] += 1
                    for name, fs in SPHERES.items():
                        if fn in fs:
                            sph[p].add(name)
                for name in SPHERES:
                    filled[name] += any(name in v for v in sph.values())
                for c in acts:
                    acting += 1
                    if not sph.get(c):
                        outside_only += 1
                for c, v in sph.items():
                    chars += 1
                    if len(v) > 1:
                        multi += 1
                        combos[' + '.join(sorted(v))] += 1
                if any({'hero', 'villain'} <= v for v in sph.values()):
                    merged_hv += 1
                heroes = [c for c, v in sph.items() if 'hero' in v]
                if heroes:
                    hero_stories += 1
                    if any(fn in ('U', 'Ex') and canon.get(u, u) in heroes for fn, _, u in entries):
                        fallen += 1
            n = float(len(stories))
            say('  %-8s %3d stories; spheres filled (share of stories): %s' % (g, len(stories), ', '.join('%s %.0f%%' % (k, 100 * filled[k] / n) for k in SPHERES)))
            say('           characters in a sphere %d, in two or more %.0f%%; commonest combinations: %s'
                % (chars, 100.0 * multi / max(1, chars), '; '.join('%s %d' % kv for kv in combos.most_common(4))))
            say('           stories where one character holds both the hero\'s and the villain\'s sphere: %.0f%%; characters who act but in no sphere: %.0f%%'
                % (100 * merged_hv / n, 100.0 * outside_only / max(1, acting)))
            say('           stories with a hero in which a hero is exposed or punished: %d of %d (%.0f%%)' % (fallen, hero_stories, 100.0 * fallen / max(1, hero_stories)))
        say('')
    open(os.path.join(HERE, out_name), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')


def strict():
    """the strict reading: the villain's sphere as villainy and pursuit only, written to SpheresExplore-strict.txt"""
    SPHERES['villain'] = {'A', 'Pr'}
    main('SpheresExplore-strict.txt', '# SpheresExplore-strict.txt -- explore.py with the villain\'s sphere as villainy and pursuit '
         'only (struggle left out, transcribers crediting it to whoever fights, often the hero); exploratory; Propp\'s spheres '
         'of action counted in the original transcriptions.')


if __name__ == '__main__':
    if sys.argv[1:] == ['strict']:
        strict()
    else:
        main()
