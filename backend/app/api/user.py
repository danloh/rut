# -*- coding: utf-8 -*-
# user 

from flask import current_app, request, g, jsonify, abort
from ..models import *
from ..utils import split_str, str_to_dict, str_to_set

from . import db, rest, auth, PER_PAGE

@rest.route('/currentuser') 
@auth.login_required  
def get_current_user(): # for authed-user to re-get info
    user = g.user
    user_dict = user.to_dict()
    return jsonify(user_dict)

@rest.route('/user/<int:id>')
def get_user(id):        # get info per userid
    user = Users.query.get_or_404(id)
    user_dict = user.to_dict()
    return jsonify(user_dict)

@rest.route('/checkfollow/<int:userid>')
@auth.login_required
def check_follow(userid):
    user = g.user
    fo_user = Users.query.get_or_404(userid)
    following = 'UnFollow' if user.is_following(fo_user) else 'Follow'
    return jsonify(following)

@rest.route('/follow/user/<int:userid>')
@auth.login_required
def follow_user(userid):
    user = g.user
    if user.followed.count() >= 42:
        abort(418)
    fo_user = Users.query.get_or_404(userid)
    user.follow(fo_user)
    return jsonify('UnFollow')
@rest.route('/unfollow/user/<int:userid>')
@auth.login_required
def unfollow_user(userid):
    user = g.user
    fo_user = Users.query.get_or_404(userid)
    user.unfollow(fo_user)
    return jsonify('Follow')

@rest.route('/user/<int:userid>/followed')
def get_followeds(userid):
    user = Users.query.get_or_404(userid)
    followeds = [ u.followed for u in user.followed ]
    user_dicts = [u.to_dict() for u in followeds]
    return jsonify(user_dicts)

@rest.route('/<int:userid>/voted/demands')
def get_voted_demands(userid):
    #user = Users.query.get_or_404(userid) #which is better?
    #vote_demands = user.vote_demands.order_by(Dvote.timestamp.desc()) 
    vote_demands = Dvote.query.filter_by(user_id=userid)\
                        .order_by(Dvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = [d.vote_demand \
            for d in vote_demands.offset(page * per_page).limit(per_page)]
    demands_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': vote_demands.count()
    }
    return jsonify(demands_dict)

@rest.route('/<int:userid>/voted/clips')
def get_voted_clips(userid):
    vote_clips = Cvote.query.filter_by(user_id=userid)\
                            .order_by(Cvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    clips = [c.vote_clip \
            for c in vote_clips.offset(page * per_page).limit(per_page)]
    clips_dict = {
        'clips': [c.to_dict() for c in clips],
        'total': vote_clips.count()
    }
    return jsonify(clips_dict)

@rest.route('/<int:userid>/voted/reviews')
def get_voted_reviews(userid):
    vote_reviews = Rvote.query.filter_by(user_id=userid)\
                        .order_by(Rvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = [c.vote_review \
            for c in vote_reviews.offset(page * per_page).limit(per_page)]
    reviews_dict = {
        'reviews': [c.to_dict() for c in reviews],
        'total': vote_reviews.count()
    }
    return jsonify(reviews_dict)

@rest.route('/<int:userid>/fav/tags')
def get_fav_tags(userid):
    fav_tags = Fav.query.filter_by(user_id=userid)\
                        .order_by(Fav.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    tags = [t.fav_tag for t in fav_tags.offset(page * per_page).limit(per_page)]
    tags_dict = {
        'tags': [t.to_dict() for t in tags],
        'total': fav_tags.count()
    }
    return jsonify(tags_dict)