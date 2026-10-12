#!/usr/bin/env python3
"""
twoLayer.py -- the test of a catalog of acts and relations (TwoLayerProtocol.md).

  python twoLayer.py setup   writes the transcribers' material, prompts and run file
                             into Story Language/ActsRoles
  python twoLayer.py score   scores the act transcriptions against the original
                             function transcriptions; writes TwoLayer/TwoLayerRun.txt

Written in full before any act transcription existed.
"""
import collections
import glob
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
OUT = os.path.join(P, 'ActsRoles')
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(ROOT, 'Calibration', 'Split.txt'), encoding='utf-8') if '|' in l}
ACTS = [l.split('|')[1].strip() for l in open(os.path.join(HERE, 'Acts.md'), encoding='utf-8')
        if l.startswith('| ') and not l.startswith('| Act') and not l.startswith('| Relation')
        and '---' not in l][:37]
GENRES = ('tale', 'fable', 'tragedy')


def fable_batches():
    out = []
    for b in ('b1', 'b2'):
        m = re.search(r'these fables only: ([^.]*)\.', open(os.path.join(P, 'Fables', 'prompts', 'transcribe-A-%s.txt' % b),
                                                             encoding='utf-8').read())
        out.append([x.strip() for x in m.group(1).split(',')])
    return out


def material():
    """{genre: {batch: [story ids]}}"""
    tales = ['A%03d' % t for t in SPLIT['test']]
    f1, f2 = fable_batches()
    plays = ['P%02d' % i for i in range(17, 25)]
    return {'tale': {'t1': tales[:12], 't2': tales[12:]},
            'fable': {'f1': f1, 'f2': f2},
            'tragedy': {'g%d' % (i + 1): plays[2 * i:2 * i + 2] for i in range(4)}}


def subset(src, dst, ids):
    with open(dst, 'w', encoding='utf-8', newline='\n') as out:
        for line in open(src, encoding='utf-8'):
            if line.split('|')[0].strip() in ids:
                out.write(line)


PROMPT = ("You are describing what happens in {what}. You start with no background on the project, and you should not look for any.\n\n"
          "Read ActsRules.md in this repository first, in full, and follow it exactly. {where}\n\n"
          "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its act, performer, undergoer, relation and Y or N.\n\n"
          "Open only ActsRules.md, {files} and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under {genre}/acts/ but your own folder. Do not search the web. You are describer {L}.\n\n"
          "Write one file, and nothing else, {genre}/acts/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on{orig}.\n\n"
          "Then reply with the report the rules' last section asks for.\n")


