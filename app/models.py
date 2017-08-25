# -*- coding: utf-8 -*-

import random
import re
from datetime import datetime, date
from flask import url_for, current_app, request
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, AnonymousUserMixin
from markdown import markdown
import bleach
from .import db, login_manager
from .utils import split_str, str_to_dict, str_to_set


# html_tags Whitelist for Bleach
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'h4','h5','p']

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
    timestamp = db.Column(db.DateTime, 
                          default=datetime.utcnow)
    update = db.Column(db.DateTime, 
                          default=datetime.utcnow)
    editable = db.Column(db.String(32),default='Creator')
    disabled = db.Column(db.Boolean)

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
        '''
        check if there is a record in Collect table,
        record indicates post linking item 
        return True or False
        '''
        return self.items.filter_by(item_id=item.id).first() is not None 

    def collecting(self, item, tips, tip_creator):
        '''
        collect item into post, 
        ie. add a record into Collect table
        '''
        if not self.collected(item):
            c = Collect(
                post=self,
                item=item,
                order=self.items.count()+1,
                tips=tips,
                tip_creator=tip_creator
            ) # refer to the relationship-backref var
            db.session.add(c)
            db.session.commit() #if need commit?

    # set and change the order of items, ##maybe an issue here##
    def ordering(self,item,new_order):

        _c = self.items  # ie. a collect-object
        c_old = _c.filter_by(item_id=item.id).first()
        old_order = c_old.order

        if new_order == old_order:
            pass
        else:            
            if new_order > old_order:
                for i in range(old_order+1,new_order+1):
                    c = _c.filter_by(order=i).first()
                    c.order = i-1
                    db.session.add(c)
            
            if new_order < old_order:                 
                for i in range(new_order,old_order):
                    c = _c.filter_by(order=i).first()
                    c.order = i+1
                    db.session.add(c)

            c_old.order = new_order
            db.session.add(c_old)
            db.session.commit()

            
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
                    db.session.add(tag)
                else:
                    _tag.posts.append(self)  
                    db.session.add(_tag)
        db.session.commit() 

    def up_time(self):
        self.update = datetime.utcnow()
        db.session.add(self)
        db.session.commit()  

    # set logo cover of  post 
    @property    
    def post_cover(self):
        n = self.items.count()
        if n ==0:
            return url_for('static', filename='pic/dpc.svg')
        else:
            m = random.randrange(n)
            return self.items.all()[m].item.cover

    @staticmethod
    def on_changed_intro(target, value, oldvalue, initiator):
        target.intro_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Posts %r>' % self.title

db.event.listen(Posts.intro, 'set', Posts.on_changed_intro)


class Items(db.Model):
    __table_name__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    res_url = db.Column(db.String(512))
    uid = db.Column(db.String(64), unique=True, nullable=False)  #isbn13 etc.
    isbn10 = db.Column(db.String(32), unique=True)
    asin = db.Column(db.String(32), unique=True)
    author = db.Column(db.String(512)) # or instructor
    cover = db.Column(db.String(512))
    cate = db.Column(db.String(16),default='Book')
    publisher = db.Column(db.String(256))
    pub_date = db.Column(db.String(64)) # or start date
    language = db.Column(db.String(256))
    binding = db.Column(db.String(32))
    page = db.Column(db.String(32)) # book page or length of course
    level = db.Column(db.String(32))
    price = db.Column(db.String(32))
    details = db.Column(db.Text)
    itag_str = db.Column(db.String(512))
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
                elif _tag.items.filter_by(id=self.id).first() is None:
                    _tag.items.append(self)  
                    db.session.add(_tag)
        db.session.commit()

    # add author to db
    def author_to_db(self,s=None):
        author_str = s or self.author
        d = str_to_dict(author_str)
        ''' 
        lst = split_str(author_str)
        d = {}
        for i in lst:
            i_lst = split_str(i,r'[()（）]')
            alst = [a.strip() for a in i_lst if a.strip()]+['Author']
            name = alst[0]
            contribution = alst[1]
            d.setdefault(name,contribution) 
        '''
        
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
        db.session.commit()
    
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
            db.session.commit()
    
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
        db.session.commit()

    def __repr__(self):
        return '<Coments %r>' % self.body 


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
                    db.session.add(tag)
                else:
                    _tag.demands.append(self)  
                    db.session.add(_tag)
        db.session.commit()   
    
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
        db.session.commit()

    def __repr__(self):
        return '<Messages %r>' % self.content


