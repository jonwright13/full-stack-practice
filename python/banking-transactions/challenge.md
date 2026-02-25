# Banking Transaction System (Python) — Prompt

## Context

You are implementing a simplified banking ledger. Users have accounts, can deposit and withdraw money, and each operation creates an immutable transaction record. The system must validate inputs, enforce business rules, and raise custom exceptions.

## Your task

Build a small Python package that provides:

- `Account` class
- `Transaction` class
- Two custom exception classes
- A minimal API that supports deposits, withdrawals, balance checks, and transaction history

You must also provide unit tests that validate correct behavior and edge cases.

---

## Functional Requirements

### 1. Money rules

- All monetary values are **float or integers** representing pounds.
- Amounts must be **strictly positive** (`> 0`).
- You must reject invalid amounts (non-float, non-int, bool, <= 0).

### 2. Account

Implement an `Account` class with:

#### Constructor

```python
Account(account_id: str, opening_balance: str = "0")
```

Rules:

- `account_id` must be a non-empty string.
- `opening_balance` must follow money rules (can be `0`).

#### Properties / Methods

- `balance -> float` (current balance)
- `deposit(amount: float, *, description: str = "") -> Transaction`
- `withdraw(amount: float, *, description: str = "") -> Transaction`
- `get_transactions() -> list[Transaction]` (return in chronological order)
- `get_statement() -> str` (human-readable multi-line string)

Business rules:

- Withdrawals must not allow the account to go below `0`.
- Every deposit/withdraw creates exactly **one** `Transaction`.
- Transactions must be recorded **in order**.
- `get_transactions()` must not allow callers to mutate internal state (return a copy or immutable structure).

### 3. Transaction

Implement an immutable `Transaction` model:

Fields (exact names recommended):

- `transaction_id: str` (unique per transaction)
- `account_id: str`
- `type: Literal["DEPOSIT", "WITHDRAW"]`
- `amount: int`
- `timestamp: datetime` (UTC or naive-but-consistent is fine; just be consistent)
- `balance_after: int`
- `description: str`

Rules:

- `amount` must follow money rules
- `balance_after` must be `>= 0`
- `transaction_id` must be unique (use `uuid4()` is fine)

### 4. Custom Exceptions (two classes)

Implement exactly these two exception types:

1. `InvalidTransactionError`
   - Raised when:
     - invalid amount
     - invalid account_id
     - invalid opening balance
     - any other input validation error you choose to route here

2. `InsufficientFundsError`
   - Raised when attempting to withdraw more than the available balance

Exceptions should include meaningful messages (useful for debugging).

---

## Output Requirements

### `get_statement()`

Return a multi-line statement string that looks like:

```Code
Account: ACC123
Balance: 2500
Transactions:
2026-02-24T10:15:30Z  DEPOSIT   3000  balance=3000  Salary
2026-02-24T10:20:00Z  WITHDRAW   500  balance=2500  Groceries
```

Formatting doesn’t have to match exactly, but must include:

- account id
- current balance
- each transaction line includes timestamp, type, amount, and balance_after
- include description if provided

---

## Non-Functional Requirements (the “interview constraints”)

### 1. No print debugging

- Do not use `print()` for debugging.
- Use tests to validate behavior.

### 2. No external libraries

- Only Python standard library (e.g., `dataclasses`, `datetime`, `uuid`, `typing`).
- Add type hints to public methods and classes.

### 4. Immutability

- Transactions should be immutable once created.

### 5. Test coverage

- deposit increases balance + adds transaction
- withdraw decreases balance + adds transaction
- withdraw beyond balance raises `InsufficientFundsError`
- amount validation (0, negative, non-int) raises `InvalidTransactionError`
- opening_balance validation
- `get_transactions()` cannot be used to mutate the stored list
- statement includes key fields

---

## Suggested Project Layout

```Code
python/banking-transactions/
├─ prompt.md
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ __init__.py
│  ├─ account.py
│  ├─ transaction.py
│  └─ errors.py
└─ tests/
   └─ test_banking.py
```

---

## Acceptance Criteria (what “done” means)

You are finished when:

- `pytest` passes
- The API behaves according to rules above
- Exceptions are raised correctly
- Transactions are immutable and correctly recorded
- Repo is clean enough that someone can read the prompt and run the tests
