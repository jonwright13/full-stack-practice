# Challenge: S3 Upload Trigger Lambda

Write a Node.js AWS Lambda function that:

1. Triggers on an S3 `PUT` event
2. Extracts and logs the following metadata:
   - Bucket name
   - Object key
   - File size
   - Event timestamp
3. Returns a structured JSON response with that metadata

## Constraints

- Use the event object passed to the handler (no AWS SDK calls needed)
- Handle the case where metadata might be missing gracefully
- Use `async/await`

## Sample S3 Event Object

```json
{
  "Records": [
    {
      "eventTime": "2024-01-15T10:30:00.000Z",
      "s3": {
        "bucket": { "name": "my-bucket" },
        "object": {
          "key": "uploads/photo.jpg",
          "size": 204800
        }
      }
    }
  ]
}
```
