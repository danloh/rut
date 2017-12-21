# -*- coding: utf-8 -*-
# rut is readup tips,included an item list and tips for each item
# here are the resource w/o auth needed 

import random
import re
from flask import g, render_template, redirect, url_for, current_app,\
                  request, session, flash, make_response, abort
from flask_login import login_required, current_user
from flask_restful import abort
from flask_sqlalchemy import get_debug_queries
#from sqlalchemy import or_
from . import api, Resource
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

class Rut(Resource):  #
    def get(self,rutid):
        rut = Posts.query.get_or_404(rutid)
        rut_dict = rut.to_dict()
        #attach tips and items included in rut 
        tips = [t.to_dict() for t in rut.items]  # in Collect model
        # sort tips per order-key in collect-dict
        from operator import itemgetter
        order_tips = sorted(tips, key=itemgetter('order'))
        rut_dict['tips'] = order_tips
        return rut_dict

class Tag(Resource):  #
    def get(self,tagid):
        tag = Tags.query.get_or_404(tagid)
        tag_dict = tag.to_dict()
        #attach ruts included in tag 
        tagruts = [p.to_dict() for p in tag.posts]
        tagruts.reverse()  # as order_by, which is faster?
        tag_dict['ruts'] = tagruts
        tag_dict['total'] = len(tagruts)
        # related tags
        parent_tags = [t.parent_tag for t in tag.parent_tags.\
                    order_by(db.func.rand()).limit(5)]
        tags = parent_tags
        for tg in parent_tags:
            child_tags = [t.child_tag for t in Clan.query.\
                    filter_by(parent_tag_id=tg.id).\
                    order_by(db.func.rand()).limit(5)]
            tags += child_tags   
        tag_dict['tags'] = [{'tagid': t.id,'tagname': t.tag} for t in tags] 
        return tag_dict

class Item(Resource):
    def get(self,itemid):
        item = Items.query.get_or_404(itemid)
        item_dict = item.to_dict()
        # attach reviews
        reviews = item.reviews
        hotreviews = reviews.order_by(Reviews.vote.desc())
        newreviews = reviews.order_by(Reviews.timestamp.desc()).limit(15)
        hot_reviews = [r.to_dict() for r in hotreviews]
        new_reviews = [r.to_dict() for r in newreviews]
        item_dict['hotreviews'] = hot_reviews
        item_dict['newreviews'] = new_reviews
        # attach included ruts
        ruts = [c.post for c in item.posts.order_by(Collect.timestamp.desc())]
        included_ruts = [{'id':r.id, 'title': r.title} for r in ruts]
        item_dict['inruts'] = included_ruts
        return item_dict


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
            prev = url_for(
                'rest.clipz', 
                userid=userid, 
                itemid=itemid, 
                page=page-1, 
                _external=True
            )
        more = None
        if pagination.has_next:
            more = url_for(
                'rest.clipz', 
                userid=userid, 
                itemid=itemid, 
                page=page+1, 
                _external=True
            )
        return {
            'clips': [c.to_dict() for c in clips],
            'prev': prev,
            'more': more,
            'total': pagination.total
        }

class Demandz(Resource):
    def get(self, userid=None, ref=None):
        query = q = Demands.query
        if userid:
            query = q.filter_by(requestor_id=int(userid))
        if ref == "new":
            demands = query.order_by(Demands.timestamp.desc())
        else:
            demands = query.order_by(Demands.vote.desc())
        return {
            'demands': [d.to_dict() for d in demands],
            'total': demands.count()
        }

class Commentz(Resource):

    def get(self):
        rid = request.args.get('rid','')
        ref = request.args.get('ref','')
        q = Comments.query
        if ref == 'creator':
            query = q.filter_by(creator_id=rid)
        if ref == 'post':
            query = q.filter_by(post_id=rid)
        if ref == 'item':
            query = q.filter_by(item_id=rid)
        if ref == 'demand':
            query = q.filter_by(demand_id=rid)
        if ref == 'review':
            query = q.filter_by(review_id=rid)
        #pagination 
        page = request.args.get('page', 1, type=int)
        pagination = query.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=PER_PAGE,
                    error_out=False
                )
        comments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for(
                'rest.commentz',
                rid=rid,
                ref=ref,
                page=page-1, 
                _external=True
            )
        more = None
        if pagination.has_next:
            more = url_for(
                'rest.commentz', 
                rid=rid,
                ref=ref,
                page=page+1, 
                _external=True
            )
        return {
            'comments': [c.to_dict() for c in comments],
            'prev': prev,
            'more': more,
            'total': pagination.total
        }

class User(Resource):
    #method_decorators = [login_required]
    def get(self):
        guser = current_user #Users.query.get(4)
        ref = request.args.get('ref','actived')
        if ref == 'verify':
            user_dict = {
                'userid': guser.id,
                'username': guser.nickname or guser.name
            }
            return user_dict
        else:
            return guser.to_dict()
    
class Rutz(Resource):

    def get(self):
        # per the request ref: 
        # create,star,chalenge,contribute
        userid = request.args.get('userid','')
        ref = request.args.get('ref','random')
        if userid:
            user = Users.query.get_or_404(userid)
            if ref == 'create':
                q = [user.posts] # a query list
            elif ref == 'star':
                q = [s.star_post for s in user.star_posts] 
            elif ref == 'challenge':
                q = [c.challenge_post for c in user.challenge_posts] 
            elif ref == 'contribute':
                q = [c.contribute_post for c in user.contribute_posts] 
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
            prev = url_for(
                'rest.ruts', 
                userid=userid, 
                ref=ref, 
                page=page-1, 
                _external=True
            )
        more = None
        if pagination.has_next:
            more = url_for(
                'rest.ruts', 
                userid=userid, 
                ref=ref, 
                page=page+1, 
                _external=True
            )
        return {
            'ruts': [r.to_dict() for r in ruts],
            'prev': prev,
            'more': more,
            'total': pagination.total
        }

