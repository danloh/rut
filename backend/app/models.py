# -*- coding: utf-8 -*-

import random
import re
from datetime import datetime
from flask import url_for, current_app, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_login import UserMixin, AnonymousUserMixin, current_user
from markdown import markdown
import bleach
from . import db, login_manager, cache
from .utils import split_str, str_to_dict, str_to_set


# html_tags Whitelist for Bleach
allowed_tags = ['a', 'abbr', 'b', 'blockquote', 'code', 'img',
                'em', 'i', 'li', 'ol', 'ul', 'pre', 'strong',
                'h3', 'h4', 'h5', 'h6', 'hr', 'p']

# simple n2n for Tags Posts
tag_post = db.Table(
    'tag_post',
    db.Column(
        'tag_id', db.Integer, db.ForeignKey("tags.id")
    ),
    db.Column(
        'post_id', db.Integer, db.ForeignKey("posts.id")
    )
)
# simple n2n for Tags Items
tag_item = db.Table(
    'tag_item',
    db.Column(
        'tag_id', db.Integer, db.ForeignKey("tags.id")
    ),
    db.Column(
        'item_id', db.Integer, db.ForeignKey("items.id")
    )
)
# simple n2n for Tags Demands
tag_demand = db.Table(
    'tag_demand',
    db.Column(
        'tag_id', db.Integer, db.ForeignKey("tags.id")
    ),
    db.Column(
        'demand_id', db.Integer, db.ForeignKey("demands.id")
    )
)


# helper Model for n2n Posts collect Items
class Collect(db.Model):
    __table_name__ = 'collect'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    order = db.Column(db.SmallInteger)   #item's order in post
    tips = db.Column(db.Text, nullable=False)
    tips_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

    # n to 1 with Users
    tip_creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )

    def to_dict(self):
        item_dict = self.item.to_dict()
        tip_dict = {
            'order': self.order,
            'cid': self.id,
            'postid': self.post_id,
            'itemid': self.item_id,
            'item': item_dict,
            'tip': self.tips_html or self.tips
        }
        return tip_dict

    @staticmethod
    def on_changed_tips(target, value, oldvalue, initiator):
        target.tips_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Collect.tips, 'set', Collect.on_changed_tips)

# helper Model for n2n Posts with Users for star
class Star(db.Model):
    __table_name__ = 'star'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

# helper Model for n2n Posts with Users for challenge
class Challenge(db.Model):
    __table_name__ = 'challenge'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    deadline = db.Column(db.Date)
    done = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

# helper Model for n2n Posts co-Contribute
class Contribute(db.Model):
    __table_name__ = 'contribute'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    disabled = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    
    def to_dict(self):
        user_dict = self.contributor.to_dict()
        contribute_dict = {
            'id': self.id,
            'contributorid': self.user_id,
            'postid': self.post_id,
            'disabled': self.disabled,
            'contributor': user_dict
        }
        return contribute_dict

# helper Model for n2n Users flag Items
class Flag(db.Model):
    __table_name__ = 'flag'
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    #flag label: read-1,reading-2,read-3
    flag_label = db.Column(db.SmallInteger,default=0)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

# helper Model for n2n Users favirate Tags
class Fav(db.Model):
    __table_name__ = 'fav'
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

# helper Model for n2n Items with Authors
# item-bys : by-items
class Byline(db.Model):
    __table_name__ = 'byline'
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        primary_key=True)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id"),
        primary_key=True)
    contribution = db.Column(db.String(32), nullable=False)

