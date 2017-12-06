# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, redirect, url_for, request, g, jsonify
from flask_login import login_required, current_user
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from .. import db
from ..models import *
from ..bot import spider

rest = Blueprint('rest', __name__)
api = Api(rest)
auth = HTTPBasicAuth()

from . import res
#api.add_resource(res.Rut, '/rut/<int:rutid>')
api.add_resource(res.Tag, '/tag/<int:tagid>')
api.add_resource(res.Item, '/item/<int:itemid>')
#api.add_resource(res.Commentz, '/comments')

# for user authentication NEEDED
@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if Users.query.filter_by(name = username).first() is not None:
        abort(400) # existing user
    user = Users(
        name = username,
        auth_server = "Registered",
        auth_social_id = "00001"
    )
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.name, 'userid': user.id })

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True

@rest.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({
        'token': token.decode('ascii'),
        'user': g.user.to_dict()
    })

@rest.route('/user')
@auth.login_required
def verify_user():       ##????
    guser = g.user
    ref = request.args.get('ref','actived')
    if ref == 'verify':
        user_dict = {
            'id': guser.id,
            'username': guser.nickname or guser.name
        }
        return jsonify(user_dict)
    else:
        return jsonify(guser.to_dict())

@rest.route('/currentuser') 
@auth.login_required  
def get_current_user(): # for authed-user to re-get info
    user = g.user
    user_dict = user.to_dict()
    return jsonify(user_dict)

@rest.route('/user/<int:id>')
def get_user(id):        # get info per userid
    user = Users.query.get_or_404(id)
    user_dict = user.to_dict()
    return jsonify(user_dict)

@rest.route('/ruts')
@auth.login_required
def get_ruts():            ##!! to be optimized
    user = g.user
    ref = request.args.get('ref','random')
    #get related tags set and fav tags
    tag_set, tag_fv = user.get_tag_set()
    # get followed posts queries
    post_fo = [f.followed.posts for f in user.followed]
    #list the queries, followed _posts as init 
    q = post_fo
    for tag_obj in tag_set:
        q.append(tag_obj.posts)
    q_rand = Posts.query.order_by(db.func.rand()).limit(0) # !! need to optimize
    query = q_rand.union(*q)
    ruts = query.order_by(Posts.timestamp.desc())  # other way,list reverse
    return jsonify({  # need to optimize
        'ruts': [r.to_dict() for r in ruts],
        'total': ruts.count(),
        'tags': [{'tagid': t.id,'tagname': t.tag} for t in tag_set] 
    })

@rest.route('/rut/<int:rutid>')
def get_rut(rutid):
    rut = Posts.query.get_or_404(rutid)
    rut_dict = rut.to_dict()
    #attach tips and items included in rut 
    tips = [t.to_dict() for t in rut.items]  # in Collect model
    # sort tips per order-key in collect-dict
    from operator import itemgetter
    order_tips = sorted(tips, key=itemgetter('order'))
    rut_dict['tips'] = order_tips
    return jsonify(rut_dict)

@rest.route('/challengerut')  # challenging rut !!
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
            'ruts': [rut_dict],
            'total': 1,
            'tags': [],
            'items': items,
            'deadline': deadline
        })
    except:
        return jsonify({
            'ruts': [],
            'total': 0,
            'tags': []
        })

@rest.route('/challengeitems')  # challenging items !!
@auth.login_required
def get_challege_items():
    user = g.user
    doing_flags = user.flag_items.filter_by(flag_label=2).limit(5) # note the order
    doing_items = [f.flag_item for f in doing_flags]
    doing_dict_list = [{'id':item.id, 'title': item.title} for item in doing_items]
    return jsonify(doing_dict_list)

@rest.route('/<int:userid>/created/ruts')
def get_created_ruts(userid):
    user = Users.query.get_or_404(int(userid))
    ruts = user.posts.order_by(Posts.timestamp.desc())
    return jsonify({
        'ruts': [r.to_dict() for r in ruts],
        'total': ruts.count(),
        'tags': []
    })

@rest.route('/<int:userid>/star/ruts')
def get_star_ruts(userid):
    user = Users.query.get_or_404(userid)
    ruts = [s.star_post for s in user.star_posts]
    ruts.reverse()
    return jsonify({
        'ruts': [r.to_dict() for r in ruts],
        'total': len(ruts),
        'tags': []
    })

