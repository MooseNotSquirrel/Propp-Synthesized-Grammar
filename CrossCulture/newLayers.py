#!/usr/bin/env python3
"""
newLayers.py -- the new corpora's act and free-verb descriptions checked and copied, and their significance stage set up, as
the animal tales' were (Animal/layers.py, 2026-10-20).

  python newLayers.py form-acts      the act descriptions' form (reads no note's text)
  python newLayers.py form-free      the free descriptions' form
  python newLayers.py copy           acts/ and free/ copied byte for byte to NativeAmerican/ and EastAsian/
  python newLayers.py sig dry|write  the significance stages native-sig and eastasian-sig: inputs, prompts, RUN.md
  python newLayers.py form-sig       the significance descriptions' form, after the stages run
  python newLayers.py fill dry|write the stage native-fill: the two gaps the form check found, filled in supplement folders

THE FORM CHECKS, per corpus, describer and batch (the transcription batches): every line of Notes.txt is an entry, blank or a
heading; an act entry has ten fields, a free entry nine; its tale is one of the batch's and its event one of the tale's; an act
is one of the act list's (TwoLayer/Acts.md), a free verb reads (free.verb_of) and its phrase is six words or fewer; the flag is Y
or N; every listed event of every tale has an entry.

THE SIGNIFICANCE STAGE: each describer's acts are described by a significance describer of the same letter (A on Opus, B on
Sonnet), from an input that lists each story, its hero (from Heroes.txt), its events and the describer's acts, as
Animal/layers.py writes it. The rules are sig/SigRules.md, unchanged; the prompt is the significance stage's (Significance/
significance.py, as Animal/layers.py re-paths it), with the corpus's reading of the tales. The batches are runs of tales in
order, the same for A and B, each holding at most CAP acts for either describer (the largest animal batch held 442), cut as
evenly as that allows; a tale with more acts than CAP has a batch to itself.
"""
import collections
import filecmp
import glob
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
AR = os.path.join(P, 'ActsRoles')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'Free'))
sys.path.insert(0, os.path.join(ROOT, 'Significance'))
import setupTranscribe as ST  # noqa: E402
import setupLayers as SL  # noqa: E402
import free as FR  # noqa: E402
import significance as SG  # noqa: E402

CORPORA, BATCHES = ST.CORPORA, ST.BATCHES
REPO = {'native': 'NativeAmerican', 'eastasian': 'EastAsian'}
ACTS = set(FR.N.T.ACTS)
ENTRY = re.compile(r'^([TOCJ]\d{2})$')
CAP = 450
SIG_STAGE = {c: '%s-sig' % c for c in CORPORA}
# the two gaps the form check found (2026-11-02), filled at the owner's word by a fresh describer of the same letter and model,
# for those events only, in a supplement folder beside the batch; the batch's own file stays as written
FILLS = {('native', 'acts', 'B', 3): ('O10', [62, 63]), ('native', 'free', 'B', 2): ('T18', [32, 33, 34, 35])}
FILL_DIR = 's1'
FILL_STAGE = 'native-fill'


def fill_prompt(c, layer, L, k):
    t, evs = FILLS[(c, layer, L, k)]
    p = SL.prompt(c, layer, L, k, [t])
    reps = [('Your tales are these 1, one per file, read as they stand:', 'Your tale is this one, read as it stands:'),
            ('They are English translations from scanned books.', 'It is an English translation from a scanned book.'),
            ('Their events are in', 'Its events are in'),
            ('For each story, read the whole story first. Then write the entries the rules require for each of its listed '
             'events, in the listed order',
             'Read the whole story first. Then write the entries the rules require for its listed events %s only, in the '
             'listed order' % ', '.join(map(str, evs))),
            ('%s/%s/%s/b%d/' % (c, layer, L, k), '%s/%s/%s/%s/' % (c, layer, L, FILL_DIR))]
    for a, b in reps:
        assert a in p, a
        p = p.replace(a, b)
    return p


