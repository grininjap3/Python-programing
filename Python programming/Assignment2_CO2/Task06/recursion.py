"""Q6: Count ways to climb stairs using 1 or 2 steps."""
import sys
from functools import lru_cache

naive_calls=0
def ways_naive(n):
    global naive_calls
    naive_calls += 1
    if n <= 1: return 1
    return ways_naive(n-1)+ways_naive(n-2)

memo_calls=0
@lru_cache(maxsize=None)
def ways_memo(n):
    global memo_calls
    memo_calls += 1
    if n <= 1: return 1
    return ways_memo(n-1)+ways_memo(n-2)

def ways_loop(n):
    if n <= 1: return 1
    previous=current=1
    for _ in range(2,n+1): previous,current=current,previous+current
    return current

if __name__ == "__main__":
    print("n=1..6:",[ways_loop(n) for n in range(1,7)])
    naive_calls=0; print("naive:",ways_naive(25),"calls:",naive_calls)
    ways_memo.cache_clear(); memo_calls=0
    print("memo:",ways_memo(25),"calls:",memo_calls)
    print("loop n=1000 digits:",len(str(ways_loop(1000))))
    print("recursion limit:",sys.getrecursionlimit())
    ways_memo.cache_clear()
    try: print("memo n=1000:",ways_memo(1000))
    except RecursionError as exc: print("RecursionError:",exc)
