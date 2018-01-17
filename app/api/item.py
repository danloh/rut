# -*- coding: utf-8 -*-
# item : such as book, on-line course, etc. as a element in a rut

from flask import request, g, jsonify, abort
from ..models import *
from ..utils import str_to_dict
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
    #get request params
    userid = request.args.get('userid', '')
    ref = request.args.get('ref', '') # hot or new
    # yield query
    query = Reviews.query.filter_by(item_id=itemid) #item.reviews # 
    if userid:
        reviews = query.filter_by(creator_id=userid) 
    elif ref == 'hot':
        reviews = query.order_by(Reviews.vote.desc())
    elif ref == 'new':
        reviews = query.order_by(Reviews.timestamp.desc())
    else:
        reviews = query
    #pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews_page = reviews.offset(per_page * page).limit(per_page)
    #yield result, a Dict
    review_list = [r.to_dict() for r in reviews_page]
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

@rest.route('/iuclips') # per item or user or any
def get_iu_clips():
    #get request params
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    #yield query
    q = Clips.query
    if userid and itemid:
        query =q.filter_by(creator_id=userid,item_id=itemid)
    elif userid:
        query = q.filter_by(creator_id=userid)
    elif itemid:
        query = q.filter_by(item_id=itemid)
    else:
        query = q
    #pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    order_query = query.order_by(Clips.timestamp.desc())\
                       .offset(page * per_page).limit(per_page)
    #yield result, a Dict
    clips_dict = {
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    }
    return jsonify(clips_dict)

# who todo /doing / done the item
@rest.route('/item/<int:itemid>/todos')
def get_item_todos(itemid):
    pass

@rest.route('/item/<int:itemid>/doings')
def get_item_doings(itemid):
    pass

@rest.route('/item/<int:itemid>/dones')
def get_item_dones(itemid):
    pass

@rest.route('/checkflag/item/<int:itemid>')
@auth.login_required
def check_flag(itemid):
    item = Items.query.get_or_404(itemid)
    user = g.user
    flaging = user.flaging(item)
    return jsonify(flaging)

@rest.route('/flagtodo/item/<int:itemid>')
@auth.login_required
def flag_item_todo(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.args.get('note','').strip()
    user = g.user
    # record activity as want to read an item
    user.set_event(action='Scheduled', item=item)
    user.flag(item,1,note)
    return jsonify('Scheduled')

@rest.route('/flagdoing/item/<int:itemid>')
@auth.login_required
def flag_item_doing(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.args.get('note','').strip()
    user = g.user
    # record activity asworking an item
    user.set_event(action='Working on', item=item)
    user.flag(item,2,note)
    return jsonify('Working On')

@rest.route('/flagdone/item/<int:itemid>')
@auth.login_required
def flag_item_done(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.args.get('note','').strip()
    user = g.user
    # record activity as have done an item
    user.set_event(action='Get done', item=item)
    user.flag(item,3,note)
    return jsonify('Done')

@rest.route('/lockitem/<int:itemid>')
@auth.login_required
def lock_item(itemid):
    item = Items.query.get_or_404(itemid)
    user = g.user
    item.lock(user)
    return jsonify('Locked')

@rest.route('/unlockitem/<int:itemid>')
def unlock_item(itemid):
    item = Items.query.get_or_404(itemid)
    item.unlock()
    return jsonify('UnLocked')

@rest.route('/checkifitem/<int:itemid>/lockedto/<int:userid>')
def check_item_if_locked(itemid, userid):
    item = Items.query.get_or_404(itemid)
    is_locked = item.check_locked(userid)
    return jsonify(is_locked)

@rest.route('/edititem/<int:itemid>', methods=['POST'])
@auth.login_required
def edit_item(itemid):
    uid = request.json.get('uid','').replace('-','').replace(' ','')
    title = request.json.get('title','').strip()
    if not uid or not title:
        abort(403)
    query = Items.query
    item = query.get_or_404(itemid)
    user = g.user
    if item.check_locked(user.id):
        return jsonify('In Editing')
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