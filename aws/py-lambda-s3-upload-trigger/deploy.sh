#!/bin/bash

# Load .env
export $(cat .env | xargs)

zip -r function.zip src/ 

if [ "$1" = "create" ]; then
  aws lambda create-function \
    --function-name $AWS_FUNCTION_NAME \
    --runtime python3.12 \
    --role arn:aws:iam::$AWS_ACCOUNT_ID:role/$AWS_ROLE \
    --handler src/main.handler \
    --zip-file fileb://function.zip
else
  aws lambda update-function-code \
    --function-name $AWS_FUNCTION_NAME \
    --zip-file fileb://function.zip
fi