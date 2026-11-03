#!/usr/bin/env python3
"""
composition.py -- EXPLORATORY: each corpus's functions by Propp's ten sections, the composition the story grammar does not see
(it scores order against shuffles of a story's own functions, so a story's mix of sections is held fixed). Asked by the owner on
2026-11-02, on the question whether fables lean on Propp's preparatory section.

  python composition.py    write StoryGrammar/Composition.txt

The units are storyGrammar.load's (rows marked Y, keys tragedyScore.NUM knows; the myths the library's 126 stories), all stories
of at least three units, held out or not; each version weighted 1 over its story's number of versions. Per corpus and
transcriber: the share of units in each section (constraintGrammar.SECTION_GROUPS), and the mean number of sections a story
reaches. No model, no test.
"""
import os

import storyGrammar as S

OUT = os.path.join(S.HERE, 'Composition.txt')
ORDER = ['tale', 'fable', 'animal', 'tragedy', 'myth']


def shares(items):
    tot = [0.0] * len(S.CG.SECTION_NAMES)
    n = reach = stories = 0.0
    for _, w, us, ms in items:
        secs = set()
        for u in us:
            k = S.CG.SEC.get(u, -1)
            if k >= 0:
                tot[k] += w
                n += w
                secs.add(k)
        reach += w * len(secs)
        stories += w
    return [x / n for x in tot], reach / stories


def main():
    data = {L: S.load(L) for L in 'AB'}
    res = {(g, L): shares(data[L][g]['fit'] + data[L][g]['held']) for g in ORDER for L in 'AB'}
    rep = ['# Composition.txt -- composition.py: EXPLORATORY; each corpus\'s functions by Propp\'s sections, per cent of its units, '
           'transcriber A / B', '#  all stories of at least three units; each version weighted 1 over its story\'s versions', '',
           '%-20s' % 'section' + ''.join('%14s' % g for g in ORDER)]
    for k, name in enumerate(S.CG.SECTION_NAMES):
        rep.append('%-20s' % name + ''.join('%7.0f / %-4.0f' % (100 * res[(g, 'A')][0][k], 100 * res[(g, 'B')][0][k]) for g in ORDER))
    rep.append('%-20s' % 'sections reached' + ''.join('%7.1f / %-4.1f' % (res[(g, 'A')][1], res[(g, 'B')][1]) for g in ORDER))
    text = '\n'.join(rep) + '\n'
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
