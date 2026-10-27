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
import re
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
    # the table as characters.py builds it now, read in memory, so that a dry run needs no table written
    for r in C.table()[1]:
        kinds[(r[2], r[0], r[3])].add(r[6])
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


def rewrite(dry):
    """after the join was mended (2026-10-26, at the owner's word): the tragedy and myth batches written again from the
    mended table, numbered on from n4; n1 to n3, already run, and their item key kept as they are; the controls that
    stood in the rewritten batches kept, where the mended table still sorts them, at new seeded positions"""
    old_key = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'NameItems.tsv'), encoding='utf-8')][1:]
    first = {'n1', 'n2', 'n3'}
    kept_key = [r for r in old_key if r[0].split('-')[0] in first]
    old_items = {(r[1], r[2], r[3]) for r in old_key if r[0].split('-')[0] not in first and not r[4]}
    old_ctl = [(r[1], r[2], r[3]) for r in old_key if r[0].split('-')[0] not in first and r[4]]
    ch = characters_by_item()
    ev, ti = event_text(), titles()

    def line(key):
        g, s, c = key
        d = ch[key]
        gid = g + ':' + s
        names = '; '.join(sorted(d['names'], key=lambda n: (-d['names'][n], n)))
        evs = ' / '.join('%d: %s' % (e, ev.get((gid, e), '')) for e in sorted(d['events'])[:3])
        return '%s | %s | %s | %s' % (s, ti.get(gid, ''), names, evs)
    unknown = [k for k, d in ch.items() if 'unknown' in d['kind'] and k[0] in ('tragedy', 'myth')]
    controls = [k for k in old_ctl if k in ch and 'unknown' not in ch[k]['kind'] and len(ch[k]['kind']) == 1]
    out = []
    for gs in GROUPS[2:]:
        ks = [k for k in unknown if k[0] in gs]
        n = -(-len(ks) // SIZE)
        for i in range(n):
            keys = ks[len(ks) * i // n: len(ks) * (i + 1) // n]
            out.append(['n%d' % (len(out) + 4), [(None, k[0], k[1], k[2], line(k), '') for k in keys]])
    rnd = random.Random(SEED + 1)
    for i, k in enumerate(controls):
        b = out[i % len(out)][1]
        b.insert(rnd.randrange(len(b) + 1), (None, k[0], k[1], k[2], line(k), next(iter(ch[k]['kind']))))
    for b, its in out:
        for j, x in enumerate(its, 1):
            its[j - 1] = ('%s-%03d' % (b, j),) + x[1:]
    new_items = {(x[1], x[2], x[3]) for _, its in out for x in its if not x[5]}
    by = collections.Counter(k[0] for k in new_items)
    print('tragedy and myth items: before %d, after %d (tragedy %d, myth %d); kept %d, gone %d, new %d; controls kept %d of %d'
          % (len(old_items), len(new_items), by['tragedy'], by['myth'], len(old_items & new_items), len(old_items - new_items),
             len(new_items - old_items), len(controls), len(old_ctl)))
    for b, its in out:
        print('%s items %3d (controls %d), corpora %s' % (b, len(its), sum(1 for x in its if x[5]), ', '.join(sorted({x[1] for x in its}))))
    writes, stale = [], []
    key = ['item\tcorpus\tstory\tcharacter\tcontrol'] + ['\t'.join(r) for r in kept_key]
    ctl = ['# NameControls.txt -- names.py: the control items, with the kind the WordNet rule gives them; never shown to the readers']
    ctl += ['%s\t%s' % (l.split('\t')[0], l.split('\t')[1]) for l in open(os.path.join(HERE, 'NameControls.txt'), encoding='utf-8')
            if l.split('-')[0] in first]
    for b, its in out:
        writes.append((os.path.join(AR, 'names', 'input', b + '.txt'), ''.join('%s | %s\n' % (i, l) for i, _, _, _, l, _ in its)))
        for L in 'AB':
            writes.append((os.path.join(AR, 'prompts', 'names-%s-%s.txt' % (L, b)), PROMPT.format(b=b, n=len(its), L=L)))
        for i, g, s, c, _, k in its:
            key.append('\t'.join((i, g, s, c, 'Y' if k else '')))
            if k:
                ctl.append('%s\t%s' % (i, k))
    writes.append((os.path.join(HERE, 'NameItems.tsv'), '\n'.join(key) + '\n'))
    writes.append((os.path.join(HERE, 'NameControls.txt'), '\n'.join(ctl) + '\n'))
    last = 'n%d' % (len(out) + 3)
    for n in range(len(out) + 4, 14):
        for path in [os.path.join(AR, 'names', 'input', 'n%d.txt' % n)] + [os.path.join(AR, 'prompts', 'names-%s-n%d.txt' % (L, n)) for L in 'AB']:
            if os.path.exists(path):
                stale.append(path)
    for path, text in writes:
        print('%s %-40s %6d bytes%s' % ('would write' if dry else 'write', os.path.relpath(path, P), len(text.encode('utf-8')),
                                       '  (replaces)' if os.path.exists(path) else ''))
    for path in stale:
        print('%s %s (no longer a batch; the batches now end at %s)' % ('would remove' if dry else 'remove', os.path.relpath(path, P), last))
    if dry:
        print('dry run: %d files to write, %d to remove; nothing written' % (len(writes), len(stale)))
        return out
    for path, text in writes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    for path in stale:
        os.remove(path)
    print('written: %d files, removed %d' % (len(writes), len(stale)))
    return out


KINDS = ('person', 'animal', 'deity', 'supernatural', 'object')
CONFIDENCES = ('high', 'medium', 'low')
# a name the transcribers wrote as a phrase, not a being ("at Zeus's order", "whoever should woo"): counted apart
PHRASE = re.compile(r'^(?:the\s+)?(?:at|for|of|by|in|to|from|with|whoever|whom|as)\b', re.I)


def item_key():
    return [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'NameItems.tsv'), encoding='utf-8')][1:]


