from datetime import date

from money_agent.transactions.models import TransactionType
from money_agent.transactions.parser import parse_narration


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