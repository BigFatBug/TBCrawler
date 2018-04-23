# coding=utf8
import sys

import json, datetime
from flask_sqlalchemy import SQLAlchemy
from utils import *
from flask import Flask, redirect, url_for, request, flash, render_template

app = Flask(__name__)
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:!23$56@localhost:3306/tb_crawler?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.debug = True

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    studyId = db.Column(db.String(32), unique=True)
    studyName = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    loginName = db.Column(db.String(32), nullable=False)
    ctime = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_json(self):
        json_student = {
            'id': self.id,
            'studyId': self.studyId,
            'loginName': self.loginName,
            'studyName': self.studyName,
            'ctime': str(self.ctime)
        }

        return json_student

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/test', methods=['GET'])
def examList():
    return responseData([])

if __name__ == '__main__':
    # db.create_all()
    app.run()
