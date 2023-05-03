import json
import os
import requests

GITHUB_CLIENT_ID_PROD = "5f5bbe0c2623f5a7e738"
GITHUB_CLIENT_ID_DEV = "244bf05034e7cf9158cc" 

GITHUB_CLIENT_SECRET_DEV = os.environ["GITHUB_CLIENT_SECRET_DEV"]
GITHUB_CLIENT_SECRET_PROD = os.environ["GITHUB_CLIENT_SECRET_PROD"]


def lambda_handler(event, context):
    if event["httpMethod"] == "OPTIONS":
        return handle_cors_options()

    client_id = event["queryStringParameters"]["client"]
    authorization_code = event["queryStringParameters"]["code"]
    if authorization_code is None:
      return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        },
        "body": json.dumps({"error": "Invalid authorization code"})
      }

    client_secret = None
    if client_id == GITHUB_CLIENT_ID_DEV:
      client_secret = GITHUB_CLIENT_SECRET_DEV
    elif client_id == GITHUB_CLIENT_ID_PROD:
      client_secret = GITHUB_CLIENT_SECRET_PROD

    if client_secret is None:
      return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        },
        "body": json.dumps({"error": "Invalid client id"})
      }

    # Exchange the authorization code for an access token
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
        },
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        },
        "body": json.dumps(response.json()) 
    }


def handle_cors_options():
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        },
    }