@rest.route('/<int:userid>/challenge/ruts')
def get_challege_ruts(userid):
    user = Users.query.get_or_404(userid)
    ruts = [c.challenge_post for c in user.challenge_posts]
    ruts.reverse()  # other way,list reverse
    return jsonify({
        'ruts': [r.to_dict() for r in ruts],
        'total': len(ruts),
        'tags': []
    })
   
    # elif ref == 'contribute':
    #     q = [c.contribute_post for c in user.contribute_posts]

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

@rest.route('/create', methods=['POST'])
@auth.login_required
def new_rut():
    post = Posts(
        creator = g.user,
        title = request.json.get('title'),
        intro = request.json.get('intro'),
        tag_str = request.json.get('tag'),
        rating = request.json.get('rating'),
        credential = request.json.get('credential'),
        editable = request.json.get('editable')
    )
    db.session.add(post)
    post.tag_to_db()
    db.session.commit()
    return jsonify(post.to_dict())

@rest.route('/editrut/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user:
        return jsonify('Error')  #how to tacle error?
    rut.title = request.json.get('title'),
    rut.intro = request.json.get('intro'),
    rut.rating = request.json.get('rating'),
    rut.credential = request.json.get('credential'),
    rut.epilog = request.json.get('epilog')
    db.session.add(rut)
    db.session.commit()
    return jsonify(rut.to_dict())

@rest.route('/edittips/<int:cid>', methods=['POST'])
@auth.login_required
def edit_tips(cid):
    user = g.user
    tip_collect = Collect.query.filter_by(id=cid).first_or_404()  #collect 's id
    post_id = tip_collect.post_id
    rut = Posts.query.get_or_404(post_id)
    if rut.creator != user:
        return jsonify('Error')  #how to tacle error?
    # get the data
    order = request.json.get('order')
    tips = request.json.get('tips')
    if not order or not tips:  # cannot be null
        return jsonify('Error')
    item = Items.query.get_or_404(tip_collect.item_id)
    # get the data
    order = request.json.get('order')
    tips = request.json.get('tips')
    # re-ordering
    rut.ordering(item, order)
    rut.renew()
    tip_collect.tips = tips
    db.session.add(tip_collect)
    db.session.commit()
    return jsonify('Done')

@rest.route('/additemtorut/<int:rutid>', methods=['POST'])
@auth.login_required
def add_item_to_rut(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user:
        return jsonify('Error')  #how to tacle error?
    uid = request.json.get('uid').replace('-','').replace(' ','')
    old_item = Items.query.filter_by(uid=uid).first()
    res_url = request.json.get('resUrl','').strip()
    tips = request.json.get('tips','No Tips Yet')
    if res_url:
        online_item = Items.query.filter_by(res_url=res_url).first()
    else:
        online_item = None
    if old_item is None and online_item is None:
        new_item = Items(
            uid = request.json.get('uid'),
            title = request.json.get('title'),
            res_url = request.json.get('resUrl',''),
            author = request.json.get('byline',''),
            cover = request.json.get('cover',''),
            cate = request.json.get('cate','Book'),
            publisher = request.json.get('publisher',''),
            pub_date = request.json.get('pubdate',''),
            language = request.json.get('language',''),
            binding = request.json.get('binding','Paperback'),
            page = request.json.get('page',''),
            level = request.json.get('level',''),
            price = request.json.get('price',''),
            details = request.json.get('detail','')
        )
        db.session.add(new_item)            
        rut.collecting(new_item,tips,user)

        if request.json.get('byline','').strip():
            new_item.author_to_db()
    elif old_item is not None:
        rut.collecting(old_item,tips,user)  
    elif online_item is not None:
        rut.collecting(online_item,tips,user)
    db.session.commit()

    return jsonify('Done')

@rest.route('/checkitemtoadd/<int:rutid>', methods=['POST'])
@auth.login_required
def check_item_for_add(rutid):
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user:
        return jsonify('Error')  #how to tacle error?
    #regexp prepare
    re_url=r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    #re_uid=r'([-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})'
    reg_url = re.compile(re_url,0)
    tips="No Tips" # default

    checker = request.json.get('url') #url_or_uid
    if reg_url.match(checker):
        pure_url = checker.split('/ref=')[0] #for amazon url
        # check if the url has been spidered, 
        # if not, to spider
        # if so,query item and add to post directly
        lst = Items.query.filter(Items.res_url.in_((checker,pure_url))).all()
        if lst:
            item = lst[0]
            rut.collecting(item,tips,user)
            db.session.commit()
            return jsonify('Done')
        else:
            d = spider.parse_html(checker)
            new_item = Items(
                uid = d.get('uid'),
                title = d.get('title'),
                res_url = d.get('res_url',''),
                author = d.get('author',''),
                cover = d.get('cover',''),
                cate = d.get('cate','Book'),
                publisher = d.get('Publisher',''),
                pub_date = d.get('Publication Date') or d.get('publish_date',''),
                language = d.get('Language','English'),
                binding = d.get('binding','Paperback'),
                page = d.get('page') or d.get('Print Length', '') ,
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
    else:
        uid=checker.replace('-','').replace(' ','')
        item=Items.query.filter_by(uid=uid).first()
        if item is not None:
            rut.collecting(item,tips,user)
            db.session.commit()
            return jsonify('Done')
        else:
            return jsonify('Back') #redirect(url_for('.check_item', id=id))

@rest.route('/<int:userid>/doing/items')
def get_doing_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=2)
    items = [d.flag_item for d in flags ]
    items.reverse()
    return jsonify({
        'items': [i.to_dict() for i in items],
        'total': len(items)
    })

@rest.route('/<int:userid>/todo/items')
def get_todo_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=1)
    items = [d.flag_item for d in flags ]
    items.reverse()
    return jsonify({
        'items': [i.to_dict() for i in items],
        'total': len(items)
    })

@rest.route('/<int:userid>/done/items')
def get_done_items(userid):
    user = Users.query.get_or_404(userid)
    flags = user.flag_items.filter_by(flag_label=3)
    items = [d.flag_item for d in flags ]
    items.reverse()
    return jsonify({
        'items': [i.to_dict() for i in items],
        'total': len(items)
    })

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

@rest.route('/clips')
@auth.login_required
def get_clips():
    user = g.user
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    ref = request.args.get('ref','')
    q = Clips.query
    if userid and itemid:
        query =q.filter_by(creator_id=userid,item_id=itemid)
    elif userid:
        query = q.filter_by(creator_id=userid)
    elif itemid:
        query = q.filter_by(item_id=itemid)
    elif ref == "All":
        query = q.filter(Clips.creator != user)
    else:
        query = q.filter_by(creator_id=user.id)
    order_query = query.order_by(Clips.timestamp.desc()) # or reverse list
    return jsonify({
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    })

@rest.route('/newclip', methods=['POST'])
@auth.login_required
def new_clip():
    itemid = request.json.get('itemid')
    clip = Clips(
        creator = g.user,
        body = request.json.get('clip'),
        item = Items.query.get(itemid) 
    )
    db.session.add(clip)
    db.session.commit()
    return jsonify(clip.to_dict())

@rest.route('/demands')
def get_demands():
    query = q = Demands.query
    userid = request.args.get('userid','')
    ref = request.args.get('type','popular')
    if userid:
        query = q.filter_by(requestor_id=int(userid))
    if ref == "new":
        demands = query.order_by(Demands.timestamp.desc())
    else:
        demands = query.order_by(Demands.vote.desc())
    demand_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': demands.count()
    }
    return jsonify(demand_dict)

