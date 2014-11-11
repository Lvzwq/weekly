# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.db import MYSQL_HOST, MYSQL_USER, MYSQL_DB, MYSQL_CHARSET, MYSQL_PASSWORD

# 安装的扩展库sqlalchemy

# conn='mysql://root:root@localhost/newscenter?charset=utf8'
conn = 'mysql://%s:%s@%s/%s?charset=%s' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_CHARSET)
engine = create_engine(conn,echo =True)
Base = declarative_base(engine)



class Area(Base):
    __tablename__ = 'area'
    __table_args__ = {'autoload': True}
    id = Column(SmallInteger, primary_key=True)
    page_id = Column(Integer)
    paper_id = Column(Integer)
    article_id = Column(Integer)
    x = Column(String(11))
    y = Column(String(11))
    width = Column(String(11))
    height = Column(String(11))


class Article(Base):
    __tablename__ = 'article'
    __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True)
    title = Column(String(11))
    sub_title = Column(String)
    content = Column(Text)
    time = Column(DateTime)
    paper_id = Column(Integer)
    page_id = Column(Integer)
    reply_title = Column(String)
    author = Column(String(64))
    keyword = Column(String)
    show_author = Column(Integer)
    has_pic = Column(Integer)


class Keyinfo(Base):
    __tablename__ = 'keyinfo'
    __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    article_id = Column(Integer)


class Paper(Base):
    __tablename__ = 'paper'
    __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True)
    num = Column(Integer)
    issued = Column(Integer)
    time = Column(DateTime)


class Model():
    def __init__(self):
        # moz_article = Table('article', metadata, autoload=True)
        # mapper(Article, moz_article)
        metadata = MetaData(engine)
        session = sessionmaker(bind=engine)
        self.session = session()


    def get_article_list(self, paper_id):
        article_list = self.session.query(Article.id, Article.title, Article.reply_title, Article.has_pic,
                                          Article.sub_title)
        article_list = article_list.filter(Article.paper_id == paper_id)
        article_list = article_list.all()
        return article_list


    def get_all_paper(self):
        paper_list = self.session.query(Paper).order_by(desc(Paper.id)).all()
        return paper_list


    def get_max_paper(self):
        max = self.session.query(Paper.num).order_by(desc(Paper.id)).limit(1).all()
        return max[0][0]


    def close_session(self):
        self.session.close()




'''
if __name__ == '__main__':
    model =Model()
    print model.get_article_list(555)
    print model.get_max_paper()
    #for i in model.get_all_paper():


'''
