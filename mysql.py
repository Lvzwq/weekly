# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from appconfig import MYSQL_HOST, MYSQL_USER, MYSQL_DB, MYSQL_CHARSET, MYSQL_PASSWORD
# 安装的扩展库sqlalchemy

# conn='mysql://root:root@localhost/newscenter?charset=utf8'
conn = 'mysql://%s:%s@%s/%s?charset=%s' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_CHARSET)
engine = create_engine(conn)
Base = declarative_base(engine)
metadata = MetaData(engine)


class Area(Base):
    __tablename__ = 'area'
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
    id = Column(Integer, primary_key=True)
    title = Column(String(11))
    sub_title = Column(String)
    content = Column(String)
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
    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    article_id = Column(Integer)


class Paper(Base):
    __tablename__ = 'paper'
    id = Column(Integer, primary_key=True)
    num = Column(Integer)
    issued = Column(Integer)
    time = Column(DateTime)


def init_db():
    # moz_article = Table('article', metadata, autoload=True)
    # mapper(Article, moz_article)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_article_list(session,paper_id,):
    article_list = session.query(Article.id,Article.title,Article.reply_title,Article.has_pic,Article.sub_title)
    article_list = article_list.filter(Article.paper_id == paper_id)
    article_list = article_list.all()
    return article_list

def get_all_paper(session):
    paper_list =session.query().all
    return paper_list


def close_session(session):
    session.close()







