#!/usr/bin/env python3
"""
session7.py -- the reader stages of Data/Plan.md session 7 (Data/Session7Protocol.md).

  python session7.py setup1 --dry   say what run 1's setup would write, and write nothing
  python session7.py setup1         write run 1's material and prompts into StoryLanguage/Projects/ActsRoles:
                                    the animal tales for the hero readers (heroes/stories/ah1.txt, ah2.txt;
                                    prompts hero-A-ah1 ... hero-B-ah2), and the act describers' prompts for
                                    P01 to P08 (hacts-A-g13 ... hacts-B-g16), with P05 to P08's cast lists
                                    copied beside the plays already under held/tragedy/plays/

The prompts are the earlier stages' own, with only the paths, counts and play names changed: Heroes/heroes.py's
PROMPT for the heroes, and the act stages' prompt for the plays (prompts/pacts-A-g5.txt, its wording kept).
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
AR = os.path.join(P, 'ActsRoles')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'Heroes'))
import tables as DT  # noqa: E402
import heroes as H  # noqa: E402

HERO_BATCHES = {'ah1': ['A%03d' % i for i in range(1, 26)], 'ah2': ['A%03d' % i for i in range(26, 51)]}
ACT_BATCHES = {'g13': ['P01', 'P02'], 'g14': ['P03', 'P04'], 'g15': ['P05', 'P06'], 'g16': ['P07', 'P08']}
ORDER = {l.split('|')[0].strip(): (l.split('|')[2].strip(), l.split('|')[3].strip())
         for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}

ACT_PROMPT = ("You are describing what happens in two Greek plays, {names}, in English translation. You start with no background on the project, and you should not look for any.\n\n"
              "Read ActsRules.md in this repository first, in full, and follow it exactly. Each play is in its folder under held/tragedy/plays/: Text.txt, one speech per line; Events.txt, its events{castfile}. {castrule} Write the two plays one after the other.\n\n"
              "For each story, read the whole story first. Then write the entries the rules require for each of its listed events, in the listed order: one entry per act, each with its act, performer, undergoer, relation and Y or N.\n\n"
              "Open only ActsRules.md, {files} and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under held/acts/ but your own folder. Do not search the web. You are describer {L}.\n\n"
              "Write one file, and nothing else, held/acts/{L}/{b}/Notes.txt (create the folders), in the format of the rules' section \"The format\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on.\n\n"
              "Then reply with the report the rules' last section asks for.\n")


def title(s):
    line = open(os.path.join(P, 'AnimalTales', 'tales', s + '.txt'), encoding='utf-8').readline()
    return line.split('|')[1].strip()


def hero_material():
    ev = {}
    for r in DT.rows('events'):
        if r['story'].startswith('animal:'):
            ev.setdefault(DT.local(r['story']), []).append((int(r['event']), r['text']))
    out = {}
    for b, ids in HERO_BATCHES.items():
        lines = []
        for s in ids:
            lines.append('story: %s | %s' % (s, title(s)))
            lines += ['  %d | %s' % (n, t) for n, t in ev[s]]
            lines.append('')
        out[b] = '\n'.join(lines) + '\n'
    return out


def act_prompt(L, b):
    plays = ACT_BATCHES[b]
    cast = all(os.path.exists(os.path.join(P, 'Tragedy', 'plays', p, 'Cast.txt')) for p in plays)
    names = ' and '.join("%s's %s (%s)" % (ORDER[p][0], ORDER[p][1], p) for p in plays)
    files = ', '.join('held/tragedy/plays/%s/Text.txt, Events.txt%s' % (p, ' and Cast.txt' if cast else '') for p in plays)
    return ACT_PROMPT.format(
        names=names, files=files, L=L, b=b,
        castfile='; and Cast.txt, its cast' if cast else '',
        castrule='Name every performer and undergoer exactly as the play\'s Cast.txt names them.' if cast else
                 'Name every performer and undergoer as the text names them.'), cast


def setup1(dry):
    writes = []
    for b, text in hero_material().items():
        writes.append((os.path.join(AR, 'heroes', 'stories', b + '.txt'), text))
        for L in 'AB':
            writes.append((os.path.join(AR, 'prompts', 'hero-%s-%s.txt' % (L, b)),
                           H.PROMPT.format(b=b, n=len(HERO_BATCHES[b]), L=L, cast='')))
    copies = []
    for b, plays in ACT_BATCHES.items():
        for L in 'AB':
            text, cast = act_prompt(L, b)
            writes.append((os.path.join(AR, 'prompts', 'hacts-%s-%s.txt' % (L, b)), text))
        for p in plays:
            src = os.path.join(P, 'Tragedy', 'plays', p, 'Cast.txt')
            if os.path.exists(src):
                copies.append((src, os.path.join(AR, 'held', 'tragedy', 'plays', p, 'Cast.txt')))
    for path, text in writes:
        exists = os.path.exists(path)
        print('%s %-60s %6d bytes%s' % ('would write' if dry else 'write', os.path.relpath(path, P), len(text.encode('utf-8')),
                                         '  (EXISTS: refused)' if exists else ''))
        if exists:
            raise SystemExit('refusing to overwrite %s' % path)
    for src, dst in copies:
        print('%s %-60s from %s' % ('would copy' if dry else 'copy', os.path.relpath(dst, P), os.path.relpath(src, P)))
    if dry:
        print('dry run: %d files to write, %d to copy; nothing written' % (len(writes), len(copies)))
        return
    for path, text in writes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    for src, dst in copies:
        shutil.copyfile(src, dst)
    print('written: %d files, %d copied' % (len(writes), len(copies)))


FIVE = ['A098', 'F043', 'F060', 'F114', 'F124']
SIG_BATCHES = {'g13': ['P01', 'P02'], 'g14': ['P03', 'P04'], 'g15': ['P05', 'P06'], 'g16': ['P07', 'P08']}


def sig_modules():
    sys.path.insert(0, os.path.join(ROOT, 'Significance'))
    import significance as S
    return S


def sig_text(stories, entries_of, S):
    """the significance input, as Significance/significance.py's inputs() writes it: each story with its hero, each
    event with the describer's acts, every act numbered; returns (text, rows)"""
    St = {s: (title, ev) for items in H.stories().values() for s, title, _, ev in items}
    lines, rows = [], []
    for s in stories:
        title, evs = St[s]
        lines.append('story: %s | %s | hero: %s' % (s, title, S.hero_line(s)))
        ents = entries_of(s)
        for k, t in evs:
            mine = [e for e in ents if e[0] == k]
            if not mine:
                continue
            lines.append('  ev %d | %s' % (k, t))
            for ev, a, pf, u, r, note in mine:
                rows.append(None)
                eid = 'e%04d' % len(rows)
                lines.append('    %s | %s | %s | %s | %s | %s' % (eid, a, pf, u, r, note))
        lines.append('')
    return '\n'.join(lines) + '\n', len(rows)


