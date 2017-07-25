# -*- coding: utf-8 -*-

import random
from datetime import datetime
from flask import url_for, current_app, request
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, AnonymousUserMixin
from .import db, login_manager


tag_post = db.Table('tag_post',  # simple n2n tag with posts 
        db.Column('tag_id', db.Integer, db.ForeignKey("tags.id")),
        db.Column('post_id', db.Integer, db.ForeignKey("posts.id"))
        )
tag_item = db.Table('tag_item',  # simple n2n tag with items 
        db.Column('tag_id', db.Integer, db.ForeignKey("tags.id")),
        db.Column('item_id', db.Integer, db.ForeignKey("items.id"))
        )
tag_demand = db.Table('tag_demand',  # simple n2n tag with demands 
        db.Column('tag_id', db.Integer, db.ForeignKey("tags.id")),
        db.Column('demand_id', db.Integer, db.ForeignKey("demands.id"))
        )
author_item = db.Table('author_item',  # simple n2n tag with item 
        db.Column('author_id', db.Integer, db.ForeignKey("authors.id")),
        db.Column('item_id', db.Integer, db.ForeignKey("items.id"))
        )

class Collect(db.Model): 
    __table_name__ = 'collect'   # helper Model for n2n  posts with items
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) ##??
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), 
                        primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), 
                        primary_key=True)
    order = db.Column(db.Integer)   #item's order in post
    tips = db.Column(db.Text, nullable=False)
    tip_creator_id = db.Column(db.Integer, db.ForeignKey("users.id")) # n to 1 with Users
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class Star(db.Model): 
    __table_name__ = 'star'   # helper Model for n2n  posts with users for star
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), 
                        primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), 
                        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Challenge(db.Model): 
    __table_name__ = 'challenge'   # helper Model for n2n  posts with users for challenge
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), 
                        primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), 
                        primary_key=True)
    deadline = db.Column(db.Date)
    done = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
     
class Flag(db.Model): 
    __table_name__ = 'flag'      # helper Model for n2n  users with items
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), 
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), 
                        primary_key=True)
    flag_label = db.Column(db.Integer,default=0) #label to read-1,reading-2,read-3
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Fav(db.Model): 
    __table_name__ = 'fav'      # helper Model for n2n  users with tags
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), 
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), 
                        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

