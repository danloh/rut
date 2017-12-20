# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, redirect, url_for, request, g, jsonify
from flask_login import login_required, current_user
from flask_httpauth import HTTPBasicAuth
from .. import db
from ..models import *
from ..bot import spider
from ..utils import split_str, str_to_dict, str_to_set
from ..task.email import send_email
from .errors import bad_request, error_response

rest = Blueprint('rest', __name__)
auth = HTTPBasicAuth()

#from flask_restful import Api, Resource
#api = Api(rest)
#from . import res
#api.add_resource(res.Rut, '/rut/<int:rutid>')
#api.add_resource(res.Tag, '/tag/<int:tagid>')
#api.add_resource(res.Item, '/item/<int:itemid>')
#api.add_resource(res.Commentz, '/comments')

# for user authentication NEEDED
@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None:
        abort(400) # missing arguments
    if Users.query.filter_by(name = username).first() is not None:
        abort(400) # existing user
    user = Users(
        name = username,
        email = email,
        auth_server = "Registered",
        auth_social_id = "00001"
    )
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    if email:
        token = user.generate_confirmation_token().replace('.', '@')
        url= 'localhost:8080/confirm/%s' %token
        send_email(user.email, 'Confirm Your Account',
                    'email/confirm', name=user.name, url=url)
    # log in once register successfully
    auth_token = user.generate_auth_token()
    return jsonify({ 'username': user.name, 'userid': user.id, 'token': auth_token.decode('ascii') })

@rest.route('/editprofile', methods = ['POST'])
@auth.login_required
def edit_profile():
    user = g.user
    user.nickname = request.json.get('nickname')
    user.location = request.json.get('location')
    user.avatar = request.json.get('avatarUrl')
    user.about_me = request.json.get('about')
    user.links = request.json.get('url')
    db.session.add(user)
    db.session.commit()
    return jsonify('Have Updated Your Profile')

@rest.route('/checkname/<username>')
def checkname(username=None):
    if username and Users.query.filter_by(name=username).first() is None:
        return jsonify(1)
    return jsonify(0)
@rest.route('/checkemail/<email>')
def checkemail(email=None):
    if email and Users.query.filter_by(email=email).first() is None:
        return jsonify(1)
    return jsonify(0)

@rest.route('/confirm/<token>')
@auth.login_required
def confirm(token):
    user = g.user
    token = token.replace('@', '.')
    if user.confirmed:
        return jsonify('You have confirmed your account. Thanks!')
    if user.confirm(token):
        db.session.commit()
        return jsonify('You have confirmed your account. Thanks!')
    else:
        return jsonify('The confirmation link is invalid or has expired.')

@rest.route('/confirm')
@auth.login_required
def resend_confirmation():
    user= g.user
    token = user.generate_confirmation_token().replace('.', '@')
    url= 'localhost:8080/confirm/%s' %token
    send_email(user.email, 'Confirm Your Account',
               'email/confirm', name=user.name, url=url)
    return jsonify('A new confirmation email has been sent to you by email.')

@rest.route('/changepassword', methods=['GET', 'POST'])
@auth.login_required
def change_password():
    user = g.user
    old_psw = request.json.get('oldpsw')
    new_psw = request.json.get('newpsw')
    if user.verify_password(old_psw):
        user.password = new_psw
        db.session.add(user)
        db.session.commit()
        return jsonify('Your password has been Changed, Please login again.')
    else:
        return jsonify('Invalid password.')

@rest.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    email = request.json.get('email')
    username = request.json.get('username')
    user = Users.query.filter_by(email=email, name=username).first()
    if user:
        token = user.generate_reset_token().replace('.', '@')
        url= 'localhost:8080/reset/%s' % token
        send_email(
            user.email, 
            'Reset Your Password',
            'email/reset_password',
            name=user.name, url=url,
            next=request.args.get('next')
        )
        return jsonify('An email with instructions to reset your password has been '
            'sent to you.')
    else:
        return jsonify('Invalid username or email.')

