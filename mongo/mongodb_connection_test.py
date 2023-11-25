from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.textcrafters.keywords

doc = {'restaurant':'아건','category':'price','keyword':'가성비가 좋아요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'price','keyword':'가성비가 있어요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'price','keyword':'너무 가성비 뿜뿜해요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'price','keyword':'가성비가 좋은 편이예요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'price','keyword':'가성비가 좋은 것 같아요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'너무 맛있어요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'정말 맛있어요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'맛있게 먹었어요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'너무 맛있었어요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'짱 맛나요'}
db.insert_one(doc)

doc = {'restaurant':'아건','category':'taste','keyword':'짱 맛있었어요'}
db.insert_one(doc)


doc = {'restaurant':'조용한 식탁','category':'service','keyword':'사장님이 친절해요'}
db.insert_one(doc)

doc = {'restaurant':'조용한 식탁','category':'service','keyword':'직원들이 친절해요'}
db.insert_one(doc)

doc = {'restaurant':'조용한 식탁','category':'service','keyword':'사장님이 너무 친절해요'}
db.insert_one(doc)

doc = {'restaurant':'조용한 식탁','category':'service','keyword':'전반적으로 친절해요'}
db.insert_one(doc)

doc = {'restaurant':'조용한 식탁','category':'service','keyword':'외국인 직원이 친절해요'}
db.insert_one(doc)