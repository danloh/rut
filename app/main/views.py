# -*- coding: utf-8 -*-

import random
from flask import g, render_template, redirect, url_for, current_app,\
                  request, session, flash, make_response, abort
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, ItemForm, EditItemForm, TagForm, EditPostForm,\
                   EditTipsForm, CommentForm, TagStrForm, ClipForm,\
                   DeadlineForm, DemandForm, ReviewForm
from .. import db
from ..models import Posts, Items, Collect, Tags, Clan, Fav, tag_post, tag_item,\
                     Comments, Reviews, Clips, Demands, tag_demand, Reply,\
                     Star, Flag, Challenge, Contribute, \
                     Users, Follow, Roles, Permission,\
                     Authors, author_item, Messages, Dialog, Events
from ..decorators import admin_required, permission_required


@main.route('/')
def index():

    _query = Posts.query

    posts_latest = _query.order_by(Posts.timestamp.desc()).limit(20)
    posts_popular = _query.order_by(Posts.starers).limit(20)
    posts_random = _query.order_by(db.func.rand()).limit(20)

    tags = Tags.query.order_by(db.func.rand()).limit(20)

    return render_template("index.html",tags =tags, 
                            posts_latest = posts_latest, 
                            posts_popular = posts_popular,
                            posts_random = posts_random)


@main.route('/collection', methods=['GET','POST'])
@login_required
def collection():
     
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
        db.session.commit()

        demand.dtag_to_db()  # need to confirm

        return redirect(url_for('.collection'))
    
    # list all tag related to user
    tag_s = [p.star_post.tags for p in current_user.star_posts] #2D LIST
    tag_c = [p.challenge_post.tags for p in current_user.challenge_posts] #2D 
    tag_fg = [i.flag_item.itags for i in current_user.flag_items] #2D 
    tag_fv = [i.fav_tag for i in current_user.fav_tags.order_by(db.func.rand())]
    #be unique
    tag_all = sum(tag_s + tag_c + tag_fg,[]) + tag_fv
    tag_set = set(tag_all)
    # get followed posts queries
    post_fo = [f.followed.posts for f in current_user.followed] 
    #list the queries, followed _posts as init 
    q_list = post_fo
    for tag_obj in tag_set:
        q_list.append(tag_obj.posts)
    q_rand = Posts.query.order_by(db.func.rand()).limit(5)
    # union the queries,
    query = q_rand.union(*q_list) #or q_rand

    #posts = query.all()
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
#@login_required
def create():
    
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
        db.session.commit()
        #add tag to db, attach post to tag
        post.tag_to_db()
        
        id = post.id
        flash('The post has been created, now add items to it.')  
        return redirect(url_for('.post',id=id))  
    return render_template('create.html',form = form)


@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    
    post = Posts.query.get_or_404(id) 
    contribute = post.contributors.filter_by(
        user_id=current_user.id,
        disabled=False
        ).first()

    posts_query = post.creator.posts.filter(Posts.id != id)
    m = 20
    posts = posts_query.limit(m) 
    posts_count = posts_query.count()
    
    if current_user == post.creator \
      or contribute  or post.editable == 'Everyone' :
        display = True 
    else:
        display = False
    
    items = [_c.item for _c in post.items.order_by(Collect.order)]  
    c_tips = Collect.query.filter_by(post_id=id)
    tips_c = {t.item_id:t for t in c_tips}  # item_id maping tip-object

    contributes = post.contributors
     
    return render_template('post.html', 
                           m=m, posts_count=posts_count,
                           post=post, items=items, posts=posts,
                           tips_c=tips_c, display=display,
                           contributes=contributes)


