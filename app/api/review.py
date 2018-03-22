# -*- coding: utf-8 -*-
# review: a note, review or mindmap on a item

from flask import request, g, jsonify, abort
from ..models import Reviews, Rvote, Comments, Items
from . import db, rest, auth, PER_PAGE


@rest.route('/reviews')  # per user, item or any
@auth.login_required
def get_reviews():
    userid = request.args.get('userid', type=int)
    itemid = request.args.get('itemid', type=int)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Reviews.query
    if userid and itemid:
        reviews = query.filter_by(creator_id=userid, item_id=itemid)
    if userid:
        reviews = query.filter_by(creator_id=userid)
    elif itemid:
        reviews = query.filter_by(item_id=itemid)
    else:
        reviews = query
    rs = reviews.order_by(Reviews.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    review_list = [r.to_dict() for r in rs]
    reviews_dict = {'reviewcount': reviews.count(), 'reviews': review_list}
    return jsonify(reviews_dict)


@rest.route('/all/reviews')
@auth.login_required
def get_all_reviews():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_reviews = Reviews.query
    reviews = all_reviews.offset(page*per_page).limit(per_page)
    reviews_dict = {
        'reviews': [rev.to_dict() for rev in reviews],
        'total': all_reviews.count(),
        'currentpage': page
    }
    return jsonify(reviews_dict)


@rest.route('/review/<int:reviewid>')
def get_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    review_dict = review.to_dict()
    # attach comments
    rev_comments = review.comments.order_by(Comments.timestamp.desc())
    review_dict['commentcount'] = rev_comments.count()
    comments = [c.to_dict() for c in rev_comments.limit(PER_PAGE)]
    review_dict['comments'] = comments
    return jsonify(review_dict)


@rest.route('/review/<int:reviewid>/comments')
@auth.login_required
def get_review_comments(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    rev_comments = review.comments.order_by(Comments.timestamp.desc())\
        .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in rev_comments]
    return jsonify(comments)


@rest.route('/review/<int:reviewid>/voters')
@auth.login_required
def get_review_voters(reviewid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Rvote.query.filter_by(review_id=reviewid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_simple_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)


@rest.route('/upvotereview/<int:reviewid>')
@auth.login_required
def upvote_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    user = g.user
    voted = Rvote.query.filter_by(user_id=user.id, review_id=reviewid).first()
    if user != review.creator and voted is None:
        review.vote = review.vote + 1
        db.session.add(review)
        rvote = Rvote(
            voter=user,
            vote_review=review
        )
        db.session.add(rvote)
        db.session.commit()
        # record activity as post a review
        from task.tasks import set_event_celery
        set_event_celery.delay(user.id, action='Endorsed', reviewid=review.id)
    return jsonify(review.vote)


@rest.route('/newreview/<int:itemid>', methods=['POST'])
@auth.login_required
def new_review(itemid):
    body = request.json.get('review', '').strip()
    heading = request.json.get('title', '').strip()
    if not body or not heading:
        abort(403)
    item = Items.query.get_or_404(itemid)
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    user = g.user
    review = Reviews(
        heading=heading,
        body=body,
        spoiler=spoiler,
        item=item,
        creator=user
    )
    db.session.add(review)
    db.session.commit()
    review_dict = review.to_dict()
    # item.cal_vote()
    # record activity as post a review
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Posted', reviewid=review.id)
    return jsonify(review_dict)


@rest.route('/editreview/<int:reviewid>', methods=['POST'])
@auth.login_required
def edit_review(reviewid):
    body = request.json.get('review', '').strip()
    heading = request.json.get('title', '').strip()
    if not body or not heading:
        abort(403)
    review = Reviews.query.get_or_404(reviewid)
    user = g.user
    if user != review.creator and user.role != 'Admin':
        abort(403)  # No Permission
    review.heading = heading
    review.body = body
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    review.spoiler = spoiler
    db.session.add(review)
    db.session.commit()
    review_dict = review.to_dict()
    return jsonify(review_dict)


@rest.route('/delete/review/<int:reviewid>')
@auth.login_required
def del_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    user = g.user
    if review.creator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(review)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/disable/review/<int:reviewid>')
@auth.login_required
def disable_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    user = g.user
    if review.creator != user and user.role != 'Admin':
        abort(403)
    review.disabled = True
    db.session.add(review)
    db.session.commit()
    return jsonify('Disabled')


@rest.route('/recover/review/<int:reviewid>')
@auth.login_required
def recover_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    user = g.user
    if review.creator != user and user.role != 'Admin':
        abort(403)
    review.disabled = False  # enable
    db.session.add(review)
    db.session.commit()
    return jsonify('Enabled')
