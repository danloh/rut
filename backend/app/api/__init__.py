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
#api.add_resource(res.Demandz, '/demands', '/demands/<userid>', '/demands/<ref>/<userid>')
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
def get_ruts():            ##!! to be optimized
    user = g.user
    ref = request.args.get('ref','random')
    #get related tags set and fav tags
    tag_set, tag_fv = user.get_tag_set()
    # get followed posts queries
    post_fo = [f.followed.posts for f in user.followed]
    #list the queries, followed _posts as init 
    q = post_fo
    for tag_obj in tag_set:
        q.append(tag_obj.posts)
    q_rand = Posts.query.limit(0)
    query = q_rand.union(*q)
    ruts = query.order_by(Posts.timestamp.desc())  # other way,list reverse
    return jsonify({  # need to optimize
        'ruts': [r.to_dict() for r in ruts],
        'total': ruts.count(),
        'tags': [{'tagid': t.id,'tagname': t.tag} for t in tag_set] 
    })

@rest.route('/challengeruts')
@auth.login_required
def get_challege_ruts():
    user = g.user
    ref = request.args.get('ref','') # for current challenge
    if ref:
        challenge_rut = user.challenge_posts.first()
        try:
            rut = challenge_rut.challenge_post
            deadline = challenge_rut.deadline
            rut_dict = rut.to_dict()
            items = [t.item.to_dict() for t in rut.items]
            return jsonify({
                'ruts': [rut_dict],
                'total': 1,
                'tags': [],
                'items': items,
                'deadline': deadline
            })
        except:
            return jsonify({
                'ruts': [],
                'total': 0,
                'tags': []
            })
    q = [c.challenge_post for c in user.challenge_posts]
    q_rand = Posts.query.limit(0)  ##???
    query = q_rand.union(*q)
    ruts = query.order_by(Posts.timestamp.desc())  # other way,list reverse
    return jsonify({
        'ruts': [r.to_dict() for r in ruts],
        'total': ruts.count(),
        'tags': []
    })

    # if ref == 'create':
    #     q = [user.posts] # a query list
    # elif ref == 'star':
    #     q = [s.star_post for s in user.star_posts]
   
    # elif ref == 'contribute':
    #     q = [c.contribute_post for c in user.contribute_posts]
    # else:

@rest.route('/create', methods=['POST'])
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
        query = q.filter(Clips.creator != user)
    else:
        query = q.filter_by(creator_id=user.id)
    order_query = query.order_by(Clips.timestamp.desc()) # or reverse list
    return jsonify({
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    })

@rest.route('/newclip', methods=['POST'])
@auth.login_required
def new_clip():
    clip = Clips(
        creator = g.user,
        body = request.json.get('clip'),
        item = Items.query.get(1)  # for test currently
    )
    db.session.add(clip)
    db.session.commit()
    return jsonify(clip.to_dict())

@rest.route('/demands')
def get_demands():
    query = q = Demands.query
    userid = request.args.get('userid','')
    ref = request.args.get('type','popular')
    if userid:
        query = q.filter_by(requestor_id=int(userid))
    if ref == "new":
        demands = query.order_by(Demands.timestamp.desc())
    else:
        demands = query.order_by(Demands.vote.desc())
    demand_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': demands.count()
    }
    return jsonify(demand_dict)

@rest.route('/newdemand', methods=['POST'])
@auth.login_required
def new_demand():
    sp = request.json.get('demand').split('#') + ['42']
    body = sp[0]
    tag_str = sp[1]
    demand = Demands(
        requestor = g.user,
        body = body,
        dtag_str = tag_str
    )
    db.session.add(demand)
    demand.dtag_to_db()
    db.session.commit()
    return jsonify(demand.to_dict())
