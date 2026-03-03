# Lambda S3 Upload Trigger — Python

A Python AWS Lambda that triggers on S3 `PUT` events and returns file metadata.

## What it does

- Triggers on S3 `PUT` event
- Extracts and logs bucket name, object key, file size, and event timestamp
- Returns a structured JSON response with that metadata
- Handles missing metadata gracefully

## Prerequisites

- Python 3.12
- AWS CLI configured (`aws configure`)
- IAM role with Lambda execution permissions

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```env
AWS_ACCOUNT_ID=123456789
AWS_ROLE=your-role-name
AWS_FUNCTION_NAME=my-function
```

## Scripts

```bash
pytest                  # Run tests
bash deploy.sh create   # first time
bash deploy.sh update   # subsequent
```

## Project Structure

```Code
├── src/
│   └── main.py           # Lambda handler
├── tests/
│   └── test_handler.py   # Pytest tests
├── pytest.ini            # Pytest configuration
├── deploy.sh             # Deployment script
├── prompt.md             # Challenge description
├── .env                  # Environment variables (gitignored)
└── requirements.txt
```

## Response

```json
{
  "statusCode": 200,
  "body": {
    "bucket": "my-bucket",
    "key": "my-file.txt",
    "fileSize": 1024,
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```
