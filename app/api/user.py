# -*- coding: utf-8 -*-
# user

from datetime import datetime, timedelta
from flask import request, g, jsonify, abort
from ..models import Users, Flag, Posts, Star, Cvote, Fav, Heat,\
                     Demands, Dvote, Reviews, Rvote, Comments, Events
from . import rest, auth, PER_PAGE


@rest.route('/currentuser', methods=['GET'])
@auth.login_required
def get_current_user():  # #??
    # for authed-user to re-get info
    user = g.user
    user_dict = user.to_dict()
    return jsonify(user_dict)


@rest.route('/users/<int:userid>', methods=['GET'])
@auth.login_required
def get_user(userid):
    user = Users.query.get_or_404(userid)
    user_dict = user.to_dict()
    return jsonify(user_dict)


@rest.route('/users/<int:userid>/iffollow', methods=['GET'])
@auth.login_required
def check_follow(userid):
    # check if follow someone
    fo_user = Users.query.get_or_404(userid)
    user = g.user
    following = 'UnFollow' if user.is_following(fo_user) else 'Follow'
    return jsonify(following)


@rest.route('/users/<int:userid>/follows', methods=['PATCH'])
@auth.login_required
def follow_user(userid):
    # me fo other
    user = g.user
    if user.followed.count() >= 42:
        abort(418)
    fo_user = Users.query.get_or_404(userid)
    user.follow(fo_user)
    return jsonify('UnFollow')


@rest.route('/users/<int:userid>/follows', methods=['DELETE'])
@auth.login_required
def unfollow_user(userid):
    # me unfo other
    fo_user = Users.query.get_or_404(userid)
    user = g.user
    user.unfollow(fo_user)
    return jsonify('Follow')


@rest.route('/users/<int:userid>/followeds', methods=['GET'])
@auth.login_required
def get_followeds(userid):
    # who be followed by me
    user = Users.query.get_or_404(userid)
    followeds = [u.followed for u in user.followed]
    user_dicts = [u.to_simple_dict() for u in followeds]
    return jsonify(user_dicts)


@rest.route('/users/<int:userid>/createdruts', methods=['GET'])
@auth.login_required
def get_created_ruts(userid):
    user = Users.query.get_or_404(int(userid))
    created_ruts = user.posts.order_by(Posts.timestamp.desc())
    # created_ruts = Posts.query.filter_by(creator_id=userid).order_by(Posts.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = created_ruts.offset(page * per_page).limit(per_page)
    ruts_dict = {
        'ruts': [r.to_simple_dict() for r in ruts],
        'total': created_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)


