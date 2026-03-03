import { handler } from "./index";
import { S3Event } from "aws-lambda";

const mockEvent: S3Event = {
  Records: [
    {
      eventTime: "2024-01-15T10:30:00.000Z",
      s3: {
        s3SchemaVersion: "1.0",
        configurationId: "test-config",
        bucket: {
          name: "my-bucket",
          ownerIdentity: { principalId: "" },
          arn: "",
        },
        object: {
          key: "my+file.txt",
          size: 1024,
          eTag: "",
          sequencer: "",
        },
      },
    } as any,
  ],
};

handler(mockEvent).then(console.log).catch(console.error);