def held_entries(L):
    def of(s):
        return [(int(r['event']), r['act'].lower(), r['performer'], r['undergoer'], r['relation'].lower(), r['note'])
                for r in DT.rows('acts') if r['study'] == 'held' and r['reader'] == L and DT.local(r['story']) == s and not r['id_flag']]
    return of


def setup2(dry):
    S = sig_modules()
    writes = []
    held_prompt = S.PROMPT.replace('sig/input/{L}-{b}.txt', 'held/sig/input/{L}-{b}.txt').replace(
        'nothing else under sig/ and nothing under any acts/ folder', 'nothing else under sig/ or held/sig/ and nothing under any acts/ folder').replace(
        'sig/{L}/{b}/Significance.txt', 'held/sig/{L}/{b}/Significance.txt')
    five_prompt = S.PROMPT.replace('sig/input/{L}-{b}.txt', 'five/sig/input/{L}-{b}.txt').replace(
        'nothing else under sig/ and nothing under any acts/ folder', 'nothing else under sig/ or five/sig/ and nothing under any acts/ folder').replace(
        'sig/{L}/{b}/Significance.txt', 'five/sig/{L}/{b}/Significance.txt')
    for L in 'AB':
        n = 0
        for b, plays in SIG_BATCHES.items():
            def counted(s, of=held_entries(L)):
                return of(s)
            text, m = sig_text(plays, counted, S)
            # number the acts on across this describer's batches, as inputs() does
            out = []
            for line in text.split('\n'):
                if line.startswith('    e'):
                    n += 1
                    line = '    e%04d' % n + line[9:]
                out.append(line)
            text = '\n'.join(out)
            names = ' and '.join("%s's %s (%s)" % (ORDER[p][0], ORDER[p][1], p) for p in plays)
            where = ("Your stories are Greek plays, %s, in English translation; each play's text is in its folder under held/tragedy/plays/, in Text.txt, one speech per line." % names)
            files = ', '.join('held/tragedy/plays/%s/Text.txt' % p for p in plays)
            writes.append((os.path.join(AR, 'held', 'sig', 'input', '%s-%s.txt' % (L, b)), text))
            writes.append((os.path.join(AR, 'prompts', 'hsig-%s-%s.txt' % (L, b)),
                           held_prompt.format(L=L, b=b, n=len(plays), m=m, where=where, files=files)))
        text, m = sig_text(FIVE, lambda s, L=L: S.act_entries(L, s), S)
        where = ("Your stories are one tale from Aleksandr Afanasyev's collection of Russian folktales, in Russian, in tale/tales/A098.txt; "
                 "and four of Aesop's fables, in George Fyler Townsend's 1867 translation, in fable/Fables.txt, one per line as \"identifier | title | text\".")
        writes.append((os.path.join(AR, 'five', 'sig', 'input', '%s-v1.txt' % L), text))
        writes.append((os.path.join(AR, 'prompts', 'fsig-%s-v1.txt' % L),
                       five_prompt.format(L=L, b='v1', n=len(FIVE), m=m, where=where, files='tale/tales/A098.txt, fable/Fables.txt')))
    for path, text in writes:
        exists = os.path.exists(path)
        acts = text.count('\n    e')
        print('%s %-44s %6d bytes%s%s' % ('would write' if dry else 'write', os.path.relpath(path, P), len(text.encode('utf-8')),
                                         ', %d acts' % acts if acts else '', '  (EXISTS: refused)' if exists else ''))
        if exists:
            raise SystemExit('refusing to overwrite %s' % path)
    if dry:
        print('dry run: %d files to write; nothing written' % len(writes))
        return
    for path, text in writes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print('written: %d files' % len(writes))


