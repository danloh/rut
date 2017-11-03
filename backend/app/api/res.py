# -*- coding: utf-8 -*-

import random
import re
from flask import g, render_template, redirect, url_for, current_app,\
                  request, session, flash, make_response, abort
from flask_login import login_required, current_user
from flask_restful import abort
from flask_sqlalchemy import get_debug_queries
#from sqlalchemy import or_
from . import api, Resource
from .forms import PostForm, ItemForm, EditItemForm, SelectAddForm,\
                   TagForm, EditPostForm, EpilogForm, EditTipsForm, CommentForm,\
                   TagStrForm, ClipForm, ArticleForm, SelectDoneForm,\
                   DeadlineForm, DemandForm, ReviewForm, CheckItemForm, EditProfileForm
from .. import db
from ..models import Posts, Items, Collect, Tags, Clan, Fav, tag_post, tag_item,\
                     Comments, Reviews, Clips, Demands, tag_demand, Reply,\
                     Star, Flag, Challenge, Contribute, Respon, Rvote, Dvote,\
                     Users, Follow, Roles, Permission, Articles, Columns,\
                     Authors, Byline, Messages, Dialog, Events
from ..decorators import admin_required, permission_required
from ..utils import split_str, str_to_dict, str_to_set
from ..bot import spider


PER_PAGE = 20

class User(Resource):
    method_decorators = [login_required]

    def get(self):
        guser = current_user
        ref = request.args.get('ref','actived')
        if ref == 'verify':
            user = {
                'userid': guser.id,
                'username': guser.nickname or guser.name
            }
            return user
        else:
            return guser.to_dict()
    
class Ruts(Resource):

    def get(self):
        # per he request ref: 
        # create,star,chalenge,contribute
        userid = request.args.get('userid','')
        ref = request.args.get('ref','random')

        if userid:
            user = Users.query.get_or_404(userid)
            if ref == 'create':
                q = [user.posts]
            elif ref == 'star':
                q = [s.star_post for s in user.star_posts] # a query list
            elif ref == 'challenge':
                q = [c.challenge_post for c in user.challenge_posts] # a query list
            elif ref == 'contribute':
                q = [c.contribute_post for c in user.contribute_posts] # a query list
            else:
                #get related tags set and fav tags, from cached Model-func
                tag_set, tag_fv = user.get_tag_set()
                # get followed posts queries
                post_fo = [f.followed.posts for f in current_user.followed]
                #list the queries, followed _posts as init 
                q = post_fo
                for tag_obj in tag_set:
                    q.append(tag_obj.posts)
        else:
            q = [Posts.select_posts()]
        
        q_rand = Posts.query.limit(0)
        query = q_rand.union(*q)

        #pagination 
        page = request.args.get('page', 1, type=int)
        pagination = query.order_by(Posts.timestamp.desc()).\
                paginate(
                    page,
                    per_page=PER_PAGE,
                    error_out=False
                )
        ruts = pagination.items
        
        prev = None
        if pagination.has_prev:
            prev = url_for('rest.ruts', userid=userid, ref=ref, page=page-1, _external=True)
        more = None
        if pagination.has_next:
            more = url_for('rest.ruts', userid=userid, ref=ref, page=page+1, _external=True)
        return {
            'ruts': [r.to_dict() for r in ruts],
            'prev': prev,
            'more': more,
            'total': pagination.total
        }

class Rut(Resource):

    def get(self,rutid):
        rut = Posts.query.get_or_404(rutid)
        rut_dict = rut.to_dict()
        tips = [t.to_dict() for t in rut.items]
        rut_dict['tips'] = tips
        return rut_dict

class Clipz(Resource):

    def get(self):
        userid = request.args.get('userid','')
        itemid = request.args.get('itemid','')
        q = Clips.query
        if userid and itemid:
            query =q.filter_by(creator_id=userid,item_id=itemid)
        elif userid:
            query = q.filter_by(creator_id=userid)
        elif itemid:
            query = q.filter_by(item_id=itemid)
        else:
            query = q
        
        #pagination 
        page = request.args.get('page', 1, type=int)
        pagination = query.order_by(Clips.timestamp.desc()).\
                paginate(
                    page,
                    per_page=PER_PAGE,
                    error_out=False
                )
        clips = pagination.items
        
        prev = None
        if pagination.has_prev:
            prev = url_for('rest.clipz', userid=userid, itemid=itemid, page=page-1, _external=True)
        more = None
        if pagination.has_next:
            more = url_for('rest.clipz', userid=userid, itemid=itemid, page=page+1, _external=True)
        return {
            'clips': [c.to_dict() for c in clips],
            'prev': prev,
            'more': more,
            'total': pagination.total
        }














