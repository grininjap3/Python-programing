"""Q7: Diagnose and redesign Q4 statement construction."""
from Task04.string_building import build_plus, build_join, measure

if __name__ == "__main__":
    for size in (1_000,10_000,200_000):
        data=[f"Record{i}:value{i%100}" for i in range(size)]
        old,old_samples,old_avg=measure(build_plus,data)
        new,new_samples,new_avg=measure(build_join,data)
        print({"items":size,"output_length":len(new),"identical":old==new,
               "plus_samples":old_samples,"plus_mean":old_avg,
               "join_samples":new_samples,"join_mean":new_avg})