@rest.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    token = token.replace('@', '.')
    new_psw = request.json.get('newpsw')
    if Users.reset_password(token, new_psw):
        db.session.commit()
        return jsonify('Your password has been updated, Please log in again.')
    else:
        return jsonify('Something wrong, Try Again')

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False  # how to hadle error?
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            return False # how to hadle error?
    g.user = user
    return True

@auth.error_handler
def auth_error():
    return error_response(401, 'Unauthorized Access')

@rest.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({
        'token': token.decode('ascii'),
        'userid': g.user.id
    })

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

@rest.route('/checkfollow/<int:userid>')
@auth.login_required
def check_follow(userid):
    user = g.user
    fo_user = Users.query.get_or_404(userid)
    following = 'UnFollow' if user.is_following(fo_user) else 'Follow'
    return jsonify(following)

@rest.route('/follow/user/<int:userid>')
@auth.login_required
def follow_user(userid):
    user = g.user
    fo_user = Users.query.get_or_404(userid)
    user.follow(fo_user)
    return jsonify('UnFollow')
@rest.route('/unfollow/user/<int:userid>')
@auth.login_required
def unfollow_user(userid):
    user = g.user
    fo_user = Users.query.get_or_404(userid)
    user.unfollow(fo_user)
    return jsonify('Follow')

@rest.route('/user/<int:userid>/followed')
def get_followeds(userid):
    user = Users.query.get_or_404(userid)
    followeds = [ u.followed for u in user.followed ]
    user_dicts = [u.to_dict() for u in followeds]
    return jsonify(user_dicts)

