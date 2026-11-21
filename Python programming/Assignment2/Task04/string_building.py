"""Q4: Compare +=, join and f-string statement construction."""
import time

def build_plus(parts):
    text = ""
    for part in parts: text += part + ";"
    return text

def build_join(parts):
    return "".join(part + ";" for part in parts)

def build_fstring(parts):
    return "".join(f"{part};" for part in parts)

def measure(fn, parts, repeats=3):
    times=[]; result=None
    for _ in range(repeats):
        start=time.perf_counter(); result=fn(parts); times.append(time.perf_counter()-start)
    return result, times, sum(times)/len(times)

if __name__ == "__main__":
    for size in (1_000, 10_000, 200_000):
        items=[f"Item{i}:Rs{i%50}" for i in range(size)]
        results=[measure(fn,items) for fn in (build_plus,build_join,build_fstring)]
        print("size:",size,"same:",results[0][0]==results[1][0]==results[2][0])
        for name,(_,samples,avg) in zip(("plus","join","f-string"),results):
            print(name,"samples:",[round(x,6) for x in samples],"average:",round(avg,6))