@rest.route('/users/<int:userid>/starruts', methods=['GET'])
@auth.login_required
def get_star_ruts(userid):
    user = Users.query.get_or_404(userid)
    star_ruts = user.star_posts.order_by(Star.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = [s.star_post for s in star_ruts.offset(page * per_page).limit(per_page)]
    ruts_dict = {
        'ruts': [r.to_simple_dict() for r in ruts],
        'total': star_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)


@rest.route('/users/<int:userid>/doingitems', methods=['GET'])
@auth.login_required
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


@rest.route('/users/<int:userid>/todoitems', methods=['GET'])
@auth.login_required
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


@rest.route('/users/<int:userid>/doneitems', methods=['GET'])
@auth.login_required
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


@rest.route('/users/challengeitems', methods=['GET'])
@auth.login_required
def get_challege_items():
    """challenging items for challenge view page"""
    user = g.user
    # get the earliest flaged items as doing
    doing_flags = user.flag_items\
            .order_by(Flag.timestamp)\
            .filter_by(flag_label=2).limit(5)  # special limit num
    doing_items = [f.flag_item for f in doing_flags]
    doing_list = [{'id': item.id, 'title': item.title} for item in doing_items]
    return jsonify(doing_list)


@rest.route('/users/<int:userid>/voted/clips', methods=['GET'])
@auth.login_required
def get_voted_clips(userid):
    vote_clips = Cvote.query.filter_by(user_id=userid)\
                            .order_by(Cvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    clips = [c.vote_clip
             for c in vote_clips.offset(page * per_page).limit(per_page)]
    clips_dict = {
        'clips': [c.to_dict() for c in clips],
        'total': vote_clips.count()
    }
    return jsonify(clips_dict)


@rest.route('/users/<int:userid>/favtags', methods=['GET'])
@auth.login_required
def get_fav_tags(userid):
    fav_tags = Fav.query.filter_by(user_id=userid)\
                        .order_by(Fav.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 12, type=int)  # PER_PAGE special limit num
    tags = [t.fav_tag for t in fav_tags.offset(page * per_page).limit(per_page)]
    tags_dict = {
        'tags': [t.to_dict() for t in tags],
        'total': fav_tags.count()
    }
    return jsonify(tags_dict)


@rest.route('/users/<int:userid>/reviews', methods=['GET'])
@auth.login_required
def get_created_reviews(userid):
    # user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = Reviews.query.filter_by(creator_id=userid)
    revs_list = reviews.order_by(Reviews.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    reviewcount = reviews.count()
    review_list = [r.to_dict() for r in revs_list]
    review_dict = {'reviewcount': reviewcount, 'reviews': review_list}
    return jsonify(review_dict)


@rest.route('/users/<int:userid>/voted/reviews', methods=['GET'])
@auth.login_required
def get_voted_reviews(userid):
    vote_reviews = Rvote.query.filter_by(user_id=userid)\
                        .order_by(Rvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = [c.vote_review
               for c in vote_reviews.offset(page * per_page).limit(per_page)]
    reviews_dict = {
        'reviews': [c.to_dict() for c in reviews],
        'total': vote_reviews.count()
    }
    return jsonify(reviews_dict)


@rest.route('/users/<int:userid>/demands', methods=['GET'])
@auth.login_required
def get_request_demands(userid):
    # user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = Demands.query.filter_by(requestor_id=userid)
    ds = demands.order_by(Demands.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    demandcount = demands.count()
    d_list = [d.to_dict() for d in ds]
    demand_dict = {'demandcount': demandcount, 'demands': d_list}
    return jsonify(demand_dict)


@rest.route('/users/<int:userid>/voted/demands', methods=['GET'])
@auth.login_required
def get_voted_demands(userid):
    # user = Users.query.get_or_404(userid) #which is better?
    # vote_demands = user.vote_demands.order_by(Dvote.timestamp.desc())
    vote_demands = Dvote.query.filter_by(user_id=userid)\
                        .order_by(Dvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = [d.vote_demand
               for d in vote_demands.offset(page * per_page).limit(per_page)]
    demands_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': vote_demands.count()
    }
    return jsonify(demands_dict)


@rest.route('/users/<int:userid>/comments', methods=['GET'])
@auth.login_required
def get_post_comments(userid):
    """comments post by user"""
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


@rest.route('/users/<int:userid>/myactivity', methods=['GET'])
@auth.login_required
def get_activity(userid):
    # user = Users.query.get_or_404(userid)
    m = 42  # special limit num
    evs = Events.query.filter_by(user_id=userid)\
                      .order_by(Events.timestamp.desc()).limit(m)
    evs_list = [e.to_dict() for e in evs]
    return jsonify(evs_list)


@rest.route('/users/feeds', methods=['GET'])
@auth.login_required
def get_feeds():
    m = 42  # special limit num
    user = g.user
    late_events = Events.query.order_by(Events.timestamp.desc()).limit(5)
    follow_events = [f.followed.events for f in user.followed]
    query = late_events.union(*follow_events)
    evs = query.order_by(Events.timestamp.desc()).limit(m)
    evs_list = [e.to_dict() for e in evs]
    return jsonify(evs_list)

@rest.route('/users/<int:userid>/eventheat', methods=['GET'])
@auth.login_required
def get_heat(userid):
    heat_query = Heat.query.filter_by(user_id=userid)
    today = datetime.utcnow().date()
    delta = timedelta(days=365)
    start = today - delta
    heats = heat_query.filter(Heat.day >= start)
    heat_list = [
        {'counting': h.num, 'created_at': h.day.strftime('%Y-%m-%d')} for h in heats
    ]
    heat_count = sum([h.num for h in heats])
    heat_dict = {'heats': heat_list, 'heatcount': heat_count}
    return jsonify(heat_dict)
