#!/usr/bin/env python3
"""
names.py -- the name stage (Data/NamesProtocol.md, frozen 2026-10-26): the characters whose kind the WordNet rule
leaves unknown, given to two readers to sort.

  python names.py setup --dry   say what the setup would write, and write nothing
  python names.py setup         write the batches and prompts into Story Language/ActsRoles (names/input/n1.txt ...
                                n8.txt; prompts names-A-n1 ... names-B-n8), and on the keeper's side the item key
                                (Characters/NameItems.tsv) and the controls (Characters/NameControls.txt)

Each item is one story and one character, the two transcribers' rows merged where they give the same character, with
its names and up to three events that name it. The readers see no sphere, role or function code. Fifty controls,
characters the rule does sort, are mixed in unmarked by a fixed seed.
"""
import collections
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.dirname(ROOT)
AR = os.path.join(P, 'ActsRoles')
sys.path.insert(0, HERE)
import characters as C  # noqa: E402

DT, SX = C.DT, C.SX
# the corpora's items in this order, the fables and animal tales together, each group cut into as few batches of at
# most SIZE items as hold it, numbered on across the groups (NamesProtocol.md, amended at the owner's word 2026-10-26)
GROUPS = [['tale'], ['fable', 'animal'], ['tragedy'], ['myth']]
SIZE = 75
SEED = 20261026
CONTROLS = 50
PROMPT = """You are reading short notes on characters in stories and saying, for each, what kind of being it is. You start with no background on the project, and you should not look for any.

Read names/input/{b}.txt in this repository in full. It holds {n} items, one per line, each as

ITEM | STORY | TITLE | NAMES | EVENTS

where NAMES are the ways the character is named, and EVENTS are up to three of the story's events in which it appears, each with its number.

For each item, decide what kind of being the character is, from these five only:
- person: a human being, or a group of human beings;
- animal: a beast, bird, fish or insect, speaking or not;
- deity: a god or goddess, or a being the story treats as divine;
- supernatural: a being of the other world that is not a god, such as a witch, a monster, a spirit or a demon;
- object: anything else, such as a thing, a place, a plant, a people's land, or a force of nature.

Judge from the item: the names, the title and the events. Where they leave it open, judge from what the story's own words suggest, not from what you may know of the name elsewhere. Open only names/input/{b}.txt. Do not open, list or search any other file or folder in this repository, in particular nothing under names/answers/ but your own folder. Do not search the web. You are reader {L}.

Write one file, and nothing else, names/answers/{L}/{b}/Kinds.txt (create the folders): one line per item, in the order of the file, in the form

ITEM | KIND | CONFIDENCE | REASON

where KIND is one of the five words above, CONFIDENCE is high, medium or low, and REASON is one short sentence. For example: "{b}-000 | animal | high | the events call it a she-wolf that runs off with the child". Keep any working file inside names/answers/{L}/{b}/ and delete it before you finish.

Then reply with a short report: the number of items, how many you judged with low confidence, and how many you found hard to place, with their item numbers.
"""


def characters_by_item():
    """{(corpus, story, character key): {'names', 'events', 'kind'}} across both transcribers, from the function layer"""
    out = collections.OrderedDict()
    for g in C.PATS:
        for L in 'AB':
            for s, ents in C.entries(L, g).items():
                canon = SX.merge([e[:3] for e in ents])
                for fn, p, u, pr, ur, ev in ents:
                    for k, raw in ((p, pr), (u, ur)):
                        if not k:
                            continue
                        c = ' '.join(canon.get(k, k))
                        d = out.setdefault((g, s, c), {'names': collections.Counter(), 'events': set()})
                        d['names'][raw] += 1
                        if ev.isdigit():
                            d['events'].add(int(ev))
    kinds = collections.defaultdict(set)
    for r in DT.rows('characters'):
        kinds[(r['corpus'], r['story'], r['character'])].add(r['kind'])
    for key, d in out.items():
        d['kind'] = kinds.get(key, {'unknown'})
    return out


