# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, current_app, request, g, jsonify, abort
from flask_sqlalchemy import get_debug_queries
from flask_httpauth import HTTPBasicAuth
from .. import db
from ..models import *
from ..bot import spider
from ..utils import split_str, str_to_dict, str_to_set
from ..task.email import send_email
from .errors import error_response

rest = Blueprint('rest', __name__)
auth = HTTPBasicAuth()

PER_PAGE = 20 # for pagination except items in rut--42

@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email','').strip()
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
    return jsonify({
        'username': user.name, 
        'userid': user.id, 
        'token': auth_token.decode('ascii') 
    })

@rest.route('/editprofile', methods = ['POST'])
@auth.login_required
def edit_profile():
    user = g.user
    user.nickname = request.json.get('nickname','').strip()
    user.location = request.json.get('location','').strip()
    user.avatar = request.json.get('avatarUrl','').strip()
    user.about_me = request.json.get('about','').strip()
    user.links = request.json.get('url','').strip()
    db.session.add(user)
    db.session.commit()
    return jsonify('Your Profile Updated')

# check if name / email duplicated when regsiter
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
        return jsonify('Your password Changed, Please login again.')
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

@rest.route('/reset/<string:token>', methods=['GET', 'POST'])
def password_reset(token):
    token = token.replace('@', '.')
    new_psw = request.json.get('newpsw')
    if Users.reset_password(token, new_psw):
        db.session.commit()
        return jsonify('Your password updated, Please login again.')
    else:
        return jsonify('Something wrong, Try Again')

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            abort(401)
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            abort(401)
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
    if user.followed.count() >= 42:
        abort(418)
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
    ruts_dict = {  # need to optimize
        'ruts': ruts, #[r.to_dict() for r in ruts],
        'total': total,
        'tags': [{'tagid': t.id,'tagname': t.tag} for t in tag_set] 
    }
    return jsonify(ruts_dict)

@rest.route('/all/ruts')
def get_all_ruts():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_ruts = Posts.query
    ruts = all_ruts.offset(page*per_page).limit(per_page)
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': all_ruts.count(),
        'currentpage': page
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

@rest.route('/<int:userid>/created/ruts')
def get_created_ruts(userid):
    user = Users.query.get_or_404(int(userid))
    created_ruts = user.posts.order_by(Posts.timestamp.desc())
    #created_ruts = Posts.query.filter_by(creator_id=userid).order_by(Posts.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = created_ruts.offset(page * per_page).limit(per_page)
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': created_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)

@rest.route('/<int:userid>/star/ruts')
def get_star_ruts(userid):
    user = Users.query.get_or_404(userid)
    star_ruts = user.star_posts.order_by(Star.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = [s.star_post for s in star_ruts.offset(page * per_page).limit(per_page)]
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': star_ruts.count(),
        'tags': []
    }
    return jsonify(ruts_dict)

