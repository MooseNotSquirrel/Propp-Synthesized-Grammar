#!/usr/bin/env python3
"""
revealedVillain.py -- the revealed villain, route (a), from the tables (FailedHero/RevealedVillainProtocol.md, frozen
2026-10-28).

  python revealedVillain.py r1    test R1: the invented stories of R1Stories.txt give their known answers
  python revealedVillain.py r4    test R4: two runs byte-identical
  python revealedVillain.py dry   counts only: stories, judged heroes found, stories with an Ex, stories with a Q
  python revealedVillain.py run   write FailedHero/RevealedVillainTables.txt
  python revealedVillain.py setup-b --dry   route (b): say what the reader stage would write, and write nothing
  python revealedVillain.py setup-b         write the stage's inputs and prompts into ActsRoles, and the item key here

A story counts when its judged hero is the undergoer of an exposure (Ex), or of a recognition (Q) that follows a
villainy (A) in the same story. The hero is the judged hero as failedHero.py finds it (mended 2026-10-28); stories whose
readers named no single hero, or none, are left out, and the myths take no part. Every figure per transcriber. The
route's known false positive, recorded in R1: a hero recognized after another's villainy counts.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import failedHero as F  # noqa: E402

CORPORA = ['tale', 'animal', 'fable', 'tragedy']
OUT = os.path.join(HERE, 'RevealedVillainTables.txt')


def revealed(funcs, hero):
    """funcs: [(function, performer, undergoer)] in order"""
    seen_a = False
    for fn, p, u in funcs:
        if fn == 'A':
            seen_a = True
        if u == hero and (fn == 'Ex' or (fn == 'Q' and seen_a)):
            return True
    return False


def r1():
    ok, cur, out = True, None, []
    for l in open(os.path.join(HERE, 'R1Stories.txt'), encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('story '):
            w = l.split()
            cur = [w[1], w[3], []]
        elif l.startswith('expect ') and cur:
            got = 'Y' if revealed(cur[2], cur[1]) else 'N'
            want = l.split('=')[1].strip()
            good = got == want
            ok &= good
            print('R1 %-40s %s' % (cur[0], 'pass' if good else 'FAIL: expected %s, got %s' % (want, got)))
        elif ' | ' in l and cur:
            cur[2].append(tuple(x.strip() for x in l.split('|')))
    print('R1 %s' % ('PASS' if ok else 'FAIL'))
    return ok


def per_story(L, g, T, J):
    out = []
    for s, (n, ents) in F.stories(L, g).items():
        chars = T.get((g, L, s), {})
        h, how = F.heroes(g, L, s, chars, J)
        if h is None:
            out.append((s, None, how, None))
            continue
        # one function a position: the parts of a split field keep their function's place
        funcs = [(fn, p, u) for i, fn, neg, p, u in ents]
        out.append((s, h, how, revealed(funcs, h)))
    return out


def dry():
    T, J = F.table(), F.judged()
    for g in CORPORA:
        for L in 'AB':
            st = F.stories(L, g)
            ps = per_story(L, g, T, J)
            print('%-8s %s stories %3d, judged hero found %3d, stories with an Ex %3d, with a Q %3d'
                  % (g, L, len(st), sum(1 for x in ps if x[1]), sum(1 for n, ents in st.values() if any(e[1] == 'Ex' for e in ents)),
                     sum(1 for n, ents in st.values() if any(e[1] == 'Q' for e in ents))))


def report():
    T, J = F.table(), F.judged()
    out = ['# RevealedVillainTables.txt -- revealedVillain.py: route (a) of FailedHero/RevealedVillainProtocol.md (frozen 2026-10-28), per transcriber',
           '# the hero revealed: the undergoer of an Ex, or of a Q after an A; the hero the judged hero, mended; the myths take no part']
    M = {}
    for g in CORPORA:
        for L in 'AB':
            ps = per_story(L, g, T, J)
            M[(g, L)] = ps
            ms = [x for x in ps if x[1]]
            yes = sorted(s for s, h, how, r in ms if r)
            out.append('%-12s %s: judged heroes %3d, revealed %3d (%.0f%%): %s' % (F.NAMES[g], L, len(ms), len(yes),
                       100 * F.share([bool(r) for s, h, how, r in ms]), ' '.join(yes) or 'none'))
    out.append('')
    out.append('== prediction 2 (route a): permutation test, %d permutations, p at most 0.05; floor %d stories a side' % (F.PERMS, F.FLOOR))
    held = {}
    for L in 'AB':
        t = [bool(r) for s, h, how, r in M[('tragedy', L)] if h]
        w = [bool(r) for s, h, how, r in M[('tale', L)] if h]
        if len(t) < F.FLOOR or len(w) < F.FLOOR:
            held[L] = None
            out.append('  2. %s: NOT TESTABLE (floor): tragedies %d, wondertales %d' % (L, len(t), len(w)))
            continue
        d, p = F.perm_p(t, w, lambda a, b: F.share(a) - F.share(b))
        held[L] = d > 0 and p <= 0.05
        out.append('  2. %s: revealed, tragedies %.0f%% (%d) against wondertales %.0f%% (%d): difference %+.0f points, p %.4f: %s'
                   % (L, 100 * F.share(t), len(t), 100 * F.share(w), len(w), 100 * d, p, 'holds' if held[L] else 'does not hold'))
    out.append('  2. by the tables, the hero revealed in more tragedies than wondertales: %s' % F.verdict(held['A'], held['B']))
    return '\n'.join(out) + '\n'


def r4():
    ok = report() == report()
    print('R4 two runs byte-identical: %s' % ('PASS' if ok else 'FAIL'))
    return ok


# ---------------------------------------------------------------- route (b): the reader stage
AR = os.path.join(os.path.dirname(F.ROOT), 'ActsRoles')
BATCHES = [('r1', 'tragedy'), ('r2', 'tale')]
# R3: named by the keeper from the events before the stage (2026-10-28); P03 is Oedipus at Colonus, whose crime is known
# from the start, so the protocol's "Oedipus P03" gives way to P20, Oedipus the King
CONTROLS = {'P20': 'yes', 'P26': 'yes', 'P13': 'yes', 'A095': 'no', 'A098': 'no', 'A100': 'no'}
QUESTION = ('Does the story reveal, at some point, that its hero is himself the cause of the harm the story turns on, whether he did it '
            'before the story begins or during it, knowingly or not? Answer yes or no, give the number of the event where it is '
            'revealed, and one sentence of reason.')
PROMPT_B = """You are reading the events of stories and answering one question about each. You start with no background on the project, and you should not look for any.

