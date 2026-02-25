class InvalidTransactionError(Exception):
    """
    Exception raised when there is an:
        - Invalid amount
        - Invalid transaction type
    """

    def __init__(self, amount: str):
        self.message = f"Invalid amount: {amount}. Amount should be a valid number cast to a string"
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """
    Exception raised when attempting to withdraw more than the available balance or when account initialised with an invalid opening balance
    """

    def __init__(self, balance: int):
        self.message = f"Insufficient funds available: {balance}"
        super().__init__(self.message)
