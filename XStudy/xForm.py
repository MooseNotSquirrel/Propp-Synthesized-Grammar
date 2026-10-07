#!/usr/bin/env python3
"""xForm.py GENRE -- form check of a stage 5 transcription: every event has an entry, every symbol is
Propp's or a candidate act, every entry is marked Y or N. Parses nothing, judges nothing."""
import sys,re,glob,collections,os
sys.path.insert(0,r'C:/Users/Steve1/Desktop/Story Language/SynthesizedProppGrammar/Tragedy')
import tragedyScore as TS
X=r'C:/Users/Steve1/Desktop/Story Language/XStudy'
CANDS=[l.split('|')[1].strip() for l in open(r'C:/Users/Steve1/Desktop/Story Language/SynthesizedProppGrammar/XStudy/Candidates.md',encoding='utf-8') if l.startswith('| x')]
g=sys.argv[1]
def events():
    ev=collections.defaultdict(set)
    paths=[os.path.join(X,'test',g,'Events.txt')] if g!='tragedy' else glob.glob(os.path.join(X,'test','tragedy','plays','P*','Events.txt'))
    for p in paths:
        for l in open(p,encoding='utf-8'):
            f=[x.strip() for x in l.split('|')]
            if len(f)>=3 and f[1].isdigit(): ev[f[0]].add(int(f[1]))
    return ev
EV=events()
for L in 'AB':
    for d in sorted(glob.glob(os.path.join(X,'test',g,'transcriptions',L,'t*'))):
        got=collections.defaultdict(set); bad=collections.Counter(); nomark=0; n=0; cand=0
        for l in open(os.path.join(d,'Notes.txt'),encoding='utf-8'):
            f=[x.strip() for x in l.split('|',10)]
            if len(f)<10 or not re.match(r'^[PFA]\d{2}',f[0]): continue
            n+=1; e=re.search(r'\d+',f[3])
            if e: got[f[0].split('/')[0]].add(int(e.group()))
            s=f[4]
            if s in CANDS: cand+=1
            elif TS.base(s) not in TS.BASES: bad[s]+=1
            if f[7][:1].upper() not in 'YN': nomark+=1
        stories=sorted(got)
        missing=sum(len(EV[s]-got[s]) for s in stories)
        print(g,L,os.path.basename(d),'stories',len(stories),'entries',n,'candidate entries',cand,'events without entry',missing,'odd symbols',dict(bad),'unmarked',nomark)
