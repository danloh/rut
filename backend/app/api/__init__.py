# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, redirect, url_for, request, g, jsonify
from flask_login import login_required, current_user
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from .. import db
from ..models import *

rest = Blueprint('rest', __name__)
api = Api(rest)

auth = HTTPBasicAuth()

from . import res

PER_PAGE = 2

#api.add_resource(res.User, '/user')
#api.add_resource(res.Rutz, '/ruts')
api.add_resource(res.Rut, '/rut/<int:rutid>')  #
api.add_resource(res.Tag, '/tag/<int:tagid>')  #
#api.add_resource(res.Clipz, '/clips')
#api.add_resource(res.Demandz, '/demands')
#api.add_resource(res.Item, '/item/<int:itemid>')
#api.add_resource(res.Commentz, '/comments')

# for user authentication
@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if Users.query.filter_by(name = username).first() is not None:
        abort(400) # existing user
    user = Users(
        name = username,
        auth_server = "Registered",
        auth_social_id = "00001"
    )
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.name, 'userid': user.id })

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True

@rest.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({
        'token': token.decode('ascii'),
        'user': g.user.to_dict()
    })

@rest.route('/user')
@auth.login_required
def get_user():
    guser = g.user
    ref = request.args.get('ref','actived')
    if ref == 'verify':
        user_dict = {
            'id': guser.id,
            'username': guser.nickname or guser.name
        }
        return jsonify(user_dict)
    else:
        return jsonify(guser.to_dict())

@rest.route('/ruts')
@auth.login_required
def get_ruts():
    user = g.user
    ref = request.args.get('ref','random')
    #get related tags set and fav tags
    tag_set, tag_fv = user.get_tag_set()
    if ref == 'create':
        q = [user.posts] # a query list
    elif ref == 'star':
        q = [s.star_post for s in user.star_posts]
    elif ref == 'challenge':
        q = [c.challenge_post for c in user.challenge_posts]
    elif ref == 'contribute':
        q = [c.contribute_post for c in user.contribute_posts]
    else:
        # get followed posts queries
        post_fo = [f.followed.posts for f in user.followed]
        #list the queries, followed _posts as init 
        q = post_fo
        for tag_obj in tag_set:
            q.append(tag_obj.posts)
    q_rand = Posts.query.limit(0)
    ruts = query = q_rand.union(*q)
    
    return jsonify({  # need to optimize
        'ruts': [r.to_dict() for r in ruts],
        'total': ruts.count(),
        'tags': [{'tagid': t.id,'tagname': t.tag} for t in tag_set]   
    })

@rest.route('/create')
@auth.login_required
def new_rut():
    post = Posts(
        creator = g.user,
        title = request.json.get('title'),
        intro = request.json.get('intro'),
        tag_str = request.json.get('tag'),
        rating = request.json.get('rating'),
        credential = request.json.get('credential'),
        editable = request.json.get('editable')
    )
    db.session.add(post)
    post.tag_to_db()
    db.session.commit()
    return jsonify(post.to_dict())

@rest.route('/clips')
@auth.login_required
def get_clips():
    user = g.user
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    ref = request.args.get('ref','')
    q = Clips.query
    if userid and itemid:
        query =q.filter_by(creator_id=userid,item_id=itemid)
    elif userid:
        query = q.filter_by(creator_id=userid)
    elif itemid:
        query = q.filter_by(item_id=itemid)
    elif ref == "All":
        query = q.filter(creator_id != user.id)
    else:
        query = q.filter_by(creator_id=user.id)
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
            'rest.get_clips', 
            userid=userid, 
            itemid=itemid, 
            page=page-1, 
            _external=True
        )
    more = None
    if pagination.has_next:
        more = url_for(
            'rest.get_clips', 
            userid=userid,
            itemid=itemid,
            page=page+1, 
            _external=True
        )
    return jsonify({
        'clips': [c.to_dict() for c in clips],
        'prev': prev,
        'more': more,
        'total': pagination.total
    })

@rest.route('/tag')
def get_tag_ruts():
    tagid = request.args.get('tagid','')
    tag = Tags.query.get_or_404(tagid)
    tagruts = [p.to_dict() for p in tag.posts]
    return jsonify({
        'tagid': tag.id,
        'tagname': tag.tag,
        'descript': tag.descript,
        'tagruts': tagruts
    })