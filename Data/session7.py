#!/usr/bin/env python3
"""
session7.py -- the reader stages of Data/Plan.md session 7 (Data/Session7Protocol.md).

  python session7.py setup1 --dry   say what run 1's setup would write, and write nothing
  python session7.py setup1         write run 1's material and prompts into Story Language/ActsRoles:
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


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup1', '--dry']:
        setup1(True)
    elif a == ['setup1']:
        setup1(False)
    else:
        sys.exit(__doc__)
