#!/usr/bin/env python3
"""
free.py -- the bottom-up test: acts described in the describers' own verbs (FreeProtocol.md).

  python free.py setup     writes the rules and prompts into Story Language/Projects/ActsRoles/free/
  python free.py form      checks the descriptions' form
  python free.py score     scores them; writes Free/FreeRun.txt

Written in full before any free description existed.
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
sys.path.insert(0, os.path.join(ROOT, 'Ngrams'))
import ngrams as N  # noqa: E402
DT = N.DT

T, Pm, H = N.T, N.Pm, N.Pm.H
OUT = os.path.join(P, 'ActsRoles')
BASE = os.path.join(OUT, 'free')
STAGES = {'free-1': ['t1', 't2', 't3', 't4'], 'free-2': ['f1', 'f2', 'f3', 'f4'], 'free-3': ['g1', 'g2', 'g3', 'g4'],
          'free-4': ['g5', 'g6', 'g7', 'g8'], 'free-5': ['g9', 'g10', 'g11', 'g12']}
SIX = [('forbid', 'disobey'), ('seek-information', 'reveal-information'), ('deceive', 'be-taken-in'),
       ('test', 'respond'), ('fight', 'win'), ('set-task', 'do-task')]   # the act pairs confirmed in Ngrams/
SPLIT_GAIN = 0.5   # a pair's halves are apart when the verb closes at least half the distance from chance to perfect


# ---------------------------------------------------------------- material
def batches():
    """{batch: (genre, [story ids], where the files are: '' for the two-layer test's, 'problems/' for the problem test's)}"""
    out = collections.OrderedDict()
    for g, bs in T.material().items():
        for b, ids in bs.items():
            out[b] = (g, ids, '')
    for g, bs in Pm.material().items():
        for b, ids in bs.items():
            out[b] = (g, ids, 'problems/')
    return out


PROMPT = ("You are describing what happens in {what}. You start with no background on the project, and you should not look for any.\n\n"
          "Read free/FreeRules.md in this repository first, in full, and follow it exactly. {where}\n\n"
          "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its verb, phrase, performer, undergoer and Y or N.\n\n"
          "Open only free/FreeRules.md, {files} and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under any acts/ or sig/ folder and nothing under free/ but your own folder. Do not search the web. You are describer {L}.\n\n"
          "Write one file, and nothing else, free/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on{orig}.\n\n"
          "Then reply with the report the rules' last section asks for.\n")


def setup():
    os.makedirs(BASE, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'FreeRules.md'), os.path.join(BASE, 'FreeRules.md'))
    names = Pm.play_names()
    for L in 'AB':
        for b, (g, ids, pre) in batches().items():
            if g == 'tale':
                files = ', '.join('%stale/tales/%s.txt' % (pre, i) for i in ids) + ', %stale/Events.txt' % pre
                text = PROMPT.format(what="some tales from Aleksandr Afanasyev's collection of Russian folktales", L=L, b=b,
                                     where='Your tales are these %d, one per file, read in their original language: %s. Their events are in %stale/Events.txt; write the verbs and phrases in English.'
                                           % (len(ids), ', '.join('%stale/tales/%s.txt' % (pre, i) for i in ids), pre),
                                     files=files, orig=', in the original language')
            elif g == 'fable':
                text = PROMPT.format(what="some of Aesop's fables, in George Fyler Townsend's 1867 translation", L=L, b=b,
                                     where='The fables are in %sfable/Fables.txt, one per line as "identifier | title | text", and their events in %sfable/Events.txt. Your fables are these: %s.'
                                           % (pre, pre, ', '.join(ids)),
                                     files='%sfable/Fables.txt, %sfable/Events.txt' % (pre, pre), orig='')
            else:
                text = PROMPT.format(what='two Greek plays, %s, in English translation' % ' and '.join('%s (%s)' % (names[p], p) for p in ids),
                                     L=L, b=b,
                                     where="Each play is in its folder under %stragedy/plays/: Text.txt, one speech per line; Events.txt, its events; and Cast.txt, its cast. Name every performer and undergoer exactly as the play's Cast.txt names them. Write the two plays one after the other, each line beginning with its play's identifier." % pre,
                                     files=', '.join('%stragedy/plays/%s/Text.txt, Events.txt and Cast.txt' % (pre, p) for p in ids), orig='')
            open(os.path.join(OUT, 'prompts', 'free-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(text)
    print({b: len(v[1]) for b, v in batches().items()})


# ---------------------------------------------------------------- reading
def verb_of(field):
    w = re.findall(r"[a-z][a-z'-]*", field.lower())
    if w and w[0] == 'to' and len(w) > 1:
        w = w[1:]
    return w[0] if w else ''


def read_free(L, b):
    """[(story, event, verb, phrase, performer, undergoer, matters)] in order, and faults"""
    g, ids, _ = batches()[b]
    path = os.path.join(BASE, L, b, 'Notes.txt')
    if not os.path.exists(path):
        return [], ['%s %s: no file' % (L, b)]
    out, faults = [], []
    for r in DT.file_rows('free', path):       # from the normalized tables (Data/tables.py)
        s, ev = DT.local(r['story']), int(r['event'])
        if int(r['fields']) < 9 or not ev or not re.match(r'^[A-Z]\d+', s):
            continue
        if s not in ids:
            faults.append('%s %s line %s: story %s not in the batch' % (L, b, r['line'], s))
            continue
        v = verb_of(r['verb'])
        if not v or r['matters'][:1].upper() not in 'YN':
            faults.append('%s %s line %s: verb or mark missing' % (L, b, r['line']))
            continue
        out.append((s, ev, v, r['phrase'], r['performer'], r['undergoer'], r['matters'][:1].upper()))
    return out, faults


def form():
    evs = {s: [k for k, _ in e] for items in H.stories().values() for s, _, _, e in items}
    total = 0
    for L in 'AB':
        for b, (g, ids, _) in batches().items():
            rows, faults = read_free(L, b)
            unc = [(s, k) for s in ids for k in evs[s] if not any(r[0] == s and r[1] == k for r in rows)]
            many = sum(1 for r in rows if len(r[2].split()) > 1)
            print('%s %-3s stories %2d, entries %4d, verbs %3d, uncovered events %3d, faults %d'
                  % (L, b, len(ids), len(rows), len({r[2] for r in rows}), len(unc), len(faults)))
            for x in faults[:5] + ['   uncovered: %s ev %d' % u for u in unc[:5]]:
                print('   ' + x)
            total += len(unc) + len(faults) + many
    print('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)


def free_strings():
    """{L: {story: [verbs in text order]}}, and {L: {(story, event): [verbs]}}"""
    st, by_ev = {}, {}
    for L in 'AB':
        s_out, e_out = collections.OrderedDict(), collections.defaultdict(list)
        for b in batches():
            for s, ev, v, _, _, _, _ in read_free(L, b)[0]:
                s_out.setdefault(s, []).append(v)
                e_out[(s, ev)].append(v)
        st[L], by_ev[L] = s_out, e_out
    return st, by_ev


def act_events():
    """{L: {(story, event): [acts]}} from both act transcriptions, `other` kept"""
    out = {}
    for L in 'AB':
        e = collections.defaultdict(list)
        raw = T.read_acts(sorted(p for g in N.GENRES for p in glob.glob(os.path.join(T.OUT, g, 'acts', L, '*', 'Notes.txt'))))
        for k, v in raw.items():
            e[k] += [a for a, _, _, _ in v]
        for g, bs in Pm.material().items():
            for b in bs:
                for r in Pm.act_lines(L, b)[0]:
                    e[(r[0], r[1])].append(r[2])
        out[L] = e
    return out


# ---------------------------------------------------------------- scoring
def alignment(by_ev, acts):
    """{L: {verb: Counter of acts}} over the clean events: one free entry and one act entry"""
    out = {}
    for L in 'AB':
        al = collections.defaultdict(collections.Counter)
        for k, vs in by_ev[L].items():
            a = acts[L].get(k, [])
            if len(vs) == 1 and len(a) == 1:
                al[vs[0]][a[0]] += 1
        out[L] = al
    return out


def split_accuracy(by_ev, acts, L, x, y):
    """leave-one-out: in clean events whose act is x or y, how often a token's verb, by the other tokens of the
    same verb, tells which of the two it is; and the chance rate"""
    toks = []
    for k, vs in by_ev[L].items():
        a = acts[L].get(k, [])
        if len(vs) == 1 and len(a) == 1 and a[0] in (x, y):
            toks.append((vs[0], a[0]))
    if not toks:
        return None, None, 0
    c = collections.defaultdict(collections.Counter)
    for v, a in toks:
        c[v][a] += 1
    right = 0
    for v, a in toks:
        cc = c[v].copy()
        cc[a] -= 1
        if cc[a] > cc[x if a == y else y]:
            right += 1
    n = len(toks)
    chance = max(sum(1 for _, a in toks if a == x), sum(1 for _, a in toks if a == y)) / float(n)
    return right / float(n), chance, n


def dominant(al, v):
    c = al.get(v)
    if not c or sum(c.values()) < 5:
        return None
    a, n = c.most_common(1)[0]
    return a if n / float(sum(c.values())) >= 0.5 else None


def pairs(strings):
    """discovery and confirmation as Ngrams/ freezes them, on the verb strings: confirmed (x, y, class)"""
    disc = N.stats_for(strings, 'discovery')
    conf = N.stats_for(strings, 'confirmation', gaps=tuple(range(1, N.MAX_GAP + 1)))
    vocab = sorted(set(disc['A'][0].vocab) & set(disc['B'][0].vocab))
    found = []
    for x in vocab:
        for y in vocab:
            if x == y:
                continue
            for c in (1, 'near'):
                if all(N.cell(disc, L, c, x, y)[0] >= N.MIN_COUNT and N.lift(*N.cell(disc, L, c, x, y)[:2]) >= N.MIN_LIFT
                       and N.cell(disc, L, c, x, y)[2] <= N.DISCOVER_P for L in 'AB'):
                    ok = all(N.lift(*N.cell(conf, L, c, x, y)[:2]) > 1 and N.cell(conf, L, c, x, y)[2] <= N.CONFIRM_P for L in 'AB')
                    found.append((x, y, c, ok, N.shape(N.gap_profile(conf, x, y))))
    return found


def score():
    strings, by_ev = free_strings()
    acts = act_events()
    al = alignment(by_ev, acts)
    rep = ['# FreeRun.txt -- free.py score, as FreeProtocol.md freezes it.', '']
    for L in 'AB':
        cnt = collections.Counter(v for s in strings[L].values() for v in s)
        rep.append('describer %s: %d stories, %d entries, %d verbs (%d used once); the commonest, with the act they meet most often in clean events and its share:'
                   % (L, len(strings[L]), sum(cnt.values()), len(cnt), sum(1 for n in cnt.values() if n == 1)))
        line = []
        for v, n in cnt.most_common(40):
            c = al[L].get(v)
            if c:
                a, k = c.most_common(1)[0]
                line.append('%s %d (%s %.0f%%)' % (v, n, a, 100.0 * k / sum(c.values())))
            else:
                line.append('%s %d' % (v, n))
        rep.append('  ' + '; '.join(line))
    rep += ['', 'THE UNITS: whether a verb tells apart the two halves of each pair (leave-one-out accuracy in clean events; chance is the larger half; gain is (accuracy - chance) / (1 - chance), apart at %.2f or more)' % SPLIT_GAIN]
    split_ok = 0
    for x, y in SIX:
        cells, ok = [], True
        for L in 'AB':
            acc, ch, n = split_accuracy(by_ev, acts, L, x, y)
            gain = (acc - ch) / (1 - ch) if acc is not None and ch < 1 else None
            ok = ok and gain is not None and gain >= SPLIT_GAIN and n >= 10
            cells.append('%s accuracy %s, chance %s, gain %s, n %d' % (L, '%.2f' % acc if acc is not None else '-', '%.2f' % ch if ch is not None else '-',
                                                                   '%.2f' % gain if gain is not None else '-', n))
        split_ok += ok
        top = {}
        for a in (x, y):
            c = collections.Counter()
            for L in 'AB':
                for v, cc in al[L].items():
                    c[v] += cc[a]
            top[a] = ', '.join('%s %d' % kv for kv in c.most_common(5) if kv[1])
        rep.append('  %s / %s: %s  %s' % (x, y, 'APART' if ok else 'not apart', '; '.join(cells)))
        rep.append('     verbs for %s: %s' % (x, top[x]))
        rep.append('     verbs for %s: %s' % (y, top[y]))
    rep += ['', 'THE PAIRS: discovery and confirmation on the verb strings, as Ngrams/ freezes them']
    found = pairs(strings)
    mapped = set()
    for x, y, c, ok, shp in found:
        dx = [dominant(al[L], x) for L in 'AB']
        dy = [dominant(al[L], y) for L in 'AB']
        m = (dx[0], dy[0]) if dx[0] and dx[0] == dx[1] and dy[0] and dy[0] == dy[1] else None
        if ok and m:
            mapped.add(m)
        rep.append('  %-8s %s -> %s  %s  %s  acts: %s' % ('adjacent' if c == 1 else 'near', x, y, 'CONFIRMED' if ok else 'not confirmed', shp,
                                                         '%s -> %s' % m if m else 'no single act for both describers'))
    hit = [p for p in SIX if p in mapped]
    rep += ['', 'PREDICTIONS (FreeProtocol.md)',
            '  1. the describers\' own verbs keep apart the halves of at least four of the six pairs, for both describers: %d of 6 -> %s'
            % (split_ok, 'HOLDS' if split_ok >= 4 else 'FAILS'),
            '  2. at least four of the six pairs come out as a confirmed pair of verbs whose acts, for both describers, are the pair\'s: %d of 6 (%s) -> %s'
            % (len(hit), ', '.join('%s->%s' % p for p in hit) or '-', 'HOLDS' if len(hit) >= 4 else 'FAILS'),
            '  3. the request and its answer comes out so (plead -> respond): %s' % ('HOLDS' if ('plead', 'respond') in mapped else 'FAILS'),
            '', 'REPORTED: the confirmed verb pairs whose acts are none of these: %s'
            % (', '.join('%s->%s' % m for m in sorted(mapped - set(SIX) - {('plead', 'respond')})) or '-')]
    open(os.path.join(HERE, 'FreeRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    cmds = {'setup': setup, 'form': form, 'score': score}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
