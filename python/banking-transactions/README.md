# Banking Transaction System (Python)

A small, interview-style banking ledger system implemented in Python.

This project simulates:

- Account creation with validated starting balance
- Deposits and withdrawals
- Immutable transaction records
- Strict input validation
- Custom exception handling
- Unit testing with pytest
- Reproducible execution via Docker

## Design Overview

### Account

The Account class is responsible for:

- Maintaining account balance
- Validating transaction inputs
- Enforcing business rules (e.g., no overdrafts)
- Creating immutable Transaction records
- Maintaining transaction history

The account exposes:

- balance (read-only property)
- deposit(amount, description)
- withdraw(amount, description)
- get_transactions()
- get_statement()

### Transaction

Transactions are implemented as:

```Python
@dataclass(frozen=True, slots=True)
```

This ensures:

- Immutability (cannot modify transaction fields after creation)
- Memory efficiency via slots
- Clear separation between domain state and historical record

Each transaction contains:

- transaction_id
- account_id
- timestamp (UTC)
- transaction_type `("DEPOSIT" | "WITHDRAW")`
- amount
- balance_after
- description

### Validation Rules

Amounts must:

- Be a string
- Contain only ASCII digits (0-9)
- Have no leading or trailing whitespace
- Be strictly positive for transactions
- Be zero or positive for starting balance
- Unicode digits (e.g. "٠١٢") are rejected.

### Error Handling

Custom exceptions:

- `InvalidTransactionError`
  Raised for invalid input amounts

- `InsufficientFundsError`
  Raised when withdrawal would cause negative balance

## Project Structure

```text
banking-transactions/
│
├── account.py
├── transaction.py
├── errors.py
├── tests/
│ └── test_banking.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Running Tests Locally

Create a virtual environment:

```Bash
python -m venv .venv
source .venv/bin/activate # Windows CMD: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## Running with Docker

Build the image:

```Bash
docker build -t banking-transactions .
```

Run tests inside container:

```Bash
docker run --rm banking-transactions
```

## Example Usage

```Python
from account import Account

account = Account(starting_balance="1500")
account.deposit("3000", "Salary")
account.withdraw("500", "Groceries")

print(account.get_statement())
```

## Example output

```Code
Account: 4f2c3c5b-...
Balance: 4000
Transactions:
2026-02-25 12:00:00+00:00 | Type: DEPOSIT | 3000 | Balance=4500 | Salary
2026-02-25 12:01:00+00:00 | Type: WITHDRAW | 500 | Balance=4000 | Groceries
```

## Design Decisions

### Why integers for money?

Money is stored as integers to avoid floating point precision issues.

### Why immutable transactions?

Transactions represent historical events and should not be modified after creation.

### Why strict ASCII validation?

To prevent unexpected Unicode numeric characters and enforce predictable input format.

## Improvements / Extensions (Future Work)

- Introduce multi-account transfers
- Add persistent storage layer
- Add API layer (FastAPI)
- Add CI pipeline for automated test execution
- Support currency subunits (e.g., cents) explicitly
