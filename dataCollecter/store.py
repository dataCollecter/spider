from pymongo import MongoClient

client = MongoClient('39.105.9.158', 27017)
datacollecter = client.spider
follow_path = datacollecter.follow_path
lastest_data = datacollecter.LastData
data = datacollecter.Data
spider = datacollecter.Spider
mail = datacollecter.Mail
