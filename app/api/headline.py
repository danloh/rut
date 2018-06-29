# -*- coding: utf-8 -*-
# headline: news for reader

from flask import request, g, jsonify, abort
from ..models import Headlines, Hvote, Comments, Items
from . import db, rest, auth, PER_PAGE


@rest.route('/headlines', methods=['GET'])
def get_headlines():
    # get request args
    userid = request.args.get('userid', type=int)
    itemid = request.args.get('itemid', type=int)
    ref = request.args.get('ref', '')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # yield query per filter criteria
    query = Headlines.query
    if userid and itemid:
        headlines_query = query.filter_by(submitor_id=userid, item_id=itemid)
    elif userid:
        headlines_query = query.filter_by(submitor_id=userid)
    elif itemid:
        headlines_query = query.filter_by(item_id=itemid)
    else:
        headlines_query = query
    # order per point or timestamp
    if ref == 'top':
        headlines = headlines_query.order_by(Headlines.point.desc())
    else:
        headlines = headlines_query
    # pagination then result
    hs_list = headlines.order_by(Headlines.timestamp.desc(), Headlines.score.desc())\
                  .offset(per_page * page).limit(per_page)
    headlines_dict = {
        'headlines': [h.to_dict() for h in hs_list],
        'total': headlines.count()
    }
    return jsonify(headlines_dict)


@rest.route('/headlines/<int:headlineid>', methods=['GET'])
@auth.login_required
def get_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    headline_dict = headline.to_dict()
    return jsonify(headline_dict)


@rest.route('/headlines/<int:headlineid>/comments', methods=['GET'])
@auth.login_required
def get_headline_comments(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    # headline_dict = headline.to_dict()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    comments_query = headline.comments
    h_comments = comments_query\
            .order_by(Comments.vote.desc(), Comments.timestamp.desc())\
            .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in h_comments]
    comments_dict = {
        'comments': comments,
        'commentcount': comments_query.count()
    }
    return jsonify(comments_dict)


@rest.route('/headlines/<int:headlineid>/voters', methods=['GET'])
@auth.login_required
def get_headline_voters(headlineid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Hvote.query.filter_by(headline_id=headlineid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_simple_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)


@rest.route('/headlines', methods=['POST'])
@auth.login_required
def new_headline():
    title = request.json.get('title', '').strip()
    if not title:
        abort(403)
    url = request.json.get('url', '').strip()
    if url:
        exist = Headlines.query.filter_by(url=url).first()
        if exist:
            return jsonify(exist.to_dict())
    content = request.json.get('content', '').strip()
    if not (url or content):
        abort(403)
    # att to item
    itemid = request.json.get('itemid', 0)
    item = Items.query.get_or_404(itemid) if itemid else None
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    user = g.user
    headline = Headlines(
        submitor=user,
        title=title,
        url=url,
        content=content,
        spoiler=spoiler,
        item=item,
    )
    db.session.add(headline)
    db.session.commit()
    # record activity as submit a headline
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Submitted', headlineid=headline.id)
    return jsonify(headline.to_dict())


@rest.route('/headlines/<int:headlineid>', methods=['PUT'])
@auth.login_required
def edit_headline(headlineid):
    content = request.json.get('headline', '').strip()
    title = request.json.get('title', '').strip()
    if not content or not title:
        abort(403)
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if user != headline.submitor and user.role != 'Admin':
        abort(403)  # No Permission
    headline.title = title
    headline.content = content
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    headline.spoiler = spoiler
    db.session.add(headline)
    db.session.commit()
    headline_dict = headline.to_dict()
    return jsonify(headline_dict)


@rest.route('/headlines/<int:headlineid>/voters', methods=['PATCH'])
@auth.login_required
def upvote_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)  # headline's id
    user = g.user
    voted = Hvote.query.filter_by(user_id=user.id, headline_id=headlineid).first()
    if voted is None:
        headline.vote = headline.vote + 1
        db.session.add(headline)
        hvote = Hvote(
            voter=user,
            vote_headline=headline
        )
        db.session.add(hvote)
        db.session.commit()
        # record activity as upvote a headline
        # user.set_event(action='Push', headlineid=headline.id)
        # headline.cal_point() # to be in task queue
    # return jsonify(headline.vote)
    return jsonify(headline.vote)


@rest.route('/headlines/<int:headlineid>', methods=['DELETE'])
@auth.login_required
def del_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if headline.submitor != user and user.role != 'Admin':
        abort(403)
    db.session.delete(headline)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/headlines/<int:headlineid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_or_enable_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if headline.submitor != user and user.role != 'Admin':
        abort(403)
    dis_or_enb = request.json.get('disbaled', True)
    headline.disabled = dis_or_enb
    db.session.add(headline)
    db.session.commit()
    return jsonify(headline.disabled)