@main.route('/post/add/<int:id>',methods=['GET','POST'])
@login_required
def add_item(id):
    '''add item and tips to post'''
    post = Posts.query.get_or_404(id)
    contribute = post.contributors.filter_by(
        user_id=current_user.id,
        disabled=False
        ).first()
    if current_user != post.creator and contribute is None \
       and post.editable != 'Everyone' :
        abort(403)

    form = ItemForm()

    if form.validate_on_submit():

        old_item = Items.query.filter_by(uid=form.uid.data).first()

        if form.res_url.data.strip() is not "":  # check the input whitespace
            oc_item = Items.query.filter_by(
                res_url=form.res_url.data.strip()).first()
        else:
            oc_item = None

        tips = form.tips.data
        tip_creator = current_user._get_current_object()

        if old_item is None and oc_item is None:
            new_item = Items(
                uid=form.uid.data,
                title=form.title.data,
                res_url = form.res_url.data,
                author=form.author.data,
                cover=form.cover.data,
                cate=form.cate.data
            )
            db.session.add(new_item)            
            post.collecting(new_item,tips,tip_creator)
            
        elif old_item is not None:
            post.collecting(old_item,tips,tip_creator)
            
        elif oc_item is not None:
            post.collecting(oc_item,tips,tip_creator)
            
        
        return redirect(url_for('.post', id=post.id))

    return render_template('add_item.html', 
                            form=form, post=post)


@main.route('/post/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    contribute = post.contributors.filter_by(
        user_id=current_user.id,
        disabled=False
        ).first()
    if current_user != post.creator and contribute is None \
       and post.editable != 'Everyone' :
        abort(403)

    form = EditPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.intro = form.intro.data
        post.rating = form.rating.data
        post.credential = form.credential.data
        post.editable = form.editable.data
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.intro.data = post.intro
    form.rating.data = post.rating
    form.credential.data = post.credential
    form.editable.data = post.editable
    return render_template('edit_post.html', form=form)

@main.route('/post/del/<int:id>',methods=['GET','POST'])
@login_required
def del_post(id):
    post = Posts.query.get_or_404(id)  #post 's id

    if current_user != post.creator\
     or post.starers.count() != 0\
     or post.challengers.count() != 0\
     or post.contributors.count() != 0:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('.index'))


@main.route('/post/applycontribute/<int:id>',methods=['GET'])
@login_required
def apply_contributor(id):
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
        flash('You have applied to be a contributor, waiting on approval')
        return redirect(url_for('.post', id=id))

@main.route('/post/approcecontributor/<int:id>',methods=['GET'])
@login_required
def approve_contributor(id):
    c = Contribute.query.filter_by(id=id).first()
    post = Posts.query.get_or_404(c.post_id)
    if current_user == post.creator:
        c.disabled = False
        db.session.add(c)
        db.session.commit()
        flash('Approved')
        return redirect(url_for('.post', id=post.id))

@main.route('/post/disablecontributor/<int:id>',methods=['GET'])
@login_required
def disable_contributor(id):
    c = Contribute.query.filter_by(id=id).first()
    post = Posts.query.get_or_404(c.post_id)
    if current_user == post.creator:
        c.disabled = True
        db.session.add(c)
        db.session.commit()
        flash('Disabled')
        return redirect(url_for('.post', id=post.id))


@main.route('/post/tagstr/<int:id>',methods=['GET','POST'])
@login_required
def edit_tag_str(id):
    post = Posts.query.get_or_404(id)
    form = TagStrForm()

    #old_str = set(_tag.tag for _tag in post.tags)
    old = post.tag_str
    old_str = set(t.strip() for t in old.split(','))
    
    if form.validate_on_submit():

        post.tag_str = form.tag.data
        db.session.add(post)

        new_str = set(t.strip() for t in form.tag.data.split(','))
        add_tags = new_str - old_str
        del_tags = old_str - new_str

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
        
        return redirect(url_for('.post', id=post.id))

    form.tag.data = old
    
    return render_template('edit_tagstr.html', 
                            post=post, form=form)


## star and unstar --non-ajax
@main.route('/star/post/<int:id>',methods=['GET','POST'])
@login_required
def star_post(id):
    post = Posts.query.get_or_404(id)
    current_user.star(post)
    
    return redirect(url_for('.post', id=post.id))

@main.route('/unstar/post/<int:id>',methods=['GET','POST'])
@login_required
def unstar_post(id):
    post = Posts.query.get_or_404(id)
    current_user.unstar(post)
    
    return redirect(url_for('.post', id=post.id))

##start for star Ajax ##################################################
######################################################################
@main.route('/countstar/<int:id>',methods=['GET'])
#@login_required
def countstar(id):
    post = Posts.query.get_or_404(id)
    if not current_user.staring(post):
        current_user.star(post)
    else:
        current_user.unstar(post)

    n = post.starers.count()
    m=str(n)

    return m 
