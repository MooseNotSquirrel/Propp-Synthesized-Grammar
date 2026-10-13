#!/usr/bin/env python3
"""
posthoc.py -- after the verdict: how much of the failure the keeper's fault in the
frozen mapping explains. The card tells the transcribers to assign a function
whoever performs it, while derive3 withholds trickery and villainy from the
hero. Here they are given whoever performs the act; nothing else changes.
Reported, not judged; the frozen verdict stands.

  python posthoc.py      writes Significance/PostHoc.txt
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import significance as S  # noqa: E402

T, W, BL = S.T, S.W, S.BL


def derive3_card(act, part, value, place, after):
    out = S.derive3(act, part, value, place, after)
    if place in ('opens', 'worsens') and value == 'harms' and act in ('harm', 'other', 'deceive'):
        out.add('A')
    if act == 'deceive' and place in ('serves', 'opens', 'worsens'):
        out.add('η')
    return out


def main():
    M = T.material()
    J = W.judged()
    gen = {s: g for g, bs in M.items() for b in bs.values() for s in b}
    funcs, D = {}, {}
    for L in 'AB':
        o = {}
        for g in T.GENRES:
            o.update({e: v for e, v in T.read_functions(glob.glob(os.path.join(S.P, BL.ORIG[g] % L))).items() if e[0] in gen})
        funcs[L] = o
        D[L] = S.described(L)
    events = sorted(e for e in set(funcs['A']) & set(funcs['B']) & set(D['A']) & set(D['B']) if e[0] in J)
    jab = T.jaccard(funcs['A'], funcs['B'], events)
    rep = ['# PostHoc.txt -- posthoc.py, after the verdict; reported, not judged.', '']
    for name, fn in (('frozen mapping', S.derive3), ('trickery and villainy whoever performs them', derive3_card)):
        r = [T.jaccard({e: set().union(*[fn(x['act'], x['part'], x['value'], x['place'], x['after']) for x in D[L][e]]) for e in events},
                       funcs[L], events) for L in 'AB']
        rep.append('%-46s A %.3f  B %.3f  mean %.3f   (original A against B %.3f)' % (name, r[0], r[1], sum(r) / 2, jab))
    open(os.path.join(HERE, 'PostHoc.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
