# -*- coding: utf-8 -*-
# rut is readup tips, included an item list and tips for each item

from flask import request, g, jsonify, abort
from ..models import Posts, Star, Collect, Users, Tags,\
                     Comments, Flag, Demands, Items, Respon
from . import db, rest, auth, PER_PAGE


@rest.route('/index/ruts')
# @auth.login_required
def get_index_ruts():
    # #personalized ruts
    # user = g.user
    # #get related tags set and fav tags
    # tag_set, tag_fv = user.get_tag_set()
    # # get followed posts queries
    # post_fo = [f.followed.posts for f in user.followed]
    # #list the queries, followed _posts as init
    # q = post_fo
    # for tag_obj in tag_set:
    #     q.append(tag_obj.posts)
    # q_rand = Posts.query.order_by(db.func.rand()).limit(0) # !! need to optimize
    # query = q_rand.union(*q)
    # ruts = query.order_by(Posts.timestamp.desc())  # other way,list reverse
    # total = ruts.count()
    # #Top Picked ruts
    ruts = Posts.select_posts()
    total = len(ruts)  # ruts.count() #
    tag_set = Tags.get_tags()
    ruts_dict = {  # need to optimize
        'ruts': ruts,  # [r.to_dict() for r in ruts],
        'total': total,
        'tags': [{'tagid': t.id, 'tagname': t.tag} for t in tag_set]
    }
    return jsonify(ruts_dict)


@rest.route('/rut/<int:rutid>')
def get_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut_dict = rut.to_dict()
    # attach tips and items included in rut
    r_items = rut.items.order_by(Collect.order).limit(42)
    tips = [t.to_dict() for t in r_items]  # in Collect model
    # # sort tips per order-key in collect-dict -- deprecated way
    # from operator import itemgetter
    # order_tips = sorted(tips, key=itemgetter('order'))
    rut_dict['tips'] = tips  # order_tips
    # attach demands respon to
    r_demands = rut.demands.limit(PER_PAGE)
    demands = [{'id': r.demand_id, 'demand': r.demand.body} for r in r_demands]
    rut_dict['demands'] = demands
    return jsonify(rut_dict)


@rest.route('/rut/<int:rutid>/tips')
def get_rut_tips(rutid):
    rut = Posts.query.get_or_404(rutid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 42, type=int)
    r_items = rut.items.order_by(Collect.order)\
                       .offset(page*per_page).limit(per_page)
    tips_list = [t.to_dict() for t in r_items]
    return jsonify(tips_list)


@rest.route('/rut/<int:rutid>/demands')
def get_rut_demands(rutid):
    rut = Posts.query.get_or_404(rutid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    r_demands = rut.demands.offset(page*per_page).limit(per_page)
    demands_list = [{'id': r.demand_id, 'demand': r.demand.body} for r in r_demands]
    return jsonify(demands_list)


@rest.route('/rut/<int:rutid>/stars')
@auth.login_required
def get_rut_stars(rutid):
    # rut = Posts.query.get_or_404(rutid)  #other way: rut.stars
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    stars = Star.query.filter_by(post_id=rutid)
    starcount = stars.count()
    r_stars = stars.offset(page*per_page).limit(per_page)
    stars_list = [u.starer.to_simple_dict() for u in r_stars]
    stars_dict = {
        'stars': stars_list,
        'starcount': starcount
    }
    return jsonify(stars_dict)


@rest.route('/commentsonrut/<int:rutid>')
@auth.login_required
def get_rut_comments(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut_dict = {
        'id': rut.id,
        'title': rut.title
    }
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 50, type=int)
    r_comments = rut.comments
    rut_dict['commentcount'] = r_comments.count()
    rut_comments = r_comments.order_by(Comments.timestamp.desc())\
        .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in rut_comments]
    rut_dict['comments'] = comments
    return jsonify(rut_dict)


@rest.route('/challengeitems')  # challenging items !!
@auth.login_required
def get_challege_items():
    user = g.user
    # get the earliest flaged items as doing
    doing_flags = user.flag_items\
                      .order_by(Flag.timestamp)\
                      .filter_by(flag_label=2).limit(5)
    doing_items = [f.flag_item for f in doing_flags]
    doing_list = [{'id': item.id, 'title': item.title} for item in doing_items]
    return jsonify(doing_list)


