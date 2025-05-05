import json
import base64
import boto3
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'kinesis-lambda-s3-bucket1'  # Replace with your actual bucket name

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode and parse the Kinesis record
        payload = base64.b64decode(record['kinesis']['data'])
        weather_data = json.loads(payload)

        # Create a dynamic S3 key (path) for organized storage
        date = weather_data.get('date', 'unknown').split('T')[0]
        datatype = weather_data.get('datatype', 'weather')
        timestamp = str(datetime.now().timestamp())

        s3_key = f"weather_data/{date}/{datatype}_{timestamp}.json"

        # Upload to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(weather_data),
            ContentType='application/json'
        )
        print(f"✅ Stored to S3: {s3_key}")

    return {
        'statusCode': 200,
        'body': 'Data processed and stored in S3'
    }
