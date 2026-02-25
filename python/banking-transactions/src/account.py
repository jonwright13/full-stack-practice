from uuid import uuid4
from datetime import datetime, timezone

from errors import InsufficientFundsError, InvalidTransactionError
from transaction import Transaction


class Account:

    def __init__(self, *, starting_balance: str = "0"):

        # Perform checks on starting balance
        self._validate_starting_amount(starting_balance)

        # Init starting balance and account id
        self.account_id = str(uuid4())
        self._balance = int(starting_balance)

        # Init empty list for transaction history
        self._transaction_history: list[Transaction] = []

    @property
    def balance(self) -> int:
        return self._balance

    def deposit(self, amount: str, description: str = "") -> Transaction:
        """
        Deposit funds into the account. Checks amount if is valid before updating the account balance and updating the transaction history with a Transaction object
        """
        # Perform checks on amount
        self._validate_transaction(amount)

        # Calculate new balance
        deposit_amount = int(amount)
        self._balance += deposit_amount

        # Init a transaction object
        transaction = Transaction(
            str(uuid4()),
            self.account_id,
            datetime.now(timezone.utc),
            "DEPOSIT",
            deposit_amount,
            self._balance,
            description,
        )

        # Append the transaction history with the transaction
        self._transaction_history.append(transaction)

        return transaction

    def withdraw(self, amount: str, description: str = "") -> Transaction:
        """
        Withdraw funds from account. Checks amount if is valid and whether the remaining balance is valid before updating the account balance and updating the transaction history.
        """

        # Check is amount valid
        self._validate_transaction(amount)

        # Calculate new balance
        withdraw_amount = int(amount)
        new_balance = self._balance - withdraw_amount

        # Check if the new balance is valid
        if new_balance < 0:
            raise InsufficientFundsError(new_balance)

        # Push the new balance to the account
        self._balance = new_balance

        # Init a transaction object
        transaction = Transaction(
            str(uuid4()),
            self.account_id,
            datetime.now(timezone.utc),
            "WITHDRAW",
            withdraw_amount,
            new_balance,
            description,
        )

        # Append the transaction history with the transaction
        self._transaction_history.append(transaction)

        return transaction

    def get_transactions(self) -> tuple[Transaction]:
        """
        Returns a copy of the transaction history
        """
        return tuple(self._transaction_history)

    def get_statement(self) -> str:
        lines = "\n".join([f"{t}" for t in self._transaction_history])
        return f"Account: {self.account_id}\nBalance: {self._balance}\nTransactions:\n{lines}"

    def _validate_transaction(self, amount: str) -> None:
        """
        Validate the transaction amount
        """
        self._validate_amount(amount)

        # Positive only and not 0
        if int(amount) <= 0:
            raise InvalidTransactionError(amount)

    def _validate_starting_amount(self, amount: str) -> None:
        """
        Validate the starting amount
        """

        self._validate_amount(amount)

        # Positive or 0 only
        if int(amount) < 0:
            raise InvalidTransactionError(amount)

    @staticmethod
    def _validate_amount(amount: str) -> None:
        """
        Validate amount is a string, not empty, no whitespace, is a string digit, and is not non-ASCII digits
        """
        # Must be a string
        if not isinstance(amount, str):
            raise InvalidTransactionError(amount)

        # Reject empty
        if amount == "":
            raise InvalidTransactionError(amount)

        # Reject any whitespace
        if amount.strip() != amount:
            raise InvalidTransactionError(amount)

        # Reject non-ASCII digits or is not a digit
        if not amount.isascii() or not amount.isdigit():
            raise InvalidTransactionError(amount)


if __name__ == "__main__":
    account = Account(starting_balance="1500")
    account.deposit("3000", "Salary")
    account.withdraw("500", "Groceries")
    stm = account.get_statement()
    print(stm)
