# -*- coding: utf-8 -*-

import random
import re
from flask import g, render_template, redirect, url_for, current_app,\
                  request, session, flash, make_response, abort
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, ItemForm, EditItemForm, SelectAddForm,\
                   TagForm, EditPostForm, EditTipsForm, CommentForm,\
                   TagStrForm, ClipForm, ArticleForm, \
                   DeadlineForm, DemandForm, ReviewForm, CheckItemForm
from .. import db
from ..models import Posts, Items, Collect, Tags, Clan, Fav, tag_post, tag_item,\
                     Comments, Reviews, Clips, Demands, tag_demand, Reply,\
                     Star, Flag, Challenge, Contribute, Respon, Rvote, Dvote,\
                     Users, Follow, Roles, Permission, Articles, Columns,\
                     Authors, Byline, Messages, Dialog, Events
from ..decorators import admin_required, permission_required
from ..utils import split_str, str_to_dict, str_to_set
from ..bot import spider


@main.route('/')
def index():
    """Get posts from func in Model. need to tackle the cache issue"""
    posts_select = Posts.select_posts()
    tags = Tags.get_tags()

    return render_template("index.html",tags =tags,
                            posts_select=posts_select)


@main.route('/collection', methods=['GET','POST'])
@login_required
def collection():
    """
    News Feeds as per user's activities: follow, favirate, 
    challenge etc.
    """ 
    form = DemandForm() 
    if form.validate_on_submit():
        sp = form.body.data.split("#")+['42']
        tag_str = sp[1].strip()
        demand = Demands(
            body=sp[0],
            dtag_str = tag_str,
            requestor=current_user._get_current_object()
        )
        db.session.add(demand)
        #save activity to db Events
        current_user.set_event(action='request',demand=demand)
        demand.dtag_to_db()  # need to confirm
        db.session.commit()

        return redirect(url_for('.collection'))
    
    #get related tags set and fav tags, from cached Model-func
    tag_set, tag_fv = current_user.get_tag_set()
    # get followed posts queries
    post_fo = [f.followed.posts for f in current_user.followed] 
    #list the queries, followed _posts as init 
    q_list = post_fo
    for tag_obj in tag_set:
        q_list.append(tag_obj.posts)
    q_rand = Posts.query.order_by(db.func.rand()).limit(5)
    # union the queries,
    query = q_rand.union(*q_list) 
   
    page = request.args.get('page', 1, type=int)
    pagination = query.filter(Posts.creator != current_user).\
                order_by(Posts.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    posts = pagination.items

    return render_template('collection.html', 
                        posts=posts, form=form,
                        pagination=pagination, tags=tag_fv[:20])


@main.route('/create',methods=['GET','POST'])
@main.route('/answer/<int:id>',methods=['GET','POST'])
@login_required
def create(id=None):
    """Create new Post or Answer a Request"""
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            intro=form.intro.data,
            tag_str=form.tag.data,
            rating=form.rating.data,
            credential=form.credential.data,
            editable=form.editable.data,
            creator=current_user._get_current_object()
        )
        db.session.add(post)

        # link to demand if come from demand
        if id:
            demand = Demands.query.get(id) #demand's id
            if demand:
                respon = Respon(
                    post=post,
                    demand=demand
                )
                db.session.add(respon) 

        #add tag to db, attach post to tag
        post.tag_to_db()
        #save activity to db Events
        current_user.set_event(action='create',post=post)
        db.session.commit()

        post_id = post.id
        flash('The post has been created, now add items to it.')
        return redirect(url_for('.post',id=post_id))

    return render_template('create.html',form=form)


