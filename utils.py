# coding=utf8
import sys
import random, uuid, hashlib, time
from flask import jsonify


def responseData(data, code=0, msg=''):
    res = {}
    res['status'] = code
    res['data'] = data
    res['msg'] = msg
    return jsonify(res)


def encryptUserId(userId):
    r = uuid.uuid4()
    t = time.time()
    return hashlib.md5('{}-{}-{}'.format(r, t, userId)).hexdigest()[8:-8]


duoxuan = {0: '', 1: 'A', 2: 'B', 3: 'AB', 4: 'C', 5: 'AC', 6: 'BC', 7: 'ABC', 8: 'D', 9: 'AD', 10: 'BD', 11: 'ABD', 12: 'CD',
           13: 'ACD', 14: 'BCD', 15: 'ABCD'}

def duoxuanTransfer(numList):
    return [duoxuan[num] for num in numList]