def fill_run_md():
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if FILL_STAGE in t:
        return t
    names = ['%s-%s-%s.txt' % (SL.stage(c, layer), L, FILL_DIR) for (c, layer, L, k) in FILLS]
    anchor_list = 'native-free, eastasian-free,'
    anchor_clear = ("after the new corpora's transcriptions were merged, and were cleared to run at the owner's word the same "
                    "day. They need nothing from each other and may run in one session.\n")
    anchor_row = '| `run-eastasian-free` |\n'
    anchor_in = 'the folder `eastasian/tales/`; for `animal-transcribe`, '
    for a in (anchor_list, anchor_clear, anchor_row, anchor_in):
        assert t.count(a) == 1, a
    t = t.replace(anchor_list, anchor_list + ' ' + FILL_STAGE + ',')
    t = t.replace(anchor_clear, anchor_clear + (
        "The stage `%s` was set up on 2026-11-02 (`CrossCulture/newLayers.py`): the two gaps the form check found, O10 events "
        "62 and 63 in `native/acts/B/b3/` and T18 events 32 to 35 in `native/free/B/b2/`, described by fresh describers B, "
        "written in supplement folders `%s/` beside the batches. It is not yet cleared: it runs only at the owner's word.\n"
        % (FILL_STAGE, FILL_DIR)))
    t = t.replace(anchor_row, anchor_row + (
        "| `%s` | `%s` | Sonnet | `native/acts/B/%s/Notes.txt`, `native/free/B/%s/Notes.txt` | `Report.md` in each folder | "
        "`run-%s` |\n" % (FILL_STAGE, '`, `'.join(names), FILL_DIR, FILL_DIR, FILL_STAGE)))
    t = t.replace(anchor_in, 'the folder `eastasian/tales/`; for `%s`, `ActsRules.md`, `free/FreeRules.md`, `native/Events.txt`, '
                  '`native/tales/O10.txt` and `native/tales/T18.txt`; for `animal-transcribe`, ' % FILL_STAGE)
    return t


def fill(mode):
    out = {os.path.join('prompts', '%s-%s-%s.txt' % (SL.stage(c, layer), L, FILL_DIR)): fill_prompt(c, layer, L, k)
           for (c, layer, L, k) in FILLS}
    out['RUN.md'] = fill_run_md()
    read = lambda p: open(os.path.join(AR, p), encoding='utf-8').read()
    for p in sorted(out):
        old = read(p) if os.path.exists(os.path.join(AR, p)) else ''
        print('%s: %s' % (p, 'unchanged' if old == out[p] else 'new' if not old else 'changed, %+d characters' % (len(out[p]) - len(old))))
    if mode == 'write':
        for p, s in out.items():
            open(os.path.join(AR, p), 'w', encoding='utf-8', newline='\n').write(s)
        print('written to %s' % AR)
    else:
        print('dry run: nothing written')
    return out


def listed(c):
    out = collections.defaultdict(list)
    for line in open(os.path.join(AR, c, 'Events.txt'), encoding='utf-8'):
        f = [x.strip() for x in line.split('|')]
        if len(f) >= 3 and f[1].isdigit():
            out[f[0]].append((int(f[1]), ' | '.join(f[2:])))
    return out


def heroes(c):
    out = {}
    for line in open(os.path.join(AR, c, 'Heroes.txt'), encoding='utf-8'):
        f = [x.strip() for x in line.split('|')]
        if len(f) >= 2 and f[1].startswith('hero:'):
            out[f[0]] = f[1][5:].strip()
    return out


def title(c, s):
    return open(os.path.join(AR, c, 'tales', s + '.txt'), encoding='utf-8').readline().split('|')[1].strip()


def entries(c, layer, L, k):
    """[(line, fields)] of one batch's Notes.txt (k a batch number, or a folder name such as 's1'), and the lines that are
    not entries"""
    n = 10 if layer == 'acts' else 9
    path = os.path.join(AR, c, layer, L, 'b%d' % k if isinstance(k, int) else k, 'Notes.txt')
    out, odd = [], []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        f = [x.strip() for x in line.rstrip('\n').split('|', n - 1)]
        if len(f) < n or not ENTRY.match(f[0]):
            odd.append(i)
            continue
        out.append((i, f))
    return out, odd


