import os
from io import BytesIO
from PIL import Image
import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Check if the event contains 'Records' key
    if 'Records' in event and len(event['Records']) > 0:
        # Get the uploaded image details from the S3 event
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Download the image from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()

        # Resize the image
        img = Image.open(BytesIO(image_data))
        img.thumbnail((200, 200))  # Resize to 200x200 pixels

        # Save the resized image to S3
        destination_bucket = 'imageresized1'  # Replace with your destination bucket name
        resized_key = os.path.splitext(key)[0] + '-resized.jpg'
        with BytesIO() as output:
            img.save(output, format="JPEG")
            output_data = output.getvalue()
            s3.put_object(Bucket=destination_bucket, Key=resized_key, Body=output_data)

        # Send a notification to the SNS topic
        message = f"Image {key} has been resized and uploaded to {destination_bucket}"
        sns_topic_arn = 'arn:aws:sns:us-east-1:475233874405:imageresize'
        sns.publish(TopicArn=sns_topic_arn, Message=message)
        
        
        
        return {
            'statusCode': 200,
            'body': json.dumps('Image resized successfully.')
        }
        
    else:
        print("No records found in the event.")
        return {
            'statusCode': 400,
            'body': json.dumps('No records found in the event.')
        }
