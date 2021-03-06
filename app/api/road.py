# -*- coding: utf-8 -*-
"""road is learning road map"""

import re
from flask import request, g, jsonify, abort
from ..models import Roads, Gather, Items, Users, Posts, Flag
from . import db, rest, auth, PER_PAGE


@rest.route('/roads/<int:roadid>', methods=['GET'])
def get_road(roadid):
    """Get  a specific road"""
    road = Roads.query.get_or_404(roadid)
    road_dict = road.to_dict()
    # attach items included in road
    r_items = road.items.order_by(Gather.order).limit(42)  # special limit num
    marks = [m.to_dict() for m in r_items]
    road_dict['marks'] = marks
    # cal done num
    itemids = [i.item_id for i in r_items]
    done_num = Flag.query.filter(
        Flag.user_id == road.owner.id,
        Flag.flag_label == 3,
        Flag.item_id.in_(itemids)
    ).count()
    road_dict['donenum'] = done_num
    return jsonify(road_dict)


# for challenge page # challenging road
@rest.route('/getonroad')
@auth.login_required
def get_on_road():
    """Get the in-progress Road: earliest and not done """
    userid = request.args.get('userid', '')
    user = Users.query.get_or_404(userid) if userid else g.user
    road = user.roads.filter_by(done=False).first()
    road_dict = {'items': []}
    if road:
        road_dict = road.to_dict()
        # attach items included in road: not done, per order
        # not need items in some case
        noitem = request.args.get('noitem', False)
        items = [
            t.item.to_simple_dict()
            for t in road.items.order_by(Gather.order)
            if Flag.query.filter_by(
                user_id=user.id,
                flag_label=3,
                item_id=t.item_id
            ).first() is None
        ] if not noitem else []
        road_dict['items'] = items
    return jsonify(road_dict)


@rest.route('/roads', methods=['GET'])
@auth.login_required
def get_roads():
    # get query args
    rf = request.args.get('rf', '') # my -all my, on -nodones
    userid = request.args.get('userid', '')
    # yield query
    user = Users.query.get_or_404(userid) if userid else g.user
    roads_query = user.roads
    # per rf
    if rf == 'my':
        roads = roads_query.order_by(Roads.done, Roads.timestamp.desc())
    elif rf == 'on':
        roads = roads_query.filter_by(done=False)
    else:
        # roads = Roads.query
        abort(403)
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # limit per PER_PAGE
    rs_list = roads.offset(page*per_page).limit(per_page)
    # yield result: a dict
    roads_dict = {
        'roads': [r.to_dict() for r in rs_list],
        'total': roads.count(),
        'currentpage': page
    }
    return jsonify(roads_dict)


@rest.route('/roads', methods=['POST'])
@auth.login_required
def new_road():
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    deadline = request.json.get('deadline')
    # extract tags
    taglst = re.findall(r'#(\w+)', intro)
    if not (title and intro and deadline):
        abort(403)  # cannot be ''
    user = g.user
    road = Roads(
        owner=user,
        title=title,
        intro=intro,
        deadline=deadline
    )
    db.session.add(road)
    road.rtag_to_db(taglst)
    db.session.commit()
    return jsonify({'id': road.id, 'title': road.title})


@rest.route('/roads/<int:roadid>', methods=['PUT'])
@auth.login_required
def edit_road(roadid):
    road = Roads.query.get_or_404(roadid)
    # check not-null column can not be ''
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    # extract tags
    taglst = re.findall(r'#(\w+)', intro)
    if not (title and intro):
        abort(403)  # cannot be ''
    user = g.user
    if user != road.owner:
        abort(403)
    road.title = title
    road.intro = intro
    # renew the update time and add to db
    road.renew()
    # db.session.add(road)
    road.rtag_to_db(taglst)
    db.session.commit()
    return jsonify(road.to_dict())


