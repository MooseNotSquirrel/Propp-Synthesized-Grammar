#!/usr/bin/env python3
"""
setupHeroes.py -- the heroes stage of the two new corpora (CrossCultureProtocol.md section 3: heroes by two readers), set up
in Propp-ActsRoles as animal-heroes was (Data/session7.py, setup1): native-heroes and eastasian-heroes.

  python setupHeroes.py dry      say what would be written, and change nothing
  python setupHeroes.py write    write it (refused if a file it writes exists)

Each reader is given its stories as session7.py gives them: each story's identifier and title, then its listed events,
numbered, from the corpus's Events.txt; no tale text and no transcription. The prompt is Heroes/heroes.py's PROMPT, unchanged.
Readers A on Opus and B on Sonnet. The batches are runs of tales in order, cut as evenly as the events allow, at most CAP events
each (the animal batches held 640 and 643): native in three, East Asian in two. Writes heroes/stories/<batch>.txt, the prompts
hero-<A or B>-<batch>.txt, and RUN.md's two stages, set up and not cleared.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'Heroes'))
import newLayers as NL  # noqa: E402
import heroes as H  # noqa: E402

AR, CORPORA = NL.AR, NL.CORPORA
PREFIX = {'native': 'nh', 'eastasian': 'eh'}
STAGE = {'native': 'native-heroes', 'eastasian': 'eastasian-heroes'}
CAP = 650


def batches(c):
    ids = CORPORA[c]['ids']
    ev = NL.listed(c)
    load = [len(ev[t]) for t in ids]
    k = 1
    while True:
        best = {(0, 0): (0, [])}
        for j in range(1, k + 1):
            for e in range(1, len(ids) + 1):
                cands = [(max(best[(j - 1, s)][0], sum(load[s:e])), best[(j - 1, s)][1] + [(s, e)])
                         for s in range(j - 1, e) if (j - 1, s) in best]
                if cands:
                    best[(j, e)] = min(cands)
        worst, runs = best[(k, len(ids))]
        if worst <= CAP:
            return [(ids[s:e], sum(load[s:e])) for s, e in runs]
        k += 1


def material(c, ids):
    ev = NL.listed(c)
    lines = []
    for s in ids:
        lines.append('story: %s | %s' % (s, NL.title(c, s)))
        lines += ['  %d | %s' % (n, t) for n, t in ev[s]]
        lines.append('')
    return '\n'.join(lines) + '\n'


def run_md(names):
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if 'native-heroes' in t:
        return t
    stages = [STAGE[c] for c in CORPORA]
    anchor_list = 'native-sig-1, native-sig-2, eastasian-sig,'
    anchor_row = '| `run-eastasian-sig` |\n'
    anchor_in = 'for `animal-transcribe`, `animal/AfanasyevRules-C.md`'
    for a in (anchor_list, anchor_row, anchor_in):
        assert t.count(a) == 1, a
    t = t.replace(anchor_list, anchor_list + ' ' + ', '.join(stages) + ',')
    row = ("| `{s}` | `hero-A-{f}.txt` to `-{l}`, `hero-B-{f}.txt` to `-{l}` | `-A-`: Opus; `-B-`: Sonnet | "
           "`heroes/answers/<A or B>/<batch>/Heroes.txt` | `Report.md` in that folder | `run-{s}` |\n")
    t = t.replace(anchor_row, anchor_row + ''.join(row.format(s=STAGE[c], f=names[c][0], l=names[c][-1]) for c in CORPORA))
    t = t.replace(anchor_in, ''.join('for `%s`, the files `heroes/stories/%s.txt` to `%s.txt`; ' % (STAGE[c], names[c][0], names[c][-1])
                                     for c in CORPORA) + anchor_in)
    clear = ("The stages `native-heroes` and `eastasian-heroes` were set up on 2026-11-03 (`CrossCulture/setupHeroes.py`), "
             "as `animal-heroes` was, and are not yet cleared: they run only at the owner's word. They need nothing from each "
             "other and may run in one session.\n")
    anchor_clear = "`native-sig-2` was cleared to run at the owner's word the same day."
    assert t.count(anchor_clear) == 1
    i = t.index(anchor_clear)
    j = t.index('\n', i) + 1
    return t[:j] + clear + t[j:]


def main(mode):
    out, names = {}, {}
    for c in CORPORA:
        bs = batches(c)
        names[c] = []
        for q, (ids, n) in enumerate(bs, 1):
            b = '%s%d' % (PREFIX[c], q)
            names[c].append(b)
            out[os.path.join('heroes', 'stories', b + '.txt')] = material(c, ids)
            for L in 'AB':
                out[os.path.join('prompts', 'hero-%s-%s.txt' % (L, b))] = H.PROMPT.format(b=b, n=len(ids), L=L, cast='')
            print('%s %s: %s to %s, %2d tales, %3d events' % (STAGE[c], b, ids[0], ids[-1], len(ids), n))
    out['RUN.md'] = run_md(names)
    clash = [p for p in out if p != 'RUN.md' and os.path.exists(os.path.join(AR, p))]
    if clash:
        raise SystemExit('refusing: these exist: %s' % clash)
    print('files: %d' % len(out))
    if mode == 'write':
        for p, s in out.items():
            os.makedirs(os.path.dirname(os.path.join(AR, p)), exist_ok=True)
            open(os.path.join(AR, p), 'w', encoding='utf-8', newline='\n').write(s)
        print('written to %s' % AR)
    else:
        print('dry run: nothing written')
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a not in (['dry'], ['write']):
        sys.exit(__doc__)
    main(a[0])
