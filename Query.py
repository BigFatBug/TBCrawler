# -*- coding: utf8 -*-

import time
from datetime import datetime, timedelta
import calendar
from MongoHandler import MongoHandler


class Query(object):
    def __init__(self):
        self.mongoHandler = MongoHandler()

    def queryStatus(self):
        pass

    # 评论列表
    def queryRates(self, objectId, pageNum):
        while 1:
            try:
                total = self.mongoHandler.getData('info', {'objectId': objectId})['total']
                pageMax = self.mongoHandler.getData('info', {'objectId': objectId})['total']
                indexRange = (total - (pageNum - 1) * 20, total - pageNum * 20)
                rateList = self.mongoHandler.getDatas('comment', {'objectId': objectId,
                                                                  'index': {'$gte': indexRange[1], '$lt': indexRange[0]}})
                break
            except Exception:
                time.sleep(2)
        return {'total': total, 'pageMax': pageMax, 'rateList': rateList}

    # 标签数
    def queryTags(self, objectId):
        while 1:
            try:
                return self.mongoHandler.getData('info', {'objectId': objectId})['tags']
            except Exception:
                time.sleep(2)

    # 评论种类占比
    def queryRateTypeWeight(self, objectId):
        while 1:
            try:
                return self.mongoHandler.getData('info', {'objectId': objectId})['count']
            except Exception:
                time.sleep(2)

    # 前六个月评论比
    def queryLastSixMonth(self, objectId):
        '''
        db.getCollection('comment').aggregate([{'$match': {'commentDate': {'$gte': '2017-01-01', '$lt': '2018-03-01'}}},
                                               {'$group': {'_id': '$rateType', 'count': {'$sum': 1}}}])
        '''
        sMonth = datetime.today()
        bMonth = datetime(sMonth.year, sMonth.month, calendar.monthrange(sMonth.year, sMonth.month)[1]) + timedelta(days=1)
        res = []
        for i in range(6):
            res.append({'month':sMonth.strftime('%Y-%m'), 'res': self.mongoHandler.getAggregate('comment', [
                {'$match': {'objectId': objectId, 'commentDate': {'$gte': sMonth.strftime('%Y-%m'), '$lt': bMonth.strftime('%Y-%m')}}},
                {'$group': {'_id': '$rateType', 'count': {'$sum': 1}}}])})
            bMonth = datetime(sMonth.year, sMonth.month, 1)
            sMonth = bMonth - timedelta(days=1)
        return res

    # 日评论比例曲线
    def queryRateTypeEveryDay(self, objectId):
        today = datetime.today()
        resSum = self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'commentDate': {'$gte': (today - timedelta(days=100)).strftime('%Y-%m-%d'), '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': 'commentDate', 'count': {'$sum': 1}}}])

        good = self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': 1, 'commentDate': {'$gte': (today - timedelta(days=100)).strftime('%Y-%m-%d'), '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': 'commentDate', 'count': {'$sum': 1}}}])

        normal = self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': 0, 'commentDate': {'$gte': (today - timedelta(days=100)).strftime('%Y-%m-%d'), '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': 'commentDate', 'count': {'$sum': 1}}}])

        bad = self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': -1, 'commentDate': {'$gte': (today - timedelta(days=100)).strftime('%Y-%m-%d'), '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': 'commentDate', 'count': {'$sum': 1}}}])
        for i in range(len(resSum)):
            bad[i] = bad[i] / resSum[i]
            normal[i] = normal[i] / resSum[i]
            good[i] = good[i] / resSum[i]

        return {'badList': bad, 'normal': normal, 'good': good}

    # 商品分类比例
    def queryObjectTypeWeight(self, objectId):
        res = []
        sku = self.mongoHandler.getData('info', {'objectId': objectId})['sku']
        for k,v in sku.items():
            res.append({'titleList': v.keys(), 'dataList': v})
        return res

if __name__ == '__main__':
    q = Query()
    print(q.queryLastSixMonth('37900975113'))
