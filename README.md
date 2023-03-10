# 호텔 예약 Web page 구현
 
#### 프로젝트 목표 : AWS Lambda, dynamoDB 등을 이용해서 Serverless APP을 구현하고 Serverless 환경의 동작 원리를 이해한다.

## 개발 언어
  - Python (Lambda)
  - Html (Frontend)
  - css (Frontend)
  - js (Frontend)
  
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
 - 호텔 예약에 필요한 정보를 저장할 DB를 생성해주었다.
 - user_id와 type(방 번호)를 main key로 받아 구성하였다.
 - dynamoDB는 NoSQL 기반 Database로 스키마가 미리 정의되어있어야하는 RDBS보다 유연하게 데이터를 처리할 수 있다는 장점이 있어 이를 이용하였다.
 - 또한 Serverless 서비스이므로 DB 데이터를 Lambda 함수와 같은 Serverless 서비스와 연결하여 사용이 가능하다는 점 또한 채택 이유이다.

### 2. Lambda 함수 생성 (Get, Post)
#### 2-1) Get Lambda - 현재 예약된 팀 수 확인 기능
 - 가장 우선적으로 생성한 함수이다.
 - Get Lambda 함수의 경우 event가 발생 시 event에서 user_id와 type을 읽어온 후 boto3 api를 이용해 미리 생성한 dynamoDB Table에 읽어온 값이 있는지 확인한다.
 - 확인 후 이에 해당하는 item을 불러와 출력해준다.
 - Get 함수의 경우 발생한 event에 대해서 값을 읽어오는 역할이다.
 - 실제 웹페이지에선 중복 가입 방지 등을 사용하는 역할로 사용되거나, 사용자 정보를 읽어오는 방식 등으로 사용할 수 있다.

#### 2-2) Post Lambda - 새로 예약할 사람 정보 추가
 - Post Lambda는 발생한 event를 Post 해주는 동작을 수행한다.
 - event를 삽입하는 과정에서 미리 정의 스키마를 올바르게 입력해주어야만 db에 삽입되는 반면, dynamoDB는 NoSQL 방식으로 작동하기에 main key만 입력된다면 다른 정보가 포함된 event가 발생 시 그 정보 또한 저장하게 된다.
 - dynamoDB에 event를 삽입해주고, SNS의 Publisher로써 동작한다.

### 3. SNS 생성 (Post Lambda가 Publisher로 작동)
 - AWS에서 제공하는 SNS란 Simple Notification Service의 준말로 Publisher와 Subscriber를 설정하고, Publisher에서 발행한 정보를 Subscriber에게 알림 메세지를 전송하는 서비스이다.
 - 이는 AWS에서 제공하는 여러 서비스들과 함께 이용할 수 있으며, 이번 프로젝트에서는 Lambda와 연결하여 사용하였다.
 - 앞서 생성한 Post Lambda 함수를 SNS의 Publisher로 설정하여, event가 발생하면 이를 Subscribe한 다른 Lambda에 전송되게끔 설정하였다.
 - 생성한 SNS는 Making Image로 실제로 QR code를 생성해주는 함수를 Subscriber로 설정하여 기능을 구현하였다.

### 4. Lambda 함수 생성 (MakeIMAGE, SNS의 Subscriber)
 - SNS의 Subscriber로 작동할 Lambda 함수이다.
 - Publisher에서 SNS를 통해 발행된 정보는 event의 Records로 전달되므로 Records를 변수에 저장하고 이 변수에서 main key인 user_name phone_numbe을 받아 따로 변수를 생성한다.
 - 생성한 변수의 정보를 dynamoDB table에서 받아온다.
 - makeIMAGE 함수는 실제로 이미지를 만들어주는 함수이기에 Python library인 Pillow와 Qrcode를 사용해주었다.
 - Pillow와 Qr code는 Lambda에 기본적으로 등록된 라이브러리가 아니므로 두 기능을 layer로 만들어 추가해서 사용하였다.
 - 사용할 logo와 font는 만든 qr code를 저장하기 위해 생성해둔 s3 bucket에서 불러와서 사용해주었고, Pillow와 qr code documents를 참고하여 이미지를 생성한 후 이를 s3 bucket에 저장하였다.
 - 구현을 마친 후 Publisher에서 발생한 event가 qr code화가 되어 s3 bucket에 저장되는지를 확인하였다.
 - 아래 사진은 s3 bucket에 qr code 폴더가 자동으로 생선된 사진이고, 그 안에 생성된 qr code 이미지이다.
  
