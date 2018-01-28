from scrapy import cmdline
from time import sleep

try:
    for i in range(20):
        cmdline.execute('scrapy crawl test'.split())
        sleep(1)
except:
    pass
    pass
