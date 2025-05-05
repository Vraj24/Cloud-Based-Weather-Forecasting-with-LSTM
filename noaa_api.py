import json
import boto3
import requests
import os
from datetime import datetime

# Environment variables (set these in Lambda console or Terraform)
API_TOKEN = os.environ.get("NOAA_API_TOKEN")
REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")
STREAM_NAME = os.environ.get("KINESIS_STREAM_NAME", "weather-stream")

# NOAA API
API_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
HEADERS = {'token': API_TOKEN}

def lambda_handler(event, context):
    #date_str = datetime.utcnow().strftime("%Y-%m-%d")
    date_str = "2025-04-01"

    params = {
        'datasetid': 'GHCND',
        'stationid': 'GHCND:USW00023234',
        'startdate': date_str,
        'enddate': date_str,
        'limit': 1000,
        'units': 'standard'
    }

    try:
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            raise Exception(f"NOAA error {response.status_code}: {response.text}")

        results = response.json().get("results", [])
        if not results:
            raise Exception("No data returned from NOAA.")

        record = {'date': results[0]['date'], 'station': results[0]['station']}
        for entry in results:
            record[entry['datatype']] = entry['value']

        # Send to Kinesis
        kinesis = boto3.client('kinesis', region_name=REGION_NAME)
        kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(record),
            PartitionKey="weather-data"
        )

        return {
            'statusCode': 200,
            'body': f"✅ Successfully sent weather data for {record['date']}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"❌ Lambda error: {str(e)}"
        }
