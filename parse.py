#!/usr/bin/env python3
"""
Predictive LL(1) acceptor for a Propp EBNF grammar.
Input: a list of Propp function tokens (e.g. ["A","B","C","↑","K"]).
Output: ACCEPT, or REJECT with the offending position and the set of
tokens that would have been valid there.

This is stage two of the corpus test: purely mechanical. It never
'interprets' a tale; it only decides whether a token string is in the
language the grammar defines.
"""
import re, sys

def load(text):
    def strip(line):
        o=[];i=0;q=False
        while i<len(line):
            c=line[i]
            if c=='"' or c=="'":
                q=False if q==c else (q or c)
                o.append(c);i+=1;continue
            if not q and c=='#':break
            o.append(c);i+=1
        return ''.join(o)
    # A head whose '=' opens the FOLLOWING line was formerly read as a bare
    # continuation of the previous production, silently truncating the grammar
    # and stranding the '='. A line that is a bare identifier and whose next
    # code line opens with '=' is therefore joined to it. The rule is narrow on
    # purpose: a bare identifier alone is a legitimate continuation and must
    # not be disturbed. Inert on any file that wraps no head. Same change as
    # regression.joincode, which this deliberately mirrors.
    lines=[]
    for ln in text.split('\n'):
        if ln.strip().startswith('#'):continue
        code=strip(ln)
        if not code.strip():continue
        lines.append(code)
    joined=[];i=0
    while i<len(lines):
        if (i+1<len(lines)
                and re.match(r'^\s*[A-Za-z][A-Za-z0-9]*\s*$',lines[i])
                and lines[i+1].lstrip().startswith('=')):
            joined.append(lines[i].rstrip()+' '+lines[i+1].lstrip());i+=2;continue
        joined.append(lines[i]);i+=1
    prods={};order=[];cur=None
    for code in joined:
        m=re.match(r'^\s*([A-Za-z][A-Za-z0-9]*)\s*=(.*)$',code)
        if m:
            cur=m.group(1)
            if cur not in prods:order.append(cur);prods[cur]=''
            prods[cur]+=' '+m.group(2)
        elif cur is not None:prods[cur]+=' '+code
    return prods,order

def tokenize(s):
    t=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c.isspace():i+=1;continue
        if c=='"' or c=="'":
            j=i+1
            while j<n and s[j]!=c:j+=1
            t.append(('T',s[i+1:j]));i=j+1;continue
        if c in '|[]{}()':t.append((c,c));i+=1;continue
        m=re.match(r'[A-Za-z][A-Za-z0-9]*',s[i:])
        if m:t.append(('ID',m.group(0)));i+=m.end();continue
        raise ValueError(f"bad char {c!r}")
    return t

class RP:
    def __init__(self,t):self.t=t;self.i=0
    def peek(self):return self.t[self.i] if self.i<len(self.t) else (None,None)
    def nx(self):x=self.t[self.i];self.i+=1;return x
    def alt(self):
        s=[self.seq()]
        while self.peek()[0]=='|':self.nx();s.append(self.seq())
        return ('alt',s)
    def seq(self):
        f=[]
        while self.peek()[0] in ('T','ID','[','{','('):f.append(self.factor())
        return ('seq',f)
    def factor(self):
        k,v=self.peek()
        if k=='T':self.nx();return ('term',v)
        if k=='ID':self.nx();return ('nt',v)
        if k=='[':self.nx();a=self.alt();assert self.nx()[0]==']';return ('opt',a)
        if k=='{':self.nx();a=self.alt();assert self.nx()[0]=='}';return ('star',a)
        if k=='(':self.nx();a=self.alt();assert self.nx()[0]==')';return ('group',a)
        raise ValueError

def desugar(prods,order):
    bnf={};ctr=[0]
    def fresh(h):ctr[0]+=1;return f"{h}#{ctr[0]}"
    def dseq(s,ctx):return [dfac(f,ctx) for f in s[1]]
    def dfac(f,ctx):
        t=f[0]
        if t=='term':return ('t',f[1])
        if t=='nt':return ('n',f[1])
        if t=='opt':nm=fresh(ctx+'_opt');bnf[nm]=[dseq(s,nm) for s in f[1][1]]+[[]];return ('n',nm)
        if t=='star':nm=fresh(ctx+'_star');bnf[nm]=[dseq(s,nm)+[('n',nm)] for s in f[1][1]]+[[]];return ('n',nm)
        if t=='group':nm=fresh(ctx+'_grp');bnf[nm]=[dseq(s,nm) for s in f[1][1]];return ('n',nm)
    for name in order:bnf[name]=[dseq(s,name) for s in RP(tokenize(prods[name])).alt()[1]]
    return bnf,order[0]

