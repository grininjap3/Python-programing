"""Q1: Daily Rainfall Records - Lists and Slicing"""
import random, time

def moving_average_naive(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]

def moving_average_running(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    if len(values) < window: return []
    total = sum(values[:window]); result = [total/window]
    for i in range(window, len(values)):
        total += values[i] - values[i-window]
        result.append(total/window)
    return result

def analyse(readings):
    weekly = [sum(readings[i:i+7]) for i in range(0, len(readings), 7)]
    wet = max(enumerate(weekly, 1), key=lambda x:x[1]) if weekly else None
    dry = min(enumerate(weekly, 1), key=lambda x:x[1]) if weekly else None
    dry_days = [(i+1,v) for i,v in enumerate(readings) if v == 0]
    return weekly, wet, dry, moving_average_running(readings), dry_days

if __name__ == "__main__":
    random.seed(42)
    readings = [round(random.uniform(0,25),1) for _ in range(365)]
    weekly, wet, dry, averages, dry_days = analyse(readings)
    print("Weekly totals:", [round(x,1) for x in weekly])
    print("Wettest week:", wet, "Driest week:", dry)
    print("First 5 moving averages:", [round(x,2) for x in averages[:5]])
    print("Dry days:", dry_days)
    print("readings[7:14]:", readings[7:14])
    print("readings[-7:]:", readings[-7:])
    print("readings[::7]:", readings[::7])
    print("Short/empty:", moving_average_running([1,2,3]), moving_average_running([]))
    for n in (365, 36500, 365000):
        data = [random.random()*30 for _ in range(n)]
        t=time.perf_counter(); a=moving_average_naive(data); naive=time.perf_counter()-t
        t=time.perf_counter(); b=moving_average_running(data); fast=time.perf_counter()-t
        assert all(abs(x-y)<1e-9 for x,y in zip(a,b))
        print(n, "naive:", round(naive,5), "running:", round(fast,5))
