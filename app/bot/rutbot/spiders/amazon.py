# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from ..items import RutItem
from ...spider import author2str

class AmazonSpider(Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = []

    def parse(self, response):
        # extract title
        title = response.xpath('//*[@id="ebooksProductTitle"]/text()').extract_first()
        binding = response.xpath('//*[@id="title"]/span[2]/text()').extract_first()
        pub_date = response.xpath('//*[@id="title"]/span[3]/text()').extract_first()
        # extract cover img
        cover_e = response.xpath('//*[@id="ebooksImgBlkFront"]/@src').extract_first()
        cover_p = response.xpath('//*[@id="imgBlkFront"]/@src').extract_first()
        cover = cover_p or cover_e
        # extract author
        author_tags = response.xpath('//*[@id="byline"]/span')
        dict_author = {}
        for e in author_tags:
            name = e.xpath('span[1]/a[1]/text()').extract_first()
            contr = e.xpath('span[2]/span/text()').extract_first()
            dict_author[name] = contr
        author_str = author2str(dict_author)
        # extract detail
        detail_tags = response.xpath('//*[@id="productDetailsTable"]')\
                              .css('li/text()').extract()
        dict_detail = {}
        for dt in detail_tags:
            lst = dt.split(':')+[""]
            key = lst[0].strip()
            val = lst[1].strip()
            dict_detail[key] = val
        uid = dict_detail.get('ISBN-13') or dict_detail.get('ASIN')
        item = RutItem({
            'title': title,
            'uid': uid.replace('-', '').replace(' ', ''),
            'cover': cover,
            'publisher': dict_detail.get('Publisher', ''),
            'pub_date': pub_date,
            'author': author_str,
            'language': dict_detail.get('Language', 'English'),
            'binding': binding,
            'res_url': response.url
        })
        return item
