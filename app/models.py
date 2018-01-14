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
from . import db, cache
from .utils import split_str, str_to_dict, str_to_set
#from markdown import markdown
#import bleach

# html_tags Whitelist for Bleach
# markdown: comment, clip
# rich text: intro, epilog, tips, review
# now parse markdown in frontend
# allowed_tags = ['a', 'abbr', 'b', 'blockquote', 'code', 'img',
#                 'em', 'i', 'li', 'ol', 'ul', 'pre', 'strong',
#                 'h3', 'h4', 'h5', 'h6', 'hr', 'p']

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
    spoiler = db.Column(db.Boolean, default=False) # if tips spoiler ahead?
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
            'tip':  self.tips,
            'spoiler': self.spoiler
        }
        return tip_dict

#     @staticmethod
#     def on_changed_tips(target, value, oldvalue, initiator):
#         target.tips_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))
# db.event.listen(Collect.tips, 'set', Collect.on_changed_tips)

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
    #flag label: to read-1,reading-2,read-3
    flag_label = db.Column(db.SmallInteger,default=0)
    flag_note = db.Column(db.String(128), default="")
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

# helper for n2n Users vote Clips
class Cvote(db.Model):
    __table_name__ = 'cvote'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    clip_id = db.Column(
        db.Integer,
        db.ForeignKey("clips.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

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
    editing_id = db.Column(db.Integer)
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
    # 1 to n with Circles
    circles = db.relationship(
        'Circles', backref='post', lazy='dynamic')
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

    def collecting(self, item, tips, tip_creator, spoiler=False):
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
                tip_creator=tip_creator,
                spoiler=spoiler
            ) # refer to the relationship-backref var
            db.session.add(c)
            # update item's vote
            item.cal_vote()
            # update the renew timestamp
            self.renew()
            #db.session.commit() #if need commit?

    # set and change the order of items, ## ??maybe an issue here!!##
    def ordering(self,item,new_order):
        _c = self.items  # ie. a collect-object
        c_old = _c.filter_by(item_id=item.id).first()
        old_order = c_old.order
        new_order = int(new_order)

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
    
    #check if can be edited, permission
    def uneditable(self, user):
        if (user != self.creator 
        and self.editable != 'Everyone' 
        and user.role.duty != 'Admin'):
            return True
        else:
            return False

    # lock and unlock status in/after edit: a stopgap
    def lock(self, user):
        # set a start time and id  to indicate in editing
        self.edit_start = datetime.utcnow()
        self.editing_id = user.id
        db.session.add(self)
        db.session.commit()
    def unlock(self):
        # reset eidt_start to None, after edit done
        self.edit_start = None
        self.editing_id = None
        db.session.add(self)
        db.session.commit()
    def force_unlock(self, start=None, timeout=2400):
        # sometime user forget submit, need to force unlock
        start = start or self.edit_start
        if start:
            now = datetime.utcnow()
            delta = now - start
            if delta.seconds >= timeout:
                self.unlock()
    def check_locked(self, userid):
        # if eidt_start is not None, it is locked as editing
        start = self.edit_start
        if start and self.editing_id != userid:
            #force_unlock firstly
            self.force_unlock(start=start)
            return bool(self.edit_start)
        else:
            return False
    def check_editable(self, user):
        """permission and unlocked"""
        is_uneditable = self.uneditable(user)
        is_locked = self.check_locked(user.id)
        can_edit =  (not is_locked) and (not is_uneditable)
        return can_edit

    def renew(self):
        self.renewal = datetime.utcnow()
        db.session.add(self)
        #db.session.commit()

    def cal_vote(self,i=None,s=None,c=None):
        i = i or self.items.count()
        s = s or self.starers.count()
        c = c or self.challengers.count() * 2
        self.vote = i+s+c
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
            item = self.items.all()[m].item
            return item.item_cover

    @staticmethod
    @cache.memoize() #to tackle
    def select_posts():
        _query = Posts.query
        m = current_app.config['POST_PER_PAGE']

        posts_latest = _query.order_by(Posts.renewal.desc()).limit(m)
        posts_popular = _query.order_by(Posts.vote.desc()).limit(m)
        posts_random = _query.order_by(db.func.rand()).limit(m)

        posts_select = posts_latest.union(posts_popular,posts_random).\
                       order_by(db.func.rand())#.all()
        posts = [r.to_dict() for r in posts_select]  #execute here for cache
        return posts

    def to_dict(self):
        creator = self.creator.to_dict()
        #contributes = self.contributors
        #contributors = [i.to_dict() for i in contributes]
        #contributor_id_list = [i.user_id for i in contributes]
        tags = [t.to_dict() for t in self.tags]
        post_dict = {
            'id': self.id,
            'title': self.title,
            'intro': self.intro,
            'credential': self.credential,
            'rating': self.rating,
            'epilog': self.epilog or '',
            'createat': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            # OR .strftime('%Y-%m-%dT%H:%M:%SZ') # as timezone
            #'renewat': self.renewal.strftime('%Y-%m-%d %H:%M:%S'),
            'itemcount': self.items.count(),
            'starcount': self.starers.count(),
            'challengecount': self.challengers.count(),
            'commentcount': self.comments.count(),
            'demandcount': self.demands.count(),
            'cover': self.post_cover,
            'editable': self.editable,
            'creator': creator,
            #'contributors': contributors,
            #'contributoridlist': contributor_id_list,
            'tags': tags
        }
        return post_dict
    
    def __repr__(self):
        return '<Posts %r>' % self.title

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
    edit_start = db.Column(db.DateTime,default=None)
    editing_id = db.Column(db.Integer)

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
            return url_for('static', filename='pic/dpc.svg')
        else:
            return self.cover

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
    
        # lock and unlock status in/after edit item: a stopgap
    def lock(self, user):
        # set a start time and id  to indicate in editing
        self.edit_start = datetime.utcnow()
        self.editing_id = user.id
        db.session.add(self)
        db.session.commit()
    def unlock(self):
        # reset eidt_start to None, after edit done
        self.edit_start = None
        self.editing_id = None
        db.session.add(self)
        db.session.commit()
    def force_unlock(self, start=None, timeout=2400):
        # sometime user forget submit, need to force unlock
        start = start or self.edit_start
        if start:
            now = datetime.utcnow()
            delta = now - start
            if delta.seconds >= timeout:
                self.unlock()
    def check_locked(self, userid):
        # if eidt_start is not None, it is locked as editing
        start = self.edit_start
        if start and self.editing_id != userid:
            #force_unlock firstly
            self.force_unlock(start=start)
            return bool(self.edit_start)
        else:
            return False
    
    def to_dict(self):
        item_dict = {
            'id': self.id,
            'cate': self.cate,
            'title': self.title,
            'uid': self.uid,
            'byline': self.author or '', 
            'rutcount': self.posts.count(),
            'reviewcount': self.reviews.count(),
            'clipcount': self.clips.count(),
            'commentcount': self.comments.count(),
            'cover': self.item_cover,
            'publisher': self.publisher or '',
            'pubdate': self.pub_date or '',
            'language': self.language or '',
            'page': self.page or '',
            'level': self.level or '',
            'binding': self.binding or '',
            'price': self.price or '',
            'resurl': self.res_url or '',
            'details': self.details or ''
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
    edit_start = db.Column(db.DateTime,default=None)
    editing_id = db.Column(db.Integer)

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
        if tag and (not self.parent_is(tag)):
            c = Clan(child_tag=self, parent_tag=tag)
            db.session.add(c)
            #db.session.commit()

    #cache get rand tags
    @staticmethod
    @cache.memoize()
    def get_tags():
        return Tags.query.order_by(Tags.vote.desc()).limit(16).all()

    def cal_vote(self,i=None,p=None,d=None,f=None):
        i = i or self.items.count()
        p = p or self.posts.count()
        d = d or self.demands.count()
        f = f or self.favers.count()
        self.vote = i+p+d+f
        db.session.add(self)
        #db.session.commit()
    
    # lock and unlock status in/after edit tag: a stopgap
    def lock(self, user):
        # set a start time and id  to indicate in editing
        self.edit_start = datetime.utcnow()
        self.editing_id = user.id
        db.session.add(self)
        db.session.commit()
    def unlock(self):
        # reset eidt_start to None, after edit done
        self.edit_start = None
        self.editing_id = None
        db.session.add(self)
        db.session.commit()
    def force_unlock(self, start=None, timeout=600):
        # sometime user forget submit, need to force unlock
        start = start or self.edit_start
        if start:
            now = datetime.utcnow()
            delta = now - start
            if delta.seconds >= timeout:
                self.unlock()
    def check_locked(self, userid):
        # if eidt_start is not None, it is locked as editing
        start = self.edit_start
        if start and self.editing_id != userid:
            #force_unlock firstly
            self.force_unlock(start=start)
            return bool(self.edit_start)
        else:
            return False

    def to_dict(self):
        tag_dict = {
            'id': self.id,
            'tagname': self.tag,
            'descript': self.descript or '',
            'favcount': self.favers.count()
        }
        return tag_dict

    def __repr__(self):
        return '<Tags %r>' % self.tag


# helper Model for Reply comments, can be deprecated?
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

    # n2n with self can be deprecated?
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
    ## end  n2n  with self, can be deprecated?

    def to_dict(self):
        comment_dict = {
            'id': self.id,
            'heading': self.heading or '',
            'body': self.body,
            'vote': self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'creator': {'id': self.creator_id, 'name': self.creator.nickname or self.creator.name},
            'children': [c.to_dict() for c in self.child_comments]
        }
        return comment_dict

    def __repr__(self):
        return '<Coments %r>' % self.body

#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))
# db.event.listen(Comments.body, 'set', Comments.on_changed_body)

# Monkey patched for self reference -reply
Comments.parent_comment_id = db.Column(
    db.Integer, db.ForeignKey("comments.id")
)
Comments.parent_comment = db.relationship(
    'Comments',
    backref='child_comments',
    remote_side=Comments.id
)
# end Monkey patch


class Reviews(db.Model):
    __table_name__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    spoiler = db.Column(db.Boolean, default=False)
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

    def to_dict(self):
        creator = self.creator
        item = self.item
        review_dict = {
            'id': self.id,
            'heading': self.heading,
            'creator': {'id': creator.id, 'name': creator.nickname or creator.name},
            'body': self.body,
            'spoiler': self.spoiler,
            'item': {'id': item.id, 'title': item.title},
            'vote':  self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return review_dict

    def __repr__(self):
        return '<Reviews %r>' % self.heading


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
    # n2n with Users for vote
    voters = db.relationship(
        'Cvote',
        foreign_keys=[Cvote.clip_id],
        backref=db.backref('vote_clip', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def to_dict(self):
        clip_dict = {
            'id': self.id,
            'creator': self.creator.to_dict(),
            'fromitem': self.item.to_dict(),
            'body': self.body,
            'vote': self.vote,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return clip_dict

    def __repr__(self):
        return '<Clips %r>' % self.body
    
#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))
# db.event.listen(Clips.body, 'set', Clips.on_changed_body)


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

    # n2n with Posts, as answer
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
        requestor = self.requestor
        demand_dict = {
            'id': self.id,
            'requestor': {'id': requestor.id, 'name': requestor.nickname or requestor.name},
            'body': self.body,
            'vote': self.vote,
            'tagStr': self.dtag_str or '',
            'answercount': self.posts.count(),
            'commentcount': self.comments.count(),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return demand_dict

    def __repr__(self):
        return '<Demands %r>' % self.body

# helper Model for Users participate Circles
class Participate(db.Model):
    __tablename__ = 'participate'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True)
    circle_id = db.Column(
        db.Integer,
        db.ForeignKey("circles.id"),
        primary_key=True)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow)

class Circles(db.Model):
    __table_name__ = "circles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    area = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    time = db.Column(db.String(256), nullable=False)
    note = db.Column(db.String(256))
    disabled = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime,
                         default=datetime.utcnow)
    # n to 1 relation with Users
    facilitator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )
    # n to 1 with Posts
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id")
    )
    # n2n with Users for participate
    participators = db.relationship(
        'Participate',
        foreign_keys=[Participate.circle_id],
        backref=db.backref('participate_circle', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    def to_dict(self):
        facilitator = self.facilitator
        rut = self.post
        circle_dict = {
            'id': self.id,
            'facilitator': {'id': facilitator.id, 'name': facilitator.nickname or facilitator.name},
            'name': self.name,
            'area': self.area,
            'address': self.address,
            'time': self.time,
            'note': self.note or '',
            'rut': {'id': rut.id, 'title': rut.title},
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return circle_dict
    
    def __repr__(self):
        return '<Circles %r>' % self.name
    

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

class Users(db.Model):
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
    credit = db.Column(db.Integer, default=0)
    incode = db.Column(db.String(12)) #code of who invite me
    recode = db.Column(db.String(12)) #my code to invite other

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
    # 1 to n with Circles
    circles = db.relationship(
        'Circles', backref='facilitator', lazy='dynamic')
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
    
    # n2n with Clips for vote
    vote_clips = db.relationship(
        'Cvote',
        foreign_keys=[Cvote.user_id],
        backref=db.backref('voter', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Demands for vote
    vote_demands = db.relationship(
        'Dvote',
        foreign_keys=[Dvote.user_id],
        backref=db.backref('voter', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    # n2n with Circles for participate
    participate_circles = db.relationship(
        'Participate',
        foreign_keys=[Participate.user_id],
        backref=db.backref('participator', lazy='joined'),
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
    
    # password hashing
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    # confirm and reset psw
    def generate_confirmation_token(self, expiration=24*3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = Users.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    # token auth
    def generate_auth_token(self, exp=1): # unit d
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=exp*24*3600) # unit to s
        return (s.dumps({'id': self.id}), exp)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None #'valid token expired' # None #    # valid token, but expired
        except BadSignature:
            return None #'invalid token' #None    # invalid token
        user = Users.query.get(data.get('id'))
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
            post.cal_vote()
            db.session.commit() # need to commit for API??
    def unstar(self, post):
        s = self.star_posts.filter_by(post_id=post.id).first()
        if s:
            db.session.delete(s)
            post.cal_vote()
            db.session.commit() # need to commit for API??
    def staring(self, post):
        return self.star_posts.filter_by(
            post_id=post.id).first() is not None

    #challenge a post
    def challenge(self, post):
        if not self.challenging(post):
            c = Challenge(challenger=self, challenge_post=post)
            db.session.add(c)
            post.cal_vote()
            db.session.commit() # need to commit for API??
    def unchallenge(self, post):
        c = self.challenge_posts.filter_by(post_id=post.id).first()
        if c:
            db.session.delete(c)
            post.cal_vote()
            db.session.commit() # need to commit for API??
    def challenging(self, post):
        return self.challenge_posts.filter_by(
            post_id=post.id).first() is not None

    #follow and unfollow user
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit() # need to commit for API??
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit() # need to commit for API??
    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None
    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    # flag an item as read, to read or reading
    def flag(self, item, n, note=''):
        fl = Flag.query.filter_by(user_id=self.id,item_id=item.id).\
            first()
        if fl:
            fl.flag_label = n
            fl.flag_note = note
            db.session.add(fl)
        else:
            new_fl = Flag(
                flager=self, 
                flag_item=item,
                flag_label=n,
                flag_note=note
            )
            db.session.add(new_fl)
        # update item's vote
        item.cal_vote()
        db.session.commit() # need to commit for API??

    def flaging(self,item):
        fl = Flag.query.filter_by(user_id=self.id,item_id=item.id).\
            first()
        if fl is None:
            return {'label': 'Flag It', 'note': ''}
        if fl.flag_label == 1:
            return {'label': 'Scheduled', 'note': fl.flag_note}
        if fl.flag_label == 2:
            return {'label': 'Working on', 'note': fl.flag_note}
        if fl.flag_label == 3:
            return {'label': 'Have Done', 'note': fl.flag_note}

    #fav and unfav a tag
    def faving(self, tag):
        return self.fav_tags.filter_by(
            tag_id=tag.id).first() is not None
    def fav(self, tag):
        if not self.faving(tag):
            fv = Fav(faver=self, fav_tag=tag)
            db.session.add(fv)
            tag.cal_vote()
            db.session.commit() #for API??
    def unfav(self, tag):
        fv = self.fav_tags.filter_by(tag_id=tag.id).first()
        if fv:
            db.session.delete(fv)
            tag.cal_vote()
            db.session.commit() #for API??
    
    #participate or not a circle
    def parting(self, circle):
        return self.participate_circles.filter_by(
            circle_id=circle.id).first() is not None
    def participate(self, circle):
        if not self.parting(circle):
            pt = Participate(participator=self, participate_circle=circle)
            db.session.add(pt)
            db.session.commit()
    def unparticipate(self, circle):
        pt = self.participate_circles.filter_by(circle_id=circle.id).first()
        if pt:
            db.session.delete(pt)
            db.session.commit()

    #save activities to db Events
    def set_event(self,action=None,post=None,item=None,comment=None,\
                       clip=None,review=None,demand=None,tag=None):
        query = self.events
        # avoid duplicated entry
        if action in ['Created','Starred','Started challenge']:
            e = query.filter_by(action=action,post_id=post.id).first()
        elif action in ['Scheduled','Working on','Get done']:
            e = query.filter_by(action=action,item_id=item.id).first()
        elif action in ['Followed','Updated Description']:
            e = query.filter_by(action=action,tag_id=tag.id).first()
        elif action in ['Posted','Endorsed']:
            e = query.filter_by(action=action,review_id=review.id).first()
        elif action in ['Send','Voted']:
            e = query.filter_by(action=action,demand_id=demand.id).first()
        else:
            return None
        if e:
            return None
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

    def cal_credit(self,p=None,t=None,r=None,a=None,c=None,d=None,m=None):
        m = m or self.mission*10
        p = p or self.posts.count()*5
        t = t or self.tips.count()*5
        r = r or self.reviews.count()*5
        a = a or self.articles.count()*5
        c = c or self.clips.count()*2
        d = d or self.demands.count()
        self.credit = m+p+t+r+a+c+d
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
    # set avatar
    @property
    def user_avatar(self):
        avatar = self.avatar
        if not avatar or not avatar.strip():
            return url_for('static', filename='pic/profile.svg')
        return avatar

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'name': self.nickname or self.name,
            'nickname': self.nickname or '',
            'username': self.name,
            'role': self.role.duty,
            'confirmed': self.confirmed,
            'avatar': self.user_avatar,
            'location': self.location or '',
            'about': self.about_me or '',
            'followercount': self.followers.count(), 
            'followedcount': self.followed.count(), # following other
            'exlink': self.links or '',
            'incode': self.incode,
            'recode': self.recode
        }
        return user_dict

    def __repr__(self):
        return '<Users %r>' % (self.name + str(self.id))

# can be deleted??
class AnonymousUser():
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
#login_manager.anonymous_user = AnonymousUser


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
        content_dict = {}
        if act in ['Created','Starred','Started challenge']:
            q = self.post
            if q:
                content_dict = {
                    'type': 'readuplist',
                    'id': q.id,
                    'content': q.title
                }
        if act in ['Scheduled','Working on','Get done']:
            q=self.item
            if q:
                content_dict = {
                    'type': 'item',
                    'id': q.id,
                    'content': q.title
                }
        if act in ['Posted','Endorsed']:
            q=self.review
            if q:
                content_dict = {
                    'type': 'review',
                    'id': q.id,
                    'content': q.heading
                }
        if act in ['Followed','Updated Description']:
            q=self.tag
            if q:
                content_dict = {
                    'type': 'tag',
                    'id': q.id,
                    'content': q.tag
                }
        if act in ['Send','Voted']:
            q=self.demand
            if q:
                content_dict = {
                    'type': 'demand',
                    'id': q.id,
                    'content': q.body
                }
        return content_dict

    def to_dict(self):
        actor = {'id': self.actor.id, 'name': self.actor.name, 'avatar': self.actor.user_avatar}
        event_dict = {
            'actor': actor,
            'action': self.action,
            'event': self.action_content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        return event_dict

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
    
    def __repr__(self):
        return '<Articles %r>' % self.title

    # @staticmethod
    # def on_changed_body(target, value, oldvalue, initiator):
    #     target.body_html = bleach.linkify(bleach.clean(
    #         markdown(value, output_format='html'),
    #         tags=allowed_tags, strip=True))
# db.event.listen(Articles.body, 'set', Articles.on_changed_body)


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