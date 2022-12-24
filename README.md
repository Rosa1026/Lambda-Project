# AWS Lambda를 이용한 Serverless 환경 만들기 프로젝트
 
#### 클라이언트가 접속하는 웹페이지를 AWS에서 제공하는 Gateway와 Lambda, S3, DynamoDB를 이용해 Serverless 환경 구축

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

<hr/>

## Scenario
![image](https://github.com/Rosa1026/Lambda-Project/blob/main/image/%EC%A0%84%EA%B3%B5%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4.png)

## 1. Lambda 함수 생성 (Get, Post)
# 1-1) Get Lambda
  - 가장 우선적으로 진행한 함수 생성 과정이다.
  - Get Lambda 함수의 경우 event가 발생 시 event에서 user_id와 type을 읽어온 후 앞서 선언한 dynamoDB Table에 읽어온 값이 있는지 확인한다.
  - 확인 후 이에 해당하는 item을 불러와 출력해준다.
  - Get 함수의 경우 발생한 event에 대해서 값을 읽어오는 역할이다.
  - 실제 웹페이지에선 중복 가입 방지 등을 사용하는 역할로 사용되거나, 사용자 정보를 읽어오는 방식 등으로 사용할 수 있다.

# 1-2) Post Lambda
  - Post Lambda는 발생한 event를 Post 해주는 동작을 수행한다.
  - dynamoDB에 event를 삽입해주고, SNS의 Publisher로써 동작한다.

## 2. SNS 생성 (Post Lambda가 Publisher로 작동)

## 3. Lambda 함수 생성 (MakeIMAGE, SNS의 Subscriber)


#### 챗봇

<hr/>


<hr/>

<hr/>

<hr/>

<hr/>

<hr/>

<hr/>
