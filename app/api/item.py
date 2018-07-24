# -*- coding: utf-8 -*-
# item : such as book, on-line course, etc. as a element in a rut

import re
from flask import request, g, jsonify, abort, current_app
from ..models import Items, Flag, Articles, Collect, Byline, Authors
from ..utils import str_to_dict
from ..bot import spider
from . import db, rest, auth, PER_PAGE


@rest.route('/items', methods=['GET'])
@auth.login_required
def get_items():
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


@rest.route('/items/submitted', methods=['GET'])
@auth.login_required
def get_submitted_items():
    user = g.user
    items = user.sub_items.order_by(Items.timestamp.desc()).limit(PER_PAGE)
    item_list = [i.to_simple_dict() for i in items]
    return jsonify(item_list)


@rest.route('/items/<int:itemid>', methods=['GET'])
def get_item(itemid):
    item = Items.query.get_or_404(itemid)
    item_dict = item.to_dict()
    included_ruts = [
        {
            'id': r.post_id,
            'title': r.post.title,
            'itemtip': r.to_dict()
        } for r in item.posts.order_by(Collect.timestamp.desc()).limit(PER_PAGE)
    ]
    item_dict['inruts'] = included_ruts
    return jsonify(item_dict)


@rest.route('/items/<int:itemid>/articles', methods=['GET'])
@auth.login_required
def get_item_articles(itemid):
    # item = Items.query.get_or_404(itemid)
    # get request params
    userid = request.args.get('userid', type=int)
    ref = request.args.get('ref', '')  # hot or new
    # yield query
    query = Articles.query.filter_by(item_id=itemid)  # item.articles
    if userid:
        articles = query.filter_by(submitor_id=userid)
    elif ref == 'hot':
        articles = query.order_by(Articles.point.desc(), Articles.score.desc())
    elif ref == 'new':
        articles = query.order_by(Articles.timestamp.desc())
    else:
        articles = query
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    articles_page = articles.offset(per_page * page).limit(per_page)
    # yield result, a Dict
    article_list = [r.to_dict() for r in articles_page]
    articles_dict = {
        'articlecount': articles.count(),
        'articles': article_list
    }
    return jsonify(articles_dict)


