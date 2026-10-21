#!/usr/bin/env python3
"""
significance.py -- the test of a significance layer (SignificanceProtocol.md).

  python significance.py setup   writes the describers' material, rules and prompts
                                 into Story Language/ActsRoles/sig/
  python significance.py form    checks the returned descriptions' form
  python significance.py score   scores them; writes Significance/SignificanceRun.txt

Written in full before any description under the layer existed.
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
sys.path.insert(0, os.path.join(ROOT, 'Heroes'))
sys.path.insert(0, os.path.join(ROOT, 'TwoLayer'))
sys.path.insert(0, HERE)
import heroes as H  # noqa: E402
import twoLayer as T  # noqa: E402
import withJudgedHeroes as W  # noqa: E402
import baseline as BL  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, 'Data'))
import tables as DT  # noqa: E402

OUT = os.path.join(P, 'ActsRoles')
SIG = os.path.join(OUT, 'sig')
PARTS = ('does', 'undergoes', 'both', 'neither')
VALUES = ('helps', 'harms', 'neither')
PLACES = ('opens', 'worsens', 'serves', 'repairs', 'rewards', 'punishes', 'none')
LINKS = ('answers', 'enables', 'none')


# ---------------------------------------------------------------- material
def acts_batch(story):
    """the act transcription's batch a story is in"""
    for g, bs in T.material().items():
        for b, ids in bs.items():
            if story in ids:
                return g, b
    return None


def batches():
    """{batch: [story ids]}, stories with a judged hero only; the tales in four batches, the fables in one, the plays as before."""
    J = W.judged()
    M = T.material()
    tales = [s for b in ('t1', 't2') for s in M['tale'][b] if s in J]
    fables = [s for b in ('f1', 'f2') for s in M['fable'][b] if s in J]
    q = (len(tales) + 3) // 4
    out = collections.OrderedDict()
    for i in range(4):
        out['s%d' % (i + 1)] = tales[i * q:(i + 1) * q]
    out['s5'] = fables
    for i in range(4):
        out['s%d' % (i + 6)] = [s for s in M['tragedy']['g%d' % (i + 1)] if s in J]
    return out


def act_entries(L, story):
    """the act transcription's entries for one story, in order: [(event, act, performer, undergoer, relation, note)]"""
    g, b = acts_batch(story)
    path = os.path.join(OUT, g, 'acts', L, b, 'Notes.txt')
    out = []
    recover = None
    for line in open(path, encoding='utf-8'):
        f = [x.strip() for x in line.rstrip('\n').split('|', 9)]
        if len(f) < 10:
            continue
        ev = re.search(r'\d+', f[1])
        if not ev:
            continue
        if re.match(r'^S\d+$', f[0]):
            recover = recover or T.speech_story(path)
            s = recover(f[0], int(ev.group())) if recover else None
        elif re.match(r'^[PFA]\d{2}', f[0]):
            s = f[0].split('/')[0]
        else:
            continue
        if s == story and f[6][:1].upper() in 'YN':
            out.append((int(ev.group()), f[2].lower(), f[3], f[4], f[5].lower(), f[9]))
    return out


def hero_line(s):
    name = H.answers('A')[s][0]
    if name.lower().startswith('no single hero'):
        who = [x.strip() for x in name.split(':', 1)[1].split(';') if x.strip()]
        return '%s (the story divides between them; count either as the hero)' % ' or '.join(who)
    return name


