from flask import Flask

app = Flask(__name__)
app.config.from_object('instance.ProductionConfig')

from .handlers import *
