# -*- coding: utf-8 -*-
# clip : a quote excerpted from a book , or a spark of thought

import re
from flask import request, g, jsonify, abort
from ..models import Clips, Cvote, Items
from . import db, rest, auth, PER_PAGE

@rest.route('/clips', methods=['GET'])
# @auth.login_required
def get_clips():
    ref = request.args.get('ref', '')
    userid = request.args.get('userid', type=int)
    itemid = request.args.get('itemid', type=int)
    # yield query
    _q = Clips.query
    if userid and itemid:
        q = _q.filter_by(creator_id=userid, item_id=itemid)
    elif userid:
        q = _q.filter_by(creator_id=userid)
    elif itemid:
        q = _q.filter_by(item_id=itemid)
    else:
        q = _q
    # order per ref
    if ref == "Hot":
        query = q.order_by(Clips.vote.desc())
    else:
        query = q
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    order_query = query.order_by(Clips.timestamp.desc())\
        .offset(page * per_page).limit(per_page)
    clips_dict = {
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    }
    return jsonify(clips_dict)


@rest.route('/clips/<int:clipid>', methods=['GET'])
@auth.login_required
def get_clip(clipid):
    clip = Clips.query.get_or_404(clipid)
    clip_dict = clip.to_dict()
    return jsonify(clip_dict)


@rest.route('/clips/<int:clipid>/voters', methods=['GET'])
@auth.login_required
def get_clip_voters(clipid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Cvote.query.filter_by(clip_id=clipid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_simple_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)


@rest.route('/clips', methods=['POST'])
@auth.login_required
def new_clip():
    text = request.json.get('clip', '').strip()
    spl = text.split('#') + ['']
    body = spl[0].strip()
    if not body:
        abort(403)
    chaplst = (re.findall(r'#([0-9]+):([0-9]+):([0-9]+)', text))
    chapnum = sectnum = pagenum = ''
    if chaplst:
        chap = chaplst[0]
        chapnum = chap[0]
        sectnum = chap[1]
        pagenum = chap[2]
    itemid = request.json.get('itemid')
    user = g.user
    clip = Clips(
        creator=user,
        body=body,
        item=Items.query.get(itemid),
        chapnum=chapnum,
        sectnum=sectnum,
        pagenum=pagenum
    )
    db.session.add(clip)
    db.session.commit()
    # record activity as excerpt a clip
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Excerpted', clipid=clip.id)
    return jsonify(clip.to_dict())


@rest.route('/clips/<int:clipid>/voters', methods=['PATCH'])
@auth.login_required
def upvote_clip(clipid):
    clip = Clips.query.get_or_404(clipid)
    user = g.user
    voted = Cvote.query.filter_by(user_id=user.id, clip_id=clipid).first()
    if voted is None:
        clip.vote = clip.vote + 1
        db.session.add(clip)
        cvote = Cvote(
            voter=user,
            vote_clip=clip
        )
        db.session.add(cvote)
        # record activity as upvote a clip
        # user.set_event(action='Liked', clipid=clip.id)
        db.session.commit()
    return jsonify(clip.vote)


@rest.route('/clips/<int:clipid>', methods=['DELETE'])
@auth.login_required
def del_clip(clipid):
    clip = Clips.query.get_or_404(clipid)
    user = g.user
    if clip.creator != user and user.role.duty != 'Admin':
        abort(403)
    db.session.delete(clip)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/clip/<int:clipid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_or_enable_clip(clipid):
    clip = Clips.query.get_or_404(clipid)
    user = g.user
    if clip.creator != user and user.role.duty != 'Admin':
        abort(403)
    dis_or_enb = request.json.get('disbaled', True)
    clip.disabled = dis_or_enb
    db.session.add(clip)
    db.session.commit()
    return jsonify(clip.disabled)
