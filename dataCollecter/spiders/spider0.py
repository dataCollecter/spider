import re

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider
from urllib.parse import urljoin
from time import sleep


class Spider0(Spider):

    name = 'test'

    def __init__(self):
        self.path_all = []
        self.path_tot = []
        self.path_a = []
        self.path_date = []
        self.attrs_date = {}
        self.attrs_tot = {}
        self.attrs_all = {}
        self.attrs_all_hasclass = {}
        # self.json = eval(json)
        self.json = {'string0': '第27个全国“土地日”优秀组织单位和宣传项目',
                     'date0': '2018.01.19',
                     'string1': '调整找矿突破战略行动专家技术指导组组成人员',
                     'date1': '2018.01.10'}
        self.urls = []
        fp = open(
            'D:\\workspace\\scrapy spider\\dataCollect\\dataCollect\\test0.txt')
        for line in fp.readlines():
            self.urls.append(line.strip())

    def start_requests(self):
        # for url in self.urls:
        #     yield Request(url, callback=self.parse, dont_filter=True)
        #     yield Request(url, callback=self.parse0)
        url = 'http://www.mlr.gov.cn/zwgk/zytz/'
        yield Request(url, callback=self.parse0, dont_filter=True)
        sleep(3)
        yield Request(url, callback=self.parse1)

    def parse0(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag_a0 = soup.find('a', string=self.json['string0'])
        print(tag_a0)
        # 提供两组数据，查找连结点
        loc0 = tag_a0
        loc1 = tag_a0.parent
        while loc0.find(string=re.compile('.*' + self.json['date0'] + '.*')) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_a.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_a.reverse()
        print(self.path_a)

        tag_date0 = loc1.find(string=re.compile(
            '.*' + self.json['date0'] + '.*')).parent
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
        print(self.path_date)

        loc0 = tag_tot
        loc1 = loc0.parent
        while loc0.find('a', string=self.json['string1']) is None:
            for count, i in enumerate(loc1.find_all(loc0.name, recursive=False)):
                if i == loc0:
                    self.path_tot.append([loc0.name, count])
                    break
            loc0 = loc1
            loc1 = loc1.parent
        self.path_tot.reverse()
        print(self.path_tot)

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
        print(self.path_all)

        

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag_all = soup.find('body')
        for i in self.path_all:
        # print(tag_all.name)
            tag_all = tag_all.find_all(i[0], recursive=False)[i[1]]
        tag_all = tag_all.find_all(self.path_tot[0])
        self.path_tot.remove(self.path_tot[0])
        for tot in tag_all:
            try:
                for i in self.path_tot:
                    tot = tot.find_all(i[0], recursive=False)[i[1]]
                tag_date = tot
                tag_a = tot
                for i in self.path_date:
                    tag_date = tag_date.find_all(i[0], recursive=False)[i[1]]
                date = re.findall('\\d{4}[-\.\/]{1}\\d{2}[-\.\/]{1}\\d{2}', tag_date.find(
                    string=re.compile('.*\\d{4}[-\.\/]{1}\\d{2}[-\.\/]{1}\\d{2}.*')).string)[0]
                print(date, end='    ')
                for i in self.path_a:
                    tag_a = tag_a.find_all(i[0], recursive=False)[i[1]]
                a = urljoin(response.url, tag_a['href'])
                print(tag_a.get_text().strip())
            except:
                continue
