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
        worker.start()
        print(time.time() - start)
        return responseData(worker.queryId)
    except Exception as e:
        return responseData(None, -1, str(e))

@app.route('/queryStatus', methods=['GET'])
def queryStatus():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryStatus(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))

@app.route('/queryRates', methods=['GET'])
def queryRates():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        pageNum = request.args.get('pageNum')
        q = Query()
        res = q.queryRates(queryId, int(pageNum))
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryTags', methods=['GET'])
def queryTags():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryTags(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryRateTypeWeight', methods=['GET'])
def queryRateTypeWeight():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryRateTypeWeight(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryLastSixMonth', methods=['GET'])
def queryLastSixMonth():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryLastSixMonth(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))

@app.route('/queryRateTypeEveryDay', methods=['GET'])
def queryRateTypeEveryDay():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryRateTypeEveryDay(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


@app.route('/queryObjectTypeWeight', methods=['GET'])
def queryObjectTypeWeight():
    try:
        queryId = request.args.get('queryId')
        queryId = int(queryId)
        q = Query()
        res = q.queryObjectTypeWeight(queryId)
        return responseData(res)
    except Exception as e:
        return responseData(None, -1, str(e))


if __name__ == '__main__':
    # db.create_all()
    app.run(processes=5)
