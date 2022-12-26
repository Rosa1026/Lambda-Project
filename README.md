# AWS 기능을 이용한 회의 참석용 QR code 생성 웹페이지
 
#### 클라이언트가 접속하는 웹페이지에서의 기능을 AWS에서 제공하는 Gateway와 Lambda, S3, DynamoDB를 이용해 Serverless 환경에서 구현

## 개발 언어
  - Python
  - Html
  - css
  - js
  
## 개발 플랫폼
  - AWS Lambda
  - API Gateway
  - AWS DynamoDB
  - AWS Cloud Front
  - AWS S3
  - AWS Cloud Watch
  - AWS SNS

## Scenario
![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/%EC%A0%84%EA%B3%B5%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4.png)

## Business Logic 구현
### 1. dynamoDB 생성
### 2. Lambda 함수 생성 (Get, Post)
#### 2-1) Get Lambda
  - 가장 우선적으로 진행한 함수 생성 과정이다.
  - Get Lambda 함수의 경우 event가 발생 시 event에서 user_id와 type을 읽어온 후 앞서 선언한 dynamoDB Table에 읽어온 값이 있는지 확인한다.
  - 확인 후 이에 해당하는 item을 불러와 출력해준다.
  - Get 함수의 경우 발생한 event에 대해서 값을 읽어오는 역할이다.
  - 실제 웹페이지에선 중복 가입 방지 등을 사용하는 역할로 사용되거나, 사용자 정보를 읽어오는 방식 등으로 사용할 수 있다.

#### 2-2) Post Lambda
  - Post Lambda는 발생한 event를 Post 해주는 동작을 수행한다.
  - dynamoDB에 event를 삽입해주고, SNS의 Publisher로써 동작한다.

### 3. SNS 생성 (Post Lambda가 Publisher로 작동)
  - AWS에서 제공하는 SNS란 Simple Notification Service의 준말로 Publisher와 Subscriber를 설정하고, Publisher에서 발행한 정보를 Subscriber에게 알림 메세지를 전송하는 서비스이다.
  - 이는 AWS에서 제공하는 여러 서비스들과 함께 이용할 수 있으며, 이번 프로젝트에서는 Lambda와 연결하여 사용하였다.
  - 앞서 생성한 Post Lambda 함수를 SNS의 Publisher로 설정하여, event가 발생하면 이를 Subscribe한 다른 Lambda에 전송되게끔 설정하였다.
  - 생성한 SNS는 Making Image로 실제로 QR code를 생성해주는 함수를 Subscriber로 설정하여 기능을 구현하였다.

### 4. Lambda 함수 생성 (MakeIMAGE, SNS의 Subscriber)
  - SNS의 Subscriber로 작동할 Lambda 함수이다.
  - Publisher에서 SNS를 통해 발행된 정보는 event의 Records로 전달되므로 Records를 변수에 저장하고 이 변수에서 user_id와 type을 받아 따로 변수를 생성한다.
  - 생성한 변수의 정보를 dynamoDB table에서 받아오고 전화번호, 회사이름, 사용자 이름 정보를 받아온다.
  - makeIMAGE 함수는 실제로 이미지를 만들어주는 함수이기에 Python library인 Pillow와 Qrcode를 사용해주었다.
  - 사용할 logo와 font는 만든 qr code를 저장하기 위해 생성해둔 s3 bucket에서 불러와서 사용해주었고, Pillow와 qr code documents를 참고하여 이미지를 생성한 후 이를 s3 bucket에 저장하였다.

  - 구현을 마친 후 Publisher에서 발생한 event가 qr code화가 되어 s3 bucket에 저장되는지를 확인하였다.
  - 아래 사진은 s3 bucket에 qr code 폴더가 자동으로 생선된 사진이고, 그 안에 생성된 qr code 이미지이다.
![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/s3%20bucket.png)![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/qrcode.jpg)

### 5. Internet Gateway 생성 후 연결
 - gateway 생성
 - 리소스 그룹 생성 후 get 함수 연결
 - POST 함수 연결
 - 올바른 key가 입력이 안 됐을 때 정보가 입력되는 것을 대비한 모델 생성
 - post 요청 본문에 생성한 모델 추가

## Hosting 구현
### 1. Frontend 구현
  - Frontend는 css, js, html 형식으로 구현되어 s3 bucket에 저장하였다.
  - Cloud Front에서 s3 bucket에 저장된 내용을 가져와 Client한테 제공하는 방식을 채택하였다.

### 2. CloudFront 구현

## Hosting Part를 IGW를 이용해 deploy
 -
