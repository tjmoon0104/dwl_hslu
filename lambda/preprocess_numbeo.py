import json
import boto3
import pandas as pd


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'hslu-dwl-numbeo-data2'

    # Price Items
    response = s3.get_object(Bucket=bucket_name, Key='price_items/price_items.json')
    content = response['Body']
    json_object = json.loads(content.read())
    df = pd.DataFrame(json_object['items'])
    df[['item_id', 'name', 'category', 'rent_factor', 'cpi_factor']].to_csv(f'/tmp/price_items.csv', index=False)
    s3.upload_file(f'/tmp/price_items.csv', 'hslu-dwl-data-warehouse', f'price_items/price_items.csv')

    # Historical Country Prices
    files = s3.list_objects_v2(Bucket=bucket_name, Prefix='historical_country_prices').get('Contents')

    for file in files:
        key: str = file['Key']
        country = key.split('/')[1].split('.json')[0]
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body']
        json_object = json.loads(content.read())

        df = pd.DataFrame(json_object['entry'])
        df['country'] = json_object['country']
        df[['country', 'year', 'item_id', 'amount']].to_csv(f'/tmp/{country}.csv', index=False)
        s3.upload_file(f'/tmp/{country}.csv', 'hslu-dwl-data-warehouse', f'historical_country_prices/{country}.csv')

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
