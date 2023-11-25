from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from TextCrafters.settings import MONGO_DB
from collections import defaultdict
import json
@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
        user_collection = MONGO_DB['users']  # user 저장 collection
        # 이미 유저가 등록 되어 있는 경우
        if user_collection.find_one({'email': data['email']}):
            return JsonResponse({'message': 'Email already registered'}, status=400)

        # hashing 후 비번 저장
        hashed_password = make_password(data['password'])
        data['password'] = hashed_password

        user_collection.insert_one(data)
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
        user_collection = MONGO_DB['users']
        user = user_collection.find_one({'email': data['email']})
        if user and check_password(data['password'], user['password']):
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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