def inputs():
    """{(L, batch): [(entry id, story, event, act, performer, undergoer, relation)]}, and writes nothing"""
    S = {s: (title, ev) for items in H.stories().values() for s, title, _, ev in items}
    out, text = {}, {}
    for L in 'AB':
        n = 0
        for b, ids in batches().items():
            rows, lines = [], []
            for s in ids:
                title, evs = S[s]
                lines.append('story: %s | %s | hero: %s' % (s, title, hero_line(s)))
                ents = act_entries(L, s)
                for k, t in evs:
                    mine = [x for x in ents if x[0] == k]
                    if not mine:
                        continue
                    lines.append('  ev %d | %s' % (k, t))
                    for ev, a, pf, u, r, note in mine:
                        n += 1
                        eid = 'e%04d' % n
                        rows.append((eid, s, ev, a, pf, u, r))
                        lines.append('    %s | %s | %s | %s | %s | %s' % (eid, a, pf, u, r, note))
                lines.append('')
            out[L, b] = rows
            text[L, b] = '\n'.join(lines) + '\n'
    return out, text


PROMPT = ("You are describing what some acts mean for the stories they are in. You start with no background on the project, and you should not look for any.\n\n"
          "Read sig/SigRules.md in this repository first, in full, and follow it exactly. Your input file is sig/input/{L}-{b}.txt; it holds {n} stories and {m} acts. {where}\n\n"
          "For each story, read the whole story and its whole list of acts first. Then write one line for every act, in the order of your input file, as the rules ask, with a problem line before the first act that uses each problem label.\n\n"
          "Open only sig/SigRules.md, sig/input/{L}-{b}.txt, {files} and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing else under sig/ and nothing under any acts/ folder. Do not search the web. You are describer {L}.\n\n"
          "Write one file, and nothing else, sig/{L}/{b}/Significance.txt (create the folders). Keep any working file inside that folder, and delete it before you finish.\n\n"
          "Then reply with the report the rules' last section asks for.\n")


