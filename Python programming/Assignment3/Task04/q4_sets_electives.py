"""Q4: Elective Registration Clash Detection"""
import time
ai={"192311001","192311004","192311007","192311009"}
iot={"192311002","192311004","192311009","192311010"}
all_students={f"1923110{i:02d}" for i in range(1,11)}
print("Clash:",sorted(ai & iot))
print("Exactly one:",sorted(ai ^ iot))
print("Neither:",sorted(all_students-(ai|iot)))
print("Methods:",sorted(ai.intersection(iot)), sorted(ai.symmetric_difference(iot)))
print("Empty intersection:",set().intersection(ai))
print("Identical symmetric difference:",ai.symmetric_difference(ai))
for n in (10000,100000,1000000):
    values=[f"REG{i:07d}" for i in range(n)]; lookup=set(values); target=values[-1]
    t=time.perf_counter(); _=target in values; list_time=time.perf_counter()-t
    t=time.perf_counter(); _=target in lookup; set_time=time.perf_counter()-t
    print(n,"list membership:",round(list_time,7),"set membership:",round(set_time,7))
