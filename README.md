# TextCrafters_backend
<br><br/>
## http://cscp2.sogang.ac.kr/CSE4187/index.php/%EA%B0%9C%EB%B0%9C%EB%8F%84%EC%83%81%EA%B5%AD
<br><br/>
## Rest API 사용법


### 1. 회원가입 REST API: 
#### URL: http://localhost:8000/api/register/ 
#### METHOD: POST

#### (1) Front-End 서버에서 username, email, password를 담은 json파일을 Back-End 서버로 전송
##### 형식: 
{
  "username": "aaa",
  "email": "aaa100@gmail.com",
  "password": "pbkdf2_sha256$390000$BsNmd9HY3xOTWCji07qvHB$WuYGYbNyMfC4Tybx2AjYG7hbBifwy+1zuqsAjreZ2mc="
}
<br><br/>
#### (2) Back-End 서버에서 Front-End 서버로 회원가입 실패/ 성공 메세지 전송
##### 형식:
{
    "message": "회원가입을 성공적으로 완료하였습니다."
}



<br><br/>
### 2. 로그인 REST API: 
#### URL: http://localhost:8000/api/login/
#### METHOD: POST

#### (1) Front-End 서버에서 email, password 담은 json파일 Back-End 서버로 전송
##### 형식: 
{
    "email": "aaa0@gmail.com",
    "password": "aaa"
}
<br><br/>
#### (2) Back-End 서버에서 리뷰 담은 json파일 Front-End 서버로 전송
##### 형식:
{
    "message": "로그인에 실패/성공하였습니다."
}



<br><br/>
### 3. 키워드 REST API: 
#### URL: http://localhost:8000/api/keywords/
#### METHOD: POST

#### (1) Front-End 서버에서 식당 이름 담은 json파일 Back-End 서버로 전송
##### 형식: 
{
    "restaurant": "현명식탁"
}
<br><br/>
#### (2) Back-End 서버에서 키워드 리스트 담은 json파일 Front-End 서버로 전송
##### 형식:
[
    {
        "category": "price",
        "keywords": [
            {
                "id": 1,
                "label": "점심에 10000원"
            },
            {
                "id": 2,
                "label": "혼밥하기 좋아요"
            }
        ]
    },
    {
        "category": "sevice",
        "keywords": [
            {
                "id": 1,
                "label": "파스타 맵기 조절 가능해요"
            },
            {
                "id": 2,
                "label": "직원들이 친절해요"
            },
            {
                "id": 3,
                "label": "양이 많아요"
            }
        ]
    },
    ...
]



<br><br/>
### 4. 리뷰 REST API: 
#### URL: http://localhost:8000/api/review/
#### METHOD: POST

#### (1) Front-End 서버에서 식당 이름, 키워드들, 리뷰 글자수 담은 json파일을 Back-End 서버로 전송
##### 형식: 
{
    "restaurant": "현명식탁",
    "keywords": ["각자 원하는 정도에 맞춰 굽기 조절하기 좋아요", "맛있어요", "졸업기념 가족식사로 방문했어요", "배려해주셔요"],
    "char_num": "200"
}
<br><br/>
#### (2) Back-End 서버에서 리뷰 담은 json파일 Front-End 서버로 전송
##### 형식:
{
    "review": "현명식탁에서 졸업기념 가족식사로 방문했어요. 정말 맛있어요! 각자 원하는 정도에 맞춰 굽기 조절하기 좋아요. 가족들과 함께 즐거운 시간을 보낼 수 있었습니다. 직원분들도 친절하게 배려해주셔요. 다음에도 기회가 되면 꼭 다시 방문하고 싶어요. 현명식탁을 추천합니다!"
}
<br><br/>
