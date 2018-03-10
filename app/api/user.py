# -*- coding: utf-8 -*-
# user

from flask import request, g, jsonify, abort
from ..models import Users, Flag, Posts, Star, Items, Cvote, Fav,\
                     Demands, Dvote, Reviews, Rvote, Comments, Events
from . import rest, auth, PER_PAGE


@rest.route('/currentuser')
@auth.login_required
def get_current_user():  # for authed-user to re-get info
    user = g.user
    user_dict = user.to_dict()
    return jsonify(user_dict)


@rest.route('/user/<int:userid>')
def get_user(userid):        # get info per userid
    user = Users.query.get_or_404(userid)
    user_dict = user.to_dict()
    return jsonify(user_dict)


@rest.route('/checkfollow/<int:userid>')
@auth.login_required
def check_follow(userid):
    fo_user = Users.query.get_or_404(userid)
    user = g.user
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
    fo_user = Users.query.get_or_404(userid)
    user = g.user
    user.unfollow(fo_user)
    return jsonify('Follow')


@rest.route('/user/<int:userid>/followed')
def get_followeds(userid):
    user = Users.query.get_or_404(userid)
    followeds = [u.followed for u in user.followed]
    user_dicts = [u.to_simple_dict() for u in followeds]
    return jsonify(user_dicts)


@rest.route('/<int:userid>/created/ruts')
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


@rest.route('/<int:userid>/star/ruts')
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


@rest.route('/searchruts')
@auth.login_required
def search_ruts():
    """search ruts, esp. created ruts"""
    title = request.args.get('title', '').strip()  # search per title
    # if keywork is '', just return created
    if not title:
        ruts = g.user.posts.order_by(Posts.timestamp.desc()).limit(PER_PAGE)
    else:
        ref = request.args.get('ref', 'created').strip()  # search in all or created
        if ref == 'created':
            query = g.user.posts
        else:
            query = Posts.query
        ruts = query.filter(Posts.title.contains(title))\
                    .order_by(Posts.timestamp.desc())
    ruts_list = [{'id': r.id, 'title': r.title} for r in ruts]
    return jsonify(ruts_list)


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


@rest.route('/search/<int:label>/items')
@auth.login_required
def search_items(label):
    uid_or_title = request.args.get('uid_or_title', '').strip()
    user = g.user
    userid = request.args.get('userid', type=int) or user.id
    # related pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # if keyword is '', return flag-items, otherwise, query per keyword
    if not uid_or_title:
        # abort(403)
        flags = user.flag_items.filter_by(flag_label=label)\
                               .order_by(Flag.timestamp.desc())\
                               .offset(page*per_page).limit(per_page)
        items = [d.flag_item for d in flags]  # i.e. flaged, may huge
    else:
        query = Items.query
        item_uid = query.filter_by(uid=uid_or_title)
        item_title = query.filter(Items.title.contains(uid_or_title))  # query per substring
        items = item_uid.union(item_title)\
            .offset(page*per_page).limit(per_page).all()
    if not items:
        return jsonify({'items': [], 'keyword': uid_or_title})
    items_list = []
    for item in set(items):
        if not item:
            continue
        # filter per label to get result from flag-items or all
        if label in [1, 2, 3] and userid and uid_or_title:
            flag = Flag.query.filter_by(
                user_id=userid,
                item_id=item.id,
                flag_label=label
            ).first()
            if flag is None:
                continue
        item_dict = {
            'id': item.id,
            'cate': item.cate,
            'title': item.title
        }
        items_list.append(item_dict)
    return jsonify({'items': items_list, 'keyword': uid_or_title})


@rest.route('/<int:userid>/voted/clips')
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


@rest.route('/<int:userid>/fav/tags')
def get_fav_tags(userid):
    fav_tags = Fav.query.filter_by(user_id=userid)\
                        .order_by(Fav.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 12, type=int)  # PER_PAGE
    tags = [t.fav_tag for t in fav_tags.offset(page * per_page).limit(per_page)]
    tags_dict = {
        'tags': [t.to_dict() for t in tags],
        'total': fav_tags.count()
    }
    return jsonify(tags_dict)


@rest.route('/user/<int:userid>/reviews')
def get_created_reviews(userid):
    # user = Users.query.get_or_404(userid)
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
    reviews = [c.vote_review
               for c in vote_reviews.offset(page * per_page).limit(per_page)]
    reviews_dict = {
        'reviews': [c.to_dict() for c in reviews],
        'total': vote_reviews.count()
    }
    return jsonify(reviews_dict)


@rest.route('/user/<int:userid>/demands')
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


@rest.route('/<int:userid>/voted/demands')
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


@rest.route('/<int:userid>/myactivity')
def get_activity(userid):
    # user = Users.query.get_or_404(userid)
    m = 42
    evs = Events.query.filter_by(user_id=userid)\
                      .order_by(Events.timestamp.desc()).limit(m)
    evs_list = [e.to_dict() for e in evs]
    return jsonify(evs_list)


@rest.route('/feeds')
@auth.login_required
def get_feeds():
    m = 42
    user = g.user
    late_events = Events.query.order_by(Events.timestamp.desc()).limit(5)
    follow_events = [f.followed.events for f in user.followed]
    query = late_events.union(*follow_events)
    evs = query.order_by(Events.timestamp.desc()).limit(m)
    evs_list = [e.to_dict() for e in evs]
    return jsonify(evs_list)
