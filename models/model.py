# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import update
from datetime import datetime
from config import mysql

# from SQLAlchemy.pool import NullPool
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

    def get_articles(self, paper_id):
        """获得一期中所有的文章"""
        article_list = self.session.query(Article.id, Article.title)
        article_list = article_list.filter(Article.paper_id == paper_id).all()
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
        is_exist = self.session.query(Paper.id).filter(Paper.num == paper_num).first()
        if is_exist:
            self.session.query(Paper).filter(Paper.num == paper_num).delete()
            self.session.commit()
            return True
        else:
            return None

    def insert_article(self, **kwargs):
        """新增一篇文章."""
        args = ["title", "sub_title", "reply_title", "content",
                "paper_id", "page_id", "show_author", "has_pic",
                "author"]
        d = dict()
        for key in kwargs.iterkeys():
            if key in args:
                d[key] = kwargs[key]
        d["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        article = Article(**d)
        self.session.add(article)
        self.session.commit()
        return article

    def update_article(self, **kwargs):
        """修改一篇文章"""
        # article = self.session.query(Article).get(kwargs["id"])
        # for key in kwargs.iterkeys():
        # article.key = kwargs[key]
        # self.session.commit()
        return update(Article).where(Article.id == kwargs['id']).values(kwargs).execute()

    def delete_article(self, article_id):
        """删除一篇文章"""
        article = self.session.query(Article).filter(Article.id == article_id)
        self.session.delete(article)
        self.session.commit()
        return article

    def new_page(self, paper_id, num, pic_url, name):
        """添加报刊"""
        page = Page(paper_id=paper_id, num=num, pic_url=pic_url, name=name)
        self.session.add(page)
        self.session.commit()
        return page

    def update_page(self, page_id, paper_id=None, num=None, pic_url=None, name=None):
        """修改报刊"""
        page = self.session.query(Page).filter(Page.id == page_id).first()
        if paper_id is not None:
            page.paper_id = paper_id
        if pic_url is not None:
            page.pic_url = pic_url
        if name is not None:
            page.name = name
        if num is not None:
            page.num = num
        self.session.add(page)
        self.session.commit()

    def insert_area(self, **kwargs):
        """新增一个报刊区域"""
        args = ["page_id", "paper_id", "article_id", "x", "y", "width", "height"]
        d = dict()
        for key in kwargs.iterkeys():
            if key in args:
                d[key] = kwargs[key]
        d['x'] = str(d['x']) + "px"
        d['y'] = str(d['y']) + "px"
        d['width'] = str(d['width']) + "px"
        d['height'] = str(d['height']) + "px"
        area = Area(**d)
        self.session.add(area)
        self.session.commit()
        return area

    def paper_issued(self, paper_id, issued):
        """改变期刊的发布状态"""
        paper = self.session.query(Paper).filter(Paper.id == paper_id).first()
        if not paper:
            return False
        paper.issued = issued
        self.session.add(paper)
        self.session.commit()

    def delete_page(self, page_id):
        """删除报刊"""
        page = self.session.query(Page).filter(Page.id == page_id).first()
        self.session.delete(page)
        self.session.commit()

    def close_session(self):
        self.session.close()
