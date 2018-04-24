# -*- coding: utf8 -*-
from RedisClient import RedisClient


class Query(object):
    def __init__(self, queryId):
        self.queryId = queryId
        self.redisClient = RedisClient()
        self.redisClient.connect()

    def queryStatus(self):
        return self.redisClient.getValue(self.queryId, 'status')


if __name__ == '__main__':
    pass
