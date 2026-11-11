"""Exact calibration only. No learner outcomes or performance simulation."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json

def main():
    assignments=list(product((0,1),repeat=12)); rows=[]
    for m in range(13):
        tails={k:Fraction(sum(comb(m,j) for j in range(k,m+1)),2**m) for k in range(m+1)}
        histogram=[0]*(m+1)
        for bits in assignments: histogram[sum(bits[:m])]+=1
        for k in range(m+1):
            empirical=Fraction(sum(histogram[k:]),len(assignments))
            if empirical!=tails[k]: raise ValueError('enumeration disagrees with binomial tail')
        rejection_count=sum(histogram[k] for k in range(m+1) if tails[k]<=Fraction(1,20))
        rate=Fraction(rejection_count,4096)
        if rate>Fraction(1,20): raise ValueError('type I bound exceeded')
        rows.append({'discordant_pairs':m,'minimum_treatment_wins_to_reject':next((k for k in range(m+1) if tails[k]<=Fraction(1,20)),None),'rejection_probability_under_sharp_null':str(rate),'assignments_rejected':rejection_count})
    print(json.dumps({'scope':'Exact randomisation calibration under independent fair within-pair assignment and sharp null; no observations','pairs':12,'assignments_per_row':4096,'alpha':'1/20','alternative':'lesson improves joint correctness','rows':rows,'all_discordant_examples':{'wins_9_of_12_p':str(Fraction(sum(comb(12,j) for j in range(9,13)),4096)),'wins_10_of_12_p':str(Fraction(sum(comb(12,j) for j in range(10,13)),4096))},'observed_agent_sessions':0,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'command':'python research/agent-attempts/0004/calibrate.py'},indent=2,sort_keys=True))
if __name__=='__main__':main()
