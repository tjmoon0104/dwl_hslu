# DWL"Coding Fishes in the Lake"

DWL project for analysis on "How does gasoline price increase influence our daily life"

## Installation

You need [Terraform](https://terraform.io/) & [Docker](https://www.docker.com/) to setup AWS environment

Install according to your operating system

Setup your credentials and use below commands to setup AWS infrastructure

```shell
terraform init
terraform apply
```

## Terraform Codes

All infrastructures are included inside **.tf** files. Files are separated between services lambda, s3, etc.

- lambda.tf: AWS Lambda Function defined, Lambda Layer
- s3.tf: AWS S3 Bucket and access control
- variables.tf: Variables used for setting up AWS infrastructures (region, name, etc)
- main.tf: basic setup and cloudwatch events

## Lambda Functions

All lambda functions are located in directory **lambda**

- get_gasoline_price.py
- get_tweet_lambda.py
- country_prices.py (Numbeo API)
- historical_country_prices.py (Numbeo API)
- ranking_by_country_historical.py (Numbeo API)

## Additional Data

- World Happiness Report Data (world-happines-report-data-cleaning.ipynb)