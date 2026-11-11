"""Bounded Q0004 experiment; no universal formal-verification claim."""
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import hashlib, json, sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from atlas_math.engine import verify

def bezout(a,c):
    r,s=abs(a),abs(c); u,v,w,z=1,0,0,1
    while s:
        q=r//s; r,s=s,r-q*s; u,w=w,u-q*w; v,z=z,v-q*z
    return r,u*(-1 if a<0 else 1),v*(-1 if c<0 else 1)

def certificate(A,p,q,x,y):
    a,b=A[0]; c,d=A[1]; D=a*d-b*c
    result=verify({'id':'q4','A':A,'b':[p,q],'kind':'unique'},
        {'status':'unique','solution':[str(x),str(y)],'certificate':{'determinant':str(D)}})
    if not result['accepted']: raise ValueError(result)

def main():
    counts=dict(matrices=0,singular_excluded=0,primitive=0,nonprimitive=0,rhs_checked=0,constructive_witnesses=0,obstruction_witnesses=0,shortcut_false_positives=0,negative_determinants=0,zero_entry_matrices=0)
    digest=hashlib.sha256()
    for a,b,c,d in product(range(-3,4),repeat=4):
        D=a*d-b*c
        if not D: counts['singular_excluded']+=1; continue
        counts['matrices']+=1; counts['negative_determinants']+=D<0
        counts['zero_entry_matrices']+=0 in (a,b,c,d)
        g,u,v=bezout(a,c)
        if g!=gcd(a,c) or u*a+v*c!=g: raise ValueError('Bezout certificate')
        A=[[a,b],[c,d]]; counts['primitive' if g==1 else 'nonprimitive']+=1
        if g>1:
            p,q=a//g,c//g
            certificate(A,p,q,Fraction(1,g),0)
            if (a*q-c*p)!=0 or Fraction(1,g).denominator==1: raise ValueError('obstruction')
            counts['obstruction_witnesses']+=1
        for p,q in product(range(-3,4),repeat=2):
            counts['rhs_checked']+=1
            x,y=Fraction(d*p-b*q,D),Fraction(a*q-c*p,D)
            certificate(A,p,q,x,y)
            integral=x.denominator==y.denominator==1
            passes=(a*q-c*p)%D==0
            if integral and not passes: raise ValueError('necessity')
            if passes and g==1:
                k=(a*q-c*p)//D; r,s=p-b*k,q-d*k
                constructed=u*r+v*s
                certificate(A,p,q,constructed,k)
                if not integral or (constructed,k)!=(x,y): raise ValueError('construction')
                counts['constructive_witnesses']+=1
            counts['shortcut_false_positives']+=passes and not integral
            digest.update(json.dumps([a,b,c,d,p,q,str(x),str(y),passes,integral],separators=(',',':')).encode()+b'\n')
    print(json.dumps({'bounds':{'matrix_entries':[-3,3],'rhs_entries':[-3,3]},'counts':counts,
       'ordered_case_sha256':digest.hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'verifier_sha256':hashlib.sha256((ROOT/'atlas_math/engine.py').read_bytes()).hexdigest(),
       'status':'finite-certificate-checks-passed','source_base':'e829b52ef6ca89e7409a7b950d829870f19529dd',
       'scope':'All stated finite cases only; no new Lean proof, novelty or measured learning',
       'command':'python research/agent-attempts/0003/check.py'},indent=2,sort_keys=True))
if __name__=='__main__': main()
