from pymongo import MongoClient

client = MongoClient('localhost', 27017)
datacollecter = client.datacollecter
follow_path = datacollecter.follow_path
data = datacollecter.Data
spider = datacollecter.Spider
mail = datacollecter.Mail
