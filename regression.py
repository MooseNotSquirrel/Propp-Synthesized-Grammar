#!/usr/bin/env python3
"""
Propp EBNF regression harness.
Folds together: structural audit (undefined / duplicate / unused),
full FIRST/FOLLOW LL(1) check (every production and every [ ]/{ } boundary),
and style invariants (no em dashes, no dissolved rule names), run across
all four toggle states (task-liquidation x tragedy). Exit code 0 == all pass.

Usage: python regression.py [path-to-grammar.txt]
"""
import re, sys

# ---------- load code-only productions ----------
# strip() is module level rather than nested inside load() so that the style
# invariant in main() can measure code text through the reader the loader
# itself uses, instead of through a second copy of the same logic that could
# drift away from it. Nothing else about it changed.
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

def joincode(text):
    """Code lines, with a wrapped production head joined to its '=' line.

    A head whose '=' opens the FOLLOWING line was formerly read as a bare
    continuation of the previous production, silently truncating the grammar
    and stranding the '='. A line that is a bare identifier and whose next code
    line opens with '=' is therefore joined to it. The rule is narrow on
    purpose: a bare identifier alone is a legitimate continuation and must not
    be disturbed. Inert on any file that wraps no head.
    """
    lines=[]
    for ln in text.split('\n'):
        if ln.strip().startswith('#'):continue
        code=strip(ln)
        if not code.strip():continue
        lines.append(code)
    out=[];i=0
    while i<len(lines):
        if (i+1<len(lines)
                and re.match(r'^\s*[A-Za-z][A-Za-z0-9]*\s*$',lines[i])
                and lines[i+1].lstrip().startswith('=')):
            out.append(lines[i].rstrip()+' '+lines[i+1].lstrip());i+=2;continue
        out.append(lines[i]);i+=1
    return out

def load(text):
    prods={};order=[];dups=[];cur=None
    for code in joincode(text):
        m=re.match(r'^\s*([A-Za-z][A-Za-z0-9]*)\s*=(.*)$',code)
        if m:
            cur=m.group(1)
            if cur in prods:dups.append(cur)
            else:order.append(cur);prods[cur]=''
            prods[cur]+=' '+m.group(2)
        elif cur is not None:
            prods[cur]+=' '+code
    return prods,order,dups

# ---------- tokenize + parse an EBNF RHS ----------
def tokenize(s):
    toks=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c.isspace():i+=1;continue
        if c=='"' or c=="'":
            j=i+1
            while j<n and s[j]!=c:j+=1
            toks.append(('T',s[i+1:j]));i=j+1;continue
        if c in '|[]{}()':toks.append((c,c));i+=1;continue
        m=re.match(r'[A-Za-z][A-Za-z0-9]*',s[i:])
        if m:toks.append(('ID',m.group(0)));i+=m.end();continue
        raise ValueError(f"bad char {c!r} near ...{s[max(0,i-15):i+15]!r}")
    return toks

class RP:
    def __init__(self,t):self.t=t;self.i=0
    def peek(self):return self.t[self.i] if self.i<len(self.t) else (None,None)
    def nx(self):tok=self.t[self.i];self.i+=1;return tok
    def alt(self):
        seqs=[self.seq()]
        while self.peek()[0]=='|':self.nx();seqs.append(self.seq())
        return ('alt',seqs)
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
        raise ValueError("parse error")

# ---------- desugar EBNF -> BNF ----------
def desugar(prods,order):
    bnf={};ctr=[0]
    def fresh(h):ctr[0]+=1;return f"{h}#{ctr[0]}"
    def d_seq(seqnode,ctx):return [d_factor(f,ctx) for f in seqnode[1]]
    def d_factor(fac,ctx):
        t=fac[0]
        if t=='term':return ('t',fac[1])
        if t=='nt':return ('n',fac[1])
        if t=='opt':
            nm=fresh(ctx+'_opt');bnf[nm]=[d_seq(s,nm) for s in fac[1][1]]+[[]];return ('n',nm)
        if t=='star':
            nm=fresh(ctx+'_star');bnf[nm]=[d_seq(s,nm)+[('n',nm)] for s in fac[1][1]]+[[]];return ('n',nm)
        if t=='group':
            nm=fresh(ctx+'_grp');bnf[nm]=[d_seq(s,nm) for s in fac[1][1]];return ('n',nm)
    for name in order:
        bnf[name]=[d_seq(s,name) for s in RP(tokenize(prods[name])).alt()[1]]
    return bnf