def build(text):
    prods,order=load(text)
    bnf,start=desugar(prods,order)
    # Same fault as regression.py carried: a dangling reference reaches the
    # FIRST computation below and raises KeyError. Say what is undefined.
    refs={s[1] for prod in bnf.values() for alt in prod for s in alt if s[0]=='n'}
    undef=sorted(r for r in refs if r not in bnf)
    if undef:raise ValueError("undefined nonterminals: %s"%undef)
    nullable=set();ch=True
    while ch:
        ch=False
        for A,ps in bnf.items():
            if A in nullable:continue
            for p in ps:
                if all(s[0]=='n' and s[1] in nullable for s in p):nullable.add(A);ch=True;break
    def sn(s):return s[0]=='n' and s[1] in nullable
    FIRST={A:set() for A in bnf}
    def fsym(s):return {s[1]} if s[0]=='t' else FIRST[s[1]]
    def fseq(seq):
        S=set()
        for s in seq:
            S|=fsym(s)
            if not sn(s):break
        return S
    ch=True
    while ch:
        ch=False
        for A,ps in bnf.items():
            b=len(FIRST[A])
            for p in ps:FIRST[A]|=fseq(p)
            if len(FIRST[A])!=b:ch=True
    def seqnull(seq):return all(sn(s) for s in seq)
    FOLLOW={A:set() for A in bnf};FOLLOW[start].add('$');ch=True
    while ch:
        ch=False
        for A,ps in bnf.items():
            for p in ps:
                for i,s in enumerate(p):
                    if s[0]!='n':continue
                    rest=p[i+1:];b=len(FOLLOW[s[1]])
                    FOLLOW[s[1]]|=fseq(rest)
                    if seqnull(rest):FOLLOW[s[1]]|=FOLLOW[A]
                    if len(FOLLOW[s[1]])!=b:ch=True
    # LL(1) table: table[A][t] -> production (rhs)
    table={A:{} for A in bnf}
    for A,ps in bnf.items():
        for p in ps:
            pred=set(fseq(p))
            if seqnull(p):pred|=FOLLOW[A]
            for t in pred:
                assert t not in table[A], f"LL(1) conflict at {A} on {t}"
                table[A][t]=p
    return bnf,start,table

def accept(tokens,bnf,start,table):
    inp=list(tokens)+['$']
    stack=[('t','$'),('n',start)]
    pos=0
    while stack:
        top=stack.pop()
        a=inp[pos]
        if top[0]=='t':
            if top[1]==a:
                if a=='$':return True,pos,None
                pos+=1
            else:
                return False,pos,{top[1]}
        else:
            A=top[1]
            if a in table[A]:
                rhs=table[A][a]
                for s in reversed(rhs):stack.append(s)
            else:
                return False,pos,set(table[A].keys())
    return (inp[pos]=='$'),pos,None

def run(label,toks,bnf,start,table,expect):
    ok,pos,exp=accept(toks,bnf,start,table)
    verdict="ACCEPT" if ok else "REJECT"
    tag="OK" if (ok==expect) else "!! UNEXPECTED"
    s=' '.join(toks) if toks else '(empty)'
    print(f"[{tag:14}] {verdict:6} {s}")
    if not ok:
        shown=inp_at(toks,pos)
        valid=sorted(x for x in exp if x!='$')
        endmark=' or end-of-tale' if '$' in exp else ''
        print(f"                 halted at position {pos} ({shown}); "
              f"valid there: {{{', '.join(valid)}}}{endmark}")
    return ok==expect

def inp_at(toks,pos):
    if pos>=len(toks):return "end of input"
    return f"token '{toks[pos]}'"

if __name__=="__main__":
    unknown = [a for a in sys.argv[1:] if a.startswith('-')]
    if unknown:
        sys.exit("parse.py: unknown option %s" % unknown[0])
    path=sys.argv[1] if len(sys.argv)>1 else 'ProppEBNF43.txt'
    try:
        bnf,start,table=build(open(path,encoding='utf-8').read())
    except ValueError as e:
        print(f"grammar: {path}\n\nGRAMMAR NOT READABLE: {e}")
        sys.exit(1)
    print(f"grammar: {path}  (start = {start})\n")

    print("== KNOWN-GOOD (must ACCEPT) ==")
    good=[
     ("canonical struggle magic tale",
      "α β γ δ A B C ↑ D E F G H J I K ↓ Pr Rs Q U W"),
     ("non-combat rescue tale",
      "α β γ δ A B C ↑ D E F G K ↓ Pr Rs"),
     ("minimal a...K (Propp/Dundes boundary)", "a K"),
     ("false-hero litigation (o L Q Ex)", "a K o L Q Ex"),
     ("difficult-task validation (M N Q)", "a K M N Q"),
     ("A/a co-occurrence in a VillainyMove", "A a K"),
    ]
    ok=True
    for lab,s in good:ok&=run(lab,s.split(),bnf,start,table,expect=True)

    print("\n== KNOWN-BAD (must REJECT) ==")
    bad=[
     ("liquidation before any crisis", "K a"),
     ("lack with no liquidation", "a"),
     ("struggle with no victory", "A H K"),
     ("stray second liquidation", "a K K"),
    ]
    for lab,s in bad:ok&=run(lab,s.split(),bnf,start,table,expect=False)

    print("\nACCEPTOR SELF-TEST:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)