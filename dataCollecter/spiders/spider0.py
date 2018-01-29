import re
from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from ..items import DataCollecterItem
from ..store import follow_path, spider


class Spider0(Spider):

    name = 'test'

    def __init__(self, spider_name):
        self.path_all = []
        self.path_tot = []
        self.path_a = []
        self.path_date = []
        self.spider_name = spider_name
        # self.json = {'title1': '第27个全国“土地日”优秀组织单位和宣传项目',
        #              'date1': '2018.01.19',
        #              'title2': '调整找矿突破战略行动专家技术指导组组成人员',
        #              'date2': '2018.01.10'}

    def start_requests(self):
        if len(spider.find({'spider_name': self.spider_name})) != 0:
            if len(follow_path.find(
                    {'spider_name': self.spider_name})) == 0:
                self.json = spider.find(
                    {'spider_name': self.spider_name})[0]
                yield Request(self.json['url'], callback=self.parse0, dont_filter=True)
                sleep(3)
            else:
                json = dict(follow_path.find(
                    {'spider_name': self.spider_name}))
                self.path_all = json.get('path_all', [])
                self.path_tot = json.get('path_tot', [])
                self.path_a = json.get('path_a', [])
                self.path_date = json.get('path_date', [])
            yield Request(json['url'], callback=self.parse1)

    def parse0(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag_a0 = soup.find('a', string=self.json['title1'])
        # print(tag_a0)
        # 提供两组数据，查找连结点
        loc0 = tag_a0
        loc1 = tag_a0.parent
        while loc0.find(string=re.compile('.*' + self.json['date1'] + '.*')) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_a.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_a.reverse()
        # print(self.path_a)

        tag_date1 = loc1.find(string=re.compile(
            '.*' + self.json['date1'] + '.*')).parent
        tag_tot = loc0

        loc0 = tag_date1
        loc1 = loc0.parent
        while loc0 != tag_tot:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_date.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_date.reverse()
        # print(self.path_date)

        loc0 = tag_tot
        loc1 = loc0.parent
        while loc0.find('a', string=self.json['title2']) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_tot.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_tot.reverse()
        # print(self.path_tot)

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
        # print(self.path_all)
        follow_path.update({'spider_name': self.spider_name},
                           {'$set': dict({'path_all': self.path_all, 'path_tot': self.path_tot,
                                          'path_date': self.path_date, 'path_a': self.path_a})},
                           upsert=True)

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag_all = soup.find('body')
        for i in self.path_all:
            # print(tag_all.name)
            tag_all = tag_all.find_all(i[0], recursive=False)[i[1]]
        tag_all = tag_all.find_all(self.path_tot[0])
        self.path_tot.remove(self.path_tot[0])
        for tot in tag_all:
            item = DataCollecterItem()
            try:
                for i in self.path_tot:
                    tot = tot.find_all(i[0], recursive=False)[i[1]]
                tag_date = tot
                tag_a = tot
                for i in self.path_date:
                    tag_date = tag_date.find_all(i[0], recursive=False)[i[1]]
                date = re.findall('\\d{4}[-\.\/]{1}\\d{2}[-\.\/]{1}\\d{2}', tag_date.find(
                    string=re.compile('.*\\d{4}[-\.\/]{1}\\d{2}[-\.\/]{1}\\d{2}.*')).string)[0]
                item['date'] = date
                for i in self.path_a:
                    tag_a = tag_a.find_all(i[0], recursive=False)[i[1]]
                a = urljoin(response.url, tag_a['href'])
                item['url'] = a
                item['title'] = tag_a.get_text().strip()
                item['spider_name'] = self.spider_name
            except:
                continue
