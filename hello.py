print("Day 1 is running");
def bad(items=[]):   # DON'T — the [] is created ONCE and shared across all calls
    items.append(1)
    return items
print(bad())

merchant = "Netflix"
amount = 649

f"Your {merchant} charge was ₹{amount}"        # "Your Netflix charge was ₹649.0"
print(f"Amount: ₹{amount:.1f}")