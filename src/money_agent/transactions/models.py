from dataclasses import dataclass;
from datetime import date;
from enum import Enum;

class TransactionType(str, Enum):
    """The kinds of transactions we can identify from a raw narration."""
    SUBSCRIPTION = "subscription"
    SALARY = "salary"
    FEE = "fee"
    EMI = "emi"
    TRANSFER = "transfer"
    PURCHASE = "purchase"
    UNKNOWN = "unknown"

@dataclass
class Transaction:
    """A single bank transaction, after we've interpreted its raw narration."""
    raw_narration: str          # the cryptic original, e.g. "POS DR 4412XXXX8901 MUMBAI"
    amount: float               # positive = credit (money in), negative = debit (money out)
    txn_date: date
    txn_type: TransactionType = TransactionType.UNKNOWN
    merchant: str | None = None  # e.g. "NETFLIX" — None if we couldn't identify one