@rest.route('/ruts')
#@auth.login_required
def get_ruts():
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
    return jsonify({  # need to optimize
        'ruts': ruts, #[r.to_dict() for r in ruts],
        'total': total,
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

@rest.route('/create/', methods=['POST'])
@rest.route('/create/<int:demandid>', methods=['POST'])
@auth.login_required
def new_rut(demandid=None):
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
    # link to demand if come from demand
    if demandid:
        demand = Demands.query.get(demandid)
        if demand:
            respon = Respon(
                post=post,
                demand=demand
            )
            db.session.add(respon)
    db.session.commit()
    return jsonify({'id':post.id})

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
    rut.renew() # renew the update time and add to db
    #db.session.add(rut)
    db.session.commit()
    return jsonify(rut.to_dict())

@rest.route('/edittags/<int:rutid>', methods=['POST'])
@auth.login_required
def edit_tags(rutid):
    rut = Posts.query.get_or_404(rutid)
    old = request.json.get('old')
    new = request.json.get('new')
    old_set = set(old)
    new_set = set(new)
    add_tags = new_set - old_set
    del_tags = old_set - new_set
    _query = Tags.query
    for t in add_tags:
        _tag = _query.filter_by(tag=t).first()
        if _tag is None:
            new_tag = Tags(tag=t)
            new_tag.posts.append(rut)
            db.session.add(new_tag)
        else:
            _tag.posts.append(rut)
            db.session.add(_tag)
    for tg in del_tags:
        _tag = _query.filter_by(tag=tg).first()
        _tag.posts.remove(rut)
    db.session.commit()
    new_tags = [t.to_dict() for t in rut.tags]
    return jsonify(new_tags)

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
    """Input item info and then check if exsiting 
    and add to rut as new or exsitingf item
    """
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

@rest.route('/item/<int:itemid>/torut/<int:rutid>')
@auth.login_required
def item_to_rut(itemid, rutid):
    """Add existing item to Rut"""
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user:
        return jsonify('Error')
    item = Items.query.get_or_404(itemid)
    rut.collecting(item,'No Tips',user)
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

@rest.route('/item/<int:itemid>')
def get_item(itemid):
    item = Items.query.get_or_404(itemid)
    item_dict = item.to_dict()
    # attach reviews
    reviews = item.reviews
    hotreviews = reviews.order_by(Reviews.vote.desc())
    newreviews = reviews.order_by(Reviews.timestamp.desc()).limit(15)
    hot_reviews = [r.to_dict() for r in hotreviews]
    new_reviews = [r.to_dict() for r in newreviews]
    item_dict['hotreviews'] = hot_reviews
    item_dict['newreviews'] = new_reviews
    # attach included ruts
    ruts = [c.post for c in item.posts.order_by(Collect.timestamp.desc())]
    included_ruts = [{'id':r.id, 'title': r.title} for r in ruts]
    item_dict['inruts'] = included_ruts
    return jsonify(item_dict)

@rest.route('/edititem/<int:itemid>', methods=['POST'])
@auth.login_required
def edit_item(itemid):
    query = Items.query
    item = query.get_or_404(itemid)
    uid = request.json.get('uid').replace('-','').replace(' ','')
    if query.filter_by(uid=uid) and item.uid != uid:
        return jsonify('Error')
    #update item 
    item.uid = uid
    item.cate = request.json.get('cate')
    item.title = request.json.get('title')
    item.author = request.json.get('byline')
    item.cover = request.json.get('cover')
    item.res_url = request.json.get('resUrl')
    item.publisher = request.json.get('publisher','')
    item.pub_date = request.json.get('publishDate','')
    item.language = request.json.get('language','')
    item.binding = request.json.get('binding','')
    item.page = request.json.get('page','')
    item.level = request.json.get('level','')
    item.price = request.json.get('price','')
    item.details = request.json.get('details','')
    #edit author  byline
    old_str = item.author
    old_d = str_to_dict(old_str)
    old_set = set(k for k in old_d if k is not "None")
    new_str = request.json.get('byline')
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
    return jsonify('Done')

@rest.route('/clips')
@auth.login_required
def get_clips():
    user = g.user
    ref = request.args.get('ref','')
    q = Clips.query
    if ref == "All":
        query = q.filter(Clips.creator != user)
    elif ref == "Hot":
        query = q.order_by(Clips.vote.desc())
    else:
        query = q.filter_by(creator_id=user.id)
    order_query = query.order_by(Clips.timestamp.desc()) # or reverse list
    return jsonify({
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    })

@rest.route('/iuclips')
def get_iuclips():
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    q = Clips.query
    if userid and itemid:
        query =q.filter_by(creator_id=userid,item_id=itemid)
    elif userid:
        query = q.filter_by(creator_id=userid)
    elif itemid:
        query = q.filter_by(item_id=itemid)
    order_query = query.order_by(Clips.timestamp.desc())
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

@rest.route('/upvoteclip/<int:clipid>')
@auth.login_required
def upvote_clip(clipid):
    user = g.user
    clip = Clips.query.get_or_404(clipid)
    voted = Cvote.query.filter_by(user_id=user.id,clip_id=clipid).first()
    if voted is None:
        clip.vote = clip.vote + 1 
        db.session.add(clip)
        cvote = Cvote(
            voter=user,
            vote_clip=clip
        )
        db.session.add(cvote)
        db.session.commit()
    return jsonify(clip.vote)

@rest.route('/newreview/<int:itemid>', methods=['POST'])
@auth.login_required
def new_review(itemid):
    user = g.user
    item = Items.query.get_or_404(itemid)
    review = Reviews(
        heading = request.json.get('title'),
        body = request.json.get('review'),
        item = item,
        creator = user
    )
    db.session.add(review)
    item.cal_vote()
    db.session.commit()
    review_dict = review.to_dict()
    return jsonify(review_dict)

@rest.route('/editreview/<int:reviewid>', methods=['POST'])
@auth.login_required
def edit_review(reviewid):
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    if user != review.creator:
        return jsonify('No Permission')
    review.heading = request.json.get('title'),
    review.body = request.json.get('review'),
    db.session.add(review)
    db.session.commit()
    review_dict = review.to_dict()
    return jsonify(review_dict)

@rest.route('/review/<int:reviewid>')
def get_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    review_dict = review.to_dict()
    return jsonify(review_dict)

@rest.route('/upvotereview/<int:reviewid>')
@auth.login_required
def upvote_review(reviewid):
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    voted = Rvote.query.filter_by(user_id=user.id,review_id=reviewid).first()
    if user != review.creator and voted is None:
        review.vote = review.vote + 1 
        db.session.add(review)
        rvote = Rvote(
            voter=user,
            vote_review=review
        )
        db.session.add(rvote)
        db.session.commit()
    return jsonify(review.vote)
    
@rest.route('/demands')
def get_demands():
    query = Demands.query
    userid = request.args.get('userid','')
    ref = request.args.get('type','popular')
    if userid:
        demands = query.filter_by(requestor_id=int(userid))
    elif ref == "new":
        demands = query.order_by(Demands.timestamp.desc())
    elif ref == "popular":  # popular
        demands = query.order_by(Demands.vote.desc())
    demands_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': demands.count()
    }
    return jsonify(demands_dict)

@rest.route('/demand/<int:demandid>')
def get_demand(demandid):
    demand = Demands.query.get_or_404(demandid)
    demand_dict = demand.to_dict()
    #attach answers to demand
    respons = [r.post for r in demand.posts]
    answers = [{'id':p.id,'title':p.title} for p in respons]
    demand_dict['answers'] = answers
    #attach comments
    comments = [c.to_dict() for c in demand.comments]
    comments.reverse()
    demand_dict['comments'] = comments
    return jsonify(demand_dict)

@rest.route('/upvotedemand/<int:demandid>')
@auth.login_required
def upvote_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid) # demand's id
    voted = Dvote.query.filter_by(user_id=user.id,demand_id=demandid).first()
    if voted is None:
        demand.vote = demand.vote + 1 
        db.session.add(demand)
        dvote = Dvote(
            voter=user,
            vote_demand=demand
        )
        db.session.add(dvote)
        db.session.commit()
        #return jsonify(demand.vote)
    return jsonify(demand.vote)

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


