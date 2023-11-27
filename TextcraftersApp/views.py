from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from TextCrafters.settings import MONGO_DB
from collections import defaultdict
import json
import openai


'''
==== 회원가입 REST API: URL: http://localhost:8000/api/register/ ====

1. Front-End 서버에서 username, email, password를 담은 json파일을 Back-End 서버로 전송
형식: 
{
  "username": "최이정",
  "email": "ejeong100@gmail.com",
  "password": "pbkdf2_sha256$390000$BsNmd9HY3xOTWCji07qvHB$WuYGYbNyMfC4Tybx2AjYG7hbBifwy+1zuqsAjreZ2mc="
}

2. Back-End 서버에서 Front-End 서버로 회원가입 실패/ 성공 메세지 전송
형식:
{
    "message": "회원가입을 성공적으로 완료하였습니다."
}
'''
@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
        user_collection = MONGO_DB['users']  # user 저장 collection
        # 이미 유저가 등록 되어 있는 경우
        if user_collection.find_one({'email': data['email']}):
            return JsonResponse({'message': '이미 가입된 회원입니다.'}, status=400)

        # hashing 후 비번 저장
        hashed_password = make_password(data['password'])
        data['password'] = hashed_password

        user_collection.insert_one(data)
        return JsonResponse({'message': '회원가입을 성공적으로 완료하였습니다.'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



'''
==== 로그인 REST API: URL: http://localhost:8000/api/login/ ====

1. Front-End 서버에서 email, password 담은 json파일 Back-End 서버로 전송
형식: 
{
    "email": "ejeong100@gmail.com",
    "password": "ejeong"
}

2. Back-End 서버에서 리뷰 담은 json파일 Front-End 서버로 전송
형식:
{
    "message": "로그인에 실패/성공하였습니다."
}
'''
@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
        user_collection = MONGO_DB['users']
        user = user_collection.find_one({'email': data['email']})
        if user and check_password(data['password'], user['password']):
            return JsonResponse({'message': '로그인에 성공하였습니다.'}, status=200)
        else:
            return JsonResponse({'message': '로그인에 실패하였습니다.'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


'''
==== 키워드 REST API: URL: http://localhost:8000/api/keywords/ ====

1. Front-End 서버에서 식당 이름 담은 json파일 Back-End 서버로 전송
형식: 
{
    "restaurant": "현명식탁"
}

2. Back-End 서버에서 키워드 리스트 담은 json파일 Front-End 서버로 전송
형식:
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
'''
@csrf_exempt
@require_http_methods(['POST'])
def get_keywords(request):
    try:
        data = json.loads(request.body)
        restaurant_name = data.get('restaurant')

        keywords_collection = MONGO_DB['keywords']
        keywords_docs = keywords_collection.find({'restaurant': restaurant_name})

        # 카테고리 별로 키워드 묶기
        category_keywords = defaultdict(list)
        for doc in keywords_docs:
            category_keywords[doc['category']].append(doc['keyword'])

        # frontend 서버에 전송하기 위한 폼으로 수정
        formatted_keywords = []
        for category, keywords in category_keywords.items():
            formatted_category = {
                'category': category,
                'keywords': [{'id': index + 1, 'label': keyword} for index, keyword in enumerate(keywords)]
            }
            formatted_keywords.append(formatted_category)

        return JsonResponse(formatted_keywords, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




openai.api_key = "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"

'''
==== 리뷰 REST API: URL: http://localhost:8000/api/review/ ====

1. Front-End 서버에서 식당 이름, 키워드들, 리뷰 글자수 담은 json파일을 Back-End 서버로 전송
형식: 
{
    "restaurant": "현명식탁",
    "keywords": ["각자 원하는 정도에 맞춰 굽기 조절하기 좋아요", "맛있어요", "졸업기념 가족식사로 방문했어요", "배려해주셔요"],
    "char_num": "200"
}

2. Back-End 서버에서 리뷰 담은 json파일 Front-End 서버로 전송
형식:
{
    "review": "현명식탁에서 졸업기념 가족식사로 방문했어요. 정말 맛있어요! 각자 원하는 정도에 맞춰 굽기 조절하기 좋아요. 가족들과 함께 즐거운 시간을 보낼 수 있었습니다. 직원분들도 친절하게 배려해주셔요. 다음에도 기회가 되면 꼭 다시 방문하고 싶어요. 현명식탁을 추천합니다!"
}
'''
@csrf_exempt
@require_http_methods(['POST'])
def generate_review(request):
    try:
        data = json.loads(request.body)

        # Front-End에서 restaurant 이름, keyword array, 글자수 전송
        restaurant_name = data.get('restaurant', 'Restaurant')
        keyword_string = ', '.join(data.get('keywords', []))
        char_num = data.get('char_num', "200")  # 글자수 입력 안하는 경우 default 200

        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            temperature=0,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": "You are a helpful assistant in "
                                              "writing automated reviews for restaurants, "
                                              "with given keywords and instructions."},
                {"role": "user", "content": "Create me a restaurant review for '%s' restaurant, "
                                            "that includes '%s' keywords in Korean. "
                                            "Do not include additional information that are not mentioned."
                                            "The restaurant review must be minimum %s characters (in Korean)."
                                            % (restaurant_name, keyword_string, char_num)}
            ],
        )

        review_content = response["choices"][0]["message"]["content"]
        return JsonResponse({'review': review_content}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