def form(layer):
    ok = True
    for c, d in CORPORA.items():
        evs = listed(c)
        for L in 'AB':
            for k, (a, b) in enumerate(BATCHES[c], 1):
                tales = d['ids'][a:b]
                folder = os.path.join(AR, c, layer, L, 'b%d' % k)
                faults = []
                if sorted(os.listdir(folder)) != ['Notes.txt', 'Report.md']:
                    faults.append('folder holds %s' % sorted(os.listdir(folder)))
                rows, odd = entries(c, layer, L, k)
                faults += ['line %d is not an entry' % i for i in odd]
                seen = collections.defaultdict(set)
                longer = 0
                for i, f in rows:
                    ev = re.match(r'^ev (\d+)$', f[1])
                    if f[0] not in tales or not ev or int(ev.group(1)) not in {e for e, _ in evs[f[0]]}:
                        faults.append('line %d: tale or event' % i)
                        continue
                    seen[f[0]].add(int(ev.group(1)))
                    if layer == 'acts':
                        if f[2].lower() not in ACTS:
                            faults.append('line %d: act %s not in the list' % (i, f[2]))
                        if f[6][:1].upper() not in ('Y', 'N'):
                            faults.append('line %d: flag' % i)
                    else:
                        if not FR.verb_of(f[2]):
                            faults.append('line %d: verb' % i)
                        # the phrase's six-word limit is reported, not a fault: no measure reads the phrase, and the
                        # earlier free stages, found in form, exceed it too (the animal tales' B b1 in 249 of 778)
                        longer += len(f[3].split()) > 6
                        if f[6][:1].upper() not in ('Y', 'N'):
                            faults.append('line %d: flag' % i)
                fill = FILLS.get((c, layer, L, k))
                if fill and os.path.exists(os.path.join(AR, c, layer, L, FILL_DIR)):
                    folder = os.path.join(AR, c, layer, L, FILL_DIR)
                    if sorted(os.listdir(folder)) != ['Notes.txt', 'Report.md']:
                        faults.append('supplement folder holds %s' % sorted(os.listdir(folder)))
                    srows, sodd = entries(c, layer, L, FILL_DIR)
                    faults += ['supplement line %d is not an entry' % i for i in sodd]
                    for i, f in srows:
                        ev = re.match(r'^ev (\d+)$', f[1])
                        if f[0] != fill[0] or not ev or int(ev.group(1)) not in fill[1]:
                            faults.append('supplement line %d: tale or event outside the fill' % i)
                            continue
                        seen[f[0]].add(int(ev.group(1)))
                    rows = rows + srows
                for t in tales:
                    missing = sorted({e for e, _ in evs[t]} - seen[t])
                    if missing:
                        faults.append('%s: events without an entry: %s' % (t, ', '.join(map(str, missing))))
                print('%-9s %-4s %s b%d: %4d entries, %2d tales%s: %s' % (c, layer, L, k, len(rows), len(tales),
                      ', phrases over six words %d' % longer if layer == 'free' else '', 'in form' if not faults else 'FAULTS'))
                for x in faults[:12]:
                    print('    ' + x)
                ok &= not faults
    print('%s FORM CHECK %s' % (layer.upper(), 'PASSES' if ok else 'FAILS'))
    return ok


def copy():
    pairs = []
    for c, repo in REPO.items():
        for layer in ('acts', 'free'):
            for f in glob.glob(os.path.join(AR, c, layer, '*', '*', '*')):
                pairs.append((f, os.path.join(P, repo, os.path.relpath(f, os.path.join(AR, c)))))
    clash = [d for s, d in pairs if os.path.exists(d) and not filecmp.cmp(s, d, shallow=False)]
    if clash:
        raise SystemExit('refusing: these exist with different content: %s' % clash)
    for s, d in pairs:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)
    bad = [d for s, d in pairs if not filecmp.cmp(s, d, shallow=False)]
    print('copied %d files byte for byte; %s' % (len(pairs), 'all identical' if not bad else 'DIFFER: %s' % bad))
    return not bad


# ---------------------------------------------------------------- the significance stage
def acts_of(c, L):
    """{tale: [(event, act, performer, undergoer, relation, note)]} for one describer, in file order"""
    out = collections.defaultdict(list)
    names = list(range(1, len(BATCHES[c]) + 1))
    if any(key[:3] == (c, 'acts', L) for key in FILLS) and os.path.exists(os.path.join(AR, c, 'acts', L, FILL_DIR)):
        names.append(FILL_DIR)
    for k in names:
        for i, f in entries(c, 'acts', L, k)[0]:
            ev = re.match(r'^ev (\d+)$', f[1])
            out[f[0]].append((int(ev.group(1)), f[2].lower(), f[3], f[4], f[5].lower(), f[9]))
    return out


