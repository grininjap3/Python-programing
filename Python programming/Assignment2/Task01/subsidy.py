"""Q1: State electricity subsidy eligibility."""
def subsidy_separate(units, ration_card, senior_over_80):
    results = []
    if units <= 100:
        results.append("Full subsidy")
    if 101 <= units <= 200 and ration_card:
        results.append("Partial subsidy")
    if units > 200 and senior_over_80:
        results.append("Senior-citizen exception")
    if not results:
        results.append("No subsidy")
    return results

def subsidy_chain(units, ration_card, senior_over_80):
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200:
        return "Partial subsidy" if ration_card else "No subsidy"
    elif units > 200:
        return "Senior-citizen exception" if senior_over_80 else "No subsidy"

if __name__ == "__main__":
    cases = [(80,False,False),(100,False,False),(101,True,False),
             (150,False,False),(200,True,False),(201,True,False),
             (250,False,True),(250,False,False)]
    for case in cases:
        print(case, "=>", subsidy_separate(*case), "|", subsidy_chain(*case))
