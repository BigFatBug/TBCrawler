# coding=utf8
from utils import *
from flask import Flask, request
from Worker import Worker
from Query import Query

app = Flask(__name__)
app.debug = True

@app.route('/start', methods=['GET'])
def crawler():
    try:
        start = time.time()
        objectUrl = request.args.get('objectUrl')
        worker = Worker(objectUrl)
        worker.run()
        print(time.time() - start)
        return responseData(worker.objectId)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryRates', methods=['GET'])
def queryRates():
    try:
        objectId = request.args.get('objectId')
        pageNum = request.args.get('pageNum')
        q = Query()
        res = q.queryRates(objectId, int(pageNum))
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryTags', methods=['GET'])
def queryTags():
    try:
        objectId = request.args.get('objectId')
        q = Query()
        res = q.queryTags(objectId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryRateTypeWeight', methods=['GET'])
def queryRateTypeWeight():
    try:
        objectId = request.args.get('objectId')
        q = Query()
        res = q.queryRateTypeWeight(objectId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryLastSixMonth', methods=['GET'])
def queryLastSixMonth():
    try:
        objectId = request.args.get('objectId')
        q = Query()
        res = q.queryLastSixMonth(objectId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))

@app.route('/queryRateTypeEveryDay', methods=['GET'])
def queryRateTypeEveryDay():
    try:
        objectId = request.args.get('objectId')
        q = Query()
        res = q.queryRateTypeEveryDay(objectId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryObjectTypeWeight', methods=['GET'])
def queryObjectTypeWeight():
    try:
        objectId = request.args.get('objectId')
        q = Query()
        res = q.queryObjectTypeWeight(objectId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


if __name__ == '__main__':
    # db.create_all()
    app.run(processes=5)
