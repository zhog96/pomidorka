from flask import Flask
from flask_jsonrpc import JSONRPC
#from authlib.flask.client import OAuth
from flask_oauth import OAuth
import json
from .config2 import *
import boto3
import sys

# Here!
from werkzeug.contrib.cache import MemcachedCache
from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.contrib.profiler import MergeStream

app = Flask(__name__)
app.config.from_object('instance.ProductionConfig')
app.secret_key = 'adfasjfh23437fhufhskjfd'

# Here!
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, open('profiler.log', 'w'), restrictions=[30])

jsonrpc = JSONRPC(app, '/api/')

file = open('../centrifugo/config.json', 'r')
config = json.load(file)
app.centrifugo_secret = config['secret']
file.close()

oauth = OAuth()

# Here!
cache = MemcachedCache(['127.0.0.1'])
cache.clear()

vk = oauth.remote_app('vk',
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    consumer_key=VK_APP_ID,
    consumer_secret=VK_APP_SECRET,
    request_token_params={'scope': 'email'})

from .centrifugo import *
from .handlers import *

