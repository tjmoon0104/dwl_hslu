import pandas as pd
import numpy as np
from datetime import datetime
import boto3
import urllib.request
from bs4 import BeautifulSoup
import json


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    ## Request the URL
    url = "https://tradingeconomics.com/commodities"
    res = urllib.request.urlopen(url)

    ## Read the data into from the url as a string
    html = res.read()

    ## parse with BeautifulSoup
    bs = BeautifulSoup(html, "html.parser")

    ## Choose the first table
    tables = bs.find_all('table')
    table = tables[0]
    rows = table.find_all("tr")
    column_names = []
    header_cells = rows[0].find_all("th")

    for cell in header_cells:
        header = cell.text
        header = header.strip()
        header = header.replace("\n", " ")
        column_names.append(header)

    data = []
    for row in rows[1:]:
        cells = row.find_all("td")

        ## create an empty tuple
        dt = ()
        for cell in cells:
            dp = cell.text

            dp = dp.strip()
            dp = dp.replace("\n", " ")

            ## add to tuple
            dt = dt + (dp,)
        data.append(dt)
    ## Import the data into a dataframe
    df = pd.DataFrame(data, columns=column_names)
    df['Price'] = df['Price'].str.replace(',', '.')
    df['Price'] = df['Price'].astype(np.float64)
    filename = f'price_{datetime.now().strftime("%H%M_%m%d%Y")}.csv'
    df.to_csv(f'/tmp/{filename}')

    s3.upload_file(
        f'/tmp/{filename}',
        'gasoline-price',
        filename
    )

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

