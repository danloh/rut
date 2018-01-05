# -*- coding: utf-8 -*-
# demand: a request to get a rut like book list on a subject

from flask import current_app, request, g, jsonify, abort
from ..models import *
from ..utils import split_str, str_to_dict, str_to_set

from . import db, rest, auth, PER_PAGE

@rest.route('/user/<int:userid>/demands')
def get_user_demands(userid):
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

@rest.route('/all/demands')   
@rest.route('/demands')
def get_demands():
    query = Demands.query
    userid = request.args.get('userid','')
    ref = request.args.get('type','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    if userid:
        demands = query.filter_by(requestor_id=int(userid))\
                       .order_by(Demands.timestamp.desc())
    elif ref == "new":
        demands = query.order_by(Demands.timestamp.desc())
    elif ref == "popular":  # popular
        demands = query.order_by(Demands.vote.desc())
    else:
        demands = query
    ds = demands.offset(per_page * page).limit(per_page)
    demands_dict = {
        'demands': [d.to_dict() for d in ds],
        'total': demands.count()
    }
    return jsonify(demands_dict)

@rest.route('/onlydemand/<int:demandid>')
def get_demand_only(demandid):
    demand = Demands.query.get_or_404(demandid)
    demand_dict = demand.to_dict()
    return jsonify(demand_dict)

@rest.route('/demand/<int:demandid>')
def get_demand(demandid):
    demand = Demands.query.get_or_404(demandid)
    demand_dict = demand.to_dict()
    #attach answers to demand
    resps = demand.posts.order_by(Respon.timestamp.desc()).limit(PER_PAGE)
    respons = [r.post for r in resps]
    answers = [{'id':p.id,'title':p.title,'intro':p.intro} for p in respons]
    demand_dict['answers'] = answers
    #attach comments
    d_comments = demand.comments.order_by(Comments.timestamp.desc()).limit(50)
    comments = [c.to_dict() for c in d_comments]
    ##comments.reverse()
    demand_dict['comments'] = comments
    return jsonify(demand_dict)

@rest.route('/demand/<int:demandid>/comments')
def get_demand_comments(demandid):
    demand = Demands.query.get_or_404(demandid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 50, type=int)
    d_comments = demand.comments.order_by(Comments.timestamp.desc())\
                                .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in d_comments]
    return jsonify(comments)

@rest.route('/demand/<int:demandid>/answers')
def get_demand_answers(demandid):
    demand = Demands.query.get_or_404(demandid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    d_resps = demand.posts.order_by(Respon.timestamp.desc())\
                          .offset(page*per_page).limit(per_page)
    d_respons = [r.post for r in d_resps]
    answers = [{'id':p.id,'title':p.title,'intro':p.intro} for p in d_respons]
    return jsonify(answers)

@rest.route('/upvotedemand/<int:demandid>')
@auth.login_required
def upvote_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid) # demand's id
    voted = Dvote.query.filter_by(user_id=user.id,demand_id=demandid).first()
    if voted is None:
        demand.vote = demand.vote + 1 
        db.session.add(demand)
        dvote = Dvote(
            voter=user,
            vote_demand=demand
        )
        db.session.add(dvote)
        db.session.commit()
        #return jsonify(demand.vote)
    return jsonify(demand.vote)

@rest.route('/newdemand', methods=['POST'])
@auth.login_required
def new_demand():
    text = request.json.get('demand','').strip()
    if not text:
        abort(403)
    sp = text.split('#') + ['42']
    body = sp[0]
    tag_str = sp[1].strip() or '42'
    demand = Demands(
        requestor = g.user,
        body = body,
        dtag_str = tag_str
    )
    db.session.add(demand)
    demand.dtag_to_db()
    db.session.commit()
    return jsonify(demand.to_dict())

@rest.route('/rut/<int:rutid>/answerdemand/<int:demandid>')
@auth.login_required
def rut_as_answer(rutid, demandid):
    """link  Rut to  a demand as Answer"""
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user and user.role != 'Admin':
        abort(403) #no permission
    demand = Demands.query.get_or_404(demandid)
    respon = Respon(
        post = rut,
        demand = demand
    )
    db.session.add(respon)
    db.session.commit()
    answer = {'id': rut.id, 'title': rut.title}
    return jsonify(answer)

@rest.route('/delete/demand/<int:demandid>')
@auth.login_required
def del_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    db.session.delete(demand)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/demand/<int:demandid>')
@auth.login_required
def disable_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    demand.disabled = True
    db.session.add(demand)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/demand/<int:demandid>')
@auth.login_required
def recover_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    demand.disabled = False #enable
    db.session.add(demand)
    db.session.commit()
    return jsonify('Enabled')