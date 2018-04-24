# coding=utf8
import uuid, hashlib, time
from flask import jsonify


def responseData(data, code=0, msg=''):
    res = {}
    res['status'] = code
    res['data'] = data
    res['msg'] = msg
    return jsonify(res)


def encrypt(id):
    r = uuid.uuid4()
    t = time.time()
    return hashlib.md5('{}-{}-{}'.format(r, t, id)).hexdigest()[8:-8]
