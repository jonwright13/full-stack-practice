import { S3Event } from "aws-lambda";

export const handler = async (
  event: S3Event,
): Promise<{
  statusCode: number;
  body: {
    bucket: string;
    key: string;
    fileSize: number;
    timestamp: string;
  };
}> => {
  const record = event.Records[0];
  if (!record) {
    throw new Error("No records found in event");
  }

  const metadata = {
    bucket: record.s3.bucket.name ?? "unknown",
    key: record.s3.object.key
      ? decodeURIComponent(record.s3.object.key.replace(/\+/g, " "))
      : "unknown",
    fileSize: record.s3.object.size ?? null,
    timestamp: record.eventTime ?? null,
  };

  const response = {
    statusCode: 200,
    body: metadata,
  };

  return response;
};
