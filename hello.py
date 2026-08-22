# hello.py — personal scratch/experiment file for trying things out.
# Not part of the actual money-agent package. Safe to ignore.

print("Day 1 is running");
def bad(items=[]):   # DON'T — the [] is created ONCE and shared across all calls
    items.append(1)
    return items
print(bad())

merchant = "Netflix"
amount = 649

f"Your {merchant} charge was ₹{amount}"        # "Your Netflix charge was ₹649.0"
print(f"Amount: ₹{amount:.1f}")

txn = "2100.00  UPI/CR/774521/REFUND AMAZON"
op = txn.split(" ")
print(op[-1])

l1 = " an an d "
print(l1.strip())



# try_loader
# import json
# from pathlib import Path
# from money_agent.transactions.loader import load_transactions;
# from money_agent.transactions.analyzer import compute_running_balance;


# path = Path("data/transactions.json")

# with open(path, "r", encoding="utf-8") as f:
#     opening = json.load(f)["opening_balance"]

# txns = load_transactions(path)
# points = compute_running_balance(txns, opening_balance=opening)

# print(f"\nOpening balance: {opening:>12,.2f}\n")
# for point in points:
#     txn = point.transaction
#     print(
#         f" {txn.txn_date} {txn.txn_type.value:12}  "
#         f" {txn.amount:>18,.2f}  →  balance:{point.balance_after:>12,.2f}"
#         )