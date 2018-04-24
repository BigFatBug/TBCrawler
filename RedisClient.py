# -*- coding: utf8 -*-

import redis


class RedisClient(object):

    def __init__(self, host='127.0.0.1', port=6379):
        self.host = host
        self.port = port
        # self.r = None

    def connect(self):
        self.r = redis.StrictRedis(host=self.host, port=self.port)

    def getValue(self, queryId, key):
        return self.r.hget(queryId, key)

    def setValue(self, queryId, key, value):
        self.r.hset(queryId, key, value)

    def firstQuery(self, objectId, queryId):
        self.setValue(queryId, 'objectId', objectId)



if __name__ == '__main__':
    pass