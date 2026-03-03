# Lambda S3 Upload Trigger

A TypeScript AWS Lambda that triggers on S3 `PUT` events and returns file metadata.

## What it does

- Triggers on S3 `PUT` event
- Extracts and logs bucket name, object key, file size, and event timestamp
- Returns a structured JSON response with that metadata
- Handles missing metadata gracefully

## Prerequisites

- Node.js 20.x
- AWS CLI configured (`aws configure`)
- IAM role with Lambda execution permissions

## Setup

```bash
npm install
```

Create a `.env` file (see `.env.example`):

```env
AWS_ACCOUNT_ID=123456789
AWS_ROLE=your-role-name
AWS_FUNCTION_NAME=my-function
```

## Scripts

```bash
npm test              # Run locally with mock S3 event
npm run build         # Compile TypeScript to dist/
npm run deploy:create # First time deployment
npm run deploy:update # Subsequent deployments
```

## Project Structure

```Code
├── index.ts          # Lambda handler
├── test-event.ts     # Local test with mock S3 event
├── dist/             # Compiled output (generated)
├── .env              # Environment variables (gitignored)
└── tsconfig.json
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