@main.route('/readuplist/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)

    if post.disabled and current_user != post.creator:
        return 'This Post was Disabled or Deleted'

    contribute = post.contributors.filter_by(
        user_id=current_user.id,
        disabled=False
        ).first()

    posts_query = post.creator.posts.filter(Posts.id != id)
    m = current_app.config['COMMENT_PER_PAGE']
    posts = posts_query.limit(m) 
    posts_count = posts_query.count()
    
    if post.uneditable:
        display = False
    else:
        display = True
    
    items = [_c.item for _c in post.items.order_by(Collect.order)]
    c_tips = Collect.query.filter_by(post_id=id)
    tips_c = {t.item_id:t for t in c_tips}  # item_id maping tip-object

    contributes = post.contributors
    contributors = [i.contributor for i in contributes]
    comments = post.comments.order_by(Comments.timestamp.desc())
     
    return render_template('post.html', 
                           m=m, posts_count=posts_count,
                           post=post, items=items, posts=posts,
                           tips_c=tips_c, display=display,
                           contributes=contributes,
                           contributors=contributors,
                           comments=comments)


@main.route('/checkitemfor/<int:id>',methods=['GET','POST'])
@login_required
def check_item(id):
    """Check a item if in db or can get info by spider"""
    post = Posts.query.get_or_404(id)

    if post.uneditable:
        flash('You do not have the permissions to edit this content')
        abort(403)
    #Should be locked during editing
    if post.editable != "Creator":
        if post.mod_locked():
            return redirect(url_for('.post',id=id))
    
    re_url=r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    #re_uid=r'([-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})'
    reg_url = re.compile(re_url,0)
    form = CheckItemForm()
    if form.validate_on_submit():
        checker = form.checker.data
        if reg_url.match(checker):
            d = spider.parse_html(checker)
        else:
            uid=checker.replace('-','').replace(' ','')
            item=Items.query.filter_by(uid=uid).first()
            d={}
            if item is not None:
                d['title'] = item.title
                d['uid'] = item.uid
                d['res_url'] = item.res_url
                d['author'] = item.author
                d['cover'] = item.cover
                d['cate'] = item.cate    

        session['d_pass'] = d        
                
        return redirect(url_for('.add_item', id=id))
    
    return render_template('check_item.html',form=form,post=post)  

@main.route('/checktoadditemfor/<int:id>')
@login_required
def check_to_add(id):
    """bridge gap and unlock temporarily"""
    post = Posts.query.get_or_404(id)
    post.unlock() ##!!
    return redirect(url_for('.add_item',id=id))

                
@main.route('/readuplist/add/<int:id>',methods=['GET','POST'])
@login_required
def add_item(id):
    """Add item and tips to post"""
    post = Posts.query.get_or_404(id)
    if post.uneditable:
        flash('You do not have the permissions to edit this content')
        abort(403)

    form = ItemForm()
    d = session.get('d_pass') or {}
    #session.pop('d_pass',None) #if pop here, no d for on_submit

    #Should be locked during editing, cannot bypass if from check_item
    if post.editable != "Creator":
        if post.mod_locked():
            return redirect(url_for('.post',id=id))

    if form.validate_on_submit():
        uid=form.uid.data.replace('-','').replace(' ','')
        old_item = Items.query.filter_by(uid=uid).first()

        if form.res_url.data.strip(): # is not "": # check the input whitespace
            oc_item = Items.query.filter_by(
                res_url=form.res_url.data.strip()).first()
        else:
            oc_item = None

        tips = form.tips.data
        tip_creator = current_user._get_current_object()

        if old_item is None and oc_item is None:
            _binding=d.get('binding')
            new_item = Items(
                uid=uid,
                title=form.title.data,
                res_url = form.res_url.data,
                author=form.author.data,
                cover=form.cover.data,
                cate=d.get('cate') or form.cate.data,
                publisher=d.get('Publisher'),
                pub_date=d.get('Publication Date') or d.get('publish_date'),
                language=d.get('Language','English'),
                details=d.get('details'),
                isbn10=d.get('ISBN-10').replace('-','').replace(' ','') \
                       if d.get('ISBN-10') else None,
                asin=d.get('ASIN').replace('-','').replace(' ','') \
                       if d.get('ASIN') else None,
                binding= _binding, 
                page=d.get(_binding) or d.get('Print Length'),
                price=d.get('price'),
                level=d.get('Level')
            )
            db.session.add(new_item)            
            post.collecting(new_item,tips,tip_creator)

            if form.author.data.strip(): # is not "":
                new_item.author_to_db()
            
        elif old_item is not None:
            post.collecting(old_item,tips,tip_creator)
            
        elif oc_item is not None:
            post.collecting(oc_item,tips,tip_creator)

        db.session.commit()
        #pop session
        session.pop('d_pass',None)

        return redirect(url_for('.post', id=id))

    if d:
        form.cate.data = d.get('cate','Book')
        form.title.data = d.get('title')
        form.uid.data = d.get('uid')
        form.author.data = d.get('author')
        form.cover.data = d.get('cover')
        form.res_url.data = d.get('res_url')
    
    return render_template('add_item.html', 
                            form=form, post=post)

@main.route('/item/<int:item_id>/tolist',methods=['GET','POST'])
@login_required
def item_to_post(item_id=None,post_id=None):
    """Add an existing item to created Post"""
    item = Items.query.get_or_404(item_id)
    #get lists created by current_user and set as chioices
    myposts = current_user.posts.order_by(db.func.rand())
    form = SelectAddForm()
    if myposts.count() == 0:
        flash('You have not created any list, You can create now')
        return redirect(url_for('.create'))
    else:
        form.selectlist.choices = [(0,"")] + [(m.id,m.title) for m in myposts]

    if form.validate_on_submit():
        post = Posts.query.get_or_404(form.selectlist.data)
        #Should be locked during editing
        if post.editable != "Creator":
            post.unlock()  ##!!
        
        tips = form.tips.data
        tip_creator = current_user._get_current_object()
        #collect to post
        post.collecting(item,tips,tip_creator)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    return render_template('item_to_post.html', form=form, item=item)


@main.route('/lockselected/<id>')
def lock_select(id):
    post = Posts.query.get(int(id))
    if current_user == post.creator and post.editable != "Creator":
        post.lock() ## if change select w/o submit, how to unlock the locked ?
    return 'The content selected should be locked during edit'


@main.route('/readuplist/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    """Edit Post Title,intro,credential,editable"""
    post = Posts.query.get_or_404(id)

    if post.uneditable:
        flash('You do not have the permission to edit this content')
        abort(403)
    #Should be locked during editing
    if post.editable != "Creator":
        if post.mod_locked():
            return redirect(url_for('.post',id=id))
        # # GET to  render edit tpl
        # if request.method == "GET":
        #     if post.check_locked():
        #         flash('The content is in editing, to avoid conflict, Please Try later')
        #         return redirect(url_for('.post',id=id))
        #     # set edit_start as indict editing
        #     post.lock()
        # # on_submit as edit done POST
        # if request.method == "POST":
        #     post.unlock()
    
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.intro = form.intro.data
        post.rating = form.rating.data
        post.credential = form.credential.data
        post.editable = form.editable.data
        
        #update the renew timestamp
        post.renew()
        # save activity to db Events
        current_user.set_event(action='alter',post=post)
        db.session.commit()    
        
        return redirect(url_for('.post',id=id))

    form.title.data = post.title
    form.intro.data = post.intro
    form.rating.data = post.rating
    form.credential.data = post.credential
    form.editable.data = post.editable
    return render_template('edit_post.html',form=form,post=post)

@main.route('/gobackreaduplist/<int:id>')  
@login_required
def goback_edit(id):
    """give up the editing and unlock"""
    post = Posts.query.get_or_404(id)
    post.unlock() ##!!
    return redirect(url_for('.post',id=id))


@main.route('/del/readuplist/<int:id>')
@login_required
def del_post(id):
    """Del Post by creator if no star or challenge"""
    post = Posts.query.get_or_404(id)  #post 's id

    if (current_user != post.creator or 
        post.starers.count() != 0 or 
        post.challengers.count() != 0 or 
        post.contributors.count() != 0 or 
        post.check_locked()):
        flash('You do not have the permissions to delete this content \
               or The content is locked')
        abort(403)
    
    post.disabled = True
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('.index'))

@main.route('/recover/readuplist/<int:id>')
@login_required
def recover_post(id):
    """recover Post by creator"""
    post = Posts.query.get_or_404(id)  #post 's id

    if current_user == post.creator and post.disabled:
        post.disabled = False
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post',id=post.id))


@main.route('/applycontributetolist/<int:id>')
@login_required
def apply_contributor(id):
    """Apply to be a contributor if the post set as editable"""
    post = Posts.query.get_or_404(id)  #post 's id
    if current_user == post.creator:
        pass
    else:
        c = Contribute(
            contributor = current_user._get_current_object(),
            contribute_post = post
        )
        db.session.add(c)
        db.session.commit()
        flash('You have applied to be a contributor, Please Waiting on approval')

        return redirect(url_for('.post',id=id))

@main.route('/approcecontributoroflist/<int:id>')
@login_required
def approve_contributor(id):
    """Approve contributor by creator"""
    c = Contribute.query.filter_by(id=id).first_or_404() # collect's id
    post = Posts.query.get_or_404(c.post_id)
    if current_user == post.creator:
        c.disabled = False
        db.session.add(c)
        db.session.commit()
        flash('Approved')

        return redirect(url_for('.post',id=id))


@main.route('/disablecontributoroflist/<int:id>')
@login_required
def disable_contributor(id):
    """Disable contributor by creator"""
    c = Contribute.query.filter_by(id=id).first_or_404() #collect's id
    post = Posts.query.get_or_404(c.post_id)
    if current_user == post.creator:
        c.disabled = True
        db.session.add(c)
        db.session.commit()
        flash('Disabled')

        return redirect(url_for('.post',id=id))


@main.route('/tagstr/readuplist/<int:id>',methods=['GET','POST'])
@login_required
def edit_tag_str(id):
    """Edit tag_str and add new tags to db"""
    post = Posts.query.get_or_404(id)
    form = TagStrForm()

    #old_str = set(_tag.tag for _tag in post.tags)
    old_str = post.tag_str
    old_set = str_to_set(old_str)
    
    if form.validate_on_submit():
        post.tag_str = form.tag.data
        db.session.add(post)

        new_str = form.tag.data
        new_set = str_to_set(new_str)
        add_tags = new_set - old_set
        del_tags = old_set - new_set

        _query = Tags.query

        for t in add_tags:
            _tag = _query.filter_by(tag=t).first()
            if _tag is None:
                new_tag = Tags(tag=t)
                new_tag.posts.append(post)
                db.session.add(new_tag)
            else:
                _tag.posts.append(post)
                db.session.add(_tag)
        for tg in del_tags:
            _tag = _query.filter_by(tag=tg).first()
            _tag.posts.remove(post)

        db.session.commit()

        return redirect(url_for('.post',id=id))

    form.tag.data = old_str
    
    return render_template('edit_tagstr.html', 
                            post=post, form=form)


## star and unstar --non-ajax
@main.route('/star/readuplist/<int:id>',methods=['GET','POST'])
@login_required
def star_post(id):
    post = Posts.query.get_or_404(id)
    current_user.star(post)
    db.session.commit()
    return redirect(url_for('.post', id=post.id))

@main.route('/unstar/readuplist/<int:id>',methods=['GET','POST'])
@login_required
def unstar_post(id):
    post = Posts.query.get_or_404(id)
    current_user.unstar(post)
    db.session.commit()
    return redirect(url_for('.post', id=post.id))

##start for star Ajax ##################################################
######################################################################
@main.route('/countstar/<int:id>')
#@login_required
def countstar(id):
    post = Posts.query.get_or_404(id)
    if not current_user.staring(post):
        current_user.star(post)
        #save activity to db Events
        current_user.set_event(action='star',post=post)
    else:
        current_user.unstar(post)
    
    n = post.starers.count()
    post.cal_vote(n=n)
    db.session.commit()

    m=str(n)
    return m 
#######################################################################
##end for star Ajax ######################################################

##start for challenge Ajax ##################################################
######################################################################
@main.route('/countchallenge/<int:id>')
#@login_required
def countchallenge(id):
    post = Posts.query.get_or_404(id)
    if not current_user.challenging(post):
        current_user.challenge(post)
        #save activity to db Events
        current_user.set_event(action='challenge',post=post)
    else:
        current_user.unchallenge(post)

    a = post.challengers.count()
    post.cal_vote(m=a*2)
    db.session.commit()
    
    b=str(a)
    return b 
#######################################################################
##end for challenge Ajax ######################################################


@main.route('/item/<int:id>')
def item(id):
    item = Items.query.get_or_404(id)   # item 's id
    posts = [_c.post for _c in item.posts]

    m = current_app.config['COMMENT_PER_PAGE']
    
    review_q = item.reviews
    count_review = review_q.count()
    comment_q = item.comments
    count_comment = comment_q.count()
    #comment_my = query.filter(Comments.creator==current_user)
    #count_my = comment_my.count()
  
    comments = comment_q.order_by(Comments.timestamp.desc()).limit(m)
    review_latest = review_q.order_by(Reviews.timestamp.desc()).limit(m)
    review_hot = review_q.order_by(Reviews.vote.desc()).limit(m)
     
    return render_template('item.html', 
                           item=item, posts=posts,
                           review_hot=review_hot,
                           count_review=count_review, 
                           review_latest=review_latest, 
                           count_comment=count_comment, 
                           comments=comments, m=m)


@main.route('/item/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_item(id):
    _query = Items.query     
    item = _query.get_or_404(id)  # item 's id
    form = EditItemForm()

    #for edit author  byline
    old_str = item.author

    if form.validate_on_submit():
        uid=form.uid.data.replace('-','').replace(' ','')
        if (_query.filter_by(uid=uid).first() is not None) and \
        (item.uid != uid):
            abort(403)

        item.uid = uid
        item.title = form.title.data
        item.res_url = form.res_url.data
        item.author = form.author.data
        item.cover = form.cover.data
        item.cate = form.cate.data
        item.publisher = form.publisher.data
        item.pub_date = form.pub_date.data
        item.language = form.language.data
        item.binding = form.binding.data
        item.page = form.page.data
        item.level = form.level.data
        item.price = form.price.data
        item.details = form.details.data

        # add tags to db, if any
        if form.itag.data.strip(): # is not "":
            itag_str = item.itag_str
            if itag_str:
                itag_str += ',' + form.itag.data.strip()
            else:
                itag_str = form.itag.data.strip()
            item.itag_str = itag_str 
            item.itag_to_db()

        db.session.add(item)
        
        #edit author  byline
        old_d = str_to_dict(old_str)
        old_set = set(k for k in old_d if k is not "None")
        new_str = form.author.data
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

        #save activity to db Events
        current_user.set_event(action='edit',item=item)
        db.session.commit()

        return redirect(url_for('.item', id=id))

    form.uid.data = item.uid 
    form.title.data = item.title 
    form.res_url.data = item.res_url
    form.author.data = old_str    
    form.cover.data = item.cover 
    form.cate.data = item.cate  
    form.publisher.data = item.publisher
    form.pub_date.data = item.pub_date
    form.language.data = item.language
    form.binding.data = item.binding
    form.page.data = item.page 
    form.level.data = item.level
    form.price.data = item.price  
    form.details.data = item.details 

    return render_template('edit_item.html',form=form,item=item)

#####################################################
##### flag  non-ajax ,using in _show_item_1, post ###
@main.route('/item/flag1/<int:id>')
@login_required
def flag_1_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,1)
    #save activity to db Events
    current_user.set_event(action='schedule',item=item)
    db.session.commit()
    return redirect(url_for('.item',id=id))

@main.route('/item/flag2/<int:id>')
@login_required
def flag_2_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,2)
    #save activity to db Events
    current_user.set_event(action='working on',item=item)
    db.session.commit()
    return redirect(url_for('.item',id=id))

