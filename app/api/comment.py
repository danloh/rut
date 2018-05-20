# -*- coding: utf-8 -*-
# comment : on rut, demand, clip, item, review, etc.

import re
from flask import request, g, jsonify, abort
from ..models import Comments, Posts, Demands, Items, Headlines, Reviews, Mvote
from . import db, rest, auth, PER_PAGE


@rest.route('/all/comments')
@auth.login_required
def get_all_comments():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_comments = Comments.query
    comments = all_comments.offset(page*per_page).limit(per_page)
    comments_dict = {
        'comments': [c.to_dict() for c in comments],
        'total': all_comments.count(),
        'currentpage': page
    }
    return jsonify(comments_dict)


@rest.route('/comment/<int:commentid>')
@auth.login_required
def get_comment(commentid):
    commt = Comments.query.get_or_404(commentid)
    commt_dict = commt.to_dict()
    return jsonify(commt_dict)


@rest.route('/comment/<int:commentid>/voters')
@auth.login_required
def get_comment_voters(commentid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Mvote.query.filter_by(comment_id=commentid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_simple_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)


@rest.route('/upvotecomment/<int:commentid>')
@auth.login_required
def upvote_comment(commentid):
    comment = Comments.query.get_or_404(commentid)  # comment's id
    user = g.user
    voted = Mvote.query.filter_by(user_id=user.id, comment_id=commentid).first()
    if voted is None:
        comment.vote = comment.vote + 1
        db.session.add(comment)
        mvote = Mvote(
            voter=user,
            vote_comment=comment
        )
        db.session.add(mvote)
        db.session.commit()
    return jsonify("Done")


@rest.route('/comment/tag/', methods=['POST'])
@rest.route('/comment/rut/<int:rutid>', methods=['POST'])
@rest.route('/comment/demand/<int:demandid>', methods=['POST'])
@rest.route('/comment/comment/<int:commentid>', methods=['POST'])
@rest.route('/comment/item/<int:itemid>', methods=['POST'])
@rest.route('/comment/review/<int:reviewid>', methods=['POST'])
@rest.route('/comment/headline/<int:headlineid>', methods=['POST'])
@auth.login_required
def new_comment(demandid=None, rutid=None, commentid=None, itemid=None,
                reviewid=None, headlineid=None):
    body = request.json.get('comment', '').strip()
    if not body:
        abort(403)
    user = g.user
    comment = Comments(
        body=body,
        demand=Demands.query.get(demandid) if demandid else None,
        post=Posts.query.get(rutid) if rutid else None,
        item=Items.query.get(itemid) if itemid else None,
        parent_comment=Comments.query.get(commentid) if commentid else None,
        review=Reviews.query.get(reviewid) if reviewid else None,
        headline=Headlines.query.get(headlineid) if headlineid else None,
        creator=user
    )
    db.session.add(comment)
    # extract tags and intro
    taglst = re.findall(r'#(\w+)', body)
    comment.ctag_to_db(taglst)
    db.session.commit()
    comment_dict = comment.to_dict()
    return jsonify(comment_dict)


@rest.route('/delete/comment/<int:commentid>')
@auth.login_required
def del_comment(commentid):
    comment = Comments.query.get_or_404(commentid)
    user = g.user
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/disable/comment/<int:commentid>')
@auth.login_required
def disable_comment(commentid):
    comment = Comments.query.get_or_404(commentid)
    user = g.user
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return jsonify('Disabled')


@rest.route('/recover/comment/<int:commentid>')
@auth.login_required
def recover_comment(commentid):
    comment = Comments.query.get_or_404(commentid)
    user = g.user
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    comment.disabled = False  # enable
    db.session.add(comment)
    db.session.commit()
    return jsonify('Enabled')
