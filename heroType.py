#!/usr/bin/env python3
"""
heroType.py -- which hero the tale follows: the seeker or the victim.

  python heroType.py            the tables
  python heroType.py --summary  one line, as StepTests.txt pins it

Propp splits heroes in two at p.36: where a girl is carried off and the
tale follows the one who goes after her, the hero is a seeker; where it
follows the girl herself, he is a victimized hero. He adds that no tale in
his material follows both. At p.37 he states that the four forms of
mediation B he has just listed refer to seeker-heroes and the forms after
them to the victimized hero, so the variety digit on B tells which hero a
move follows: B1-B4 seeker, B5-B7 victim. At p.38 he restricts the decision
to act, C, to tales whose hero is a seeker.

The reading rules are those of the first project's ConsentClaim.md, as
consentScan.py applies them: the superscript is the variety, subscripts
and marks are dropped, a raised B carries no digit, and a move's B is its
first. Moves are counted where B and the departure stand together, as
finding BM counts them; tales are counted where any move carries B, as
finding BO counts them. A tale is seeker or victim when every digit it
carries agrees, mixed when they differ, and undigited when it has none.

CAUTION: a move without B says nothing here about its hero. The type is
read only where Propp marked it.
"""
import collections
import sys

CORPUS = 'ResolvedMoves.txt'
SUP_DIGIT = {c: str(i) for i, c in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹')}
DROP = '₀₁₂₃₄₅₆₇₈₉₊₋*ⁱᵛˣ'
BRAISED = 'ᴮ'
UP = '↑'
SEEKER, VICTIM = set('1234'), set('567')


def load(path=CORPUS):
    rows = []
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or not line.strip():
            continue
        cells = line.rstrip('\n').split('\t')
        if len(cells) >= 3:
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def parse(move):
    out = []
    for tok in move.split():
        if tok.startswith(BRAISED):
            out.append(('B', None))
            continue
        base = ''.join(ch for ch in tok if ch not in SUP_DIGIT and ch not in DROP)
        var = ''.join(SUP_DIGIT[ch] for ch in tok if ch in SUP_DIGIT)
        out.append((base, var or None))
    return out


def kind(var):
    if var is None:
        return 'undigited'
    return 'seeker' if var in SEEKER else 'victim' if var in VICTIM else 'undigited'


def tally(path=CORPUS):
    moves = collections.Counter()
    withc = collections.Counter()
    tales = collections.OrderedDict()
    for tale, mv, move in load(path):
        toks = parse(move)
        bases = [b for b, _ in toks]
        if 'B' not in bases:
            continue
        k = kind(toks[bases.index('B')][1])
        tales.setdefault(tale, set()).add(k)
        if UP in bases:
            moves[k] += 1
            withc[k] += 'C' in bases
    per = collections.Counter()
    victims = []
    for tale, ks in tales.items():
        ks = ks - {'undigited'}
        t = 'mixed' if len(ks) > 1 else ks.pop() if ks else 'undigited'
        per[t] += 1
        if t == 'victim':
            victims.append(tale)
    return moves, withc, per, victims, len(tales)


def summary():
    moves, withc, per, victims, n = tally()
    m = ', '.join('%s %d (C %d)' % (k, moves[k], withc[k]) for k in ('seeker', 'victim', 'undigited'))
    return ('B with departure %d: %s; tales with B %d: seeker %d, victim %d (%s), undigited %d, mixed %d'
            % (sum(moves.values()), m, n, per['seeker'], per['victim'], ' '.join(victims),
               per['undigited'], per['mixed']))


def main(argv):
    if argv == ['--summary']:
        print(summary())
        return 0
    moves, withc, per, victims, n = tally()
    print('moves carrying B and the departure: %d' % sum(moves.values()))
    for k in ('seeker', 'victim', 'undigited'):
        print('  %-10s %2d moves, C in %2d' % (k, moves[k], withc[k]))
    print('tales carrying B: %d' % n)
    for k in ('seeker', 'victim', 'undigited', 'mixed'):
        print('  %-10s %2d' % (k, per[k]))
    print('  victim tales: %s' % ' '.join(victims))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
