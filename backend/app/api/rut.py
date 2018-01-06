# -*- coding: utf-8 -*-
# rut is readup tips, included an item list and tips for each item

from flask import request, g, jsonify, abort
from ..models import *
from ..bot import spider
from . import db, rest, auth, PER_PAGE

@rest.route('/index/ruts')
#@auth.login_required
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
    total = len(ruts) #ruts.count() #
    tag_set = Tags.get_tags()
    ruts_dict = {  # need to optimize
        'ruts': ruts, #[r.to_dict() for r in ruts],
        'total': total,
        'tags': [{'tagid': t.id,'tagname': t.tag} for t in tag_set] 
    }
    return jsonify(ruts_dict)
    
@rest.route('/rut/<int:rutid>')
def get_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut_dict = rut.to_dict()
    #attach tips and items included in rut
    r_items = rut.items.order_by(Collect.order).limit(42)
    tips = [t.to_dict() for t in r_items]  # in Collect model
    ## sort tips per order-key in collect-dict -- deprecated way
    # from operator import itemgetter
    # order_tips = sorted(tips, key=itemgetter('order'))
    rut_dict['tips'] = tips #order_tips
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

@rest.route('/rut/<int:rutid>/challengers')
def get_rut_challengers(rutid):
    #rut = Posts.query.get_or_404(rutid)  #other way: rut.challengers
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    challengers = Challenge.query.filter_by(post_id=rutid)
    challengercount = challengers.count()
    r_challengers = challengers.offset(page*per_page).limit(per_page)
    challengers_list = [u.challenger.to_dict() for u in r_challengers]
    challengers_dict = {
        'challengers': challengers_list,
         'challengercount': challengercount
    }
    return jsonify(challengers_dict)

@rest.route('/rut/<int:rutid>/stars')
def get_rut_stars(rutid):
    #rut = Posts.query.get_or_404(rutid)  #other way: rut.stars
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    stars = Star.query.filter_by(post_id=rutid)
    starcount = stars.count()
    r_stars = stars.offset(page*per_page).limit(per_page)
    stars_list = [u.starer.to_dict() for u in r_stars]
    stars_dict = {
        'stars': stars_list,
        'starcount': starcount
    }
    return jsonify(stars_dict)

@rest.route('/rut/<int:rutid>/contributors')
def get_rut_contributors(rutid):
    pass