Read revealed/input/{b}.txt in this repository in full. It holds {n} stories. Each begins with a line

=== ITEM | STORY | TITLE | HERO

followed by the story's events, one a line, each with its number. The HERO is the character two earlier readers named as the story's hero.

For each story, answer this question, from the events only:

{q}

Open only revealed/input/{b}.txt. Do not open, list or search any other file or folder in this repository, in particular nothing under revealed/answers/ but your own folder. Do not search the web. You are reader {L}.

Write one file, and nothing else, revealed/answers/{L}/{b}/Answers.txt (create the folders): one line per story, in the order of the file, in the form

ITEM | ANSWER | EVENT | REASON

where ANSWER is yes or no, EVENT is the number of the event where it is revealed (write 0 when the answer is no), and REASON is one short sentence. Keep any working file inside revealed/answers/{L}/{b}/ and delete it before you finish.

Then reply with a short report: the number of stories, how many you answered yes, and any you found hard to decide, with their item numbers.
"""


def stage_items():
    """[(batch, [(item, story, title, hero, [(event, text)])])]: the stories of the tragedies and wondertales with a judged
    hero, none for a "no single hero" entry"""
    J = F.judged()
    ev = F.collections.defaultdict(list)
    for r in F.DT.rows('events'):
        ev[r['story']].append((int(r['event']), r['text'].replace('|', '/').strip()))
    ti = {r['story']: r['title'].replace('|', '/').strip() for r in F.DT.rows('stories')}
    out = []
    for b, g in BATCHES:
        its = []
        for s in F.stories('A', g):
            gid = g + ':' + s
            if s not in J or F.no_single(J[s]) or not ev.get(gid):
                continue
            its.append(('%s-%03d' % (b, len(its) + 1), s, ti.get(gid, ''), J[s], sorted(ev[gid])))
        out.append((b, its))
    return out


def setup_b(dry):
    batches = stage_items()
    writes, key = [], ['item\tstory\thero\tcontrol']
    for b, its in batches:
        text = ''.join('=== %s | %s | %s | %s\n%s' % (i, s, t, h, ''.join('%d: %s\n' % e for e in evs)) for i, s, t, h, evs in its)
        writes.append((os.path.join(AR, 'revealed', 'input', b + '.txt'), text))
        for L in 'AB':
            writes.append((os.path.join(AR, 'prompts', 'revealed-%s-%s.txt' % (L, b)), PROMPT_B.format(b=b, n=len(its), q=QUESTION, L=L)))
        key += ['\t'.join((i, s, h, CONTROLS.get(s, ''))) for i, s, t, h, evs in its]
        print('%s %-8s stories %2d, events %4d, controls %d (%s)' % (b, dict(BATCHES)[b], len(its), sum(len(x[4]) for x in its),
              sum(1 for x in its if x[1] in CONTROLS), ' '.join('%s=%s' % (x[1], CONTROLS[x[1]]) for x in its if x[1] in CONTROLS)))
    missing = sorted(set(CONTROLS) - {x[1] for b, its in batches for x in its})
    if missing:
        raise SystemExit('controls not among the items: %s' % ' '.join(missing))
    writes.append((os.path.join(HERE, 'RevealedItems.tsv'), '\n'.join(key) + '\n'))
    for path, text in writes:
        if os.path.exists(path):
            raise SystemExit('refusing to overwrite %s' % path)
        print('%s %-46s %7d bytes' % ('would write' if dry else 'write', os.path.relpath(path, os.path.dirname(F.ROOT)), len(text.encode('utf-8'))))
    if dry:
        print('dry run: %d files; nothing written' % len(writes))
        return
    for path, text in writes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print('written: %d files' % len(writes))


def run():
    text = report()
    if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != text:
        raise SystemExit('refusing to overwrite the record %s' % OUT)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    cmds = {'r1': r1, 'r4': r4, 'dry': dry, 'run': run}
    a = sys.argv[1:]
    if a in (['setup-b', '--dry'], ['setup-b']):
        setup_b(len(a) == 2)
        sys.exit(0)
    if len(a) != 1 or a[0] not in cmds:
        sys.exit(__doc__)
    r = cmds[a[0]]()
    sys.exit(0 if r in (None, True) else 1)