class Permission:
    COMMENT = 0x0001
    SCFFF = 0x0002  # STAR,CHALLENGE,FAV,FLAG,FOLLOW
    POST = 0x0004
    ADD_ITEM = 0x0008
    ADD_TIPS = 0x0010
    EDIT_POST = 0x0020
    EDIT_ITEM = 0x0040
    EDIT_TIPS = 0x0080 
    ADD_DEMAND = 0x0100
    MOD_COMMENT =0x2000
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

    # for add roles
    role_cases ={
        "user":(Permission.COMMENT | Permission.SCFFF | 
                Permission.POST | Permission.ADD_ITEM | 
                Permission.ADD_TIPS | Permission.EDIT_POST | 
                Permission.EDIT_ITEM | Permission.EDIT_TIPS | 
                Permission.ADD_DEMAND, 
                True),
        "moderator":(Permission.COMMENT | Permission.SCFFF | 
                    Permission.POST | Permission.ADD_ITEM | 
                    Permission.ADD_TIPS | Permission.EDIT_POST | 
                    Permission.EDIT_ITEM | Permission.EDIT_TIPS | 
                    Permission.ADD_DEMAND | Permission.MOD_COMMENT, 
                    False), 
        "Admin":(0xffff, False)               
    }

    @staticmethod
    def add_role(cases=role_cases):
        '''receive a dict like role_cases, add role to db'''
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
    name = db.Column(db.String(128), nullable=False)   
    email = db.Column(db.String(128))   
    avatar = db.Column(db.String(512))   
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    nickname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    links = db.Column(db.String(64))

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

    #check the user's permission
    def can(self,permission):
        return self.role is not None and \
              (self.role.permissions & permission) == permission

    #star and unstar a post
    def star(self, post):
        if not self.staring(post):
            s = Star(starer=self, star_post=post)
            db.session.add(s)
            db.session.commit()
    def unstar(self, post):
        s = self.star_posts.filter_by(post_id=post.id).first()
        if s:
            db.session.delete(s)
            db.session.commit()
    def staring(self, post):
        return self.star_posts.filter_by(
            post_id=post.id).first() is not None

    #challenge a post
    def challenge(self, post):
        if not self.challenging(post):
            c = Challenge(challenger=self, challenge_post=post)
            db.session.add(c)
            db.session.commit()
    def unchallenge(self, post):
        c = self.challenge_posts.filter_by(post_id=post.id).first()
        if c:
            db.session.delete(c)
            db.session.commit()
    def challenging(self, post):
        return self.challenge_posts.filter_by(
            post_id=post.id).first() is not None
        
    #follow and unfollow user
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit()
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()
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
        db.session.commit()
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
            db.session.commit()
    def unfav(self, tag):
        fv = self.fav_tags.filter_by(tag_id=tag.id).first()
        if fv:
            db.session.delete(fv)
            db.session.commit()
    def faving(self, tag):
        return self.fav_tags.filter_by(
            tag_id=tag.id).first() is not None

 
    def __repr__(self):
        return '<Users %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    @property
    def id(self):
        id = -1
        return id

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

    def role(self):
        r = Roles(duty=None,permissions=0x0000)
        return r

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
    date = db.Column(db.Date, default=date.today)
    timestamp = db.Column(db.DateTime, 
                          default=datetime.utcnow)
    
    # n to 1 with Users and others for record activities
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

    def __repr__(self):
        return '<Events %r>' % self.action


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
    update = db.Column(db.DateTime, 
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
    
    def up_time(self):
        self.update = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

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