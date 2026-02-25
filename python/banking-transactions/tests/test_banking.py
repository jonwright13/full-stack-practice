import pytest, dataclasses

from account import Account
from errors import InvalidTransactionError, InsufficientFundsError


def test_create_successful_account():
    """
    Tests the successful creation of an account with a valid amount
    """
    account = Account(starting_balance="3000")
    assert account.balance == 3000

    account = Account(starting_balance="0")
    assert account.balance == 0


def test_creat_invalid_account():
    """
    Tests the creation of an account with an invalid amount (0, non-number, negative) and the raised error
    """
    with pytest.raises(InvalidTransactionError):
        Account(starting_balance="")

    with pytest.raises(InvalidTransactionError):
        Account(starting_balance="ddd")

    with pytest.raises(InvalidTransactionError):
        Account(starting_balance=" 0 ")

    with pytest.raises(InvalidTransactionError):
        Account(starting_balance="-3000")


def test_deposit_with_valid_amount():
    """
    Tests depositing valid amounts into the account, the increase in the balance, and the successful appending of the transaction history
    """
    account = Account(starting_balance="3000")
    account.deposit("500")
    assert account.balance == 3500

    tsx = account.get_transactions()
    assert len(tsx) == 1
    assert tsx[0].amount == 500
    assert tsx[0].transaction_type == "DEPOSIT"
    assert tsx[0].balance_after == 3500

    account.deposit("200")
    assert account.balance == 3700

    tsx = account.get_transactions()
    assert len(tsx) == 2
    assert tsx[1].amount == 200
    assert tsx[1].transaction_type == "DEPOSIT"
    assert tsx[1].balance_after == 3700


def test_deposit_withdraw_with_invalid_amount():
    """
    Tests depositing invalid amounts into the account and the raised error
    """
    account = Account(starting_balance="3000")
    with pytest.raises(InvalidTransactionError):
        account.deposit("")

    with pytest.raises(InvalidTransactionError):
        account.deposit("-500")

    with pytest.raises(InvalidTransactionError):
        account.deposit("1234dd")

    with pytest.raises(InvalidTransactionError):
        account.deposit("0")

    with pytest.raises(InvalidTransactionError):
        account.deposit(" 500")

    # Test with unicode
    with pytest.raises(InvalidTransactionError):
        account.deposit("٠١٢")

    with pytest.raises(InvalidTransactionError):
        account.withdraw("")

    with pytest.raises(InvalidTransactionError):
        account.withdraw("-500")

    with pytest.raises(InvalidTransactionError):
        account.withdraw("1234dd")

    with pytest.raises(InvalidTransactionError):
        account.withdraw("0")

    with pytest.raises(InvalidTransactionError):
        account.withdraw(" 500")


def test_withdraw_with_valid_amount():
    """
    Tests withdrawing valid amounts from the account, the new balances, and the appending of the transaction history
    """
    account = Account(starting_balance="3000")

    # Withdraw some amount with a description
    account.withdraw("500", "Bills")
    assert account.balance == 2500

    # Validate the latests transaction
    tsx = account.get_transactions()
    assert len(tsx) == 1
    assert tsx[0].amount == 500
    assert tsx[0].transaction_type == "WITHDRAW"
    assert tsx[0].description == "Bills"
    assert tsx[0].balance_after == 2500

    # Withdraw some additional amount with a description
    account.withdraw("1000", "Meal")
    assert account.balance == 1500

    # Validate the latest transaction
    tsx = account.get_transactions()
    assert len(tsx) == 2
    assert tsx[1].amount == 1000
    assert tsx[1].transaction_type == "WITHDRAW"
    assert tsx[1].description == "Meal"
    assert tsx[1].balance_after == 1500


def test_insufficient_funds_error():
    """
    Tests withdrawing an insufficient amount from the account
    """
    account = Account(starting_balance="3000")
    with pytest.raises(InsufficientFundsError):
        account.withdraw("3500")
    assert account.balance == 3000
    assert len(account.get_transactions()) == 0


def test_get_transactions_does_not_mutate():
    """
    Tests whether the account balance and transaction history is not mutated by the get_transactions() method
    """

    account = Account(starting_balance="3000")
    account.deposit("500", "Salary")
    account.withdraw("1000", "Groceries")

    assert account.balance == 2500
    assert len(account.get_transactions()) == 2

    # Test whether the returned object returns an error if user tries to mutate it (Tuple)
    tsx = account.get_transactions()
    with pytest.raises(AttributeError):
        tsx.pop()

    with pytest.raises(dataclasses.FrozenInstanceError):
        tsx[0].amount = 999

    assert account.balance == 2500
    assert len(account.get_transactions()) == 2


def test_transaction_history_order():
    account = Account(starting_balance="3000")
    account.deposit("500", "Salary")
    account.withdraw("1000", "Groceries")
    tsx = account.get_transactions()
    assert [t.transaction_type for t in tsx] == ["DEPOSIT", "WITHDRAW"]
