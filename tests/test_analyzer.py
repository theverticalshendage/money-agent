from datetime import date

from money_agent.transactions.models import Transaction, TransactionType
from money_agent.transactions.analyzer import compute_running_balance


def _txn(amount: float, day: int) -> Transaction:
    """Small helper to build a test transaction quickly."""
    return Transaction(
        raw_narration=f"TEST TXN {day}",
        amount=amount,
        txn_date=date(2025, 7, day),
        txn_type=TransactionType.UNKNOWN,
    )


def test_empty_list_returns_empty():
    result = compute_running_balance([], opening_balance=1000.0)
    assert result == []


def test_single_credit_increases_balance():
    txns = [_txn(500.0, day=1)]
    result = compute_running_balance(txns, opening_balance=1000.0)
    assert len(result) == 1
    assert result[0].balance_after == 1500.0


def test_single_debit_decreases_balance():
    txns = [_txn(-300.0, day=1)]
    result = compute_running_balance(txns, opening_balance=1000.0)
    assert result[0].balance_after == 700.0


def test_running_balance_accumulates_in_sequence():
    txns = [_txn(1000.0, day=1), _txn(-200.0, day=2), _txn(-300.0, day=3)]
    result = compute_running_balance(txns, opening_balance=5000.0)
    # 5000 -> 6000 -> 5800 -> 5500
    assert result[0].balance_after == 6000.0
    assert result[1].balance_after == 5800.0
    assert result[2].balance_after == 5500.0


def test_transactions_are_sorted_by_date_before_computing():
    # Deliberately pass them OUT of date order (day 3 first, day 1 last).
    # The analyzer must sort them, so the result should be in date order.
    txns = [_txn(-300.0, day=3), _txn(1000.0, day=1), _txn(-200.0, day=2)]
    result = compute_running_balance(txns, opening_balance=5000.0)

    # Results must come back in DATE order (day 1, 2, 3), not input order.
    assert result[0].transaction.txn_date == date(2025, 7, 1)
    assert result[1].transaction.txn_date == date(2025, 7, 2)
    assert result[2].transaction.txn_date == date(2025, 7, 3)

    # And the balance must reflect that sorted order: 5000 -> 6000 -> 5800 -> 5500
    assert result[2].balance_after == 5500.0


def test_does_not_mutate_the_input_list():
    # Purity check: the original list order must be untouched after the call.
    txns = [_txn(-300.0, day=3), _txn(1000.0, day=1)]
    original_first = txns[0]
    compute_running_balance(txns, opening_balance=1000.0)
    assert txns[0] is original_first  # still day 3 first — input unchanged