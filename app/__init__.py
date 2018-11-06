from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api/')
app.config.from_object('instance.ProductionConfig')

from .handlers import *
