# -*- coding: utf-8 -*-
# article: news for reader

from flask import request, g, jsonify, abort
from ..models import Articles, Avote, Comments, Items
from . import db, rest, auth, PER_PAGE


@rest.route('/articles', methods=['GET'])
def get_articles():
    # get request args
    userid = request.args.get('userid', type=int)
    itemid = request.args.get('itemid', type=int)
    ref = request.args.get('ref', '')
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    # yield query per filter criteria
    query = Articles.query
    if userid and itemid:
        articles_query = query.filter_by(submitor_id=userid, item_id=itemid)
    elif userid:
        articles_query = query.filter_by(submitor_id=userid)
    elif itemid:
        articles_query = query.filter_by(item_id=itemid)
    else:
        articles_query = query
    # order per point or timestamp
    if ref == 'top':
        articles = articles_query.order_by(Articles.point.desc())
    else:
        articles = articles_query
    # pagination then result
    hs_list = articles.order_by(Articles.timestamp.desc(), Articles.score.desc())\
                  .offset(per_page * page).limit(per_page)
    articles_dict = {
        'articles': [h.to_dict() for h in hs_list],
        'total': articles.count()
    }
    return jsonify(articles_dict)


@rest.route('/articles/<int:articleid>', methods=['GET'])
# @auth.login_required
def get_article(articleid):
    article = Articles.query.get_or_404(articleid)
    article_dict = article.to_dict()
    return jsonify(article_dict)


@rest.route('/articles/<int:articleid>/comments', methods=['GET'])
# @auth.login_required
def get_article_comments(articleid):
    article = Articles.query.get_or_404(articleid)
    # article_dict = article.to_dict()
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    comments_query = article.comments
    h_comments = comments_query\
            .order_by(Comments.vote.desc(), Comments.timestamp.desc())\
            .offset(page*per_page).limit(per_page)
    comments = [c.to_dict() for c in h_comments]
    comments_dict = {
        'comments': comments,
        'commentcount': comments_query.count()
    }
    return jsonify(comments_dict)


@rest.route('/articles/<int:articleid>/voters', methods=['GET'])
@auth.login_required
def get_article_voters(articleid):
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    query = Avote.query.filter_by(article_id=articleid)
    voters = query.offset(page * per_page).limit(per_page)
    voters_dict = {
        'voters': [v.voter.to_simple_dict() for v in voters],
        'votecount': query.count()
    }
    return jsonify(voters_dict)


@rest.route('/articles', methods=['POST'])
@auth.login_required
def new_article():
    title = request.json.get('title', '').strip()
    if not title:
        abort(403)
    url = request.json.get('url', '').strip()
    if url:
        exist = Articles.query.filter_by(url=url).first()
        if exist:
            return jsonify(exist.to_dict())
    content = request.json.get('content', '').strip()
    if not (url or content):
        abort(403)
    # att to item
    itemid = request.json.get('itemid', 0)
    item = Items.query.get_or_404(itemid) if itemid else None
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    user = g.user
    article = Articles(
        submitor=user,
        title=title,
        url=url,
        content=content,
        spoiler=spoiler,
        item=item,
    )
    db.session.add(article)
    db.session.commit()
    # record activity as submit a article
    from task.tasks import set_event_celery
    set_event_celery.delay(user.id, action='Submitted', articleid=article.id)
    return jsonify(article.to_dict())


@rest.route('/articles/<int:articleid>', methods=['PUT'])
@auth.login_required
def edit_article(articleid):
    title = request.json.get('title', '').strip()
    if not title:
        abort(403)
    content = request.json.get('content', '').strip()
    url = request.json.get('url', '').strip()
    if not (content or url):
        abort(403)
    article = Articles.query.get_or_404(articleid)
    user = g.user
    if user != article.submitor and user.role.duty != 'Admin':
        abort(403)  # No Permission
    article.title = title
    article.url = url
    article.content = content
    spoiler_text = request.json.get('spoiler')
    spoiler = True if spoiler_text == 'Spoiler Ahead' else False
    article.spoiler = spoiler
    db.session.add(article)
    db.session.commit()
    article_dict = article.to_dict()
    return jsonify(article_dict)


@rest.route('/articles/<int:articleid>/voters', methods=['PATCH'])
@auth.login_required
def upvote_article(articleid):
    article = Articles.query.get_or_404(articleid)  # article's id
    user = g.user
    voted = Avote.query.filter_by(user_id=user.id, article_id=articleid).first()
    if voted is None:
        article.vote = article.vote + 1
        db.session.add(article)
        avote = Avote(
            voter=user,
            vote_article=article
        )
        db.session.add(avote)
        db.session.commit()
        # record activity as upvote a article
        # user.set_event(action='Push', articleid=article.id)
        # article.cal_point() # to be in task queue
    # return jsonify(article.vote)
    return jsonify(article.vote)


@rest.route('/articles/<int:articleid>', methods=['DELETE'])
@auth.login_required
def del_article(articleid):
    article = Articles.query.get_or_404(articleid)
    user = g.user
    if article.submitor != user and user.role.duty != 'Admin':
        abort(403)
    db.session.delete(article)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/articles/<int:articleid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_or_enable_article(articleid):
    article = Articles.query.get_or_404(articleid)
    user = g.user
    if article.submitor != user and user.role.duty != 'Admin':
        abort(403)
    dis_or_enb = request.json.get('disbaled', True)
    article.disabled = dis_or_enb
    db.session.add(article)
    db.session.commit()
    return jsonify(article.disabled)
