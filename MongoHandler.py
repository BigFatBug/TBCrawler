# coding: utf-8

from copy import deepcopy
from pymongo import MongoClient


class MongoHandler():

    def __init__(self, host='127.0.0.1', port=27017):
        self.client = MongoClient(host=host, port=port)
        self.commentModel = {
            'id': None,
            'objectId': None,
            'tag': None,
            'comment': None,
            'commentId': None,
            'rateType': None,
            'sku': None,
            'commentDate': None,
            'commentTime': None,
            'createTime': None,
            'updateTime': None
        }
        self.statusDic = {}

    def getDb(self, db):
        return self.client.get_database(db)

    def getCollection(self, collection, db='taobao'):
        return self.client.get_database(db).get_collection(collection)

    def update(self, collection_name, key, value,  updateRow):
        collection = self.getCollection(collection_name)
        data = collection.find_one({key: value})
        data.update(updateRow)
        collection.update({key: value}, {'$set': data})

    def updateStatus(self, status, queryId):
        collection = self.getCollection('status')
        data = collection.find_one({'queryId': queryId})
        data['status'] = self.statusDic.get(status)
        collection.update({'queryId': queryId}, {'$set': data})

    def insertComment(self, row):
        collection = self.getCollection('comment')
        data = collection.insert(row)

if __name__ == '__main__':
    pass