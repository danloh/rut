# -*- coding: utf-8 -*-
"""road is learning road map"""

from flask import request, g, jsonify, abort
from ..models import Roads, Gather, Items, Users, Posts
from . import db, rest, auth, PER_PAGE


@rest.route('/road/<int:roadid>')
def get_road(roadid):
    """Get  a specific road"""
    road = Roads.query.get_or_404(roadid)
    road_dict = road.to_dict()
    # attach items included in road
    r_items = road.items.order_by(Gather.order).limit(42)
    marks = [m.to_dict() for m in r_items]
    road_dict['marks'] = marks
    return jsonify(road_dict)


@rest.route('/<int:userid>/roads')
def get_roads(userid):
    """Get the roads which user have not done"""
    # yield query
    user = Users.query.get_or_404(userid)
    roads = user.roads.filter_by(done=False)
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # limit per PER_PAGE
    rs = roads.offset(page*per_page).limit(per_page)
    # yield result: a dict
    roads_dict = {
        'roads': [r.to_dict() for r in rs],
        'total': roads.count(),
        'currentpage': page
    }
    return jsonify(roads_dict)


# for challenge page
@rest.route('/getonroad')  # challenging road
@auth.login_required
def get_on_road():
    """Get the working Road: earliest and not done """
    user = g.user
    road = user.roads.filter_by(done=False).first()
    road_dict = {'items': []}
    if road:
        road_dict = road.to_dict()
        # attach items included in road
        items = [t.item.to_simple_dict() for t in road.items]
        road_dict['items'] = items
    return jsonify(road_dict)


@rest.route('/<int:userid>/allroads')
def get_all_roads(userid):
    """Get  All, order per done or not and timestamp"""
    # yield query
    user = Users.query.get_or_404(userid)
    roads = user.roads.order_by(Roads.done, Roads.timestamp.desc())
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    rs = roads.offset(page*per_page).limit(per_page)
    # yield result: a dict
    roads_dict = {
        'roads': [r.to_dict() for r in rs],
        'total': roads.count(),
        'currentpage': page
    }
    return jsonify(roads_dict)


@rest.route('/markasdone/<int:roadid>')
@auth.login_required
def mark_road_done(roadid):
    road = Roads.query.get_or_404(roadid)
    road.as_done()
    return jsonify(road.done)


@rest.route('/newroad', methods=['POST'])
@auth.login_required
def new_road():
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    deadline = request.json.get('deadline')
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
    db.session.commit()
    return jsonify({'id': road.id, 'title': road.title})


@rest.route('/editroad/<int:roadid>', methods=['POST'])
@auth.login_required
def edit_road(roadid):
    road = Roads.query.get_or_404(roadid)
    # check not-null column can not be ''
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    if (not title) or (not intro):
        abort(403)  # cannot be ''
    road.title = title
    road.intro = intro
    # renew the update time and add to db
    road.renew()
    # db.session.add(road)
    db.session.commit()
    return jsonify(road.to_dict())


@rest.route('/resetdeadline')
@auth.login_required
def edit_deadline():
    roadid = request.args.get('roadid')
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if user != road.owner:
        abort(403)
    deadline = request.args.get('date')
    road.deadline = deadline
    db.session.add(road)
    db.session.commit()
    due = road.deadline
    return jsonify(due)


@rest.route('/editmark/<int:gid>', methods=['POST'])
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


@rest.route('/item/<int:itemid>/toroad/<int:roadid>', methods=['GET', 'POST'])
@auth.login_required
def item_to_road(itemid, roadid):
    """Add item to roadmap"""
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if user != road.owner or road.items.count() >= 42:
        abort(403)
    item = Items.query.get_or_404(itemid)
    mark = request.json.get('mark', '...').strip()
    road.gathering(item, mark)
    db.session.commit()
    # to load mark_dict, radditem: load, itemtor, not
    load = request.json.get('load', False)
    g_dict = {}
    if load:
        gi = Gather.query.filter_by(road_id=roadid, item_id=itemid).first()
        g_dict = gi.to_dict() if gi else {}
    return jsonify(g_dict)


@rest.route('/delmark/<int:gid>')
@auth.login_required
def del_mark(gid):
    """Del, re-ordering items"""
    mark_g = Gather.query.filter_by(id=gid).first_or_404()
    road = Roads.query.get_or_404(mark_g.road_id)
    user = g.user
    if user != road.owner and user.role != 'Admin':
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


@rest.route('/convertroad/<int:roadid>/torut')
@auth.login_required
def convert_road_to_rut(roadid):
    """convert road to rut when get  road done"""
    road = Roads.query.get_or_404(roadid)
    if road.converted:
        return jsonify(False)
    user = g.user
    rut = Posts(
        creator=user,
        title=road.title,
        intro=road.intro,
        rating="All"
    )
    db.session.add(rut)
    #db.session.commit()
    for ga in road.items:
        item = ga.item
        tips = ga.mark
        od = ga.order
        rut.collecting(item, tips, user, od=od)
    # change to converted
    road.converted = True
    db.session.add(road)
    db.session.commit()
    return jsonify({'id': rut.id, 'title': rut.title})


@rest.route('/disable/road/<int:roadid>')
@auth.login_required
def disable_road(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if road.owner != user and user.role != 'Admin':
        abort(403)
    road.disabled = True
    db.session.add(road)
    db.session.commit()
    return jsonify('Disabled')


@rest.route('/recover/road/<int:roadid>')
@auth.login_required
def recover_road(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if road.owner != user and user.role != 'Admin':
        abort(403)
    road.disabled = False  # enable
    db.session.add(road)
    db.session.commit()
    return jsonify('Enabled')


@rest.route('/delroad/<int:roadid>')
@auth.login_required
def delete_road(roadid):
    road = Roads.query.get_or_404(roadid)
    user = g.user
    if road.owner != user and user.role != 'Admin':
        abort(403)
    db.session.delete(road)
    db.session.commit()
    return jsonify('Deleted')
