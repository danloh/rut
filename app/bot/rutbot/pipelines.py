# -*- coding: utf-8 -*-

# Define item pipelines
# Don't forget to add your pipeline to the ITEM_PIPELINES setting


from .items import RutItem
from ...models import Items
from ... import db

class RutbotPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, RutItem):
            # check if spidered
            item_query = Items.query
            res_url = item.get('res_url', '')
            pure_url = res_url.split('/ref=')[0]
            lst = item_query.filter(Items.res_url.in_((res_url, pure_url))).all()
            uid = item.get('uid')
            old_item = item_query.filter_by(uid=uid).first() if uid else True
            if not (lst and old_item):
                new_item = Items(
                    uid=uid,
                    title=item.get('title'),
                    res_url=res_url,
                    author=item.get('author', '').strip(),
                    cover=item.get('cover', '').strip(),
                    cate='Book',
                    publisher=item.get('publisher', '').strip(),
                    pub_date=item.get('pub_date', '').strip(),
                    language=item.get('language', '').strip(),
                    binding=item.get('binding', '').strip()
                )
                db.session.add(new_item)
                if item.get('author', '').strip():
                    new_item.author_to_db()
                db.session.commit()
        return item
