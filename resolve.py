#!/usr/bin/env python3
"""
resolve.py -- STAGE 1 of the Propp grammar test harness: the combination resolver.

Propp separates two things and so must we (Morphology, p. 94): "the method of
combining moves does not exert any influence whatever" on the internal structure
of a move. This stage handles combination; the parser (stage 2) handles internal
structure and must never see a combination marker.

INPUT   the token-stream corpus (TaleTokenStreamsV4Utf8.txt), which records
        the tale AS PRINTED, with Propp's combination markers intact.
OUTPUT  a flat list of complete move-strings, one per (tale, move), with every
        combination marker resolved away -- ready for the regular move grammar.

The markers, and what this stage does with each (all attested in the corpus):

  <<shared>> / shared:   tale 125. Propp method 5, "two moves may have a common
        ending" (p. 93). A DAG: two moves, one tail. UNFOLD: append the shared
        tail to each move that points at it. Two move-strings result.

  <N>   tales 138, 159, 162. Propp methods 2-3, interruption (p. 93): "a
        development which has begun pauses, and a new move is inserted." The
        interrupting move N is recorded separately already; the marker is just
        a cross-reference. REMOVE it -- the interrupted move's own tokens are
        complete without it. The interrupter is parsed as its own move.

  > Y / <   tale 155. Propp method 6, two seekers (p. 93). Road marker "<" and
        signaller "Y". These are combination apparatus, not functions. They sit
        inside overflow[...] here, so they are already quarantined; REMOVE them
        from the parse stream.

  overflow[...]   15 cells. Position-undetermined BECAUSE THE TABLE DOES NOT
        FIX PARKED-CELL ORDER, which is a reading of the table and not a
        citation of Propp. The gloss this comment carried -- that Propp
        footnotes 105 II to say the parked cells belong elsewhere -- IS
        WITHDRAWN: PublicationGridMaster.txt 105c records that it is not in
        Propp's note on 105, which gives only the mare/struggle designation,
        and that it was imported by analogy from 113's footnote 3, itself
        unverified. NOT combination, but also not
        parseable in place. Two outputs per move: the CANONICAL string (overflow
        cells dropped) that the order-test sees, and the FULL string (overflow
        cells kept, marked) for the record. Only the canonical one is falsified.

  park[...]   3 cells: 139 I's J-super-2, 140 I's F-super-7 and 141 I's
        F-super-2. THE COUNT READ 2 AND NAMED ONLY THE FIRST TWO until it
        was derived; FalsificationResult.md's parking table had all three
        throughout. Same treatment as
        overflow[...], and dropped by the same regex. The difference is only
        where the cell was found: overflow[...] marks the parking area left of
        A, park[...] a headerless column elsewhere on the line. Both are
        position-undetermined and both are excluded from the order test by
        S9 in ProppGrammarLogic.md. The two annotations live in the corpus
        file, not here; this resolver honours them, it does not decide them.

  B-opener   tale 133. Not a marker at all -- just a move that opens on B
        instead of A/a (Propp p. 37: mediation substitutes for villainy). The
        resolver does nothing; the grammar's opener set A|a|B handles it.

  { X / Y }   repetition or branching, ruling 68. NOT combination --
        either way it is internal move structure, and it stays for the
        parser to handle. The resolver leaves braces untouched.
"""
import re, sys

def strip_marks(s):
    """remove combination cross-references that are not functions"""
    s = re.sub(r'<[IVX]+>', ' ', s)          # <II> <III> <IV> interruption refs
    s = re.sub(r'\.\.\.', ' ', s)            # interruption dots
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def split_overflow(s):
    """return (canonical, full): canonical drops overflow and parked cells; full marks them"""
    full = s
    # overflow[ ... ] and park[ ... ] -> drop for the canonical string.
    # Both are position-undetermined and excluded from the order test by the
    # same rule (ProppGrammarLogic.md S9); they differ only in where on the
    # page the cell was found, not in how the order test must treat it.
    canon = re.sub(r'(?:overflow|park)\[[^\]]*\]', ' ', s)
    canon = re.sub(r'\s+', ' ', canon).strip()
    return canon, full

def parse_corpus(path):
    tales, cur = [], None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        m = re.match(r'^tale:\s*(\S+)', line)
        if m:
            cur = {'tale': m.group(1), 'name': '', 'moves': [], 'shared': None}
            tales.append(cur); continue
        if cur is None: continue
        m = re.match(r'^name:\s*(.*)', line)
        if m: cur['name'] = m.group(1).strip(); continue
        m = re.match(r'^move:\s*([^|]+)\|\s*(.*)', line)
        if m:
            cur['moves'].append({'label': m.group(1).strip(), 'raw': m.group(2).strip()})
            continue
        m = re.match(r'^shared:\s*\|?\s*(.*)', line)
        if m:
            cur['shared'] = m.group(1).strip(); continue
    return tales

