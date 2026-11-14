"""Q2: OTP attempts using while, for and recursion."""
def verify_while(correct, entries):
    attempts = i = 0
    while attempts < 3:
        if i >= len(entries):
            break
        entered = entries[i]; i += 1
        if not entered.strip():
            continue
        attempts += 1
        if entered == correct:
            print("OTP verified"); break
        else:
            pass  # intentional no-op for a wrong OTP
    else:
        print("Account locked for 30 minutes")
    return attempts

def verify_for(correct, entries):
    attempts = 0
    for entered in entries:
        if attempts >= 3: break
        if not entered.strip(): continue
        attempts += 1
        if entered == correct:
            print("OTP verified"); break
        else: pass
    else:
        if attempts == 3: print("Account locked for 30 minutes")
    return attempts

def verify_recursive(correct, entries, index=0, attempts=0, limit=3):
    if attempts >= limit:
        print("Account locked for 30 minutes"); return False
    if index >= len(entries): return False
    entered = entries[index]
    if not entered.strip():
        return verify_recursive(correct, entries, index+1, attempts, limit)
    if entered == correct: print("OTP verified"); return True
    return verify_recursive(correct, entries, index+1, attempts+1, limit)

if __name__ == "__main__":
    sample = ["", "1111", "2222", "1234"]
    verify_while("1234", sample)
    verify_for("1234", sample)
    verify_recursive("1234", sample)
