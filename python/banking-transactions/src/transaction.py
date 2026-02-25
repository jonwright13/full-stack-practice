from typing import Literal
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Transaction:
    """
    Provides a record of the transaction
    """

    transaction_id: str
    account_id: str
    timestamp: datetime
    transaction_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: int
    balance_after: int
    description: str

    def __str__(self):
        return f"{self.timestamp} | Type: {self.transaction_type} | {self.amount} | Balance={self.balance_after} | {self.description}"
