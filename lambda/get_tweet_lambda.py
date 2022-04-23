import base64
import requests
import json
import boto3
import datetime
import os
import tweepy
from requests.structures import CaseInsensitiveDict
from datetime import datetime


def lambda_handler(event, context):
    # API credentials
    with open('twitter.json') as f:
        credentials = json.load(f)

    # Credentials
    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    access_token = credentials["access_token"]
    access_token_secret = credentials["access_token_secret"]

    url = "https://api.twitter.com/oauth2/token"

    key = f"{consumer_key}:{consumer_secret}".encode("ascii")
    apikey_base64 = base64.b64encode(key).decode()

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = f"Basic {apikey_base64}"
    data = "grant_type=client_credentials"

    resp = requests.post(url, headers=headers, data=data).json()
    bearer_token = resp['access_token']

    # Tweeter Client
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret)

    query = 'gasoline OR gas OR oilprice OR fuelprice OR gasprice OR petrolprice'

    tweets = client.get_recent_tweets_count(
        query=query,
        granularity='day')

    s3 = boto3.client('s3')

    s3.put_object(
        Body=json.dumps(tweets.data).encode('UTF-8'),
        Bucket='tweet-count',
        Key=f'tweet_count_{datetime.now().strftime("%H%M_%m%d%Y")}.json'
    )

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