def event_text():
    t = {}
    for r in DT.rows('events'):
        t[(r['story'], int(r['event']))] = r['text'].replace('|', '/').strip()
    return t


def titles():
    return {r['story']: r['title'].replace('|', '/').strip() for r in DT.rows('stories')}


def items():
    """the batches: [(batch, [(item id, corpus, story, character, line, control kind or '')])]"""
    ch = characters_by_item()
    ev, ti = event_text(), titles()
    unknown = [k for k, d in ch.items() if 'unknown' in d['kind']]
    known = sorted(k for k, d in ch.items() if 'unknown' not in d['kind'] and len(d['kind']) == 1)
    rnd = random.Random(SEED)
    controls = rnd.sample(known, CONTROLS)

    def line(key):
        g, s, c = key
        d = ch[key]
        gid = g + ':' + s
        names = '; '.join(sorted(d['names'], key=lambda n: (-d['names'][n], n)))
        evs = ' / '.join('%d: %s' % (e, ev.get((gid, e), '')) for e in sorted(d['events'])[:3])
        return '%s | %s | %s | %s' % (s, ti.get(gid, ''), names, evs)
    by_corpus = collections.defaultdict(list)
    for k in unknown:
        by_corpus[k[0]].append(k)
    out = []
    for gs in GROUPS:
        ks = [k for g in gs for k in by_corpus[g]]
        n = -(-len(ks) // SIZE)
        for i in range(n):
            keys = ks[len(ks) * i // n: len(ks) * (i + 1) // n]
            out.append(['n%d' % (len(out) + 1), [(None, k[0], k[1], k[2], line(k), '') for k in keys]])
    for i, k in enumerate(controls):
        b = out[i % len(out)][1]
        b.insert(rnd.randrange(len(b) + 1), (None, k[0], k[1], k[2], line(k), next(iter(ch[k]['kind']))))
    for b, its in out:
        for j, x in enumerate(its, 1):
            its[j - 1] = ('%s-%03d' % (b, j),) + x[1:]
    return out


def setup(dry):
    batches = items()
    writes = []
    key, ctl = ['item\tcorpus\tstory\tcharacter\tcontrol'], ['# NameControls.txt -- names.py: the control items, '
                                                             'with the kind the WordNet rule gives them; never shown to the readers']
    for b, its in batches:
        writes.append((os.path.join(AR, 'names', 'input', b + '.txt'), ''.join('%s | %s\n' % (i, l) for i, _, _, _, l, _ in its)))
        for L in 'AB':
            writes.append((os.path.join(AR, 'prompts', 'names-%s-%s.txt' % (L, b)), PROMPT.format(b=b, n=len(its), L=L)))
        for i, g, s, c, _, k in its:
            key.append('\t'.join((i, g, s, c, 'Y' if k else '')))
            if k:
                ctl.append('%s\t%s' % (i, k))
    writes.append((os.path.join(HERE, 'NameItems.tsv'), '\n'.join(key) + '\n'))
    writes.append((os.path.join(HERE, 'NameControls.txt'), '\n'.join(ctl) + '\n'))
    for b, its in batches:
        print('%s items %3d (controls %d), corpora %s' % (b, len(its), sum(1 for x in its if x[5]), ', '.join(sorted({x[1] for x in its}))))
    for path, text in writes:
        exists = os.path.exists(path)
        print('%s %-40s %6d bytes%s' % ('would write' if dry else 'write', os.path.relpath(path, P), len(text.encode('utf-8')),
                                       '  (EXISTS: refused)' if exists else ''))
        if exists:
            raise SystemExit('refusing to overwrite %s' % path)
    if dry:
        print('dry run: %d files; nothing written' % len(writes))
        return
    for path, text in writes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print('written: %d files' % len(writes))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['setup', '--dry']:
        setup(True)
    elif a == ['setup']:
        setup(False)
    else:
        sys.exit(__doc__)
