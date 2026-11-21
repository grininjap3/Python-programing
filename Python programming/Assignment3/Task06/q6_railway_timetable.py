"""Q6: Railway Timetable - Nested Data"""
import time
timetable={
"12631":{"name":"Nellai Express","stops":[("Chennai Egmore","20:10","20:20"),("Tambaram","20:42","20:44"),("Villupuram","22:25","22:30"),("Tirunelveli","06:50","07:00")],"days":{"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}},
"12633":{"name":"Kanyakumari Express","stops":[("Chennai Egmore","17:20","17:30"),("Tambaram","18:00","18:02"),("Villupuram","20:10","20:15"),("Nagercoil","05:30","05:40")],"days":{"Mon","Wed","Fri"}},
"12635":{"name":"Vaigai Express","stops":[("Chennai Egmore","13:50","14:00"),("Tambaram","14:30","14:32"),("Villupuram","16:20","16:25"),("Madurai","22:00","22:10")],"days":{"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}},
"12637":{"name":"Pandian Express","stops":[("Chennai Egmore","21:00","21:10"),("Tambaram","21:40","21:42"),("Villupuram","23:30","23:35"),("Madurai","06:15","06:25")],"days":{"Tue","Thu","Sat"}},
"12639":{"name":"Ananthapuri Express","stops":[("Chennai Egmore","19:30","19:40"),("Tambaram","20:10","20:12"),("Villupuram","22:00","22:05"),("Kollam","07:00","07:10")],"days":{"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}}}

def build_index(data):
    index={}
    for number,details in data.items():
        for station,arr,dep in details["stops"]:
            index.setdefault(station,[]).append((number,arr,dep))
    return index

def find_trains(data,index,station,day):
    result=[]
    for number,arr,dep in index.get(station,[]):
        if day in data[number]["days"]:
            result.append((dep,number,data[number]["name"],arr))
    return sorted(result)

if __name__=="__main__":
    index=build_index(timetable)
    for dep,no,name,arr in find_trains(timetable,index,"Tambaram","Mon"):
        print(no,name,"arrival",arr,"departure",dep)
    print("Unknown station:",find_trains(timetable,index,"Atlantis","Mon"))
    print("Non-running day:",find_trains(timetable,index,"Tambaram","Sun"))
    for n in (100,1000,10000):
        generated={str(i):{"name":f"Train {i}","stops":[(f"Station{j%100}","08:00","08:05") for j in range(10)],"days":{"Mon","Wed","Fri"}} for i in range(n)}
        t=time.perf_counter(); idx=build_index(generated); build=time.perf_counter()-t
        t=time.perf_counter(); find_trains(generated,idx,"Station20","Mon"); query=time.perf_counter()-t
        print(n,"index build:",round(build,4),"indexed query:",round(query,4))
