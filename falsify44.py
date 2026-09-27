#!/usr/bin/env python3
"""
falsify44.py -- STAGE 2 + 3: run the frozen v44 grammar over the resolved moves.

The v44 move grammar is REGULAR (ProppEBNF44.txt): an opener (A|a|B) followed
by Propp's canonical functions in order, each optional, each optionally repeated.
Recognition is therefore a single left-to-right pass:

  1. reduce every token to its base function and its canonical RANK
  2. the opener must be A, a, or B
  3. ranks must never DECREASE (canonical order as subsequence) -- equal is fine
     (a function may recur); a strict decrease is an order violation
  4. a brace { X / Y } is a repetition or a branching, ruling 68: each
     member is checked on its own, starting no earlier than the floor,
     and the floor afterwards is the highest rank the brace reached

The grammar is FROZEN. This program reports pass/fail. It does not modify v44.
A failed PRINTED, non-overflow move is a FINDING, not a bug to patch.

The slot sequence is READ FROM THE GRAMMAR at run time, the way
checkNotation.py reads its productions from the notation spec, so the
recognizer and the grammar cannot drift apart. A slot is a POSITION in the
sequence. Propp's function numbers VIII-XXXI (p.26-66) are carried beside the
slots for reporting only and are no longer the key: function XVII holds TWO
slots, the combat wound in the struggle run and the ring or towel between M
and N (p.104). The preparatory functions I-VII are not in the scheme and hold
no slot here.
"""
import os, re, sys

# --------------------------------------------------------------------------
# THE SLOT SEQUENCE, READ FROM THE GRAMMAR AT RUN TIME
# --------------------------------------------------------------------------
# The order is not restated in this program. It is read out of the grammar
# file, so an edit to the grammar reaches the recognizer without a code
# change, and a symbol the grammar names but this program does not know is a
# HARD STOP rather than a silent divergence.
#
# Three things are not in the grammar file and stay here:
#   NUMBER  Propp's function number, for reporting only. Two slots may carry
#           the same number -- J is XVII in the struggle run and XVII again
#           between M and N.
#   ALIAS   spellings the corpus uses that the grammar does not name: KF,
#           liquidation in form F, at K's slot; w, the rudimentary form, at
#           W's slot.
#   the arrow glyph names, handled in reduce() below.
GRAMMAR = 'ProppEBNF44.txt'

NUMBER = {
    'A':8, 'a':8,       # VIII villainy / VIIIa lack   (opener)
    'B':9,              # IX mediation                  (also opener)
    'C':10,             # X beginning counteraction
    'up':11,            # XI departure          (up-arrow)
    'D':12,             # XII first donor function
    'E':13,             # XIII hero's reaction
    'F':14,             # XIV receipt of agent
    'G':15,             # XV spatial transference
    'H':16,             # XVI struggle
    'J':17,             # XVII branding         (TWO slots; see p.104)
    'I':18,             # XVIII victory
    'K':19,             # XIX liquidation
    'down':20,          # XX return             (down-arrow)
    'Pr':21,            # XXI pursuit
    'Rs':22,            # XXII rescue
    'o':23,             # XXIII unrecognized arrival
    'L':24,             # XXIV unfounded claims
    'M':25,             # XXV difficult task
    'N':26,             # XXVI solution
    'Q':27,             # XXVII recognition
    'Ex':28,            # XXVIII exposure
    'T':29,             # XXIX transfiguration
    'U':30,             # XXX punishment
    'W':31,             # XXXI wedding / reward
}
ALIAS = {'K': ('KF',), 'W': ('w',)}


def resolve_file(name):
    """Return the name if it is on disk, else None. Ruling 63 closed the
    spelling question: no name in the set carries a space or an underscore."""
    if os.path.exists(name):
        return name
    return None


def load_grammar(name=GRAMMAR):
    """Build the ordered slot list from the opener and tail productions.

    Returns [(accepted_keys, propp_number), ...] in the grammar's own order.
    Exits on any symbol with no function number here: that means the grammar
    moved and this table did not, which is the failure this design exists to
    make impossible to miss."""
    path = resolve_file(name)
    if path is None:
        raise SystemExit('%s: not found' % name)
    with open(path, 'rb') as fh:
        text = fh.read().decode('utf-8').replace('\r\n', '\n')
    prods, cur = {}, None
    for raw in text.split('\n'):
        line = raw.split('#')[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r'^(\w+)\s*=\s*(.*)$', line)
        if m and not line[:1].isspace():
            cur = m.group(1)
            prods[cur] = m.group(2)
        elif cur is not None:
            prods[cur] += ' ' + line.strip()
    slots, seen = [], set()
    for prod in ('opener', 'tail'):
        if prod not in prods:
            raise SystemExit('%s: no %s production' % (name, prod))
        for sym in re.findall(r"'([^']*)'", prods[prod]):
            if prod == 'opener' and sym in seen:
                continue                 # B is named by opener and tail alike
            if sym not in NUMBER:
                raise SystemExit('%s: no function number for %r' % (name, sym))
            slots.append(((sym,) + ALIAS.get(sym, ()), NUMBER[sym]))
            seen.add(sym)
    return slots


