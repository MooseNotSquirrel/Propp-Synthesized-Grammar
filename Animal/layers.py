#!/usr/bin/env python3
"""
layers.py -- the animal tales described in acts, significance and free verbs (LayersProtocol.md).

  python layers.py setup        writes the prompts for animal-acts and animal-free into Story Language/ActsRoles
  python layers.py form-acts    checks the act descriptions' form
  python layers.py form-free    checks the free descriptions' form
  python layers.py setup-sig    writes the significance describers' inputs and prompts (after form-acts)
  python layers.py form-sig     checks the significance descriptions' form
  python layers.py selftest     the scorer with the problem test's fables, then random descriptions, standing in
  python layers.py score        writes Animal/LayersRun.txt

Written in full before any animal tale was described in acts, significance or free verbs. The instruments are
the problem test's and the bottom-up test's, unchanged: ActsRules.md, SigRules.md, FreeRules.md, and the
measures, null and permutation test of Problems/problems.py.
"""
import collections
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
for d in ('Problems', 'Free'):
    sys.path.insert(0, os.path.join(ROOT, d))
import problems as Pm  # noqa: E402
import free as F  # noqa: E402

S = Pm.S
OUT = os.path.join(P, 'ActsRoles')
BASE = os.path.join(OUT, 'animal')
TALES = ['A%03d' % i for i in range(1, 51)]
BATCHES = collections.OrderedDict([('b1', TALES[:17]), ('b2', TALES[17:34]), ('b3', TALES[34:])])
SIG_BATCHES = collections.OrderedDict(('q%d' % (i + 1), TALES[10 * i:10 * i + 10]) for i in range(5))
SEED, PERMS = Pm.SEED, Pm.PERMS
PREDICTIONS = [('hero opens', +1), ('repaired', -1), ('acts help', -1), ('acts harm', +1)]
# (measure, direction): the animal tales differ from the tale in that direction, and their own excess over the
# null points that way; both by at least Pm.MIN_EFFECT with one-sided p at most 0.05, for both describers.
REPORT = []


def say(s=''):
    REPORT.append(s)
    print(s)


# ---------------------------------------------------------------- material and prompts
def events():
    """{story: [(event, text)]} from the event lists"""
    out = collections.defaultdict(list)
    for l in open(os.path.join(BASE, 'Events.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|', 2)]
        if len(f) == 3 and re.match(r'^A\d{3}$', f[0]):
            out[f[0]].append((int(f[1]), f[2]))
    return out


def heroes():
    out = {}
    for l in open(os.path.join(BASE, 'Heroes.txt'), encoding='utf-8'):
        m = re.match(r'^(A\d{3}) \| hero: ([^|]*)', l)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def title(s):
    return open(os.path.join(BASE, 'tales', s + '.txt'), encoding='utf-8').readline().split('|')[1].strip()


WHAT = "some animal tales from Aleksandr Afanasyev's collection of Russian folktales"


def files(ids):
    return ', '.join('animal/tales/%s.txt' % s for s in ids)


ACTS_PROMPT = ("You are describing what happens in {what}. You start with no background on the project, and you should not look for any.\n\n"
               "Read ActsRules.md in this repository first, in full, and follow it exactly. Your tales are these {n}, one per file, read in their original language: {files}. Their events are in animal/Events.txt.\n\n"
               "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its act, performer, undergoer, relation and Y or N.\n\n"
               "Open only ActsRules.md, {files}, animal/Events.txt and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under animal/transcriptions/, animal/free/ or animal/sig/, and nothing under animal/acts/ but your own folder. Do not search the web. You are describer {L}.\n\n"
               "Write one file, and nothing else, animal/acts/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on, in the original language.\n\n"
               "Then reply with the report the rules' last section asks for.\n")

FREE_PROMPT = ("You are describing what happens in {what}. You start with no background on the project, and you should not look for any.\n\n"
               "Read free/FreeRules.md in this repository first, in full, and follow it exactly. Your tales are these {n}, one per file, read in their original language: {files}. Their events are in animal/Events.txt; write the verbs and phrases in English.\n\n"
               "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its verb, phrase, performer, undergoer and Y or N.\n\n"
               "Open only free/FreeRules.md, {files}, animal/Events.txt and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under animal/transcriptions/, animal/acts/ or animal/sig/, and nothing under animal/free/ but your own folder. Do not search the web. You are describer {L}.\n\n"
               "Write one file, and nothing else, animal/free/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on, in the original language.\n\n"
               "Then reply with the report the rules' last section asks for.\n")

