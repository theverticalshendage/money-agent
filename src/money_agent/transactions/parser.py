from datetime import date;
from money_agent.transactions.models import Transaction, TransactionType

# A lookup of known merchant keywords -> (clean name, transaction type).
# This is the "fast path": if we recognize a keyword, no guessing needed.
_MERCHANT_RULES: dict[str, tuple[str, TransactionType]] = {
    "NETFLIX": ("Netflix", TransactionType.SUBSCRIPTION),
    "SPOTIFY": ("Spotify", TransactionType.SUBSCRIPTION),
    "PRIME": ("Prime", TransactionType.SUBSCRIPTION),
    "SALARY": ("Salary", TransactionType.SALARY)
}

# Keywords that identify bank fees, mapped to a readable label.
_FEE_KEYWORDS: dict[str, str] = {
    "MAB CHG": "Minimum balance charge",
    "CHQ RTN": "Cheque return charge",
    "MB CHG": "Mobile banking charge"
}

def parse_narration(raw_narration: str, amount: float, txn_date: date) -> Transaction:
    """Interpret a raw bank narration into a structured Transaction.

    This is pure: same inputs always produce the same output, with no
    side effects. That is what makes it reusable and easy to test.
    """
    # Normalize once, so all our matching is case-insensitive.
    text = raw_narration.upper()

    # 1. Is it a known fee?
    for keyword, label in _FEE_KEYWORDS.items():
        if keyword in text:
            return Transaction(
                raw_narration=raw_narration,
                amount=amount,
                txn_date=txn_date,
                txn_type=TransactionType.FEE,
                merchant=label
            )

    # 2. Is it a known merchant / salary?
    for keyword, (clean_name, txn_type) in _MERCHANT_RULES.items():
        if keyword in text:
            return Transaction(
                raw_narration=raw_narration,
                amount=amount,
                txn_date=txn_date,
                txn_type=txn_type,
                merchant=clean_name,
            )

    # 3. Is it an EMI?
    if "EMI" in text:
        return Transaction(
            raw_narration=raw_narration,
            amount=amount,
            txn_date=txn_date,
            txn_type=TransactionType.EMI,
        )

    # 4. A card purchase (POS = point of sale)?
    if "POS" in text:
        return Transaction(
            raw_narration=raw_narration,
            amount=amount,
            txn_date=txn_date,
            txn_type=TransactionType.PURCHASE,
        )

    # 5. Fallback: we could not identify it.
    return Transaction(
        raw_narration=raw_narration,
        amount=amount,
        txn_date=txn_date,
        txn_type=TransactionType.UNKNOWN,
    )