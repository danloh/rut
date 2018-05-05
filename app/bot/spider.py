# -*- coding: utf-8 -*-

import os
import random
import re
import requests
from bs4 import BeautifulSoup as bs
from ..models import Items, Authors, Byline
from .. import db


def random_uid():
    m = round(random.random()*10E8)
    uid = 'RUT'+str(m)
    while Items.query.filter_by(uid=uid).first() is not None:
        uid = 'RUT'+str(round(random.random()*10E8))
    else:
        return uid


def author2str(d):
    authors = d
    if authors:
        lst = [str(k)+str(v) for k, v in authors.items()]
        author_str = ' '.join(lst)
    else:
        author_str = ""
    return author_str


def validUrl(url):
    re_url = r'^https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
    reg_url = re.compile(re_url, 0)
    try:
        return reg_url.match(url)
    except Exception:
        return False


def fakeheader():
    '''
    customize headers
    '''
    agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
              'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
              'Mozilla/5.0 (Windows NT 6.3; Win64, x64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3179.0 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3185.1 Safari/537.36']
    agent = agents[random.randint(0, len(agents)-1)]
    fake_header = {}
    fake_header['User-Agent'] = agent
    return fake_header


def get_html(url):
    try:
        r = requests.get(url, headers=fakeheader(), timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        return None


def get_soup(url):
    html = get_html(url)
    if html:
        try:
            soup = bs(html, 'lxml')
            return soup
        except Exception:
            return None
    else:
        return None


def down_img(imgUrl, filename):
    # img_dir = '/Users/oo/Project/flasking/app/static/img/'
    img_dir = os.path.join(os.getcwd(), 'app/static/img/')
    if validUrl(imgUrl):
        with open(img_dir+filename+'.jpg', 'wb+') as f:
            f.write(
                requests.get(
                    imgUrl,
                    headers=fakeheader(),
                    timeout=30,
                    stream=True
                ).content
            )
    else:
        pass


def parse_html_amazon(url):
    soup = get_soup(url)
    # init a dict to store info
    d = {}
    d['resUrl'] = url.split('/ref=')[0]  # discard the ref part in amazon url
    if not soup:
        return d

    # get title then get info
    titleTag = soup.find('h1', id='title')
    try:
        tg = titleTag.select('span')
    except Exception:
        tg = []
    tg = tg + ['','','']
    d['title'] = tg[0].text.strip()
    # d['bind'] = tg[1].get_text(strip=True)
    d['PublishDate'] = tg[2].text.strip()

    # get authors
    bylineTag = soup.find('div', id='bylineInfo')
    try:
        authorTag = bylineTag.find_all(
            'span',
            attrs={'class': 'author'}
        )
    except Exception:
        authorTag = []
    d_authors = {}
    for author in authorTag:
        try:
            name = author.find(
                'a',
                class_='a-link-normal',
                string=re.compile(r'^(?!(Visit|search|Learn)).*$', re.I)
            ).text.strip()
            role = author.find(
                'span',
                class_='contribution'
            ).text.strip()
        except Exception:
            name = None
        else:
            d_authors[name] = role

    d['authors'] = d_authors

    # get binding and price
    swatchSect = soup.find('li', class_='swatchElement selected')
    try:
        selected = swatchSect.find('a').find_all('span')
        binding = selected[0].text.strip()
        price = selected[1].text.strip()
    except Exception:
        binding = d.get('bind')
        price = ''
    d['binding'] = binding
    d['price'] = price

    # get detail info :ISBN, Publisher, Language, etc
    detailTable = soup.find(
        'table',
        id='productDetailsTable'
    )
    try:
        detailList = detailTable.find_all('li')
    except Exception:
        detailList = []
    for detail in detailList:
        lst = detail.get_text(strip=True).split(':')+[""]
        key = lst[0].strip()
        val = lst[1].strip()
        d[key] = val
    #get page
    bd = d.get('binding', '')
    d['page'] = d.get(bd, '')

    # get about
    aboutSection = soup.find('div', id='iframeContent')
    try:
        about = aboutSection.get_text()
    except Exception:
        about = ""
    d['details'] = about

    # get img url

    # imgTag = soup.find(
    #     'div',
    #     attrs={'id':'img-canvas'}
    # )

    front = soup.find(
        'img',
        id=re.compile(r'mgBlkFront')
    )
    try:
        # front_img_url = front.get('src')  # why src value is not url but data??
        img_d = front['data-a-dynamic-image']
        front_img_url = 'https:' + img_d.split(':')[1].split('"')[0]
    except Exception:
        front_img_url = ""
    d['cover'] = front_img_url

    # back img url, why attr['src'] value is not url_string but data??
    # back = imgTag.find(
    #     'img',
    #     attrs={'id':'imgBlkBack'}
    # )
    # back_img_url = back['src']
    # d['back'] = back_img_url

    # uid
    asin = d.get('ASIN')
    isbn10 = d.get('ISBN-10')
    isbn13 = d.get('ISBN-13')
    uid = isbn13 or isbn10 or asin or random_uid()
    d['uid'] = uid.replace('-', '').replace(' ', '')
    return d


def parse_html_edx(url):
    soup = get_soup(url)

    # init a dict to store info
    d = {}
    d['resUrl'] = url
    d['Publisher'] = 'edX'
    d['cate'] = 'Online'
    if not soup:
        return d

    # get title
    try:
        title = soup.select_one('head > title').text.strip()
    except Exception:
        title = ""
    d['title'] = title

    # get instructors  - about
    aboutArea = soup.select_one('#course-about-area')
    try:
        staffList = aboutArea.find('ul')
        instructorsList = staffList.find_all('li')
    except Exception:
        instructorsList = []
    d_instructor = {}
    for instructor in instructorsList:
        name_p = instructor.find(
            'a > p',
            atrrs={'class': 'instructor-name'}
        )
        if name_p:
            name = name_p.text.strip()
            d_instructor[name] = '(instructor)'
    d['authors'] = d_instructor

    # get about
    try:
        descript = aboutArea.find(
            'div',
            class_='course-description'
        )
        about = descript.find('div').get_text()
    except Exception:
        about = ""
    d['details'] = about

    # get img
    imgArea = soup.find(
        'div',
        attrs={'class': 'course-detail-video'}
    )
    try:
        imgUrl = imgArea.find('a > img').get('src')
    except Exception:
        imgUrl = ""
    cover_img = imgUrl # if validUrl(imgUrl) else ""
    d['cover'] = cover_img
    d['uid'] = random_uid()
    return d


def parse_html_coursera(url):
    soup = get_soup(url)

    # init a dict to store info
    d = {}
    d['resUrl'] = url
    d['Publisher'] = 'coursera'
    d['cate'] = 'Online'
    if not soup:
        return d

    # get title
    try:
        title = soup.select_one('head > title').text.strip()
    except Exception:
        title = ""
    d['title'] = title

    # get instructors
    instructorSection = soup.find('ul', class_='instructors-section')
    try:
        instructorList = instructorSection.find_all('li')
    except Exception:
        instructorList = []
    d_instructor = {}
    for instructor in instructorList:
        nameSetion = instructor.find('p', class_='instructor-name')
        try:
            name_a = nameSetion.find('a')
        except Exception:
            name = None
        else:
            if name_a:
                name = name_a.text.strip()
                d_instructor[name] = '(Instructor)'
    d['authors'] = d_instructor

    # get publisher/ creator insititution
    creatorInfo = soup.select_one('div.rc-CreatorInfo')
    try:
        creatorName = creatorInfo.find(
            'div', class_='creator-names'
        ).get_text()
        creator = creatorName.split(':')[1].strip()
    except Exception:
        creator = 'coursera'
    d['Publisher'] = creator

    # get about
    aboutSection = soup.find('div', class_='about-section-wrapper')
    try:
        about = aboutSection.find(
            'p',
            class_='body-1-text course-description'
        ).text.strip()
    except Exception:
        about = ""
    d['details'] = about

    # get detail info
    infoTable = soup.find('table', class_='basic-info-table')
    try:
        infoTr = infoTable.find_all('tr')
    except Exception:
        infoTr = []
    for info in infoTr:
        try:
            infoTd = info.find_all('td')
            key = infoTd[0].span.text.strip()
            val = infoTd[1].text.strip()
            d[key] = val
        except Exception:
            infoTd = []

    # get img, instructor's pic
    try:
        imgUrl = instructorSection.find('img').get('src')
    except Exception:
        imgUrl = ""
    cover_img = imgUrl if validUrl(imgUrl) else ""
    d['cover'] = cover_img
    d['uid'] = random_uid()
    return d


def parse_html_other(url):
    soup = get_soup(url)

    # init a dict to store info
    d = {}
    d['resUrl'] = url
    d['cate'] = 'Online'
    if not soup:
        return d

    # get title
    try:
        title = soup.select_one('head > title').text.strip()
    except Exception:
        title = ""
    d['title'] = title

    # get img by blind search
    try:
        imgUrl = soup.body.find('img').get('src')
    except Exception:
        imgUrl = ""
    cover_img = imgUrl if validUrl(imgUrl) else ""
    d['cover'] = cover_img
    d['uid'] = random_uid()
    return d


def parse_html(url):
    re_amazon = re.compile(r'^https?://(www\.)?(amazon){1}(.*)', 0)
    re_edx = re.compile(r'^https?://(www\.)?(edx){1}(.*)', 0)
    re_coursera = re.compile(r'^https?://(www\.)?(coursera){1}(.*)', 0)

    if re_amazon.match(url):
        d = parse_html_amazon(url)
    elif re_edx.match(url):
        d = parse_html_edx(url)
    elif re_coursera.match(url):
        d = parse_html_coursera(url)
    else:
        d = parse_html_other(url)

    author_str = author2str(d.get('authors'))
    d['byline'] = author_str

    # #download img
    # cover_img = d.get('cover', '')
    # uid = d.get('uid')
    # if cover_img:
    #     filename = str(uid)
    #     try:
    #         down_img(cover_img,filename)
    #     except Exception:
    #         pass

    return d


def parse_and_store(d=None, url=''):
    d = d or parse_html(url)
    try:
        title = d['title']
        uid = d['uid']
    except Exception:
        return 'Something Wrong'
    else:
        # store or update item
        uid = uid.replace('-', '').replace(' ', '') if uid else None
        item = Items.query.filter_by(uid=uid).first()
        if item is None:
            item = Items(
                title=title,
                uid=uid,
                author=d.get('byline'),
                cover=d.get('cover'),
                res_url=d.get('resUrl'),
                publisher=d.get('Publisher'),
                pub_date=d.get('publish_date'),
                language=d.get('Language'),
                details=d.get('details'),
                page=d.get('Paperback') or d.get('Hardcover'),
                level=d.get('Level')
            )
        else:
            item.author = d.get('byline')
            item.cover = d.get('cover')
            item.res_url = d.get('resUrl')
            item.publisher = d.get('Publisher')
            item.pub_date = d.get('publish_date')
            item.language = d.get('Language')
            item.details = d.get('details')
            item.page = d.get('Paperback') or d.get('Hardcover')
            item.level = d.get('Level')

        db.session.add(item)

        # store authors and update byline
        authors = d.get('authors')
        a_query = Authors.query
        b_query = Byline.query
        for name, contribution in authors.items():
            author = a_query.filter_by(name=name).first()
            if author is None:
                author = Authors(name=name)
                db.session.add(author)

            byline = b_query.filter_by(
                item=item,
                by=author)
            if byline is None:
                byline = Byline(
                    item=item,
                    by=author,
                    contribution=contribution
                )
                db.session.add(byline)

        db.session.commit()


# for debug case
def start():
    url = 'https://www.amazon.com/Art-War-AmazonClassics-Sun-Tzu/dp/1542047528/'
    # get_html(url)
    parse_html(url)


if __name__ == "__main__":
    start()
