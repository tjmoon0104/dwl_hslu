import json
import boto3
from numbeopy import NumbeoClient
from iso3166 import countries


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    nb = NumbeoClient()

    for c in countries:
        # country = countries.get('japan').name
        country = c.alpha3

        response = nb.country_prices(country)

        if len(response.keys()) > 0:
            s3.put_object(
                Body=json.dumps(response).encode('UTF-8'),
                Bucket='hslu-dwl-numbeo-data',
                Key=f'country_prices/{country}.json'
            )

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