# ---------- FIRST/FOLLOW/LL(1) for one state ----------
def check_state(text,tag):
    fails=[]
    prods,order,dups=load(text)
    # A file with no productions is not an EBNF file at all. load()
    # returns an empty order, and start=order[0] below indexes it.
    # Report what was found instead of crashing on it.
    if not order:
        return ["no productions recognised: not an EBNF file"],[],0,0
    start=order[0]
    if dups:fails.append(f"duplicate LHS: {sorted(set(dups))}")
    bnf=desugar(prods,order)
    NT=set(bnf)
    refs={s[1] for prod in bnf.values() for alt in prod for s in alt if s[0]=='n'}
    undef=sorted(r for r in refs if r not in NT)
    if undef:fails.append(f"undefined nonterminals: {undef}")
    unused=sorted(d for d in order if d not in refs and d!=start)
    # unused is a warning, not a failure
    # A dangling reference makes the FIRST computation below index a key that
    # does not exist. Report what was found instead of crashing on it.
    if undef:return fails,unused,len(order),len(bnf)

    nullable=set();ch=True
    while ch:
        ch=False
        for A,ps in bnf.items():
            if A in nullable:continue
            for p in ps:
                if all(s[0]=='n' and s[1] in nullable for s in p):nullable.add(A);ch=True;break
    def snull(s):return s[0]=='n' and s[1] in nullable
    def seqnull(seq):return all(snull(s) for s in seq)
    FIRST={A:set() for A in bnf}
    def fsym(s):return {s[1]} if s[0]=='t' else FIRST[s[1]]
    def fseq(seq):
        S=set()
        for s in seq:
            S|=fsym(s)
            if not snull(s):break
        return S
    ch=True
    while ch:
        ch=False
        for A,ps in bnf.items():
            b=len(FIRST[A])
            for p in ps:FIRST[A]|=fseq(p)
            if len(FIRST[A])!=b:ch=True
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
    ll1=[]
    for A,ps in bnf.items():
        preds=[]
        for p in ps:
            P=set(fseq(p))
            if seqnull(p):P|=FOLLOW[A]
            preds.append(P)
        for a in range(len(preds)):
            for b in range(a+1,len(preds)):
                inter=preds[a]&preds[b]
                if inter:ll1.append(f"{A}: alt#{a} vs alt#{b} on {sorted(inter)}")
    if ll1:fails.append(f"{len(ll1)} LL(1) conflict(s): "+"; ".join(ll1))
    return fails,unused,len(order),len(bnf)

def task_on(t):
    t=t.replace('\nNonCombatResolution = SuccessTail\n','\n# NonCombatResolution = SuccessTail\n',1)
    t=t.replace('# NonCombatResolution = [TaskLiquidation] SuccessTail','NonCombatResolution = [TaskLiquidation] SuccessTail',1)
    t=t.replace('# TaskLiquidation  = difficultTask solution','TaskLiquidation  = difficultTask solution',1)
    return t
def trag_on(t):
    t=t.replace('\nCombatOutcome    = victory SuccessTail\n','\n# CombatOutcome    = victory SuccessTail\n',1)
    t=t.replace('# CombatOutcome    = victory SuccessTail | TragicFall','CombatOutcome    = victory SuccessTail | TragicFall',1)
    t=t.replace('# TragicFall       = exposure punishment','TragicFall       = exposure punishment',1)
    return t

def main():
    unknown = [a for a in sys.argv[1:] if a.startswith('-')]
    if unknown:
        sys.exit("regression.py: unknown option %s" % unknown[0])
    path=sys.argv[1] if len(sys.argv)>1 else 'ProppEBNF43.txt'
    src=open(path,encoding='utf-8').read()
    ok=True

    print("== STYLE INVARIANTS ==")
    em=src.count('\u2014')
    print(f"  em dashes: {em}", "OK" if em==0 else "FAIL");    ok&=em==0
    dead=[d for d in ['DirectConflict','CoreDevelopment','TragicConflict','TragicMove'] if d in src]
    print(f"  dissolved rule names present: {dead or 'none'}", "OK" if not dead else "FAIL"); ok&=not dead
    marks=[m.group(1) for m in
           (re.match(r'^#\s+(\S+)\s+\.\.\.',ln) for ln in src.split('\n') if 'comment' in ln.lower())
           if m]
    badmark=[m for m in marks if m!='#']
    # Positive form: a file documenting no marker FAILS. The negative form
    # was vacuously satisfiable, so a grammar file carrying no notation
    # block passed in silence, which is the case this invariant exists for.
    goodmark=bool(marks) and not badmark
    print(f"  documented comment marker: {marks or 'none'}", "OK" if goodmark else "FAIL"); ok&=goodmark
    dq=sum(strip(ln).count('"') for ln in src.split('\n')
           if not ln.strip().startswith('#'))
    # Terminals are single quoted. Measured in CODE TEXT ONLY, through the
    # loader's own strip(), because the comment blocks carry Propp's
    # quotation marks and a raw count over the whole file would fail every
    # grammar file in the set. Two characters per terminal, so the failing
    # figure is the delimiter count and not the number of terminals.
    print(f"  double quotes in code text: {dq}", "OK" if dq==0 else "FAIL"); ok&=dq==0

    print("== STRUCTURE + LL(1), all four toggle states ==")
    states=[("both off",src),("task on",task_on(src)),
            ("tragedy on",trag_on(src)),("both on",trag_on(task_on(src)))]
    for tag,text in states:
        fails,unused,nr,nb=check_state(text,tag)
        status="OK" if not fails else "FAIL"
        print(f"  [{tag:10}] rules {nr} -> {nb} nonterminals : {status}")
        for f in fails:print("       -",f)
        if unused:print("       (unused, non-fatal):",unused)
        ok&=not fails

    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)

if __name__=="__main__":
    main()