#######################################################################
##end for star Ajax ######################################################

##start for challenge Ajax ##################################################
######################################################################
@main.route('/countchallenge/<int:id>',methods=['GET'])
#@login_required
def countchallenge(id):
    post = Posts.query.get_or_404(id)
    if not current_user.challenging(post):
        current_user.challenge(post)
    else:
        current_user.unchallenge(post)

    a = post.challengers.count()
    b=str(a)

    return b 
#######################################################################
##end for challenge Ajax ######################################################


@main.route('/item/<int:id>', methods=['GET'])  
def item(id):
    item = Items.query.get_or_404(id)   # item 's id
    posts = [_c.post for _c in item.posts]

    m = 10
    
    review_q = item.reviews
    count_review = review_q.count()

    comment_q = item.comments
    count_comment = comment_q.count()

    #comment_my = query.filter(Comments.creator==current_user)
    #count_my = comment_my.count()
  
    comments = comment_q.limit(m)
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

    if form.validate_on_submit():
        if (_query.filter_by(uid=form.uid.data).first() is not None) and \
        (item.uid != form.uid.data):
            abort(403)

        item.uid = form.uid.data
        item.title = form.title.data
        item.res_url = form.res_url.data
        item.author = form.author.data
        item.translator = form.translator.data
        item.cover = form.cover.data
        item.cate = form.cate.data
        item.publisher = form.publisher.data
        item.language = form.language.data
        item.details = form.details.data

        # add tags to db, if any
        if form.itag.data.strip() is not "":
            itag_str = item.itag_str
            if itag_str:
                itag_str += ',' + form.itag.data
            else:
                itag_str = form.itag.data
            item.itag_str = itag_str 
            item.itag_to_db()

        db.session.add(item)
        db.session.commit()
        
        return redirect(url_for('.item', id=item.id))

    form.uid.data = item.uid 
    form.title.data = item.title 
    form.res_url.data = item.res_url
    form.author.data = item.author  
    form.translator.data = item.translator  
    form.cover.data = item.cover 
    form.cate.data = item.cate  
    form.publisher.data = item.publisher 
    form.language.data = item.language  
    form.details.data = item.details 

    return render_template('edit_item.html', form=form)

##### flag  non-ajax ,using in _show_item_1, post ###
@main.route('/item/flag1/<int:id>',methods=['GET','POST'])
@login_required
def flag_1_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,1)
    return redirect(url_for('.item', id=item.id))
@main.route('/item/flag2/<int:id>',methods=['GET','POST'])
@login_required
def flag_2_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,2)
    return redirect(url_for('.item', id=item.id))
@main.route('/item/flag3/<int:id>',methods=['GET','POST'])
@login_required
def flag_3_item(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,3)
    return redirect(url_for('.item', id=item.id))

##start for flag Ajax #################################################
#################################################################
@main.route('/flag1/<int:id>',methods=['GET'])
#@login_required
def flag_1(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,1)
    return "" 
@main.route('/flag2/<int:id>',methods=['GET'])
#@login_required
def flag_2(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,2)
    return "" 
@main.route('/flag3/<int:id>',methods=['GET'])
#@login_required
def flag_3(id):
    item = Items.query.get_or_404(id)
    current_user.flag(item,3)
    return "" 
###################################################################
###end for flag Ajax####################################################


