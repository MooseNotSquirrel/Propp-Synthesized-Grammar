#!/usr/bin/env python3
"""
withJudgedHeroes.py -- the hero-dependent measures redone with the heroes the
two readers agree on (HeroLooseMatch.txt's match), 2026-10-12. A re-analysis,
not a frozen test; it replaces the counting rule's heroes, nothing else.

  python withJudgedHeroes.py     writes Heroes/WithJudgedHeroes.txt

1. The failed hero (XStudy/threatAndFall.py's second measure), on the
   original transcriptions of the tales, fables and tragedies.
2. The trickster: in the act transcriptions (TwoLayer), how many deceptions
   and harms the hero performs.
3. Recovering Propp (TwoLayer's third measure), per genre.

A story counts only where the readers agree. A hero is the set of name words
in both readers' answers (articles and the like left out, a plural s
ignored); a name matches if it shares a word. Russian names in the tales' act
transcriptions are transliterated to Latin letters first; names the event
lists translated rather than transliterated will not match, and the share of
tales where the hero is found is reported.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'TwoLayer'))
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import heroes as H  # noqa: E402
import twoLayer as T  # noqa: E402
import tragedyScore as TS  # noqa: E402

STOP = {'the', 'a', 'an', 'his', 'her', 'their', 'of', 'and', 'with', 'to', 'in', 'on', 'its', 'single', 'hero', 'no',
        'together', 'little', 'old', 'young', 'youngest', 'eldest', 'son', 'daughter', 'man', 'woman'}
CYR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
               ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
                'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def latin(s):
    return ''.join(CYR.get(c, c) for c in s.lower())


def words(name):
    name = latin(name)
    if name.startswith('no single hero'):
        name = name.split(':', 1)[1] if ':' in name else ''
    return {w.rstrip('s') for w in re.findall(r'[^\W\d_]+', name) if w not in STOP and len(w) > 2}


def judged():
    A, B = H.answers('A'), H.answers('B')
    out = {}
    for s in set(A) & set(B):
        wa, wb = words(A[s][0]), words(B[s][0])
        na, nb = A[s][0].lower().startswith('no single'), B[s][0].lower().startswith('no single')
        if (wa & wb) or (na and nb):
            out[s] = wa | wb
    return out


def is_hero(hw, name):
    return bool(hw) and bool(hw & words(name))


def entries(paths):
    st = collections.OrderedDict()
    for p in paths:
        for l in open(p, encoding='utf-8'):
            f = [x.strip() for x in l.split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]) or f[7][:1].upper() != 'Y':
                continue
            st.setdefault(f[0].split('/')[0], []).append((f[4], f[5], f[6]))
    return st


def failed_hero(J):
    say('1. THE FAILED HERO, with judged heroes (original transcriptions)')
    pats = {'tale': 'Afanasyev/transcriptions/U/%s/b*/Notes.txt', 'fable': '%s/transcriptions/%s/b*/Notes.txt',
            'tragedy': 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'}
    for g in ('tale', 'fable', 'tragedy'):
        for L in 'AB':
            if g == 'fable':
                paths = sorted(glob.glob(os.path.join(P, 'Aesop', 'transcriptions', L, 'b*', 'Notes.txt'))) + \
                    sorted(glob.glob(os.path.join(P, 'Fables', 'transcriptions', L, 'b*', 'Notes.txt')))
            else:
                paths = sorted(glob.glob(os.path.join(P, pats[g] % L)))
            n = won = fa = fb = 0
            ex = set()
            for s, ents in entries(paths).items():
                if s not in J:
                    continue
                hw = J[s]
                n += 1
                w = next((i for i, (sym, pf, u) in enumerate(ents) if TS.base(sym) in ('I', 'K', 'W', 'N')
                          and not TS.negative(sym) and (is_hero(hw, pf) or is_hero(hw, u))), None)
                if w is None:
                    continue
                won += 1
                rest = ents[w + 1:]
                if any((TS.base(sym) in ('Ex', 'U') and is_hero(hw, u)) or (TS.base(sym) == 'I' and TS.negative(sym) and is_hero(hw, pf))
                       for sym, pf, u in rest):
                    fa += 1
                j = next((i for i, (sym, pf, u) in enumerate(rest) if TS.base(sym) == 'A' and is_hero(hw, u)), None)
                if j is not None and not any(TS.base(sym) == 'K' for sym, _, _ in rest[j + 1:]):
                    fb += 1
                    ex.add(s)
            say('  %-8s %s: %3d stories with a judged hero; the hero succeeds in %3d; then exposed, punished or defeated %2d; '
                'a villainy on the hero never undone %2d (%.0f%%) %s' % (g, L, n, won, fa, fb, 100.0 * fb / max(1, won),
                                                                       ' '.join(sorted(ex)) if g == 'tragedy' else ''))


def acts_sections(J):
    M = T.material()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    stories = set(gen)
    raw, funcs, der = {}, {}, {}
    orig_paths = {'tale': 'Afanasyev/transcriptions/U/%s/b*/Notes.txt', 'fable': 'Fables/transcriptions/%s/b*/Notes.txt',
                  'tragedy': 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'}
    T.is_ = lambda hw, name: is_hero(hw, name)
    for L in 'AB':
        raw[L] = T.read_acts(sorted(glob.glob(os.path.join(T.OUT, '*', 'acts', L, '*', 'Notes.txt'))))
        o = {}
        for g in T.GENRES:
            o.update({e: v for e, v in T.read_functions(glob.glob(os.path.join(P, orig_paths[g] % L))).items() if e[0] in stories})
        funcs[L] = o
        der[L] = {e: {f for a, pf, u, r in v for f in [T.derive(a, pf, u, J.get(e[0], set()))] if f}
                  for e, v in raw[L].items() if e[0] in J}
    say('')
    say('2. THE TRICKSTER, with judged heroes (act transcriptions; stories with a judged hero)')
    for g in T.GENRES:
        for L in 'AB':
            c = collections.Counter()
            found = set()
            for e, v in raw[L].items():
                if gen.get(e[0]) != g or e[0] not in J:
                    continue
                for a, pf, u, r in v:
                    hp = is_hero(J[e[0]], pf)
                    if hp or is_hero(J[e[0]], u):
                        found.add(e[0])
                    if a in ('deceive', 'harm'):
                        c[a] += 1
                        c[a + ' by hero'] += hp
            nst = len({e[0] for e in raw[L] if gen.get(e[0]) == g and e[0] in J})
            say('  %-8s %s: the hero found in %d of %d stories; the hero deceives in %d of %d deceptions (%.0f%%), harms in %d of %d (%.0f%%)'
                % (g, L, len(found), nst, c['deceive by hero'], c['deceive'], 100.0 * c['deceive by hero'] / max(1, c['deceive']),
                   c['harm by hero'], c['harm'], 100.0 * c['harm by hero'] / max(1, c['harm'])))
    say('')
    say('3. RECOVERING PROPP, with judged heroes (TwoLayer\'s third measure; stories with a judged hero)')
    events = sorted(set(funcs['A']) & set(funcs['B']) & set(raw['A']) & set(raw['B']))
    events = [e for e in events if e[0] in J]
    for g in list(T.GENRES) + ['all']:
        E = [e for e in events if g == 'all' or gen[e[0]] == g]
        say('  %-8s events %4d: recovered against original A %.3f, B %.3f; original A against B %.3f'
            % (g, len(E), T.jaccard(der['A'], funcs['A'], E), T.jaccard(der['B'], funcs['B'], E), T.jaccard(funcs['A'], funcs['B'], E)))


if __name__ == '__main__':
    J = judged()
    say('# WithJudgedHeroes.txt -- withJudgedHeroes.py, a re-analysis with the heroes both readers agree on; not a frozen test.')
    say('Stories with a judged hero: %d' % len(J))
    say('')
    failed_hero(J)
    acts_sections(J)
    open(os.path.join(HERE, 'WithJudgedHeroes.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(OUT) + '\n')
