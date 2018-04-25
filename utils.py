# coding=utf8
import json, datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
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


# 转为json
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)     # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:    # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)