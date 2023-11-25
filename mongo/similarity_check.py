import difflib
from pymongo import MongoClient

def calculate_similarity(keyword1, keyword2):
    answer_bytes = bytes(keyword1, 'utf-8')
    input_bytes = bytes(keyword2, 'utf-8')
    sm = difflib.SequenceMatcher(None, list(answer_bytes), list(input_bytes))
    return sm.ratio()

def integrate_keywords(collection, restaurant, category, keyword1, keyword2):
    # Keep keyword1 and delete keyword2
    result = collection.delete_one({'restaurant': restaurant, 'category': category, 'keyword': keyword2})
    print(f"Deleted {keyword2}, result: {result.deleted_count}")
#
# # Connect to MongoDB
# client = MongoClient('localhost', 27017)
# db = client.textcrafters
# collection = db.keywords
#
# # Fetch unique restaurants
# restaurants = collection.distinct('restaurant')
# print(f"Restaurants: {restaurants}")
#
# # Categories to process
# categories = ['price', 'service', 'taste', 'atmosphere']
# similarity_threshold = 0.7
#
# for restaurant in restaurants:
#     for category in categories:
#         print(f"Processing restaurant: {restaurant}, category: {category}")
#         while True:
#             keywords = collection.find({'restaurant': restaurant, 'category': category})
#             keyword_list = [doc['keyword'] for doc in keywords]
#             print(f"Keywords: {keyword_list}")
#
#             integrated = False
#             for i, keyword1 in enumerate(keyword_list):
#                 for keyword2 in keyword_list[i+1:]:
#                     similarity = calculate_similarity(keyword1, keyword2)
#                     print(f"Similarity between '{keyword1}' and '{keyword2}': {similarity}")
#                     if similarity >= similarity_threshold:
#                         integrate_keywords(collection, restaurant, category, keyword1, keyword2)
#                         integrated = True
#                         break
#
#                 if integrated:
#                     break
#
#             if not integrated:
#                 break