SIG_PROMPT = S.PROMPT.replace('sig/input/{L}-{b}.txt', 'animal/sig/input/{L}-{b}.txt').replace(
    'nothing else under sig/ and nothing under any acts/ folder',
    'nothing else under sig/ or animal/sig/, and nothing under animal/acts/, animal/free/ or animal/transcriptions/').replace(
    'sig/{L}/{b}/Significance.txt', 'animal/sig/{L}/{b}/Significance.txt')


def write(name, text):
    open(os.path.join(OUT, 'prompts', name), 'w', encoding='utf-8', newline='\n').write(text)


def setup():
    for L in 'AB':
        for b, ids in BATCHES.items():
            kw = dict(what=WHAT, n=len(ids), files=files(ids), L=L, b=b)
            write('aacts-%s-%s.txt' % (L, b), ACTS_PROMPT.format(**kw))
            write('afree-%s-%s.txt' % (L, b), FREE_PROMPT.format(**kw))
    print('prompts written: aacts-* and afree-*, %d each' % (2 * len(BATCHES)))


# ---------------------------------------------------------------- reading
def act_lines(L, b, base=None):
    """[(story, event, act, performer, undergoer, relation, matters, note)], faults"""
    path = os.path.join(base or BASE, 'acts', L, b, 'Notes.txt')
    if not os.path.exists(path):
        return [], ['%s %s: no file' % (L, b)]
    out, faults = [], []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|', 9)]
        if len(f) < 10 or not re.match(r'^A\d{3}', f[0]):
            continue
        ev = re.search(r'\d+', f[1])
        s = f[0].split('/')[0]
        if not ev or s not in BATCHES[b]:
            faults.append('%s %s line %d: story or event' % (L, b, i))
            continue
        out.append((s, int(ev.group()), f[2].lower(), f[3], f[4], f[5].lower(), f[6][:1].upper(), f[9]))
    return out, faults


def form_acts():
    E = events()
    total = 0
    for L in 'AB':
        for b, ids in BATCHES.items():
            rows, faults = act_lines(L, b)
            got = collections.defaultdict(set)
            for r in rows:
                got[r[0]].add(r[1])
            unknown = sum(1 for r in rows if r[2] not in F.N.T.ACTS)
            missing = sum(len({k for k, _ in E[s]} - got[s]) for s in ids)
            print('%s %s entries %4d, events missing %3d, unknown acts %3d, faults %d' % (L, b, len(rows), missing, unknown, len(faults)))
            total += missing + unknown + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def free_lines(L, b):
    path = os.path.join(BASE, 'free', L, b, 'Notes.txt')
    if not os.path.exists(path):
        return [], ['%s %s: no file' % (L, b)]
    out, faults = [], []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        f = [x.strip() for x in line.rstrip('\n').split('|', 8)]
        if len(f) < 9 or not re.match(r'^A\d{3}', f[0]):
            continue
        ev = re.search(r'\d+', f[1])
        s = f[0].split('/')[0]
        v = F.verb_of(f[2])
        if not ev or s not in BATCHES[b] or not v or f[6][:1].upper() not in 'YN':
            faults.append('%s %s line %d' % (L, b, i))
            continue
        out.append((s, int(ev.group()), v))
    return out, faults


def form_free():
    E = events()
    total = 0
    for L in 'AB':
        for b, ids in BATCHES.items():
            rows, faults = free_lines(L, b)
            got = collections.defaultdict(set)
            for s, ev, _ in rows:
                got[s].add(ev)
            missing = sum(len({k for k, _ in E[s]} - got[s]) for s in ids)
            print('%s %s entries %4d, events missing %3d, faults %d' % (L, b, len(rows), missing, len(faults)))
            total += missing + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def inputs(base=None):
    """{(L, q): [(entry id, story, event, act, performer, undergoer, relation)]}, and the input texts"""
    E, Hn = events(), heroes()
    out, text = {}, {}
    for L in 'AB':
        ents = [r for b in BATCHES for r in act_lines(L, b, base)[0]]
        n = 0
        for q, ids in SIG_BATCHES.items():
            rows, lines = [], []
            for s in ids:
                lines.append('story: %s | %s | hero: %s' % (s, title(s), Hn[s]))
                for k, t in E[s]:
                    mine = [r for r in ents if r[0] == s and r[1] == k]
                    if not mine:
                        continue
                    lines.append('  ev %d | %s' % (k, t))
                    for _, ev, a, pf, u, r, _, note in mine:
                        n += 1
                        eid = 'e%04d' % n
                        rows.append((eid, s, ev, a, pf, u, r))
                        lines.append('    %s | %s | %s | %s | %s | %s' % (eid, a, pf, u, r, note))
                lines.append('')
            out[L, q] = rows
            text[L, q] = '\n'.join(lines) + '\n'
    return out, text


