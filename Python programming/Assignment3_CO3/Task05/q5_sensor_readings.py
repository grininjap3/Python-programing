"""Q5: Cleaning Sensor Readings"""
import random, time, sys

def valid(c): return -50 <= c <= 50

def for_loop(data):
    clean=[]; fahrenheit=[]
    for x in data:
        if valid(x):
            clean.append(x); fahrenheit.append(x*9/5+32)
    return clean,fahrenheit

def comprehension(data):
    clean=[x for x in data if valid(x)]
    fahrenheit=[x*9/5+32 for x in data if valid(x)]
    return clean,fahrenheit

def map_filter(data):
    clean=list(filter(lambda x:valid(x),data))
    return clean,list(map(lambda x:x*9/5+32,clean))

if __name__=="__main__":
    readings=[2.5,3.0,60.0,-55.0,7.2,9.1,1.5]
    assert for_loop(readings)==comprehension(readings)==map_filter(readings)
    c,f=comprehension(readings)
    alarms=[(i,t) for i,t in enumerate(readings) if valid(t) and not 2<=t<=8]
    print("Valid Celsius:",c)
    print("Fahrenheit:",[round(x,2) for x in f])
    print("Alarm minutes (zero-based):",alarms)
    for n in (10000,100000,1000000):
        data=[random.uniform(-60,60) for _ in range(n)]; times=[]
        for fn in (for_loop,comprehension,map_filter):
            t=time.perf_counter(); fn(data); times.append(time.perf_counter()-t)
        print(n,"loop/comprehension/map-filter:",[round(x,4) for x in times])
    print("All valid:",len(comprehension([1,2,3])[0])==3)
    print("All invalid:",len(comprehension([100,-100])[0])==0)
    print("Generator shallow size:",sys.getsizeof((x for x in readings)))
