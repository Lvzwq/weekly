# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import update, delete, insert
from datetime import datetime
from config import mysql

# from sqlalchemy.pool import NullPool
# 安装的扩展库SQLAlchemy

conn = 'mysql://{user}:{password}@{host}/{db}?charset={charset}'.format(**mysql)
engine = create_engine(conn, echo=True)  # 使用非连接池的方式连接数据库
Base = declarative_base(engine)


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

    def __repr__(self):
        return "<Area(page_id='%s', paper_id='%s', article_id='%s', x='%s', y='%s', width='%s', height='%s')>" % (
            self.page_id, self.paper_id, self.article_id, self.x, self.y, self.width, self.height)


class Article(Base):
    __tablename__ = 'article'
    # __table_args__ = {'autoload': True}
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


class KeyInfo(Base):
    __tablename__ = 'keyinfo'
    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    article_id = Column(Integer)


class Paper(Base):
    __tablename__ = 'paper'
    # __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True, nullable=False)
    num = Column(Integer)
    issued = Column(Integer)
    time = Column(DateTime)


class Page(Base):
    __tablename__ = 'page'
    # __table_args__ = {'autoload': True}
    id = Column(Integer, primary_key=True, nullable=False)
    paper_id = Column(Integer)
    num = Column(Integer)
    pic_url = Column(String)
    name = Column(String)


class Connection():
    table_page = Page.__table__
    table_paper = Paper.__table__
    table_article = Article.__table__
    table_area = Area.__table__

    def __init__(self):
        super(Connection, self).__init__()
        self.conn = engine.connect()


class Model():
    def __init__(self):
        # moz_article = Table('article', metadata, autoload=True)
        # mapper(Article, moz_article)
        # metadata = MetaData(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def get_article_list(self, page_id):
        """根据页面获得页面所有文章列表."""
        article_list = self.session.query(Article.id, Article.title,
                                          Article.reply_title,
                                          Article.has_pic,
                                          Article.sub_title)
        article_list = article_list.filter(Article.page_id == page_id).all()
        return article_list

    def get_all_paper(self, all_select=False, issued=1):
        """获得所有的期刊"""
        if all_select:
            paper_list = self.session.query(Paper).order_by(desc(Paper.id)).all()
        else:
            paper_list = self.session.query(Paper).filter(Paper.issued == issued).order_by(desc(Paper.id)).all()
        return paper_list

    def get_max_paper(self):
        """获得最近的一期"""
        last = self.session.query(Paper.num, Paper.id).filter(Paper.issued == 1).order_by(desc(Paper.id)).first()
        return last

    def get_max_paper_issued(self):
        last = self.session.query(Paper).order_by(desc(Paper.id)).first()
        return last

    def get_area_list(self, page_id):
        area_list = self.session.query(Area).filter(Area.page_id == page_id).all()
        return area_list

    def get_pic_info(self, paper_id, num=1):
        """获得当前期数的默认第一个页面"""
        pic_info = self.session.query(Page).filter(Page.paper_id == paper_id).filter(Page.num == num).first()
        return pic_info

    def get_page_info(self, page_id):
        """获得指定页面."""
        page_info = self.session.query(Page).filter(Page.id == page_id).first()
        return page_info

    def get_article_info(self, article_id):
        """获得文章内容"""
        article_info = self.session.query(Article).filter(Article.id == article_id).first()
        return article_info

    def get_paper_info(self, paper_id):
        page_info = self.session.query(Paper.num).filter(Paper.id == paper_id).all()
        return page_info[0].num

    def get_paper(self, paper_num):
        return self.session.query(Paper).filter(Paper.num == paper_num).first()

    def get_column_list(self, paper_id):
        """根据期数id获得报纸4个页面"""
        column_list = self.session.query(Page).filter(Page.paper_id == paper_id).all()
        return column_list

    def get_paper_list(self, offset=0, limit=20):
        """获得所有的期刊列表."""
        paper_list = self.session.query(Paper).order_by(desc(Paper.id)).limit(limit).offset(offset).all()
        return paper_list

    def get_paper_count(self):
        num = self.session.query(func.count(Paper.id)).all()
        return num[0][0]

    def new_paper(self, paper_num, pub_time=datetime.now()):
        """新增一个期刊."""
        is_exist = self.session.query(Paper).filter(Paper.num == paper_num).first()
        if is_exist:
            p = update(Paper).where(Paper.num == paper_num).values(time=pub_time)
            self.session.execute(p)
            self.session.commit()
            return is_exist
        else:
            paper = Paper()
            paper.num = paper_num
            paper.time = pub_time
            paper.issued = 0
            self.session.add(paper)
            self.session.commit()
            return paper

    def delete_paper(self, paper_num):
        """删除报纸期刊."""
        is_exist = self.session.query(Paper.id).filter(Paper.num == paper_num).all()
        if is_exist:
            self.session.query(Paper).filter(Paper.num == paper_num).delete()
            self.session.commit()
        else:
            return True

    def insert_article(self, article_info):
        """新增一篇文章."""
        sql = insert(Article, values=article_info)
        self.session.execute(sql)
        self.session.commit()

    # 修改一篇文章
    def update_article(self, article_id, article_info):
        return update(Article).where(Article.id == article_id).values(article_info).execute()

    # 删除一篇文章
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
