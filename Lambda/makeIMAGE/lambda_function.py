import json
import boto3
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

def lambda_handler(event, context):
 
    #DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    
    #S3
    s3 = boto3.resource('s3')
    
    #1.SNS subcriber등록 - SNS conferenceTopic에 구독생성(subscriber) 
    #                      make lambda arn등록
    records = event['Records']
    if records : 
        user_id = records[0]['Sns']['Message']
        type = records[0]['Sns']['Subject']
        response = table.get_item(
            Key={
                'user_id': user_id,
                'type': type
            }
        )
        
        item = response['Item']
        phone_number = item.get('phone_number', '')
        start_date = item.get('start_date', '')
        end_date = item.get('end_date', '')
        user_name = item.get('user_name', '')  
        
        #3. image build
        W, H = (400, 250)

        #1) logo img
        s3.Bucket(os.environ['BUCKET_NAME']).download_file('images/logo.png', '/tmp/logo.png')
        s3.Bucket(os.environ['BUCKET_NAME']).download_file('font/Cafe24Classictype.ttf', '/tmp/Cafe24Classictype.ttf')

        logo = Image.open('/tmp/logo.png') #image logo
        otf = '/tmp/Cafe24Classictype.ttf' #f


        #2) qr code img
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )

        qr.add_data(phone_number)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # 3) merge
        img = Image.new('RGB', (W, H), color='#fff')
        img.paste(logo, (200, 0), logo)
        img.paste(qr_img, (15, 100))

        # 4) draw
        font_m = ImageFont.truetype(otf, 15)
        font_b = ImageFont.truetype(otf, 20)
        font_B = ImageFont.truetype(otf, 22)

        draw = ImageDraw.Draw(img)

        draw.text((150, 110), user_name, fill='#000', font=font_b)

        draw.text((150, 140), 'Reserve Hotel', fill='#ed244b', font=font_B)
        draw.text((150, 170), f'{start_date}~{end_date}', fill='#000', font=font_m)

        img.save(f'/tmp/signed.jpg', quality=100)

        key = f'qrcodes/{user_id}/{type}/qrcode.jpg'
        s3.meta.client.upload_file('/tmp/signed.jpg', os.environ['BUCKET_NAME'], key, ExtraArgs={'ContentType':'image/jpeg'})

        #2.DynamoDB에서 key의 사용자 정보 가져오기

    return {
        'statusCode': 200,
        'event':event
    }
