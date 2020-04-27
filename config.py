from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'prkaly007'
DB_NAME = 'primecart'

DATABASE = MongoClient('mongodb+srv://prkprime:prkaly007@primecart-uvg6p.gcp.mongodb.net/test?retryWrites=true&w=majority')[DB_NAME]
USERS_COLLECTION = DATABASE.Users
PRODUCT_COLLECTION = DATABASE.ProductData
PURCHASE_COLLECTION = DATABASE.PurchaseData

DEBUG = True
