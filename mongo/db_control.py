from pymongo import MongoClient  # pymongo 임포트

client = MongoClient('localhost', 27017)  # mongoDB라는 27017 포트로 돌아갑니다.
db = client.textcrafters.keywords


def insert(restaurant, category, keyword):
    doc = {'restaurant': restaurant, 'category': category, 'keyword': keyword}
    db.insert_one(doc)


def find_restaurant(restaurant):
    if db.find_one({'restaurant': {'$eq': restaurant}}):
        return True
    else:
        return False
