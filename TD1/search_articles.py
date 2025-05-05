from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'blogdumoderateur'
COLLECTION_NAME = 'articles'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def search_articles(query=None):
    if query:
        return list(collection.find({
            "$or": [
                {"titre": {"$regex": query, "$options": "i"}},
                {"resume": {"$regex": query, "$options": "i"}},
                {"auteur": {"$regex": query, "$options": "i"}},
                {"categorie": {"$regex": query, "$options": "i"}},
                {"sous_categorie": {"$regex": query, "$options": "i"}},
            ]
        }).sort("date_publication", -1))
    else:
        return list(collection.find().sort("date_publication", -1))