def setup():
    rows, text = inputs()
    os.makedirs(os.path.join(SIG, 'input'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'Significance.md'), os.path.join(SIG, 'SigRules.md'))
    order = {l.split('|')[0].strip(): l.split('|')[2].strip() + "'s " + l.split('|')[3].strip()
             for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}
    for (L, b), t in text.items():
        open(os.path.join(SIG, 'input', '%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(t)
        ids = batches()[b]
        g = acts_batch(ids[0])[0]
        if g == 'tale':
            files = ', '.join('tale/tales/%s.txt' % s for s in ids)
            where = ("Your stories are tales from Aleksandr Afanasyev's collection of Russian folktales; each tale's text is in its own file, in Russian: %s." % files)
        elif g == 'fable':
            files = 'fable/Fables.txt'
            where = "Your stories are Aesop's fables, in George Fyler Townsend's 1867 translation; their texts are in fable/Fables.txt, one per line as \"identifier | title | text\"."
        else:
            files = ', '.join('tragedy/plays/%s/Text.txt' % s for s in ids)
            where = ('Your stories are Greek plays, %s, in English translation; each play\'s text is in its folder under tragedy/plays/, in Text.txt, one speech per line.'
                     % ' and '.join('%s (%s)' % (order[s], s) for s in ids))
        open(os.path.join(OUT, 'prompts', 'sig-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(
            PROMPT.format(L=L, b=b, n=len(ids), m=len(rows[L, b]), where=where, files=files))
    print({b: (len(v), len(rows['A', b]), len(rows['B', b])) for b, v in batches().items()})


# ---------------------------------------------------------------- reading
def read_sig(L, b):
    """{entry id: (part, value, place, problem, link, target)}, problem lines {(story, label): name}, and form faults"""
    path = os.path.join(SIG, L, b, 'Significance.txt')
    out, probs, faults = {}, {}, []
    if not os.path.exists(path):
        return out, probs, ['%s %s: no file' % (L, b)]
    # read from the normalized tables (Data/tables.py): the file's problem lines, then its entries
    for r in DT.file_rows('problems', path):
        if re.match(r'^[PFA]\d{2}', DT.local(r['story'])):
            probs[(DT.local(r['story']), r['problem'].lower())] = r['text'].split(' | ')[0]
    for r in DT.file_rows('significance', path):
        f = [r['entry'], r['part'], r['value'], r['place'], r['problem'], r['link'], r['target']]
        if int(r['fields']) < 9:
            faults.append('%s %s line %s: %s fields' % (L, b, r['line'], r['fields']))
            continue
        part, value, place, prob, link, target = (x.lower() for x in f[1:7])
        bad = [x for x, ok in ((part, PARTS), (value, VALUES), (place, PLACES), (link, LINKS)) if x not in ok]
        if bad:
            faults.append('%s %s %s: not in the lists: %s' % (L, b, f[0], ', '.join(bad)))
        out[f[0]] = (part, value, place, prob, link, target)
    return out, probs, faults


def material_rows():
    rows, _ = inputs()
    return rows


def form():
    rows = material_rows()
    total = 0
    for (L, b), rs in sorted(rows.items()):
        sig, probs, faults = read_sig(L, b)
        missing = [r[0] for r in rs if r[0] not in sig]
        extra = sorted(set(sig) - {r[0] for r in rs})
        print('%s %-3s acts %4d, described %4d, missing %3d, unknown ids %d, problem lines %3d, faults %d'
              % (L, b, len(rs), len(sig), len(missing), len(extra), len(probs), len(faults)))
        for x in faults[:10]:
            print('   ' + x)
        total += len(missing) + len(extra) + len(faults)
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


# ---------------------------------------------------------------- the mapping
def derive2(act, part):
    """TwoLayer's frozen mapping, with the hero's part as the describer gives it instead of a name match."""
    hd, hu = part in ('does', 'both'), part in ('undergoes', 'both')
    return T.derive(act, 'H' if hd else 'x', 'H' if hu else 'x', 'h')


def derive3(act, part, value, place, after):
    """the functions an act maps to with its significance (SignificanceProtocol.md, the mapping); `after` is
    whether the act's problem has already opened at an earlier act."""
    if place == 'none':
        return set()
    hd, hu = part in ('does', 'both'), part in ('undergoes', 'both')
    hi = hd or hu
    harms, helps = value == 'harms', value == 'helps'
    out = set()
    # the significance rules, for any act
    if place == 'opens':
        if act == 'want' or not harms:
            out.add('a')
        elif not hd:
            out.add('A')
    if place == 'worsens' and harms and not hd and act in ('harm', 'other', 'deceive'):
        out.add('A')
    if place == 'repairs' and act in ('repair', 'receive', 'give', 'other', 'escape'):
        out.add('K')
    if place == 'punishes' and not hu:
        out.add('U')
    if place == 'rewards' and hi:
        out.add('W')
    # the act rules
    f = None
    if act == 'leave':
        f = '↑' if hd else ('β' if harms else None)
    elif act == 'return':
        f = '↓' if hd else None
    elif act in ('forbid', 'send'):
        if hu and after:
            f = 'B'
        elif act == 'forbid' or (hu and not after):
            f = 'γ'
    elif act == 'disobey':
        f = 'δ'
    elif act == 'seek-information':
        f = 'ε' if harms else None
    elif act == 'reveal-information':
        if harms:
            f = 'ζ'
        elif hu and after:
            f = 'B'
    elif act == 'deceive':
        if hd and place == 'repairs':
            f = 'I'
        elif harms or (not hd and place in ('serves', 'opens', 'worsens')):
            f = 'η'
    elif act == 'be-taken-in':
        f = 'θ' if place in ('serves', 'opens', 'worsens') else None
    elif act == 'harm':
        if place == 'repairs' and not hu:
            f = 'I'
    elif act == 'want':
        f = 'a' if place in ('opens', 'worsens') else None
    elif act == 'plead':
        if hu:
            f = 'B' if after and not helps else 'D'
        elif hd and place == 'opens':
            f = 'a'
    elif act == 'decide':
        f = 'C' if hd and after else None
    elif act == 'test':
        f = 'D' if hu else None
    elif act == 'respond':
        if hd:
            f = 'E'
        elif hu and helps:
            f = 'F'
    elif act == 'give':
        f = 'F' if hu and helps and place != 'rewards' else None
    elif act == 'receive':
        f = 'F' if hd and helps and place not in ('rewards', 'repairs') else None
    elif act == 'guide':
        f = 'G' if hu else None
    elif act == 'fight':
        f = 'H' if hi else None
    elif act == 'win':
        f = 'I' if hd else None
    elif act == 'lose':
        f = 'I-' if hd else ('I' if helps else None)
    elif act == 'mark':
        f = 'J' if hu else None
    elif act == 'repair':
        f = 'K'
    elif act == 'pursue':
        f = 'Pr' if hu else None
    elif act == 'escape':
        f = 'Rs' if hi else None
    elif act == 'arrive-unknown':
        f = 'o' if hd else None
    elif act == 'claim-falsely':
        f = 'L'
    elif act == 'set-task':
        f = 'M' if hu else None
    elif act == 'do-task':
        f = 'N' if hd else None
    elif act == 'recognize':
        f = 'Q' if hi else None
    elif act == 'expose':
        f = 'Ex' if not hu else None
    elif act == 'transform':
        f = 'T' if hi else None
    elif act == 'punish':
        f = 'U' if not hu and place == 'punishes' else None
    elif act == 'marry':
        f = 'W' if hi else None
    if f:
        out.add(f)
    return out


# ---------------------------------------------------------------- scoring
def described(L):
    """{(story, event): [entry dicts]} for one describer, in input order"""
    rows = material_rows()
    out = collections.defaultdict(list)
    for b in batches():
        sig, _, _ = read_sig(L, b)
        opened = set()
        for eid, s, ev, a, pf, u, r in rows[L, b]:
            d = sig.get(eid)
            if d is None:
                continue
            part, value, place, prob, link, target = d
            after = (s, prob) in opened
            if place == 'opens':
                opened.add((s, prob))
            out[(s, ev)].append({'id': eid, 'act': a, 'part': part, 'value': value, 'place': place,
                                 'problem': prob, 'link': link, 'after': after, 'rel': r})
    return out


def score():
    M = T.material()
    J = W.judged()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    funcs, D = {}, {}
    for L in 'AB':
        o = {}
        for g in T.GENRES:
            o.update({e: v for e, v in T.read_functions(glob.glob(os.path.join(P, BL.ORIG[g] % L))).items() if e[0] in gen})
        funcs[L] = o
        D[L] = described(L)
    events = sorted(e for e in set(funcs['A']) & set(funcs['B']) & set(D['A']) & set(D['B']) if e[0] in J)
    d2 = {L: {e: set().union(*[{derive2(x['act'], x['part'])} - {None} for x in D[L][e]]) for e in events} for L in 'AB'}
    d3 = {L: {e: set().union(*[derive3(x['act'], x['part'], x['value'], x['place'], x['after']) for x in D[L][e]]) for e in events}
          for L in 'AB'}
    rep = ['# SignificanceRun.txt -- significance.py score, as SignificanceProtocol.md freezes it.', '',
           'Events compared: %d, in %d stories with a judged hero (in both original transcriptions and both descriptions)'
           % (len(events), len({e[0] for e in events})), '']
    jab = T.jaccard(funcs['A'], funcs['B'], events)
    r2 = [T.jaccard(d2[L], funcs[L], events) for L in 'AB']
    r3 = [T.jaccard(d3[L], funcs[L], events) for L in 'AB']
    m2, m3 = sum(r2) / 2, sum(r3) / 2
    rep.append('original A against B: %.3f' % jab)
    rep.append('two layers (the frozen mapping, the hero\'s part as described): A %.3f, B %.3f, mean %.3f' % (r2[0], r2[1], m2))
    rep.append('three layers (the significance mapping): A %.3f, B %.3f, mean %.3f' % (r3[0], r3[1], m3))
    gap = jab - m2
    closed = (m3 - m2) / gap if gap > 0 else 0.0
    rep.append('share of the gap closed: %.0f%%' % (100 * closed))
    if m3 >= jab:
        v = 'THE THREE LAYERS RECOVER PROPP\'S FUNCTIONS'
    elif closed >= 0.5:
        v = 'THE SIGNIFICANCE LAYER CLOSES MOST OF THE GAP, BUT DOES NOT RECOVER PROPP\'S FUNCTIONS'
    else:
        v = 'THE SIGNIFICANCE LAYER DOES NOT RECOVER PROPP\'S FUNCTIONS'
    rep += ['', 'VERDICT: ' + v, '']
    rep.append('PREDICTIONS (the keeper\'s, recorded before any description)')
    rep.append('  1. the three-layer mean lies between 0.30 and 0.40: %.3f -> %s' % (m3, 'HOLDS' if 0.30 <= m3 <= 0.40 else 'FAILS'))
    rep.append('  2. the verdict is the third level, closing less than half the gap: %s' % ('HOLDS' if m3 < jab and closed < 0.5 else 'FAILS'))
    rep.append('')
    rep.append('REPORTED, NOT JUDGED')
    for g in T.GENRES:
        E = [e for e in events if gen[e[0]] == g]
        rep.append('  %-8s events %4d: original A against B %.3f; two layers A %.3f B %.3f; three layers A %.3f B %.3f'
                   % (g, len(E), T.jaccard(funcs['A'], funcs['B'], E), T.jaccard(d2['A'], funcs['A'], E), T.jaccard(d2['B'], funcs['B'], E),
                      T.jaccard(d3['A'], funcs['A'], E), T.jaccard(d3['B'], funcs['B'], E)))
    # the learned mapping, as Significance/baseline.py learns it
    for name, keys in (('learned, act + hero\'s part', ['act', 'part']),
                       ('learned, act + hero\'s part + value + place', ['act', 'part', 'value', 'place'])):
        r = [BL.run(J, {e: D[L][e] for e in events}, funcs[L], events, keys, gen) for L in 'AB']
        rep.append('  %-48s A %.3f  B %.3f  mean %.3f' % (name, r[0], r[1], sum(r) / 2))
    # agreement on the layer, where both describers give an event the same act
    same = collections.Counter()
    n = 0
    for e in events:
        for a in {x['act'] for x in D['A'][e]} & {x['act'] for x in D['B'][e]}:
            xa = next(x for x in D['A'][e] if x['act'] == a)
            xb = next(x for x in D['B'][e] if x['act'] == a)
            n += 1
            for k in ('part', 'value', 'place'):
                same[k] += xa[k] == xb[k]
    rep.append('  agreement where both give an event the same act (%d): hero\'s part %.0f%%, value %.0f%%, place %.0f%%'
               % (n, 100.0 * same['part'] / max(1, n), 100.0 * same['value'] / max(1, n), 100.0 * same['place'] / max(1, n)))
    # the problems
    for g in T.GENRES:
        for L in 'AB':
            st = {e[0] for e in D[L] if gen.get(e[0]) == g}
            probs = collections.defaultdict(set)
            for e, xs in D[L].items():
                if gen.get(e[0]) != g:
                    continue
                for x in xs:
                    if x['place'] != 'none' and x['problem'] not in ('-', ''):
                        probs[(e[0], x['problem'])].add(x['place'])
            rep.append('  %-8s %s: %d stories, %d problems (%.1f a story); repaired %.0f%%, punished %.0f%%, rewarded %.0f%%'
                       % (g, L, len(st), len(probs), len(probs) / float(max(1, len(st))),
                          100.0 * sum('repairs' in v for v in probs.values()) / max(1, len(probs)),
                          100.0 * sum('punishes' in v for v in probs.values()) / max(1, len(probs)),
                          100.0 * sum('rewards' in v for v in probs.values()) / max(1, len(probs))))
    open(os.path.join(HERE, 'SignificanceRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup']:
        setup()
    elif a == ['form']:
        form()
    elif a == ['score']:
        score()
    else:
        sys.exit(__doc__)
