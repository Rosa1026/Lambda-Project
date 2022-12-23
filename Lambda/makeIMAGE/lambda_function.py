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
    
        #2.DynamoDB에서 key의 사용자 정보 가져오기
        response = table.get_item(
            Key={
                'user_id': user_id,
                'type': type
            }
        )
        item = response['Item']
        phone_number = item.get('phone_number', '')
        company_name = item.get('company_name', '')
        user_name = item.get('user_name', '')  
        
        #3. image build
        W, H = (400, 250)

        # 3-1) logo img
        s3.download_file(os.environ['BUCKET_NAME'], 'fonts/font.otf', '/tmp/font.otf')
        s3.download_file(os.environ['BUCKET_NAME'], 'images/logo.png', '/tmp/logo.png')

        logo = Image.open('/tmp/logo.png') #image logo
        otf = '/tmp/font.otf' #font

        # 3-2) qr code img
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )

        qr.add_data(phone_number)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # 3-3) merge
        img = Image.new('RGB', (W, H), color='#fff')
        img.paste(logo, (15, 15), logo)
        img.paste(qr_img, (15, 100))

        # 3-4) draw
        font_m = ImageFont.truetype(otf, 15)
        font_b = ImageFont.truetype(otf, 20)
        font_B = ImageFont.truetype(otf, 22)

        draw = ImageDraw.Draw(img)

        draw.text((150, 110), user_name, fill='#000', font=font_b)
        draw.text((150, 140), f'From {company_name}', fill='#000', font=font_m)

        draw.rectangle((145, 170, 375, 205), fill='#f0f0f0')
        draw.text((150, 170), 'CONFERENCE PASS', fill='#ed244b', font=font_B)

        img.save(f'/tmp/signed.jpg', quality=100)

        key = f'qrcodes/{user_id}/{type}/qrcode.jpg'
        s3.meta.client.upload_file('/tmp/signed.jpg', os.environ['BUCKET_NAME'], key, ExtraArgs={'ContentType':'image/jpeg'})

    return {
        'statusCode': 200,
        'event': event,
 
    }