![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/s3.png)![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/qr.png)

### 5. Internet Gateway 생성 & Lambda 함수 연결
 - REST API로 설정하여 생성하고 배포를 진행한다.
 - Gateway에 리소스 그룹 생성 후 get 메소드를 생성해서 get 함수와 연결해주고, POST 메소드를 생성하여 POST 함수와 연결한다.
 - 올바른 key가 입력이 안 됐을 때 정보가 입력되는 것을 대비한 모델을 생성해주었다.
 - 앞서 생성한 모델을 Post 메소드의 요청 본문에 모델을 추가한다.

## Hosting 구현
### 1. Frontend 구현
 - Frontend는 css, js, html 형식으로 구현하였다.
#### CSS
 - css는 간단하게 documents를 참조하여 기본적인 스타일 구현
 
#### Html
 - html의 경우 header에서는 css 와 stylesheet를 불러와 사용
 - body는 header class, body class, footer class로 나누어 작업 진행
 - header class는 fixed-tab으로 구현 -> 페이지 탭으로 구분
 - body class는 type은 select, 나머지 정보는 직접 기입으로 설정, start-end date는 달력형태로 설정
 - submit 버튼을 통해 event가 발생하고 이 정보가 IGW를 통해 Lambda 함수로 전달된다.
 - history 탭에선 예약한 사람의 정보를 확인 가능하고, 원하는 사람의 qr code를 print 할 수 있게 설정
 
#### js
 - 발생하는 event 및 함수에 대한 작업을 진행
 - Endpoint와 cf에 s3 버킷 도메인, cloudfront 도메인을 입력
 - 달력 작업 진행 및 document 클릭 시 qr code를 보여주게 설정
 - get 함수와 post 함수의 역할은 ajax 비동기식 call을 사용해 정보를 가져오거나 보내주어 앞서 구현한 기능들이 정상적으로 작동하게 제작

### 2. CloudFront 구현
 - S3의 도메인을 원본 도메인으로 사용하고, index.html을 기본값 루트 객체로 설정한 후 배포한다.

## Front Hosting
 - CORS(Cross-Origin Resource Sharing) 구조로 deploy를 진행하였다.
 - CORS란 웹 페이지 상의 제한된 리소스를 최초 자원이 서비스된 도메인 밖의 다른 도메인으로부터 요청할 수 있게 허용하는 구조이다.
 - 본래 REST 방법을 이용해서 구현하려 하였으나, REST 방법의 경우 browser의 same origin 규칙에 어긋나기에 CORS 방식을 사용하였다.
 - 생성된 S3 bucket을 통해 유저와 연결하기에 S3 bucket의 public access를 활성화 시켜주었다.
 - Dev stage를 생성한 후 dev stage url을 미리 생성한 index.js의 endpoint에 입력하고, 생성한 Cloud Front의 domain name을 CF endpoint에 입력하였다.
 - Frontend 파일이 저장된 s3 bucket에서 인덱스 문서를 index.html로 설정하고, 정적 웹 사이트 호스팅을 활성화시켰다.
 - index.html url을 통해서 접속하면 결과 화면이 나타나는 것을 확인할 수 있다.
 - History를 들어가면 DynamoDB에 저장된 유저의 정보가 나타나므로 Get 동작이 올바르게 작동하는 것을 알 수 있다.
 - Sign Up에서 정보를 입력하고 submit시 qr code가 생성되고 History에 저장되는 것을 보아 Post 동작 또한 올바르게 동작하는 것을 알 수 있다.
