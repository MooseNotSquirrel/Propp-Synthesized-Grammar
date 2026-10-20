#!/usr/bin/env python3
"""
group.py -- the free verbs grouped by their contexts, and the frequency analysis rerun
on the groups (GroupProtocol.md).

  python group.py score      writes Group/Classes.txt and Group/GroupRun.txt
  python group.py selftest   the method on planted synonyms

Written in full before any verb was grouped.
"""
import collections
import os
import random
import re
import sys

import numpy as np
from sklearn.cluster import AgglomerativeClustering

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Free'))
import free as F  # noqa: E402

N = F.N
CLASSES, MIN_USES = 37, 5
STOP = set('a an the to of his her their him them with for on in at from and it its by into into up out as is be that this '
           'who what all one two own each other some any no not so too very'.split())
REQUESTS = ['ask', 'beg', 'pray', 'urge', 'plead', 'implore', 'entreat']


# ---------------------------------------------------------------- the entries
def entries():
    """{L: [(story, event, verb, phrase words)] in text order}"""
    out = {}
    for L in 'AB':
        rows = []
        for b in F.batches():
            for s, ev, v, ph, _, _, _ in F.read_free(L, b)[0]:
                words = [w for w in re.findall(r"[a-z]+", ph.lower())[1:] if w not in STOP and len(w) > 2]
                rows.append((s, ev, v, words))
        out[L] = rows
    return out


def contexts(E):
    """{verb: Counter of context features}, pooled over both describers: the words of its phrases, and the verbs
    just before and just after it in the same story"""
    ctx = collections.defaultdict(collections.Counter)
    uses = collections.Counter()
    for L, rows in E.items():
        for i, (s, ev, v, words) in enumerate(rows):
            uses[v] += 1
            ctx[v].update('w:' + w for w in words)
            if i > 0 and rows[i - 1][0] == s:
                ctx[v]['p:' + rows[i - 1][2]] += 1
            if i + 1 < len(rows) and rows[i + 1][0] == s:
                ctx[v]['n:' + rows[i + 1][2]] += 1
    return ctx, uses


def cluster(ctx, uses, k=CLASSES, min_uses=MIN_USES):
    """{verb: class name} for the verbs used at least min_uses times, pooled; a class is named by its commonest verb"""
    verbs = sorted(v for v, n in uses.items() if n >= min_uses)
    feats = sorted({f for v in verbs for f in ctx[v]})
    fi = {f: i for i, f in enumerate(feats)}
    X = np.zeros((len(verbs), len(feats)))
    for r, v in enumerate(verbs):
        for f, c in ctx[v].items():
            X[r, fi[f]] = c
    for part in ('w:', 'p:', 'n:'):
        cols = [fi[f] for f in feats if f.startswith(part)]
        sub = X[:, cols]
        norm = np.linalg.norm(sub, axis=1, keepdims=True)
        X[:, cols] = np.divide(sub, norm, out=np.zeros_like(sub), where=norm > 0)
    labels = AgglomerativeClustering(n_clusters=min(k, len(verbs)), metric='cosine', linkage='average').fit_predict(X + 1e-9)
    members = collections.defaultdict(list)
    for v, l in zip(verbs, labels):
        members[l].append(v)
    name = {l: max(m, key=lambda v: (uses[v], v)) + '+' for l, m in members.items()}
    return {v: name[l] for v, l in zip(verbs, labels)}


def strings(E, cls):
    st = {}
    for L, rows in E.items():
        s_out = collections.OrderedDict()
        for s, ev, v, _ in rows:
            s_out.setdefault(s, []).append(cls.get(v, v))
        st[L] = s_out
    return st


