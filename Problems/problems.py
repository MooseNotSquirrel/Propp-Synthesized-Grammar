#!/usr/bin/env python3
"""
problems.py -- the test of the genres' problem structures (ProblemsProtocol.md).

  python problems.py setup-acts   writes the act describers' material and prompts
                                  into Story Language/Projects/ActsRoles/problems/
  python problems.py form-acts    checks the act descriptions' form
  python problems.py setup-sig    writes the significance describers' inputs and prompts,
                                  from the act descriptions
  python problems.py form-sig     checks the significance descriptions' form
  python problems.py dev          the measures and predictions on the development
                                  stories (Significance/), for the record
  python problems.py score        scores the test; writes Problems/ProblemsRun.txt

Written in full before any description of the test stories existed.
"""
import collections
import os
import random
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Significance'))
import significance as S  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, 'Data'))
import tables as DT  # noqa: E402

T, W, H = S.T, S.W, S.H
OUT = os.path.join(P, 'ActsRoles')
BASE = os.path.join(OUT, 'problems')
GENRES = ('tale', 'fable', 'tragedy')
PLAYS = ['P%02d' % i for i in list(range(9, 17)) + list(range(25, 33))]
RELATIONS = ('kin', 'spouse', 'above', 'below', 'ally', 'enemy', 'stranger', 'divine', 'self', 'none')
SEED, PERMS = 46, 10000


# ---------------------------------------------------------------- material
def fable_ids():
    out = []
    for b in ('b3', 'b4'):
        m = re.search(r'these fables only: ([^.]*)\.', open(os.path.join(P, 'Fables', 'prompts', 'transcribe-A-%s.txt' % b),
                                                             encoding='utf-8').read())
        out += [x.strip() for x in m.group(1).split(',')]
    return out


def material():
    """{genre: {act batch: [story ids]}}: stories with a judged hero that no act describer has read"""
    J = W.judged()
    tales = [s for s in ('A%03d' % t for t in T.SPLIT['dev']) if s in J]
    fables = [s for s in fable_ids() if s in J]
    h, k = (len(tales) + 1) // 2, (len(fables) + 1) // 2
    return {'tale': {'t3': tales[:h], 't4': tales[h:]},
            'fable': {'f3': fables[:k], 'f4': fables[k:]},
            'tragedy': {'g%d' % (i + 5): PLAYS[2 * i:2 * i + 2] for i in range(8)}}


def genre_of():
    return {s: g for g, bs in material().items() for b in bs.values() for s in b}


ACT_STAGES = {'p-acts-1': ['t3', 't4', 'f3', 'f4'], 'p-acts-2': ['g5', 'g6', 'g7', 'g8'], 'p-acts-3': ['g9', 'g10', 'g11', 'g12']}
SIG_STAGES = {'p-sig-1': ['q1', 'q2', 'q3', 'q4', 'q5'], 'p-sig-2': ['q6', 'q7', 'q8', 'q9'], 'p-sig-3': ['q10', 'q11', 'q12', 'q13']}


def subset(src, dst, ids):
    with open(dst, 'w', encoding='utf-8', newline='\n') as out:
        for line in open(src, encoding='utf-8'):
            if line.split('|')[0].strip() in ids:
                out.write(line)


ACTS_PROMPT = ("You are describing what happens in {what}. You start with no background on the project, and you should not look for any.\n\n"
               "Read ActsRules.md in this repository first, in full, and follow it exactly. {where}\n\n"
               "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its act, performer, undergoer, relation and Y or N.\n\n"
               "Open only ActsRules.md, {files} and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under problems/acts/ but your own folder. Do not search the web. You are describer {L}.\n\n"
               "Write one file, and nothing else, problems/acts/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on{orig}.\n\n"
               "Then reply with the report the rules' last section asks for.\n")


def play_names():
    return {l.split('|')[0].strip(): l.split('|')[2].strip() + "'s " + l.split('|')[3].strip()
            for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}