@rest.route('/newdemand', methods=['POST'])
@auth.login_required
def new_demand():
    sp = request.json.get('demand').split('#') + ['42']
    body = sp[0]
    tag_str = sp[1]
    demand = Demands(
        requestor = g.user,
        body = body,
        dtag_str = tag_str
    )
    db.session.add(demand)
    demand.dtag_to_db()
    db.session.commit()
    return jsonify(demand.to_dict())

@rest.route('/edittag/<int:tagid>', methods=['POST'])
@auth.login_required
def edit_tag(tagid):
    query = Tags.query
    tag = query.get_or_404(tagid)
    # get data
    name = request.json.get('name').strip()
    parent = request.json.get('parent').strip()
    description = request.json.get('description').strip()
    if not name:
        return jsonify('Error')
    if tag.tag != name and query.filter_by(tag=name).first():
        return jsonify('Duplicated Tag Name')
    tag.tag = name
    tag.descript = description
    db.session.add(tag)
    # update parent tag
    parent_tag = query.filter_by(tag=parent).first()
    if not parent_tag:
        parent_tag = Tags(tag=parent)
        db.session.add(parent_tag)
    tag.parent(parent_tag)
    db.session.commit()
    return jsonify('Done')

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
    user.fav(tag)
    return jsonify('UnFollow')

@rest.route('/unfav/tag/<int:tagid>')
@auth.login_required
def unfav_tag(tagid):
    user = g.user
    tag = Tags.query.get_or_404(tagid)
    user.unfav(tag)
    return jsonify('Follow')