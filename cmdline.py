import os
from time import sleep

from scrapy import cmdline

spider_name = os.sys.argv[1]
cmdline.execute(('scrapy crawl test -a spider_name=%s' % spider_name).split())
sleep(1)