class Posts(db.Model):
    __table_name__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    credential = db.Column(db.Text)
    rating = db.Column(db.String(32))
    tag_str = db.Column(db.String(256), default="42")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # n to 1 with Users
    
    comments = db.relationship('Comments', backref='post', lazy='dynamic') # 1 to n with Comments

    starers = db.relationship('Star',                          # n2n with Users for star
                                foreign_keys=[Star.post_id],
                                backref=db.backref('star_post',lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    challengers = db.relationship('Challenge',                          # n2n with Users for challenge
                                foreign_keys=[Challenge.post_id],
                                backref=db.backref('challenge_post',lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    items = db.relationship('Collect',                              # n2n with Items
                            foreign_keys=[Collect.post_id],
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
        collect item into post, ie. add a record into Collect table
        '''
        if not self.collected(item):
            c = Collect(post=self,item=item,order=self.items.count()+1,
                        tips=tips,tip_creator=tip_creator) # refer to the relationship-backref var
            db.session.add(c)
            db.session.commit() #if need commit?

    # set and change the order of items
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
        _tagset = set(t.strip() for t in self.tag_str.split(','))
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip()
            if _tg is not "":
                _tag = _query.filter_by(tag=_tg).first()
                if _tag is None:
                    tag=Tags(tag=_tg)
                    tag.posts.append(self)  
                    db.session.add(tag)
                else:
                    _tag.posts.append(self)  
                    db.session.add(_tag)
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

    def __repr__(self):
        return '<Posts %r>' % self.title


class Items(db.Model):
    __table_name__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    res_url = db.Column(db.String(256))
    uid = db.Column(db.String(64), unique=True, nullable=False)
    author = db.Column(db.String(128))
    translator = db.Column(db.String(128))
    cover = db.Column(db.String(256))
    cate = db.Column(db.String(32))
    publisher = db.Column(db.String(128))
    language = db.Column(db.String(32))
    details = db.Column(db.Text)
    itag_str = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comments',backref='item',lazy='dynamic') # 1 to n with Comments

    posts = db.relationship('Collect',                                   # n2n with Posts
                            foreign_keys=[Collect.item_id],
                            backref=db.backref('item', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    
    flagers = db.relationship('Flag',
                              foreign_keys=[Flag.item_id],
                              backref=db.backref('flag_item',lazy='joined'),
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

    # add item tags to database        
    def itag_to_db(self):
        '''
        split the input tags to seperated tag,
        and add them into Tags Table
        '''
        #_taglist = self.itag_str.split(',')
        _tagset = set(t.strip() for t in self.itag_str.split(','))
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip()
            if _tg is not "":
                _tag = _query.filter_by(tag=_tg).first()
                if _tag is None:
                    tag=Tags(tag=_tg)
                    tag.items.append(self)  
                    db.session.add(tag)
                elif _tag.items.filter_by(id=self.id).first() is None:
                    _tag.items.append(self)  
                    db.session.add(_tag)
        db.session.commit()


    def __repr__(self):
        return '<Items %r>' % self.title

class Clan(db.Model):
    __tablename__ = 'clan'
    parent_tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),
                            primary_key=True)
    child_tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Tags(db.Model):
    __table_name__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), nullable=False, unique=True)  
    descript = db.Column(db.String(320))

    favers = db.relationship('Fav',       # n2n with users
                              foreign_keys=[Fav.tag_id],
                              backref=db.backref('fav_tag',lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    posts = db.relationship('Posts',      # simple n2n relationship with Posts
                            secondary=tag_post,
                            backref=db.backref('tags', lazy='joined'),
                            lazy='dynamic')

    items = db.relationship('Items',      # simple n2n relationship with items
                            secondary=tag_item,
                            backref=db.backref('itags', lazy='joined'),
                            lazy='dynamic')

    demands = db.relationship('Demands',      # simple n2n relationship with demands
                            secondary=tag_demand,
                            backref=db.backref('dtags', lazy='joined'),
                            lazy='dynamic')


    parent_tags = db.relationship('Clan',
                               foreign_keys=[Clan.child_tag_id],
                               backref=db.backref('child_tag', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    child_tags = db.relationship('Clan',
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


class Reply(db.Model):
    __tablename__ = 'reply'
    parent_commt_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                            primary_key=True)
    child_commt_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Comments(db.Model):
    __table_name__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    vote = db.Column(db.Integer,default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # n to 1   with Users
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))  # n to 1  with Posts
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))  # n to 1   with Items
    demand_id = db.Column(db.Integer, db.ForeignKey("demands.id"))  # n to 1 with demands

    parent_commts = db.relationship('Reply',
                               foreign_keys=[Reply.child_commt_id],
                               backref=db.backref('child_commt', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    child_commts = db.relationship('Reply',
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


class Demands(db.Model):
    __table_name__ = "demands"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    vote = db.Column(db.Integer,default=1)
    dtag_str = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comments',backref='demand',lazy='dynamic') # 1 to n with Comments

    requestor_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # n to 1 relation with Users

    def dtag_to_db(self):
      
        #_taglist = self.dtag_str.split(',')
        _tagset = set(t.strip() for t in self.dtag_str.split(','))
        _query = Tags.query
        for _tg in _tagset:
            #_tg = _tg.strip()
            if _tg is not "":
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
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('Users', backref='role', lazy='dynamic')  #1 to n with Users

    # for add roles
    role_cases ={
        "user":(Permission.COMMENT | Permission.SCFFF | Permission.POST | 
                Permission.ADD_ITEM | Permission.ADD_TIPS | Permission.EDIT_POST | 
                Permission.EDIT_ITEM | Permission.EDIT_TIPS | Permission.ADD_DEMAND, 
                True),
        "moderator":(Permission.COMMENT | Permission.SCFFF | Permission.POST | 
                    Permission.ADD_ITEM | Permission.ADD_TIPS | Permission.EDIT_POST | 
                    Permission.EDIT_ITEM | Permission.EDIT_TIPS | Permission.ADD_DEMAND | 
                    Permission.MOD_COMMENT, 
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

class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Users(UserMixin, db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    auth_server = db.Column(db.String(32), nullable=False)      
    auth_social_id = db.Column(db.String(64), nullable=False)   
    name = db.Column(db.String(64), nullable=False)   
    email = db.Column(db.String(128))   
    avatar = db.Column(db.String(256))   
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    nickname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    links = db.Column(db.String(64))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # n to 1 with Roles
    posts = db.relationship('Posts', backref='creator', lazy='dynamic')  # 1 to n with Posts 
    tips = db.relationship('Collect', backref='tip_creator', lazy='dynamic')  # 1 to n with Collect for Tips 
    comments = db.relationship('Comments', backref='creator', lazy='dynamic')  # 1 to n with Comments 
    demands = db.relationship('Demands', backref='requestor', lazy='dynamic')  # 1 to n with Demands

    star_posts = db.relationship('Star',                         # n2n with Posts for star
                                 foreign_keys=[Star.user_id],
                                 backref=db.backref('starer',lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')
    
    challenge_posts = db.relationship('Challenge',               # n2n with Posts for challenge
                                 foreign_keys=[Challenge.user_id],
                                 backref=db.backref('challenger',lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')
    
    flag_items = db.relationship('Flag',
                              foreign_keys=[Flag.user_id],
                              backref=db.backref('flager',lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    
    fav_tags = db.relationship('Fav',
                              foreign_keys=[Fav.user_id],
                              backref=db.backref('faver',lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    

    #init and set role
    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Roles.query.filter_by(permissions=0xffff).first()
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
            f = Follow(follower=self, followed=user)
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
    def flag(self, item,n):
        fl = Flag.query.filter_by(user_id=self.id, item_id=item.id).first()
        if fl:
            fl.flag_label = n
            db.session.add(fl)
        else:
            new_fl = Flag(flager=self, flag_item=item, flag_label=n)
            db.session.add(new_fl)
        db.session.commit()
    def flaging(self,item):
        fl = Flag.query.filter_by(user_id=self.id, item_id=item.id).first()
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
    name = db.Column(db.String(64), nullable=False)    
    photo = db.Column(db.String(256)) 
    link =  db.Column(db.String(256))
    nation = db.Column(db.String(64))
    language = db.Column(db.String(64))
    gender = db.Column(db.String(16))
    age = db.Column(db.String(8))
    about = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('Items',      # simple n2n relationship with items
                            secondary=author_item,
                            backref=db.backref('authors', lazy='joined'),
                            lazy='dynamic')

    def __repr__(self):
        return '<Authors %r>' % self.name