@main.route('/tips/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_tips(id):

    tip_c = Collect.query.filter_by(id=id).first_or_404()  #collect 's id
    post = Posts.query.get_or_404(tip_c.post_id)

    contribute = post.contributors.filter_by(
        user_id=current_user.id,
        disabled=False
        ).first()
    if current_user != post.creator and contribute is None \
       and post.editable != 'Everyone' :
        abort(403)

    item = Items.query.get_or_404(tip_c.item_id)
    
    form = EditTipsForm()

    if form.validate_on_submit():
        post.ordering(item, form.order.data)
        tip_c.tips = form.tips.data
        db.session.add(tip_c)
        db.session.commit()
    
        return redirect(url_for('.post', id=tip_c.post_id))
    
    form.tips.data = tip_c.tips
    form.order.data = tip_c.order
     
    return render_template('edit_tips.html', 
                           form=form, tip_c=tip_c,
                           post=post, item=item)    

@main.route('/tips/del/<int:id>',methods=['GET','POST'])
@login_required
def del_tips(id):
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


@main.route('/tag/<int:id>',methods=['GET'])
def tagcollect(id):
    # joined query should be here, per the tagname, return the posts
    _query = Tags.query 
    tag = _query.get_or_404(id)

    parent_tags = [t.parent_tag for t in tag.parent_tags.\
                    order_by(db.func.rand()).limit(5)]
    tags = Tags.query.order_by(db.func.rand()).limit(0).all()
    for tg in parent_tags:
        c_tags = [t.child_tag for t in Clan.query.\
                  filter_by(parent_tag_id=tg.id).\
                  order_by(db.func.rand()).limit(5)]
        tags += c_tags

     
    posts = tag.posts
    
    return render_template('tagcollect.html',
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
        
        db.session.commit()
        tag.parent(parent_tag)

        return redirect(url_for('.tagcollect', id=tag.id))
    
    form.tag.data = tag.tag
    form.descript.data = tag.descript
     
    return render_template('edit_tag.html',
                           tag=tag, form=form) 

##start for fav tag Ajax ##################################################
######################################################################
@main.route('/countfav/<int:id>',methods=['GET'])
#@login_required
def countfav(id):
    tag = Tags.query.get_or_404(id)   # tag 's id
    if not current_user.faving(tag):
        current_user.fav(tag)
    else:
        current_user.unfav(tag)

    v = tag.favers.count()
    fv=str(v)

    return fv 
#######################################################################
##end for fav tag Ajax ######################################################


@main.route('/catagory',methods=['GET'])
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
        db.session.commit()
    
    form2 = DeadlineForm()
    if form2.validate_on_submit() and chal_post is not None:
        chal_post.deadline = form2.deadline.data
        db.session.add(chal_post)
        db.session.commit()

    # clips  
    m = 20  # when exeed this to show more
    query_my = current_user.clips.order_by(Clips.timestamp.desc())
    count_my = query_my.count()
    
    myclips =query_my.limit(m)
    
            
    return render_template('challenge.html', 
                            form=form, form2=form2, m=m,
                            myclips=myclips, count_my=count_my,
                            chal_post=chal_post, 
                            items=items, post_chal=post_chal)


@main.route('/myclips/<int:id>',methods=['GET'])
@login_required
def myclips(id):
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

@main.route('/allclips',methods=['GET'])
@login_required
def allclips():
    
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


@main.route('/demands', methods=['GET'])
def demands():
    _query = Demands.query

    page = request.args.get('page', 1, type=int)

    demands_most = _query.order_by(Demands.vote.desc()).limit(50)
    demands_random = _query.order_by(db.func.rand()).limit(50)


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
        
    page = request.args.get('page', 1, type=int)

    pagination = demand.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    tags = Tags.query.order_by(db.func.rand()).limit(20)

    return render_template('demand.html',
                            demand=demand, form=form, tags=tags,
                            pangination=pagination, comments=comments)

    
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
        
        #return redirect(url_for('.demand', id=id))
    page = request.args.get('page', 1, type=int)

    pagination = review.comments.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    tags = Tags.query.order_by(db.func.rand()).limit(20)

    return render_template(
                'review.html',
                review=review, form=form, tags=tags,
                pangination=pagination, comments=comments)


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


@main.route('/delcommt/<int:id>', methods=['GET','POST'])  
@login_required
def del_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id
    user_id = commt.creator.id
    if current_user == commt.creator:
        db.session.delete(commt)
        db.session.commit()

    return redirect(url_for('auth.profile', id=user_id))

## Moderate comments
@main.route('/disablecomment/<int:id>', methods=['GET','POST'])  
@login_required
@permission_required(Permission.MOD_COMMENT)
def disable_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id
    commt.disabled = True
    db.session.add(commt)
    db.session.commit()

    return "Disabled,DONE" #redirect(url_for('.index'))

@main.route('/enablecommt/<int:id>', methods=['GET','POST'])  
@login_required
@permission_required(Permission.MOD_COMMENT)
def enable_comment(id):
    commt = Comments.query.get_or_404(id)   # comment 's id    
    commt.disabled = False
    db.session.add(commt)
    db.session.commit()

    return "Enabled, DONE" #redirect(url_for('.index'))


@main.route('/morecommt/u/<int:id>', methods=['GET','POST'])  
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

@main.route('/morecommt/i/<int:id>', methods=['GET','POST'])  
@login_required
def morecomment_i(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)

    pagination = item.comments.filter(Comments.heading == None).\
                order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['COMMENT_PER_PAGE'],
                    error_out=False
                )
    comments = pagination.items

    return render_template('morecomment_i.html',
                           item=item, comments=comments,
                           pagination=pagination, user=None)

@main.route('/mycommt/i/<int:id>', methods=['GET','POST'])  
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

@main.route('/morecommt/p/<int:id>', methods=['GET','POST'])  
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


@main.route('/morepost/u/<int:id>', methods=['GET','POST'])  
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
                           pagination=pagination, ref="created")


