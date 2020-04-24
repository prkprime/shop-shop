import redis
from os import environ

class Config:
    SECRET_KEY = 'bda'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = 'redis://:'