def setup_sig():
    rows, text = inputs()
    os.makedirs(os.path.join(BASE, 'sig', 'input'), exist_ok=True)
    for (L, q), t in text.items():
        open(os.path.join(BASE, 'sig', 'input', '%s-%s.txt' % (L, q)), 'w', encoding='utf-8', newline='\n').write(t)
        ids = SIG_BATCHES[q]
        where = ("Your stories are animal tales from Aleksandr Afanasyev's collection of Russian folktales; each tale's text is in its own file, in Russian: %s."
                 % files(ids))
        write('asig-%s-%s.txt' % (L, q), SIG_PROMPT.format(L=L, b=q, n=len(ids), m=len(rows[L, q]), where=where, files=files(ids)))
    print({q: (len(rows['A', q]), len(rows['B', q])) for q in SIG_BATCHES})


def read_sig(L, q):
    saved = S.SIG
    S.SIG = os.path.join(BASE, 'sig')
    try:
        if not os.path.exists(os.path.join(S.SIG, L, q, 'Significance.txt')):
            return {}, {}, ['%s %s: no file' % (L, q)]
        return S.read_sig(L, q)
    finally:
        S.SIG = saved


def form_sig():
    rows, _ = inputs()
    total = 0
    for (L, q), rs in sorted(rows.items()):
        sig, probs, faults = read_sig(L, q)
        missing = [r[0] for r in rs if r[0] not in sig]
        extra = sorted(set(sig) - {r[0] for r in rs})
        print('%s %s acts %4d, described %4d, missing %3d, unknown ids %d, problem lines %3d, faults %d'
              % (L, q, len(rs), len(sig), len(missing), len(extra), len(probs), len(faults)))
        total += len(missing) + len(extra) + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def described_animal():
    rows, _ = inputs()
    out = {L: collections.defaultdict(list) for L in 'AB'}
    for (L, q), rs in rows.items():
        sig, _, _ = read_sig(L, q)
        for eid, s, ev, a, pf, u, r in rs:
            d = sig.get(eid)
            if d:
                part, value, place, prob = d[:4]
                out[L][s].append({'id': eid, 'event': ev, 'act': a, 'part': part, 'value': value, 'place': place, 'problem': prob})
    return out


# ---------------------------------------------------------------- the measures
def trickster(xs):
    """the share of the hero's own acts that are deceiving; None if the hero does nothing"""
    mine = [x for x in xs if x['part'] in ('does', 'both')]
    return sum(x['act'] == 'deceive' for x in mine) / float(len(mine)) if mine else None


def flip_p(x, sign, rnd):
    """one-sided sign-flip test that the mean of x, times sign, is above 0"""
    obs = sign * Pm.mean(x)
    k = 0
    for _ in range(PERMS):
        if sign * Pm.mean([v if rnd.random() < 0.5 else -v for v in x]) >= obs - 1e-12:
            k += 1
    return (k + 1) / float(PERMS + 1)


def evaluate(D, gen, label='animal'):
    """D: {L: {story: entries}}, gen: {story: genre} with 'animal' for the new stories. Returns the verdicts."""
    saved = Pm.GENRES
    Pm.GENRES = ('tale', 'fable', 'tragedy', 'animal')
    try:
        ex, raw = Pm.excess(D, gen)
    finally:
        Pm.GENRES = saved
    say('stories: %s' % ', '.join('%s %s %d' % (L, g, len(raw[L][g]['problems'])) for L in 'AB' for g in ('tale', 'fable', 'tragedy', 'animal')))
    say('%-14s %s %14s %14s %14s %14s' % ('measure', 'L', 'tale', 'fable', 'tragedy', label))
    for m in Pm.MEASURES:
        for L in 'AB':
            say('%-14s %s ' % (m, L) + ' '.join('%7.2f/%+6.2f' % (Pm.mean(raw[L][g][m]), Pm.mean(ex[L][g][m]) if ex[L][g][m] else float('nan'))
                                               for g in ('tale', 'fable', 'tragedy', 'animal')))
    say()
    rnd = random.Random(SEED)
    v = []
    for i, (m, sign) in enumerate(PREDICTIONS, 1):
        ok, parts = True, []
        for L in 'AB':
            x, y = ex[L]['animal'][m], ex[L]['tale'][m]
            d = sign * (Pm.mean(x) - Pm.mean(y))
            p1 = Pm.perm_p(list(x), list(y), sign, rnd)
            p2 = flip_p(list(x), sign, rnd)
            good = d >= Pm.MIN_EFFECT and p1 <= 0.05 and sign * Pm.mean(x) >= Pm.MIN_EFFECT and p2 <= 0.05
            ok = ok and good
            parts.append('%s against tale %+.2f p %.4f, own excess %+.2f p %.4f' % (L, d, p1, Pm.mean(x), p2))
        v.append(ok)
        say('  %d. %-13s %s than the tale and than its null: %s   %s'
            % (i, m, 'higher' if sign > 0 else 'lower', 'HOLDS' if ok else 'FAILS', '; '.join(parts)))
    say()
    say("REPORTED, the trickster: the mean share of the hero's own acts that are deceiving")
    for L in 'AB':
        say('  %s: %s' % (L, ', '.join('%s %.2f' % (g.replace('animal', label), Pm.mean([t for t in (trickster(xs) for s, xs in D[L].items() if gen.get(s) == g and xs) if t is not None]))
                                       for g in ('tale', 'fable', 'tragedy', 'animal'))))
    return v


