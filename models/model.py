# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import update, delete, insert
from datetime import datetime
# from sqlalchemy.pool import NullPool

from config.db import MYSQL_HOST, MYSQL_USER, MYSQL_DB, MYSQL_CHARSET, MYSQL_PASSWORD

# 安装的扩展库sqlalchemy

# conn='mysql://root:root@localhost/newscenter?charset=utf8'
conn = 'mysql://%s:%s@%s/%s?charset=%s' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_CHARSET)
engine = create_engine(conn)  # 使用非连接池的方式连接数据库
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
    # __table_args__ = {'autoload': True}
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


class Page(Base):
    __tablename__ = 'page'
    __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer)
    num = Column(Integer)
    pic_url = Column(String)
    name = Column(String)


class Model():
    def __init__(self):
        # moz_article = Table('article', metadata, autoload=True)
        # mapper(Article, moz_article)
        # metadata = MetaData(engine)
        session = sessionmaker(bind=engine)
        self.session = session()


    def get_article_list(self, page_id):
        article_list = self.session.query(Article.id, Article.title, Article.reply_title, Article.has_pic,
                                          Article.sub_title)
        article_list = article_list.filter(Article.page_id == page_id)
        article_list = article_list.all()
        return article_list


    def get_all_paper(self):
        paper_list = self.session.query(Paper).filter(Paper.issued == 1).order_by(desc(Paper.id)).all()
        return paper_list


    def get_max_paper(self):
        max = self.session.query(Paper.num, Paper.id).filter(Paper.issued == 1).order_by(desc(Paper.id)).limit(1).all()
        return max[0]

    def get_area_list(self, page_id):
        area_list = self.session.query(Area).filter(Area.page_id == page_id).all()
        return area_list

    def get_pic_info(self, paper_id, num=1):
        pic_info = self.session.query(Page).filter(Page.paper_id == paper_id).filter(Page.num == num).all()
        return pic_info[0]

    def get_page_info(self, page_id):
        page_info = self.session.query(Page).filter(Page.id == page_id).all()
        return page_info[0]

    # 获得一篇文章的内容
    def get_article_info(self, article_id):
        article_info = self.session.query(Article).filter(Article.id == article_id).all()
        return article_info[0]

    def get_paper_info(self, paper_id):
        page_info = self.session.query(Paper.num).filter(Paper.id == paper_id).all()
        return page_info[0].num

    def get_paper(self,paper_num):
        return self.session.query(Paper).filter(Paper.num == paper_num).all()

    # 根据报纸id获得报纸页面id
    def get_column_list(self, paper_id):
        column_list = self.session.query(Page).filter(Page.paper_id == paper_id).all()
        return column_list

    # 后台管理页面获得报纸期数列表
    def get_paper_list(self, offset=0, limit=20):
        paper_list = self.session.query(Paper).order_by(desc(Paper.id)).limit(limit).offset(offset).all()
        return paper_list

    def get_paper_count(self):
        num = self.session.query(func.count(Paper.id)).all()
        return num[0][0]

    # 新增一个期刊
    def new_paper(self, paper_num):
        is_exist = self.session.query(Paper.id).filter(Paper.num == paper_num).all()
        if is_exist:
            p = update(Paper).where(Paper.num == paper_num).values(time=datetime.now())
            self.session.execute(p)
            self.session.commit()
        else:
            paper = Paper()
            paper.num = paper_num
            paper.time = datetime.now()
            paper.issued = 0
            self.session.add(paper)
            return self.session.commit()

    # 删除报纸期刊
    def delete_paper(self, paper_num):
        is_exist = self.session.query(Paper.id).filter(Paper.num == paper_num).all()
        if is_exist:
            self.session.query(Paper).filter(Paper.num == paper_num).delete()
            self.session.commit()
        else:
            return True

    # 新增一篇文章
    def insert_article(self, article_info):
        sql = insert(Article, values=article_info)
        self.session.execute(sql)
        self.session.commit()

    # 修改一篇文章
    def update_article(self, article_id, article_info):
        return update(Article).where(Article.id == article_id).values(article_info).execute()

    #删除一篇文章
    def delete_article(self, article_id):
        return delete(Article, returning=Article.id, return_defaults=True).where(Article.id == article_id).execute()

    def insert_area(self, area):
        pass

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    model = Model()
    # print model.get_paper_count()
    # print model.get_article_list(555)
    # print model.get_max_paper().id
    # print
    # print model.delete_paper(508)

    # for i in model.get_area_list(273):
    # print i.paper_id
    # for i in model.get_all_paper():