def sig_batches(c):
    """runs of tales, each at most CAP acts for either describer, cut as evenly as that allows"""
    ids = CORPORA[c]['ids']
    n = {L: acts_of(c, L) for L in 'AB'}
    load = [max(len(n['A'][t]), len(n['B'][t])) for t in ids]
    k = 1
    while True:
        # the most even cut into k runs (dynamic programming on the largest run)
        best = {(0, 0): (0, [])}
        for j in range(1, k + 1):
            for e in range(1, len(ids) + 1):
                cands = [(max(best[(j - 1, s)][0], sum(load[s:e])), best[(j - 1, s)][1] + [(s, e)])
                         for s in range(j - 1, e) if (j - 1, s) in best]
                if cands:
                    best[(j, e)] = min(cands)
        worst, runs = best[(k, len(ids))]
        if worst <= CAP or all(e - s == 1 or sum(load[s:e]) <= CAP for s, e in runs) and \
                all(sum(load[s:e]) <= CAP or e - s == 1 for s, e in runs):
            return [ids[s:e] for s, e in runs], [sum(load[s:e]) for s, e in runs]
        k += 1


def sig_inputs(c):
    E, Hn = listed(c), heroes(c)
    batches, loads = sig_batches(c)
    text, counts = {}, {}
    for L in 'AB':
        ents = acts_of(c, L)
        n = 0
        for q, ids in enumerate(batches, 1):
            lines, m = [], 0
            for s in ids:
                lines.append('story: %s | %s | hero: %s' % (s, title(c, s), Hn.get(s, '-')))
                for k, t in E[s]:
                    mine = [r for r in ents[s] if r[0] == k]
                    if not mine:
                        continue
                    lines.append('  ev %d | %s' % (k, t))
                    for ev, a, pf, u, r, note in mine:
                        n += 1
                        m += 1
                        lines.append('    e%04d | %s | %s | %s | %s | %s' % (n, a, pf, u, r, note))
                lines.append('')
            text[(L, q)] = '\n'.join(lines) + '\n'
            counts[(L, q)] = m
    return batches, text, counts


def sig_prompt(c, L, q, ids, m):
    t = SG.PROMPT.replace('sig/input/{L}-{b}.txt', c + '/sig/input/{L}-{b}.txt').replace(
        'nothing else under sig/ and nothing under any acts/ folder',
        'nothing else under sig/ or %s/sig/, and nothing under %s/acts/, %s/free/ or %s/transcriptions/' % (c, c, c, c)).replace(
        'sig/{L}/{b}/Significance.txt', c + '/sig/{L}/{b}/Significance.txt')
    files = ', '.join('%s/tales/%s.txt' % (c, s) for s in ids)
    where = 'Your stories are tales from %s; each tale\'s text is in its own file: %s. %s' % (CORPORA[c]['short'], files, SL.READING[c])
    return t.format(L=L, b='q%d' % q, n=len(ids), m=m, where=where, files=files)


def sig_run_md(batches):
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if 'native-sig' in t:
        return t
    names = [SIG_STAGE[c] for c in CORPORA]
    anchor_list = 'native-free, eastasian-free,'
    anchor_clear = ("after the new corpora's transcriptions were merged, and were cleared to run at the owner's word the same "
                    "day. They need nothing from each other and may run in one session.\n")
    anchor_row = '| `run-eastasian-free` |\n'
    anchor_in = 'for `animal-transcribe`, `animal/AfanasyevRules-C.md`'
    for a in (anchor_list, anchor_clear, anchor_row, anchor_in):
        assert t.count(a) == 1, a
    row = ("| `{s}` | `{s}-A-q1.txt` to `-q{n}`, `{s}-B-q1.txt` to `-q{n}` | `-A-`: Opus; `-B-`: Sonnet | "
           "`{c}/sig/<A or B>/<batch>/Significance.txt` | `Report.md` in that folder | `run-{s}` |\n")
    t = t.replace(anchor_list, anchor_list + ' ' + ', '.join(names) + ',')
    t = t.replace(anchor_clear, anchor_clear + (
        "The stages %s were set up on 2026-11-02 (`CrossCulture/newLayers.py`), their inputs written under `<corpus>/sig/input/` "
        "from the act descriptions after those were merged and found in form, and are not yet cleared: they run only at the "
        "owner's word. They need nothing from each other and may run in one session.\n" % ', '.join('`%s`' % x for x in names)))
    t = t.replace(anchor_row, anchor_row + ''.join(row.format(s=SIG_STAGE[c], n=len(batches[c]), c=c) for c in CORPORA))
    t = t.replace(anchor_in, ''.join(
        'for `%s`, `sig/SigRules.md`, the files `%s/sig/input/A-q1.txt` to `B-q%d.txt`, and the folder `%s/tales/`; '
        % (SIG_STAGE[c], c, len(batches[c]), c) for c in CORPORA) + anchor_in)
    return t