@rest.route('/commentsonrut/<int:rutid>')
def get_rut_comments(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut_dict = {
        'id': rut.id, 
        'title': rut.title, 
        'challengecount': rut.challengers.count()
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

# for challenge page
@rest.route('/challengerut')  # challenging rut
@auth.login_required
def get_challege_rut():
    user = g.user
    challenge_rut = user.challenge_posts.first()
    try:
        rut = challenge_rut.challenge_post
        deadline = challenge_rut.deadline
        rut_dict = rut.to_dict()
        items = [t.item.to_dict() for t in rut.items]
        return jsonify({
            'rut': rut_dict,
            'items': items,
            'deadline': deadline or ''
        })
    except:
        return jsonify({
            'rut': {},
            'items': [],
            'deadline': ''
        })

@rest.route('/challengeitems')  # challenging items !!
@auth.login_required
def get_challege_items():
    user = g.user
    doing_flags = user.flag_items.filter_by(flag_label=2).limit(5) # note the order
    doing_items = [f.flag_item for f in doing_flags]
    doing_list = [{'id':item.id, 'title': item.title} for item in doing_items]
    return jsonify(doing_list)

@rest.route('/setdeadline')
@auth.login_required
def set_deadline():
    user = g.user
    challenge_rut = user.challenge_posts.first()
    deadline = request.args.get('date')
    challenge_rut.deadline = deadline
    db.session.add(challenge_rut)
    db.session.commit()
    due = challenge_rut.deadline
    return jsonify(due)
# end for challenge page

@rest.route('/ruts')
def get_all_ruts():
    #yield query
    ruts = Posts.query
    #pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    rs = ruts.offset(page*per_page).limit(per_page)
    #yield result: a dict
    ruts_dict = {
        'ruts': [r.to_dict() for r in rs],
        'total': ruts.count(),
        'currentpage': page
    }
    return jsonify(ruts_dict)

@rest.route('/checkstar/rut/<int:rutid>')
@auth.login_required
def check_star(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    staring = 'Unstar' if user.staring(rut) else 'Star'
    return jsonify(staring)

@rest.route('/checkchallenge/rut/<int:rutid>')
@auth.login_required
def check_challenge(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    challenging = 'Endchallenge' if user.challenging(rut) else 'Challenge'
    return jsonify(challenging)

@rest.route('/star/rut/<int:rutid>')
@auth.login_required
def star_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    user.star(rut)
    return jsonify('Unstar')

@rest.route('/unstar/rut/<int:rutid>')
@auth.login_required
def unstar_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    user.unstar(rut)
    return jsonify('Star')

@rest.route('/challenge/rut/<int:rutid>')
@auth.login_required
def challenge_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    user.challenge(rut)
    return jsonify('EndChallenge')

@rest.route('/unchallenge/rut/<int:rutid>')
@auth.login_required
def unchallenge_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    user.unchallenge(rut)
    return jsonify('Challenge')

@rest.route('/create/', methods=['POST'])
@rest.route('/create/<int:demandid>', methods=['POST'])
@auth.login_required
def new_rut(demandid=None):
    title = request.json.get('title','').strip()
    intro = request.json.get('intro','').strip()
    if not title or not intro:
        abort(403) # cannot be ''
    post = Posts(
        creator = g.user,
        title = title,
        intro = intro,
        tag_str = request.json.get('tag','').strip(),
        rating = request.json.get('rating'),
        credential = request.json.get('credential','...').strip(),
        editable = request.json.get('editable')
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
    return jsonify({
        'id':post.id,
        'title': post.title
    })

@rest.route('/lockrut/<int:rutid>')
@auth.login_required
def lock_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    rut.lock(user)
    return jsonify('Locked')

@rest.route('/unlockrut/<int:rutid>')
def unlock_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut.unlock()
    return jsonify('UnLocked')

@rest.route('/checkif/<int:rutid>/lockedto/<int:userid>')
def check_rut_if_locked(rutid, userid):
    rut = Posts.query.get_or_404(rutid)
    is_locked = rut.check_locked(userid)
    return jsonify(is_locked)

@rest.route('/checkif/<userid>/canedit/<int:rutid>')
#@auth.login_required
def check_rut_editable(userid, rutid):
    if not userid:
        return jsonify(False)
    user = Users.query.get_or_404(userid)
    if not user:
        return jsonify(False)
    rut = Posts.query.get_or_404(rutid)
    can_edit = rut.check_editable(user)
    who = Users.query.get(rut.editing_id) if rut.editing_id else None
    if who:
        can_dict = {'id': who.id, 'name': who.nickname or who.name}
    else:
        can_dict = {'id': None, 'name': None}
    can_dict['canedit'] = can_edit
    return jsonify(can_dict)

@rest.route('/editrut/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if not rut.check_editable(user):
        abort(403)
    # check not-null column can not be ''
    title = request.json.get('title','').strip()
    intro = request.json.get('intro','').strip()
    if not title or not intro:
        abort(403) # cannot be ''
    rut.title = title,
    rut.intro = intro,
    rut.rating = request.json.get('rating'),
    rut.editable = request.json.get('editable'),
    rut.credential = request.json.get('credential','...').strip(),
    rut.epilog = request.json.get('epilog','').strip()
    # renew the update time and add to db
    rut.renew()
    #db.session.add(rut)
    db.session.commit()
    return jsonify(rut.to_dict())

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
    _query = Tags.query
    for tg in add_tags:
        t = tg.strip()
        if not t:
            continue # if t is '' then next element
        _tag = _query.filter_by(tag=t).first()
        if _tag is None:
            new_tag = Tags(tag=t)
            new_tag.posts.append(rut)
            new_tag.cal_vote()
            #db.session.add(new_tag) # add when cal
        else:
            _tag.posts.append(rut)
            _tag.cal_vote()
            #db.session.add(_tag)
    for tg in del_tags:
        _tag = _query.filter_by(tag=tg).first()
        _tag.posts.remove(rut)
    db.session.commit()
    new_tags_list = [t.to_dict() for t in rut.tags]
    return jsonify(new_tags_list)

@rest.route('/edittips/<int:cid>', methods=['POST'])
@auth.login_required
def edit_tips(cid):
    user = g.user
    tip_collect = Collect.query.filter_by(id=cid).first_or_404()  #collect 's id
    post_id = tip_collect.post_id
    rut = Posts.query.get_or_404(post_id)
    if not rut.check_editable(user):
        abort(403)
    # get the data
    order = request.json.get('order')
    tips = request.json.get('tips','').strip()
    if not order or not tips:
        abort(403) # cannot be None
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

@rest.route('/additemtorut/<int:rutid>', methods=['POST'])
@auth.login_required
def add_item_to_rut(rutid):
    """Input item info and then check if exsiting 
    and add to rut as new or exsiting item
    """
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if not rut.check_editable(user):
        abort(403)
    # get data in request
    title = request.json.get('title','').strip()
    item_uid = request.json.get('uid','').replace('-','').replace(' ','')
    res_url = request.json.get('resUrl','').strip()
    if not title or not (item_uid or res_url):
        abort(403) # cannot be None
    uid = item_uid or spider.random_uid()
    tips = request.json.get('tips','...')
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    # check item if existing per the uid or url
    old_item = Items.query.filter_by(uid=uid).first()
    if res_url:
        online_item = Items.query.filter_by(res_url=res_url).first()
    else:
        online_item = None
    if old_item is None and online_item is None:
        new_item = Items(
            uid = uid,
            title = title,
            res_url = res_url,
            author = request.json.get('byline','').strip(),
            cover = request.json.get('cover','').strip(),
            cate = request.json.get('cate','Book'),
            publisher = request.json.get('publisher','').strip(),
            pub_date = request.json.get('pubdate','').strip(),
            language = request.json.get('language','').strip(),
            binding = request.json.get('binding','Paperback').strip(),
            page = request.json.get('page','').strip(),
            level = request.json.get('level','').strip(),
            price = request.json.get('price','').strip(),
            details = request.json.get('detail','').strip()
        )
        db.session.add(new_item)            
        rut.collecting(new_item,tips,user,spoiler)

        if request.json.get('byline','').strip():
            new_item.author_to_db()
    elif old_item is not None:
        rut.collecting(old_item,tips,user,spoiler)  
    elif online_item is not None:
        rut.collecting(online_item,tips,user,spoiler)
    db.session.commit()
    return jsonify('Done')

@rest.route('/item/<int:itemid>/torut/<int:rutid>')
@auth.login_required
def item_to_rut(itemid, rutid):
    """Add existing item to Rut"""
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if not rut.check_editable(user):
        abort(403)
    item = Items.query.get_or_404(itemid)
    rut.collecting(item,'...',user)
    db.session.commit()
    return jsonify('Done')


@rest.route('/checkitemtoadd/<int:rutid>', methods=['POST'])
@auth.login_required
def check_item_to_add(rutid):
    """get item info via Spider or query in db per uid"""
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if not rut.check_editable(user):
        abort(403)
    #regexp prepare
    re_url=r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    #re_uid=r'([-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})'
    reg_url = re.compile(re_url,0)
    tips="..." # default
    # get checker, via url_or_uid
    checker = request.json.get('url','').strip()
    # by spider 
    if reg_url.match(checker):
        pure_url = checker.split('/ref=')[0] #for amazon url
        # check if the url has been spider-ed, 
        # if not, to spider
        # if so,query item and add to post directly
        item_query = Items.query
        lst = item_query.filter(Items.res_url.in_((checker,pure_url))).all()
        if lst:
            item = lst[0]
            rut.collecting(item,tips,user)
            db.session.commit()
            return jsonify('Done')
        else:
            d = spider.parse_html(checker) # if any error??
            uid = d.get('uid','').replace('-','').replace(' ','') # random_uid in spider if needed
            ex_item = item_query.filter_by(uid=uid).first()
            if ex_item:
                rut.collecting(ex_item,tips,user)
                db.session.commit()
                return jsonify('Done')
            new_item = Items(
                uid = uid,
                title = d.get('title'),
                res_url = d.get('res_url',''),
                author = d.get('author',''),
                cover = d.get('cover',''),
                cate = d.get('cate','Book'),
                publisher = d.get('Publisher',''),
                pub_date = d.get('Publication Date') or d.get('publish_date',''),
                language = d.get('Language','English'),
                binding = d.get('binding','Paperback'),
                page = d.get('page') or d.get('Print Length', ''),
                level = d.get('Level',''),
                price = d.get('price',''),
                details = d.get('details','')
            )
            db.session.add(new_item)          
            rut.collecting(new_item,tips,user)
            if request.json.get('byline','').strip():
                new_item.author_to_db()
            db.session.commit()     
            return jsonify('Done')
    # check if exsiting by UID
    else:
        uid=checker.replace('-','').replace(' ','')
        item=Items.query.filter_by(uid=uid).first()
        if item is not None:
            rut.collecting(item,tips,user)
            db.session.commit()
            return jsonify('Done')
        else:
            return jsonify('Back') # if None by uid, back to try again

@rest.route('/del/tips/<int:cid>')
@auth.login_required
def del_tips_in_rut(cid):
    """Del tips, re-ordering items"""
    user = g.user
    #collect 's id,but not get_or_404, for 3 primary key
    tip_c = Collect.query.filter_by(id=cid).first_or_404()
    if user != tip_c.tip_creator and user.role != 'Admin':
        abort(403)
    #once delete an item. need to re-ordering,
    #order the to-be-del item to the last, then del
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
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if ((rut.creator != user and user.role != 'Admin')
        or rut.starers.count() != 0
        or rut.challengers.count() != 0):
        abort(403)
    rut.disabled = True
    db.session.add(rut)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/rut/<int:rutid>')
@auth.login_required
def recover_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user and user.role != 'Admin':
        abort(403)
    rut.disabled = False #enable
    db.session.add(rut)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/delete/rut/<int:rutid>')
@auth.login_required
def delete_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if ((rut.creator != user and user.role != 'Admin')
        or rut.starers.count() != 0
        or rut.challengers.count() != 0):
        abort(403)
    db.session.delete(rut)
    db.session.commit()
    return jsonify('Deleted')