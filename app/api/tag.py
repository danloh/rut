# -*- coding: utf-8 -*-
# tag: a topic

from flask import request, g, jsonify, abort
from ..models import Tags, Posts, Demands, Items, Comments
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


@rest.route('/gettagid/<string:tagname>')
def get_tagid(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    return jsonify(tag.id)


@rest.route('/tag/<string:tagname>')
@auth.login_required
def get_tag(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    tag_dict = tag.to_dict()
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


@rest.route('/tag/<string:tagname>/ruts')
@auth.login_required
def get_tag_ruts(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    # request param {page: int}
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    post_query = tag.posts
    posts = post_query.order_by(Posts.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tagruts = [p.to_simple_dict() for p in posts]
    tagruts_dict = {'ruts': tagruts, 'rutcount': post_query.count()}
    return jsonify(tagruts_dict)


@rest.route('/tag/<string:tagname>/demands')
@auth.login_required
def get_tag_demands(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demand_query = tag.demands
    demands = demand_query.order_by(Demands.point_incre.desc(), Demands.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tag_demands = [d.to_dict() for d in demands]
    tagdemands_dict = {'demands': tag_demands, 'demandcount': demand_query.count()}
    return jsonify(tagdemands_dict)


@rest.route('/tag/<string:tagname>/items')
@auth.login_required
def get_tag_items(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    item_query = tag.items
    items = item_query.order_by(Items.vote_incre.desc(), Items.vote.desc())\
        .offset(per_page * page).limit(per_page)
    tag_items = [i.to_dict() for i in items]
    tagitems_dict = {'items': tag_items, 'itemcount': item_query.count()}
    return jsonify(tagitems_dict)


@rest.route('/tag/<string:tagname>/comments')
@auth.login_required
def get_tag_comments(tagname):
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    comment_query = tag.comments
    comments = comment_query.order_by(Comments.vote.desc(), Comments.timestamp.desc())\
                            .offset(per_page * page).limit(per_page)
    tag_comments = [c.to_dict() for c in comments]
    tagcomments_dict = {'comments': tag_comments, 'commentcount': comment_query.count()}
    return jsonify(tagcomments_dict)


@rest.route('/tag/<string:tagname>/relates')
@auth.login_required
def get_tag_relates(tagname):
    # page = request.args.get('page', 0, type=int)
    # per_page = request.args.get('perPage', PER_PAGE, type=int)
    tag = Tags.query.filter_by(tag=tagname).first_or_404()
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
    ftcolor = request.json.get('ftcolor', '').strip()
    bgcolor = request.json.get('bgcolor', '').strip()
    description = request.json.get('description', '').strip()
    if not name:
        abort(403)
    query = Tags.query
    tag = query.get_or_404(tagid)
    user = g.user
    if tag.check_locked(user.id):
        return jsonify('In Editing')
    t = query.filter_by(tag=name).first()
    if t and t != tag:
        abort(403)  # cannot Duplicated Tag Name
    tag.tag = name
    tag.descript = description
    tag.logo = logo
    tag.ftcolor = ftcolor
    tag.bgcolor = bgcolor
    db.session.add(tag)
    # update parent tag
    if parent:
        parent_tag = query.filter_by(tag=parent).first()
        if not parent_tag:
            parent_tag = Tags(tag=parent)
            db.session.add(parent_tag)
        tag.parent(parent_tag)
    db.session.commit()
    tag_dict = tag.to_dict()
    return jsonify(tag_dict)


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
