# coding=utf8
from utils import *
from flask import Flask, request
from Worker import Worker

app = Flask(__name__)
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:!23$56@localhost:3306/tb_crawler?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.debug = True

@app.route('/query', methods=['GET'])
def query():
    try:
        queryId = request.args.get('queryId')
        return responseData(queryId)
    except Exception as e:
        return responseData(None, -1, str(e))

@app.route('/crawler', methods=['GET'])
def crawler():
    try:
        objectUrl = request.args.get('objectUrl')
        queryId = encrypt(objectUrl)
        Worker(objectUrl, queryId).start()
        return responseData(queryId)
    except Exception as e:
        return responseData(None, -1, str(e))

if __name__ == '__main__':
    # db.create_all()
    app.run()