@main.route('/morereview/u/<id>', methods=['GET','POST'])  
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
                           user=user, ref="user")


@main.route('/morereview/i/<id>', methods=['GET','POST'])  
@login_required
def morereview(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)

    pagination = item.reviews.order_by(Comments.timestamp.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    reviews = pagination.items

    return render_template('morereview.html',
                           item=item, reviews=reviews,
                           pagination=pagination, 
                           user=None, ref="Latest")

@main.route('/morehot/i/<id>', methods=['GET','POST'])  
@login_required
def morehot(id):
    item = Items.query.get_or_404(id)   # item 's id 

    page = request.args.get('page', 1, type=int)

    pagination = item.reviews.order_by(Comments.vote.desc()).\
                paginate(
                    page,
                    per_page=current_app.config['POST_PER_PAGE'],
                    error_out=False
                )
    reviews = pagination.items

    return render_template('morereview.html',
                           item=item, reviews=reviews,
                           pagination=pagination, 
                           user=None, ref="Hot")

@main.route('/morestar/u/<id>', methods=['GET','POST'])  
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
                           pagination=pagination, ref="star-ed")

@main.route('/moreschedule/u/<id>', methods=['GET','POST'])  
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
                           pagination=pagination, ref="scheduled")


@main.route('/moredoing/u/<id>', methods=['GET','POST'])  
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
                           pagination=pagination, ref="working on")

@main.route('/moredone/u/<id>', methods=['GET','POST'])  
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
                           pagination=pagination, ref="have done")

## follow and unfollow - non-ajax
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
    return redirect(url_for('auth.profile', id=id))

##start for follow Ajax ##################################################
######################################################################
@main.route('/countfollow/<int:id>',methods=['GET'])
#@login_required
def countfollow(id):
    user = Users.query.get_or_404(id)
    if not current_user.is_following(user):
        current_user.follow(user)
    else:
        current_user.unfollow(user)

    f = user.followers.count()
    fs = str(f)

    return fs 
#######################################################################
##end for follow Ajax ######################################################

@main.route('/followers/<id>')
@login_required
def follower(id):
    user = Users.query.get_or_404(id)   # item 's id 

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
    user = Users.query.get_or_404(id)   # item 's id 

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


@main.route('/alsoreq/<int:id>', methods=['GET'])
@login_required
def alsoreq(id):

    demand = Demands.query.get_or_404(id) # demand's id
    if current_user != demand.requestor:
        demand.vote = demand.vote + 1 
        db.session.add(demand)
        db.session.commit()

    return redirect(url_for('.demands'))

@main.route('/upvote/<int:id>', methods=['GET'])
@login_required
def upvote(id):

    review = Reviews.query.get_or_404(id) # review's id
    if current_user != review.creator:
        review.vote = review.vote + 1 
        db.session.add(review)
        db.session.commit()
    #n = review.vote
    #m = str(n)
    return redirect(url_for('.review',id=id))


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/uid', methods=['GET'])
def random_uid():
    m=round(random.random()*10E8)
    uid = 'RUT'+str(m)
    while Items.query.filter_by(uid=uid).first() is not None:
        uid = 'RUT'+str(round(random.random()*10E8))
    else:
        return uid