def form1():
    """Session7Protocol.md's form checks for run 1, from the rebuilt tables; prints the lines and writes them to
    Data/forms/hacts.txt and Data/forms/aheroes.txt"""
    sys.path.insert(0, os.path.join(ROOT, 'TwoLayer'))
    sys.path.insert(0, os.path.join(ROOT, 'Problems'))
    import twoLayer as T
    import problems as Pm
    ev = {}
    for r in DT.rows('events'):
        ev.setdefault(r['story'], set()).add(int(r['event']))
    acts = [r for r in DT.rows('acts') if r['study'] == 'held']
    out, total = [], 0
    for L in 'AB':
        for b, plays in ACT_BATCHES.items():
            rows = [r for r in acts if r['reader'] == L and r['batch'] == b]
            got = {}
            for r in rows:
                got.setdefault(r['story'], set()).add(int(r['event']))
            uncovered = sum(len(ev['tragedy:' + p] - got.get('tragedy:' + p, set())) for p in plays)
            bad = sum(1 for r in rows if r['act'].lower() not in T.ACTS or r['relation'].lower() not in Pm.RELATIONS
                      or r['matters'][:1].upper() not in ('Y', 'N'))
            faults = sum(1 for r in rows if r['id_flag'])
            out.append('%s %-3s stories %2d, entries %4d, uncovered events %3d, out-of-list entries %3d, faults %d'
                       % (L, b, len(plays), len(rows) - faults, uncovered, bad, faults))
            total += uncovered + bad + faults
    out.append('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)
    open(os.path.join(HERE, 'forms', 'hacts.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))
    # the heroes: one line per story, in order, with a hero, a confidence and a reason
    hout, htot = [], 0
    for L in 'AB':
        for b, ids in HERO_BATCHES.items():
            path = os.path.join(AR, 'heroes', 'answers', L, b, 'Heroes.txt')
            rows = DT.file_rows('heroes', path)
            order = [DT.local(r['story']) for r in rows]
            bad = sum(1 for r in rows if not r['hero'].strip() or r['confidence'].strip().lower() not in ('high', 'medium', 'low')
                      or not r['basis'].strip() or int(r['fields']) < 4)
            ok = order == ids and not bad
            hout.append('%s %-3s stories %2d of %d, in order %s, entries %2d, malformed %d' % (
                L, b, len(rows), len(ids), 'yes' if order == ids else 'NO', len(rows), bad))
            htot += 0 if ok else 1
    hout.append('IN FORM' if htot == 0 else 'NOT IN FORM: %d batch(es)' % htot)
    open(os.path.join(HERE, 'forms', 'aheroes.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(hout) + '\n')
    print('\n'.join(hout))


def form2():
    """Session7Protocol.md's form checks for run 2, from the rebuilt tables; prints the lines and writes them to
    Data/forms/hsig.txt and Data/forms/fsig.txt"""
    S = sig_modules()
    saved = S.SIG
    for base, batches, name in (('held', list(SIG_BATCHES), 'hsig.txt'), ('five', ['v1'], 'fsig.txt')):
        out, total = [], 0
        S.SIG = os.path.join(AR, base, 'sig')
        try:
            for L in 'AB':
                for b in batches:
                    inp = open(os.path.join(S.SIG, 'input', '%s-%s.txt' % (L, b)), encoding='utf-8').read()
                    ids = [l.split('|')[0].strip() for l in inp.split('\n') if l.startswith('    e')]
                    sig, probs, faults = S.read_sig(L, b)
                    missing = [e for e in ids if e not in sig]
                    extra = sorted(set(sig) - set(ids))
                    out.append('%s %-3s acts %4d, described %4d, missing %3d, unknown ids %d, problem lines %3d, faults %d'
                               % (L, b, len(ids), len(sig), len(missing), len(extra), len(probs), len(faults)))
                    total += len(missing) + len(extra) + len(faults)
        finally:
            S.SIG = saved
        out.append('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)
        open(os.path.join(HERE, 'forms', name), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print('\n'.join(out))


def agreement1():
    """Session7Protocol.md's report: how often the two readers name the same hero, by the word rule unchanged and
    with its role words kept"""
    sys.path.insert(0, os.path.join(ROOT, 'Heroes'))
    import withJudgedHeroes as W
    ans = {L: {} for L in 'AB'}
    for L in 'AB':
        for b in HERO_BATCHES:
            for r in DT.file_rows('heroes', os.path.join(AR, 'heroes', 'answers', L, b, 'Heroes.txt')):
                ans[L][DT.local(r['story'])] = r['hero']
    role = {'little', 'old', 'young', 'youngest', 'eldest', 'son', 'daughter', 'man', 'woman'}
    keep = W.STOP - role

    def words2(name):
        name = W.latin(name)
        if name.startswith('no single hero'):
            name = name.split(':', 1)[1] if ':' in name else ''
        return {w.rstrip('s') for w in W.re.findall(r'[^\W\d_]+', name) if w not in keep and len(w) > 2}
    ids = sorted(set(ans['A']) & set(ans['B']))
    lines = ['# animal-heroes, agreement of the two readers (Session7Protocol.md); reported, not judged.', '']
    for label, fn in (('the word rule unchanged (withJudgedHeroes.words)', W.words), ('with its role words kept', words2)):
        agree = [s for s in ids if fn(ans['A'][s]) & fn(ans['B'][s]) or
                 (ans['A'][s].lower().startswith('no single') and ans['B'][s].lower().startswith('no single'))]
        lines.append('%s: %d of %d stories agree' % (label, len(agree), len(ids)))
    lines.append('')
    lines.append('story | reader A | reader B')
    lines += ['%s | %s | %s' % (s, ans['A'][s], ans['B'][s]) for s in ids]
    os.makedirs(os.path.join(HERE, 'Parity'), exist_ok=True)
    open(os.path.join(HERE, 'Parity', 'heroes-animal.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:4]))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup1', '--dry']:
        setup1(True)
    elif a == ['setup1']:
        setup1(False)
    elif a == ['setup2', '--dry']:
        setup2(True)
    elif a == ['setup2']:
        setup2(False)
    elif a == ['form1']:
        form1()
    elif a == ['form2']:
        form2()
    elif a == ['agreement1']:
        agreement1()
    else:
        sys.exit(__doc__)
