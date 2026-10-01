#!/usr/bin/env python3
"""
trickAuditDraw.py -- draw the DeceptionTrap audit as Blocks/TrickAudit.txt
fixes it.

  python trickAuditDraw.py KEY_OUT

Writes Blocks/TrickAuditItems.json (the page's data, no transcriber or
sample) and the key, transcriber and sample per item, to KEY_OUT, which is
kept out of the repository until the audit is done; prints the key's
SHA-256.
"""
import glob
import hashlib
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import blockStream as BS  # noqa: E402
import blockAgreement as BA  # noqa: E402

PARENT = os.path.dirname(ROOT)


def notes(paths):
    """{(version, event): [(symbol, quoted words)]}"""
    out = {}
    for p in paths:
        for line in open(p, encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 10)]
            if len(f) < 11 or not re.match(r'^F\d{3}', f[0]):
                continue
            m = re.search(r'\d+', f[3])
            if m:
                out.setdefault((f[0], int(m.group())), []).append((f[4], f[10]))
    return out


def main(key_out):
    g = BS.Grammar()
    cells = []
    for sample, repo in (('training', 'Aesop'), ('held-out', 'Fables')):
        fab = {l.split(' | ', 1)[0]: l.rstrip('\n').split(' | ', 2)
               for l in open(os.path.join(PARENT, repo, 'Fables.txt'), encoding='utf-8') if l.strip()}
        evs = {}
        for l in open(os.path.join(PARENT, repo, 'Events.txt'), encoding='utf-8'):
            f = l.rstrip('\n').split(' | ', 2)
            if len(f) == 3:
                evs[(f[0], int(f[1]))] = f[2]
        for L in 'AB':
            paths = sorted(glob.glob(os.path.join(PARENT, repo, 'transcriptions', L, 'b[1-4]', 'Notes.txt')))
            vers, nts = BA.read(paths), notes(paths)
            found = []
            for v, (items, ev) in vers.items():
                for e, s in BA.blocks(items, ev, g, 'strict'):
                    if e == 'DeceptionTrap':
                        found.append((v, sorted(s)))
            cells.append(((sample, L), found, fab, evs, nts))
    rng = random.Random(3501)
    items, key = [], []
    for (sample, L), found, fab, evs, nts in cells:
        pick = rng.sample(found, min(5, len(found)))
        print('%-8s %s: %d instances, %d drawn' % (sample, L, len(found), len(pick)))
        for v, es in pick:
            fid = v.split('/', 1)[0]
            entries = []
            for e in es:
                for sym, q in nts.get((v, e), []):
                    b = BS.TS.base(sym)
                    if b in ('η', 'θ'):
                        entries.append({'event': e, 'function': 'trick' if b == 'η' else 'complicity',
                                        'quote': re.split(r'";|”;', q)[0].strip().strip('"“”') if q else ''})
            items.append({'fable': fid, 'title': fab[fid][1], 'text': fab[fid][2],
                          'events': ['%d. %s' % (e, evs.get((fid, e), '')) for e in es], 'entries': entries})
            key.append({'sample': sample, 'transcriber': L, 'version': v})
    order = list(range(len(items)))
    rng.shuffle(order)
    items = [dict(items[i], id='T%02d' % (k + 1)) for k, i in enumerate(order)]
    key = [dict(key[i], id='T%02d' % (k + 1)) for k, i in enumerate(order)]
    json.dump(items, open(os.path.join(ROOT, 'Blocks', 'TrickAuditItems.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    blob = json.dumps(key, sort_keys=True).encode('utf-8')
    open(key_out, 'wb').write(blob)
    print('items', len(items), 'key sha256', hashlib.sha256(blob).hexdigest())


if __name__ == '__main__':
    main(sys.argv[1])
