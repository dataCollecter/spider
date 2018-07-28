"""@author jessfx;@desc 通用爬虫;@data 2018/07/26."""
import re
from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from ..items import DataCollecterItem
from ..store import *


class Spider0(Spider):
    """@author jessfx."""

    name = 'test'
    custom_settings = {
        # 渲染服务的url
        'SPLASH_URL': 'http://39.105.9.158:8050',

        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重过滤器
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 使用Splash的Http缓存
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    }

    def __init__(self, spider_name):
        """Init."""
        self.path_all = []
        self.path_tot = []
        self.path_a = []
        self.path_date = []
        self.spider_name = spider_name
        self.retry = 3

    def start_requests(self):
        """Crawl control."""
        if len(list(spider.find({'spider_name': self.spider_name}))) != 0:
            # 找不到记录则需要爬取历史数据
            if len(list(follow_path.find(
                    {'spider_name': self.spider_name}))) == 0:
                self.json = spider.find(
                    {'spider_name': self.spider_name})[0]
                yield Request('http://39.105.9.158:8050/render.html?url=' + self.json['url'], callback=self.parse0, dont_filter=True)
                sleep(3)
                meta = {'timing': False}
                self.logger.info("timing:" + str(meta['timing']))
                yield Request('http://39.105.9.158:8050/render.html?url=' + self.json['url'], callback=self.parse1, meta=meta, dont_filter=True)
            else:  # 如果找得到path记录说明不是第一次爬，只需要更新最新数据
                json = dict(follow_path.find(
                    {'spider_name': self.spider_name}).next())
                self.path_all = json.get('path_all', [])
                self.path_tot = json.get('path_tot', [])
                self.path_a = json.get('path_a', [])
                self.path_date = json.get('path_date', [])
                meta = {'timing': True}
                self.logger.info("timing:" + str(meta['timing']))
                yield Request('http://39.105.9.158:8050/render.html?url=' + json['url'], callback=self.parse1, meta=meta, dont_filter=True)

    def parse0(self, response):
        """Structure analyze parser."""
        body = re.sub('<script.*>.*</script>', '',
                      response.body.decode('utf-8'))
        body = re.sub('<!--.*-->', '',
                      body)
        body = re.sub('<head>.*</head>', '',
                      body)
        body = re.sub('<thead.*>.*</thead>', '',
                      body)
        body = str(body).replace("<tbody>", "").replace(
            "</tbody>", "").replace("</br>", "").replace("<br>", "")
        self.logger.info("replace tag <thead>, <br>, <script> and <tbody>.")

        soup = BeautifulSoup(body, 'html.parser')
        self.logger.info("beautifulsoup successed.")
        print(soup.find('a', string=re.compile(
            '.*' + self.json['title1'].strip().replace('.', '\\.') + '.*')))
        print(soup.find(string=re.compile(
            '.*' + self.json['title1'].strip().replace('.', '\\.') + '.*')))
        tag_a0 = soup.find('a', string=re.compile(
            '.*' + self.json['title1'].strip().replace('.', '\\.') + '.*'))
        self.logger.info("find first link tag location")

        loc0 = tag_a0
        loc1 = tag_a0.parent
        while loc0.find(string=re.compile('.*' + self.json['date1'].strip().replace('.', '\\.') + '.*')) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_a.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_a.reverse()
        self.logger.info(
            "get path from tot to link tag.\npath:" + str(self.path_a))

        tag_date0 = loc0.find(string=re.compile(
            '.*' + self.json['date1'].strip().replace('.', '\\.') + '.*')).parent
        tag_tot = loc0
        loc0 = tag_date0
        loc1 = loc0.parent
        while loc0 != tag_tot:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_date.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_date.reverse()
        self.logger.info(
            "get path from tot to link tag.\npath:" + str(self.path_date))

        loc0 = tag_tot
        loc1 = loc0.parent
        while loc0.find('a', string=re.compile('.*' + self.json['title2'].strip().replace('.', '\\.') + '.*')) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_tot.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_tot.reverse()
        self.logger.info(
            "get path from all to tot tag.\npath:" + str(self.path_tot))

        tag_all = loc0

        loc0 = tag_all
        loc1 = loc0.parent
        while loc0.name != 'body':
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_all.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_all.reverse()
        self.logger.info(
            "get path from body tag to all tag.\npath:" + str(self.path_all))

        follow_path.update({'spider_name': self.spider_name},
                           {'$set': dict({'spider_name': self.spider_name,
                                          'url': response.url.replace('http://39.105.9.158:8050/render.html?url=', ''),
                                          'path_all': self.path_all,
                                          'path_tot': self.path_tot,
                                          'path_date': self.path_date, 'path_a': self.path_a})},
                           upsert=True)
        self.logger.info("save path infomation to mongodb.")

    def parse1(self, response):
        """Data parser."""
        tot1 = self.path_tot[0]
        self.path_tot.remove(self.path_tot[0])
        body = re.sub('<script.*>.*</script>', '',
                      response.body.decode('utf-8'))
        body = re.sub('<!--.*-->', '',
                      body)
        body = re.sub('<head.*>.*</head>', '',
                      body)
        body = re.sub('<thead.*>.*</thead>', '',
                      body)
        body = str(body).replace("<tbody>", "").replace(
            "</tbody>", "").replace("</br>", "").replace("<br>", "")
        self.logger.info("replace tag <thead>, <br>, <script> and <tbody>.")

        soup = BeautifulSoup(body, 'html.parser')
        self.logger.info("beautifulsoup successed.")

        tag_all = soup.find('body')
        for i in self.path_all:
            try:
                tag_all = tag_all.find_all(i[0], recursive=False)[i[1]]
            except:
                continue
        tag_all = tag_all.find_all(tot1)
        for tot in tag_all:
            item = DataCollecterItem()
            try:
                for i in self.path_tot:
                    try:
                        tot = tot.find_all(i[0], recursive=False)[i[1]]
                    except:
                        continue
                tag_date = tot
                tag_a = tot
                for i in self.path_date:
                    tag_date = tag_date.find_all(i[0], recursive=False)[i[1]]
                date = re.findall('\\d{4}[-\\.\\/]{1}\\d{2}[-\\.\\/]{1}\\d{2}', tag_date.find(
                    string=re.compile('.*\\d{4}[-\\.\\/]{1}\\d{2}[-\\.\\/]{1}\\d{2}.*')).string)[0]
                item['date'] = date.replace("./\\-", "-")
                for i in self.path_a:
                    tag_a = tag_a.find_all(i[0], recursive=False)[i[1]]
                a = urljoin(response.url.replace(
                    'http://39.105.9.158:8050/render.html?url=', ''), tag_a['href'])
                item['url'] = a
                item['title'] = tag_a.get_text().strip()
                item['spider'] = self.spider_name
                yield item
            except Exception as e:
                # print(e)
                continue
        print(soup.find('a', attrs={'href': True},
                        string=re.compile('.*下一页.*')))
        if response.meta['timing'] is False and soup.find('a', attrs={'href': True}, string=re.compile('.*下一页.*')) is not None:
            next_page = urljoin(response.url.replace(
                'http://39.105.9.158:8050/render.html?url=', ''), soup.find('a', string=re.compile('.*下一页.*'))['href'])
            if next_page == response.url.replace('http://39.105.9.158:8050/render.html?url=', ''):
                print(0)
                return
            self.logger.info("next page: " + next_page)
            self.path_tot.reverse()
            self.path_tot.append(tot1)
            self.path_tot.reverse()
            yield Request('http://39.105.9.158:8050/render.html?url=' + next_page, callback=self.parse1, meta=response.meta, dont_filter=True)
            self.retry = 3
        elif self.retry > 0 and response.meta['timing'] is False:
            self.path_tot.reverse()
            self.path_tot.append(tot1)
            self.path_tot.reverse()
            yield Request(response.url, callback=self.parse1, meta=response.meta, dont_filter=True)
            self.retry -= 1