def reference():
    D = Pm.described()
    return D, dict(Pm.genre_of())


def free_report():
    say('THE FREE VERBS, reported and not judged (the bottom-up test\'s measures on the animal tales alone)')
    strings, by_ev, acts = {}, {}, {}
    for L in 'AB':
        st, be = collections.OrderedDict(), collections.defaultdict(list)
        for b in BATCHES:
            for s, ev, v in free_lines(L, b)[0]:
                st.setdefault(s, []).append(v)
                be[(s, ev)].append(v)
        strings[L], by_ev[L] = st, be
        e = collections.defaultdict(list)
        for b in BATCHES:
            for r in act_lines(L, b)[0]:
                e[(r[0], r[1])].append(r[2])
        acts[L] = e
    al = F.alignment(by_ev, acts)
    for x, y in F.SIX + [('plead', 'respond')]:
        cells = []
        for L in 'AB':
            acc, ch, n = F.split_accuracy(by_ev, acts, L, x, y)
            cells.append('%s n %d, accuracy %s, chance %s' % (L, n, '%.2f' % acc if acc is not None else '-', '%.2f' % ch if ch is not None else '-'))
        say('  %s / %s: %s' % (x, y, '; '.join(cells)))
    for x, y, c, ok, shp in F.pairs(strings):
        dx = [F.dominant(al[L], x) for L in 'AB']
        dy = [F.dominant(al[L], y) for L in 'AB']
        say('  pair %s -> %s (%s) %s, acts %s -> %s' % (x, y, 'adjacent' if c == 1 else 'near', 'confirmed' if ok else 'not confirmed', dx, dy))


def score():
    D, gen = reference()
    A = described_animal()
    for L in 'AB':
        D[L] = dict(D[L])
        D[L].update(A[L])
    gen.update({s: 'animal' for s in TALES})
    say('# LayersRun.txt -- layers.py score, as LayersProtocol.md freezes it.')
    say()
    v = evaluate(D, gen)
    say()
    say('PREDICTIONS (LayersProtocol.md): %d of 4 hold' % sum(v))
    say()
    free_report()
    open(os.path.join(HERE, 'LayersRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(REPORT) + '\n')


def selftest():
    D, gen = reference()
    say('=== SELF-TEST 1: the problem test\'s 41 fables standing in for the animal tales (relabelled; they leave the fable column)')
    g1 = {s: ('animal' if g == 'fable' else g) for s, g in gen.items()}
    v = evaluate(D, g1, label='stand-in')
    say('  %d of 4 hold' % sum(v))
    say()
    say('=== SELF-TEST 2: random descriptions standing in: the 22 tales\' acts, each act\'s part, value and place drawn from the pooled descriptions')
    rnd = random.Random(SEED)
    D2 = {}
    g2 = dict(gen)
    for L in 'AB':
        pool = [(x['part'], x['value'], x['place']) for xs in D[L].values() for x in xs]
        D2[L] = dict(D[L])
        for s, xs in D[L].items():
            if gen.get(s) == 'tale':
                labels = sorted({x['problem'] for x in xs if x['problem'] not in ('-', '')}) or ['p1']
                ys = []
                for x in xs:
                    part, value, place = rnd.choice(pool)
                    ys.append(dict(x, part=part, value=value, place=place, problem=rnd.choice(labels)))
                D2[L]['R' + s] = ys
                g2['R' + s] = 'animal'
    v = evaluate(D2, g2, label='random')
    say('  %d of 4 hold' % sum(v))
    open(os.path.join(HERE, 'LayersSelfTest.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(REPORT) + '\n')


if __name__ == '__main__':
    cmds = {'setup': setup, 'form-acts': form_acts, 'form-free': form_free, 'setup-sig': setup_sig, 'form-sig': form_sig,
            'selftest': selftest, 'score': score}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
