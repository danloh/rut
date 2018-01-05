# -*- coding: utf-8 -*-
# item : such as book, on-line course, etc. as a element in a rut

from flask import current_app, request, g, jsonify, abort
from ..models import *
from ..utils import split_str, str_to_dict, str_to_set

from . import db, rest, auth, PER_PAGE

@rest.route('/all/items')
def get_all_items():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_items = Items.query
    items = all_items.offset(page*per_page).limit(per_page)
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': all_items.count(),
        'currentpage': page
    }
    return jsonify(items_dict)

@rest.route('/<int:userid>/doing/items')
def get_doing_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=2).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

@rest.route('/<int:userid>/todo/items')
def get_todo_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=1).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

@rest.route('/<int:userid>/done/items')
def get_done_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=3).order_by(Flag.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    items = [d.flag_item for d in flags.offset(page * per_page).limit(per_page)]
    items_dict = {
        'items': [i.to_dict() for i in items],
        'total': flags.count()
    }
    return jsonify(items_dict)

@rest.route('/checkflag/item/<int:itemid>')
@auth.login_required
def check_flag(itemid):
    user = g.user
    item = Items.query.get_or_404(itemid)
    flaging = user.flaging(item)
    return jsonify(flaging)

@rest.route('/flagtodo/item/<int:itemid>')
@auth.login_required
def flag_item_todo(itemid):
    user = g.user
    item = Items.query.get_or_404(itemid)
    user.flag(item,1)
    return jsonify('Scheduled')

@rest.route('/flagdoing/item/<int:itemid>')
@auth.login_required
def flag_item_doing(itemid):
    user = g.user
    item = Items.query.get_or_404(itemid)
    user.flag(item,2)
    return jsonify('Working On')

@rest.route('/flagdone/item/<int:itemid>')
@auth.login_required
def flag_item_done(itemid):
    user = g.user
    item = Items.query.get_or_404(itemid)
    user.flag(item,3)
    return jsonify('Done')

@rest.route('/item/<int:itemid>')
def get_item(itemid):
    item = Items.query.get_or_404(itemid)
    item_dict = item.to_dict()
    ruts = [c.post \
        for c in item.posts.order_by(Collect.timestamp.desc()).limit(PER_PAGE)]
    included_ruts = [{'id':r.id, 'title': r.title} for r in ruts]
    item_dict['inruts'] = included_ruts
    return jsonify(item_dict)

@rest.route('/item/<int:itemid>/reviews')
def get_item_reviews(itemid):
    #item = Items.query.get_or_404(itemid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ref = request.args.get('ref', '') # hot or new
    reviews = Reviews.query.filter_by(item_id=itemid) #item.reviews # 
    if ref == 'hot':
        hotreviews = reviews.order_by(Reviews.vote.desc())\
                            .offset(per_page * page).limit(per_page)
        review_list = [r.to_dict() for r in hotreviews]
    if ref == 'new':
        newreviews = reviews.order_by(Reviews.timestamp.desc())\
                            .offset(per_page * page).limit(per_page)
        review_list = [r.to_dict() for r in newreviews]
    reviews_dict = {
        'reviewcount': reviews.count(), 
        'reviews': review_list
    }
    return jsonify(reviews_dict)

@rest.route('/item/<int:itemid>/inruts')
def get_item_inruts(itemid):
    item = Items.query.get_or_404(itemid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    included_ruts = item.posts.order_by(Collect.timestamp.desc())\
                              .offset(per_page * page).limit(per_page)
    ruts_list = [c.post for c in included_ruts]
    in_ruts_list = [{'id':r.id, 'title': r.title} for r in ruts_list]
    return jsonify(in_ruts_list)

@rest.route('/edititem/<int:itemid>', methods=['POST'])
@auth.login_required
def edit_item(itemid):
    uid = request.json.get('uid','').replace('-','').replace(' ','')
    title = request.json.get('title','').strip()
    if not uid or not title:
        abort(403)
    query = Items.query
    item = query.get_or_404(itemid)
    if query.filter_by(uid=uid).first() and item.uid != uid:
        abort(403) # can not be duplicated uid
    #update item 
    item.uid = uid
    item.cate = request.json.get('cate')
    item.title = title
    item.author = request.json.get('byline','').strip()
    item.cover = request.json.get('cover','').strip()
    item.res_url = request.json.get('resUrl','').strip()
    item.publisher = request.json.get('publisher','').strip()
    item.pub_date = request.json.get('publishDate','').strip()
    item.language = request.json.get('language','').strip()
    item.binding = request.json.get('binding','').strip()
    item.page = request.json.get('page','').strip()
    item.level = request.json.get('level','').strip()
    item.price = request.json.get('price','').strip()
    item.details = request.json.get('details','').strip()
    #edit author  byline
    old_str = item.author
    old_d = str_to_dict(old_str)
    old_set = set(k for k in old_d if k is not "None")
    new_str = request.json.get('byline','').strip()
    new_d = str_to_dict(new_str)
    new_set = set(k for k in new_d)
    add_name = new_set - old_set
    del_name = old_set - new_set

    a_query = Authors.query
    for name in add_name:
        author = a_query.filter_by(name=name).first()
        if author is None:
            new_author = Authors(name=name)
            db.session.add(new_author)
            byline=Byline(
                item=item,
                by=new_author,
                contribution=new_d.get(name,"Author")
            )
            db.session.add(byline)
        else:
            byline=Byline(
                item=item,
                by=author,
                contribution=new_d.get(name,"Author")
            )
            db.session.add(byline)

    b_query = Byline.query
    for name in del_name:
        old_author = a_query.filter_by(name=name).first()
        byline = b_query.filter_by(item=item,by=old_author).first()
        db.session.delete(byline)
    #END edit author byline
    db.session.add(item)
    db.session.commit()
    return jsonify('The item info Updated, Thank You')

@rest.route('/delete/item/<int:itemid>')
@auth.login_required
def del_item(itemid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    item = Items.query.get_or_404(itemid)
    db.session.delete(item)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/item/<int:itemid>')
@auth.login_required
def disable_item(itemid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    item = Items.query.get_or_404(itemid)
    item.disabled = True
    db.session.add(item)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/item/<int:itemid>')
@auth.login_required
def recover_item(itemid):
    user = g.user
    if user.role != 'Admin':
        abort(403)
    item = Items.query.get_or_404(itemid)
    item.disabled = False #enable
    db.session.add(item)
    db.session.commit()
    return jsonify('Enabled')