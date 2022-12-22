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
    
    user_id = event.get('user_id', None)
    type = event.get('type', None)
    
    if user_id == '*':
        response = table.scan()
    else:
        if type:
            q = Key('user_id').eq(user_id) & Key('type').eq(type)
        else:
            q = Key('user_id').eq(user_id)
            
        response = table.query(
            KeyConditionExpression=q
        )
        
    items = response['Items']
    
    print(items)
    return {
        'statusCode': 200,
        'items': items,
        'event': event
    }