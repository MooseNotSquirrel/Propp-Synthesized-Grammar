#!/usr/bin/env python3
"""
wordnetGroup.py -- the free verbs grouped by WordNet, and the frequency analysis rerun on
the groups (WordNetProtocol.md).

  python wordnetGroup.py score      writes Group/WordNetClasses.txt and Group/WordNetRun.txt
  python wordnetGroup.py selftest   the rule on WordNet's own synonyms

WordNet 3.0 (Princeton University; used under its license, which allows use for any purpose
with its copyright notice kept) is read through nltk from C:/Users/Steve1/nltk_wordnet,
outside the repositories. Written in full before any of the stories' verbs was looked up.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import group as G  # noqa: E402

F, N = G.F, G.N
WORDNET = r'C:/Users/Steve1/nltk_wordnet'
LEVEL = 2   # the class is the first sense's ancestor at this level from the top of its tree (1 is the top)


def wordnet():
    import nltk
    nltk.data.path.insert(0, WORDNET)
    from nltk.corpus import wordnet as wn
    return wn


def classify(verbs, wn):
    """{verb: class name}: the verb's first verb sense, cut at LEVEL on its first path from the top; a verb WordNet
    does not know as a verb keeps its own name (and is not in the result)"""
    out = {}
    for v in verbs:
        ss = wn.synsets(v, pos='v')
        if not ss:
            continue
        path = ss[0].hypernym_paths()[0]
        node = path[min(LEVEL, len(path)) - 1]
        out[v] = node.lemma_names()[0] + '~'
    return out


def score():
    wn = wordnet()
    E = G.entries()
    _, uses = G.contexts(E)
    cls = classify(sorted(v for v, n in uses.items() if n >= G.MIN_USES), wn)
    members = collections.defaultdict(list)
    for v, c in cls.items():
        members[c].append(v)
    with open(os.path.join(HERE, 'WordNetClasses.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# WordNetClasses.txt -- wordnetGroup.py: the free verbs used at least %d times, classed by WordNet 3.0 '
                '(first sense, level %d); class | uses | members by uses\n' % (G.MIN_USES, LEVEL))
        for c in sorted(members, key=lambda c: -sum(uses[v] for v in members[c])):
            f.write('%s | %d | %s\n' % (c, sum(uses[v] for v in members[c]), ', '.join('%s %d' % (v, uses[v]) for v in sorted(members[c], key=lambda v: -uses[v]))))
    st = G.strings(E, cls)
    _, by_ev = F.free_strings()
    acts = F.act_events()
    al_v = F.alignment(by_ev, acts)
    al = {L: collections.defaultdict(collections.Counter) for L in 'AB'}
    for L in 'AB':
        for v, c in al_v[L].items():
            al[L][cls.get(v, v)].update(c)
    tot = sum(uses.values())
    big = max(members, key=lambda c: sum(uses[v] for v in members[c]))
    rep = ['# WordNetRun.txt -- wordnetGroup.py score, as WordNetProtocol.md freezes it.', '',
           '%d of the %d verbs used at least %d times classed by WordNet into %d classes (WordNetClasses.txt); the largest, %s, holds %.0f%% of all uses.'
           % (len(cls), sum(1 for n in uses.values() if n >= G.MIN_USES), G.MIN_USES, len(members), big,
              100.0 * sum(uses[v] for v in members[big]) / tot), '']
    rep.append('THE REQUESTS')
    ok1 = True
    for L in 'AB':
        cnt = collections.Counter(v for _, _, v, _ in E[L])
        req = [v for v in G.REQUESTS if cnt[v] >= 10]
        where = collections.Counter(cls.get(v, v) for v in req)
        top, n = where.most_common(1)[0] if where else ('-', 0)
        good = len(req) > 0 and 3 * n >= 2 * len(req)
        ok1 = ok1 and good
        rep.append('  %s: request verbs used at least 10 times: %s; their classes: %s; the most in one class %d of %d'
                   % (L, ', '.join('%s %d' % (v, cnt[v]) for v in req), ', '.join('%s %d' % kv for kv in where.most_common()), n, len(req)))
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
    rep += ['', 'PREDICTIONS (WordNetProtocol.md)',
            '  0. no class holds more than a third of all uses (the grouping does not degenerate): %s' % (
                'HOLDS' if 3 * sum(uses[v] for v in members[big]) <= tot else 'FAILS'),
            '  1. the request verbs used at least 10 times fall, two thirds or more of them, in one class, for both describers: %s' % ('HOLDS' if ok1 else 'FAILS'),
            '  2. the exchange comes out as a confirmed pair of classes whose acts are plead -> respond: %s' % ('HOLDS' if ('plead', 'respond') in mapped else 'FAILS'),
            '  3. grouping does not bring out Propp\'s pairs: at most one of the six comes out as a confirmed pair of classes with the pair\'s acts: %d (%s) -> %s'
            % (len(six), ', '.join('%s->%s' % p for p in six) or '-', 'HOLDS' if len(six) <= 1 else 'FAILS'),
            '', 'REPORTED: confirmed pairs of classes whose acts are none of these: %s'
            % (', '.join('%s->%s' % m for m in sorted(mapped - set(F.SIX) - {('plead', 'respond')})) or '-')]
    open(os.path.join(HERE, 'WordNetRun.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


def selftest():
    """WordNet's own synonyms: the lemmas of one verb synset must share a class when each takes that synset as its first
    sense; and the rule must give more than one class over a varied list of common verbs"""
    wn = wordnet()
    checks = 0
    agree = 0
    for name in ('kill.v.01', 'give.v.03', 'fight.v.02', 'travel.v.01', 'deceive.v.01', 'say.v.01', 'request.v.01', 'think.v.01'):
        s = wn.synset(name)
        lemmas = [l for l in s.lemma_names() if '_' not in l and wn.synsets(l, pos='v')[0] == s]
        if len(lemmas) < 2:
            continue
        cl = classify(lemmas, wn)
        checks += 1
        agree += len(set(cl.values())) == 1
        print('%s: %s -> %s' % (name, ', '.join(lemmas), sorted(set(cl.values()))))
    varied = classify(['walk', 'eat', 'think', 'build', 'sing', 'sleep', 'buy', 'see'], wn)
    print('synsets whose first-sense lemmas share a class: %d of %d (want all); classes over eight varied verbs: %d (want more than 1)'
          % (agree, checks, len(set(varied.values()))))


if __name__ == '__main__':
    cmds = {'score': score, 'selftest': selftest}
    a = sys.argv[1:]
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
