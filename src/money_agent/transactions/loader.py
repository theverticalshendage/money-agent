import json;
from datetime import date;
from pathlib import Path;

from money_agent.transactions.models import Transaction;
from money_agent.transactions.parser import parse_narration;

def load_transactions(file_path: str | Path)-> list[Transaction]:
    """Load transactions from a JSON file and parse each into a Transaction.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file is not valid JSON or is missing expected fields.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Transaction file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"File is not valid JSON: {path}") from e

    raw_transactions = data.get("transactions", [])

    transactions: list[Transaction] = []
    for record in raw_transactions:
        txn = parse_narration(
            raw_narration=record["narration"],
            amount=record["amount"],
            txn_date=date.fromisoformat(record["date"]),
        )
        transactions.append(txn)

    return transactions