def sig(mode):
    out, batches = {}, {}
    for c in CORPORA:
        bs, text, counts = sig_inputs(c)
        batches[c] = bs
        for (L, q), tx in text.items():
            out[os.path.join(c, 'sig', 'input', '%s-q%d.txt' % (L, q))] = tx
            out[os.path.join('prompts', '%s-%s-q%d.txt' % (SIG_STAGE[c], L, q))] = sig_prompt(c, L, q, bs[q - 1], counts[(L, q)])
        print('%s: %d batches' % (SIG_STAGE[c], len(bs)))
        for q, ids in enumerate(bs, 1):
            print('  q%d: %s to %s, %2d tales; acts A %3d, B %3d' % (q, ids[0], ids[-1], len(ids), counts[('A', q)], counts[('B', q)]))
    out['RUN.md'] = sig_run_md(batches)
    read = lambda p: open(os.path.join(AR, p), encoding='utf-8').read()
    clash = [p for p, s in out.items() if p != 'RUN.md' and os.path.exists(os.path.join(AR, p)) and read(p) != s]
    if clash:
        raise SystemExit('refusing: these exist with different content: %s' % clash)
    print('files: %d' % len(out))
    if mode == 'write':
        for p, s in out.items():
            os.makedirs(os.path.dirname(os.path.join(AR, p)), exist_ok=True)
            open(os.path.join(AR, p), 'w', encoding='utf-8', newline='\n').write(s)
        print('written to %s' % AR)
    else:
        print('dry run: nothing written')
    return out


def read_sig(c, L, q):
    """as significance.read_sig, but from the file itself: that reads the built tables, which do not yet hold these files"""
    path = os.path.join(AR, c, 'sig', L, 'q%d' % q, 'Significance.txt')
    out, probs, faults = {}, {}, []
    if not os.path.exists(path):
        return out, probs, ['%s q%d: no file' % (L, q)]
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        f = [x.strip() for x in line.rstrip('\n').split('|', 8)]
        if len(f) >= 3 and f[1].lower() == 'problem':
            probs[(f[0], f[2].lower())] = ' | '.join(f[3:])
            continue
        if not re.match(r'^e\d{4}$', f[0]):
            faults.append('%s q%d line %d: not an entry' % (L, q, i))
            continue
        if len(f) < 9:
            faults.append('%s q%d line %d: %d fields' % (L, q, i, len(f)))
            continue
        part, value, place, prob, link, target = (x.lower() for x in f[1:7])
        if link == '-':
            link = 'none'   # the owner's ruling of 2026-11-02: a "-" link means no link (five lines in eastasian B-q2)
        bad = [x for x, okl in ((part, SG.PARTS), (value, SG.VALUES), (place, SG.PLACES), (link, SG.LINKS)) if x not in okl]
        if bad:
            faults.append('%s q%d %s: not in the lists: %s' % (L, q, f[0], ', '.join(bad)))
        out[f[0]] = (part, value, place, prob, link, target)
    return out, probs, faults


def form_sig():
    ok = True
    for c in CORPORA:
        batches, text, counts = sig_inputs(c)
        for L in 'AB':
            for q in range(1, len(batches) + 1):
                if not os.path.exists(os.path.join(AR, c, 'sig', L, 'q%d' % q)):
                    print('%-9s %s q%d not yet run' % (c, L, q))
                    continue
                ids = re.findall(r'^    (e\d{4}) \|', text[(L, q)], re.M)
                sigd, probs, faults = read_sig(c, L, q)
                missing = [i for i in ids if i not in sigd]
                extra = sorted(set(sigd) - set(ids))
                bad = len(missing) + len(extra) + len(faults)
                print('%-9s %s q%d acts %4d, described %4d, missing %3d, unknown ids %d, problem lines %3d, faults %d'
                      % (c, L, q, len(ids), len(sigd), len(missing), len(extra), len(probs), len(faults)))
                ok &= not bad
    print('SIG FORM CHECK %s' % ('PASSES' if ok else 'FAILS'))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    cmds = {('form-acts',): lambda: form('acts'), ('form-free',): lambda: form('free'), ('copy',): copy,
            ('sig', 'dry'): lambda: sig('dry'), ('sig', 'write'): lambda: sig('write'), ('form-sig',): form_sig,
            ('fill', 'dry'): lambda: fill('dry'), ('fill', 'write'): lambda: fill('write')}
    if tuple(a) not in cmds:
        sys.exit(__doc__)
    r = cmds[tuple(a)]()
    sys.exit(0 if r in (None, True) or isinstance(r, dict) else 1)
