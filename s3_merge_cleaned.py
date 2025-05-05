import json
import boto3
import pandas as pd
from io import BytesIO

# === CONFIGURATION ===
BUCKET_NAME = 'kinesis-lambda-s3-bucket1'   # Replace if needed
INPUT_PREFIX = 'weather_data/'              # Folder where JSON files are stored
OUTPUT_KEY = 'cleaned/cleaned_weather_dataset.csv'  # Output path for merged CSV

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    all_records = []

    try:
        # Step 1: List folders
        folders = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=INPUT_PREFIX, Delimiter='/')
        for folder in folders.get('CommonPrefixes', []):
            folder_prefix = folder['Prefix']

            # Step 2: List JSON files inside each folder
            objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_prefix)
            for obj in objects.get('Contents', []):
                key = obj['Key']
                if key.endswith('.json'):
                    try:
                        file = s3.get_object(Bucket=BUCKET_NAME, Key=key)
                        content = file['Body'].read().decode('utf-8')
                        record = json.loads(content)
                        all_records.append(record)
                    except Exception as e:
                        print(f"❌ Skipped invalid JSON in {key}: {str(e)}")

        if not all_records:
            return {
                'statusCode': 400,
                'body': '❌ No JSON data found in S3.'
            }

        # Step 3: Clean and format
        df = pd.DataFrame(all_records)
        df_cleaned = df.dropna(subset=['date', 'station']).copy()
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
        df_cleaned = df_cleaned.sort_values('date')

        # Step 4: Convert to CSV and upload
        csv_buffer = BytesIO()
        df_cleaned.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=BUCKET_NAME, Key=OUTPUT_KEY, Body=csv_buffer.getvalue())

        return {
            'statusCode': 200,
            'body': f"✅ Cleaned CSV uploaded to s3://{BUCKET_NAME}/{OUTPUT_KEY}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"❌ Lambda error: {str(e)}"
        }
