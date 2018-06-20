# -*- coding: utf8 -*-

import time
from datetime import datetime, timedelta
import calendar
from MongoHandler import MongoHandler


class Query(object):
    def __init__(self):
        self.mongoHandler = MongoHandler()

    def queryObjectId(self, queryId):
        return self.mongoHandler.getData('status', {'queryId': queryId})['objectId']


    def queryStatus(self, queryId):
        return self.mongoHandler.getData('status', {'queryId': queryId})

    # 评论列表
    def queryRates(self, queryId, pageNum):
        # while 1:
        #     try:
        objectId = self.queryObjectId(queryId)
        total = self.mongoHandler.getData('info', {'objectId': objectId})['total']
        pageMax = self.mongoHandler.getData('info', {'objectId': objectId})['pageMax']
        indexRange = (total - (pageNum - 1) * 20, total - pageNum * 20)
        rateList = self.mongoHandler.getDatas('comment', {'objectId': objectId,
                                                          'index': {'$gte': indexRange[1], '$lt': indexRange[0]}})
        #     break
        # except Exception:
        #     time.sleep(2)
        return {'total': total, 'pageMax': pageMax, 'rateList': rateList}

    # 标签数
    def queryTags(self, queryId):
        while 1:
            try:
                objectId = self.queryObjectId(queryId)
                return self.mongoHandler.getData('info', {'objectId': objectId})['tags']
            except Exception:
                time.sleep(2)

    # 评论种类占比
    def queryRateTypeWeight(self, queryId):
        while 1:
            try:
                objectId = self.queryObjectId(queryId)
                return self.mongoHandler.getData('info', {'objectId': objectId})['count']
            except Exception:
                time.sleep(2)

    # 前六个月评论比
    def queryLastSixMonth(self, queryId):
        '''
        db.getCollection('comment').aggregate([{'$match': {'commentDate': {'$gte': '2017-01-01', '$lt': '2018-03-01'}}},
                                               {'$group': {'_id': '$rateType', 'count': {'$sum': 1}}}])
        '''
        objectId = self.queryObjectId(queryId)
        sMonth = datetime.today()
        bMonth = datetime(sMonth.year, sMonth.month, calendar.monthrange(sMonth.year, sMonth.month)[1]) + timedelta(
            days=1)
        res = {
            'monthList': [],
            'badList': [],
            'goodList': [],
            'normalList': []
        }
        xxx = []
        for i in range(6):
            xxx.append({'month': sMonth.strftime('%Y-%m'), 'res': self.mongoHandler.getAggregate('comment', [
                {'$match': {'objectId': objectId,
                            'commentDate': {'$gte': sMonth.strftime('%Y-%m'), '$lt': bMonth.strftime('%Y-%m')}}},
                {'$group': {'_id': '$rateType', 'count': {'$sum': 1}}}])})
            bMonth = datetime(sMonth.year, sMonth.month, 1)
            sMonth = bMonth - timedelta(days=1)
        for x in xxx:
            res['monthList'].append(x['month'])
            a, b, c = 0, 0, 0
            for _ in x['res']:
                if _['_id'] == '-1':
                    a = _['count']
                if _['_id'] == '0':
                    b = _['count']
                if _['_id'] == '1':
                    c = _['count']

            res['badList'].append(a)
            res['normalList'].append(b)
            res['goodList'].append(c)
        return res

    # 日评论比例曲线
    def queryRateTypeEveryDay(self, queryId):
        today = datetime.today()
        objectId = self.queryObjectId(queryId)
        res = {
            'dayList': [],
            'badList': [],
            'goodList': [],
            'normalList': []
        }
        resSum = {x['_id']: x['count'] for x in self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'commentDate': {'$gte': (today - timedelta(days=99)).strftime('%Y-%m-%d'),
                                                              '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': '$commentDate', 'count': {'$sum': 1}}}])}

        good = {x['_id']: x['count'] for x in self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': '1',
                        'commentDate': {'$gte': (today - timedelta(days=99)).strftime('%Y-%m-%d'),
                                        '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': '$commentDate', 'count': {'$sum': 1}}}])}

        normal = {x['_id']: x['count'] for x in self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': '0',
                        'commentDate': {'$gte': (today - timedelta(days=99)).strftime('%Y-%m-%d'),
                                        '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': '$commentDate', 'count': {'$sum': 1}}}])}

        bad = {x['_id']: x['count'] for x in self.mongoHandler.getAggregate('comment', [
            {'$match': {'objectId': objectId, 'rateType': '-1',
                        'commentDate': {'$gte': (today - timedelta(days=99)).strftime('%Y-%m-%d'),
                                        '$lte': today.strftime('%Y-%m-%d')}}},
            {'$group': {'_id': '$commentDate', 'count': {'$sum': 1}}}])}

        for i in range(99, -1, -1):
            d = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            res['dayList'].append(d)
            if not resSum.get(d):
                res['goodList'].append(0)
                res['badList'].append(0)
                res['normalList'].append(0)
            else:
                res['goodList'].append(good.get(d, 0) / resSum[d])
                res['normalList'].append(normal.get(d, 0) / resSum[d])
                res['badList'].append(bad.get(d, 0) / resSum[d])

        return res

    # 商品分类比例
    def queryObjectTypeWeight(self, queryId):
        objectId = self.queryObjectId(queryId)
        res = []
        sku = self.mongoHandler.getData('info', {'objectId': objectId})['sku']
        for k, v in sku.items():
            res.append({'name': k, 'titleList': list(v.keys()), 'dataList': v})
        return res


if __name__ == '__main__':
    q = Query()
    print(q.queryLastSixMonth('37900975113'))