@rest.route('/tag/<int:tagid>')
def get_tag(tagid):
    tag = Tags.query.get_or_404(tagid)
    tag_dict = tag.to_dict()
    #attach ruts included in tag 
    tagruts = [p.to_dict() for p in tag.posts]
    tagruts.reverse()  # as order_by, which is faster?
    tag_dict['ruts'] = tagruts
    tag_dict['total'] = len(tagruts)
    # related tags
    parent_tags = [t.parent_tag for t in tag.parent_tags.\
                order_by(db.func.rand()).limit(5)]
    tags = parent_tags
    for tg in parent_tags:
        child_tags = [t.child_tag for t in Clan.query.\
                filter_by(parent_tag_id=tg.id).\
                order_by(db.func.rand()).limit(5)]
        tags += child_tags   
    tag_dict['tags'] = [{'tagid': t.id,'tagname': t.tag} for t in tags] 
    return jsonify(tag_dict)

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

@rest.route('/comment/rut/<int:rutid>', methods=['POST'])
@rest.route('/comment/demand/<int:demandid>', methods=['POST'])
@rest.route('/comment/comment/<int:commentid>', methods=['POST'])
@rest.route('/comment/item/<int:itemid>', methods=['POST'])
@rest.route('/comment/review/<int:reviewid>', methods=['POST'])
@auth.login_required
def new_comment(demandid=None,rutid=None,commentid=None,itemid=None,reviewid=None):
    user = g.user
    comment = Comments(
        body = request.json.get('comment'),
        demand = Demands.query.get(demandid) if demandid else None,
        post = Posts.query.get(rutid) if rutid else None,
        item = Items.query.get(itemid) if itemid else None,
        parent_comment = Comments.query.get(commentid) if commentid else None,
        review = Reviews.query.get(reviewid) if reviewid else None,
        creator = user
    )
    db.session.add(comment)
    db.session.commit()
    comment_dict = comment.to_dict()
    return jsonify(comment_dict)