def input_items(b):
    return [l.split(' | ')[0].strip() for l in open(os.path.join(AR, 'names', 'input', b + '.txt'), encoding='utf-8') if l.strip()]


def answers(L, b):
    """{item: (kind, confidence, reason)} and the items in the order written"""
    path = os.path.join(AR, 'names', 'answers', L, b, 'Kinds.txt')
    out, order = {}, []
    for l in open(path, encoding='utf-8'):
        f = [x.strip() for x in l.rstrip('\n').split('|', 3)]
        if len(f) == 4 and re.match(r'^n\d+-\d{3}$', f[0]):
            out[f[0]] = (f[1].lower(), f[2].lower(), f[3])
            order.append(f[0])
    return out, order


def batches():
    return sorted({r[0].split('-')[0] for r in item_key()}, key=lambda b: int(b[1:]))


def form():
    """NamesProtocol.md's form check: one line per item, in order; a kind from the five, a confidence from the three,
    a reason; written to Data/forms/names.txt"""
    out, total = [], 0
    for L in 'AB':
        for b in batches():
            items = input_items(b)
            got, order = answers(L, b)
            bad = sum(1 for i in items if i in got and (got[i][0] not in KINDS or got[i][1] not in CONFIDENCES or not got[i][2]))
            missing = sum(1 for i in items if i not in got)
            extra = len(set(got) - set(items))
            in_order = order == items
            out.append('%s %-3s items %3d, answered %3d, missing %d, unknown items %d, out-of-list answers %d, in order %s'
                       % (L, b, len(items), len(got), missing, extra, bad, 'yes' if in_order else 'NO'))
            total += missing + extra + bad + (0 if in_order else 1)
    out.append('IN FORM' if total == 0 else 'NOT IN FORM: %d problem(s)' % total)
    open(os.path.join(ROOT, 'Data', 'forms', 'names.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out))


def agreed():
    """{(corpus, story, character): kind} where both readers give the same kind, controls and phrase-names left out;
    and the lines of the report"""
    key = item_key()
    ans = {L: {} for L in 'AB'}
    for L in 'AB':
        for b in batches():
            ans[L].update(answers(L, b)[0])
    names = {}
    for b in batches():
        for l in open(os.path.join(AR, 'names', 'input', b + '.txt'), encoding='utf-8'):
            f = [x.strip() for x in l.split(' | ')]
            if len(f) >= 4:
                names[f[0]] = f[3]
    ctl = {l.split('\t')[0]: l.split('\t')[1].strip() for l in open(os.path.join(HERE, 'NameControls.txt'), encoding='utf-8')
           if not l.startswith('#') and '\t' in l}
    out, lines = {}, []
    by = collections.defaultdict(collections.Counter)
    phrases = []
    for item, g, s, c, control in key:
        a, b = ans['A'].get(item), ans['B'].get(item)
        if control:
            for L, x in (('A', a), ('B', b)):
                by['controls ' + L]['n'] += 1
                by['controls ' + L]['agree'] += bool(x) and x[0] == ctl.get(item)
            continue
        if PHRASE.match(names.get(item, '').split(';')[0]):
            phrases.append(names.get(item, ''))
            continue
        x = by[g]
        x['items'] += 1
        if a and b and a[0] == b[0]:
            x['agree'] += 1
            x['both high'] += a[1] == 'high' and b[1] == 'high'
            out[(g, s, c)] = a[0]
            x['kind ' + a[0]] += 1
    lines.append('# NameRun.txt -- names.py score: the name stage (Data/NamesProtocol.md), reported and not judged')
    for g in ('tale', 'animal', 'fable', 'tragedy', 'myth'):
        x = by[g]
        if x['items']:
            lines.append('%-8s items %3d, both readers the same kind %3d (%.0f%%), both with high confidence %3d; agreed kinds: %s'
                         % (g, x['items'], x['agree'], 100.0 * x['agree'] / x['items'], x['both high'],
                            ', '.join('%s %d' % (k, x['kind ' + k]) for k in KINDS if x['kind ' + k])))
    for L in 'AB':
        x = by['controls ' + L]
        lines.append('controls, reader %s: %d of %d the kind the WordNet rule gives (%.0f%%)' % (L, x['agree'], x['n'], 100.0 * x['agree'] / max(1, x['n'])))
    lines.append('phrase-names counted apart, given no kind: %d (%s)' % (len(phrases), '; '.join(sorted(phrases))))
    return out, lines


def score():
    _, lines = agreed()
    open(os.path.join(HERE, 'NameRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a in (['form'], ['score']):
        {'form': form, 'score': score}[a[0]]()
        sys.exit(0)
    if a == ['setup', '--dry']:
        setup(True)
    elif a == ['setup']:
        setup(False)
    elif a == ['rewrite', '--dry']:
        rewrite(True)
    elif a == ['rewrite']:
        rewrite(False)
    else:
        sys.exit(__doc__)
