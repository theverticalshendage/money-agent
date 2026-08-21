from datetime import date

from money_agent.transactions.models import TransactionType
from money_agent.transactions.parser import parse_narration


def test_enum_values_are_spelled_correctly():
    # Guards against typos in enum string values (like "subscritption").
    # These strings end up in JSON and the agent's output, so they must be exact.
    assert TransactionType.SUBSCRIPTION.value == "subscription"
    assert TransactionType.SALARY.value == "salary"
    assert TransactionType.FEE.value == "fee"
    assert TransactionType.EMI.value == "emi"
    assert TransactionType.TRANSFER.value == "transfer"
    assert TransactionType.PURCHASE.value == "purchase"
    assert TransactionType.UNKNOWN.value == "unknown"

def test_identifies_a_fee():
    txn = parse_narration("MAB CHG JUL 2025", amount=-590.0, txn_date=date(2025, 7, 15))
    assert txn.txn_type == TransactionType.FEE
    assert txn.merchant == "Minimum balance charge"


def test_identifies_a_subscription():
    txn = parse_narration("NETFLIX SUBSCRIPTION", amount=-649.0, txn_date=date(2025, 7, 3))
    assert txn.txn_type == TransactionType.SUBSCRIPTION
    assert txn.merchant == "Netflix"


def test_identifies_salary_as_a_credit():
    txn = parse_narration("NEFT CR SALARY", amount=85000.0, txn_date=date(2025, 7, 1))
    assert txn.txn_type == TransactionType.SALARY
    assert txn.amount > 0  # a credit is positive


def test_identifies_an_emi():
    txn = parse_narration("EMI HDFC HOME LOAN", amount=-22000.0, txn_date=date(2025, 7, 5))
    assert txn.txn_type == TransactionType.EMI


def test_identifies_a_card_purchase():
    txn = parse_narration("POS DR 4412XXXX8901 MUMBAI", amount=-1250.0, txn_date=date(2025, 7, 12))
    assert txn.txn_type == TransactionType.PURCHASE


def test_unknown_narration_falls_back_gracefully():
    txn = parse_narration("SOME CRYPTIC GIBBERISH XYZ", amount=-100.0, txn_date=date(2025, 7, 20))
    assert txn.txn_type == TransactionType.UNKNOWN
    assert txn.merchant is None


def test_matching_is_case_insensitive():
    txn = parse_narration("netflix subscription", amount=-649.0, txn_date=date(2025, 7, 3))
    assert txn.txn_type == TransactionType.SUBSCRIPTION

# ---- Edge case exploration (some of these will FAIL — that's the point) ----

def test_edge_netflix_refund_is_not_a_subscription():
    # A refund: money coming BACK (positive amount), but narration says NETFLIX
    txn = parse_narration("NETFLIX REFUND", amount=649.0, txn_date=date(2025, 7, 3))
    # We might EXPECT a refund not to be labeled a plain subscription...
    # what does it actually do? Let's assert it IS subscription and see:
    assert txn.txn_type == TransactionType.UNKNOWN
    assert txn.amount > 0  # this part is true — but is the type right?


def test_edge_empty_narration():
    txn = parse_narration("", amount=-100.0, txn_date=date(2025, 7, 20))
    assert txn.txn_type == TransactionType.UNKNOWN


def test_edge_multiple_keywords_which_wins():
    # Contains BOTH "SALARY" and "NETFLIX" — which does the parser pick?
    txn = parse_narration("SALARY BONUS NETFLIX GIFT", amount=5000.0, txn_date=date(2025, 7, 1))
    # Guess which one wins, then assert it and see if you're right:
    assert txn.txn_type == TransactionType.SALARY


def test_edge_whitespace_and_casing():
    txn = parse_narration("  netflix   subscription  ", amount=-649.0, txn_date=date(2025, 7, 3))
    assert txn.txn_type == TransactionType.SUBSCRIPTION


def test_edge_zero_amount():
    txn = parse_narration("MAB CHG", amount=0.0, txn_date=date(2025, 7, 15))
    assert txn.txn_type == TransactionType.FEE