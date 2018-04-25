# -*- coding: utf8 -*-
from RedisClient import RedisClient
from MysqlClient import MysqlClient


class Query(object):
    def __init__(self, queryId):
        self.queryId = queryId
        self.redisClient = RedisClient()
        self.redisClient.connect()
        self.session = MysqlClient().getSession()

    def queryStatus(self):
        return self.redisClient.getValue(self.queryId, 'status')

    # 评论列表
    def queryRates(self):
        pass

    # 标签数
    def queryTagsCount(self):
        pass

    # 评论种类占比
    def queryRateTypeWeight(self):
        pass

    # 前六个月评论比
    def queryLastSixMonth(self):
        pass

    # 日评论比例曲线
    def queryRateTypeEveryDay(self):
        pass

    # 商品分类比例
    def queryObjectTypeWeight(self):
        pass

if __name__ == '__main__':
    pass