SLOTS = load_grammar()
SLOTNUM = [n for _keys, n in SLOTS]

# reduce() answers with a slot index. Where a key holds more than one slot the
# first is returned; advance() is what picks the right one against the floor.
RANK = {}
for _i, (_keys, _n) in enumerate(SLOTS):
    for _k in _keys:
        RANK.setdefault(_k, _i)


def slots_for(key):
    """every slot index that accepts this key, in order."""
    return [i for i, (keys, _n) in enumerate(SLOTS) if key in keys]


def advance(key, floor):
    """the earliest slot at or after the floor accepting this key, else None.

    This is the recognizer. A function holding two slots is matched against
    whichever one the walk has not yet passed, which is why M J N and H J I
    are both in the language and J H I is not."""
    for i in slots_for(key):
        if i >= floor:
            return i
    return None


MULTI = ('KF', 'Pr', 'Rs', 'Ex')     # two-letter bases, matched before single
WRAPPERS = ('overflow[', 'park[', ']', '[')   # apparatus, not functions

# COLUMN TAGS. A cell whose printed glyph disagrees with its column is written
# with a leading SUPERSCRIPT CAPITAL naming the column it stands in. The COLUMN
# carries the canonical position, so such a cell ranks by its tag and not by its
# glyph. Attested: B at 144 I, 163 I and 164 II, function B discharged in an
# assimilated M- or F-form (Propp's consequences rule, p.67); E at 137 II,
# function E discharged in a K-form. Only letters Unicode supplies as
# superscript capitals can be written this way -- C, F and Q have none -- so a
# future case in one of those columns needs a notation decision, not a silent
# fall back to the glyph. Keys are the tags; values are RANK keys.
# THE TABLE IS HELD TWICE. dagWalk.py's TAGS carries the same two
# entries. Ruling 84 keeps both rather than importing one from the
# other, and nothing checks that they still agree: edit both or neither.
COLUMN_TAG = {'ᴮ': 'B', 'ᴱ': 'E'}

# What Propp licenses to stand before the crisis opener, and nothing else.
# DERIVED FROM ProppPermittedDeviations.md, which is the frozen licence list:
#   D, E, F   p.107, the inverted sequence, DEF before A
#   up        p.107, the second inversion, the departure before A
#   T         p.108, "the most unstable function in relation to its position"
#   o, X      not functions Propp places: an arrival and Appendix IV's alien
#             forms, unorderable rather than licensed
#   None      a bracket or sign that reduces to no function
# G IS DELIBERATELY ABSENT. Propp licenses no G before A, and this list once
# carried it while omitting T, disagreeing with the licence list in BOTH
# directions. Finding FJ measured that; ruling 101 corrected it.
# deviationScan.py imports this rather than restating it (ruling 84's class).
PRE_CRISIS = ('D', 'E', 'F', 'T', 'up', 'o', 'X', None)

def reduce(tok):
    """a raw token -> (base_key, rank) or ('X', None) for unorderable / unknown.

    A cell carrying a leading column tag ranks by that tag; see COLUMN_TAG."""
    t = tok.strip()
    if t and t[0] in COLUMN_TAG:
        key = COLUMN_TAG[t[0]]
        return key, RANK[key]
    if t == '↑': return 'up', RANK['up']
    if t == '↓': return 'down', RANK['down']
    if t in ('X', 'Y', '<', '>'): return 'X', None   # unorderable, on their own
    # Wrapper openers are apparatus, never functions. resolve.py strips them
    # from the canonical string, so the walk does not normally see one -- but
    # 'overflow[' reduced to ('o', 23), the unrecognized-arrival function,
    # purely because it begins with an o. Anything reading a FULL string, or
    # any future caller that skips stage 1, would have taken that rank as real.
    if t in WRAPPERS: return None, None
    # a trailing arrow glued to a cell is a modifier, not a function: strip it
    # and rank by the base (page-verified: W*↓ ranks as W). Same for trailing X.
    stripped = t.rstrip('↑↓X')
    if stripped:
        t = stripped
    # if stripping emptied it, it was a pure arrow/X run -> handled above/below
    # strip Propp's decorations: brackets, * prefix, signs, variety digits
    t = t.strip('[]')
    t = t.lstrip('*')
    if not t: return None, None
    # X = "unclear or alien forms" (App. IV): has no canonical position
    if t[0] in ('X', 'Y', '<', '>'): return 'X', None
    for m in MULTI:
        if t.startswith(m):
            return m, RANK[m]
    c = t[0]
    key = c if c in RANK else c.upper() if c.upper() in RANK else None
    if key is None:
        return 'X', None                 # unrecognised -> treat as unorderable
    return key, RANK[key]

