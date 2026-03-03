import json, requests
from urllib.parse import unquote_plus
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.context import Context


def handler(event: APIGatewayProxyEventV2, context: Context) -> dict:

    record = event["Records"][0]

    if record is None:
        raise AttributeError("Records not found in event")

    metatdata = {
        "bucket": record["s3"]["bucket"]["name"] or "unknown",
        "key": unquote_plus(
            record["s3"]["object"]["key"] or "unknown", encoding="utf-8"
        ),
        "fileSize": record["s3"]["object"]["size"] or None,
        "timestamp": record["eventTime"] or None,
    }

    return {"statusCode": 200, "body": metatdata}
