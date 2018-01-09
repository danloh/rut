# -*- coding: utf-8 -*-
# tag: a topic

from flask import request, g, jsonify, abort
from ..models import *
from . import db, rest, auth, PER_PAGE

@rest.route('/all/tags')
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

@rest.route('/tag/<int:tagid>')
def get_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    tag_dict = tag.to_dict()
    #attach ruts included in tag 
    tagruts = [p.to_dict() \
            for p in tag.posts.order_by(Posts.timestamp.desc()).limit(PER_PAGE)]
    #tagruts.reverse()  # as order_by, which is faster?
    tag_dict['ruts'] = tagruts
    tag_dict['total'] = tag.posts.count() #len(tagruts)
    # related tags
    parent_tags = [t.parent_tag \
                for t in tag.parent_tags.order_by(db.func.rand()).limit(5)]
    tags = parent_tags
    for tg in parent_tags:
        child_tags = [t.child_tag \
                    for t in tg.child_tags.order_by(db.func.rand()).limit(5)]
        tags += child_tags
    tag_dict['tags'] = [{'tagid': t.id,'tagname': t.tag} for t in set(tags)]
    return jsonify(tag_dict)

@rest.route('/tag/<int:tagid>/ruts')
def get_tag_ruts(tagid):
    tag = Tags.query.get_or_404(tagid)
    # request param {page: int}
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    posts = tag.posts.order_by(Posts.timestamp.desc())\
                    .offset(per_page * page).limit(per_page)
    tagruts = [p.to_dict() for p in posts]
    return jsonify(tagruts)

@rest.route('/tag/<int:tagid>/demands')
def get_tag_demands(tagid):
    tag = Tags.query.get_or_404(tagid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = tag.demands.order_by(Demands.timestamp.desc())\
                        .offset(per_page * page).limit(per_page)
    tag_demands = [d.to_dict() for d in demands]
    return jsonify(tag_demands)

@rest.route('/tag/<int:tagid>/relates')
def get_tag_relates(tagid):
    #page = request.args.get('page', 0, type=int)
    #per_page = request.args.get('perPage', PER_PAGE, type=int)
    tag = Tags.query.get_or_404(tagid)
    parent_tags = [t.parent_tag for t in tag.parent_tags]
    related_tags = []
    for tg in parent_tags:
        c_tags = [t.child_tag for t in tg.child_tags]
        related_tags += c_tags
    child_tags = [t.child_tag for t in tag.child_tags]
    tags_dict = {
        'parents': [t.to_dict() for t in parent_tags],
        'totalparents': len(parent_tags),
        'children': [t.to_dict() for t in child_tags],
        'totalchildren': len(child_tags),
        'relates': [t.to_dict() for t in related_tags],
        'totalrelates': len(related_tags)
    }
    return jsonify(tags_dict) 

@rest.route('/edittag/<int:tagid>', methods=['POST'])
@auth.login_required
def edit_tag(tagid):
    query = Tags.query
    tag = query.get_or_404(tagid)
    # get data
    name = request.json.get('name','').strip()
    parent = request.json.get('parent','').strip()
    description = request.json.get('description','').strip()
    if not name:
        abort(403)
    if tag.tag != name and query.filter_by(tag=name).first():
        abort(403) # no Duplicated Tag Name
    tag.tag = name
    tag.descript = description
    db.session.add(tag)
    # update parent tag
    if parent:
        parent_tag = query.filter_by(tag=parent).first()
        if not parent_tag:
            parent_tag = Tags(tag=parent)
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
    tag.disabled = False #enable
    db.session.add(tag)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/checkfavtag/<int:tagid>')
@auth.login_required
def check_fav(tagid):
    user = g.user
    tag = Tags.query.get_or_404(tagid)
    faving = 'UnFollow' if user.faving(tag) else 'Follow'
    return jsonify(faving)

@rest.route('/fav/tag/<int:tagid>')
@auth.login_required
def fav_tag(tagid):
    user = g.user
    tag = Tags.query.get_or_404(tagid)
    # record activity as favor a tag
    user.set_event(action='Followed', tag=tag)
    user.fav(tag)
    return jsonify('UnFollow')

@rest.route('/unfav/tag/<int:tagid>')
@auth.login_required
def unfav_tag(tagid):
    user = g.user
    tag = Tags.query.get_or_404(tagid)
    user.unfav(tag)
    return jsonify('Follow')