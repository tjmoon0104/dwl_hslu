import json
import boto3
from numbeopy import NumbeoClient
from iso3166 import countries


def upload(s3, response, filename, dir):
    if len(response.keys()) >> 0:
        s3.put_object(
            Body=json.dumps(response).encode('UTF-8'),
            Bucket='hslu-dwl-numbeo-data2',
            Key=f'{dir}/{filename}.json'
        )


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    nb = NumbeoClient()

    # Price  Items
    response = nb.price_items()
    upload(s3, response, 'price_items', 'price_items')

    # Rankings by Country Historical
    sections = {
        "1": "Cost_of_Living",
        "2": "Property_Prices",
        "4": "Traffic",
        "7": "Crime",
        "8": "Pollution",
        "12": "Quality_of_Life"
    }

    for key, value in sections.items():
        response = nb.rankings_by_country_historical(key)
        upload(s3, response, value, 'rankings_by_country_historical')

    # Historical Country Prices
    for c in countries:
        country = c.alpha3

        response = nb.historical_country_prices(country=country, currency='USD')
        upload(s3, response, country, 'historical_country_prices')

    return {
        'statusCode': 200,
        'body': json.dumps('Data Stored to S3 Successfully')
    }
