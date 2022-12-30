import json
import boto3
import os

def lambda_handler(event, context):
    user_id = event.get('user_id', None)
    type = event.get('type', None)
    
    #dynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    table.put_item(
       Item=event
    )
    
    #SNS
    sns = boto3.resource('sns')
    topic = sns.Topic(os.environ['SNS_ARN'])
    response = topic.publish(
        Message = user_id,
        Subject = type
    )

    return {
        'statusCode': 200,
        'event': event,
        'response':response
    }
