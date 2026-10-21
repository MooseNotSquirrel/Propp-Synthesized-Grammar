#!/usr/bin/env python3
"""
heroes.py -- judged heroes against the counting rule (HeroProtocol.md).

  python heroes.py setup   writes the readers' material and prompts into Story Language/ActsRoles/heroes/
  python heroes.py score   writes Heroes/HeroRun.txt and Heroes/JudgedHeroes.txt

Written in full before any reader saw a story.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
OUT = os.path.join(P, 'ActsRoles', 'heroes')
GENRES = ('tale', 'fable', 'tragedy')
sys.path.insert(0, os.path.join(ROOT, 'Data'))
import tables as DT  # noqa: E402


def events(path):
    """{story: [(event, text)]} from one event list, read from the normalized tables (Data/tables.py)"""
    out = collections.OrderedDict()
    for r in DT.file_rows('events', path):
        s = DT.local(r['story'])
        if re.match(r'^[PFA]\d{2}', s):
            out.setdefault(s, []).append((int(r['event']), r['text']))
    return out


def stories():
    """{genre: [(id, title, cast or None, [(n, text)])]}"""
    out = {}
    af = events(os.path.join(P, 'Afanasyev', 'Events.txt'))
    out['tale'] = [(s, open(os.path.join(P, 'Afanasyev', 'tales', s + '.txt'), encoding='utf-8').readline().split('|')[1].strip(),
                    None, ev) for s, ev in af.items()]
    titles = {}
    for repo in ('Aesop', 'Fables'):
        for l in open(os.path.join(P, repo, 'Fables.txt'), encoding='utf-8'):
            f = l.split('|')
            if len(f) >= 2:
                titles[f[0].strip()] = f[1].strip()
    drawn = open(os.path.join(P, 'Aesop', 'Sample.txt'), encoding='utf-8').read().split()
    fa = events(os.path.join(P, 'Aesop', 'Events.txt'))
    fb = events(os.path.join(P, 'Fables', 'Events.txt'))
    out['fable'] = [(s, titles.get(s, ''), None, fa[s]) for s in drawn if s in fa] + \
                   [(s, titles.get(s, ''), None, ev) for s, ev in fb.items()]
    order = {l.split('|')[0].strip(): l.split('|')[3].strip()
             for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}
    out['tragedy'] = []
    for i in range(1, 33):
        p = 'P%02d' % i
        d = os.path.join(P, 'Tragedy', 'plays', p)
        cast = [l.split('|')[1].strip() for l in open(os.path.join(d, 'Cast.txt'), encoding='utf-8') if '|' in l] \
            if os.path.exists(os.path.join(d, 'Cast.txt')) else None
        out['tragedy'].append((p, order[p], cast, events(os.path.join(d, 'Events.txt'))[p]))
    return out


def batches(S):
    b = {'tale': {'h1': S['tale'][:23], 'h2': S['tale'][23:]}}
    f = S['fable']
    b['fable'] = {'h%d' % (i + 3): f[i * 50:(i + 1) * 50] for i in range(4)}
    t = S['tragedy']
    b['tragedy'] = {'h%d' % (i + 7): t[i * 8:(i + 1) * 8] for i in range(4)}
    return b


PROMPT = """You are reading short accounts of stories and saying, for each, whose story it is. You start with no background on the project, and you should not look for any.

Read heroes/stories/{b}.txt in this repository in full. It holds {n} stories. Each is given by its identifier and title{cast}, and then as a numbered list of its events, in order.

For each story, decide who its hero is. The hero is the character whose fortunes the story follows: whose want or misfortune sets it going, who acts toward its outcome or suffers it, and whom the telling stays with; not simply the one who appears most. Read each whole list of events before you decide. If the story truly divides between two or three characters, say so rather than choosing.

Open only heroes/stories/{b}.txt. Do not open, list or search any other file or folder in this repository, in particular nothing under heroes/answers/ but your own folder. Do not search the web, and do not use what you may know of these stories from elsewhere: judge from the events given. You are reader {L}.

Write one file, and nothing else, heroes/answers/{L}/{b}/Heroes.txt (create the folders): one line per story, in the order of the file, in the form

STORY | HERO | CONFIDENCE | REASON

where HERO is the character's name as the events name it, or "no single hero: NAME; NAME" naming the characters the story divides between; CONFIDENCE is high, medium or low; and REASON is one short sentence. For example: "Z000 | the Miller | high | the story follows his attempt to please everyone and ends with his loss". Keep any working file inside heroes/answers/{L}/{b}/ and delete it before you finish.