def setup_acts():
    M = material()
    af, fa, tr = (os.path.join(P, x) for x in ('Afanasyev', 'Fables', 'Tragedy'))
    os.makedirs(os.path.join(BASE, 'tale', 'tales'), exist_ok=True)
    tales = [t for b in M['tale'].values() for t in b]
    for t in tales:
        shutil.copy(os.path.join(af, 'tales', t + '.txt'), os.path.join(BASE, 'tale', 'tales', t + '.txt'))
    subset(os.path.join(af, 'Events.txt'), os.path.join(BASE, 'tale', 'Events.txt'), set(tales))
    fables = {f for b in M['fable'].values() for f in b}
    os.makedirs(os.path.join(BASE, 'fable'), exist_ok=True)
    for f in ('Fables.txt', 'Events.txt'):
        subset(os.path.join(fa, f), os.path.join(BASE, 'fable', f), fables)
    for p in PLAYS:
        os.makedirs(os.path.join(BASE, 'tragedy', 'plays', p), exist_ok=True)
        for f in ('Text.txt', 'Events.txt', 'Cast.txt'):
            shutil.copy(os.path.join(tr, 'plays', p, f), os.path.join(BASE, 'tragedy', 'plays', p, f))
    names = play_names()
    for L in 'AB':
        for b, ids in M['tale'].items():
            files = ', '.join('problems/tale/tales/%s.txt' % i for i in ids) + ', problems/tale/Events.txt'
            text = ACTS_PROMPT.format(what="some tales from Aleksandr Afanasyev's collection of Russian folktales", L=L, b=b,
                                      where='Your tales are these %d, one per file, read in their original language: %s. Their events are in problems/tale/Events.txt.'
                                            % (len(ids), ', '.join('problems/tale/tales/%s.txt' % i for i in ids)),
                                      files=files, orig=', in the original language')
            open(os.path.join(OUT, 'prompts', 'pacts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
        for b, ids in M['fable'].items():
            text = ACTS_PROMPT.format(what="some of Aesop's fables, in George Fyler Townsend's 1867 translation", L=L, b=b,
                                      where='The fables are in problems/fable/Fables.txt, one per line as "identifier | title | text", and their events in problems/fable/Events.txt. Your fables are these: %s.' % ', '.join(ids),
                                      files='problems/fable/Fables.txt, problems/fable/Events.txt', orig='')
            open(os.path.join(OUT, 'prompts', 'pacts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
        for b, ids in M['tragedy'].items():
            text = ACTS_PROMPT.format(what='two Greek plays, %s, in English translation' % ' and '.join('%s (%s)' % (names[p], p) for p in ids),
                                      L=L, b=b,
                                      where="Each play is in its folder under problems/tragedy/plays/: Text.txt, one speech per line; Events.txt, its events; and Cast.txt, its cast. Name every performer and undergoer exactly as the play's Cast.txt names them. Write the two plays one after the other.",
                                      files=', '.join('problems/tragedy/plays/%s/Text.txt, Events.txt and Cast.txt' % p for p in ids), orig='')
            open(os.path.join(OUT, 'prompts', 'pacts-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
    print({g: {b: len(v) for b, v in bs.items()} for g, bs in M.items()})


# ---------------------------------------------------------------- reading the acts
def play_events(play):
    """{event: speech} for a test play"""
    out = {}
    for l in open(os.path.join(BASE, 'tragedy', 'plays', play, 'Events.txt'), encoding='utf-8'):
        f = [x.strip() for x in l.split('|')]
        if len(f) >= 3 and f[1].isdigit():
            out[int(f[1])] = f[2]
    return out


def act_lines(L, b):
    """the act describer's entries in one batch, in order: [(story, event, act, performer, undergoer, relation, matters, note)],
    and the faults met. A line with a speech number (S001...) where the play belongs is read as in TwoLayer (its
    KeeperLog, the S000 placeholder): the batch's two plays in order, events restarting at 1 for the second, every
    speech number checked against the play's event list; a line that does not match is a fault."""
    g = next(g for g, bs in material().items() if b in bs)
    path = os.path.join(BASE, 'acts', L, b, 'Notes.txt')
    if not os.path.exists(path):
        return [], ['%s %s: no file' % (L, b)]
    plays = material()['tragedy'].get(b, [])
    out, faults = [], []
    # read from the normalized tables (Data/tables.py), where the speech-numbered plays are recovered by the rule
    # above and a line that does not match is flagged
    for r in DT.file_rows('acts', path):
        ev, raw = int(r['event']), r['raw_id']
        if re.match(r'^S\d+$', raw) and plays:
            s = DT.local(r['story'])
            if r['id_flag']:
                faults.append('%s %s line %s: speech %s at event %d does not match %s' % (L, b, r['line'], raw, ev, s))
                continue
        elif re.match(r'^[PFA]\d{2}', raw):
            s = DT.local(r['story'])
        else:
            continue
        out.append((s, ev, r['act'].lower(), r['performer'], r['undergoer'], r['relation'].lower(),
                    r['matters'][:1].upper(), r['note']))
    return out, faults


def form_acts():
    M = material()
    ev_lists = {s: [k for k, _ in evs] for items in H.stories().values() for s, _, _, evs in items}
    total = 0
    for L in 'AB':
        for g, bs in M.items():
            for b, ids in bs.items():
                rows, faults = act_lines(L, b)
                bad = [r for r in rows if r[2] not in T.ACTS or r[5] not in RELATIONS or r[6] not in 'YN' or r[0] not in ids]
                uncovered = [(s, k) for s in ids for k in ev_lists[s] if not any(r[0] == s and r[1] == k for r in rows)]
                print('%s %-3s stories %2d, entries %4d, uncovered events %3d, out-of-list entries %3d, faults %d'
                      % (L, b, len(ids), len(rows), len(uncovered), len(bad), len(faults)))
                for x in faults[:5] + ['   uncovered: %s ev %d' % u for u in uncovered[:5]] + ['   out of list: %s' % (r[:7],) for r in bad[:5]]:
                    print('   ' + x)
                total += len(uncovered) + len(bad) + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


# ---------------------------------------------------------------- the significance stage
def sig_batches():
    """{sig batch: [story ids]}: the tales in four, the fables in one, the plays as their act batches"""
    M = material()
    tales = M['tale']['t3'] + M['tale']['t4']
    q = (len(tales) + 3) // 4
    out = collections.OrderedDict()
    for i in range(4):
        out['q%d' % (i + 1)] = tales[i * q:(i + 1) * q]
    out['q5'] = M['fable']['f3'] + M['fable']['f4']
    for i in range(8):
        out['q%d' % (i + 6)] = M['tragedy']['g%d' % (i + 5)]
    return out


def act_batch(story):
    return next(b for g, bs in material().items() for b, ids in bs.items() if story in ids)


def inputs():
    """{(L, sig batch): [(entry id, story, event, act, performer, undergoer, relation)]}, and the input texts"""
    St = {s: (title, ev) for items in H.stories().values() for s, title, _, ev in items}
    cache = {}
    out, text = {}, {}
    for L in 'AB':
        n = 0
        for q, ids in sig_batches().items():
            rows, lines = [], []
            for s in ids:
                b = act_batch(s)
                if (L, b) not in cache:
                    cache[L, b] = act_lines(L, b)[0]
                ents = [r for r in cache[L, b] if r[0] == s]
                title, evs = St[s]
                lines.append('story: %s | %s | hero: %s' % (s, title, S.hero_line(s)))
                for k, t in evs:
                    mine = [r for r in ents if r[1] == k]
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


SIG_PROMPT = S.PROMPT.replace('sig/input/{L}-{b}.txt', 'problems/sig/input/{L}-{b}.txt').replace(
    'nothing else under sig/ and nothing under any acts/ folder', 'nothing else under sig/ or problems/sig/ and nothing under any acts/ folder').replace(
    'sig/{L}/{b}/Significance.txt', 'problems/sig/{L}/{b}/Significance.txt')


def setup_sig():
    rows, text = inputs()
    os.makedirs(os.path.join(BASE, 'sig', 'input'), exist_ok=True)
    names = play_names()
    M = material()
    for (L, q), t in text.items():
        open(os.path.join(BASE, 'sig', 'input', '%s-%s.txt' % (L, q)), 'w', encoding='utf-8', newline='\n').write(t)
        ids = sig_batches()[q]
        g = genre_of()[ids[0]]
        if g == 'tale':
            files = ', '.join('problems/tale/tales/%s.txt' % s for s in ids)
            where = "Your stories are tales from Aleksandr Afanasyev's collection of Russian folktales; each tale's text is in its own file, in Russian: %s." % files
        elif g == 'fable':
            files = 'problems/fable/Fables.txt'
            where = "Your stories are Aesop's fables, in George Fyler Townsend's 1867 translation; their texts are in problems/fable/Fables.txt, one per line as \"identifier | title | text\"."
        else:
            files = ', '.join('problems/tragedy/plays/%s/Text.txt' % s for s in ids)
            where = ("Your stories are Greek plays, %s, in English translation; each play's text is in its folder under problems/tragedy/plays/, in Text.txt, one speech per line."
                     % ' and '.join('%s (%s)' % (names[s], s) for s in ids))
        open(os.path.join(OUT, 'prompts', 'psig-%s-%s.txt' % (L, q)), 'w', encoding='utf-8', newline='\n').write(
            SIG_PROMPT.format(L=L, b=q, n=len(ids), m=len(rows[L, q]), where=where, files=files))
    assert M
    print({q: (len(v), len(rows['A', q]), len(rows['B', q])) for q, v in sig_batches().items()})


def read_sig(L, q):
    path = os.path.join(BASE, 'sig', L, q, 'Significance.txt')
    saved = S.SIG
    S.SIG = os.path.join(BASE, 'sig')
    try:
        return S.read_sig(L, q) if os.path.exists(path) else ({}, {}, ['%s %s: no file' % (L, q)])
    finally:
        S.SIG = saved


def form_sig():
    rows, _ = inputs()
    total = 0
    for (L, q), rs in sorted(rows.items(), key=lambda kv: (kv[0][0], int(kv[0][1][1:]))):
        sig, probs, faults = read_sig(L, q)
        missing = [r[0] for r in rs if r[0] not in sig]
        extra = sorted(set(sig) - {r[0] for r in rs})
        print('%s %-3s acts %4d, described %4d, missing %3d, unknown ids %d, problem lines %3d, faults %d'
              % (L, q, len(rs), len(sig), len(missing), len(extra), len(probs), len(faults)))
        for x in faults[:10]:
            print('   ' + x)
        total += len(missing) + len(extra) + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def described():
    """{L: {story: [entry dicts in order]}} for the test stories"""
    rows, _ = inputs()
    out = {L: collections.defaultdict(list) for L in 'AB'}
    for (L, q), rs in rows.items():
        sig, _, _ = read_sig(L, q)
        for eid, s, ev, a, pf, u, r in rs:
            d = sig.get(eid)
            if d:
                part, value, place, prob, link, target = d
                out[L][s].append({'id': eid, 'event': ev, 'act': a, 'part': part, 'value': value, 'place': place, 'problem': prob})
    return out


# ---------------------------------------------------------------- the measures
MEASURES = ('problems', 'repaired', 'open', 'hero opens', 'ends repaired', 'acts help', 'acts harm')


def measures(xs):
    """the seven measures for one story's entries, in order; None where a measure does not apply"""
    xs = sorted(xs, key=lambda x: x['id'])
    probs = collections.OrderedDict()
    openers = collections.OrderedDict()
    for x in xs:
        if x['place'] == 'none' or x['problem'] in ('-', ''):
            continue
        probs.setdefault(x['problem'], set()).add(x['place'])
        if x['place'] == 'opens' and x['problem'] not in openers:
            openers[x['problem']] = x
    n = len(probs)
    m = {'problems': n,
         'acts help': sum(x['value'] == 'helps' for x in xs) / float(len(xs)) if xs else None,
         'acts harm': sum(x['value'] == 'harms' for x in xs) / float(len(xs)) if xs else None}
    if n:
        m['repaired'] = sum('repairs' in v for v in probs.values()) / float(n)
        m['open'] = sum(not v & {'repairs', 'punishes', 'rewards'} for v in probs.values()) / float(n)
    else:
        m['repaired'] = m['open'] = None
    if openers:
        m['hero opens'] = sum(o['part'] in ('does', 'both') for o in openers.values()) / float(len(openers))
        m['ends repaired'] = 1.0 if 'repairs' in probs[list(openers)[-1]] else 0.0
    else:
        m['hero opens'] = m['ends repaired'] = None
    return m


NULL_DRAWS = 200
MIN_EFFECT = 0.05  # a prediction needs a difference of at least this, half the rule's 0.10 for admitting it
JUDGED = ('repaired', 'open', 'hero opens', 'ends repaired', 'acts help', 'acts harm')


def excess(D, gen):
    """{L: {genre: {measure: [per-story excess]}}}, and the raw figures {L: {genre: {measure: [values]}}}.
    A story's excess is its measure minus the mean of the same measure over NULL_DRAWS random descriptions of
    its own acts: each act's hero's part, value and place drawn together from that describer's pooled
    descriptions of all the stories scored, and its problem label drawn from the labels the describer used in
    that story (p1 if none). The null keeps each story's length and number of problems, so the excess is the
    structure beyond what length and the describer's overall rates produce."""
    rnd = random.Random(SEED)
    ex = {L: {g: {m: [] for m in MEASURES} for g in GENRES} for L in 'AB'}
    raw = {L: {g: {m: [] for m in MEASURES} for g in GENRES} for L in 'AB'}
    for L in 'AB':
        stories = [(s, sorted(xs, key=lambda x: x['id'])) for s, xs in sorted(D[L].items()) if gen.get(s) and xs]
        pool = [(x['part'], x['value'], x['place']) for _, xs in stories for x in xs]
        for s, xs in stories:
            g = gen[s]
            obs = measures(xs)
            labels = sorted({x['problem'] for x in xs if x['place'] != 'none' and x['problem'] not in ('-', '')}) or ['p1']
            acc = collections.defaultdict(list)
            for _ in range(NULL_DRAWS):
                ys = []
                for x in xs:
                    part, value, place = rnd.choice(pool)
                    ys.append(dict(x, part=part, value=value, place=place, problem=rnd.choice(labels)))
                for m, v in measures(ys).items():
                    if v is not None:
                        acc[m].append(v)
            for m in MEASURES:
                if obs[m] is not None:
                    raw[L][g][m].append(obs[m])
                    if acc[m]:
                        ex[L][g][m].append(obs[m] - mean(acc[m]))
    return ex, raw


PREDICTIONS = [  # (measure, higher genre, lower genre): `problems.py dev`'s output, by the rule
    ('repaired', 'tale', 'tragedy'), ('repaired', 'fable', 'tragedy'), ('open', 'tragedy', 'tale'), ('open', 'tragedy', 'fable'),
    ('hero opens', 'fable', 'tale'), ('ends repaired', 'tale', 'tragedy'), ('ends repaired', 'fable', 'tragedy'),
    ('acts help', 'tale', 'fable'), ('acts help', 'tale', 'tragedy'), ('acts harm', 'fable', 'tale'), ('acts harm', 'tragedy', 'tale')]
# in ProblemsProtocol.md: every comparison of excesses the development stories show in the same direction for
# both describers, by at least 0.10.


def qualifying(ex):
    """the comparisons of excesses that the rule admits as predictions"""
    out = []
    for m in JUDGED:
        for hi in GENRES:
            for lo in GENRES:
                if hi != lo and all(mean(ex[L][hi][m]) - mean(ex[L][lo][m]) >= 0.10 for L in 'AB'):
                    out.append((m, hi, lo))
    return out


def mean(v):
    return sum(v) / float(len(v)) if v else float('nan')


def perm_p(x, y, sign, rnd):
    """one-sided: the chance, shuffling labels, of a difference sign*(mean x - mean y) at least the observed"""
    obs = sign * (mean(x) - mean(y))
    pool = x + y
    k = 0
    for _ in range(PERMS):
        rnd.shuffle(pool)
        if sign * (mean(pool[:len(x)]) - mean(pool[len(x):])) >= obs - 1e-12:
            k += 1
    return (k + 1) / float(PERMS + 1)


def evaluate(D, gen, title, preds):
    """D: {L: {story: entries}}; returns report lines, the number of predictions that hold, and the excesses"""
    ex, raw = excess(D, gen)
    rep = [title, '']
    rep.append('stories: %s' % ', '.join('%s %s %d' % (L, g, len(raw[L][g]['problems'])) for L in 'AB' for g in GENRES))
    rep.append('%-14s %s %14s %14s %14s' % ('measure', 'L', 'tale', 'fable', 'tragedy'))
    rep.append('%-14s %s %14s %14s %14s' % ('', '', 'raw / excess', 'raw / excess', 'raw / excess'))
    for m in MEASURES:
        for L in 'AB':
            rep.append('%-14s %s ' % (m, L) + ' '.join('%7.2f/%+6.2f' % (mean(raw[L][g][m]), mean(ex[L][g][m]) if ex[L][g][m] else float('nan'))
                                                      for g in GENRES))
    rep += ['', 'PREDICTIONS, on the excess (each holds when the higher genre is higher by at least %.2f and the one-sided permutation p <= 0.05, for both describers)' % MIN_EFFECT]
    rnd = random.Random(SEED)
    held = 0
    for i, (m, hi, lo) in enumerate(preds, 1):
        parts = []
        ok = True
        for L in 'AB':
            x, y = ex[L][hi][m], ex[L][lo][m]
            d = mean(x) - mean(y)
            p = perm_p(list(x), list(y), +1, rnd)
            good = d >= MIN_EFFECT and p <= 0.05
            ok = ok and good
            parts.append('%s %+.2f p %.4f%s' % (L, d, p, '' if good else ' x'))
        held += ok
        rep.append('  %2d. %-13s %-7s above %-7s %s   %s' % (i, m, hi, lo, 'HOLDS' if ok else 'FAILS', '; '.join(parts)))
    return rep, held, ex, raw


def verdict(held, n):
    if 4 * held >= 3 * n:
        return 'THE GENRES HAVE DISTINCT PROBLEM STRUCTURES'
    if 4 * held >= n:
        return 'THEY DIFFER IN PART'
    return 'NOT SHOWN'


def dev():
    Sm = S.T.material()
    gen = {s: g for g, bs in Sm.items() for b in bs.values() for s in b}
    D = {}
    for L in 'AB':
        d = collections.defaultdict(list)
        for (s, ev), xs in S.described(L).items():
            for x in xs:
                d[s].append(dict(x, event=ev))
        D[L] = d
    ex, _ = excess(D, gen)
    preds = qualifying(ex)
    rep, held, _, _ = evaluate(D, gen, '# ProblemsDev.txt -- problems.py dev: the measures on the development stories (Significance/), already seen; '
                               'the predictions are the comparisons the rule admits here; not the test.', preds)
    rep += ['', 'On the development stories: %d of %d predictions hold -> %s' % (held, len(preds), verdict(held, len(preds))),
            '', 'THE PREDICTIONS THE RULE ADMITS, for PREDICTIONS in problems.py:', '  ' + repr(preds)]
    open(os.path.join(HERE, 'ProblemsDev.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def score():
    if not PREDICTIONS:
        sys.exit('PREDICTIONS is empty: the test is not frozen')
    gen = genre_of()
    D = described()
    rep, held, ex, raw = evaluate(D, gen, '# ProblemsRun.txt -- problems.py score, as ProblemsProtocol.md freezes it.', PREDICTIONS)
    rep += ['', 'VERDICT: %d of %d predictions hold -> %s' % (held, len(PREDICTIONS), verdict(held, len(PREDICTIONS))), '',
            'REPORTED, NOT JUDGED']
    rnd = random.Random(SEED + 1)
    for m in MEASURES:
        for hi, lo in (('tale', 'fable'), ('tale', 'tragedy'), ('fable', 'tragedy')):
            if (m, hi, lo) in PREDICTIONS or (m, lo, hi) in PREDICTIONS:
                continue
            cells = []
            for L in 'AB':
                x, y = ex[L][hi][m], ex[L][lo][m]
                if x and y:
                    p2 = min(1.0, 2 * min(perm_p(list(x), list(y), +1, rnd), perm_p(list(x), list(y), -1, rnd)))
                    cells.append('%s %+.2f p %.4f' % (L, mean(x) - mean(y), p2))
            rep.append('  not predicted, %-13s %-7s against %-7s (excess, two-sided): %s' % (m, hi, lo, '; '.join(cells)))
    by_ev = {L: collections.defaultdict(list) for L in 'AB'}
    for L in 'AB':
        for s, xs in D[L].items():
            for x in xs:
                by_ev[L][(s, x['event'])].append(x)
    n = 0
    same = collections.Counter()
    for e in set(by_ev['A']) & set(by_ev['B']):
        for a in {x['act'] for x in by_ev['A'][e]} & {x['act'] for x in by_ev['B'][e]}:
            xa = next(x for x in by_ev['A'][e] if x['act'] == a)
            xb = next(x for x in by_ev['B'][e] if x['act'] == a)
            n += 1
            for k in ('part', 'value', 'place'):
                same[k] += xa[k] == xb[k]
    rep.append("  agreement where both give an event the same act (%d): hero's part %.0f%%, value %.0f%%, place %.0f%%"
               % (n, 100.0 * same['part'] / max(1, n), 100.0 * same['value'] / max(1, n), 100.0 * same['place'] / max(1, n)))
    open(os.path.join(HERE, 'ProblemsRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    cmds = {'setup-acts': setup_acts, 'form-acts': form_acts, 'setup-sig': setup_sig, 'form-sig': form_sig, 'dev': dev, 'score': score}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
