#!/usr/bin/env python3
"""
auditDraw.py -- draw the audit sample as ApollodorusPrediction.txt part 3
fixes it, and write the items the audit page shows and the key it hides.

  python auditDraw.py WORK

Writes AuditItems.json (what the auditor sees: no transcriber, no move,
no parse result) and AuditKey.txt (which transcriber, episode, move and
event each item came from). The key is not shown on the page.
"""
import json
import os
import random
import re
import sys

import scoreApollodorus as S

NAMES = {'α': 'initial situation', 'β': 'absentation', 'γ': 'interdiction', 'δ': 'violation',
         'ε': 'reconnaissance', 'ζ': 'delivery', 'η': 'trickery', 'θ': 'complicity',
         'λ': 'preliminary misfortune', 'A': 'villainy', 'a': 'lack', 'B': 'mediation, the connective incident',
         'C': 'beginning counteraction', '↑': 'departure', 'D': 'the first function of the donor',
         'E': "the hero's reaction", 'F': 'receipt of a magical agent', 'f': 'receipt of a magical agent',
         'G': 'guidance to the place sought', 'H': 'struggle', 'I': 'victory', 'J': 'branding, marking',
         'K': 'liquidation of the misfortune or lack', 'KF': 'liquidation of the misfortune or lack',
         '↓': 'return', 'Pr': 'pursuit', 'Rs': 'rescue', 'o': 'unrecognized arrival', 'L': 'unfounded claims',
         'M': 'difficult task', 'N': 'solution', 'Q': 'recognition', 'Ex': 'exposure',
         'T': 'transfiguration', 'U': 'punishment', 'W': 'wedding', 'w': 'wedding', 'C↑': 'beginning counteraction and departure'}


def sections():
    out = {}
    for src in ('Library.txt', 'Epitome.txt'):
        for line in open(os.path.join(S.HERE, src), encoding='utf-8'):
            c, t = line.rstrip('\n').split(' | ', 1)
            out[c] = t
    return out


def lines(work, lineage):
    scored = {v for ep, n, h in S.scored_episodes() for v, _, _ in S.versions(ep, h)}
    ents, _ = S.load_notes(work, lineage)
    rows = []
    import glob
    for d in sorted(glob.glob(os.path.join(work, 'transcriber' + lineage, 'b[0-9][0-9]'))):
        for line in open(os.path.join(d, 'Notes.txt'), encoding='utf-8'):
            f = [x.strip() for x in line.rstrip('\n').split('|', 9)]
            if len(f) < 10 or f[0] not in scored or S.base(f[5]) == 'X':
                continue
            rows.append(f)
    rows.sort(key=lambda f: (f[0], S.roman(f[1]), int(re.search(r'\d+', f[2]).group() or 0)))
    return rows


def main(work):
    rng = random.Random(4646)
    drawn = []
    for L in 'AB':
        for f in rng.sample(lines(work, L), 50):
            drawn.append((L, f))
    random.Random(4647).shuffle(drawn)
    sec = sections()
    items, key = [], []
    for i, (L, f) in enumerate(drawn, 1):
        cite = f[4]
        first = re.split(r'[-–,; ]', cite)[0]
        m = re.search(r'"([^"]+)"|“([^”]+)”', f[9])
        quote = (m.group(1) or m.group(2)) if m else ''
        b = S.base(f[5])
        items.append({'id': 'Q%03d' % i, 'cite': cite, 'text': sec.get(first, ''), 'quote': quote,
                      'symbol': f[5], 'name': NAMES.get(b, b), 'negative': S.negative(f[5]),
                      'performer': f[6], 'undergoer': f[7]})
        key.append('Q%03d | %s | %s | move %s | pos %s | %s' % (i, L, f[0], f[1], f[2], f[3]))
    json.dump(items, open(os.path.join(S.HERE, 'AuditItems.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(S.HERE, 'AuditKey.txt'), 'w', encoding='utf-8').write('\n'.join(key) + '\n')
    print(len(items), 'items;', sum(1 for it in items if not it['text']), 'without section text;',
          sum(1 for it in items if not it['quote']), 'without a quote')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
