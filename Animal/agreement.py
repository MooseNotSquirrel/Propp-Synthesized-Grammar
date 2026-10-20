#!/usr/bin/env python3
"""
agreement.py -- a check, not a frozen test: how far transcribers A and B agree
on the animal tales, beside the same figures for every corpus already
transcribed (wondertales arms U and C, fables, tragedies, myths).

  python agreement.py        writes Animal/AgreementCheck.txt

Written after the animal tales were scored (AnimalRun.txt), to see whether the
split on placement comes from a weaker agreement on these tales.

THE MEASURES, all computed here the same way for every corpus:
  content, order, moves   the calibration's yardstick (Calibration/compare.py):
                          per story, the functions marked Y in the order of the
                          notes, X and the preparatory functions left out,
                          symbols reduced by tragedyScore.key; content is the
                          Dice of the two multisets, order one minus the
                          Levenshtein distance over the longer length, moves
                          the share of stories with equal move counts;
                          averaged over stories, unweighted.
  events                  the two-layer test's agreement on functions
                          (TwoLayer/twoLayer.py): over the events both
                          transcribers wrote an entry for, the functions both
                          give an event over the functions either gives it,
                          X left out, a negative I kept apart, every entry
                          counted whatever its mark; pooled over the corpus.
Each story's first reading, as Model/model.py and animal.py read it.
The myths' rules carry no relevance mark, so every myth entry counts as marked Y.
The arm C wondertales are the nearest comparison: the animal tales were
transcribed under the same card.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Tragedy'))
import tragedyScore as TS  # noqa: E402

VOCAB = set(TS.NUM) - TS.PREP
CORPORA = [('wondertales, arm U', ['Afanasyev/transcriptions/U/%s/b*/Notes.txt'], 4),
           ('wondertales, arm C', ['Afanasyev/transcriptions/C/%s/b*/Notes.txt'], 4),
           ('fables', ['Aesop/transcriptions/%s/b*/Notes.txt', 'Fables/transcriptions/%s/b*/Notes.txt'], 4),
           ('tragedies', ['Tragedy/transcriptions/%s/P[0-9][0-9]/Notes.txt'], 4),
           ('myths', ['Apollodorus/Apollodorus/transcriptions/%s/b*/Notes.txt'], 5),
           ('animal tales', ['AnimalTales/transcriptions/%s/b*/Notes.txt'], 4)]
OUT = []


def say(s=''):
    OUT.append(s)
    print(s)


def read(pats, sf, L):
    """{story: [(move, event, symbol, marked Y)]}, each story's first reading"""
    st = collections.OrderedDict()
    for pat in pats:
        for path in sorted(glob.glob(os.path.join(P, pat % L))):
            for line in open(path, encoding='utf-8'):
                f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
                if len(f) < 10 or not re.match(r'^([PFA]\d{2}|L\d-\d{3})', f[0]):
                    continue
                base, _, ver = f[0].partition('/')
                ev = re.search(r'\d+', f[3])
                st.setdefault(base, collections.OrderedDict()).setdefault(ver or '1', []).append(
                    (f[1], int(ev.group()) if ev else None, f[sf], sf == 5 or f[sf + 3].upper().startswith('Y')))
    return {s: vs[sorted(vs, key=lambda v: (len(v), v))[0]] for s, vs in st.items()}


def stream(es):
    return [k for _, _, sym, y in es if y and TS.base(sym) != 'X' for k in TS.key(sym) if k in VOCAB]


def by_event(es):
    out = collections.defaultdict(set)
    for _, ev, sym, _ in es:
        if ev is None:
            continue
        out[ev]
        b = TS.base(sym)
        if b and b != 'X':
            out[ev].add(b + ('-' if TS.negative(sym) and b == 'I' else ''))
    return out


def dice(a, b):
    if not a and not b:
        return 1.0
    ca, cb = collections.Counter(a), collections.Counter(b)
    return 2.0 * sum((ca & cb).values()) / (len(a) + len(b))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def order(a, b):
    if not a and not b:
        return 1.0
    return 1.0 - lev(a, b) / float(max(len(a), len(b)))


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float('nan')


def measure(pats, sf):
    A, B = read(pats, sf, 'A'), read(pats, sf, 'B')
    common = [s for s in A if s in B]
    c = [dice(stream(A[s]), stream(B[s])) for s in common]
    o = [order(stream(A[s]), stream(B[s])) for s in common]
    m = [len({e[0] for e in A[s]}) == len({e[0] for e in B[s]}) for s in common]
    both = either = 0
    for s in common:
        ea, eb = by_event(A[s]), by_event(B[s])
        for ev in set(ea) & set(eb):
            both += len(ea[ev] & eb[ev])
            either += len(ea[ev] | eb[ev])
    size = (mean(len(stream(A[s])) for s in common), mean(len(stream(B[s])) for s in common))
    return len(common), mean(c), mean(o), mean(m), both / float(either) if either else float('nan'), size, c, o


def main():
    say('# AgreementCheck.txt -- agreement.py: transcribers A and B, every corpus measured the same way.')
    say('# A check, not a frozen test; nothing here is judged.')
    say()
    say('%-20s %7s %8s %7s %7s %7s %13s' % ('corpus', 'stories', 'content', 'order', 'moves', 'events', 'functions A B'))
    rows = {}
    for name, pats, sf in CORPORA:
        r = measure(pats, sf)
        rows[name] = r
        say('%-20s %7d %8.3f %7.3f %6.1f%% %7.3f %6.1f %6.1f' % (name, r[0], r[1], r[2], 100 * r[3], r[4], r[5][0], r[5][1]))
    say()
    say('functions A B: the mean count per story of the functions content and order compare, for each transcriber.')
    say()
    say('The animal tales against the wondertales of arm C, the same card, story by story:')
    for name in ('wondertales, arm C', 'animal tales'):
        c, o = sorted(rows[name][6]), sorted(rows[name][7])
        q = lambda xs: (xs[len(xs) // 4], xs[len(xs) // 2], xs[3 * len(xs) // 4])
        say('  %-20s content quartiles %.2f %.2f %.2f; order quartiles %.2f %.2f %.2f'
            % ((name,) + q(c) + q(o)))
    A, B = read(CORPORA[-1][1], 4, 'A'), read(CORPORA[-1][1], 4, 'B')
    low = sorted((dice(stream(A[s]), stream(B[s])), s) for s in A if s in B)[:10]
    say('  the ten animal tales A and B agree on least (content): %s'
        % ', '.join('%s %.2f' % (s, v) for v, s in low))
    with open(os.path.join(HERE, 'AgreementCheck.txt'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
