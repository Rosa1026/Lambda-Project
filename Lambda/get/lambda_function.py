import json
import boto3
import os
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    # DynamoDB conference table list return
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    # Get the dynamoDB table
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    
    user_name = event.get('user_name', None)
    phone_number = event.get('phone_number', None)
    
    if user_name == '*':
        response = table.scan()
    else:
        if type:
            q = Key('user_name').eq(user_name) & Key('phone_number').eq(phone_number)
        else:
            q = Key('user_name').eq(user_name)
            
        response = table.query(
            KeyConditionExpression=q
        )
        
    items = response['Items']
    
    return {
        'statusCode': 200,
        'items': items,
        'event': event
    }