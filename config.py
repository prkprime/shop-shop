from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'prkaly007'
DB_NAME = 'primecart'

DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.users

DEBUG = True
