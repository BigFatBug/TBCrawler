# coding: utf-8

from datetime import datetime
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

    def getCommentSize(self, objectId):
        return self.getCollection('comment').count({'objectId': objectId})

    def getData(self, collectionName, filterRow):
        return self.getCollection(collectionName).find_one(filterRow)

    def getDatas(self, collectionName, filterRow):
        return list(self.getCollection(collectionName).find(filterRow))

    def getMaxIndex(self):
        return self.getCollection('comment').find().sort({'index': -1}).limit(1)

    def getAggregate(self, collectionName, filterRow):
        return list(self.getCollection(collectionName).aggregate(filterRow))

    def update(self, collectionName, key, value,  updateRow):
        collection = self.getCollection(collectionName)
        data = collection.find_one({key: value})
        if not data:
            data = updateRow
            data[key] = value
            data['createTime'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            data['updateTime'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            collection.insert(data)
        else:
            data.update(updateRow)
            data['updateTime'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
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