@rest.route('/ruts')
@auth.login_required
def get_all_ruts():
    # yield query
    ruts = Posts.query
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts_list = ruts.offset(page*per_page).limit(per_page)
    # yield result: a dict
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts_list],
        'total': ruts.count(),
        'currentpage': page
    }
    return jsonify(ruts_dict)


@rest.route('/checkstar/rut/<int:rutid>')
@auth.login_required
def check_star(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    staring = 'Unstar' if user.staring(rut) else 'Star'
    return jsonify(staring)


@rest.route('/star/rut/<int:rutid>')
@auth.login_required
def star_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    user.star(rut)  # commit included
    # record activity as star a rut
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Starred', postid=rut.id)
    return jsonify('Unstar')


@rest.route('/unstar/rut/<int:rutid>')
@auth.login_required
def unstar_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    user.unstar(rut)
    return jsonify('Star')


@rest.route('/create/', methods=['POST'])
@rest.route('/create/<int:demandid>', methods=['POST'])
@auth.login_required
def new_rut(demandid=None):
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    if not title or not intro:
        abort(403)  # cannot be ''
    user = g.user
    post = Posts(
        creator=user,
        title=title,
        intro=intro,
        tag_str=request.json.get('tag', '42').strip(),
        rating=request.json.get('rating'),
        credential=request.json.get('credential', '...').strip(),
        editable=request.json.get('editable')
    )
    db.session.add(post)
    post.tag_to_db()
    # link to demand as answer if come from demand
    if demandid:
        demand = Demands.query.get(demandid)
        if demand:
            respon = Respon(
                post=post,
                demand=demand
            )
            db.session.add(respon)
    db.session.commit()
    # record activity as create a rut
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Created', postid=post.id)
    return jsonify({'id': post.id, 'title': post.title})


@rest.route('/lockrut/<int:rutid>')
@auth.login_required
def lock_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    rut.lock(user)
    return jsonify('Locked')


@rest.route('/unlockrut/<int:rutid>')
def unlock_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut.unlock()
    return jsonify('UnLocked')


@rest.route('/checkifrut/<int:rutid>/lockedto/<int:userid>')
def check_rut_if_locked(rutid, userid):
    rut = Posts.query.get_or_404(rutid)
    is_locked = rut.check_locked(userid)
    return jsonify(is_locked)


@rest.route('/checkif/<userid>/caneditrut/<int:rutid>')
# @auth.login_required
def check_rut_editable(userid, rutid):
    if not userid:
        return jsonify(False)
    user = Users.query.get_or_404(userid)
    if not user:
        return jsonify(False)
    rut = Posts.query.get_or_404(rutid)
    can_edit = rut.check_editable(user)
    editor_id = rut.editing_id
    can_dict = {'editorid': editor_id, 'rutid': rutid, 'canedit': can_edit}
    return jsonify(can_dict)


@rest.route('/editrut/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    # check if rut editable
    if not rut.check_editable(user):
        abort(403)
    # check not-null column can not be ''
    title = request.json.get('title', '').strip()
    intro = request.json.get('intro', '').strip()
    if (not title) or (not intro):
        abort(403)  # cannot be ''
    rut.title = title
    rut.intro = intro
    rut.rating = request.json.get('rating')
    rut.editable = request.json.get('editable')
    # renew the update time and add to db
    rut.renew()
    # db.session.add(rut)
    db.session.commit()
    return jsonify(rut.to_dict())


@rest.route('/editrutce/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_rut_epi_or_cred(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    # check if rut editable
    if not rut.check_editable(user):
        abort(403)
    credential = request.json.get('credential', '').strip()
    epilog = request.json.get('epilog', '').strip()
    if (not credential) and (not epilog):
        abort(403)  # cannot both be ''
    if credential:
        rut.credential = credential
    if epilog:
        rut.epilog = epilog
    # renew the update time and add to db
    rut.renew()
    # db.session.add(rut)
    db.session.commit()
    ce_dict = {
        'credential': rut.credential,
        'epilog': rut.epilog
    }
    return jsonify(ce_dict)


@rest.route('/edittags/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_rut_tags(rutid):
    rut = Posts.query.get_or_404(rutid)
    old = request.json.get('old')
    new = request.json.get('new')
    old_set = set(old)
    new_set = set(new)
    add_tags = new_set - old_set
    del_tags = old_set - new_set
    query = Tags.query
    for tg in add_tags:
        t = tg.strip()
        if not t:
            continue  # if t is '' then next element
        t = t.title()  # titlecased sytle
        tag = query.filter_by(tag=t).first()
        if tag is None:
            new_tag = Tags(tag=t)
            new_tag.posts.append(rut)
            # new_tag.cal_vote()
            db.session.add(new_tag)
        else:
            tag.posts.append(rut)
            # tag.cal_vote()
            db.session.add(tag)
    for tg in del_tags:
        tag = query.filter_by(tag=tg).first()
        tag.posts.remove(rut)
    db.session.commit()
    new_tags_list = [t.to_dict() for t in rut.tags]
    return jsonify(new_tags_list)


@rest.route('/edittips/<int:cid>', methods=['POST'])
@auth.login_required
def edit_tips(cid):
    tip_collect = Collect.query.filter_by(id=cid).first_or_404()  # collect 's id
    post_id = tip_collect.post_id
    rut = Posts.query.get_or_404(post_id)
    user = g.user
    if not rut.check_editable(user):
        abort(403)
    # get the data
    order = request.json.get('order')
    tips = request.json.get('tips', '').strip()
    if not order or not tips:
        abort(403)  # cannot be None
    item = Items.query.get_or_404(tip_collect.item_id)
    # get the spoiler
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    # re-ordering
    rut.ordering(item, order)
    rut.renew()
    tip_collect.tips = tips
    tip_collect.spoiler = spoiler
    db.session.add(tip_collect)
    db.session.commit()
    return jsonify('Done')


@rest.route('/item/<int:itemid>/torut/<int:rutid>', methods=['GET', 'POST'])
@auth.login_required
def item_to_rut(itemid, rutid):
    """Add existing item to Rut"""
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    if not rut.check_editable(user):
        abort(403)
    item = Items.query.get_or_404(itemid)
    tips = request.json.get('tips', '...').strip()
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    rut.collecting(item, tips, user, spoiler)
    db.session.commit()
    return jsonify('Done')


@rest.route('/del/tips/<int:cid>')
@auth.login_required
def del_tips_in_rut(cid):
    """Del tips, re-ordering items"""
    # collect 's id,but not get_or_404, for 3 primary key
    tip_c = Collect.query.filter_by(id=cid).first_or_404()
    user = g.user
    if user != tip_c.tip_creator and user.role != 'Admin':
        abort(403)
    # once delete an item. need to re-ordering,
    # order the to-be-del item to the last, then del
    item = Items.query.get_or_404(tip_c.item_id)
    rut = Posts.query.get_or_404(tip_c.post_id)
    n = rut.items.count()
    rut.ordering(item, n)
    db.session.delete(tip_c)
    db.session.commit()
    rutid = rut.id
    return jsonify(rutid)


@rest.route('/disable/rut/<int:rutid>')
@auth.login_required
def disable_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    if ((rut.creator != user and user.role != 'Admin')
            or rut.starers.count() != 0):
        abort(403)
    rut.disabled = True
    db.session.add(rut)
    db.session.commit()
    return jsonify('Disabled')


@rest.route('/recover/rut/<int:rutid>')
@auth.login_required
def recover_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    if rut.creator != user and user.role != 'Admin':
        abort(403)
    rut.disabled = False  # enable
    db.session.add(rut)
    db.session.commit()
    return jsonify('Enabled')


@rest.route('/delete/rut/<int:rutid>')
@auth.login_required
def delete_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    user = g.user
    if ((rut.creator != user and user.role != 'Admin')
            or rut.starers.count() != 0):
        abort(403)
    db.session.delete(rut)
    db.session.commit()
    return jsonify('Deleted')