@rest.route('/items/<int:itemid>/inruts', methods=['GET'])
@auth.login_required
def get_item_inruts(itemid):
    item = Items.query.get_or_404(itemid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    included_ruts = item.posts.order_by(Collect.timestamp.desc())\
                              .offset(per_page * page).limit(per_page)
    in_ruts_list = [
        {
            'id': r.post_id,
            'title': r.post.title,
            'itemtip': r.to_dict()
        } for r in included_ruts
    ]
    return jsonify(in_ruts_list)


# who todo /doing / done the item
@rest.route('/items/<int:itemid>/users/<string:flag>', methods=['GET'])
@auth.login_required
def get_item_whoflags(itemid, flag):
    flagers = Flag.query.filter_by(item_id=itemid)
    label_dict = {'todo': 1, 'doing': 2, 'done': 3}
    label = label_dict.get(str(flag), 0)
    flagers = flagers.filter_by(flag_label=label)
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    whos = flagers.offset(page * per_page).limit(per_page)
    flager_dict = {
        'flagers': [f.flager.to_simple_dict() for f in whos],
        'flagcount': flagers.count(),
        'label': flag,
        'itemid': itemid
    }
    return jsonify(flager_dict)


@rest.route('/items/<int:itemid>/flag', methods=['GET'])
@auth.login_required
def check_flag(itemid):
    item = Items.query.get_or_404(itemid)
    user = g.user
    flaging = user.flaging(item)
    return jsonify(flaging)


@rest.route('/items/<int:itemid>/flagtodo', methods=['PATCH'])
@auth.login_required
def flag_item_todo(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.json.get('note', '').strip()
    user = g.user
    user.flag(item, 1, note)
    # record activity as want to read an item
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Scheduled', itemid=item.id)
    return jsonify('Scheduled')


@rest.route('/items/<int:itemid>/flagdoing', methods=['PATCH'])
@auth.login_required
def flag_item_doing(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.json.get('note', '').strip()
    user = g.user
    user.flag(item, 2, note)
    # record activity asworking an item
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Working', itemid=item.id)
    return jsonify('Working')


@rest.route('/items/<int:itemid>/flagdone', methods=['PATCH'])
@auth.login_required
def flag_item_done(itemid):
    item = Items.query.get_or_404(itemid)
    note = request.json.get('note', '').strip()
    user = g.user
    user.flag(item, 3, note)
    # record activity as have done an item
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Get done', itemid=item.id)
    return jsonify('Done')


@rest.route('/items/<int:itemid>/lock', methods=['GET'])
@auth.login_required
def lock_item(itemid):
    item = Items.query.get_or_404(itemid)
    user = g.user
    item.lock(user)
    return jsonify('Locked')


@rest.route('/items/<int:itemid>/unlock', methods=['GET'])
def unlock_item(itemid):
    item = Items.query.get_or_404(itemid)
    item.unlock()
    return jsonify('UnLocked')


@rest.route('/items/<int:itemid>/locked/<int:userid>', methods=['GET'])
def check_item_if_locked(itemid, userid):
    item = Items.query.get_or_404(itemid)
    is_locked = item.check_locked(userid)
    return jsonify(is_locked)


@rest.route('/items/<int:itemid>', methods=['PUT'])
@auth.login_required
def edit_item(itemid):
    uid = request.json.get('uid', '').replace('-', '').replace(' ', '')
    title = request.json.get('title', '').strip()
    if not uid or not title:
        abort(403)
    query = Items.query
    item = query.get_or_404(itemid)
    old_author_str = item.author  # use this later
    user = g.user
    if item.check_locked(user.id):
        return jsonify('In Editing')
    if query.filter_by(uid=uid).first() and item.uid != uid:
        abort(403)  # can not be duplicated uid
    # update item
    item.uid = uid
    item.cate = request.json.get('cate')
    item.title = title
    item.author = request.json.get('byline', '').strip()
    item.cover = request.json.get('cover', '').strip()
    item.itag_str = request.json.get('tags', '').strip()
    item.res_url = request.json.get('resUrl', '').strip()
    item.publisher = request.json.get('publisher', '').strip()
    item.pub_date = request.json.get('publishDate', '').strip()
    item.language = request.json.get('language', '').strip()
    item.binding = request.json.get('binding', '').strip()
    item.page = request.json.get('page', '').strip()
    item.level = request.json.get('level', '').strip()
    item.price = request.json.get('price', '').strip()
    item.details = request.json.get('details', '...').strip()
    # edit author  byline
    old_set = set(k for k in str_to_dict(old_author_str) if k is not "None")
    new_str = request.json.get('byline', '').strip()
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
            byline = Byline(
                item=item,
                by=new_author,
                contribution=new_d.get(name, "Author")
            )
            db.session.add(byline)
        else:
            byline = Byline(
                item=item,
                by=author,
                contribution=new_d.get(name, "Author")
            )
            db.session.add(byline)
    b_query = Byline.query
    for name in del_name:
        old_author = a_query.filter_by(name=name).first()
        byline = b_query.filter_by(item=item, by=old_author).first()
        db.session.delete(byline)
    # END edit author byline
    db.session.add(item)
    # item tags to db
    item.itag_to_db()
    db.session.commit()
    return jsonify('The item info Updated, Thank You')


########## new item func-set ##################

def new_item_pipe(d, uid, user, flag=None):
    new_item = Items(
        uid=uid or spider.random_uid(),
        title=d.get('title', 'untitled').strip(),
        res_url=d.get('resUrl', '').strip(),
        author=d.get('byline', '').strip(),
        cover=d.get('cover', '').strip(),
        cate=d.get('cate', 'Book'),
        publisher=d.get('Publisher', '').strip(),
        pub_date=d.get('PublishDate', '').strip(),
        language=d.get('Language', '').strip(),
        binding=d.get('binding', '').strip(),
        page=d.get('page', '').strip(),
        level=d.get('Level', '').strip(),
        price=d.get('price', '').strip(),
        details=d.get('details', '...').strip(),
        submitor=user
    )
    db.session.add(new_item)
    if d.get('byline', '').strip():
        new_item.author_to_db()
    db.session.commit()
    # flag once item added
    if flag in [1, 2, 3]:
        user.flag(new_item, flag)
    return new_item


def add_new_item(d, user, flag):
    uid = d.get('uid', '').replace('-', '').replace(' ', '')
    res_url = d.get('resUrl', '').strip()
    if not (uid or res_url):
        abort(403)  # cannot be both blank
    # check item if existing per the uid
    old_item = Items.query.filter_by(uid=uid).first() if uid else None
    if old_item:
        # flag once item added
        if flag in [1, 2, 3]:
            user.flag(old_item, flag)  # here a bug: not bound to threading session??
        return old_item
    new_item = new_item_pipe(d, uid, user, flag)
    return new_item


def spider_new_item(app, url, user, flag):
    """add new item via spider async"""
    with app.app_context():
        d = spider.parse_html(url)
        add_new_item(d, user, flag)

########## end new item func-set ##################


@rest.route('/items', methods=['POST'])
@auth.login_required
def submit_new_item():
    """add new item mannually or via spider"""
    res_url = request.json.get('resUrl', '').strip()
    # extratc flag info
    user = g.user
    flag_dict = {'Done': 3, 'Schedule': 1, 'Working': 2}
    label = request.json.get('flag', '').strip()
    flag = flag_dict.get(label)
    # check if the url has been spider-ed,
    re_url = r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    reg_url = re.compile(re_url, 0)
    if reg_url.match(res_url):
        pure_url = res_url.split('/ref=')[0]  # for amazon url
        lst = Items.query.filter(Items.res_url.in_((res_url, pure_url))).all()
        if lst:
            item = lst[0]
            if flag in [1, 2, 3]:
                user.flag(item, flag)
            return jsonify(item.id)
    # via spider or manually
    how = request.json.get('how', '').strip()
    if how == 'spider':
        from threading import Thread
        c_app = current_app._get_current_object()
        thr = Thread(target=spider_new_item, args=[c_app, res_url, user, flag])
        thr.start()
        return jsonify(None)
    else:
        d = request.json
        item = add_new_item(d, user, flag)
        return jsonify(item.id)


@rest.route('/items/<int:itemid>/tags', methods=['POST'])
@auth.login_required
def add_item_tags(itemid):
    item = Items.query.get_or_404(itemid)
    itag_str = request.json.get('tags', '').strip()
    if not itag_str:
        return jsonify(False)
    item.itag_to_db(itag_str)
    db.session.commit()
    tags = [t.to_dict() for t in item.itags][-12:]
    return jsonify(tags)


@rest.route('/items/search/<int:label>', methods=['GET'])
@auth.login_required
def search_items(label):
    uid_or_title = request.args.get('uid_or_title', '').strip()
    user = g.user
    userid = request.args.get('userid', type=int) or user.id
    # related pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # re
    re_url = r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    reg_url = re.compile(re_url, 0)
    # if keyword is '', return flag-items
    if not uid_or_title:
        # abort(403)
        flags = user.flag_items.filter_by(flag_label=label)\
                               .order_by(Flag.timestamp.desc())\
                               .offset(page*per_page).limit(per_page)
        items = [d.flag_item for d in flags]  # i.e. flaged, may huge
    # spider per url
    elif reg_url.match(uid_or_title):
        d = spider.parse_html(uid_or_title)
        item = add_new_item(d, user, label)
        items = [item]
    # query per keyword
    else:
        query = Items.query
        item_uid = query.filter_by(uid=uid_or_title)
        item_title = query.filter(Items.title.contains(uid_or_title))  # query per substring
        items = item_uid.union(item_title)\
            .offset(page*per_page).limit(per_page).all()
    if not items:
        return jsonify({'items': [], 'keyword': uid_or_title})
    items_list = []
    for item in set(items):
        if not item:
            continue
        # filter per label to get result from flag-items or all
        if label in [1, 2, 3] and userid and uid_or_title:
            flag = Flag.query.filter_by(
                user_id=userid,
                item_id=item.id,
                flag_label=label
            ).first()
            if flag is None:
                continue
        item_dict = {
            'id': item.id,
            'cate': item.cate,
            'title': item.title
        }
        items_list.append(item_dict)
    return jsonify({'items': items_list, 'keyword': uid_or_title})


@rest.route('/items/<int:itemid>', methods=['DELETE'])
@auth.login_required
def del_item(itemid):
    user = g.user
    if user.role.duty != 'Admin':
        abort(403)
    item = Items.query.get_or_404(itemid)
    db.session.delete(item)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/items/<int:itemid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_or_enable_item(itemid):
    user = g.user
    if user.role.duty != 'Admin':
        abort(403)
    item = Items.query.get_or_404(itemid)
    dis_or_enb = request.json.get('disbaled', True)
    item.disabled = dis_or_enb
    db.session.add(item)
    db.session.commit()
    return jsonify(item.disabled)
