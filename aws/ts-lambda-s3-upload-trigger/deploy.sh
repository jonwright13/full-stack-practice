#!/bin/bash
zip -r function.zip dist/index.js node_modules

if [ "$1" = "create" ]; then
  aws lambda create-function \
    --function-name $AWS_FUNCTION_NAME \
    --runtime nodejs20.x \
    --role arn:aws:iam::$AWS_ACCOUNT_ID:role/$AWS_ROLE \
    --handler index.handler \
    --zip-file fileb://function.zip
else
  aws lambda update-function-code \
    --function-name $AWS_FUNCTION_NAME \
    --zip-file fileb://function.zip
fi