def tokenize(s):
    """split into tokens and brace groups. A free-standing arrow (space on both
    sides) is its own token. An arrow GLUED to a symbol stays with that symbol:
    verified on the page, W*↓ is one cell in the W column, the ↓ a modifier on
    the wedding, not a separate return function. Only pad braces and slashes."""
    s = s.replace('{', ' { ').replace('}', ' } ').replace('/', ' / ')
    return [t for t in s.split(' ') if t]

def check(canon):
    """returns (ok, floor_path, reason). ok=False on order/opener violation."""
    toks = tokenize(canon)
    if not toks:
        return False, [], 'empty'
    # opener: the first CRISIS token, seen through braces, brackets, prefixes,
    # and any parked pre-crisis overflow the resolver left in place. Per the
    # grammar the opener is A|a|B; we scan for the first token that reduces to
    # one of those, and only fail if none of the leading tokens is a crisis.
    op_key = None
    for t in toks:
        if t in ('{', '}', '/'): continue
        k, _ = reduce(t)
        if k in ('A', 'a', 'B'):
            op_key = k; break
        # allow Propp's legal pre-crisis material to precede the opener:
        # a parked donor cell (D/E/F/G), an arrival o, an up-arrow -- all of
        # which occur in the OVERFLOW area left of A. Keep scanning past them.
        if k in PRE_CRISIS:
            continue
        # anything else before a crisis is a real opener violation
        op_key = k; break
    if op_key not in ('A', 'a', 'B'):
        return False, [], f'opens on {op_key!r}, not A/a/B'

    # find the index of the opener token; everything before it is parked
    # overflow (out of canonical position) and is excluded from the order test
    # exactly as the 15 marked overflow cells are (logic doc S9).
    # BUT if a brace opens before the opener, the whole move is ONE repetition
    # group -- start at the brace, not inside it, or the brace is never seen and
    # its parallel alternatives get read as one sequential run (163, 164, 136 IV).
    start = 0
    for idx, t in enumerate(toks):
        if t == '{':
            start = idx; break
        if t in ('}', '/'): continue
        k, _ = reduce(t)
        if k in ('A', 'a', 'B'):
            start = idx; break
        if k in PRE_CRISIS:
            continue
        start = idx; break
    floor = 0
    i = start
    trace = []
    while i < len(toks):
        t = toks[i]
        if t == '{':
            # gather the brace group up to matching }
            depth = 1; j = i+1; inner = []
            while j < len(toks) and depth > 0:
                if toks[j] == '{': depth += 1
                elif toks[j] == '}': depth -= 1
                if depth > 0: inner.append(toks[j])
                j += 1
            # split alternatives on '/'
            alts, cur = [], []
            for x in inner:
                if x == '/': alts.append(cur); cur = []
                else: cur.append(x)
            alts.append(cur)
            brace_max = floor
            for alt in alts:
                f = floor
                for x in alt:
                    k, r = reduce(x)
                    if r is None:      # unorderable (X); skip
                        continue
                    nxt = advance(k, f)
                    if nxt is None:
                        return False, trace, (f'in repetition: {k}({SLOTNUM[r]})'
                                              f' < floor {SLOTNUM[f]}')
                    f = nxt
                    brace_max = max(brace_max, nxt)
            floor = brace_max
            trace.append(('{rep}', floor))
            i = j
            continue
        if t in ('}', '/'):
            i += 1; continue
        k, r = reduce(t)
        if r is None:
            trace.append((k, None)); i += 1; continue
        nxt = advance(k, floor)
        if nxt is None:
            return False, trace, (f'{k}({SLOTNUM[r]}) after floor '
                                  f'{SLOTNUM[floor]}')
        floor = nxt
        trace.append((k, nxt))
        i += 1
    return True, trace, 'ok'

def load(path):
    out = []
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 3: continue
        out.append({'tale': parts[0], 'move': parts[1], 'canon': parts[2]})
    return out

if __name__ == '__main__':
    unknown = [a for a in sys.argv[1:] if a.startswith('-')]
    if unknown:
        sys.exit("falsify44.py: unknown option %s" % unknown[0])
    path = sys.argv[1] if len(sys.argv) > 1 else 'ResolvedMoves.txt'
    moves = load(path)
    npass = nfail = 0
    fails = []
    for m in moves:
        ok, trace, reason = check(m['canon'])
        if ok: npass += 1
        else:
            nfail += 1; fails.append((m, reason))
    print(f"v44 (FROZEN) vs {len(moves)} resolved move-strings")
    print(f"  PASS: {npass}")
    print(f"  FAIL: {nfail}\n")
    if fails:
        print("FAILURES (findings, not yet triaged):")
        for m, reason in fails:
            print(f"  {m['tale']:>4} {m['move']:<8} {reason}")
            print(f"         {m['canon']}")
