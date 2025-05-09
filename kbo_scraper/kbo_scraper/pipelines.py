import pymongo

class MongoPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get("MONGO_URI"))
        self.db = self.client[spider.settings.get("MONGO_DATABASE")]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one({'numero_entreprise': item['numero_entreprise']}, {'$set': dict(item)}, upsert=True)
        return item