def setup():
    M = material()
    os.makedirs(os.path.join(OUT, 'prompts'), exist_ok=True)
    af, fa, tr = (os.path.join(P, x) for x in ('Afanasyev', 'Fables', 'Tragedy'))
    os.makedirs(os.path.join(OUT, 'tale', 'tales'), exist_ok=True)
    tales = [t for b in M['tale'].values() for t in b]
    for t in tales:
        shutil.copy(os.path.join(af, 'tales', t + '.txt'), os.path.join(OUT, 'tale', 'tales', t + '.txt'))
    subset(os.path.join(af, 'Events.txt'), os.path.join(OUT, 'tale', 'Events.txt'), set(tales))
    fables = {f for b in M['fable'].values() for f in b}
    os.makedirs(os.path.join(OUT, 'fable'), exist_ok=True)
    for f in ('Fables.txt', 'Events.txt'):
        subset(os.path.join(fa, f), os.path.join(OUT, 'fable', f), fables)
    for p in (p for b in M['tragedy'].values() for p in b):
        os.makedirs(os.path.join(OUT, 'tragedy', 'plays', p), exist_ok=True)
        for f in ('Text.txt', 'Events.txt', 'Cast.txt'):
            shutil.copy(os.path.join(tr, 'plays', p, f), os.path.join(OUT, 'tragedy', 'plays', p, f))
    order = {l.split('|')[0].strip(): l.split('|')[2].strip() + "'s " + l.split('|')[3].strip()
             for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}
    for L in 'AB':
        for b, ids in M['tale'].items():
            files = ', '.join('tale/tales/%s.txt' % i for i in ids) + ', tale/Events.txt'
            text = PROMPT.format(what='some tales from Aleksandr Afanasyev\'s collection of Russian folktales', L=L, b=b, genre='tale',
                                 where='Your tales are these %d, one per file, read in their original language: %s. Their events are in tale/Events.txt.'
                                       % (len(ids), ', '.join('tale/tales/%s.txt' % i for i in ids)),
                                 files=files, orig=', in the original language')
            open(os.path.join(OUT, 'prompts', 'acts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
        for b, ids in M['fable'].items():
            text = PROMPT.format(what="some of Aesop's fables, in George Fyler Townsend's 1867 translation", L=L, b=b, genre='fable',
                                 where='The fables are in fable/Fables.txt, one per line as "identifier | title | text", and their events in fable/Events.txt. Your fables are these: %s.' % ', '.join(ids),
                                 files='fable/Fables.txt, fable/Events.txt', orig='')
            open(os.path.join(OUT, 'prompts', 'acts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
        for b, ids in M['tragedy'].items():
            text = PROMPT.format(what='two Greek plays, %s, in English translation' % ' and '.join('%s (%s)' % (order[p], p) for p in ids),
                                 L=L, b=b, genre='tragedy',
                                 where='Each play is in its folder under tragedy/plays/: Text.txt, one speech per line; Events.txt, its events; and Cast.txt, its cast. Name every performer and undergoer exactly as the play\'s Cast.txt names them. Write the two plays one after the other.',
                                 files=', '.join('tragedy/plays/%s/Text.txt, Events.txt and Cast.txt' % p for p in ids), orig='')
            open(os.path.join(OUT, 'prompts', 'acts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
    print({g: {b: len(v) for b, v in bs.items()} for g, bs in M.items()})


# ---------------------------------------------------------------- scoring
def hero_names():
    h = {}
    paths = [os.path.join(P, 'Afanasyev', 'Heroes.txt'), os.path.join(P, 'Fables', 'Heroes.txt')] + \
        glob.glob(os.path.join(P, 'Tragedy', 'plays', 'P*', 'Hero.txt'))
    for path in paths:
        for l in open(path, encoding='utf-8'):
            if '|' in l:
                s, rest = l.split('|', 1)
                rest = rest.split('| moral')[0].split('|')[0]
                names = [x.split('(')[0].strip() for x in rest.replace('hero:', '').split(';') if x.strip()]
                words = [[w for w in re.findall(r'[^\W\d_]+', n.lower()) if w not in ('the', 'a', 'an')] for n in names]
                h[s.strip()] = [w[0] for w in words if w]
    return h


def is_(hero, name):
    return bool(hero) and hero in name.lower()


def derive(act, perf, und, hero):
    """the function an act maps to, for one hero, or None (TwoLayerProtocol.md)."""
    hp, hu = is_(hero, perf), is_(hero, und)
    hi = hp or hu
    table = {
        'leave': '↑' if hp else 'β', 'forbid': 'γ', 'disobey': 'δ', 'seek-information': 'ε',
        'reveal-information': 'B' if hu else 'ζ', 'deceive': None if hp else 'η', 'be-taken-in': 'θ',
        'harm': None if hp else 'A', 'want': 'a', 'plead': 'B' if hu else None, 'send': 'B' if hu else None,
        'decide': 'C' if hp else None, 'test': 'D' if hu else None, 'respond': 'E' if hp else None,
        'give': 'F' if hu else None, 'receive': 'F' if hp else None, 'guide': 'G' if hu else None,
        'fight': 'H' if hi else None, 'win': 'I' if hp else None, 'lose': 'I-' if hp else None,
        'mark': 'J' if hu else None, 'repair': 'K', 'return': '↓' if hp else None, 'pursue': 'Pr' if hu else None,
        'escape': 'Rs' if hp else None, 'arrive-unknown': 'o' if hp else None, 'claim-falsely': 'L',
        'set-task': 'M' if hu else None, 'do-task': 'N' if hp else None, 'recognize': 'Q' if hi else None,
        'expose': None if hu else 'Ex', 'transform': 'T' if hi else None, 'punish': None if hu else 'U',
        'marry': 'W' if hi else None}
    return table.get(act)


def read_acts(paths):
    """{(story, event): [(act, performer, undergoer, relation)]}"""
    out = collections.defaultdict(list)
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 9)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
                continue
            ev = re.search(r'\d+', f[1])
            if ev and f[6][:1].upper() in 'YN':
                out[(f[0].split('/')[0], int(ev.group()))].append((f[2].lower(), f[3], f[4], f[5].lower()))
    return out


def read_functions(paths):
    """{(story, event): set of function keys}, X left out; every event with an entry is present."""
    out = collections.defaultdict(set)
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 10 or not re.match(r'^[PFA]\d{2}', f[0]):
                continue
            ev = re.search(r'\d+', f[3])
            if not ev:
                continue
            key = (f[0].split('/')[0], int(ev.group()))
            out[key]
            b = TS.base(f[4])
            if b != 'X':
                out[key].add(b + ('-' if TS.negative(f[4]) and b == 'I' else ''))
    return out


def jaccard(X, Y, events):
    both = either = 0
    for e in events:
        a, b = X.get(e, set()), Y.get(e, set())
        both += len(a & b)
        either += len(a | b)
    return both / float(either) if either else 0.0


def score():
    M = material()
    heroes = hero_names()
    orig_paths = {'tale': 'Afanasyev/transcriptions/U/%s/b*/Notes.txt', 'fable': 'Fables/transcriptions/%s/b*/Notes.txt',
                  'tragedy': 'Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'}
    stories = {s for bs in M.values() for b in bs.values() for s in b}
    acts, funcs, derived = {}, {}, {}
    for L in 'AB':
        raw = read_acts(sorted(glob.glob(os.path.join(OUT, '*', 'acts', L, '*', 'Notes.txt'))))
        acts[L] = {e: {a for a, _, _, _ in v if a in ACTS and a != 'other'} for e, v in raw.items()}
        acts[L, 'raw'] = raw
        o = {}
        for g in GENRES:
            o.update({e: v for e, v in read_functions(glob.glob(os.path.join(P, orig_paths[g] % L))).items() if e[0] in stories})
        funcs[L] = o
        d = {}
        for e, v in raw.items():
            fs = set()
            for h in heroes.get(e[0], []) or ['']:
                for a, perf, und, rel in v:
                    f = derive(a, perf, und, h)
                    if f:
                        fs.add(f)
            d[e] = fs
        derived[L] = d
    events = sorted(set(funcs['A']) & set(funcs['B']) & set(acts['A', 'raw']) & set(acts['B', 'raw']))
    rep = ['# TwoLayerRun.txt -- twoLayer.py score, as TwoLayerProtocol.md freezes it.', '',
           'Events compared: %d (in both original transcriptions and both new ones)' % len(events), '']
    cov_ok = True
    for L in 'AB':
        cn = sum(1 for e in events if acts[L].get(e)) / float(len(events))
        co = sum(1 for e in events if funcs[L].get(e)) / float(len(events))
        cov_ok = cov_ok and cn - co >= 0.10
        rep.append('1. coverage, transcriber %s: acts %.1f%%, Propp\'s functions %.1f%%, difference %+.1f points'
                   % (L, 100 * cn, 100 * co, 100 * (cn - co)))
    ja, jf = jaccard(acts['A'], acts['B'], events), jaccard(funcs['A'], funcs['B'], events)
    rep.append('2. agreement: on acts %.3f, on Propp\'s functions %.3f' % (ja, jf))
    jr = [jaccard(derived[L], funcs[L], events) for L in 'AB']
    rep.append('3. recovering Propp: derived against original, A %.3f, B %.3f, mean %.3f; original A against B %.3f'
               % (jr[0], jr[1], sum(jr) / 2, jf))
    ok2, ok3 = ja >= jf, sum(jr) / 2 >= jf
    fails = [n for n, ok in (('coverage', cov_ok), ('agreement', ok2), ('recovering Propp', ok3)) if not ok]
    rep += ['', 'VERDICT: %s' % ('THE TWO-LAYER CATALOG IS ADOPTED' if not fails else 'IT IS NOT ADOPTED; failing: ' + ', '.join(fails)), '']
    rep.append('REPORTED, NOT JUDGED')
    same = agree = 0
    for e in events:
        ra = {(a, r) for a, _, _, r in acts['A', 'raw'].get(e, [])}
        rb = {(a, r) for a, _, _, r in acts['B', 'raw'].get(e, [])}
        for a in {x for x, _ in ra} & {x for x, _ in rb}:
            same += 1
            agree += bool({r for x, r in ra if x == a} & {r for x, r in rb if x == a})
    rep.append('  relations: where both give an event the same act, the same relation in %d of %d (%.0f%%)'
               % (agree, same, 100.0 * agree / max(1, same)))
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    for g in GENRES:
        for L in 'AB':
            tot = collections.Counter()
            hero_does = collections.Counter()
            for e, v in acts[L, 'raw'].items():
                if gen.get(e[0]) != g:
                    continue
                hs = heroes.get(e[0], [])
                for a, perf, und, rel in v:
                    tot[a] += 1
                    hero_does[a] += any(is_(h, perf) for h in hs)
            rep.append('  %s %s: the hero deceives in %d of %d deceptions, harms in %d of %d harms; most common acts: %s'
                       % (g, L, hero_does['deceive'], tot['deceive'], hero_does['harm'], tot['harm'],
                          ', '.join('%s %d' % kv for kv in tot.most_common(6))))
    open(os.path.join(HERE, 'TwoLayerRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup']:
        setup()
    elif a == ['score']:
        score()
    else:
        sys.exit(__doc__)