def resolve(tale):
    """produce the flat move-strings for one tale"""
    out = []
    shared = tale['shared']
    for mv in tale['moves']:
        raw = mv['raw']
        uses_shared = '<<shared>>' in raw
        raw = raw.replace('<<shared>>', '').strip()
        s = strip_marks(raw)
        if uses_shared and shared:
            s = (s + ' ' + shared).strip()
        canon, full = split_overflow(s)
        out.append({'tale': tale['tale'], 'move': mv['label'],
                    'canonical': canon, 'full': full,
                    'shared_tail': bool(uses_shared)})
    return out

def opener(canon):
    """the move's opening crisis -- must be A, a, or B (p.37, p.92).

    Must see through Propp's own decorations to find it:
      [ x ]   bracket: a crisis not underscored by the tale is still a crisis
      { x ..  a move may open with its repeated block; the crisis is inside
      leading non-crisis tokens (a parked F, an o) are skipped
    The first A/a/B token, ignoring [ ] { } and variety marks, is the opener."""
    toks = canon.replace('{', ' ').replace('}', ' ').replace('[', ' ').replace(']', ' ')
    toks = toks.replace('/', ' ').split()
    for t in toks:
        b = re.match(r'\*?([AaB])', t)
        if b:
            return b.group(1)
        # stop only at a genuine function that isn't a legal pre-crisis element
        # (pre-crisis: the parked overflow was already stripped for canonical)
    return None

CANON_HEADER = """\
# STAGE 1 OUTPUT -- resolved move-strings, ready for the regular move grammar.
# Generated by resolve.py from {src}.
# {ntales} tales -> {nmoves} move-strings.
#
# canonical = overflow and parked cells dropped (this is what the ORDER test sees)
# full      = as printed, overflow and parked cells kept and marked
# +tail     = a shared ending was unfolded onto this move (Propp method 5).
#             THE UNFOLD IS FOR TESTING WELL-FORMEDNESS ONLY. Propp prints
#             that tail ONCE, after both moves. Each +tail move carries a
#             copy so it can be parsed alone, so this file OVER-COUNTS those
#             cells. Do not tally function frequencies from it: 125's tail is
#             L Q Ex U W* and 155's is ↓X, each counted twice here and once
#             on the page. Tale 162 is NOT one of these -- its brace closes a
#             move resumed after the <II> interruption, so its ↓ W* is Move
#             I's alone.
#
"""

def write_canonical(path, src, tales, allmoves):
    """write the three-field record file that falsify44.py reads.

    Fields are tab-separated: tale, move label, canonical string. The move
    label carries the ' +tail' flag inline, as field 2 is opaque to every
    consumer. THIS FILE IS GENERATED -- regenerate rather than edit.
    """
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(CANON_HEADER.format(src=src, ntales=len(tales), nmoves=len(allmoves)))
        for m in allmoves:
            label = m['move'] + (' +tail' if m['shared_tail'] else '')
            f.write(f"{m['tale']}\t{label}\t{m['canonical']}\n")

if __name__ == '__main__':
    flags = {'-o'}
    unknown = [a for a in sys.argv[1:]
               if a.startswith('-') and a not in flags]
    if unknown:
        sys.exit("resolve.py: unknown option %s" % unknown[0])
    args = [a for a in sys.argv[1:]]
    out = None
    if '-o' in args:
        i = args.index('-o')
        if i + 1 >= len(args):
            sys.exit("resolve.py: -o needs a filename, e.g. -o ResolvedMoves.txt")
        out = args[i + 1]
        del args[i:i + 2]
    path = args[0] if args else 'TaleTokenStreamsV4Utf8.txt'
    tales = parse_corpus(path)
    allmoves = []
    for t in tales:
        allmoves += resolve(t)
    if out:
        write_canonical(out, path, tales, allmoves)
        print(f"wrote {out}: {len(allmoves)} move-strings from {len(tales)} tales\n")
    print(f"{len(tales)} tales  ->  {len(allmoves)} move-strings\n")
    bad = []
    for m in allmoves:
        op = opener(m['canonical'])
        flag = '' if op in ('A','a','B') else f'  <-- opens on {op!r}, not A/a/B'
        if flag: bad.append(m)
        tail = ' +tail' if m['shared_tail'] else ''
        print(f"  {m['tale']:>4} {m['move']:<7}{tail:6} | {m['canonical']}{flag}")
    print(f"\nmove-strings not opening on A/a/B: {len(bad)}")
    for m in bad:
        print(f"  {m['tale']} {m['move']}: {m['canonical']}")