@rest.route('/roads/<int:roadid>/done', methods=['PATCH'])
@auth.login_required
def mark_road_done(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if user != road.owner:
        abort(403)
    road.as_done()
    return jsonify(road.done)


@rest.route('/roads/<int:roadid>/deadline', methods=['PATCH'])
@auth.login_required
def edit_deadline(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if user != road.owner:
        abort(403)
    deadline = request.json.get('date', '')
    road.deadline = deadline
    db.session.add(road)
    db.session.commit()
    due = road.deadline
    return jsonify(due)


@rest.route('/roads/<int:roadid>/items/<int:itemid>', methods=['POST'])
@auth.login_required
def add_item_to_road(roadid, itemid):
    """Add item to roadmap, i.e. add new marks"""
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if user != road.owner:
        abort(403)
    if road.items.count() >= 42:  # special limit num
        abort(418)
    item = Items.query.get_or_404(itemid)
    mark = request.json.get('mark', '...').strip()
    road.gathering(item, mark)
    # check if need to alter road to not-done per frontend request
    alter = request.json.get('alter', False)
    if alter:
        road.done = False
        road.converted = False
        db.session.add(road)
    db.session.commit()
    # to load mark_dict, radditem: load, itemtor, not
    load = request.json.get('load', False)
    g_dict = {}
    if load:
        gi = Gather.query.filter_by(road_id=roadid, item_id=itemid).first()
        g_dict = gi.to_dict() if gi else {}
    return jsonify(g_dict)


@rest.route('/marks/<int:gid>', methods=['PUT'])
@auth.login_required
def edit_mark(gid):
    mark_g = Gather.query.filter_by(id=gid).first_or_404()  # collect 's id
    road_id = mark_g.road_id
    road = Roads.query.get_or_404(road_id)
    user = g.user
    if road.owner != user:
        abort(403)
    # get the data
    order = request.json.get('order')
    mark = request.json.get('mark', '').strip()
    if not order or not mark:
        abort(403)  # cannot be None
    item = Items.query.get_or_404(mark_g.item_id)
    # re-ordering
    road.ordering(item, order)
    road.renew()
    mark_g.mark = mark
    db.session.add(mark_g)
    db.session.commit()
    return jsonify('Done')


@rest.route('/marks/<int:gid>', methods=['DELETE'])
@auth.login_required
def del_mark(gid):
    """Del, re-ordering items"""
    mark_g = Gather.query.filter_by(id=gid).first_or_404()
    road = Roads.query.get_or_404(mark_g.road_id)
    user = g.user
    if user != road.owner and user.role.duty != 'Admin':
        abort(403)
    # once delete an item. need to re-ordering,
    # order the to-be-del item to the last, then del
    item = Items.query.get_or_404(mark_g.item_id)
    n = road.items.count()
    road.ordering(item, n)
    db.session.delete(mark_g)
    db.session.commit()
    roadid = road.id
    return jsonify(roadid)


@rest.route('/road/<int:roadid>/torut', methods=['PATCH'])
@auth.login_required
def convert_road_to_rut(roadid):  #  -test
    """convert road to rut when get road done"""
    road = Roads.query.get_or_404(roadid)
    if road.converted or (not road.done):
        return jsonify(False)
    user = g.user
    if user != road.owner:
        abort(403)
    rut = road.post
    if rut:
        rut.itle = road.title
        rut.intro = road.intro
    else:
        rut = Posts(
            creator=user,
            road=road,
            title=road.title,
            intro=road.intro,
            rating="All"
        )
    db.session.add(rut)
    # db.session.commit()
    for ga in road.items:
        item = ga.item
        tips = ga.mark
        od = ga.order
        rut.collecting(item, tips, user, od=od)
    # change to converted
    road.converted = True
    db.session.add(road)
    # tag rut
    tags = road.rtags
    for tag in tags:
        tag.posts.append(rut)
        db.session.add(tag)
    db.session.commit()
    return jsonify({'id': rut.id, 'title': rut.title})


@rest.route('/roads/<int:roadid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_or_enable_road(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if road.owner != user and user.role.duty != 'Admin':
        abort(403)
    dis_or_enb = request.json.get('disbaled', True)
    road.disabled = dis_or_enb
    db.session.add(road)
    db.session.commit()
    return jsonify(road.disabled)


@rest.route('/roads/<int:roadid>', methods=['DELETE'])
@auth.login_required
def delete_road(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if road.owner != user and user.role.duty != 'Admin':
        abort(403)
    db.session.delete(road)
    db.session.commit()
    return jsonify('Deleted')