Then reply with a short report: the number of stories, how many you judged with low confidence, and how many you found to have no single hero.
"""


def setup():
    S = stories()
    B = batches(S)
    os.makedirs(os.path.join(OUT, 'stories'), exist_ok=True)
    prompts = os.path.join(os.path.dirname(OUT), 'prompts')
    for g, bs in B.items():
        for b, items in bs.items():
            with open(os.path.join(OUT, 'stories', b + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
                for s, title, cast, ev in items:
                    f.write('story: %s | %s\n' % (s, title))
                    if cast:
                        f.write('cast: %s\n' % '; '.join(cast))
                    for n, text in ev:
                        f.write('  %d | %s\n' % (n, text))
                    f.write('\n')
            for L in 'AB':
                open(os.path.join(prompts, 'hero-%s-%s.txt' % (L, b)), 'w', encoding='utf-8', newline='\n').write(
                    PROMPT.format(b=b, n=len(items), L=L, cast=', its cast list,' if g == 'tragedy' else ''))
    print({g: {b: len(v) for b, v in bs.items()} for g, bs in B.items()})


# ---------------------------------------------------------------- scoring
def key(name):
    if name.lower().startswith('no single hero'):
        return 'NONE'
    words = [w for w in re.findall(r'[^\W\d_]+', name.lower()) if w not in ('the', 'a', 'an')]
    return words[0] if words else ''


def rule_heroes():
    h = {}
    paths = [os.path.join(P, 'Afanasyev', 'Heroes.txt'), os.path.join(P, 'Aesop', 'Heroes.txt'),
             os.path.join(P, 'Fables', 'Heroes.txt')] + glob.glob(os.path.join(P, 'Tragedy', 'plays', 'P*', 'Hero.txt'))
    for path in paths:      # the event listers' heroes, from the normalized tables (Data/tables.py)
        for r in DT.file_rows('heroes', path):
            h[DT.local(r['story'])] = {key(n) for n in r['hero'].replace('hero:', '').split(';') if n.strip()}
    return h


def answers(L):
    out = {}
    for p in glob.glob(os.path.join(OUT, 'answers', L, 'h*', 'Heroes.txt')):    # from the normalized tables
        for r in DT.file_rows('heroes', p):
            s = DT.local(r['story'])
            if int(r['fields']) >= 3 and re.match(r'^[PFA]\d{2}', s):
                out[s] = (r['hero'], r['confidence'].lower())
    return out


def score():
    S = stories()
    gen = {s: g for g, items in S.items() for s, _, _, _ in items}
    A, B, R = answers('A'), answers('B'), rule_heroes()
    rep = ['# HeroRun.txt -- heroes.py score, as HeroProtocol.md freezes it.', '']
    agree_rate, rule_rate = {}, {}
    judged = []
    for g in GENRES:
        ss = [s for s, _, _, _ in S[g] if s in A and s in B]
        both = [s for s in ss if key(A[s][0]) == key(B[s][0])]
        withrule = [s for s in both if key(A[s][0]) in R.get(s, set())]
        none = sum(1 for s in ss for X in (A, B) if key(X[s][0]) == 'NONE')
        agree_rate[g] = len(both) / float(len(ss)) if ss else 0.0
        rule_rate[g] = len(withrule) / float(len(both)) if both else 0.0
        rep.append('%-8s stories %3d; readers agree %3d (%.0f%%); the rule matches the agreed hero in %3d of %d (%.0f%%); '
                   '"no single hero" answers %d of %d' % (g, len(ss), len(both), 100 * agree_rate[g], len(withrule), len(both),
                                                         100 * rule_rate[g], none, 2 * len(ss)))
        for s in ss:
            if s in both:
                judged.append('%s | %s | %s' % (s, A[s][0], 'agrees with the rule' if s in withrule else 'differs from the rule'))
    rep += ['', 'PREDICTIONS',
            '  1. readers agree on at least 90%% of the Russian tales: %.0f%% -> %s'
            % (100 * agree_rate['tale'], 'HOLDS' if agree_rate['tale'] >= 0.90 else 'FAILS'),
            '  2. they agree less often in the tragedies than in the tales: %.0f%% against %.0f%% -> %s'
            % (100 * agree_rate['tragedy'], 100 * agree_rate['tale'], 'HOLDS' if agree_rate['tragedy'] < agree_rate['tale'] else 'FAILS'),
            '  3. the rule matches the agreed hero less often in the tragedies than in the tales: %.0f%% against %.0f%% -> %s'
            % (100 * rule_rate['tragedy'], 100 * rule_rate['tale'], 'HOLDS' if rule_rate['tragedy'] < rule_rate['tale'] else 'FAILS'),
            '', 'DISAGREEMENTS (reported)']
    for g in GENRES:
        for s, _, _, _ in S[g]:
            if s in A and s in B and key(A[s][0]) != key(B[s][0]):
                rep.append('  %s: A %s (%s); B %s (%s); rule %s' % (s, A[s][0], A[s][1], B[s][0], B[s][1], ', '.join(sorted(R.get(s, [])))))
    open(os.path.join(HERE, 'HeroRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    open(os.path.join(HERE, 'JudgedHeroes.txt'), 'w', encoding='utf-8', newline='\n').write(
        '# JudgedHeroes.txt -- heroes both readers agree on (heroes.py score)\n' + '\n'.join(judged) + '\n')
    print('\n'.join(rep[:12]))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup']:
        setup()
    elif a == ['score']:
        score()
    else:
        sys.exit(__doc__)
