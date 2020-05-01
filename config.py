from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'prkaly007'
DB_NAME = 'primecart'

#uncomment bellow line for cloud db
DATABASE = MongoClient('mongodb+srv://prkprime:prkaly007@primecart-uvg6p.gcp.mongodb.net/test?retryWrites=true&w=majority')[DB_NAME]

#uncomment bellow line for local db
#DATABASE = MongoClient()[DB_NAME]

USERS_COLLECTION = DATABASE.Users
PRODUCT_COLLECTION = DATABASE.ProductData

#actual data
PURCHASE_COLLECTION = DATABASE.PurchaseData
#this for checkout purpose
PURCHASE_COLLECTION2 = DATABASE.TempPurchaseData


CARTS_COLLECTION = DATABASE.Carts

DEBUG = True
