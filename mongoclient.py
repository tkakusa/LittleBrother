from pymongo import MongoClient
import pprint
client = MongoClient()
db = client.test_database

def insert_data(data):
	
#post = {"author": "Mike", "Date": "Today"}
#post2 = {"author": "Ted", "Date": "Tommorow"}
posts = db.posts
#post_id = posts.insert_one(post).inserted_id
#posts.insert_one(post2).inserted_id
for post in posts.find({"author": "Ted"}):
	print(post)
