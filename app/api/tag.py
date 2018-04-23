# -*- coding: utf-8 -*-
# tag: a topic

from flask import request, g, jsonify, abort
from ..models import Tags, Posts, Demands, Items
from . import db, rest, auth, PER_PAGE


@rest.route('/all/tags')
@auth.login_required
def get_all_tags():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_tags = Tags.query
    tags = all_tags.offset(page*per_page).limit(per_page)
    tags_dict = {
        'tags': [t.to_dict() for t in tags],
        'total': all_tags.count(),
        'currentpage': page
    }
    return jsonify(tags_dict)


@rest.route('/gettag/<string:tagname>')
def get_tagid(tagname):
    tagname = str(tagname).split("@")[-1]
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    return jsonify(tag.id)

@rest.route('/tag/<int:tagid>')
@auth.login_required
def get_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    tag_dict = tag.to_dict()
    # attach ruts included in tag
    tagruts = [
        p.to_dict() for p in tag.posts.order_by(Posts.timestamp.desc()).limit(PER_PAGE)
    ]
    # tagruts.reverse()  # as order_by, which is faster?
    tag_dict['ruts'] = tagruts
    tag_dict['total'] = tag.posts.count()  # len(tagruts)
    # related tags
    parent_tags = [
        t.parent_tag for t in tag.parent_tags.order_by(db.func.rand()).limit(5)
    ]
    tags = parent_tags
    for tg in parent_tags + [tag]:
        child_tags = [
            t.child_tag for t in tg.child_tags.order_by(db.func.rand()).limit(5)
        ]
        tags += child_tags
    relate_tags = set(tags)-set([tag])
    tag_dict['tags'] = [{'tagid': t.id, 'tagname': t.tag} for t in relate_tags]
    return jsonify(tag_dict)


@rest.route('/tag/<int:tagid>/ruts')
@auth.login_required
def get_tag_ruts(tagid):
    tag = Tags.query.get_or_404(tagid)
    # request param {page: int}
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    post_query = tag.posts
    posts = post_query.order_by(Posts.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tagruts = [p.to_simple_dict() for p in posts]
    tagruts_dict = {'ruts': tagruts, 'rutcount': post_query.count()}
    return jsonify(tagruts_dict)


@rest.route('/tag/<int:tagid>/demands')
@auth.login_required
def get_tag_demands(tagid):
    tag = Tags.query.get_or_404(tagid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demand_query = tag.demands
    demands = demand_query.order_by(Demands.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tag_demands = [d.to_dict() for d in demands]
    tagdemands_dict = {'demands': tag_demands, 'demandcount': demand_query.count()}
    return jsonify(tagdemands_dict)


@rest.route('/tag/<int:tagid>/items')
@auth.login_required
def get_tag_items(tagid):
    tag = Tags.query.get_or_404(tagid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    item_query = tag.items
    items = item_query.order_by(Items.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tag_items = [i.to_dict() for i in items]
    tagitems_dict = {'items': tag_items, 'itemcount': item_query.count()}
    return jsonify(tagitems_dict)


@rest.route('/tag/<int:tagid>/relates')
@auth.login_required
def get_tag_relates(tagid):
    # page = request.args.get('page', 0, type=int)
    # per_page = request.args.get('perPage', PER_PAGE, type=int)
    tag = Tags.query.get_or_404(tagid)
    parent_tags = [t.parent_tag for t in tag.parent_tags]
    related_tags = []
    for tg in parent_tags:
        c_tags = [t.child_tag for t in tg.child_tags]
        related_tags += c_tags
    relate_tags_set = set(related_tags) - set([tag])
    child_tags = [t.child_tag for t in tag.child_tags]
    tags_dict = {
        'parents': [t.to_dict() for t in parent_tags],
        'totalparents': len(parent_tags),
        'children': [t.to_dict() for t in child_tags],
        'totalchildren': len(child_tags),
        'relates': [t.to_dict() for t in relate_tags_set],
        'totalrelates': len(relate_tags_set)
    }
    return jsonify(tags_dict)


@rest.route('/searchtags')
@auth.login_required
def search_tags():
    """Search tag"""
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify(None)
    # related pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    tags = Tags.query.filter(Tags.tag.contains(name))\
                     .offset(page*per_page).limit(per_page)
    tags_list = [{'id': t.id, 'name': t.tag} for t in tags]
    return jsonify(tags_list)


@rest.route('/locktag/<int:tagid>')
@auth.login_required
def lock_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    user = g.user
    tag.lock(user)
    return jsonify('Locked')


@rest.route('/unlocktag/<int:tagid>')
def unlock_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    tag.unlock()
    return jsonify('UnLocked')


@rest.route('/checkiftag/<int:tagid>/lockedto/<int:userid>')
def check_tag_if_locked(tagid, userid):
    tag = Tags.query.get_or_404(tagid)
    is_locked = tag.check_locked(userid)
    return jsonify(is_locked)


@rest.route('/edittag/<int:tagid>', methods=['POST'])
@auth.login_required
def edit_tag(tagid):
    # get data
    name = request.json.get('name', '').strip()
    parent = request.json.get('parent', '').strip()
    logo = request.json.get('logo', '').strip()
    description = request.json.get('description', '').strip()
    if not name:
        abort(403)
    query = Tags.query
    tag = query.get_or_404(tagid)
    user = g.user
    if tag.check_locked(user.id):
        return jsonify('In Editing')
    name = name.title()  # titlecased style
    if tag.tag.title() != name and query.filter_by(tag=name).first():
        abort(403)  # cannot Duplicated Tag Name
    tag.tag = name
    tag.descript = description
    tag.logo = logo
    db.session.add(tag)
    # update parent tag
    if parent:
        parent_tag = query.filter_by(tag=parent).first()
        if not parent_tag:
            parent_tag = Tags(tag=parent.title())
            db.session.add(parent_tag)
        tag.parent(parent_tag)
    db.session.commit()
    return jsonify('Tag Info Updated, Thank You')


@rest.route('/delete/tag/<int:tagid>')
@auth.login_required
def del_tag(tagid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    tag = Tags.query.get_or_404(tagid)
    db.session.delete(tag)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/disable/tag/<int:tagid>')
@auth.login_required
def disable_tag(tagid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    tag = Tags.query.get_or_404(tagid)
    tag.disabled = True
    db.session.add(tag)
    db.session.commit()
    return jsonify('Disabled')


@rest.route('/recover/tag/<int:tagid>')
@auth.login_required
def recover_tag(tagid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    tag = Tags.query.get_or_404(tagid)
    tag.disabled = False  # enable
    db.session.add(tag)
    db.session.commit()
    return jsonify('Enabled')


@rest.route('/checkfavtag/<int:tagid>')
@auth.login_required
def check_fav(tagid):
    tag = Tags.query.get_or_404(tagid)
    user = g.user
    faving = 'UnFollow' if user.faving(tag) else 'Follow'
    return jsonify(faving)


@rest.route('/fav/tag/<int:tagid>')
@auth.login_required
def fav_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    user = g.user
    user.fav(tag)
    # record activity as favor a tag
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Followed', tagid=tag.id)
    return jsonify('UnFollow')


@rest.route('/unfav/tag/<int:tagid>')
@auth.login_required
def unfav_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    user = g.user
    user.unfav(tag)
    return jsonify('Follow')
