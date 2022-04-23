import json
import boto3
from numbeopy import NumbeoClient


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    nb = NumbeoClient()

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

        if len(response.keys()) > 0:
            s3.put_object(
                Body=json.dumps(response).encode('UTF-8'),
                Bucket='hslu-dwl-numbeo-data',
                Key=f'rankings_by_country_historical/{value}.json'
            )

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
