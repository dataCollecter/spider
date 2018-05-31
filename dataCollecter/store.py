from pymongo import MongoClient

client = MongoClient('localhost', 27017)
datacollecter = client.spider
follow_path = datacollecter.follow_path
lastest_data = datacollecter.LastData
data = datacollecter.Data
spider = datacollecter.Spider
mail = datacollecter.Mail