@main.route('/item/flag3/<int:id>')
@login_required
def flag_3_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,3)
    #save activity to db Events
    current_user.set_event(action='get done',item=item)
    db.session.commit()
    return redirect(url_for('.item',id=id))

#################################################################
#### start for flag Ajax ########################################
#################################################################
@main.route('/flag1/<int:id>')
#@login_required
def flag_1(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,1)
    #save activity to db Events
    current_user.set_event(action='schedule',item=item)
    db.session.commit()
    return "" 
@main.route('/flag2/<int:id>')
#@login_required
def flag_2(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,2)
    #save activity to db Events
    current_user.set_event(action='working on',item=item)
    db.session.commit()
    return "" 
@main.route('/flag3/<int:id>')
#@login_required
def flag_3(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,3)
    #save activity to db Events
    current_user.set_event(action='get done',item=item)
    db.session.commit()
    return "" 
###################################################################
#### end for flag Ajax#############################################
###################################################################


@main.route('/readuptips/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_tips(id):
    """Edit tips or modify the item order"""
    tip_c = Collect.query.filter_by(id=id).first_or_404()  #collect 's id
    post_id = tip_c.post_id
    post = Posts.query.get_or_404(post_id)

    if post.uneditable:
        flash('You do not have the permissions to edit the content')
        abort(403)
    #Should be locked during editing
    if post.editable != "Creator":
        if post.mod_locked():
            return redirect(url_for('.post',id=post_id))

    item = Items.query.get_or_404(tip_c.item_id)
    
    form = EditTipsForm()
    if form.validate_on_submit():
        post.ordering(item, form.order.data)
        post.renew()
        tip_c.tips = form.tips.data
        db.session.add(tip_c)
        #save activity to db Events
        current_user.set_event(action='modify',post=post,item=item)
        db.session.commit()

        return redirect(url_for('.post', id=post_id))
    
    form.tips.data = tip_c.tips
    form.order.data = tip_c.order
     
    return render_template('edit_tips.html', 
                           form=form, tip_c=tip_c,
                           post=post, item=item)    

@main.route('/tips/del/<int:id>')
@login_required
def del_tips(id):
    """Del item and tips , re-ordering items"""
    tip_c = Collect.query.filter_by(id=id).first_or_404()  
    #collect 's id,but not get_or_404, for 3 primary key

    if current_user != tip_c.tip_creator:
        abort(403)

    #once delete an item. need to re-ordering,
    #order the to-be-del item to the last, then del
    item = Items.query.get_or_404(tip_c.item_id)
    post = Posts.query.get_or_404(tip_c.post_id)
    n = post.items.count()
    post.ordering(item, n)
    db.session.delete(tip_c)
    db.session.commit()

    return redirect(url_for('.post', id=tip_c.post_id))


@main.route('/tag/<int:id>')
def tag(id):
    # joined query should be here, per the tagname, return the lists
    _query = Tags.query 
    tag = _query.get_or_404(id)

    parent_tags = [t.parent_tag for t in tag.parent_tags.\
                    order_by(db.func.rand()).limit(5)]
    tags = []
    for tg in parent_tags:
        c_tags = [t.child_tag for t in Clan.query.\
                  filter_by(parent_tag_id=tg.id).\
                  order_by(db.func.rand()).limit(5)]
        tags += c_tags

    posts = tag.posts
    
    return render_template('tag.html',
                           tag=tag, tags=tags, 
                           posts=posts, parent_tags=parent_tags)


@main.route('/tag/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_tag(id):
    _query = Tags.query
    tag = _query.get_or_404(id)  #tag 's id

    form = TagForm()
    if form.validate_on_submit():
        if (tag.tag != form.tag.data) and \
        (_query.filter_by(tag=form.tag.data).first() is not None):
            flash('Duplicated Tag Name,please try again')
            abort(403)  # check if duplicate tag name
        tag.tag = form.tag.data
        tag.descript = form.descript.data
        db.session.add(tag)

        parent_tag = _query.filter_by(tag=form.parent.data).first()
        if parent_tag is None:
            parent_tag= Tags(tag=form.parent.data)
            db.session.add(parent_tag)
        #save activity to db Events
        current_user.set_event(action='edit',tag=tag)
        tag.parent(parent_tag)
        db.session.commit()
        
        return redirect(url_for('.tag', id=id))
    
    form.tag.data = tag.tag
    form.descript.data = tag.descript
     
    return render_template('edit_tag.html',
                           tag=tag, form=form) 

######################################################################
#### start for fav tag Ajax ##########################################
######################################################################
@main.route('/countfav/<int:id>')
#@login_required
def countfav(id):
    tag = Tags.query.get_or_404(id)   # tag 's id
    if not current_user.faving(tag):
        current_user.fav(tag)
        #save activity to db Events
        current_user.set_event(action='fav',tag=tag)
    else:
        current_user.unfav(tag)

    v = tag.favers.count()
    db.session.commit()

    fv=str(v)
    return fv 
#######################################################################
#### end for fav tag Ajax #############################################
#######################################################################


@main.route('/catagory')
def catagory():
    page = request.args.get('page', 1, type=int)
    pagination = Tags.query.order_by(db.func.rand()).\
                paginate(
                    page,
                    per_page=current_app.config['TAG_PER_PAGE'],
                    error_out=False
                )
    tags = pagination.items

    return render_template('catagory.html', 
                           tags=tags,pagination=pagination)


@main.route('/challenge',methods=['GET','POST'])
@login_required
def challenge():
    """
    Show user's challenge post and items included
    Post clips of some item working on, like quote
    Set deadline for challenging
    """
    n = 5  # the num will show in challenge page
    ing_n = [i.flag_item for i in current_user.flag_items.\
               filter_by(flag_label=2).order_by(Flag.timestamp.desc())\
               .limit(n)]
    form = ClipForm()   
    # dynamic choice SelectField
    form.resource.choices = [(i.id,i.title) for i in ing_n]+[(0,"")]

    chal_post = current_user.challenge_posts.first()
    if chal_post is not None:
        post_chal = chal_post.challenge_post
        items = [i.item for i in post_chal.items.order_by(Collect.order)]
        
    else:
        post_chal = None
        items = None
         
    if form.validate_on_submit():
        clip = Clips(
            body = form.body.data,
            item = Items.query.get(form.resource.data),
            creator = current_user._get_current_object()
        )
        db.session.add(clip)
        #save activity to db Events
        current_user.set_event(action='excerpt',clip=clip)
        db.session.commit()

        return redirect(url_for('.challenge'))
    
    form2 = DeadlineForm()
    if form2.validate_on_submit() and chal_post is not None:
        chal_post.deadline = form2.deadline.data
        db.session.add(chal_post)
        db.session.commit()

        return redirect(url_for('.challenge'))

    # clips  
    m = current_app.config['COMMENT_PER_PAGE']  # when exeed this to show more
    query_my = current_user.clips.order_by(Clips.timestamp.desc())
    count_my = query_my.count()
    myclips =query_my.limit(m)
     
    return render_template('challenge.html', 
                            form=form, form2=form2, m=m,
                            myclips=myclips, count_my=count_my,
                            chal_post=chal_post, 
                            items=items, post_chal=post_chal)


@main.route('/myclips/<int:id>')
@login_required
def myclips(id):
    """Show all the clips of a user"""
    user = Users.query.get_or_404(id) # user id
    chal_post = user.challenge_posts.first()
    if chal_post is not None:
        post_chal = chal_post.challenge_post
        items = [i.item for i in post_chal.items.order_by(Collect.order)]
    else:
        post_chal = None
        items = None

    page = request.args.get('page', 1, type=int)
    pagination = user.clips.order_by(Clips.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    myclips = pagination.items

    return render_template('myclips.html',
                            user=user,pagination=pagination, 
                            myclips=myclips, chal_post=chal_post, 
                            items=items, post_chal=post_chal)

@main.route('/allclips')
@login_required
def allclips():
    """Show all clips except current_user's"""
    page = request.args.get('page', 1, type=int)
    pagination = Clips.query.filter(Clips.creator!=current_user)\
                      .order_by(Clips.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    allclips = pagination.items

    return render_template('allclips.html',
                           pagination=pagination,
                           allclips=allclips)


@main.route('/demands')
def demands():
    _query = Demands.query
    demands_most = _query.order_by(Demands.vote.desc()).limit(50)
    demands_random = _query.order_by(db.func.rand()).limit(50)

    page = request.args.get('page', 1, type=int)
    pagination_latest = _query.order_by(Demands.timestamp.desc()).\
                        paginate(
                            page,
                            per_page=current_app.config['DEMAND_PER_PAGE'],
                            error_out=False
                        )
    demands_latest = pagination_latest.items

    return render_template('demands.html',
                            demands_latest=demands_latest,
                            pagination_latest=pagination_latest,
                            demands_most=demands_most,
                            demands_random=demands_random)

@main.route('/demand/<int:id>', methods=['GET','POST'])
@login_required
def demand(id):
    demand = Demands.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        commt = Comments(
            body=form.body.data,
            demand = demand,
            creator=current_user._get_current_object()
        )
        db.session.add(commt)
        db.session.commit()

        return redirect(url_for('.demand', id=id))
        
    page = request.args.get('page', 1, type=int)
    pagination = demand.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    tags = Tags.get_tags()

    return render_template('demand.html',
                            demand=demand, form=form, tags=tags,
                            pagination=pagination, comments=comments)

    
@main.route('/comment/p/<int:id>', methods=['GET','POST'])  
@login_required
def add_post_comment(id):
    post = Posts.query.get_or_404(id)   # post 's id
    form = CommentForm()
    if form.validate_on_submit():
        commt = Comments(
            body=form.body.data,
            post = post,
            creator=current_user._get_current_object()
        )
        db.session.add(commt)
        db.session.commit()

        return redirect(url_for('.post', id=id))

    return render_template('comment.html', 
                            form=form, 
                            onsth=post, mark=None)

@main.route('/comment/i/<int:id>', methods=['GET','POST'])  
@login_required
def add_item_comment(id):
    item = Items.query.get_or_404(id)   # item 's id
    form = CommentForm()
    if form.validate_on_submit():
        commt = Comments(
            body=form.body.data,
            item = item,
            creator=current_user._get_current_object()
        )
        db.session.add(commt)
        db.session.commit()

        return redirect(url_for('.item', id=id))

    return render_template('comment.html', 
                            form=form, 
                            onsth=item, mark=True)


@main.route('/review/<int:id>', methods=['GET','POST'])
@login_required
def review(id):
    review = Reviews.query.get_or_404(id) #review's id
    form = CommentForm()
    if form.validate_on_submit():
        commt = Comments(
            body=form.body.data,
            review=review,
            creator=current_user._get_current_object()
        )
        db.session.add(commt)
        db.session.commit()

        return redirect(url_for('.review',id=id))
        
    page = request.args.get('page', 1, type=int)
    pagination = review.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template(
                'review.html',
                review=review, form=form,
                pagination=pagination, comments=comments)


@main.route('/review/i/<int:id>', methods=['GET','POST'])
@login_required
def add_review(id):
    item = Items.query.get_or_404(id)   # item 's id
    form = ReviewForm()
    if form.validate_on_submit():
        review = Reviews(
            heading=form.heading.data,
            body=form.body.data,
            item = item,
            creator=current_user._get_current_object()
        )
        db.session.add(review)
        #save activity to db Events
        current_user.set_event(action='add',review=review)
        db.session.commit()

        return redirect(url_for('.item', id=id))

    return render_template('add_review.html', 
                           form=form, item=item)
                           
@main.route('/review/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_review(id):
    review = Reviews.query.get_or_404(id) # review 's id
    form = ReviewForm()
    if form.validate_on_submit():
        review.heading=form.heading.data
        review.body=form.body.data
        db.session.add(review)
        db.session.commit()
        
        return redirect(url_for('.review', id=id))

    form.heading.data = review.heading
    form.body.data = review.body
    
    return render_template('edit_review.html', 
                           form=form, review=review)


@main.route('/alsoreq/<int:id>')
@login_required
def alsoreq(id):
    demand = Demands.query.get_or_404(id) # demand's id
    voted = Dvote.query.filter_by(user_id=current_user.id,demand_id=id).first()
    if current_user != demand.requestor and voted is None:
        demand.vote = demand.vote + 1 
        db.session.add(demand)

        dvote = Dvote(
            voter=current_user._get_current_object(),
            vote_demand=demand
        )
        db.session.add(dvote)
        #save activity to db Events
        current_user.set_event(action='request',demand=demand)
        db.session.commit()

    return redirect(url_for('.demand',id=id))

@main.route('/endorse/<int:id>')
@login_required
def endorse(id):
    review = Reviews.query.get_or_404(id) # review's id
    endorsed = Rvote.query.filter_by(user_id=current_user.id,review_id=id).first()
    if current_user != review.creator and endorsed is None:
        review.vote = review.vote + 1 
        db.session.add(review)

        rvote = Rvote(
            voter=current_user._get_current_object(),
            vote_review=review
        )
        db.session.add(rvote)
        #save activity to db Events
        current_user.set_event(action='endorse',review=review)
        db.session.commit()
    #n = review.vote
    #m = str(n)
    return redirect(url_for('.review',id=id))


@main.route('/delcommt/<int:id>')  
@login_required
def del_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id
    user_id = commt.creator.id
    if current_user == commt.creator:
        db.session.delete(commt)
        db.session.commit()

    return redirect(url_for('auth.profile', id=user_id))

## Moderate comments
@main.route('/disablecomment/<int:id>')  
@login_required
@permission_required(Permission.MOD_CONTENT)
def disable_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id
    commt.disabled = True
    db.session.add(commt)
    db.session.commit()

    return "Disabled,DONE" #redirect(url_for('.index'))

@main.route('/enablecommt/<int:id>')  
@login_required
@permission_required(Permission.MOD_CONTENT)
def enable_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id    
    commt.disabled = False
    db.session.add(commt)
    db.session.commit()

    return "Enabled, DONE" #redirect(url_for('.index'))


@main.route('/morecommt/u/<int:id>')  
@login_required
def morecomment_u(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template('morecomment_u.html',
                           user=user, 
                           comments=comments,
                           pagination=pagination)

@main.route('/morecommt/i/<int:id>')  
@login_required
def morecomment_i(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)
    pagination = item.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template('morecomment_i.html',
                           item=item, comments=comments,
                           pagination=pagination, user=None)

@main.route('/mycommt/i/<int:id>')  
@login_required
def mycomment_i(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)
    pagination = item.comments.filter(Comments.creator == current_user).\
                order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template('morecomment_i.html',
                           item=item, comments=comments,
                           pagination=pagination, user=True)

@main.route('/morecommt/p/<int:id>')  
@login_required
def morecomment_p(id):
    post = Posts.query.get_or_404(id)   # post 's id 
    challengers = [c.challenger for c in post.challengers]

    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template('morecomment_p.html',
                           post=post, comments=comments,
                           pagination=pagination, 
                           challengers=challengers)


@main.route('/morelist/u/<int:id>')
@login_required
def morepost(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Posts.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    posts = pagination.items

    return render_template('morepost.html',
                           user=user, posts=posts,
                           pagination=pagination, ref="created",
                           endpoint=".morepost")

@main.route('/morestar/u/<id>')  
@login_required
def morestar(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.star_posts.order_by(Star.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    posts = [item.star_post for item in pagination.items]

    return render_template('morepost.html',
                           user=user, posts=posts,
                           pagination=pagination, ref="star-ed",
                           endpoint=".morestar")


@main.route('/morereview/u/<id>')  
@login_required
def morereview_u(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.reviews.order_by(Reviews.vote.desc()).\
                paginate(
                     page,
                     per_page=current_app.config['POST_PER_PAGE'],
                     error_out=False
                )
    reviews = pagination.items

    return render_template('morereview.html',
                           item=None, reviews=reviews,
                           pagination=pagination, 
                           user=user, ref="user",
                           endpoint=".morereview_u")


@main.route('/morereview/i/<id>')  
@login_required
def morereview(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)
    pagination = item.reviews.order_by(Reviews.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    reviews = pagination.items

    return render_template('morereview.html',
                           item=item, reviews=reviews,
                           pagination=pagination, 
                           user=None, ref="Latest",
                           endpoint=".morereview")

@main.route('/morehot/i/<id>')  
@login_required
def morehot(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)
    pagination = item.reviews.order_by(Reviews.vote.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    reviews = pagination.items

    return render_template('morereview.html',
                           item=item, reviews=reviews,
                           pagination=pagination, 
                           user=None, ref="Hot",
                           endpoint=".morehot")


@main.route('/moreschedule/u/<id>')  
@login_required
def moreschedule(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.flag_items.filter_by(flag_label=1).\
                order_by(Flag.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    items = [item.flag_item for item in pagination.items]

    return render_template('moreitem.html',
                           user=user, items=items,
                           pagination=pagination, ref="scheduled",
                           endpoint=".moreschedule")


@main.route('/moredoing/u/<id>')  
@login_required
def moredoing(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.flag_items.filter_by(flag_label=2).\
                order_by(Flag.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    items = [item.flag_item for item in pagination.items]

    return render_template('moreitem.html',
                           user=user, items=items,
                           pagination=pagination, ref="working on",
                           endpoint=".moredoing")

@main.route('/moredone/u/<id>')  
@login_required
def moredone(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.flag_items.filter_by(flag_label=3).\
                order_by(Flag.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    items = [item.flag_item for item in pagination.items]

    return render_template('moreitem.html',
                           user=user, items=items,
                           pagination=pagination, ref="have done",
                           endpoint=".moredone")

##################################################################
#### follow and unfollow - non-ajax ##############################
@main.route('/follow/<id>')
@login_required
def follow(id):
    user = Users.query.get_or_404(id)  # to_be_followed user 's id
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('auth.profile', id=id))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('auth.profile', id=id))

@main.route('/unfollow/<id>')
@login_required
def unfollow(id):
    user = Users.query.get_or_404(id)  # to_be_unfollowed user 's id
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('auth.profile', id=id))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('auth.profile', id=id))

######################################################################
#### start for follow Ajax ###########################################
######################################################################
@main.route('/countfollow/<int:id>')
#@login_required
def countfollow(id):
    user = Users.query.get_or_404(id)
    if not current_user.is_following(user):
        current_user.follow(user)
    else:
        current_user.unfollow(user)

    f = user.followers.count()
    db.session.commit()

    fs = str(f)
    return fs 
#######################################################################
#### end for follow Ajax ##############################################
#######################################################################

@main.route('/followers/<id>')
@login_required
def follower(id):
    user = Users.query.get_or_404(id)   # user's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.followers.order_by(Follow.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    followers = [item.follower for item in pagination.items]

    return render_template('follows.html',
                           user=user, follows=followers,
                           pagination=pagination, ref='follower')

@main.route('/following/<id>')
@login_required
def following(id):
    user = Users.query.get_or_404(id)   # user 's id 

    page = request.args.get('page', 1, type=int)
    pagination = user.followed.order_by(Follow.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    following = [item.followed for item in pagination.items]

    return render_template('follows.html',
                           user=user, follows=following,
                           pagination=pagination, ref='following')


@main.route('/article/<int:id>')
@login_required
def article(id):
    article = Articles.query.get_or_404(id)

    return render_template('article.html',article=article)


@main.route('/write', methods=['GET','POST'])
@main.route('/write/<int:id>',methods=['GET','POST'])
@login_required
def write(id=None):
    form = ArticleForm()
    if form.validate_on_submit():   
        if id:
            column = Columns.query.get_or_404(id) #column's id
        else:
            column = None
        article = Articles(
            title=form.title.data,
            figure=form.figure.data,
            body=form.body.data,
            column=column,
            writer=current_user._get_current_object()
        )
        db.session.add(article)
        db.session.commit()

        article_id = article.id
        return redirect(url_for('.article',id=article_id))
    
    return render_template('write.html',form=form)

@main.route('/article/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_article(id):
    article = Articles.query.get_or_404(id)

    if current_user != article.writer:
        abort(403)

    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.figure = form.figure.data
        article.body = form.body.data
        
        article.renew()
        db.session.commit()
        
        return redirect(url_for('.article', id=id))

    form.title.data = article.title
    form.figure.data = article.figure
    form.body.data = article.body

    return render_template('write.html',form=form,article=article)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/uid')
def random_uid():
    m=round(random.random()*10E8)
    uid = 'RUT'+str(m)
    while Items.query.filter_by(uid=uid).first() is not None:
        uid = 'RUT'+str(round(random.random()*10E8))
    else:
        return uid

# some random action
@main.route('/randreq')
def randreq():
    demand = Demands.query.order_by(db.func.rand()).first()
    if demand:
        return redirect(url_for('.demand',id=demand.id))
    else:
        return redirect(url_for('.index'))

@main.route('/randlist')
def randpost():
    post = Posts.query.order_by(db.func.rand()).first()
    if post:
        return redirect(url_for('.post',id=post.id))
    else:
        return redirect(url_for('.index'))

@main.route('/randreview')
def randreview():
    review = Reviews.query.order_by(db.func.rand()).first()
    if review:
        return redirect(url_for('.review',id=review.id))
    else:
        return redirect(url_for('.index'))
# check latest 
@main.route('/latest/list')
def latestpost():
    post = Posts.query.order_by(Posts.timestamp.desc()).first()
    if post:
        return redirect(url_for('.post',id=post.id))
    else:
        return redirect(url_for('.index'))

@main.route('/latest/<string:cat>')
def latestitem(cat):
    cate=str(cat).capitalize()
    item = Items.query.filter_by(cate=cate).order_by(Items.timestamp.desc()).first()
    if item:
        return redirect(url_for('.item',id=item.id))
    else:
        return redirect(url_for('.index'))