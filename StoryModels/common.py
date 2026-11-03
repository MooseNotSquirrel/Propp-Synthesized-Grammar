#!/usr/bin/env python3
"""
common.py -- what arcs.py and networks.py both read (ArcsNetworksProtocol.md, frozen 2026-11-03): the six corpora, each
story's one significance or act study per describer, the lister's hero and the heroes-stage readers' heroes, and the
names as Spheres/explore.py splits and keys them. Everything is read through Data/tables.py.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Data'))
sys.path.insert(0, os.path.join(ROOT, 'Spheres'))
import tables as DT  # noqa: E402
import explore as SX  # noqa: E402

# protocol section 1: the corpora with acts and significance for every story they describe; the myths and Aesop have none
ORDER = ['tale', 'animal', 'fable', 'tragedy', 'native', 'eastasian']
NAMES = {'tale': 'wondertales', 'animal': 'animal tales', 'fable': 'Fables', 'tragedy': 'tragedies',
         'native': 'Native American', 'eastasian': 'East Asian'}
LEFT_OUT = 'the myths (Apollodorus) and Aesop: no acts or significance in the tables (Data/Coverage.txt)'
READERS = 'AB'
NO_SINGLE = re.compile(r'^\s*no single hero\s*:?\s*', re.I)


def corpus(story):
    return story.split(':', 1)[0]


def by_story(table):
    """{(story, reader): rows} for the six corpora and describers A and B, one study each: a story's describer has one
    study in the tables (checked here), its rows in the order the builder read them"""
    out = collections.OrderedDict()
    for r in DT.rows(table):
        if r['reader'] in READERS and r['reader'] and corpus(r['story']) in ORDER and not r.get('id_flag'):
            out.setdefault((r['story'], r['reader']), collections.OrderedDict()).setdefault(r['study'], []).append(r)
    two = [k for k, v in out.items() if len(v) != 1]
    if two:
        raise SystemExit('%s: stories with more than one study: %s' % (table, two[:5]))
    return collections.OrderedDict((k, list(v.values())[0]) for k, v in out.items())


def in_order(rows):
    """the rows in the story's order: by event, then by entry, the builder's order breaking ties"""
    return [r for _, r in sorted(enumerate(rows), key=lambda ir: (int(ir[1]['event']), ir[1]['entry'], ir[0]))]


def hero_names(raw):
    """a hero field as the names it holds: "no single hero: X; Y" and "X, the youngest brother" give each name"""
    return SX.split_field(NO_SINGLE.sub('', raw or ''))


def same(a, b):
    """do two names name one character? Their keys are equal, or one may join the other (explore.joins)"""
    ka, kb = SX.key(a), SX.key(b)
    return bool(ka) and bool(kb) and (ka == kb or SX.joins(ka, kb) or SX.joins(kb, ka))


def heroes():
    """{story: lister's hero names}, and {(story, reader): heroes-stage reader's hero names}"""
    lister, readers = {}, {}
    for r in DT.rows('heroes'):
        if r['reader'] == 'lister':
            lister[r['story']] = hero_names(r['hero'])
        elif r['reader'] in READERS and r['reader'] and r['study'] == 'heroes':
            readers[(r['story'], r['reader'])] = hero_names(r['hero'])
    return lister, readers


def agreed(lister, readers):
    """the stories whose heroes-stage readers both name the lister's hero (protocol section 1, decision 3): each reader
    names at least one name that is the same as one of the lister's"""
    return {s for s, ls in lister.items()
            if all(any(same(a, b) for a in readers.get((s, L), []) for b in ls) for L in READERS)}
