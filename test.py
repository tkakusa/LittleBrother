from pymongo import MongoClient

client = MongoClient()
db1 = client.host1
db2 = client.host2

#db1.posts.delete_many({})
posts1 = db1.posts
posts2 = db2.posts


for post in posts1.find():
    print(post)
