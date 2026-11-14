"""Q7: Contact Merging from First Principles"""
import re, time

def normalize_phone(phone):
    digits=re.sub(r"\D","",phone)
    if len(digits)==12 and digits.startswith("91"): digits=digits[2:]
    return digits

def merge_contacts(sources):
    by_phone={}
    for source in sources:
        for contact in source:
            name=contact.get("name","").strip()
            phones={normalize_phone(p) for p in contact.get("phones",[])}; phones.discard("")
            emails={e.strip().lower() for e in contact.get("emails",[]) if e.strip()}
            if not phones:
                key="NAME:"+" ".join(name.lower().split())
                rec=by_phone.setdefault(key,{"names":set(),"phones":set(),"emails":set()})
                rec["names"].add(name); rec["emails"].update(emails); continue
            linked=[]
            for phone in phones:
                if phone in by_phone and all(by_phone[phone] is not r for r in linked):
                    linked.append(by_phone[phone])
            rec=linked[0] if linked else {"names":set(),"phones":set(),"emails":set()}
            for other in linked[1:]:
                rec["names"].update(other["names"]); rec["phones"].update(other["phones"]); rec["emails"].update(other["emails"])
            rec["names"].add(name); rec["phones"].update(phones); rec["emails"].update(emails)
            for phone in rec["phones"]: by_phone[phone]=rec
    unique={id(v):v for v in by_phone.values()}
    return sorted(unique.values(),key=lambda r:sorted(r["phones"])[0] if r["phones"] else "")

if __name__=="__main__":
    phone_a=[{"name":"Dr. Ravi","phones":["+91 98400 12345","044-22223333"],"emails":["Ravi@Example.com"]},{"name":"Meena","phones":["98765 43210"],"emails":["meena@example.com"]}]
    phone_b=[{"name":"ravi kumar","phones":["9840012345"],"emails":["r.kumar@example.com"]},{"name":"Meena R","phones":["+91-9876543210"],"emails":["MEENA@example.com"]}]
    sim=[{"name":"Ravi","phones":["04422223333"],"emails":["ravi.home@example.com"]},{"name":"Unknown contact","phones":[],"emails":["unknown@example.com"]}]
    start=time.perf_counter(); merged=merge_contacts([phone_a,phone_b,sim]); elapsed=time.perf_counter()-start
    for i,c in enumerate(merged,1):
        print("Contact",i,"Names:",sorted(c["names"]),"Phones:",sorted(c["phones"]),"Emails:",sorted(c["emails"]))
    print("Merge time:",round(elapsed,6),"seconds")
