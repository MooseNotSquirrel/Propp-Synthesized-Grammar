#!/usr/bin/env python3
"""
exploreConcordance.py -- EXPLORATORY, outside the predictions: why some corpora's held-out concordance (prediction 1) is lower.
Asked by the owner on 2026-10-28, after the freeze.

  python exploreConcordance.py    write StoryGrammar/ExploreConcordance.txt

The frozen grammar is not refitted or changed. The weights are recomputed by the committed program (storyGrammar.fit, which
G4 shows is deterministic), and used only if their text is byte-identical to the frozen Weights-A.txt and Weights-B.txt.
Each held-out story's 200 alternatives are drawn exactly as `storyGrammar.py run` drew them, and each corpus's mean concordance
must equal the record's (StoryGrammarRun.txt) before anything is reported.

For each held-out story: its number of functions; the number of Propp's ten sections its functions reach; the share of its
alternatives that tie with it (score equal); its concordance (ties a half); and its concordance among the alternatives that do
not tie. Per corpus, the means of these; and the six tragedies one by one, for each transcriber.
"""
import os
import re

import numpy as np

import storyGrammar as S

OUT = os.path.join(S.HERE, 'ExploreConcordance.txt')


def frozen(L):
    w = S.fit(L)
    text = open(S.WEIGHTS % L, encoding='utf-8').read()
    if S.weights_text(L, w) != text:
        raise SystemExit('the recomputed weights for %s differ from the frozen Weights-%s.txt; nothing reported' % (L, L))
    return w


def recorded():
    """the mean concordance per (corpus, transcriber) from the record"""
    out, L = {}, None
    for line in open(S.RECORD, encoding='utf-8'):
        m = re.match(r'^TRANSCRIBER (\w)', line)
        if m:
            L = m.group(1)
        m = re.match(r'^\s+(\w+)\s+\d+ versions: concordance ([\d.]+)', line)
        if m and L:
            out[(m.group(1), L)] = float(m.group(2))
    return out


def story(w, us, ms, pl, rng):
    fr = S.features(us, ms) @ w
    fa = np.array([S.features(a, b) for a, b in S.alternatives(us, ms, pl, S.TEST_ALTS, rng)]) @ w
    win, tie = int((fa > fr).sum()), int((fa == fr).sum())
    lose = S.TEST_ALTS - win - tie
    secs = len({S.CG.SEC[u] for u in us if u in S.CG.SEC})
    return {'n': len(us), 'secs': secs, 'tie': tie / S.TEST_ALTS, 'conc': (win + 0.5 * tie) / S.TEST_ALTS,
            'untied': win / max(1, win + lose)}


def main():
    rec = recorded()
    rep = ['# ExploreConcordance.txt -- exploreConcordance.py: EXPLORATORY, outside the predictions; the frozen grammar, unchanged',
           '# per held-out version: functions, sections reached (of 10), share of alternatives tied, concordance (ties a half),',
           '# and concordance among the untied alternatives; per corpus the means, weighted as the record weights them', '']
    allrows = []
    for L in 'AB':
        w = frozen(L)
        data = S.load(L)
        rep.append('TRANSCRIBER %s (weights byte-identical to Weights-%s.txt)' % (L, L))
        rep.append('  %-8s %3s %9s %9s %7s %11s %9s' % ('corpus', 'n', 'functions', 'sections', 'tied', 'concordance', 'untied'))
        for g in S.CORPORA:
            rng = np.random.default_rng(S.SEED + 10)
            pl = S.pool(data[g]['fit'])
            rows = [(wt, s, story(S.weights_of(w, g), us, ms, pl, rng)) for s, wt, us, ms in data[g]['held']]
            tw = sum(wt for wt, _, _ in rows)

            def mean(k):
                return sum(wt * r[k] for wt, _, r in rows) / tw
            if abs(mean('conc') - rec[(g, L)]) > 0.0005:
                raise SystemExit('%s %s: concordance %.4f does not reproduce the record %.3f' % (g, L, mean('conc'), rec[(g, L)]))
            rep.append('  %-8s %3d %9.1f %9.1f %6.0f%% %11.3f %9.3f' % (g, len(rows), mean('n'), mean('secs'), 100 * mean('tie'),
                                                                     mean('conc'), mean('untied')))
            allrows += [(g, L, r) for _, _, r in rows]
            if g == 'tragedy':
                trag = rows
        rep.append('  the tragedies one by one:')
        for wt, s, r in trag:
            rep.append('    %-8s functions %3d, sections %2d, tied %3.0f%%, concordance %.3f, untied %.3f'
                       % (s, r['n'], r['secs'], 100 * r['tie'], r['conc'], r['untied']))
        rep.append('')
    x = np.array([[r['secs'], r['n'], r['tie'], r['conc'], r['untied']] for _, _, r in allrows])
    rep.append('ACROSS ALL HELD-OUT VERSIONS, BOTH TRANSCRIBERS (%d): rank correlations (Spearman)' % len(x))
    for i, name in ((0, 'sections reached'), (1, 'functions'), (2, 'share tied')):
        rep.append('  %-17s with concordance %+.2f; with untied concordance %+.2f'
                   % (name, S.spearmanr(x[:, i], x[:, 3]).correlation, S.spearmanr(x[:, i], x[:, 4]).correlation))
    text = '\n'.join(rep) + '\n'
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
