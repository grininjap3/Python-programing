"""Q3: Farmer Helpline Complaint Analysis"""
import re, random, time
from collections import Counter
STOP={"not","high"}
CALLS=["seeds not received seeds delayed","fertiliser price high","seeds price high subsidy not received"]

def frequencies(texts, stop):
    counts={}
    for text in texts:
        for word in re.findall(r"[a-zA-Z]+", text.lower()):
            if word not in stop: counts[word]=counts.get(word,0)+1
    return counts

def top(counts,k):
    return sorted(counts.items(), key=lambda item:(-item[1],item[0]))[:k]

def group_by_district(records):
    groups={}
    for district, complaint in records:
        groups.setdefault(district,[]).append(complaint)
    return groups

if __name__=="__main__":
    counts=frequencies(CALLS,STOP)
    print("Top words:",top(counts,3))
    print("District groups:",group_by_district([("Nellore","seed issue"),("Guntur","water issue"),("Nellore","fertiliser issue")]))
    random.seed(7); words=["seed","water","crop","fertiliser","price","subsidy"]
    for n in (1000,10000,100000):
        texts=[" ".join(random.choices(words,k=8)) for _ in range(n)]
        t=time.perf_counter(); d=frequencies(texts,set()); td=time.perf_counter()-t
        t=time.perf_counter(); c=Counter(w for line in texts for w in line.split()); tc=time.perf_counter()-t
        print(n,"dict:",round(td,4),"Counter:",round(tc,4),"unique terms:",len(d))
    print("Empty:",frequencies([""],STOP),"Case/punctuation:",frequencies(["SEEDS, Seeds!"],STOP))
