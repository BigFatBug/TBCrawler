# coding: utf-8

import json, datetime
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, VARCHAR, Integer, Date, TIMESTAMP, func, text

Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objectId = Column(VARCHAR(32))
    tag = Column(VARCHAR(32))
    comment = Column(VARCHAR(2048))
    commentId = Column(VARCHAR(32))
    rateType = Column(Integer)
    sku = Column(VARCHAR(256))
    commentDate = Column(Date)
    commentTime = Column(TIMESTAMP)
    createTime = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updateTime = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


# from sqlalchemy import create_engine
# engine = create_engine('mysql+mysqldb://root:!23$56@localhost:3306/comment?charset=utf8')
# Base.metadata.create_all(engine)