# helper for n2n Users vote Demands
class Dvote(db.Model):
    __table_name__ = 'dvote'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    demand_id = db.Column(
        db.Integer,
        db.ForeignKey("demands.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

# helper for n2n Users vote Reviews
class Rvote(db.Model):
    __table_name__ = 'rvote'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    review_id = db.Column(
        db.Integer,
        db.ForeignKey("reviews.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

# helper Model for n2n Posts re Demands
class Respon(db.Model):
    __table_name__ = 'respon'
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    demand_id = db.Column(
        db.Integer,
        db.ForeignKey("demands.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

class Posts(db.Model):
    __table_name__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    intro_html = db.Column(db.Text)
    credential = db.Column(db.String(256))
    rating = db.Column(db.String(32))
    tag_str = db.Column(db.String(256), default="42")
    epilog = db.Column(db.Text)
    epilog_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    renewal = db.Column(db.DateTime,
                          default=datetime.utcnow)
    editable = db.Column(db.String(32),default='Creator')
    edit_start = db.Column(db.DateTime,default=None)
    disabled = db.Column(db.Boolean)
    vote = db.Column(db.Integer, default=0)
    refer = db.Column(db.String(32))  # to mark off some special list

    # n to 1 with Users
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # 1 to n with Comments
    comments = db.relationship(
        'Comments', backref='post', lazy='dynamic')
    # 1 to n with Events
    events = db.relationship(
        'Events',backref='post',lazy='dynamic')

    # n2n with Users for contributor
    contributors = db.relationship(
        'Contribute',
        foreign_keys=[Contribute.post_id],
        backref=db.backref('contribute_post',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Users for star
    starers = db.relationship(
        'Star',
        foreign_keys=[Star.post_id],
        backref=db.backref('star_post',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Users for challenge
    challengers = db.relationship(
        'Challenge',
        foreign_keys=[Challenge.post_id],
        backref=db.backref('challenge_post',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Items
    items = db.relationship(
        'Collect',
        foreign_keys=[Collect.post_id],
        backref=db.backref('post', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Demands
    demands = db.relationship(
        'Respon',
        foreign_keys=[Respon.post_id],
        backref=db.backref('post', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # collect items into post
    def collected(self,item):
        """
        check if there is a record in Collect table,
        record indicates post linking item
        return True or False
        """
        return self.items.filter_by(item_id=item.id).first() is not None

    def collecting(self, item, tips, tip_creator):
        """
        collect item into post,
        ie. add a record into Collect table
        """
        if not self.collected(item):
            c = Collect(
                post=self,
                item=item,
                order=self.items.count()+1,
                tips=tips,
                tip_creator=tip_creator
            ) # refer to the relationship-backref var
            db.session.add(c)
            # update item's vote
            item.cal_vote()
            # update the renew timestamp
            self.renew()
            #save activity to db Events
            current_user.set_event(action='updates',post=self,item=item)
            #db.session.commit() #if need commit?

    # set and change the order of items, ## ??maybe an issue here!!##
    def ordering(self,item,new_order):
        _c = self.items  # ie. a collect-object
        c_old = _c.filter_by(item_id=item.id).first()
        old_order = c_old.order

        if new_order == old_order:
            pass
        else:
            if new_order > old_order:
                _c.filter(Collect.order > old_order, Collect.order <= new_order).\
                update({'order':Collect.order-1})
            if new_order < old_order:
                _c.filter(Collect.order < old_order, Collect.order >= new_order).\
                update({'order':Collect.order+1})
            
            c_old.order = new_order
            db.session.add(c_old)
            #db.session.commit()

    # add post tags to database
    def tag_to_db(self):
        '''
        split the input tags to seperated tag,
        and add them into Tags Table
        '''
        _tag_str = self.tag_str
        _tagset = str_to_set(_tag_str)
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip()
            if _tg: # is not "":
                _tag = _query.filter_by(tag=_tg).first()
                if _tag is None:
                    tag=Tags(tag=_tg)
                    tag.posts.append(self)
                    tag.cal_vote()
                    db.session.add(tag)
                else:
                    _tag.posts.append(self)
                    _tag.cal_vote()
                    db.session.add(_tag)
        #db.session.commit()
    
    #check if can be edited
    @property
    def uneditable(self):
        contribute = self.contributors.filter_by(
            user_id=current_user.id,
            disabled=False
        ).first()
        if (current_user != self.creator and
                contribute is None and
                self.editable != 'Everyone'):
            return True
        else:
            return False

    # lock and unlock status in/after edit: a stopgap
    def lock(self):
        self.edit_start = datetime.utcnow()
        db.session.add(self)
        # set a value to indicate in editing
        db.session.commit()
    def unlock(self):
        self.edit_start = None
        db.session.add(self)
        # reset eidt_start to None, after edit done
        db.session.commit()
    def force_unlock(self, start=None, timeout=2400):
        # sometime user forget submit, need to force unlock
        start = start or self.edit_start
        if start:
            now = datetime.utcnow()
            delta = now - start
            if delta.seconds >= timeout:
                self.unlock()
    def check_locked(self):
        # if eidt_start is not None, it is locked as editing
        start = self.edit_start
        if start:
            #force_unlock firstly
            self.force_unlock(start=start)
            return bool(self.edit_start)
        else:
            return False
    def mod_locked(self):
        # GET: lock and  render edit tpl, POST: unlock
        if request.method == "GET":
            if self.check_locked():
                flash('This Content is in Editing, to Avoid Conflict, Please Try later, up to 40min')
                return True
            # set edit_start as indict editing
            self.lock()
        # on_submit as edit done POST
        if request.method == "POST":
            self.unlock()

    def renew(self):
        self.renewal = datetime.utcnow()
        db.session.add(self)
        #db.session.commit()

    def cal_vote(self,n=None,m=None):
        n = n or self.starers.count()
        m = m or self.challengers.count() * 2
        self.vote = n+m
        db.session.add(self)
        #db.session.commit()
    @property
    def score(self):
        """caculate the post score, can be deprecated"""
        itemcount = self.items.count()
        starcount = self.starers.count()
        challengecount = self.challengers.count()
        score = itemcount*2 + starcount * 5 + challengecount *10
        return score

    # set logo cover of  post
    @property
    @cache.memoize()
    def post_cover(self):
        n = self.items.count()
        if n ==0:
            return url_for('static', filename='pic/dpc.svg')
        else:
            m = random.randrange(n)
            return self.items.all()[m].item.cover

    @staticmethod
    #@cache.memoize() #to tackle
    def select_posts():
        _query = Posts.query
        m = current_app.config['POST_PER_PAGE']

        posts_latest = _query.order_by(Posts.renewal.desc()).limit(m)
        posts_popular = _query.order_by(Posts.vote.desc()).limit(m)

        posts_select = posts_latest.union(posts_popular).\
                       order_by(db.func.rand()).limit(m)

        return posts_select

    def to_dict(self):
        creator = self.creator.to_dict()
        contributes = self.contributors
        contributors = [i.to_dict() for i in contributes]
        contributor_id_list = [i.user_id for i in contributes]
        tags = [t.to_dict() for t in self.tags]
        post_dict = {
            'id': self.id,
            'title': self.title,
            'intro': self.intro,
            'credential': self.credential,
            'rating': self.rating,
            'epilog': self.epilog,
            'createat': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            #'renewat': self.renewal.strftime('%Y-%m-%d %H:%M:%S'),
            'score': self.score,
            'itemcount': self.items.count(),
            'starcount': self.starers.count(),
            'challengecount': self.challengers.count(),
            'commentcount': self.comments.count(),
            'cover': self.post_cover,
            'editable': self.editable,
            'creator': creator,
            'contributors': contributors,
            'contributoridlist': contributor_id_list,
            'tags': tags
        }
        return post_dict

    ## markdown to html
    # @staticmethod
    # def on_changed_intro(target, value, oldvalue, initiator):
    #     target.intro_html = bleach.linkify(bleach.clean(
    #         markdown(value, output_format='html'),
    #         tags=allowed_tags, strip=False))
    # @staticmethod
    # def on_changed_epilog(target, value, oldvalue, initiator):
    #     target.epilog_html = bleach.linkify(bleach.clean(
    #         markdown(value, output_format='html'),
    #         tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Posts %r>' % self.title

# db.event.listen(Posts.intro, 'set', Posts.on_changed_intro)
# db.event.listen(Posts.epilog, 'set', Posts.on_changed_epilog)

class Items(db.Model):
    __table_name__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    res_url = db.Column(db.String(512))
    uid = db.Column(db.String(128), unique=True, nullable=False)  #isbn13 etc.
    isbn10 = db.Column(db.String(32), unique=True)
    asin = db.Column(db.String(32), unique=True)
    author = db.Column(db.String(512)) # or instructor
    cover = db.Column(db.String(512))
    cate = db.Column(db.String(16),default='Book')
    publisher = db.Column(db.String(256))
    pub_date = db.Column(db.String(128)) # or start date
    language = db.Column(db.String(256))
    binding = db.Column(db.String(128))
    page = db.Column(db.String(128)) # book page or length of course
    level = db.Column(db.String(256))
    price = db.Column(db.String(128))
    details = db.Column(db.Text)
    itag_str = db.Column(db.String(512))
    vote = db.Column(db.Integer,default=0)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # 1 to n with Comments
    comments = db.relationship(
        'Comments',backref='item',lazy='dynamic')
    # 1 to n with reviews
    reviews = db.relationship(
        'Reviews',backref='item',lazy='dynamic')
    # 1 to n with Clips
    clips = db.relationship(
        'Clips',backref='item',lazy='dynamic')
    # 1 to n with Events
    events = db.relationship(
        'Events',backref='item',lazy='dynamic')

    # n2n with Posts
    posts = db.relationship(
        'Collect',
        foreign_keys=[Collect.item_id],
        backref=db.backref('item', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Users
    flagers = db.relationship(
        'Flag',
        foreign_keys=[Flag.item_id],
        backref=db.backref('flag_item',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    #n2n with Authors
    bys =  db.relationship(
        'Byline',
        foreign_keys=[Byline.item_id],
        backref=db.backref('item',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # set default item cover
    @property
    def item_cover(self):
        if self.cover is None or not self.cover.strip():
            if self.cate == 'Online':
                return url_for('static', filename='pic/online.svg')
            if self.cate == 'Book':
                return url_for('static', filename='pic/book.svg')
            if self.cate == 'Video':
                return url_for('static', filename='pic/video.svg')
            if self.cate == 'Album':
                return url_for('static', filename='pic/album.svg')
            if self.cate == 'Other':
                return url_for('static', filename='pic/other.svg')

    # add item tags to database
    def itag_to_db(self):
        '''
        split the input tags to seperated tag,
        and add them into Tags Table
        '''
        #_taglist = self.itag_str.split(',') #
        _itag_str = self.itag_str
        _tagset = str_to_set(_itag_str)
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip() #
            if _tg: # is not "":
                _tag = _query.filter_by(tag=_tg).first()
                if _tag is None:
                    tag=Tags(tag=_tg)
                    tag.items.append(self)
                    db.session.add(tag)
                    tag.cal_vote()
                elif _tag.items.filter_by(id=self.id).first() is None:
                    _tag.items.append(self)
                    db.session.add(_tag)
                    _tag.cal_vote()
        #db.session.commit()

    # add author to db
    def author_to_db(self,s=None):
        author_str = s or self.author
        d = str_to_dict(author_str)
        a_query = Authors.query
        for k,v in d.items():
            author_old = a_query.filter_by(name=k).first()
            if author_old is None:
                author = Authors(name=k)
                db.session.add(author)
            else:
                author = author_old
            if self.bys.filter_by(author_id=author.id).first() is None:
                byline = Byline(
                    item=self,
                    by=author,
                    contribution=v
                )
                db.session.add(byline)
        #db.session.commit()
    
    def cal_vote(self,c=None,p=None,r=None,f=None):
        c = c or self.clips.count()
        p = p or self.posts.count()
        r = r or self.reviews.count()
        f = f or self.flagers.count()
        self.vote = c+p+r+f
        db.session.add(self)
        #db.session.commit()
    
    def to_dict(self):
        item_dict = {
            'id': self.id,
            'cate': self.cate,
            'title': self.title,
            'uid': self.uid,
            'byline': self.author, 
            'rutcount': self.posts.count(),
            'reviewcount': self.reviews.count(),
            'clipcount': self.clips.count(),
            'commentcount': self.comments.count(),
            'cover': self.cover or self.item_cover,
            'publisher': self.publisher,
            'pubdate': self.pub_date,
            'language': self.language,
            'resurl': self.res_url,
            'details': self.details
        }
        return item_dict

    def __repr__(self):
        return '<Items %r>' % self.title


# helper Model for Tags hierarchy
class Clan(db.Model):
    __tablename__ = 'clan'
    parent_tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True)
    child_tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

class Tags(db.Model):
    __table_name__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(128), nullable=False, unique=True)
    descript = db.Column(db.String(512))
    vote = db.Column(db.Integer, default=0)

    # 1 to n with Events
    events = db.relationship(
        'Events',backref='tag',lazy='dynamic')

    # n2n with users
    favers = db.relationship(
        'Fav',
        foreign_keys=[Fav.tag_id],
        backref=db.backref('fav_tag',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # simple n2n relationship with Posts
    posts = db.relationship(
        'Posts',
        secondary=tag_post,
        backref=db.backref('tags', lazy='joined'),
        lazy='dynamic')
    # simple n2n relationship with items
    items = db.relationship(
        'Items',
        secondary=tag_item,
        backref=db.backref('itags', lazy='joined'),
        lazy='dynamic')
    # simple n2n relationship with demands
    demands = db.relationship(
        'Demands',
        secondary=tag_demand,
        backref=db.backref('dtags', lazy='joined'),
        lazy='dynamic')

    # n2n with self
    parent_tags = db.relationship(
        'Clan',
        foreign_keys=[Clan.child_tag_id],
        backref=db.backref('child_tag', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    child_tags = db.relationship(
        'Clan',
        foreign_keys=[Clan.parent_tag_id],
        backref=db.backref('parent_tag', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def parent_is(self, tag):
        return self.parent_tags.filter_by(
            parent_tag_id=tag.id).first() is not None

    def parent(self, tag):
        if not self.parent_is(tag):
            c = Clan(child_tag=self, parent_tag=tag)
            db.session.add(c)
            #db.session.commit()

    #cache get rand tags
    @staticmethod
    @cache.memoize()
    def get_tags():
        return Tags.query.order_by(db.func.rand()).limit(20).all()

    def cal_vote(self,i=None,p=None,d=None,f=None):
        i = i or self.items.count()
        p = p or self.posts.count()
        d = d or self.demands.count()
        f = f or self.favers.count()
        self.vote = i+p+d+f
        db.session.add(self)
        #db.session.commit()
    @property
    def score(self):
        itemcount = self.items.count()
        postcount = self.posts.count()
        demandcount = self.demands.count()
        favcount = self.favers.count()
        score = itemcount + postcount + demandcount + favcount
        return score, demandcount

    def to_dict(self):
        tag_dict = {
            'id': self.id,
            'tagname': self.tag,
            'descript': self.descript,
            'favcount': self.favers.count()
        }
        return tag_dict

    def __repr__(self):
        return '<Tags %r>' % self.tag


# helper Model for Reply comments
class Reply(db.Model):
    __tablename__ = 'reply'
    parent_commt_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id'),
        primary_key=True)
    child_commt_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

class Comments(db.Model):
    __table_name__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    #1 to n with Events
    events = db.relationship(
        'Events',backref='comment',lazy='dynamic')

    # n to 1 with Users
    creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )
    # n to 1 with Posts
    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id")
    )
    # n to 1 with Items
    item_id = db.Column(
        db.Integer, db.ForeignKey("items.id")
    )
    # n to 1 with Reviews
    review_id = db.Column(
        db.Integer, db.ForeignKey("reviews.id")
    )
    # n to 1 with demands
    demand_id = db.Column(
        db.Integer, db.ForeignKey("demands.id")
    )

    # n2n with self
    parent_commts = db.relationship(
        'Reply',
        foreign_keys=[Reply.child_commt_id],
        backref=db.backref('child_commt', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    child_commts = db.relationship(
        'Reply',
        foreign_keys=[Reply.parent_commt_id],
        backref=db.backref('parent_commt', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def reply(self, commt):
        r = Reply(parent_commt=self, child_commt=commt)
        db.session.add(r)
        #db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_dict(self):
        comment_dict = {
            'id': self.id,
            'heading': self.heading,
            'body': self.body_html or self.body,
            'vote': self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'children': [c.child_commt.to_dict() for c in self.child_commts]
        }
        return comment_dict

    def __repr__(self):
        return '<Coments %r>' % self.body

db.event.listen(Comments.body, 'set', Comments.on_changed_body)


class Reviews(db.Model):
    __table_name__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # 1 to n with Comments
    comments = db.relationship(
        'Comments',backref='review',lazy='dynamic')
    # 1 to n with Events
    events = db.relationship(
        'Events',backref='review',lazy='dynamic')

    # n to 1 with Users
    creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )
    # n to 1 with Items
    item_id = db.Column(
        db.Integer, db.ForeignKey("items.id")
    )

    # n2n with Users for vote
    voters = db.relationship(
        'Rvote',
        foreign_keys=[Rvote.review_id],
        backref=db.backref('vote_review', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    
    def to_dict(self):
        review_dict = {
            'id': self.id,
            'heading': self.heading,
            'creator': self.creator.to_dict(),
            'body': self.body_html or self.body,
            'vote':  self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return review_dict

    def __repr__(self):
        return '<Reviews %r>' % self.heading

db.event.listen(Reviews.body, 'set', Reviews.on_changed_body)


class Clips(db.Model):
    __table_name__ = "clips"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # 1 to n with Events
    events = db.relationship(
        'Events',backref='clip',lazy='dynamic')

    # n to 1   with Users
    creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )
    # n to 1   with Items
    item_id = db.Column(
        db.Integer, db.ForeignKey("items.id")
    )

    def to_dict(self):
        clip_dict = {
            'id': self.id,
            'creator': self.creator.to_dict(),
            'fromitem': self.item.to_dict(),
            'body': self.body_html or self.body,
            'vote': self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return clip_dict

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    
    def __repr__(self):
        return '<Clips %r>' % self.body

db.event.listen(Clips.body, 'set', Clips.on_changed_body)


class Demands(db.Model):
    __table_name__ = "demands"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    vote = db.Column(db.Integer,default=1)
    dtag_str = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # 1 to n with Comments
    comments = db.relationship(
        'Comments',backref='demand',lazy='dynamic')
    # 1 to n with Events
    events = db.relationship(
        'Events',backref='demand',lazy='dynamic')

    # n to 1 relation with Users
    requestor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # n2n with Posts
    posts = db.relationship(
        'Respon',
        foreign_keys=[Respon.demand_id],
        backref=db.backref('demand', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Users for vote
    voters = db.relationship(
        'Dvote',
        foreign_keys=[Dvote.demand_id],
        backref=db.backref('vote_demand', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def dtag_to_db(self):

        #_taglist = self.dtag_str.split(',') #
        _dtag_str = self.dtag_str
        _tagset = str_to_set(_dtag_str)
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip() #
            if _tg: # is not "":
                _tag = _query.filter_by(tag=_tg).first()
                if _tag is None:
                    tag=Tags(tag=_tg)
                    tag.demands.append(self)
                    tag.cal_vote()
                    db.session.add(tag)
                else:
                    _tag.demands.append(self)
                    _tag.cal_vote()
                    db.session.add(_tag)
        #db.session.commit()
    
    def to_dict(self):
        demand_dict = {
            'id': self.id,
            'requestor': self.requestor.to_dict(),
            'body': self.body,
            'vote': self.vote,
            'answercount': self.posts.count(),
            'commentcount': self.comments.count(),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return demand_dict

    def __repr__(self):
        return '<Demands %r>' % self.body


# helper Model for Messages n2n with self for dialog
class Dialog(db.Model):
    __tablename__ = 'dialog'
    s_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id'),
        primary_key=True)
    r_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                         default=datetime.utcnow)

class Messages(db.Model):
    __table_name__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text) # !! encrypt, to do
    status = db.Column(db.String(16)) #unread,read,s_del,r_del

    # n to 1 with Users for send and receive msg
    send_id = db.Column(
        db.Integer, db.ForeignKey('users.id')
    )
    receive_id = db.Column(
        db.Integer, db.ForeignKey('users.id')
    )

    # n2n with self for re msg, ie, dialog
    sends = db.relationship(
        'Dialog',
        foreign_keys=[Dialog.r_id],
        backref=db.backref('re', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    res = db.relationship(
        'Dialog',
        foreign_keys=[Dialog.s_id],
        backref=db.backref('send', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def dialog(self, message):
        d = Dialog(send=self, re=message)
        db.session.add(d)
        #db.session.commit()

    def __repr__(self):
        return '<Messages %r>' % self.content


class Permission:
    SCFFFV = 0x0001  # STAR,CHALLENGE,FAV,FLAG,FOLLOW,VOTE
    DEMAND = 0x0002
    EDIT_ITEM = 0x0004 # EDIT ITEM/TAG
    COMMENT = 0x0008
    POST = 0x0010
    ADD_ITEM = 0x0020
    REVIEW = 0x0040
    ARTICLE = 0x0080
    EDIT_POST = 0x0100
    EDIT_TIPS = 0x0200

    MOD_CONTENT =0x2000
    MOD_ROLE = 0x4000
    ADMIN =0x8000

class Roles(db.Model):
    __table_name__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    duty = db.Column(db.String(32), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)

    # 1 to n with Users
    users = db.relationship(
        'Users', backref='role', lazy='dynamic')
    
    def to_dict(self):
        role_dict = {
            'duty': self.duty,
            'permissions': self.permissions
        }

    # for add roles
    role_cases ={
        "limited":(Permission.SCFFFV, False),
        "user":(Permission.SCFFFV | Permission.DEMAND |
                Permission.EDIT_ITEM | Permission.COMMENT |
                Permission.POST | Permission.ADD_ITEM |
                Permission.REVIEW | Permission.ARTICLE,
                True),
        "moderator":(Permission.SCFFFV | Permission.DEMAND |
                Permission.EDIT_ITEM | Permission.COMMENT |
                Permission.POST | Permission.ADD_ITEM |
                Permission.REVIEW | Permission.ARTICLE |
                Permission.EDIT_POST | Permission.EDIT_TIPS |
                Permission.MOD_CONTENT, False),
        "Admin":(0xffff, False)
    }

    @staticmethod
    def add_role(cases=role_cases):
        """receive a dict like role_cases, add role to db"""
        for r in cases:
            role = Roles.query.filter_by(duty=r).first()
            if role is None:
                role = Roles(duty=r)
            role.permissions = cases[r][0]
            role.default = cases[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Roles %r>' % self.duty

# helper Model for follow Users
class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

class Users(UserMixin, db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    auth_server = db.Column(db.String(32), nullable=False)
    auth_social_id = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    nickname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    links = db.Column(db.String(256))
    #record mission accomplished
    mission = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)

    # n to 1 with Roles
    role_id = db.Column(
        db.Integer, db.ForeignKey('roles.id')
    )

    # 1 to n with Posts
    posts = db.relationship(
        'Posts', backref='creator', lazy='dynamic')
    # 1 to n with Collect for Tips
    tips = db.relationship(
        'Collect', backref='tip_creator', lazy='dynamic')
    # 1 to n with Comments
    comments = db.relationship(
        'Comments', backref='creator', lazy='dynamic')
    # 1 to n with Reviews
    reviews = db.relationship(
        'Reviews', backref='creator', lazy='dynamic')
    # 1 to n with Clips
    clips = db.relationship(
        'Clips', backref='creator', lazy='dynamic')
    # 1 to n with Demands
    demands = db.relationship(
        'Demands', backref='requestor', lazy='dynamic')
    # 1 to n with Events
    events = db.relationship(
        'Events', backref='actor', lazy='dynamic')
    # 1 to n with Articles
    articles = db.relationship(
        'Articles', backref='writer', lazy='dynamic')
    # 1 to n with Columns
    columns = db.relationship(
        'Columns', backref='host', lazy='dynamic')

    # n2n with self for Messages
    # 1 to n with Messages for send
    send_messages = db.relationship(
        'Messages',
        foreign_keys=[Messages.send_id],
        backref=db.backref('sender',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # 1 to n with Messages for receive
    receive_messages = db.relationship(
        'Messages',
        foreign_keys=[Messages.receive_id],
        backref=db.backref('receiver',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Posts for contribute
    contribute_posts = db.relationship(
        'Contribute',
        foreign_keys=[Contribute.user_id],
        backref=db.backref('contributor',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Posts for star
    star_posts = db.relationship(
        'Star',
        foreign_keys=[Star.user_id],
        backref=db.backref('starer',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Posts for challenge
    challenge_posts = db.relationship(
        'Challenge',
        foreign_keys=[Challenge.user_id],
        backref=db.backref('challenger',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Items for flag
    flag_items = db.relationship(
        'Flag',
        foreign_keys=[Flag.user_id],
        backref=db.backref('flager',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Tags for favirate
    fav_tags = db.relationship(
        'Fav',
        foreign_keys=[Fav.user_id],
        backref=db.backref('faver',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with self for follow
    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with self for follow
    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # n2n with Demands for vote
    vote_demands = db.relationship(
        'Dvote',
        foreign_keys=[Dvote.user_id],
        backref=db.backref('voter', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Reviews for vote
    vote_reviews = db.relationship(
        'Rvote',
        foreign_keys=[Rvote.user_id],
        backref=db.backref('voter', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    #init and set role
    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Roles.query.filter_by(permissions=0xffff).\
                           first()
            if self.role is None:
                self.role = Roles.query.filter_by(default=True).first()
    
    # password hashing and token
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None #'valid token expired' # None #    # valid token, but expired
        except BadSignature:
            return None #'invalid token' #None    # invalid token
        user = Users.query.get(data['id'])
        return user
    
    #check the user's permission
    def can(self,permission):
        return self.role is not None and \
              (self.role.permissions & permission) == permission

    #star and unstar a post
    def star(self, post):
        if not self.staring(post):
            s = Star(starer=self, star_post=post)
            db.session.add(s)
            db.session.commit() # need to commit for API??
    def unstar(self, post):
        s = self.star_posts.filter_by(post_id=post.id).first()
        if s:
            db.session.delete(s)
            db.session.commit() # need to commit for API??
    def staring(self, post):
        return self.star_posts.filter_by(
            post_id=post.id).first() is not None

    #challenge a post
    def challenge(self, post):
        if not self.challenging(post):
            c = Challenge(challenger=self, challenge_post=post)
            db.session.add(c)
            db.session.commit() # need to commit for API??
    def unchallenge(self, post):
        c = self.challenge_posts.filter_by(post_id=post.id).first()
        if c:
            db.session.delete(c)
            db.session.commit() # need to commit for API??
    def challenging(self, post):
        return self.challenge_posts.filter_by(
            post_id=post.id).first() is not None

    #follow and unfollow user
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            #db.session.commit()
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            #db.session.commit()
    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None
    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    # flag an item as read, to read or reading
    def flag(self, item, n):
        fl = Flag.query.filter_by(user_id=self.id,item_id=item.id).\
            first()
        if fl:
            fl.flag_label = n
            db.session.add(fl)
        else:
            new_fl = Flag(flager=self, flag_item=item,flag_label=n)
            db.session.add(new_fl)
        # update item's vote
        item.cal_vote()
        db.session.commit() # need to commit for API??
    def flaging(self,item):
        fl = Flag.query.filter_by(user_id=self.id,item_id=item.id).\
            first()
        if fl is None:
            return "Flag It"
        if fl.flag_label == 1:
            return "Scheduled"
        if fl.flag_label == 2:
            return "Working on"
        if fl.flag_label == 3:
            return "Have Done"

    #fav and unfav a tag
    def fav(self, tag):
        if not self.faving(tag):
            fv = Fav(faver=self, fav_tag=tag)
            db.session.add(fv)
            #db.session.commit()
    def unfav(self, tag):
        fv = self.fav_tags.filter_by(tag_id=tag.id).first()
        if fv:
            db.session.delete(fv)
            #db.session.commit()
    def faving(self, tag):
        return self.fav_tags.filter_by(
            tag_id=tag.id).first() is not None

    #save activities to db Events
    def set_event(self,action=None,post=None,item=None,comment=None,\
                       clip=None,review=None,demand=None,tag=None):
        ev = Events(
            actor=self,
            action=action,
            post=post,
            item=item,
            comment=comment,
            clip=clip,
            review=review,
            demand=demand,
            tag=tag
        )
        db.session.add(ev)
        #db.session.commit()

    def accomplished(self):
        pass

    def cal_rank(self,p=None,t=None,r=None,a=None,c=None,d=None,m=None):
        m = m or self.mission*10
        p = p or self.posts.count()*5
        t = t or self.tips.count()*5
        r = r or self.reviews.count()*5
        a = a or self.articles.count()*5
        c = c or self.clips.count()*2
        d = d or self.demands.count()
        self.rank = m+p+t+r+a+c+d
        db.session.add(self)
        #db.session.commit()

    #@cache.memoize(timeout=60*5)#cannot cache,due to n2n lazy opt? to tackle.
    def get_tag_set(self):
        # star posts' Tags
        tag_s = [p.star_post.tags for p in self.star_posts] #2D LIST
        #challenge posts'tags
        tag_c = [p.challenge_post.tags for p in self.challenge_posts] #2D
        #flaged items' Tags
        tag_fg = [i.flag_item.itags for i in self.flag_items] #2D
        #faving tags
        tag_fv = [i.fav_tag for i in self.fav_tags]
        #merge and unduplicated
        tag_all = sum(tag_s + tag_c + tag_fg, tag_fv)
        tag_set = set(tag_all)

        return tag_set,tag_fv

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'name': self.nickname or self.name,
            'role': self.role.duty,
            'avatar': self.avatar,
            'location': self.location,
            'about': self.about_me,
            'followercount': self.followers.count(), 
            'followedcount': self.followed.count(), # following other
            'exlink': self.links,
            'url': '/profile/'+str(self.id)
        }
        return user_dict

    def __repr__(self):
        return '<Users %r>' % (self.name + str(self.id))


class AnonymousUser(AnonymousUserMixin):
    @property
    def id(self):
        id = -1
        return id
    @property
    def nickname(self):
        return None
    @property
    def name(self):
        return None
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
    def staring(self, post):
        return False
    def challenging(self, post):
        return False
    def is_following(self, user):
        return False
    def is_followed_by(self, user):
        return False
    def faving(self, tag):
        return False
    def flaging(self,item):
        return "Flag It"
    @property
    def followed(self):
        return []
    def role(self):
        r = Roles(duty=None,permissions=0x0000)
        return r
    def to_dict(self):
        return None
login_manager.anonymous_user = AnonymousUser


class Authors(db.Model):
    __table_name__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False) # uni maybe an issue
    photo = db.Column(db.String(256))
    link =  db.Column(db.String(256))
    nation = db.Column(db.String(64))
    language = db.Column(db.String(64))
    gender = db.Column(db.String(16))
    birth = db.Column(db.Date)
    age = db.Column(db.String(8))
    about = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

    #n2n with items for byline
    items = db.relationship(
        'Byline',
        foreign_keys=[Byline.author_id],
        backref=db.backref('by',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return '<Authors %r>' % self.name


class Events(db.Model):
    __table_name__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    
    dict_action_content = {
        'create':'post',
        'alter':'post', #edit intro
        'updates':'post', #add item
        'modify':'post', #edit tips
        'star':'post',
        'challenge':'post',
        'comment':'comment',
        'request':'demand',
        'add':'review',
        'endorse':'review',
        'excerpt':'clip',
        'fav':'tag',
        'descript':'tag',
        'edit':'item',  #add item info
        'schedule':'item',
        'working on':'item',
        'get done':'item'
    }

    # n to 1 with Users and others for record activities
    #events - actor
    user_id =  db.Column(
        db.Integer, db.ForeignKey('users.id')
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id')
    )
    comment_id = db.Column(
        db.Integer, db.ForeignKey('comments.id')
    )
    clip_id = db.Column(
        db.Integer, db.ForeignKey('clips.id')
    )
    review_id = db.Column(
        db.Integer, db.ForeignKey('reviews.id')
    )
    item_id = db.Column(
        db.Integer, db.ForeignKey('items.id')
    )
    demand_id = db.Column(
        db.Integer, db.ForeignKey('demands.id')
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey('tags.id')
    )

    # get events, ##need to tacle some issue #if del, the obj is None,error occur 
    # warning: fragile!!
    @property
    def action_content(self):
        act = self.action
        if act in ['create','alter','updates','update','modify','star','challenge']:
            q=self.post
            h=q.title if q else 'No title'
            return ('post',q,h)
        if act in ['edit','schedule','working on','get done']:
            q=self.item
            h=q.title if q else 'No title'
            return ('item',q,h)
        if act in ['add','endorse']:
            q=self.review
            h=q.heading if q else 'No title'
            return ('review',q,h)
        if act in ['fav','descript']:
            q=self.tag
            h=q.tag if q else 'No title'
            return ('tag',q,h)
        if act == 'request':
            q=self.demand
            h=q.body if q else 'No content'
            return ('demand',q,h)
        if act == 'excerpt':
            q=self.clip
            h=q.body if q else 'No content'
            return ('myclips',q.creator,h)

    def __repr__(self):
        return '<Events %r>' % (self.action + str(self.id))


class Articles(db.Model):
    __table_name__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    figure = db.Column(db.String(512))
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    renewal = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # n to 1 with Users
    writer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )
    # n to 1 with Columns
    column_id = db.Column(
        db.Integer,
        db.ForeignKey("columns.id")
    )

    def renew(self):
        self.renewal = datetime.utcnow()
        db.session.add(self)
        #db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Articles %r>' % self.title

db.event.listen(Articles.body, 'set', Articles.on_changed_body)


class Columns(db.Model):
    __table_name__ = "columns"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    intro = db.Column(db.Text)
    figure = db.Column(db.String(512))
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)
    disabled = db.Column(db.Boolean)

    # n to 1 with Users
    host_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # 1 to n with Articles
    articles = db.relationship(
        'Articles', backref='column', lazy='dynamic')

    def __repr__(self):
        return '<Columns %r>' % self.title

#update db
# cd backend
# python manage.py db init
# python manage.py db migrate -m "comment"
# python manage.py db upgrade