@rest.route('/<int:userid>/challenge/ruts')
def get_challege_ruts(userid):
    user = Users.query.get_or_404(userid)
    challenge_ruts = user.challenge_posts.order_by(Challenge.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    ruts = [c.challenge_post \
        for c in challenge_ruts.offset(page * per_page).limit(per_page)]
    ruts_dict = {
        'ruts': [r.to_dict() for r in ruts],
        'total': challenge_ruts.count(),
        'tags': []
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
    uid = request.json.get('uid','').replace('-','').replace(' ','')
    if not title or not uid:
        abort(403) # cannot be None
    res_url = request.json.get('resUrl','').strip()
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
        lst = Items.query.filter(Items.res_url.in_((checker,pure_url))).all()
        if lst:
            item = lst[0]
            rut.collecting(item,tips,user)
            db.session.commit()
            return jsonify('Done')
        else:
            d = spider.parse_html(checker) # if any error??
            new_item = Items(
                uid = d.get('uid','').replace('-','').replace(' ',''),
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

@rest.route('/all/clips')
def get_all_clips():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_clips = Clips.query
    clips = all_clips.offset(page*per_page).limit(per_page)
    clips_dict = {
        'clips': [c.to_dict() for c in clips],
        'total': all_clips.count(),
        'currentpage': page
    }
    return jsonify(clips_dict)

@rest.route('/clips')
@auth.login_required
def get_clips():
    user = g.user
    ref = request.args.get('ref','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    q = Clips.query
    if ref == "All":
        query = q.filter(Clips.creator != user)
    elif ref == "Hot":
        query = q.order_by(Clips.vote.desc())
    else:
        query = q.filter_by(creator_id=user.id)
    order_query = query.order_by(Clips.timestamp.desc())\
                  .offset(page * per_page).limit(per_page)
    clips_dict = {
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    }
    return jsonify(clips_dict)

@rest.route('/iuclips') # per item or user or any
def get_iuclips():
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    q = Clips.query
    if userid and itemid:
        query =q.filter_by(creator_id=userid,item_id=itemid)
    elif userid:
        query = q.filter_by(creator_id=userid)
    elif itemid:
        query = q.filter_by(item_id=itemid)
    else:
        query = q
    order_query = query.order_by(Clips.timestamp.desc())\
                       .offset(page * per_page).limit(per_page)
    clips_dict = {
        'clips': [c.to_dict() for c in order_query],
        'total': query.count()
    }
    return jsonify(clips_dict)

@rest.route('/newclip', methods=['POST'])
@auth.login_required
def new_clip():
    body = request.json.get('clip','').strip()
    if not body:
        abort(403)
    itemid = request.json.get('itemid')
    clip = Clips(
        creator = g.user,
        body = body,
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

@rest.route('/delete/clip/<int:clipid>')
@auth.login_required
def del_clip(clipid):
    user = g.user
    clip = Clips.query.get_or_404(clipid)
    if clip.creator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(clip)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/clip/<int:clipid>')
@auth.login_required
def disable_clip(clipid):
    user = g.user
    clip = Clips.query.get_or_404(clipid)
    if clip.creator != user and user.role != 'Admin':
        abort(403)
    clip.disabled = True
    db.session.add(clip)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/clip/<int:clipid>')
@auth.login_required
def recover_clip(clipid):
    user = g.user
    clip = Clips.query.get_or_404(clipid)
    if clip.creator != user and user.role != 'Admin':
        abort(403)
    clip.disabled = False #enable
    db.session.add(clip)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/newreview/<int:itemid>', methods=['POST'])
@auth.login_required
def new_review(itemid):
    body = request.json.get('review','').strip()
    heading = request.json.get('title','').strip()
    if not body or not heading:
        abort(403)
    user = g.user
    item = Items.query.get_or_404(itemid)
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    review = Reviews(
        heading = heading,
        body = body,
        spoiler = spoiler,
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
    body = request.json.get('review','').strip()
    heading = request.json.get('title','').strip()
    if not body or not heading:
        abort(403)
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    if user != review.creator and user.role != 'Admin':
        abort(403) #No Permission
    review.heading = heading
    review.body = body
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    review.spoiler = spoiler
    db.session.add(review)
    db.session.commit()
    review_dict = review.to_dict()
    return jsonify(review_dict)

@rest.route('/delete/review/<int:reviewid>')
@auth.login_required
def del_review(reviewid):
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    if review.creator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(review)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/review/<int:reviewid>')
@auth.login_required
def disable_review(reviewid):
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    if review.creator != user and user.role != 'Admin':
        abort(403)
    review.disabled = True
    db.session.add(review)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/review/<int:reviewid>')
@auth.login_required
def recover_review(reviewid):
    user = g.user
    review = Reviews.query.get_or_404(reviewid)
    if review.creator != user and user.role != 'Admin':
        abort(403)
    review.disabled = False #enable
    db.session.add(review)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/review/<int:reviewid>')
def get_review(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    review_dict = review.to_dict()
    #attach comments
    rev_comments = review.comments.order_by(Comments.timestamp.desc())
    review_dict['commentcount'] = rev_comments.count()
    comments = [c.to_dict() for c in rev_comments.limit(50)]
    review_dict['comments'] = comments
    return jsonify(review_dict)

@rest.route('/review/<int:reviewid>/comments')
def get_review_comments(reviewid):
    review = Reviews.query.get_or_404(reviewid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 50, type=int)
    rev_comments = review.comments.order_by(Comments.timestamp.desc())\
                                .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in rev_comments]
    return jsonify(comments)

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

@rest.route('/user/<int:userid>/reviews')
def get_user_reviews(userid):
    #user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = Reviews.query.filter_by(creator_id=userid)
    rs = reviews.order_by(Reviews.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    reviewcount = reviews.count()
    review_list = [r.to_dict() for r in rs]
    review_dict = {'reviewcount': reviewcount, 'reviews': review_list}
    return jsonify(review_dict)

@rest.route('/reviews') # per user, item or any
def get_reviews():
    userid = request.args.get('userid','')
    itemid = request.args.get('itemid','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Reviews.query
    if userid and itemid:
        reviews = query.filter_by(creator_id=userid,item_id=itemid)
    if userid:
        reviews = query.filter_by(creator_id=userid)
    elif itemid:
        reviews = query.filter_by(item_id=itemid)
    else:
        reviews = query
    rs = reviews.order_by(Reviews.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    review_list = [r.to_dict() for r in rs]
    reviews_dict = {'reviewcount': reviews.count(), 'reviews': review_list}
    return jsonify(reviews_dict)

@rest.route('/all/reviews')
def get_all_reviews():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_reviews = Reviews.query
    reviews = all_reviews.offset(page*per_page).limit(per_page)
    reviews_dict = {
        'reviews': [rev.to_dict() for rev in reviews],
        'total': all_reviews.count(),
        'currentpage': page
    }
    return jsonify(reviews_dict)

@rest.route('/user/<int:userid>/demands')
def get_user_demands(userid):
    #user = Users.query.get_or_404(userid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = Demands.query.filter_by(requestor_id=userid)
    ds = demands.order_by(Demands.timestamp.desc())\
                .offset(per_page * page).limit(per_page)
    demandcount = demands.count()
    d_list = [d.to_dict() for d in ds]
    demand_dict = {'demandcount': demandcount, 'demands': d_list}
    return jsonify(demand_dict)

@rest.route('/all/demands')   
@rest.route('/demands')
def get_demands():
    query = Demands.query
    userid = request.args.get('userid','')
    ref = request.args.get('type','')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    if userid:
        demands = query.filter_by(requestor_id=int(userid))\
                       .order_by(Demands.timestamp.desc())
    elif ref == "new":
        demands = query.order_by(Demands.timestamp.desc())
    elif ref == "popular":  # popular
        demands = query.order_by(Demands.vote.desc())
    else:
        demands = query
    ds = demands.offset(per_page * page).limit(per_page)
    demands_dict = {
        'demands': [d.to_dict() for d in ds],
        'total': demands.count()
    }
    return jsonify(demands_dict)

@rest.route('/onlydemand/<int:demandid>')
def get_demand_only(demandid):
    demand = Demands.query.get_or_404(demandid)
    demand_dict = demand.to_dict()
    return jsonify(demand_dict)

@rest.route('/demand/<int:demandid>')
def get_demand(demandid):
    demand = Demands.query.get_or_404(demandid)
    demand_dict = demand.to_dict()
    #attach answers to demand
    resps = demand.posts.order_by(Respon.timestamp.desc()).limit(PER_PAGE)
    respons = [r.post for r in resps]
    answers = [{'id':p.id,'title':p.title,'intro':p.intro} for p in respons]
    demand_dict['answers'] = answers
    #attach comments
    d_comments = demand.comments.order_by(Comments.timestamp.desc()).limit(50)
    comments = [c.to_dict() for c in d_comments]
    ##comments.reverse()
    demand_dict['comments'] = comments
    return jsonify(demand_dict)

@rest.route('/demand/<int:demandid>/comments')
def get_demand_comments(demandid):
    demand = Demands.query.get_or_404(demandid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', 50, type=int)
    d_comments = demand.comments.order_by(Comments.timestamp.desc())\
                                .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in d_comments]
    return jsonify(comments)

@rest.route('/demand/<int:demandid>/answers')
def get_demand_answers(demandid):
    demand = Demands.query.get_or_404(demandid)
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    d_resps = demand.posts.order_by(Respon.timestamp.desc())\
                          .offset(page*per_page).limit(per_page)
    d_respons = [r.post for r in d_resps]
    answers = [{'id':p.id,'title':p.title,'intro':p.intro} for p in d_respons]
    return jsonify(answers)

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
    text = request.json.get('demand','').strip()
    if not text:
        abort(403)
    sp = text.split('#') + ['42']
    body = sp[0]
    tag_str = sp[1].strip() or '42'
    demand = Demands(
        requestor = g.user,
        body = body,
        dtag_str = tag_str
    )
    db.session.add(demand)
    demand.dtag_to_db()
    db.session.commit()
    return jsonify(demand.to_dict())

@rest.route('/rut/<int:rutid>/answerdemand/<int:demandid>')
@auth.login_required
def rut_as_answer(rutid, demandid):
    """link  Rut to  a demand as Answer"""
    user = g.user
    rut = Posts.query.get_or_404(rutid)
    if rut.creator != user and user.role != 'Admin':
        abort(403) #no permission
    demand = Demands.query.get_or_404(demandid)
    respon = Respon(
        post = rut,
        demand = demand
    )
    db.session.add(respon)
    db.session.commit()
    answer = {'id': rut.id, 'title': rut.title}
    return jsonify(answer)

@rest.route('/delete/demand/<int:demandid>')
@auth.login_required
def del_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    db.session.delete(demand)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/demand/<int:demandid>')
@auth.login_required
def disable_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    demand.disabled = True
    db.session.add(demand)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/demand/<int:demandid>')
@auth.login_required
def recover_demand(demandid):
    user = g.user
    demand = Demands.query.get_or_404(demandid)
    if demand.requestor != user and user.role != 'Admin':
        abort(403)
    demand.disabled = False #enable
    db.session.add(demand)
    db.session.commit()
    return jsonify('Enabled')

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
    #tagruts.reverse()
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
    body = request.json.get('comment','').strip()
    if not body:
        abort(403)
    user = g.user
    comment = Comments(
        body = body,
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

@rest.route('/delete/comment/<int:commentid>')
@auth.login_required
def del_comment(commentid):
    user = g.user
    comment = Comments.query.get_or_404(commentid)
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/comment/<int:commentid>')
@auth.login_required
def disable_comment(commentid):
    user = g.user
    comment = Comments.query.get_or_404(commentid)
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/comment/<int:commentid>')
@auth.login_required
def recover_comment(commentid):
    user = g.user
    comment = Comments.query.get_or_404(commentid)
    if comment.creator != user and user.role != 'Admin':
        abort(403)
    comment.disabled = False #enable
    db.session.add(comment)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/<int:userid>/comments')
def get_user_comments(userid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_comments = Comments.query.filter_by(creator_id=userid)\
                           .order_by(Comments.timestamp.desc())
    comments = all_comments.offset(page*per_page).limit(per_page)
    comments_dict = {
        'comments': [c.to_dict() for c in comments],
        'total': all_comments.count(),
        'currentpage': page
    }
    return jsonify(comments_dict)

@rest.route('/all/comments')
def get_all_comments():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    all_comments = Comments.query
    comments = all_comments.offset(page*per_page).limit(per_page)
    comments_dict = {
        'comments': [c.to_dict() for c in comments],
        'total': all_comments.count(),
        'currentpage': page
    }
    return jsonify(comments_dict)

@rest.route('/<int:userid>/voted/demands')
def get_voted_demands(userid):
    #user = Users.query.get_or_404(userid) #which is better?
    #vote_demands = user.vote_demands.order_by(Dvote.timestamp.desc()) 
    vote_demands = Dvote.query.filter_by(user_id=userid)\
                        .order_by(Dvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    demands = [d.vote_demand \
            for d in vote_demands.offset(page * per_page).limit(per_page)]
    demands_dict = {
        'demands': [d.to_dict() for d in demands],
        'total': vote_demands.count()
    }
    return jsonify(demands_dict)

@rest.route('/<int:userid>/voted/clips')
def get_voted_clips(userid):
    vote_clips = Cvote.query.filter_by(user_id=userid)\
                            .order_by(Cvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    clips = [c.vote_clip \
            for c in vote_clips.offset(page * per_page).limit(per_page)]
    clips_dict = {
        'clips': [c.to_dict() for c in clips],
        'total': vote_clips.count()
    }
    return jsonify(clips_dict)

@rest.route('/<int:userid>/voted/reviews')
def get_voted_reviews(userid):
    vote_reviews = Rvote.query.filter_by(user_id=userid)\
                        .order_by(Rvote.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    reviews = [c.vote_review \
            for c in vote_reviews.offset(page * per_page).limit(per_page)]
    reviews_dict = {
        'reviews': [c.to_dict() for c in reviews],
        'total': vote_reviews.count()
    }
    return jsonify(reviews_dict)

@rest.route('/<int:userid>/fav/tags')
def get_fav_tags(userid):
    fav_tags = Fav.query.filter_by(user_id=userid)\
                        .order_by(Fav.timestamp.desc())
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    tags = [t.fav_tag for t in fav_tags.offset(page * per_page).limit(per_page)]
    tags_dict = {
        'tags': [t.to_dict() for t in tags],
        'total': fav_tags.count()
    }
    return jsonify(tags_dict)


@rest.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context))
    return response

@rest.errorhandler(400)
@rest.errorhandler(401)
@rest.errorhandler(403)
@rest.errorhandler(404)
@rest.errorhandler(418)
@rest.errorhandler(500)
def error_handler(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        msg = error.message
        code = 500
    return error_response(code, message=msg)

#################################################
## just for test
@rest.route('/testerror')
#@auth.login_required
def test_error():
    abort(502)
##################################################