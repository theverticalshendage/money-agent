from money_agent.transactions.models import Transaction, BalancePoint

def compute_running_balance(transactions: list[Transaction], opening_balance: float)-> list[BalancePoint]:
    """Compute the running balance after each transaction, in date order.

    Pure function: given the same transactions and opening balance, always
    returns the same result. Does not print or mutate its inputs.
    """

    ordered = sorted(transactions, key=lambda txn:txn.txn_date)

    running_balance = opening_balance
    points: list[BalancePoint] = []

    for txn in ordered:
        running_balance = running_balance + txn.amount
        points.append(BalancePoint(transaction=txn, balance_after=running_balance))
        
    return points
