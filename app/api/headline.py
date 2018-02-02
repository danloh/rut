# -*- coding: utf-8 -*-
# headline: news for reader

from flask import request, g, jsonify, abort
from ..models import *
from . import db, rest, auth, PER_PAGE
 
@rest.route('/headlines')
def get_headlines():
    query = Headlines.query
    userid = request.args.get('userid','')
    ref = request.args.get('ref','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # yield query per filter criteria
    if userid:
        headlines_query = query.filter_by(submitor_id=int(userid))
    else:
        headlines_query = query
    # order per point or timestamp
    if ref == 'new':
        headlines = headlines_query.order_by(Headlines.timestamp.desc())
    else:
        headlines = headlines_query.order_by(Headlines.point.desc())
    # pagination then result
    hs = headlines.offset(per_page * page).limit(per_page)
    headlines_dict = {
        'headlines': [h.to_dict() for h in hs],
        'total': headlines.count()
    }
    return jsonify(headlines_dict)

@rest.route('/headline/<int:headlineid>')
def get_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    headline_dict = headline.to_dict()
    return jsonify(headline_dict)

@rest.route('/headline/<int:headlineid>/comments')
def get_headline_comments(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    headline_dict = headline.to_dict()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 50, type=int)
    h_comments = headline.comments.order_by(Comments.timestamp.desc())\
                                .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in h_comments]
    headline_dict['comments'] = comments
    return jsonify(headline_dict)

@rest.route('/headline/<int:headlineid>/voters')
def get_headline_voters(headlineid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Hvote.query.filter_by(headline_id=headlineid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)

@rest.route('/upvoteheadline/<int:headlineid>')
@auth.login_required
def upvote_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid) # headline's id
    user = g.user
    voted = Hvote.query.filter_by(user_id=user.id,headline_id=headlineid).first()
    if voted is None:
        headline.vote = headline.vote + 1 
        db.session.add(headline)
        hvote = Hvote(
            voter=user,
            vote_headline=headline
        )
        db.session.add(hvote)
        # record activity as upvote a headline
        #user.set_event(action='Push', headline=headline)
        headline.cal_point() # to be in task queue
        db.session.commit()
        #return jsonify(headline.vote)
    return jsonify(headline.point)

@rest.route('/newheadline', methods=['POST'])
@auth.login_required
def new_headline():
    title = request.json.get('title','').strip()
    if not title:
        abort(403)
    url = request.json.get('url','').strip()
    if url:
        exist = Headlines.query.filter_by(url=url).first()
        if exist:
            return jsonify(exist.to_dict())
    content = request.json.get('content','').strip()
    if not (url or content):
        abort(403)
    user = g.user
    headline = Headlines(
        submitor = user,
        title = title,
        url = url,
        content = content
    )
    db.session.add(headline)
    # record activity as submit a headline
    user.set_event(action='Submitted', headline=headline)
    db.session.commit()
    return jsonify(headline.to_dict())

@rest.route('/delete/headline/<int:headlineid>')
@auth.login_required
def del_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if headline.submitor != user and user.role != 'Admin':
        abort(403)
    db.session.delete(headline)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/headline/<int:headlineid>')
@auth.login_required
def disable_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if headline.submitor != user and user.role != 'Admin':
        abort(403)
    headline.disabled = True
    db.session.add(headline)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/headline/<int:headlineid>')
@auth.login_required
def recover_headline(headlineid):
    headline = Headlines.query.get_or_404(headlineid)
    user = g.user
    if headline.submitor != user and user.role != 'Admin':
        abort(403)
    headline.disabled = False #enable
    db.session.add(headline)
    db.session.commit()
    return jsonify('Enabled')