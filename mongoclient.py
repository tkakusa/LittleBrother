from pymongo import MongoClient
client = MongoClient()

db = client.test_database
post = {"author": "Mike"}
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)
