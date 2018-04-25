# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MysqlClient():

    def __init__(self):
        self.engine = create_engine('mysql+mysqldb://root:!23$56@localhost:3306/comment?charset=utf8')
        self.Dsession = sessionmaker(bind=self.engine)
        self.session = self.Dsession()

    def getSession(self):
        return self.session


if __name__ == '__main__':
    m = MysqlClient()
    from Model import *

    comment = Comment()
    comment.objectId = '2'
    m.session.query(Comment).filter(Comment.id == 1).update({Comment.commentId: '3'})
    m.session.commit()
