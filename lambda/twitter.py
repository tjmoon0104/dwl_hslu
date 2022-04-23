import tweepy
import requests
import base64
from requests.structures import CaseInsensitiveDict
import io
import json

def lambda_handler(event, context):
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
        access_token_secret=access_token_secret
    )

    query = 'gasoline OR gas OR oilprice OR fuelprice OR gasprice OR petrolprice'
    tweets = client.get_recent_tweets_count(query=query,
                                            start_time='2022-04-02T00:00:00.000Z',
                                            end_time='2022-04-03T00:00:00.000Z')
    print(tweets)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
