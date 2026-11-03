#!/usr/bin/env python3
"""
strings.py -- the strings the induction reads (Induction/InductionProtocol.md section 1, frozen 2026-11-03), for split.py
and induce.py alike.

Function strings: the units StoryGrammar/storyGrammar.py load takes (and predict34.load_new for the two new corpora),
every story, fitting and held-out alike; each story's units cut into its moves. Act strings: the acts layer, one study per
story and describer (StoryModels/common.py), in event and entry order, `other` left out, the whole story one sequence.
Stories of fewer than three units are left out in both.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPLIT = os.path.join(HERE, 'Split.txt')
sys.path.insert(0, os.path.join(ROOT, 'StoryGrammar'))
sys.path.insert(0, os.path.join(ROOT, 'StoryModels'))
import storyGrammar as S  # noqa: E402  (its imports change the working directory; every path here is absolute)
import predict34 as P34  # noqa: E402
import common as CM  # noqa: E402

DT, TS, CG = S.DT, S.TS, S.CG
FUNC_CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'myth', 'native', 'eastasian']
ACT_CORPORA = ['tale', 'animal', 'fable', 'tragedy', 'native', 'eastasian']
LAYERS = {'functions': FUNC_CORPORA, 'acts': ACT_CORPORA}
READERS = 'AB'
_LOAD = {}


def _old(L):
    if L not in _LOAD:
        _LOAD[L] = S.load(L)
    return _LOAD[L]


def functions(g, L):
    """[(story, weight, [move: [unit]], [move: [event]])] for a corpus and transcriber, in the loader's order"""
    if g in S.CORPORA:
        d = _old(L)[g]
        items = d['fit'] + d['held']
    else:
        items = P34.load_new(g, L)
    out = []
    for s, w, us, ms in items:
        order = list(collections.OrderedDict.fromkeys(ms))
        out.append((s, w, [[u for u, m in zip(us, ms) if m == mv] for mv in order], None))
    return out


_ACTS = []


def acts(g, L):
    """[(story, 1.0, [[act]], [[event]])], the whole story one move"""
    if not _ACTS:
        _ACTS.append(CM.by_story('acts'))
    out = []
    for (s, r), rows in _ACTS[0].items():
        if r != L or CM.corpus(s) != g:
            continue
        rows = [x for x in CM.in_order(rows) if x['act'].lower() != 'other' and x['act']]
        if len(rows) >= 3:
            out.append((DT.local(s), 1.0, [[x['act'].lower() for x in rows]], [[int(x['event']) for x in rows]]))
    return out


def strings(layer, g, L):
    return functions(g, L) if layer == 'functions' else acts(g, L)


def stories(layer, g):
    """the sorted story ids of a corpus and layer, both transcribers joined"""
    return sorted({s for L in READERS for s, _, _, _ in strings(layer, g, L)})


def read_split():
    """{(layer, corpus): {'induction': set, 'checking': set}} from Split.txt"""
    out = collections.defaultdict(dict)
    for line in open(SPLIT, encoding='utf-8'):
        m = re.match(r'^(\w+) (\w+) (induction|checking) \d+: (.*)$', line.strip())
        if m:
            out[(m.group(1), m.group(2))][m.group(3)] = set(m.group(4).split())
    return out
