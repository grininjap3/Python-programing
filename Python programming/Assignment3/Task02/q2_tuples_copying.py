"""Q2: Tuples, Mutability and Copying"""
import copy, sys, time
bad = [[0]*4]*3
bad[0][1] = 7
good = [[0 for _ in range(4)] for _ in range(3)]
good[0][1] = 7
print("Aliased grid:", bad)
print("Independent grid:", good)
print("Same row?", bad[0] is bad[1], good[0] is good[1])

locations = {(13.0827,80.2707):"Chennai Central", (13.0418,80.2341):"T. Nagar"}
print(locations[(13.0418,80.2341)])
try: locations[[13.0,80.0]] = "invalid"
except TypeError as e: print("List key error:", e)

original=[[1,2],[3,4]]
alias=original; shallow=copy.copy(original); deep=copy.deepcopy(original)
original[0][0]=99
print("Alias:", alias, "Shallow:", shallow, "Deep:", deep)
for coord, name in locations.items():
    lat, lon = coord
    print(name, "latitude:", lat, "longitude:", lon)
print("Container sizes (bytes):", sys.getsizeof(tuple(range(1000000))), sys.getsizeof(list(range(1000000))))
nested=("route", [1,2,3]); nested[1].append(4)
print("Tuple with mutable list:", nested)