# ---------------------------------------------------------------- scoring
def score():
    E = entries()
    ctx, uses = contexts(E)
    cls = cluster(ctx, uses)
    members = collections.defaultdict(list)
    for v, c in cls.items():
        members[c].append(v)
    with open(os.path.join(HERE, 'Classes.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Classes.txt -- group.py: the free verbs used at least %d times, in %d classes by context; class | uses | members by uses\n' % (MIN_USES, CLASSES))
        for c in sorted(members, key=lambda c: -sum(uses[v] for v in members[c])):
            f.write('%s | %d | %s\n' % (c, sum(uses[v] for v in members[c]), ', '.join('%s %d' % (v, uses[v]) for v in sorted(members[c], key=lambda v: -uses[v]))))
    st = strings(E, cls)
    _, by_ev = F.free_strings()
    acts = F.act_events()
    al_v = F.alignment(by_ev, acts)
    al = {L: collections.defaultdict(collections.Counter) for L in 'AB'}
    for L in 'AB':
        for v, c in al_v[L].items():
            al[L][cls.get(v, v)].update(c)
    rep = ['# GroupRun.txt -- group.py score, as GroupProtocol.md freezes it.', '',
           '%d verbs used at least %d times grouped into %d classes (Classes.txt); %d verbs used fewer times keep their own names.'
           % (len(cls), MIN_USES, len(members), sum(1 for v in uses if v not in cls)), '']
    # prediction 1
    rep.append('THE REQUESTS')
    ok1 = True
    for L in 'AB':
        cnt = collections.Counter(v for rows in [E[L]] for _, _, v, _ in rows)
        req = [v for v in REQUESTS if cnt[v] >= 10]
        where = collections.Counter(cls.get(v, v) for v in req)
        top, n = where.most_common(1)[0] if where else ('-', 0)
        good = len(req) > 0 and 3 * n >= 2 * len(req)
        ok1 = ok1 and good
        rep.append('  %s: request verbs used at least 10 times: %s; their classes: %s; the most in one class %d of %d'
                   % (L, ', '.join('%s %d' % (v, cnt[v]) for v in req), ', '.join('%s %d' % kv for kv in where.most_common()), n, len(req)))
    # the pairs
    found = F.pairs(st)
    mapped = set()
    rep += ['', 'THE PAIRS: discovery and confirmation on the class strings, as Ngrams/ freezes them']
    for x, y, c, ok, shp in found:
        dx = [F.dominant(al[L], x) for L in 'AB']
        dy = [F.dominant(al[L], y) for L in 'AB']
        m = (dx[0], dy[0]) if dx[0] and dx[0] == dx[1] and dy[0] and dy[0] == dy[1] else None
        if ok and m:
            mapped.add(m)
        rep.append('  %-8s %s -> %s  %s  %s  acts: %s' % ('adjacent' if c == 1 else 'near', x, y, 'CONFIRMED' if ok else 'not confirmed', shp,
                                                         '%s -> %s' % m if m else 'no single act for both describers'))
    six = [p for p in F.SIX if p in mapped]
    rep += ['', 'PREDICTIONS (GroupProtocol.md)',
            '  1. the request verbs used at least 10 times fall, two thirds or more of them, in one class, for both describers: %s' % ('HOLDS' if ok1 else 'FAILS'),
            '  2. the exchange comes out as a confirmed pair of classes whose acts are plead -> respond: %s' % ('HOLDS' if ('plead', 'respond') in mapped else 'FAILS'),
            '  3. grouping does not bring out Propp\'s pairs: at most one of the six comes out as a confirmed pair of classes with the pair\'s acts: %d (%s) -> %s'
            % (len(six), ', '.join('%s->%s' % p for p in six) or '-', 'HOLDS' if len(six) <= 1 else 'FAILS'),
            '', 'REPORTED: confirmed pairs of classes whose acts are none of these: %s'
            % (', '.join('%s->%s' % m for m in sorted(mapped - set(F.SIX) - {('plead', 'respond')})) or '-')]
    open(os.path.join(HERE, 'GroupRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def selftest():
    """planted: twelve acts, each said with three synonyms, each act with its own object words and its own place in a
    fixed sequence; the grouping into twelve classes must put each act's synonyms together"""
    rnd = random.Random(5)
    acts = ['act%d' % i for i in range(12)]
    syn = {a: ['%s_%s' % (a, x) for x in 'xyz'] for a in acts}
    objs = {a: ['obj%d_%d' % (i, j) for j in range(4)] for i, a in enumerate(acts)}
    E = {}
    for L in 'AB':
        rows = []
        for s in range(150):
            start = rnd.randrange(12)
            for k in range(8):
                a = acts[(start + k) % 12]
                rows.append(('S%03d' % s, k, rnd.choice(syn[a]), [rnd.choice(objs[a]), rnd.choice(objs[a])]))
        E[L] = rows
    ctx, uses = contexts(E)
    cls = cluster(ctx, uses, k=12)
    pure = sum(len({cls[v] for v in syn[a]}) == 1 for a in acts)
    print('acts whose three synonyms share one class: %d of 12 (want 12); classes used: %d' % (pure, len(set(cls.values()))))


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
