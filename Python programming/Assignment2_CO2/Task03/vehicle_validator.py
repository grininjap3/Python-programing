"""Q3: Normalise, validate and format vehicle registration numbers."""
def normalise(text):
    return text.replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    if len(reg) not in (9, 10): return False
    if not reg[:2].isalpha() or not reg[2:4].isdigit(): return False
    series = reg[4:-4]
    return len(series) in (1, 2) and series.isalpha() and reg[-4:].isdigit()

def format_receipt(reg):
    if not is_valid(reg): raise ValueError("Invalid registration number")
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"

if __name__ == "__main__":
    samples = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234",
               "TN 22 1234 AB", "ap 05 z 6789", "MH-12-XY-987"]
    for raw in samples:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")
        if is_valid(reg): print("Receipt:", format_receipt(reg))
