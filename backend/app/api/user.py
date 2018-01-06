# -*- coding: utf-8 -*-
# user 

from flask import request, g, jsonify, abort
from ..models import *
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

@rest.route('/<int:userid>/created/ruts')
def get_created_ruts(userid):
    user = Users.query.get_or_404(int(userid))
    created_ruts = user.posts.order_by(Posts.timestamp.desc())
    #created_ruts = Posts.query.filter_by(creator_id=userid).order_by(Posts.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = created_ruts.offset(page * per_page).limit(per_page)
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': created_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)

@rest.route('/<int:userid>/star/ruts')
def get_star_ruts(userid):
    user = Users.query.get_or_404(userid)
    star_ruts = user.star_posts.order_by(Star.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = [s.star_post for s in star_ruts.offset(page * per_page).limit(per_page)]
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': star_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)

@rest.route('/<int:userid>/challenge/ruts')
def get_challege_ruts(userid):
    user = Users.query.get_or_404(userid)
    challenge_ruts = user.challenge_posts.order_by(Challenge.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = [c.challenge_post \
        for c in challenge_ruts.offset(page * per_page).limit(per_page)]
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': challenge_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)

@rest.route('/<int:userid>/doing/items')
def get_doing_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=2).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

@rest.route('/<int:userid>/todo/items')
def get_todo_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=1).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

@rest.route('/<int:userid>/done/items')
def get_done_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=3).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

### user created clips: see get_iu_clip in item.py

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

@rest.route('/user/<int:userid>/reviews')
def get_created_reviews(userid):
    #user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = Reviews.query.filter_by(creator_id=userid)
    rs = reviews.order_by(Reviews.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    reviewcount = reviews.count()
    review_list = [r.to_dict() for r in rs]
    review_dict = {'reviewcount': reviewcount, 'reviews': review_list}
    return jsonify(review_dict)

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

@rest.route('/user/<int:userid>/demands')
def get_request_demands(userid):
    #user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = Demands.query.filter_by(requestor_id=userid)
    ds = demands.order_by(Demands.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    demandcount = demands.count()
    d_list = [d.to_dict() for d in ds]
    demand_dict = {'demandcount': demandcount, 'demands': d_list}
    return jsonify(demand_dict)

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

@rest.route('/<int:userid>/comments')
def get_post_comments(userid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_comments = Comments.query.filter_by(creator_id=userid)\
                           .order_by(Comments.timestamp.desc())
    comments = all_comments.offset(page*per_page).limit(per_page)
    comments_dict = {
        'comments': [c.to_dict() for c in comments],
        'total': all_comments.count(),
        'currentpage': page
    }
    return jsonify(comments_dict)