import difflib
from pymongo import MongoClient

def calculate_similarity(keyword1, keyword2):
    answer_bytes = bytes(keyword1, 'utf-8')
    input_bytes = bytes(keyword2, 'utf-8')
    sm = difflib.SequenceMatcher(None, list(answer_bytes), list(input_bytes))
    return sm.ratio()

def integrate_keywords(collection, restaurant, category, keyword1, keyword2):
    # 둘 중 더 짧은 키워드를 저장할 수 있게
    if keyword1 > keyword2:
        result = collection.delete_one({'restaurant': restaurant, 'category': category, 'keyword': keyword1})
        print(f"Deleted keyword1 longer {keyword1}, result: {result.deleted_count}")
    else:
        result = collection.delete_one({'restaurant': restaurant, 'category': category, 'keyword': keyword2})
        print(f"Deleted keyword2 longer {keyword2}, result: {result.deleted_count}")

# MongoDB 연결
client = MongoClient('localhost', 27017)
db = client.textcrafters
collection = db.keywords

# db 내 데이터 'restaurant' tag로 탐색
restaurants = collection.distinct('restaurant')
print(f"Restaurants: {restaurants}")

# Category로 탐색
categories = ['price', 'service', 'taste', 'atmosphere']
similarity_threshold = 0.7

for restaurant in restaurants:
    for category in categories:
        print(f"Processing restaurant: {restaurant}, category: {category}")
        while True:
            keywords = collection.find({'restaurant': restaurant, 'category': category})
            keyword_list = [doc['keyword'] for doc in keywords]
            print(f"Keywords: {keyword_list}")

            integrated = False
            for i, keyword1 in enumerate(keyword_list):
                for keyword2 in keyword_list[i+1:]:
                    similarity = calculate_similarity(keyword1, keyword2)
                    print(f"Similarity between '{keyword1}' and '{keyword2}': {similarity}")
                    if similarity >= similarity_threshold:
                        integrate_keywords(collection, restaurant, category, keyword1, keyword2)
                        integrated = True
                        break

                if integrated:
                    break

            if not integrated:
                break
